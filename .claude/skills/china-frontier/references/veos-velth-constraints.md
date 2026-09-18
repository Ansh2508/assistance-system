# veOS / VELTH adoption constraints

Load this before recommending any model, embedding, or service from a
China-origin (or any non-incumbent) source for veOS or VELTH. It turns the
skill's generic "check rights, boundary, and reproducibility" into the concrete
gates that already exist in this environment. Facts below were read from the
repo and standing project policy on 2026-09-18; re-check anything that could
have changed.

## Hard gates (a candidate that fails one is rejected, not "risky")

1. **No partner or third-party models through Vertex AI Model Garden or any GCP
   Marketplace path.** Standing policy after the EUR 2,300 incident (Aug 2026):
   Google program credits do not cover Marketplace or partner spend. Qwen,
   DeepSeek, Kimi, GLM and similar are partner listings if offered there, so
   "available on Vertex" is NOT a hosting route. Legitimate routes: open weights
   run on compute we control, a direct provider API under a fresh explicit
   decision, or a model already reachable through the AWS Bedrock path veOS
   uses for Claude (`us-east-1`).
2. **Model-routing changes on live traffic need a fresh confirmation.** Per the
   project's GCP action policy, changing a routing toggle that affects real
   founder traffic (`VEOS_MODEL_PROVIDER` and similar) is never assumed from a
   research result. Propose it; do not flip it.
3. **New billed services and builds need cost stated first.** Enabling a new
   billed API, or running `gcloud builds submit`, requires stating the cost
   before acting.

## Data boundary (decide before any evaluation that sends real data)

VELTH is German workplace-safety compliance (ArbSchG, DGUV). Real customer
documents and founder Drive/Slack/GitHub content are in scope for veOS. Sending
prompts containing that content to any externally hosted API, in China or
anywhere, is a data-transfer decision that needs a human and, where personal or
customer data is involved, legal review. Default posture for evaluations:

- Use synthetic or already-public text for hosted-API probes.
- Use real data only with open weights running inside our own boundary.
- Record which data class each probe used, in the packet's source ledger.

## Where a China-origin candidate could plausibly matter here

Stated as hypotheses to test, each with the incumbent it must beat:

| Job | Incumbent today (from config) | Candidate lane | Winning criterion to predeclare |
|---|---|---|---|
| Multilingual (DE/EN) retrieval embeddings | `gemini-embedding-001` (`embedding_model`); Claude has no embeddings endpoint, so this stays a separate model choice | FlagEmbedding / BGE-M3 line (see `verified-candidates-2026-09-18.md`) | Recall@k on German+English veOS/VELTH queries, plus latency and cost per 1k docs |
| Cheap extraction/classification tier | `claude_extraction_model` and `claude_default_model` = Claude Haiku 4.5 on Bedrock | MiniCPM-class small models, open weights, in-boundary | Field-level extraction accuracy on veOS fixtures, refusal/injection behaviour, ops cost |
| Synthesis tier | `claude_synthesis_model` = Claude Sonnet 4.6 | Large open-weight models (Qwen3, DeepSeek-V3, GLM-4.5, Kimi-K2) | Only if hosting cost and licence terms pass the gates above; otherwise reject without a run |

## Where to measure, so results are comparable

- veOS has an eval harness: `src/veos_runtime/evals/` (`cases.py`, `runner.py`,
  `scorers.py`, `gates.py`, fixtures in `evals/fixtures/`). Add candidate cases
  there rather than inventing a parallel harness (project principle: reuse over
  reinvention).
- A unit test or a benchmark chart is not adoption evidence. The veOS standard,
  learned the hard way, is a real end-to-end call against the running system and
  a messy adversarial input, plus `infra/runtime/verify-deployed-image.sh` after
  any deploy (see the `veos-wiring-and-ai-test` skill). Reading code proved
  nothing in several real incidents.

## Handoff

Pass surviving candidates to `research-simulate-encode` (local reproduction and
adversarial test), then `research-to-code` (smallest enforceable change), then
`velth-truth-gate` before any "it's better" claim leaves the session.
