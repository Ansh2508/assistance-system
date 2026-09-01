---
name: risk-vault
description: Build Risk Vault YAML files (v2.0 RiskObjects). Use when creating vertical configs, hazard categories, or legal banks.
---

# VELTH Risk Vault — Build Skill

## What You Build
Schema v2.0 RiskObject YAMLs.
Output: config.yaml + risks/*.yaml

## RiskObject Quality (Non-Negotiable)
- id: unique_identifier
- detection.keywords: 5+ German terms
- detection.negative_keywords: prevent false positives
- legal_basis.primary: min 2 refs with paragraph + reason
- controls: min 4 (S/T/O/P order)
- controls[].description: specific, DIN/DGUV cited
- inspections: min 3 checklist items
- training.modules: min 1 quiz question
- ba.employee_rules: required + prohibited behavior

## System Prompt (Every Vertical)
- Persona: name, years, exact role
- 5 real incidents (German, 2019-2023)
- COMMON MISTAKES: 5 wrong interpretations
- NIEMALS: 8+ forbidden statements
- FALSCH/RICHTIG: min 6 examples
- FUNDSTELLE: Typ A/B/C explanation
- confidence_threshold: 0.75
- field_max_chars: reason 200, measure 150, legal_ref 100

## Hazard Detection Prompt
- Image mode: max 6 hazards, visible only, confidence <0.6 filtered
- BILDBASIERTE ANALYSE: when photos trigger image mode
- RAG injection: keywords map to hazard IDs
- JSON schema: exact output format
- Error handling: ambiguous input response

## Legal References (Verified)
- ADR 2025 (NOT 2023 - expired 01.07.2025)
- BKrFQG 2026: 12h e-learning valid since 03.02.2026
- ArbSchG: always cite exact paragraph
- DGUV Vorschrift 1, 68, 70, 307-309
- GDA-IDs: map to gda_id in every risk
- NO invented paragraph numbers

## STOP Principle (ArbSchG §4 - Enforced)
S: Substitution (eliminate)
T: Technical (engineering)
O: Organisational (procedures)
P: Personal/PPE (last resort)
Never reverse. Never skip S.

## Validation (Run After Every Vertical)
./check.sh

Must pass with exit code 0.

## Gold Standards (Read First)
- apps/platform/verticals/safelogistik/config.yaml
- apps/platform/verticals/safeevent/config.yaml

## Do NOT Build From Scratch
1. Copy structure from safelogistik or safeevent
2. Change vertical.id, name, industry
3. Adapt system_prompt persona
4. Update hazard_categories: modify keywords
5. Verify legal_refs match German law
6. Run ./check.sh
7. Report done - do NOT commit

## Why the Minimums Are Non-Negotiable, Not Just Strict

The "Non-Negotiable" counts above (min 4 controls, min 6 FALSCH/RICHTIG,
8+ NIEMALS, etc.) aren't arbitrary strictness — they're the same
principle as **Design by Contract** (Meyer, 1992): a requirement the
schema/validator enforces mechanically is one that survives a rushed
session; a requirement that's only a convention gets skipped under
deadline pressure. `./check.sh` failing on a missing count is the
contract being enforced, not a formality to work around.

Two checks worth running specifically because this skill generates
structured YAML with many field names:

- **A count can be satisfied by padding, not by real content.** Five
  FALSCH/RICHTIG examples that are trivial variants of one real example
  is a vacuous pass — it raises the count without adding a real
  counterexample. Where practical, spot-check that a new entry actually
  changes what the check would catch (would this FALSCH example be
  caught without the RICHTIG example next to it? if the check would
  behave identically either way, it isn't testing anything).
- **A field name that "sounds right" for a RiskObject's purpose can
  still be wrong.** Before writing a new field key into a RiskObject
  YAML, confirm it against the actual v2.0 schema/gold standard, not
  against what a similar field is usually called. This is the same
  failure mode as a hallucinated attribute name on a class ("Hallucinated
  Objects," Tambon et al., 2024) — the guess is dangerous precisely
  because it's close to right, not because it's obviously wrong.

If a fault-injection tool is available (mutmut/cosmic-ray equivalent),
running it against the legal-critical validation paths (STOP order,
FUNDSTELLE typing, legal_ref format) is high-value before trusting
`./check.sh` green on those paths specifically — the same
"does this check actually catch a real fault" question, made mechanical
rather than judged by eye.
