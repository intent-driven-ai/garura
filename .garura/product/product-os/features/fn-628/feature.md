# Feature: See one plan as a tree

## What it does
Anyone runs /show-plan with a plan's number, or with no number while on a plan's branch, and sees that one plan as a tree from its plan file alone: the work not yet done is shown, the work that is Done or Dropped is hidden and counted, and each plan it needs is printed after it, so a person back after two days away knows where the plan stands from the tree alone.
- The legend comes first: the mark and name of every status: ○ Not Started, ◐ In Progress, ▶ Now, ⛔ Blocked, ✓ Done and ✗ Dropped.
- The first line is the plan's business intent: its number and title, with no mark. Each line under it is one item: its status mark, its issue number and its title, indented under its parent with tree lines. No line is a bare number.
- Each item shows the status its plan file gives it. Nothing is worked out from the items under it: an epic may be Done with stories still open.
- Not Started, In Progress, Now and Blocked are shown. Done and Dropped are hidden, and the last line counts them, for each hidden status.
- A hidden item that has a shown item under it is still printed, so the shown item keeps its place: a Done story with a new bug under it is printed, with the bug.
- A shown item whose children are all Done or Dropped prints them too, one level down, so a person sees what was finished under it and can decide on it, such as marking it Done. They are not in the hidden count.
- Each plan this plan needs is printed after it, on the same screen, with a note. A needed plan that has no file gets the plain line that there is no such plan.
- With no number, the plan is read from the name of the branch the person is on: a plan's own branch, `plan/<id>/base`, or an issue's branch in it, `plan/<id>/<issue>-<slug>`. The tree is the same as with the number. A typed number always wins.
- A number no plan has, or a branch that belongs to no plan, gets a plain message and no tree.
- The plan tool prints the tree from the plan-view template, with no tracker read and no model call. A check rebuilds the expected tree from the plan file on its own, and fails the run when a line, the hidden count or a needed plan differs.
- It is read only. It writes no plan file, no issue and no branch, and it runs on any branch.
- Examples, in different kinds of project:
  - In a clinic's booking app, a developer back from two days off runs /show-plan on a story branch and sees the plan for online check-in: two stories In Progress, one Now, one Blocked, and a last line that counts 3 Done and 1 Dropped as not shown.
  - In a shop's checkout project, a feature item whose stories are all Done prints with each of them under it, so the product owner sees it can be marked Done.
  - In a bank's payments service, the plan for new statements needs the plan for the account data feed, and that plan's tree prints after it on the same screen.
- How it meets the capability: this is "sees every plan and where it stands", for one plan in full.

Status: built, in /show-plan and the plan tool's show. Its first form showed one plan as a tree, from its plan file alone. Later came showing the children of an open parent when all of them are Done or Dropped, and showing the plan of the current branch when no number is given. Not built, or open:
- The run may end on its run summary, not on the tree: /list-plans ends on a run summary instead of the plans, and /show-plan has the same ending, read from its steps and not seen in a run.

## Inputs / Outputs
- In: the plan's number as the person typed it, or the name of the branch the person is on.
- In: the plan files: the plan's own file and the file of each plan it needs.
- In: a copy of the plan-view template.
- Out: the tree, shown to the person as the tool printed it: the legend, the plan, the hidden count, and each plan it needs.
- Out: a plain message when no plan has the number, or when the branch belongs to no plan.
- Out: the check's record: each line, the hidden count and the needed plans as the plan file says, the same print twice, and no plan file changed.

## Rules & behavior
- Done and Dropped are hidden and counted. The reason: "The tree shows what is left and what is moving; finished work is a count, not a wall of lines."
- No status is worked out from the items under it. The reason: "Each node shows the status its plan file gives it: no status is worked out from the nodes under it (no roll-ups)."
- A hidden item with a shown item under it is printed. The reason: "so the shown node keeps its place".
- The finished children of a shown item are printed. The reason: "so a person sees what was finished under it and can decide on it".
- A typed number always wins; with none, the plan is read from the branch name. The reason: "A typed number always wins.", and a plan is never guessed: "The play halts and prints the error; a plan is never guessed."
- Each line is a mark, a number and a title. The reason: a bare number tells a reader nothing after time away, and "No line is a bare number."
- A plan file with a status the template does not know stops the play with the file named. This stops a person with no way past it: a person fixes the file. The way past is Give every gate a way past's, in Orchestration.
- Read only. The reason: a view that changed what it shows could not be trusted, and "the play writes no plan file, no issue and no branch".

## Acceptance criteria
- Given a plan with items Not Started, In Progress, Now, Done and Dropped, when /show-plan with its number runs, then every item that is not Done or Dropped is a line of mark, number and title, and the last line counts the hidden ones.
- Given a Done story with a Not Started bug under it, when /show-plan runs, then the story is printed with the bug under it and is not in the hidden count.
- Given an open feature item whose stories are all Done or Dropped, when /show-plan runs, then each of those stories is printed under it, and none is in the hidden count.
- Given a plan that needs another plan, when /show-plan runs, then the needed plan's tree prints after it on the same screen.
- Given a person on an issue's branch of a plan and no number typed, when /show-plan runs, then the tree is the same as with that plan's number.
- Given a person on main and no number typed, or a number no plan has, when /show-plan runs, then it prints a plain message and no tree.

## Out of scope
- Every plan at once. See every plan and where it stands (fn-729) does it.
- Each plan's branch against main. See every plan's branch against main (fn-806) does it.
- Setting the status of an item. Set each item's status and the plan's status and direction in one approved session (fn-730) does it.
- Choosing which item is worked next. Choose which item is worked next (fn-choose-next-item) will do it; it is not built.
- The issues in the tracker. Track execution in the team's tracker owns them.
- What a plan file holds, as the ontology's Plan kind says. Product model owns it.

## Sources
- The product owner on 2026-11-10: "A person chooses what is delivered next as a slice, sees every plan and where it stands, and sets the order and status of the work as it runs."
- core/components/plays/show-plan/reference/ice.md: "The tree shows what is left and what is moving; finished work is a count, not a wall of lines.", "Each node shows the status its plan file gives it: no status is worked out from the nodes under it (no roll-ups).", "so the shown node keeps its place", "so a person sees what was finished under it and can decide on it", "A typed number always wins.", "No line is a bare number.", "the play writes no plan file, no issue and no branch"
- core/components/plays/show-plan/scripts/resolve_args.py: "The play halts and prints the error; a plan is never guessed."
- standards/templates/plan-view.md, in Phoenix memory: "A shown node whose children are all Done or Dropped prints those children too, one level down"
- The research and drafts for Orchestrate agent work through planning, the page this one replaces as it read on 2026-11-10: "a reader coming back after two days knows where a plan stands from the tree alone"
