# Feature: Run any loop the same way

## What it does
When a person runs a loop with its goal, the loop takes the same steps whatever loop it is: it checks it can run, opens one change, asks first only what it needs to start, writes one contract for every play, reads its source once, and runs its plays in rounds, deciding after each round whether it is done, goes again, or asks; then it hands the result to the checker and lands its change, so every loop behaves the same way and a person can tell what it will do.
- The steps are written once, in the Shared Loop Run. A loop holds only its own values, between two anchor lines: its plays in the order they run, its questions, the documents it asks for, the source it reads, its settings keys and how it ends.
- Pre-flight, before anything is opened. A script reads the settings and the installed plays and returns the facts. It halts the loop when a play is missing, a play cannot run inside a loop because it checks no loop contract, a skill of the knowledge step is missing, the runner or the checker kind is unknown, or a sub-agent checker names no model. Then the loop runs its own pre-flight rows, such as the Discovery loop's check that the prototype runs.
- Open the change. The opening play runs as a sub-play: one issue and one branch for the whole loop. Everything the loop and its plays write goes under that issue.
- Questions first. Before any play runs, the loop asks only what it needs to start, in plain words, one at a time, and waits for typed answers. It records where each answer came from. A loop that names documents gets them here and keeps each exactly as given, such as the Discovery loop's write-up in five parts. The loop never writes the document itself, and it reads no memory itself.
- One contract for every play. A script writes it from the loop's facts, the plays' inputs and the answers, and checks it before any play gets it. Each play reads its own inputs and answers from it. Inside a loop a play opens nothing, does not wait at a conditional checkpoint, and writes a question it cannot answer for the loop instead of stopping.
- The source, read once. A loop that names a source captures it once and has it walked once, and every play reads that one capture.
- Rounds. Round one runs every play, in turn. Each play runs with the runner the settings name:
  - a sub-agent the loop waits for in the foreground, the default;
  - or a headless session the loop starts and waits for.
- After each play, a script checks that the play's done check was written by this run and reads held, and another commits the play's run files on the loop's branch and checks that nothing outside the issue's folder is left changed.
- After each round, the product-os-keeper agent finds and closes the product model's gaps with two skills, and the round is committed once. Then a script decides:
  - done: no question is open and the gaps are closed, so the loop goes to its checker;
  - again: the model, the open questions or the gaps moved and the round limit is not reached, so the next round runs only the plays given work, each on exactly that work;
  - ask: a whole round closed nothing new, or the round limit is reached, three rounds by default, so the loop goes to its knowledge step and its brief.
- The end. The loop runs the change plays to land its change, the merge keeping the person's typed yes, then its close. A loop always records its evidence: its own evidence setting, which the loop builder turns on, wins over the global one.
- A halted loop closes with its reason, and its run stays under the issue, so a run again picks up from the first play not done and reuses what was done.
- Where it stops a person with no way past: a failed pre-flight, a play that misses its done check, and files left changed outside the issue each halt the loop. The person can only fix the cause and run the loop again; nothing lets them pass the halt and record what is owed.
- Examples, in different kinds of project:
  - In a clinic's booking app, the product owner runs the Discovery loop on a working prototype. It asks where the prototype is and how it starts, gets the write-up, opens one issue and one branch, and runs its three plays in rounds on that branch.
  - In a bank's payments service, a loop's pre-flight finds one of its plays not installed and halts before any issue or branch is made.
  - In a team's planning tool, a loop halted when its second play missed its done check is run again. It starts from the second play and keeps the first play's work.
- How it meets the capability: this is "a loop runs its plays until the goal is met": every loop runs on one issue and one branch, asks first, runs its plays in rounds, and decides after each round whether the goal is met or a person must be asked.

