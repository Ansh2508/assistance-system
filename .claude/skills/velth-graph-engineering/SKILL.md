---
name: velth-graph-engineering
description: Design the TOPOLOGY of any VELTH multi-actor task — which nodes exist, which transitions are legal, where humans gate, where determinism replaces judgment. Load this BEFORE decomposing any non-trivial task and BEFORE writing any Cowork prompt with more than one actor, more than one phase, or any irreversible action (git write, migration apply, deploy, send, delete, shared-table write). Also load it whenever an agentic run has FAILED and you are about to "fix the prompt" — classify the failure mode structurally first. Complements velth-loop (how one node executes) and velth-spec (what one node is asked to do).
---

# VELTH Graph Engineering

## 0. What this skill governs

**Loop engineering** (`velth-loop`) designs how ONE node executes: plan → act → observe → repeat.
**Graph engineering** (this skill) designs the ORGANIZATION: which nodes exist, which
transitions are permitted, what state crosses each edge, and where the graph
pauses for a human.

Task-agnostic: migration, catalog work, engine changes, doc pipeline, infra, research.

### The empirical case

Source: Cemri et al., *Why Do Multi-Agent LLM Systems Fail?*, arXiv:2503.13657v3
(UC Berkeley + Intesa Sanpaolo, v1 Mar 2025 / v3 Oct 2025). MAST taxonomy built by
Grounded Theory over 150 traces with 6 expert annotators (κ = 0.88), then scaled to
**MAST-Data: 1,642 annotated traces across 7 MAS frameworks** via an o1-based
LLM-as-a-judge (94% accuracy, κ = 0.77 vs. humans; κ = 0.79 out-of-domain).

