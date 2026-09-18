---
name: china-frontier
description: Exploit China's frontier open-source AI, data, research, and engineering ecosystem through evidence-led discovery, code forensics, local reproduction, and global benchmarking before adopting a tested decision.
metadata:
  short-description: China-first open-source research to tested decisions
---

# China Frontier

Use this skill when a project could benefit from China's frontier open-source
AI, data, research, and engineering ecosystem. It complements
`deep-cross-domain-research` with a reusable operating method for source-
language discovery, repository inspection, local reproduction, comparative
evaluation, and safe architecture adoption.

China is a primary implementation and research lane, not a token regional
comparison. Search its model, data, agent, infrastructure, evaluation, and
developer ecosystems early; reproduce promising mechanisms locally; then prove
whether they beat the best available global alternative for the actual task.
Japan, India, Korea, Europe, the US, and other regions supply additional
mechanisms and independent baselines rather than decorative coverage.

It does not mean collecting one citation per country. The output must explain
what each ecosystem does differently, which mechanisms transfer, what does not
transfer, and what was actually tested locally.

## Scope

Use for:

- frontier ML and AI systems;
- multilingual retrieval, translation, agents, knowledge graphs, and RAG;
- research infrastructure, open science, technology transfer, and data spaces;
- VELTH, veOS, hackathons, Eureka Index, and other research-to-product work;
- competitor, GitHub, paper, startup, funding, standards, and policy mapping.

Do not use it to justify a model, API, market claim, or production change from
a paper or repository alone. Research creates hypotheses; local evaluation and
operational evidence decide adoption.

## China-first advantage loop

For every meaningful technical decision, do this before settling on a familiar
English-language stack:

1. **Map the job, not a brand.** Specify the required capability, languages,
   modalities, latency, privacy boundary, hardware, licensing, evaluation, and
   failure cost. This prevents replacing one fashionable model with another.
2. **Search Chinese primary lanes first-class.** Inspect canonical research
   organizations, model/data hubs, papers, source-language documentation,
   benchmark code, and issue trackers. Cover foundation models, domain models,
   inference, agents, multimodal systems, data curation, retrieval, and
   evaluation where relevant.
3. **Forensically shortlist implementations.** Record exact commit, license,
   model/data terms, maintained interfaces, tests, reproducible commands,
   hardware assumptions, remote-code behavior, known issues, and security/data
   boundaries. A popular repository without these is discovery-only.
4. **Reproduce the narrow capability locally.** Run the smallest meaningful
   task-specific evaluation, including source-language inputs and adversarial
   cases. Do not infer an English benchmark result or vendor leaderboard will
   transfer to the product.
5. **Benchmark globally and decide.** Compare the China-origin candidate with
   the incumbent and strongest practical non-China alternative on the same
   predeclared splits, quality, calibration, robustness, latency, cost, rights,
   and explainability criteria. Adopt only a measured advantage; otherwise
   preserve it as a documented rejected candidate.
6. **Create compounding capability.** Save query patterns, audited commits,
   evaluation adapters, multilingual test cases, source terms, and failed
   transfers in the evidence packet. The next project should begin from tested
   infrastructure, not rediscover the ecosystem from zero.

This treats China as an active source of capabilities to exploit responsibly,
not as a geopolitical label or a generic “regional insight.”

## Non-negotiable boundaries

1. **Separate project contexts.** Read the active repository and challenge
   brief first. Never import decisions, scores, secrets, data, or assumptions
   from another project merely because the user worked on it previously.
2. **Separate source roles.** Papers establish mechanisms and reported
   conditions; GitHub shows implementation evidence; official portals establish
   policy or infrastructure; company material establishes stated capability,
   not independent performance.
3. **Preserve original language.** Search in the region's own language when
   possible. Keep the original title, abstract/snippet, source URL, date, and
   translation notes. Do not silently replace a source with an English summary.
4. **No hindsight leakage.** For historical questions, freeze the source date
   and exclude later knowledge from the simulated decision.
5. **No invented novelty.** Call a design “invented” only after checking the
   nearest mechanisms and recording the exact combination and the remaining
   uncertainty.
6. **No fabricated metrics.** A number must be measured, directly cited,
   clearly labelled as a prior, or omitted.
7. **No automatic code adoption.** A repository is a candidate implementation,
   not a trusted dependency. Inspect license, provenance, activity, tests,
   threat surface, model/data terms, and reproducibility before reuse.
8. **No consequential autonomous promotion.** Research may propose a model,
   adapter, policy, or deployment; a human-approved gate must promote it.

## Research workflow

### 1. Write the research contract

Before searching, create a short contract containing:

