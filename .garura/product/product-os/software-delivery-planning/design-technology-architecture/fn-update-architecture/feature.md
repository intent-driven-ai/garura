# Feature: Update the architecture as the project changes

## What it does
When the project outgrows its architecture, a person confirms an update, and what held before stays readable with why it changed.
- The project's architecture is the shape of the whole system and what it is built with: its style, its main parts and how they connect, and the technology of each part with its version. Set the project's architecture (fn-set-architecture) sets it.
- A project changes as it grows. For example: it gains a database or a new surface, many more people use it, several teams start to deploy on their own schedules, or a quality level in the product profile goes up. The product profile holds the quality levels the product commits to, such as how fast or how secure it must be.
- The update is proposed from Phoenix memory first. Phoenix memory is the shared memory on the machine that every project draws from. Its architecture and technology learnings say when a choice is outgrown and what comes after it, such as one deployable unit giving way to separate services once the product and its teams grow past the unit.
- Only when Phoenix memory has no answer does the agent research the update. It raises what it found as a memory update, a proposed addition to memory, for a person to approve, and the update waits for that approval. No update comes from what the AI agent knows by itself.
- A person confirms the update.
- From its confirmation, the updated architecture is the one in force. What held before is kept as it was, marked replaced, and points to the update, with what changed in the project and why.
- How it meets the capability: the project's architecture is set once and can evolve. This feature is how it evolves as the project changes, without losing what held before.

Status: not built. What exists covers only parts of it:
- A decision record about the product can be replaced through the decision play. An accepted record is never edited: a new record replaces it, and the old one points forward to it. Nothing ties this to the architecture of the whole project.
- The play that designs architecture is stale and waits for a rebuild. When it runs again, it reuses its technology decision, and a new decision replaces the old one, never editing it.
- Phoenix memory's learnings each say which choice comes after them.
- Reading memory first and then researching exists in parts: a skill researches on the web when memory has too little, and the memory tool raises a memory update for a person. Nothing joins them for an update of the architecture.
- An older skill refused to change a locked architecture until it was moved back to draft. No play calls it.

## Inputs / Outputs
- In: the architecture in force, and what changed in the project that calls for an update.
- In: Phoenix memory's architecture and technology learnings that say when a choice is outgrown and what comes next.
- In: a memory update a person approved, when Phoenix memory had no answer and the agent researched the update.
- In: the project's code and its settings, and the product profile as it is now.
- In: the person's confirmation of the update.
- Out: a memory update for each part of the update the agent researched, waiting for a person's approval.
- Out: the updated architecture, in force from its confirmation, with its reasons, its source and the person who confirmed it.
- Out: what held before, kept as it was and marked replaced, pointing to the update, with what changed and why.

## Rules & behavior
- Phoenix memory first. An update is proposed from Phoenix memory's architecture and technology learnings, matched to the project's conditions as they are now. The reason: memory's learnings say when a choice is outgrown and what comes after it, and anyone can read them to judge the update.
- Research only when Phoenix memory has no answer, and only through a memory update. The agent researches the update, raises what it found as a memory update, and uses it only after a person approves it. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- Never from the AI agent's own knowledge. An update with no Phoenix memory learning and no approved memory update behind it is not proposed. The reason: the agent's own knowledge can be neither checked nor read back.
- An update replaces what held before and never edits it. The reason: work already built on the old architecture must still be explainable, and a reader must be able to see which architecture held when.
- An update says why: what changed in the project, with its source. The reason: the next person can then tell a step of growth from a mistake that was put right.
- A person confirms each update. The reason: the architecture binds every builder in the project, so changing it is the person's decision, never an agent's.
- An update follows the other rules of a first choice too: the project's code describes what is, each proposal names its source, and the product profile sizes it. The reason: an updated choice must be as well founded as the first one.
- One answer in force for each job. The reason: an agent that finds two would pick one, and the next agent might pick the other.
- Nothing waits for an update. An update in progress, or one waiting for a memory update, does not stop design or build. The reason: the Spec → Design business intent blocks no work, and each design can run at any time.
- Not decided: how an update reaches the work already built or planned on what held before. Nothing names that work today.

