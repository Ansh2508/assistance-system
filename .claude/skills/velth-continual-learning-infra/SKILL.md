---
name: velth-continual-learning-infra
description: The strategic + technical architecture reference for VELTH's fine-tuning / continual-learning infrastructure build — the weight-level layer (LoRA, DPO, adapter registry) that sits above the already-built context_store (prompt-level) and hazard_feedback/export_pipeline (data-capture level). Load this BEFORE scoping, designing, or greenlighting any fine-tuning, LoRA, DPO, multi-tenant model-serving, adapter versioning, or "make the AI learn from corrections" work. Also load whenever the conversation touches training-data poisoning, per-company vs shared model architecture, eval harnesses for a fine-tuned model, canary rollout or rollback of a new model/adapter version, or EU AI Act / regulatory implications of continual learning. This skill encodes a dated research snapshot (August 2026) — its FIRST section is a standing mandate to re-verify before acting on anything time-sensitive in it, because this field moves in months, not years. Do not treat this as frozen truth.
---

# VELTH Continual Learning & Fine-Tuning Infrastructure

Research snapshot compiled: **2026-08-09**, by Claude (chat), with Anshu. Built from a genuine research pass (11 web searches across strategy, training method, data volume, eval harness, production safety, and poisoning defense) plus a `conversation_search` grounding pass against VELTH's actual V2 engine architecture. Not a Cowork-generated document — written in chat, cross-referenced against real code findings from the same session (Batch 1.5's converged correction-write architecture).

---

## 0. Research mandate — read this before acting on anything below

**This document is a snapshot, not a spec.** Everything in it — the specific numbers (poisoning thresholds, data-volume floors, cost anchors), the specific tools named (LoRAX, Punica, unsloth, axolotl, vLLM flags), and the specific papers cited — was current as of the search dates shown next to each claim. AI infrastructure and safety research moves faster than almost any other engineering domain right now. A number or a recommended tool that was correct in March 2026 may already be superseded by the time this skill is loaded.

