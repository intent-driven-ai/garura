Harness verdict (gate off per gates.plays.check-change): reject

Round 2. Reason: 1 P1 (blocker) finding(s). Counts: P1 1, P2 18, P3 49, P4 22.

Blocking:
- QS-01 (core/tools/plan/test_plan_branch.py:43): the word in a test repo's throwaway git identity — basis: standard DATA-18 (DATA-18). The scanner's own notes record it as a false positive.

Fixed since round 1: the four data-safety P2 findings (plan_branch.py staged files and failed push; commit_plan.py scope; track_changes.py a second issue on rerun) and three smaller ones, each with tests.

Design P2 findings that stand:
- HF-1 (harness, .garura/project/issues/720/review/pr.diff (core/tools/plan/plan_branch.py, called from core/components/plays/update-plan/SKILL.md Step 3)): /update-plan's first session on a plan with no branch writes straight to main (a commit and a push) and becomes a second creator of plan/<id>/base, beside start-change. The branch step is declared in the play's own ICE (
- HF-2 (harness, core/components/agents/product-os-keeper.md): Only the capability comes from a skill (find-work-placement). The slice choice (read the spine, pick the slice whose intents hold the plan's intent), the new id fn-<slug>, the one_line and the five-part ice (goal, limit,
- MEM-1 (memory, core/components/memory/standards/schemas/product-os/ontology.md): The Plan kind now makes /update-plan cut the plan's branch and set main's plan file to In Progress; the committed branch rules and ADR 060 say the opposite, and no committed record covers the change

Next: the product owner decides at merge-change's pinned approval.
