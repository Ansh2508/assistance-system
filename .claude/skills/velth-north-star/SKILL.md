---
name: velth-north-star
description: The strategic decision lens for every non-trivial VELTH decision — architecture, roadmap, product scope, partnership, pricing, expansion, hiring. Load BEFORE deciding, not after building. Encodes the moat ladder VELTH is climbing, the data properties that make tomorrow's continual learning possible or impossible, the regulatory clock that actually binds, and the robotics/Machinery-Regulation opening. Also load when an agent is about to defer, skip, or simplify away something that touches the event log, hazard_feedback, provenance, or document lineage — those are moat-bearing and the bar is different. Triggers on "should we build", "is this worth it", "which do we prioritise", "new vertical", "new market", "partnership", "data model", "what do we tell an investor/BG/insurer", or any decision where speed and data integrity appear to trade off.
---

# VELTH North Star — the decision lens

VELTH is a forever-private pan-EU risk-intelligence company that currently ships
workplace-safety documentation. The documents are the wedge. The asset is the
accumulating record of expert judgment about physical-world danger, with legal
consequence attached.

Every section below exists to make one kind of decision better. If a section is
not changing a decision you are actually making, skip it.

---

## 0. RESEARCH MANDATE — read this before trusting anything below

**This file decays.** Frontier AI, EU regulation, and the competitive landscape
all move faster than this document is revised. Facts below carry an
`[as of YYYY-MM]` marker. Any fact older than ~4 months is a hypothesis, not a
fact.

**Mandatory before acting on any time-sensitive claim in this skill:**

1. **Web-search to re-verify** any `[as of ...]` fact you are about to make a
   real decision on — a regulatory date, a competitor's position, a technique's
   state of the art, a funding round, a standard's status.
2. **Prefer primary sources.** EUR-Lex over a compliance vendor's blog. arXiv
   over a summary of arXiv. The DGUV's own publications over trade press.
   A GitHub repo over a description of the repo.
3. **Read the paper, not the abstract**, when a number will drive an
   architecture decision. Abstracts round; methods sections disclose the
   conditions under which the number holds.
4. **Search in German** for anything DACH-regulatory. The English coverage of
   DGUV / BG / ArbSchG topics is thin and often wrong on specifics.
5. **When research contradicts this file, the research wins** — and update this
   file in the same session. A skill that silently goes stale is worse than no
   skill, because it launders an outdated assumption as institutional knowledge.

**Standing research questions** — re-check these each quarter, they are the ones
most likely to invalidate a VELTH plan:

- Has the continual-learning forgetting problem moved again? (§2)
- Have the Machinery Regulation delegated acts or harmonized standards landed? (§5)
- Has anyone entered the employer-side robot-deployment risk assessment lane? (§5)
- Has the DGUV/BG digital agenda produced a procurement surface? (§4)
- Has a frontier lab shipped a vertical safety/compliance product? (§1)

---

## 1. The moat ladder — what VELTH is actually climbing

From the Stanford CodeX framework (Mandal & Sinha, *Defensible Moats for Vertical
AI Application Companies*, 2026), five product moats in ascending defensibility.
VELTH's honest current position:

| Rung | Moat | VELTH status | What moves it up |
|---|---|---|---|
| A | Workflows & UX | **Weak.** External SiFa testers report the UI is unintuitive; one gave up in ~10 min. Reports too long to be usable. | Real usability work. Cheapest rung, also the most replicable — do not over-invest here. |
| B | Vertical harness & tools | **Medium.** 6-document pipeline, vault YAML, deterministic renderers. | Deeper integrations into systems SiFas already live in. |
| C | Built-in compliance | **Strongest current rung.** Nohl gate (risk_class never from LLM), legal registry, pre-export gate, deterministic RPZ. | Keep. This is what horizontal players won't absorb. |
| D | The "Brain" | **Building.** 9,185-entry catalog, but engine sees only the human-authored subset until promotion. | The promotion workflow is the bottleneck, not generation. |
| E | **Embedded judgment** | **Leaking.** `hazard_feedback` — SiFa accept/reject/edit with before/after risk — is the raw material, and it silently 500'd from B11 until Aug 2026. | Every design decision that preserves and enriches correction data. |

**The rule this ladder produces:** when two options are otherwise close, take the
one that moves up a rung. When an option is faster but costs a rung, it is not
faster — it is borrowing from the only thing that compounds.