**Before any of the following, re-search rather than trust this document's numbers verbatim:**
- Before finalizing the training method (base → SFT → DPO is the 2026 consensus stack here — verify this is still the consensus, not just cheaper-to-cite)
- Before finalizing the poisoning-defense threshold (the "~250 samples" and "50–100 samples" figures below are from specific studies — re-check for newer, more VELTH-relevant numbers, especially anything from Anthropic's own alignment team, since they are the most authoritative and closest source)
- Before picking a serving architecture (Multi-LoRA / vLLM specifics below are a live, fast-moving OSS space — versions and flags drift)
- Before assuming EU AI Act provisions are unchanged (this is genuinely unsettled regulatory ground — see §8)
- Before assuming a competitor's or frontier lab's stated capability is still their frontier — this space reshuffles in weeks

**How to re-verify:** `web_search` with the actual current date (not this document's date), read at least 2–3 independent sources per claim before treating a number as load-bearing for a real architecture decision, and prefer primary sources (Anthropic's own alignment blog, arXiv papers, not aggregator blogspam) for anything safety-critical.

**When you re-verify something and it's changed:** update this file in place, note what changed and the date, don't just silently build against the old number.

---

## 1. Where this fits — the three learning layers VELTH already has vs. still needs

Do **not** re-litigate the RAG-vs-fine-tuning question. It's already decided, and correctly:

> **V2 removed RAG entirely on purpose.** Deterministic catalog lookups + `legal.py` handle anything correctness-critical (hazard identification, Nohl RPZ math, legal citations). The LLM is reserved for extraction/interpretation, not authoritative content generation. Per the actual architectural decision record: *"V2 inverts this — deterministic output is already trustworthy (catalog-based, no RAG). L3 [hybrid RAG] now becomes an enhancement layer for recall on complex multi-hazard scenarios, not a correctness gate."*

Given that, VELTH already has **two of three** learning layers live. This skill is about building the third.

| Layer | What it is | Status | Scope | Latency to effect |
|---|---|---|---|---|
| **Tier 0 — `context_store`** | Explicit rules/logs, 3 scopes (user/company/project), tables `context_ablaufe`/`context_log`/`context_rules` | **Already live** (`core/engine_v2/context_store.py`, 511 lines) | Per-scope, prompt-injected | Immediate — next request |
| **Tier 1 — `hazard_feedback` capture** | Structural correction signal (hazard_id + action + risk delta, no free text), converged into one atomic transaction with the offline DPO export as of Batch 1.5 | **Live as of tonight's build** | Company-partitioned reads via `get_learned_corrections` | Immediate — next `/gbu/reanalyze` call, via prompt injection of past corrections |
| **Tier 2 — weight-level fine-tuning** | Actually updating model weights (LoRA/DPO) from accumulated corrections | **Does not exist yet — this skill is the plan for it** | See §2 for the two-sub-tier design | Batched — days to weeks, not per-session |

**Why three tiers, not one.** Dwarkesh Patel's Aug 2026 essay *"8 Predictions for the Era of Continual Learning"* frames this precisely with a saxophone-teaching metaphor: passing notes between sessions (Tier 0/context_store) has a real ceiling — some judgment is too tacit to write down as an explicit rule, and only shows up as a pattern across many examples. That's the actual justification for Tier 2: it exists to capture what Tier 0 structurally cannot.

**Do not confuse with Batch 2's inference-time reasoning work `[as of 2026-08]`.**
`velth_core/confirmation_pass.py` (calibrated cross-model confirmation) and
`velth_core/measure_impact.py` (counterfactual measure-impact advisory) — built
2026-08-11 — are a **different axis entirely**: reasoning-quality improvements
on the current, already-deployed model at inference time. Neither touches
weights, adapters, or training data. `confirmation_pass.py` reuses
`core/analytics/confidence_calibration.py` (SiFa ground truth) as its trigger,
not anything from this skill's Tier 2 pipeline. If a future session is scoping
"AI quality" work, check which axis it's actually on before assuming it belongs
in this skill's plan — conflating the two would misfile inference-time work as
weight-level work or vice versa.

---

## 2. Tier 2's own internal split — do not build this as one shared model

This is the single most important architectural decision in this document, and it resolves a real safety problem (§4) that a naive "pool everyone's corrections into one fine-tune" design would create.

### Tier 2a — per-company LoRA adapters
- Cheap, isolated, zero cross-tenant contamination **by construction** — adapters physically cannot mix across tenants in a correctly-built serving layer.
- This is the weight-level upgrade path for exactly what `context_store`'s company scope already handles at the prompt-injection level — same scope boundary, deeper effect.
- Captures company-specific idiosyncrasies: a company's actual site conditions, self-insurance structure, risk tolerance quirks — things that are true for THAT company and nobody else, where pooling would just be noise.
- **Serving architecture — established, production-proven pattern, not something to invent:** "Multi-LoRA serving" — one shared, immutable base model resident in memory, per-tenant adapters as lightweight, hot-swappable overlays, loaded per-request in milliseconds. Real open-source implementations: **Punica** (MLSys 2024, 12× throughput vs. naive multi-model serving), **S-LoRA**, **LoRAX**. Production stack anchor (2026): `vLLM --enable-lora --max-loras N --max-cpu-loras M`.
- **Isolation requirement, stated explicitly by the architecture pattern itself**: "the per-tenant secret (the fine-tuned adapter) is never mixed across requests." Per-tenant VRAM cost approaches zero at scale (100+ tenants on one GPU is a documented real configuration).
- **Graceful degradation**: if an adapter fails to load, fall back to the shared base model's generic behavior rather than failing the request outright. Build this in from day one, not as a later hardening pass.
- **Deployment/rollback economics**: a new customer's fine-tune is "a small artifact you register and route to, not a new GPU deployment." Rolling back a bad per-company fine-tune is deleting an adapter, not redeploying a model. This is a genuinely low-risk, low-blast-radius tier to build first.
- **Adapter registry — a required component, not an afterthought.** Never deploy adapters directly onto the base model instance; route through a dedicated registry that handles dynamic load/unload keyed by client ID (`company_id`). Per-adapter metadata to track from day one: lineage (base model version, training-data hash, commit SHA), performance (offline eval scores, human-review summary), risk profile (bias/safety checks, data-freshness expiration), and ownership (who to page if it misbehaves). Automate registry updates from CI/CD so every promotion is auditable. This is also the traceability artifact a regulator or auditor would ask for — discrete, versioned adapters are much easier to demonstrate compliance with than an opaque full-weight update.

### Tier 2b — shared core DPO fine-tune
- The layer that captures corrections that **generalize across companies** — e.g., a hazard false-positive pattern that shows up the same way at multiple unrelated companies is real signal about the base model's judgment, not noise from one site.
- This is the tier where the poisoning defense in §4 is **non-negotiable**, not optional hardening — see below for why.
- Trains on data sourced from `export_pipeline.py`, `content_tier='full'` rows, per the existing consent-gated design — no new consent mechanism needed, the gate already exists.

**Build order recommendation:** Tier 2a (per-company adapters) is lower-risk, lower-blast-radius, and delivers value per-customer immediately upon having enough of that company's own corrections. Tier 2b (shared core) is higher-value long-term (it's the actual cross-company moat) but requires the poisoning-defense design in §4 to be built and tested *before* it trains on real data, not after.

