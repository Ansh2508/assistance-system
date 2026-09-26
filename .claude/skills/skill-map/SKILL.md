---
name: skill-map
description: >
  Project-agnostic skill router across all of Anshu's repos and general
  work, not just one codebase. Load at the start of any session where no
  project-specific preflight skill has fired yet, or when it's unclear
  which of the ~40 skills in ~/.claude/skills applies. Detects the current
  project from the working directory and hands off to that project's own
  preflight skill if one exists; otherwise routes by task category using
  the general-purpose skills below.
---

# skill-map — the router above the per-project routers

This is deliberately NOT a replacement for `velth-preflight` or
`veos-preflight` — those are project-specific and go deeper (environment
constants, git rules, known traps) than a general router should. This skill
exists for the layer above them: knowing WHICH project-specific router to
load in the first place, and covering the general-purpose skills that apply
regardless of project.

## Step 1 — detect the project from the working directory

| Working directory root | Project | Load first |
|---|---|---|
| `C:\Users\redmi\velth-clean` (or `velth`, `velth-pr1-integration`, any `velth-*` worktree) | VELTH (frontend+backend, FastAPI/Next.js) | `$velth-preflight` — it has its own skills map for the ~25 VELTH-specific skills, load it and stop here |
| `C:\Users\redmi\veos` | veOS (VELTH's internal agentic OS, separate GCP project) | `$veos-preflight` — separate environment constants, known traps, deploy discipline |
| `C:\Users\redmi\Documents\repo-anshu-raj-3c08-se` | TH Deggendorf coursework | `sde-preflight` / `sde-test-strategy` — completely different codebase, do not apply VELTH/veOS conventions here |
| Anything else not yet listed here | An unmapped project | No project-specific preflight exists yet — fall through to Step 2, and consider whether this project has grown enough real, recurring traps to deserve its own `<project>-preflight` skill (see "When a new project earns its own preflight" below) |

If genuinely unsure which project a working directory belongs to (a fresh
clone, an unfamiliar path), check for the project's own `CLAUDE.md`/`AGENTS.md`
first — those name the project and its conventions directly, more reliably
than inferring from a directory name alone.

## Step 2 — no project-specific preflight exists: route by task category

These apply regardless of which project you're in. Load the project-specific
preflight FIRST if one exists (Step 1) — these are supplementary, not a
substitute for a project's own environment constants and rules.

**Research / verifying an external claim before acting on it:**
- `research-simulate-encode` — read primary sources, validate at your own
  scale, encode the decision structurally. Use before committing to a design
  based on a paper/benchmark/best-practice you haven't personally verified.
- `research-to-code` — once research is validated, translate it into an
  actual code/architecture decision.
- `deep-cross-domain-research` — when a task asks for genuine depth across
  multiple countries/languages/fields, not a token citation per item.
- `china-frontier` / `silicon-valley-frontier` / `frontier-ml-research` —
  region- or domain-specific frontier research lanes (open-source AI,
  compute, standards, ML model ladders). Load the one matching the task's
  actual geography/domain, not all three.

**Before/during any non-trivial coding task, project-agnostic:**
- `ponytail` — minimal-change engineering lens: smallest validated change,
  never delete edge-case/safety/security/accessibility/data-integrity
  behavior to look smaller. Route risky architectural choices to
  `research-simulate-encode` instead of simplifying past them.
- `ponytail-review` — diff review focused only on over-engineering
  (what to delete), separate from correctness/security review.
- `ponytail-debt` — harvest `ponytail:` comment markers into a debt ledger,
  one-shot, changes nothing.
- `build-test-verify` — run all validation/test/build commands before
  reporting work done. The generic version of what `velth-loop`'s VERIFY
  step and `veos-preflight`'s local-verification-substitutes-for-CI policy
  each do in a project-specific way.
- `quota-tiered-delegation` — split judgment-heavy phases (kept on the
  primary model) from high-volume mechanical phases (delegated to a
  cheaper Claude tier via `Agent(model: "haiku")`) when cost/quota is a
  stated concern. Deliberately does NOT proxy traffic through any
  third-party model gateway — see the skill body for why (OmniRoute's real,
  documented CVEs were the reason this was built instead of installing it).

**Codebase mapping / architecture questions spanning many files:**
- `graphify` — turn a folder (code, docs, PDFs, images, video) into a
  queryable knowledge graph, local tree-sitter AST parsing, no vector store.
  `$velth-graphify` / `$veos-graphify` are the project-specific pointers for
  those two repos; for any other project, use `graphify` directly with no
  wrapper needed yet (see "When a new project earns its own preflight"
  below for when a wrapper becomes worth writing).

**Reviewing AI-produced work before accepting/reporting it done:**
- `ai-output-self-audit` — check any AI-generated deliverable against the
  original request line by line before saying "done."
- `audit-like-a-sifa` — Anshu's own five-question verification method
  (vacuous tests, write/read coupling, uninvited changes, undetectable
  defects, confident-false-success) for judging AI-produced work when he
  can't read the code fluently himself.

**Frontend / UI / design work, any project:**
- `impeccable` — frontend design/UX audit and improvement (hierarchy,
  accessibility, motion, theming, anti-patterns).
- `design-motion-principles` — motion/interaction design review specifically
  (animations, transitions, hover states).

**Domain-specific, cross-project (VELTH's core domain, may recur elsewhere):**
- `risk-vault` — build Risk Vault YAML files (v2.0 RiskObjects) for hazard
  categories/vertical configs. VELTH-domain-specific but not filed under
  `velth-*` naming, worth knowing it exists regardless of which project.
- `legal-updater` — check/update legal references (ADR versions, DGUV
  updates) in YAML files. Same note as above.

## When a new project earns its own `<project>-preflight` skill

Per this environment's own established pattern (`velth-preflight`,
`veos-preflight`, `sde-preflight`): a project graduates from "route by
category" (Step 2 above) to "has its own preflight" once it has real,
recurring, hard-won specifics worth encoding — environment constants that
keep needing to be re-discovered, a git-hygiene rule specific to that
repo's quirks, or a KNOWN TRAPS-style incident log (see `veos-preflight`'s
own section for the shape that takes). Don't create a preflight skill
pre-emptively for a project that's only been touched once or twice — that's
premature scaffolding this environment's own `ponytail` skill would flag.
When a project does earn one, add its row to the Step 1 table above in the
same edit.

## Boundaries

This skill does not replace reading a project's own `CLAUDE.md`/`AGENTS.md`
— those are checked into the repo and are the actual source of truth for
that project's rules. This skill's job is purely routing: which skill(s) to
load, given where you are and what the task looks like.