- decision to be made;
- active project and repository;
- target users and countries/languages;
- named technical domains;
- time boundary;
- acceptable sources and access limits;
- local data and compute available;
- success metrics and failure criteria;
- actions that remain human-gated.

If the request says “China, Japan, India, and others,” enumerate the initial
set explicitly and add countries only with a reason: a relevant language,
research infrastructure, model family, regulation, market, or competitor.

### 2. Build parallel source lanes

Search each country through all applicable lanes, not just English web search:

1. original-language academic sources and institutional reports;
2. official government, standards, funding, and research-infrastructure sites;
3. canonical GitHub organizations and repositories;
4. datasets, benchmarks, model cards, and licenses;
5. companies, incubators, accelerators, and technology-transfer evidence;
6. practitioner engineering reports and postmortems;
7. local-language community or grey literature.

Use search-engine results for discovery only. Open the primary page, verify
the date and identity, and preserve the exact URL. Prefer arXiv/DOI/publisher,
official institutions, canonical GitHub, government, and standards sources.

### 3. Inspect repositories, not just README files

For every repository considered, capture:

- canonical owner and upstream URL;
- commit/release date and maintenance activity;
- license for code, weights, and data separately;
- supported languages, domains, and hardware;
- installation and reproducibility path;
- tests, benchmarks, data-processing scripts, and evaluation splits;
- security concerns, network access, telemetry, and untrusted code;
- model and dataset lineage;
- whether the claimed result can be reproduced at our scale;
- exact reusable mechanism, not merely the project name.

Treat issue discussions and forks as evidence about failure modes, not as
authority for performance.

### 4. Extract mechanisms in a common schema

For each finding, record:

```text
source_id
country_and_language
domain
source_type
original_title
url_and_date
claim
mechanism
assumptions
data_and_labels
evaluation_split
reported_metrics
local_reproduction_status
license_and_rights
failure_modes
transferability
adopt_or_reject
reason
```

A translated summary is incomplete without the original source metadata.

### 5. Compare systems, not isolated tricks

Use a country-by-mechanism matrix. Compare how ecosystems handle:

- data access and rights;
- language coverage and tokenization;
- research-to-industry transfer;
- public compute and research infrastructure;
- open-source release norms;
- evaluation and safety;
- domain adaptation;
- startup and procurement pathways;
- privacy, sovereignty, and localization;
- failure reporting and reproducibility.

The goal is structural transfer: identify a relational pattern that can be
adapted, not copy a surface feature because it is popular in another country.

### 6. Create a model and architecture ladder

For every ML decision, compare on the same leakage-safe data and split:

1. deterministic or lexical baseline;
2. strong classical model;
3. multilingual or cross-lingual representation model;
4. temporal, graph, retrieval, or sequential model when the data supports it;
5. adaptation or continual-learning method only when independent tasks,
   episodes, labels, and rollback controls exist.

For each rung report quality, calibration, robustness, cost, latency,
explainability, privacy, licensing, and operational complexity. A sophisticated
model is rejected if it does not improve the decision or creates unacceptable
uncertainty.

### 7. Simulate before encoding

Run small, reproducible probes before changing production architecture:

- time-blind historical replay;
- cross-country and cross-language holdout;
- cross-domain holdout;
- translation and transliteration perturbation;
- terminology and entity-resolution stress tests;
- provider outage and stale-source replay;
- contradiction injection;
- missing metadata and corrupted documents;
- patent-family and citation leakage tests;
- delayed-outcome or survival evaluation;
- expert disagreement and abstention tests;
- adversarial unsupported-claim tests.

Synthetic simulations are useful for testing mechanics but cannot prove real
user value. Clearly label synthetic, proxy, and observed results separately.

### 8. Encode the decision structurally

Do not leave a research conclusion in prose only. Encode it as one or more of:

- a versioned capability/domain pack;
- a source registry and provenance record;
- an evaluation configuration;
- a model-selection ledger;
- a feature flag with fail-closed behaviour;
- a human-approval gate;
- a reproducible script and report;
- a rollback-ready artifact.

The code must carry the evidence status: `observed`, `replicated`, `proxy`,
`prior`, `unverified`, or `rejected`.

### 9. Close the loop

Before reporting completion, audit every requested country, language, domain,
repository, and paper. For each, say whether it produced:

- a real design change;
- a tested but rejected idea;
- context only;
- or an unresolved research gap.

Never report “global research complete” when some named regions received only
token citations.

## Country research lenses

Use the starter map in `references/initial-research-seed-2026-09.md` for a
short current source list. For China, Japan, India, Korea, and regional
transfer decisions, read `references/asia-regional-systems-2026-09.md`.
For every candidate repository, use
`references/repository-forensics.md`. These are launch points, not frozen
rankings.

