# Capability: Start and land work against a plan

## Directional intent
the implementation plays know about plans. start-change cuts a plan's branch and each issue's branch from it; merge-change lands an issue on its plan branch, and a plan on main whenever it pauses and its review approves it.

## Agent intent (ICE)
- Goal: All of a plan's work collects on its plan branch, and reaches main whenever the plan pauses and its review approves it.
- Limit: No change to how a change outside any plan (a one-off fix) starts or lands.
- Fails if: an issue in a plan merges straight into main, or a plan's branch is held off main for its open issues or for a plan it needs.
- Checked by: a test plan with two issues: both land on the plan branch; with one still open, the plan's branch lands on main once its review approves it, and that issue stays open.
