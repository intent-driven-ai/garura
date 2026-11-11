## Intent
- Goal: A plan session is on the plan's own branch before it changes anything, stays, switches or, for a plan with no branch, has it cut main first through the one script, and at the end is back on the branch the person started on; on "abort" a branch the session cut is undone when nothing else is on it.
- Limit: Uncommitted work on any branch, the plan's own included, stops it before anything changes, with each file named.
- Limit: It decides from git, never from the plan file, and never cuts a branch for a plan that main's file marks Done or Dropped.
- Limit: It never deletes a branch that holds a commit found nowhere else, and "abort" undoes nothing when the cut branch holds more than main's commit.
- Fails if: The session switches away from uncommitted work, or goes on over uncommitted work on the plan's own branch.
- Fails if: A plan is changed on a branch other than its own, beyond the main-first step of a cut.
- Fails if: The session does not end on the branch the person started on, or "abort" leaves a branch it cut, or main's plan file still set, when nothing else was on that branch.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the branch the person is on, the uncommitted and staged files, the plan's branch here and on the remote, main and main's plan file, the commits a cut branch holds, and the record the session wrote when it got onto the branch.
- Never read: any memory file by its path, any ICE page, and any plan's evals folder.
- Persona: the product owner, who runs a plan session from wherever they are; and the developer, a person or an AI agent who builds the code, whose uncommitted work must not be carried off.
- Scope: In: the stop on uncommitted work, staying, switching, calling the main-first cut, the stale copy, the record, going back, and undoing a cut on "abort". Out: the cut's own rules when a plan's work starts, landing a plan's branch on main, what the session changes on the branch, writing the branch field on a pause, and a way past the stop.

## Expectation
- Scenario: In a clinic's booking app, the product owner is on main and runs /update-plan for the reminders plan, which has no branch. Main's plan file is set to In Progress with the branch named, committed and pushed, and the branch is cut from that commit. The product owner then types "abort": the cut is reverted on main, the branch is deleted here and on the remote, and the session ends on main. The next day, a developer on a story branch with one unsaved test file runs it for the same plan, and it stops and names that file.
- Done means: Someone other than the product owner and the developer reads git here and on the remote, main's plan file and the session's records, and finds the cut commit and its revert on main, main's plan file as it was before the cut, no reminders branch left here or on the remote, the session ended on main, and, for the developer's run, the story branch and its commit unchanged with the test file named.
