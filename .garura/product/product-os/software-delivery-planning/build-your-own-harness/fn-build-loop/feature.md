# Feature: Build a loop from its ICE

## What it does
A person builds a loop with /create-loop from its ICE and its own parts, its plays, the questions it asks first, its checker, its runner and how it ends, so that the loop holds only its own values and a pointer to the run every loop shares, and runs the same way as every other loop.
- It first checks that the loop can be built:
  - it names at least one play, and every play exists and runs inside a loop, which means the play checks a loop contract. A play that cannot is fixed first, through its own ICE and /edit-play;
  - its intent has at least one constraint and one failure condition, and a Done means can be composed;
  - it does no work of its own. A step that is real work, such as writing a page, belongs in a play: the builder names the play, or says one is missing, and stops.
- It interviews the person for the loop's ICE and its parts:
  - the Intent: the goal, the constraints about the run, and the failure conditions;
  - the plays, in any order, with what each gets from the loop's contract. Every input comes from the loop, never from another play's output, and a key a play does not read is not handed to it;
  - the questions the loop asks before any play runs;
  - the checker, a sub-agent on a model that is not the session's, or Codex, which judges the result from the loop's outputs only;
  - the runner, a sub-agent or a headless session;
  - how the loop ends: its end steps and its close.
- It generates the Expectation: the scenarios, one recovery for each failure condition, and the Done means, read from the loop's own run folder.
- A loop's steps are fixed: open the change, ask the questions, write the contract, run the plays in rounds and decide after each round, run the checker, then the end plays, the scenario checks and the close.
- It writes the loop's folder: the compiled `SKILL.md` with the Shared Loop Run's anchor lines and the loop's own values between them, the stop-condition file from the Done means, and the shared run's scripts stamped unchanged. It computes the fingerprint from the ICE, adds the loop to the map of what runs next, and adds the loop's runner and checker settings, with its evidence turned on.
- It runs the loop linter until it passes, then clears any component linter error in the loop's own files.
- It tells the person to check the loop principles the linter does not check yet by hand (fn-check-loop-principles).
- In review mode it reports gaps and changes nothing. With no person reachable, it records that approval was assumed.
- Examples, in different kinds of project:
  - In a shop's harness repository, the technical lead builds a loop that runs three plays to turn a prototype into business intents. The loop holds its plays, its first questions and a checker on another model, and the loop linter passes.
  - In a hospital's harness, a developer asks for a loop step that writes a summary page. The builder says it is real work that belongs in a play, and stops.
  - In a logistics firm's harness repository, one play the loop names does not check a loop contract. The builder names it, and the loop is not built until the play is changed through /edit-play.
- How it meets the capability: the capability's line names "your own plays, loops, sub-agents and skills", and every loop built here is the one shared run plus its own values.

