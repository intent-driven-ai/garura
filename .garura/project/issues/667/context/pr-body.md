## What this delivers

**ADR 036** — `docs/adr/036-approved-answer-lands-in-short-term-memory.md`, accepted by Kapil on 18 October ("accept and update plan. pdate items and story 664. pdate adr"). It writes down his answers to the PR #666 review, so ADR 035 and the merged memory tool contract say the same thing:

1. Short-term memory is the current issue only. Garura and Phoenix memory are read in full by every issue. The lookup order stays short-term → Garura → Phoenix; research only after all three have nothing.
2. A researched answer, approved by a person, lands in the issue's short-term memory.
3. Promotion to Garura or Phoenix memory happens outside the work, as its own approved update.
4. A person's own answer to a question goes into Garura memory.
5. Learned checkpoint answers are not memory.
6. A play's own working files stay direct.
7. Memory and ADRs are reviewed in the review tool's third section, **Memory and ADRs**, on the Catch up cards (#644). Typing stays until that section exists.

It amends ADR 035 (§1, §5, §7, "Not decided here"), ADR 034 (§2) and ADR 032 (§3). Each older ADR changes only on its Status line, and the index is rebuilt.

**Plans and stories, on Kapil's word:**
- `.garura/project/issues/653/specs/plan.md` — item 1 names ADR 036; item 5 writes the approved answer to the issue's short-term memory, with promotion as its own update; item 11 points to ADR 036 §7; "Where we are now" and the review lines are current.
- `.garura/project/issues/617/specs/review-tool.md` — §4 has three sections: Intents, Product, Memory and ADRs.
- GitHub stories rewritten to follow ADR 036 ("fix story.. is important. as GH issues are the mechanic that will execute the agents work"): #664 (new title and text), #658, #657, #660, #661, #663. #658 and #657 also carry the PR #666 review findings left to them: proving a person gave the word (TIC-2); the `../` refusal (TIC-7) and lookups without an issue for Garura and Phoenix memory (TIC-3). The local mirror is `.garura/project/issues/654/specs/stories.yaml`.

Closes #667

## Self-review

Rules: base `standards/rules/self-review.md` (no project override). Findings that stop the raise: **none** (0 blocking, 9 non-blocking). Full review: `.garura/project/issues/667/context/self-review.md`.

- All six of Kapil's quotes in ADR 036 match the brief word for word; all ten paths it names exist; ADR lint passes; a fresh index rebuild is identical; the #653 plan check passes.
- ADR 032, 034 and 035 differ from main only on their Status line.
- **Fixed after the self-review:** story #658's stale text (and #657, #660, #661, #663); #664's old title in `filed-stories.json`; the review tool plan's two-section wording; three stale lines in the #653 plan. The self-review file predates commit 2c3fcdcb.

**For the reviewer (non-blocking, carried):**
- The glossary, `docs/components/memory.md`, `README.md` and `docs/philosophy/architecture.md` still describe the old memory layout. That predates ADR 036; story #663 is its home.
- The older ADR bodies keep their old words on purpose; their Status lines point forward.
- Two points stay open in ADR 036 and are written into story #664: where a product decision waiting for a person is reviewed, and who writes the approval on a swipe.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
