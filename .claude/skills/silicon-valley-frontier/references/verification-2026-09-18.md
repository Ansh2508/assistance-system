# Verification ledger, 2026-09-18

Run when this skill was installed. Every line was EXECUTED on 2026-09-18 (live
HTTP request, GitHub API call, or arXiv page fetch). Re-run before relying on
anything time-sensitive.

## Source URLs (12 unique)

- 11 resolved (HTTP 200).
- 1 returned 403: `mlcommons.org/working-groups/benchmarks/inference/`. Bot
  protection, not proven dead; open it in a browser before citing.

## Citations

- arXiv 2312.07104 fetched: "SGLang: Efficient Execution of Structured Language
  Model Programs". Matches the reference's description.

## Commit SHAs in us-frontier-systems-2026-09.md (previously inherited claims)

Each SHA was looked up through the GitHub API and exists in its upstream repo:

| Repo | SHA (first 10) | Upstream commit date |
|---|---|---|
| vllm-project/vllm | 8b1d188046 | 2026-09-16 |
| sgl-project/sglang | 00a9a81b67 | 2026-09-16 |
| stanfordnlp/dspy | bb8ba59c0c | 2026-09-15 |
| EleutherAI/lm-evaluation-harness | d6de816439 | 2026-09-14 |

This confirms the commits are real and match the stated 2026-09-16 audit window.
It does NOT re-verify the reference's license or test-path counts, and it says
nothing about quality, security, or fit.

## Repository health snapshot (GitHub API, 2026-09-18)

| Repo | Archived | Last push | License (API) |
|---|---|---|---|
| vllm-project/vllm | no | 2026-09-18 | Apache-2.0 |
| sgl-project/sglang | no | 2026-09-18 | Apache-2.0 |
| stanfordnlp/dspy | no | 2026-09-18 | MIT |
| ray-project/ray | no | 2026-09-18 | Apache-2.0 |
| EleutherAI/lm-evaluation-harness | no | 2026-09-14 | MIT |

`ray-project/ray` is named in SKILL.md's US-specific lenses but had no audit row
in the reference; the row above is an existence/maintenance check only.

## What this ledger does NOT establish

No provider API was called, no benchmark was run, and no commercial claim (NAIRR
project counts, SBIR routes) was independently checked beyond the page loading.
Those remain "fetched source", the lowest evidence tier the skill itself defines.
