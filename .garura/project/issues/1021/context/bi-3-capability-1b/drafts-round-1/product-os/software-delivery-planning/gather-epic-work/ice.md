Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: The work of the epic a person or Orchestrate agent work through planning names, its stories and each story's chores, bugs and spikes with their text and status, and the context each story's guidance points to, is gathered from the plan and the tracker into short-term memory, with what the builder receives kept apart from what the tests are written from.
- Limit: The builder's share holds no eval, no test and no success scenario, and names no ICE page, hidden file or evals folder.
- Limit: Context comes from the project's code and memory first, then Garura memory, then Phoenix memory; only when none of them answers is it researched, and the research is used only after a person approves it as a memory update. Nothing comes from what the AI agent knows by itself.
- Limit: Gathering chooses no epic and changes no work item, plan file or status; what does not match is named, not fixed.
- Fails if: An item under the epic in the plan file is missing from the gathered work, or an item from outside the epic is in it.
- Fails if: The builder's share holds a story's expectations, an eval or a test, or names an ICE page, the hidden file or the evals folder.
- Fails if: A part of the collected context has no source in the project, in memory or in a memory update a person approved.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the epic that was named, the plan file that holds it with its tree, kinds, statuses and marks, each item's text in the tracker, each story's Context guidance and what it points to, and the ontology's rules for each kind of work item and for the build's context sub-agent.
- Never read: the plan's evals folder, the eval, the slice's hidden file and any ICE page.
- Persona: the developer, a person or an agent who starts the build of an epic, and the agent that builds each story from what is gathered for it.
- Scope: In: finding the work under a named epic, reading each item's text and status, collecting each story's context, and keeping the builder's share apart from the test share. Out: choosing the epic, the order and status of the work, making and changing work items, writing the evals, designing the work, writing the tests and the code, fixing defects, and the ICE itself.

## Expectation
- Scenario: A developer names the epic of a team's planning tool that holds three stories, with a bug under one and a chore under another. The gathered work holds the three stories, the bug and the chore with their text and status. Each story's context is collected from the project's code and memory, each part with its source. The builder's share holds each story's goals, limits and context and no expectation; the test share holds the three stories' expectations. Nothing in the tracker or the plan file changed.
- Done means: Someone other than the one who gathered the work compares it with the plan file's tree and the tracker, and finds every item of the epic, none from outside it, and the same text and status.
- Done means: Someone other than the one who gathered the work searches the builder's share and finds no expectation, eval, test, hidden file, evals folder or ICE page, and finds behind each part of the collected context a source in the project, in memory or in a memory update a person approved.
