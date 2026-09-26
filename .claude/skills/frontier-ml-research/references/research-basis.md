# Research basis (checked 2026-09-15)

This is a decision aid, not a claim that any method wins every dataset.

| Question | Primary source | Transferable finding | Boundary |
|---|---|---|---|
| Pairwise ranking | Burges et al., *Learning to Rank using Gradient Descent* (Microsoft Research, 2005) | Probabilistic pairwise loss can train a ranking function with gradient descent. | Needs meaningful order labels; a proxy is not enjoyment truth. |
| Self-supervised sequences | Yue et al., *TS2Vec* (AAAI 2022) | Hierarchical contrastive views can learn timestamp/subsequence representations without manual labels. | Downstream task still needs a valid target and leakage-safe evaluation. |
| Patch-based sequences | Nie et al., *A Time Series is Worth 64 Words* (ICLR 2023) | Patching can preserve local temporal structure while reducing attention cost for long sequences. | The paper studies forecasting; route-ranking transfer must be tested. |
| Few-shot adaptation | Finn, Abbeel and Levine, *MAML* (ICML 2017) | Meta-training can make a model adaptable with a few gradient steps on a new task. | Needs independent tasks and repeated data; sparse anonymous telemetry is insufficient. |

## Required local test

Compare the current ranker with at least one temporal candidate on the same
geographic/trip/time holdout. Report ranking metric, Brier/log loss, interval,
missing-sensor stress, inference cost, and explanation faithfulness. If the
temporal candidate is not better, keep the transparent ranker and record why.

## Evidence discipline

The user-provided OpenTSLM paper (`2510.02410v3.pdf`) is a candidate source,
not automatically a validated solution. Read it in full before claiming its
method or results apply; map task, data scale, objective, and evaluation to
the local telemetry problem.