**Why E is the top rung and why it's fragile:** the framework's own argument is
that embedded judgment "compounds: every additional customer and every observed
decision widens the gap" — but it can only compound if the decisions are
*captured*. A dropped correction is not a delayed gain; it is a permanently lost
observation. There is no backfill for judgment that was never recorded.

---

## 2. Continual-learning readiness — the five properties

The technique is no longer the blocker. **The data shape is.**

### 2.1 The mechanism (why this is now real) `[as of 2026-08]`

Catastrophic forgetting was the reason you couldn't update a deployed model on
new knowledge. Sparse memory finetuning (Lin, Zettlemoyer, Ghosh, Yih, Markosyan,
Berges, Oğuz — arXiv 2510.15103) reports, on the same knowledge-acquisition
budget:

- full finetuning: NaturalQuestions F1 **−89%**
- LoRA: **−71%**
- sparse memory finetuning: **−11%**

Mechanism: memory-layer models are sparsely updated by design; update only the
memory slots highly activated by the new knowledge *relative to their activation
on pretraining data*. Interference is reduced because the trainable parameters
stop being shared across all tasks.

Serving is solved at the infrastructure layer: S-LoRA serves thousands of
concurrent adapters; vLLM hot-loads adapters in GPU memory with an SGMV decode
kernel fusing per-adapter work into one launch per decode step, so multiple
adapters share a batch. Trajectory's C-LoRA (open-sourced, `NovaSky-AI/SkyRL`)
folds training into a live service, ~2.81× experiment throughput.

**The constraint that decides adapter granularity:** efficient serving of a
distinct weight set needs thousands of concurrent sequences decoding against it.
Per-**company** adapters are uneconomic until a company generates that much
concurrent traffic. Per-**vertical** and per-**BG** adapters are viable now.
Design the data model so granularity is a runtime choice, not a schema rewrite.

### 2.2 The five properties — check these before any new table or event type ships

Data has to carry all five to be trainable later. Missing any one is
unrecoverable after the fact.

1. **Tenant attribution** — company_id AND vertical_id on every judgment record.
   Determines adapter routing granularity later. Cheap now, impossible to
   reconstruct later.
2. **Expert identity + credential** — *which* SiFa, with what qualification.
   Not for display; for weighting. A correction from a certified SiFa with 20
   years in Bau is not the same training signal as an unverified user's edit,
   and a model trained as if they were equal is worse than one trained on the
   credentialed subset alone.
3. **Accept/reject/edit signal with before→after values** — this is a preference
   pair. `hazard_feedback.action` (deleted/added/edited/risk_changed/reanalyzed)
   plus `original_risk`/`new_risk` is DPO-shaped training data already. Preserve
   the *rejected* branch; a dataset of only accepted outputs teaches nothing
   about the boundary.
4. **Temporal + version anchors** — timestamp, model version, catalog version,
   vault version. Without these you cannot do clean temporal splits (train on
   past, eval on future), you cannot detect distribution shift, and you cannot
   tell whether a correction argues against a model that no longer exists.
5. **Outcome linkage** — did the workplace actually get safer? Re-inspection
   result, subsequent accident/near-miss, BG audit finding, Maßnahme
   verification.

**Properties 1–4 give you preference data. Only 5 gives you ground truth.**

This is the single most important distinction in this file. Preference data
teaches the model what SiFas *prefer*. Outcome data teaches it what was
*actually right*. Almost no vertical AI company ever gets (5) — it requires
being in the loop long enough to observe consequences. VELTH structurally can:
re-inspections happen, Maßnahmen get verified, BGs record accidents.

**If outcome linkage is not yet captured, treat adding it as the highest-leverage
data-model work available.** It is the difference between a preference-tuned
assistant and an actual risk-intelligence model — and it is the only asset in
this whole document that an insurer or a BG would pay for directly.

### 2.3 The brittleness finding — why correction data is the fix, not a stopgap

`[as of 2026-05]` Two preprints from LeCun's group formally characterised when
JEPA-family architectures recover real-world structure, and a paired benchmark
found **current models collapse under minor visual shifts**.

