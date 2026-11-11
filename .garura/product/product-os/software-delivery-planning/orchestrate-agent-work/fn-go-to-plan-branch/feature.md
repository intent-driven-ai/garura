# Feature: Get onto a plan's branch for a session, and come back

## What it does
Before a plan session changes anything, it gets onto the plan's own branch, `plan/<id>/base`, through the one script every play uses for it; at the end it goes back to the branch the person started on, and on "abort" it undoes a branch the session cut, so a plan is only ever changed on its own branch and the person ends where they began.
- Uncommitted work stops it first, on every branch, the plan's own included, and it names the files. Nothing is changed. The person cleans up and runs the session again. The session's own working folder does not count; a staged file always counts.
- Then one of three paths, read from git, never from the plan file:
  - on the plan's branch already: it stays, and takes the remote's new commits, fast-forward only;
  - the plan's branch exists here or on the remote: it switches to it, and takes the remote's new commits;
  - the plan has no branch: it switches to main, takes the remote's new commits, sets main's plan file to In Progress with the branch named, commits that on main, pushes main, and cuts the branch from that commit. This is the one write a session makes before the person approves anything. The cut is the same one Ship every change the same way makes when a plan's work starts; the session only calls it.
- A plan that main's file marks Done or Dropped gets no branch: it stops with the status named, and nothing is written.
- A copy of the plan's branch that is here but gone on the remote, because the plan paused and its branch landed and was deleted, is deleted when every commit on it is on main, and the plan is then cut fresh. When the copy holds a commit that is not on main, it stops, keeps the copy and names the commits.
- A call to the remote never asks for a password and gives up after two minutes, so a stalled remote is a stop, never a hang.
- It writes a record: what it did (stay, switch, cut or stop), the plan's branch, the branch the person started on, the main commit of a cut, whether main's file was written, and the files that stopped it.
- At the end, it switches back to the branch the record says the session started on. Uncommitted work stops that too.
- On "abort", when the session cut the branch, it first checks that the branch holds nothing but main's commit, here and on the remote. Then it reverts that commit on main, pushes main, deletes the branch here and on the remote, and goes back. When anything else is on the branch, it stops and names the commits, and nothing is undone. When the session stayed or switched, the branch is left as it is. A second "abort" finishes one that stopped after the revert.
- Examples, in different kinds of project:
  - In a shop's checkout project, the product owner runs /update-plan on main for the guest checkout plan, which has a branch; the session switches to it, and after the landing it goes back to main.
  - In a clinic's booking app, the reminders plan has no branch; the session sets main's plan file to In Progress and cuts the branch, and when the product owner types "abort", it reverts that commit, deletes the branch and ends on main.
  - In a bank's payments service, a developer with an unsaved change to a test file runs /update-plan; the session stops, names that file, and changes nothing.
- How it meets the capability: "sets the order and status of the work as it runs" happens on the plan's own branch and nowhere else, and the person's own place in the repository is kept.

Status: built, in the plan tool's branch script (go, back and abort), used by /update-plan. It came with #720 (manage a plan with /update-plan, closed) and #730 (the /update-plan session, closed). The stop on a stale copy came with #953 (the findings of a review: an unsafe delete of a stale plan branch, closed). The same script also cuts a plan's branch for /start-change when a plan's work starts; that is Open each change where it will land (fn-731), in Developer tooling. Not built, or open:
- The stop on uncommitted work has no way past it.
- After a plan pauses and its branch lands, main's plan file still names the branch until a person fixes it by hand. The session is not stopped by it, because it decides from git, but the file reads wrong. Pause a plan and start it again (fn-pause-plan) is not built.

## Inputs / Outputs
- In: the plan's id, the plans folder, and the folders the session may leave uncommitted (its own working folder).
- In: git: the branch the person is on, the uncommitted files, the plan's branch here and on the remote, and main.
- In: main's plan file, for a plan with no branch.
- Out: the record of the step onto the branch: stay, switch, cut or stop, with the branches, the main commit of a cut and the files named.
- Out, for a cut: main's plan file set to In Progress with the branch named, committed and pushed, and the plan's branch cut from that commit and pushed.
- Out, at the end: the person on the branch they started on.
- Out, for "abort": main's plan file put back by a revert commit, the cut branch deleted here and on the remote, and the person back where they started.

## Rules & behavior
- Uncommitted work stops it, on every branch. The reason: "On any branch with uncommitted work — the plan's own branch included — it stops, names the files and changes nothing; the person cleans up."
  - This stops a person with no way past it: in the product owner's words, "a stop on uncommitted work is the person's to clean up". The way past is Give every gate a way past's, in Orchestration.
