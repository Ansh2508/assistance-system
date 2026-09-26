---
name: quota-tiered-delegation
description: Split a task into judgment-heavy phases (kept on the primary model) and high-volume mechanical phases (delegated to a cheaper/faster tier), to save cost and quota without routing traffic through any third-party proxy. Use when a task is large, has a clear plan/implement split, or when quota/cost is a stated concern.
---

# Quota-tiered delegation — same idea as OmniRoute, none of the risk

## Why this exists, and what it deliberately does NOT do

Researched 2026-09-26 after being asked to install "OmniRoute" (a third-party
MCP gateway, `diegosouzapw/OmniRoute`, that proxies Claude Code's coding
phases through non-Anthropic model providers to save Anthropic quota). Real
findings from that research, kept here so this decision isn't re-litigated
blind next time:

- OmniRoute's own container image carries **7 critical + 62 high-severity
  CVEs** (Aqua Trivy scan, reported in a GitHub security issue against it).
- Its entire mechanism is routing your prompts/code through a **third-party
  MCP server** to whichever external model provider you configure — for a
  codebase handling GDPR-sensitive client data (VELTH), that is a real
  data-exfiltration and prompt-injection surface, not a hypothetical one.
- **Decision: do not install or run OmniRoute.** The underlying idea (split
  judgment from mechanical work, delegate the mechanical part somewhere
  cheaper) is sound and worth keeping — just not via an unvetted proxy.

This skill implements the same underlying principle using only first-party
tooling already in this environment: the `Agent` tool's `model` parameter,
which accepts Claude model tiers directly (no third-party network hop, no
new credential, no new attack surface).

## The principle

Not every phase of a task needs the most capable (most expensive, slowest)
model. Split the work:

- **Judgment-heavy phases stay on the primary/default model** (whatever this
  session is already running as): scoping, planning, spec-writing,
  acceptance-criteria review, anything where a wrong call is expensive to
  unwind.
- **High-volume mechanical phases delegate to a cheaper/faster tier** via
  `Agent(model: "haiku")`: boilerplate generation, repetitive edits across
  many similar files, straightforward test-writing from an already-approved
  spec, log/output summarization, simple search-and-report tasks.

This is the same "judgment vs. mechanical" split OmniRoute's own skill
documents (its phases 0-6 and 8 stay on Claude; only phase 7, "Implement,"
delegates) — just kept entirely inside Anthropic's own model family instead
of exiting to a third-party gateway.

## How to apply it

1. Before delegating, name explicitly which phase this is and why it's
   mechanical, not judgment-heavy — don't delegate a phase just because it's
   long; delegate because getting it wrong is cheap to catch and fix.
2. Call `Agent` with `model: "haiku"` and a **self-contained** prompt (per
   this environment's own Agent-tool guidance: include the exact spec/plan
   the mechanical phase should follow — a cheaper model needs MORE explicit
   instruction, not less, since it won't infer as much from thin context).
3. The calling session (you, on the primary model) still reviews the
   delegated output before it's treated as done — cheaper-model output gets
   the same verification bar as anything else, per this project's own
   truth-gate discipline. Delegating execution never means skipping
   verification.
4. If a mechanical-looking phase turns out to need real judgment calls
   partway through (an edge case, an ambiguous spec gap), stop the
   delegation and pull it back to the primary model rather than letting the
   cheaper tier guess.

## What this does NOT claim

- This is not a drop-in replacement for OmniRoute's specific feature set
  (it has no non-Anthropic provider routing, no MCP gateway, no
  360-provider fallback). It replicates the one underlying idea — cost-
  tiered delegation — that was actually worth keeping.
- Cost savings here come from using a cheaper Claude tier for mechanical
  work, not from routing to a free third-party provider. That's a smaller
  saving than OmniRoute claims, traded for zero new attack surface — a
  trade worth making for a codebase with real client data in it.