VELTH's own logged failure modes are instances of exactly this: near-identical
scenes producing divergent hazard sets, ambiguous visual chips ("Fußkappen
fehlen" collapsing three distinct referents), the same input scoring 6/10 then
8/10 across runs.

**Decision consequence:** do not plan on frontier visual understanding fixing
these on its own timeline. The correction data is not a workaround while waiting
for better models — it is the artifact the better models will need, and it is
scarce precisely because it requires a certified expert in a real workplace.

### 2.4 Own-model trigger — sovereignty before cost `[as of 2026-08]`

VELTH runs Claude via Bedrock EU today, with Tier-2 LoRA/DPO fine-tuning infra
built and merged, 0 training rows at time of writing. "Should we train/host our
own model" is a real future question, not a hyperscaler fantasy — but it needs a
trigger, not a vibe. Two independent 2026 sources converge: self-hosting an
open-weight model beats API cost somewhere between **~$4k–20k/month of displaced
frontier-tier API spend**, far below an older ~$6M/year figure found this session
and now explicitly superseded — do not cite the $6M number again.

**The decision rule — two triggers, expected in this order:**

1. **Data-sovereignty (expected FIRST).** One signed DACH/BG-adjacent customer,
   or a credible pipeline of 2–3, contractually requiring workplace-safety data
   never leave a customer-controlled or German-only environment — a demand
   Bedrock EU cannot satisfy (on-prem / VPC-isolated / no non-EU sub-processor).
   This alone justifies a scoped self-host pilot. Note: sovereignty is satisfied
   by self-hosting an off-the-shelf open-weight model — it does **not** require
   Tier-2 training rows first.
2. **Cost (expected LATER).** Sustained equivalent inference spend above
   ~€15–20k/month, concentrated on the expensive frontier tier.

**Open-weight candidates for a future German/legal-domain base**, Apache-2.0,
genuinely self-hostable (verify license currency before committing, §0):
**Teuken-7B** (OpenGPT-X — Fraunhofer/Jülich/TU Dresden/DFKI, BMWK-funded, all 24
EU languages, heavy German instruction-tuning — the strongest sovereignty
story); **EuroLLM-9B** (Unbabel/IST/Edinburgh, EU-funded, best raw EU-language
quality among self-hostable options). Precedent that domain adaptation beats
scale for German legal reasoning: **SteuerLLM** (arXiv 2602.11081), a
German-tax-law model beating larger general models on its domain.

**This is not a near-term build.** §2.2's outcome-linkage work and the existing
Tier-2 infra remain the priority; nothing here changes that sequencing.

---

## 3. Data-moat integrity — non-negotiable rules

These are learned from real incidents, not principles. Each has a scar behind it.

**R1 — Provenance columns are load-bearing, not metadata.** Who created this
version, when, under which model, from which catalog. Continual-learning
research names memory provenance — not memory capacity — as the binding
constraint. A document trail with unknown authorship cannot be trained on,
audited, or defended.

**R2 — Never fabricate a provenance value. NULL beats a plausible guess.**
Backfilling `created_by` with "probably the project owner" produces a false
claim on a compliance document. An honest gap is recoverable; a fabricated
lineage poisons everything downstream that trusts it — including any future
model trained on it. *(Scar: vault_doc_versions, Aug 2026 — 1,498 rows left
deliberately NULL.)*

**R3 — Feedback writes must be transactionally coupled to what they're feedback
about, or they silently drop.** *(Scar: `hazard_feedback.analysis_id` carried an
enforced FK to `gbu_versions.id` since B11, but GBU versions are written
fire-and-forget in a background thread and the ID never reached the dashboard.
Every SiFa dashboard correction 500'd for months. Invisible because
`gbu_versions` had 0 rows in production.)*

**R4 — Every fire-and-forget write path needs a success counter and an alert on
zero.** Zero rows and no activity look identical from the outside. This is how
R3's failure survived months of active use. If a path can fail silently, assume
it eventually will, and instrument accordingly.

**R5 — A correction is only as valuable as the state it corrected.** Capture
what the model proposed alongside what the human changed it to. A record showing
only the final value is an edit log; a record showing both is training data.

**R6 — Apply the same rigor to access control as to the data itself.** Data that
cannot be shown to have been properly access-controlled cannot be shown to an
auditor, a regulator, or an insurance partner — which destroys its commercial
value regardless of its content. *(Scar: `audit_events` has an RLS policy
checking `profiles.is_admin`, but the connecting role has `rolbypassrls=TRUE`,
so the policy never enforces. The application-layer `get_current_admin`
dependency is the sole real lock. Any repository method reading that table must
assume the DB will not help.)*

---

## 4. The regulatory clock

`[as of 2026-08 — re-verify every date before planning against it, §0]`

| Date | What binds | Status |
|---|---|---|
| 2 Aug 2026 | AI Act Art. 50 transparency obligations | Did **not** move in the Omnibus |
| 2 Dec 2026 | Watermarking grace period ends (shortened 6mo→3mo) | Did **not** move |
| **20 Jan 2027** | **EU Machinery Regulation 2023/1230 applies in full** | **No grace period. No transition.** |
| 2 Dec 2027 | AI Act Annex III high-risk standalone | Moved +16 months (Omnibus) |
| 2 Aug 2028 | AI Act embedded products (Annex I) | Moved +12 months (Omnibus) |

**The Omnibus carve-out (political agreement 7 May 2026)** removed embedded AI
under the Machinery Regulation from the AI Act's *direct* application; AI-safety
obligations for machinery now arrive via **delegated acts under 2023/1230**
instead. Read this correctly: it is a re-channelling, not a reprieve. The
Machinery Regulation date did not move, the delegated acts are not written, and
the harmonized standards giving presumption of conformity are unfinished — so
every AI-enabled machine conformity case is currently bespoke.

**German-specific, and moving:**
- DGUV Vorschrift 2 revised, in force from 1 Jan 2026 — digital care models,
  digital competency requirements for SiFas and Betriebsärzte.
- Joint DGUV / DRV / GKV-Spitzenverband digital position paper (Nov 2025)
  calling for actively shaping digitalisation and explicitly for **European
  solutions**.
- VBG–BGHM "NOVA" IT cooperation building `nova.Applications` as shared
  Arbeits-/Gesundheitsschutz infrastructure.

**BG contribution mechanics — know these before any BG conversation.**
Contribution = Umlagesoll ÷ (Arbeitsentgelte × Gefahrklasse). Gefahrklassen are
set per Gewerbezweig from the ratio of paid benefits to wages, fixed in a
Gefahrtarif valid ≤6 years, approved by the BAS (§157 SGB VII). Individual
company risk enters **only** through Zuschläge/Nachlässe based on reportable
accidents.

**Consequence:** BGs do not compete on price and cannot buy underwriting alpha.
The doors that exist are (a) prevention-effectiveness evidence feeding the
Zuschlag/Nachlass and Prämien mechanisms, (b) the private layer —
Betriebshaftpflicht, product liability, D&O — where competitive underwriting is
real, and (c) partnership into the DGUV's own stated European-digital agenda.
Pitching a BG as if it were a US carrier will fail on structure, not on pitch
quality.

---

## 5. Robotics — the Machinery Regulation opening

`[as of 2026-08]`

**Decision, dated: Anshu, 2026-08-11 — DEFER.** The deadline below (20 Jan 2027,
no grace period) and the documentation-volume finding make a real case for
treating this as urgent — that case is recorded honestly below, not softened.
The deliberate call is to hold anyway and stay focused on the core vertical.
Revisit if a concrete signal changes: a named robotics-customer inquiry, or if
Q4 2026 arrives without this having been revisited. This is a considered
override of the framing that follows, not an oversight — do not silently
re-escalate this section's urgency without a new trigger.

### 5.1 Why this is a real market with a countdown

From 20 Jan 2027, machinery placed on the EU market must comply with 2023/1230.
New mandatory requirements that did not exist under 2006/42/EC:

- **Safety review of AI and self-evolving behaviour** (new EHSR category)
- **Protection of safety functions against corruption** (cybersecurity), with
  security updates required for **10 years** after placement
- **Digital documentation** as default; paper only on request
- **10-year technical file retention**
- **Mandatory notified-body assessment** for high-risk Annex I Part A categories
  — self-declaration no longer sufficient. The trigger, per Recital 54
  (primary-confirmed): self-evolving ML behaviour that **ensures a safety
  function** — "data dependency, opacity, autonomy and connectivity." VELTH's
  own architecture (deterministic risk_class from a catalog, never from an LLM;
  the LLM extracts/proposes, a human confirms) is the pattern that stays
  outside this tier by design — the same reason §6's anti-test protects rung C
  today would protect a robotics product tomorrow. Annex I Part A items 5/6's
  exact wording was only secondary-sourced as of 2026-08 — read
  EUR-Lex CELEX:32023R1230 Annex I directly before any external or legal use.

Documentation volume: a single product model's complete technical file runs
**800–2,000 pages**.

### 5.2 The substantial-modification rule — VELTH's actual bridge

Substantially modifying a machine, **physically or digitally**, makes you the
manufacturer of the modified machine, with full conformity, CE marking and
liability duties. Retrofitting an AI vision system onto existing machinery
triggers this.

**This is the finding to act on.** German SMEs integrating or retrofitting robots
are becoming manufacturers under EU law, mostly without knowing it. That is
VELTH's existing customer profile, facing a new obligation, on a hard deadline,
with no established provider serving them.

### 5.3 The lane — manufacturer-side vs employer-side

Do not confuse these. They are different products for different buyers.

| | Manufacturer-side | **Employer-side (VELTH's lane)** |
|---|---|---|
| Question | Is this robot *model* compliant? | Is this robot, in *this* hall, beside *these* workers, safe? |
| Artifact | CE technical file, DoC | Gefährdungsbeurteilung §5 ArbSchG, Betriebsanweisung, Unterweisung |
| Buyer | OEM / importer | Employer / integrator / SME |
| Occupied by | HardwareCompliance (YC W26), TÜV, notified bodies, consultancies | **Largely open** |

This is the same structural split as the BG BAU thesis already in play: BesA ends
at "deficiency found"; VELTH owns the employer-side remediation loop. Verify the
employer-side lane is still open before committing (§0).

### 5.4 The standards stack

- **ISO 12100** — risk assessment/reduction framework (the base; everything
  inherits from it)
- **ISO 13849-1** — safety-related control system parts, PLd/PLe
- **IEC 62061** — functional safety, SIL-rated
- **ISO 10218-1/2:2025** — the core robot standard set, published Feb 2025;
  check current Official Journal harmonisation citation status
- **ISO/TS 15066** — collaborative robots (cobots); note PFL cobots still
  require a full risk assessment

**The six documents a robot deployment needs**, in build order — risk assessment
first, because every other document inherits its findings:
1. Risk assessment → 2. Facility readiness assessment → 3. Energy control
procedure (LOTO) → 4. EU technical file → 5. Training records → 6. Incident
reports

**Note the shape:** that is a document *cascade* inheriting from one upstream
risk assessment. VELTH's existing 6-document pipeline is architecturally the
same pattern in a different domain. That is why this expansion is adjacent
rather than a rebuild — and also why VELTH's known state-propagation P0 (documents
reading different state snapshots) must be fixed before entering a domain where
the cascade is legally binding.

**The catalog is genuinely net-new, not a reskin `[as of 2026-08]`.** ISO 12100's
risk-assessment loop maps cleanly onto the existing engine (hazard ID → S×W
rating → risk_class → measures → residual is structurally the ISO 12100 loop).
The *content* does not transfer: robot-specific hazard classes governed by ISO
10218-1/-2 and ISO/TS 15066 — collaborative contact forces (biomechanical limits
per body region), speed-and-separation zones, unexpected energised movement in
a shared workspace, end-effector hazards, mode-dependent (teach/auto/manual)
hazards — do not exist in a construction/general-safety catalog. Read ISO
10218-1/-2:2025 and ISO/TS 15066 in full before scoping this catalog's size.

---

## 6. Expansion decision framework

Before committing to a new vertical, market, or product line, all four must pass:

1. **Regulatory burden test** — does the domain require certifications, audit
   trails, or specific compliance frameworks? If not, foundation models eat it
   within ~18 months and there is no durable position.
2. **Proprietary data test** — does operating in this domain accumulate data
   that is hard to get elsewhere and that compounds per customer? If the data is
   publicly available, the product is a wrapper.
3. **Workflow depth test** — is the workflow multi-step with real state, or a
   single-shot generation? Single-step tasks are trivially replicable.
4. **Outcome observability test** *(VELTH-specific addition)* — can you observe
   whether your output made the real world safer? If not, you accumulate
   preference data only, and forfeit the ground-truth advantage from §2.2.

**Anti-test — reject if true:** the expansion requires abandoning determinism in
risk classification. The Nohl gate (risk_class computed in Python, never trusted
from an LLM) is the compliance moat. A vertical that cannot be served without
LLM-decided risk levels is a vertical that erodes the strongest current rung.

---

## 7. The three-audience test

Before shipping anything that touches judgment data, documents, or provenance,
ask all three. They ask different questions and all three must pass.

**The SiFa** — "Would I sign this?" A certified professional puts their name and
liability on VELTH's output. Test: is every claim traceable to a real legal
reference or an explicit gap statement? Is anything fabricated, including
plausible-sounding measures not in the vault?

**The BG auditor** — "Show me how this decision was reached." Tests provenance
end-to-end: which model, which catalog version, which human confirmed it, when,
under what access control. §3's rules exist for this audience.

**The insurance partner** — "Why should I trust this data enough to price on
it?" The hardest one. Underwriting research consistently finds the blocker for
AI-driven risk selection is not model quality but data cleanliness and
reliability. This audience is why R1–R6 are non-negotiable rather than
aspirational.

---

## 8. Failure modes this skill exists to prevent

- Shipping a data model that cannot be trained on later, because tenant,
  credential, or outcome fields were "not needed yet."
- Treating a silent write failure as a low-priority bug rather than a moat leak.
- Deferring a decision on grounds of scope discipline when the real cost is a
  lost, unrecoverable observation.
- Pitching a BG with a US-carrier framing.
- Entering robotics without fixing state propagation first.
- Trusting any dated fact in this file without re-verifying it (§0).
- Optimising a rung-A improvement while a rung-E leak is open.

### 8.1 The specific way VELTH has actually lost frontier progress — not
hypothetical, this already happened `[as of 2026-08]`

Task 2.1's entire arc (see /areas/continual-learning-readiness.md for the
full history) is a real case study, not a cautionary tale invented for this
section: multiple builds — Build 3, Build 4, Build 5, a final enrichment
pass — each fully built, tested green, hash-verified on disk, sat
**uncommitted across multiple sessions** while new adjacent work kept
getting scoped on top. The all-87-table final audit is genuinely excellent
work. None of it compounded the moat until someone actually ran the
commit. A finished capability sitting unmerged earns VELTH exactly the same
data-moat position as a capability that was never built — the frontier
progress existed and was, for that whole window, indistinguishable from
not existing.

