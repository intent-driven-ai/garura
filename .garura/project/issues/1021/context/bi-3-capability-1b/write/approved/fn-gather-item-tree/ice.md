## Intent
- Goal: The item the technical lead names by its ID, at any level of the plan, and every item under it, every level down, are gathered with their text and status into short-term memory, nothing outside its tree, and each gathered story is split so the builder's part holds its goals, limits and Context guidance and the test writer's part holds its expectations.
- Limit: Only the plan file's tree and its marks say what is under the chosen item; no item is found by its title, no ID is guessed, and the tracker is read only through the tool that knows it.
- Limit: Gathering changes no work item, plan file or status; what does not match is named, not fixed.
- Limit: The builder's part holds no expectation, eval or test, and names no ICE page, hidden file or evals folder.
- Fails if: An item under the chosen item in the plan file is missing from the gathered tree, or an item from outside its tree is in it.
- Fails if: The builder's part holds a story's expectations, or names an ICE page, the eval, the hidden file or the evals folder.
- Fails if: A work item, the plan file or a status changed during gathering.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the ID that was named, the plan file that holds it with its tree, kinds, statuses and marks, each item's text in the tracker, the fixed parts of a story's text, and the ontology's rules for each kind of work item and its parent.
- Never read: the plan's evals folder, the eval, the slice's hidden file and any ICE page.
- Persona: the technical lead, who names the plan item and designs the work from the tree gathered under it.
- Scope: In: finding the whole tree under a named item, reading each item's text and status, splitting each gathered story into the builder's part and the test writer's part, and naming what does not match. Out: choosing the item, statuses, changing work items, collecting each story's context, designing the work, writing the tests and writing the evals.

## Expectation
- Scenario: The technical lead of a clinic's booking product names a story by its ID. The story and the bug under it are gathered with their text and status, and nothing else of its epic. The builder's part holds the story's goals, limits and Context guidance, and the test writer's part holds its expectations. The plan file holds a chore under the story that the tracker does not have; it is named, the technical lead chooses to go on, and the plan file and the tracker are unchanged.
- Done means: Someone other than the one who gathered the work compares it with the plan file's tree and the tracker, finds every item under the chosen item and none from outside its tree, and finds no expectation and no name of an ICE page, the eval, the hidden file or the evals folder in the builder's part.
