# Feature: Update the deployment design as the project changes

## What it does
When the project outgrows how it runs, or a part of the design or a cloud's cartridge must change, a person confirms an update, and what held before stays readable with why it changed.
- The deployment design says how the whole project runs: its physical architecture, which services run, on what container platform and on which cloud; the path through the environments Environment setup declares, ending at pre-production, and the one design each environment is built from; the pipeline for continuous integration and continuous delivery; the tests in each environment; release and rollback; where secrets and settings are kept; and the cost on each cloud. Design how the project runs (fn-design-how-project-runs) sets it. Each cloud's cartridge, one ready pack for one cloud that the design reads, is prepared by Prepare a dedicated cartridge for each cloud: AWS, GCP and Azure (fn-cloud-cartridges).
- A project changes as it grows. For example: the architecture splits one deployable unit into parts that each release on their own, so new services must run; a new surface, such as a mobile app, must be reached; the product profile commits to a higher reliability; the project outgrows its container platform; the cost grows past what was planned; the team moves to another cloud, so the physical architecture is mapped onto that cloud's cartridge; a cloud changes its services or its prices, so its cartridge, and the costs drawn from it, change; or a new environment is set up in the path before pre-production.
- The update is proposed from the project's own memory and code first: what the files now show, such as a new pipeline, new Kubernetes files or another cloud's services; an update of the architecture or of the surfaces; a release that went wrong or was taken back, and why; a quality level that rose in the product profile; or a set-up answer that changed when the project set-up step (initialize) ran again. Then it is proposed from the cartridges and Garura memory, the memory Garura keeps for the project, and from Phoenix memory, the shared memory on the machine that every project draws from, including a learning or a cartridge entry that a part names as its source and that has changed, or a learning whose own conditions for being outgrown are now met.
- Only when no memory has an answer does the agent research the update. It raises what it found as a memory update, a proposed addition to memory, for a person to approve, and the update waits for that approval. No update comes from what the AI agent knows by itself.
- An update of a cartridge names the costs and the parts of the design drawn from it, and they are proposed again with it.
- No update brings production into the project's path. The path still ends at pre-production.
- A person confirms the update, with its reason.
- From its confirmation, the updated design or cartridge is the one in force. What held before is kept as it was, marked replaced, and points to the update, with what changed and why.
- How it meets the capability: how the project runs is designed once and changes as the project changes. This feature is how the design and the cartridges change, without losing what held before.

Status: not built. What exists covers only parts of it:
- The design play for a slice's run is stale. Run again, it adds or changes one environment and keeps the others as they were, and it carries the rest of the slice's run design forward unless the new environment forces a change, which it records as a decision. A new decision replaces an old one and never edits it. Nothing does this for the whole project.
- Phoenix memory's learnings for running say when each is outgrown, for example when one deployable unit holds the product back and its parts must release on their own, or when a cloud's container service is outgrown and its managed Kubernetes is needed. Nothing reads them to propose an update.
- No cartridge exists to update.
- A decision record about the product can be replaced through the decision play: an accepted record is never edited, a new record replaces it, and the old one points forward to it. Nothing ties this to the deployment design.
- The project set-up step, initialize, will run again when the project changes, such as when it gains a database or a web surface, and propose the earlier answers again. It is not built.

## Inputs / Outputs
- In: the design and the cartridges in force, and what changed in the project or in a cloud that calls for an update.
- In: the project's files as they are now, the architecture and the surfaces as they are now, the product profile as it is now, and the set-up answers once initialize is built.
- In: what happened to releases since the design was set, such as a release that was taken back and why.
- In: the Phoenix memory learnings and the cartridge entries that a part names as its source, as they are now.
- In: a memory update a person approved, when no memory had an answer and the agent researched the update.
- In: the person's confirmation of the update, with its reason.
- Out: a memory update for each part of the update the agent researched, waiting for a person's approval.
- Out: the updated design or cartridge, in force from the confirmation, with the reason, the source and the person who confirmed it, and, for a cartridge, the costs and parts of the design proposed again from it.
- Out: what held before, kept as it was and marked replaced, pointing to the update, with what changed and why.

## Rules & behavior
- The project's memory first. An update is proposed from the project's own memory and code first, then from the cartridges and Garura memory, then from Phoenix memory. The reason: a change in the project's files, its architecture, its releases, its profile or a cloud is the evidence for the update, and anyone can read it to judge the update.
- Research only when no memory has an answer, and only through a memory update. The agent uses what it found only after a person approves it. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- Never from the AI agent's own knowledge. An update with no source behind it is not proposed. The reason: the agent's own knowledge can be neither checked nor read back.
- An update replaces what held before and never edits it. The reason: releases already made on the old design must still be explainable, and a reader must be able to see which design held when.
- An update says why: what changed in the project or in the cloud, with its source. The reason: the next person can then tell a step of growth from a mistake that was put right.
- A person confirms each update. The reason: the design decides how every change is run and released, and what the project pays to run, so changing it is a person's decision, never an agent's.
- An update of a cartridge carries through. The costs and the parts of the design drawn from it are proposed again with it. The reason: a cost worked out from an old price looks current while it is not.
- No update brings production into the path. The reason, in the product owner's words: "We are never touching production."
- An update follows the rules of a first design too: the path through the environments Environment setup declares ends at pre-production, each environment is built from the one reused design, every part of the architecture has a place to run, every release has a way back that keeps stored data, each part names its source, the cost is shown on all three clouds the same way, the design never holds a secret's value, and the product profile sizes each choice. The reason: an updated design must be as well founded as the first one.
- One answer in force for each part of the design and each cartridge entry. The reason: an agent that finds two would pick one, and the next agent might pick the other.
- Nothing waits for an update. An update in progress, or one waiting for a memory update, does not stop design, build or release. The reason: the Spec → Design business intent must not block on anything except the lock.
- Not decided: how what already runs is moved onto an updated design, such as moving the project to another cloud. Carrying it out is work for the build and the delivery, from work items.
- Not decided: how the deployment design is updated once the design is locked. Lock the design owns the lock, the only gate, and it is not built.