**The mechanism, stated precisely so it's checkable, not just a mood:** the
actual risk to "missing AI/data frontier progress" is almost never a
dramatic, loud failure. It's one of three quiet, specific shapes, each with
a real incident behind it:

1. **A capability is built, tested, and never merged.** (Task 2.1's whole
   arc, above — the biggest single instance found in this project's own
   history.) The fix is mechanical, not aspirational: a build task is not
   "done" until it is committed and on the branch it needs to be on. A
   staged, hash-verified, green-tested deliverable sitting in a scratch
   folder is a TODO, not a result — track it as one explicitly rather than
   letting "tested green" read as "shipped."
2. **A dependency a new capability needs is silently absent, and passes
   anyway on whichever machine happens to have it already.** (The real
   `hypothesis` incident, 2026-08-11 — two new test files imported it,
   neither `pyproject.toml` nor `uv.lock` declared it, and it passed
   locally because it was ambiently installed. Would have failed on any
   clean checkout, including CI, silently gatekeeping the very tests meant
   to prove the new capability correct.) See velth-test-strategy's Pattern
   7 for the mechanical check this now requires on every new test file.
3. **A stub or placeholder correctly defers implementation, but the text
   inside it silently points at a pattern that's already stale by the time
   someone acts on it.** (The real `doc_verify.py` incident, same date — a
   `NotImplementedError` message told a future implementer to use a
   pre-migration Supabase pattern for data that had already moved to the
   repository layer. No guardrail could see it, because it was a string,
   not a real call site, until someone followed the instruction.) See
   velth-test-strategy's Pattern 8.

