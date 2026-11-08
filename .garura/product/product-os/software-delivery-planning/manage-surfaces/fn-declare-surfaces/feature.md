# Feature: Declare a surface, its properties and its guidelines

## What it does
It declares each surface the project has, with its kind, who opens it and why, what it offers and how it behaves, and the guidelines every design on it must handle, so each design on that surface is made for it.
- A surface is a place where a person, or another system, opens the product to use it. Each declared surface holds:
  - Its name and its kind: a command line, a browser, a mobile app, or another kind, such as an API that another system calls. For example: a clinic's booking page, a shop's mobile app or a build tool's release command.
  - Who opens it, named as a persona, a role and never a person's name, and what they do there.
  - Why it is that kind. For example, a tool that must read files on a person's laptop at night stays a command line, and a page where a person who is not technical grants access is not a command line.
  - Its properties: what the surface offers and how it behaves. For example: for a browser surface, whether one layout reflows across screen sizes or each device gets a layout of its own, and which screen sizes it serves; for a mobile app, the alerts it can push to a person's phone; for a coding agent that a person runs in a terminal, such as Claude Code, that each piece of work runs as a command and the person answers by typing.
  - Its guidelines: what every design on the surface must handle. For example: for a browser surface, working within the project's design system, the shared colours, type and components that every screen is built from, and meeting the accessibility level the product commits to; for a coding agent, how it asks a person a question and how it reports back in plain words.
  - For each part, its source and the person who confirmed it.
- The guidelines follow from what the surface offers. A surface that serves many screen sizes needs a guideline for how a design fits each one, and a surface where a person answers by typing needs a guideline for how a question is asked. So a surface, its properties and its guidelines are declared together, in one step.
- It runs before the slices are designed, and again when the project needs a surface it does not have yet. A slice is an ordered group of features that one person can test end to end on one surface.
- For each surface, property and guideline, an agent proposes an answer:
  - A project that already has code shows much of it in that code and its settings: a command it installs, pages it serves and how they lay out, the components and the style guide those pages use, an app it ships, or an endpoint other systems call. The proposal describes them as they are, with the files that show them.
  - Where the code does not settle it, the proposal comes from what the project's memory holds: the Sources a person gave when the product was specified, such as a prototype that runs in a browser; the business intents, the needs the product meets, each with who asks for it; the rough list of surfaces and the quality levels in the product profile; and the project's set-up answers, once the set-up step (initialize) is built. A Source is a saved copy of what a person gave. The product profile is the record of the product's shape and the quality levels it commits to.
  - Then the proposal comes from Garura memory, the memory Garura keeps for the project, and then from Phoenix memory, the shared memory on the machine that every project draws from. Phoenix memory's learnings are matched to the kind of surface, such as a web app or site.
  - Only when no memory has an answer does the agent research it. It raises what it found as a memory update, a proposed addition to memory, for a person to approve. Until the person approves it, that part stays open.
  - Nothing comes from what the AI agent knows by itself. A part that nothing backs stays open, with no default, and the person decides it.
- Only surfaces go on the list. A file the product hands out, such as an export, is not a surface, even when a person downloads it.
- The person confirms or corrects each surface, property and guideline, and gives the reason when the proposal has none. Only a confirmed part is declared.
- How it meets the capability: this is how each surface is declared once for the whole project, with what it offers and the rules for designing on it. Each slice then picks its one surface from this list, and its design follows that surface's properties and guidelines.

Status: not built. What exists covers only parts of it:
- When a product is first specified, a rough list of surface kinds is written into the product profile, and only when the project has no profile yet. The list holds one word for each kind, such as web or cli, with no properties, no guidelines and no confirmation of its own.
- Each slice names its one surface when it is shaped, from the business intent, the people in the model and where the slice's parts sit, and shows it to the person for a yes. It does not read the profile's list.
- The project set-up step, initialize, will ask about the surfaces (web, mobile, command line, API), with a proposed answer that names its source, and keep the answer in the product profile. It is not built.
- The design play for a slice's screens is stale and waits for a rebuild. For its own slice, it records the kind each surface runs on and why. It reads the name of the design system from the product profile or an earlier decision, says plainly when none exists, and records the product's visual core as a decision that later slices reuse. Nothing declares these for the whole project first.
- Phoenix memory holds learnings for a browser surface: one layout that reflows or a layout for each device, navigation, design tokens and shared components, states and feedback, and forms. One learning covers accessibility for any public screen. Domain shelves say what a mobile surface brings, such as alerts pushed to a phone or one-tap phone wallets. For a coding agent, Garura's own rules say how its plays ask a person and report back, and that no command name is a coding tool's own command. Nothing joins them into a surface's properties and guidelines.
- An older rule held, for each type of surface, whether a person uses it, the check that proves it runs and where it can be reached. It was written for a work record that no longer exists, and nothing uses it now.
- Planned and tracked, not built: every surface carries its kind, decided by a person with the reason written down; a written definition tells a surface from an integration point, a place where the product hands something to another system; and the profile's list holds only surfaces, and every surface the product needs.

