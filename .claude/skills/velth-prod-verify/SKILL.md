---
name: velth-prod-verify
description: The mandatory check before ANY claim that a VELTH fix/regression "did/didn't reach production," "is/isn't live," or "was/wasn't deployed." Load it the moment a deploy-status question comes up — from a bug report, a "was it deployed" question, or before writing that a regression is or isn't in prod. Distinct from velth-truth-gate (which governs the report in general): this is the specific, mechanical procedure for the one claim type that has already produced a real false report in this project (2026-09-22, the senden() Begehung regression).
---

# VELTH prod-verify — deploy-status claims expire the instant you stop looking

## Why this exists, in one incident

2026-09-22: a regression (`36236d0b1`) merged to `main`. I checked Cloud Build
history in the correct production project and found the last successful build
predated the regression — correct, true, EXECUTED evidence at that moment. I
reported "not deployed" to the user.

**It was already stale by the time I said it.** A separate PR merged minutes
later, triggered a real deploy (`gcloud builds` `1ff74976`, image `b035b40`,
08:30:36Z), and the live Cloud Run revision now included the regression. I only
caught this because the user (correctly) refused to accept my claim and pushed
back twice ("was it deployed", "are usure", "alihan says it went in production
but still not fixed") — the fix should not have depended on the human catching
the AI's stale claim. This is `velth-truth-gate`'s "structural vs. functional
verification" and `veos-wiring-and-ai-test`'s "configuration drift" failure
mode, now confirmed real on VELTH specifically, not just veOS.

**A deploy-status check is a snapshot, not a fact.** It is true only at the
instant it ran. Any commit merge, any CI trigger, any manual `gcloud builds
submit` between the check and the report can invalidate it silently — there is
no error, no warning, nothing "looks wrong." The check itself is not the bug;
treating its output as durable is.

## Also confirmed wrong in the same session: guessing the production project

Before finding the actual regression-in-prod evidence, I spent multiple turns
querying the WRONG GCP projects (`veth-veos-dev` — a different, unrelated
product; `velth-outbound-gbu` — a BigQuery/Places project with no Cloud
Run/Build history at all) because I trusted `gcloud config get-value project`
(the CLI's ambient default) instead of confirming the real target first. The
user had to correct me twice ("velth project not veos", "find real project")
before I checked `gcloud services list --enabled` across all `gcloud projects
list` candidates and found the one with `run.googleapis.com` +
`cloudbuild.googleapis.com` actually enabled and populated
(`project-586773bf-b9c9-4237-ae2`, services `velth-frontend` / `velth-api`,
region `europe-west3` — confirmed against `deploy.ps1`'s own hardcoded values,
which should have been the FIRST thing checked, not the last).

**Never run a deploy-status check against whatever project `gcloud` happens to
default to.** Confirm the target first, cheaply, from a source that can't
drift with your shell session:

```bash
# The authoritative source — read it, don't assume it:
grep -E "PROJECT|REGION|SERVICE" deploy.ps1
# Cross-check: which project(s) actually have Run+Build enabled and populated
for p in $(gcloud projects list --format="value(projectId)"); do
  echo "=== $p ==="
  gcloud services list --enabled --project=$p 2>/dev/null | grep -E "run\.googleapis|cloudbuild\.googleapis"
done
gcloud run services list --project=<candidate> 2>&1  # confirm velth-frontend/velth-api exist here
```

If a human names the project explicitly ("velth project not veos"), that
overrides everything above immediately — don't keep querying the wrong one to
"confirm" what they already told you.

## The mechanical procedure — every time, no shortcuts

**1. Confirm the real production project/services first** (see above). Do not
skip this because a prior session or memory says you already know it — GCP
project topology is exactly the kind of thing that can have multiple
similarly-named decoys (`veth-veos-dev`, `velth-outbound-gbu`,
`begehung-prototype` all exist alongside the real one).

**2. Get the LIVE revision's actual build commit, not the build log in
isolation:**

```bash
P=project-586773bf-b9c9-4237-ae2
gcloud run services describe velth-frontend --project=$P --region=europe-west3 \
  --format="value(status.latestReadyRevisionName)"
# Cloud Run revision names for this service embed the SHORT_SHA substitution
# used at build time (e.g. velth-frontend-bb035b40-1ff74976 -> SHORT_SHA=b035b40)
```

**3. Check ancestry, not recency.** A commit's timestamp relative to "when I
last checked" is not the question. The question is whether the regression
commit is a git ancestor of the exact SHA the live revision was built from:

```bash
git fetch origin main
git merge-base --is-ancestor <regression-commit> <deployed-short-sha> \
  && echo "LIVE — regression is deployed" \
  || echo "not in this build"
```

**4. State the claim with an explicit expiry, in the same sentence.** Never
write bare "not deployed" or "deployed." Write: *"As of `<gcloud command
timestamp>`, the live revision (`<revision name>`, built from `<short sha>`)
does/does not include commit `<sha>`. This will go stale the moment another
build runs — re-check before relying on it if more than a few minutes, or any
new merge to main, has passed."*

**5. If the deploy pipeline itself looks broken (CI `startup_failure`,
`workflowName` empty, etc.), that does NOT mean nothing has deployed.**
2026-09-22's first check made exactly this inference error implicitly — GitHub
Actions' `cd-production.yml` was failing at startup on every recent run, which
was true and real, but Cloud Build deploys in this repo can also run via
`deploy.ps1`'s direct `gcloud builds submit`, independent of that GitHub
Actions workflow entirely. **A broken CI workflow only tells you that ONE
deploy path is broken. Check the actual Cloud Run revision, not the health of
a workflow that might not be the only way code reaches it.**

**6. Before reporting DONE on a regression fix, re-run steps 2–3 one more
time**, immediately before the message is sent — not from memory of an earlier
check in the same conversation. If any commit landed on `main` since your
last check (`git log --oneline origin/main -5` after a fresh `git fetch`),
re-verify; do not assume the deploy state is unchanged just because little
time has passed in wall-clock terms — a fast-moving repo with concurrent
agents/PRs (confirmed real in this project: 5 Begehung-related PRs merged
inside roughly 3 hours on 2026-09-22) can deploy multiple times inside a
single conversation turn.

## What NOT to do

- Don't trust `gcloud config get-value project` as the production target —
  confirm against `deploy.ps1`/`cloudbuild.*.yaml`'s hardcoded values first.
- Don't treat a Cloud Build history check as durable — it answers "as of this
  query," not "as of now" the moment any time passes or you move to another
  task.
- Don't infer "nothing has deployed" from "the automated CI workflow is
  broken" — check the actual running revision; a manual/alternate deploy path
  may still have shipped it.
- Don't re-report a deploy-status claim made earlier in the same conversation
  without re-running the check — especially right before a "done"/PR-merge
  message, which is exactly the moment staleness costs the most.
- Don't guess at production identity-provider credentials (Zitadel PAT scopes,
  endpoint versions) through live trial-and-error against a real IdP — two
  failed authenticated attempts against `auth.velth.io` in one session is the
  line; stop and report the blocker rather than continuing to probe.

## Where this sits

`velth-truth-gate` governs report honesty in general — this is the specific,
mechanical checklist for the one claim category (deploy/production status)
that has already produced a real, user-corrected false report on this
project. Load both when a fix's production impact is being assessed; this one
first (it is more specific), truth-gate's five-question pass second (for
everything else in the same report).
