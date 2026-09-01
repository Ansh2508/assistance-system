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
