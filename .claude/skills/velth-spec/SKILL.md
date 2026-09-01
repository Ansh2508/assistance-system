---
name: velth-spec
description: The planning front-end for every non-trivial VELTH task - turn an idea into an approved, testable plan before Cowork writes any code. Explore (read-only) -> Plan -> confirm -> TDD-first -> implement. This is where Anshu spends his attention as architect; it is the single biggest lever on output quality and the biggest reducer of his cognitive load. Load with velth-loop at the start of an implementation session.
trigger: auto
---

# VELTH Spec Skill (plan before code)

## WHY (research-grounded)

Planning before implementation is non-negotiable for production code; Explore +
Plan are the CHEAPEST phases in tokens and the MOST valuable in outcome (Anthropic
Claude Code best practices; Plan Mode). "Vibe coding" is fine for throwaway MVPs,
not for documents a SiFa signs. Anthropic's own harness research: a bare agent
reported a task "done" in 20 minutes and nothing worked; with an independent
evaluator in the loop the same model ran 6 hours and delivered a working result.
So: plan explicitly, define the test that proves success, then implement.

## THE FRONT OF THE LOOP (Anshu approves before any edit)

```
EXPLORE (read-only)   Cowork reads the relevant files and summarises them. NO edits.
                      Ask it the questions you'd ask a senior engineer ("what does
                      X handle? where is Y wired?"). Use neutral language ("correct
                      me if I'm wrong, the flow is...") to reduce model bias.
PLAN                  Numbered plan: each change as <file> + <why> + the EXACT verify
                      command that will prove it. Surface assumptions and open
                      questions. No code in this phase.
CONFIRM               Anshu reads and approves/edits the plan. This is your one
                      high-leverage decision point - think here, once, at design level.
TDD-FIRST             BEFORE implementation: write the FAILING test(s) / the
                      doc-verify expectation that encodes "done". Claude defaults to
                      implementation-first; you must say explicitly: "write the
                      failing test first, do NOT implement yet." Tests drive design
                      and become the loop's external target (velth-loop VERIFY).
IMPLEMENT             Hand to velth-loop (checkpoint -> implement -> verify -> stop).
```

## TODO DECOMPOSITION (Claude Code's short-term-memory pattern)

For any multi-step task, Cowork breaks it into a tracked todo list and keeps it
updated (in_progress / done) as it works - the same mechanism Claude Code uses so
steps are never silently dropped across a long task. State the decomposition in the
plan; the todo list IS the progress record for the session. This is the main
cognitive-load reducer: you track the list, not the keystrokes.

## ANSHU'S ROLE

You are the architect/gatekeeper. Your job is the EXPLORE summary review + PLAN
approval + the test definition - not line-by-line code. Spend attention at the plan
level; let velth-loop execute below it. If the plan is right and the test is right,
the implementation is mostly mechanical.

## RULES

1. NO code before the plan is approved. Explore is strictly read-only.
2. The plan MUST name the exact verify command (pytest target + pre_commit_gate +
   doc-verify scope) - if you can't name how you'll prove it, the plan isn't ready.
3. TDD-first for any logic change: failing test before implementation.
4. Decompose multi-step work into a tracked todo list; keep it updated.
5. One clarifying round max in the plan; then proceed on the best interpretation
   and log the assumption (do not stall).
6. Output the plan IN CHAT for approval. No spec file, no .log.

## REFERENCES

- Anthropic. Claude Code best practices (code.claude.com/docs) - Explore/Plan/
  Implement/Commit; "ask questions you'd ask a senior engineer".
- Anthropic. Effective harnesses for long-running agents - the independent-evaluator
  result (20 min "done"/broken vs 6 h working).
- Anthropic. Effective context engineering for AI agents - structured note-taking /
  to-do lists as agentic memory.
- TDD with Claude (FlorianBruniaux/claude-code-ultimate-guide) - Claude writes
  implementation-first; TDD requires explicit "failing test first" prompting.
- Cherny, B. Claude Code workflow (X, Jan 2026) - Plan Mode for every non-trivial task.
