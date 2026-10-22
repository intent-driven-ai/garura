# Capability: Start and land work against a plan

## Directional intent
the implementation plays know about plans. start-change cuts a plan's branch and each issue's branch from it; merge-change lands an issue on its plan branch, and a plan on main only when it is done.

## Agent intent (ICE)
- Goal: All of a plan's work collects on its plan branch, and reaches main only when the plan is done.
- Limit: No change to how a change outside any plan (a one-off fix) starts or lands.
- Fails if: an issue in a plan merges straight into main, or a plan lands on main with an open issue, or before a plan it needs.
- Checked by: a test plan with two issues: both land on the plan branch; the plan is refused on main while one is open, and lands when both are closed.
