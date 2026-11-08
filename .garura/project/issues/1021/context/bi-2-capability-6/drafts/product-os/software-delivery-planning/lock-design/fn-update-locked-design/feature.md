# Feature: Update the locked design as the project changes

## What it does
When a position changes after the lock, the locked version stays in force until a person locks the update, and the work already started on the old version is named, not stopped.
- A position changes as the project changes. For example: the architecture gains a search service, a mobile surface is added, the deployment design moves to another cloud, or an environment is added before pre-production.
- Each position's own update feature makes the update and has a person confirm it: Update the architecture as the project changes, Update the surfaces as the project changes, Update the deployment design as the project changes, and Update the environments as the project changes. Each of them leaves to this capability how it is updated once the design is locked.
- While an update is being made and confirmed, the locked version stays in force. Builds keep starting from it. The lock is never opened, so no build waits for an update.
- Once an update is confirmed, an agent shows the product owner what changed since the lock in force: each position's old and new version, why it changed and who confirmed it, the gaps it closes or opens, and the work items being built from the old version.
- The product owner locks the new version with a yes. From then on, builds start from it. The old lock stays readable as it was, marked replaced, with what replaced it and why.
- Work already started on the old version is named, with each work item and its status, as out of date. It is not stopped and not changed; a person decides what happens to it.
- Several updates confirmed since the last lock can be locked with one yes.
- How it meets the capability: the design is locked before agents take over, and it still changes as the project changes. This feature is how it changes with no moment when nothing is locked and with no silent drift.

Status: not built. What exists covers only parts of it:
- Older design skills refused to change a locked file and asked that it be moved back to draft first. No play calls them.
- A slice whose build has started is never changed by a shaping run. It changes only when a person approves the change, and an edit names each epic already started, with its status, as out of date, because work already started from the old text. This is built for slices, not for the project's design.
- A decision record is never edited once accepted. A new record replaces it, and the old one points forward to it.
- Each of the four positions' update features keeps what held before and why it changed, and leaves how it is updated once the design is locked to this capability.

## Inputs / Outputs
- In: the lock in force, and each position's update a person confirmed since that lock.
- In: the work items being built, each with the lock it started from.
- In: the product owner's yes, with a reason when there is one.
- Out: what changed since the lock in force, shown to the product owner before the yes.
- Out: the new lock, in force from the yes, covering each position's new version with its fingerprint, the gaps, who locked it, when and why.
- Out: the old lock, kept as it was, marked replaced and pointing to the new one.
- Out: the work items started on the old version, named as out of date with their status.

## Rules & behavior
- The locked version stays in force until the new one is locked. The reason: opening the lock would leave a time with nothing locked, and every build would then wait for the length of each update.
- Each update is made and confirmed by its position's own update feature; this feature only locks it. The reason: those features already hold the rules for each update, and a second path would let the two disagree.
- A confirmed update is not locked by its confirmation; the product owner locks it with a yes of its own. The reason: the person who confirms a position, such as the architect or the devops engineer, is not always the one who hands the design to agents.
- Only a confirmed version is locked. An update no person confirmed is not shown as ready to lock. The reason: each position holds only what a person confirmed.
- The product owner sees what changed before the yes: old and new, why, who confirmed it, and the work started on the old version. The reason: a yes to something not shown is no yes.
- Work started on the old version is named, never stopped and never changed. The reason: as built for a slice in progress, "No change to work in flight is silent.", and a person, not an agent, decides what happens to work in flight.
- A lock is never edited. The new lock replaces the old one, and the old one stays readable with why it changed. The reason: each build must stay explainable by the lock it started from.
- An update waiting for its lock stops nothing. Builds start from the locked version, and design and planning go on. The reason: the Spec → Design business intent must not block on anything except the lock.
- What is shown is read from the project's records and memory, the project's own memory and code first, then Garura memory, then Phoenix memory, never from what the AI agent knows by itself; a question no memory answers is raised as a memory update for a person to approve. The reason: the product owner locks what the project holds, and each line shown must be checkable.
- Not decided: how the work named out of date is brought onto the new version. The build owns building, from the work items that Turn intents into agent work makes.

## Acceptance criteria
- Given a locked design and an architecture update the architect confirmed, when a build starts before the product owner locks the update, then the build starts from the locked version.
- Given that confirmed update, when the product owner locks it, then the new lock covers the new architecture version, and the old lock is readable as it was, marked replaced, with why.
- Given two stories being built from the old version, when the new lock lands, then both are named as out of date with their status, and both go on.
- Given an update that no person confirmed, when someone asks to lock it, then it is not locked.
- Given updates of the surfaces and the environments confirmed since the last lock, when the product owner locks, then one new lock covers both.
- Given someone edits the lock in force, when the edit is made, then it is written as a new lock and the old one stays as it was.
- Given an update in progress, when a slice is designed and a story is built, then the work goes on.

## Out of scope
- Making and confirming each update. The update features of the other four capabilities of the Spec → Design business intent do it.
- The first lock. Lock the design (fn-lock-design) does it.
- Checking the lock when a build starts. Check the lock before an agent builds (fn-check-lock) does it.
- Bringing the work named out of date onto the new version. The build owns it (Code → Validation), from work items that Turn intents into agent work makes.
- Writing and keeping the decision record behind an update. Manage ADRs (Orchestration) owns decision records.

## Sources
- The one line the product owner agreed on 2026-11-03: "A design is locked before agents take over. This is the only gate, because without it agents drift."
- .garura/product/product-os/intents/bi-2.md: "Each position is written down and can change later.", "No agent builds from a design that isn't locked.", "Block on anything except the lock, which is the only gate."
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/fn-update-architecture/feature.md: "Not decided: how the architecture is updated once the design is locked. Lock the design owns the lock, the only gate, and it is not built.", "Opening a locked design for an update. Lock the design owns the lock."
- .garura/product/product-os/software-delivery-planning/manage-surfaces/fn-update-surfaces/feature.md: "Not decided: how the surfaces are updated once the design is locked.", "Opening a locked design for an update. Lock the design owns the lock."
- .garura/product/product-os/software-delivery-planning/deployment-design/fn-update-deployment/feature.md: "Not decided: how the deployment design is updated once the design is locked.", "Opening a locked design for an update. Lock the design owns the lock."
- .garura/product/product-os/software-delivery-planning/environment-setup/fn-update-environments/feature.md: "Not decided: how the environments are updated once the design is locked.", "Opening a locked design for an update. Lock the design owns the lock."
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/fn-update-architecture/feature.md: "Moving work already built onto the updated architecture. The build owns it (Code → Validation), from work items that Turn intents into agent work makes."
- core/components/skills/author-technical-approach/SKILL.md: "architecture.yaml is LOCKED -- drop to DRAFT first."
- docs/adr/058-an-edit-the-person-approves-may-change-a-slice-in-progress.md: "A shaping run still never touches a slice in progress", "It names each epic past ready, with its status, as out of date, because work already started from the old text.", "No change to work in flight is silent."
- standards/schemas/product-os/decision.yaml, in Phoenix memory: "accepted decisions are not edited — supersede or amend with a new record"
- core/components/plays/record-decision/SKILL.md: "keeps every older ADR pointing forward"
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