- Measured failure rate on 7 SOTA open-source MAS: **41% – 86.7%**.
- Failure category prevalence, full MAST-Data corpus (Figure 1, n=1,642 traces
  — the paper's headline breakdown): **FC1 System Design 44.2% · FC2
  Inter-Agent Misalignment 32.3% · FC3 Task Verification 23.5%**. A separate
  Figure 4 reports 41.8% / 36.9% / 21.3% over a smaller 210-trace subsample
  (30 traces per framework) used for a different per-system chart — cite the
  1,642-trace figure as primary; both are real, they answer different
  questions. **Re-verified against the full paper text 2026-08-26; corrected
  from an earlier version of this file that both mis-cited the numbers and
  summed them.**
- **"~79% is specification + coordination" does NOT appear in the paper and
  should not be repeated.** It is not an authored statistic — the only way to
  reach it is summing two category prevalence rates (41.8+36.9, only under
  the smaller subsample), and the paper's own Appendix E category-correlation
  matrix (FC1↔FC2 r=0.32, FC1↔FC3 r=0.17, FC2↔FC3 r=0.28) shows the
  categories are NOT mutually exclusive per trace — a single trace can carry
  more than one failure category, so summing overcounts. There is no
  authors'-own "topology accounts for X% of failures" figure to cite; say
  System Design and Inter-Agent Misalignment are the two largest categories
  by a wide margin, not a combined percentage.
- Same model, same user prompt, structural change only:
  **+15.6%** task success on ChatDev/ProgramDev from adding a *high-level task
  objective verification step*; **+9.4%** from enforcing role hierarchy so the
  superior agent has final say.

**Read the numbers correctly.** Category figures are share of total failure
annotations; per-mode figures in §6 are trace-level prevalence. Different
denominators — **they do not sum to their category totals.** Do not add them.

**What the paper does NOT say.** It does not say topology always beats prompting.
In its AG2/MathChat case study the topology change was *not* statistically
significant on GPT-4 (Wilcoxon p = 0.4) while the improved prompt was; on GPT-4o
both were significant (p = 0.03). The paper's actual conclusion is stronger and
less convenient: **isolated tactical fixes — prompt OR topology — are
inconsistent across models, and reliability requires structural redesign.**

Operational directive you must internalize:
> When an agentic task fails, **classify the failure mode before you change
> anything**, and prefer the fix that survives a model swap. A standing
> deterministic gate survives; a prompt tweak that worked once on one model may not.

**Tooling.** The taxonomy ships as a pip package: `pip install agentdash`. Point it
at a failed Cowork trace to get MAST labels + reasons before you touch the graph.
This is the cheapest available implementation of "classify first."

---

## 1. Node taxonomy

Not every node is an agent. Six kinds. Naming them explicitly is half the work.

| Node | Executes | Judgment? | Reversible? | VELTH examples |
|---|---|---|---|---|
| **RECON** | agent, read-only | yes | always | live-schema reflection, grep call sites, `git log`, reading a route |
| **CONTRACT** | agent → artifact | yes | always | data contract, invariant list, acceptance criteria |
| **BUILD** | agent, writes files | yes | locally (git) | write ORM/repo, edit route, author test |
| **DETERMINISTIC** | code, no LLM | **no** | n/a | `risk_classifier.py` RPZ=S×W, `guardrail_no_supabase.py`, ruff, `alembic check`, pytest, schema diff |
| **ROUTER** | code or cheap agent | minimal | n/a | which vertical? which model tier? is this domain blocked? |
| **HUMAN GATE** | Anshu | yes | — | approve contract, run `git commit`, sign DPIA, SiFa Freigabe |

**The prime directive:**
> Put a DETERMINISTIC node wherever a wrong answer is expensive AND checkable.

VELTH already does this at the single most important point in the product:
`risk_class` is never taken from the LLM — always computed in Python (L4 → Nohl
Gate Engine). That is a deterministic node placed at the highest-consequence
junction. Every new graph should ask: *what is this task's `risk_class`?* — then
make that node code, not judgment.

---

## 2. Edges: the transitions that exist, and the ones that must not

An edge is a permitted transition. **Graph engineering is mostly deciding which
edges DON'T exist.**

**Permanent forbidden edges in every VELTH graph:**
- `BUILD ─X→ git write` — Cowork never runs `git add/commit/push/stash/checkout`,
  never touches `.husky/`. Git writes are reachable ONLY from a HUMAN GATE.
- `BUILD ─X→ irreversible external effect` — no deploy, no prod migration apply,
  no send, no delete, without a HUMAN GATE immediately upstream.
- `RECON ─X→ BUILD` — recon may never write. Separate the node; a node that both
  investigates and edits will edit on unverified evidence.
- `BUILD ─X→ self-approval` — an agent may not gate its own output. Verification
  is a different node (FM-3.3 *Incorrect verification*, 9.1% of traces).

**Edge contract.** Every edge carries a payload. Specify it or you get FM-2.4
*Information withholding* — rare (0.85%) but the paper's own worked example
(Figure 3) of how a whole task dies: one agent knew the API's username format and
never passed it on, the other never asked. Write edges as:

```
RECON ──[quoted schema + file:line evidence]──▶ CONTRACT
CONTRACT ──[invariant list + acceptance criteria]──▶ HUMAN GATE
BUILD ──[changed-file list + self-gate results + drafted commands]──▶ HUMAN GATE
```

If you cannot name the payload, the edge is underspecified — that is an FC1
System Design failure (41.8%) waiting to happen.

---

## 3. The checkpoint-width law

The single most reusable rule in this skill.

```
                    irreversibility × blast_radius
checkpoint_freq  ∝  ─────────────────────────────
                     proven_reliability_of_node
```

Read as: gate OFTEN when an action can't be undone and touches shared state; gate
RARELY when it's local and the node has many uneventful reps behind it.

| Action | Irrev. | Blast | Gate |
|---|---|---|---|
| Edit a local file | none | self | never |
| Run ruff / pytest / docker test | none | self | never |
| `alembic merge heads` on a shared branch | high | team | **human** |
| `git commit` | med | self→team | **human** |
| `git push --force` | high | team | **human** |
| Apply migration to prod | absolute | all tenants | **human + second pair of eyes** |
| Write to a shared multi-tenant table | high | all tenants | **human + deterministic guard** |

**Width is a tunable, not a constant.** Start narrow on a new task class, widen
as reliability is proven. Widening ≠ removing: batch the gate (per-wave instead
of per-item), never delete it.

**Gate BEFORE the effect, not after the node.** The industry's most common
human-in-the-loop mistake is pausing after the action has already happened.
Concretely, in LangGraph terms: `interrupt_before` / `interrupt_after` are
**static breakpoints and LangChain's own docs now state they are not recommended
for human-in-the-loop workflows** — they are debugging tools. The supported
mechanism is the dynamic `interrupt()` call placed *inside* the node, on the line
immediately before the side effect, resumed with `Command(resume=...)`; it
requires a checkpointer. This is strictly better than node-boundary gating,
because the pause sits at the exact statement that mutates the world rather than
at an arbitrary graph seam. **All VELTH gates on irreversible actions pause
before the effect, never after.**

**Field evidence (internal, July 2026 migration session — not externally citable).**
The git HUMAN GATE caught four separate state drifts that every agent involved
reported as success: a merge that didn't land, a wrong grep signature, a
NUL-corrupted `.git/HEAD`, and a stale mount serving truncated file reads. Zero
reached a commit. The gate is not ceremony; it is the node that sees what the
others structurally cannot.

---

## 4. State and durability

Every graph needs an explicit answer to: **what survives a node boundary?**

- **Carried state** — the small typed payload on each edge (§2).
- **Persisted state** — what survives session death. In VELTH: git commits,
  memory files, `SESSION.md`, the migration doc. **If it isn't committed or
  filed, it does not exist.** Sessions die; sandboxes get remounted; mounts go
  stale.
- **Checkpoint identity** — what a resumed run keys off. In VELTH: the branch
  name + HEAD SHA. Any resumed session's FIRST action is to verify identity (§7,
  Node 0).

