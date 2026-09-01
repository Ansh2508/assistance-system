---
name: velth-merge-conflict-resolution
description: Use when merging origin/main (or any long-diverged branch) into a VELTH migration/feature branch with real conflicts - especially the repo-layer migration branches. Load BEFORE running `git merge`, and again before resolving each conflicted file. Encodes the verify-before-trust discipline learned from three real merge sessions (documents.py paywall merge, sections/innung/teams 3-way land, main-sync into feat/repo-wave-b3-remainder). Complements velth-cowork-sandbox-safety (that skill covers Cowork's sandbox unreliability; this one covers the merge mechanics themselves, done by Anshu directly in PowerShell).
---

# VELTH merge-conflict resolution

## 0. The one-sentence lesson

**A merge conflict resolution is not verified by "no `<<<<<<<` markers remain" — it is
verified by `ast.parse` (or equivalent) succeeding AND the actual test for that
behavior passing.** Every real bug in three sessions' worth of merges slipped
through the marker-check and was only caught by one of those two later checks —
sometimes hours later. Do the AST/compile check immediately after every single
edit to a conflicted file, not just at the end.

## 1. Before touching `git merge`

1. Confirm current branch and clean state:
   ```powershell
   git status --short   # only expected scratch/untracked dirs, nothing else
   git log --oneline -5  # confirm you're where you think you are
   ```
2. Fetch fresh, don't trust a stale local view of the remote:
   ```powershell
   git fetch origin main <your-branch>
   git log --oneline origin/main -3
   git log --oneline origin/<your-branch> -3
   ```
3. If someone else (a teammate, a bot) pushed to your branch or the shared
   integration branch since you last looked — even one commit — check what it
   touched (`git show --stat <hash>`) before merging on top. A single new
   commit from a teammate mid-session is common; don't assume your merge-base
   is still what you last recorded.
4. For a large sync (hundreds of commits), get real numbers before starting,
   not a vibe: `git log --oneline <merge-base>..origin/main | Measure-Object -Line`.
   A 5-file sync and a 461-file sync need different amounts of care; know
   which one you're doing before you start.

## 2. Running the merge

```powershell
git merge origin/main
```

Do not chain further commands after this in the same paste-block. Read the
actual conflict list git prints before doing anything else — it is the ground
truth for which files need resolving, not a plan you made five minutes ago.

If you need to abandon a merge cleanly, `git merge --abort` restores the
pre-merge state exactly. Prefer this over trying to manually undo partial
resolution.

## 3. Resolving each conflicted file — the actual discipline

For **every** conflicted file, in this order, no skipping steps:

1. **Get fresh line numbers for the markers, right now, in this file**, don't
   reuse numbers from three turns ago — indices shift as soon as any earlier
   conflict in the same file gets resolved:
   ```powershell
   Select-String -Path <file> -Pattern "^<<<<<<<|^=======|^>>>>>>>"
   ```
2. **Read enough real context around the conflict to understand intent, not
   just the diff.** A conflict where one side is a blank region and the other
   has real code is not automatically "take the non-blank side" — check what
   calls the surrounding function immediately after the conflict block; the
   non-conflicting call site sometimes tells you the *other* side already
   won and the block is dead weight (see workspace.py case below).
3. **Classify the conflict before resolving:**
   - **Pure structural/mechanical** (a rename, a signature-only change): pick
     the correct side directly, verify.
   - **Both sides changed the same logic for different reasons** (repo-layer
     flip vs. a new feature main added): this needs the new feature's logic
     *ported onto* the migrated side, not "pick a side." Read both sides in
     full before writing the resolution.
   - **HEAD's side is empty/comment-only, other side has a real feature**: do
     not assume HEAD wins by default. Check whether the surrounding code
     (just after the conflict) already calls the feature inline — if so,
     the "empty HEAD" side may already be the working, complete
     implementation and the other side's block is genuinely dead. Verify by
     reading the actual call site, don't guess from the diff shape.
   - **A fabricated-default bug you already fixed elsewhere in this session
     re-appears** (e.g. `hazard.get("risk_level", 3)` after you already
     removed one instance): grep the WHOLE file for the pattern, not just the
     conflicted region — these bugs cluster at multiple call sites in the
     same file and one resolved instance does not mean the file is clean.
4. **Write the resolution using file-content matching, not manual line
   splicing where avoidable.** `git-scm`-style resolution by hand (deleting
   marker lines with an array-index splice) is genuinely more error-prone
   than an exact-string `.Contains()`/`.Replace()` — a single off-by-one
   silently duplicates or drops a block. Prefer:
   ```powershell
   $content = [System.IO.File]::ReadAllText((Resolve-Path $path).Path, [System.Text.Encoding]::UTF8)
   if ($content.Contains($old)) {
       $content = $content.Replace($old, $new)
       [System.IO.File]::WriteAllText((Resolve-Path $path).Path, $content, (New-Object System.Text.UTF8Encoding($false)))
   } else {
       Write-Host "NO MATCH - paste exact current content, do not guess" -ForegroundColor Red
   }
   ```
   If `.Contains()` returns false, **stop and re-read the file fresh** — do
   not adjust the match string by guessing at what might be different. Line
   endings (see §4) are the most common silent cause.
5. **Verify immediately, this file only, before moving to the next
   conflict:**
   ```powershell
   python -c "import ast; ast.parse(open('<path>', encoding='utf-8').read())"
   ```
   Silent output = pass. Any traceback = the resolution is wrong; fix it
   before touching another file. A clean marker-grep with a broken AST parse
   is the single most common false-confidence trap in this whole workflow —
   it happened three times in one session with the same root cause
   (duplicate method left behind after a "successful" edit).
6. Only after ALL conflicts in the merge are resolved and every touched file
   passes its own `ast.parse`, run the full gate (§5).

## 4. Encoding pitfalls that cause silent match failures

These cost real hours across multiple sessions. Check for them proactively,
don't wait for a mysterious `NO MATCH`.

- **Line endings are not uniform within one file after a merge.** A file can
  mix CRLF and LF post-merge. `` `r`n `` typed literally in a PowerShell
  here-string does NOT reliably match what's actually in the file. **Prefer
  regex with `\r?\n`** over literal newline matching once a first
  literal-match attempt fails:
  ```powershell
  $pattern = [regex]::new("<<<<<<< HEAD\r?\n=======\r?\n<content>.*?\r?\n>>>>>>> origin/main\r?\n", [System.Text.RegularExpressions.RegexOptions]::Singleline)
  ```
  Diagnose which line ending is actually present before guessing:
  ```powershell
  $content.Substring($content.IndexOf("<<<<<<< HEAD"), 40) | ForEach-Object { [System.Text.Encoding]::UTF8.GetBytes($_) } | ForEach-Object { "{0:X2}" -f $_ }
  # 0D 0A = CRLF, bare 0A = LF
  ```
- **PowerShell single-quoted strings do not interpret `` `n ``/`` `r`n ``
  backtick-escapes at all** — only double-quoted strings and here-strings do.
  A replacement built with single quotes and backtick-n sequences will write
  the literal two characters `` `n `` into the file, which passes a naive
  marker-grep but fails `ast.parse` with a confusing syntax error at the
  literal backtick. Use a `@'...'@` here-string (real embedded line breaks)
  or double-quoted strings for any multi-line replacement text.
- **Mojibake (cp1252-as-UTF8) survives silently through git merges.** Em-dash
  and umlaut characters mis-encoded before the merge (e.g. `fÃ¼r` instead of
  `für`) stay mis-encoded after — git doesn't repair encoding. If a
  string-literal comparison in code (a role-name allowlist, a normalized-text
  check) needs to match a *correctly*-encoded value from a test, and it's
  quietly failing, check for this before assuming logic is wrong:
  ```powershell
  Select-String -Path <file> -Pattern "<the suspect literal>"
  # if PowerShell renders it with Ã, Â, or similar, it's mojibake
  ```
- **Writing files: always specify UTF8 without BOM explicitly.**
  `[System.IO.File]::WriteAllText(path, content, (New-Object
  System.Text.UTF8Encoding($false)))` — the `$false` suppresses the BOM.
  Plain PowerShell `Set-Content` without `-Encoding` can silently prepend a
  BOM (`EF BB BF`), which is invisible in most viewers but changes the file's
  first bytes. Check after every write if BOM state matters:
  ```powershell
  [System.IO.File]::ReadAllBytes($path) | Select-Object -First 4 | ForEach-Object { "{0:X2}" -f $_ }
  # EF BB BF = BOM present, strip it (see below)
  ```
  Strip an accidental BOM:
  ```powershell
  $bytes = [System.IO.File]::ReadAllBytes($path)
  if ($bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
      $text = [System.Text.Encoding]::UTF8.GetString($bytes, 3, $bytes.Length - 3)
      [System.IO.File]::WriteAllText($path, $text, (New-Object System.Text.UTF8Encoding($false)))
  }
  ```

## 5. The silent-regression class: clean-merged files that need re-checking anyway

**A file that merges with ZERO conflicts can still be broken.** If the other
branch added code to a file your branch already migrated/cleaned, and that
addition lands in a region your branch didn't touch, git auto-merges it with
no conflict shown — and the new code can silently reintroduce exactly what
you removed (a raw Supabase call into a guardrail-clean file, a duplicate
Python-package import, etc). This is invisible to `git diff --check` and to
every conflict-resolution step above.

**The only catch for this class is a domain-specific automated check run
AFTER the merge, regardless of whether any conflicts were reported**:
- Run your project's "no forbidden pattern" guardrail script (or equivalent
  grep) on the full merged tree, not just the files you touched.
