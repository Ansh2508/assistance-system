---
name: velth-test-strategy
description: VELTH mandatory testing strategy for every backend task. Load before writing any test, before any git commit, before any Cowork implementation prompt. Contains all learnings from May 2026 sprint. Universal — applies to every feature, fix, and refactor, not just specific bugs.
trigger: auto
---

# VELTH Test Strategy — Permanent Rules

## WHY THIS EXISTS

Three bugs shipped in committed code during the May 2026 sprint and were caught by visual inspection or external review — not tests:

- XML escape bug in GBU renderer — caught by visual PDF audit
- BA STOP ordering (O: after P:) — caught by SiFa legal knowledge check
- English strings in `_risk_class()` fallback — caught by external architecture reviewer

Root cause every time: **we tested what we built, not what can go wrong.**

The deeper problem: the Gate Engine normalised English → German at comparison time. Tests passed. The upstream risk dict already had English. The gate masked the bug. This is the failure mode to watch for permanently — **a downstream normalisation making upstream corruption invisible to tests.**

We cannot rely on luck. This skill makes luck irrelevant.

---

## THE FUNDAMENTAL TESTING PRINCIPLE

**Every test must assert what lands downstream, not just what the function returns.**

| Function writes to | What to assert |
|---|---|
| A dict | `assert risk["field"] == expected_value` |
| audit_events / DB | The logged row value, not the function return |
| A PDF section | The section content string, not the render call result |
| A rendered document | Open the PDF, check visually or byte-scan |

If you only assert the return value you will miss every bug where the value is correctly returned but incorrectly stored, transformed, or rendered downstream.

---

## THE 5-LEVEL GATE — mandatory before every `git add`

### L1 — CI gate (import safety)
```bash
uv run --no-sync pytest tests/unit/test_no_direct_anthropic.py -q
```
Must be 0 violations. No `anthropic.Anthropic()` direct calls anywhere.
Only `get_anthropic_client(region="auto")` is permitted.

### L2 — Unit tests cover ALL branches
Not just the happy path. Every branch. Every fallback. Every except.

Rules:
- For every `if/elif/else` → test must exercise each branch
- For every `x = foo.get("field") or self._fallback()` → test with the field missing
- For every `try/except Exception: return default` → test must trigger the except
- For every LLM output consumer → test with None, "", missing fields, wrong types
- Assert the **downstream output** not the return value

Run:
```bash
uv run --no-sync pytest tests/unit/test_t16a_nohl_payload.py \
  tests/unit/test_t16b_nohl_gate.py \
  tests/unit/test_t16_meta_harness.py -q
```
Must be 140/140.

### L3 — Full regression
```bash
uv run --no-sync pytest tests/unit/ -q --tb=short
```

**Do NOT trust a hardcoded baseline in this file.** This section previously read
"Baseline: 3831 passed, 4 pre-existing" — by 2026-08-14 the real number was
**15,875 passed**, roughly 4x off, and every pre-existing failure listed below had
been replaced by different ones. A stale baseline is worse than no baseline: it
makes a real regression look normal, or a normal run look broken.

**Establish the baseline at session start, mechanically:**
```bash
# BEFORE touching any code, capture the real current numbers:
uv run --no-sync pytest tests/unit/ -q --tb=short 2>&1 | tail -5
```
Record that output. The gate is **zero NEW failures against the number you just
measured**, not against any number written in this file.

**Pre-existing failures are environment-dependent and change often.** As of
2026-08-14 they were `pdftotext` (Poppler not on PATH) and `xlrd` (not installed)
— tooling gaps, not product bugs. Earlier sessions saw a completely different set
(Supabase-singleton and PDF-gate tests). Identify the current set from your own
session-start run; do not fix them in a feature commit, and do not assume the set
named here is still the set you'll see.

