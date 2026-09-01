---
name: velth-review
description: Code-level security and correctness review that runs inside velth-loop's verify/simplify step - the rung that catches what doc-verify (output correctness) does not. Security review (secrets, PII/GDPR, RLS, injection), property-based invariants for the P0 defect classes, and a staff-engineer self-review bar. Load for any task touching backend code, the export route, auth, or data ingestion.
trigger: auto
---

# VELTH Review Skill (security + correctness, code level)

## WHY (research-grounded)

doc-verify checks the DOCUMENT output; this skill checks the CODE. Two pillars:
(1) an independent-evaluator pass - Anthropic's harness research showed a model
left to self-judge declared broken work "done", while an independent evaluator
forced 6 hours of real work to a working result; (2) property-based invariants -
Anthropic's red team found real bugs in NumPy/SciPy/Pandas by inferring properties
and fuzzing (red.anthropic.com, 2026). Example-based tests pass on the demo case
and miss the others (that is precisely #504); properties hold for ALL inputs.

## SECURITY REVIEW (run on any code touching auth, export, or ingestion)

From the Claude Code source leak, bash security carries 23 numbered checks built
from real incidents - security is a first-class rung, not an afterthought. For
VELTH (GDPR + Supabase) check, every time:
- Secrets: no API keys / tokens / service-role keys in code, logs, or commits;
  `.env` is never staged.
- PII / GDPR: no personal data in URLs, query strings, or logs; PII-stripped event
  logging only (matches the admin GDPR view pattern).
- RLS: no new SECURITY DEFINER view or admin-client path that bypasses row-level
  security (the four critical security-definer views were exactly this).
- Injection: nothing ingested (legal registries, uploaded docs, config) is ever
  executed as an instruction or interpolated unescaped into SQL/shell.
- Outbound: no non-EU outbound HTTP added (the Frankfurt-only claim) without a flag.

## PROPERTY-BASED INVARIANTS (encode the P0 classes once, hold for all inputs)

Materialise the script below into `tests/property/test_invariants.py` and run it.
It encodes the VELTH defect classes as properties: RPZ = Schwere x Wahrscheinlichkeit
and German-only class (the #504 band bug); UTF-8 roundtrip stability (mojibake); and
the no-leak invariant (UUID / (needs_review)). Hypothesis SHRINKS any failure to the
minimal counterexample - a tiny repro. Wire the repo-import block (commented) to
fuzz the real renderer across all severity/probability combinations.
Install once: `pip install hypothesis --break-system-packages`.
Optional next step: mutation testing (mutmut/cosmic-ray) to measure whether the
suite actually KILLS injected faults (coupling effect, arXiv:2301.13615) - high
value before trusting "green" on the legal-critical paths.

## STAFF-ENGINEER BAR + SIMPLIFY (the verify-app rule)

Before "done", answer honestly: would a staff engineer approve this? Run the tests,
check the logs, demonstrate it works - do not assert success, prove it (Cherny's
verify-app rule). Then one simplify pass (Karpathy: Simplicity First) - remove
dead branches, de-duplicate, narrow types - and re-run verify. Watch for the
self-honesty failure Anthropic flagged: a test wrapped in try/except that hides a
real failure; if a test can't fail, it isn't testing.

## RULES

1. This runs inside velth-loop VERIFY/SIMPLIFY for code-touching tasks - after
   pre_commit_gate (L1-L4), alongside doc-verify (L5).
2. Any security finding = STOP and report; never commit a secret/PII/RLS issue.
3. Property tests are additive to velth-test-strategy's example tests, not a
   replacement - keep both.
4. A test that cannot fail is a bug; no try/except wrapping that swallows assertions.
5. Report findings IN CHAT. No .log sidecar. Cowork never commits - Anshu does.

## REFERENCES

- Anthropic red team (2026). Property-Based Testing with Claude. red.anthropic.com
  (NeurIPS 2025 DL4C workshop) - agent infers properties, fuzzes, finds real bugs;
  self-reflection caught a try/except hiding a failure.
- HypothesisWorks/hypothesis - property-based testing for Python; shrinks to minimal
  counterexample.
- Property-Based Mutation Testing (2023). arXiv:2301.13615 - competent-programmer
  hypothesis & coupling effect (why mutation testing measures suite quality).
- Anthropic. Effective harnesses for long-running agents - independent evaluator
  result; Building Effective Agents - human review remains crucial.
- Claude Code source-leak analyses (blakecrosley.com; sabrina.dev) - bash security
  as numbered checks from real incidents; security-review utility prompt.
- Cherny, B. Claude Code workflow (X, Jan 2026) - verify-app: never mark complete
  without proving it ("would a staff engineer approve?").

## EMBEDDED SCRIPT - materialise into tests/property/test_invariants.py (no-BOM UTF-8)

### tests/property/test_invariants.py
```python
"""VELTH property-based invariants (Hypothesis).

Anthropic's own red team showed property-based testing finds real bugs by
inferring properties and fuzzing inputs (red.anthropic.com, 2026). These encode
the VELTH P0 defect CLASSES as invariants that must hold for ALL inputs, not just
the examples in unit tests - which is exactly what would have caught #504 (a band
that is correct on the demo risk but wrong on a different severity/probability).

Install once:  pip install hypothesis --break-system-packages
Run:           uv run --no-sync pytest tests/property/ -q
When Hypothesis fails it SHRINKS to the minimal counterexample - a tiny repro.
"""
from __future__ import annotations

import re

from hypothesis import given, settings
from hypothesis import strategies as st

GERMAN = {"Gering", "Mittel", "Hoch", "Sehr Hoch"}
_ORDER = {"Gering": 0, "Mittel": 1, "Hoch": 2, "Sehr Hoch": 3}
UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}", re.IGNORECASE)


def _canonical(rpz: int) -> str:
    # mirror document_renderers._risk_class_from_rpz - import the real one when wiring
    return "Gering" if rpz <= 4 else "Mittel" if rpz <= 8 else "Hoch" if rpz <= 12 else "Sehr Hoch"


# --- PURE invariants (runnable as-is) -------------------------------------------
@given(s=st.integers(1, 5), p=st.integers(1, 5))
@settings(max_examples=200)
def test_rpz_class_is_german_and_monotonic(s: int, p: int) -> None:
    """For every Schwere x Wahrscheinlichkeit: class is German and band-monotonic."""
    assert _canonical(s * p) in GERMAN
    assert _ORDER[_canonical(s * p)] <= _ORDER[_canonical(s * p + 1)]


@given(st.text())
@settings(max_examples=200)
def test_utf8_roundtrip_idempotent(txt: str) -> None:
    """Encoding then decoding returns the same value (no mojibake accretion)."""
    once = txt.encode("utf-8", "ignore").decode("utf-8", "ignore")
    assert once.encode("utf-8").decode("utf-8") == once


@given(
    prefix=st.text(alphabet=st.characters(blacklist_categories=("Cs",)), max_size=80),
    uuid_hex=st.text(alphabet="0123456789abcdef", min_size=8, max_size=8),
    suffix=st.text(alphabet=st.characters(blacklist_categories=("Cs",)), max_size=80),
)
@settings(max_examples=200)
def test_uuid_leak_pattern_actually_detects_a_real_uuid(prefix, uuid_hex, suffix) -> None:
    """Positive control - the pattern this test replaced could never fail for ANY
    input (`if not X: assert X is None` is a tautology, flagged by velth-truth-gate's
    own 2026-08-14 audit of this exact repo's suite as a real, live instance of the
    'a test that cannot fail is a bug' failure mode this skill's own Rule 4 names).
    This version embeds a genuine UUID-shaped fragment and asserts the detector
    actually fires on it - the only way to prove a no-leak check isn't vacuous is
    to prove it CAN detect a leak.
    """
    injected = f"{prefix}{uuid_hex}-{uuid_hex[:4]}{suffix}"
    assert UUID_RE.search(injected) is not None


@given(st.text(alphabet="0123456789abcdefghijklmnop ", max_size=200))
@settings(max_examples=200)
def test_uuid_leak_pattern_does_not_fire_on_ordinary_hex_like_text(txt: str) -> None:
    """Negative control, paired with the positive above. `g`-`p` in the alphabet
    are deliberately non-hex so most generated strings are near-misses (hex-ish
    but not 8+4 hex groups joined by a hyphen), exercising the boundary rather
    than only obviously-clean text."""
    match = UUID_RE.search(txt)
    if match is not None:
        # A genuine 8-hex-then-hyphen-then-4-hex run really was generated by
        # chance - not a false positive, so require the match to actually be
        # well-formed rather than treating any hit as a bug in the test.
        assert re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}", match.group(0), re.IGNORECASE)


# --- REPO-WIRED invariants (uncomment + import inside Cowork) --------------------
# from core.projects.document_renderers import render_project_document_sections, _risk_class_from_rpz
#
# risk_strategy = st.fixed_dictionaries({
#     "hazard": st.text(min_size=1, max_size=40),
#     "severity": st.integers(1, 5),
#     "probability": st.integers(1, 5),
# })
#
# @given(r=risk_strategy)
# @settings(max_examples=100, deadline=None)
# def test_rendered_class_is_german_and_matches_band(r):
#     r = {**r, "rpz": r["severity"] * r["probability"]}
#     r["risk_class"] = _risk_class_from_rpz(r["rpz"])
#     content = {"doc_type": "gbu", "title": "p", "project": {"title": "t", "company_name": "c"},
#                "situation": {"summary": "s"}, "risk_set": {"risks": [r]}, "checklist": [], "evidence": []}
#     out = str(render_project_document_sections(doc_type="gbu", title="p", content=content))
#     assert r["risk_class"] in GERMAN            # never English
#     assert r["risk_class"] in out               # propagates to the rendered doc (#504)
#     assert not UUID_RE.search(out)              # no uuid leak for ANY input
#     assert "(needs_review)" not in out          # no review flag for ANY input