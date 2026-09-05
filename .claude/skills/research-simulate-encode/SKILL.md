---
name: research-simulate-encode
description: For risky architectural decisions - read primary sources in full, validate the claim yourself at your own scale, then encode the decision structurally (not as a comment or convention). Use before committing to a design based on a paper, benchmark, or best practice you haven't personally verified at your own parameters.
---

# Research → Simulate → Encode

Distilled from veOS Sprint 5, where this pattern caught real defects a
"trust the paper" or "trust the benchmark" approach would have shipped.
Grounded in three independently-established practices, not one unified
methodology someone else already named — that combination is this skill's
own synthesis, not a textbook technique. Say so if asked; don't oversell it.

## The four steps, in order

**1. Read primary sources in full.** Not abstracts, not blog summaries of
the paper. Follow citations to primaries. Tag every claim you use:
`[FETCHED-FULL]` (you read the actual text), `[SECONDARY]` (summary only),
`[NOT VERIFIED]`, `[DOES NOT RESOLVE]` (the source doesn't actually support
the claim you wanted it to). A number a secondary source attributes to a
primary is not verified until you've seen it in the primary.

**2. Validate the claim yourself, at your own scale.** A benchmark run at
200,000 rows is not evidence about what happens at 40. A best practice
proven at a company doing millions of transactions a day is not
automatically evidence for a team doing tens a week. Build the smallest
simulation that tests the claim under YOUR actual parameters before
trusting it. This is the same discipline as **Chaos Engineering**
(Netflix, principlesofchaos.org): "a discipline of experimenting on a
system in order to build confidence in the system's capability" — defined
steady state, hypothesize it holds, inject the real variable, try to
disprove it. Don't trust the claim; run the experiment on your own system
or a faithful model of it.

**The pass bar is YOUR actual required scale (current + realistic growth),
not an arbitrary larger one.** A design that fails at n=50,000 but works
cleanly at n=20,000 is not disqualified if n=20,000 is the real target
(current scale plus the documented growth scenario, per
`synthetic_data_for_validation`) — ship it with the scale ceiling stated
explicitly, not silently, and keep improving it later. Don't hold a design
to an untested-need scale nobody asked for; don't hide a real scale limit
either. Both failure modes are real: over-demanding kills useful designs,
under-disclosing ships a landmine.

## When there's no primary source to validate — invention, not a dead end

Sometimes step 1 turns up nothing: real research (including a full
`deep-cross-domain-research` pass) finds zero precedent for the thing you
need. That is not a stop condition. Per the standing project rule (see
`cross_domain_first_principles_invention` memory, set explicitly because a
research pass came back empty for exactly this reason), inventing a
mechanism is sanctioned — but it still has to earn trust, just via a
different route than steps 1-2 above:

- **Ground it in named, real, established mechanisms from OTHER fields**,
  not vibes. Real examples that have worked as transplants: a distributed-
  systems pattern (single write-log, many read-projections) solving an
  AI-output-consistency problem; a compiler's single-IR/multiple-backend
  design solving a "one truth, many renderings" problem; content-addressed
  hashing (Merkle trees) proving two derived artifacts trace to the same
  source; a statistical concept (sufficient statistics, coupling to prevent
  independent-draw divergence) explaining WHY a design should hold together.
  Mathematics — graph theory, information theory, statistics, optimization
  — is worth checking routinely, not just AI/software precedent, because it
  is frequently the actual source of a clean, provably-correct mechanism.
- **Not limited to whatever domains/countries come to mind first.** Search
  wider than the obvious — the closest-fitting mechanism may live in a
  field or a country's engineering practice nobody thought to name at the
  start. Combine 2-3 domains deliberately (an existing domain pattern as the
  base with AI/tech as the addition, or the reverse) rather than defaulting
  to "AI feature bolted onto the problem."
- **Then it must clear a real gate before being trusted**, in this order:
  simulate at your actual required scale (see above), run deliberate
  adversarial tests that try to break the design's own stated guarantee
  (`veos-wiring-and-ai-test`'s pattern: name the exact claim, construct the
  one input built to break it, run it for real), and check at least one
  real-life/production-shaped scenario. Trying several candidate designs or
  parameterizations in simulation and keeping whichever survives is a
  legitimate method here, not just single-shot invent-and-test.
- **Label it invented, explicitly**, the same way a synthetic data row gets
  tagged `is_synthetic` — never let an invented mechanism read as verified
  industry precedent in a doc or a comment. State its known limitations
  (including any scale ceiling found above) next to the decision, not
  buried or omitted.

**3. Encode the validated decision structurally, not conventionally.** A
comment saying "always do X" gets ignored under deadline pressure. A
required function parameter with no override, a database CHECK constraint,
an import-linter rule that fails CI — these survive a tired afternoon. This
is **Design by Contract** (Bertrand Meyer, *Applying "Design by Contract"*,
IEEE Computer, 1992): make the assumption something the machine enforces,
with a real cost to violating it, not something a human is trusted to
remember.

**4. Write the evidence chain into the code, next to the decision.** Paper
→ your own validation → the resulting rule → why. This is
**Architecture Decision Records** (Michael Nygard, "Documenting
Architecture Decisions," 2011) applied inline rather than in a separate
`/adr` directory: "One of the hardest things to track during the life of a
project is the motivation behind certain decisions." Nygard's structure —
context, decision, **consequences** (all of them, not just the positive
ones) — is worth following even in a code comment. The point is a future
reader (including future you) can audit the *reasoning*, not just trust
the conclusion.

## What NOT to do

- Don't skip step 2 because step 1's source is prestigious. A famous paper
  proved a claim under conditions that may not be yours.
- Don't skip step 4 because the code is "self-explanatory." The code shows
  WHAT; only the comment can show WHY, and why is what stops someone from
  reverting your fix in six months because it looked unnecessary.
- Don't claim this four-step pattern is A Recognized Industry Methodology
  when reporting it to someone. It's a real, defensible synthesis of three
  separately-established practices (Chaos Engineering, Design by Contract,
  ADRs) — cite those three by name, not an invented umbrella term.

## Known gap

No formal academic framework exists (as of this research pass) for
"validate a claim at your own scale before trusting a benchmark from a
different one" as a single named practice outside chaos engineering's
production-systems context. Applying it to architectural/data-modeling
decisions (not just runtime resilience) is this skill's own extension —
be honest about that when explaining the practice to someone else.

## Step 4 has a maintenance half, not just a write-once half

The evidence chain in step 4 is a claim about the world at the time it
was written, and the world moves. An independently-established rule from
a different project's own practice: "when research contradicts this
file, the research wins — and update this file in the same session. A
skill or comment that silently goes stale is worse than no skill,
because it launders an outdated assumption as institutional knowledge."
If new research, a new benchmark, or your own later validation
contradicts an encoded decision's stated reasoning, update the comment
and the constraint together, in the same pass that found the
contradiction — don't leave the old "why" standing once it's no longer
true. A `[NOT VERIFIED]`-tagged claim that later gets confirmed or
refuted should have its tag corrected too, not just its conclusion.
