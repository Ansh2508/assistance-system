# Asia Regional Systems Research — 2026-09

This is a deepening pass over China, Japan, and India, with Korea as a
comparison lane. It combines primary national/institutional sources with
canonical repositories inspected at the source-code level. It does not claim
to represent every organisation in any country.

## Research contract

**Decision:** build a reusable research method that can use regional AI and
open-science ecosystems without importing language bias, legal assumptions,
model-license risk, or benchmark leakage.

**Target systems:** VELTH, veOS, hackathons, research products, and future
multilingual retrieval/agent systems.

**Regions and language lanes:** China/Chinese, Japan/Japanese, India/Indic
languages and scripts, South Korea/Korean; Europe, US, Singapore/SEA, and
Israel remain comparator/extension lanes.

**Time boundary:** sources and repository heads were inspected in September
2026. Re-verify current policy, repository state, hosted API, and license
terms before adoption.

**Current limitation:** this pass audited code/documents and ecosystem
mechanisms. It did not run foundation-model weights or claim local model
quality, because no target task, labelled corpus, hardware budget, or
deployment environment was specified.

## Country mechanism matrix

| Region | What is structurally distinctive | Transferable mechanism | Wrong transfer to avoid |
|---|---|---|---|
| China | Model hubs combine task registries, model distribution, deployment, and evaluation; policy actively links AI, science, public data, and industry | registry-driven capability packs with explicit task contracts, owners, versions, evaluation, and safety checks | downloading or executing hub/model code by default; assuming model, code, and data rights are equivalent |
| Japan | national research-data infrastructure and language-aware analysis are treated as research infrastructure, not merely app preprocessing | preserve source-language structure first, then retrieve/translate; store research-data metadata and provenance as first-class objects | English tokenization/NER/translation as the sole representation of Japanese source material |
| India | multilingual deployment is a multiscript systems problem; evaluation, normalisation, tagging, and data-leakage controls are concrete parts of the stack | explicit language-script tags, numeral/format preservation, separate per-language evaluation, benchmark deduplication | a single aggregate “Indic accuracy” or English-pivot result claimed as equal quality for every language |
| South Korea | strong industrial-academic-public research links provide a useful comparison for deployments tied to product and manufacturing contexts | track whether evidence is academic, industrial, public-programme, or independently reproduced, and evaluate against field constraints | treating a publication list or state programme as a proof of commercial reliability |

## China / 中国

### Ecosystem findings

China’s relevant pattern is not simply “larger models.” It is the coupling of
model infrastructure, application/deployment tooling, AI-for-science efforts,
and large-scale public/industry mobilisation.

