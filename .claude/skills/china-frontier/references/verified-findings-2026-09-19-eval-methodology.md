# Verified findings: Chinese AI companies' output-quality evaluation methodology (2026-09-19)

Real research dispatched for VELTH/veOS's growth-specialist eval harness
design. All DeepSeek claims independently verified (arXiv HTML fetched and
parsed directly; GitHub facts checked via `api.github.com`, not a page
summary). Alibaba/Baidu/ByteDance findings came from three dedicated
background research agents, each fetching primary sources directly.

## DeepSeek — the strongest, most transferable finding

**DeepSeek-R1 (arXiv:2501.12948) Appendix D.3, "DeepSeek-R1 Safety Report"**
is the single most relevant artifact found across all four companies
researched: a formally published, dedicated pre-ship safety/red-team
report with a named taxonomy (4 categories, 28 subcategories), external
benchmark citations (HarmBench, Mazeika et al. 2024), a documented
production Risk Control System, and multilingual jailbreak testing across
50 languages. **No equivalent was found for Alibaba, Baidu, or ByteDance**
- each was explicitly checked and confirmed absent, not just unsearched.

**Appendix G.2, "Unsuccessful Attempts"** - DeepSeek publishes its own
negative results: Process Reward Model (PRM) abandoned because "once a
model-based PRM is introduced, it inevitably leads to reward hacking";
Monte Carlo Tree Search abandoned because "training a fine-grained value
model is inherently difficult." A real, citable instance of a frontier lab
disclosing failed methodology, not just successes.

**DeepSeek-V3 (arXiv:2412.19437) Section 5.4.2** explicitly names its own
precedent rather than inventing a distinct "Chinese constitutional AI":
*"we employ the constitutional AI approach (Bai et al., 2022)"* - directly
citing Anthropic's own paper. Useful fact for any future claim about
"Chinese self-rewarding/constitutional-AI equivalents" - the real answer is
DeepSeek reuses and cites the Western framework, not a parallel invention.

**deepseek-ai/deepseek-harness**: real, current (created 2026-08-13),
verified via the GitHub API (229,574 stars, 27,468 forks as of 2026-09-19
- an initial WebFetch summary undersold this repo; always cross-check a
page summary against the API for star/fork/activity claims). An open-source
coding-agent harness, NOT a chat/answer-quality product - its
`docs/postmortem/` numbered incident reports and "don't trust green status,
verify real state" philosophy is philosophically identical to this
project's own standing rule, but it answers "how does DeepSeek verify
agentic task completion," not "how does DeepSeek grade an end-user
answer's quality" - don't conflate the two when citing this repo.

## Alibaba / Baidu / ByteDance — real but genuinely thinner

- **Alibaba's WebDetective** (arXiv:2510.05137): a real, formal
  claim-level grounding check (LLM verification that a claim is entailed
  by its cited source) plus named anti-gaming metrics (Good Refusal F1,
  Knowledge Utilization F1) - the single most GEO-relevant artifact from
  any of the three. No confirmation it's wired into Quark's own shipped
  product as a gate, though.
- **A secondhand claim about a Qwen "reflection and traceability,
  forward/reverse mode" hallucination-detection mechanism was checked
  against the actual Alibaba Cloud doc, found ABSENT from it, and traced
  to unofficial community blog posts instead.** This was correctly
  retracted by the researching agent rather than reported as a real
  Alibaba claim - a live example of exactly the self-correction discipline
  this skill and `ai-output-self-audit` require. Do not cite a "Qwen
  reflection/traceability" mechanism without re-verifying against Alibaba's
  own primary documentation first.
- **Baidu's ERNIE 4.5 technical report** (ernie.baidu.com, NOTE: the older
  yiyan.baidu.com URL for this doc is now dead) mentions "safety" exactly
  once across a 4,735-line report, with no protocol, benchmark, or
  taxonomy - confirmed genuinely thin, not an under-search.
- **ByteDance's Seed1.5-Thinking** (arXiv:2504.13914) has a real two-tier
  verifier (Seed-Verifier 82.7% accuracy, Seed-Thinking-Verifier 99.3% on
  a 456-case test set) but candidly states there is no systematic
  red-teaming protocol, only "manual inspection of rewards did not reveal
  substantial signs of reward hacking" - a post-hoc spot check, not a
  designed adversarial process.
- **AlignBench** (arXiv:2311.18743, Tsinghua/THUDM - academic, not
  company-authored) is confirmed adopted by DeepSeek, Qwen, ChatGLM, Yi,
  Baichuan, and Abab for Chinese-language alignment evaluation - a real,
  shared external standard underneath multiple companies' own pipelines.

## What this does NOT establish

GEO/AI-search-answer-quality methodology at the PRODUCTION-GATE level
(as opposed to the research-paper level) is confirmed genuinely thin or
absent for Quark, Doubao's own search feature, and ERNIE's search
integration specifically - Chinese-language search consistently surfaced
consumer product journalism rather than engineering disclosure for this
specific question, across all three non-DeepSeek companies, checked in
both English and native-language framing.
