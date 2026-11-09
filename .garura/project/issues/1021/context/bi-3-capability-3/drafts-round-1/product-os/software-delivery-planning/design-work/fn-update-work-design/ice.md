Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: When the work under the chosen item, a project standard it follows, or what the build finds no longer matches the design, the technical lead confirms an update that is in force from its confirmation, and what held before stays readable as it was, with who changed it, when and why.
- Limit: The design is never edited in place; an update replaces only the parts the change touches and keeps what held before.
- Limit: An update keeps the first design's rules: it starts from the builder's part, holds no eval, test, success scenario, story expectation or failure condition, follows the project's standards without changing them, and comes from the project's code and memory first, or from research only after a person approves it as a memory update.
- Limit: Only the technical lead confirms an update, each update says why with its source, and no work waits for one.
- Fails if: The design's words change in place, or what held before can no longer be read with who changed it and why.
- Fails if: The design in force changes with no confirmation by the technical lead, or a part the change does not touch changes.
- Fails if: An updated design holds an eval, a test, a success scenario, a story's expectation or a failure condition, or changes a project standard.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the design in force and the versions before it, what changed in the work items, the project standard that was updated or the gap that was closed, the developer's recorded reason for building another way, the builder's part of the changed work items and their collected context, and the project's code as it is now.
- Never read: the test writer's part, the plan's evals folder, the eval, the slice's hidden file and any ICE page.
- Persona: the technical lead, who confirms each update of the design; the developer builds from the design in force.
- Scope: In: updating the design of the chosen work when the work, a project standard or the build changes it, keeping what held before with why. Out: the first design, changing the plan and its work items, updating a project standard, changing the tests and the code, and the product model.

## Expectation
- Scenario: In a shop's checkout, the developer builds the receipt function in the payments module instead of the orders module the design named, and writes down that the payments module already sends mail. The agent proposes bringing the design up to what was built; the technical lead confirms it. The design in force names the payments module; the earlier version stays readable, marked replaced, with the developer's reason, who confirmed the update and when. No other part of the design changed.
- Done means: Someone other than the one who updated the design compares the version in force with the one before, and finds only the parts the change touches changed, each with its reason and source, the earlier version readable as it was, the technical lead's confirmation, and no eval, test, expectation or failure condition in it.
