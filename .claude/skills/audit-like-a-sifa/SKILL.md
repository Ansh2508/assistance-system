---
name: audit-like-a-sifa
description: Anshu's operating system for verifying AI-produced work when he cannot read the code fluently. Use this skill whenever he is about to accept, gate, merge, stage, or sign off on anything an AI produced — code, tests, migrations, documents, research claims, or a plan — and whenever he asks "is this right?", "did this actually work?", "can I commit this?", "review this diff", "check these tests", or pastes terminal/PowerShell output for judgement. Also use it when writing a dispatch for a coding agent, when an agent reports success, when a test suite goes green, when deciding what to build next, and when a claim cites a paper, a number, or a line reference. It converts his existing expert-level safety-engineering instinct (SiFa, hazard analysis, ArbSchG §5) into a verification method for software, so he stops needing to read code fluently in order to catch the defects that matter.
---

# Audit like a SiFa

## Why this exists

Anshu runs VELTH. He directs very large amounts of AI engineering capability, he runs
his own gates, and he refuses to let an agent make the final commit. Those instincts are
right and rare. The gap is narrow and specific:

> His gate catches *"does it run."* It does not catch *"does it mean anything."*

A green test suite is not evidence. In one real session, a determinism test was **merged
into the main working branch while comparing two empty results** — it passed, it proved
nothing, and nothing in the pipeline noticed. In the same session a repository fake
drifted from the real interface and the code silently returned "no rules" instead of
failing, because the caller swallowed the error by design.

He does not need to become a programmer to catch these. He is already an expert at
exactly this task in another domain. A SiFa walks into a Betrieb and asks: what can hurt
someone here, what control is supposed to prevent it, is that control *actually present
and effective*, and if it failed would anyone find out? That is the same question a code
reviewer asks. **This skill is the translation layer.**

## The one thing to internalise

**Vigilance is not a strategy.** Parasuraman & Manzey (2010) found automation
complacency and automation bias affect *naive and expert operators alike*, "cannot be
overcome with simple practice", and "cannot be prevented by training or instructions" —
and they persist in teams, not just individuals. Attention is the mechanism, and
attention is a finite resource that automation quietly drains.

So "I'll be careful" will fail, reliably, no matter how experienced he gets. The only
things that work are **structural**: a fixed question set that runs whether or not he
feels sharp, a hard budget, and a ratchet that converts every caught defect into an
automatic check so it can never depend on his attention again.

Build the structure. Do not rely on the vigilance.

---

## The Questions

Run these on every change, in this order. Q1–Q4 are the original set; Q5 was added
2026-08-14 after direct experience. Together they take about fifteen minutes and catch a
different class of defect than "did the tests pass."

### Q1 — The deletion test (catches vacuous tests)

> **"If I deleted the feature this tests, would this test fail?"**

If the honest answer is no or "not sure", the test is decoration. This is manual
mutation testing, and it is the single highest-yield question available.

Google ran this industrially across 24,000+ developers, 1,000+ projects and 776,740
changelists (arXiv 2102.11378). Two findings transfer directly:

- **Scope it to the diff.** Naively mutating everything produced a median of **820**
  mutants per changelist — unusable. Restricting to changed lines and suppressing
  uninteresting code cut it to a median of **7**. Ask Q1 only about what changed.
- **Aim for "productive."** Their term for a mutant worth surfacing: one where killing
  it would genuinely improve the suite. Applied here: don't interrogate every assertion,
  interrogate the one that is supposed to prove the *feature's whole point*.

Concretely, for each new test: name the ONE line of production code it exists to defend.
If it cannot be named, the test is ceremony.

### Q2 — The write/read test (catches schema and data defects)

> **"What does this write, and what reads it?"**

Most defects that survive review are not logic errors, they are *coupling* errors: a
column nobody reads, a field written and silently ignored, a name that two modules spell
differently. He does not need to read the algorithm to catch these — he needs to read the
data flow.

Real example from his own codebase: `hazard_id` is accepted at the API, forwarded through
the save path, and then **silently dropped at storage in both rule systems** — so a
safeguard built on it (the orphaned-rule check) is structurally incapable of ever firing.
That is a Q2 defect. No algorithm knowledge was required to find it. Just: who writes it,
who reads it, do those two sets overlap.

See `references/reading-diffs-and-schemas.md` for how to actually do this without
fluency.

### Q3 — The uninvited-change test (catches scope creep and collateral damage)

> **"What changed here that I did not ask for?"**

Agents fix things they were not asked to fix, rename things, and "improve" things. Each
of those is an unreviewed change riding along inside a reviewed one. Read the file list
before the file contents: a file you did not expect is worth more attention than a line
you did not understand.