## Inputs / Outputs
- In: the project's code and its settings, when it has any: its commands, its pages and their layouts, its components and its style guide, its apps and its endpoints.
- In: the Sources a person gave when the product was specified, such as a prototype, a document or their own words.
- In: the business intents, each with who asks for it.
- In: the rough list of surfaces and the quality levels in the product profile, and the project's set-up answers once initialize is built.
- In: Phoenix memory's learnings for each kind of surface, and its domain shelves.
- In: a memory update a person approved, when no memory had an answer and the agent researched it.
- In: the person's confirmation or correction of each proposal.
- Out: the proposals: each surface with its name, its kind, who opens it, what they do there and why, its properties and its guidelines, each part with its reasons and its source. The source is a file of the project, a Source, a memory file or an approved memory update.
- Out: a memory update for each part the agent researched, waiting for a person's approval.
- Out: the declared surfaces of the whole project, each with all of these parts, each part with its source and the person who confirmed it.
- Out: each part left open, named as a gap.

## Rules & behavior
- The project's memory first. Each surface, property and guideline is proposed from the project's own memory and code first, then from Garura memory, then from Phoenix memory. The reason: a source in the project or in memory can be checked and read back, so the person can judge the proposal from it.
- Research only when no memory has an answer, and only through a memory update. The agent uses what it found only after a person approves the update. Until then that part stays open, and the work goes on. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- Never from the AI agent's own knowledge. A part with no source behind it is not proposed. The reason: a property or guideline an agent assumed is found wrong only after the design is written, and then the design is written again.
- What the project's code already shows is described as it is. When its pages already use a component library and a style guide, the proposed design system is that one. The reason: a declaration that contradicts what runs sends every design after a surface that nobody builds. Moving away from it is an update (fn-update-surfaces).
- Each part names its source. The reason: a person can check it without a search, and when a learning in memory changes, the declarations built on it can be found.
- Each guideline says which property of its surface, or which quality level of the product profile, it serves. The reason: a guideline with no reason in its surface is a rule nobody can judge, and a property with no guideline leaves each slice to handle it alone.
- The product profile's quality levels bound the guidelines. A guideline meets the levels the profile commits to, such as an accessibility level, and never changes them. The reason: the profile is the box the product commits to, and only an approved decision moves it.
- A person confirms each surface, property and guideline, and the reason is written beside it. The reason: each has reasons, and without them the next person cannot tell a choice from an accident.
- Each surface names who opens it and what they do there. The reason: a surface is chosen for a person and a job, so a reader can check its kind, properties and guidelines against them.
- Only surfaces are declared. The reason: a list that holds something that is not a surface sends design and tests after the wrong thing. Not decided: the written definition that tells a surface from an integration point; until it is written, a person decides each doubtful case.
- Nothing waits for the surfaces. A slice can be designed with a surface, a property or a guideline still open: the work goes on, and the designer names what it chose, so a person can declare it later. The reason: the Spec → Design business intent must not block on anything except the lock.
- Not decided: where the declared surfaces are kept, and which list of kinds they use. The model has no kind for a surface, and today four lists of kinds disagree.

## Acceptance criteria
- Given a project whose code installs a command and serves no pages, when its surfaces are proposed, then the proposal is a command line and names the files that show it.
- Given a project whose pages already use a component library and a style guide, when the guidelines of its browser surface are proposed, then they name that design system and the files that show it.
- Given a browser surface and a Phoenix memory learning for that kind of surface, when its properties are proposed, then each property the learning backs names the learning.
- Given a property or guideline that nothing in the project or in memory backs, when the proposals are made, then the agent researches it, raises a memory update with what it found, and the part stays open until a person approves the update.
- Given a proposal with no source behind it, when the proposals are checked, then it is taken out and the part is named as open.
- Given a guideline that asks for less than the accessibility level the product profile commits to, when the guidelines are checked, then it is named as below the profile, and the profile's level stands.
- Given the person corrects a proposed property, when the surfaces are written, then the surface holds the person's answer with the reason and names the person.
- Given a product that exports a file of the day's bookings, when its surfaces are declared, then the export is not on the list.
- Given a declared surface, when an agent that did not declare it designs a slice on it, then it can name the surface's kind, properties and guidelines without asking a person.
- Given no surface is declared yet, when a slice is designed, then the work goes on and what is missing is named.

