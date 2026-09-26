---
name: ponytail
description: Use a minimal-change engineering lens without deleting edge-case, safety, security, accessibility, data-integrity, or explicitly requested behavior; route risky architectural choices directly through research-simulate-encode.
license: MIT
metadata:
  short-description: Minimal code, preserved behavior, research-first when risky
---

# Ponytail — guarded minimalism

This is a locally adapted copy of Ponytail by Dietrich Gebert. The upstream
skill is preserved at `references/upstream-SKILL.md` and its MIT license at
`references/UPSTREAM-LICENSE.txt`. Source commit:
`e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156`.

The goal is not “delete code.” The goal is the smallest **validated** change
that solves the actual problem. Minimalism may remove duplication or an
unneeded abstraction; it must not remove behavior merely because the behavior
is difficult to see.

## Hard handoff: research before simplification

Go directly to `$research-simulate-encode` before deciding how to simplify
when any of these apply:

- a paper, benchmark, external repository, vendor claim, or best practice is
  being used to justify the change;
- the change affects an ML model, ranking, data pipeline, evaluation, schema,
  safety boundary, security control, legal/compliance behavior, or data rights;
- the code is unfamiliar, the edge-case behavior is undocumented, or deleting
  it could change a user-visible contract;
- the proposed shortcut changes failure behavior, temporal semantics, retries,
  numerical assumptions, or a trust boundary.

Research-simulate-encode must produce: the primary source, the exact claim,
the smallest local simulation or reproduction, failure cases, and the
structural rule that will prevent a regression. Do not use Ponytail to bypass
research or validation.

## Guarded ladder

After reading the task and tracing the code path, stop at the first rung that
is both sufficient **and behavior-preserving**:

1. Does this need to exist? Remove only genuinely speculative scope; keep
   every explicit requirement.
2. Does the repository already contain the correct helper or pattern? Reuse it
   only after checking its callers and edge-case contract.
3. Does the standard library solve it correctly for the supported inputs?
4. Does the native platform or an already-installed dependency solve it?
5. Can the implementation be shorter without changing observable behavior?
6. Otherwise write the smallest new implementation that passes the contract.

The ladder is applied after understanding the whole flow, never instead of
understanding it. Two solutions may be equally short; choose the one with the
stronger edge-case behavior and clearer failure mode.

## Preservation rule

Before deleting or collapsing code, make a short inventory of what it protects:

- empty, malformed, duplicate, missing, future-dated, and partial inputs;
- retries, timeouts, provider outages, and partial writes;
- authorization, privacy, secrets, injection, and tenant boundaries;
- numerical overflow, precision, units, and missing-value semantics;
- accessibility, keyboard, localization, and responsive behavior;
- audit, provenance, rollback, and user-visible error contracts.

An item can be removed only when an equivalent contract remains and a targeted
check demonstrates it. If that proof is unavailable, keep the behavior and
mark the uncertainty for research or follow-up. Never use “YAGNI” to erase an
edge case, a guard, a test, or an explicit user requirement.

## Rules

- Fix root causes at the shared boundary, not symptoms in one caller.
- Prefer boring, standard, readable code over clever compression.
- Do not add abstractions, configuration, dependencies, or scaffolding for a
  hypothetical future use.
- Do not delete tests to make a change pass; reduce or replace a test only when
  the behavior contract is unchanged and the replacement covers it.
- Keep deliberate simplifications visible with a `ponytail:` note naming the
  known ceiling and the upgrade trigger.
- For non-trivial logic, leave one runnable targeted check. A full suite is
  required when the repository's validation policy or risk level requires it.
- Keep explanations short by default, but provide the full reasoning when the
  user asks for research, a plan, an audit, or a walkthrough.

## Modes

- `lite`: build the request, then name one safer smaller alternative.
- `full`: apply the guarded ladder and preservation rule. Default.
- `ultra`: challenge speculative scope aggressively, but never bypass the
  preservation rule, research handoff, security, safety, accessibility, data
  integrity, or validation.

The mode changes effort spent on optional scope, not the safety bar. “Stop
ponytail” or “normal mode” disables this skill for the current task.
