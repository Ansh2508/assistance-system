---
name: velth-commit-prep
description: After the loop is green, emit an explicit copy-paste git add + commit + push block IN CHAT for Anshu to run. Cowork never runs git - Anshu commits. Load at the end of an implementation session once velth-loop verification passes. Uses explicit file paths (never git add -A) to preserve the untracked scratch/venv pile.
trigger: auto
---

# VELTH Commit-Prep Skill

## WHY

Cowork never commits - Anshu does. This skill turns "done" into a ready-to-paste
commit block in chat, with EXPLICIT paths so untracked scratch scripts, broken
venvs, and `dashboard/_components/*.tsx` are never swept in.

## PRECONDITION

Do NOT emit a commit block unless velth-loop step 3 (VERIFY) is fully green:
ruff clean; pre_commit_gate.py L1-L4 pass with zero new failures; velth-doc-verify
PASS for the session's doc types/verticals; ui_smoke PASS if a UI/export path
changed. If any is red, report the failure instead - no commit block.

## WHAT TO EMIT (in chat, never as a file)

1. Verification summary: which gates ran, pass counts, judge verdict + judge id.
2. The exact files changed this session as an explicit `git add` list.
3. A Conventional-Commits message: `type(scope): summary` + body bullets (what
   changed, why / ticket #). ASCII only.
4. The push line for the current branch.

Template:

```bash
# from C:\Users\redmi\velth   (Anshu runs this - Cowork does not)
git status                                   # confirm only intended files
git add apps/backend/<file1> apps/backend/<file2>   # EXPLICIT - never -A / .
# list every changed file individually

git commit -m "fix(scope): one-line summary" \
  -m "- what changed, concretely" \
  -m "- why (root cause / ticket #)" \
  -m "- verify: L1-L5 + doc-verify green; localhost propagation confirmed"

git push origin <branch>
```

**`--no-verify` was removed from this template 2026-08-26 — it was silently
bypassing a real, currently-active gate.** `.husky/pre-push` runs
`bun run lint:backend && bun run lint:frontend && bun run type-check`, plus a
`uv.lock`-triggered `pip-audit` and a `verticals/*.yaml`-triggered
`validate_configs` — this is not decorative, it is the actual mechanism that
catches a regression in a file the current push didn't touch but broke
anyway. The root `CLAUDE.md`'s own rule is explicit: `.husky/` is a NEVER,
same tier as `git commit`/`git push` without asking. If the PRECONDITION
above was honored (velth-loop step 3 fully green before this template is
even reached), the hook should pass trivially and cost nothing to leave in;
its only function then is to catch the case where the precondition was
skipped or the checked-out tree drifted since VERIFY ran.

## RULES

1. EXPLICIT paths only. Never `git add -A` / `git add .`.
2. Never stage: `.claude/`, `apps/platform/`, `uv.lock`, `migrations`, `state.db`,
   `smoke_*.py`, `scripts/doc_verify.py`/`scripts/ui_smoke.py` if you treat them as
   local tooling, untracked scratch (`_patch_*.py`, `_*_probe.py`), broken venvs.
3. ASCII-only commit message (no umlauts/emoji) - avoids encoding noise.
4. If the branch needs reconciling with main first, say so and give the
   `git fetch origin main` + merge/rebase line - do not assume clean.
5. Output the whole block IN CHAT. No commit script file, no .log.
