# Eval: slice sl-intent-to-design — epic #794

Plan 788, business intent "Agents design the work, then build it through plays and a loop" (#788).
Surface: the Claude Code command line
Surface kind: command-line
Time limit for each scenario: 1800 seconds
Written by /shape-eval from epic #794, its stories and the slice's hidden file.

## Pass rule

The eval passes only when every scenario of every story below passes. There is no score. A scenario that runs past the
time limit fails.

## Stories, in build order

1. Story #795 (fn-795) — eval.fn-795.feature.md
2. Story #818 (fn-818) — eval.fn-818.feature.md
3. Story #798 (fn-798) — eval.fn-798.feature.md
4. Story #898 (fn-898) — eval.fn-898.feature.md

## Names

The usage guide (`guides/intent-to-design.md`) maps each name to the real thing the build made.

The test project is a small project made for the eval. Its business intent 788 is served by one slice. That slice has two features. The two features share one capability. Each feature has one goal and one expectation in its story. The hidden file holds the failure conditions of each feature and of the capability. The words "eval" and "hidden" do not appear in the text of the features or of the capability.

A command in a name is a small command of the test project. It reads files and writes its answer to a file. It uses no judgment.

Setups (a Given step):

- [a test project with business intent 788, a model and memory that answer every question, and an empty tracker]: the test project with no slice yet. Every question the play could ask is already answered.
- [a test project whose business intent 788 could be tested on two surfaces]: the same test project, but its intent could be tested on two different surfaces.
- [a test project whose business intent 788 has no surface that a person can test]: the same test project, but its intent has no surface that a person can test.
- [a slice that already serves business intent 788]: the test project already has one slice for the intent.
- [a test project with business intent 788 served by a slice, an empty tracker and no plan file]: the test project after /shape-slice. It has the slice and the hidden file. The tracker has no epic and no story. There is no plan file.
- [a test project where a model page of the slice is missing]: the same test project, but one domain page of the product model is missing.
- [a test project that holds #717 and its partner, served by slices, with the trees that were filed by hand on 2026-10-21]: a test project that has business intent #717 and its partner, each served by a slice and with no plan file. It also holds the tree of each plan as it was filed by hand on 2026-10-21.
- [a test project where /shape-plan has run for business intent 788, with a hidden file]: the test project after /shape-plan. It has the plan file, one epic, two stories and the hidden file. The slice's evals folder holds the hidden file only.
- [a build play whose inputs name the evals folder]: a build play in the test project that lists the plan's evals folder as an input.
- [a build play whose inputs name the eval]: a build play in the test project that lists the eval as an input.
- [a build play whose inputs name the hidden file]: a build play in the test project that lists the hidden file as an input.
- [a build play whose inputs are the stories of the slice]: a build play in the test project that lists the two stories of the slice as its inputs and nothing else.
- [a build run with evidence that holds the session stamp of one build session and no flag]: a record of a build run in the test project. Its evidence holds the stamp of one play session. It has no flag. No real build ran.
- [a build run with evidence that holds the session stamp of a build skill and no flag]: the same record, but the stamp is the one of a build skill.
- [a build run with evidence that holds the session stamp of a build agent and no flag]: the same record, but the stamp is the one of a build agent.
- [a build run with evidence that holds the session stamp of a context sub-agent that a build started and no flag]: the same record, but the stamp is the one of a context sub-agent that a build started.

Commands (a When step):

- [the command that saves the list of new files outside the product model to a file]: a command that writes the new files of the last run, outside the product model, to a file. It leaves out the play's own records in the issue folder.
- [the command that saves the tracker's issues of business intent 788 to a file]: a command that writes the epics and stories of business intent 788 from the tracker to a file.
- [the command that saves the list of new files outside the slice's evals folder to a file]: a command that writes the new files of the last run, outside the slice's evals folder, to a file. It leaves out the play's own records in the issue folder.
- [the command that saves the recovery check of the hidden file to a file]: a command that reads the hidden file. For each failure line, it counts the recovery parts that follow it. A recovery part is complete when it holds a symptom, a guide for the way back and the name of who fixes it. The command writes the number of failure lines it read, and the list of failure lines that do not have exactly one complete recovery.
- [the command that saves the lines that the stories and the plan file share with the hidden file to a file]: a command that compares line by line the text of the tracker export file and of the plan file with the text of the hidden file. It skips empty lines. It writes the list of lines that are the same in both.
- [the command that checks the steps of the story files against the step library]: a command that reads each story file of the slice's eval. It checks that each step is a sentence of the step library of the slice's surface kind. It ends with exit code 0 only when all steps match.
- [the command that saves the tag check of the first story file to a file]: a command that reads the first story file and the story's goals, expectations and failure lines. It writes four things: the number of story lines it checked, the number of those lines that have a scenario, the list of lines that have no scenario and no Untestable line, and the list of tags in the file that are not a goal, an expectation or a failure line of that story. A tag counts for a scenario only when it stands on a tag line above a scenario heading.
- [the command that saves the tag check of the second story file to a file]: the same command, for the second story file.
- [the command that makes the handoff plan for a failed check of the first failure condition]: a command that makes the eval report that its check of the first failure condition failed, and that writes the handoff plan for it.
- [the lint check over the build plays]: the lint command that checks the inputs of every build play. It ends with exit code 1 when an input names the evals folder, the eval or the hidden file, and then prints the name of that build play.
- [the ledger check over that build session]: the check that reads the ledger of the build session and writes a flag in the build run's evidence for each read of the plan's evals folder. It never stops a build.
- [the command that saves the ledger of the last play run to a file]: a command that writes the list of files the last play run read to a file.
- [the shape-plan command for the partner of #717]: the command "/shape-plan" with the number of the partner of #717.

Files and folders:

- [the spine file]: the file of the product model that lists the slices.
- [the hidden file]: the file of failure conditions and recoveries that /shape-slice writes in the slice's evals folder.
- [the path of the hidden file]: the path of the hidden file, as text.
- [the slice's evals folder]: the folder .garura/project/plans/788/evals/ and the slice's own folder in it.
- [the plan file of business intent 788]: the plan file of the intent, in .garura/project/plans/.
- [the plan file of #717]: the plan file of business intent #717, in .garura/project/plans/.
- [the plan file of the partner of #717]: the plan file of the partner of #717, in .garura/project/plans/.
- [the question record]: the file where /shape-slice keeps its questions and the answers.
- [the tracker export file]: the file that the tracker command writes.
- [the list of new files outside the product model]: the file that the new-files command writes. The test project expects one entry: the hidden file.
- [the list of new files outside the slice's evals folder]: the file that the new-files command writes. The test project expects no entry.
- [the recovery check file]: the file that the recovery check command writes.
- [the shared lines file]: the file that the shared-lines command writes.
- [the tag check file of the first story]: the file that the tag check command writes for the first story file.
- [the tag check file of the second story]: the file that the tag check command writes for the second story file.
- [the slice file of the eval]: the file eval.<slice-id>.md in the slice's evals folder.
- [the eval file of the first story]: the story file of the first story of the test project's slice, in the slice's evals folder.
- [the eval file of the second story]: the story file of the second story of the test project's slice, in the slice's evals folder.
- [the handoff plan that the eval writes]: the file where the eval writes its handoff plan when a check fails. The stories do not name it. The usage guide names it.
- [the ledger of the last play run]: the file that the ledger command writes.
- [the ledger of that build session]: the file that lists what the build session read.
- [the evidence of that build run]: the evidence file of the build run. The ledger check writes the flags in it.
- [the inputs of that build play]: the file where the build play lists its inputs.
- [the path of the story of the first feature]: the path of the story of the first feature, as text.
- [the path of the story of the second feature]: the path of the story of the second feature, as text.
- [the folder of the test project's code]: the folder in the test project that holds its code.

Fields and parts of a file:

- [the slices field of the spine file]: the list of slices in the spine file.
- [the feature order field of the slice]: the list of the slice's features in build order.
- [the surface field of the slice]: the surface that the slice names.
- [the surfaces field of the slice]: the list of surfaces that the slice names.
- [the tester field of the slice]: the person who tests the slice.
- [the link from the slice to business intent 788]: the text in the spine file that joins the slice to the intent.
- [the questions field of the question record]: the list of questions in the question record.
- [the issues field of the tracker export file]: the list of all issues in the tracker file.
- [the epics field of the tracker export file]: the list of epics in the tracker file.
- [the stories field of the tracker export file]: the list of stories in the tracker file.
- [the epics field of the plan file]: the list of epics in the plan file.
- [the stories field of the plan file]: the list of stories in the plan file.
- [the tree field of the plan file]: the tree of epics and stories in the plan file.
- [the files field of that list]: the list of files in a new-files file.
- [the failure lines checked field of the recovery check file]: the number of failure lines that the recovery check read.
- [the failure lines without exactly one complete recovery field of the recovery check file]: the list of failure lines that have no recovery, an incomplete recovery or more than one recovery.
- [the lines field of the shared lines file]: the list of lines that the shared-lines command found in both files.
- [the story lines checked field of the tag check]: the number of goals, expectations and failure lines of the story that the tag check read.
- [the number of lines with a scenario field of the tag check]: the number of those lines that have a scenario in the story file.
- [the lines without a scenario and without an Untestable line field of the tag check]: the list of story lines that have neither a scenario nor an Untestable line.
- [the tags outside the story field of the tag check]: the list of tags in the story file that are not a goal, an expectation or a failure line of that story.
- [the flags field of the evidence]: the list of flags in the evidence of the build run.
- [the heading of the first feature's entry in the hidden file]: the heading line of the first feature in the hidden file.
- [the heading of the second feature's entry in the hidden file]: the heading line of the second feature in the hidden file.
- [the Fails if line of the first feature]: the Fails if line of the first feature, word for word.
- [the Fails if line of the second feature]: the Fails if line of the second feature, word for word.
- [the Fails if line of the capability of both features]: the Fails if line of the shared capability, word for word.
- [the name of the first feature]: the name of the first feature, word for word.
- [the name of the second feature]: the name of the second feature, word for word.
- [the name of the capability of both features]: the name of the shared capability, word for word.
- [the line that names the first feature in its story]: the line of the first feature's story that gives the id of the feature.
- [the line that names the second feature in its story]: the line of the second feature's story that gives the id of the feature.
- [the ICE of the first feature as the product model gives it, without its Fails if lines]: the text of the first feature's ICE page in the product model, with its Fails if lines taken out. The test project keeps this text apart from the plan file.
- [the ICE of the second feature as the product model gives it, without its Fails if lines]: the same, for the second feature.
- [the ICE of the capability of both features as the product model gives it, without its Fails if lines]: the same, for the shared capability.
- [the first failure condition of the hidden file]: the first failure condition line of the hidden file, word for word.
- [the second failure condition of the hidden file]: the second failure condition line of the hidden file, word for word.
- [the id of the first failure condition of the hidden file]: the id that the hidden file gives to the first failure condition.
- [the id of the second failure condition of the hidden file]: the id that the hidden file gives to the second failure condition.
- [the tag of the failure condition of the first feature]: the tag of the first feature's failure condition in its story file, for example @F1.
- [the tag of the failure condition of the second feature]: the tag of the second feature's failure condition in its story file.
- [the title of the scenario that checks the first failure condition]: the title of the scenario in the first story file that has the tag of the first failure condition.
- [the title of the scenario that checks the second failure condition]: the title of the scenario in the second story file that has the tag of the second failure condition.
- [the flag that names the read of the eval]: the flag text that the ledger check writes for a read of the eval.
- [the flag that names the read of the hidden file]: the flag text that the ledger check writes for a read of the hidden file.
- [the flag that names the read of the plan's evals folder]: the flag text that the ledger check writes for a read of the plan's evals folder.

Values that the test project expects, and texts that a Given step writes:

- [the feature order that the test project expects]: the two features of the test project's slice, in their build order.
- [the surface that the test project expects]: the surface that the test project's slice must name.
- [the tester that the test project expects]: the person who must test the test project's slice.
- [the reason that no surface can be tested]: the text the play prints when it finds no surface that a person can test.
- [the number of failure lines that the test project expects]: the number of failure lines in the test project's hidden file.
- [the number of lines of the first story that the test project expects]: the number of goals, expectations and failure lines of the first story and its feature.
- [the number of lines of the second story that the test project expects]: the same, for the second story.
- [the tree of #717 that was filed by hand on 2026-10-21]: the tree of the plan of #717 as a person filed it by hand on 2026-10-21.
- [the tree of the partner of #717 that was filed by hand on 2026-10-21]: the same, for the partner of #717.
- [the name of that build play]: the name of the build play that the Given step set up.
- [a read of the plan's evals folder]: one line in a ledger that says the session read the plan's evals folder.
- [a read of the eval in the plan's evals folder]: one line in a ledger that says the session read the eval.
- [a read of the hidden file in the plan's evals folder]: one line in a ledger that says the session read the hidden file.
- [two reads of the plan's evals folder, one of the eval and one of the hidden file]: two lines in a ledger, one for each read.
- [a read of the story of the first feature and a read of the story of the second feature]: two lines in a ledger that say the session read the two stories of the slice. It reads nothing in the evals folder.

## Context

For the running eval:

- Read: the eval files of this slice, the usage guide that maps the names above, and the recovery parts of the hidden file.
- Persona: the product owner, who wants proof that the business intent is met.
- In: the test project, the plays /shape-slice, /shape-plan and /shape-eval run on it, the lint check over the build plays, and the records of build sessions that the scenarios write themselves.
- Out: a real build. This slice does not run one (#819).