**The common thread across all three:** none of them are caught by "did the
tests pass." They're caught by "is the thing that tested green actually
live, on the branch it needs to be on, with every dependency it needs
declared, pointing at what's actually current" — a distinct, mechanical
question from correctness, and one this skill's moat framing depends on
being asked every time, not just when something already looks wrong.

---

## 9. Insurance intelligence — the lane and the DACH catch

`[as of 2026-08]`

§7's "insurance partner" audience test names *why* this matters. This section
records *how it actually routes*, researched this session — because the naive
version of this plan (copy a US workers'-comp-MGA model onto BG data) fails on
DACH market structure, not on data quality.

**COPE is the wrong framework.** COPE (Construction, Occupancy, Protection,
Exposure) is the standard commercial-*property* underwriting framework.
Mapped against VELTH's data field-by-field: Occupancy overlaps partially
(hazard categories); Protection is a false friend (VELTH's controls are worker
safeguards — guarding, PPE, LOTO — not fire/property defence); Construction and
Exposure (external/neighbour risk) have no VELTH analog at all. **VELTH insures
the worker-hazard relationship, not the building.** The natural home is
workers'-comp / employers'-liability / occupational-accident lines, not
property.

**A real precedent exists, and it clarifies the business-model choice.**
Insurate Inc. is a US workers'-comp **MGA** (managing general agent —
underwrites and distributes on a carrier's capacity, e.g. SiriusPoint,
Markel; carries no balance-sheet risk itself). Its Safe-Tier algorithm prices
premium off safety-culture data — this is "workplace-safety data →
underwriting signal," already productised. The three roles available to
VELTH: **data provider** (sell the signal, low capital, stays a vendor),
**MGA** (capture underwriting margin on a carrier's paper, the Insurate-proven
path, no balance-sheet risk), or **full carrier** (not realistic near-term).

