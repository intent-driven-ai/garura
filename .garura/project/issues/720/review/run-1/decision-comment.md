Harness verdict (gate off per gates.plays.check-change): reject

Reason: 1 P1 (blocker) finding(s). Counts: P1 1, P2 18, P3 38, P4 16.

Blocking:
- QS-01 (core/tools/plan/test_plan_branch.py:43): email — basis: standard DATA-18 (DATA-18)

The P2 findings to fix before re-raising:
- QS-02 (executable-code/tests/docs (scan), core/tools/plan/plan_branch.py): core/tools/plan/plan_branch.py
- QS-03 (executable-code/tests/docs (scan), core/tools/plan/plan_branch.py): core/tools/plan/plan_branch.py
- QS-04 (executable-code/tests/docs (scan), core/tools/plan/plan_branch.py): core/tools/plan/plan_branch.py
- QS-05 (executable-code/tests/docs (scan), core/tools/plan/plan_branch.py): core/tools/plan/plan_branch.py
- QS-06 (executable-code/tests/docs (scan), core/tools/plan/plan_branch.py): fetch
- QS-07 (executable-code/tests/docs (scan), core/tools/plan/plan_branch.py): fetch
- QS-08 (executable-code/tests/docs (scan), core/tools/plan/test_plan_branch.py): core/tools/plan/test_plan_branch.py
- QS-09 (executable-code/tests/docs (scan), core/tools/plan/test_plan_branch.py): core/tools/plan/test_plan_branch.py
- QS-10 (executable-code/tests/docs (scan), core/tools/plan/test_plan_branch.py): core/tools/plan/test_plan_branch.py
- QS-11 (executable-code/tests/docs (scan), core/tools/plan/test_plan_branch.py): core/tools/plan/test_plan_branch.py
- QS-12 (executable-code/tests/docs (scan), core/tools/plan/test_plan_branch.py): email
- QR-01 (executable-code (data-safety read), core/tools/plan/plan_branch.py): The "uncommitted work" check skips every file under --ignore (the issue's short-term folder), including files already staged. The cut then runs `git commit -m` with no path limit, so a staged file und
- QR-02 (executable-code (data-safety read), core/tools/plan/plan_branch.py): The cut is not all-or-nothing. After `git commit` on main, a rejected `git push main` raises Stop. The Stop record has main_commit null and back_to null, so `abort` has no commit to revert and `back` 
- QR-03 (executable-code (data-safety read), core/components/plays/update-plan/scripts/commit_plan.py): The docstring says it "stages only the plan file, the model files ... and the changed files in the plan's own short-term folder". But the commit is `git commit -m` with no pathspec, and the "nothing s
- QR-04 (executable-code (data-safety read), core/components/skills/track-plan-changes/scripts/track_changes.py): The docstring says a rerun "never makes an issue twice". That holds only when the record file is written after the create. Two gaps: (1) tracker.HostTracker.create raises TrackerError when create-issu
- HF-1 (harness, .garura/project/issues/720/review/pr.diff (core/tools/plan/plan_branch.py, called from core/components/plays/update-plan/SKILL.md Step 3)): /update-plan's first session on a plan with no branch writes straight to main (a commit and a push) and becomes a second creator of plan/<id>/base, beside start-change. The branch step is declared in 
- HF-2 (harness, core/components/agents/product-os-keeper.md): Only the capability comes from a skill (find-work-placement). The slice choice (read the spine, pick the slice whose intents hold the plan's intent), the new id fn-<slug>, the one_line and the five-pa
- MEM-1 (memory, core/components/memory/standards/schemas/product-os/ontology.md): The Plan kind now makes /update-plan cut the plan's branch and set main's plan file to In Progress; the committed branch rules and ADR 060 say the opposite, and no committed record covers the change

Next: fix the cited findings on this branch and re-raise; the review runs again.
