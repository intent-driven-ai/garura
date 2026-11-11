Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Every work item under the named epic, its stories and each story's chores, bugs and spikes, is gathered with its text and status into short-term memory, and each story is split so the builder's share holds its goals, limits and Context guidance and the test share holds its expectations.
- Limit: Only the plan file's tree and its marks say what is in the epic; no item is found by its title, and the tracker is read only through the tool that knows it.
- Limit: Gathering chooses no epic and changes no work item, plan file or status; what does not match is named, not fixed.
- Limit: The builder's share holds no expectation, eval or test, and names no ICE page, hidden file or evals folder.
- Fails if: An item under the epic in the plan file is missing from the gathered work, or an item from outside the epic is in it.
- Fails if: The builder's share holds a story's expectations, or names an ICE page, the eval, the hidden file or the evals folder.
- Fails if: A work item, the plan file or a status changed during gathering.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the epic that was named, the plan file that holds it with its tree, kinds, statuses and marks, each item's text in the tracker, the fixed parts of a story's text, and the ontology's rules for each kind of work item and its parent.
- Never read: the plan's evals folder, the eval, the slice's hidden file and any ICE page.
- Persona: the developer, a person or an agent who starts the build of an epic.
- Scope: In: finding the work items under a named epic, reading their text and status, splitting each story into the builder's share and the test share, and naming what does not match. Out: choosing the epic, statuses, changing work items, collecting each story's context, writing the tests and writing the evals.

## Expectation
- Scenario: A developer names the epic of a clinic's self-booking slice. Its two stories, one with a bug under it, are gathered with their text and status. The builder's share holds each story's goals, limits and Context guidance, and the test share holds each story's expectations. The plan file holds a chore that the tracker does not have; it is named, the developer chooses to go on, and the plan file and the tracker are unchanged.
- Done means: Someone other than the one who gathered the work compares it with the plan file's tree and the tracker, finds every item of the epic and none from outside it, and finds no expectation and no name of an ICE page, the eval, the hidden file or the evals folder in the builder's share.
