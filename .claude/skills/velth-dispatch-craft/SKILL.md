---
name: velth-dispatch-craft
description: How to WRITE a Cowork dispatch — the prose and structure, not the workflow (velth-spec) or the topology (velth-graph-engineering). Load before writing any dispatch of meaningful size. Encodes real, hard-won lessons across the full working relationship (not just one session) — communication taste, what makes Cowork succeed vs fail on different prompt shapes, and verified research including a corrected reading of the MAST paper.
sources: [chat]
---

# Writing a VELTH dispatch — craft, not just content

Governing principle, Anshu's own words: no compromise, only improvement. Every rule below is
about ROUTING density correctly, never about reducing it.

Standing priority order, stated once, never reordered: **data integrity > correctness >
completeness > speed.**

---

## What actually works, ranked above taste — staleness is the field's own documented failure mode

Anshu's own explicit correction, worth stating first: preferences matter, but what has actually
worked for Cowork, what real research shows, and current industry practice for Claude Code and
agentic coding generally outrank personal taste when the two would conflict. This section is
that evidence, not VELTH anecdote dressed up as research.

**The single most load-bearing finding: a stale context/skill file can make an agent perform
WORSE than having no file at all.** A real study evaluating AGENTS.md-class files found they
can reduce task success rates versus no context, while increasing inference cost 20%+ — not
because context files are a bad idea, but because outdated instructions, contradictory rules,
and stale architecture descriptions actively mislead an agent that trusts them. This is not a
hypothetical: `velth-preflight` carried a Python version two majors stale and a hardcoded
`origin/main` RADAR check when the real shared branch had been `mig/repo-migration` for weeks;
`velth-test-strategy` carried baseline test counts (3831) against a real repo state of 9633.
Both were found and fixed this session — but the field's own research says this is the DEFAULT
trajectory of every context file, not a VELTH-specific lapse. **Treat every skill's factual
claims (versions, branch names, baseline counts, table schemas) as provisionally stale until
re-verified in the current session — the research says this is the correct default posture,
not excessive caution.**

**Format research, 9,649 experiments across 11 models comparing YAML/Markdown/JSON/TOML:**
structured formats consistently outperform unstructured prose, but format matters LESS than
content quality. Markdown (what every VELTH skill already uses) is a validated choice, not an
arbitrary one.

**The bullets-vs-prose question, resolved by research rather than preference:** *"Use bullet
lists for rules — direct, scannable, unambiguous. Use brief prose when you need to explain the
WHY behind a convention, because rationale genuinely helps agents apply rules correctly in edge
cases."* This validates, rather than merely states, Anshu's stated preference for bullets — and
it's also exactly this skill's own existing shape: a bulleted rule followed by the real incident
that produced it. That's not a compromise between taste and rigor; the research says that
specific combination is what performs best.

**A concrete, adoptable practice from this same research, not yet standard in VELTH's skills:**
maintained context files carry lightweight metadata — last-reviewed date, owner — specifically
because it lets an agent (or a human) judge whether a file is worth trusting before reading it
in depth, and prevents silent rot. Worth adopting on skills going forward: a `reviewed:
YYYY-MM-DD` line in frontmatter, updated whenever a fact-bearing edit lands, so staleness is
visible at the listing level, not only discoverable by reading the body.

