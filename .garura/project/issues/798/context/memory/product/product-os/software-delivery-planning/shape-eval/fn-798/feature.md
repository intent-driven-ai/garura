# Feature: /shape-eval writes the hidden eval

## What it does
/shape-eval <intent> runs after /shape-plan, on its own. It reads the epic, its stories and the slice's hidden file, and writes the eval for the business intent in the plan's evals folder (.garura/project/plans/<plan-id>/evals/<slug>/). No build is given that folder: the build is given the business intent, never the eval (fn-898). Not built yet (#798).

> To be deepened later: written by /shape-slice for bi-788 at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.

## Inputs / Outputs
- In: the epic of the slice, with its feature-to-story map, and its stories. The map joins each hidden-file entry (by its feature) to its story (ontology v11, Q36).
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
- The eval stays in plain text in the repo. The build is given the intent, never the eval, and fn-898's check flags a build session that read the evals folder, in that build run's evidence (eval encryption, #828, was dropped on 2026-10-26).

## Acceptance criteria
- Given a plan with an epic and its stories, when the product owner runs /shape-eval, then the eval is in the plan's evals folder.
- Given the eval, when a person reads it, then each goal and expectation of the stories, and each failure condition of the hidden file, has a check or a note that it cannot be tested yet.

## Out of scope
- Running the eval after the build.
- Encrypting the eval (#828): dropped by the product owner on 2026-10-26.
- The slice, the hidden file, the plan, the epic and the stories (fn-795, fn-818).
- The checks that no build is given the evals folder and that flag a build session that read it, in that build run's evidence (fn-898).

## Sources
- GitHub #798 (open): the eval play.
- ADR 057 (docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md), its Context and section 7: the product owner dropped encryption and #828 on 2026-10-26. The eval stays in the repo in plain text. The build is given the business intent through the stories, never the eval.
- GitHub #898 (open): the build is given the business intent, never the eval, and a check flags each build session that read the evals folder.

Thin: proposed by `/shape-slice` from the person's answers; deepen with `/discover-capabilities`.

## Agent intent (ICE)
- Goal: After /shape-eval <intent>, the slice's evals folder holds one eval that checks from the outside, on the slice's surface, each goal and expectation of the stories, and that no failure condition in the hidden file happens.
- Limit: Read only the epic, its stories and the slice's hidden file; never an ICE page, the usage guide or the code.
- Limit: The play writes the eval only in the plan's evals folder (.garura/project/plans/<plan-id>/evals/<slug>/) and nowhere else.
- Fails if: the eval is written outside the plan's evals folder.
- Fails if: a story's goal or expectation, or a failure condition in the hidden file, has no check, and the eval does not say that it cannot test it yet.
- Fails if: a handoff plan that the eval writes names a failure condition, its id or the check.
- Context: serves the product owner; for Garura the surface is often a play, so the eval runs the play on a test project; the running eval reaches the slice only through its usage guide (guides/<slug>.md). Not built yet (#798).
- Checked by: the product owner runs /shape-eval 788 in Claude Code after /shape-plan and finds the eval in plans/788/evals/<slug>/.