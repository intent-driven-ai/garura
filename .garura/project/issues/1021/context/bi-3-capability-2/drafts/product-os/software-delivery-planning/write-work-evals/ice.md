## Intent
- Goal: Before the work under a chosen plan item is built, each slice under it has an eval, written from its epic, its stories and its hidden file, that says from the outside, on the slice's surface, whether every goal and expectation of its stories is met and no failure condition happens, and no part that builds the work is given it.
- Limit: An eval is written only from the epic with its map of features to stories, the stories and the hidden file; never from an ICE page, the usage guide or the code. Only the hidden file is written from the "Fails if" lines of the ICE.
- Limit: Every step is a sentence of the step library of the slice's kind of surface and every result is exact; there is no score, and the eval passes only when every scenario passes.
- Limit: A scenario that is there is never changed or deleted; a later run only adds.
- Limit: Evals are written only in the plan's evals folder, and nothing is kept before the product owner's typed yes on a summary that never shows the eval.
- Limit: The eval's rules, templates and step libraries come from memory through the memory tool; a new or grown step library is used only after a person approves it as a memory update; nothing comes from what the AI agent knows by itself.
- Fails if: A goal or an expectation of a story under the chosen item, or a failure condition in its hidden file, has no scenario and no Untestable line with its reason.
- Fails if: An eval, the hidden file or the evals folder is given to, or named in the inputs of, a part that builds the work, or a build session read the evals folder and its evidence holds no flag.
- Fails if: A scenario that was there changed or went away.
- Fails if: An eval was written from an ICE page, the usage guide or the code, or holds a way back or a handoff text.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the chosen item and the plan file that holds it, the epic with its map of features to stories, the stories' goals, expectations and Context guidance, the "Fails if" lines of each feature's two ICE for the hidden file, the slice's surface, the eval rules, the two eval templates, the step library of the slice's kind of surface, the eval files the slice already has, and each build run's evidence and session ledger.
- Never read: the usage guide and the code; and, when an eval is written, any ICE page.
- Persona: the product owner, who sees a summary of each eval, never the eval itself, and trusts a pass only when the build aimed at what was asked.
- Scope: In: writing the evals and the hidden file of the work under a chosen item before it is built, updating them as the work changes, the step library of each kind of surface, and the checks that no build was given or read the evals. Out: choosing and gathering the work, the slice, the plan and its work items, the design, the code-level tests and the code, the usage guide, running the evals and the verdict, the surfaces, and the ICE itself.

## Expectation
- Scenario: The technical lead of a team's task tool, a command a person runs in a terminal, names the epic of a slice with two stories. Its hidden file holds three failure conditions. Two story files and a slice file are written in the plan's evals folder: each goal, expectation and failure condition has a scenario, and one expectation that needs a wait longer than the time limit is under Untestable with its reason. The product owner sees the counts and the untestable line, never the eval, and types yes. Later, the inputs of the parts that build the two stories name no eval, and the build's evidence holds no flag.
- Done means: Someone other than the one who wrote the evals checks each story file against its story and the hidden file, and finds every goal, expectation and failure condition covered by a scenario or named as untestable, every step a sentence of the library, every result exact, and no scenario that changed or went away.
- Done means: Someone other than the builder runs the checks over the build's inputs and its session ledger, and finds no input that names the evals and a flag for each read of their folder.
