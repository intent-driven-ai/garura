## Intent
- Goal: Each piece of work a play files or takes in for a business intent hangs under that intent by the tracker's own parent and child link, also when the intents live in another tracker than the work, so the tracker alone shows the trace from each intent down to its work and from each piece of work up to its intent.
- Limit: Where the tracker has a parent and child link, that link is used; a mention of the intent in a text never stands in for it there.
- Limit: The link is made only through the one tool that knows the tracker, and a business intent never gets a parent.
- Limit: The model never rests on the link; an epic reaches its intents through its slice.
- Fails if: A piece of work a play filed for an intent does not hang under it, where the tracker has the link.
- Fails if: A piece of work hangs under an intent it does not serve, or is linked to its intent twice.
- Fails if: A link that cannot be made stops a person with no way past that records what is owed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the settings that name the intents tracker and the work tracker, each plan file and the intent it is given, the work items with their parents as the tracker holds them, each intent's issue with its sub-issues, and how each tracker links work across repositories or platforms.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who reads from an intent's issue the work that serves it; and the developer, a person or an AI agent who builds the code, who reads from a work item the intent it serves.
- Scope: In: the link from each piece of work to the intent it serves, inside one tracker and across trackers, and the link of an unplanned epic to the intent whose work broke. Out: the one tool that knows the tracker, each item's type and its parent under its epic or story, making the epics and stories, the model's own trace through the slice, and recording what is owed.

## Expectation
- Scenario: In a clinic's booking app, the business intents live in one GitHub repository and the work in another, in one organization. /shape-plan makes the epic for online booking, and the tracker shows it as a sub-issue of the intent it serves, across the two repositories; run again, it makes no second link. In a shop's checkout project, an unplanned epic gathers two defects found after release and hangs under the intent whose delivered work broke.
- Done means: Someone other than the one who ran the plays reads both trackers and the plan files, and finds each epic under the intent its plan is given, by the tracker's own link, linked once, and the unplanned epic under the intent whose work broke.
