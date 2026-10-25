# Decisions — #878, the first /shape-plan 788 run

## 1. The tracker check's failure on #794 (2026-10-25)

The tracker check failed: work order #794 holds 16 sub-issues besides its three stories (#795, #818, #798). 14 are closed; #796 and #828 are open. They come from plan 788's tree, which was filed by hand before /shape-plan existed.

Choice: option 2. Nothing changes in GitHub. A bug is filed against the check.

The product owner's words: "2 Also, we have to record that what we are running is plan splines. We are in the middle of the splines, or shake right, or whatever we call it, shape plan, kind of a thing, right? This is an existing and running plan. Once the plan is built, it is built differently, and the plan can continue to evolve. I think we can mark the runner as closed and okay."

What this means:
- /shape-plan ran in the middle of plan 788, a plan that already existed and was running. A plan that /shape-plan builds from the start is shaped differently.
- A plan keeps evolving after it is built, so a work order can hold more than the stories of its slice.
- The run is closed and accepted by the product owner. Its stop condition reads unmet on D4 (the tracker check) for this reason only; every other check passed, and every tracker write the brief showed was made.
