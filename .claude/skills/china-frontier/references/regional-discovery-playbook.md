# Regional Discovery Playbook

Use this playbook to discover the right research repositories, papers, data,
standards, and technology ecosystems for a specific project. Do not start with
a favourite model or country. Start with the decision, the data type, the
rights boundary, and the evidence needed to make the decision safely.

## Route by project shape

| Project shape | First source lanes | Required regional checks | Typical failure if skipped |
|---|---|---|---|
| Multilingual research/retrieval | national scholarly indexes, institutional repositories, language NLP labs, cross-lingual benchmarks | language, script, translation lineage, entity accuracy, jurisdiction | English translation erases a decisive term, entity, negation, or citation |
| AI-for-science | national science data infrastructures, domain databases, HPC programmes, model repositories, reproducibility papers | dataset rights, scientific validity, temporal leakage, units, calibration | a model predicts a proxy but is framed as a scientific discovery |
| Legal/regulatory | official law/regulator/court portals, local language law databases, legal NLP research, standards | jurisdiction, effective date, official text, translation status, legal scope | foreign or outdated law is treated as binding local law |
| Industrial/IoT | national standards, sector labs, engineering repositories, incident reports, device/cloud docs | physical constraints, sampling, safety case, sensor missingness, local regulation | benchmark data hides real operating conditions |
| Consumer/hackathon | local user communities, market alternatives, official APIs, field studies, relevant OSS | real user task, latency/cost, safety, demo dependencies, local geography/language | an impressive prototype cannot survive real input or live APIs |
| Continual learning | primary ML papers, model/adaptor repos, evaluation frameworks, data-protection rules | independent tasks, label quality, poisoning, consent, rollout, rollback | sparse/noisy corrections corrupt a shared model |
| Technology transfer | patents, grants, publications, TTO policies, company registries, standards | family/assignee identity, date, territory, source rights, outcome labels | semantic similarity is falsely presented as FTO, novelty, or commercial proof |

## Source hierarchy by evidence type

1. **Binding or factual record:** statute, regulator, public registry,
   standards body, official programme, original dataset, canonical repository.
2. **Primary technical evidence:** paper, technical report, benchmark,
   implementation and test code, model card.
3. **Independent replication or review:** systematic review, external benchmark,
   independent evaluator, reproducibility study.
4. **Practitioner context:** engineering postmortem, reputable institute blog,
   conference materials, industry report.
5. **Discovery only:** news, social media, a GitHub fork, vendor marketing,
   search snippets, LLM summaries.

Never use level 5 as final proof. Do not let a level-4 company report prove
its own product performance when a primary or independent source is available.

## China / 中国 discovery routes

### Native query patterns

Replace `<topic>` and retain the Chinese form in the source ledger:

```text
<topic> 研究进展 论文
<topic> 开源 数据集 基准 评测
<topic> 科学数据 共享 管理 办法
<topic> 人工智能 科研 基础设施
<topic> 产学研 协同 创新
<topic> 专利 技术转移 产业化
```

### Source lanes

- Government: State Council, ministries, NSFC, CAS, CAC, SASAC; establish
  programmes, data rules, and public-infrastructure claims.
- Academic: Chinese Academy of Sciences journals, university/lab pages, local
  conference proceedings, original Chinese technical reports.
- Science data: national/CAS data services and discipline repositories; record
  access control and data classification.
- Code/models: canonical organisations such as Qwen, THUDM, ModelScope,
  DeepModeling, and BAAI; audit code, model, data, and service rights apart.
- Industry: only use corporate ecosystems to generate hypotheses; validate
  stated capability independently.

### What to extract

- whether a mechanism is a national policy objective, a released service, a
  published model, a reproducible implementation, or a local pilot;
- Chinese original terms and English aliases;
- Chinese access/residency and export constraints where applicable;
- direct links to implementation and evidence, not an English press summary.

## Japan / 日本 discovery routes

### Native query patterns

```text
<topic> 研究 動向 論文
<topic> 研究データ オープンサイエンス
<topic> 人工知能 基盤モデル 評価
<topic> 産学連携 技術移転
<topic> 実証 実装 事例
<topic> 日本語 固有表現 関係抽出
```

### Source lanes

- NII/CiNii Research for papers, datasets, projects, researchers, grants,
  repositories, and linked metadata. Its data-source filters are useful signals
  that must be preserved in the ledger.
- J-STAGE, Jxiv, JAIRO/IRDB, KAKEN/e-Rad, NII RCOS, JST and MEXT for research
  outputs, grants, open science, and AI-for-science infrastructure.
- University and national labs: RIKEN, NII, Kyoto NLP, AIST, universities;
  preserve Japanese source text and translated alias.
