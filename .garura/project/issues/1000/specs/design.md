# Design: #1000 + #951 (approved by the product owner, 2026-10-31)

One change under plan 717, on `plan/717/1000-show-plan-branch-and-pr950-findings`. The merge closes both.

## #1000 — /show-plan with no number

- No number given: the plan number is read from the branch name (`plan/<id>/base` or
  `plan/<id>/<issue>-<slug>`); the tree is printed exactly as `/show-plan <id>` prints it.
- A branch that belongs to no plan (main, feature/...): the play stops with a plain message
  ("this branch belongs to no plan; give a plan number"); no tree, nothing changed.
- A typed number wins, whatever the branch.
- In show-plan's resolve_args.py (the branch passed in), with tests; show-plan ICE C8 and a new
  scenario, through /edit-play.

## #951 — the five small findings of round 1 of the PR #950 review

1. The pre-flight script reports `plans_base` (plans.base-path, default .garura/project/plans/);
   start-change reads it from there. The script is shared by 30 plays: every copy is restamped.
2. submit_pr.py: when the PR opens but its number cannot be looked up, `on_target` is left
   unknown (null), so the done check fails instead of passing blind. With a test.
3. merge-change: SE-9 and scenario S5 also check the capability close (the capability is in
   issues_closed when every issue under it is closed). ICE change, through /edit-play.
4. The harness standard's principle 8 gains one sentence: the plans a plan needs do not hold it
   off main (ADR 060, decision 4).
5. Memory rule pages: git.md's branch table gains the plan branch shapes; pipeline-position.md
   no longer says start-change always cuts off fresh main. Promoted to Phoenix memory before the
   merge.

## Out of scope

update-plan, show-plan and list-plans also read plans.base-path themselves (finding 1 names
start-change only). #989 and #991 stay their own work.

## Landing

commit, propose, check; reinstall and promote before the merge; merge on the product owner's word;
#1000 and #951 Done in plan 717 inside the change.
