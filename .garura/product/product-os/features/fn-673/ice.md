## Intent
- Goal: Each change merges into where its branch lands, its plan's branch for an issue in a plan and main for a one-off change or a plan's own branch, only after the review's verdict reads approve, the change can be merged with no failing required check, and a person typed yes; afterwards the checkout is on that branch with the latest, the change's branch is gone, a landed issue in a plan is closed with only its own item set Done, and the merge's records are committed there.
- Limit: Nothing merges without the person's typed yes, and no setting, policy or record of earlier yeses turns it off.
- Limit: When the verdict is not approve, the change cannot be merged or a required check fails, the merge stops and the person is not asked.
- Limit: Nothing merges when the pull request's target is not where the branch lands.
- Limit: A plan's branch is never held off main for its open issues or for a plan it needs, and a landed issue changes only its own item.
- Fails if: A change is merged without an approval verdict, or without the person's typed yes.
- Fails if: An issue in a plan lands on main instead of its plan's branch, or a plan's branch is held off main for its open issues or for a plan it needs.
- Fails if: After a merge, the change's branch is still there, a landed issue in a plan or its item is still open, or an item above it changed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the change's pull request and its target, the branch name, the review's verdict and who decided it, whether the change can be merged and its required checks, and, for an issue in a plan, the plan files and the landed issue's item.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who gives each merge their yes once the review approved it; the developer runs the merge.
- Scope: In: the machine checks before the yes, the yes, the merge, the move to the landing branch, deleting the change's branch, closing a landed issue in a plan and setting its own item Done, and the merge's records. Out: the review and its verdict, the evidence that every commit of a plan's branch was reviewed, cutting branches, and a plan's other items.

## Expectation
- Scenario: A clinic's booking app has a test plan for online check-in with two stories. The first story's change is approved by the review; the product owner types yes; it merges into the plan's branch, its issue closes and its item reads Done, while the epic stays open. The plan then pauses with the second story still open: the plan's branch is raised to main, approved, and on the yes merges into main, and the second story stays open and in the plan. A rejected change in the same week stops before the yes is asked.
- Done means: Someone other than the one who merged reads the code host, the plan file and the merge records, and finds an approval verdict and a recorded yes before each merge, the first story landed on the plan's branch and not on main, its item Done and its epic unchanged, the plan's branch on main with the second story still open, no change branch left, and, for the rejected change, no merge and no question asked.