---

## 3. Go/no-go gate — check this before building anything

Do not build training infrastructure for a dataset that doesn't exist yet. Concrete floors from 2026 industry practice:

- **SFT** (supervised fine-tune, teaches format/base behavior): "a few thousand high-quality examples" typically needed for a measurable domain lift.
- **DPO** (preference pairs, teaches judgment/preference): **1,000–10,000 well-curated preference pairs is the typical floor** for it to be worth doing at all.
- **Quality beats quantity — the LIMA result still holds in 2026 sources**: "1,000 hand-curated examples often beat 100,000 noisy ones." This favors VELTH's actual situation (corrections are naturally scarce because each one requires a real SiFa doing real work) — don't chase volume, chase quality and genuine domain coverage.

**First concrete action, before any pipeline design work**: count actual `content_tier='full'` rows in `project_inline_edits` (via `export_pipeline.py`'s `_full_tier_select`) against these floors. If it's in the low hundreds, the honest move is to keep the consent-gated capture pipeline running and grow adoption (see §7's note on why earlier consent adoption compounds), not build training infra for a dataset that isn't there yet.

### 3.1 Before trusting that count — confirm the pipeline isn't silently
leaking, not just that it ran `[as of 2026-08]`

A row count from `_full_tier_select` only tells you what actually landed.
It says nothing about what should have landed and didn't. Real, dated
incidents in this project — not hypothetical risks — show the specific
shapes this takes; each has a mechanical check, not a promise to "be more
careful":

- **A capture path that's been fully built, migrated, and tested can still
  sit uncommitted for days while unrelated work continues** — Task 2.1's
  Build 3/4/5 arc (`/areas/continual-learning-readiness.md`) is the real
  case: verbandbuch outcome-linking and `ProxyOutcomeSignal` were both
  built, tested green, and confirmed — in a later session — to have
  **never landed on any branch**, because the commit step never ran.
  A row-count check run against the wrong branch, or before a genuinely
  finished build was merged, will silently under-report and look like a
  data-volume problem rather than the shipping gap it actually is.
  **Check:** before trusting a `content_tier='full'` count as representing
  "what VELTH has," confirm the branch being counted on actually has every
  capture-path commit that's supposed to be live — `git log` against what
  `/areas/continual-learning-readiness.md`'s standing-next-actions section
  says should already be merged, not assumed from a prior session's report.
- **A test proving a capture path works can pass locally while silently
  proving nothing on a clean environment** — the real `hypothesis`
  incident (2026-08-11): two new tests imported an undeclared dependency,
  passed on the machine that happened to have it installed, and would
  have failed collection everywhere else, including CI. Applied here: a
  "the export pipeline's tests are green" report is only meaningful if the
  environment those tests ran in had every dependency genuinely declared,
  not ambiently present. See velth-test-strategy's Pattern 7 for the
  mechanical grep-based check.
- **A stub correctly deferring a piece of the pipeline can point at a
  data-access pattern that's already stale by the time it's implemented**
  — the real `doc_verify.py` incident, same date: a placeholder pointed a
  future implementer at a pre-migration Supabase pattern for data that had
  already moved to the repository layer. Applied here: any stub or TODO
  touching how a future piece of this pipeline reads correction data
  (`hazard_feedback`, `project_inline_edits`, `verbandbuch_entries`) needs
  its referenced pattern re-verified as current before anyone acts on it,
  not trusted because it was correct when written. See velth-test-strategy's
  Pattern 8.

**The general rule this section exists to state plainly:** "the tests
passed" and "the count looks right" are both necessary and both
insufficient. Before treating a data-volume or readiness number as ground
truth for a real Tier 2 decision, confirm the thing that produced the
number is actually live, on the right branch, with every dependency it
needs — the same discipline §0 already demands for research claims,
applied here to the pipeline's own operational state.

---

## 4. Poisoning defense — this is the load-bearing safety requirement for Tier 2b

**Do not skip this. Do not treat it as optional hardening to add later.** The numbers here are why:

- Anthropic's own research: **~250 poisoned samples can poison a model regardless of total dataset size.** (Cited via Anthropic's alignment team's "Poisoning Fine-tuning Datasets of Constitutional Classifiers" work, 2026.)
- Independent studies: **as few as 50–100 poisoned samples can implant an effective backdoor** in a fine-tuned LLM.
- **DPO is documented as MORE vulnerable to poisoning than PPO** (Pathmanathan et al., cited in "Sequential Data Poisoning in LLM Post-Training," Sanderson/Wang/Lu/Kamath/Lu, arXiv:2606.04929, June 2026) — this matters directly because DPO is the exact method §5 (and 2026 industry consensus generally) recommends.
- The same paper's key finding: **"alignment training deactivates rather than eliminates SFT-embedded backdoors."** A poison introduced early in the pipeline is not reliably cleaned up by later stages — defense has to happen at ingestion, not just be assumed away by downstream steps.

**What this means concretely for VELTH's shared Tier 2b model**: if even one company's SiFa is bad at their job, has a compromised account, or is simply systematically wrong about something in a way that repeats — that alone could be enough samples (per the numbers above) to measurably bias the shared model for every other company. This is not a hypothetical edge case; it is the realistic, ordinary-case threat model for a multi-tenant SaaS pooling correction data.

**The defense — built from infrastructure VELTH already has, repurposed:**

`core/privacy.py` already has `meets_k_anonymity(cohort_size, *, k=K_ANONYMITY_MIN_COHORT)` (floor of 5) and `pseudonymize(value, *, scope)`, currently built for gating aggregate-statistic publication. **Repurpose the same primitive as a training-set poisoning gate**: a correction *pattern* (not an individual row) does not earn weight in the Tier 2b training set until it has been **independently corroborated by k≥5 distinct companies**. One correction from one company is a single data point that could be error, malice, or a genuine site-specific quirk (which is exactly what Tier 2a is for). The same correction pattern independently arising from five unrelated companies is real cross-domain signal.

This is a genuinely well-grounded design, not an invented one — it's the direct analog of what multi-party/Byzantine-robust aggregation research recommends for federated and crowdsourced-labeling poisoning defense, applied to VELTH's actual existing k-anonymity primitive instead of building new infrastructure.

**Do not rely on this alone** — per the "defense-in-depth, no single tool solves it" consensus across every 2026 poisoning-defense source reviewed: also keep `guardrail_no_llm_risk_class.py`'s existing rule (LLM-sourced risk_class can never enter training data — prevents self-reinforcing hallucination loops), and treat this as one layer of several, not the whole answer.

---

## 5. Training method — 2026 industry consensus (verify currency per §0 before committing)

**The stack**: base model → SFT → DPO. RLHF/PPO is now the minority choice, reserved for agentic/long-horizon reward-shaping problems — not VELTH's situation.

**Method**: LoRA/QLoRA is the default over full fine-tuning. Cost anchor from a live 2026 guide: an 8B model, 50k examples, QLoRA on a single A100, ~6 hours, **~$12–15**. This is not a six-figure ML-team undertaking — worth knowing before assuming this needs a dedicated ML hire before it can start.

**Catastrophic forgetting mitigations** (the fine-tune must not degrade general legal/document reasoning VELTH depends on elsewhere):
- Prefer LoRA over full fine-tune — base weights stay untouched, bounding the blast radius of a bad fine-tune by construction.
- Low learning rate, short training runs.
- **Replay**: keep a small percentage of general/base-distribution data in the training mix.
- **O-LoRA / OPLoRA** (orthogonal-projection LoRA, AAAI 2026) — constrains the fine-tune's gradient update to be orthogonal to previously-learned task directions, measurably reducing interference versus plain LoRA. Newer than the LoRA baseline; worth using if/when this is actually built.

---

## 6. Eval harness — build this BEFORE the training loop, not after

Confirmed in tonight's audit: **zero eval infrastructure exists today** for anything that would be trained on this data. Without it, there is no way to tell if a fine-tune helped or quietly made things worse — this is not optional scaffolding, it's the thing that makes the rest of this trustworthy.

**Concrete 2026 pattern:**
1. **Golden dataset**: start at 20–50 real production failures (not synthetic examples). Expand only as real failures surface. Version it alongside code, same discipline as any other test asset.
2. **Four-stage gate**: local dev (millisecond sanity checks — schema validity, forbidden content) → CI/PR (judge run against the golden set, must hit 85–90% agreement with a human-annotated baseline) → deployment gate (hard threshold block on any regression) → production monitoring (samples live traffic, feeds new failures back into the golden set).
3. **Judge discipline — VELTH already does this, just apply it here too.** "Pin the judge to a different model family than production, or scores inflate on subjective rubrics" is exactly the existing `velth-loop`/`velth-doc-verify` "maker ≠ checker" house principle, applied to a new context. No new discipline to invent — just extend the existing one to cover fine-tune eval.
4. **Cost-control pattern worth adopting**: tiered judges — a cheap classifier for easy axes (toxicity, schema validity, refusal-compliance), escalate only disagreements to an expensive frontier judge. Documented to cut eval cost 60–70% with minimal signal loss.

---

## 7. Production safety — for when a fine-tune actually ships

- **Shadow mode first**: run the candidate model/adapter on real requests without using its output for real decisions. Log and compare before it ever touches a user.
- **Canary, not big-bang**: route 5–10% of traffic to the fine-tuned candidate; the rest stays on the current pipeline.
- **Hard rollback thresholds, decided in advance, not improvised in the moment**: e.g., error-rate +1pp, P99 latency +20%, eval score −5%, any toxicity increase → automatic rollback. AI outputs exist on a quality spectrum, not a binary pass/fail — "a response can be grammatically correct, factually wrong, and still return HTTP 200," so infra-only monitoring (latency, error rate) is not sufficient by itself; the eval harness from §6 has to feed the canary gate directly.
- **Version pinning, explicitly**: "latest" is called out repeatedly across 2026 production-ML sources as "a future incident," not a deployment strategy. Every serving config should reference a pinned, specific model/adapter version.

**Note on why earlier is better, independent of the technical build**: Dwarkesh's essay argues the compounding effect of real-usage learning is roughly monotonic in accumulated data — the earlier broad consent adoption + correction capture starts flowing at real volume, the bigger the eventual lead, all else equal. This is a real argument for prioritizing consent-adoption UX/marketing alongside the pipeline build itself, not just the engineering.

---

## 8. Regulatory watch — genuinely unsettled ground, monitor rather than assume

Dwarkesh's essay raises a real, unresolved point: most current AI regulatory proposals assume a clean train-then-deploy split, and continual/adaptive learning erodes that distinction (if the model updates from millions of real sessions, "the moment after training, before deployment" stops being a meaningfully distinct checkpoint to regulate). This is **not yet resolved anywhere** — it's a live argument, not settled law.

**What VELTH already correctly does**: Art. 50 EU AI Act disclosure ("KI-generierter Entwurf gemäß Art. 50 EU AI Act") is already baked into every generated document. That obligation is about disclosure of AI-generated content to end users and is very unlikely to be affected by how the underlying model is trained or updated — keep it exactly as-is.

**What's genuinely unresolved and worth monitoring, not building against yet**: whether an adaptively-fine-tuned model used in a workplace-safety-document-generation context could trigger different EU AI Act obligations (e.g., post-market monitoring duties, Annex III high-risk classification questions) than a static model would. This is worth a real check with counsel once Tier 2 is actually close to shipping — not something to design around speculatively now, but also not something to ignore until it's a surprise.

**One concrete legal tension worth flagging now, before anyone reaches for it**: Dwarkesh notes some labs may eventually gate their best model on training-data access ("consent or lose the good version"). If VELTH ever considered something structurally similar (e.g., best-tier features gated on `content_training_consent`), this runs directly into **GDPR Art. 7(4)** — consent conditioned on service access generally is not "freely given." Any version of this would need very careful structuring (e.g., a genuinely separate paid tier that doesn't disadvantage non-consenters) to survive scrutiny, not a blanket "consent or no service" gate.

---

## 9. Sources (dated — check staleness before relying on any of these)

- Seldo.com, *"2026 is the year of fine-tuned small models"* — Oct 2025
- Toloka.ai, *"Foundation model training data: How frontier labs build pre-training datasets at scale"* — Jun 2026
- Jordan McAfoose, *"New and Noteworthy for July 2026"* — Jul 2026 (post-frontier-era / open-weight-squeeze framing)
- Jiaxin Zhang, *"How Frontier Labs Train Large Language Models"* — 2026 (standard pipeline; O-LoRA/OPLoRA/model-souping survey)
- FutureAGI, *"LLM Fine-Tuning Guide 2026"* and *"LLM Fine-Tuning Techniques 2026"* — May 2026 (SFT→DPO stack, cost anchors, forgetting mitigations)
- hjLabs.in, *"LLM Fine-Tuning Best Practices 2026"* — May 2026 (RAG-first caveat, QLoRA defaults, LIMA result)
- Xiong & Xie, *"OPLoRA: Orthogonal Projection LoRA Prevents Catastrophic Forgetting"*, AAAI 2026
- Inference.net, Medium (Milind Nair), Braintrust, FutureAGI, Galtea, QASkills.sh — LLM eval / golden-dataset guides, Feb–Jul 2026 (converging four-stage-gate pattern, judge-family-pinning, cost control)
- Medium (Duckweave), MLflow, GMI Cloud, 123ofAI — ML canary/rollback deployment guides, Feb–Jun 2026
- FutureAGI, *"Evaluating Fine-Tuned LLMs: A 2026 Playbook"* — May 2026 (canary + eval-gate integration)
- SQMagazine, Silvercloud, TTMS, Lakera — AI data poisoning threat landscape, Jan–May 2026 (the ~250/50–100 sample figures, Anthropic citation)
- Anthropic Alignment, *"Poisoning Fine-tuning Datasets of Constitutional Classifiers"* — 2026
- Sanderson, Wang, Lu, Kamath, Lu, *"Sequential Data Poisoning in LLM Post-Training"*, arXiv:2606.04929 — Jun 2026
- Towards AI (Neel Shah), *"The Architectural Paradigm of Multi-Adapter Inference: LoRAX"* — Mar 2026
- Chen et al., *Punica: Multi-Tenant LoRA Serving*, MLSys 2024
- Medium (Louis Philip), *"Multi-LoRA Serving: How to Run Hundreds of AI Tenants on a Single GPU"* — Apr 2026
- Spheron Network, *"Multi-Tenant LLM Serving on GPU Cloud"* — Jun 2026 (vLLM production flags)
- Introl, *"Model Versioning Infrastructure"* — Mar 2026; huuphan.com, *"5 Critical LoRA Assumption Mistakes"* — May 2026; lorakontext.world, *"Production Deployment Best Practices for LoRA Adapters"* — Jan 2025; AI Business Solutions, *"PEFT at Scale 2026"* — Jun 2026 (adapter registry, lineage metadata, never-deploy-direct-to-base rule)
- Dwarkesh Patel, *"8 Predictions for the Era of Continual Learning"* — Aug 7, 2026 (strategic framing throughout; saxophone metaphor §1; switching-cost moat argument; inference-economics calibration; regulatory framing §8)

**Internal (VELTH conversation history, grounded via `conversation_search`):** V2 engine architecture decision (no RAG, deterministic catalog + `legal.py`), `context_store` design (3 scopes, live tables), `velth-north-star` moat-ladder positioning, Batch 1.5's converged correction-write architecture (this same session).

---

## 10. Trigger test set — for verifying this skill actually fires when it should

Because this skill will load repeatedly across many future sessions, its description quality matters more than most. This section is the trigger-eval set, embedded here (not as a separate file) so a single SKILL.md is all that needs saving.

**If you're in an environment with the `claude` CLI (Cowork or Claude Code, not claude.ai chat)**: extract the JSON block below into a file (e.g. `trigger-eval.json`) and run the real automated loop —
```
python -m scripts.run_loop --eval-set trigger-eval.json --skill-path <path-to-this-skill> --model <current-model-id>
```
from `skill-creator`'s bundled scripts. That runs an actual 60/40 train/test split, 3 runs per query, and iterates the description automatically based on measured trigger rates — far more reliable than the manual read below.

**If you don't have that tooling available**: read each query against the current frontmatter `description` above and reason about whether it would plausibly fire. Less rigorous, but still catches real gaps — doing exactly this is what found the original description was missing "LoRA," "adapter registry," and "canary/rollback" entirely before this section even existed.

```json
[
  {"query": "Let's design the fine-tuning pipeline for VELTH's correction data", "should_trigger": true},
  {"query": "Should we use DPO or SFT on the corrections we've been collecting?", "should_trigger": true},
  {"query": "How do we stop one bad company's corrections from poisoning the shared model?", "should_trigger": true},
  {"query": "Let's build the adapter registry for per-company LoRA fine-tunes", "should_trigger": true},
  {"query": "Should this correction go into the per-company adapter or the shared core model?", "should_trigger": true},
  {"query": "Set up the golden dataset and eval harness for the fine-tune we're about to build", "should_trigger": true},
  {"query": "What's our rollback plan if the new adapter regresses in production?", "should_trigger": true},
  {"query": "Let's get moving on the continual learning infra", "should_trigger": true},
  {"query": "Do we actually have enough consented corrections yet to start fine-tuning, or should we wait?", "should_trigger": true},
  {"query": "Does fine-tuning on customer corrections change our EU AI Act obligations?", "should_trigger": true},
  {"query": "How do we serve a different LoRA adapter per company without a dedicated GPU per customer?", "should_trigger": true},
  {"query": "Build out tier 2b of the continual learning architecture", "should_trigger": true},
  {"query": "What's the difference between LoRA and QLoRA and which should VELTH use?", "should_trigger": true},
  {"query": "How many corroborating companies do we need before a correction pattern can train the shared model?", "should_trigger": true},
  {"query": "Design the canary rollout for the first fine-tuned adapter we ship", "should_trigger": true},
  {"query": "I want to write the DPIA section covering how we train on customer corrections", "should_trigger": true},
  {"query": "Add a new rule to context_store excluding hazard X for this company", "should_trigger": false},
  {"query": "Fix the failing test for the hazard_feedback converged write transaction", "should_trigger": false},
  {"query": "Should we bring RAG back into VELTH's V2 engine?", "should_trigger": false},
  {"query": "What's Claude's context window size?", "should_trigger": false},
  {"query": "Fix the AGB clause about photo training disclosure", "should_trigger": false},
  {"query": "Style the export button in ProjectWorkspacePanel.tsx", "should_trigger": false},
  {"query": "Why isn't the SiFa's hazard correction actually saving right now?", "should_trigger": false},
  {"query": "Run the full backend test suite and tell me what's failing", "should_trigger": false}
]
```

**Manual dry-run findings (done in chat, no CLI available) — carry these forward rather than re-discovering them:**
- 20 of 24 cases are high-confidence matches against the current description as written.
- **4 genuinely moderate-confidence cases, flagged rather than papered over:**
  - *"Build out tier 2b..."* — relies on the skill's own internal jargon ("tier 2b"). Only reliable once this skill has already loaded earlier in the same conversation; a cold first-message use of "tier 2b" may not trigger reliably. Not obviously fixable by rewording the description — would need the term itself to become common enough usage to add explicitly, or accept this as a within-session-only shorthand.
  - *"Design the canary rollout..."* — fixed once already (canary/rollback added), re-verify this is now solid.
  - *"I want to write the DPIA section..."* — a real judgment call about scope (DPIA drafting is arguably a different skill's job that would need to *reference* this one, not be triggered *by* this one). Worth resolving explicitly once you see how it actually plays out in practice, not guessed at now.
  - *The bare LoRA/QLoRA question* (#13) — included as should_trigger:true on the reasoning that any VELTH-scoped ML-architecture question benefits from this skill's content, but this is a slightly generous read of "infra-building" intent versus pure curiosity — worth watching whether it over-triggers in practice.
- **The 8 negative cases are the ones that matter most to get right** — they specifically test the boundary between this skill (Tier 2, weight-level) and adjacent-but-different territory (Tier 0 `context_store`, Tier 1 `hazard_feedback` capture, unrelated VELTH work). If any of these start false-triggering, that's a sign the description has drifted too broad and needs tightening, not expanding.

**When you do get real numbers from the automated loop, update this section with the actual measured trigger rates** rather than leaving this manual estimate as the permanent record.