## Out of scope
- Updating the declared surfaces as the project changes. Update the surfaces as the project changes (fn-update-surfaces) does it.
- Choosing the one surface of a slice and the person who tests it there. Design slices owns it.
- Designing a slice on its surface, such as its screens, its flows, its states and the look of each screen. Use the lenses on each slice owns it, following what is declared here.
- The step library of each kind of surface and the eval of each slice. Design for evaluation and testing owns them.
- The technology a surface and its design system are built with, such as a web framework or a component library and their versions. Design the technology and architecture owns it.
- The first rough profile and the product's quality levels. Specify the product owns them.
- Moving an approved memory update into Phoenix memory. A person does it on purpose, as a promotion, outside this work.

## Sources
- The one line the product owner agreed on 2026-11-03: "The project's surfaces are declared: CLI, browser, mobile or other."
- The product owner on 2026-11-07, on the first drafts: "the surface needs to be designed based on what they offer for example web would be responsive, adaptive, view ports etc.", "same for agentic like claude-code we need to use the characteristics.", "declare the surface, and its properties is what this is about for each surface we need to define guidelines example for web - we need to handle for design system etc."
- .garura/product/product-os/intents/bi-2.md: "Without shared positions, each builder invents its own answer.", "Block on anything except the lock, which is the only gate."
- .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-domains/feature.md: "Out: one rough product profile, only when none exists: the product's stage, users, way of earning and surfaces (where people use it, such as the web), with coarse quality levels."
- core/components/skills/author-domains/SKILL.md: "the `shape` at a rough cut", "(stage / users / monetization / surfaces)"
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "# web | mobile | cli | api | desktop | embedded", "The box moves ONLY by an approved decision."
- core/components/skills/author-slice/SKILL.md: "the thing the outcome names: a screen, a command line command or an endpoint.", "intent page (asked by, outcome), the personas and journeys in the model, and the placement.", "Never ask the person for them: they see the surface and the tester in the brief and say yes"
- .garura/product/product-os/software-delivery-planning/initialize/fn-setup-questions/feature.md: "the surfaces (web, mobile, command line, API)", "Where nothing backs a proposal, the question carries no proposed answer and the person answers it; there is never a default in place of a source"
- core/components/skills/author-ux-lens/SKILL.md: "`personas` and `surfaces` (medium each surface runs on,", "read from the product profile or an existing product decision. If none", "If the product already carries a visual-core decision (check under `product_base`), REUSE it"
- core/components/plays/shape-ux-lens/SKILL.md: "waits for the rebuild of the design plays after the shaping loop (#855, ADR 053)"
- standards/schemas/product-os/grounding/lens/ux.md, in Phoenix memory: "the name of the design system the real look comes from and"
- knowledge/technology/ux-responsive-default-adaptive-on-evidence.md, in Phoenix memory: "surface: web-app-or-site", "Any web surface that must work across device sizes."
- knowledge/technology/ux-design-system-tokens.md, in Phoenix memory: "How the product's visual consistency is held — design tokens and a reused component set."
- knowledge/technology/ux-navigation-by-shape.md, in Phoenix memory: "Any web surface with more than a couple of destinations."
- knowledge/technology/ux-state-and-feedback.md, in Phoenix memory: "Every screen handles its states; every action gives feedback"
- knowledge/technology/ux-accessibility-floor.md, in Phoenix memory: "surface: any-public-ui"
- knowledge/domains/content-management.md, in Phoenix memory: "Responsive rendering — one experience that reflows across viewports."
- knowledge/domains/notifications.md, in Phoenix memory: "Push — when `shape.surfaces` includes mobile (or web with push support) and timely re-engagement matters."
- knowledge/domains/payments.md, in Phoenix memory: "Wallets — Apple Pay / Google Pay one-tap. Add when `shape.surfaces` includes mobile."
- standards/schemas/eval/steps-command-line.yaml, in Phoenix memory: "A Claude Code play is a command-line surface: the runner starts the play as"
- core/components/skills/_shared/asking-a-person.md: "Each question asks one thing."
- standards/rules/user-facing-voice.md, in Phoenix memory: "When addressing the user, lead in the language the user operates in:"
- standards/rules/naming.md, in Phoenix memory: "Never a tool's own command."
- standards/rules/surface-contract.md, in Phoenix memory: "`surface.type` is exactly one of:", "For each `surface.type`, validation is only complete when it has run the matching"
- GitHub #553 (open, under the Spec → Design business intent in the tracker): "an API can be a surface", "Nobody ever asked what kind of screen this is."
- GitHub #559 (open): "Every surface record carries a medium and a reason for it.", "It had reasons that belong on the record", "it has to read tool logs on that laptop, which a browser cannot, and has to run nightly when no browser is open", "granting access should not require a technical person"
- GitHub #560 (open): "CVS downloads are integration points. we will never expose that as a surface.", "A person downloading a file does not make the file a surface."
- GitHub #562 (open): "The profile's surface list contains only surfaces, and contains every surface the capability needs."
- core/tools/memory/GUIDE.md: "Never answer from what you already know, and never from the web, without a", "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- core/tools/memory/GUIDE.md: "Your work goes on while the update waits, unless you cannot go on without it.", "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
