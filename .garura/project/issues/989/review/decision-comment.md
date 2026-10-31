Harness verdict (gate off per gates.plays.check-change): approve

Round 2. No P1. #991 is out: propose-change, merge-change and the landing script are not in the diff. Five kinds of work reviewed: start-change (harness), the scripts, the tests, the plan tool README, and the issue's run records.

What ran: every test that covers a changed script is green — the plan tool (46), start-change (12), and all 17 script-style tests in create-play/references, among them setup_branch (14 passed) and resolve_plan (27 passed). ruff is clean on the changed scripts (6 one-line-statement hits in test_setup_branch are there before). The play linter passes start-change; the component linter has nothing in changed files (37 there before). The first review's R-01, R-02, H2, H6, H7 and H10 are fixed; H1, H3, H5, H8 and H9 went with #991.

Worth fixing (not blocking):
- N1 (P2): the plan-start Done means sit in a second hand-made manifest (stop-condition-plan.yaml). The compiler writes one stop-condition.yaml with every clause, so the next /edit-play of start-change would put D5–D8 into every change start and close it HALTED.
- N4 (P3): the typed words go into a shell line (`--args="…"`); a quote, backtick or `$(…)` in a description would be cut short or run.
- N3 (P3): C10 says loops pass the issue "as today"; loop-run.md R2 does not say what it passes.
- N2 (P3): "a closed plan's branch is never cut" has no failure condition or recovery of its own.
- Q-01..Q-03 (P3): plan_branch.py's go() and abort() grew past ruff's size and complexity limits.
- N5, N6, N7 (P4): an unwritten work-description in issue mode; the close's artifact list on the plan path; closed_plan not named in Step 4.

Full list: `.garura/project/issues/989/review/findings.yaml`; round 1 is kept in `review/round-1/`.
