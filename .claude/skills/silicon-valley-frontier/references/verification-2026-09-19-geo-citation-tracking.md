# Verification log: free/durable GEO citation-tracking architecture (2026-09-19)

Real research dispatched after VELTH explicitly refused any paid API
(Perplexity Sonar) for GEO (generative-engine-optimization) citation
tracking. All findings below fetched directly from primary sources.

## Perplexity: confirmed no durable free path

`docs.perplexity.ai/getting-started/pricing` (fetched directly): no free
tier, $1/1M input tokens + $5/1,000 requests minimum. "Perplexity for
Startups" (perplexity.ai/startups) exists but requires VC/accelerator
referral, is capped at 6 months, and credits expire — not durable, and
conflicts with a standing "never pay" policy even as free credits (creates
a dependency that becomes a real cost the moment it expires).

## Gemini API (ai.google.dev, direct — not Vertex) + google_search grounding

Exact response shape confirmed via `ai.google.dev/gemini-api/docs/generate-content/google-search`:
`groundingMetadata.groundingChunks[].web.{uri,title}` +
`groundingSupports[].segment.{startIndex,endIndex,text}`.

**Two real, dated reliability caveats, found via direct fetches, not
assumed:**
- `web.uri` is a `vertexaisearch.cloud.google.com/grounding-api-redirect/...`
  REDIRECT, not the real source URL (confirmed via GitHub issue
  googleapis/python-genai#1512) — the real domain is only in `web.title`.
  A pipeline must follow the redirect (or parse the title) or its citation
  database fills with Google redirect links instead of real domains.
- A real, dated regression (discuss.ai.google.dev thread 131137, starting
  ~April 2026): `groundingChunks` sometimes goes missing entirely from a
  response while search still executed, and the model reportedly
  hallucinates source URLs ~50% of the time in structured-output mode when
  this happens. Build an explicit check for empty `groundingChunks` — do
  not treat "no error" as "grounding worked."
- Free-tier grounding is model-specific: Gemini 2.5 Flash/Flash-Lite get
  500 RPD free (shared); **Gemini 3.x does NOT get free grounding at all**
  (paid-only). Pin any free-tier GEO harness to 2.5 Flash/Flash-Lite, not
  3.x, for the grounding-specific call path (non-grounded calls on 3.x
  models are separately free — see the growth-eval-quality reference file
  in this same directory for the real, live-confirmed 3.5-flash-lite
  rate limits, which are a different, non-grounding use case).

## Brave Search API — confirmed real free tier

`brave.com/search/api/` (fetched directly): $5/month free credit
auto-applied, ≈1,000 Search API calls/month. Returns raw URLs/snippets
only (no LLM synthesis) — a retrieval component, not a citation-tracking
engine by itself. Real, durable, no expiration mentioned.

## Open-source self-hosted answer engines (Perplexity-alternative architecture)

- **Perplexica** (github.com/ItzCrazyKns/Perplexica): MIT, 36.9k stars,
  4.1k forks, 1,009 commits, active. Uses SearxNG (free, self-hosted) as
  retrieval, pluggable LLMs (Anthropic/Gemini/Ollama). Citation-extraction
  code path NOT independently verified this session (a specific file path
  attempted 404'd — repo structure likely changed) — treat "does real
  citation extraction" as plausible, not confirmed, until someone reads
  the current source.
- **LibreChat** (github.com/danny-avila/LibreChat): MIT, 44.4k stars,
  5,643 commits, very active, documented web-search feature (search
  providers + scrapers + rerankers). Same caveat: citation-extraction
  mechanics not confirmed at code level.

## The recommended durable architecture (in-house, not vendor-dependent)

`ddgs` (PyPI, actively maintained, v9.16.0 as of Aug 2026, real URLs, no
LLM involved) + Brave free tier for retrieval, feeding numbered/URL-tagged
snippets to Gemini 2.5 Flash (free grounding, pinned away from 3.x) and/or
an already-paid model for synthesis, with citations constrained to IDs
from the retrieved set and validated post-hoc (never letting the model
free-text a URL it wasn't given — the standard, well-precedented
"retrieve-then-generate-with-attribution" RAG pattern, not a novel
approach). This avoids Gemini's redirect-URL and missing-chunk fragility
as a single point of failure, since ddgs/Brave URLs are real and direct.

**Explicitly unverified, flagged for follow-up**: Bing/Copilot free API
status (Azure's free F1 tier for Bing Search was reportedly retired — not
independently re-confirmed this session), You.com free tier status, and
the actual citation-extraction source code inside Perplexica/LibreChat.

## UPDATE 2026-09-19 (later same session): both real limitations fixed, not just documented

Per explicit instruction ("find fix to limitation no compromises"), both
citation-quality caveats above were fixed for real in veOS
(`monitoring_agent.py`), verified against 3 real live grounded calls
(ai.google.dev direct API, not Vertex):

1. **Redirect-URL fix**: confirmed live that attempting to follow a real
   `vertexaisearch.cloud.google.com/grounding-api-redirect/...` URL gets a
   real 403 from the destination's own CDN bot-challenge (BunnyCDN) —
   proving "just follow the redirect" is unreliable in practice, not just
   theoretically imperfect. The actual fix: `web.title` reliably held the
   real, clean domain across all 3 real calls (`schmalz.com`, `baua.de`,
   `bayern.de`) — a new `domain` field is now extracted via a real
   bare-domain-pattern check (`_looks_like_a_bare_domain`), kept separate
   from `uri` (which is retained only for a human clicking a link in a
   real browser, where redirects work fine).
2. **Missing-groundingChunks fix**: the function now explicitly logs a
   warning distinguishing "grounding may have silently failed" (the real,
   dated Google-side issue from discuss.ai.google.dev thread 131137) from
   "genuinely zero sources exist" — never silently returns an empty list
   as if that were proof of anything.

**A separate, real finding surfaced while testing this fix**: `gemini-2.5-pro`
now returns a real, live 404 ("no longer available to new users") on this
API key, despite ai.google.dev's own pricing page still listing it with a
free tier as of the same date — a real, live, unresolved discrepancy
between Google's docs and actual API behavior. Google's own suggested
replacement, `gemini-3.1-pro(-preview)`, was tested live and found to have
a **hard 0 free-tier request/token limit** — i.e., it requires real paid
billing to use at all, at any volume, which a standing "never spend real
cash" policy forbids defaulting to. `gemini-2.5-flash` is the corrected,
confirmed-working, confirmed-free default used instead. This is a real,
live-moving-target risk worth re-checking before trusting any specific
Gemini model name as "the free one" — verify by a real API call, not by
reading the pricing page alone, since the two can genuinely disagree.
