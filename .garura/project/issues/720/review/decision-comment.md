Harness verdict (gate off per gates.plays.check-change): reject

Round 3. Reason: 1 P1 (blocker) finding(s). Counts: P1 1, P2 15, P3 50, P4 25.

Blocking:
- QS-01 (core/tools/plan/test_plan_branch.py:43): the word in a test repo's throwaway git identity — basis: standard DATA-18 (DATA-18). The scanner's own notes record it as a false positive.

Fixed since round 2:
- HF-1 and MEM-1: ADR 061 (accepted) records that a plan's branch is cut by the play that starts its work, main first; ADR 060 points to it.
- HF-2: a new feature is placed by a script (place_feature.py) and the placement skill; the model sub-agent drafts nothing itself.
- HF-8, and the absolute paths in the linter report (lint-components now reports paths relative to where it ran).

No design P2 stands. The 15 scanner P2 rows are path-only matches, each answered in code-evidence.md (ruff format, the import trace, node --check) or a false positive. What stands is P3 and P4 only.

Next: the product owner decides at merge-change's pinned approval.
