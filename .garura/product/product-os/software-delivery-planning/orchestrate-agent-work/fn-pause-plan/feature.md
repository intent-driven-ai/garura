# Feature: Pause a plan and start it again

## What it does
When a person pauses a plan, its branch lands on main, and once that branch is gone, main's plan file says the plan has no branch; when the plan's work starts again, a new branch is cut from main and main's plan file names it. So a plan file always says truly whether the plan has a branch, with no hand edit, and the views, the removal of a plan and the next start read it right.
- A pause of a plan has three steps, in this order:
  - A person sets the plan to Paused in a session. This is built, in the session (fn-730).
  - The plan's branch lands on main through the change plays, with the plan's open issues still open and still in the plan. This is built, in Ship every change the same way (fn-673).
  - Once the branch has landed and is deleted, main's plan file reads no branch, `branch: null`. This feature does that step; it is built nowhere today.
- The branch field reads none only when git shows that the branch is gone and every commit on it is on main. A branch that still holds work that is not on main is never written as none.
- Only the branch field changes. The plan's Status, its Direction, its items and its Waits on stay as a person set them.
- Starting again: the plan's work starts in a session or with /start-change, a new branch is cut from main, main first, and main's plan file reads In Progress with the new branch named. This is built, in the step onto a plan's branch (fn-go-to-plan-branch) and in /start-change (fn-731).
- What a branch field that is not kept true does today: the graph shows a gone branch with counts of ?, and the removal of a plan refuses the plan for that branch, until a person edits the file by hand. The step onto a plan's branch is not stopped by it, because it decides from git.
- Examples, in different kinds of project:
  - In a shop's checkout project, the product owner pauses the guest checkout plan while the team waits for a new payment provider. Its branch lands on main with two stories open, and main's plan file then reads Paused with no branch, so /list-plans --graph names the plan on main.
  - In a clinic's booking app, the reminders plan, paused last month, starts again in a session. A new branch is cut from main, and main's plan file reads In Progress with that branch named.
  - In a bank's payments service, the product owner approves removing an old plan that paused long ago. Its file reads no branch, so the removal is not refused for a branch that no longer exists.
- How it meets the capability: "sees every plan and where it stands" holds only when each plan file says truly whether its plan has a branch, and "sets the order and status of the work as it runs" includes stopping a plan's work and starting it again.

Status: not built. Writing the branch field as none is built nowhere: ADR 060 (a plan's branch merges into main when the plan pauses) left it to the /update-plan session, and ADR 061 (a plan's branch is cut by the play that starts its work, main first) found that no script writes it. Today a person sets it by hand. The other steps are built: setting Paused in the session (fn-730), landing the branch (fn-673), and the cut on a new start, in the step onto a plan's branch (fn-go-to-plan-branch) and in /start-change (fn-731), which cuts through the same script. Also open:
- After a session sets a plan to Paused, nothing then lands its branch; a person raises it with the change plays.
- No issue is filed for writing the branch field on a pause.

## Inputs / Outputs
- In: the plan's id, and its Status as main's plan file holds it.
- In: git: the plan's branch here and on the remote, and whether every commit on it is on main.
- In: main's plan file and its branch field.
- Out: main's plan file with no branch once the paused plan's branch has landed and is gone, and nothing else in the file changed.
- Out: a record of what it did: the plan, the branch that was gone, and the commit that wrote the field.
- Out, when the branch still holds work that is not on main: the field unchanged, and the commits named.

## Rules & behavior
- When a plan pauses, its branch lands on main, and the plan file then says it has none. The reason: "The branch is then deleted, and the plan file says `branch: null`."
- The plan's open issues stay open and stay in the plan. The reason: "Those issues stay open and stay in the plan."
- Main's copy is the one that says it. The reason: "Only two copies of the plan file count: the one on the plan's branch and main's.", and once the branch is gone only main's is left.
- The field is never kept by hand. The reason: a field kept by hand is one that no play writes, "so it can drift from the branches".
- Only the branch field changes. The reason: "Apart from an item whose issue closed, a status or the direction changes only when a person asks for it."
- A branch that holds work that is not on main is never written as none. The reason: a branch with commits found nowhere else holds work, and "deleting it loses work".
- Starting again cuts a new branch from main. The reason: "When the plan starts again, a new branch is cut from main.", and "Cutting the plan's branch moves main's plan file to In Progress".
- A stale field stops no start. The reason: "The cut itself is safe: `plan_branch.py go` decides from git, not from the file, so a stale name does not stop it."
- Not decided: whether writing the plan's branch field as none when the plan pauses stays owed by the /update-plan session or becomes work of its own.
- Not decided: when the branch field is written as none: by the merge as the paused plan's branch lands, or by the next session that reads the plan.
- Not decided: whether a session that sets a plan to Paused also starts the landing of its branch on main, or a person starts it with the change plays.
- Not decided: whether pausing a plan also asks the person for its Direction.

