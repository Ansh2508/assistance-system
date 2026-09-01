---
name: velth-gcp-migration
description: The per-domain loop for VELTH's Supabase-to-Cloud-SQL repository-layer migration (Path B). Encodes the recipe from docs/REPOSITORY_LAYER_MIGRATION.md + PART2 HARDENED with researched best practices (strangler-fig / branch-by-abstraction, asyncpg+pgbouncer footguns, Alembic autogen blind spots, testcontainers parity) AND real land-time lessons (guardrail-drop-on-merge, cross-domain raw-SQL drift, docker false-green skip, slug truncation, prod-env upgrade trap). Steps 0-7 build one domain; STEP 8 lands it. WHICH DOMAINS REMAIN IS NOT STATED HERE AND MUST NOT BE INFERRED FROM THIS FILE — see the STATUS WARNING at the top of the body. Load at the start of any migration domain alongside velth-preflight, velth-spec, velth-loop, velth-test-strategy, velth-review, velth-commit-prep. Maker != checker; Cowork never runs git; Anshu commits.
trigger: auto
---

# VELTH GCP Migration Skill (repository layer, Path B)

## ⚠ STATUS WARNING — read before using anything below as current

**This file's METHOD is durable. Its PROGRESS claims are not, and were verifiably
stale once already.** The description previously stated "CP1 (sections/innung/teams)
done; next workspace → project_events → promo → outcomes → vext" — by 2026-08-14 all
of those had long since landed, the repository-layer portion had been merged (Batch 8,
2026-08-04), and the project had moved two phases onward into the Render→Cloud Run
migration. Anyone trusting that line would have re-migrated finished work.

**Before using this skill: confirm the real current phase and remaining domains with
Anshu, or from git directly.** Do not infer them from this file, and do not infer them
from a memory summary either — both age. If you find yourself planning work off a
progress claim written in a skill, that is the failure mode this warning exists for.

Named-person role assignments (who owns which domain) are deliberately NOT recorded
here — they change per batch and were wrong in this file before.

**A git-based data point, dated so it can't be mistaken for a fresh claim later:**
as of 2026-08-26, the 5 most recent commits on `main` are unrelated bug fixes
(catalog Unicode decode retry, an intake dialog fix, alembic-drift/layout test
fixes) with no active migration-domain work visible, and the most recent
migration-tagged commits found (`c90ecf4d feat(migration): finish person A
cutover gates`, `2d80039c fix(migration): close person A gate proofs`) are
phrased as completions, not progress. This is consistent with — not proof of —
the migration being finished. It is exactly the kind of check this warning
already asks for ("confirm ... from git directly"), done once and dated; it is
not a substitute for asking Anshu, and it will itself go stale the moment new
migration work starts.

## WHAT THIS IS (one paragraph)

Path B = decompose Supabase -> Cloud SQL. That makes the app stop speaking
Supabase PostgREST (`sb.table(...)`) and speak portable Postgres through a
SQLAlchemy **repository layer**. This skill is the bounded, repeatable loop for
migrating ONE domain at a time, behind one small PR, with main staying live on
the old path until each PR lands. Authority is
`apps/backend/docs/REPOSITORY_LAYER_MIGRATION.md` + the `employees` reference
domain; this skill ADDS the researched guardrails that the doc does not spell out
and that bit us (or would).

## THE NAMED PATTERN (why the order is the order)

This is **Strangler Fig** at the route boundary + **Branch by Abstraction** in
the code (Fowler; AWS Prescriptive Guidance; Azure Architecture Center; Microsoft
resilient-coding-patterns). The repository is the abstraction; old (Supabase) and
new (SQLAlchemy) coexist behind it; callers move one domain at a time; the old
path is deletable only when the last caller is migrated.

Five rules fall straight out of the pattern, and they are LOAD-BEARING:

1. **Start with the easiest slice, not the most important.** "Migrate the data
   layer" as a horizontal cut never finishes; vertical domain slices do
   (Kinney; AWS). => `sections` first, `vault_extract` LAST.
2. **Each slice ships independently with a rollback path.** Small PR per domain;
   until merged, main uses the old Supabase code unchanged. AWS: "each refactored
   service needs a rollback plan."
