# Capability: Manage surfaces

## Directional intent
The project's surfaces are declared: CLI, browser, mobile or other.
A surface is a place where a person, or another system, opens the product to use it. This capability declares each surface the project has, with what the surface offers and the rules for designing on it, so that every design on that surface is made for it. Each declared surface holds:
- its name and its kind: a command line, a browser, a mobile app, or another kind, such as an API that another system calls;
- who opens it, what they do there, and why it is that kind;
- its properties: what the surface offers and how it behaves. For a browser surface, for example, whether one layout reflows across screen sizes (responsive) or each device gets a layout of its own (adaptive), and which screen sizes (viewports) it serves. For a coding agent that a person runs in a terminal, such as Claude Code, its own characteristics, for example that each piece of work runs as a command and the person answers by typing;
- its guidelines: what every design on that surface must handle. For a browser surface, for example, working within the project's design system, the shared colours, type and components that every screen is built from. For a coding agent, for example, how it asks a person a question and how it reports back;
- for each part, its source and the person who confirmed it.

The surfaces are declared once for the project, before the slices are designed, and they are updated as the project changes. A slice is an ordered group of features that one person can test end to end on one surface. Each slice picks its one surface from the declared ones, and its design follows that surface's properties and guidelines. Designing the slice stays with Design slices and Use the lenses on each slice, which read what is declared here.
An agent proposes each surface, property and guideline, and a person confirms it. The agent looks first at what the project already holds, its code, its settings and its own records, then at Garura memory, then at Phoenix memory. Garura memory is the memory Garura keeps for the project, and it holds the product model, the shared map of the product that people and agents read. Phoenix memory is the shared memory on the machine that every project draws from; its learnings say what fits a kind of surface. Only when none of them has an answer does the agent research it. It then raises what it found as a memory update, a proposed addition to memory, and a person approves it before it is used. Nothing comes from what the AI agent knows by itself.
It matters to software delivery planning because that domain prepares the work before agents build it. A design made without knowing what its surface offers is made for the wrong surface, and it is written again once someone notices.

Features:
- Declare a surface, its properties and its guidelines (fn-declare-surfaces): declares each surface the project has, with its kind, who opens it and why, what it offers and how it behaves, and the guidelines every design on it must handle, so each design on that surface is made for it.
- Update the surfaces as the project changes (fn-update-surfaces): when the project gains or drops a surface, or a surface's kind, properties or guidelines must change, a person confirms an update, and what held before stays readable with why it changed.

What is not built yet:
- Neither feature is built. Nothing declares a surface, its properties or its guidelines for the whole project.
- When a product is first specified, a rough list of surface kinds is written into the product profile, and only when the project has no profile yet. The product profile is the record of the product's shape, such as its stage, its users and its surfaces, and of the quality levels it commits to. The list holds one word for each kind, with no properties and no guidelines, nobody confirms it on its own, and nothing changes it later.
- Each slice names its one surface when it is shaped, from its business intent, a need the product meets in the words of the person who asked for it, and from the people in the model. It does not read the profile's list.
- As built, a slice's own design decides parts of this alone. The design play for a slice's screens is stale and waits for a rebuild. It records, for its own slice, the kind each surface runs on and why. It reads the name of the design system from the product profile or an earlier decision, and records the product's visual core as a decision that later slices reuse, so the first slice would set it for the whole product.
- Phoenix memory holds properties and guidelines only in parts. Its learnings for a browser surface cover layout across screen sizes, navigation, design tokens and components, states and feedback, and forms, and one for any public screen covers accessibility. Its domain shelves say what a mobile surface brings, such as alerts pushed to a phone. For a coding agent, the only rules written down are Garura's own: how its plays ask a person, how they report back, and that no command name is a coding tool's own command. Nothing joins them into the properties and guidelines of a declared surface.
- Four lists of surface kinds disagree: the product profile's, the eval's, an older rule's for the surface a piece of work promises, and the one initialize, the project set-up step, will ask about. The eval is the test that checks a slice from the outside, on its surface.
- The product model has no kind for a surface, so where the declared surfaces are kept is not decided.
- The planned work for this capability is tracked and not built: every surface carries its kind, decided by a person with the reason; a written definition tells a surface from an integration point, a place where the product hands something to another system, such as a file it exports; and the profile's list holds only surfaces, and every surface the product needs.

