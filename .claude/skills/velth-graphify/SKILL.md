---
name: velth-graphify
description: >
  How to point the installed `graphify` skill (a separate, upstream-managed
  tool at ~/.claude/skills/graphify) usefully at VELTH and veOS specifically,
  and which of this project's other skills should consume or feed its output.
  Load this alongside `graphify` whenever the user asks to map, graph, or
  visualize this codebase, or asks an architecture question that graphify's
  own graph could answer faster than a fresh grep pass.
---

# velth-graphify — pointing an upstream tool at this project's real shape

`graphify` (`Graphify-Labs/graphify`, Apache-2.0, installed 2026-09-26 via
`uv tool install graphifyy` + `graphify install`) is a separate, actively
maintained upstream tool — do not edit `~/.claude/skills/graphify/SKILL.md`
directly, it gets overwritten on `graphify install`/upgrade. This file is the
place for VELTH-specific guidance instead.

## What it actually does, in one line

Deterministic, local, tree-sitter AST parsing (no LLM, nothing leaves the
machine) turns a folder into a queryable knowledge graph — `graph.html`
(clickable), `graph.json` (query anytime without re-reading files), and
`GRAPH_REPORT.md` (plain-language highlights). Docs/PDFs/images optionally
use the assistant's own model for a semantic pass; code parsing never does.

## Where to point it in this workspace

Two separate repos, two separate graphs — never merge them into one `/graphify`
run unless the task is genuinely cross-repo (e.g. "how does veOS's Growth
domain consume VELTH's Rechtskataster data"):

- `C:\Users\redmi\velth-clean` — the VELTH frontend+backend monorepo (this is
  the working checkout; see `$velth-preflight` for why `velth-clean` and not
  the original `velth` checkout).
- `C:\Users\redmi\veos` — the standalone veOS repo (`$veos-preflight`).

For a genuinely cross-repo question, use graphify's multi-path merge:
`/graphify C:\Users\redmi\velth-clean C:\Users\redmi\veos`.

## When to reach for it instead of grep/Explore

- **Architecture questions spanning many files**: "how does a contact form
  submission reach Twenty CRM" touches `ContactV2.tsx` → `contact.py` →
  `revenue/schemas.py` → `crm_twenty.py` — exactly the kind of multi-hop trace
  graphify's `path`/`query` commands are built for, versus several rounds of
  manual grep.
- **Before a large refactor or migration wave** (`$velth-gcp-migration`'s
  per-domain loop, or any `$velth-graph-engineering`-scoped multi-actor task):
  run `/graphify . --mode deep` once at the start of the session so the whole
  session's exploration steps become `graphify query` calls instead of
  repeated fresh reads — cheaper and it keeps a durable map across a long
  session per `$velth-context`'s own state-recovery goals.
- **Onboarding a new session/agent to an unfamiliar part of the codebase**:
  `graphify explain "<ConceptName>"` is often faster and more complete than a
  cold `$Explore` pass for a concept that spans many files (a vertical
  config's full pipeline, a renderer's full call graph).

## When NOT to reach for it

- A single, already-known file path — just `Read` it. Graphify is for
  multi-file, multi-hop, "how does this connect to that" questions, not a
  grep replacement for something you can name directly.
- Anything requiring the CURRENT, uncommitted state of a fast-moving file —
  the graph is a snapshot from the last `/graphify` or `--update` run, not
  live. Re-run `--update` before trusting it on a file that changed this
  session (this is the same staleness discipline `$velth-prod-verify` applies
  to deploy claims — a graph is a snapshot, not a fact, until refreshed).

## Cross-references to this project's other skills

- **`$velth-context`**: graphify's `graph.json` is a genuinely useful
  `NEXT_TASK.md`-adjacent artifact — if a session builds one, note its
  existence and freshness in the session-end resume note so the next session
  knows to `--update` rather than rebuild from scratch.
- **`$velth-graph-engineering`**: do not confuse graphify's knowledge-graph
  (a read-only map of what exists) with that skill's task-topology graph (the
  node/edge model for what a multi-actor task is ALLOWED to do). They share
  the word "graph" and nothing else — graphify never gates an action or
  represents a human-approval checkpoint.
- **`$ponytail-audit`** (upstream companion, not yet reviewed for adoption
  here) and `$ponytail-review`: a graphify `GRAPH_REPORT.md`'s "surprising
  connections" section is a reasonable input to a ponytail-review pass — an
  unexpected edge between two modules can be exactly the kind of accidental
  coupling worth flagging as `yagni:`/`delete:`.
- **`$research-to-code`**: when translating an external paper/benchmark's
  design into a real architecture decision, graphify on the target
  paper/repo (`/graphify <path-or-url> --mode deep`) can surface the actual
  structure faster than reading linearly, before deciding what to port.

## Honest limits, stated so they aren't rediscovered per-session

- Semantic passes on docs/PDFs/images use whichever model this session is
  running as — for VELTH's GDPR-sensitive documents (Rechtskataster,
  hazard_feedback, any real customer PDF), do not point graphify's semantic
  pass at those without checking the same data-boundary rules
  `$velth-continual-learning-infra` and `$velth-north-star` already apply to
  training-data handling. Code-only graphs (no semantic pass) are unaffected
  — tree-sitter parsing never leaves the machine and carries no such risk.
- Not yet exercised in this project as of 2026-09-26 — the guidance above is
  design-time, not verified-in-use. Treat the first real `/graphify` run on
  `velth-clean` as a chance to correct anything above that turns out wrong,
  the way `$veos-preflight`'s own "KNOWN TRAPS" section grows from real
  incidents rather than speculation.
