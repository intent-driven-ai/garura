Harness verdict (gate off per gates.plays.review-change): approve — round 2

Round 1's findings were judged against the fixes (`.garura/project/issues/661/review/round-2.yaml`): of 24 design findings, 7 fixed, 5 partly fixed, 6 not fixed (all P3/P4), 6 carried. The P1 is fixed:

- **F1** — `write_drive_review.py` (all three copies) now takes the memory tool's citations answer from contract v4 and v5, with a test.

Also fixed: `author-shape-bundle` no longer uses the removed router (H2); each judge gets only the per-section guidance block, cut by one shared, tested script (H3); `/intent` has its own "the run lives in its issue" rule and runs its pre-flight before Step 0 (H5, H6); the plays' ICE records `template-manager` and `judge-grounding` (H7); a drive's unanswered question is a memory update a person approves (MEM-4). Round 2's two small new findings are fixed too (N-2, N-3).

Carried on the owner's decisions: H1 / MEM-1 (eight other plays still name the old judge prompt place — they move in #663), MEM-2 (the old Rule 12 file is named only by deprecated skills), H8 (Kickoff evidence in the issue), MEM-5 (ADR 039), H10 (ADR 034/035's ICE line changes — for the owner to confirm).

Open, not blocking (`findings.yaml`): P3 — F2, F3, F4, H4, H9, MEM-3, N-1; P4 — F5, H11, H12, H13, MEM-6, N-4.

The standards scan's P2 groups are dismissed: BE-19 matched Python `from`/`join`, no import cycles (ARCH-02/CODE-14), `ruff check` passes on every changed `.py` file (CODE-03), the repo has no adopted formatter (CODE-04), and the config URL is unchanged from main (ARCH-07).

Checks: every test suite passes; `lint_play` passes on the three plays; `lint-components` gives the same findings as on main; no memory path is left in the scope.