### L4 — Smoke e2e all 6 doc types
```bash
uv run --no-sync python smoke_e2e_t16.py
```
Must be 7/7 PASS. All 6 doc types render to real PDF.
Combined PDF: 18 pages, ~55 KB.

### L5 — Visual PDF check
Open `smoke_t16_combined_*.pdf` after every commit touching a renderer or extractor.

Check for:
- STOP order correct: T: measures before O: before P: in BA Section 4
- German strings only: Hoch/Mittel/Gering/Sehr Hoch — never high/medium/low
- No UUID leaks in body text
- No `(needs_review)` flags visible
- Legal refs present and correct (DGUV, TRGS, ArbSchG)
- GBU has Psychische Belastungen section (GDA category 10)
- GFV has AGW/Grenzwert column with 0.05 mg/m³ for Quarz

---

## PRE-COMMIT GATE SCRIPT

Run before every `git add`. Lives at `apps/backend/scripts/pre_commit_gate.py`.

```bash
# From apps/backend/
uv run --no-sync python scripts/pre_commit_gate.py
```

If any level fails — fix it. Do not commit. Do not `--force` past it.

---

## PATTERNS THAT ALWAYS HIDE BUGS

These code patterns have a fallback branch that is almost never tested.
Every time you write one, write a test for the fallback immediately.

### Pattern 1 — Optional field with fallback
```python
risk["risk_class"] = risk.get("risk_class") or self._risk_class(risk_level)
```
**Test required:** pass a risk dict with no `risk_class` key.
Assert `risk["risk_class"]` after the call — not the return value of `_risk_class()`.

### Pattern 2 — LLM output consumer
```python
rc = str(risk.get("risk_class") or "").strip().lower()
```
**Test required:** pass `risk_class=None`, `risk_class=""`, `risk_class="high"` (English).
Assert the downstream value in the correct language/format.

### Pattern 3 — Downstream normalisation masking upstream corruption
```python
# Gate normalises at comparison time
normalised = _normalise_llm_class(llm_class)  # English → German
# But upstream dict still has English
risk["risk_class"] = "high"  # ← never caught because gate masks it
```
**Rule:** if a normalisation function exists, check whether it's called BEFORE or AFTER the value is written to its destination. If after — the stored value is wrong even if the comparison is right.

### Pattern 4 — Renderer reading from dict directly
```python
lvl = risk.get("risk_class") or risk.get("risk_level") or risk.get("level")
```
**Test required:** assert what the renderer outputs when `risk_class` is missing,
when it's English, when it's None. Don't just test that the renderer doesn't crash.

### Pattern 5 — Try/except swallowing errors silently
```python
try:
    result = complex_operation()
except Exception:
    return 3  # silent fallback
```
**Test required:** mock `complex_operation` to raise. Assert the fallback return value
is correct AND that it doesn't corrupt downstream state.

### Pattern 6 — String returned from method used as DB value
```python
def _risk_class(self, level: int) -> str:
    if level >= 5:
        return "critical"  # ← English, wrong
```
**Test required:** call the method directly. Assert the return value is in the
correct language/format. Also assert it when called via the parent pipeline.

### Pattern 7 — New import not declared as a real dependency
```python
from hypothesis import given, settings  # in a new test file
```
**Real incident, 2026-08-11:** `hypothesis` was imported in two new test files.
Both passed locally and were merged — because the machine that built and ran
them happened to have `hypothesis` installed ambiently, not because it was a
real project dependency. `pyproject.toml` and `uv.lock` had zero references to
it. On any other machine, including CI, both files failed at collection with
`ModuleNotFoundError` before a single test could even run. Caught after merge
by an external reviewer, not by any gate that ran.

**Why the existing L3 full-suite gate didn't catch this:** it only catches a
missing dependency if it actually runs against a genuinely clean,
freshly-`uv`-resolved environment. A proxy/stub run, or a run on a machine
where the package is already ambiently present, will pass green while hiding
exactly this gap — the same proxy-vs-real distinction that applies to test
logic (see cowork-sandbox-safety §5) applies just as much to the environment
itself, not just the code being tested.

