---
name: deep-cross-domain-research
description: When a research task asks for coverage across multiple countries, languages, or fields - go genuinely deep on every single one named, not a token citation per item. Use before dispatching or accepting cross-domain/cross-country research, and before reporting such research as complete.
---

# Deep Cross-Domain, Cross-Country Research

Distilled from a real failure: a research dispatch asked for depth across
Germany, UK, USA, China, Japan, Korea, and India. It delivered real depth
for three, one usable finding for China, and near-nothing for the rest —
and got reported as complete without anyone checking it against the
original ask. This skill exists to stop that from happening again.

## Why a token citation per domain doesn't work

Not a vibe — there's a mechanism. **Gentner's structure-mapping theory**
(Dedre Gentner, "Structure-Mapping: A Theoretical Framework for Analogy,"
*Cognitive Science* 7(2), 1983) holds that analogical transfer works by
mapping *systems of relations* between domains, not isolated surface
features — the "systematicity principle." One citation captures a surface
feature. It does not capture the relational structure of how a problem
was actually solved elsewhere, which is the only part that transfers into
a genuinely new approach. A citation list with one paper per requested
country reads as complete and is not.

**TRIZ** (Genrich Altshuller, built from analyzing 400,000+ patents
starting 1946) is the industrial proof this works at scale: it exists
because deep, systematic cross-domain pattern-mining produces reusable
inventive principles that a single-field search cannot. That's what "go
deep across domains" is actually for — not compliance with an instruction,
but access to solution patterns your own field hasn't found yet.

## Why English-only / Anglophone-only search fails silently

This is a **formally named, actively-studied bias**, not an invented
concern: "language bias in systematic reviews." A 2016 audit found 38% of
sampled systematic reviews explicitly restricted to English-language
sources; the methodology literature treats this as a known, correctable
problem, not a fringe worry. The documented cause is structural — time and
translation resources, not principle — which means it happens by default
unless deliberately corrected.

The named mitigation is **Multivocal Literature Review** (Garousi,
Felderer, Mäntylä — arXiv:1707.02553): include grey literature — blog
posts, practitioner writeups, engineering postmortems, forum discussion —
alongside formal papers, and do it in the target language/region's own
venues, not just what surfaces in an English-language search. A standard
literature-review search process is explicitly insufficient for this;
MLR requires its own search and source-quality process.

This isn't only literature-review theory — it's already independently
established, working practice on a different project: "search in German
for anything DACH-regulatory; the English coverage of DGUV/BG/ArbSchG
topics is thin and often wrong on specifics." Same mechanism, same fix,
arrived at separately from real regulatory research rather than from the
academic bias literature. When both an academic methodology and an
unrelated team's hands-on practice converge on the same rule, that's
stronger grounding than either alone.

## What to actually do

1. **Before dispatching**, name every country/domain in the request
   explicitly in the research brief, not just as a general "go global"
   instruction. Vague scope produces vague coverage.
2. **For each one, require primary sources in that region's own venues**
   where possible — not just what an English search surfaces. For a
   technical domain, that can mean CCF-ranked conference papers, regional
   engineering blogs, or practitioner writeups in the local language,
   summarized rather than skipped because they're not in English.
3. **After the research returns, self-audit it against the original list**
   before reporting it as done. Literally check off each named item: did
   this one get a real finding that changed a decision, or a citation that
   exists only to look complete? If it's the latter, that domain did not
   get researched — say so, and either re-run it or report the gap
   honestly. Do not let a report that names every requested item pass as
   "done" without checking whether each mention carries real weight.
4. **Look outside the obvious fields too.** Don't limit "cross-domain" to
   variations within tech/math/medicine/physics. The domain that solved
   your structural problem first might be logistics, library science,
   supply-chain, agriculture, or something with no obvious connection —
   the transfer is about the shape of the problem, not the subject label.
5. **When reporting research to someone**, state explicitly which named
   items got real depth and which didn't, in the same message — don't
   wait to be asked three times.

## When the search comes back empty — that's the invention trigger, not the end

A real, thorough cross-domain pass sometimes finds nothing (a 103-agent,
fully-verified pass on "how do organizations deliver one truth as many
personalized deliveries without drift" came back with every single claim
refuted or unrepresented — a genuine, confirmed gap, not a thin search).
Per the standing project rule (`cross_domain_first_principles_invention`
memory), a confirmed empty result is the trigger to INVENT a mechanism by
combining domains, not a dead end to report and stop at:

- The domain/country list in any research brief (§1 above) is a starting
  point, never an allow-list. Search wider than what was named when the
  first pass comes up empty — the closest-fitting real mechanism may sit in
  a field or country nobody thought to name (mathematics — graph theory,
  information theory, statistics, optimization — is worth checking on
  every pass, not just when AI/tech precedent runs dry).
- Combine 2-3 domains deliberately rather than settling for "no precedent
  exists" as the final answer: an established pattern from one field as the
  structural base with AI/tech as the addition on top, or the reverse.
- Any resulting design is INVENTED, not precedent-backed — say so
  explicitly when reporting it, and route it through `research-simulate-
  encode`'s invention gate (simulate at actual required scale, adversarial
  stress test, real-scenario check) before it's trusted, never presented as
  verified industry practice.
