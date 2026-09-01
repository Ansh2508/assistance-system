---
name: veos-preflight
description: veOS project preflight checks, absolute rules, environment constants, and hard-won traps for every Claude Code session touching velthdev/veos. Load at the start of ANY task in this repo. Distinct from VELTH-proper's velth-preflight — separate repo, separate GCP project (veth-veos-dev), separate tooling.
---

# veOS Preflight

veOS is VELTH's internal agentic operating system, deployed on GCP and in
active use by the whole team — not a personal tool. Treat its data and
approval design with the same seriousness as customer-facing VELTH work.

## ENVIRONMENT CONSTANTS
- Repo: velthdev/veos, standalone, never merged into velthdev/velth.
- GCP project: veth-veos-dev. VERIFY `gcloud config get-value project`
  before any gcloud call — Anshu runs a second GCP project for VELTH-proper.
- CI is structurally blocked by an unpaid GitHub org bill (org-owner-only
  setting). This is known, not a bug to re-diagnose. Local verification —
  full test suite, ruff, import-linter — is the substitute while the bill
  is unpaid, per the manual-deploy doc's own stated policy.
- Git: draft diffs and commit commands; Anshu runs every commit/push.
- Deploy: build a fresh image off the exact commit, push to Artifact
  Registry, pull+restart on BOTH veos-core-01 and veos-drive-ingestor-01.
  Never trust "deployed" without checking the image tag traces to the
  commit you think it does — Sprint 3's own near-miss was a stale image.

## KNOWN TRAPS (verified 2026-08-26)
- **Never declare `google_compute_instance.boot_disk.initialize_params.
  resource_policies` in Terraform config for an existing instance.** The
  provider's own schema says plainly: "Modifying this list will cause the
  instance to recreate." Attach/detach a resource policy on a running
  instance's disk via `gcloud compute disks add-resource-policies` /
  `remove-resource-policies` instead, and leave the attribute undeclared in
  `.tf` (it's `optional` + `computed`, so Terraform accepts whatever's live
  without diffing, as long as config never sets it). Caught before it
  destroyed `veos-core-01` a second time, by checking the schema before
  applying rather than after.
- `enforce_capability` and `before_tool_callback` must share one check —
  do not let them diverge again after Sprint 4 lands.
- `session.merge()` (upsert) is the wrong pattern for anything meant to be
  an immutable audit table. New audit tables need `REVOKE UPDATE, DELETE`
  plus a SECURITY DEFINER insert-only path — application discipline alone
  doesn't hold once anything has direct table access.
- The outbox/idempotency state names in the Sprint 4 PDF are a reasonable
  elaboration, not canon — cite Brandur Leach's started/finished +
  separate locked_at shape instead; see the Sprint 4 dispatch for why.
- Six of nine Compose services are intentional placeholders
  (health-smoke image) — check docs/STATUS.md for the current real count
  before assuming a service does anything.
- Terraform has carried unresolved destructive drift (wants to destroy
  the live VM) since Sprint 1. Never run `terraform apply`.
- ORM/migration type mismatches are invisible on SQLite because SQLite
  builds tables from ORM metadata, not from the reviewed migration. Three
  have shipped this way (`embedding_json`, `run_id`/`candidate_id` uuid,
  `metadata_json`/`keywords_json` jsonb). Any new column whose migration
  type is not a plain primitive needs a dialect-aware TypeDecorator plus a
  test asserting it compiles to the real Postgres type.
- The Action Gateway runs under its own dedicated service account, never
  `veos-core-runtime`. That identity already holds `objectAdmin` on the
  artifacts bucket and `secretAccessor` on every Slack secret — reusing it
  makes "the gateway is the only thing holding connector credentials"
  false the moment the gateway exists.
- Creating a dedicated SA is not the security step; **removing the old
  grant is.** Creating `veos-action-gateway` with `objectAdmin` and giving
  `veos-core-runtime` `serviceAccountTokenCreator` on it, without removing
  `veos-core-runtime`'s own `objectAdmin`, leaves the VM identity with
  strictly more authority than before. Do the pair or neither.
