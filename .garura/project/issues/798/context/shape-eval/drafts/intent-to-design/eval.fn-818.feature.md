`@story-818`
# Feature: Story #818 — The plan play makes the plan file, the epic and one story per feature

Feature fn-818 of slice sl-intent-to-design, epic #794. Written by /shape-eval from story #818 and the slice's hidden file.

## Background:
* Given [the test project with a shaped slice] is set up

`@goal-1`
## Scenario: The product owner runs /shape-plan and the plan file holds one epic and one story for each feature of the slice
* When I run "/shape-plan 788" and answer "yes"
* Then the exit code is 0
* And the file ".garura/project/plans/788.yaml" exists
* And the file ".garura/project/plans/788.yaml" field [the epics list] has 1 items
* And the file ".garura/project/plans/788.yaml" field [the stories list] has 4 items

`@goal-2`
## Scenario: The plan names every feature it holds, each with its ICE
* When I run "/shape-plan 788" and answer "yes"
* Then the file ".garura/project/plans/788.yaml" field [the features list] has 4 items
* And the file ".garura/project/plans/788.yaml" contains [the ICE of the first feature]

`@goal-3`
## Scenario: A second run finds the plan, the epic and the stories and makes no copies
* When I run "/shape-plan 788" and answer "yes"
* And I run "/shape-plan 788" and answer "yes"
* Then the file ".garura/project/plans/788.yaml" field [the epics list] has 1 items
* And the file ".garura/project/plans/788.yaml" field [the stories list] has 4 items

`@expectation-1`
## Scenario: The product owner finds the plan file, one epic and one story for each feature
* When I run "/shape-plan 788" and answer "yes"
* Then the file ".garura/project/plans/788.yaml" exists
* And the file ".garura/project/plans/788.yaml" field [the epics list] has 1 items
* And the file ".garura/project/plans/788.yaml" field [the stories list] has 4 items

`@expectation-2`
## Scenario: No story holds any line from the hidden file
* When I run "/shape-plan 788" and answer "yes"
* Then the file [the story texts] does not contain [a line of the hidden file]
* And the file [the story texts] does not contain "Way back:"

`@F7`
## Scenario: Each feature of the slice has a story
* When I run "/shape-plan 788" and answer "yes"
* Then the file ".garura/project/plans/788.yaml" field [the features list] has 4 items
* And the file ".garura/project/plans/788.yaml" field [the stories list] has 4 items

`@F8`
## Scenario: Neither a story nor the plan file holds a failure condition or a recovery condition
* When I run "/shape-plan 788" and answer "yes"
* Then the file ".garura/project/plans/788.yaml" does not contain "Fails if"
* And the file ".garura/project/plans/788.yaml" does not contain "Way back:"
* And the file [the story texts] does not contain "Fails if"
* And the file [the story texts] does not contain "Way back:"

`@F9`
## Scenario: A second run does not make a second epic or a second story
* When I run "/shape-plan 788" and answer "yes"
* And I run "/shape-plan 788" and answer "yes"
* Then the file ".garura/project/plans/788.yaml" field [the epics list] has 1 items
* And the file ".garura/project/plans/788.yaml" field [the stories list] has 4 items

`@F10`
## Scenario: The epic and each story have a tracker issue
* When I run "/shape-plan 788" and answer "yes"
* Then the file [the tracker record] field [the issue numbers] has 5 items

`@F10`
## Scenario: A missing model page does not stop the run
* Given [the test project with a shaped slice and a missing model page] is set up
* When I run "/shape-plan 788" and answer "yes"
* Then the exit code is 0
* And the file ".garura/project/plans/788.yaml" field [the stories list] has 4 items

`@F11`
## Scenario: No story holds a failure condition and the intent has one plan
* When I run "/shape-plan 788" and answer "yes"
* And I run "/shape-plan 788" and answer "yes"
* Then the file [the story texts] does not contain "Fails if"
* And the folder ".garura/project/plans" holds 1 files

`@F12`
## Scenario: The plan play leaves the evals folder as /shape-slice wrote it
* When I run "/shape-plan 788" and answer "yes"
* Then the folder [the evals folder of the slice] holds 1 files
* And the file [the hidden file] exists

## Untestable

- `@expectation-3`: the trees filed by hand on 2026-10-21 for #717 and its partner are not in the story, so no exact result can be written. The eval can compare them when the usage guide maps them.
