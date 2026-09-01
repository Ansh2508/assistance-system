---
name: legal-updater
description: Check and update legal references in YAML files. Use when verifying ADR versions, DGUV updates.
---

# Legal Updater Skill

## Purpose
Verify and update legal references across all YAML verticals.

## Current Valid References
- ADR 2025 (effective 01.01.2025)
- BKrFQG 2026 amendment (effective 03.02.2026)
- ArbSchG (current consolidation)
- DGUV Vorschrift 1 (current)
- DGUV Vorschrift 68 (Flurförderzeuge, current)
- DGUV Vorschrift 70 (LKW/Fahrzeuge, current)
- GGA/GDA: map to gda_id fields

## Before Running Crawler
1. git pull origin develop
2. List all YAML files with legal_ref fields
3. Extract unique legal references
4. Verify each against:
   - https://www.dguv.de/
   - https://www.gesetze-im-internet.de/
5. Flag any ADR 2023, outdated DGUV, non-existent paragraphs
6. Report findings - do NOT edit YAMLs

## What NOT to Do
- Never invent legal references
- Never cite OSHA, HSE, Swiss law in DE
- Never assume a law exists - always verify
- Never change vertical without running ./check.sh

## When Complete
Report which refs are current, which need updating, which are hallucinated.
Do NOT commit. Report findings only.

## Tag Every Claim (added from real cross-country legal research)

When verifying a reference or researching a new one, tag it so a reader
can tell what was actually checked:
- `[FETCHED-FULL]` — read the primary source itself (gesetze-im-internet.de,
  dguv.de, an actual court decision), not a summary of it
- `[SECONDARY]` — only a summary, commentary, or a source citing the
  primary was available
- `[NOT VERIFIED]` — could not confirm either way
- `[DOES NOT RESOLVE]` — the source was checked and does NOT support the
  claim, even though it looked like it should

This caught real errors in a different domain this session: a widely
repeated claim about a legal rule turned out to be backwards once the
actual court ruling was read in full rather than trusted from a summary
— the correct reading was the opposite of what secondary sources
implied, and reversed a design decision that had been treated as
settled. "Verify against the primary source" already covers this in
principle; the tags make it checkable in the output, not just implied.

If a claim can only be tagged `[SECONDARY]` or `[NOT VERIFIED]` and it
matters (changes a legal_ref, changes STOP-order guidance), say so
explicitly in the report rather than presenting it with the same
confidence as a `[FETCHED-FULL]` finding.
