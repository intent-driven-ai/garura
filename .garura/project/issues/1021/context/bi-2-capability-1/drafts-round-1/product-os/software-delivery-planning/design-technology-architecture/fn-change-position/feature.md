# Feature: Change a position as the project evolves

## What it does
When the project outgrows a position, a person replaces it with a new one, and the old one stays readable with why it changed.
- A position is one technology or architecture choice that holds for the whole project, written down with its reasons. Set the project's technology (fn-set-technology) and Set the project's architecture (fn-set-architecture) set them.
- A project changes as it grows. For example: it gains a database or a new surface, many more people use it, several teams start to deploy on their own schedules, or a quality level in the product profile goes up. The product profile holds the quality levels the product commits to, such as how fast or how secure it must be.
- Memory says when a choice is outgrown. Each of its architecture learnings names the style that comes after it, such as one deployable unit giving way to separate services once the product and its teams grow past the unit.
- A change is proposed the same way as a first position: from the project's code, its profile and memory, with its source and its reasons. A person confirms it.
- From its confirmation the new position is the one in force. The old one is kept as it was, marked replaced, and points to the new one, with what changed in the project and why.
- How it meets the capability: the capability's positions are set once and can evolve. This feature is how they evolve, without losing what held before.

Status: not built. What exists covers only parts of it:
- A decision record about the product can be replaced through the decision play. An accepted record is never edited: a new record replaces it, and the old one points forward to it. Nothing ties this to a position of the whole project.
- The play that designs architecture is stale and waits for a rebuild. When it runs again, it reuses its technology decision, and a new decision replaces the old one, never editing it.
- Memory's learnings each say which choice comes after them.
- An older skill refused to change a locked architecture until it was moved back to draft. No play calls it.

## Inputs / Outputs
- In: the position to change, and what changed in the project that calls for it.
- In: memory's learning that says when the position is outgrown and what comes next.
- In: the project's code and its settings, and the product profile as it is now.
- In: the person's confirmation of the change.
- Out: the new position, in force from its confirmation, with its reasons, its source and the person who confirmed it.
- Out: the old position, kept as it was and marked replaced, pointing to the new one, with what changed and why.

## Rules & behavior
- A change replaces a position and never edits it. The reason: work already built on the old position must still be explainable, and a reader must be able to see which position held when.
- A change says why: what changed in the project, with its source. The reason: the next person can then tell a step of growth from a mistake that was put right.
- A person confirms each change. The reason: a position binds every builder in the project, so changing one is the person's decision, never an agent's.
- A change follows the same proposal rules as a first position: the project's code first, a source for each proposal, and sized by the product profile. The reason: a changed position is a new position, and it must be as well founded as the first one.
- Only one position is in force for each job. The reason: an agent that finds two would pick one, and the next agent might pick the other.
- Nothing waits for a change. A change in progress does not stop design or build. The reason: the Spec → Design business intent must not block on anything except the lock.
- Not decided: how a change reaches the work already built or planned on the old position. Nothing names that work today.
- Not decided: how a position changes once the design is locked. Lock the design owns the lock, the only gate, and it is not built.

## Acceptance criteria
- Given a confirmed position and a change the person confirmed, when the change lands, then the new position is in force, and the old one is readable as it was, marked replaced, with what replaced it and why.
- Given a change that no person confirmed, when it is asked for, then no position changes.
- Given a position someone tries to edit in place, when the edit is made, then it is written as a new position that replaces the old one, and the old one stays as it was.
- Given a changed position, when an agent reads the positions, then it finds one position in force for that job, and the old one only as history.
- Given a change in progress, when a slice is designed and built, then the work goes on.

## Out of scope
- Setting a first position. Set the project's technology (fn-set-technology) and Set the project's architecture (fn-set-architecture) do it.
- Moving work already built onto the new position. The build owns it (Code → Validation), from work items that Turn intents into agent work makes.
- Raising a quality level in the product profile. Specify the product owns the profile, and a decision moves it.
- Writing and keeping the decision record behind a change. Manage ADRs owns decision records.
- Opening a locked design for a change. Lock the design owns the lock.

## Sources
- The one line the product owner agreed on 2026-11-03: "The technology and architecture for the whole project are set here and can evolve."
- .garura/product/product-os/intents/bi-2.md: "Each position is written down and can change later.", "Block on anything except the lock, which is the only gate."
- standards/schemas/product-os/decision.yaml, in Phoenix memory: "accepted decisions are not edited — supersede or amend with a new record", "id of the decision that replaced this one; else null"
- core/components/plays/record-decision/SKILL.md: "keeps every older ADR pointing forward", "Only a person accepts an ADR."
- core/components/plays/shape-architecture-lens/reference/ice.md: "accepted decisions are superseded, never edited in place", "reuse the product decision if one exists"
- core/components/skills/author-technical-approach/SKILL.md: "architecture.yaml is LOCKED -- drop to DRAFT first."
- knowledge/architecture/modular-monolith.md, in Phoenix memory: "Not a compromise on the way to microservices but an", "evolve_when:"
- knowledge/architecture/microservices.md, in Phoenix memory: "Microservices: independently deployable services — earned, not started with", "deploy-cadence: independent-per-team"
- .garura/product/product-os/software-delivery-planning/initialize/capability.md: "A project changes (it gains a database, a web surface or a new tracker)"
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "The box moves ONLY by an approved decision."
- The capability list the product owner locked on 2026-11-03: "Lock the design: A design is locked before agents take over. This is the only gate", "Its final place is settled when it is built."