**Idempotency requirement.** Assume any node may re-execute from the top after a
pause. Anything before the gate must be safe to repeat — no double-charging, no
duplicate inserts, no append-that-accumulates. In VELTH terms: prefer
`ON CONFLICT DO NOTHING` / upsert-with-arbiter over blind insert in any node that
might rerun.

FM-1.4 *Loss of conversation history* (2.8%) and FM-2.1 *Conversation reset*
(2.2%) are exactly this failure. Their mitigation is not a longer context window
— it's persisting state OUTSIDE the conversation. Anthropic's context-engineering
guidance points the same way: retrieve just-in-time from the live environment
rather than relying on what happens to still be in the window.

---

## 5. Pattern selection

Match topology to task shape. **Sophistication should follow workload complexity,
never precede it.** Anthropic's current working definition — *agents are LLMs
autonomously using tools in a loop* — is deliberately minimal; add structure only
when the simpler thing demonstrably fails.

| Task shape | Topology | VELTH example |
|---|---|---|
| Known steps, stable order | **Pipeline / prompt chaining** (predefined code path) | L0→L8 doc pipeline, per-domain migration loop |
| Different inputs need different handling | **Router** → specialist | vertical classifier, MoE model routing (Llama 8B / Mistral 22B / Claude) |
| N genuinely independent subtasks | **Parallelization: fan-out → join** | 7 red-team verticals, multi-file recon |
| Subtasks unknown until runtime | **Orchestrator-worker** | "migrate this domain" — file count unknown a priori |
| Clear eval criteria + iteration pays | **Evaluator-optimizer** | GBU quality gate (L5), SiFa-expert scoring, L8 Gemini judge |
| >50 truly independent concurrent units | **Swarm** | *nothing in VELTH today* |
| High stakes, cost premium justified | **Debate** | *avoid — not justified for VELTH task shapes* |

**Default for VELTH:** pipeline with deterministic gates + one human checkpoint.
Escalate only on evidence.

**Anti-pattern — dynamic handoff/swarm on a task a pipeline handles.** The
dominant failure is the infinite handoff loop (A→B→C→A) because *nobody owns the
task*. Every VELTH graph has exactly one owner per run. Note the paper's own
finding here: AppWorld's star topology with no predefined workflow shows the
highest rate of premature termination (FM-3.1) precisely because termination
conditions are never obvious to anyone.

---

## 6. MAST failure modes → topology countermeasures

The diagnostic table. When a run fails, classify first (`agentdash` if you want it
automated), then apply the **structural** fix — not a prompt tweak.
Percentages = trace-level prevalence across MAST-Data (n = 1,642).

### FC1 · System Design Issues (41.8% of failures)
| Mode | % | Topological countermeasure |
|---|---|---|
| 1.1 Disobey task specification | 11.8 | CONTRACT node before BUILD; acceptance criteria are the edge payload |
| 1.2 Disobey role specification | 1.5 | Delete the forbidden edge (make it structurally impossible, not "please don't") |
| 1.3 **Step repetition** | 15.7 | Persist completed-step state outside context; router checks "already done?" |
| 1.4 Loss of conversation history | 2.8 | Persist to file/commit, not chat |
| 1.5 **Unaware of termination conditions** ☠ | 12.4 | **Explicit DONE predicate as a deterministic node** |

