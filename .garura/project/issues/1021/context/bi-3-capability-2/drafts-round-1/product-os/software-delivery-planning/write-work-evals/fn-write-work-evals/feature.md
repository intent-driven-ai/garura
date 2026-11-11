# Feature: Write the evals of the chosen work before it is built

## What it does
For the stories under the item a person names from the plan, this feature writes their evals before their build starts, so the work is later checked from the outside against what it was asked to do.
- The chosen item may be an epic, a feature item, which groups some stories inside one epic, or a story. Each epic stands for one slice, an ordered group of features that one person can test end to end on one surface. A slice has one eval, kept in plain text in the plan's evals folder, beside its hidden file of failure conditions.
- For each story under the chosen item, it writes one story file. Its title is the story. It holds a scenario for each goal and each expectation of the story, and, for each failure condition of the story's feature in the hidden file, a scenario that shows the failure does not happen. Each scenario names what it covers, and the file keeps the exact words of each story line it covers.
- It writes the slice file: the epic's stories in build order, the kind of surface, a time limit for each scenario, the rule for a pass, the names the usage guide will map, and the stories' Context guidance, the part of a story that says what to read, what never to read, who the work is for, and what is in and out.
- Each step is a sentence of the step library of the slice's kind of surface, and each result is exact. What only the build will make, such as a command or a page, is a name in square brackets. What it cannot test yet goes under Untestable, with the reason.
- It reads only the epic with its map of features to stories, the stories, and the hidden file. It never reads an ICE page, the usage guide or the code. An ICE is the agent's intent for one capability or feature.
- The product owner sees a short summary, never the eval: each story's counts, each item that cannot be tested yet with its reason, and each slice that got no eval with why. Nothing is kept before the product owner's typed yes.
- How it meets the capability: this is where the evals are written, before anything is built, so a later pass means the work did what its stories ask. In the product owner's words: "making evals is going to be critical because those are the evals that are going to be used to check its own work".