**Rule — do this BEFORE running any test, not after:** for every new or
changed test file, grep it for every top-level third-party import, then grep
`pyproject.toml`'s dependency lists (both main and dev) for each one. This is
a cheap, deterministic, static text check — it works even in a constrained
sandbox with no working venv, which is precisely why it must run first, not
be assumed covered by a pytest run that might itself be silently proxy/stub.
Any import not found in `pyproject.toml` — add it via `uv add` / `uv add --dev`
before reporting done. Do not report a test file as passing on the strength of
a run where the environment's own dependency completeness was never verified.

### Pattern 8 — Stub/placeholder text pointing at a migrated-away pattern
```python
def load_live_project(project_id: str) -> dict:
    raise NotImplementedError("wire to X via get_supabase_admin_client()")
```
**Real incident, 2026-08-11:** a stub function's `NotImplementedError` message
told a future implementer to use `get_supabase_admin_client()` for
`project_risk_sets` access — the pre-repository-migration pattern.
`project_risk_sets` had already been fully migrated to
`ProjectRepository.get_active_risk_set(...)`. No harm the day it was written —
it was a string inside an unimplemented function, so the L1 import-safety
scanner correctly saw nothing to flag. The harm was deferred: whoever
eventually implements the stub follows the instruction verbatim and
recreates a call-site the guardrail structurally cannot see, because it never
becomes a real import until someone acts on the stale text.

**Rule:** automated guardrails can only see real code — actual imports, actual
calls. They cannot see an instruction sitting inside a string, docstring, or
comment. Any time you write or review a placeholder that names a specific
service, client, or pattern to use later, verify that pattern is still the
CURRENT one — grep for its real, live call sites elsewhere in the codebase —
before writing it into the stub. A stub's job is to correctly defer
implementation, not to silently preserve a stale instruction past whatever
migration made it wrong.

### Pattern 9 — Hallucinated field names on a real, existing class
```python
report.by_vertical[vid].successes       # looks plausible, doesn't exist
report.by_vertical[vid].total_signals   # looks plausible, doesn't exist
```
**Real incident, 2026-08-13:** a dispatch specified `CalibrationReport.successes`
and `.total_signals` as the field names to read a vertical's raw counts from —
both names sounded exactly right given the class's well-understood purpose
(per-vertical calibration data) and were written into a plan confidently before
any code existed. Neither field exists. The real shape only exposed a
precomputed `.precision` ratio; the raw counts had to be reconstructed from two
DIFFERENT fields (`n_signals`, `n_added`, `n_deleted`) via a formula.

This is a named, documented failure mode in the code-LLM literature —
"Hallucinated Objects" (Tambon et al., 2024): the model invents an attribute
name that sounds right for the object's purpose but was never actually defined.
Not a rare edge case — a 2026 replication study still measures commercial-model
hallucination rates in the low single digits per generation, meaning it recurs
routinely, not once.

**Rule — do this BEFORE writing any code that reads a field off an existing
class:** read the class's real, current definition (grep the class name, open
the file) and confirm every field name used, even when the class's PURPOSE is
already well understood. Purpose-familiarity is exactly what makes the guess
feel safe to skip — it's dangerous precisely because it's close to right.

