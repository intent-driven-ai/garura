`@story-795`
# Feature: Story #795 — /shape-slice grills within the tier and assembles the slice that delivers the business intent

Feature fn-795 of slice sl-intent-to-design, epic #794. Written by /shape-eval from story #795 and the slice's hidden file.

## Background:
* Given [a test project with business intent 788, a model and memory that answer every question, and an empty tracker] is set up

`@goal-1` `@expectation-1`
## Scenario: The play writes one slice for the intent, and its hidden file in the slice's evals folder
* When I run "/shape-slice 788" and answer "yes"
* Then the exit code is 0
* And the file [the spine file] field [the slices field of the spine file] has 1 items
* And the file [the spine file] contains [the link from the slice to business intent 788]
* And the file [the spine file] field [the feature order field of the slice] equals [the feature order that the test project expects]
* And the file [the spine file] field [the surface field of the slice] equals [the surface that the test project expects]
* And the file [the spine file] field [the tester field of the slice] equals [the tester that the test project expects]
* And the file [the hidden file] exists

`@goal-2`
## Scenario: A person can walk the three plays in order on the one surface, and each play ends well
* When I run "/shape-slice 788" and answer "yes"
* Then the exit code is 0
* And the file [the spine file] field [the slices field of the spine file] has 1 items
* And the file [the hidden file] exists
* When I run "/shape-plan 788" and answer "yes"
* Then the exit code is 0
* And the file [the plan file of business intent 788] exists
* And the file [the plan file of business intent 788] field [the epics field of the plan file] has 1 items
* And the file [the plan file of business intent 788] field [the stories field of the plan file] has 2 items
* When I run "/shape-eval 788" and answer "yes"
* Then the exit code is 0
* And the file [the slice file of the eval] exists
* And the file [the eval file of the first story] exists
* And the file [the eval file of the second story] exists

`@goal-2` `@F4`
## Scenario: The slice names one surface and one tester
* When I run "/shape-slice 788" and answer "yes"
* Then the exit code is 0
* And the file [the spine file] field [the surfaces field of the slice] has 1 items
* And the file [the spine file] field [the surface field of the slice] equals [the surface that the test project expects]
* And the file [the spine file] field [the tester field of the slice] equals [the tester that the test project expects]

`@F4`
## Scenario: A business intent that can be tested on two surfaces gets one surface
* Given [a test project whose business intent 788 could be tested on two surfaces] is set up
* When I run "/shape-slice 788" and answer "yes"
* Then the exit code is 0
* And the file [the spine file] field [the surfaces field of the slice] has 1 items

`@F4`
## Scenario: A business intent with no surface to test gets no slice, and the play says why
* Given [a test project whose business intent 788 has no surface that a person can test] is set up
* When I run "/shape-slice 788" and answer "yes"
* Then the file [the spine file] field [the slices field of the spine file] has 0 items
* And the file [the hidden file] does not exist
* And the output contains [the reason that no surface can be tested]

`@goal-3` `@F3`
## Scenario: The hidden file is written in the slice's evals folder, with the entry of each feature
* When I run "/shape-slice 788" and answer "yes"
* Then the exit code is 0
* And the file [the hidden file] exists
* And the file [the hidden file] contains [the heading of the first feature's entry in the hidden file]
* And the file [the hidden file] contains [the heading of the second feature's entry in the hidden file]
* And the file [the hidden file] contains "### Failure conditions"
* And the file [the hidden file] contains "### Recovery"
* And the file [the hidden file] contains "- For "

`@goal-3` `@F3`
## Scenario: Each failure line of the hidden file has exactly one complete recovery
* When I run "/shape-slice 788" and answer "yes"
* And I run [the command that saves the recovery check of the hidden file to a file]
* Then the file [the recovery check file] field [the failure lines checked field of the recovery check file] equals [the number of failure lines that the test project expects]
* And the file [the recovery check file] field [the failure lines without exactly one complete recovery field of the recovery check file] has 0 items

`@expectation-2`
## Scenario: The play makes no new file outside the product model except the hidden file
* When I run "/shape-slice 788" and answer "yes"
* And I run [the command that saves the list of new files outside the product model to a file]
* Then the file [the list of new files outside the product model] field [the files field of that list] has 1 items
* And the file [the list of new files outside the product model] contains [the path of the hidden file]

`@F1` `@expectation-3`
## Scenario: The play writes one slice and its hidden file, and no plan, no epic, no story and no eval
* When I run "/shape-slice 788" and answer "yes"
* And I run [the command that saves the tracker's issues of business intent 788 to a file]
* Then the file [the spine file] field [the slices field of the spine file] has 1 items
* And the file [the hidden file] exists
* And the file [the plan file of business intent 788] does not exist
* And the file [the tracker export file] field [the issues field of the tracker export file] has 0 items
* And the file [the tracker export file] field [the epics field of the tracker export file] has 0 items
* And the file [the tracker export file] field [the stories field of the tracker export file] has 0 items
* And the file [the slice file of the eval] does not exist
* And the folder [the slice's evals folder] holds 1 files

`@F2`
## Scenario: A business intent that a slice already serves does not get a second slice
* Given [a slice that already serves business intent 788] is set up
* When I run "/shape-slice 788" and answer "yes"
* Then the exit code is 0
* And the file [the spine file] field [the slices field of the spine file] has 1 items

`@F5`
## Scenario: The play asks no question that the model or memory answers
* When I run "/shape-slice 788" and answer "yes"
* Then the exit code is 0
* And the file [the question record] field [the questions field of the question record] has 0 items

`@F6`
## Scenario: Each "Fails if" line of the features and of their capability is in the hidden file
* When I run "/shape-slice 788" and answer "yes"
* Then the exit code is 0
* And the file [the hidden file] contains [the Fails if line of the first feature]
* And the file [the hidden file] contains [the Fails if line of the second feature]
* And the file [the hidden file] contains [the Fails if line of the capability of both features]

## Untestable

None. Every goal, expectation and failure condition of this story has a scenario.

## Lines covered

- `@goal-1`: When the product owner runs /shape-slice on a business intent, the spine gets one slice that serves that intent, with its features in build order, its one surface and the persona who tests it.
- `@goal-2`: One person can test the slice end to end on that one surface.
- `@goal-3`: The same run puts the slice's hidden file in the plan's evals folder, with one entry for each feature of the slice and each entry closed by exactly one way back. This part is not built yet; decision 6 adds it.
- `@expectation-1`: The product owner runs /shape-slice 788 in Claude Code and finds one slice in the spine and the hidden file in plans/788/evals/<slug>/.
- `@expectation-2`: No other new file appears outside the product model.
- `@expectation-3`: Run on a real business intent, the play writes one slice and its hidden file, and no plan, epic, story or eval.
