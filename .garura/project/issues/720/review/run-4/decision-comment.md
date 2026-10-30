Harness verdict (gate off per gates.plays.check-change): reject

Round 4. Reason: 1 P1 (blocker) finding(s). Counts: P1 1, P2 23, P3 68, P4 44.

Blocking:
- QS-01 (core/tools/plan/test_plan_branch.py:43): the word in a test repo's throwaway git identity — basis: standard DATA-18 (DATA-18). The scanner's own notes record it as a false positive.

Fixed since round 3: every reviewed P3 — harness HF-3 to HF-7 and HF-10 (ADR 062, the guard, session_files.py, verify.json, the asking rule, the in-progress slice), memory MEM-2 to MEM-4 (the Thin line, plan status, the feature item), and the three code P3s (abort after a refused delete, the marked-issue search test, placement questions on a rerun).

Reviewed findings that stand: one new P3, HF-12 (the Step 8 and Step 9 model dispatches write one model record with no add-or-replace rule, and that record is the guard's allow list), and P4s only otherwise. The scan's P2 and P3 rows are path-only or catch-all rows (lint, format, cycle, git fetch), answered by runnable-checks.txt (ruff, node --check, 34 suites green).

Next: HF-12 is fixed in the next round, then the product owner decides at merge-change's pinned approval.