### Pattern 10 — Mocking the definition site instead of the lookup site
```python
@patch("core.hazard_feedback.repository.HazardFeedbackRepository")  # WRONG
```
**Real incident, 2026-08-13:** an integration-test fixture patched
`core.hazard_feedback.repository.HazardFeedbackRepository` — where the class is
DEFINED. The code under test does `from core.hazard_feedback import
HazardFeedbackRepository` — a package-level re-export. Python's `patch()`
replaces a name in the module where it's LOOKED UP, not where it was originally
defined (Python docs, `unittest.mock`: *"patch()... looks up an object in a
given module and replaces that object"*). The fixture's patch target and the
code's actual reference pointed at two different names, so the mock never
intercepted anything — the fixture would have silently exercised the REAL
repository against whatever `DATABASE_URL` happened to point at.

**Rule — before writing any `@patch`/mock target, confirm the exact import
statement in the file under test**, not the class's own defining module. If the
file does `from package import Thing`, the patch target is
`package.module_that_does_the_importing.Thing` — the name's location in the
caller's namespace, not the class's home file. Grep the file under test for its
own import line first, every time.

---

### Pattern 11 — mechanical diff-assertions over recall, for accumulating
structural constraints (database/ORM work specifically)

**Real research, verified 2026-08-14: Dente, Satriani, Papotti, "Constraint
Decay: The Fragility of LLM Agents in Backend Code Generation" (arXiv
2605.06445, real, peer-cited).** A systematic study across 80 greenfield +
20 feature-implementation tasks, 8 web frameworks: *"as structural
requirements accumulate, agent performance exhibits a substantial decline."*
Two findings sharpen this beyond the headline claim, and both point straight
at VELTH's own work: the decay is worse in convention-heavy, opinionated
frameworks than minimal ones, and *"data-layer defects, including incorrect
query composition and ORM runtime violations"* are the leading root cause —
i.e. exactly Alembic/SQLAlchemy migration and repository work, not an
incidental category. The paper reports no proven mitigation and calls it an
open challenge — there is no citation here for "and this fixes it."

**The defensible response, adopted this session, not paper-validated but a
sound inference from the same mechanical-over-recall principle Pattern 9/10
already establish:** when a task carries more than a handful of "don't touch
X" constraints (a fixed set of counters, an append-only table, specific
unchanged expressions), don't rely on remembering them across a large edit.
Assert them mechanically, at the diff level, as part of the same change —
e.g. confirm specific strings/expressions are byte-identical before and
after, not "I was careful." Real instance: an adapter.py edit touching three
protected counter expressions shipped with an explicit check that each
string was untouched post-edit, rather than a stated intention to preserve
them. This is the same discipline as a vacuous-test check (RULE ZERO) turned
around — proving the constraint held, not asserting it did.

---

## MANDATORY TEST STRUCTURE FOR EVERY NEW FUNCTION

For every new function that processes external data (LLM output, user input, DB rows):

```python
class TestMyFunction:
    # 1. Happy path
    def test_happy_path(self):
        result = my_function(valid_input)
        assert result["key"] == expected_value  # assert downstream output

    # 2. Missing optional fields
    def test_missing_optional_field(self):
        result = my_function({})  # empty / minimal input
        assert result is not None
        assert result.get("key") in VALID_VALUES

    # 3. Fallback branch
    def test_fallback_branch(self):
        # Remove the field that triggers the fallback
        input_without_field = {k: v for k, v in valid_input.items() if k != "field"}
        result = my_function(input_without_field)
        # Assert DOWNSTREAM output — what lands in the dict/DB/PDF
        assert result["field"] in VALID_GERMAN_CLASSES  # not just != None

    # 4. Wrong type / language
    def test_wrong_language_input(self):
        result = my_function({**valid_input, "risk_class": "high"})  # English
        assert result["risk_class"] in {"Gering", "Mittel", "Hoch", "Sehr Hoch"}

    # 5. Null / None
    def test_null_input(self):
        result = my_function(None)  # should not crash
        # assert either raises ValueError (fail-fast) or returns safe default

    # 6. Adversarial LLM output
    def test_llm_garbage(self):
        result = my_function({**valid_input, "risk_class": "definitely_a_real_risk_class_lol"})
        assert result["risk_class"] in VALID_VALUES  # graceful degradation
```

---

## MANDATORY COWORK PROMPT FOOTER

Add this verbatim to the end of every Cowork implementation prompt.
Do not shorten it. Do not make it optional.

