---
name: velth-truth-gate
description: The terminal node every VELTH task must pass before any success claim leaves the session. Load it at the MOMENT OF REPORTING — before writing "done", "fixed", "green", "passed", "verified", "working", "all tests pass", "ready to commit", or any status summary — and load it when reviewing a report someone else produced. Every other VELTH skill governs how work gets DONE; this one governs whether the CLAIM ABOUT that work is TRUE. Use it whenever a test suite goes green, a gate reports clean, an agent says it finished, a fix is proposed with a stated root cause, a number or citation is about to be asserted, or a handoff/commit block is being written. Not a code-quality check (velth-review), not an output check (velth-doc-verify), not a process check (velth-loop) — those all verify the work. This verifies the report, which is the only artifact a human actually acts on.
---

# Truth gate — the report is an artifact, and it can be false while everything else is fine

## Why this exists, in one number

**75.8%** of self-assessing coding-agent trajectories that made an explicit status claim were
**false successes** (arXiv 2606.09863, *From Confident Closing to Silent Failure*, FAGEN@ICML2026
— 9,876 tau2-bench trajectories across 8 model families plus 1,879 AppWorld trajectories across 4).

Separately, **27–78% of benchmark-reported successes are procedurally corrupt** — the terminal
state looks right but a mandatory constraint was violated on the way. Under integrity gating,
Pass^4 reliability (success across repeated attempts, not to be confused with Pass@4
solvability, which stays much higher — 0.22–0.87 gated in the same paper) collapses from
headline rates to **2–24%**, and **model rankings reverse** (arXiv 2603.03116).

Sit with what that means. Not "agents sometimes fail" — everyone knows that. **Agents fail and
then report success**, and the report is the only thing a human sees. Every other skill in this
library makes the *work* better. None of them check the *claim*.

### The mechanism, which is the actionable part

2606.09863 identifies exactly what substitutes for truth in a false success:

- **"Confident closing language"** — fluent, definitive summary prose
- **"Coarse action-sequence volume"** — many tool calls, therefore surely something happened

...used **instead of verifying actual state changes.**

That is the whole failure. An agent that ran twenty commands and wrote a confident paragraph has
produced two signals, and neither is evidence. **The only evidence is the changed state.**

### And the counterintuitive finding that shapes this gate's design

Lightweight **TF-IDF detectors** hit AUROC 0.83 / 0.95 and recovered **4–8× more false successes
than the best LLM judge** at the same flag rate, at **3,300× lower latency**. LLM judges never
exceeded AUROC **0.65** — barely above coin-flip on one benchmark.

**So this gate must be mechanical, not another model asking a model whether it did well.**
Cheap deterministic checks beat sophisticated judgement here, by a wide margin, and that is a
measured result rather than a preference. Where this skill offers a choice between "run a command"
and "reason about it", run the command.

---

## The gate — five questions, in order, before any status claim

Fast by design. If it takes more than three minutes the claim was too vague to check.

### 1. State, not story: what CHANGED, and how do I know?

For every claimed effect, name the observable state and the command that observed it.

| Claim | Not evidence | Evidence |
|---|---|---|
| "Tests pass" | "I ran the tests" | The pass/fail line, with counts and a plausible duration |
| "The file is updated" | "I wrote the file" | `sha256sum` or a re-read of the changed region |
| "The fix works" | "The logic is now correct" | The test that failed before and passes now |
| "It's wired up" | "I added the call" | The value observed arriving at the far end |
| "Migration applied" | "alembic ran" | `alembic heads` = 1, and the table exists |

If the evidence column is empty, the honest report is **"changed, not verified."** That phrase is
always available and it is never wrong.

### 2. Could this be green for the wrong reason?

Silent green is the dominant failure mode in this repo — **three live instances found in VELTH's
own verification stack in one session**, which is why this question is second and not last:

- **A skipped run reads as a pass.** `sssss` is not `.....`. `61 skipped in 1.24s` is not a pass;
  61 tests didn't run. Confirm the literal word **passed** and a duration consistent with real work.
- **A missing dependency reads as a pass.** `doc_verify.py` computed `judge_failed = verdict.get("pass") is False`.
  With no `GEMINI_API_KEY` the judge returns `None`, `None is False` is `False`, and the script
  printed `RESULT: PASS` having never run half its verification.
- **A tautology reads as a pass.** `if not X: assert X is None` cannot fail for any input.
- **An empty comparison reads as a pass.** Two `AnalysisResult`s both empty serialise identically.
  A determinism test built on that merged and proved nothing.
