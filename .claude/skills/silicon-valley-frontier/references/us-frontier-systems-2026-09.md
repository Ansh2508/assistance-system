# US Frontier Systems: Verified Starter Evidence

This is a dated source map for discovery, not a list of endorsed tools. Recheck
versions, access, pricing, terms, and results before use.

## Research and public infrastructure

- **NSF NAIRR:** The National AI Research Resource is US research infrastructure
  for compute, software, data, models, educational resources, and expertise.
  NSF reported in March 2026 that the pilot supported more than 600 research
  projects and 6,000 students across all US states, DC, and Puerto Rico. This is
  evidence that access pathways exist; confirm program eligibility and resource
  availability for a specific project. Sources: [NSF NAIRR](https://www.nsf.gov/focus-areas/ai/nairr), [two-year update](https://www.nsf.gov/cise/updates/nairr-2-years-advancing-american-artificial-intelligence).
- **NIST AI RMF:** NIST positions its framework as voluntary risk-management
  guidance and provides a Generative AI Profile. Use it to turn risks into
  measurable controls, evaluation, and documentation. It is not a certification
  or proof that a system is trustworthy. Sources: [AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf).
- **SBIR/STTR:** America’s Seed Fund describes SBIR/STTR as non-dilutive support
  and commercialization pathways for eligible US small businesses. It is a
  possible route, not evidence of product demand or a funding guarantee. Source:
  [SBIR overview](https://www.sbir.gov/about).

## Open-source systems and reproducibility

- **vLLM / UC Berkeley:** vLLM is a high-throughput LLM serving project. Its
  PagedAttention paper reports gains under its tested workloads; measure the
  actual model, request mix, hardware, and p95 latency before making a product
  choice. Source: [Berkeley project page](https://sky.cs.berkeley.edu/project/vllm/).
  Local code audit on 2026-09-16: commit `8b1d188046034b42024d22ee52fa6c3948b4acbd`, Apache-2.0 license, 2,199 test/evaluation paths.
- **SGLang:** SGLang is a structured language-model programming and serving
  system; its research paper states its focus on workflows with multiple calls,
  control flow, and structured inputs/outputs. Treat claimed performance as a
  candidate hypothesis under your workload. Source: [paper](https://arxiv.org/abs/2312.07104).
  Local code audit on 2026-09-16: commit `00a9a81b67774e8374172646c092e14999472703`, Apache-2.0 license, 3,023 test/evaluation paths.
- **DSPy / Stanford:** a programming/optimization framework candidate for
  structured LM programs. Local code audit on 2026-09-16: commit
  `bb8ba59c0c6d7c7337af3b14a18994eb8cee501b`, MIT license, 175
  test/evaluation paths. Repository presence and tests are not a local result.
- **lm-evaluation-harness / EleutherAI:** a candidate benchmark harness, not a
  substitute for target-task evaluation. Local code audit on 2026-09-16: commit
  `d6de81643928d653435c431bae19945d41d32520`, MIT license, 781
  test/evaluation paths.
- **Hugging Face model cards:** model cards are designed to document intended
  use, limitations, training, data, and evaluation. Missing or weak information
  is a provenance warning, not permission to infer it. Source:
  [Model Cards](https://huggingface.co/docs/hub/model-cards).

## Systems measurement and transparency

- **MLPerf Inference:** MLCommons defines standardized scenarios, latency,
  throughput, quality, and compliance rules for system benchmarking. Use it for
  comparable systems evidence where applicable; add project workload tests for
  actual adoption decisions. Source: [MLPerf Inference](https://mlcommons.org/working-groups/benchmarks/inference/).
- **Foundation Model Transparency Index:** Stanford’s 2025/2026 reporting shows
  that disclosure varies substantially by developer and dimension. Absence of
  disclosure should narrow claims and strengthen local testing. It does not by
  itself measure task quality. Sources: [2026 AI Index transparency chapter](https://hai.stanford.edu/assets/files/ai_index_report_2026.pdf), [Stanford analysis](https://hai.stanford.edu/news/transparency-in-ai-is-on-the-decline).

## Policy context

- The White House’s July 2025 AI Action Plan frames US policy around innovation,
  infrastructure, and international diplomacy/security. It is policy context,
  not technical performance evidence. Source: [America’s AI Action Plan](https://www.whitehouse.gov/wp-content/uploads/2025/07/Americas-AI-Action-Plan.pdf).

## Audit limits

The local audits above confirm shallow-clone integrity, a snapshot commit,
license file, and test/evaluation-path count only. They do not establish security,
quality, legal suitability, hardware compatibility, or product value. All code
was inspected as source; no third-party model code or weights were executed.
