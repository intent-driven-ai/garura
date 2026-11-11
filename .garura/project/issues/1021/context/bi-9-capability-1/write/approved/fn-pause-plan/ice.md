## Intent
- Goal: Once a paused plan's branch has landed on main and is gone, main's plan file says the plan has no branch, with no hand edit, and when the plan's work starts again main's plan file names the new branch; so a plan file always says truly whether its plan has a branch.
- Limit: Only the plan file's branch field changes; the plan's Status, Direction, items and Waits on stay as a person set them.
- Limit: The field is written as none only when git shows the branch gone and every commit on it on main.
- Limit: It never lands, cuts or deletes a branch, and never closes or moves an issue.
- Fails if: After a paused plan's branch has landed and is gone, main's plan file still names it, or a person had to edit it by hand.
- Fails if: The plan file reads no branch while the plan's branch still holds commits that are not on main.
- Fails if: A status, the direction or an item changed that the person did not set, or an open issue of the paused plan was closed or left the plan.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: main's plan file and its branch field, git's branches here and on the remote and whether every commit of the plan's branch is on main, the session's word that the plan is paused, the landing of the plan's branch, and the ontology's rules for a plan's branch.
- Never read: any memory file by its path, any ICE page, and any plan's evals folder.
- Persona: the product owner, who pauses a plan and starts it again; and the technical lead, who checks which plan is on which branch.
- Scope: In: writing main's plan file's branch field as none once a paused plan's branch has landed and is gone, refusing it while the branch holds work not on main, and keeping the field true through the next start. Out: setting Paused and the direction, landing the branch and the review of its commits, cutting the new branch, the views, and removing a plan.

## Expectation
- Scenario: In a shop's checkout project, the product owner pauses the guest checkout plan with two stories open. Its branch is raised to main, approved, merged after the product owner's yes, and deleted. Main's plan file then reads Paused with no branch, and /list-plans --graph names the plan on main. A month later a session starts on the plan again: a new branch is cut from main, and main's plan file reads In Progress with that branch named.
- Done means: Someone other than the product owner reads git here and on the remote and the history of main's plan file, and finds no branch named while none existed, the new branch named after the start, both stories still open and in the plan, the Status and Direction as the product owner set them, and no hand edit of the branch field.
