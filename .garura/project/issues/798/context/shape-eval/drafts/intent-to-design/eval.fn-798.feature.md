`@story-798`
# Feature: Story #798 — The eval play writes the slice's eval: is the business intent met, tested on the slice's surface

Feature fn-798 of slice sl-intent-to-design, epic #794. Written by /shape-eval from story #798 and the slice's hidden file.

## Background:
* Given [the test project with a plan] is set up

`@goal-1`
## Scenario: The product owner runs /shape-eval and the slice's evals folder holds one eval for the slice
* When I run "/shape-eval 788" and answer "yes"
* Then the exit code is 0
* And the file [the slice eval file] exists
* And the folder [the evals folder of the slice] holds 6 files

`@goal-2`
## Scenario: The eval checks each goal and expectation of a story, and that nothing the hidden file warns about happens
* When I run "/shape-eval 788" and answer "yes"
* Then the file [the first story eval file] contains "@goal-1"
* And the file [the first story eval file] contains "@expectation-1"
* And the file [the first story eval file] contains "@F1"

`@goal-3`
## Scenario: The eval says that the business intent is met only when every scenario passes
* When I run "/shape-eval 788" and answer "yes"
* Then the file [the slice eval file] contains "The eval passes only when every scenario of every story below passes."
* And the file [the slice eval file] contains "There is no score."

`@expectation-1`
## Scenario: The product owner finds the eval in the slice's evals folder
* When I run "/shape-eval 788" and answer "yes"
* Then the output contains [the evals folder of the slice]
* And the file [the slice eval file] exists

`@expectation-2`
## Scenario: No build play's inputs name the evals folder
* When I run "/shape-eval 788" and answer "yes"
* Then the file [the build inputs] does not contain "evals"

`@F13`
## Scenario: The eval is written only in the plan's evals folder and no builder's inputs name that folder
* When I run "/shape-eval 788" and answer "yes"
* Then the folder ".garura/project/plans/788" holds 0 files
* And the folder [the evals folder of the slice] holds 6 files
* And the file [the build inputs] does not contain "evals"

`@F14`
## Scenario: Each goal, expectation and failure condition of a story has a check or a note that it cannot be tested yet
* When I run "/shape-eval 788" and answer "yes"
* Then the file [the first story eval file] contains "@goal-1"
* And the file [the first story eval file] contains "@expectation-1"
* And the file [the first story eval file] contains "@F1"
* And the file [the first story eval file] contains "## Untestable"

`@F19`
## Scenario: A build session that read the evals folder has a flag that names the read
* Given [the test project with a build run that read the evals folder] is set up
* When I run [the ledger check command]
* Then the exit code is 0
* And the file [the evidence of the build run] contains [the flag that names the read]

`@F18`
## Scenario: The eval play does not read an ICE page, the usage guide or the code
* When I run "/shape-eval 788" and answer "yes"
* Then the file [the ledger of the eval run] does not contain "feature.md"
* And the file [the ledger of the eval run] does not contain "capability.md"
* And the file [the ledger of the eval run] does not contain "ice.md"
* And the file [the ledger of the eval run] does not contain "guides/"

## Untestable

- `@F15`: a handoff plan is written only when a check of the eval fails after the build, and this eval writes none, so there is no handoff plan to check yet.
- `@F17`: no library sentence can say that a check asks for more than the goals, expectations and failure conditions of the stories; each scenario of the story files carries the tag of the line that it covers, and a person reads the tags.
