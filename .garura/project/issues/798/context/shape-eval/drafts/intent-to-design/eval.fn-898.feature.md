`@story-898`
# Feature: Story #898 — Agents build for the business intent, not only to pass the eval: the build is given the intent, never the eval

Feature fn-898 of slice sl-intent-to-design, epic #794. Written by /shape-eval from story #898 and the slice's hidden file.

## Background:
* Given [the test project with clean build plays] is set up

`@goal-1`
## Scenario: No build play, skill, agent or sub-agent is given the eval, the hidden file or the evals folder
* When I run [the lint command]
* Then the exit code is 0
* And the file [the build inputs] does not contain "evals"
* And the file [the build inputs] does not contain [the hidden file]
* And the file [the build inputs] does not contain [the slice eval file]

`@goal-2`
## Scenario: A build is given the business intent through the slice's stories
* When I run [the lint command]
* Then the file [the build inputs] contains [the story of the slice]

`@goal-3`
## Scenario: A build session that read the evals folder has a flag that names the read
* Given [the test project with a build run that read the evals folder] is set up
* When I run [the ledger check command]
* Then the file [the evidence of the build run] contains [the flag that names the read]

`@goal-4`
## Scenario: The slice has one eval that says if the business intent is met
* Given [the test project with a plan] is set up
* When I run "/shape-eval 788" and answer "yes"
* Then the file [the slice eval file] exists
* And the file [the slice eval file] contains "The eval passes only when every scenario of every story below passes."

`@expectation-1`
## Scenario: The lint check stops a build play whose inputs name the evals folder
* Given [the test project with a build play that names the evals folder, the eval and the hidden file] is set up
* When I run [the lint command]
* Then the output contains [the lint failure line]

`@expectation-2`
## Scenario: The session-ledger check flags a session that read the evals folder and passes a clean session
* Given [the test project with one build session that read the evals folder and one that did not] is set up
* When I run [the ledger check command]
* Then the file [the evidence of the reading session] contains [the flag that names the read]
* And the file [the evidence of the clean session] does not contain [the flag that names the read]

`@expectation-3`
## Scenario: After /shape-plan, /shape-eval writes the eval in the evals folder and no build play's inputs name that folder
* Given [the test project with a plan] is set up
* When I run "/shape-eval 788" and answer "yes"
* Then the folder [the evals folder of the slice] holds 6 files
* And the file [the build inputs] does not contain "evals"

`@F20`
## Scenario: The lint check fails a build play whose inputs name the evals folder, the eval or the hidden file
* Given [the test project with a build play that names the evals folder, the eval and the hidden file] is set up
* When I run [the lint command]
* Then the output contains [the lint failure line]
* And the output contains [the hidden file]

`@F21`
## Scenario: A build session that read the evals folder gets a flag in its evidence
* Given [the test project with a build run that read the evals folder] is set up
* When I run [the ledger check command]
* Then the file [the evidence of the build run] contains [the flag that names the read]

`@F22`
## Scenario: A clean build session gets no flag and the check does not stop a build
* Given [the test project with a clean build session] is set up
* When I run [the ledger check command]
* Then the exit code is 0
* And the file [the evidence of the clean session] does not contain [the flag that names the read]

`@F23`
## Scenario: A builder is not given the eval, and a read of the evals folder has a flag
* Given [the test project with a build run that read the evals folder] is set up
* When I run [the ledger check command]
* Then the file [the evidence of the build run] contains [the flag that names the read]
* And the file [the build inputs] does not contain [the slice eval file]

`@F25`
## Scenario: The eval play does not read an ICE page, the usage guide or the code
* Given [the test project with a plan] is set up
* When I run "/shape-eval 788" and answer "yes"
* Then the file [the ledger of the eval run] does not contain "feature.md"
* And the file [the ledger of the eval run] does not contain "capability.md"
* And the file [the ledger of the eval run] does not contain "ice.md"
* And the file [the ledger of the eval run] does not contain "guides/"

## Untestable

- `@F24`: no library sentence can say that a check asks for more than the goals, expectations and failure conditions of the stories; each scenario of the story files carries the tag of the line that it covers, and a person reads the tags.
