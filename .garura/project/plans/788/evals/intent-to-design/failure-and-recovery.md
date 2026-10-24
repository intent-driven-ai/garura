# Failure and recovery: slice sl-intent-to-design

Slice: From a named piece of work to its design (sl-intent-to-design). Plan: 788 (business intent bi-788). Surface: the Claude Code command line; tested by the product owner.

Written by /shape-slice (decision 6 of #844), from the ICE of each feature and its capability. The ICE is thin: proposed by /shape-slice, to be deepened with /discover-capabilities. When an ICE changes, its entry here is made again from the same ICE.

Who reads this file: /shape-eval reads all of it. The running eval reads only the Recovery parts. No builder, no build skill and no context sub-agent reads this file. A story never holds these lines.

Rule: standards/rules/expectation-generation.md, "A story's recovery (product ICE)": one recovery for each "Fails if" line, with When (a symptom), Way back (guidance, never code) and Who fixes.

## fn-795: /shape-slice writes the slice only

- Capability: cap-shape-slice (Shape a slice)
- Story: (filled in by /shape-plan)

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

- Capability: cap-718 (Build a plan)
- Story: (filled in by /shape-plan)

### Failure conditions

- F7 (from the feature ICE): A feature of the slice has no story.
- F8 (from the feature ICE): A story or the plan file holds a failure condition or a recovery condition.
- F9 (from the feature ICE): A second run makes a second epic for the slice or a second story for one feature.
- F10 (from the capability ICE): The epic or a story has no tracker issue, or building stops because a domain or model page is missing.
- F11 (from the capability ICE): A story holds a failure condition, or a second plan is made for one business intent.
- F12 (from the capability ICE): The plan play writes a failure condition, a recovery condition or the eval into the plan's evals folder.

### Recovery

- For F7
  - When: The epic has fewer stories than the slice has features, or no story names one of the features.
  - Way back: Make the missing story under the epic, from its feature's ICE and that feature's capability's ICE.
  - Who fixes: a person must decide
- For F8
  - When: A story's text or the plan file says what must never happen, or how to recover.
  - Way back: Take the line out of the story and the plan file; the line stays only in the hidden file. The person decides if the eval must be made again, because a builder may have read the line.
  - Who fixes: a person must decide
- For F9
  - When: The tracker has two epics for the slice, or two stories for one feature.
  - Way back: Keep the first epic or story, and close the copy with a pointer to the first.
  - Who fixes: a person must decide
- For F10
  - When: The epic or a story has no issue in the tracker, or the run stopped and named a missing domain or model page.
  - Way back: Give the epic or the story its issue; write a missing page as a light page and go on.
  - Who fixes: a person must decide
- For F11
  - When: Two plan files exist for one intent, or a story says what must never happen.
  - Way back: Keep one plan, whose ID is the intent's issue number, and move the slices of the other into it; take the failure line out of the story.
  - Who fixes: a person must decide
- For F12
  - When: A failure line, a recovery line or the eval in the evals folder was changed by /shape-plan.
  - Way back: Put the hidden file back as /shape-slice wrote it, keep only the story numbers that /shape-plan added, and leave the eval to /shape-eval.
  - Who fixes: the builder can fix this alone

## fn-798: /shape-eval writes the hidden eval

- Capability: cap-shape-eval (Write the hidden eval)
- Story: (filled in by /shape-plan)

### Failure conditions

- F13 (from the feature ICE): The eval is written outside the plan's evals folder, or a builder's inputs name that folder.
- F14 (from the feature ICE): A story's goal or expectation, or a failure condition in the hidden file, has no check, and the eval does not say that it cannot test it yet.
- F15 (from the feature ICE): A handoff plan that the eval writes names a failure condition, its id or the check.
- F16 (from the capability ICE): A builder can read the eval.
- F17 (from the capability ICE): The eval checks something the business intent does not ask for.
- F18 (from the capability ICE): The eval play reads an ICE page, the usage guide or the code.

### Recovery

- For F13
  - When: An eval file is outside plans/788/evals/intent-to-design/, or the inputs of a build play, a build skill or a context sub-agent name the evals folder.
  - Way back: Move the eval into the evals folder and take the folder out of the builder's inputs. The person decides if the eval must be made again, because a builder may have read it.
  - Who fixes: a person must decide
- For F14
  - When: A goal, an expectation or a failure line has no check in the eval and no note that it cannot be tested yet.
  - Way back: Add a check from the outside, on the slice's surface, or a note that says why it cannot be tested yet.
  - Who fixes: the builder can fix this alone
- For F15
  - When: A handoff plan holds a failure line, an F id or the name of a check.
  - Way back: Rewrite the handoff plan so that it says only what the product does wrong, as a symptom, and the way back.
  - Who fixes: the builder can fix this alone
- For F16
  - When: The eval or the hidden file is in a place that a build play, a build skill or a context sub-agent reads, or a builder's short-term memory holds its text.
  - Way back: Keep the eval only in the evals folder, remove its text from the builder's short-term memory, and treat a pass of that build as not proven.
  - Who fixes: a person must decide
- For F17
  - When: A check traces to no line of the business intent, its epic or its stories.
  - Way back: Remove the check, or trace it to the line of the intent that it serves.
  - Who fixes: a person must decide
- For F18
  - When: The eval run's reads name an ICE page, a usage guide or a code file.
  - Way back: Build the eval again from only the epic, its stories and the hidden file.
  - Who fixes: the builder can fix this alone
