# Repository Forensics

Use this checklist for every GitHub/GitLab repository that may influence a
model, architecture, data pipeline, or product decision.

## Evidence record

```text
canonical_repository:
commit_sha_and_date:
upstream_identity_verified_by:
native_language_documents_read:
license_code:
license_weights:
license_data:
hosted_service_terms:
maintenance_signal:
installation_surface:
network_and_secret_surface:
unsafe_dynamic_code_surface:
data_preparation_surface:
training_surface:
evaluation_surface:
test_surface:
reproduction_attempt:
observed_result:
transferable_mechanism:
non_transferable_assumptions:
adoption_status:
```

## Inspection order

1. Confirm the canonical owner, release/commit, and license files.
2. Read the native-language README, model card, technical report, and
   evaluation documentation before third-party English explanations.
3. Locate the entry points, configuration, data preparation, training,
   inference, evaluation, tests, and deployment paths.
4. Search for dynamic import, plugin loading, `trust_remote_code`, shell
   execution, downloads, telemetry, credentials, external endpoints, and
   license-acceptance flows.
5. Check whether preprocessing prevents leakage: deduplication, split creation,
   normalization, source timestamps, and entity/family grouping.
6. Identify the actual claimed contribution. It might be a data pipeline,
   tokenizer, evaluation discipline, model architecture, deployment interface,
   or governance pattern—not necessarily the headline model.
7. Decide whether the finding is a constraint, default, design pattern,
   invented-and-gated mechanism, or rejection. See `research-to-code`.

## Non-negotiable questions

- Is the model code license different from the model-weight license?
- Does the repository have evaluation scripts and held-out splits, or merely
  reported benchmark tables?
- Does preprocessing leak benchmark or future data into training?
- Does the implementation assume a specific language, script, jurisdiction,
  GPU, API, or research-data permission?
- Could a security-sensitive application safely run this code with untrusted
  inputs or downloaded artifacts?
- Is a hosted API required even though the repository appears open source?
- Which mechanism is reusable without copying the entire stack?

## Adoption levels

| Level | Meaning |
|---|---|
| `discovery_only` | Source is a lead; no claim about reliability. |
| `mechanism_documented` | Code/docs identify a transferable mechanism. |
| `isolated_reproduced` | The relevant result ran in an isolated environment. |
| `locally_compared` | It beat or lost to alternatives on local leakage-safe data. |
| `approved_for_integration` | Human-approved, licensed, tested, rollback-ready. |
| `rejected` | A known reason blocks use. |

No repository progresses above `mechanism_documented` merely because it is
well known, widely starred, or from a prestigious laboratory.