### Q4 — The detection test (catches the defects nobody will ever report)

> **"If this were wrong, how would I find out?"**

This is the deepest question and the one his domain makes him unusually good at. In
safety terms it is the difference between a hazard that announces itself and a hazard
that doesn't.

The canonical VELTH example: a wrongly learned `never_include` rule silently removes a
real hazard from a legal document. Nobody complains, because the thing that would have
complained is the missing item. The feedback signal is **censored** — its absence is not
evidence of correctness. Any metric built on "how often was this overridden" will rate the
most dangerous rules as the safest.

Ask Q4 of every feature. If the answer is "we'd find out when someone gets hurt" or "we
wouldn't", that is the finding — bigger than any bug in the diff.

### Q5 — The confident-closing test (catches false success reported as true)

> **"Did the environment actually change, or did the agent just say it did?"**

*Added 2026-08-14, after an `alembic heads` check was read as successful because a regex
matched the substring "(head)" **inside a printed error traceback**, not inside real output.*

This has its own dedicated skill now — **`velth-truth-gate`**, loaded at the moment ANY
status claim is written, not only when reviewing one. It carries the full research (75.8%
false-success rate in self-assessing coding agents; mechanical checks beat LLM judges by 4-8x
at 3,300x lower cost) and a five-question gate. Load it alongside this one rather than
duplicating its citations here — this entry stays short, for the reviewer's side of the same
problem. **Operational rule: never accept "it worked" from language alone.** Ask for the
mechanical fact underneath the claim, not the sentence describing it.

---

## Calibrating trust in the AI

The most useful number in this whole skill, from *Are LLMs Reliable Code Reviewers?*
(Automated Software Engineering, 2026):

| What the AI says | How accurate | How to treat it |
|---|---|---|
| "Something is wrong here" (symptom detection) | **94–100%** | Believe it. Investigate. |
| "Here is why it's wrong" (root-cause diagnosis) | **41–71%** | Treat as a hypothesis. Verify independently before acting. |

Read that table again, because it is the whole discipline in two rows. **The AI is an
excellent smoke detector and a mediocre fire investigator.**

This matches his own logs exactly. Across one session an agent correctly detected every
symptom it reported, and got the root cause wrong three separate times — proposing a
key-derivation fix when the real bug was an event-loop lifecycle, calling a formula
discrepancy a "test bug" when it was actually two different inputs, and assuming a write
guard broke a test suite when the real cause was a drifted test double. Every time, the
detection was right and the explanation was wrong.

**Operational rule:** when an agent says "the cause is X", the correct next instruction is
never "fix X". It is *"prove X is the cause."*

### One more dimension: who supplied the expected value