Status: built, in the Shared Loop Run and its scripts, used by the one loop built, the Discovery loop. It has run on the Argus mockup and in a test project. Not built, or open:
- A round's plays run one after another. Run a round's plays side by side (fn-run-plays-side-by-side) would run them at once, and it is not built.
- Only a person starts a loop, and no single record tells the next round what was tried and whether it worked. Start a loop from a schedule or a hook, and keep a record across rounds (fn-start-loop-on-trigger) adds them (#699, the loop builders check the loop principles).
- No part of a loop says what context each play gets, or how it is trimmed across rounds (#699, the loop builders check the loop principles).
- The step after each round closes the product model's gaps. A loop whose plays build or test code has no step of its own there yet.
- No loop is installed in Garura's own repository, so none runs there.

## Inputs / Outputs
- In: the person's goal and what the loop starts from, such as a working prototype, given with the loop's command or asked for first.
- In: the person's typed answers to the loop's questions, and any documents the loop asks for.
- In: the loop's settings: its runner, its checker, its round limit and its evidence setting.
- In: the installed plays the loop runs, each of which checks a loop contract.
- Out: one issue, one branch and one change, with every file the loop and its plays write under that issue.
- Out: the loop contract, written again at each round, and the answers with where each came from.
- Out: for each play, its done check and its commit record.
- Out: for each round, the gap records, the round's commit, and the round record: done, again or ask, why, the questions left open, the gaps left, and the plays the next round runs.
- Out: the loop's evidence record and its close, or a halt with its reason.

## Rules & behavior
- One run for every loop, written once. The reason: "So the run is the same for every loop and lives once", and a loop's steps between its plays "are run steps. They are not rules about the product."
- One issue and one branch for the whole loop. The reason: "Everything the loop and its plays write goes under that issue", so the work can be traced to one issue and reviewed as one change.
- Pre-flight before anything is opened. The reason: a loop that cannot run leaves nothing behind: "no issue or branch exists for a prototype that does not run."
- Questions first, and only what the loop needs to start. The reason: "only what the loop itself needs from the person to start"; the plays' own questions depend on what the source shows.
- The loop reads no memory itself. The reason: "what memory can answer is for its plays' agents, through the memory tool."
- No play takes another play's output as its input. The reason: when the plays ran in a chain, "One error at the top spread to every node below it."
- Inside a loop a play opens nothing, and a pinned checkpoint is never put off by the contract. The reason: "The loop opens and lands the change.", and "A pinned checkpoint is never deferred by a contract."
- A play's done check counts only when this run wrote it. The reason: "a verdict older than the play's start is left from an earlier run and proves nothing."
- The tree is clean before the next play starts. The reason: the loop halts on files left changed "so the next play does not start on an unclean tree."
- After each round, the model's gaps are closed and the round is decided. The reason, in the product owner's words: "The whole point of a drive is that these loops are closed".
- The next round runs only the plays given work. The reason: the round record names the plays and their work, and "only those plays run".
- A round limit, three by default. The reason: "More rounds cost more time and tokens.", and "The round limit bounds it."
- A play runs in the foreground. The reason: "A headless session ends its turn while a background sub-agent runs, and stops it 10 minutes later."
- A loop always records its evidence. The reason: a loop "Ends with the check and an evidence record", and the settings say "A loop always records its evidence".
- A halted run picks up where it stopped. The reason: "a re-run resumes from the first play not done."
- Not on a coding agent's own never-stop loop. The reason: "that would push the decision onto the model."

## Acceptance criteria
- Given a loop whose plays are all installed and each checks a loop contract, when it runs, then one issue and one branch are opened, and every file the loop and its plays write is under that issue.
- Given a loop with a play that is not installed, when it runs, then pre-flight halts and names the play, and no issue or branch is made.
- Given a loop that names questions, when it starts, then each is asked and answered, with where the answer came from, before any play runs.
- Given a play whose done check is missing or older than its start, when the loop checks it, then the loop halts with the reason that the play is not done.
- Given a round after which a capability has no features, when the round is decided, then it reads again, and the next round runs only the play given that work, on that work.
- Given a round that closed nothing new, or the third round ended with questions open, when the round is decided, then it reads ask and the loop goes to its knowledge step.
- Given a halted loop, when it is run again, then it starts from the first play not done and keeps what was done.

## Out of scope
- Judging the loop's result. Have a checker that did not run the loop judge its result (fn-check-loop-result) does it.
- Closing the open questions and briefing the person. Brief the person only on what no play could close, and let them stop (fn-brief-open-points) does it.
- The status file. Show what a long run is doing now (fn-show-run-status) does it.
- Starting a loop from a schedule or a hook, and a record across rounds. Start a loop from a schedule or a hook, and keep a record across rounds (fn-start-loop-on-trigger) is to do it; it is not built.
- Running a round's plays at once. Run a round's plays side by side (fn-run-plays-side-by-side) is to do it; it is not built.
- What each loop's plays do and write. The transition intents, Product → Spec (BI-1), Spec → Design (BI-2), Design → Code (BI-3), Code → Validation (BI-4), Validation → Run (BI-5) and Run → Product (BI-6), own them.
- The link rules the step after each round applies. Manage the model, in Product model, owns them.
- Opening, committing, raising and merging the change, and the review it ends in. Ship every change the same way and Review what agents make (Argus), in Developer tooling (BI-8), own them.
- Building and changing a loop. Build your own harness (BI-10) owns it. The settings themselves: Settings (BI-10) owns them.
- Choosing which loop runs and when. Orchestrate agent work through planning owns it.
- A way past a halt, and the record of what is owed. Give every gate a way past owns it.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md, lines 97 and 101: "Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met.", "we are building from what already exists"
- core/components/loops/_shared/loop-run.md, lines 3-11, 45-63, 65-91, 92-102, 151-257 and 395-422: "So the run is the same for every loop and lives once", "one issue, one branch for the whole loop", "Everything the loop and its plays write goes under that issue", "only what the loop itself needs from the person to start", "what memory can answer is for its plays' agents, through the memory tool.", "A loop never writes the document itself.", "The first build runs the plays one after another, in turn", "A headless session ends its turn while a background sub-agent runs, and stops it 10 minutes later.", "so the next play does not start on an unclean tree.", "It never takes another play's output as its input", "the merge keeping its pinned human approval", "a re-run resumes from the first play not done."
- core/components/loops/complete-discovery/SKILL.md, lines 106-120 and 126-127: "no issue or branch exists for a prototype that does not run."
- core/components/loops/complete-discovery/scripts/loop_preflight.py, lines 1-23 and 114-141: "these plays cannot run inside a loop (they check no loop contract)", "the runner is unknown"
- core/components/loops/complete-discovery/scripts/write_loop_contract.py, lines 1-17: "so a play never gets a contract it would reject"
- core/components/loops/complete-discovery/scripts/check_play_done.py, lines 1-15: "a verdict older than the play's start is left from an earlier run and proves nothing."
- core/components/loops/complete-discovery/scripts/commit_run_files.py, lines 1-19: "It commits only paths under the issue folder, on the loop's branch, and never sweeps in anything someone else staged."
- core/components/loops/complete-discovery/scripts/round_state.py, lines 1-40 and 96-112: "only those plays run", "a whole round closed nothing new: what is left is the loop's"
- core/components/loops/complete-discovery/scripts/run_play_headless.py, lines 1-17: "for a loop started outside an interactive session"
- core/config.yaml, lines 119-145: "A loop always records its evidence", "max_rounds: 3", "runner: subagent"
- standards/rules/loop-contract.md, in Phoenix memory, lines 63-80: "The loop opens and lands the change.", "A pinned checkpoint is never deferred by a contract."
- docs/components/loops.md, lines 52-54: "No trigger part: schedules and hooks are not supported (#699)", "No part of a loop says what context each play gets, or how it is trimmed across rounds (#699)", "No single record tells the next round what was tried and whether it worked (#699)"
- docs/adr/029-drives.md, lines 36 and 39: "that would push the decision onto the model.", "Ends with the check and an evidence record."
- docs/adr/041-a-drive-runs-in-rounds-and-owns-its-questions.md, lines 7 and 107: "after Kickoff runs 1–5 on the Argus mockup", "More rounds cost more time and tokens.", "The round limit bounds it."
- docs/adr/043-kickoff-plays-read-independently-and-the-drive-closes-the-loop.md, the product owner on 2026-10-21, lines 16 and 20: "One error at the top spread to every node below it.", "The whole point of a drive is that these loops are closed"
- docs/adr/044-the-shared-drive-run-owns-the-steps-between-plays.md, line 36: "These are run steps. They are not rules about the product."
- core/components/plays/install-garura/scripts/install.py, line 265: "a harness repo builds loops but runs none"
- .garura/product/product-os/software-delivery-planning/specify-product/capability.md, line 48: "The work of managing the model owns the link rules."
- The stock-take of Orchestration, .garura/project/issues/1021/context/bi-9-inventory/inventory.md, sections 2.1, 2.2, 2.4 and 2.7: the run, the one loop and its test runs, the settings, and the step after each round that only a model-writing loop has.
