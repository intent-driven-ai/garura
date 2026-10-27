# Failure and recovery: slice sl-intent-to-design

Slice: From a named piece of work to its design (sl-intent-to-design). Plan: 788 (business intent bi-788). Surface: the Claude Code command line; tested by the product owner.

Written by /shape-slice (decision 6 of #844), from the ICE of each feature and its capability. The ICE is thin: proposed by /shape-slice, to be deepened with /discover-capabilities. When an ICE changes, its entry here is made again from the same ICE.

Who reads this file: /shape-eval reads all of it, and joins each entry to its story through the epic's feature-to-story map (ontology v11, ADR 052). The running eval reads only the Recovery parts. No builder, no build skill and no context sub-agent reads this file. A story never holds these lines.

Rule: standards/rules/expectation-generation.md, "A feature's recovery (product ICE)": one recovery for each "Fails if" line, with When (a symptom), Way back (guidance, never code) and Who fixes.

## fn-795: /shape-slice writes the slice and its hidden file

- Capability: cap-shape-slice (Shape a slice)
- Thin: both ICE (the feature's and its capability's) are thin.

### Failure conditions

- F1 (from the feature ICE): /shape-slice writes a plan, an epic, a story or an eval.
- F2 (from the feature ICE): A new slice is made for an intent that a slice already serves.
- F3 (from the feature ICE): The hidden file is not written, or a failure condition in it has no recovery or more than one.
- F4 (from the capability ICE): The slice has no surface that a person can test, has no tester, or has more than one surface.
- F5 (from the capability ICE): The person is asked a question that the model or memory answers.
- F6 (from the capability ICE): A "Fails if" line of a slice feature or of its capability is missing from the hidden file.

### Recovery

- For F1
  - When: After /shape-slice, a plan file, an epic or story in the tracker, or an eval file exists that the run made.
  - Way back: Take back each file the run wrote outside the slice, its record, the model parts it added and the hidden file. The plan and the eval are left to /shape-plan and /shape-eval.
  - Who fixes: the builder can fix this alone
- For F2
  - When: The spine has two slices that list the same intent, or two slices with the same features and the same surface.
  - Way back: Keep the slice that served the intent first, add the intent to it, and remove the new slice.
  - Who fixes: the builder can fix this alone
- For F3
  - When: The slice's evals folder has no failure-and-recovery file, or one failure line has no recovery or two recoveries.
  - Way back: Write the file from the "Fails if" lines of each feature and its capability, with exactly one recovery for each line.
  - Who fixes: the builder can fix this alone
- For F4
  - When: The slice record has an empty surface or tester, or it names two surfaces.
  - Way back: Do not write the slice until one surface and the person who tests it are named; when there is none, say why.
  - Who fixes: a person must decide
- For F5
  - When: The question record holds a question whose answer is already in the model or in memory.
  - Way back: Drop the question and use the answer that the model or memory gives, with its source.
  - Who fixes: the builder can fix this alone
- For F6
  - When: A "Fails if" line on a feature page or a capability page of the slice is not in the hidden file.
  - Way back: Add the missing line to the entry of its feature, with one recovery.
  - Who fixes: the builder can fix this alone

## fn-818: /shape-plan writes the plan, the epic and the stories

- Capability: cap-718
- Written from: the feature ICE (thin) and the capability ICE (thin).
- Thin ICE: the feature ICE is thin, so its recovery may be weak until `/discover-capabilities` deepens it.
- Thin ICE: the capability ICE is thin, so its recovery may be weak until `/discover-capabilities` deepens it.

### Failure conditions

- F7 (from the feature ICE): a feature of the slice has no story.
- F8 (from the feature ICE): a story or the plan file holds a failure condition or a recovery condition.
- F9 (from the feature ICE): a second run makes a second epic for the slice or a second story for one feature.
- F26 (from the feature ICE): a story, or its Context guidance, names the eval, the hidden file or the plan's evals folder.
- F10 (from the capability ICE): the epic or a story has no tracker issue, or building stops because a domain or model page is missing.
- F11 (from the capability ICE): a story holds a failure condition, or a second plan is made for one business intent.
- F12 (from the capability ICE): the plan play writes a failure condition, a recovery condition or the eval into the plan's evals folder.

### Recovery

- For F7
  - When: After /shape-plan, a feature of the slice has no story in the epic.
  - Way back: Write one story for each feature of the slice, under the epic.
  - Who fixes: a person must decide
- For F8
  - When: A story or the plan file has a line that says how the feature fails, or how to recover.
  - Way back: Keep only the goals, the limits, the expectations and the Context guidance in each story and in the plan file.
  - Who fixes: a person must decide
- For F9
  - When: After a second run of /shape-plan, the tracker has two epics for the slice, or two stories for one feature.
  - Way back: Keep one epic for the slice and one story for each feature. A person closes each copy in the tracker.
  - Who fixes: a person must decide
- For F26
  - When: A story, or its Context guidance, names the eval, the hidden file or the plan's evals folder.
  - Way back: Take that name out of the story and its Context guidance. A person decides if a build that read the story must run again.
  - Who fixes: a person must decide
- For F10
  - When: The epic or a story has no issue in the tracker, or /shape-plan stops because a domain or model page is missing.
  - Way back: Make one tracker issue for the epic and for each story, after the product owner's yes. When a page is missing, write a light page and go on.
  - Who fixes: a person must decide
- For F11
  - When: A story has a line that says how the feature fails, or one business intent has two plan files.
  - Way back: Keep the goals, the limits, the expectations and the Context guidance in each story, and nothing more. Keep one plan file for each business intent.
  - Who fixes: a person must decide
- For F12
  - When: /shape-plan writes a file other than the plan file, the epic and the stories.
  - Way back: Make /shape-plan write only the plan file, the epic and the stories. Take back each other file it wrote.
  - Who fixes: the builder can fix this alone

## fn-798: /shape-eval writes the hidden eval

- Capability: cap-shape-eval
- Written from: the feature ICE (thin) and the capability ICE (thin).
- Thin ICE: the feature ICE is thin, so its recovery may be weak until `/discover-capabilities` deepens it.
- Thin ICE: the capability ICE is thin, so its recovery may be weak until `/discover-capabilities` deepens it.

### Failure conditions

- F27 (from the feature ICE): the eval is written outside the plan's evals folder.
- F14 (from the feature ICE): a story's goal or expectation, or a failure condition in the hidden file, has no check, and the eval does not say that it cannot test it yet.
- F15 (from the feature ICE): a handoff plan that the eval writes names a failure condition, its id or the check.
- F19 (from the capability ICE): a builder is given the eval, or a build session read the evals folder and that build run's evidence has no flag that names the read.
- F17 (from the capability ICE): the eval checks something the business intent does not ask for.
- F18 (from the capability ICE): the eval play reads an ICE page, the usage guide or the code.

### Recovery

- For F27
  - When: /shape-eval writes a file outside the one folder that its limit names.
  - Way back: Make /shape-eval write only in the one folder that its limit names. Take back each file it wrote elsewhere.
  - Who fixes: the builder can fix this alone
- For F14
  - When: A goal or expectation of a story, or a failure condition in the hidden file, has no scenario in the eval. The eval does not list it as one it cannot test yet.
  - Way back: Add one scenario for it, or list it under Untestable with its reason. Change no scenario that is there.
  - Who fixes: a person must decide
- For F15
  - When: A handoff plan names a failure condition, its id or the check that found it.
  - Way back: Take those names out of the handoff plan. A person decides if a build that read it must run again.
  - Who fixes: a person must decide
- For F19
  - When: A build's inputs name the eval. Or a build session read the evals folder, and that build run's evidence has no flag that names the read.
  - Way back: Take the eval out of the build's inputs, and add the missing flag to that build run's evidence. A person decides if the build must run again.
  - Who fixes: a person must decide
- For F17
  - When: A scenario of the eval checks something that the business intent does not ask for.
  - Way back: The eval checks only what the business intent asks for. A person decides if that scenario goes, because a scenario that is there does not change.
  - Who fixes: a person must decide
- For F18
  - When: /shape-eval opens an ICE page, the usage guide or the code.
  - Way back: Make /shape-eval open no ICE page, no usage guide and no code. It reads only the files that its limit names.
  - Who fixes: the builder can fix this alone

## fn-898: The build is given the business intent, never the eval

- Capability: cap-shape-eval
- Written from: the feature ICE (thin) and the capability ICE (thin).
- Thin ICE: the feature ICE is thin, so its recovery may be weak until `/discover-capabilities` deepens it.
- Thin ICE: the capability ICE is thin, so its recovery may be weak until `/discover-capabilities` deepens it.

### Failure conditions

- F20 (from the feature ICE): a build play's inputs name the evals folder, the eval or the hidden file, and the lint check passes.
- F21 (from the feature ICE): a build session read the plan's evals folder, and that build run's evidence has no flag that names the read.
- F22 (from the feature ICE): a clean build session gets a flag, or the check stops a build.
- F23 (from the capability ICE): a builder is given the eval, or a build session read the evals folder and that build run's evidence has no flag that names the read.
- F24 (from the capability ICE): the eval checks something the business intent does not ask for.
- F25 (from the capability ICE): the eval play reads an ICE page, the usage guide or the code.

### Recovery

- For F20
  - When: a build play's inputs name the evals folder, the eval or the hidden file, and the lint check still passes
  - Way back: the lint check fails each build play whose inputs name the evals folder, the eval or the hidden file, and names each of those inputs
  - Who fixes: the builder can fix this alone
- For F21
  - When: a build session's ledger shows a read of the plan's evals folder, and that build run's evidence holds no flag that names the read
  - Way back: the ledger check records, in that build run's evidence, one flag for each read of the plan's evals folder
  - Who fixes: the builder can fix this alone
- For F22
  - When: a build session with no read of the evals folder gets a flag, or a build stops because of the ledger check
  - Way back: a clean build session gets no flag, and the ledger check only records a flag and never stops a build
  - Who fixes: the builder can fix this alone
- For F23
  - When: a builder was given the eval, or a build session read the plan's evals folder and that build run's evidence holds no flag that names the read
  - Way back: take the eval out of every input a builder is given, record in that build run's evidence a flag that names the read, and let the product owner say if the build's pass still counts
  - Who fixes: a person must decide
- For F24
  - When: the eval holds a check that no goal, expectation or failure condition of the business intent's stories and hidden file asks for
  - Way back: each check of the eval comes from one goal, expectation or failure condition of the intent. A person decides if that check goes, because a check that is there does not change
  - Who fixes: a person must decide
- For F25
  - When: the eval play's run shows that it read an ICE page, the usage guide or the code
  - Way back: the play reads only the pages its limit names, and no ICE page, usage guide or code. This feature does not build that play, so a person decides who fixes it and if its work must be done again
  - Who fixes: a person must decide
