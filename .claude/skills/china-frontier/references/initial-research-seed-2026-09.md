# Initial Multilingual Research Seed — 2026-09

This is a dated starter map produced during skill creation. It is not an
exhaustive review and must be refreshed for time-sensitive decisions.

## Why these regions are included

The regions were selected because they expose different mechanisms relevant to
research intelligence, multilingual AI, open science, data infrastructure,
technology transfer, and product deployment. They are not ranked by quality.

## China

### Primary starting points

- [QwenLM/Qwen](https://github.com/QwenLM/Qwen) — canonical Alibaba Qwen
  repository; inspect model and code licensing separately.
- [THUDM/GLM](https://github.com/THUDM/GLM) — Tsinghua GLM implementation and
  training structure.
- [THUDM/WebGLM](https://github.com/THUDM/WebGLM) — web-enhanced retrieval,
  human-preference scoring, and an explicit retriever/generator evaluation
  pattern.
- [Chinese Academy of Sciences ecosystem analysis](https://old2022.bulletin.cas.cn/publish_article/2025/4/20250413.htm)
  — Chinese-language institutional analysis of government, industry, and
  research interactions.
- [AI innovation ecosystem theory paper](https://arxiv.org/abs/2508.16526)
  — comparative framework for the Chinese AI innovation ecosystem.

### Transferable mechanisms to test

- bilingual/multilingual retrieval rather than English-only search;
- retriever plus human-preference or task-specific scorer;
- explicit public-industry-academia linkage modelling.

### Do not assume

- that a Chinese model's license permits commercial use of every checkpoint;
- that Chinese benchmark performance transfers to European or Indian domains;
- that translated Chinese sources preserve legal or technical nuance.

## Japan

### Primary starting points

- [National Institute of Informatics research](https://www.nii.ac.jp/en/research/)
  — research-data, trust, digital identity, big-data mathematics, LLM, and
  cross-sector infrastructure.
- [JST CRDS AI trends report](https://www.jst.go.jp/crds/report/CRDS-FY2024-RR-07.html)
  — Japanese strategic review of foundation models, impact, and risks.
- [NII research-data ecosystem deliverables](https://www.nii.ac.jp/creded/deliverables.html)
  — data-ecosystem and funding context.
- [llm-jp/llm-jp-sft](https://github.com/llm-jp/llm-jp-sft) — Japanese LLM
  supervised fine-tuning implementation.
- [ku-nlp/kwja](https://github.com/ku-nlp/kwja) — integrated Japanese analysis
  covering segmentation, NER, dependency, discourse, and coreference.
- [ku-nlp/jumanpp](https://github.com/ku-nlp/jumanpp) — Japanese morphology and
  segmentation tooling.

### Transferable mechanisms to test

- language-specific preprocessing before cross-lingual retrieval;
- domain terminology and entity-resolution evaluation;
- research-data ecosystems connecting repositories, tools, and institutions.

### Do not assume

- whitespace tokenization or English NER is adequate for Japanese;
- an English translation preserves entity boundaries, relations, or citations;
- Japanese institutional release practices are equivalent to US open-source
  practices.

## India

### Primary starting points

- [IndiaAI / Principal Scientific Adviser](https://psa.gov.in/ai-mission) —
  India AI ecosystem, policy, datasets, models, and public infrastructure.
- [AIKosha announcement](https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=2108961&lang=2&reg=48)
  — official description of India's dataset/model/use-case and sandbox
  platform.
- [AI4Bharat/IndicTrans2](https://github.com/AI4Bharat/IndicTrans2) — 22
  scheduled Indic languages, datasets, scripts, benchmarks, and licenses.
- [India AI ecosystem map](https://github.com/suyash333/india-ai-ecosystem) —
  community-maintained discovery map; useful for leads, not authoritative
  validation.
- [India research-growth study](https://arxiv.org/abs/2411.15451) — context
  for IIT research productivity and impact, with limitations of bibliometrics.

### Transferable mechanisms to test

- multilingual and multiscript retrieval;
- low-resource evaluation rather than aggregate language averages;
- public digital infrastructure and frugal deployment;
- separate language coverage, script coverage, and domain coverage metrics.

### Do not assume

- one Indic-language result transfers to all 22 scheduled languages;
- a translation benchmark proves scientific or legal retrieval quality;
- community ecosystem lists are complete or independently validated.

## South Korea

### Primary starting points

- [KAIST AI publication/research areas](https://gsai.kaist.ac.kr/publication-research-area/)
  — research themes and venues.
- [KAIST yearly publication index](https://gsai.kaist.ac.kr/publication-research-year/)
  — candidate papers and model families.
- [KAIST InnoCORE](https://kaist.ac.kr/kr/html/footer/0814.html?file_id=70891&mode=D&no=77fa2313248e793e7c6a9d2024c5e70d)
  — example of academia, industry, and public research collaboration.
- [KAIST working papers](https://futures.kaist.ac.kr/ko/?c=234&gbn=list&gp=1&sw=2026)
  — policy and governance context; verify language and date.

### Transferable mechanisms to test

- industrially grounded research evaluation;
- domain-specific and regional model deployment;
- explicit connections between academia, corporations, and government labs.

### Do not assume

- a university publication index is a market database;
- Korean-language entity and patent retrieval behaves like English retrieval;
- state-backed programme claims equal independently reproduced performance.

## Europe

### Primary starting points

- [European open-source AI landscape](https://digital-strategy.ec.europa.eu/en/library/europes-open-source-ai-landscape-lever-innovation-and-sovereignty)
  — multilingual, trusted, sector-specific, and sovereign AI opportunity.
- [European Open Science Cloud](https://research-and-innovation.ec.europa.eu/strategy/strategy-research-and-innovation/our-digital-future/open-science/european-open-science-cloud-eosc_en)
  — FAIR research data, tools, services, and cross-border interoperability.
- [EU Data Union Strategy](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:52025DC0835)
  — data spaces, data labs, rights, quality, and AI infrastructure.
- [AI4EOSC](https://ai4eosc.eu/) — research-grade model serving in an open
  science ecosystem.
- [EuroLLM](https://arxiv.org/abs/2409.16235) — multilingual European model
  research and tokenizer/data-mix decisions.

### Transferable mechanisms to test

- federated or controlled data access;
- FAIR provenance and interoperable research objects;
- language and jurisdiction-aware evidence handling;
- trusted data labs rather than ungoverned bulk ingestion.

## United States

### Primary starting point

- [US National AI Research Resource](https://www.nsf.gov/focus-areas/ai/nairr)
  — coordinated access to tools and compute for research.

### Transferable mechanisms to test

- shared research infrastructure;
- benchmark and reproducibility culture;
- university/startup/industry transfer pathways.

### Do not assume

- US compute or venture access is available in every region;
- US legal, data, or procurement assumptions transfer to Europe or Asia.

## Singapore and Southeast Asia

- [IMDA National Multimodal LLM Programme](https://www.imda.gov.sg/about-imda/emerging-technologies-and-research/national-multimodal-llm-programme)
  — SEA-LION and regional multilingual context.
- [AI Singapore SEA-LION](https://github.com/aisingapore/sealion) — open-source
  regional model and documentation.
- [SEA-LION paper](https://arxiv.org/abs/2504.05747) — low-resource, cultural,
  and regional language motivation.

## Israel and Hebrew/Arabic NLP

- [NNLP-IL](https://github.com/NNLP-IL) — national Hebrew/Arabic NLP
  infrastructure and resources.
- [AI Israel resources](https://aiisrael.org.il/resources/) — regional resource
  index; use as a discovery source and verify each artifact.

## Cross-country synthesis

The initial research suggests a design principle, not a final architecture:

> Build a language- and jurisdiction-aware evidence layer that can route each
> source to the appropriate parser, retriever, ontology, rights policy, and
> evaluator, while keeping a common provenance and decision schema.

This combines mechanisms observed in Japanese linguistic tooling, Indian
multiscript translation, Chinese retrieval/model ecosystems, Korean
industry-academia structures, European FAIR data governance, US shared compute,
and Southeast Asian cultural-language modelling. The combination is an
engineering hypothesis, not an established published system. It must be
simulated and evaluated before being called novel or frontier.

## Minimum local experiments

Before implementation claims are made, run:

1. parallel-language retrieval on the same intent;
2. original-language versus machine-translated retrieval;
3. entity and patent-family resolution across scripts;
4. cross-country temporal holdout;
5. rights/license filtering;
6. contradiction and stale-source injection;
7. human relevance and provenance review;
8. cost/latency comparison for specialist versus general models.

Record results in the schema from `SKILL.md`. This seed is successful only if
it changes or rejects a design decision with local evidence.
