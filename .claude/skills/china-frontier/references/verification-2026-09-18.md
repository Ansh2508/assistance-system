# Verification ledger, 2026-09-18

Run when this skill was installed. Every line below was EXECUTED (a live HTTP
request, GitHub API call, or arXiv page fetch on 2026-09-18), not inferred.
Re-run before relying on anything time-sensitive; the seed reference is a dated
starter map, not a ranking.

## Source URLs (44 unique URLs across SKILL.md and references)

- 40 resolved (HTTP 200).
- 1 returned 403 (`aiisrael.org.il/resources/`): bot protection, not proven dead.
  Open it in a browser before citing it.
- 3 unreachable from the verifying machine, so **unverified, not confirmed dead**:
  - `old2022.bulletin.cas.cn/.../20250413.htm` (connection timeout x2)
  - `www.kisti.re.kr/eng/rnd/pageView/250` (connection timeout x2)
  - `wap.sasac.gov.cn/.../c34141937/content.html` (**expired TLS certificate**,
    `SEC_E_CERT_EXPIRED`; a genuine source-side fault, do not bypass verification)
  Treat these as discovery leads only. Find the same content on a reachable
  primary page or mark the claim `unverified`.

## arXiv citations (title fetched from the abstract page)

| ID | Title as fetched | Matches the skill's description |
|---|---|---|
| 2508.16526 | Innovation ecosystems theory revisited: The case of artificial intelligence in China | yes |
| 2411.15451 | Quantitative Analysis of IITs' Research Growth and SDG Contributions | yes |
| 2409.16235 | EuroLLM: Multilingual Language Models for Europe | yes |
| 2504.05747 | SEA-LION: Southeast Asian Languages in One Network | yes |

## Repositories cited by the seed (GitHub API)

| Repo | Archived | Last push | License (API) | Note |
|---|---|---|---|---|
| QwenLM/Qwen | no | 2026-03-05 | Apache-2.0 | This is the original Qwen repo; the current line is Qwen3 (below) |
| THUDM/GLM | no | **2023-11-03** | MIT | **Stale** as a "primary starting point"; current line is zai-org/GLM-4.5 (below) |
| THUDM/WebGLM | no | 2025-03-25 | Apache-2.0 | Older; verify before reuse |
| llm-jp/llm-jp-sft | no | **2024-06-13** | Apache-2.0 | **Stale**; check the llm-jp org for successors |
| ku-nlp/kwja | no | 2026-09-13 | MIT | Active |
| ku-nlp/jumanpp | no | 2026-04-17 | Apache-2.0 | Active |
| AI4Bharat/IndicTrans2 | no | 2025-10-03 | MIT | Maintained; check the data/weights terms separately |
| aisingapore/sealion | no | 2026-09-18 | **none detected** | License must be read manually |
| suyash333/india-ai-ecosystem | no | 2026-04-18 | none detected | 2 stars; leads only, as the seed already says |

"License (API)" is GitHub's code-license detection only. Weights and data carry
their own terms (see Non-negotiable boundary 7). Not one of these rows is a
reproduction result; they are existence and maintenance checks.

## What this ledger does NOT establish

- No model in this skill was run, benchmarked, or compared. Everything about
  quality, cost, or "China wins on X" remains a hypothesis until the skill's own
  local-reproduction step produces evidence.
- The Asia regional-systems and discovery-playbook references were not
  individually fact-checked beyond the URL reachability above.