### FC2 · Inter-Agent Misalignment (36.9%)
| Mode | % | Topological countermeasure |
|---|---|---|
| 2.1 Conversation reset | 2.2 | Externalized state + identity check on resume |
| 2.2 Fail to ask for clarification | 6.8 | STOP CONDITIONS list; make "halt and ask" a first-class legal transition |
| 2.3 Task derailment | 7.4 | Router re-checks goal each phase; scoped node charters |
| 2.4 **Information withholding** ☠ | 0.85 | Typed edge payloads. Low frequency, high lethality — the paper's canonical worked failure |
| 2.5 Ignored other agent's input | 1.9 | Join node must consume ALL inputs; assert on missing |
| 2.6 **Reasoning-action mismatch** | 13.2 | Deterministic node re-derives the claim from artifacts (evidence rule, §7) |

### FC3 · Task Verification (21.3%)
| Mode | % | Topological countermeasure |
|---|---|---|
| 3.1 Premature termination | 6.2 | DONE predicate + "all contract items asserted?" gate |
| 3.2 No/incomplete verification | 8.2 | Verification is a NODE, never a step inside BUILD |
| 3.3 **Incorrect verification** | 9.1 | **Multi-level:** low-level (compiles/lints) AND high-level (objective met) |

> Insight 3 in the paper, verbatim in spirit: sole reliance on final-stage,
> low-level checks is inadequate. Their worked example is a ChatDev chess program
> that compiles, passes review, and is unusable because nobody validated it
> against the actual rules of chess. **VELTH equivalent: a green ruff run is not a
> green migration.** The docker integration test asserting the DATA CONTRACT is
> the real verifier. This is also the intervention that bought +15.6%.

---

## 7. The VELTH standard graph

Reusable spine. Instantiate per task; delete nodes only with a stated reason.

```
        ┌─────────────────────────────────────────────┐
        │ 0. SELF-DIAGNOSIS  (deterministic, first)   │
        │    identity + reliability of the workspace  │
        └───────────────┬─────────────────────────────┘
                        │ verified ──▶ proceed
                        │ mismatch ──▶ HALT + report (never build)
                        ▼
   ┌────────────┐   evidence   ┌──────────────┐   contract   ┌────────────┐
   │ 1. RECON   │─────────────▶│ 2. CONTRACT  │─────────────▶│ 3. GATE 🧑 │
   │ read-only  │  (quoted)    │  invariants  │              │  approve   │
   └────────────┘              └──────────────┘              └─────┬──────┘
                                                                   │
                        ┌──────────────────────────────────────────┘
                        ▼
                  ┌───────────┐        ┌──────────────────────────┐
                  │ 4. BUILD  │───────▶│ 5. VERIFY (fan-out, det.)│
                  │  writes   │◀───────│ lint·types·unit·docker·  │
                  └───────────┘  red   │ guardrail·single-head    │
                                       └───────────┬──────────────┘
                                             green │
                                                   ▼
                                       ┌────────────────────────┐
                                       │ 6. GATE 🧑 irreversible│
                                       │  commit / push / apply │
                                       └───────────┬────────────┘
                                                   ▼
                                       ┌────────────────────────┐
                                       │ 7. JOIN / integrate    │
                                       │ merge heads, reconcile │
                                       └────────────────────────┘
```

### Node 0 — SELF-DIAGNOSIS (mandatory, deterministic, no permission needed)

Never build on an unverified workspace. Branch on evidence:

```
IF identity check fails (rev-parse errors / ref unresolvable)
   → workspace corrupt or mount stale. Do NOT repair blindly.
     Report the exact failure + prescribed remedy. HALT.

ELIF identity ≠ expected (wrong SHA / branch)
   → report actual vs expected, draft (don't run) the corrective commands. HALT.

ELIF identity OK but a content fingerprint disagrees
   → verify via a SECOND independent transport before trusting either.
     Byte-count agreement is weak; content hash agreement is proof.
     If they disagree → reads are unreliable → HALT.

ELSE → verified. Proceed. State what you verified, with the values.
```

