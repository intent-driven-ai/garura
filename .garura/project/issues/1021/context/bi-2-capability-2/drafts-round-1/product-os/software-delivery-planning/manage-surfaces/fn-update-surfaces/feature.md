# Feature: Update the surfaces as the project changes

## What it does
When the project gains or drops a surface, or a surface must change its kind, a person confirms an update, and what held before stays readable with why it changed.
- The project's surfaces are the places where people, or other systems, open the product to use it, each with its kind: a command line, a browser, a mobile app or another kind. Declare the project's surfaces (fn-declare-surfaces) declares them.
- A project changes as it grows. For example: a team tool built as a command line gains a browser page for team leads who are not technical, a shop adds a mobile app, a clinic opens an API to a partner's system, or a surface nobody uses is dropped.
- The update is proposed from the project's own memory and code first: what the code now shows, such as a new app or new pages; a slice designed on a surface that is not on the list; or a set-up answer that changed when the project set-up step (initialize) ran again. Then it is proposed from Garura memory, the memory Garura keeps for the project, and from Phoenix memory, the shared memory on the machine that every project draws from.
- Only when no memory has an answer does the agent research the update. It raises what it found as a memory update, a proposed addition to memory, for a person to approve, and the update waits for that approval. No update comes from what the AI agent knows by itself.
- A person confirms the update, with its reason.
- From its confirmation, the updated surfaces are the ones in force. What held before is kept as it was, marked replaced, and points to the update, with what changed in the project and why.
- How it meets the capability: the project's surfaces are declared once and change as the project changes. This feature is how they change, without losing what held before.

Status: not built. What exists covers only parts of it:
- The rough list of surfaces in the product profile is written once, and only when the project has no profile yet. Firming the profile later keeps the list as it was. So nothing changes the list today but an edit by hand.
- The project set-up step, initialize, will run again when the project changes, such as when it gains a web surface, and propose the earlier answers again. It is not built.
- Planned and tracked, not built: a change to a surface's kind is recorded as a decision, not made as a silent edit.
- A decision record about the product can be replaced through the decision play: an accepted record is never edited, a new record replaces it, and the old one points forward to it. Nothing ties this to the project's surfaces.

## Inputs / Outputs
- In: the surfaces in force, and what changed in the project that calls for an update.
- In: the project's code and its settings as they are now, the slices with the surface each is on, and the set-up answers once initialize is built.
- In: a memory update a person approved, when no memory had an answer and the agent researched the update.
- In: the person's confirmation of the update, with its reason.
- Out: a memory update for each part of the update the agent researched, waiting for a person's approval.
- Out: the updated surfaces, in force from the confirmation, with the reason, the source and the person who confirmed it.
- Out: what held before, kept as it was and marked replaced, pointing to the update, with what changed and why.

## Rules & behavior
- The project's memory first. An update is proposed from the project's own memory and code first, then from Garura memory, then from Phoenix memory. The reason: a change in the project's code or in a slice is the evidence for the update, and anyone can read it to judge the update.
- Research only when no memory has an answer, and only through a memory update. The agent uses what it found only after a person approves it. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- Never from the AI agent's own knowledge. An update with no source behind it is not proposed. The reason: the agent's own knowledge can be neither checked nor read back.
- An update replaces what held before and never edits it. The reason: slices already designed on the old surfaces must still be explainable, and a reader must be able to see which surfaces held when.
- An update says why: what changed in the project, with its source. The reason: the next person can then tell a step of growth from a mistake that was put right.
- A person confirms each update. The reason: the kind of a surface decides how every slice on it is designed and tested, so changing it is a person's decision, never an agent's.
- An update follows the rules of a first declaration too: the project's code describes what is, each proposal names its source, each surface names who opens it and why it is that kind, and only surfaces go on the list. The reason: an updated surface must be as well founded as the first one.
- One kind in force for each surface. The reason: an agent that finds two would pick one, and the next agent might pick the other.
- Nothing waits for an update. An update in progress, or one waiting for a memory update, does not stop design or build. The reason: the Spec → Design business intent must not block on anything except the lock.
- Not decided: how an update reaches the slices already designed or built on a surface it changes. A changed kind can mean a slice's design is written again.
- Not decided: how the surfaces are updated once the design is locked. Lock the design owns the lock, the only gate, and it is not built.

## Acceptance criteria
- Given declared surfaces with one command line, and a project whose code now serves pages in a browser, when an update is proposed, then it proposes a browser surface and names the files that show it.
- Given a slice designed on a surface that is not on the list, when an update is proposed, then it proposes that surface and names the slice.
- Given an update that no memory has an answer for, when it is proposed, then the agent researches it, raises a memory update with what it found, and the update waits until a person approves the memory update.
- Given an update with no source behind it, when it is checked, then it is not proposed.
- Given an update the person confirmed, when it lands, then the updated surfaces are in force, and what held before is readable as it was, marked replaced, with what replaced it and why.
- Given an update that no person confirmed, when it is asked for, then the surfaces do not change.
- Given someone edits the surfaces in place, when the edit is made, then it is written as an update that replaces what held before, and the old text stays as it was.
- Given a surface whose kind was updated, when an agent reads the surfaces, then it finds one kind in force for that surface, and the old one only as history.
- Given an update in progress, when a slice is designed and built, then the work goes on.

## Out of scope
- Declaring the first surfaces. Declare the project's surfaces (fn-declare-surfaces) does it.
- Moving slices already designed or built onto an updated surface. The design of each slice and the build own it (Design → Code and Code → Validation), from work items that Turn intents into agent work makes.
- The technology of a new surface. Design the technology and architecture owns it, and a new surface can call for an update of the architecture.
- Writing and keeping the decision record behind an update. Manage ADRs owns decision records.
- Opening a locked design for an update. Lock the design owns the lock.
- Moving an approved memory update into Phoenix memory. A person does it on purpose, as a promotion, outside this work.

## Sources
- The one line the product owner agreed on 2026-11-03: "The project's surfaces are declared: CLI, browser, mobile or other."
- .garura/product/product-os/intents/bi-2.md: "Each position is written down and can change later.", "Block on anything except the lock, which is the only gate."
- GitHub #559 (open): "Changing a medium later is recorded as a decision, not a silent edit.", "Every surface record carries a medium and a reason for it."
- GitHub #553 (open, under the Spec → Design business intent in the tracker): "all of them cost a rewrite after the design was already written"
- core/components/plays/discover-domains/scripts/persist_seed.py: "the profile block: added ONLY if the live spine has none."
- core/components/plays/discover-capabilities/scripts/rollup_box.py: "proposed = dict(profile)"
- .garura/product/product-os/software-delivery-planning/initialize/fn-rerun-initialize/feature.md: "when the project changes: it gains a database, a web surface, personal data or a new tracker, or it drops one."
- .garura/product/product-os/software-delivery-planning/initialize/capability.md: "A project changes (it gains a database, a web surface or a new tracker)"
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/fn-update-architecture/feature.md: "it gains a database or a new surface"
- standards/schemas/product-os/decision.yaml, in Phoenix memory: "accepted decisions are not edited — supersede or amend with a new record"
- core/components/plays/record-decision/SKILL.md: "keeps every older ADR pointing forward", "Only a person accepts an ADR."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- core/tools/memory/GUIDE.md: "Your work goes on while the update waits, unless you cannot go on without it.", "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
- The capability list the product owner locked on 2026-11-03: "Lock the design: A design is locked before agents take over. This is the only gate", "Its final place is settled when it is built."