- **A swallowed exception reads as empty, not as an error.** A repository fake whose signature had
  drifted raised `TypeError`; the caller caught it by design and returned `[]`. Eleven tests went
  red for a reason that looked like logic and was interface drift.
- **A count-based gate rewards a vacuous test.** It raises the baseline. See velth-test-strategy
  RULE ZERO.

The generalisation: **ask what this check would output if the thing it checks did not exist.**
If the answer is "the same thing", it is not a check.

### 3. Tier every claim: executed / read / inferred / relayed

Label each load-bearing statement. Only the first two can support a DONE.

| Tier | Meaning | May support a success claim? |
|---|---|---|
| **EXECUTED** | I ran it and observed the output | Yes |
| **READ** | I opened the file/page and quote it | Yes |
| **INFERRED** | Reasoned from what I read | No — mark it, or verify it |
| **RELAYED** | An agent, a doc, or a prior session said so | No — verify or attribute it |

Fabrication lives at RELAYED and INFERRED, and it is confident there. Real instances from one
session: a dispatch specified `.successes` and `.total_signals` on a dataclass that had neither;
a subagent reported two arXiv ids as invented when one was real; a skill's §0 described per-claim
date markers its own body did not contain; a skill edit reported "Successfully replaced string" —
true, EXECUTED for the tool call itself — while the surrounding file content was INFERRED from an
old, partial view rather than READ fresh, landing new content in the wrong position with no error
from the tool to reveal it.

**Cheap rule:** if a field name, line number, function signature, file path, or citation appears
in a report, it must be EXECUTED or READ. Never RELAYED. Files do not hallucinate; summaries do.

**The rule applies to the dispatch itself, not only to what an agent reports back.** A dispatch
that states "confirmed by direct inspection," "verified," or "already checked" is making a claim —
and from the executing agent's own position, that claim is RELAYED until independently
re-verified, no matter how genuinely it was checked upstream. Real instance, 2026-08-14: a
dispatch asserted a third PDF attachment was "genuinely empty (3 blank pages, confirmed by direct
inspection)." True for that upload — but the agent receiving the dispatch had a DIFFERENT upload
under a similar name, accepted the claim anyway, and proceeded on two of three required source
documents. The missing one held the answer to the single question the resulting plan had flagged
as blocking. The check that caught it wasn't smarter reasoning — it was refusing to let "the
dispatch already said so" stand in for the agent's own READ.

### 4. Root cause is a hypothesis until proven

Measured accuracy of AI review claims (Jin & Chen, *Are LLMs Reliable Code Reviewers?
Systematic Overcorrection in Requirement Conformance Judgement*, Automated Software
Engineering, 2026, arXiv:2603.00539):

| Claim type | Accuracy |
|---|---|
| Symptom detection — "something is wrong here" | **91.2–100.0%** |
| Root-cause diagnosis — "here is why" | **38.2–75.2%** |

An excellent smoke detector and a mediocre fire investigator. So a report may state a symptom as
fact and **must** mark a cause as a hypothesis until a demonstration exists — the minimum being:
the change that makes the symptom disappear, and the check that it reappears without it.

Never write "the cause was X, so I fixed X." Write "X reproduces it; removing X removes it."

### 5. What did I NOT do that could be read as done?

False success is often omission read as completion. State the negative explicitly:

- Tests **written but not run** (no Docker, no key, no network) → say so, first line
- Files **written but not committed**, or written to a sandbox rather than the real machine
- A gate **skipped**, not passed
- Work **out of scope** that a reader might assume was included
- Numbers **taken from a summary** rather than the source

A report with no negative section is suspicious on its face. Real work has edges.

---

## The report template

Everything above compresses to this. If a section is empty, say so rather than deleting it —
the absence is information.

```
ENVIRONMENT: <where this ran; what could NOT run here>

DONE (executed, with evidence):
  - <claim> -> <command> -> <observed output>

CHANGED, NOT VERIFIED:
  - <what was touched but not proven>

NOT DONE / OUT OF SCOPE:
  - <what a reader might assume happened and didn't>

HYPOTHESES (not facts):
  - <any root cause without a demonstration>

CLAIM TIERS:
  - executed: <n>   read: <n>   inferred: <n>   relayed: <n>
```

---

## Sources — tiered, because a truth gate that cites loosely is self-refuting