### Benefit hypothesis
- Who it serves: the product owner, who decides where people use the product and what each surface must handle; and the agents that design, build and test each slice on its surface.
- What we believe: every slice is designed for the surface it is on, and no design is written again because it was made for the wrong surface, if the work stands on these rules:
  - Each surface is declared once for the project, with its properties and its guidelines, not worked out again in each slice.
  - A person confirms each surface, property and guideline, and its reason is written down.
  - Each one comes from the project's code or memory, or from research a person approved into memory.
  - The design of each slice on a surface follows that surface's properties and guidelines.
  - The surfaces are updated as the project changes, and what held before stays readable with why it changed.
  - Nothing waits for the surfaces.
- How we will know: two slices built at different times on one surface follow the same properties and guidelines, and no slice's design is written again because it was made for the wrong kind of surface.
  - This is not tested today, because nothing declares a surface's properties or guidelines.

### Boundary (In / Out / Never)
- In: declaring each surface the project has: its name, its kind, who opens it and what they do there, and why it is that kind.
- In: declaring each surface's properties, what it offers and how it behaves, and its guidelines, what every design on it must handle.
- In: updating the surfaces, their properties and their guidelines as the project changes, keeping what held before and why it changed.
- Out: the first rough list of surfaces, and the rest of the product profile. Specify the product writes the first rough profile and sets its quality levels. This capability takes the rough list as a proposal and reads the quality levels to bound the guidelines. It never writes the profile's stage, users or quality levels.
- Out: choosing the one surface of a slice and the person who tests it there. Design slices (Design → Code) owns it, and picks from the declared surfaces.
- Out: designing a slice on its surface, such as its screens, its flows, its states and the look of each screen. Use the lenses on each slice owns it, following the surface's properties and guidelines, and Bring the design together for a vertical slice joins it with the rest of the slice's design. A lens is one view of a slice's design, such as its screens or its architecture.
- Out: how each kind of surface is tested. Design for evaluation and testing owns the eval of each slice and the step library of each kind of surface. A step library is the fixed list of sentences that a test step may use on one kind of surface.
- Out: the technology a surface and its design system are built with, such as a web framework or a component library and their versions. Design the technology and architecture owns it. This capability names the design system that designs on a surface work within, and the guideline to stay within it.
- Out: putting the memory and the review rules that fit the surfaces into the project. Seed the memory for the lenses, a part of the project set-up step (initialize), owns it, and reads the declared surfaces.
- Out: writing the decision record behind an update, accepting it and keeping its history. A decision record says what was decided, why, and what else was weighed. Manage ADRs (Orchestration) owns the records; this capability decides what the update says and hands it over.
- Out: moving an approved memory update into Phoenix memory. A memory update goes to the project's short-term memory, and moving it up is a promotion a person makes on purpose, outside this work.
- Out: how the product is deployed (Deployment design), its environments (Environment setup), and locking the design before agents take over (Lock the design, the only gate).
- Never: block work on a missing surface, property or guideline. The work goes on from the project's code and memory, and what is open is named. The reason: the Spec → Design business intent must not block on anything except the lock.
- Never: declare a surface, a property or a guideline from what the AI agent knows by itself, or one that no person confirmed. The reason: they decide how every slice on that surface is designed, and an agent's guess is found wrong only after the design is written.
- Never: change a declared surface in place. An update replaces what held before and keeps it. The reason: slices already designed on the old surface must still be explainable.