**The DACH catch — this is decisive, per §4's own BG mechanics.** German
statutory employer-accident insurance runs through the Berufsgenossenschaft
monopoly: contribution = Umlagesoll ÷ (Arbeitsentgelte × Gefahrklasse); BGs do
not compete on price and cannot buy underwriting alpha (§4). **The Insurate/MGA
model does not directly transplant onto the statutory home market.** Per §4's
existing doors, insurance intelligence most plausibly enters via **(b), the
private layer** — Betriebshaftpflicht, product liability, D&O, where
competitive underwriting is real — not the statutory BG layer. Do not pitch
this as "we'll price BG contributions"; pitch the private-liability layer, or
the Zuschlag/Nachlass prevention-evidence door §4 already names.

**Parametric insurance is expanding into commercial lines** (trigger-based
payout, not assessed loss) and is a real, growing design target — but it needs
a richer outcome signal than currently planned. §2.2's outcome-linkage record
(`outcome_type ∈ reinspection | incident | no_recurrence`) would need severity/
magnitude, precise timestamp, and frequency/count to serve as a parametric
trigger — a dispute-resistant trigger cannot be built on three coarse values
alone. Flagged here for whoever designs that record next; not a redesign
mandate in this file.

**Decision point, not a build item:** before touching the outcome schema for
this purpose, resolve which role VELTH wants — signal-vendor or
occupational-MGA — and confirm the private-layer routing (this section's DACH
catch) rather than assuming the statutory layer is the door.

