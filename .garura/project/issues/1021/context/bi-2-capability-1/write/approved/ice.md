## Intent
- Goal: The project's architecture, with its technology, is set once for the whole project, each choice written down with its reasons, its source and the person who confirmed it, and every slice is designed and built on it, while the architecture is updated as the project changes.
- Limit: Each choice is proposed from Phoenix memory's architecture and technology learnings first; only when they have no answer is the choice researched, and the research is used only after a person approves it as a memory update. No choice comes from what the AI agent knows by itself.
- Limit: Nothing waits for the architecture. A missing choice is named as a gap, and the work goes on from the project's code and memory.
- Limit: Only a person confirms a choice or an update, and an update replaces what held before without editing it, so the old architecture stays readable with why it changed.
- Fails if: An architecture choice is made with no memory behind it and no approved memory update.
- Fails if: Two slices of one project use different technology for the same job, and nothing in the architecture or its updates explains it.
- Fails if: A choice is written with no person's confirmation.
- Fails if: Work stops because a choice of the architecture is missing.
- Fails if: The architecture was updated and no one can read what held before and why it changed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: Phoenix memory's architecture and technology learnings, with the conditions each fits and when each is outgrown; the project's code and its settings; the product profile with its shape and quality levels; the business intents; and the project's architecture as set so far, with the decisions behind it.
- Persona: the architect, who decides the project's architecture and its technology, and the product owner, who asked that every builder work from the same architecture.
- Scope: In: proposing, setting and updating the project's architecture, with its technology, for the whole project. Out: each slice's design through the lenses, the product profile, writing and keeping decision records, seeding memory, moving a memory update into Phoenix memory, surfaces, deployment, environments and the lock.

## Expectation
- Scenario: The architect of a new project confirms one deployable unit split into modules, with a language and a framework for it, each proposed from a Phoenix memory learning. Two slices built later use them. When the product outgrows the one unit, the architecture is updated, and what held before stays readable with why it changed.
- Done means: Someone other than the one who set the architecture checks each choice and finds behind it a Phoenix memory learning or an approved memory update, its reasons and the person who confirmed it, and for each update, what held before and why it changed.
- Done means: Someone other than the builder compares the technology of two built slices with the architecture, and finds no difference that the architecture or a recorded update does not explain.
