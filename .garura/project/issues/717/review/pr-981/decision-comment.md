Harness verdict (gate off per gates.plays.check-change): approve

No blocking finding. test_plan green (17); lint-play on /list-plans PASS (0 gaps, Next-line check ran); lint-components: 37 violations, all there before, none in this change; /list-plans' check passes on the real plans. This is a recorded harness verdict, not a human review.

**Findings — {'P2': 1, 'P4': 6, 'P3': 1}**

P2:
- **Q1** (code-and-tests) The changed check logic (the new card() helper and the as_set comparison of the direction line, blank line and Status row, and the narrowed heading match) has no test. No test file in this diff or in core/ imports check_

P3:
- **H1** (harness) The Intent paragraph (line 9) still says each card shows "the plan's direction, its number and business intent", in that order. This PR moves the direction to its own line under the heading (S6 now says so, and the SKILL

P4:
- **Q2** (code-and-tests) Line 197, inside the listing() docstring, is 152 characters. The edit joined two sentences without re-wrapping, so the docstring wraps at about 100 columns on its first line and then runs far past it. Every other line in
- **Q3** (code-and-tests) The new inner function card(h, direction, status) never uses its first argument h; the caller passes a heading it does not need.
- **H2** (harness) The Context line that lists the stories the play was compiled from (line 64: #729, #806, #983) does not name #986, while SKILL.md Compiled From and the compiled_by row now cite #986. The two provenance lists disagree.
- **H3** (harness) Scenario S6 now breaks after "the check record" and leaves a short line ("*Measure:* the check record" then "reads `as_set: true`."). The author's own self-review called it cosmetic. Style only.
- **MEM-1** (memory) The example in 'The list' shows a second card (#722) that ends after the Status row. It has no Branch row, no Waits on row, and no Epic/Progress rows. The prose above it says Branch and Waits on are always shown (Waits o
- **PLAN-1** (plan-records) The comment says plan/717/base "merged into main on 2026-10-29 after #719, #983 and #986 landed". This diff adds #986 to that sentence, but the branch has not merged: PR #988, the PR under review, is the merge, and the b

**Routing:** approve → squash-merge into main (as with #981, #985); then the plan-view template promotion to Phoenix memory and the reinstall. Follow-up: a test for /list-plans' check script (Q1); /list-plans' intent sentence, story list and S6 wrap through `/edit-play` (H1–H3); the template's second example card (MEM-1); the plan tool's long docstring line and the unused argument (Q2, Q3).
