`@story-818`
# Feature: Story #818 — The plan play makes the plan file, the epic and one story per feature

Feature fn-818 of slice sl-intent-to-design, epic #794. Written by /shape-eval from story #818 and the slice's hidden file.

## Background:
* Given [a test project with business intent 788 served by a slice, an empty tracker and no plan file] is set up

`@goal-1` `@expectation-1` `@F7` `@F10`
## Scenario: The play makes the plan file, one epic and one story for each feature, and each has a tracker issue
* When I run "/shape-plan 788" and answer "yes"
* Then the exit code is 0
* And the file [the plan file of business intent 788] exists
* And the file [the plan file of business intent 788] field [the epics field of the plan file] has 1 items
* And the file [the plan file of business intent 788] field [the stories field of the plan file] has 2 items
* And the file [the plan file of business intent 788] contains [the line that names the first feature in its story]
* And the file [the plan file of business intent 788] contains [the line that names the second feature in its story]
* When I run [the command that saves the tracker's issues of business intent 788 to a file]
* Then the file [the tracker export file] field [the epics field of the tracker export file] has 1 items
* And the file [the tracker export file] field [the stories field of the tracker export file] has 2 items
* And the file [the tracker export file] contains [the line that names the first feature in its story]
* And the file [the tracker export file] contains [the line that names the second feature in its story]

`@goal-2`
## Scenario: The plan file names each feature and its capability, each with its ICE
* When I run "/shape-plan 788" and answer "yes"
* Then the exit code is 0
* And the file [the plan file of business intent 788] contains [the name of the first feature]
* And the file [the plan file of business intent 788] contains [the name of the second feature]
* And the file [the plan file of business intent 788] contains [the name of the capability of both features]
* And the file [the plan file of business intent 788] contains [the ICE of the first feature as the product model gives it, without its Fails if lines]
* And the file [the plan file of business intent 788] contains [the ICE of the second feature as the product model gives it, without its Fails if lines]
* And the file [the plan file of business intent 788] contains [the ICE of the capability of both features as the product model gives it, without its Fails if lines]

`@goal-3` `@F9` `@F11`
## Scenario: A second run makes no second epic, no second story and no second plan file
* When I run "/shape-plan 788" and answer "yes"
* And I run "/shape-plan 788" and answer "yes"
* And I run [the command that saves the tracker's issues of business intent 788 to a file]
* Then the file [the tracker export file] field [the epics field of the tracker export file] has 1 items
* And the file [the tracker export file] field [the stories field of the tracker export file] has 2 items
* And the file [the plan file of business intent 788] field [the epics field of the plan file] has 1 items
* And the file [the plan file of business intent 788] field [the stories field of the plan file] has 2 items
* And the folder ".garura/project/plans" holds 1 files

`@expectation-2` `@F8` `@F11`
## Scenario: No story and no plan file holds a line of the hidden file
* When I run "/shape-plan 788" and answer "yes"
* And I run [the command that saves the tracker's issues of business intent 788 to a file]
* And I run [the command that saves the lines that the stories and the plan file share with the hidden file to a file]
* Then the file [the shared lines file] field [the lines field of the shared lines file] has 0 items
* And the file [the tracker export file] does not contain "### Failure conditions"
* And the file [the tracker export file] does not contain "### Recovery"
* And the file [the tracker export file] does not contain "Way back:"
* And the file [the tracker export file] does not contain "Who fixes:"
* And the file [the tracker export file] does not contain [the Fails if line of the first feature]
* And the file [the tracker export file] does not contain [the Fails if line of the second feature]
* And the file [the tracker export file] does not contain [the Fails if line of the capability of both features]
* And the file [the plan file of business intent 788] does not contain "### Failure conditions"
* And the file [the plan file of business intent 788] does not contain "### Recovery"
* And the file [the plan file of business intent 788] does not contain "Way back:"
* And the file [the plan file of business intent 788] does not contain "Who fixes:"
* And the file [the plan file of business intent 788] does not contain [the Fails if line of the first feature]
* And the file [the plan file of business intent 788] does not contain [the Fails if line of the second feature]
* And the file [the plan file of business intent 788] does not contain [the Fails if line of the capability of both features]

`@expectation-3`
## Scenario: The plans for #717 and its partner give the same trees that were filed by hand on 2026-10-21
* Given [a test project that holds #717 and its partner, served by slices, with the trees that were filed by hand on 2026-10-21] is set up
* When I run "/shape-plan 717" and answer "yes"
* Then the exit code is 0
* And the file [the plan file of #717] field [the tree field of the plan file] equals [the tree of #717 that was filed by hand on 2026-10-21]
* When I run [the shape-plan command for the partner of #717] and answer "yes"
* Then the exit code is 0
* And the file [the plan file of the partner of #717] field [the tree field of the plan file] equals [the tree of the partner of #717 that was filed by hand on 2026-10-21]

`@F26`
## Scenario: No story names the eval, the hidden file or the evals folder
* When I run "/shape-plan 788" and answer "yes"
* And I run [the command that saves the tracker's issues of business intent 788 to a file]
* Then the file [the tracker export file] does not contain "eval"
* And the file [the tracker export file] does not contain "hidden"

`@F10`
## Scenario: The epic and each story get a tracker issue, also when a model page is missing
* Given [a test project where a model page of the slice is missing] is set up
* When I run "/shape-plan 788" and answer "yes"
* Then the exit code is 0
* When I run [the command that saves the tracker's issues of business intent 788 to a file]
* Then the file [the tracker export file] field [the epics field of the tracker export file] has 1 items
* And the file [the tracker export file] field [the stories field of the tracker export file] has 2 items

`@F12`
## Scenario: The plan play adds no file to the slice's evals folder
* When I run "/shape-plan 788" and answer "yes"
* Then the exit code is 0
* And the folder [the slice's evals folder] holds 1 files
* And the file [the slice file of the eval] does not exist

## Untestable

None. Every goal, expectation and failure condition of this story has a scenario.

## Lines covered

- `@goal-1`: When the product owner runs /shape-plan on a business intent, the intent's one plan file (.garura/project/plans/<intent>.yaml) exists, with one epic for each slice that serves the intent and one story for each feature of that slice.
- `@goal-2`: The plan names every capability and feature it holds, each with its ICE.
- `@goal-3`: A second run finds the plan, the epics and the stories that exist, and makes no copies of them.
- `@expectation-1`: The product owner runs /shape-plan 788 in Claude Code after /shape-slice and finds the plan file, one epic, and one story for each feature of the slice.
- `@expectation-2`: No story holds any line from the hidden file.
- `@expectation-3`: Building the plans for #717 and its partner gives the same trees that were filed by hand on 2026-10-21.
