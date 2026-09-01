---
name: velth-cowork-sandbox-safety
description: Use BEFORE handing Cowork any task that involves git writes, verifying a fix by running tests, or "fix everything autonomously" scope. Load when a Cowork report claims a file is broken/corrupted, claims git state is corrupted, cannot run pytest/docker, or when Anshu is about to ask Cowork to "make it autonomous" or "use it even for pre-existing issues." Encodes real, repeated failure patterns from multiple sessions where Cowork's sandbox diverged from the real machine (virtiofs/bindfs stale-metadata bug, no network egress, no Docker, Windows-only venv) and where Cowork's own git writes corrupted state. Complements velth-merge-conflict-resolution (that skill is the merge mechanics; this one is when to trust Cowork's output about that merge at all).
---

# VELTH Cowork sandbox safety

## 0. The one-sentence lesson

**Cowork's sandbox is a different filesystem from Anshu's real machine, and
this difference is not always visible — the correct default is "verify on
the real machine," and the correct trigger for skepticism is "Cowork reports
something alarming," not "Cowork reports something alarming AND it's been a
long session."** Multiple separate sessions hit this same root cause
(virtiofs/bindfs stale file-size metadata causing null-byte padding or hard
truncation of files that are clean on the real host disk) and each time it
produced a cascade of wasted diagnostic turns before anyone checked the real
machine directly.

## 1. Before delegating anything to Cowork — know its actual capabilities

Do not assume Cowork's sandbox has parity with the real dev machine. Confirmed
across sessions, check freshly each time capability matters (these drift):
- **Network egress may be fully blocked** (`Tunnel connection failed: 403`).
  If the task requires `uv sync`, `pip install`, or any package fetch,
  confirm connectivity first or expect it to fail.
- **Docker may not be installed at all** in the sandbox. Any task requiring
  `pytest -m docker` or a real Postgres testcontainer cannot be verified
  there, full stop.
- **The `.venv` mounted into the sandbox may be a Windows-native venv**
  (`Scripts/activate.bat`, no `bin/`) — completely unusable from the Linux
  sandbox even though the path exists and looks populated.
- **`pytest` itself may not be importable** in the sandbox's system Python
  even when `python3` exists and other packages are present.
- **Cowork cannot always unlink/delete files at the OS level**
  (`Operation not permitted`) — this specifically breaks git's atomic index
  write, producing a corrupted `.git/index` with a stale `.git/index.lock`
  that Cowork also cannot remove. If Cowork's `git add` is followed by an
  "unable to unlink" error, STOP further git operations in that sandbox
  immediately — don't let it retry or attempt a workaround write.

**If a task plan requires ANY of the above, either confirm the capability
exists first with a cheap probe command, or route the task to "on your
computer" mode instead of the cloud sandbox** (the desktop app's "Run this
task" picker) — that mode has the real venv, real Docker, real git, real
network.

## 2. The virtiofs stale-metadata failure signature — recognize it fast

**Symptom:** Cowork reports one or more source files as truncated,
containing null-byte padding, or failing to parse with a syntax error at a
suspicious mid-token boundary (`SyntaxError: '(' was never closed` at a line
that looks structurally fine) — especially files that were confirmed clean
minutes or turns earlier.

**Do not accept this as ground truth. Do not let Cowork "restore" or
overwrite the file based on this observation** — a restore from git can
silently revert real, uncommitted work that exists cleanly on the real host
disk but was never truthfully seen by the sandbox.

**The check, run on the REAL machine, not in Cowork's sandbox:**
```powershell
python -c "import ast; ast.parse(open('<path>', encoding='utf-8').read())"
```
Silent = the real file is fine, the sandbox was lying. This single command
resolved every one of this pattern's occurrences across multiple sessions —
always in the direction of "the real file was fine all along."

If Cowork also claims the git index or `.git/index.lock` is corrupted,
check the real machine the same way before acting:
```powershell
git status --short
Test-Path .git\index.lock
```
An empty/clean result on the real machine means the corruption, like the
file truncation, existed only in Cowork's sandbox view and never touched the
actual repository.

## 3. When a Cowork report contradicts itself, treat that as signal, not noise

Watch for two claims in the same report that cannot both be true (e.g. "this
file is a documented, known deferral, not new" stated near "this file is
genuinely new, unowned, zero doc mentions" about the same subject). This is
not automatically a hallucination of a whole fact — it can also be an
internal inconsistency from summarizing at different points in a long
process. **The correct response is a targeted, evidence-only follow-up
prompt** asking for the exact commands and their exact raw output (not a
re-summary), specifically instructing:
- No file-based deliverables — every command's output must be pasted
  directly into the chat response, so it can be verified without another
  round-trip.
- An explicit self-audit: "review your own last report — is there anything
  you stated with confidence that you did NOT verify with an actual command
  versus something you inferred?"

This pattern (ask for raw command output + an explicit self-audit) reliably
separates "genuinely fabricated" from "real finding, imprecisely reported" —
in the one session that tested this directly, the self-audit surfaced two
real reporting errors (a wrong claim about test-fixture recoverability, an
unsupported authorship claim) while confirming the flagged "fabrication" was
not one.

## 4. Scoping an autonomous Cowork task safely

If asked to make a task "fully autonomous" or "fix everything, even
pre-existing issues, use the internet if stuck": this is legitimate and
Cowork can do real, good work this way — but it needs exactly two
non-negotiable boundaries stated explicitly in the prompt, not implied:

1. **Git write scope**: `status`/`diff`/`log`/`show`/`add` (staging only)
   are fine to hand over; `commit`, `push`, `merge --abort`, `reset --hard`
   must be explicitly forbidden every time, regardless of how much
   autonomy is otherwise granted. This is the one thing that must never be
   delegated, because it's the one thing that isn't cleanly reversible if a
   wrong call gets committed and pushed.
2. **Guessing boundary for high-consequence categories**: legal/regulatory
   reference content, production data-shape changes, anything touching
   money — Cowork should research thoroughly (web search, primary sources)
   and if still uncertain, take the *safest reversible* action (e.g. add to
   an allowlist with a comment, rather than editing authoritative registry
   data) and flag it clearly, rather than either silently guessing or
   silently skipping. Both silent failure modes are worse than a flagged,
   conservative choice.

Everything else (test fixtures, async/await bugs, stale assertions and
regexes, missing dependencies, reordering validation logic, frontend
copy for a new backend event type) is safe to grant full autonomous
judgment on, provided the task also mandates real verification per §5
below — autonomy over *what* to fix should never extend to autonomy over
*whether it was actually verified*.

## 5. Verification that counts, versus verification that doesn't

A Cowork report claiming "fixed and verified" only counts as verified if the
report shows one of:
- An actual `pytest <specific file> -v` run with a real pass/fail count
  (not "should pass now").
- An actual `ast.parse`/compile-check with genuinely silent output shown.
- An actual guardrail/lint script run with its real output pasted.

It does NOT count as verified if the report shows:
- `py_compile` walks or import-chain checks substituting for a real test
  run, when the task actually needed pytest and pytest wasn't available in
  that sandbox (see §1) — this is Cowork doing its best with what it has,
  which is honest, but it is not the same evidence and must not be treated
  as equivalent when deciding whether to commit.
- A confident summary sentence with no command shown at all.

**When Cowork's environment genuinely cannot run the real verification
(§1), the correct outcome is Cowork saying so plainly and handing back a
list of ready-to-apply, statically-verified fixes — not Cowork inventing
pass/fail numbers to look complete.** Treat an honest "I could not run this
here" as a successful, trustworthy report, not a failure — and always
re-run the actual verification yourself on the real machine before treating
any fix as final, regardless of how the Cowork report reads.

## 6. Iterating with Cowork without re-explaining full context every time

Long Cowork sessions on the same task benefit from stating, once, near the
top of a follow-up prompt: which specific bugs are already confirmed real
(cite the earlier evidence briefly), which are settled non-issues (and why),
and which remain open — so Cowork doesn't re-diagnose settled questions from
scratch or, worse, "helpfully" re-open something already correctly decided.
A prompt that says "fix these 4 confirmed bugs" with the evidence inline is
more reliable than one that says "here's the full history, figure out what's
still wrong" — the latter re-invites exactly the kind of confident
re-diagnosis that produces new, unverified claims layered on top of old
ones.
