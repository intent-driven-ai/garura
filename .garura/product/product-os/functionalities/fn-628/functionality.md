# Functionality: Show the plan as a plain-words tree: goal, done, now, next, wait

## What it does
Print one plan as a tree from its plan file: one node per line, each line a status mark, the issue ID and the title; legend done / now / next / blocked; linked plans one after the other.

## Agent intent (ICE)
- Goal: a reader coming back after two days knows where a plan stands from the tree alone.
- Limit: read only; prints from the plan file, no tracker reads.
- Fails if: a line is only an issue number, or a done line does not say decided, built or shipped.
- Checked by: the tree for plan #717 matches its plan file.