- Code: llm-jp, ku-nlp, RIKEN/AIST projects, native-language model cards and
  tokenization notes.

### What to extract

- source-language analytical layers: morphology, entities, relations,
  discourse, and document provenance;
- research-data and repository metadata rather than paper text alone;
- collaboration/technology-transfer structure and dates;
- a clear distinction between peer-reviewed, preprint, institutional report,
  and project page.

## India / भारत discovery routes

### Native query patterns

```text
<topic> कृत्रिम बुद्धिमत्ता अनुसंधान डेटा
<topic> भारतीय भाषाएँ मॉडल डेटासेट मूल्यांकन
<topic> ओपन सोर्स अनुसंधान परियोजना
<topic> विज्ञान प्रौद्योगिकी नवाचार नीति
<topic> भाषा प्रौद्योगिकी API
<topic> शोध प्रबंध रिपॉजिटरी
```

Use English and the relevant regional-language query together. “India” is not a
single language, script, or user group.

### Source lanes

- Government/public infrastructure: IndiaAI, AIKosh, BHASHINI, DST, MeitY,
  Principal Scientific Adviser, Digital Public Infrastructure sources.
- Research: IITs, IISc, IIIT Hyderabad, AI4Bharat, Shodhganga, National Digital
  Library, India Science & Technology portal, discipline repositories.
- Code/data: AI4Bharat, IndicTrans2, IndicXlit, IndicBERT, BHASHINI examples,
  BharatGen when canonical code/terms are confirmed.
- Community/field practice: use local-language developer and public-service
  examples to identify accessibility and low-bandwidth constraints, then
  validate capabilities at the primary source.

### What to extract

- language plus script, including transliteration and code switching;
- numeric, name, place, and legal/technical term preservation;
- per-language and per-script evaluation—not only macro average;
- cost, device, voice, OCR, and network assumptions;
- hosted-API terms versus open-weight/code terms.

## South Korea / 대한민국 discovery routes

### Native query patterns

```text
<topic> 인공지능 연구 동향 논문
<topic> 연구데이터 플랫폼 공개 데이터
<topic> 산학연 기술이전 사업화
<topic> 한국어 자연어처리 평가 데이터셋
<topic> 인공지능 안전성 신뢰성 평가
```

### Source lanes

- KISTI / ScienceON / DataON / NTIS / KoreaScience / KCI for research outputs,
  data, reports, and national research infrastructure.
- KAIST, ETRI, KIST, KISTEP, NRF and Korean-language university/lab materials.
- Korean OSS/model providers and industrial labs, subject to the same separate
  code/weight/data/API-rights audit.

### What to extract

- evidence origin: academic, government programme, industry, independent
  replication, or commercial claim;
- applied-manufacturing/robotics/health constraints when relevant;
- Korean-language retrieval and name/entity-resolution evaluation;
- interoperability links to global repository systems.

## Comparator lanes: add only for a reason

| Region | Add when you need | Primary discovery starting points |
|---|---|---|
| Europe | regulated/FAIR/sovereign data, multilingual deployment, cross-border research | EOSC, OpenAIRE, CORDIS, EuroHPC, standards bodies, national repositories |
| US | frontier benchmark, research compute, technology transfer, startup practice | NSF/NAIRR, NIST, OSTI, PubMed, grants, university TTOs, canonical model repos |
| Singapore/SEA | multilingual/multicultural delivery and public-sector AI | AI Singapore, SEA-LION, A*STAR, national policy/materials |
| Israel | Hebrew/Arabic NLP, cyber/security, applied startup validation | national NLP infrastructure, universities, official innovation sources |
| Brazil/Africa/Latin America | Portuguese/indigenous languages, public digital infrastructure, resource-constrained deployment | national science agencies, regional repositories, local ML communities |

## How to discover repositories by need

Do not search “best AI repo.” Search for the missing capability plus evidence:

```text
<language> <task> official implementation evaluation GitHub
<domain> <task> benchmark dataset license repository
<country> <task> 研究データ / 科学数据 / अनुसंधान डेटा
<task> train test overlap deduplication repository
<task> model card data license reproducibility GitHub
<task> error analysis benchmark paper code
```

Candidate repository selection needs all of:

- a real project capability gap it may fill;
- canonical ownership or clearly documented provenance;
- a compatible license/right path;
- a testable task and local acceptance metric;
- an integration/rollback plan;
- a clear reason a smaller internal implementation is not better.

## Stop conditions

Stop discovery when the current evidence is sufficient to make one of these
decisions:

- adopt a locally validated mechanism;
- run one specific local experiment;
- defer until required data/labels/access exists;
- reject a candidate due to rights, quality, safety, or non-transferability.

Do not continue collecting sources after the decision becomes clear. Depth is
the quality of the causal/evidence chain, not an unlimited bibliography.