**Anthropic's own real-usage research** (~400,000 Claude Code sessions, Oct 2025–Apr 2026):
*"people make most of the planning decisions... Claude makes most of the execution decisions.
The greater domain expertise a person brings to a session, the more work Claude does per
instruction."* Directly relevant to dispatch-writing: the more precisely a dispatch's PLANNING
is specified (which is Anshu's role per this same research), the more can legitimately be
delegated to Cowork's EXECUTION in one pass — this is why dispatches have grown more
comprehensive over time without that being scope creep; it's the correct response to
established trust, per the same research that describes the general pattern.

---

## Communication taste — established across many sessions, not inferred from one

- **Zero fluff.** No "Sure, I can help with that," no "Here is the code," no preamble, no
  recap of his own question back to him. Lead with the answer or the code.
- **Code first, explanation second.** Show the diff or command, then a tight rationale.
- **Bullets over paragraphs** for anything procedural.
- **Inline comments explain WHY a non-obvious choice was made, never WHAT the syntax does.**
- **He writes brief, fragmented messages, often with typos, in ALL CAPS under pressure.**
  Parse intent accurately. Do not ask for clarification on garbled phrasing when the intent is
  inferable — proceed, state the interpretation briefly, keep moving.
- **Proactive issue detection beyond what's explicitly asked is expected, not optional.**
  Established standard: a "find all issues even when not in the prompt" testing philosophy
  applied to code — the same posture applies to dispatches and reports. Surfacing something
  real that wasn't asked about is not scope creep; missing it silently is the actual failure.

### The chat-vs-file rule — a direct, explicit standing instruction

Verbatim, on record: *"i hate getting separated files include log, md whatever in chat itself,
if anything needs to be on git do it, i will commit but my work every output should be in
chat."* Codified at the time as permanent: reports, logs, commit commands, and summaries MUST
be returned IN the chat response. Only code destined for git goes to the repo working tree.

**How this reconciles with writing investigation plans to disk (a real, live practice):**
it doesn't relax the rule, it narrows the exception. Writing a genuine, persistent, git-worthy
artifact — a design doc future sessions or teammates will reference — to disk is fine, but
NEVER as a substitute for having the content in chat. The full content still goes in chat,
every time, not "see the attached file." File-writing is the addition, never the alternative.
Default to chat-only; write to disk only when the content is genuinely meant to outlive this
one exchange as a repo artifact, and say so explicitly when you do.

---

## Token cost vs. context window — the distinction that matters most

Real finding: these got conflated in a live dispatch and cost real quality — subagent reports
got compressed out of chat citing "context," which was actually a decision made under a
physical constraint, not a financial one.

- **Token cost is money.** Cheap. Never shapes output — never compress a caveat, thin a
  citation, or skip a verification pass to save it.
- **Context window is physical.** A hard limit inside one session, not purchasable. THIS is
  the actual resource dispatch-writing manages.

The discipline is routing, not rationing:
- **Heavy reading → a subagent.** Any survey touching more than ~4-5 files. It burns its own
  context, reports back a summary. Real result: two subagents burned ~190k tokens between them
  and returned ~2k of findings each — the correct trade whenever a task needs more than a few
  files read.
- **Bulk output → the chat-vs-file rule above governs this**, not context alone. Even a large
  report goes in chat; a file is an addition when it's a genuine persistent artifact.
- **Main-session context → reserved for what can't be delegated.** Cross-question reasoning,
  contradiction-spotting between subagent reports, synthesis. That's the scarce resource.

**One line prevents the collision that happened tonight, when using subagents:**
*"Subagent reports get pasted in full in chat as their own section; the main session adds
synthesis on top, it does not replace them."* Without it, a dispatch can ask for full verbatim
output AND a full synthesis AND a meta-report in one turn — more than one window holds — and
something gets silently thinned.

---

## Mechanical checks over judgment checks, wherever a mechanical form exists

Real result: `cowork-sandbox-safety`'s hash-mismatch detection and `test-strategy` Pattern 9
("read fresh, never infer a field name from purpose") fired perfectly — zero judgment
required, a clean yes/no. `truth-gate`'s Q5 ("what did I not do") is a judgment scan, and
judgment self-reports "yes I read the inputs" even when it read half of them. Confirmed by
research this session (arXiv 2606.09863): a cheap mechanical check catches what
self-assessment misses, 4-8x more reliably than an LLM judge, at far lower cost.

When writing a dispatch: wherever a requirement CAN be phrased as an enumerable list with
marks — a manifest, a table, an explicit count — phrase it that way. "Did you read the
inputs" is judgment. "List every attachment by filename with a read/not-read mark, before
writing anything else" is mechanical. The second form is what actually catches the miss.

---

## The read-manifest requirement — standing, not optional

Real incident: a dispatch quoted three lines from a source PDF, verbatim and correct — the
agent checked, they matched character-for-character. The quotes were so accurate that having
them FELT like having the source. That's exactly what let two required attachments go unread
for a full pass, one of which held the answer to the single question the resulting plan had
flagged as blocking. **A precise quote is a checksum for the specific line it covers, not
evidence the surrounding document was read.**

Every dispatch citing more than one source document requires an explicit manifest as its own
first step: every attachment, named, marked EXECUTED / READ / NOT READ, before any synthesis
begins.

---

## Never assert a convention — confirm it

Real catch: a dispatch specified a docs subdirectory that didn't exist; the executing agent
found the real flat-file convention instead of inventing one, then used it and reported the
deviation. Generalize this to every path, field name, table name, and naming convention a
dispatch asks an agent to touch. Never state a convention as settled fact unless verified
fresh this session — phrase it as "the expected convention, confirm before use" instead, and
require the deviation to be reported, not silently corrected.

---

## Precise-language quoting — a real technique, used correctly

Verbatim domain-language quotes (German, in VELTH's case) alongside precise English
instructions is a deliberate, validated split: instructions need to be unambiguous to an
agent; domain facts need to be matchable against a source character-for-character. Keep using
it. Always pair it with the read-manifest rule above — a good quote is precisely what makes
skipping the rest of the source feel safe.

---

## Skill triage — APPLIES / CONDITIONAL / DOES NOT APPLY, every time, with reasons

Classify every skill in the catalog before writing the dispatch body, not only the ones that
obviously fit — and name WHY a skill doesn't apply, not just omit it. This has real precedent
predating tonight: an earlier session built the identical table (skill / applies-to-this-task /
why) for a repo-migration batch, catching that a skill's own baseline numbers (`3831` tests,
a named smoke script) were stale against the real current repo state (`9633`, no such script) —
confirming this discipline catches drift, not just relevance. Standard for any dispatch of
meaningful size.

**The counter-caution, also real and also worth holding:** "load everything and research" is
not automatically safe just because it sounds thorough. An earlier session flagged this
directly — unbounded scope is itself a MAST-style failure mode (see below); research should
fill genuine gaps in *how* to do the task safely, not become license to re-litigate settled
decisions. Triage with reasons is what keeps loading-everything from becoming loading-on-vibes.

---

## Subagent delegation and topology — the MAST paper, read correctly

Per Anthropic's own primary-source guidance (`code.claude.com/docs/en/best-practices`):
*"Subagents run in separate context windows and report back summaries"* — the documented fix
for *"the infinite exploration... reads hundreds of files, filling the context."* Delegate any
survey touching more than ~4-5 files, or any question independent enough not to need the main
session's accumulated reasoning. Don't delegate cross-question synthesis.

**The MAST paper (Cemri et al., arXiv:2503.13657v3, "Why Do Multi-Agent LLM Systems Fail?"),
verified against the actual paper, not a prior summary of it** — get this one right, a
mischaracterization of it was caught and corrected once already:

- Real, measured failure rate across 7 SOTA multi-agent systems: 41-86.7%. Category
  prevalence over the full MAST-Data corpus (Figure 1, n=1,642 traces — the paper's
  headline breakdown): System Design 44.2%, Inter-Agent Misalignment 32.3%, Task
  Verification 23.5%. **This corrects a second, still-wrong version of the same
  citation that survived in this exact file** (41.8/36.9/21.3 is real too, but is
  Figure 4's smaller 210-trace subsample, not the headline number) **immediately
  after the paragraph below that already warned against exactly this kind of
  error — re-verified against the full paper text 2026-08-26 rather than trusted
  a second time.** There is no authors'-own "~79%" combined figure: the paper's
  own Appendix E correlation matrix (FC1↔FC2 r=0.32, FC1↔FC3 r=0.17, FC2↔FC3
  r=0.28) shows the categories are not mutually exclusive per trace, so summing
  two category percentages overcounts and was never something the authors did
  themselves.
- Concrete structural wins: +15.6% task success from adding a high-level objective
  verification step; +9.4% from enforcing role hierarchy so one agent has final say.
- **What the paper does NOT say: that topology always beats prompting.** In its own AG2/
  MathChat case study, a topology change was NOT statistically significant on GPT-4 (p=0.4)
  while an improved prompt WAS significant; on GPT-4o, both were significant. The paper's
  actual, harder conclusion: isolated tactical fixes — prompt OR topology alone — are
  inconsistent across models; reliability needs structural redesign, not either fix alone.
- Practical rule for dispatches: don't write "be careful about X" when a structural removal
  is available — a stop condition that removes a dangerous edge from the graph entirely
  (real example: "no edge from RECON to BUILD exists in this graph — that transition belongs
  to Anshu alone") is more reliable than an instruction asking for caution. But don't treat
  structural fixes as a silver bullet either — verify statistics carefully before citing this
  or any paper; category-level and trace-level percentages in MAST use different denominators
  and do not sum.

---

## Standing mandatory dispatch elements (Karpathy rules + header structure)

Karpathy coding rules, permanent, applied to all VELTH work: **Think Before Coding, Simplicity
First, Surgical Changes, Goal-Driven Execution.**

A complete dispatch header, established as the minimum bar — missing any element makes the
dispatch incomplete: **SKILLS** (triaged, with reasons) + **RESEARCH MANDATE** (real papers,
verified, cited) + environment/tooling **DIRECTIVES** specific to the task + **KARPATHY**
(the four rules above) + standing **RULES** (no git from Cowork, read before writing, STOP
conditions stated explicitly, never self-approve).

Additional real, evolved conventions worth including where relevant: declare the report
format up front (e.g. "table" vs "prose") rather than leaving it implicit; pre-declare known
facts so an agent doesn't waste a read confirming something already established; batch
independent reads before dependent ones; use short task-ID breadcrumbs when a dispatch spans
multiple named pieces of work, so a later reference is unambiguous.

---

## What this skill does not cover

The workflow (explore → plan → confirm → build) is `velth-spec`. The topology (node
structure, checkpoints, forbidden edges, blast radius) is `velth-graph-engineering`. Reporting
discipline once work is done is `velth-truth-gate`. This skill is the prose, structure, and
communication register of the dispatch itself — what to name, quote, delegate, classify, route
where, and how to say it, before any of those other skills' disciplines even engage.
