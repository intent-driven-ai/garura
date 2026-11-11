## Intent
- Goal: The project's architecture is set once for the whole project: its style, each main part with its one job and its technology with the version, and each seam with what crosses it, each choice with its reasons, its source and the person who confirmed it.
- Limit: Each choice the project's code does not settle is proposed from Phoenix memory's architecture and technology learnings first; only when they have no answer is it researched, and the research is used only after a person approves it as a memory update. No choice comes from what the AI agent knows by itself.
- Limit: A part is named by its job, and its technology names a real product and its version.
- Limit: Only a person confirms a choice, and no work waits for one.
- Fails if: An architecture choice is made with no memory behind it and no approved memory update.
- Fails if: A choice is written with no person's confirmation.
- Fails if: A choice contradicts what the project's code already uses, and no update of the architecture explains it.
- Fails if: Two main parts hold the same job, or a seam does not say what crosses it.
- Fails if: Work stops because a choice of the architecture is missing.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: Phoenix memory's architecture and technology learnings, with the conditions each fits and when to avoid each; the project's code, its settings and how it is deployed; the product profile with its shape and quality levels; and the project's architecture as set so far.
- Persona: the architect, who confirms each choice of the project's architecture.
- Scope: In: proposing and setting the style, the main parts with their technology, and the seams of the whole system. Out: updating the confirmed architecture, each slice's own parts and seams, the platform the product runs on and its environments, the product profile, the memory the project gets, and moving a memory update into Phoenix memory.

## Expectation
- Scenario: A new internal tool for a small team is proposed one deployable unit with firm module borders and a framework with its version, each from the Phoenix memory learning that fits it, and the architect confirms them.
- Done means: An agent that did not set the architecture reads it and names the style, each main part with its job and its technology, and each seam with what crosses it, and a person other than the one who set it agrees, finding a Phoenix memory learning or an approved memory update behind each choice.
