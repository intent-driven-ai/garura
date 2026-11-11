# Feature: Lock the design

## What it does
A person locks the project's design as it stands, the architecture with its technology, the surfaces, the deployment design and the environments, with each open choice named as a gap, so every agent builds from one version a person chose.
- The project's design is what the other four capabilities of the Spec → Design business intent set for the whole project: the architecture with its technology (Design the technology and architecture), the surfaces (Manage surfaces), how the whole project runs (Deployment design) and the environments (Environment setup). Each position has a version in force, confirmed by a person, and names its open choices as gaps.
- When the product owner asks to lock, an agent shows the design as it stands, read from the project's records: for each position, its version in force, what it holds, the person who confirmed it, its gaps, and the decision records behind it, accepted or still proposed. A decision record says what was decided, why, and what else was weighed. The product owner sees what agents will build from before saying yes.
- The product owner locks it with a yes, and a reason when there is one. A position not set at all is named as a gap; the lock never waits for it.
- The lock records four things about the version it fixes:
  - the version of each position it covers, with a fingerprint of its words, a short code worked out from the text, so that a later change to those words is caught;
  - each gap, so the builders and any later step know the choice was left open on purpose, not forgotten;
  - the decision records of that version, each with its status;
  - the person who locked it, when, and why.
- From that moment the lock is in force, and each build of a work item starts from it (fn-check-lock). A work item is an epic, a story, a chore or another piece of work in the team's tracker.
- How it meets the capability: this is the step where a person hands the design to agents. Before it, no agent starts a build; after it, every build starts from the version the person locked.

Status: not built. What exists covers only parts of it:
- Older design skills wrote each design file with a status that went from draft to validated to locked, and Garura's glossary says such a file moves to locked after a person's review. No step ever set a file to locked, and no play calls those skills.
- Approval of every piece of the product model was decided: a person approves exact words, and the piece keeps a fingerprint of them, who approved it, when and in which review. The step that writes approval is not built, so nothing writes it.
- A decision record is accepted only on a person's word, by one command of its tool, and names who accepted it. It is the nearest built step to a lock, for one decision at a time.
- The product profile has a locked state, the product's box fixed, but no play sets it since the play that did was dropped.
- The stale build play asked a person to approve each epic's spec before its build ran on its own. That approval is now switched off by a setting, and the play waits for a rebuild.

## Inputs / Outputs
- In: the design as it stands: the version in force of each of the four positions, with what it holds, its gaps and the person who confirmed it.
- In: the decision records behind that version, accepted or still proposed.
- In: the lock in force, when there is one.
- In: the product owner's yes, with a reason when there is one.
- Out: what the lock would cover, shown to the product owner before the yes: each position, its gaps and its decision records.
- Out: the lock: the version of each position with its fingerprint, the gaps, the decision records with their status, the person who locked it, when and why.
- Out: when a lock was already in force, that lock kept as it was and marked replaced.

## Rules & behavior
- Only a person locks. An agent shows the design and records the person's yes; it never locks by itself, and no setting lets it. The reason: as with confirming a business intent or accepting a decision record, which Garura leaves to a person alone, the lock decides what agents may do, so an agent never grants it to itself.
- The product owner sees what is locked before the yes: each position, its gaps and each decision record still proposed. The reason: a yes to something not shown is no yes.
- Only a confirmed version of a position can be locked. A draft no person confirmed is not part of the lock. The reason: each position holds only what a person confirmed, and the lock must not hand agents anything less.
- The design is locked as it stands. A missing choice, or a position not set at all, is named as a gap, and the lock never waits for it. The reason: each position treats a missing choice as a gap, not a stop, and the business intent must not block on anything except the lock.
- A decision record still proposed does not hold back the lock; the lock names it as proposed. The reason: Manage ADRs accepts each record on its own path, and the lock must not wait on another step.
- One lock covers the whole design. The reason: a build reads all four positions together, and locks set at different moments for each could hand one build four moments.
- The lock keeps a fingerprint of each position's words. The reason: a write to the product model is never blocked, so a later change to a locked position must be caught by its words, with no play having to remember to flag it.
- What the lock shows is read from the project's records: the positions, their gaps, the decision records and the earlier locks, from the project's own memory and code first, then Garura memory, then Phoenix memory. Nothing comes from what the AI agent knows by itself; a question no memory answers is raised as a memory update for a person to approve. The reason: the product owner locks what the project holds, not what an agent believes.
- A lock is never edited. A new lock replaces it, and the old one stays readable, marked replaced. The reason: each build must stay explainable by the lock it started from.
- Not decided: where the product owner gives the yes: the end review of the Spec → Design loop, a set of plays run in rounds until its goal is met; the tool where people review what agents make; or a command a person runs, like the accept step of a decision record. Its final place is settled when it is built.
- Not decided: where the lock is kept. The product model has no kind for the project's design.

