# Verified current candidates, 2026-09-18

Added at install time to replace the stale entries in the seed's China section.
Each row was checked through the GitHub API on 2026-09-18 (exists, not archived,
last push, detected code license). These are **candidates to evaluate, not
recommendations**: none was run, and the skill's rule stands that a repository
is a hypothesis until it beats the incumbent on a predeclared local task.

| Repo | Why it is worth a probe | Last push | License (API) | Read before use |
|---|---|---|---|---|
| QwenLM/Qwen3 | Current Qwen line; multilingual, wide size range | 2026-01-09 | **none detected** | Repo license is undetected; read the LICENSE file and each weight's model card separately |
| deepseek-ai/DeepSeek-V3 | Large open-weight reasoning/general model | 2025-08-28 | MIT | Code MIT; weights have their own license, and serving cost at this size is a real constraint |
| MoonshotAI/Kimi-K2 | Open-weight agentic/tool-use model | 2026-01-21 | **NOASSERTION** | A non-standard license: read it (modified terms are common) before any commercial use |
| zai-org/GLM-4.5 | Current GLM line (successor lineage to the stale THUDM/GLM) | 2026-02-01 | Apache-2.0 | Confirm weight terms per checkpoint |
| FlagOpen/FlagEmbedding | BAAI embedding/reranker family (multilingual retrieval, incl. the BGE-M3 line) | 2026-08-24 | MIT | Most directly relevant to veOS retrieval; see the constraints file |
| OpenBMB/MiniCPM | Small models for edge and low-cost inference | 2026-09-12 | Apache-2.0 | Check the quality/latency trade against a Haiku-class incumbent |

## How to use a row

1. Write the task contract first (see SKILL.md, "China-first advantage loop").
2. Pull the exact commit and the exact weight card; record code, weights, and
   data licenses as three separate facts.
3. Run in an isolated environment; never enable `trust_remote_code` inside the
   product to "just look".
4. Compare against the incumbent AND the best non-China alternative (the
   silicon-valley-frontier skill supplies the US lane) on the same split.
5. If it does not win on the measured criteria, record it as a rejected
   candidate in the packet. That is a valid, valuable outcome.