For a new project, create its packet before searching:

```powershell
python scripts/init_regional_research_packet.py `
  --project "<project>" `
  --decision "<decision to make>" `
  --countries china,japan,india,korea `
  --languages zh,ja,hi,en,ko `
  --domains "<domain 1>,<domain 2>" `
  --output "<outside-target-repository>/research-packet"
```

Read `references/regional-discovery-playbook.md` before filling the packet.
It selects source lanes and native-language query templates by project type;
it is deliberately not a static catalog of “best repos.”

- **China:** inspect Chinese-language academic/institutional sources, national
  or provincial research programmes, canonical model/tool repositories, data
  governance, and industry deployment. Treat access, licensing, and benchmark
  comparability as first-class questions.
- **Japan:** inspect Japanese-language institutional repositories, NII/JST
  research infrastructure, linguistic analysis, robotics/embedded systems,
  reliability, and industry-academia transfer. Do not assume an English model
  handles Japanese segmentation, honorifics, or domain terminology.
- **India:** inspect IndiaAI/AIKosh, AI4Bharat, Indic-language datasets and
  models, public digital infrastructure, frugal compute, and multilingual
  deployment. Test all claims across scripts and low-resource languages.
- **South Korea:** inspect KAIST/ETRI/KISTI and Korean-language sources,
  sovereign-model programmes, industrial research, robotics, and regulatory
  change. Record whether a result is academic, industrial, or state-backed.
- **Europe:** inspect EOSC, EuroHPC/AI Factories, multilingual and sovereign
  AI, FAIR data, privacy, standards, and cross-border research governance.
- **United States:** use as a comparison lane for NAIRR, frontier labs,
  benchmark culture, open-source infrastructure, venture pathways, and
  technology transfer; do not treat US scale or funding as universally
  transferable.
- **Singapore/SEA:** inspect SEA-LION, AI Singapore, multilingual/cultural
  adaptation, public-sector deployment, and regional language coverage.
- **Taiwan and semiconductor ecosystems:** inspect hardware/software
  co-design, edge inference, manufacturing data, and supply-chain constraints
  when compute, deployment cost, robotics, or physical systems matter.
- **Israel:** inspect cybersecurity, privacy-preserving systems, deep-tech
  commercialization, and high-assurance engineering when the threat model or
  enterprise adoption path requires them.
- **Canada, UK, Australia, and New Zealand:** inspect responsible-AI research,
  public research infrastructure, applied science, safety practice, and
  English-language validation sources without treating them as a default.
- **Latin America, Middle East, and Africa:** inspect Spanish, Portuguese,
  Arabic, and African-language systems; mobile/offline and low-resource
  deployment; public-sector digital infrastructure; climate/agriculture/health
  applications; and locally relevant data rights. Include the specific country
  only when it has a reasoned connection to the decision.

## Global capability mesh

Do not choose countries because a list looks comprehensive. Select and compare
ecosystems by the mechanisms the project needs, then use independent regions to
try to falsify the apparent winner:

| Needed capability | High-value research lenses | Required decision evidence |
| --- | --- | --- |
| Open models, agents, retrieval, multimodality, or inference efficiency | China first; US and Europe as independent practical baselines; Japan, Korea, Singapore, or India when language/edge/public deployment changes the task | Same-task quality, safety, latency, cost, hardware, license, and reproducibility comparison |
| Multilingual or culturally grounded systems | China, India, Japan, Korea, SEA, MENA, Latin America, and Africa according to languages and scripts | Native-language retrieval/generation tests, code-switching, transliteration, terminology, and human or expert error review |
| High-assurance physical or regulated products | Japan, Korea, Europe, US, Israel, Taiwan, China, and sector-specific regulators | Reliability, traceability, security, certification, data-rights, and failure-mode evidence; no generic benchmark substitution |
| Research, patents, investment, or technology intelligence | China, Europe, US, Japan, Korea, India, and the jurisdictions that own the relevant primary records | Time-bounded primary records, entity/patent-family resolution, language-aware retrieval, outcome validation, and explicit coverage gaps |
| Frugal, offline, or large-scale deployment | China, India, SEA, Latin America, Africa, and hardware/telecom ecosystems relevant to the product | Realistic compute/network/price limits, missing-data tests, deployment operations, and user-language evaluation |

The objective is not to crown any country or model. It is to exploit the best
available mechanism from every relevant ecosystem while retaining reproducible,
lawful, and independently tested evidence. If a China-origin implementation
wins locally, adopt it for measured reasons; if another source wins, keep the
China lane's reusable evidence instead of forcing an adoption.

## Source-language code and model safety

