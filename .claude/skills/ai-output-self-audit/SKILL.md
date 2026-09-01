---
name: ai-output-self-audit
description: Before reporting any AI-generated deliverable (code, research, a report) as complete, check it against the original request line by line - don't let it pass just because it superficially covers every topic asked about. Use before saying "done" on anything an agent, subagent, or model produced.
---

# Self-Audit AI Output Against the Original Ask

Distilled from a real failure: a research report named every country
that was asked for, so it read as complete. It wasn't — most of those
mentions were a single thin citation standing in for real depth. The
report got passed along as finished without anyone checking it against
what was actually requested, and the person who caught it had to ask
"were they used?" three times before getting an honest answer.

## Why this matters, with verified numbers

An earlier version of this skill said no formal research existed on this
specific failure mode. That was wrong, and was corrected the same way this
skill asks you to correct anything: by independently re-verifying the
claim rather than trusting the summary. The following were fetched and
read directly, not relayed from a secondary source:

- **75.8% false-success rate** among self-assessing coding-agent
  trajectories that made an explicit status claim (arXiv:2606.09863,
  *From Confident Closing to Silent Failure*, FAGEN@ICML2026 — 9,876
  tau2-bench + 1,879 AppWorld trajectories, 8+4 model families).
  **Confident closing language and tool-call volume substitute for
  verifying actual state changes** — an agent that ran many commands and
  wrote a fluent summary has produced two signals, and neither is
  evidence. The only evidence is the changed state itself.
- **The check has to be mechanical, not another model judging the
  work.** The same paper found lightweight TF-IDF detectors recovered
  4–8x more false successes than the best LLM judge at the same flag
  rate, at ~3,300x lower latency — LLM judges never exceeded AUROC 0.65.
  Where this skill offers a choice between running a command and
  reasoning about whether something probably worked, run the command.
- **27–78% of benchmark-reported "successes" are procedurally
  corrupt** — the end state looks right but a constraint was violated
  getting there (arXiv:2603.03116). Under a gate that checks the whole
  procedure, reliability across repeated attempts collapses to 2–24%,
  and model rankings reverse.
- **Symptom detection is far more reliable than root-cause diagnosis**:
  91.2–100.0% accuracy identifying that something is wrong, vs.
  38.2–75.2% accuracy explaining why (Jin & Chen, *Are LLMs Reliable
  Code Reviewers?*, Automated Software Engineering 2026,
  arXiv:2603.00539 — verified directly against the paper's own
  Table 3; a commonly-repeated paraphrase of this paper states 94–100%
  / 41–71%, which does not match the source and should not be
  propagated). Report a symptom as fact. Report a root cause as a
  hypothesis until you've shown the fix makes the symptom go away and
  its absence brings the symptom back.

Anthropic's own guidance on agentic coding ("Building verification loops
in Claude Code with skills") frames the fix the same way: "a repeating
cycle where an AI agent checks its own work — running tests, linters, or
custom checks — and fixes what fails before moving on," with
project-specific checks encoded as reusable skills rather than trusted
to memory. Veracode's 2025 GenAI Code Security Report (industry data,
not peer-reviewed — treat as directional) found AI-generated code
introduced vulnerabilities in 45% of tasks even when it looked locally
correct, which is the same failure at the code-quality layer rather than
the status-report layer.

## Tier every claim before it goes in a report

Label each load-bearing statement by how you actually know it:

| Tier | Meaning | May support "done"? |
|---|---|---|
| EXECUTED | You ran it and observed the output | Yes |
| READ | You opened the file/source and can quote it | Yes |
| INFERRED | Reasoned from something you read | No — verify or mark it |
| RELAYED | A subagent, doc, or prior session said so | No — re-verify, don't inherit the claim |

A field name, line number, citation, or file path in a report must be
EXECUTED or READ, never RELAYED — files and papers don't hallucinate,
summaries of them do. This applies to what a dispatch tells a subagent
too: a dispatch that states a fact as "already confirmed" is RELAYED
from the receiving agent's position until independently re-checked, no
matter how carefully it was verified upstream.

**The mechanical test for whether a check is real:** ask what it would
output if the thing it's checking did not exist. If the answer is "the
same thing," it isn't a check — a skipped test suite, a swallowed
exception returning a plausible-looking default, and two empty results
compared as equal all read as green while proving nothing.

## The checklist, before saying "done"

1. **Re-read the original request, not your summary of it.** Requests
   drift in your own head as work progresses. Go back to the literal ask.
2. **For a multi-part request (multiple items, countries, features,
   bugs), check off each part individually.** Does this specific part
   have a real finding/change/result behind it, or does it merely get
   *mentioned*? A mention is not evidence of completion.
3. **Distinguish "covered" from "addressed."** Code that imports a
   library isn't tested. A report that names a country isn't research on
   that country. A test that runs isn't a test that would catch the bug.
   Ask what would have to be true for this part to actually be false, and
   check whether you tested that.
4. **State gaps in the same message that reports success**, not only
   when asked. If 5 of 7 items got real depth and 2 didn't, say "5 of 7,
   here's what's missing on the other 2" up front. Don't wait to be
   pushed.
5. **For code specifically: verify with something that wasn't authored
   by the same process that wrote the code.** A real end-to-end call, a
   live system check, an adversarial test — not just "the code I wrote
   passes the tests I also wrote." This is the practice that caught real
   bugs in Sprint 5 that unit tests alone had missed, because the unit
   tests shared the same blind spot as the code.
6. **When delegating to a subagent or research dispatch, the self-audit
   still belongs to you, not the subagent.** A subagent reporting "done"
   is exactly as unverified as your own draft — audit its output against
   the original ask before passing it along as finished.

## A report shape that makes gaps visible instead of hidden

If a section below is empty, say so rather than deleting the heading —
the absence is itself information a reader needs.

```
DONE (executed, with evidence):
  - <claim> -> <command/source> -> <what was actually observed>

CHANGED, NOT VERIFIED:
  - <touched but not proven>

NOT DONE / OUT OF SCOPE:
  - <what a reader might assume happened and didn't>

HYPOTHESES (not facts):
  - <any root cause without a before/after demonstration>
```

A report with no "not done" section is suspicious on its face — real
work has edges. "Changed, not verified" is always an available, honest
answer, and a human who reads it can act correctly; a human told "done"
when it isn't finds out later, at a cost set by how long the gap
survived unflagged.

## What "done" actually requires

Not "every part of the request was touched." **Every part of the request
was verified**, by something independent of the process that produced it,
and any part that wasn't is named explicitly rather than silently passed
as complete.
