---
name: velth-loop
description: The bounded research/implement/verify loop for every VELTH coding task in Cowork. Encodes plan-implement-verify with iteration caps, a DIFFERENT-FAMILY external judge (maker != checker), checkpoint-and-restore against snowballing, and external-ground-truth-only stopping. Load at the start of every implementation session alongside velth-preflight, velth-test-strategy, and velth-doc-verify. This is the Claude Code team's loop, tightened for compliance-bearing output.
trigger: auto
---

# VELTH Loop Skill (plan -> implement -> verify -> stop)

## THE ONE RULE (research-grounded)

A self-improvement loop ENHANCES output only when the feedback is EXTERNAL
ground truth. A loop where the model grades its own reasoning DEGRADES output:
Huang (ICLR 2024) and Kamoi (TACL 2024) - intrinsic self-correction often fails
and can make things worse; the bottleneck is error detection, not correction.

VELTH's external ground truth = pytest + ruff + pre_commit_gate.py (L1-L4) +
velth-doc-verify (L5: deterministic checks + a SEPARATE different-family judge) +
the localhost smoke. "Done" means those are green - never Cowork's own say-so.

## THE LOOP (every non-trivial task)

```
0. PLAN (read-only)    Investigate first; do not edit. Output a numbered plan:
                       files, why, and the exact verify command that will prove it.
                       Separating research from implementation is the single biggest
                       quality lever (Anthropic Claude Code best practices).
1. CHECKPOINT          Before the first edit and before each fix iteration, snapshot
                       the target files (copy / note git ref). Lets a bad round be
                       reverted instead of compounded - guards "snowballing"
                       (arXiv 2604.06066).
2. IMPLEMENT           Surgical edits only (velth-preflight). One coherent change.
3. VERIFY (external)   In order:
                         a. uvx ruff format + check (changed files)
                         b. uv run --no-sync python scripts/pre_commit_gate.py  (L1-L4)
                         c. velth-doc-verify on the session's doc types/verticals (L5)
                         d. scripts/ui_smoke.py if a UI/export path changed
                       The VERIFIER is not the IMPLEMENTER. The judge is a DIFFERENT
                       family from Cowork's Claude (see velth-doc-verify) - same-family
                       judging is self-biased and that bias is amplified in loops
                       (Xu 2024; "Play Favorites" arXiv 2508.06709; arXiv 2509.00462).
4. LOOP or STOP        Fail -> read failure, fix, GOTO 1 (re-checkpoint). CAP 3 rounds:
                       self-repair gains saturate after ~2 rounds (arXiv 2604.10508);
                       a 4th round usually means the plan was wrong, not the code.
5. SIMPLIFY            Once green, one DRY/simplify pass (Karpathy). Re-run VERIFY.
6. REPORT IN CHAT      Load velth-truth-gate before writing this report - it is the
                       terminal check on the CLAIM, not the work, and this step is
                       exactly the moment it exists for. Emit verify output + the
                       commit command (velth-commit-prep). No auto-commit. No
                       _DELIVERY file. No .log sidecar.
```

## WHAT STAYS HUMAN (never automate past these rungs)

- COWORK NEVER COMMITS. Anshu reads the diff and runs git himself.
- SiFa reviews and signs anything compliance-bearing. The loop can reach
  "gate-green + judge-approved"; it does NOT reach "shipped". This is the answer
  to the criticism that autonomous loops ship unfixable production code.

## STOP CONDITIONS (bounded - no runaway)

- 3 fix rounds without green -> STOP, report the last failure in chat.
- Same failure twice in a row -> STOP (fix is not addressing the cause).
- Two checkpoint/restores -> STOP (snowballing; re-plan).
- Any destructive op needed (delete/overwrite/migration) -> STOP, ask Anshu.

## CONTEXT DISCIPLINE

- Read SCHEMA.md + NEXT_TASK.md at session start (input only).
- Use subagents for wide investigation; have them return a condensed summary, not
  raw file dumps (Anthropic context engineering: more tokens makes agents worse).
