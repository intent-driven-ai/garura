# Feature: /shape-eval writes the hidden eval

## What it does
/shape-eval <intent> runs after /shape-plan, on its own. It reads the epic, its stories and the slice's hidden file, and writes the eval for the business intent in the plan's evals folder (.garura/project/plans/<plan-id>/evals/<slug>/). No builder reads that folder. Not built yet (#798).

> To be deepened later: written by /shape-slice for bi-788 at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.

## Inputs / Outputs
- In: the epic of the slice and its stories.
- In: the slice's hidden file (failure-and-recovery.md) from the plan's evals folder.
- Out: one eval for the business intent in `.garura/project/plans/<plan-id>/evals/<slug>/`.
- Out (when needed): a handoff plan, which never names a failure condition, its id or its check.
- Thin: the format of the eval and of the handoff plan is not set yet.

## Rules & behavior
- The play runs after /shape-plan, on its own.
- It reads only the epic, its stories and the hidden file. It never reads an ICE page, the usage guide or the code.
- The eval checks from the outside, on the slice's surface. For Garura that surface is often a play, so the eval runs the play on a test project.
- The running eval reaches the slice only through its usage guide (`guides/<slug>.md`).
- When the eval cannot test a goal, an expectation or a failure condition yet, it says so.
- Until eval encryption (#828) exists, only a read rule keeps builders out of the evals folder.

## Acceptance criteria
- Given a plan with an epic and its stories, when the product owner runs /shape-eval, then the eval is in the plan's evals folder.
- Given the eval, when a person reads it, then each goal and expectation of the stories, and each failure condition of the hidden file, has a check or a note that it cannot be tested yet.
- Given the build plays, when a person reads their inputs, then none names the evals folder.

## Out of scope
- Running the eval after the build.
- Encrypting the eval so that no builder can read it (#828).
- The slice, the hidden file, the plan, the epic and the stories (fn-795, fn-818).

> Thin ICE: proposed by /shape-slice for bi-788 (#844, decision 7); deepen with /discover-capabilities.

## Agent intent (ICE)
- Goal: After /shape-eval <intent>, the slice's evals folder holds one eval that checks from the outside, on the slice's surface, each goal and expectation of the stories, and that no failure condition in the hidden file happens.
- Limit: Read only the epic, its stories and the slice's hidden file; never an ICE page, the usage guide or the code.
- Limit: The play writes the eval only in the plan's evals folder (.garura/project/plans/<plan-id>/evals/<slug>/) and nowhere else.
- Fails if: the eval is written outside the plan's evals folder, or a builder's inputs name that folder.
- Fails if: a story's goal or expectation, or a failure condition in the hidden file, has no check, and the eval does not say that it cannot test it yet.
- Fails if: a handoff plan that the eval writes names a failure condition, its id or the check.
- Context: serves the product owner; for Garura the surface is often a play, so the eval runs the play on a test project; the running eval reaches the slice only through its usage guide (guides/<slug>.md). Not built yet (#798).
- Checked by: the product owner runs /shape-eval 788 in Claude Code after /shape-plan and finds the eval in plans/788/evals/<slug>/, and no build play's inputs name that folder.
