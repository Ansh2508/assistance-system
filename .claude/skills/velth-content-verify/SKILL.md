---
name: velth-content-verify
description: Verify velth LinkedIn drafts (carousel PDFs, captions, first comments) for content correctness before publishing. Checks every legal citation, norm reference, number, and date against the canonical fact sheet and primary sources; flags outdated law, wrong paragraph numbers, unverifiable claims, and date-anchored wording that will age badly. MUST be used on every uploaded or updated draft before it is approved in Buffer, whenever the user says "check this draft", "prüfe den Post", "review vor Freigabe", "content check", or uploads a carousel PDF or caption for review. Also use when auditing the existing Drive library or Buffer queue. A single wrong § or an outdated rule destroys velth's credibility with SiFas, CFOs, and Berufsgenossenschaften, so when in doubt, this skill applies.
---

# velth content verify

Adversarial pre-publication review of velth safety-content drafts. The maker of a draft is never its checker: content is built by one model (typically Claude), verified by another (this skill, typically run by Codex CLI). Your job is to find errors, not to confirm quality. A review that finds nothing must state what it verified and how, or it is worthless.

## Non-negotiable principles

1. **Primary sources only.** A legal claim is confirmed by gesetze-im-internet.de, baua.de, dguv.de (Publikationsdatenbank/Regelwerk), bmas.de, or the official text of the cited norm. Blog posts, vendor sites, and news aggregators can raise suspicion but can NEVER confirm correctness.
2. **Canon before web.** Check `references/legal_canon.md` first. If the draft contradicts the canon, that is a P0 finding even before any web lookup. If the canon is silent, verify against primary sources.
3. **Absence of evidence is a finding.** If a claim cannot be verified within the session, it is flagged UNVERIFIED with severity, never silently passed. UNVERIFIED claims are not publishable.
4. **Existence errors cut both ways.** Before declaring a cited rule nonexistent or outdated, check whether it was newly introduced (example that actually happened: DGUV Regel 100-002 looked wrong but is real, published 01/2026 with the reformed DGUV Vorschrift 2). Before accepting a familiar-looking citation, check whether a reform replaced it.
5. **Today's date matters.** Resolve every relative or anchored date against the current date. "Ab dem 2. August 2026" is wrong wording the day after 2 August 2026. Month names ("im Juli") are wrong the moment the posting date moves.
6. **Report, do not repair.** Findings go into the report with exact location, quote, evidence, and a proposed correction. The fix itself is a separate, human-approved step.

## Inputs

One or more of:
- Carousel PDF (extract text with `pdftotext <file> -`; page count must be 7 unless stated otherwise)
- Caption text (Buffer draft body)
- First-comment source block
- Posting date (from Buffer `dueAt`; if unknown, assume publication may happen any time in the next 90 days)

## Workflow

### Step 1: Deterministic pre-checks (run the script first)

```
python scripts/precheck.py <textfile-or-pdf> [--posting-date YYYY-MM-DD]
```

The script flags mechanically detectable issues: em/en dashes, street address, forbidden number patterns, date-anchored wording, month names, missing year on "seit <Monat>". Its output is a starting list, never the whole review.

### Step 2: Reference extraction

List EVERY checkable claim in the draft, one row each:
- Legal citations (§, Abs., Satz, law abbreviation)
- Norms and rules (DIN EN, DGUV Vorschrift/Regel/Information, TRBS, TRGS, ASR, AMR, VDI, MuSchR, BK numbers)
- Numbers (fines, thresholds, statistics, dates, percentages, physical values)
- Legal-effect claims (Vermutungswirkung, Beweislastumkehr, Haftungsübergang, Beschäftigungsverbot)
- Company claims about velth itself (partnerships, programmes, patent, pilot phase, role of the human expert) — checked against `references/company_context.md`

No claim is exempt because it "sounds standard". The most dangerous errors sound standard.

### Step 3: Canon match