- Bare `storage.Client()` (and any bare ADC call) on a GCE VM resolves to
  the VM's **attached** service account through the metadata server. No
  import is involved, so `.importlinter` cannot see it and a container is
  not a credential boundary. Grep for bare SDK clients before claiming any
  per-service identity.
  **`artifacts.py` addressed 2026-08-26**: `GcsArtifactStore` now takes an
  optional `service_account` (impersonation, same pattern as
  `connectors/gcs_object.py`) and an optional `expected_principal` that
  asserts the resolved ADC principal before writing. Both default to `None`,
  so behaviour is unchanged unless configured - bare ADC on
  `veos-drive-ingestor-01` resolves to `veos-drive-reader` and is correct
  there. The point is that the identity is now explicit and checkable rather
  than implicit; set `expected_principal` in the drive-ingestor env to turn
  "we assume this runs as the reader" into a precondition that fails loudly
  on the wrong host. Six tests in `tests/unit/test_artifacts_identity.py`.
- `veos_runtime` — the role the app connects to Cloud SQL as — is a member
  of `cloudsqlsuperuser` and owns the tables it creates. Any "immutable at
  the database level" claim has to say *to whom*: `REVOKE` + an
  `ENABLE ALWAYS` trigger stops ordinary SQL, but this role can drop the
  trigger. Check `pg_auth_members` before writing the claim down.
- **`ALTER TABLE ... OWNER TO` silently drops the old owner's self-grants.**
  A `GRANT SELECT, INSERT ... TO role` issued while that role owned the
  table is redundant and is not stored as a durable ACL entry, so moving
  ownership leaves the role with NO privileges. This took the Action
  Gateway down for real on 2026-08-25 (every action writes an audit
  record). Any ownership reassignment must re-issue the grants explicitly,
  and must be followed by a POSITIVE control, not only negative ones -
  the negative controls all passed while production was broken.
- **Table/function OWNERSHIP, not just role membership, is the real DDL
  bypass.** `veos_runtime` being a `cloudsqlsuperuser` member was the
  suspected hole in `audit_records`' immutability; the actual hole was that
  `veos_runtime` *owned* the table and the guard function (whoever runs
  `CREATE TABLE`/`CREATE FUNCTION` becomes owner by default), which grants
  `ALTER`/`DROP` rights independent of any role membership. `SECURITY
  DEFINER` only protects anything when the function's owner differs from the
  connecting role — check `pg_tables.tableowner` / `pg_proc.proowner`, not
  just `pg_auth_members`, before trusting an immutability claim.
- **A naive population-informed prior for a fatigue/anomaly detector is
  usually wrong, in the opposite direction from the fixed-constant problem.**
  Blending an individual's own accumulating signal into their own threshold
  (Bühlmann credibility shrinkage, `Z = n/(n+K)`) lets a genuine bad actor's
  own misbehaviour drag their own bar up before there's enough evidence to
  catch them - simulated: rubber-stamp detection in a diligent population
  collapsed from 80% to 0%. A fixed threshold's virtue is precisely that it
  does *not* respond to the thing being tested. Simulate before trusting an
  "obviously more sophisticated" statistical fix.
- **Secrets in this project have carried trailing CRs (0x0D).** Seven of
  fifteen did, found 2026-08-25 - created from Windows, where `gcloud`
  emits CRLF, and `$(...)` strips trailing newlines but NOT carriage
  returns. Impact depends entirely on the consumer, which is why it hides:
  `_csv()` calls `.strip()` so allowlists parse fine, and docker compose
  strips CR from `.env` so containers are fine - but any *direct* consumer
  breaks. A CR in a signing secret makes `hmac.new(secret.encode(), ...)`
  compute a different digest, so a correctly built signature is rejected;
  a CR in a bearer token is an HTTP header-injection hazard. The stored
  secrets were cleaned and the sync script now pipes through
  `tr -d '
'`, but **check length before trusting any secret value**
  (a Slack signing secret is exactly 32 hex chars, a bot token 59).
  This also produces misleading `FATAL: password authentication failed`
  from Cloud SQL - the password may be right and the CR wrong.