## Acceptance criteria
- Given a design for one deployable unit, and an architecture updated to split it into parts that each release on their own, when an update is proposed, then it proposes a service, a container platform and a place in the path for each new part, and names the architecture update.
- Given a declared mobile app that the design does not reach, when an update is proposed, then it proposes how the app reaches people's phones, with its source.
- Given a product profile whose reliability level rose, when an update is proposed, then the release, the rollback and the tests are proposed again against the new level.
- Given the person decides to move the project to another cloud, when an update is proposed, then the physical architecture is mapped onto that cloud's cartridge and every part that finds no service there is named as a gap.
- Given a cloud whose prices changed in its cartridge, when the cartridge is updated, then the costs drawn from it are worked out again and named in the update.
- Given an update that would add production to the path, when it is checked, then it is refused, and the path still ends at pre-production.
- Given a Phoenix memory learning that a part names as its source, and whose condition for being outgrown is now met, when an update is proposed, then it names the learning and the condition.
- Given an update that no memory has an answer for, when it is proposed, then the agent researches it, raises a memory update with what it found, and the update waits until a person approves the memory update.
- Given an update with no source behind it, when it is checked, then it is not proposed.
- Given an update the person confirmed, when it lands, then the updated design or cartridge is in force, and what held before is readable as it was, marked replaced, with what replaced it and why.
- Given an update that no person confirmed, when it is asked for, then the design and the cartridges do not change.
- Given someone edits the design or a cartridge in place, when the edit is made, then it is written as an update that replaces what held before, and the old text stays as it was.
- Given an update in progress, when a slice is designed, built and released, then the work goes on.

## Out of scope
- Setting the first design. Design how the project runs (fn-design-how-project-runs) does it.
- Preparing the first cartridges. Prepare a dedicated cartridge for each cloud: AWS, GCP and Azure (fn-cloud-cartridges) does it.
- Moving what already runs onto the updated design, such as the project onto another cloud. The build and the delivery do it (Code → Validation and Validation → Run), from work items that Turn intents into agent work makes.
- Setting up a new environment. Environment setup owns it.
- Updating the parts of the system and their technology. Design the technology and architecture owns them, and a change of cloud or platform can call for an update there.
- Raising a quality level in the product profile. Specify the product owns the profile, and a decision moves it.
- Writing and keeping the decision record behind an update. Manage ADRs owns decision records.
- Opening a locked design for an update. Lock the design owns the lock.
- Moving an approved memory update into Phoenix memory. A person does it on purpose, as a promotion, outside this work.

## Sources
- The one line the product owner agreed on 2026-11-03: "How the product gets deployed is designed."
- The product owner on 2026-11-08, on the first drafts: "We are never touching production.", "We need dedicated cartridges for AWS, GCP, and Azure.", "Which cloud?"
- .garura/product/product-os/intents/bi-2.md: "Each position is written down and can change later.", "Block on anything except the lock, which is the only gate."
- core/components/plays/shape-run-lens/reference/ice.md: "design is written once and carried forward unchanged unless the target environment forces a change", "Re-running re-derives the target environment; accepted decisions are"
- core/components/plays/shape-run-lens/SKILL.md: "Incremental: re-run to add or edit an environment; the rest are preserved."
- knowledge/technology/gcp-modular-monolith-runtime.md, in Phoenix memory: "Scale, team size, or independent-deploy pressure crosses the line where one deployment holds", "Reach for GKE only when you genuinely outgrow Cloud Run (long-lived connections, complex"
- standards/schemas/product-os/decision.yaml, in Phoenix memory: "accepted decisions are not edited — supersede or amend with a new record"
- core/components/plays/record-decision/SKILL.md: "keeps every older ADR pointing forward", "Only a person accepts an ADR."
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "The box moves ONLY by an approved decision."
- .garura/product/product-os/software-delivery-planning/initialize/fn-rerun-initialize/feature.md: "when the project changes: it gains a database, a web surface, personal data or a new tracker, or it drops one."
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/fn-update-architecture/feature.md: "it gains a database or a new surface"
- core/components/plays/release-increment/reference/ice.md: "Records a deploy evidence record — the target environment, what ran, the address, and the health"
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- core/tools/memory/GUIDE.md: "Your work goes on while the update waits, unless you cannot go on without it.", "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
- The capability list the product owner locked on 2026-11-03: "Lock the design: A design is locked before agents take over. This is the only gate", "Its final place is settled when it is built."