3. **The adapter is temporary, not the destination.** The `.storage` seam and any
   translation shim are migration tools; if they become permanent you didn't
   finish (Kinney). Document them as debt, don't enshrine them.
4. **Verify new against old before new is authoritative.** Highest-confidence
   strategy is parallel-run / shadow-compare (codelit; Azure "shadow writes and
   validation"). Our cheaper equivalent: `alembic check` proves schema parity, and
   the integration test proves behaviour parity, BEFORE the route flips.
5. **Be honest about decomposition.** If every feature reads the same central
   tables, isolation evaporates (Rangani; TechTarget). => the shared
   `vault_companies`/`profiles` tables are Person A's FIRST job and a hard
   dependency gate for any domain that touches them.

## THE PER-DOMAIN LOOP (run start to finish, every domain)

```
0. PRE-FLIGHT + EXPLORE (read-only)   velth-preflight + velth-spec. RADAR (branch+HEAD).
                                       Reflect the LIVE schema. Audit the route. Output a
                                       PLAN and STOP for Anshu. NO code yet.
1. ORM MODEL                           core/db/models/<domain>.py mirrors the reflection EXACTLY.
2. FIDELITY GATE (the safety net)      alembic autogenerate => MUST be empty; alembic check =>
                                       "No new upgrade operations detected". Against REAL Supabase.
3. DATACLASSES + REPOSITORY            core/<domain>/{models,repository}.py. Ownership in-txn.
4. ROUTE REWRITE (the flip)            api/routes/<domain>.py: repo calls replace sb.table().
                                       No supabase/sqlalchemy imports left on DB paths.
5. INTEGRATION TESTS (parity proof)    tests/integration/test_<domain>_repository.py @pytest.mark.docker.
                                       Every read + write. Runs on real Postgres via testcontainers.
6. GUARDRAIL                           Add paths to MIGRATED in scripts/guardrail_no_supabase.py.
7. VERIFY + HANDOFF                    ruff -> autogen(empty) -> alembic check -> pytest -m docker.
                                       All green -> velth-commit-prep emits git block. Anshu commits.
```

Steps 0 and 2 are where main is protected. Do not skip either, ever.

## STEP 0 — EXPLORE (read-only). The reflection is ground truth.

**Reflect from the live DB, never infer from route code.** Use `pg_catalog` for
FKs (`information_schema` misses them — doc footgun, confirmed). Capture columns,
types, nullability, server defaults, PK, every FK, every index INCLUDING partial
predicates. The reflection script pattern (asyncpg + statement_cache_size=0):

```python
url = os.environ["DATABASE_DIRECT_URL"]            # 5432 session pooler, NOT 6543
url = url.replace("postgresql://","postgresql+asyncpg://")
eng = create_async_engine(url, connect_args={"statement_cache_size": 0})
# columns: information_schema.columns ; PK + FK + indexes: pg_catalog / pg_indexes
```

**Existence gate FIRST.** `SELECT to_regclass('public.<table>')`. If NULL, the
table does not exist — STOP and pick another domain (this killed `outcomes`:
`gbu_outcomes` was never created, the feature silently no-ops). Migrating a
phantom table is impossible.

**Route audit — enumerate with line numbers:** every `sb.table("...").<op>`
(-> proposed repo method+signature), every `.storage.*` call, every embedded
PostgREST join (`select("*, child(*)")`), every timestamp the route passes as a
string, every inline ownership filter (`.eq("user_id", ...)`).

Output the plan; STOP for Anshu. Plan-then-build is the single biggest quality
lever (Anthropic Claude Code best practices; velth-spec).

## STEP 1 — ORM MODEL. Fidelity is binary.

Copy `core/db/models/employee.py`. Auto-discovers — NEVER edit
`core/db/models/__init__.py`. Mirror the reflection exactly:

- **uuid PK** `gen_random_uuid()` -> `server_default=text("gen_random_uuid()")`.
- **timestamptz** -> `DateTime(timezone=True)`, `server_default=text("now()")`
  (or `func.now()` — match what employees uses so autogen sees no diff).
- **bigint** -> `BigInteger` (NOT Integer — silent truncation risk at >2^31).
- **text** -> `Text`. **Even if it holds an id.** See "user_id is TEXT" below.
- **server defaults** (`'general'::text`, `false`, etc.) -> `server_default=text(...)`
  with the EXACT cast string, or autogen reports drift.
- **FK** -> `ForeignKey("<table>.<col>", name="<exact_constraint_name>")`, with
  `ondelete=` ONLY if the DB has it (mirror NO ACTION = omit). Wrong ondelete =
  schema drift = failed `alembic check`.
- **partial indexes** -> `Index("name","col", postgresql_where=text("<predicate>"))`.
  Missing the predicate = drift.
- **EXCLUDE `auth.users` FKs.** They will not exist on Cloud SQL. Keep the column
  as a plain UUID/Text with no FK. (Doc footgun; confirmed pattern in employees.)

## STEP 2 — FIDELITY GATE. This is the parity proof, run vs REAL Supabase.

```bash
cd C:\Users\redmi\velth\apps\backend
uv run --no-sync alembic revision --autogenerate -m "<domain> domain"   # EXPECT: empty body
uv run --no-sync alembic check                                          # EXPECT: No new upgrade operations detected
```

`alembic check` = "does my ORM match the live table?" Clean => yes. This is what
prevents shipping a wrong model to main, and it needs ZERO Docker (it talks to
Supabase via `DATABASE_DIRECT_URL`). Rewrite the autogen output as a `create_table`
baseline (mirror an existing migration), then `alembic stamp head`.

**KNOW AUTOGEN'S BLIND SPOTS** (botmonster; Alembic docs). Autogen does NOT catch,
so the human must eyeball:
- table/column RENAMES (sees drop+add — data loss risk),
- CHECK constraint changes,
- server-default changes on EXISTING columns,
- ENUM type changes.
For a fresh `create_table` baseline matching a reflected table these rarely bite,
but if `alembic check` is clean yet something feels off, suspect one of these and
diff the generated DDL against the reflection by hand.

**Multiple heads:** if Person A also cut a revision off the same base you'll get
two heads. `alembic heads` should show exactly one before deploy; reconcile with
`alembic merge heads` (harmless, just must be done). At a multi-domain land you
can get THREE+ heads (one per domain baseline, all forking the same base) —
`alembic merge heads` collapses all of them into one merge-rev in a single call.

**Alembic TRUNCATES the merge-rev slug** — `-m "merge sections innung teams heads
on mig base"` generated `312c2a293493_merge_sections_innung_teams_heads_on_.py`
(dropped `mig_base`). A glob `git add *_..._mig_base.py` on the name you *expected*
silently matches nothing. ALWAYS stage merge-revs by the ACTUAL filename from
`git status`, never a predicted glob. An unstaged merge-rev = the pushed branch
still has N heads = the next person's `alembic upgrade` breaks.

**NEVER run bare `alembic upgrade head` locally.** `.env`'s `DATABASE_URL` /
`DATABASE_DIRECT_URL` point at PRODUCTION Supabase (`aws-1-...pooler.supabase.com`).
Bare `alembic upgrade head` therefore runs migrations against PROD — it will throw
`DuplicateTableError: relation "<t>" already exists` because prod already has the
table, and it's pure luck (transactional DDL rollback) that it doesn't corrupt.
Testcontainers is the ONLY safe path to exercise `upgrade head` — it overrides the
URL with a fresh ephemeral container. `alembic check` / `upgrade head` against the
prod-pointed local env is MEANINGLESS; the testcontainers integration run is the
authoritative "migrations apply cleanly from empty" proof. (Burned a full debug
loop on this — the "target database is not up to date" was prod being mid-state,
not a real schema problem.)

## STEP 3 — REPOSITORY. Ownership lives in the transaction.

Copy `core/employees/repository.py`. `<Domain>Repository(BaseRepository[...])`;
every method opens its own `session_scope()`; ownership checks (`WHERE id AND
user_id`) run INSIDE the mutation's transaction, not as a separate read. Map
ORM->dataclass with a small `_to_*()` helper; the route/repo boundary never
imports SQLAlchemy.

### THREE footguns that are CODE-LEVEL, not schema-level:

1. **`user_id` (and section_key/project_id) is TEXT, not UUID.** VELTH user ids
   are `anon-<hash>` or JWT strings. NEVER wrap them in `uuid.UUID()` — it crashes
   on anon users. Only `id` and real uuid FK columns convert to UUID. This is the
   main divergence from `employees` and the easiest catastrophic mistake.

2. **Timestamps arrive as ISO STRINGS; asyncpg rejects str for timestamptz.**
   (asyncpg FAQ; doc lesson #3.) The repo must parse `datetime.fromisoformat(x)
   if isinstance(x, str) else x` before binding any timestamptz param. A route may
   send a string on create and a `datetime` on update — handle both.

3. **PostgREST embedded join -> explicit SQLAlchemy LEFT JOIN.** `select("*,
   child(*)")` becomes a LEFT OUTER JOIN grouped per parent. It MUST be LEFT, not
   INNER, or parents with zero children silently vanish (classic bug). Add an
   explicit test for the empty-children case.

4. **Cross-domain raw SQL against an UNMIGRATED table silently drifts from the
   real schema — and passes tests in isolation.** If your repo issues raw SQL
   (`text(...)`) against a table another domain still owns, you are guessing its
   columns from route code, and the guess can be WRONG while everything looks
   green. This bit innung hard: `compute_overdue_rollup` queried
   `project_checklist_items.completed = false`, but that table has NO `completed`
   column — completion is `status` (`'done'`/`'verified'`). It failed SOFT in prod
   (route try/excepts -> overdue always 0, no error) and only surfaced when the
   merge brought the REAL projects migration onto the branch. RULE: before writing
   any raw SQL against a table you don't own, open its actual migration/model and
   read the real column names + types. Don't trust the route's assumptions. Prefer
   NOT reaching into another domain's table at all — if you must, the correct
   predicate for checklist completion is `status NOT IN ('done','verified')`.

## STEP 4 — ROUTE REWRITE. Branch by Abstraction, cleanly.

Module-level `_repo = <Domain>Repository()`; each handler `await _repo.method(...)`;
map dataclass -> Pydantic. End state: zero `sb.table`/`.rpc`/`supabase`/`sqlalchemy`
tokens on the DB paths.

**The `.storage` seam (out of scope = Phase 4/GCS):** Supabase Storage uploads do
NOT migrate now. Per rule 3 (adapter is temporary): EXTRACT storage I/O into a
module OUTSIDE `MIGRATED` (e.g. `core/storage/<domain>_storage.py`) that keeps
using Supabase storage until Phase 4; the repository handles the ROW (incl. the
url STRING columns), storage stays behind its own seam. Prefer extraction over a
guardrail allowlist — the allowlist edits the shared guardrail (Biray's file) and
weakens the check. **Delete any dead/commented `.storage` lines** — the guardrail
regex is LINE-BASED and matches comments too.

**Opportunistic security fixes belong here, FLAGGED.** If the audit finds an
ownership hole (e.g. a delete scoped by `id` only, not `id AND user_id` — an IDOR),
tighten it to an atomic `WHERE id AND user_id` in the repo. This is a behaviour
change from current prod, however small — call it out explicitly in the PR
description so it reads as intentional, not accidental (velth-review).

## STEP 5 — INTEGRATION TESTS. Real Postgres, not a mock, not SQLite.

`tests/integration/test_<domain>_repository.py`, `@pytest.mark.docker`, reuse the
`tests/integration/conftest.py` fixtures (USE them; do NOT edit conftest —
shared-file rule, Biray owns it). The container is a real Postgres built from the
migrations (testcontainers). SQLite is NOT a valid proxy — DDL, type system, and
locking differ (botmonster; reflectoring). This is the behaviour-parity half of
rule 4, and it's a MERGE GATE (doc §8) so nothing untested reaches main.

Cover EVERY read and write the route does, plus the failure modes:
- create + get (hit AND miss/unknown-id returns None, not crash),
- list with user isolation + every filter + ordering,
- the embedded-join method returns parent with **empty children list** when none,
- update owned vs foreign (foreign -> None/false, never touches the row),
- delete owned vs foreign,
- FK violation when a child points at a missing parent (mirror NO ACTION),
- timestamp passed as ISO STRING round-trips (lesson #3),
- BigInteger column round-trips a value > 2^31,
- TEXT user_id works for BOTH `anon-...` and uuid-style strings.

Docker daemon must be up (Anshu's host; Cowork uses its own sandbox and does NOT
run these). If Docker is absent the marker SKIPS (doesn't fail) — but it cannot
merge unskipped, so the gate holds.

**THE FALSE-GREEN TRAP — `-m docker` skips SILENTLY when Docker is down.** The
output `sssssssss ... 61 skipped in 1.24s` reads like success at a glance but is
NOT a pass — it's 61 tests that never ran. `.....` (dots) = passed; `sssss` =
skipped. ALWAYS confirm the literal word "**passed**" and a realistic duration
(~30s for 61 tests, not ~1s), and run `docker ps` FIRST — it must return the
table header (`CONTAINER ID  IMAGE ...`), not a pipe/500 error, before you trust
any `-m docker` run. Docker Desktop on this host idle-stops constantly and takes
2-4 min to boot from cold (pipe-not-found -> 500 -> ready); a stuck 500 past ~4
min needs a full quit-from-tray + relaunch, or a reboot. Never accept a skipped
run as verification of anything.

**Test stubs for still-unmigrated tables HIDE the cross-domain drift above.** If
a test creates its own stub of another domain's table (with the columns you
*assumed*), the stub matches the wrong assumption and the test passes — nothing
catches the mismatch until the real migration lands. Two consequences:
(a) once the real table's migration is on the branch, DROP the stub and point the
test at the real migrated table; (b) `CREATE TABLE IF NOT EXISTS <stub>` NO-OPS
against a table a real migration already created, so your INSERTs hit the REAL
table and fail on ITS NOT NULL columns — match the real schema, don't assume the
stub won. Post-merge, re-run the full suite specifically to shake out stubs that
silently became no-ops.

## STEP 6 — GUARDRAIL

Add `"api/routes/<domain>.py"` and `"core/<domain>/**/*.py"` to `MIGRATED` in
`scripts/guardrail_no_supabase.py`. Do NOT add `core/storage/**`. The scan forbids
`.table(` / `.rpc(` / `.storage` / `get_sb(` / supabase client getters; confirm
the migrated files are clean of all of them (incl. comments). Adding to MIGRATED
is the only edit you make to that file — never weaken the FORBIDDEN list.

**A git merge (esp. `ort` auto-resolve) can SILENTLY DROP a domain's MIGRATED
entries.** When you land multiple domain branches into the integration branch, the
merge resolves the shared guardrail file — and if a domain branch never added
ITSELF to MIGRATED (or the auto-merge picks the wrong side of that hunk), the
domain lands UNGUARDED with zero warning: the guardrail still passes because it's
simply not checking those files. This is exactly how `teams` landed unguarded —
its branch never added `api/routes/teams.py` / `core/teams/**` to MIGRATED, and
nothing flagged it. THE TELL: the migrated-file COUNT didn't move (was 23, stayed
23 after landing a domain that should have added files). ALWAYS, after any land or
merge:
```bash
git show <branch>:apps/backend/scripts/guardrail_no_supabase.py | Select-String "<domain>"
```
Confirm each landed domain's paths are actually present in MIGRATED on the branch,
and that the count increased by the expected number (teams: 23 -> 27 once fixed).
A clean guardrail run means NOTHING if the files aren't in the list.

(Note: teams' *core* has no Supabase calls anyway — the shared teams/team_members
writes live in billing/claim_service, correctly excluded — so the guardrail didn't
FAIL, which is precisely why the gap was invisible. Verify presence, not just pass.)

## STEP 7 — VERIFY + HANDOFF (the external ground truth; velth-loop)

```bash
cd C:\Users\redmi\velth\apps\backend
uv run --no-sync ruff check core/db/models/<domain>.py core/<domain>/ api/routes/<domain>.py tests/integration/test_<domain>_repository.py
uv run --no-sync alembic revision --autogenerate -m "<domain> domain"   # EXPECT empty
uv run --no-sync alembic check                                          # EXPECT clean
uv run --no-sync pytest tests/integration/test_<domain>_repository.py -m docker -q
```

All green -> velth-commit-prep emits the explicit `git add <exact paths>` +
commit block. **Cowork never runs git. Anshu reads the diff and commits.**

## STEP 8 — LAND onto the shared branch (the integration step STEP 7 doesn't cover)

STEP 7 gets ONE domain gate-green on its own branch. Getting it onto the shared
`mig/repo-migration` (where everyone stacks) is a separate, higher-risk step —
it's where this session's bugs clustered. All of STEP 8 is IRREVERSIBLE-adjacent
(pushes to a branch teammates build on), so it's a hard checkpoint: verify, then
ONE confirmation before the push.

**8a. Sync main into your feature branch FIRST, then merge — Biray's rule.**
Before landing, bring `main` into your branch so conflicts surface on YOUR branch,
not at integration. `git merge origin/main` on the feature branch, resolve there,
re-run STEP 7 green, THEN land. Landing first and eating main's conflicts at the
integration branch is how you end up resolving a shared-branch conflict blind in
the GitHub web editor (never do that — no tests, commits straight to shared).

**8b. Collapse heads by ACTUAL filename.** After merging domain branches in, run
`alembic heads`; if >1, `alembic merge heads` (see STEP 2 — slug truncates, stage
by real `git status` filename, not a glob).

**8c. Re-verify on the INTEGRATED branch, not just the feature branch.** The
integration branch has other people's landed domains + main's changes on top of
your work. Re-run the full STEP 7 gate THERE: 61+ integration tests must say
"**passed**" (Docker up — see STEP 5 false-green trap), guardrail present-AND-clean
(STEP 6 — verify count moved), ruff clean. A feature-branch green does not prove
integration-branch green.

**8d. Marker sweep before commit** (shared-branch paranoia):
```bash
findstr /r /n "^<<<<<<< ^>>>>>>>" <every file you touched>
```
Must return nothing. Then commit (explicit paths, never `-A` — preserves the
untracked scratch/venv pile) and push. Confirm `git rev-parse <branch>
origin/<branch>` shows local == remote after.

**8e. The integration branch merges to `main` ONCE, at the very end.** Per Biray:
`mig/repo-migration -> main` happens only when the WHOLE migration is done, as one
coordinated event — NOT per domain. If a PR auto-opens with base `main` mid-
migration, that base is wrong: close it (or fix the base), don't resolve it. Your
per-domain PRs base on `mig/repo-migration`, always.

**8f. Local DB is NOT a gate; testcontainers is.** After a land, `alembic check` /
`upgrade head` against your prod-pointed local env will fail on stale prod state
(STEP 2) — that is NOT a branch defect and NOT a merge blocker. The testcontainers
integration run is the authoritative signal. Don't chase a local-check green; it's
a rabbit hole that never touches the branch.

## CONNECTION / ENV CONSTANTS (burned in this session)

- **Two URLs, never crossed:** `DATABASE_URL` = 6543 transaction pooler (app
  runtime; `statement_cache_size=0` already set); `DATABASE_DIRECT_URL` = 5432
  session pooler (alembic + reflection). The repo layer reads `DATABASE_URL`;
  alembic/reflection read `DATABASE_DIRECT_URL`.
- **asyncpg + pgbouncer = NO prepared statements.** Supabase's 6543 pooler is
  pgbouncer transaction mode, which breaks asyncpg's prepared statements
  (`DuplicatePreparedStatementError` / `prepared statement does not exist`).
  Fix that's already in place: `statement_cache_size=0`. (asyncpg FAQ; SQLAlchemy
  #6467; Supabase #35684; Duch/Medium.) If a new engine is created anywhere, it
  MUST carry this connect_arg or it will crash intermittently under load.
- **Stale pooler host prefix** `aws-0` vs `aws-1`: error `Tenant or user not
  found`. Copy the host VERBATIM from a known-good URL; don't retype. (Bit us:
  key rotation silently set `aws-0`; correct is `aws-1`.)
- **PROD env flag (Render):** migrated endpoints 500 on deploy if prod lacks
  `DATABASE_DIRECT_URL` and the correct `aws-1` host. This is Alihan's lane but a
  hard pre-merge check for any domain PR.

## PERSON B SCOPE (what is and isn't yours) — current as of the CP1 land

- **✅ DONE (landed + guardrailed on `mig/repo-migration`):** `sections`,
  `innung`, `teams` (CP1). 27 files in MIGRATED; single head after the
  analyses-domain merge.
- **Yours remaining, in recommended order (PART2 Wave B1 then B2/B3):**
  1. **`workspace`** — `workspaces`, `workspace_assignments`, `workspace_sections`,
     `workspace_uploads`, `workspace_acknowledgements`. Teams-adjacent, so patterns
     carry directly from teams. Clean re-entry; unblocks nobody.
  2. **`project_events`** (CP3) — kick off `vext` early. Unblocks A's projects M2
     (`create_situation_version` emits a `project_events` audit row). Owner-first:
     you model the table, A consumes once landed.
  3. **`promo`** (CP2) — `promo_codes`, `promo_redemptions`, `api/routes/promo.py`.
     Unblocks A's `referrals.py` (single-transaction double-credit fix).
  4. **`outcomes`** — `gbu_outcomes`. NOTE: `to_regclass` this FIRST — as of the
     last check the table did NOT exist (feature silently no-ops); if still NULL,
     STOP and skip (STEP 0 existence gate).
  5. **`vext` / `vault_extract` giant (Wave B2)** — LAST: `project_events`,
     `whatsapp_sessions`, `vault_files`, `vault_rules`, `vault_workflows`,
     `vault_history`, `vault_transfers`, `company_bereiche`,
     `vault_company_profiles`, `companies`; then lifecycle/integrations consumers;
     then `vext_session` + router session/tenant + extraction.
  6. **Wave B3 long tail:** handwerk verticals (qualifikationen/verbandbuch/pruefen/
     substance_qr/fair), review, comms, regulatory, memory (PhoneLinkRepository),
     and the misc tail (feedback, gbu_share, partners, beta_invite, consent,
     claim_service partner_codes, training/capture, audit/event_logger, vault/rag).
- **The two CPs (promo, project_events) unblock Person A — prioritise them over
  outcomes**, which blocks nobody. Coordinate one `alembic merge heads` at each CP
  hand-off.
- **Gate before any domain touching shared tables:** check footprint for
  `vault_companies`/`profiles` (A owns); if referenced, BLOCKED until A migrates.
- **Not yours:** Auth->Zitadel (Phase 3), Storage->GCS (Phase 4), Cloud SQL
  provisioning / DSN flip (Phase 2, ops — Alihan cleared the Render env: both URLs
  live, `aws-1` host, verified `SELECT 1` 131ms), Person A's domains, `.github/` CI
  (Alihan). The repo layer is target-agnostic: GCP Cloud SQL vs AWS RDS is a
  connection-string flip, so your work is identical regardless of final host.

## WHAT STAYS HUMAN (never automate past these)

- Cowork NEVER commits. Anshu runs git.
- Maker != checker: any LLM judge is a DIFFERENT family (Gemini), never Cowork's
  own Claude (velth-loop; "Play Favorites" arXiv 2508.06709).
- A domain reaching gate-green is NOT "shipped" — it's a small PR for review +
  the prod-env check + (for compliance-bearing output) SiFa sign-off.

## STOP CONDITIONS

- `to_regclass` NULL -> table absent -> STOP, pick another domain.
- `alembic check` reports drift after an honest model pass -> STOP, fix the model
  (the reflection is truth), do not hand-edit the migration to mask it.
- Shared-table dependency on unmigrated Person-A tables -> STOP, coordinate.
- 3 fix rounds without green (velth-loop cap) -> STOP, re-plan; the plan was
  likely wrong, not the code.
