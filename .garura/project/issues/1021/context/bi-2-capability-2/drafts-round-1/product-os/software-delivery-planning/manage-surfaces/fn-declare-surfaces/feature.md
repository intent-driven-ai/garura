# Feature: Declare the project's surfaces

## What it does
It sets the list of places where people or other systems use the product, each with its kind, who opens it, what they do there and why, so every slice is designed and tested on a declared surface.
- A surface is a place where a person, or another system, opens the product to use it. Each declared surface holds:
  - Its name, such as a clinic's booking page, a shop's mobile app or a build tool's release command.
  - Its kind: a command line, a browser, a mobile app, or another kind, such as an API that another system calls, a desktop app or a device.
  - Who opens it, named as a persona, a role and never a person's name, and what they do there.
  - Why it is that kind. For example, a tool that must read files on a person's laptop at night stays a command line, and a page where a person who is not technical grants access is not a command line.
  - Its source, and the person who confirmed it.
- It runs before the slices are designed, and again when the project needs a surface it does not have yet. A slice is an ordered group of features that one person can test end to end on one surface.
- For each surface, an agent proposes an answer:
  - A project that already has code shows its surfaces in that code and its settings: a command it installs, pages it serves, an app it ships, or an endpoint other systems call. The proposal describes them as they are, with the files that show them.
  - Where the code does not settle it, the proposal comes from what the project's memory holds: the Sources a person gave when the product was specified, such as a prototype that runs in a browser; the business intents, the needs the product meets, each with who asks for it; the rough list of surfaces in the product profile; and the project's set-up answers, once the set-up step (initialize) is built. A Source is a saved copy of what a person gave. The product profile is the record of the product's shape and the quality levels it commits to.
  - Then the proposal comes from Garura memory, the memory Garura keeps for the project, and then from Phoenix memory, the shared memory on the machine that every project draws from.
  - Only when no memory has an answer does the agent research it. It raises what it found as a memory update, a proposed addition to memory, for a person to approve. Until the person approves it, the surface or its kind stays open.
  - No surface and no kind comes from what the AI agent knows by itself. A kind that nothing backs stays open, with no default, and the person decides it.
- Only surfaces go on the list. A file the product hands out, such as an export, is not a surface, even when a person downloads it.
- The person confirms or corrects each surface and its kind, and gives the reason when the proposal has none. Only a confirmed surface is declared.
- How it meets the capability: this is how the project's surfaces are declared once for the whole project. Each slice then picks its one surface from this list, and the slice's design and its eval start from that surface's kind. The eval is the test that checks a slice from the outside, on its surface.

Status: not built. What exists covers only parts of it:
- When a product is first specified, a rough list of surface kinds is written into the product profile, and only when the project has no profile yet. The list holds one word for each kind, such as web or cli, with no person, no reason and no confirmation of its own.
- Each slice names its one surface when it is shaped, from the business intent, the people in the model and where the slice's parts sit, and shows it to the person for a yes. It does not read the profile's list.
- The project set-up step, initialize, will ask about the surfaces (web, mobile, command line, API), with a proposed answer that names its source, and keep the answer in the product profile. It is not built.
- The design play for a slice's screens is stale and waits for a rebuild. For its own slice, it records the kind each surface runs on and why. Nothing records this for the whole project.
- Planned and tracked, not built: every surface carries its kind, decided by a person with the reason written down; a written definition tells a surface from an integration point, a place where the product hands something to another system; and the profile's list holds only surfaces, and every surface the product needs.

## Inputs / Outputs
- In: the project's code and its settings, when it has any.
- In: the Sources a person gave when the product was specified, such as a prototype, a document or their own words.
- In: the business intents, each with who asks for it.
- In: the rough list of surfaces in the product profile, and the project's set-up answers once initialize is built.
- In: a memory update a person approved, when no memory had an answer and the agent researched it.
- In: the person's confirmation or correction of each proposal.
- Out: the proposals, each with the surface's name, its kind, who opens it, what they do there, its reasons and its source. The source is a file of the project, a Source, a memory file or an approved memory update.
- Out: a memory update for each surface or kind the agent researched, waiting for a person's approval.
- Out: the declared surfaces of the whole project, each with its name, its kind, who opens it, what they do there, the reason for its kind, its source and the person who confirmed it.
- Out: each surface or kind left open, named as a gap.