**Tier 1 — primary, opened and read, verified 2026-08-14, RE-VERIFIED 2026-08-26 by an
independent agent fetching all three papers directly:**

- **arXiv 2606.09863** — *From Confident Closing to Silent Failure: Characterizing False Success in
  LLM Agents* (FAGEN@ICML2026, submitted 1 Jun 2026). 75.8% false success among self-assessing
  AppWorld coding trajectories with explicit status claims; 45–48% of failures in single-control
  tau2-bench; 9,876 + 1,879 trajectories, 8 + 4 model families. Confident-closing-language and
  action-volume substitute for state verification. TF-IDF detectors AUROC 0.83/0.95, 4–8× more
  false successes recovered than the best LLM judge at equal flag rate, 3,300× lower latency;
  LLM judges never above AUROC 0.65. **Source for this skill's core claim and its mechanical
  design. 2026-08-26 re-check: every number above confirmed verbatim against the fetched abstract
  — no correction needed.**
- **arXiv 2603.03116** — *Beyond Task Completion: Revealing Corrupt Success in LLM Agents through
  Procedure-Aware Evaluation* (Cao, Driouich, Thomas, Amadeus France). 27–78% of reported
  successes procedurally corrupt (Mistral: 76% Retail / 78% Airline; even GPT-5 ~27%); gated
  **Pass^4** (not Pass@4 — a distinct metric in the paper for reliability across k=4 trials)
  collapses to 2–24%; model rankings reverse (confirmed: Mistral beats Kimi-K2-Thinking 0.68 vs
  0.61 under standard utility, Kimi beats Mistral 0.27 vs 0.16 under gated utility). **Source for
  §1's state-not-story rule. 2026-08-26 re-check: numeric ranges confirmed against Table 3 and
  Section 5.1 of the full text; corrected "Pass@4" to "Pass^4" in this document's own body text
  above, which had the metric name wrong.**
- **arXiv 2603.00539** — Jin & Chen, *Are LLMs Reliable Code Reviewers? Systematic Overcorrection
  in Requirement Conformance Judgement* (Automated Software Engineering, Springer, DOI
  10.1007/s10515-026-00638-5, 2026). **2026-08-26 re-check against the paper's own Table 3
  (page 20): this document previously stated 94–100% / 41–71%. The paper's actual reported
  ranges are 91.2–100.0% (SymptomMatch, low end Mistral-3.1 on QuixBugs) and 38.2–75.2%
  (BugMatch, range Llama-3.1 on QuixBugs to Claude-4.5 on MBPP) — both corrected in §4 above.
  The qualitative finding this skill relies on (symptom detection near-ceiling, root-cause
  diagnosis substantially weaker) is strongly and correctly supported by the paper; only the
  specific numbers were wrong, likely inherited from an uncorrected paraphrase rather than the
  primary table.**

**Tier 2 — secondary, directionally useful, not load-bearing:** *Wired for Overconfidence*
(arXiv 2604.01457) on inflated verbalized confidence — consistent with the above, not verified in
this pass.

**What this correction demonstrates, which is worth keeping as part of the skill rather than
just fixing silently:** this document taught RELAYED-vs-READ tiering and got flagged Tier 1 —
"opened and read" — on a citation whose specific numbers turned out not to match the primary
source. The error survived one full editing pass because "looks like it came from the paper"
and "actually came from the paper" are not the same signal, and nothing forced a second,
independent check. Re-verifying your OWN prior Tier-1 claims periodically, not only claims made
by others, is in scope for this skill — see the "skills decay" principle in
`research-simulate-encode`.

**Internal (VELTH, all observed directly in one session):** `doc_verify.py`'s `is False` silent
green · `velth-review`'s tautological UUID property test · `test_confirmation_determinism_invariant`
comparing two empty results and merging · `FakeContextRepository.list_rules` signature drift
swallowed into `[]` · count-based gates in velth-test-strategy that reward a vacuous test.

---

## Where this sits

`velth-loop` runs the work. `velth-test-strategy` decides what the tests must prove.
`velth-review` checks the code. `velth-doc-verify` checks the output document.
**This runs last, on the report, and it is the only one that assumes all of the above may have
passed while the claim is still false.**

If it fires and the honest report is weaker than the hoped-for one, the honest report is the
deliverable. A human who is told "changed, not verified" can act correctly. A human who is told
"done" when it isn't cannot, and finds out later at a cost set by how long the lie survived.
