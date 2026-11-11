Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: When the project needs another environment, or an environment's data, size, network, access or settings must change, a person confirms an update that is in force from its confirmation, and what held before stays readable as it was, with what replaced it and why.
- Limit: Each update is proposed from the project's own memory and code first, then from Garura memory, then from Phoenix memory; only when none of them answers is it researched, and the research is used only after a person approves it as a memory update. No update comes from what the AI agent knows by itself.
- Limit: A declaration is never edited in place; an update replaces what held before and keeps it, no update brings production in or leaves fewer than dev, testing and pre-production, and an update reaches a built environment only through a build step after a person's yes.
- Limit: Only a person confirms an update, each update names its reason and its source, and no work waits for one.
- Fails if: The words of a declaration change in place, or what held before can no longer be read.
- Fails if: An environment's declaration changes with no person's confirmation, or with no reason.
- Fails if: An update brings production in, leaves fewer than dev, testing and pre-production, or leaves two answers in force for one property of an environment.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the declarations in force and what they replaced; what changed in the project, such as a new environment in the pipeline files, a new setting in the example settings file, an update of the deployment design, a compliance need that changed in the product profile, or a changed set-up answer; and the Phoenix memory learnings a property names as its source, as they are now.
- Never read: the value of any secret, such as a password or a key, and anything in production, such as its data.
- Persona: the devops engineer, who decides when an environment is added or its setup changes.
- Scope: In: updating which environments the project has and how each is set up as the project changes, and keeping what held before with why it changed. Out: declaring the first environments, applying an update to a built environment, updating the deployment design, raising a compliance need in the product profile, decision records, opening a locked design, production, and moving a memory update into Phoenix memory.

## Expectation
- Scenario: The deployment design of a team's planning tool gains a step for performance tests before pre-production. An update proposes a new environment there, with its own made-up data, a size fit for the load the tests need and access for the team only, and names the deployment design update as its source. The devops engineer confirms it with its reason. The new environment is declared and not built until a deployment needs it, and the old list of environments stays readable, marked replaced, with why it changed.
- Done means: Someone other than the one who made the update reads the declarations and finds one answer in force for each property of each environment, the source and the reason behind the update, the person who confirmed it, what held before as it was, at least dev, testing and pre-production, and no production.
