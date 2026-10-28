`@story-798`
# Feature: Story #798 — The eval play writes the slice's eval: is the business intent met, tested on the slice's surface

Feature fn-798 of slice sl-intent-to-design, epic #794. Written by /shape-eval from story #798 and the slice's hidden file.

## Background:
* Given [a test project where /shape-plan has run for business intent 788, with a hidden file] is set up

`@goal-1` `@expectation-1`
## Scenario: The play writes one eval for the slice in the slice's evals folder
* When I run "/shape-eval 788" and answer "yes"
* Then the exit code is 0
* And the folder [the slice's evals folder] holds 4 files
* And the file [the slice file of the eval] exists
* And the file [the eval file of the first story] exists
* And the file [the eval file of the second story] exists

`@goal-2`
## Scenario: Each step of each story file is a sentence of the step library of the slice's surface
* When I run "/shape-eval 788" and answer "yes"
* And I run [the command that checks the steps of the story files against the step library]
* Then the exit code is 0

`@goal-2` `@F14`
## Scenario: Each goal, each expectation and each failure condition of each story has a scenario or an Untestable line
* When I run "/shape-eval 788" and answer "yes"
* And I run [the command that saves the tag check of the first story file to a file]
* Then the file [the tag check file of the first story] field [the story lines checked field of the tag check] equals [the number of lines of the first story that the test project expects]
* And the file [the tag check file of the first story] field [the lines without a scenario and without an Untestable line field of the tag check] has 0 items
* When I run [the command that saves the tag check of the second story file to a file]
* Then the file [the tag check file of the second story] field [the story lines checked field of the tag check] equals [the number of lines of the second story that the test project expects]
* And the file [the tag check file of the second story] field [the lines without a scenario and without an Untestable line field of the tag check] has 0 items

`@goal-2` `@F14`
## Scenario: A tag stands on a scenario heading in each story file, not only on an Untestable line
* When I run "/shape-eval 788" and answer "yes"
* And I run [the command that saves the tag check of the first story file to a file]
* Then the file [the tag check file of the first story] field [the number of lines with a scenario field of the tag check] equals [the number of lines of the first story that the test project expects]
* When I run [the command that saves the tag check of the second story file to a file]
* Then the file [the tag check file of the second story] field [the number of lines with a scenario field of the tag check] equals [the number of lines of the second story that the test project expects]

`@goal-3`
## Scenario: The slice file says that the eval passes only when every scenario passes, on the slice's surface
* When I run "/shape-eval 788" and answer "yes"
* Then the exit code is 0
* And the file [the slice file of the eval] contains "The eval passes only when every scenario of every story below passes."
* And the file [the slice file of the eval] contains "There is no score."
* And the file [the slice file of the eval] contains [the surface that the test project expects]
* And the file [the slice file of the eval] contains "Surface kind: command-line"

`@expectation-2` `@F19`
## Scenario: After the eval is written, no build play names the evals folder, the eval or the hidden file
* When I run "/shape-eval 788" and answer "yes"
* And I run [the lint check over the build plays]
* Then the exit code is 0
* And the output does not contain "evals"

`@F19`
## Scenario: A build play that names the eval is stopped by the lint check
* Given [a build play whose inputs name the eval] is set up
* When I run [the lint check over the build plays]
* Then the exit code is 1
* And the output contains [the name of that build play]

`@F19`
## Scenario: A build session that read the evals folder gets a flag in its build run's evidence
* Given [a build run with evidence that holds the session stamp of one build session and no flag] is set up
* And the file [the ledger of that build session] holds [a read of the plan's evals folder]
* When I run [the ledger check over that build session]
* Then the exit code is 0
* And the file [the evidence of that build run] contains [the flag that names the read of the plan's evals folder]
* And the file [the evidence of that build run] field [the flags field of the evidence] has 1 items

`@F27`
## Scenario: The play writes nothing outside the slice's evals folder
* When I run "/shape-eval 788" and answer "yes"
* And I run [the command that saves the list of new files outside the slice's evals folder to a file]
* Then the file [the list of new files outside the slice's evals folder] field [the files field of that list] has 0 items

`@F15`
## Scenario: The handoff plan names no failure condition, no id of one and no check
* When I run "/shape-eval 788" and answer "yes"
* And I run [the command that makes the handoff plan for a failed check of the first failure condition]
* Then the file [the handoff plan that the eval writes] exists
* And the file [the handoff plan that the eval writes] does not contain [the first failure condition of the hidden file]
* And the file [the handoff plan that the eval writes] does not contain [the second failure condition of the hidden file]
* And the file [the handoff plan that the eval writes] does not contain [the id of the first failure condition of the hidden file]
* And the file [the handoff plan that the eval writes] does not contain [the id of the second failure condition of the hidden file]
* And the file [the handoff plan that the eval writes] does not contain [the tag of the failure condition of the first feature]
* And the file [the handoff plan that the eval writes] does not contain [the tag of the failure condition of the second feature]
* And the file [the handoff plan that the eval writes] does not contain [the title of the scenario that checks the first failure condition]
* And the file [the handoff plan that the eval writes] does not contain [the title of the scenario that checks the second failure condition]

`@F17`
## Scenario: Each tag of each story file is a goal, an expectation or a failure line of its own story
* When I run "/shape-eval 788" and answer "yes"
* And I run [the command that saves the tag check of the first story file to a file]
* Then the file [the tag check file of the first story] field [the tags outside the story field of the tag check] has 0 items
* When I run [the command that saves the tag check of the second story file to a file]
* Then the file [the tag check file of the second story] field [the tags outside the story field of the tag check] has 0 items

`@F18`
## Scenario: The play reads no ICE page, no usage guide and no code
* When I run "/shape-eval 788" and answer "yes"
* And I run [the command that saves the ledger of the last play run to a file]
* Then the file [the ledger of the last play run] does not contain ".garura/product/product-os/"
* And the file [the ledger of the last play run] does not contain ".garura/project/plans/788/guides/"
* And the file [the ledger of the last play run] does not contain [the folder of the test project's code]

## Untestable

- `@F17`: A person must read the steps of each scenario to see if they check only what the tag says, because no step of the library can judge that; the scenario checks only that every tag belongs to its story.

## Lines covered

- `@goal-1`: When the product owner runs /shape-eval on a business intent, the slice's evals folder holds one eval for that slice.
- `@goal-2`: The eval checks from the outside, on the slice's surface, each goal and expectation of the stories, and checks that nothing the hidden file warns about happens.
- `@goal-3`: The eval says if the business intent is met on the slice's surface.
- `@expectation-1`: The product owner runs /shape-eval 788 in Claude Code after /shape-plan and finds the eval in plans/788/evals/<slug>/.
- `@expectation-2`: No build play's inputs name the evals folder.
