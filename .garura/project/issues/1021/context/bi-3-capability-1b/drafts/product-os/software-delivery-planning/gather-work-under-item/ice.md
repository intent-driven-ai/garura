Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: The item the technical lead names by its ID, at any level of the plan, and every item under it, with their text and status, and the context each gathered story's guidance points to, are gathered from the plan and the tracker into short-term memory, nothing outside the chosen item's tree, with what the builder receives kept apart from what the tests are written from.
- Limit: The builder's part holds no eval, no test and no success scenario, and names no ICE page, hidden file or evals folder.
- Limit: Context comes from the project's code and memory first, then Garura memory, then Phoenix memory; only when none of them answers is it researched, and the research is used only after a person approves it as a memory update. Nothing comes from what the AI agent knows by itself.
- Limit: Gathering changes no work item, plan file or status; what does not match is named, not fixed.
- Fails if: An item under the chosen item in the plan file is missing from the gathered work, or an item from outside its tree is in it.
- Fails if: The builder's part holds a story's expectations, an eval or a test, or names an ICE page, the hidden file or the evals folder.
- Fails if: A part of the collected context has no source in the project, in memory or in a memory update a person approved.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the ID that was named, the plan file that holds it with its tree, kinds, statuses and marks, each item's text in the tracker, each gathered story's Context guidance and what it points to, and the ontology's rules for each kind of work item and for the build's context sub-agent.
- Never read: the plan's evals folder, the eval, the slice's hidden file and any ICE page.
- Persona: the technical lead, who names the plan item and designs the work from what is gathered under it.
- Scope: In: finding the whole tree under a named item, reading each item's text and status, collecting each gathered story's context, and keeping the builder's part apart from the test writer's part. Out: choosing the item, the order and status of the work, making and changing work items, designing the work, writing the evals, writing the tests and the code, fixing defects, and the ICE itself.

## Expectation
- Scenario: The technical lead of a team's planning tool names a feature item by its ID. It groups two stories, one with a bug under it. The gathered work holds the feature item, the two stories and the bug, with their text and status, and nothing else of the epic above it. Each story's context is collected from the project's code and memory, each part with its source. The builder's part holds each story's goals, limits and context and no expectation; the test writer's part holds the two stories' expectations. Nothing in the tracker or the plan file changed.
- Done means: Someone other than the one who gathered the work compares it with the plan file's tree and the tracker, and finds every item under the chosen item, none from outside its tree, and the same text and status.
- Done means: Someone other than the one who gathered the work searches the builder's part and finds no expectation, eval, test, hidden file, evals folder or ICE page, and finds behind each part of the collected context a source in the project, in memory or in a memory update a person approved.
