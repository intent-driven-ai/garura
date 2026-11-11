## Intent
- Goal: A person back after two days away knows where one plan stands from its tree alone: the plan the number or the branch names, with every item not Done or Dropped as a line of mark, number and title under its parent, the Done and Dropped items hidden and counted on the last line, the finished children of a shown item and the hidden parents of a shown item printed, and each plan it needs printed after it, all from the plan files by one template.
- Limit: It reads only the plan files; it never reads the tracker or the product model, and no model call makes the tree.
- Limit: It writes no plan file, no issue and no branch.
- Limit: No status is worked out from the items under it, and a plan is never guessed: a number no plan has, or a branch in no plan, gets a plain message and no tree.
- Fails if: A Done or Dropped item is shown when no shown item sits under it and it is not the finished child of a shown item, or the hidden count is wrong or missing.
- Fails if: A line has no title or no number, or a plan the plan needs is left out.
- Fails if: Two runs on the same plan file print differently, or a missing plan or a branch in no plan gets a tree.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the plan's file and the files of the plans it needs, the plan-view template's statuses and tree lines, the number the person typed, and the name of the branch the person is on.
- Never read: any memory file by its path, any ICE page, and any plan's evals folder.
- Persona: the developer, a person or an AI agent who builds the code, who comes back to a plan after time away; and the product owner, who decides on an item whose work is finished.
- Scope: In: the tree, the legend, the hidden count, the needed plans, the plan read from the branch, the plain messages, and the check of the print. Out: every plan at once, the graph against main, setting statuses, choosing the next item, and the run's closing report.

## Expectation
- Scenario: In a clinic's booking app, a developer back after two days runs /show-plan on a story branch of the online check-in plan. The tree shows the plan's title, then its epic with two stories In Progress, one Now and one Blocked, a Done story with a new Not Started bug under it, and an open feature item with its three Done stories under it; the last line counts 4 Done and 1 Dropped as not shown; the reminders plan it needs prints after it. On main with no number, the same run prints a plain message and no tree.
- Done means: Someone other than the one who ran it reads the plan files and the printed tree, and finds each line as the plan file says, the Done story printed because of its bug, the feature item's Done stories printed and not counted, a hidden count equal to the items not printed, the reminders tree after it, the same tree on a second print, no plan file changed, and no tree on main.
