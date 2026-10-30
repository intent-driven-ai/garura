# #896 — /shape-plan stops when the business intent already has a plan

Approved by the product owner, 2026-10-30 ("approve").

## What changes

- A pre-flight check: when the intent's plan file (`.garura/project/plans/<id>.yaml`) is there —
  in the checked-out tree or on main — /shape-plan stops before anything else (before
  start-change, before it reads the model, before any write) and says:
  "Plan <id> already exists for #<id>. /shape-plan makes a plan once. To change it (add an epic,
  a story, a feature, or a status), run /update-plan <id>."
- This is a pre-flight check, not a gate: the play that changes an existing plan is /update-plan.
- With no plan file, /shape-plan runs as today.

## How

1. A script, `check_plan_absent.py`, does the check (exit 0 no plan, 3 a plan exists, 2 bad
   input), with tests.
2. /shape-plan's ICE through /edit-play: a new constraint (C14), failure condition, scenario and
   recovery for the check; the promises that only an existing plan can meet are removed — C1's
   "a new slice shaped for the same intent joins the same plan", C3 narrowed to the first run,
   C4, C12, F6, S2, S3, S4, S5, REC6; the Context line on update-plan updated.
3. The scripts' code that brings an existing plan up to date stays for now; it is no longer
   reached. Taking it out is a later clean-up.
4. fn-818's ICE in the product model (/shape-plan's feature) follows after the build and before
   propose-change, through the model sub-agent and the page skill's named-line change: "a second
   run finds the plan … and makes no copies" becomes "when the plan exists, the play stops and
   points to /update-plan", and its open line on a slice that changes after a plan exists is
   settled.
5. The change lands on plan 717's branch through commit, propose, check and merge.
