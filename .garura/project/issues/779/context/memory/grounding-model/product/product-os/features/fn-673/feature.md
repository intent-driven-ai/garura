# Feature: merge-change lands an issue on its plan branch, and a plan on main whenever it pauses

## What it does
An issue in a plan merges into its plan's branch. When the plan pauses, its branch merges into main once its review approves it, even with issues of the plan still open; those issues stay open and stay in the plan. Plan order does not hold a plan off main. When work on the plan starts again, a new branch is cut from main.

## Agent intent (ICE)
- Goal: main gets a plan's work whenever the plan pauses and its review approves it.
- Limit: a one-off fix outside any plan still lands on main as today.
- Fails if: a plan's branch is held off main for its open issues or for a plan it needs, or an issue in a plan lands on main instead of its plan's branch.
- Checked by: a test plan with one open issue lands on main once its review approves it, and that issue stays open.