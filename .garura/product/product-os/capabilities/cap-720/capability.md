# Capability: Manage a plan with /update-plan

## Directional intent
a working session on one plan: a person gives instructions in their own words, the play checks each one against the product model, the rules for GitHub and how an epic holds its work, keeps a running list, and on a plain "approved" lands every change at once in the plan file, GitHub and the product model, on the plan's own branch. Orchestration only.

## Agent intent (ICE)
- Goal: After the person approves, the plan file, GitHub and the product model agree, and nothing beyond the approved list has changed.
- Limit: Nothing is written to GitHub, the model or a plan file before a plain "approved", except the one step that gives a plan with no branch its branch (main's plan file set to In Progress with the branch named, then the cut). It changes a plan only on the plan's own branch; it never merges a branch and never changes code.
- Fails if: a write to GitHub, the model or a plan file happens before approval, other than that branch step; a change lands in one of the three and not the others; a change the person did not approve lands; a plan is changed anywhere but on its own branch.
- Checked by: after landing, a compare of the plan file, GitHub and the model finds no difference, and a compare against the approved list finds nothing extra.