---

## 10. Other expansion surfaces — exploratory, lower confidence than §9

`[as of 2026-08]` **Confidence flag: this section is a lighter research pass
than §9 — one search per lane, not the multi-source depth §9 got. Treat as
"worth watching," not "worth planning against." Re-verify before any real
decision leans on it.**

**Catalog-as-a-product — real precedent, strong.** Thomson Reuters licenses
Westlaw's structured legal content as 100+ standalone APIs via a developer
portal, separate from any specific research tool — an established, large
business (legal-data licensing is Thomson Reuters' core model). VELTH's
9,185-entry hazard+legal-mapping catalog is the same kind of structured
reference layer. Real market, not speculative — the strongest of this
section's four findings.

**Adjacent regulated domain — one real structural match found.** German
environmental law (BImSchG §53) requires industrial facilities to appoint a
qualified *Immissionsschutzbeauftragter* (pollution-control officer) —
structurally the same pattern as a SiFa under ArbSchG: legally-mandated expert
sign-off, periodic structured documentation, submitted through an official
portal (BUBE-Online, per §27 BImSchG). Genuinely the closest same-shape
domain found (qualified-person-signs-off + hazard ID + mandated
documentation), distinct regulated subject matter (emissions, not workplace
hazards). Only one candidate researched — other domains may fit as well or
better; this is not an exhaustive scan.

**Benchmarking intelligence — checked and found weaker than assumed.**
TRIR/DART incident-rate benchmarking against BLS/NAICS codes is an already
crowded, mature US-OSHA-centric category (Benchmark Gensuite publishes an
annual EHS benchmarking report; several other established players exist).
Germany's BG-Gefahrklasse system doesn't natively produce TRIR/DART, so
VELTH's actual operating data doesn't even map cleanly onto the metric this
market trades on. **Do not pursue as scoped** — if a DACH-specific
leading-indicator benchmarking angle exists, it would need to be a genuinely
different metric, not an import of the US category.

**Compliance-engine-as-embedded-infrastructure — new, real pattern by
analogy, no same-domain precedent found.** Distinct from catalog licensing:
this licenses the *deterministic classification logic itself* (VELTH's rung-C
moat), not just reference content, to other platforms that need risk
classification but don't want to build a Nohl-gate-style engine from scratch.
Strongest evidence is from embedded finance, not safety: platforms embedding
a regulated function as infrastructure see materially higher net-revenue
retention than standalone tools (125%+ vs ~105%, per one 2026 market
analysis) — a real, quantified argument for the pattern, applied here by
analogy since no workplace-safety-specific precedent was found. Worth a
proper multi-source research pass if pursued further; this entry is a flag,
not a finding.

---

## 11. Equipment/machinery inspection (BetrSichV) — the priority
world-model-ready expansion

`[as of 2026-08]`

**Why this section exists, separate from §5/§9/§10.** World models (LeCun's
JEPA line, NVIDIA Cosmos, Google Genie/SIMA — all real, well-funded, shipping
in 2026, not speculative) are a genuinely new *perception* capability:
physical/spatial reasoning about a scene, not just describing it in text.
The academic hazard-detection literature independently confirms this is
exactly where today's vision-language models are weakest — multiple 2025
papers cite "poor spatial grounding" and "limited contextual reasoning" about
object relationships as the recurring failure mode. The architecture pattern
already validated elsewhere (a UAV landing-safety system that explicitly
separates a world-model perception layer from symbolic, auditable safety
rules on top) is the SAME shape as VELTH's existing engine — LLM/perception
proposes, the deterministic gate decides, per §6's anti-test. A better
perception layer slots underneath the existing gate; it does not replace it.

**This is the correct next domain to pair with that capability, ahead of
robotics (§5, currently deferred) and ahead of the exploratory lanes in
§10.** Screened against the same test used throughout this file (does a
qualified expert have to sign off, is there a mandated audit trail, does
understanding a physical space genuinely matter) plus one more specific to
world models (is the task *visual/spatial reasoning about physical state*,
not just document generation):

- **Legal foundation — the strongest of any candidate researched, verified
  at the primary-source level.** Betriebssicherheitsverordnung §14 (BetrSichV)
  is a hard statutory duty: every employer must have work equipment inspected
  "vor ihrer nächsten Verwendung" (before next use) and at recurring
  intervals by a **"zur Prüfung befähigte Person"** (a person competent to
  inspect, per TRBS 1203) or an approved inspection body (ZÜS). This sits on
  the same statutory footing as the SiFa/ArbSchG work VELTH already does —
  not a softer, best-practice-only standard.
- **Contrast with fire safety (Brandschutzbeauftragter), checked the same
  way and found weaker.** There is NO state-mandated qualification
  requirement for a fire safety officer in Germany in most cases — DGUV
  205-003 sets recommended training, not law. Real market, but a softer
  legal foundation than BetrSichV. Flagged here so the two are never
  conflated: BetrSichV is the priority; fire safety is a "build if a real
  customer asks" case, not a "build first" case.
- **The task is genuinely visual/spatial, not just documentary.** "Is this
  specific guard actually in place, is this specific ladder actually
  damaged, is this specific rack actually overloaded" is a physical-
  reasoning question about a scene's current state — closer to what a world
  model is built for than "write a risk-assessment paragraph" is.
- **Likely an EXTENSION of existing VELTH surface, not a new vertical.**
  VELTH's Prüfprotokoll/Gefahrstoffverzeichnis document types already touch
  this territory. Confirm the exact overlap (§0 — re-verify against the live
  catalog, don't assume from this note) before scoping as new work.

**What "build for world models when feasible" concretely means here,
staged, not a single leap:**
1. Now, low-risk: a world model as a synthetic training-data generator for
   rare equipment-defect scenes — this is the exact use case the
   governance layer already built (Batch 2 Component 4: provenance
   manifest, never-customer-facing gate, ratio cap) exists to make safe.
   That work is not waiting for a use case; this is the use case.
2. Later, trigger-gated: a world model as the perception layer for a real
   inspection photo — reasoning about a piece of equipment's physical state
   — feeding into the SAME deterministic gate architecture already in
   production. Do not let this become "replace the Nohl gate with a bigger
   model" — per §6's anti-test, that would erode the strongest current
   rung, not extend it.
3. Not yet: training a world model from scratch. NVIDIA Cosmos 3 trained on
   20 trillion tokens — genuinely not small-team-scale. Fine-tuning open
   weights (Cosmos ships under OpenMDW, an open license permitting
   adaptation) on VELTH's own narrow equipment-inspection data is the
   realistic ceiling.

**Decision point, not a build item:** confirm the Prüfprotokoll/GfV overlap
first (this may already be most of the way built), then decide whether
Component 4's synthetic-image pipeline gets its first real use case here.
