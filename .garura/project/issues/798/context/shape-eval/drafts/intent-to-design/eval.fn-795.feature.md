`@story-795`
# Feature: Story #795 — /shape-slice grills within the tier and assembles the slice that delivers the business intent

Feature fn-795 of slice sl-intent-to-design, epic #794. Written by /shape-eval from story #795 and the slice's hidden file.

## Background:
* Given [the test project with no slice] is set up

`@goal-1`
## Scenario: The product owner runs /shape-slice on the business intent and the spine gets one slice with its features, its surface and its tester
* When I run "/shape-slice 788" and answer [the shape-slice answers]
* Then the exit code is 0
* And the file [the spine] field "slices" has 1 items
* And the file [the slice record] field "intents" has 1 items
* And the file [the slice record] contains [the surface name]
* And the file [the slice record] contains [the tester name]

`@goal-2`
## Scenario: The slice names one surface and the person who tests it, so one person can test it end to end
* When I run "/shape-slice 788" and answer [the shape-slice answers]
* Then the file [the slice record] contains [the surface name]
* And the file [the slice record] contains [the tester name]
* And the output contains [the surface name]

`@expectation-1`
## Scenario: The product owner finds one slice in the spine and the hidden file in the slice's evals folder
* When I run "/shape-slice 788" and answer [the shape-slice answers]
* Then the file [the spine] field "slices" has 1 items
* And the file [the hidden file] exists

`@expectation-3`
## Scenario: The run writes one slice and its hidden file, and no plan, epic, story or eval
* When I run "/shape-slice 788" and answer [the shape-slice answers]
* Then the file [the hidden file] exists
* And the folder [the evals folder of the slice] holds 1 files
* And the file ".garura/project/plans/788.yaml" does not exist

`@F1`
## Scenario: /shape-slice does not write a plan, an epic, a story or an eval
* When I run "/shape-slice 788" and answer [the shape-slice answers]
* Then the file ".garura/project/plans/788.yaml" does not exist
* And the folder [the evals folder of the slice] holds 1 files

`@F2`
## Scenario: A second slice is not made for an intent that a slice already serves
* Given [the test project with a slice for business intent 788] is set up
* When I run "/shape-slice 788" and answer [the shape-slice answers]
* Then the file [the spine] field "slices" has 1 items

`@F3`
## Scenario: The hidden file is written and holds a recovery part
* When I run "/shape-slice 788" and answer [the shape-slice answers]
* Then the file [the hidden file] exists
* And the file [the hidden file] contains "### Recovery"

`@F4`
## Scenario: The slice is written with a surface a person can test and a tester
* When I run "/shape-slice 788" and answer [the shape-slice answers]
* Then the file [the slice record] contains [the surface name]
* And the file [the slice record] contains [the tester name]
* And the file [the spine] field "slices" has 1 items

`@F5`
## Scenario: The person is not asked a question that the model or memory answers
* Given [the test project whose model and memory answer every question] is set up
* When I run "/shape-slice 788" and answer "yes"
* Then the exit code is 0
* And the output does not contain [the heading of a question]

`@F6`
## Scenario: Each "Fails if" line of the slice's features is in the hidden file
* When I run "/shape-slice 788" and answer [the shape-slice answers]
* Then the file [the hidden file] contains [a Fails if line of a feature of the slice]

## Untestable

- `@goal-3`: the story says the hidden file's entries, each closed by exactly one way back, are not built yet (decision 6 adds them), and no library sentence counts the way-back lines of a Markdown file. That the hidden file exists and holds a recovery part is checked under `@expectation-1` and `@F3`.
- `@expectation-2`: no library sentence lists every new file of a project, so "no other new file appears outside the product model" cannot be checked as a whole. The plans folder and the evals folder are checked under `@expectation-3`.
