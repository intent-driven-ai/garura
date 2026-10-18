## What this lands

The decisions made so far on the Kickoff drive (#613), landed now so the memory work can start from main. Kapil chose this on 2026-10-18. Nothing is built: decision records, plans and notes only.

- **ADR 034 — inside a drive, a play answers from memory.** A play answers its own questions from memory and from what the system gives it, names where each answer came from, and asks only when nothing in memory supports an answer. It never answers from the model alone. It amends ADR 029 §2. Accepted by Kapil.
- **The memory review.** Memory is not ready for ADR 034: three copies of long-term memory that disagree, two kinds of memory that cannot answer a question, and nothing that records where an answer came from (`.garura/project/issues/613/specs/memory-review.md`).
- **The memory system, planned (draft).** Kapil's model: **Phoenix memory** is the global superset; the Garura memory in each project is the subset it pulls, and it can go up to Phoenix memory for more; short-term memory per issue. Agents read and update memory only through one command-line tool that searches the way Claude Code does, on folders now and on Griffin later. Nothing comes from the model or the web unless a person approves a memory update first. Every Garura install carries the tool and a memory guide. Its own feature, not filed yet (`.garura/project/issues/613/specs/memory-system-plan.md`).
- **Plans.** #613's plan holds the Kickoff runner at a milestone until the memory system reaches its own; #606's plan adds the memory system as step 0 of Kickoff.

**Not yet true on main:** the drive contract rule, the rules index and the glossary still carry ADR 029's old wording, and the plays still ask instead of answering from memory. That is the planned follow-up (ADR 034 "Work This Creates"; the memory plan).

Refs #613 — the issue stays open.

## Self-review

Rules: base `standards/rules/self-review.md` (no project override). Findings that stop the raise: **none**. Full review: `.garura/project/issues/613/context/self-review.md`.

**Scope**
- [PASS] Matches the planned landing: ADR 034, its pointer on ADR 029 and the index row; the #613 and #606 plans; the memory review and draft memory plan; `/adr` and play run records. No code, plays, skills or agents.
- [REVIEW] Size: 26 files, about +1,330 lines, but 91 % is plans and run records. The decision to read is ADR 034 (114 lines).
- [PASS] No stray artifacts.

**Quality**
- [PASS] No merge conflicts; no secrets; every JSON and YAML file parses.
- [PASS] ADR 034 has every section, reads Accepted, and every path it cites exists.
- [PASS] Commits are conventional, one concern each, and name #613.

**For the reviewer (non-blocking)**
- ADR 034 cites #613 plan items by the numbers they had when it was accepted. A review item was then added as item 2, so its "item 2" is now item 3 and its "item 3" is now item 4. The plan's log records the mapping; an accepted ADR is not edited.
- Three commit subjects run past 72 characters (`27d9e035`, `85c6d3fa`, `e3b10ca1`).
- The draft memory plan sits in #613's folder until its own feature is filed.
- One stale line in the #606 plan ("stops only for a new question") was fixed in this change.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