- Git decides which path, never the plan file. The reason: "The cut itself is safe: `plan_branch.py go` decides from git, not from the file, so a stale name does not stop it."
- A plan is changed only on its own branch. The reason: "While its work is in progress, a plan has its own branch, `plan/<id>/base`, and the plan changes only there."
- A plan with no branch is cut main first, through the one script. The reason: "Every cut goes through one script", so main's plan file says the plan is In Progress before its branch exists. The cut is Ship every change the same way's; the session calls it.
- A Done or Dropped plan gets no branch. The reason: "a person sets its status before work starts again".
- A stale copy is deleted only when every commit on it is on main. The reason: a local branch with commits found nowhere else holds work, and "deleting it loses work".
- "Abort" undoes only a cut that holds nothing else. The reason: the session may undo its own write and nothing more, so "it checks that the branch holds nothing but main's commit".
- A call to the remote never prompts and has a time limit. The reason: "so a stalled origin is a stop, never a hang".
- The session ends on the branch the person started on. The reason: the session fails when "The session does not end on the branch the person started on."
- Not decided: whether the stop on uncommitted work is a gate that needs a way past under Orchestration's Must not, or a stop kept on purpose (#992).

## Acceptance criteria
- Given a story branch with an uncommitted file, when the session starts on a plan, then it stops, names the file, and the branch checked out and its commit are unchanged.
- Given the plan's own branch with an uncommitted file, when the session starts, then it stops in the same way.
- Given a plan whose branch exists only on the remote, when the session starts on main, then it is on the plan's branch, which follows the remote, and at the end it is back on main.
- Given a plan with no branch, when the session starts, then main's plan file reads In Progress with the branch named at the main commit the branch was cut from; and when the person types "abort" with nothing else on the branch, then main's plan file reads as before through a revert commit, the branch is gone here and on the remote, and the person is on the starting branch.
- Given a cut branch that holds one more commit, when the person types "abort", then nothing is undone and the commit is named.
- Given a plan that main's file marks Done, when the session starts, then it stops with the status named and nothing is written.
- Given a local copy of the plan's branch that is gone on the remote and holds a commit not on main, when the session starts, then it stops, keeps the copy and names the commit.

## Out of scope
- Cutting a plan's branch when its work starts, through /start-change, and landing a plan's branch on main. Ship every change the same way, in Developer tooling, owns them: Open each change where it will land (fn-731) and Merge each change where it lands, on the review's approval and a person's yes (fn-673).
- What the session changes once it is on the branch. Set each item's status and the plan's status and direction in one approved session (fn-730) does it here, and Change the work items (fn-change-work-items), in Turn intents into agent work, does the work items.
- Writing the plan file's branch field as none when a plan pauses. Pause a plan and start it again (fn-pause-plan) will do it; it is not built.
- A way past the stop on uncommitted work. Give every gate a way past, in Orchestration, owns it.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "A person chooses what is delivered next as a slice, sees every plan and where it stands, and sets the order and status of the work as it runs."
- core/components/plays/update-plan/reference/ice.md: "On any branch with uncommitted work — the plan's own branch included — it stops, names the files and changes nothing; the person cleans up.", "a stop on uncommitted work is the person's to clean up", "The session does not end on the branch the person started on."
- core/tools/plan/plan_branch.py: "a person sets its status before work starts again", "it checks that the branch holds nothing but main's commit", "so a stalled origin is a stop, never a hang", "the one write a plan session makes before the person approves anything"
- core/tools/plan/README.md: "The one way a play gets onto a plan's branch."
- docs/adr/061-a-plans-branch-is-cut-by-the-play-that-starts-its-work-main-first.md: "The cut itself is safe: `plan_branch.py go` decides from git, not from the file, so a stale name does not stop it.", "Every cut goes through one script"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "While its work is in progress, a plan has its own branch, `plan/<id>/base`, and the plan changes only there."
- .garura/product/product-os/features/fn-731/feature.md: "deleting it loses work"
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/fn-change-work-items/feature.md: "Getting onto the plan's own branch and coming back. Orchestrate agent work through planning owns plan branches."
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- GitHub #953 (closed): "The findings left by round 2 of the PR #950 review: an unsafe delete of a stale plan branch, and four wording fixes"
- GitHub #730 (closed): "The /update-plan session: instructions, checks, one approval, one landing on the plan's branch"
- GitHub #992 (open): "or exceptions to the principle"