Status: built, started from a business intent today. What differs from this page:
- The eval play, /shape-eval, writes the eval of every slice in a business intent's plan, after the plan play made the plan. It does not start from an item a person names. It has run once, on one plan.
- It reads the epic and its stories from the tracker. The plays that read the plan must not run until the Agent-work tool, the one tool that knows the tracker, lands (#1023).
- A slice whose epic, stories or hidden file is missing, or whose kind of surface has no step library, gets no eval, and the summary names it with the reason.
- Findings left from the review of the eval play wait to be fixed (#912).
- No eval has run: the runner and the usage guide are not built.

## Inputs / Outputs
- In: the ID of the chosen item, named by a person, and the plan file that holds it.
- In: the epic of the slice the chosen item sits in, with its map of features to stories, and each story under the chosen item, read from the tracker through the tool that knows it: its goals, limits, expectations and Context guidance.
- In: the slice's hidden file: the surface the slice is tested on, and each feature's failure conditions with their ids.
- In: the step library of the slice's kind of surface, the two eval templates and the eval rules, from memory through the memory tool.
- In: the eval files the slice already has.
- Out: for each story under the chosen item, its story file in the slice's evals folder.
- Out: the slice file, in the same folder.
- Out: a summary for the product owner, with no scenario in it.

## Rules & behavior
- Before the build. The evals of the stories under the chosen item are written before their build starts. The reason, in the product owner's words: "Write the evals that will check the work, before anything is built, never shown to the builder."
- One eval for each slice, and one story file for each story. The reason: a slice "has one eval, one hidden file and one usage guide, also when two plans hold it", and a file for each story shows which story fails.
- A chosen epic gets its slice's whole eval. A chosen feature item or story gets the story files of the stories under it, and the slice file; the epic's other stories get theirs when they are chosen. The reason, in the product owner's words: "I should say an ID, and anything under it should all be planned."
- It reads the work items itself, from the plan file and the tracker, and never the builder's part that gathering hands on. The reason: the eval stays apart from what the builder receives, as the approved gathering page says it "reads the work items itself".
- From the outside, on the surface. A scenario does what a tester does on the slice's surface and checks what they see. When the surface is a play, a scenario runs the play in a test project. The reason: the eval checks the work as a person meets it.
- Every step a sentence of the library, every result exact, and what only the build will make a name, never a guess. The reason: the eval later runs with no agent and gives the same answer on every run.
- Every goal, expectation and failure condition has a scenario or an Untestable line with its reason, and a scenario covers only what its story or the hidden file says. The reason: a gap is then never silent, and the eval checks nothing the work was not asked to do.
- No way back and no handoff text in an eval. The reason: the way back stays in the hidden file, and only a failing eval writes the handoff.
- The product owner sees a summary, never the eval, and nothing is kept before the typed yes. A stop leaves no file. The reason: a person judges the counts and the gaps, and a script checks each step and result.
- No copy of the eval or of the hidden file stays in short-term memory, the issue's own folder where a run keeps its working files, after the run. The reason: the build collects its context into short-term memory, so a copy left there could reach a builder.
- Not decided: how a build that starts before its eval is written is shown to a person. Nothing stops it.
- Not decided: when the chosen item is a chore, a bug or a spike, whether anything is written. They have no goals or expectations of their own.
- Not decided: how each name the eval uses is matched in the usage guide, when the builder who writes the guide never sees the names.

## Acceptance criteria
- Given an epic whose slice is on the command line, with three stories and the slice's hidden file, when the epic is chosen, then the evals folder holds a story file for each story and one slice file, and each goal, expectation and failure condition has a scenario or an Untestable line with its reason.
- Given the same plan, when only one story is chosen, then its story file and the slice file are written, and no other story file.
- Given a story file, when it is read, then every step is a sentence of the step library, every result is exact, and no step holds a guessed command, page address or field.
- Given a slice whose surface is a mobile app and no mobile step library, when its work is chosen, then it gets no eval, and the summary names it with the reason.
- Given a run, when the product owner types stop at the summary, then no eval file is written.
- Given a finished run, when its reads and its short-term memory are checked, then it read no ICE page, usage guide or code, and no copy of the eval or the hidden file is left.

## Out of scope
- Writing the hidden file of failure conditions. Write what must never happen, and the way back from each (fn-write-failure-conditions) does it.
- Changing an eval after the work changes. Update the evals as the work changes (fn-update-evals) does it.
- A step library for a new kind of surface. Add the steps an eval may use on a kind of surface (fn-add-eval-steps) does it.
- Gathering the work under the chosen item, and splitting each story into the builder's part and the test writer's part. Gather the work under a chosen plan item does them.
- Running the eval, the verdict and the handoff plan. Test with evals the builder never sees, in Code → Validation, does them.
- The usage guide, which maps each name to the real thing. Build the work test first delivers it with the build.

## Sources
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "making evals is going to be critical because those are the evals that are going to be used to check its own work", "Write the evals that will check the work, before anything is built, never shown to the builder."
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/bi-3-capability-1b/page-approvals.md: "The entire tree needs to be handled. I should say an ID, and anything under it should all be planned."
- .garura/product/product-os/software-delivery-planning/gather-work-under-item/capability.md: "Write the evals that check the work owns it, and it reads the work items itself."
- core/components/plays/shape-eval/SKILL.md: "It reads only the epic, its stories and the hidden file. It never runs the eval"
- core/components/plays/shape-eval/reference/ice.md: "Each scenario is written from the outside: what a tester does on the slice's surface and what they see.", "When the surface is a play, the scenario runs the play on a test project."
- core/components/plays/shape-eval/reference/ice.md: "A slice whose epic, stories or hidden file is missing gets no eval; the run names it and says why.", "A slice whose surface kind has no step library yet gets no eval; the run names it and says why."
- core/components/plays/shape-eval/reference/ice.md: "The person sees a short summary, never the eval itself", "A stop leaves no file.", "No copy of the eval or of the hidden file stays in the run's short-term memory after the run"
- core/components/plays/shape-eval/reference/ice.md: "What only the build will make (a command, a page address, a field) is written as a name", "The eval holds no handoff text, and no recovery"
- core/components/skills/author-slice-eval/SKILL.md: "Read only the copies.", "Every step is a library sentence; every Then is exact; there is no score.", "Each scenario covers only what its story or its feature's hidden-file entry says."
- core/components/agents/evals-engineer.md: "When one is missing, stop with `step_failure` and name it. Do not call the skill: a part of", "an eval is worse than no eval."
- core/components/plays/shape-eval/scripts/gather_eval.py: "It never reads an ICE page, the usage guide, the code or the product model (C1)."
- git commit 36251ed6, the one run of the eval play: "feat(eval): write the eval of business intent"
- docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md: "Each story has its own file, so a person or a runner can see which story fails.", "The runner that runs the eval is not built yet (#819). Until then an eval is written but never run."
- docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md: "The names in square brackets depend on the usage guide."
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md: "The build writes the usage guide. It is the eval's only way into the built product."
- GitHub #1023 (open): "Until this lands, `/shape-slice`, `/shape-plan` and `/shape-eval` read an intent's issue from the wrong repo, so they must not run and no plan is rebuilt."
- GitHub #912 (open): "The findings the reviews of PR #900 left open"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "It has one eval, one hidden file and one usage guide, also when two plans hold it.", "The build delivers its usage guide with the slice, in the guides folder beside the evals folder but not in it, so the builder writes the guide and never sees the eval."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "When the build play runs, its context sub-agent reads the story's Context guidance, collects the context, and puts it in the issue's short-term memory"
- standards/rules/eval-format.md, in Phoenix memory: "Each Then is an exact result a tester can see. There is no score", "lists, one line each with its tag, every goal, expectation or failure condition that has no"
- standards/templates/eval-slice.md, in Phoenix memory: "The eval passes only when every scenario of every story below passes. There is no score."
