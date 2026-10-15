**Harness verdict (gate off per gates.plays.review-change): approve**

No blocking (P1) findings. 6 in all. 5 are fixed in this PR; 1 is older and tracked elsewhere.

- **P3** — the post never checked the comment against the recorded decision. Fixed: `post_verdict.py` now posts nothing unless the comment's first line names the recorded decision and decider.
- **P3** — Step 5 never named the decision record's shape, which Step 6 now insists on. Fixed: the intent (C9) and Steps 5 and 6 name it: `decision: approve | reject`, `decided_by: harness | human`.
- **P3** — D2's sentence promised more than the check proved. Fixed by the first item: `decision_recorded` is written only after both checks pass.
- **P4** — the test left three files open. Fixed.
- **P4** — fix-bug used one name for the test and for its record. Fixed: Step 3 says which is which.
- **P4** — review-change still lacks the "no unbacked recommendation" wiring. This was already on main and is tracked by #530. It does not count against this PR.

Checks run: `ruff` is clean. `test_post_verdict.py` passes 31 of 31. All 7 play-creator reference suites pass. `lint_play` passes on fix-bug. On review-change, `lint_play` shows only the #530 gap.

This review run uses the new stop condition. No file was made by hand.

Refs #536