- Externalize state to SCHEMA.md; reset context when long.

## MANDATORY SESSION HEADER (paste atop every implementation prompt)

```
SKILLS: velth-preflight + velth-test-strategy + velth-doc-verify + velth-loop
RESEARCH MANDATE: ground every non-trivial decision in a verified paper or a read
                  reference repo; investigate read-only and output a numbered plan
                  + the exact verify command before any edit. No rabbit holes.
LOOP: plan -> checkpoint -> implement -> verify(ruff, pre_commit_gate, doc-verify,
      ui_smoke) -> loop(max 3) -> simplify -> report in chat.
VERIFY = external only. Judge = DIFFERENT family. Done == gates green, not say-so.
DIRECTIVES: surgical; NO git (Anshu commits); no speculation (read first);
            LF not CRLF; no-BOM writes; null-guard everything.
OUTPUT: report + commit command IN CHAT. No _DELIVERY files. No .log.
STOP and ask before any delete / overwrite / migration / scope change.
```

## REFERENCES

Design decisions in this skill are grounded in the following. Inline cites above
map to these entries (author-date / arXiv).

Self-correction & verification loops:
- Madaan et al. (2023). Self-Refine: Iterative Refinement with Self-Feedback. NeurIPS 2023. arXiv:2303.17651.
- Shinn et al. (2023). Reflexion: Language Agents with Verbal Reinforcement Learning. NeurIPS 2023. arXiv:2303.11366.
- Huang et al. (2024). Large Language Models Cannot Self-Correct Reasoning Yet. ICLR 2024. arXiv:2310.01798. [no external signal -> cannot reliably self-correct]
- Kamoi et al. (2024). When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey. TACL 2024. [intrinsic self-correction can DEGRADE output]
- Iterative Self-Repair in LLM Code Generation Across Model Scales (2026). arXiv:2604.10508. [pass-rate gains saturate after ~2 rounds; logical errors hardest to self-detect -> cap=3 + a non-LLM layer]
- From Hallucination to Structure Snowballing (2026). arXiv:2604.06066. [reflection can snowball errors; detection is the bottleneck, citing Tyen et al. 2024 -> checkpoint/restore]

LLM-as-judge self-preference & family bias (why a different-family judge):
- Zheng et al. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. NeurIPS 2023. arXiv:2306.05685. [~80% human agreement; position/verbosity/self-enhancement bias]
- Wataoka et al. (2024). Self-Preference Bias in LLM-as-a-Judge. arXiv:2410.21819.
- Xu et al. (2024). Pride and Prejudice: LLM Amplifies Self-Bias in Self-Refinement. ACL 2024. [self-bias widespread; AMPLIFIED in self-refinement]
- Panickssery et al. (2024). LLM Evaluators Recognize and Favor Their Own Generations. NeurIPS 2024. arXiv:2404.13076.
- Play Favorites: A Statistical Method to Measure Self-Bias in LLM-as-a-Judge (2025). arXiv:2508.06709. [Claude 3.5 Sonnet / GPT-4o self- and same-family bias]
- AI Self-preferencing in Algorithmic Hiring (2025). arXiv:2509.00462. [reviews self-preference; amplified in self-refinement pipelines]

Engineering practice (NOT peer-reviewed - workflow shape, not load-bearing claims):
- Anthropic. Building Effective Agents (2024); Effective context engineering for AI agents; How we built our multi-agent research system; Claude Code best practices (code.claude.com/docs).
- Cherny, B. Claude Code workflow thread (X, Jan 2026). [verification loop 2-3x quality; plan mode; one git checkout per parallel session]
- Adaline (2026), LLM-as-a-Judge reliability & bias [secondary synthesis of the above].

VELTH-specific checks, gates, entrypoints, and German class invariants are grounded
in the repo and in velth-preflight / velth-test-strategy - codebase facts, not papers.