## Acceptance criteria
- Given a design with its four positions and the data store left open, when the product owner locks it, then the lock covers each position's version with its fingerprint, names the data store as a gap, and names the product owner, the date and the reason.
- Given a new project with no position set, when the product owner locks it, then the lock names every position as a gap, and builds can start.
- Given an agent that tries to lock with no person's yes, when it tries, then nothing is locked.
- Given an architecture update that no person confirmed yet, when the design is locked, then the lock covers the confirmed version, not the draft.
- Given a decision record still proposed, when the design is locked, then the lock names it as proposed and is not held back.
- Given a lock in force, when the product owner locks again, then the earlier lock stays readable as it was, marked replaced.
- Given the lock, when someone who did not lock it reads it, then they can name what it covers, its gaps, who locked it, when and why, without asking a person.

## Out of scope
- Checking the lock when a build starts. Check the lock before an agent builds (fn-check-lock) does it.
- Locking an update and naming the work started on the old version. Update the locked design as the project changes (fn-update-locked-design) does it.
- Setting and confirming each position. The other four capabilities of the Spec → Design business intent own them.
- Accepting a decision record. Manage ADRs (Orchestration) owns the records.
- Confirming a business intent. Only a person confirms one, as today, and the lock never does.
- Locking the product profile. Specify the product owns the profile, and an approved decision moves its box.

## Sources
- The one line the product owner agreed on 2026-11-03: "A design is locked before agents take over. This is the only gate, because without it agents drift."
- The product owner on 2026-11-08: "lock this design and bi-2 is locked"
- .garura/product/product-os/intents/bi-2.md: "a design is locked before agents take over.", "No agent builds from a design that isn't locked.", "Block on anything except the lock, which is the only gate."
- .garura/product/product-os/software-delivery-planning/domain.md: "It serves the product owner, who names the work and approves its design, and the plays that build from that design."
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "A missing choice is a gap, not a stop.", "the gap stays on record so a later step knows it was skipped, not forgotten."
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/fn-set-architecture/feature.md: "Only a confirmed choice becomes part of the project's architecture."
- core/components/skills/author-technical-approach/schemas/architecture.yaml: "Lifecycle: DRAFT → VALIDATED → LOCKED"
- core/grounding/glossary.md: "an architecture artifact starts DRAFT, moves to LOCKED after human review; agents treat it as authoritative thereafter"
- docs/adr/033-approval-in-the-product-model.md: "a person accepted these exact words.", "A piece changed after it was approved is caught by its fingerprint, with no play having to remember to flag it.", "Until they are, nothing writes approval."
- standards/rules/gate-config.md, in Phoenix memory: "only a person confirms a business intent", "only a person accepts a decision record"
- core/components/skills/author-decision/scripts/adr.py: "proposed -> accepted, on a person's word"
- core/components/plays/record-decision/SKILL.md: "Only a person accepts an ADR."
- standards/schemas/product-os/decision.yaml, in Phoenix memory: "accepted decisions are not edited — supersede or amend with a new record"
- standards/schemas/product-os/spine.yaml, in Phoenix memory: "locked (no play sets it now, ADR 053)"
- core/components/plays/build-epic/reference/ice.md: "the build does not start until they approve it.", "The spec-approval checkpoint is no longer a pinned human gate: it resolves"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "What a rule can stop is work, never a write"
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "None. Every kind a question or a relationship names is defined above."
