# Feature: merge-change lands an issue on its plan branch, and a plan on main only when it is done

## What it does
An issue in a plan merges into its plan's branch. A plan's branch merges into main only when every issue in the plan is closed, and only after every plan it needs has landed or been merged into it.

## Agent intent (ICE)
- Goal: main gets a plan's work only when the plan is done.
- Limit: a one-off fix outside any plan still lands on main as today.
- Fails if: a plan branch merges into main with an open issue, or before a plan it needs.
- Checked by: a test plan with one open issue is refused on main; with all closed it lands.
