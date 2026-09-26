---
name: hard-won-engineering-lessons
description: >
  How to read VELTH/veOS's real incident-log skills and adapt their lessons
  to a DIFFERENT project, instead of trusting a stale hand-copied summary.
  Load whenever working on a non-VELTH/veOS project and something looks like
  a familiar shape — "this should be working but the health check might be
  lying", "the deploy succeeded but is it really running new code", "this
  test passed but did it test the right thing" — or whenever explicitly
  asked to bring VELTH/veOS engineering experience into another project.
---

# hard-won-engineering-lessons — read the source, don't trust a copy

VELTH and veOS have two skills that are living incident logs, not static
advice: `$veos-preflight`'s "KNOWN TRAPS" section and
`$veos-wiring-and-ai-test`'s numbered incidents, plus `$velth-prod-verify`'s
deploy-verification procedure. Each entry there is dated, specific, and
grows every time a new real incident happens on those projects. A hand-
copied summary of them, written once, goes stale the moment the source adds
incident #7 and the copy still only has six. So this skill does not
duplicate their content — it teaches how to pull the CURRENT version live
and do the actual work of adapting it, every time.

## The three source skills, and what each is actually documenting

- **`$veos-preflight`** — its "KNOWN TRAPS" section is real, verified,
  dated incidents specific to veOS's GCP/Terraform/Postgres/Compose setup:
  configuration drift (stale image tags, feature flags silently unwired),
  COM/DDL-application false-successes, ownership/grant traps, secret
  encoding corruption, and more. Each entry states what actually happened,
  not a generalized rule.
- **`$veos-wiring-and-ai-test`** — numbered incidents specifically about
  proving a config/deploy/AI-behavior claim is TRUE versus assumed true:
  the "structural vs. functional verification" distinction, the health-
  check-lies-about-a-fallback pattern, the single-instance-test-of-a-
  distributed-mechanism trap.
- **`$velth-prod-verify`** — the mechanical deploy-status verification
  procedure, born from one real false "not deployed" report that a human
  had to catch and correct twice.

## How to actually use this on a different project (the real process, not a lookup)

1. **Read the current source, not memory of it.** `Read` the actual
   `SKILL.md` file(s) above right now — do not rely on a summary from an
   earlier turn or a prior session, since the source may have grown since.
   These files live at
   `C:\Users\redmi\.claude\skills\veos-preflight\SKILL.md`,
   `C:\Users\redmi\.claude\skills\veos-wiring-and-ai-test\SKILL.md`, and
   `C:\Users\redmi\.claude\skills\velth-prod-verify\SKILL.md` regardless of
   which project you're currently working in — they're global skills, not
   scoped to a VELTH/veOS working directory.
2. **Identify the shape of the CURRENT problem first**, independent of the
   source material: is this a "does the health check actually prove what I
   think it proves" question? A "did the deploy really ship new code"
   question? A "this passed a test but is the test itself sound" question?
   Naming the shape before reading the source keeps you from forcing a
   VELTH-specific incident onto a problem that doesn't actually match it.
3. **Find the matching incident(s) in the source file(s)**, and read past
   the VELTH/veOS-specific names (GCP project IDs, specific file paths,
   specific service names) to the actual mechanism being described. Every
   real incident in those files has a described ROOT CAUSE and a stated FIX
   THAT ACTUALLY WORKED — that's the transferable part, not the specific
   commands.
4. **Re-derive the equivalent for the current project's real stack.** A
   VELTH incident about `docker-compose.yml`'s env-var allowlist becomes,
   on a Kubernetes project, "check the Deployment/ConfigMap actually
   references this env var, not just that it's in `values.yaml`." A veOS
   incident about `_InMemoryBackend.ping()` always returning `True` becomes,
   on any project with a circuit-breaker or fallback pattern, "does this
   fallback's own health check method return positive results reflexively —
   check its actual implementation, don't assume from the class name."
   This step is the actual work; do not skip straight from "read the
   incident" to "apply this generic-sounding lesson" without checking the
   current project's real code for the equivalent structure.
5. **State the adaptation explicitly when reporting it**, so it's clear
   this came from a real prior incident and how it was translated — e.g.
   "VELTH hit this exact shape with a Redis fallback silently reporting
   healthy; checking whether this project's [X] has the same
   isinstance-vs-shared-interface gap" — rather than presenting it as
   generic best-practice advice with no origin.

## Why this shape instead of a static summary

A copy made once (the first draft of this skill did exactly this) freezes
at whatever incident count existed on the day it was written. The source
skills keep growing — `veos-preflight` explicitly documents this: "A
written warning without an enforced check does not hold" was proven true
TWICE in the same project, months apart, precisely because the lesson
wasn't kept live and re-checked. Pointing at the source and re-reading it
live is the only way this skill doesn't become the same kind of stale
warning it's trying to prevent.

## When NOT to use this

If the current task IS on VELTH or veOS, load the project-specific skill
directly (`$veos-preflight`, `$veos-wiring-and-ai-test`, `$velth-prod-verify`)
— it already has the exact commands and paths, no adaptation needed. This
skill is specifically for carrying that experience to a DIFFERENT project.
