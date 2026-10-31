# Design: #779 + #953 (approved by the product owner, 2026-10-31)

One change under plan 717, on `plan/717/779-plan-lookup-and-safe-delete`. The merge closes both.

## #779 — where start-change reads the plan from

Today the lookup reads the plan files of the checked-out branch, so an older copy says "no plan".
Reading only main is not enough: an issue added through /update-plan is written on the plan's
own branch first (for example #1001 and #1002 were on plan/717/base's 717.yaml, not main's).

- Fetch, then read each plan file from the latest `origin/main`.
- When that plan names a branch that exists on GitHub, read the plan file on that branch too.
- An issue found in either copy belongs to the plan.
- When GitHub cannot be reached, use the last fetched copies and say so in the record. Never fall
  back to the checked-out files.
- Tests: an old checkout with the issue in main's copy finds the plan; an issue only in the plan
  branch's copy finds the plan; no network uses the last fetched copies and says so.
- start-change ICE C9 changes (where the plan is read from), through /edit-play, with one new
  scenario: an issue added on main while the checkout is on an older branch.

## #953 item 1 — the unsafe delete of a stale plan branch

- A failed GitHub lookup stops the run and says GitHub could not be reached (it no longer reads
  as "gone").
- The local plan branch is deleted only when every commit on it is already on main, or was on
  the plan's branch on GitHub before it was deleted (git's last-known copy of it). Otherwise the
  run stops and names the commits that would be lost.
- Pushes are checked; a failed push stops the run.
- Tests for each case. The same /edit-play pass adds one line to C9.

## #953 items 2–5

2. start-change's one-line description gets the plan wording its intent already uses.
3. merge-change says its run records are committed "on main"; for an issue in a plan they are on
   the plan's branch. The words are in its ICE (C6 and three evals): /edit-play merge-change, no
   behaviour change.
4. Four test names carry review labels (H1, H4, H9, H10); renamed to say what each checks.
5. The fn-673 model page states the old landing rule in its title, line 4 and Goal; all three
   change to ADR 060's rule (a plan's branch lands on main whenever its review approves it),
   through product-os-keeper and enrich-grounding (named lines).

## Out of scope

#951 (the five small findings of round 1 of the same review) stays its own chore.

## Landing

commit, propose, check; reinstall from the branch before the merge (promote only if a memory
file changed); merge on the product owner's word; #779 and #953 Done in plan 717 inside the change.
