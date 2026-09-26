---
name: frontier-ml-research
description: Design and validate a research-grounded ML model ladder for time-series, ranking, personalization, or hackathon systems without confusing novelty with evidence.
---

# Frontier ML Research

Use when a team wants technically impressive ML, cites a paper, asks for
backpropagation/meta-learning/transformers, or is deciding whether a simple
baseline is sufficient. The goal is novelty that is measured, explainable,
and deployable.

## 1. State the actual learning problem

Write the prediction unit, labels, and deployment decision. Count independent
trips, riders/tasks, regions, and time periods; pooled rows are not
independent samples. Explicitly state when a target is only a behavior proxy.

## 2. Build the model ladder

Run comparable experiments in this order: heuristic/proxy; linear pairwise
ranker; nonlinear tabular ranker; temporal representation/sequence model when
raw sequences exist; personalization/meta-learning only with repeated
independent tasks; ensemble only after error-complementarity and ablation.

For telemetry, TS2Vec-style contrastive embeddings and PatchTST-style patches
are candidate hypotheses. A forecasting paper is not automatically a route-
preference paper: adapt the objective and prove transfer locally.

## 3. Split before tuning

Use group splits preventing the same trip, rider, segment, or nearby geography
from crossing train/test. Add a forward-time holdout when behavior changes.
Fit scaling, imputation, feature selection, and proxy thresholds on training
data only.

## 4. Define acceptance first

Report pairwise accuracy/AUC or NDCG; log loss and Brier calibration; missing-
sensor/corruption/unseen-region robustness; latency and memory; route
feasibility and diversity; zero safety-gate violations; and XAI completeness
plus perturbation faithfulness. Use repeated group splits or confidence
intervals and include random/shuffled-label controls.

## 5. Keep an evidence ledger

Record `claim | primary source | conditions | local simulation | result |
decision | limitation`. Classify each number as learned, source-estimated,
tuned hyperparameter, engineering guardrail, or invented synthesis. Never
present a tuned coefficient as a discovered law.

## 6. Explainability and safety

Expose feature and temporal-window contributions. Test that removing a claimed
important factor changes output in the claimed direction. Keep risk, weather,
fuel, and legal constraints outside fun utility and fail closed on missing
evidence. An LLM may verbalize verified facts but may not rank, calculate, or
override gates.

## 7. Personalization gate

Do not use MAML or per-user neural fine-tuning because it sounds advanced.
Require repeated observations, cold-start and warm-start splits, shrinkage to
the fleet prior, and improvement over the global model with uncertainty. With
sparse feedback, use a bounded Bayesian/hierarchical or regularized delta
update and call it personalization, not meta-learning.

## 8. Stop conditions

Reject a candidate if its gain disappears on the geographic/time holdout, is a
leakage artifact, worsens calibration/robustness/explanations, or exceeds the
product budget. Report the best adopted model and strongest rejected model.

Read `references/research-basis.md` before making a paper-based architecture
claim; use research-simulate-encode and research-to-code to validate and
attach it to a concrete code object.