## Acceptance criteria
- Given an architecture of one deployable unit and a project whose teams now deploy on their own schedules, when an update is proposed, then it names the Phoenix memory learning that says the unit is outgrown and what comes next.
- Given an update that Phoenix memory has no learning for, when it is proposed, then the agent researches it, raises a memory update with what it found, and the update waits until a person approves the memory update.
- Given an update with no Phoenix memory learning and no approved memory update behind it, when it is checked, then it is not proposed.
- Given an update the person confirmed, when it lands, then the updated architecture is in force, and what held before is readable as it was, marked replaced, with what replaced it and why.
- Given an update that no person confirmed, when it is asked for, then the architecture does not change.
- Given someone edits the architecture in place, when the edit is made, then it is written as an update that replaces what held before, and the old text stays as it was.
- Given an updated choice, when an agent reads the architecture, then it finds one answer in force for that job, and the old one only as history.
- Given an update in progress, when a slice is designed and built, then the work goes on.

## Out of scope
- Setting the first architecture. Set the project's architecture (fn-set-architecture) does it.
- Moving work already built onto the updated architecture. The build owns it (Code → Validation), from work items that Turn intents into agent work makes.
- Raising a quality level in the product profile. Specify the product owns the profile, and a decision moves it.
- Writing and keeping the decision record behind an update. Manage ADRs owns decision records.
- Moving an approved memory update into Phoenix memory. A person does it on purpose, as a promotion, outside this work.

## Sources
- The one line the product owner agreed on 2026-11-03: "The technology and architecture for the whole project are set here and can evolve."
- The product owner on 2026-11-07, on the first drafts: "this should be reflected as updating arch. as the project changes.", "we need to read the phoenix memory and if not found then go about research."
- .garura/product/product-os/intents/bi-2.md: "Each position is written down and can change later.", "Block other work. Each design can be run at any time."
- standards/schemas/product-os/decision.yaml, in Phoenix memory: "accepted decisions are not edited — supersede or amend with a new record", "id of the decision that replaced this one; else null"
- core/components/plays/record-decision/SKILL.md: "keeps every older ADR pointing forward", "Only a person accepts an ADR."
- core/components/plays/shape-architecture-lens/reference/ice.md: "accepted decisions are superseded, never edited in place", "reuse the product decision if one exists"
- core/components/plays/shape-architecture-lens/reference/ice.md: "recorded KB-learning-gap proposal — never the model's taste.", "F8 — An architecture choice rests on neither a matched KB learning nor a recorded proposal."
- core/components/skills/research-domain-context/SKILL.md: "Research vertical domain knowledge via web when LTM is insufficient"
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- core/tools/memory/GUIDE.md: "Your work goes on while the update waits, unless you cannot go on without it.", "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
- core/components/skills/author-technical-approach/SKILL.md: "architecture.yaml is LOCKED -- drop to DRAFT first."
- knowledge/_index.md, in Phoenix memory: "`architecture/` — product-condition → best-fit architecture ladders", "`technology/` — specific technology/stack choices and the conditions they fit."
- knowledge/architecture/modular-monolith.md, in Phoenix memory: "Not a compromise on the way to microservices but an", "evolve_when:"
- knowledge/architecture/microservices.md, in Phoenix memory: "Microservices: independently deployable services — earned, not started with", "deploy-cadence: independent-per-team"
- .garura/product/product-os/software-delivery-planning/initialize/capability.md: "A project changes (it gains a database, a web surface or a new tracker)"
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "The box moves ONLY by an approved decision."
- The capability list the product owner locked on 2026-11-03: "Lock the design: A design is locked before agents take over. This is the only gate", "Its final place is settled when it is built."
