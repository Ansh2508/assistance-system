---
name: research-to-code
description: How to translate a completed, validated research finding (a paper, a benchmark, a simulation result) into an actual code or architecture decision. Distinct from research-simulate-encode, which covers finding and validating the research itself (its steps 1-2); this skill picks up once you have real, validated research in hand and need to decide what specific code change it implies (its steps 3-4, expanded). Load when the research is done and you're staring at a paper or a finding asking "okay, so what do I actually build."
---

# Research → Code

Distilled from real instances in this codebase where a research finding
became a specific, working code change — and from real instances where
research sat unconverted, which is the failure mode this skill exists to
prevent. Complements `research-simulate-encode` (validate the claim) and
`velth-graph-engineering` (design the topology) rather than replacing
either.

## The gap this skill closes

Research-simulate-encode gets you to "I've validated this claim at my own
scale." That is not the same as "I know what code to write." A validated
finding can imply several different, incompatible code shapes, and
picking the wrong one wastes the validation work. This skill is the step
in between: turning a finding into a decision about WHERE it lives in the
system and WHAT specifically changes.

## The four-question translation

For any research finding you're about to act on, answer these in order
before writing code:

**1. Is this a constraint, a default, or a design pattern?**
A constraint (e.g. "Gemini 2.5 Flash-Lite's thinking_budget minimum is
512 tokens, confirmed via a live 400 error") becomes a hard-coded bound
with a comment citing the exact source. A default (e.g. "DPO needs
1,000-10,000 preference pairs to be worth doing") becomes a documented
threshold check, not a hard block — defaults get overridden, constraints
don't. A design pattern (e.g. "generator and verifier should never share
context") becomes a structural separation in the code — two different
functions/processes/model calls that cannot be collapsed into one without
visibly breaking an interface, not a comment asking someone to remember.
Getting this wrong is the single most common way research goes unconverted:
treating a hard constraint as a soft default lets it get silently violated
under time pressure; treating a soft default as a hard constraint produces
brittle code that breaks on a legitimate edge case.

**2. What's the smallest real object in THIS codebase the finding attaches
to?** Not "add a reranking layer" — which table, which function, which
call site. This session's real example: "false premises in a query are a
distinct hallucination trigger from missing data" (arXiv:2504.06438)
attached to exactly one place — `monitoring_agent.py`'s
`_RESEARCH_SYSTEM_INSTRUCTION`, as a new paragraph parallel to the
existing "DATA-QUALITY SKEPTICISM" section, not a new function, not a new
module, not a config flag. Finding the smallest real attachment point is
what keeps a research-grounded change from becoming a "giant refactor plus
unrelated features" (a violation this codebase's own guardrails
explicitly warn against elsewhere).

**3. Does the finding change behavior, or does it change what's
measured/enforced?** Some findings change what the code DOES (the
false-premise fix above). Others change what the code CHECKS — e.g. "DPO
is more vulnerable to poisoning than PPO, and alignment training
deactivates rather than eliminates backdoors" doesn't change any existing
training code (there isn't any yet); it changes what a future gate must
enforce (k≥5 corroboration before a correction pattern earns training
weight) before that code is written. Write the enforcement/measurement
first if the finding is about a system that doesn't exist yet — this
follows Design by Contract's own logic (a required parameter, a CHECK
constraint) applied one level earlier: encode the constraint into the
system's skeleton before there's a body to skeleton.

**4. What would prove this was translated correctly, not just
translated?** A code comment citing a paper is not evidence the code
does what the paper says. This session's real pattern: after adding the
false-premise instruction, the SAME adversarial question that originally
found the gap was re-run live, and the actual model output was read
before/after — not just the prompt diff. A research-grounded change is
only actually converted once you've shown the system's real behavior
moved, the same way a bug fix isn't real until the mutation test proves
it (see `veos-wiring-and-ai-test` for the mechanics of that specific
proof).

## Two real examples from this codebase, worked through the four questions

**Example A — thinking-token budget bounds (`model_router.py`).**
Finding: live-measured Gemini 2.5 "thinking" tokens consumed 69-96% of
`max_output_tokens` before any visible text, confirmed via 4 real,
non-mocked calls, not from documentation alone. (1) Constraint — the
per-model min/max thinking_budget ranges are real, live-verified API
limits, hard-coded as `GEMINI_25_THINKING_BUDGET_BOUNDS`. (2) Attachment
point — exactly the two Vertex-calling call sites that build
`ThinkingConfig`, not a new abstraction layer. (3) Changes behavior — the
output ceiling itself was raised (1200→3000) so real headroom survives
worst-case thinking usage. (4) Proof — a real triage-shaped call was
re-run after the fix and its actual `thoughts_token_count`/
`candidates_token_count` were read, not assumed from the formula.

**Example B — a validated finding that was NOT yet converted, correctly
left that way.** The rerank-headroom research (`_tmp_rerank_headroom_probe.py`,
explicitly marked "THROWAWAY PROBE, not a committed simulation") measured
that veOS's real Company Brain corpus (N=3 promoted, N~6,800 ceiling) sits
below where a reranking stage's benefit would show up (BEIR Table 9: an
oracle reranker adds zero recall over BM25 at this scale). The correct
translation here was NOT to build a reranker — question 1 answered itself
("this is neither a constraint nor a pattern to encode, it's a decision
NOT to build something, at least not yet") and question 4's answer was
"nothing to prove, because nothing was claimed to work." Recognizing that
a finding's correct code output is "don't build this yet, revisit at N=X"
is itself a valid translation, and a probe file honestly marked as
throwaway (never committed) is the right artifact for that outcome — not
a permanent module implementing something the data doesn't yet justify.

## Translating an INVENTED finding (no precedent, built via cross-domain synthesis)

`research-simulate-encode`'s invention path and `deep-cross-domain-research`'s
"empty search is a trigger, not an end" both produce findings with no paper
or benchmark behind them. The four questions above still apply, with one
difference on question 4: the proof isn't "re-run the same adversarial
input against a known-good baseline" (there is no baseline), it's the
invention gate itself — simulation at your actual required scale, a
deliberate adversarial test against the design's own stated guarantee, and
one real-scenario check. Question 1 also gets an explicit fourth answer
alongside constraint/default/pattern: **invented-and-gated** — encode it
the same as a design pattern (a structural separation, a hash check, a
fail-closed rule), but label it invented in the same comment/doc, with its
tested scale ceiling stated plainly rather than implied to be unlimited.

## What research-to-code is not

- Not a replacement for validating the research at your own scale first
  (that's research-simulate-encode's job — do that before this).
- Not a license to build speculative infrastructure because a paper is
  interesting. Example B above is the template for "real finding, correct
  answer is not to build yet."
- Not satisfied by a comment citing a source. The comment records WHY;
  the code change (or the documented decision not to change code) is the
  actual translation. A paper citation with no attached behavior change,
  measurement change, or explicit "not yet, here's the threshold" is
  unconverted research, indistinguishable in the codebase from research
  that never happened.

## Grounding from outside this codebase

This four-question structure is this project's own synthesis — it draws
on Design by Contract's "encode the constraint, don't trust memory"
(Bertrand Meyer, 1992, already cited in `research-simulate-encode`) for
question 1, and on Architecture Decision Records' "context → decision →
consequences" (Nygard, 2011, also already cited there) for question 4's
verification requirement. No single external framework covers all four
questions as one named method — say so if asked, the same discipline
`research-simulate-encode` already applies to itself.
