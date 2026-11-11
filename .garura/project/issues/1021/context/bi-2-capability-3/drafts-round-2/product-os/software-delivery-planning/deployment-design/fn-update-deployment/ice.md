Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: When the project outgrows how it runs, or a part of the design or a cloud's cartridge must change, a person confirms an update that is in force from its confirmation, and what held before stays readable as it was, with what replaced it and why.
- Limit: Each update is proposed from the project's own memory and code first, then from the cartridges and Garura memory, then from Phoenix memory; only when none of them answers is it researched, and the research is used only after a person approves it as a memory update. No update comes from what the AI agent knows by itself.
- Limit: The design and the cartridges are never edited in place; an update replaces what held before and keeps it, and no update brings production into the project's path.
- Limit: Only a person confirms an update, each update names its reason and its source, and no work waits for one.
- Fails if: The words of the design or a cartridge change in place, or what held before can no longer be read.
- Fails if: A part of the design or a cartridge changes with no person's confirmation, or with no reason.
- Fails if: An update brings production into the path, or leaves two answers in force for one part, such as a cost still worked out from a cartridge's old prices.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the design and the cartridges in force and what they replaced; what changed in the project, such as a new pipeline, new Kubernetes files or another cloud's services in its files, an update of the architecture or of the surfaces, a release that was taken back and why, a quality level that rose in the product profile, or a changed set-up answer; what changed in a cloud's services or prices; and the Phoenix memory learnings and cartridge entries a part names as its source, with when each is outgrown.
- Never read: the value of any secret, such as a password or a key.
- Persona: the devops engineer, who decides when the deployment design or a cartridge changes.
- Scope: In: updating how the whole project runs and each cloud's cartridge as the project and the clouds change, and keeping what held before with why it changed. Out: setting the first design, preparing the first cartridges, moving what already runs onto the updated design, setting up a new environment, updating the architecture, raising a quality level in the product profile, decision records, opening a locked design, production, and moving a memory update into Phoenix memory.

## Expectation
- Scenario: A cloud raises the price of the managed database the project uses. Its cartridge is updated from the source its price entry names, and the project's cost on that cloud is worked out again and set beside the other two. The devops engineer confirms the update with its reason, the costs shown are the new ones, and the old cartridge entry and costs stay readable, marked replaced, with why they changed.
- Done means: Someone other than the one who made the update reads the design and the cartridges and finds one answer in force for each part, the source and the reason behind the update, the person who confirmed it, what held before as it was, and a path that still ends at pre-production.
