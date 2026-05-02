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