## Acceptance criteria
- Given a plan set to Paused whose branch has landed on main and is deleted, when the pause is done, then main's plan file reads Paused with no branch, and its items, Direction and Waits on are as before. This is not built.
- Given a paused plan with two stories open, when its branch has landed and its field reads no branch, then both stories' issues are still open and both are still in the plan file. This is not built.
- Given a paused plan whose branch still holds a commit that is not on main, when the pause is done, then the branch field is unchanged, and the commit is named. This is not built.
- Given a paused plan whose file reads no branch, when /list-plans --graph runs, then the plan is named on main, with no counts of ?. This is not built.
- Given a paused plan whose file reads no branch, and that no other plan needs, when a person approves its removal, then the removal is not refused for a branch. This is not built.
- Given a plan paused and then started again, when git's history of main's plan file is read, then no commit between the pause and the start is a hand edit of its branch field. This is not built.

## Out of scope
- Setting a plan's Status to Paused, and its Direction. Set each item's status and the plan's status and direction in one approved session (fn-730) does it.
- Landing a paused plan's branch on main, and showing that every commit on it was reviewed. Ship every change the same way, in Developer tooling, owns them: Merge each change where it lands, on the review's approval and a person's yes (fn-673), and Land a plan's branch on main with evidence that every commit was reviewed (fn-land-plan-with-evidence).
- Cutting a new branch when the plan's work starts again. Get onto a plan's branch for a session, and come back (fn-go-to-plan-branch) does it for a session, and Open each change where it will land (fn-731), in Ship every change the same way, does it for /start-change.
- Showing a plan as on main. See every plan's branch against main (fn-806) does it.
- Removing a plan. Remove a plan on a person's approval (fn-remove-plan) does it.

## Sources
- The product owner on 2026-11-10: "A person chooses what is delivered next as a slice, sees every plan and where it stands, and sets the order and status of the work as it runs."
- docs/adr/060-a-plans-branch-merges-into-main-when-the-plan-pauses.md: "The branch is then deleted, and the plan file says `branch: null`.", "Those issues stay open and stay in the plan.", "so it can drift from the branches", "nothing writes a plan file's branch field yet; it is kept by hand"
- docs/adr/061-a-plans-branch-is-cut-by-the-play-that-starts-its-work-main-first.md: "No script writes `branch: null` when a plan's branch lands on main", "The cut itself is safe: `plan_branch.py go` decides from git, not from the file, so a stale name does not stop it.", "whether writing `branch: null` on a pause stays owed under [the /update-plan session], or becomes its own issue."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Only two copies of the plan file count: the one on the plan's branch and main's.", "Apart from an item whose issue closed, a status or the direction changes only when a person asks for it.", "Cutting the plan's branch moves main's plan file to In Progress", "Branch: none — its branch merged into main when it paused."
- .garura/user-provided/managing-work.md: "When the plan starts again, a new branch is cut from main."
- .garura/product/product-os/features/fn-673/feature.md: "a plan's own branch merges into main whenever the plan pauses, with issues of the plan still open; those issues stay open and stay in the plan"
- .garura/product/product-os/features/fn-731/feature.md: "deleting it loses work"
- .garura/product/product-os/software-delivery-planning/ship-every-change/fn-land-plan-with-evidence/feature.md: "Pausing a plan and changing its items. Turn intents into agent work, in Product → Spec, and Orchestration own them."
- core/tools/plan/plan.py: "the graph's counts read ?"
- core/components/skills/remove-plan/SKILL.md: "A plan whose `branch` is not null is refused, naming the branch."
- The stock-take of Orchestration (2026-11-10), section 1.9: "Nothing is filed for choosing what is built next, a view across every intent, writing the branch field on a pause, or working out `needs_plans`."