- The [State Council 2025 AI+ action](https://www.gov.cn/gongbao/2025/issue_12266/material/gwygb202525.pdf)
  explicitly includes AI-driven scientific discovery, scientific foundation
  models, intelligent research infrastructure, and open high-quality science
  datasets.
- The [NSFC 2025 next-generation AI call](https://www.nsfc.gov.cn/p1/3381/2824/66768.html)
  frames explainability, generality, robustness, lower data dependence,
  memory/reasoning separation, open scientific databases, knowledge bases, and
  physics/model/algorithm libraries as research goals.
- The [Chinese Academy of Sciences data report](https://www.cac.gov.cn/rootimages/uploadimg/1756281804811709/1756281804811709.pdf)
  reports a national research-data discovery and service pattern. Treat its
  published counts as policy context, not a local performance benchmark.
- The [CNIPA information-analysis guide](https://www.cnipa.gov.cn/module/download/downfile.jsp?classid=0&filename=16dd25176bee4c31aa311a037d3a11f8.pdf&showname=%E7%9F%A5%E8%AF%86%E4%BA%A7%E6%9D%83%E4%BF%A1%E6%81%AF%E5%88%86%E6%9E%90%E5%88%A9%E7%94%A8%E6%8C%87%E5%8D%97.pdf)
  explicitly points analysts to domestic/international scholarly databases,
  institutional thesis sources, preprints, patent sources, government reports,
  and research-project systems. This supports multi-lane source discovery.
- The [SASAC open innovation community announcement](https://wap.sasac.gov.cn/n2588020/n2588072/n2590902/n2590904/c34141937/content.html)
  illustrates an ecosystem built around central enterprises, private firms,
  institutes, universities, standards bodies, compute, models, datasets, and
  agent applications.

### Canonical code audited

#### QwenLM/Qwen

- **Local audit snapshot:** commit `2df8e8ac450fa185c421a08b0090ef81826caa6e`
  dated 2026-03-05; `README_CN.md`, `README_JA.md`, `tokenization_note_zh.md`,
  `tokenization_note_ja.md`, `eval/`, `recipes/`, and test recipes inspected.
- **Architecture lesson:** language-specific tokenizer notes and separate
  multilingual documentation are part of the implementation surface, not
  marketing.
- **Evaluation lesson:** the repository exposes C-Eval, MMLU, GSM8K,
  HumanEval, and plugin evaluation scripts. These are candidate tests; they do
  not assess a VELTH/veOS task.
- **Rights lesson:** code is Apache-2.0, but model terms vary by checkpoint.
  A code license is not permission to deploy every weight.
- **Adoption status:** `mechanism_documented`. Do not execute remote code or
  use a checkpoint until task, jurisdiction, hosting, terms, and local eval are
  defined.

#### THUDM/WebGLM

- **Local audit snapshot:** commit `dd03d8fe05b504dc734f52e8689818deff643912`
  dated 2025-03-25; `train_retriever.py`, `evaluate.py`, `evaluate/`, `model/`,
  `scripts/`, `README.md`, and `README_zh.md` inspected.
- **Mechanism:** separate web retrieval, answer generation, and preference
  scoring. The reusable part is the separation of retrieval evidence from the
  answer-quality decision, not the exact model.
- **Evaluation surface:** explicit retrieval training and QA evaluation files
  exist, but its target is web QA, not enterprise/legal/research truth.
- **Rights/safety:** code and model/data have separate terms. Web retrieval
  introduces source freshness, copyright, prompt injection, and provenance
  risks.
- **Adoption status:** `mechanism_documented`; candidate pattern for a
  source-grounded research agent only after a local faithfulness/retrieval test.

#### ModelScope/modelscope

- **Local audit snapshot:** commit `241cf7a0639c81508703df2449624fd6c10132ed`
  dated 2026-09-15; 3,576 source files and 485 test/eval-related files found;
  `tests/`, `modelscope/hub/`, `pipelines/`, `trainers/`, `README_zh.md`, and
  `README_ja.md` inspected; repository integrity check passed.
- **Mechanism:** a model/task registry with pipeline, trainer, hub, testing,
  deployment, and model-card interfaces. The transferable design is a
  capability registry that makes ownership, input/output schema, evidence,
  version, and evaluation explicit.
- **Safety finding:** the code contains explicit `trust_remote_code` checks;
  this reinforces the rule that externally supplied model code is untrusted by
  default.
- **Rights finding:** framework is Apache-2.0; individual hub artifacts require
  independent terms and provenance review.
- **Adoption status:** `mechanism_documented`. Do not import the entire hub;
  implement a small internal registry only when a target project needs it.

### China-specific research practice

Search both Chinese and English, but use Chinese primary sources for policy,
technical terminology, research programmes, and local ecosystem signals.
Preserve names in Chinese and a translated alias. Run retrieval tests on
Chinese originals, translated English, bilingual queries, and mixed-script
entities. Report each result separately.

## Japan / 日本

### Ecosystem findings

Japan’s distinctive lesson is that trustworthy AI-for-science relies on
research data and language-aware analysis infrastructure, not merely an LLM.

- The [Cabinet Office AI for Science and Open Science page](https://www8.cao.go.jp/cstp/kenkyudx.html)
  links AI-for-science to managed research data, NII RDC, SINET, open access,
  shared research infrastructure, reliability, and lower-latency systems.
- [NII RCOS](https://rcos.nii.ac.jp/) operates research infrastructure for open
  science and data ecosystems; this is a useful model for treating metadata,
  repositories, and tools as a system.
- [CiNii Research](https://cir.nii.ac.jp/) links papers, research data,
  projects, people, institutions, grants, and multiple source databases. Its
  source-level metadata should be retained rather than flattened into generic
  “search results.”
- The [JST CRDS report](https://www.jst.go.jp/crds/report/CRDS-FY2024-RR-07.html)
  frames foundation models, AI risks, and AI x domain research as distinct
  strategic streams.

### Canonical code audited

#### llm-jp/llm-jp-sft

- **Local audit snapshot:** commit `ee864f482a6014b0db607f87880266e54a12524e`
  dated 2024-06-13; training entry point, configs, converters, data directory,
  pre-commit configuration, and dependencies inspected.
- **Mechanism:** reproducible supervised-fine-tuning structure with explicit
  configs and data conversion, rather than opaque prompt-only adaptation.
- **Limit:** this small repository does not itself provide a full evaluation
  harness. Treat it as a training-layout example, not a complete deployment
  template.
- **Adoption status:** `mechanism_documented` for configuration/lineage
  discipline only.

#### ku-nlp/kwja

- **Local audit snapshot:** commit `821df300630b4d05c38406945536eaac848619da`
  dated 2026-09-02; 260 files and 65 test/eval-related files found; native
  resources, `src/kwja`, metric modules, tests, pyproject, and citations
  inspected; repository integrity check passed.
- **Mechanism:** one Japanese source can produce segmentation, normalization,
  morphology, NER, dependencies, predicate-argument relations, coreference,
  and discourse outputs. These are structured evidence layers that retrieval
  and graph systems can preserve instead of collapsing into raw translated text.
- **Rights:** MIT code; models/resources must still be checked per release.
- **Adoption status:** `mechanism_documented`. Candidate for Japanese entity
  and relation extraction evaluation, not an automatic production dependency.

#### ku-nlp/jumanpp

- **Local audit snapshot:** commit `34aa52cffbeb0ca94110a842966c9583cb151104`
  dated 2026-04-17; C++ source, build configuration, test corpus, training,
  evaluation, benchmark, dictionary, and native documentation inspected.
- **Mechanism:** language analysis uses explicit lattice/dictionary/training
  structures and substantial regression tests. This is a reminder to evaluate
  source-language preprocessing rather than assuming a general encoder absorbs
  all linguistic structure.
- **Adoption status:** `mechanism_documented`; do not treat morphology accuracy
  as research-retrieval accuracy.

### Japan-specific research practice

For Japanese material, preserve original text and structured analysis output.
Test exact native entity search, normalized forms, translation, and bilingual
retrieval separately. Do not combine scores before checking error modes such as
segmentation errors, acronym expansion, author/institution aliases, and
technical loanwords.

## India / भारत

### Ecosystem findings

India’s central lesson is that multilingual systems require explicit treatment
of language, script, code-switching, access channel, and cost—not a generic
translation toggle.

- The [IndiaAI strategy](https://psa.gov.in/ai-mission) and [AIKosha launch](https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=2108961&lang=2&reg=48)
  show a public ecosystem of data, models, compute, sandboxes, skilling, and
  applications.
- The [BharatGen initiative](https://dst.gov.in/node/7835) is a government
  supported multilingual/multimodal foundation-model effort; it is an ecosystem
  signal, not a model-quality proof for an external project.
- The [Hindi Bhashini announcement](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2239287&lang=2&reg=48)
  describes language services including identification, speech, and related NLP
  capabilities; hosted-service terms and live capability must be checked before
  use.
- The [India Science and Technology database index](https://www.indiascienceandtechnology.gov.in/scientific-resources/scientific-databases)
  identifies national research-resource lanes including the National Digital
  Library and Shodhganga/Shodhgangotri thesis repositories.

### Canonical code audited

#### AI4Bharat/IndicTrans2

- **Local audit snapshot:** commit `4f08e39cc6bf13cd62e2445dc725f22bff1a9219`
  dated 2025-10-03; 77 files; native-script preprocessing/postprocessing,
  language-code maps, overlap removal, benchmark deduplication, evaluation,
  baseline comparison, significance testing, and training scripts inspected;
  repository integrity check passed.
- **Mechanism:** each input carries language-script tags; the pipeline handles
  script unification, numeral normalization, postprocessing, and translation
  direction explicitly. It includes scripts to remove train/dev/test overlap
  and compare against baselines.
- **Transferable rule:** a multilingual system must preserve `language` and
  `script` in the schema, evaluate per language-script pair, deduplicate against
  held-out benchmark data, and preserve numeric entities.
- **Rights:** repository describes different licenses for code, corpora,
  benchmarks, and weights. Review each source before use.
- **Adoption status:** `mechanism_documented`; its leakage controls should be
  adapted to any multilingual retrieval/evaluation workflow.

#### AI4Bharat/OpenHands

- **Local audit snapshot:** commit `b9ccf9eaf2a71301fc4601a64a6af06fdef04c9b`
  dated 2023-03-15; datasets, models, docs, and training/inference structure
  inspected; repository integrity check passed.
- **Mechanism:** accessibility systems need dataset/signer/domain-aware splits,
  not an undifferentiated “multimodal” score.
- **Limit:** the snapshot is older and has limited visible test infrastructure.
  It is context and a task-design lesson, not a dependency recommendation.
- **Adoption status:** `discovery_only`.

#### bhashini-ai/bhashini-api-examples

- **Local audit snapshot:** commit `d4c7454b10c056444a72697fb1f1d6f9aec1eff9`
  dated 2026-05-05; API examples for speech, translation, OCR, and WebSocket
  interfaces inspected; repository integrity check passed.
- **Mechanism:** language access can be offered behind clearly bounded service
  interfaces rather than embedding all models inside each product.
- **Limit:** examples are not a reliability/security guarantee; live API terms,
  authentication, data residency, availability, retention, rate limits, and
  output quality must be tested for the intended use case.
- **Adoption status:** `discovery_only`.

### India-specific research practice

For every test set, stratify by language and script. Include code-switched and
numeric/legal/technical terminology cases. Evaluate original-language queries,
transliterated queries, English pivots, and direct language-pair retrieval.
Never publish only a macro average when a low-resource language fails.

## South Korea / 대한민국

### Ecosystem findings

- [KAIST AI’s publication index](https://gsai.kaist.ac.kr/publication-research-year/)
  and [research areas](https://gsai.kaist.ac.kr/publication-research-area/)
  are useful discovery lanes for current papers and model families.
- [KISTI](https://www.kisti.re.kr/eng/rnd/pageView/250?t=1751587200081)
  operates Korean research data, integrated-search, and open-access-oriented
  infrastructure, while [KCI](https://www.kci.go.kr/kciportal/po/search/poArtiTextSear.kci)
  provides a Korean-language journal/citation discovery lane.
- [KAIST InnoCORE](https://kaist.ac.kr/kr/html/footer/0814.html?file_id=70891&mode=D&no=77fa2313248e793e7c6a9d2024c5e70d)
  shows an explicit academic-industry-research collaboration structure.

### Transferable mechanism

Add `evidence_origin` to research/ML ledgers: `academic`, `industry`,
`government_programme`, `open_source`, `independent_replication`, or
`commercial_claim`. This avoids treating all evidence as equally predictive of
field deployment.

## Architecture consequences

The regional evidence supports four structural requirements for future systems:

1. **Language-aware evidence objects:** every document/query stores original
   language, script, translation lineage, locale/jurisdiction, extraction
   pipeline, and confidence by field.
2. **Capability registry:** every model/tool has an input-output contract,
   version, source, code/weight/data/API rights, evaluation suite, safety
   profile, owner, and rollback status.
3. **Evaluation matrix, not one score:** report per country, language, script,
   domain, document type, time slice, and evidence origin. Add aggregate
   measures only after the slices are inspected.
4. **Evidence-preserving orchestration:** retrieval, translation, structured
   extraction, ranking, and generation are separable stages. Generation may
   summarize verified records but cannot erase provenance or manufacture facts.

## Local validation plan before adoption

No foundation model is recommended yet. A future project must provide a target
task and data, then compare:

| Claim | Baseline | Candidate | Required evaluation |
|---|---|---|---|
| Multilingual retrieval is better than English-only retrieval | BM25/English translation | language-aware retrieval with original text | per-language nDCG/Recall, human relevance, entity preservation |
| Translation does not damage decisions | original-language retrieval | translated/pivot retrieval | paired source-level error analysis, numerical/negation/entity checks |
| A regional model helps | current approved model | regional candidate | same split, latency/cost, rights, calibration, adverse slices |
| Registry improves safe integration | ad hoc provider call | capability registry | missing-rights, stale-version, unsafe-code, and rollback tests |

The result is only adopted if it improves a predeclared product decision on a
held-out, language-stratified, leakage-safe dataset without weakening rights,
security, provenance, or operating constraints.
