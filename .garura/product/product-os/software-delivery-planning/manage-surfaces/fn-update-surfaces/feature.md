# Feature: Update the surfaces as the project changes

## What it does
When the project gains or drops a surface, or a surface's kind, properties or guidelines must change, a person confirms an update, and what held before stays readable with why it changed.
- The project's surfaces are the places where people, or other systems, open the product to use it. Each has its kind, its properties, what it offers and how it behaves, and its guidelines, what every design on it must handle. Declare a surface, its properties and its guidelines (fn-declare-surfaces) declares them.
- A project changes as it grows. For example: a team tool built as a command line gains a browser page for team leads who are not technical; a browser page built for desktop screens must now serve phones; a shop adds a mobile app; the design system that screens are built from is replaced; the accessibility level the product commits to goes up; or a surface nobody uses is dropped.
- The update is proposed from the project's own memory and code first: what the code now shows, such as a new app, new screen sizes or a new component library; a slice designed on a surface, a property or a guideline that is not declared; a set-up answer that changed when the project set-up step (initialize) ran again; or a quality level that rose in the product profile. Then it is proposed from Garura memory, the memory Garura keeps for the project, and from Phoenix memory, the shared memory on the machine that every project draws from, including a learning that changed and that a guideline names as its source.
- Only when no memory has an answer does the agent research the update. It raises what it found as a memory update, a proposed addition to memory, for a person to approve, and the update waits for that approval. No update comes from what the AI agent knows by itself.
- A person confirms the update, with its reason.
- From its confirmation, the updated surface is the one in force. What held before is kept as it was, marked replaced, and points to the update, with what changed in the project and why.
- How it meets the capability: each surface is declared once, with its properties and guidelines, and they change as the project changes. This feature is how they change, without losing what held before.

Status: not built. What exists covers only parts of it:
- The rough list of surfaces in the product profile is written once, and only when the project has no profile yet. Firming the profile later keeps the list as it was. So nothing changes the list today but an edit by hand, and it holds no properties or guidelines to change.
- The project set-up step, initialize, will run again when the project changes, such as when it gains a web surface, and propose the earlier answers again. It is not built.
- The design play for a slice's screens is stale. When it finds the product's visual core already recorded as a decision, it reuses it, and a new decision replaces an old one without editing it. Nothing ties this to a declared surface.
- Planned and tracked, not built: a change to a surface's kind is recorded as a decision, not made as a silent edit.
- A decision record about the product can be replaced through the decision play: an accepted record is never edited, a new record replaces it, and the old one points forward to it. Nothing ties this to the project's surfaces.

## Inputs / Outputs
- In: the surfaces in force, with their properties and guidelines, and what changed in the project that calls for an update.
- In: the project's code and its settings as they are now, the slices with the surface each is on, the product profile as it is now, and the set-up answers once initialize is built.
- In: the Phoenix memory learnings that a property or a guideline names as its source, as they are now.
- In: a memory update a person approved, when no memory had an answer and the agent researched the update.
- In: the person's confirmation of the update, with its reason.
- Out: a memory update for each part of the update the agent researched, waiting for a person's approval.
- Out: the updated surface, in force from the confirmation, with the reason, the source and the person who confirmed it.
- Out: what held before, kept as it was and marked replaced, pointing to the update, with what changed and why.

## Rules & behavior
- The project's memory first. An update is proposed from the project's own memory and code first, then from Garura memory, then from Phoenix memory. The reason: a change in the project's code, in a slice or in the profile is the evidence for the update, and anyone can read it to judge the update.
- Research only when no memory has an answer, and only through a memory update. The agent uses what it found only after a person approves it. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- Never from the AI agent's own knowledge. An update with no source behind it is not proposed. The reason: the agent's own knowledge can be neither checked nor read back.
- An update replaces what held before and never edits it. The reason: slices already designed on the old surface must still be explainable, and a reader must be able to see which properties and guidelines held when.
- An update says why: what changed in the project, with its source. The reason: the next person can then tell a step of growth from a mistake that was put right.
- A person confirms each update. The reason: a surface's kind, properties and guidelines decide how every slice on it is designed, so changing them is a person's decision, never an agent's.
- An update follows the rules of a first declaration too: the project's code describes what is, each part names its source, each guideline serves a property or a quality level of the profile, and only surfaces go on the list. The reason: an updated surface must be as well founded as the first one.
- One answer in force for each property and each guideline of a surface. The reason: an agent that finds two would pick one, and the next agent might pick the other.
- Nothing waits for an update. An update in progress, or one waiting for a memory update, does not stop design or build. The reason: the Spec → Design business intent blocks no work, and each design can run at any time.
- Not decided: how an update reaches the slices already designed or built on the surface it changes. A changed property or guideline can mean a slice's design is written again.