*Added 2026-08-14.* Not just whether the AI's explanation is right — whether an AI-written
test can be trusted at all depends on where its expected value came from (Autonoma, *"Claude
Write Tests: When to Trust It and When Not To,"* 2026). Reliable: boilerplate, pure functions,
parameterized cases where the correct answer is derivable straight from the code. Requires
independent verification: business logic, integration flows, permission rules — and
specifically **any test written by the same agent that wrote the code it tests.** The named
mechanism: *"the bug in the implementation becomes the expected value in the test, and CI stays
green."* Tonight's own vacuous determinism test is close to a textbook case of exactly this —
the confirmation-pass code and the test proving its behaviour were written in the same pass,
and the test's construction (two results that both happened to be empty) let a real gap pass
one full review cycle.

### The counterintuitive one about prompt length

The same paper found that **more detailed review prompts make LLM reviewers worse.**
Asking for explanations and proposed corrections pushed GPT-4o's misjudgement rate from
26.2% to 73.2% on one benchmark and 35.9% to 87.9% on another. Claude held up better
(≤7% false positives) but still degraded.

His dispatches are long and detailed, and for *building* that is correct — it is why the
work lands. But for the **review/verify step specifically**, long elaborate prompts
increase noise. Ask the reviewer a narrow, checkable question. "Does this test fail if the
feature is removed?" beats "review this thoroughly and explain everything."

More at `references/ai-calibration.md`.

---

## Budgets, because attention runs out

From the Cisco/SmartBear code-review study — still the largest of its kind:

- **200–400 lines per review session.** Beyond that, detection collapses.
- **Under 500 LOC/hour.** Defect density drops sharply above this rate.
- **60 minutes maximum, then stop.** Performance degrades from fatigue, not ignorance.
- At that pace a review finds **70–90% of defects**. Rushed, it finds almost none.

An 11-file agent output exceeds a single session's budget. Split it or accept that the
back half is unreviewed — but decide that consciously rather than discovering it later.

**Stopping rule:** if he catches himself scrolling rather than reading, the session is
over and its remaining findings are worthless. Stop, ratchet what was found, resume later.

---

## The ratchet (this is how the 100x actually happens)

Because vigilance provably fails, the only durable gain is converting attention into
automation. One rule:

> **Every defect caught by a human becomes an automated check before the session ends.**

Not "later." Not a backlog ticket. The check is part of the fix. A defect that was found
by attention once and is not encoded will be missed next time, because complacency is a
property of the system, not of the person.

This is already his strongest habit — the skills library *is* this ratchet, applied to
process. Extend it from process to code:

- Vacuous test found → a test that fails if the feature is removed
- Fake drifted from real interface → a test asserting the signatures match
- Field written but never read → a guard, or delete the field
- Silent degradation path → make it log loudly, or fail

Ratchets only turn one way. That property is the entire value.

---

## Where his existing strengths should be pointed

He does not need to be told to work harder. He needs to be told where the marginal hour
pays. From Stanford Law's 2026 white paper on vertical-AI moats:

| Asset | Moat strength | What that means for the marginal hour |
|---|---|---|
| Workflows and UX | **Low** — "can be replicated by competitors" | Make it good enough. Stop there. |
| Curated proprietary data | **High** — "the differentiator is the curation" | The catalogs and legal mappings ARE the company. |
| Compliance positioning | **Medium-high** — "switching means re-validating from scratch" | Every signed document deepens the moat. |
| Vertical integration harness | **Medium** | Worth it where it locks in workflow. |

The consequence that changes priorities: **auditability is not a feature, it is the
moat.** A compliance product whose document cannot explain why a hazard is missing cannot
be the system of record — and system-of-record is the entire prize. So a defect like
"rules from two of three scopes are applied but never disclosed in the document" is not a
UI bug. It is moat damage, and it outranks features.

More at `references/frontier-2026.md`, which also covers the real regulatory clocks
(including a post-quantum inventory deadline that lands this year) and an honest read on
which frontier technologies matter to him versus which are noise.

---

## The transfer: his day job is already this job

He is a DACH workplace-safety expert. That is not adjacent to verification — it *is*
verification, in a domain where the stakes are already legally enforced. The mapping:

| SiFa practice | Software equivalent |
|---|---|
| Gefährdungsbeurteilung (hazard assessment) | What can this change break, and how badly? |
| STOP-Prinzip (control hierarchy) | Type system > test > review > docs. Prefer the leftmost. |
| Wirksamkeitskontrolle (effectiveness check) | Q1 — is the control actually controlling anything? |
| Bowtie / barrier analysis | Which barriers stand between this defect and the customer? |
| Beinaheunfall (near-miss reporting) | Every caught-in-review defect is a near-miss. Ratchet it. |
| Work-as-imagined vs work-as-done (Hollnagel) | Spec vs code. The gap is where defects live. |

For the full method — including STPA's unsafe-control-action taxonomy applied to code
review, which is the most powerful single tool here — see
`references/verification-transfer.md`.

---

## What to do with this skill in practice

When reviewing agent output:

1. Before anything else: is there a mechanical fact behind "it worked" — an exit code, a real
   diff, a value read back from disk — or just the agent's own confident sentence? (Q5)
2. Read the **file list** first. Anything unexpected? (Q3)
3. Pick the ONE test that is supposed to prove the feature works. Ask Q1 out loud.
4. For any new field, column or parameter: who writes it, who reads it? (Q2)
5. Ask Q4 about the feature as a whole.
6. Anything the agent claimed as a *root cause* — demand proof, don't accept the fix.
7. If an AI-written test is involved: who wrote the code it checks — the same agent? Trust
   calibration required if so.
8. Ratchet every finding into a check before closing the session.
9. Respect the budget. Stop at 60 minutes.

When writing a dispatch:

- Build steps: long and detailed is correct.
- Verify steps: narrow and checkable beats thorough and open-ended.
- Always require the agent to report **field shapes and line numbers it actually read**
  before it writes code against them. Specs hallucinate; files don't.

## Reference files

- `references/reading-diffs-and-schemas.md` — the 40-hour skill, made concrete. How to
  read a diff and a schema without fluency. Start here.
- `references/verification-transfer.md` — SiFa → software in full. STPA, bowtie, HAZOP
  applied to code review.
- `references/ai-calibration.md` — when to trust an AI, with the numbers and the failure
  taxonomy.
- `references/frontier-2026.md` — what's real on the frontier (regulatory clocks,
  post-quantum, evals as the scarce skill) and what's noise.