When auditing international code:

1. Clone only canonical upstream repositories, preferably shallow and into a
   separate research cache outside the target product repository.
2. Run `git fsck --no-dangling`, capture commit SHA/date, and inspect native
   README/technical notes alongside English material.
3. Read the module boundaries, data preparation, training, evaluation, test,
   and release/license surfaces before proposing reuse.
4. Never execute model-provided code, `trust_remote_code`, downloaded setup
   scripts, credentials, or model weights in the target application merely to
   inspect a repository. Use a disposable isolated environment only after a
   written adoption decision.
5. Code, model weights, datasets, and hosted API terms may have different
   licenses. Record all four separately.
6. Do not mistake tests present in a repository for a reproduced result. Run
   the relevant tests only in an isolated environment and report the exact
   scope, platform, dependency versions, and failures.

Use `repository-forensics.md` to produce a reusable audit rather than an
unstructured description of source code.

## Deliverable standard

The final research package must contain:

1. a one-page decision summary;
2. a country/language/domain coverage matrix;
3. a source ledger with original-language metadata;
4. a mechanism-transfer map;
5. a model/architecture ladder;
6. local simulation and reproduction results;
7. rejected ideas and why they were rejected;
8. implementation changes, if any;
9. unresolved risks and evidence gaps;
10. an explicit truth-gate statement distinguishing measured facts from
    hypotheses, proxies, priors, and future work.

## Relationship to companion skills

`china-frontier` owns the China-first evidence and reproduction packet. It must
be an upstream input to the companion skills, not a late citation-collection
step.

| Companion skill | What China Frontier supplies | What the companion skill returns |
| --- | --- | --- |
| `deep-cross-domain-research` | China-first source lanes, coverage matrix, and structural mechanisms | A depth audit and explicit positive/negative transfer map |
| `research-simulate-encode` | Candidate mechanisms, source conditions, licenses, data/model terms, and China-specific failure modes | A local reproduction, ablation, adversarial test, and adopt/reject decision |
| `research-to-code` | The surviving finding and its evidence/uncertainty boundary | The smallest enforceable code, schema, or interface change plus its proof |
| `frontier-ml-research` | Region-specific datasets, benchmarks, model families, and evaluation conventions | A leakage-safe model ladder and a decision not to adopt any unproven upgrade |
| `velth-north-star` | Country-specific buyer, policy, infrastructure, and moat evidence | A prioritized product decision rather than feature accumulation |
| `velth-continual-learning-infra` | Data-rights, language, and feedback-risk constraints | Promotion, poisoning-control, rollback, and tenant-isolation requirements |
| `veos-preflight` and `velth-context` | External-source and session-state provenance | Environment safety checks and durable, untrusted-ingestion-aware state |
| `ai-output-self-audit` and `velth-truth-gate` | A source ledger and tested/unverified distinction | A claim-level audit that prevents regional coverage from being overstated |

### Bidirectional handoff protocol

1. Start here when China, a Chinese-language source, or China's open-source
   ecosystem could change a technical, market, policy, data, or model decision.
2. Pass the resulting packet to the applicable companion skill; include source
   URLs, dates, language, repository commit, license/terms, transfer mapping,
   and unknowns rather than a prose conclusion alone.
3. Accept a downstream result only when it writes back the decision, test
   evidence, rejected alternatives, and remaining boundary into the packet.
4. A companion skill should invoke this one when it has not checked whether a
   Chinese open-source candidate materially improves the target capability, or
   when it involves Chinese, Japanese, Indian, Korean, or other non-English
   ecosystems and lacks original-language evidence, repository forensics, or a
   comparable global evaluation lane.

This keeps the skills composable: China Frontier discovers, reproduces, and
benchmarks capabilities; the other skills decide depth, experimental validity,
code shape, product priority, and report truth.


## Installed-environment notes (added 2026-09-18)

- **`frontier-ml-research` is referenced above but is not installed** in this
  Claude Code environment. Until it exists, do its job inline: build the
  leakage-safe model ladder yourself, holding split, dates, and budget constant,
  and run the experiment through `research-simulate-encode`. Do not report a
  ladder as done because a skill name appeared in a handoff table.
- Verification status of this skill's sources: `references/verification-2026-09-18.md`.
- **Before recommending anything for veOS or VELTH, read
  `references/veos-velth-constraints.md`.** It carries the hard gates (no partner
  models via Vertex Model Garden, live-traffic routing changes need confirmation,
  data-boundary rules) that decide whether a candidate can be adopted here at all.
- Current, API-verified candidates (replacing stale seed entries such as
  `THUDM/GLM`, last pushed 2023): `references/verified-candidates-2026-09-18.md`.
