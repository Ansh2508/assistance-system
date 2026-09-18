---
name: silicon-valley-frontier
description: Exploit Silicon Valley and US AI, open-source, research, compute, standards, startup, and commercialization ecosystems through evidence-led discovery, code forensics, local reproduction, and global benchmarking.
metadata:
  short-description: US frontier ecosystem research to tested decisions
---

# Silicon Valley Frontier

Use this skill when a technical or product decision could benefit from the US
AI-industrial ecosystem: frontier providers, Bay Area and US research labs,
open-source infrastructure, cloud/compute, evaluation, startup ecosystems,
federal research, procurement, and commercialization.

Silicon Valley is not shorthand for the entire United States. Separate the
private-lab/startup network from university/open-source systems, federal
research infrastructure, standards, procurement, and other US technology hubs.
Treat each as a capability source with its own evidence and constraints.

This skill is a complement to `china-frontier`, not a US-vs-China popularity
contest. Search US capabilities deeply, then compare them with Chinese and
other global candidates on the same task. Adopt the measured winner, or retain
the evidence for a later decision.

## Boundaries

1. A provider announcement, funding round, model leaderboard, GitHub stars, or
   benchmark chart is discovery evidence, not proof for the active product.
2. Do not treat a closed-model API as reproducible simply because its company is
   prominent. Version, price, rate limits, data use, regional availability, and
   output behavior can change; capture a dated live test before adoption.
3. Do not execute third-party setup scripts, model code, `trust_remote_code`,
   or downloaded weights in the target product to inspect them. Isolate first.
4. Separate code, model, dataset, hosted-service, and commercial terms. A
   permissive repository license does not grant rights to weights, data, or API
   outputs.
5. Never infer product-market fit from VC activity. Validate a buyer workflow,
   willingness to pay, switching cost, regulatory path, and outcome signal.
6. Do not force a US-origin tool into the stack. A strong China, Europe, Japan,
   India, Korea, or local alternative wins when it performs better under the
   same measurable contract.

## US frontier advantage loop

1. **Define the decision contract.** State the user/job, correctness and safety
   requirement, modalities/languages, latency, cost ceiling, deployment/data
   boundary, explainability, available hardware, and commercial objective.
2. **Map the US capability graph.** Search five independent lanes: private labs
   and startups; university/open-source systems; cloud/chip/inference; federal
   research/procurement; and standards, security, and governance. Record why a
   lane can affect this decision.
3. **Forensically shortlist candidates.** For each model, library, API, dataset,
   benchmark, startup pattern, or program, capture primary URL, date, owner,
   commit/version, license/terms, maintenance, tests, hardware/data assumptions,
   known failure modes, and integration boundary.
4. **Reproduce the narrow mechanism.** Run an isolated task-specific probe. For
   software, use pinned versions and native tests plus a project-shaped case.
   For an API, use a dated live call. For a business mechanism, inspect actual
   buyer, funding, award, contract, or public outcome records.
5. **Benchmark globally.** Compare the US candidate with the incumbent and best
   practical candidates surfaced by `china-frontier` and other relevant lanes.
   Freeze the split and metrics first: quality, calibration, robustness, latency,
   throughput, total cost, security, rights, explainability, and operator load.
6. **Translate only a surviving result.** Use `research-simulate-encode` for the
   experiment and `research-to-code` for the smallest enforceable change. Record
   adopted, rejected, and unresolved candidates in the evidence packet.
7. **Compound, do not merely browse.** Preserve evaluated commits, query terms,
   integration adapters, cost measurements, failure cases, buyer evidence, and
   rejected transfers. Future work starts from this tested asset graph.

## Capability lanes

| Lane | Search for | Required proof before adoption |
| --- | --- | --- |
| Frontier providers and startups | Model/API capability, agents, multimodal systems, developer tools, vertical workflows | Dated live task evaluation, contract/terms review, fallback path, and cost/latency trace |
| Universities and open source | Algorithms, systems, datasets, benchmarks, reproducible repositories | Commit-pinned reproduction, license/data audit, tests, and same-task comparison |
| Compute and inference | Serving engines, schedulers, compilers, chips, cloud capacity, edge deployment | Workload-shaped throughput/latency/cost measurement; generic benchmarks alone fail |
| Evaluation and measurement | Benchmark harnesses, model/dataset cards, observability, red-teaming, calibration | Target-task holdout, leakage controls, failure taxonomy, and reproducible report |
| Federal research and procurement | NAIRR, NSF/DARPA/DOE/NIH programs, SBIR/STTR, standards, public challenges | Official eligibility/rights/timing check and a real path to the target user or buyer |
| Commercialization and capital | Customer design partners, technology transfer, SBIR/STTR, procurement, market structure | Evidence of a painful workflow, owner, budget, measurable outcome, and sales motion |