```
BEFORE REPORTING DONE — NON-NEGOTIABLE:

TESTING REQUIREMENTS:
1. For every if/elif/else block added: write a test exercising each branch
2. For every fallback pattern (x = foo.get() or default): write a test with the field missing
3. For every try/except: write a test that triggers the except path
4. Tests must assert DOWNSTREAM output (what lands in dict/DB/PDF section)
   NOT just the function return value
5. For every method returning a string used as a DB value: assert the string
   is in the correct language/format directly from the method
6. For every new/changed test file: grep it for every top-level third-party
   import, then grep pyproject.toml's dependency lists (main + dev) for each
   one. Any import not declared there — add it via `uv add`/`uv add --dev`
   BEFORE running any test. Do this first: a pytest run in a proxy/stub
   sandbox or on a machine with the package already ambiently installed will
   pass green while hiding a genuinely undeclared dependency (Pattern 7).
7. For every new placeholder/stub that names a specific service, client, or
   pattern to use later (e.g. a NotImplementedError message, a TODO, a
   docstring hook): grep the codebase for that pattern's real, current call
   sites before writing it in. A guardrail cannot see a stale instruction
   sitting inside a string — verify it points at what's actually live now,
   not what was correct before the last migration (Pattern 8).
8. For every field read off an existing class/dataclass (not one you're
   defining in this change): read that class's real current definition first
   and confirm the exact field names — do not infer them from the class's
   name or purpose, however well understood. Report the field names actually
   read, with a file:line citation, before writing code against them
   (Pattern 9).
9. For every @patch/mock target: grep the file under test for its own import
   statement first. If it does `from package import Thing`, the patch target
   is the NAME's location in the file under test's own namespace, not
   `Thing`'s defining module (Pattern 10).

GATE COMMANDS (all must pass before reporting done):
10. uvx ruff format {changed_file} --config pyproject.toml
11. uv run --no-sync pytest tests/unit/test_no_direct_anthropic.py -q
12. uv run --no-sync pytest tests/unit/test_t16a_nohl_payload.py tests/unit/test_t16b_nohl_gate.py tests/unit/test_t16_meta_harness.py -q
13. uv run --no-sync pytest tests/unit/ -q --tb=short (compare against the baseline YOU measured at session start — not a number written in a skill file; see L3)
14. uv run --no-sync python smoke_e2e_t16.py (must be 7/7)

Only report DONE when all 14 steps pass with zero new failures.
```

---

## PERMANENT LANGUAGE GATE TESTS

These two tests must always be present in `tests/unit/test_t16b_nohl_gate.py`.
They gate the English/German language bridge permanently. Never remove.

```python
def test_risk_class_fallback_is_german():
    """_risk_class() fallback must never write English strings.
    
    Root cause of May 2026 bug: gate normalised English->German at comparison
    time, masking that the fallback path wrote English to audit_events.
    This test catches the bug at the source.
    """
    from core.projects.risk_set_llm_extractor import RiskSetLLMExtractor
    extractor = RiskSetLLMExtractor.__new__(RiskSetLLMExtractor)
    assert extractor._risk_class(5) == "Sehr Hoch"
    assert extractor._risk_class(4) == "Hoch"
    assert extractor._risk_class(3) == "Mittel"
    assert extractor._risk_class(2) == "Gering"
    assert extractor._risk_class(1) == "Gering"
    for level in range(1, 6):
        result = extractor._risk_class(level)
        assert result not in ("low", "medium", "high", "critical"), (
            f"English string '{result}' leaked at level {level}"
        )


def test_normalise_risk_set_writes_german_risk_class():
    """risk_class must be German even when LLM omits it.
    
    Tests DOWNSTREAM output (risk dict value) not function return.
    Forces the fallback path by omitting risk_class from input.
    This is the test that would have caught the May 2026 bug on day one.
    """
    from core.projects.risk_set_llm_extractor import RiskSetLLMExtractor
    from core.analysis.evidence_bundle import EvidenceBundle, ProjectContext
    extractor = RiskSetLLMExtractor.__new__(RiskSetLLMExtractor)
    extractor.vertical_id = "safebau"
    bundle = EvidenceBundle(project=ProjectContext(project_id="test-fallback"))
    risk = {
        "hazard": "Absturzgefahr",
        "severity": 4,
        "probability": 3,
        "rpz": 12,
        "preventive_measures": [],
        "legal_refs": [],
        # deliberately NO risk_class field — forces _risk_class() fallback
    }
    result = extractor._normalise_risk_set(
        {"risks": [risk], "vertical_id": "safebau"},
        evidence_bundle=bundle,
    )
    normalised = result["risks"][0]
    german_classes = {"Gering", "Mittel", "Hoch", "Sehr Hoch"}
    assert normalised["risk_class"] in german_classes, (
        f"English string '{normalised['risk_class']}' written to risk dict"
    )
```

