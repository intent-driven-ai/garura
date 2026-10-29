# Capability: Manage a plan with /update-plan

## Directional intent
a working session on one plan: a person gives instructions in their own words, the play checks each one against the product model, the rules for GitHub and how an epic holds its work, keeps a running list, and on a plain "approved" lands every change at once in the plan file, GitHub and the product model, on the plan's own branch. Orchestration only.

## Agent intent (ICE)
- Goal: After the person approves, the plan file, GitHub and the product model agree, and nothing beyond the approved list has changed.
- Limit: Nothing is written before a plain "approved". It changes a plan only on the plan's own branch; it cuts a branch only when the plan has none (main's plan file first, then the cut), never merges one, and never changes code.
- Fails if: a write happens before approval; a change lands in one of the three and not the others; a change the person did not approve lands; a plan is changed anywhere but on its own branch.
- Checked by: after landing, a compare of the plan file, GitHub and the model finds no difference, and a compare against the approved list finds nothing extra.