- **`/slack/interactions` must be in the Caddyfile's `@runtime` path
  allowlist.** It was missing until 2026-08-25: the handler in `app.py`
  was real, tested, and completely unreachable from the internet, so a
  genuine Slack button click hit Caddy's `respond 404`. Adding a new
  public route to `app.py` is only half the job - Caddy allowlists paths
  explicitly, and nothing in the test suite covers the proxy.
- There are **two** Drive ingestion paths with different identities. The
  intended one is `/opt/veos/drive-ingest-file.sh` on
  `veos-drive-ingestor-01` (impersonates `veos-drive-reader`). A second
  `drive-ingestor` container also runs on `veos-core-01` with
  `VEOS_DRIVE_USE_ADC=false`, i.e. as `veos-core-runtime`; it is inert only
  because polling is off. Check which one a change actually affects.
- A behavioural detector compared against a fixed constant is usually
  wrong. For a repeat-the-last-disposition signal the chance baseline is
  `p^2 + (1-p)^2`, which is 0.82 at a 90% approve rate — above the 0.70
  constant that shipped. Compare against an expected baseline, the way
  MaxSPRT-style safety surveillance does, and state the residual rate.
- **Vertex routing is env-var-driven at the `google-genai` SDK layer, not
  from `Settings`.** `BaseApiClient.__init__` reads `GOOGLE_GENAI_USE_VERTEXAI`
  / `GOOGLE_CLOUD_PROJECT` / `GOOGLE_CLOUD_LOCATION` straight from
  `os.environ` — constructing a `Settings(...)` object in a local script does
  **not** configure it, no matter what the field defaults say. A local shell
  with a stray `GEMINI_API_KEY`/`GOOGLE_API_KEY` and no
  `GOOGLE_GENAI_USE_VERTEXAI` exported silently falls through to the public
  Gemini Developer API free tier — a 5 requests/minute cap that looks exactly
  like a broken model layer from the caller's side (`429 RESOURCE_EXHAUSTED`).
  Before trusting a local "real model" test result: `env | grep -i
  'GOOGLE_\|GEMINI_'` first. The deployed containers are correct — verified
  2026-08-25 by executing a real call inside `veos-event-gateway-1`:
  `client.vertexai == True`, `traffic_type=ON_DEMAND`, no `GEMINI_API_KEY` in
  the container env at all — but don't assume a local repro of that is testing
  the same thing.
- **The stale-image trap recurred, verified 2026-08-26, despite already
  being documented above.** A written warning without an enforced check
  doesn't hold — `.env`'s `VEOS_RUNTIME_IMAGE_TAG` was still pinned to a
  Sprint 4 short-SHA; `docker compose pull` re-fetched that exact same old
  image under the pin, and the deploy silently did nothing while every step
  reported success. Caught only by checking `/health/`'s `runtime` field
  post-deploy and noticing it hadn't moved. **The actual fix, not just the
  warning:** after any deploy, run
  `docker inspect <container> --format '{{.Image}}'` (or re-curl `/health/`
  for a field that changed in this release) and confirm it matches the new
  build — don't trust "pull succeeded" or "compose up reported Recreated"
  as proof, both can be true while serving the old image.
- **A feature flag can be set correctly in `.env` and still do nothing,
  because `compose.yml` lists each container's environment as an explicit
  key allowlist, not `env_file: .env`.** Verified 2026-08-26:
  `VEOS_EMBEDDINGS_ENABLED=true` in `.env`, container restarted (even
  `--force-recreate`), and `Settings().embeddings_enabled` still read
  `False` — `docker inspect ... Config.Env` showed the key **entirely
  absent** from the running container, not merely false. The variable had
  never been added to `compose.yml`'s `environment:` block for that
  service, in the repo or on the VM, since the feature shipped. Before
  trusting any new `.env` flag: grep `compose.yml` for the exact
  `VEOS_*` key under the service that needs it — presence in `.env` proves
  nothing on its own. A regression test now guards this
  (`tests/unit/test_compose_env_wiring.py`, mutation-verified) for the
  Company Brain/embedding flags specifically; extend it when adding the
  next flag rather than trusting the next one by inspection alone.