### Guiding rules
- Once for each surface of the project, not once in each slice. The reason: when nobody declares what a surface offers and what its designs must handle, each slice's design decides it alone, and the first slice decides for every later one.
- The design follows the surface. Each slice's design on a surface reads that surface's properties and guidelines and keeps to them. The reason: a design made without them is made for the wrong surface, as when a surface meant to be a web page was designed as a terminal command, and its screens were then drawn again.
- The project's memory first, then Garura memory, then Phoenix memory, then research. Each surface, property and guideline is proposed first from what the project holds: the commands its code installs, its pages and their layouts, its components and its style guide, the apps it ships, what a person gave when the product was specified, and the business intents with who asks for each. Then from Garura memory, then from Phoenix memory's learnings for that kind of surface. Only when no memory has an answer does the agent research it, and it raises what it found as a memory update for a person to approve. Nothing is declared from what the AI agent knows by itself. The reason: a source in the project or in memory can be checked and read back, while the agent's own knowledge cannot.
- Research is used only after a person approves it. Until then the surface, property or guideline stays open, with no default, and the work goes on. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- What the project's code already has is described as it is, such as a component library and a style guide its pages already use. The reason: a declaration that contradicts what runs sends every design after a surface that nobody builds.
- Each property and guideline names its source: a file of the project, a Source, a memory file or an approved memory update. A Source is a saved copy of what a person gave, such as a prototype or a document. The reason: a person can check each one without a search, and when a learning in memory changes, the declarations built on it can be found.
- Each guideline follows from what its surface offers, or from a quality level the product profile commits to. The reason: a guideline with no reason in its surface is a rule nobody can judge, and a property with no guideline leaves each slice to handle it alone.
- The product profile's quality levels bound the guidelines. A guideline meets the levels the profile commits to, such as an accessibility level, and never changes them. The reason: the profile is the box the product commits to, and Specify the product owns it.
- A person confirms each surface, property and guideline, and the reason is written beside it. The reason: each has reasons, such as a tool that must read files on a laptop at night and so stays a command line, and without them the next person cannot tell a choice from an accident.
- Each surface names who opens it and what they do there. The reason: a surface is chosen for a person and a job, so a reader can check its kind, properties and guidelines against them.
- Only surfaces are declared. A file the product hands out, such as an export, is not a surface. The reason: a list that holds something that is not a surface sends design and tests after the wrong thing. Not decided: the written definition that tells a surface from an integration point; until it is written, a person decides each doubtful case.
- A missing surface, property or guideline is a gap, not a stop. A slice can be designed with one still open; the designer names what it chose, so a person can declare it later. The reason: the business intent's only gate is the lock.
- The surfaces are kept where every agent looks first. Agents gather context from the project's code and from Garura memory before Phoenix memory, and the product model is part of Garura memory. The reason: a declaration that designers do not find is no declaration. Not decided: the place in the model and the one list of kinds, because the model has no kind for a surface and today four lists of kinds disagree.