For each extracted claim, check `references/legal_canon.md` and `references/known_traps.md`. Additionally check every statement ABOUT velth itself (product, roles, partners, pilots, patent, programmes) against `references/company_context.md`:
- Matches canon → mark CANON-OK with the canon line
- Contradicts canon → P0 finding, cite both versions
- Not covered → goes to Step 4

### Step 4: Primary-source verification

For claims not settled by canon, verify against the primary source. Quote the decisive wording (a few words suffice) and the URL. Specifically verify:
- The paragraph SAYS what the draft claims (right §, right Absatz, right content)
- The rule is IN FORCE at posting date (not repealed, not superseded by reform; check Inkrafttreten of replacements)
- Numbers match exactly (5.000 is not 30.000; 0,84 % is not 0,8 %)
- Legal effects are real (Vermutungswirkung exists for ASR via ArbStättV; it does NOT exist for ASTA recommendations or DGUV Regeln)

### Step 5: Aging check

With the posting date in hand, ask of every time expression: will this sentence still be true and natural in 90 days? Flag month names, "diesen Monat", "seit <Monat>" without year, "Ab dem <Datum>" once the date passes, "neu"/"jetzt" tied to events older than a year. Rhetorical uses ("die GBU von gestern", "STAND HEUTE?" as a section label) are fine; calendar anchors are not.

### Step 6: Report

Write the report in this exact structure:

```
# Content Review: <draft name>
Datum der Prüfung / angenommenes Postingdatum: ...
Ergebnis: FREIGABE EMPFOHLEN | FREIGABE NUR NACH KORREKTUR | NICHT FREIGEBEN

## P0 — Sachlich falsch (blockiert Freigabe)
- [Fundstelle, wörtliches Zitat] → Beleg der Falschheit (Quelle) → Korrekturvorschlag

## P1 — Unbelegt oder alterungsanfällig (vor Freigabe klären)
- ...

## P2 — Stil/Kanonabweichung (sollte gefixt werden)
- ...

## Verifiziert (Stichprobe der Belege)
- [Claim] → CANON-OK Zeile X | Primärquelle + Zitat

## Nicht prüfbar in dieser Session
- [Claim] → warum nicht, empfohlener Prüfweg
```

Policy decisions (Bruno, 2026-08-03): (a) A missing first comment in Buffer is NOT a finding — first comments are posted manually at publication time from the prepared file. (b) The 40-75 word band per slide is P2 only, never blocking. (c) The following company claims are globally confirmed and never flagged: "Gebaut in München", "gehostet in Frankfurt", free trial on velth.io, pilot access CTA, "TU München · Campus Founders".

Severity rules: wrong §/number/rule status = P0. Unverifiable claim, missing year, aging anchor = P1. Dash/address/canon-wording violations = P2. Any P0 → NICHT FREIGEBEN. Any P1 → FREIGABE NUR NACH KORREKTUR.

## Codex CLI integration

This skill is self-contained and model-agnostic. For Codex CLI, add to the repository `AGENTS.md`:

```
## Content verification
Before approving any velth social draft, follow skills/velth-content-verify/SKILL.md
verbatim. Run scripts/precheck.py first, then the manual verification steps.
Never skip Step 2 extraction. Never confirm a legal claim from a non-primary source.
```

Codex runs the same workflow; the value of using a different model family than the one that wrote the draft is that shared blind spots between maker and checker are less likely. If web access is unavailable in the Codex session, everything not settled by canon goes to "Nicht prüfbar" — it must NOT be guessed.

## Reference files

- `references/company_context.md` — what velth is, who it serves, and the mandatory wording frame (80/100 role split, "Ausbau statt Ablösung", caption/slide rules). Read FIRST if you have no prior context on velth; positioning violations found here are findings like any other.
- `references/legal_canon.md` — verified canonical facts and mandatory formulations. Read fully for every review.
- `references/known_traps.md` — errors actually made or nearly made in this pipeline; each entry names the wrong version, the right version, and the lesson. Read fully for every review.