## Acceptance criteria
- Given a declared browser page that serves desktop screens, and a project whose code now lays its pages out for phones too, when an update is proposed, then it proposes the new screen sizes and names the files that show them.
- Given declared surfaces with one command line, and a project whose code now serves pages in a browser, when an update is proposed, then it proposes a browser surface, its properties and its guidelines, and names their sources.
- Given a slice designed on a surface that is not on the list, when an update is proposed, then it proposes that surface and names the slice.
- Given an accessibility level that rose in the product profile, when an update is proposed, then the accessibility guideline of each surface it touches is proposed at the new level.
- Given an update that no memory has an answer for, when it is proposed, then the agent researches it, raises a memory update with what it found, and the update waits until a person approves the memory update.
- Given an update with no source behind it, when it is checked, then it is not proposed.
- Given an update the person confirmed, when it lands, then the updated surface is in force, and what held before is readable as it was, marked replaced, with what replaced it and why.
- Given an update that no person confirmed, when it is asked for, then the surfaces do not change.
- Given someone edits a declared surface in place, when the edit is made, then it is written as an update that replaces what held before, and the old text stays as it was.
- Given an updated guideline, when an agent reads the surface, then it finds one guideline in force, and the old one only as history.
- Given an update in progress, when a slice is designed and built, then the work goes on.

## Out of scope
- Declaring the first surfaces, properties and guidelines. Declare a surface, its properties and its guidelines (fn-declare-surfaces) does it.
- Moving slices already designed or built onto an updated surface. The design of each slice and the build own it (Design → Code and Code → Validation), from work items that Turn intents into agent work makes.
- The technology of a new surface or of a new design system. Design the technology and architecture owns it, and a new surface can call for an update of the architecture.
- Raising a quality level in the product profile. Specify the product owns the profile, and a decision moves it.
- Writing and keeping the decision record behind an update. Manage ADRs owns decision records.
- Moving an approved memory update into Phoenix memory. A person does it on purpose, as a promotion, outside this work.

## Sources
- The one line the product owner agreed on 2026-11-03: "The project's surfaces are declared: CLI, browser, mobile or other."
- The product owner on 2026-11-07, on the first drafts: "declare the surface, and its properties is what this is about for each surface we need to define guidelines example for web - we need to handle for design system etc.", "the design would be for that surface"
- .garura/product/product-os/intents/bi-2.md: "Each position is written down and can change later.", "Block other work. Each design can be run at any time."
- GitHub #559 (open): "Changing a medium later is recorded as a decision, not a silent edit.", "Every surface record carries a medium and a reason for it."
- GitHub #553 (open, under the Spec → Design business intent in the tracker): "all of them cost a rewrite after the design was already written"
- core/components/plays/discover-domains/scripts/persist_seed.py: "the profile block: added ONLY if the live spine has none."
- core/components/plays/discover-capabilities/scripts/rollup_box.py: "proposed = dict(profile)"
- .garura/product/product-os/software-delivery-planning/initialize/fn-rerun-initialize/feature.md: "when the project changes: it gains a database, a web surface, personal data or a new tracker, or it drops one."
- .garura/product/product-os/software-delivery-planning/initialize/capability.md: "A project changes (it gains a database, a web surface or a new tracker)"
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/fn-update-architecture/feature.md: "it gains a database or a new surface"
- core/components/skills/author-ux-lens/SKILL.md: "If the product already carries a visual-core decision (check under `product_base`), REUSE it"
- core/components/plays/shape-ux-lens/reference/ice.md: "the visual-core decision is reused, any new decision supersedes."
- knowledge/technology/ux-design-system-tokens.md, in Phoenix memory: "The product needs multiple brands/themes, or the token set has grown unwieldy and"
- knowledge/technology/ux-responsive-default-adaptive-on-evidence.md, in Phoenix memory: "Analytics or usability testing shows a specific device failing a specific key task on the"
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "The box moves ONLY by an approved decision."
- standards/schemas/product-os/decision.yaml, in Phoenix memory: "accepted decisions are not edited — supersede or amend with a new record"
- core/components/plays/record-decision/SKILL.md: "keeps every older ADR pointing forward", "Only a person accepts an ADR."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- core/tools/memory/GUIDE.md: "Your work goes on while the update waits, unless you cannot go on without it.", "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
- The capability list the product owner locked on 2026-11-03: "Lock the design: A design is locked before agents take over. This is the only gate", "Its final place is settled when it is built."
