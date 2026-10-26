# Eval: slice sl-intent-to-design — epic #794

Plan 788, business intent "Agents design the work, then build it through plays and a loop" (#788).
Surface: the Claude Code command line; tested by the product owner.
Surface kind: command-line
Time limit for each scenario: 1200 seconds
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

The usage guide (`guides/intent-to-design.md`) maps each name to the real thing the build made. A "test project" is a
project made only for the eval, in which the plays run.

- [the test project with no slice]: a test project with the page of business intent 788 in its product model, features that have "Fails if" lines, and no slice, no plan and no eval.
- [the test project with a slice for business intent 788]: the same project, with a slice that already serves business intent 788.
- [the test project whose model and memory answer every question]: a test project where the product model and memory already answer everything that /shape-slice could ask.
- [the test project with a shaped slice]: a test project where /shape-slice 788 ran and its slice has 4 features; it has no plan yet.
- [the test project with a shaped slice and a missing model page]: the same project, with one domain or model page missing.
- [the test project with a plan]: a test project where /shape-slice 788 and /shape-plan 788 ran; the slice has 4 features and 4 stories; the plan has 1 epic.
- [the test project with clean build plays]: a test project with the build plays, and no build play, skill, agent or sub-agent input that names the evals folder.
- [the test project with a build play that names the evals folder, the eval and the hidden file]: a test project where one build play's inputs name the evals folder, the eval and the hidden file.
- [the test project with a build run that read the evals folder]: a test project with one build run whose session ledger shows a read of the plan's evals folder.
- [the test project with a clean build session]: a test project with one build run whose session ledger shows no read of the evals folder.
- [the test project with one build session that read the evals folder and one that did not]: a test project with two build runs, one that read the plan's evals folder and one that did not.
- [the shape-slice answers]: the scripted answers to the questions of /shape-slice, in order, ending with "yes".
- [the spine]: the spine file of the product model of the test project.
- [the slice record]: the record file of the slice in the product model, with its features, its intents, its surface and its tester.
- [the surface name]: the text that names the slice's surface in the slice record.
- [the tester name]: the text that names the person who tests the slice in the slice record.
- [the evals folder of the slice]: the folder `.garura/project/plans/788/evals/<slug>/` of the test project.
- [the hidden file]: the failure-and-recovery file that /shape-slice writes in the slice's evals folder.
- [a Fails if line of a feature of the slice]: the text of one "Fails if" line of a feature of the slice.
- [a line of the hidden file]: the text of one line of the hidden file.
- [the heading of a question]: the text that starts each question in the /shape-slice brief.
- [the epics list]: the field of the plan file that lists the plan's epics.
- [the stories list]: the field of the plan file that lists the plan's stories.
- [the features list]: the field of the plan file that lists the plan's features.
- [the ICE of the first feature]: the text of the ICE of the first feature of the slice, as the plan file holds it.
- [the story texts]: the file where the test project keeps the text of the epic and of each story.
- [the tracker record]: the file where the test project keeps the tracker issue of the epic and of each story.
- [the issue numbers]: the field of the tracker record that lists those issues.
- [the slice eval file]: the file `eval.sl-intent-to-design.md` that /shape-eval writes in the slice's evals folder.
- [the first story eval file]: the story file `eval.<feature id>.feature.md` of the first story, in the slice's evals folder.
- [the ledger of the eval run]: the session ledger of the /shape-eval run, with every file that run read.
- [the build inputs]: the file or files that list what each build play, build skill, build agent and context sub-agent is given.
- [the story of the slice]: the reference to a story of the slice, as a build is given it.
- [the lint command]: the lint check over the build plays.
- [the lint failure line]: the line that the lint check prints for a build play whose inputs name the evals folder, the eval or the hidden file.
- [the ledger check command]: the check over a build session's ledger.
- [the evidence of the build run]: the evidence file of the build run that the ledger check read.
- [the evidence of the reading session]: the evidence file of the build session that read the evals folder.
- [the evidence of the clean session]: the evidence file of the build session that did not read the evals folder.
- [the flag that names the read]: the text that the ledger check writes in the evidence of a build run that read the evals folder.

## Context

From the stories' Context guidance:

- Read: the business intent's page, the spine, the Slice kind in the ontology, memory and the folder of /shape-slice (story #795); the slice in the spine and the ICE of each feature (story #818); the epic, the stories and the hidden file (story #798); the build plays' inputs and a build session's ledger, found through the session stamp (story #898).
- Never read: the plan, its epics and stories and the eval (story #795); the hidden file and the evals folder (story #818); any ICE page, the usage guide and the code (story #798); the eval, the hidden file and the rest of the plan's evals folder (story #898).
- Persona: the product owner, who names the intent, answers the questions, approves in Claude Code, runs and tracks the plan, wants proof that the intent is met, and trusts an eval pass only when the build aimed at the intent.
- In: the intent page, the questions, reuse of a slice, the slice, its record and its hidden file (story #795); the plan file, the epic and the stories (story #818); writing the eval, often by running a play on a test project (story #798); the flag in the build run's evidence and the lint check over the build plays (story #898).
- Out: the plan, the epic, the stories and the eval (story #795); picking the slice, the hidden file, the eval and the build (story #818); running the eval, since the eval is plain text (story #798); blocking by a hook, encryption, and the drift checks and evidence warnings in Griffin (story #898).