## Rules & behavior
- The project's memory first. Each surface and its kind are proposed from the project's own memory and code first, then from Garura memory, then from Phoenix memory. The reason: a source in the project or in memory can be checked and read back, so the person can judge the proposal from it.
- Research only when no memory has an answer, and only through a memory update. The agent uses what it found only after a person approves the update. Until then the surface or its kind stays open, and the work goes on. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- Never from the AI agent's own knowledge. A surface or a kind with no source behind it is not proposed. The reason: a kind an agent assumed is found wrong only after the design is written, and then the design is written again.
- What the project's code already shows is described as it is. The reason: a list that contradicts what runs sends the design after a surface that nobody uses. Moving away from it is an update (fn-update-surfaces).
- Each proposal names its source. The reason: a person can then check each surface without a search.
- A person confirms each surface's kind, and the reason is written beside it. The reason: a kind has reasons, and without them the next person cannot tell a choice from an accident.
- Each surface names who opens it and what they do there. The reason: a kind fits a person and a job, so a reader can check the one against the other.
- Only surfaces are declared. The reason: a list that holds something that is not a surface, or misses one that is, sends design and tests after the wrong thing. Not decided: the written definition that tells a surface from an integration point; until it is written, a person decides each doubtful case.
- Nothing waits for the surfaces. A slice can be designed on a surface not yet declared: the work goes on, and the surface is named so a person can declare it. The reason: the Spec → Design business intent must not block on anything except the lock.
- Not decided: where the declared surfaces are kept, and which list of kinds they use. The model has no kind for a surface, and today four lists of kinds disagree.

## Acceptance criteria
- Given a project whose code installs a command and serves no pages, when its surfaces are proposed, then the proposal is a command line and names the files that show it.
- Given a product specified from a prototype that runs in a browser, when its surfaces are proposed, then a browser surface is proposed and names that Source.
- Given a surface whose kind nothing in the project or in memory backs, when the proposals are made, then the agent researches it, raises a memory update with what it found, and the kind stays open until a person approves the update.
- Given a proposal with no source behind it, when the proposals are checked, then it is taken out and the surface is named as open.
- Given the person corrects a proposed kind, when the surfaces are written, then the surface holds the person's kind with the reason and names the person.
- Given a product that exports a file of the day's bookings, when its surfaces are declared, then the export is not on the list.
- Given the declared surfaces, when an agent that did not declare them reads them, then it can name each surface, its kind, who opens it, what they do there and why, without asking a person.
- Given no surface is declared yet, when a slice is designed, then the work goes on and the missing surface is named.

## Out of scope
- Updating the declared surfaces as the project changes. Update the surfaces as the project changes (fn-update-surfaces) does it.
- Choosing the one surface of a slice and the person who tests it there. Design slices owns it.
- Designing what a person sees and does on a surface for one slice. Use the lenses on each slice owns it.
- The step library of each kind of surface and the eval of each slice. Design for evaluation and testing owns them.
- The technology a surface is built with. Design the technology and architecture owns it.
- The first rough profile and the rest of the product profile. Specify the product owns them.
- Moving an approved memory update into Phoenix memory. A person does it on purpose, as a promotion, outside this work.

## Sources
- The one line the product owner agreed on 2026-11-03: "The project's surfaces are declared: CLI, browser, mobile or other."
- .garura/product/product-os/intents/bi-2.md: "Without shared positions, each builder invents its own answer.", "Block on anything except the lock, which is the only gate."
- .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-domains/feature.md: "Out: one rough product profile, only when none exists: the product's stage, users, way of earning and surfaces (where people use it, such as the web), with coarse quality levels."
- core/components/skills/author-domains/SKILL.md: "the `shape` at a rough cut", "(stage / users / monetization / surfaces)"
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "# web | mobile | cli | api | desktop | embedded"
- core/components/skills/author-slice/SKILL.md: "the thing the outcome names: a screen, a command line command or an endpoint.", "intent page (asked by, outcome), the personas and journeys in the model, and the placement.", "Never ask the person for them: they see the surface and the tester in the brief and say yes"
- .garura/product/product-os/software-delivery-planning/initialize/fn-setup-questions/feature.md: "the surfaces (web, mobile, command line, API)", "Where nothing backs a proposal, the question carries no proposed answer and the person answers it; there is never a default in place of a source"
- .garura/product/product-os/software-delivery-planning/initialize/fn-project-memory/feature.md: "Out: the answers recorded in the product profile, each with the question it answers."
- core/components/skills/author-ux-lens/SKILL.md: "`personas` and `surfaces` (medium each surface runs on,"
- core/components/plays/shape-ux-lens/SKILL.md: "waits for the rebuild of the design plays after the shaping loop (#855, ADR 053)"
- GitHub #553 (open, under the Spec → Design business intent in the tracker): "an API can be a surface", "Nobody ever asked what kind of screen this is."
- GitHub #559 (open): "Every surface record carries a medium and a reason for it.", "It had reasons that belong on the record", "it has to read tool logs on that laptop, which a browser cannot, and has to run nightly when no browser is open", "granting access should not require a technical person"
- GitHub #560 (open): "CVS downloads are integration points. we will never expose that as a surface.", "A person downloading a file does not make the file a surface."
- GitHub #562 (open): "The profile's surface list contains only surfaces, and contains every surface the capability needs."
- core/tools/memory/GUIDE.md: "Never answer from what you already know, and never from the web, without a", "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- core/tools/memory/GUIDE.md: "Your work goes on while the update waits, unless you cannot go on without it.", "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
- standards/schemas/eval/_index.md, in Phoenix memory: "One step library for each surface kind of a slice's eval (ADR 057)"