- Cross-reference every hit against your known-exceptions list
  (`README_DEFERRED.md` or equivalent) before treating it as new.
- If a previously-clean file now fails the guardrail, that file's new
  content needs the same repo-layer/whatever-pattern treatment as an
  original migration — find or add the matching abstraction method, port the
  call, re-verify.

## 6. Signature verification before writing repo/service calls

Never guess a method's parameter names, order, or keyword-only-ness from
memory of "similar" methods in the same file — confirm the actual signature
every single time before calling it in a fix:
```powershell
Select-String -Path <repo file> -Pattern "async def <method_name>\(" -Context 0,10
```
This session hit two near-misses from assumption: a guessed signature used
positional args and a dict where the real method was keyword-only with a
flat `name=` parameter, and a guessed `get_project`/`update_project_fields`
call was corrected only because the signature was checked first. The check
costs one command; a wrong guess costs a silent runtime bug that ast.parse
cannot catch (wrong arguments still parse as valid Python).

## 7. The multi-head / N-way land pattern (integration branch merges)

When landing several parallel feature branches into one shared integration
branch (not just a two-way main-sync):
- Land one at a time, `--no-edit`, checking after EACH merge, not chaining.
- Expect the SAME shared-list file (a guardrail's MIGRATED list, a registry)
  to conflict on the second and third merge even though the first was clean
  — every branch added to the same list region. Resolution is additive: keep
  every entry from every side, never drop one to resolve the textual
  conflict.
- If the project uses Alembic (or any linear migration-chain tool), landing
  N branches that each added migrations independently produces N heads that
  must collapse to one before the branch is usable. Check explicitly
  (`alembic heads`) — don't assume a clean git merge implies a clean
  migration chain.
- Confirm the base commit hasn't moved under you before starting a
  multi-branch land (`git rev-parse HEAD` against the value you expect) —
  a teammate pushing to the shared branch mid-land is the single most
  disruptive surprise in this pattern.

## 8. Final gate before commit (every merge, no exceptions)

Run in this order, stop and fix at the first red:
1. `git diff --check` (repo-wide) — catches any file still carrying literal
   `<<<<<<<`/`=======`/`>>>>>>>` text anywhere, not just files you remember
   touching.
2. `ast.parse` (or your language's compile-check) on every file the merge
   touched that you edited — not just the ones with markers.
3. Project guardrail/lint script, full repo, not scoped to touched files
   (see §5).
4. `ruff format --check` (or equivalent) scoped to files YOU touched — do
   not reformat pre-existing drift in files outside your actual changes,
   that's scope creep into someone else's domain.
5. Full test suite, both the fast/unit tier and any container-backed tier —
   run BOTH, a fast-tier pass does not imply the slow tier is clean.
6. Only after all four are green (or every remaining failure is confirmed,
   with evidence, to be pre-existing and unrelated — see
   velth-cowork-sandbox-safety §3 for how to make that call correctly), stage
   deliberately by explicit path (never `git add -A`) and commit.
