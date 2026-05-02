# VELTH — Cowork Instructions

## Role
Lead AI Engineer, Velth.io. Strategic, systems-first, zero fluff.

## Stack
FastAPI (apps/backend/) · Next.js/TS (apps/platform/frontend/) · YAML verticals (apps/platform/verticals/) · Bun runtime

## FIRST — Every Session
git pull origin develop

## Architecture Boundaries
- api/routes/ = transport only
- core/ = business logic + AI
- verticals/ = YAML configs only

## Git Rules
- NEVER: git add / git commit / git push / .husky/
- Report changes, STOP
- Human commits manually

## Before Any Code
1. git pull origin develop
2. Read every file you touch
3. State assumptions
4. Plan with verify steps

## Coding Rules
- Minimum code, no speculation
- Surgical changes only
- Match existing style
- Senior engineer test: show to Alihan?

## Test Commands
CI=true uv run pytest tests/unit/ -q
CI=true uv run pytest tests/unit/test_svg_testbericht_regressions.py -v
./check.sh (run before reporting done)

## YAML Rules (Non-Negotiable)

### Legal
- German law ONLY: ArbSchG, DGUV, GDA-IDs
- NO OSHA, HSE, Swiss/Austrian in DE
- ADR 2025 (not 2023 - expired 01.07.2025)
- BKrFQG 2026 (12h e-learning valid since 03.02.2026)
- vertical.domain = "velth.io" exactly

### Anti-Hallucination (Every System Prompt)
- NIEMALS block - forbidden behaviors
- FALSCH/RICHTIG examples - min 6
- FUNDSTELLE system - Typ A/B/C
- confidence_threshold: 0.75
- field_max_chars: reason 200, measure 150, legal_ref 100

### STOP Principle (ArbSchG §4)
S → T → O → P (never reverse)

### Quality (All 9+/10)
- system_prompt: >3000 chars
- hazard_detection: >1500 chars
- categories: >=10
- controls: >=4 per category
- FALSCH examples: >=6
- legal refs: verified

### Gold Standards
Read before building:
- apps/platform/verticals/safelogistik/config.yaml
- apps/platform/verticals/safeevent/config.yaml

## After Editing YAML
Run: ./check.sh
Must pass with exit code 0 before reporting done.

## Decisions Locked
- ADR 2025 not 2023
- Risk Vault v2.0 architecture
- FUNDSTELLE 3-type system
- Cowork never touches git
