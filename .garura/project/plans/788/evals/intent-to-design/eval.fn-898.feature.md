`@story-898`
# Feature: Story #898 — Agents build for the business intent, not only to pass the eval: the build is given the intent, never the eval

Feature fn-898 of slice sl-intent-to-design, epic #794. Written by /shape-eval from story #898 and the slice's hidden file.

## Background:
* Given [a test project where /shape-plan has run for business intent 788, with a hidden file] is set up

`@goal-1` `@expectation-1` `@F20`
## Scenario: The lint check stops a build play whose inputs name the evals folder
* Given [a build play whose inputs name the evals folder] is set up
* When I run [the lint check over the build plays]
* Then the exit code is 1
* And the output contains [the name of that build play]

`@goal-1` `@F20` `@F23`
## Scenario: The lint check stops a build play whose inputs name the eval
* Given [a build play whose inputs name the eval] is set up
* When I run [the lint check over the build plays]
* Then the exit code is 1
* And the output contains [the name of that build play]

`@goal-1` `@F20`
## Scenario: The lint check stops a build play whose inputs name the hidden file
* Given [a build play whose inputs name the hidden file] is set up
* When I run [the lint check over the build plays]
* Then the exit code is 1
* And the output contains [the name of that build play]

`@goal-1` `@F21` `@F23`
## Scenario: A build skill that read the eval gets a flag in its build run's evidence
* Given [a build run with evidence that holds the session stamp of a build skill and no flag] is set up
* And the file [the ledger of that build session] holds [a read of the eval in the plan's evals folder]
* When I run [the ledger check over that build session]
* Then the exit code is 0
* And the file [the evidence of that build run] contains [the flag that names the read of the eval]
* And the file [the evidence of that build run] field [the flags field of the evidence] has 1 items

`@goal-1` `@F21` `@F23`
## Scenario: A build agent that read the hidden file gets a flag in its build run's evidence
* Given [a build run with evidence that holds the session stamp of a build agent and no flag] is set up
* And the file [the ledger of that build session] holds [a read of the hidden file in the plan's evals folder]
* When I run [the ledger check over that build session]
* Then the exit code is 0
* And the file [the evidence of that build run] contains [the flag that names the read of the hidden file]
* And the file [the evidence of that build run] field [the flags field of the evidence] has 1 items

`@goal-1` `@F21` `@F23`
## Scenario: A context sub-agent that a build started and that read the evals folder gets a flag
* Given [a build run with evidence that holds the session stamp of a context sub-agent that a build started and no flag] is set up
* And the file [the ledger of that build session] holds [a read of the plan's evals folder]
* When I run [the ledger check over that build session]
* Then the exit code is 0
* And the file [the evidence of that build run] contains [the flag that names the read of the plan's evals folder]
* And the file [the evidence of that build run] field [the flags field of the evidence] has 1 items

`@goal-2`
## Scenario: A build play is given the business intent through the stories of the slice
* Given [a build play whose inputs are the stories of the slice] is set up
* When I run [the lint check over the build plays]
* Then the exit code is 0
* And the output does not contain "evals"
* And the file [the inputs of that build play] contains [the path of the story of the first feature]
* And the file [the inputs of that build play] contains [the path of the story of the second feature]

`@goal-2` `@expectation-2` `@F22`
## Scenario: A clean build session that read only the stories gets no flag, and the check does not stop the build
* Given [a build run with evidence that holds the session stamp of one build session and no flag] is set up
* And the file [the ledger of that build session] holds [a read of the story of the first feature and a read of the story of the second feature]
* When I run [the ledger check over that build session]
* Then the exit code is 0
* And the file [the evidence of that build run] field [the flags field of the evidence] has 0 items
* And the file [the evidence of that build run] does not contain [the flag that names the read of the plan's evals folder]

`@goal-3` `@expectation-2` `@F21` `@F22` `@F23`
## Scenario: A build session that read the plan's evals folder gets one flag that names the read, and the build is not stopped
* Given [a build run with evidence that holds the session stamp of one build session and no flag] is set up
* And the file [the ledger of that build session] holds [a read of the plan's evals folder]
* When I run [the ledger check over that build session]
* Then the exit code is 0
* And the file [the evidence of that build run] contains [the flag that names the read of the plan's evals folder]
* And the file [the evidence of that build run] field [the flags field of the evidence] has 1 items

`@goal-3` `@F21`
## Scenario: A build session with two reads of the plan's evals folder gets two flags
* Given [a build run with evidence that holds the session stamp of one build session and no flag] is set up
* And the file [the ledger of that build session] holds [two reads of the plan's evals folder, one of the eval and one of the hidden file]
* When I run [the ledger check over that build session]
* Then the exit code is 0
* And the file [the evidence of that build run] field [the flags field of the evidence] has 2 items

`@goal-4`
## Scenario: The slice gets one eval, and its slice file says the eval passes only when every scenario passes
* When I run "/shape-eval 788" and answer "yes"
* Then the exit code is 0
* And the folder [the slice's evals folder] holds 4 files
* And the file [the slice file of the eval] exists
* And the file [the slice file of the eval] contains "The eval passes only when every scenario of every story below passes."
* And the file [the slice file of the eval] contains [the surface that the test project expects]

`@expectation-3`
## Scenario: After the eval is written, no build play names the evals folder
* When I run "/shape-eval 788" and answer "yes"
* And I run [the lint check over the build plays]
* Then the exit code is 0
* And the output does not contain "evals"
* And the folder [the slice's evals folder] holds 4 files

`@F24`
## Scenario: Each tag of each story file is a goal, an expectation or a failure line of its own story
* When I run "/shape-eval 788" and answer "yes"
* And I run [the command that saves the tag check of the first story file to a file]
* Then the file [the tag check file of the first story] field [the tags outside the story field of the tag check] has 0 items
* When I run [the command that saves the tag check of the second story file to a file]
* Then the file [the tag check file of the second story] field [the tags outside the story field of the tag check] has 0 items

`@F25`
## Scenario: The play reads no ICE page, no usage guide and no code
* When I run "/shape-eval 788" and answer "yes"
* And I run [the command that saves the ledger of the last play run to a file]
* Then the file [the ledger of the last play run] does not contain ".garura/product/product-os/"
* And the file [the ledger of the last play run] does not contain ".garura/project/plans/788/guides/"
* And the file [the ledger of the last play run] does not contain [the folder of the test project's code]

## Untestable

- `@F24`: A person must read the steps of each scenario to see if they check only what the tag says, because no step of the library can judge that; the scenario checks only that every tag belongs to its story.

## Lines covered

- `@goal-1`: No build play, build skill, build agent or context sub-agent that a build starts is given the eval, the hidden file or the plan's evals folder.
- `@goal-2`: A build is given the business intent through the slice's stories.
- `@goal-3`: Each build session that read the plan's evals folder has a flag in that build run's evidence that names the read.
- `@goal-4`: Each slice has one eval that says, from the outside, if its business intent is met on the slice's surface.
- `@expectation-1`: The lint check runs over the build plays and stops a build play whose inputs name the evals folder.
- `@expectation-2`: The test of the session-ledger check flags, in the evidence, one session that read the evals folder, and passes a clean session.
- `@expectation-3`: After /shape-plan, /shape-eval writes the eval in the plan's evals folder, and the inputs of no build play name that folder.