Status: built, in /create-loop, with the loop linter; one loop is built with it, the Discovery loop, still under its old name /complete-discovery. Not built, or open:
- It writes into Garura's source folders, the loop's folder and the settings file, so it runs only in a repository laid out like Garura's source (fn-harness-in-own-repo).
- It does not ask what starts the loop, and the loop linter does not check loop principles 1, 3, 4, 5 and 8 (#699, the loop builders check the loop principles; fn-check-loop-principles).
- No loop runs in a harness repository: "a harness repo builds loops but runs none".
- /create-loop is written by hand and has no ICE of its own.

## Inputs / Outputs
- In: the person's intent for the loop, or a loop ICE that exists.
- In: the plays the loop names, and whether each checks a loop contract and reads each key handed to it.
- In: the Shared Loop Run, the shared close, the compiled-loop example and the shared run's scripts.
- Out: the loop's folder: its ICE source, its compiled `SKILL.md`, its stop-condition file and its stamped scripts, with the fingerprint in its metadata.
- Out: the loop's entry in the map of what runs next, and its runner, checker and evidence settings.
- Out: the loop linter's report; in review mode, a table of what passes and what has a gap, and no change.

## Rules & behavior
- A loop does no work of its own. The reason: "A loop does no work of its own.", and "If a wished-for step is real work (writing a doc, judging a design), it belongs in a play: say which play, or that one is missing, and stop."
- Every play a loop names runs inside a loop. The reason: "Every play a loop names must run inside a loop. Fix the play, not the loop."
- Each input comes from the loop. The reason: "Every input comes from the loop — the source, the person's write-up or the questions — never from another play's output"
- A loop holds only its own values. The reason: "So a loop is small: its own values, and a pointer to the run every loop shares."
- The shared run and the shared close are pointed to. The reason: "Never copy the shared run's steps or the shared close into a loop; point to them."
- The shared run's scripts are stamped unchanged. The reason: "A rebuild copies them again, so a loop never drifts from the shared run."
- A loop always has a Done means. The reason: "A loop always has a Done means, baked into `stop-condition.yaml`."
- The checker judges the outputs only. The reason: "It judges the loop's goal, constraints and Done means against the loop's outputs only"
- A loop always records its evidence. The reason: "a loop always records its evidence"
- The fingerprint is computed. The reason: "The fingerprint: run `shasum -a 256 reference/ice.md` and paste the digest. Never invent one."
- The loop linter passes first. The reason: "Run `lint_loop.py` and clear every gap before calling the loop built."
- With no person reachable, the approval is recorded as assumed. The reason: "With no person reachable, state each assumption and record that approval was assumed."
- Not decided: where /create-loop writes a loop and its settings in a team's own repository, once a new ADR changes ADR 055 section 5.

## Acceptance criteria
- Given a loop ICE with three plays that each check a loop contract, when /create-loop builds the loop, then its `SKILL.md` holds the Shared Loop Run's anchor lines with the loop's own values between them, its stop-condition file holds its Done means, its scripts match their sources byte for byte, its fingerprint is the hash of its ICE, its settings hold its runner and checker with evidence on, and the loop linter passes.
- Given a wished-for step that writes a page, when the loop is built, then the builder names the play it belongs in, or says one is missing, and stops.
- Given a play that does not check a loop contract, when the loop names it, then the loop is not built.
- Given a key handed to a play that the play does not read, when the loop is built, then the key is not handed.
- Given a team's repository with Garura installed and no Garura source folders, when the technical lead builds a loop there, then it is written where the installed layout keeps loops. This is not built.

## Out of scope
- Running a loop, its rounds, its checker and its brief. Run plays as loops, in Orchestration, owns them.
- Changing a loop that exists. Change a loop through its ICE (fn-change-loop) does it.
- Checking the loop principles the linter does not check yet. Check a loop against the loop principles, including what starts it (fn-check-loop-principles) is to do it.
- The loop settings themselves and their defaults. Settings, in Standards, structure, settings and memory, owns them.
- The loop names and the naming rule. Standards, in Standards, structure, settings and memory, owns them.
- The plays each loop runs and what they write. The transition intents own them.

## Sources
- .garura/project/issues/1021/context/capabilities.md, lines 116-117, the product owner on 2026-11-11: "You can keep building your harness with your own plays, loops, sub-agents and skills, in a consistent way."
- core/components/plays/create-loop/SKILL.md, lines 22-24, 51-56, 71-72, 82-84, 92-93, 147-149, 163, 196-202: "So a loop is small: its own values, and a pointer to the run every loop shares.", "A play that cannot is fixed first, through its own ICE and `/edit-play`; the loop does not work around it;", "If a wished-for step is real work (writing a doc, judging a design), it belongs in a play: say which play, or that one is missing, and stop.", "With no person reachable, state each assumption and record that approval was assumed.", "Every input comes from the loop — the source, the person's write-up or the questions — never from another play's output", "It judges the loop's goal, constraints and Done means against the loop's outputs only", "A rebuild copies them again, so a loop never drifts from the shared run.", "The fingerprint: run `shasum -a 256 reference/ice.md` and paste the digest. Never invent one.", "a loop always records its evidence", "A loop does no work of its own.", "Never copy the shared run's steps or the shared close into a loop; point to them.", "Every play a loop names must run inside a loop. Fix the play, not the loop.", "A loop always has a Done means, baked into `stop-condition.yaml`.", "Run `lint_loop.py` and clear every gap before calling the loop built."
- core/components/plays/create-loop/scripts/lint_loop.py: the loop linter.
- core/components/loops/complete-discovery/: the one loop built.
- core/components/plays/install-garura/scripts/install.py, line 265: "a harness repo builds loops but runs none"
- docs/components/loops.md, line 59: "`/create-loop`, `/edit-loop` and `lint_loop.py` do not yet check principles 1, 3, 4, 5 and 8."
- .garura/product/product-os/software-delivery-planning/run-plays-as-loops/capability.md, line 69: "Out: building and changing a loop, with /create-loop, /edit-loop and the loop linter. Build your own harness, in Standards, structure, settings and memory (BI-10), owns it."
- .garura/product/product-os/software-delivery-planning/run-plays-as-loops/fn-check-loop-result/feature.md, line 63: "Build your own harness (BI-10) owns building a loop from its ICE."
- The stock-take of this intent, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 1.2, 2.1 and 2.2.
