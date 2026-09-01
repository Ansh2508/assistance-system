---
name: build-test-verify
description: Run all validation, test, and build commands. Use before reporting work done.
---

# Build, Test, Verify Skill

## Commands (Run in This Order)
CI=true uv run pytest tests/unit/ -q
CI=true uv run pytest tests/unit/test_svg_testbericht_regressions.py -v
./check.sh

## Never Report Done Until
- ./check.sh passes (exit code 0)
- No FAIL in output
- All tests green
- No TypeScript errors
- No linting errors

## If Any Check Fails
1. Read error output completely
2. Do NOT skip it
3. Fix the issue
4. Re-run ./check.sh
5. Only then report done

## YAML Validation
After editing any vertical, run:
./check.sh

Expected: All PASS

## Do NOT Commit If
- Any test fails
- ./check.sh shows errors
- Prettier or linter errors remain

Report the errors. Human commits manually.

## Green Tests Are Not Proof — Verify Independently

Added from real experience (veOS Sprint 5): a resolver's own unit tests
all passed, then a real end-to-end call surfaced a bug none of them
caught — the tests shared the same blind spot as the code, because the
same process wrote both. Industry data backs this as a general risk, not
a one-off: Veracode's 2025 GenAI Code Security Report found AI-generated
code introduced vulnerabilities in 45% of tasks even when it looked
locally correct. Anthropic's own guidance on agentic coding calls this
"a repeating cycle where an agent checks its own work" — the check has
to come from something independent of what produced the code.

- Before trusting a new regression test, break the fix on purpose and
  confirm the test actually fails. If it doesn't fail, it isn't testing
  what you think it's testing.
- Where a real integration point exists (a real API call, a real file,
  a real external system) and the task touches it, exercise it for real
  at least once. A mock that was written by the same reasoning that
  wrote the code can share its blind spot.
- Before reporting done, re-read the original request line by line, not
  your memory of it. A task with several parts (several files, several
  verticals, several legal refs) needs each part checked off
  individually — "the suite is green" is not the same claim as "every
  part of the request is addressed."

## Test the Downstream Value, Not the Return Value

A function can return the right value and still write the wrong one to
the database, the rendered document, or the next function's input. Test
what actually lands where it's used, not just what the function call
returns:

- A dict field: assert the dict has the right value AFTER the call, not
  that the call returned something plausible.
- A stored/logged/rendered value: assert the stored row, the rendered
  text, or the logged event — not the function's return value alone.
- A fallback branch (`x = value.get("field") or default()`): write a
  test that triggers the fallback specifically. An untested fallback is
  an untested branch even if the happy path is covered.

Two mechanical checks worth running before trusting a change, cheap and
concrete rather than a judgment call:
- **New third-party import in a test?** Confirm it's declared in the
  real dependency file (`pyproject.toml`/`package.json`/etc.), not just
  ambiently installed on this machine. A test that passes locally because
  a package happens to already be present will fail on a clean
  environment or in CI with no warning beforehand.
- **Using a field name or attribute on an existing class/type?** Read
  the actual current definition before using it, even when you're
  confident what it should be called. Confidently-wrong field names that
  "sound right" for the object's purpose are a documented, named LLM
  failure mode ("Hallucinated Objects" — Tambon et al., 2024), not a
  rare fluke.

## If a Regression Test Won't Fail, It Isn't a Test

Before trusting a new test as a real guard, verify it can actually fail:
temporarily break the thing it's supposed to catch and confirm the test
goes red, then restore the fix and confirm it goes green again. A test
wrapped in a broad `try/except` that swallows the failure, or an assertion
that's a tautology (`assert x is None` right after setting `x = None`), or
a comparison between two empty/default results, all read as passing
while proving nothing. Mutation testing is the formal version of this
same check — see risk-vault's structural-encoding section for the
citation.
