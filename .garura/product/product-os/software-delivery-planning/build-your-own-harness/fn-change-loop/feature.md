# Feature: Change a loop through its ICE

## What it does
A person changes a loop that exists with /edit-loop, its goal, a constraint, a failure condition, a scenario, its plays or their order, its first questions, its checker or runner, or how it ends, by changing its ICE first and building it again, so the loop always matches its intent and any drift shows.
- Each kind of change has its place in the ICE, and reaches a known set of other parts:
  - the goal, a constraint or a failure condition: the Intent, then the step evals, the recoveries, and perhaps the scenarios and the Done means;
  - a scenario, a recovery or the Done means: the Expectation, then the scenario evals and the stop-condition file;
  - a play added, dropped or moved: the loop's plays, one step for each play, the task graph, the Done means and the evals that read each play's done check, and the map of what runs next when the last play changes;
  - a question asked first: the loop's questions, the contract's answers and the plays that used to ask it;
  - the checker or the runner, which are the loop's settings;
  - how the loop ends: the end steps and the task graph.
- It reads the compiled loop, its ICE and its stop-condition file first, and maps what is there.
- It names the change and the smallest set of things it reaches. A new play must exist and run inside a loop; if it does not, the edit stops, and the play is fixed first through its own ICE and /edit-play. A key a play does not read is not handed to it.
- It changes the ICE first and gets the person's typed approval of the change.
- It carries the change through only what it reaches. New ids are added after the last one, and ids that exist are never numbered again, because other files and records point at them.
- It stamps the shared run's scripts again, unchanged, computes the fingerprint again and runs the loop linter until it passes.
- The loop linter fails a loop whose ICE changed after it was built, and names /edit-loop to build it again.
- Examples, in different kinds of project:
  - In a shop's harness repository, the technical lead adds a question the loop asks first. /edit-loop adds it to the ICE, the loop's questions and the contract's answers, and the play that asked it during the run now gets it from the contract.
  - In a clinic's harness, the product owner moves the checker to another model. Only the loop's settings entry changes, and the fingerprint is computed again from the changed ICE.
  - In a game studio's harness repository, a new Done means clause is added as D5, and D1 to D4 keep their ids.
- How it meets the capability: the capability's line asks for building "in a consistent way", and a loop changed only through its ICE, with its scripts stamped again, never drifts from the shared run or from its intent.

Status: built, in /edit-loop, with its copy of the loop linter. Not built, or open:
- Only one loop exists to change, the Discovery loop.
- It runs only on Garura's source layout, as /create-loop does (fn-harness-in-own-repo).
- It does not check loop principles 1, 3, 4, 5 and 8 (#699, the loop builders check the loop principles; fn-check-loop-principles).
- /edit-loop is written by hand and has no ICE of its own: "Like `/edit-play`, this skill is written by hand."

## Inputs / Outputs
- In: the loop's compiled `SKILL.md`, its ICE source and its stop-condition file.
- In: the person's change, and their typed approval of the change to the ICE.
- In: the plays the change adds, and whether each checks a loop contract and reads each key handed to it.
- Out: the changed ICE, the loop built again with its values, steps, task graph, evals, stop-condition file and settings changed only where the change reaches, its scripts stamped again and its new fingerprint.
- Out: the loop linter's clean report, and a short summary of what changed.

## Rules & behavior
- The ICE changes first. The reason: the loop is changed "never by patching the compiled `SKILL.md` so that it says something its ICE does not."
- Drift shows. The reason: "The compiled loop records a fingerprint of its ICE, so drift shows.", and the loop linter: "The fingerprint must be the sha256 of reference/ice.md as it is now, not just present."
- Only wording is edited directly. The reason: "The one safe direct edit is wording with no change in meaning. Anything else goes through the ICE."
- The person approves the change to the ICE. The reason: "Get the person's typed approval of the ICE change."
- A new play runs inside a loop. The reason: "A new play must exist and run inside a loop (it checks a loop contract); if it does not, stop — fix the play first, through its own ICE and `/edit-play`."
- Ids are added, never numbered again. The reason: "never renumber the ones that exist — other files and records point at them."
- The reach stays small, and nothing is left behind. The reason: "Keep the reach small: change only what the change reaches.", and "Leave no orphans: remove every eval and recovery tied to what you removed."
- The scripts are stamped again and the linter passes. The reason: "Copy the shared scripts unchanged; recompute the fingerprint; run `lint_loop.py` until clean."
- With no person reachable, the approval is recorded as assumed. The reason: "With no person reachable, state each assumption, record that approval was assumed, and proceed."

## Acceptance criteria
- Given a loop and a new play that checks a loop contract, when /edit-loop adds it, then the loop's plays, one step for the play, the task graph, its done clause and its evals change, the fingerprint is computed again, and the loop linter passes.
- Given a loop whose ICE changed after it was built, when the loop linter runs, then it fails the loop and names /edit-loop.
- Given a new play that does not check a loop contract, when /edit-loop is asked to add it, then it stops and names the play to fix first.
- Given a new Done means clause, when it is added, then it takes the next free id and no id that exists changes.
- Given a change to the checker, when /edit-loop ends, then only the ICE, the loop's settings entry and the fingerprint changed.

## Out of scope
- Building a new loop. Build a loop from its ICE (fn-build-loop) does it.
- Running the loop. Run plays as loops, in Orchestration, owns it.
- The loop settings' defaults and where they live. Settings, in Standards, structure, settings and memory, owns them.
- The loop principles the linter does not check yet. Check a loop against the loop principles, including what starts it (fn-check-loop-principles) is to do it.
- The loop names and the naming rule. Standards, in Standards, structure, settings and memory, owns them.

## Sources
- .garura/project/issues/1021/context/capabilities.md, lines 116-117, the product owner on 2026-11-11: "You can keep building your harness with your own plays, loops, sub-agents and skills, in a consistent way."
- core/components/plays/edit-loop/SKILL.md, lines 16-18, 22, 24-25, 27-28, 30-40, 52-53, 61, 66-68, 93, 95 and 96: "never by patching the compiled `SKILL.md` so that it says something its ICE does not.", "The compiled loop records a fingerprint of its ICE, so drift shows.", "Like `/edit-play`, this skill is written by hand.", "The one safe direct edit is wording with no change in meaning. Anything else goes through the ICE.", "With no person reachable, state each assumption, record that approval was assumed, and proceed.", "A new play must exist and run inside a loop (it checks a loop contract); if it does not, stop — fix the play first, through its own ICE and `/edit-play`.", "Get the person's typed approval of the ICE change.", "never renumber the ones that exist — other files and records point at them.", "Keep the reach small: change only what the change reaches.", "Leave no orphans: remove every eval and recovery tied to what you removed.", "Copy the shared scripts unchanged; recompute the fingerprint; run `lint_loop.py` until clean."
- core/components/plays/create-loop/scripts/lint_loop.py, lines 180-190: "The fingerprint must be the sha256 of reference/ice.md as it is now, not just present.", and a loop whose ICE changed is told to "rebuild it"
- .garura/product/product-os/software-delivery-planning/run-plays-as-loops/fn-run-loop/feature.md, line 82: "Building and changing a loop. Build your own harness (BI-10) owns it."
- The stock-take of this intent, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 1.5, 2.1 and 9.