## US-specific research lenses

- **Open-source systems:** inspect implementation depth, not marketing. US-origin
  candidates such as vLLM, SGLang, DSPy, Ray, and lm-evaluation-harness are
  hypotheses for serving, programming, orchestration, and evaluation—not default
  dependencies. Read their source, release notes, license, issue surface, and
  test/evaluation architecture.
- **Private providers:** use official API/version documentation and a live,
  logged probe. Capture model identifier, date, region, request parameters,
  safety behavior, tool/structured-output behavior, usage policy, data handling,
  latency, cost, and outage fallback.
- **Research infrastructure:** inspect NSF/NAIRR, university labs, public
  datasets, and challenge programs for access to compute, data, evaluation, and
  collaborators. Confirm eligibility and availability; never promise access from
  an announcement alone.
- **Measurement:** combine target-task evaluation with systems measurements.
  MLPerf measures standardized inference systems, while project decisions need
  workload-specific p50/p95 latency, throughput, quality, tail failures, cost,
  and operational burden.
- **Trust and security:** use NIST AI RMF and applicable NIST/CISA resources as
  a risk-management input. Convert relevant risks into project tests, logging,
  access controls, and fail-closed behavior—not a compliance claim.
- **Commercialization:** distinguish venture attention from customer evidence.
  Evaluate whether SBIR/STTR, university technology transfer, enterprise design
  partners, channel partners, or procurement are actual routes for this product.

## Cross-ecosystem comparison

For each surviving candidate, create one row with:

`job | candidate | origin/ecosystem | exact version/commit | terms | data boundary |
quality | calibration | safety failures | p50/p95 latency | throughput | total cost |
hardware | explainability | operator load | evidence tier | decision | limitation`

Hold inputs, evaluation dates, task split, and operating budget constant across
candidates. Use at least one negative control (random/shuffled or degraded
candidate as appropriate) and test the input most likely to break the claimed
advantage. If conditions cannot be made comparable, report the comparison as
inconclusive rather than rank by reputation.

## Commercialization reality gate

Before using US ecosystem evidence to justify a product or market decision,
answer all of these with current primary evidence:

1. Who has the painful job and authority to buy?
2. What measurable outcome improves, and over what time horizon?
3. Why cannot an incumbent, model provider, or internal team cheaply copy it?
4. Which data, workflow integration, rights, trust, or distribution advantage
   compounds with use?
5. What must be proven in a paid pilot before scaling?
6. Which route is real—direct sale, channel, procurement, licensing, SBIR/STTR,
   technology transfer, or partnership—and what are its eligibility constraints?

If these cannot be answered, label the output an ecosystem hypothesis, not a
business case.

## Required artifacts

Create a packet using `scripts/init_us_frontier_packet.py` before a broad pass.
It must include a decision contract, capability graph, source ledger, repository
audits, provider test log, global comparison table, experiment plan/results,
commercialization test, rejected candidates, and explicit unknowns.

Read `references/us-frontier-systems-2026-09.md` for verified starter evidence
and `references/us-discovery-playbook.md` for task-specific query templates.
They are starting points, not rankings or an approval list.

## Companion-skill handoff

- `china-frontier` supplies China-first candidates and independent global
  baselines; this skill returns the same-task US comparison rather than a claim
  of US superiority.
- `deep-cross-domain-research` audits whether every requested ecosystem and
  domain changed a decision or is explicitly a gap.
- `frontier-ml-research` turns candidate models into a leakage-safe model ladder;
  do not confuse systems throughput with model quality.
- `research-simulate-encode` validates a mechanism locally, including adversarial
  and outage cases; `research-to-code` attaches the surviving result to the
  smallest real interface, schema, or deployment decision.
- `velth-north-star` tests whether a capability compounds into a durable product
  advantage; `velth-continual-learning-infra` governs data rights, feedback,
  tenant isolation, evaluation, and controlled promotion.
- `ai-output-self-audit` and `velth-truth-gate` audit every claim, including the
  difference between a fetched source, a local reproduction, a live provider
  call, and a commercial outcome.


## Installed-environment notes (added 2026-09-18)

- **`frontier-ml-research` is referenced above but is not installed** in this
  Claude Code environment. Until it exists, do its job inline: build the
  leakage-safe model ladder yourself, holding split, dates, and budget constant,
  and run the experiment through `research-simulate-encode`. Do not report a
  ladder as done because a skill name appeared in a handoff table.
- Verification status of this skill's sources: `references/verification-2026-09-18.md`.
- Adopting anything for veOS or VELTH (including a US-hosted provider) is gated
  by `../china-frontier/references/veos-velth-constraints.md`: no partner models
  through Vertex Model Garden, live-traffic routing changes need fresh
  confirmation, and real customer data needs a data-boundary decision first.
