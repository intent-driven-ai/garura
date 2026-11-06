## Intent
- Goal: A confirmed business intent becomes the work items agents execute, one epic for each slice and one story for each feature, each story written from its ICE so an agent can act on it without asking again.
- Limit: No epic, story or plan file holds a failure condition or a recovery condition.
- Limit: Only a ready ICE is drafted into a story. A feature whose ICE is not ready is named, never guessed.
- Limit: A work item is made once and found by its mark, never by its title.
- Limit: Nothing reaches the tracker, the plan file or the model before the product owner's typed yes, and what lands is what they saw.
- Fails if: A ready feature of a slice has no story, a slice has two epics, or a feature has two stories in one epic.
- Fails if: A story holds a line of a "Fails if" block of its two ICE, or a recovery phrase.
- Fails if: After a change lands, the tracker and the plan file disagree, or something changed that the person did not approve.
- Fails if: A story is drafted for a feature guessed from words that fit no feature or more than one.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the business intent, the slices the model links to it, each feature's ICE and its capability's ICE, the plan file, the work items the tracker holds, and the rules for each kind of work item.
- Never read: the slice's hidden file and the folder that holds the evals.
- Persona: the product owner, who approves the work items, and the agent that builds each story.
- Scope: In: making and changing epics, stories, chores, bugs and spikes from a confirmed business intent, and keeping the plan file's tree in step with the tracker. Out: the order, status and tracking of the work, the loops, plan branches, the slice, its hidden file, the eval, the ICE itself and the build.

## Expectation
- Scenario: A confirmed intent served by one slice with three ready features becomes one epic and three stories after the product owner's yes, and the epic's map names the three stories.
- Done means: The plan check, the draft check and the tracker check read ok: each feature has one story, no story holds a failure line, and each item is in the tracker with its type and no label.
- Done means: An agent that did not write a story builds its feature from the story and the context its guidance points to, without asking a person.