## Sources
- The one line the product owner agreed on 2026-11-03: "The project's surfaces are declared: CLI, browser, mobile or other."
- The product owner on 2026-11-07, on the first drafts: "the surface needs to be designed based on what they offer for example web would be responsive, adaptive, view ports etc.", "same for agentic like claude-code we need to use the characteristics.", "declare the surface, and its properties is what this is about for each surface we need to define guidelines example for web - we need to handle for design system etc.", "the design would be for that surface"
- The capability list the product owner locked on 2026-11-03: "Seed the memory for the lenses: The memory each design lens needs is seeded, ready for slices to use. It is part of initialize, not a play.", "Lock the design: A design is locked before agents take over. This is the only gate", "Bring the design together for a vertical slice: The separate parts of the design (UX, technology, aesthetics, surfaces, testing) come together cohesively to deliver one vertical slice."
- .garura/product/product-os/intents/bi-2.md: "The project's positions are set for the whole project: technology and architecture, surfaces, deployment and environments.", "Without shared positions, each builder invents its own answer.", "Each position is written down and can change later.", "Block on anything except the lock, which is the only gate."
- .garura/product/product-os/software-delivery-planning/domain.md: "Its job comes before the build"
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "Out: the project's surfaces (Manage surfaces), how the product is deployed and the platform it runs on (Deployment design), and its environments (Environment setup)."
- .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-domains/feature.md: "Out: one rough product profile, only when none exists: the product's stage, users, way of earning and surfaces (where people use it, such as the web), with coarse quality levels."
- core/components/skills/author-domains/SKILL.md: "the `shape` at a rough cut", "(stage / users / monetization / surfaces)", "Omit the profile block if one already exists in the"
- core/components/plays/discover-domains/scripts/persist_seed.py: "the profile block: added ONLY if the live spine has none."
- core/components/plays/discover-capabilities/scripts/rollup_box.py: "proposed = dict(profile)"
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "# web | mobile | cli | api | desktop | embedded", "The profile is THE BOX — the product's committed boundaries.", "The box moves ONLY by an approved decision."
- core/components/skills/author-slice/SKILL.md: "the thing the outcome names: a screen, a command line command or an endpoint.", "intent page (asked by, outcome), the personas and journeys in the model, and the placement."
- core/components/skills/author-ux-lens/SKILL.md: "`personas` and `surfaces` (medium each surface runs on,", "read from the product profile or an existing product decision. If none", "If the product already carries a visual-core decision (check under `product_base`), REUSE it"
- core/components/plays/shape-ux-lens/SKILL.md: "waits for the rebuild of the design plays after the shaping loop (#855, ADR 053)"
- standards/schemas/product-os/lens/ux.yaml, in Phoenix memory: "the product's visual core (set once, referenced by every capability)"
- standards/schemas/product-os/grounding/lens/ux.md, in Phoenix memory: "the name of the design system the real look comes from and"
- knowledge/technology/ux-responsive-default-adaptive-on-evidence.md, in Phoenix memory: "surface: web-app-or-site", "Any web surface that must work across device sizes."
- knowledge/technology/ux-design-system-tokens.md, in Phoenix memory: "How the product's visual consistency is held — design tokens and a reused component set.", "Any web surface, especially once there's more than a handful of screens."
- knowledge/technology/ux-accessibility-floor.md, in Phoenix memory: "surface: any-public-ui"
- knowledge/domains/content-management.md, in Phoenix memory: "Responsive rendering — one experience that reflows across viewports."
- knowledge/domains/notifications.md, in Phoenix memory: "Push — when `shape.surfaces` includes mobile (or web with push support) and timely re-engagement matters."
- standards/schemas/eval/steps-command-line.yaml, in Phoenix memory: "A Claude Code play is a command-line surface: the runner starts the play as"
- core/components/skills/_shared/asking-a-person.md: "Each question asks one thing."
- standards/rules/user-facing-voice.md, in Phoenix memory: "When addressing the user, lead in the language the user operates in:"
- standards/rules/naming.md, in Phoenix memory: "Never a tool's own command."
- standards/schemas/eval/_index.md, in Phoenix memory: "One step library for each surface kind of a slice's eval (ADR 057)"
- standards/rules/surface-contract.md, in Phoenix memory: "`surface.type` is exactly one of:", "For each `surface.type`, validation is only complete when it has run the matching"
- .garura/product/product-os/software-delivery-planning/initialize/fn-setup-questions/feature.md: "the surfaces (web, mobile, command line, API)"
- The names agreed with the product owner on 2026-11-03: "/design-surface (was /shape-ux-lens)"
- GitHub #553 (open, under the Spec → Design business intent in the tracker): "an API can be a surface", "terminal CUI types, full blown browser CX, mobile app types, or someting that is more like IDX? generative HTML types?"
- GitHub #559 (open): "Every surface record carries a medium and a reason for it.", "it has to read tool logs on that laptop, which a browser cannot, and has to run nightly when no browser is open", "the screens and their states redrawn from scratch"
- GitHub #560 (open): "CVS downloads are integration points. we will never expose that as a surface."
- GitHub #562 (open): "The profile's surface list contains only surfaces, and contains every surface the capability needs."
- core/tools/memory/GUIDE.md: "Never answer from what you already know, and never from the web, without a", "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
- core/tools/memory/GUIDE.md: "An update always goes to the issue's short-term memory, and it is used only after a person", "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
- core/tools/memory/GUIDE.md: "order: `core/memory`, then the product model (`product`)."
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf covers software delivery planning.