---

## GIT HYGIENE — non-negotiable

```bash
# Before any commit
git diff --cached --name-only          # must show ONLY intended files
git pull origin main --rebase          # always pull first
Remove-Item .git/index.lock -Force     # if blocked

# Never stage
# .claude/  apps/platform/  uv.lock  migrations  state.db  smoke_*.py

# Always push with
git push origin {branch}
```

**`--no-verify` removed 2026-08-26** — this "always" instruction was
unconditionally bypassing `.husky/pre-push` on every single push, which runs
a real lint/type-check/security-audit suite, not a formality. See
`velth-commit-prep`'s fuller note. If the push is blocked and the failure is
real, fix it; do not reach for `--no-verify` to get past it.

CRLF noise: virtiofs shows 300+ files modified. All noise. Never stage.
Fix if needed: `[System.IO.File]::WriteAllText(path, content -replace "\`r\`n","\`n", UTF8)`

---

## RUFF — mandatory after every code edit

```bash
uvx ruff format {file} --config pyproject.toml
uvx ruff check {file} --config pyproject.toml --select E,W,F
```

Expected: `1 file already formatted` after format.
E501 on box-drawing comment lines — pre-existing, ignore.
Any W or F error — fix before committing.

---

## WHAT GOOD LOOKS LIKE — commit checklist

Before every `git commit`:

```
[ ] L1 passed — 0 direct anthropic violations
[ ] L2 passed — 140/140 T1.6 tests including fallback paths
[ ] L3 passed — zero NEW failures vs. the baseline measured at session start (see L3; never a number hardcoded in this file)
[ ] L4 passed — 7/7 smoke e2e
[ ] L5 done  — PDF opened and visually checked (renderer/extractor commits)
[ ] Ruff clean — format + check both pass
[ ] Every new import in a new/changed test file confirmed present in
    pyproject.toml (main or dev) — checked BEFORE trusting any pytest run
    (Pattern 7)
[ ] Every new placeholder/stub naming a specific service or pattern
    verified against that pattern's real, current call sites — not a
    pre-migration one (Pattern 8)
[ ] Every field read off an existing class confirmed against that class's
    real current definition, file:line cited — never inferred from the
    class's name or purpose (Pattern 9)
[ ] Every @patch/mock target confirmed against the file-under-test's own
    import statement, not the mocked class's defining module (Pattern 10)
[ ] git diff --cached --name-only shows ONLY intended files
[ ] No .claude/ apps/platform/ uv.lock staged
[ ] Commit message: type(scope): description + bullet summary of what changed
```

If any box is unchecked — do not commit.

Note on "uv.lock staged" above: that line predates dependency work being a
routine part of this project. If the commit's actual purpose is adding or
fixing a dependency (Pattern 7's fix), `uv.lock` changing IS the intended
change — the rule is "don't stage it by accident," not "never stage it."
