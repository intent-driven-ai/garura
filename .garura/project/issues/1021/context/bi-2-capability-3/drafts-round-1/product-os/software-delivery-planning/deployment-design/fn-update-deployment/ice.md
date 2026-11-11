Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: When the project outgrows its deployment design, or a part of it must change, a person confirms an update that is in force from its confirmation, and what held before stays readable as it was, with what replaced it and why.
- Limit: Each update is proposed from the project's own memory and code first, then from Garura memory, then from Phoenix memory; only when none of them answers is it researched, and the research is used only after a person approves it as a memory update. No update comes from what the AI agent knows by itself.
- Limit: The deployment design is never edited in place; an update replaces what held before and keeps it.
- Limit: Only a person confirms an update, each update names its reason and its source, and no work waits for one.
- Fails if: The design's words change in place, or what held before can no longer be read.
- Fails if: A part of the design changes with no person's confirmation, or with no reason.
- Fails if: Two answers are in force for one part of the design after an update.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the deployment design in force and what it replaced; what changed in the project, such as a new pipeline or platform in its files, an update of the architecture or of the surfaces, a release that was taken back and why, a quality level that rose in the product profile, or a changed set-up answer; and the Phoenix memory learnings a part names as its source, with when each is outgrown.
- Never read: the value of any secret, such as a password or a key.
- Persona: the devops engineer, who decides when the deployment design changes.
- Scope: In: updating the project's deployment design as the project changes, and keeping what held before with why it changed. Out: setting the first design, moving what already runs onto the updated design, updating the environments or the architecture, raising a quality level in the product profile, decision records, opening a locked design, and moving a memory update into Phoenix memory.

## Expectation
- Scenario: A team tool that releases to one named team first opens to the public. The agent proposes, from the product profile's new stage and the Phoenix memory learning that the release rule names as its source, that a release now goes to a small share of users first; the devops engineer confirms the update with its reason, and what held before stays readable, marked replaced, with why it changed.
- Done means: Someone other than the one who made the update reads the design and finds one answer in force for each part, the source and the reason behind the update, the person who confirmed it, and what held before as it was.