**Two-transport rule.** If a workspace has ever served a bad read, one channel
agreeing with itself proves nothing (stale caches are stable across re-reads).
Compare `hash(file)` across two independent paths. Identical hashes = proof.

### Node 1 — RECON (read-only, evidence-producing)
- Output is **quoted evidence**, never inference. `file:line`, schema dumps,
  command output.
- **Reflect live, don't infer.** Live-schema reflection has repeatedly overturned
  code-derived assumptions: phantom tables that don't exist, a "tenant boundary"
  that was a public directory, an FK that was never there. This is just-in-time
  retrieval — the same reason Claude Code uses glob/grep over a pre-built index:
  a stale index is worse than no index.
- Anything unverifiable → tag `[UNVERIFIED: <exact command a human should run>]`.

### Node 2 — CONTRACT (the highest-ROI node in the graph)
For any change touching data, the contract enumerates every property that must
survive:
- ownership filters / tenant partitions (a dropped one = cross-tenant leak — the
  worst outcome in VELTH's ranking)
- RLS policies, incl. *who may write* (service-role-only writes are an
  immutability mechanism, not a detail)
- `ON CONFLICT` arbiters, UNIQUE/CHECK/NOT-NULL, FK cascade
- exact returned shape (dict keys, types, projection — what must NOT be returned
  is as load-bearing as what must)

**System Design and Inter-Agent Misalignment are, by a wide margin, the two
largest MAST failure categories (44.2% and 32.3% of traces respectively,
n=1,642 — see §0; they are not mutually exclusive per trace, so do not sum
them).** This node is where you buy that down.

### Node 3 / 6 — HUMAN GATES
- **Gate 3 (contract)** — cheap. Wrong assumptions die here for free.
- **Gate 6 (irreversible)** — pause *before* the effect. Agent presents: changed
  files, self-gate results, **drafted copy-paste commands**. Human executes.
- Agent NEVER executes. Agent ALWAYS drafts, so the gate costs one paste.

### Node 5 — VERIFY (deterministic fan-out)
Multi-level, per FM-3.3:
- **Low-level:** ruff check + format, types, `alembic check`, single head
- **High-level:** docker integration test asserting **each contract item**, plus
  `guardrail_no_supabase.py` (an executable architectural invariant — the pattern
  to replicate: `guardrail_no_llm_risk_class`, `guardrail_no_unscoped_query`,
  `guardrail_no_mojibake`)
- **Cross-family judge:** the checker must not be the maker's family (VELTH: Gemini
  judges Claude output at L8). Same-family self-review shares blind spots.
- **Scope rule:** a gate is green when THIS change's scope is green. Pre-existing
  unrelated failures are noise — record them, don't let them block forever. A
  standard that can never be met is not a standard.

### Node 7 — JOIN
Where parallel work reconciles: merge alembic heads to one, resolve conflicts,
re-verify on the INTEGRATED result (feature-branch green ≠ integration green).

---

## 8. Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| **Batch-everything, verify at the end** | No checkpoint; a defect in item 3 is buried under 12 more, unbisectable | Gate per unit; batch the *human interaction*, not the *verification* |
| **Agent gates itself** | FM-3.3; verifier and builder share the same blind spot | Verification is a separate node, ideally a different model family |
| **Trust the report, not the artifact** | FM-2.6 reasoning-action mismatch (13.2%) | Re-derive from the artifact; quote, don't paraphrase |
| **Pattern-match instead of read** | A grep for an assumed signature "proves" absence of code that's present in another form | Read the function body; quote it |
| **Prompt-patching a topology bug** | Tactical fixes are model-dependent and inconsistent (p=0.03 on one model, p=0.4 on another) | Classify the failure mode first, then fix structurally |
| **No DONE predicate** | FM-1.5 ☠ (12.4%) — runs forever or stops early | Explicit, checkable termination condition |
| **Scope elasticity under pressure** ("do it all in one go") | Converts a sized plan into an unreviewable blob; maximizes the outcome you rank worst | Re-derive the plan from constraints, not from urgency |
| **Bulk fix without inventory** | A repo-wide replace breaks the three files where the "corruption" is intentional | Inventory → classify (real / cosmetic / **intentional, exclude**) → fix per class |

---

## 9. Graph spec template

Fill this in BEFORE writing any Cowork prompt. If a row is blank, the graph is
underspecified.