- **`docker compose up -d <service>` sometimes decides nothing changed
  when a plain `.env` edit clearly should have.** Observed 2026-08-26:
  editing `.env` and running `up -d event-gateway action-gateway` reported
  `Running` (no recreate) for a flag that demonstrably wasn't live yet.
  `--force-recreate` reliably picks up the current `.env`; a plain `up -d`
  after an `.env`-only edit does not reliably do so. Use
  `--force-recreate` when the only change was `.env`, and verify with a
  `docker exec ... python -c "from veos_runtime.config import Settings; ..."`
  read of the actual running value afterward — don't trust the compose
  output's "Running"/"Recreated" line as proof either way.
- **When GitHub Actions is down (see the CI note above), the deploy
  pipeline can be reproduced by hand via Cloud Build, without granting any
  new IAM.** `deploy.yml`'s `build-and-push` job already runs as
  `veos-deploy@veth-veos-dev.iam.gserviceaccount.com` via Workload Identity
  Federation, which already holds `artifactregistry.repositories.
  uploadArtifacts`. A direct `gcloud builds submit` under the caller's own
  identity (or the VM's default Compute Engine SA) does NOT have that
  grant and fails the push step, not the build step — don't read a push
  failure as "the build is broken." Fix: `gcloud builds submit
  --config=<cloudbuild.yaml> --project=veth-veos-dev` with
  `serviceAccount: projects/veth-veos-dev/serviceAccounts/veos-deploy@...`
  and `options: {logging: CLOUD_LOGGING_ONLY}` set in the config (a custom
  service account requires non-default logging, or the submit fails before
  it even starts). Verified working end-to-end 2026-08-26 for both
  `veos-runtime` and `health-smoke` images.
- **A Python/SQLAlchemy DDL harness can silently execute nothing against a
  real migration file — no exception, no effect — while `psql -v
  ON_ERROR_STOP=1 -f` applies the identical file correctly on the first
  try.** Verified 2026-08-26 against migration `0009`: both
  `conn.execute(text(sql))` and the lower-level `conn.exec_driver_sql(sql)`
  (which bypasses SQLAlchemy's bind-parameter scanning entirely) produced
  `ddl_applied=True`-looking non-errors with zero schema change, reproduced
  byte-for-byte against a disposable scratch table before switching tools.
  Root cause not fully isolated — a `:word`-shaped token inside a SQL
  comment was a leading theory and was ruled OUT, not confirmed, since
  `exec_driver_sql` failed identically despite bypassing exactly that
  scanning. **Use `psql -v ON_ERROR_STOP=1 -f` for any real migration apply
  shaped like `BEGIN`/`COMMIT` + a `DO` block + a `CREATE FUNCTION`** —
  don't re-attempt a Python DDL harness on faith for that shape, and if one
  is used for a dry run, always independently re-verify the resulting
  schema state on a fresh connection rather than trusting the harness's
  own report of what it did.
- **`hooks.veos.velth.io/health/`'s `runtime` field was hardcoded and had
  drifted a full sprint behind reality** — it read `"sprint4"` through the
  entire Sprint 5 build and initial deploy, because nothing bumps it
  automatically. Fixed 2026-08-26 to `"sprint5"` in both `app.py` and
  `gateway_app.py`. This field has no CI check tying it to the actual
  shipped code — when the next sprint lands, bump both hardcoded strings
  as part of the same PR, don't wait to notice post-deploy the way this
  session did.

## SKILL TRIAGE — VELTH-wide skills that apply here unchanged
`velth-graph-engineering`, `velth-spec`, `velth-loop`, `velth-context`,
`velth-dispatch-craft`, `velth-truth-gate`, `audit-like-a-sifa` all apply
as-is — task-agnostic by design. `velth-north-star` and
`velth-continual-learning-infra` apply by analogy: their five-properties
checklist for data that "compounds" (tenant attribution, actor identity,
before→after with the rejected branch preserved, temporal+version
anchors, outcome linkage) is the exact lens for veOS's own
ApprovalDecision/AuditRecord tables. VELTH-repo-specific skills
(`velth-preflight`, `velth-test-strategy`, `velth-gcp-migration`, etc.)
do NOT transfer directly — different repo, different data model.
