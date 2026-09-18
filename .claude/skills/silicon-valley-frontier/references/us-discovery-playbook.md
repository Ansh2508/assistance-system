# US Frontier Discovery Playbook

Use this after writing a decision contract. Search a capability, not a company
name, and record why each lane is relevant.

## Queries by lane

| Decision shape | US-first query patterns | Independent comparison lanes |
| --- | --- | --- |
| LLM or multimodal serving | `<workload> vLLM benchmark`, `<workload> SGLang latency`, `<model> OpenAI-compatible serving`, `<hardware> MLPerf inference` | China-origin serving/model stacks; EU/Japan/Korea hardware and deployment constraints |
| Agent or structured workflow | `<task> DSPy evaluation`, `<task> structured output failure`, `<task> agent benchmark reproducible`, `<task> tool-use security` | China agent frameworks; academic and enterprise workflow research |
| Scientific or high-assurance AI | `<domain> NSF AI dataset`, `<domain> NIST evaluation`, `<domain> DARPA program`, `<domain> model card limitations` | Country-specific research infrastructure, regulation, and domain data |
| Startup or deep-tech product | `<buyer job> procurement`, `<buyer job> design partner`, `<problem> SBIR STTR`, `<sector> technology transfer` | Local buyer/regulator evidence; country-specific distribution and willingness-to-pay |
| AI infrastructure | `<workload> GPU scheduling`, `<workload> inference p95`, `<workload> cost per successful task`, `<workload> outage fallback` | Chinese and global infrastructure candidates on identical traffic |

## Repository-forensics minimum

For every candidate repository, inspect before any install:

1. canonical upstream and owner;
2. exact commit, recent releases, issue/CI health, and license;
3. architecture, input/output boundaries, data preparation, evaluation, and tests;
4. dependency supply chain, network calls, remote-code flags, serialization, and
   credential handling;
5. model, data, and hosted-service terms separately from source license;
6. a disposable reproduction plan and explicit rejection condition.

## Provider test record

For a closed API, record:

`provider | model/version | date/time/region | system prompt and parameters |
input class | schema/tool behavior | output facts | safety/refusal behavior | p50/p95 |
token or request cost | data/retention setting | outage/fallback result | decision`

Never store raw customer secrets or personal data in this record.

## Commercialization evidence hierarchy

Strongest to weakest for a product claim:

1. paid renewal or measured operational outcome;
2. paid pilot with a pre-agreed success metric;
3. signed design partner with access to the real workflow;
4. user research identifying the owner, pain, budget, and replacement behavior;
5. public procurement, grant, award, market report, funding, or competitor claim;
6. founder intuition or a generic trend article.

Do not collapse these into one “market validation” label.