```markdown
## GRAPH SPEC: <task>

GOAL (one sentence, testable):
DONE PREDICATE (deterministic, checkable):
BLAST RADIUS: local | branch | team | tenant | all-tenants
IRREVERSIBLE ACTIONS: <list — each needs a gate immediately before>

NODES
| # | Node | Type | Owner | Input payload | Output payload | May write? |
|---|------|------|-------|---------------|----------------|------------|

FORBIDDEN EDGES (structurally impossible, not "please don't"):
- BUILD → git write
- <task-specific>

DATA CONTRACT (if data is touched):
- partitions/ownership filters:
- RLS (incl. who may write):
- conflict arbiters / constraints:
- exact output shape:
- [UNVERIFIED: ...] items and the command that resolves each

VERIFY NODES
- low-level:
- high-level (asserts each contract item):
- judge family (must differ from maker):

HUMAN GATES
- gate 1 (contract approval): <what's presented>
- gate 2 (irreversible): <what's presented + drafted commands>
- checkpoint width + rationale:

STOP CONDITIONS (halt + report, never push through):
- unconfirmable contract item
- ambiguous partition/RLS/conflict semantics
- self-diagnosis branch that doesn't resolve cleanly
- any claim not backed by a quoted line of code or command output
- <task-specific>

BATCHING: gate every <unit>; rationale:
```

---

## 10. Operating rules (VELTH-specific, always in force)

- **Three actors.** chat-Claude specs + gates contracts · Cowork builds and
  self-verifies · Anshu runs every host command and every git write.
- **Windows/PowerShell.** `uv run --no-sync` always. `cmd /c dir /s /b` to find,
  `findstr /s /n /i` to search, `Get-Content` to read, `Select-String` for simple
  patterns only. Quote `"stash@{0}"` — PowerShell eats braces. Explicit staging
  only, never `git add -A`. `$env:HUSKY=0`. `Remove-Item .git/index.lock` when
  "could not write index".
- **Encoding.** German text written via Python with `encoding='utf-8'`;
  UTF-8-no-BOM; verify umlauts at the byte level (`ü` = `c3 bc`, `ä` = `c3 a4`)
  after any edit touching them.
- **RADAR CHECK** before any shared-file change: confirm the CURRENT shared branch
  first (`git branch --show-current`), then `git fetch origin` and
  `git log --oneline origin/<that-branch> -10`. Do not hardcode `main` — during the
  repo-layer migration the real shared branch was `mig/repo-migration` for weeks, and
  a `main`-only check would have reported a clean branch that was hundreds of commits
  behind.
  + `git status`.
- **Karpathy rules:** Think Before Coding · Simplicity First · Surgical Changes ·
  Goal-Driven Execution.
- **Evidence rule:** every state claim carries a quoted line of code, schema
  output, or command output. No claim from memory of what code "should" look like.
- **VELTH priority order — never reorder:**
  `data integrity > correctness > completeness > speed`.
  A cross-tenant leak or silently-unfaithful migration outranks finishing.

---

## Sources

- Cemri, M., Pan, M. Z., Yang, S., et al. (2025). *Why Do Multi-Agent LLM Systems
  Fail?* arXiv:2503.13657v3 (NeurIPS 2025). All MAST figures, failure-mode
  definitions, and intervention deltas above. Library: `pip install agentdash`.
  Dataset: `huggingface.co/datasets/mcemri/MAST-Data`. **Category prevalence
  re-verified against the full paper text 2026-08-26**: 44.2%/32.3%/23.5% is
  Figure 1's full-corpus (n=1,642) breakdown; 41.8%/36.9%/21.3% is Figure 4's
  210-trace subsample breakdown — both real, different denominators, do not
  sum either. No "~79%" combined figure exists in the paper.
- LangChain (2026). *Interrupts* — LangGraph docs. Basis for the "pause before the
  effect" rule and the deprecation of static breakpoints for HITL.
- Anthropic (2024). *Building Effective Agents*. Basis for the §5 pattern table
  (prompt chaining, routing, parallelization, orchestrator-workers,
  evaluator-optimizer) and the "simplest thing that works" rule.
- Anthropic (2025). *Effective Context Engineering for AI Agents*. Basis for the
  agent definition, just-in-time retrieval, and the §4 persistence argument.
- Internal VELTH session notes, July 2026 (§3 field evidence) — not externally
  verifiable; retained as operational experience, labelled as such.
