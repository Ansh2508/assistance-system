---
name: veos-graphify
description: >
  How to point the installed `graphify` skill (a separate, upstream-managed
  tool at ~/.claude/skills/graphify) usefully at the veOS repo specifically,
  and which of this project's other skills should consume or feed its
  output. Load this alongside `graphify` whenever the user asks to map,
  graph, or visualize veOS, or asks an architecture question that a
  knowledge graph could answer faster than a fresh grep pass across
  `src/veos_runtime/`.
---

# veos-graphify — pointing an upstream tool at veOS's real shape

`graphify` (`Graphify-Labs/graphify`, Apache-2.0, installed globally via
`uv tool install graphifyy` + `graphify install` — same install this
skill's VELTH counterpart, `velth-graphify`, documents) is a separate,
actively maintained upstream tool. Do not edit
`~/.claude/skills/graphify/SKILL.md` directly, it gets overwritten on
`graphify install`/upgrade. This file is the place for veOS-specific
guidance instead.

## What it actually does, in one line

Deterministic, local, tree-sitter AST parsing (no LLM, nothing leaves the
machine) turns a folder into a queryable knowledge graph — `graph.html`
(clickable), `graph.json` (query anytime without re-reading files), and
`GRAPH_REPORT.md` (plain-language highlights). Docs/PDFs/images optionally
use the assistant's own model for a semantic pass; code parsing never does.

## Where to point it

`C:\Users\redmi\veos` — standalone repo, never merged into `velthdev/velth`
(see `$veos-preflight`). The real bulk of the runtime is one large package,
`src/veos_runtime/`, dozens of interdependent modules (orchestration,
adk_runtime, action_gateway, brain, memory_gate, revenue/, sales_intelligence/,
work_ledger, trace, and more) — exactly the shape graphify is built for:
many-file, many-hop questions, not a single-file lookup.

For a cross-repo question spanning both VELTH and veOS (e.g. "how does the
Growth specialist's GSC ingestion reach VELTH's Rechtskataster data"), use
graphify's multi-path merge from either repo:
`/graphify C:\Users\redmi\veos C:\Users\redmi\velth-clean`. See
`$velth-graphify` for the VELTH-side half of that same guidance.

## When to reach for it instead of grep/Explore

- **Tracing a request through the orchestration layer**: `orchestration.py`'s
  `SpecialistName` enum → `adk_runtime.py`'s `if/elif` dispatch chain → the
  specialist's own agent module → back to the Chief. This is a real,
  documented multi-hop path (`$veos-preflight`'s own "KNOWN TRAPS" section
  describes exactly this chain and its silent-misroute failure mode) —
  `graphify path "SpecialistName" "adk_runtime"` or
  `graphify explain "dispatch chain"` can surface the actual call graph
  faster than re-reading `adk_runtime.py` cold each session.
- **Before a Sprint-scoped multi-file change** (any work following
  `$veos-preflight`'s own incident-log pattern, or a new specialist/growth
  domain addition per the mother plan's §14 architecture table): run
  `/graphify . --mode deep` once at the start so exploration during the
  session becomes `graphify query` calls, not repeated fresh reads.
- **Two-registration-surface bugs**: `$veos-preflight`'s own documented
  incident class is a tool registered in the ADK tool array but missing from
  `ALLOWED_CAPABILITIES`, or present in both but never mentioned in
  `CHIEF_OF_STAFF_INSTRUCTION` — a graph of "what references this tool name"
  across `adk_runtime.py`, `action_policy.py`, and the instruction string
  itself is a faster way to audit a new tool's real reachability than three
  separate greps.
- **Understanding the Revenue OS / sales_intelligence split** before touching
  either — `revenue/` (state engine, buyer types, Twenty CRM sync) and
  `sales_intelligence/` (experiments, metrics, playbook) are two related but
  separately-owned modules; a graph of their actual import edges is more
  reliable than assuming the boundary from the directory names alone.

## When NOT to reach for it

- A single, already-known file path — just `Read` it.
- Anything needing the CURRENT, uncommitted state of a file that changed
  this session — the graph is a snapshot from the last `/graphify` or
  `--update` run. Re-run `--update` before trusting it, same staleness
  discipline `$velth-prod-verify` applies to deploy claims elsewhere in this
  environment.

## Cross-references to this project's other skills

- **`$veos-preflight`**: its "KNOWN TRAPS" section is a live, growing log of
  real incidents (stale images, silent env-var drops, two-registration-
  surface bugs, ownership/grant traps). A graphify run's "surprising
  connections" in `GRAPH_REPORT.md` is a reasonable trigger to check whether
  a newly-surfaced coupling matches (or should be added as) a new trap —
  the two are complementary, not redundant: the trap log is hard-won
  incident memory, graphify is structural discovery.
- **`$veos-wiring-and-ai-test`**: that skill's core failure pattern (a value
  correct in `.env`/`config.py` but never reaching the running process
  because `compose.yml` lists env vars as an explicit allowlist) is exactly
  a "the edge you'd expect to exist doesn't" finding — graphify's
  EXTRACTED/INFERRED/AMBIGUOUS tagging on an edge between a `config.py`
  field and a `compose.yml` service block would flag a missing wire as an
  absent edge, worth checking before assuming a flag is wired.
- **`$velth-graph-engineering`** (VELTH-side, but the topology-design
  principle applies here too): do not confuse graphify's knowledge-graph (a
  read-only map of what exists) with a task-topology graph (what a
  multi-actor task is ALLOWED to do, where humans gate). They share the
  word "graph" and nothing else.
- **`$ponytail-review`**: an unexpected edge in `GRAPH_REPORT.md`'s
  "surprising connections" between two modules that shouldn't know about
  each other is a real candidate for a `yagni:`/`delete:` finding.

## Honest limits, stated so they aren't rediscovered per-session

- Not yet exercised against veOS specifically as of 2026-09-26 — this
  guidance is design-time, matching how `$velth-graphify` was written before
  its first real run. Treat the first real `/graphify` run on
  `C:\Users\redmi\veos` as a chance to correct anything above, the same way
  `$veos-preflight`'s own "KNOWN TRAPS" section grows from real incidents
  rather than speculation.
- Semantic passes on docs/PDFs use whichever model this session is running
  as. veOS's own docs (`PRODUCT.md`, `DESIGN.md`, growth-plan documents) are
  internal strategy content, not customer PII — lower sensitivity than
  VELTH's Rechtskataster/hazard_feedback data, but still worth a moment's
  thought before pointing a semantic pass at anything marked confidential.
