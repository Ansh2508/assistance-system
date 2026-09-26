# Verification log: US eval-quality research (2026-09-19)

Real, primary-source research dispatched for VELTH/veOS's growth-specialist
eval harness (see `docs/research/growth-domain-technical-architecture-2026-09-19.md`
in the veOS repo for the full application). Every source below was fetched
directly by a background research agent, not summarized from a search snippet.

## Anthropic — cold-start eval construction

- `anthropic.com/engineering/demystifying-evals-for-ai-agents` (fetched
  directly): 20-50 real tasks drawn from actual failures, not hundreds;
  validity check when no golden dataset exists = "would two domain experts
  independently reach the same pass/fail verdict"; three grader types
  (code-based, model-based, human) combined explicitly; watch for
  saturation (100% pass rate means the suite needs harder cases).
- `platform.claude.com/docs/en/docs/test-and-evaluate/develop-tests`
  (fetched via redirect from the old docs.anthropic.com URL): 50-200 test
  cases as a baseline; "use a different model for evaluation than the one
  being evaluated"; hold out 10-20% as a final validation set never used
  to tune the harness.
- Both directly encoded into `src/veos_runtime/growth_eval_harness.py` and
  `tests/evals/growth_cases.py` in the veOS repo (28 real cases, 5 held
  out, cross-family Gemini judge distinct from the Claude-generated
  content being judged).

## The Leaderboard Illusion (arXiv:2504.20879)

Fetched directly. Real, numeric findings on why a single aggregate score
is gameable: Meta tested 27 private Llama-4 variants pre-release before
choosing which to surface; Google/OpenAI received ~19-20% of Chatbot Arena
battles each while 83 open-weight models combined got only ~30%; access to
Arena battle data alone can produce up to 112% relative performance gains
on the Arena distribution specifically (a direct empirical Goodhart's Law
demonstration). Directly informs a real design choice: report pass rate
PER FAILURE CLASS, never one rolled-up eval score (see
`growth_eval_harness.py`'s `GrowthEvalSummary.pass_rate_by_failure_class`).

**"Beyond frontier" as a term: NOT FOUND as a defined technical standard
anywhere searched** (Anthropic, OpenAI, Google, or an academic benchmark
paper). Treat any use of that phrase as a marketing claim, not a measured
one, unless a specific benchmark and methodology is named alongside it.

## LangChain — LLM-as-judge calibration

`langchain.com/resources/llm-as-a-judge` (fetched): "binary or low-precision
scoring produces more reliable results than high-precision numerical
scales" - directly encoded as `CaseVerdict` (PASS/FAIL/ABSTAIN) rather than
a 1-10 score in `growth_eval_harness.py`. ~80% judge-vs-human agreement
cited as roughly matching human-human agreement, but no sample-size/kappa
methodology given on this specific page (that level of detail came from
Galileo AI instead, a different company - see the China/cross-lane note
below for where kappa specifics actually live).

## OpenAI Evals - genuinely thinner than Anthropic's guidance

`github.com/openai/evals` + cookbook: confirmed live, NO numeric minimum
sample size given anywhere in the framework's own docs - "keep iterating
until you are confident" is the only guidance. Cold-start technique found:
synthetic QA generation via a strong model, worked example uses only 5
samples with no scaling guidance. Real, disclosed gap - not padded with
adjacent material.

## What this does NOT establish

No claim here has been re-verified against a second independent source
beyond what the fetching agent itself did. Pricing/rate-limit numbers for
any model (Gemini or otherwise) decay fast - re-check via a live API call
before trusting a cached figure, not this file. This ledger is a record of
what was fetched and when, not a permanent fact base.
