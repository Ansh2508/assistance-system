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
