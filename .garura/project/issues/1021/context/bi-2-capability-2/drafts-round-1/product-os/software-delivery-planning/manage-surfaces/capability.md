# Capability: Manage surfaces

## Directional intent
The project's surfaces are declared: CLI, browser, mobile or other.
A surface is a place where a person, or another system, opens the product to use it. The project's surfaces are the list of these places for the whole project. Each surface is written down with:
- its name, such as a clinic's booking page, a shop's mobile app or a build tool's release command;
- its kind: a command line, a browser, a mobile app, or another kind, such as an API that another system calls;
- who opens it and what they do there;
- why it is that kind, with its source and the person who confirmed it.

The surfaces are declared once for the project, before the slices are designed, and they are updated as the project changes. A slice is an ordered group of features that one person can test end to end on one surface. Each slice then picks its one surface from the declared ones, and its design and its tests start from that surface's kind.
An agent proposes each surface and its kind, and a person confirms it. The agent looks first at what the project already holds, its code, its settings and its own records, then at Garura memory, then at Phoenix memory. Garura memory is the memory Garura keeps for the project, and it holds the product model, the shared map of the product that people and agents read. Phoenix memory is the shared memory on the machine that every project draws from. Only when none of them has an answer does the agent research it. It then raises what it found as a memory update, a proposed addition to memory, and a person approves it before it is used. No surface and no kind comes from what the AI agent knows by itself.
It matters to software delivery planning because that domain prepares the work before agents build it. When nobody declares the kind of a surface, the first design assumes one, and a wrong kind found after the design is written costs a rewrite of the design.

Features:
- Declare the project's surfaces (fn-declare-surfaces): sets the list of places where people or other systems use the product, each with its kind, who opens it, what they do there and why, so every slice is designed and tested on a declared surface.
- Update the surfaces as the project changes (fn-update-surfaces): when the project gains or drops a surface, or a surface must change its kind, a person confirms an update, and what held before stays readable with why it changed.

What is not built yet:
- Neither feature is built. Nothing declares the project's surfaces, and nothing records a surface's kind with its reason and the person who decided it.
- When a product is first specified, a rough list of surface kinds is written into the product profile, and only when the project has no profile yet. The product profile is the record of the product's shape, such as its stage, its users and its surfaces, and of the quality levels it commits to. Nobody confirms the list on its own, it holds one word for each kind, and nothing changes it later: firming the profile keeps it as it was.
- Each slice names its one surface when it is shaped, from its business intent, a need the product meets in the words of the person who asked for it, and from the people in the model. It does not read the profile's list.
- Four lists of surface kinds disagree:
  - the product profile has web, mobile, cli, api, desktop and embedded;
  - the eval of a slice, the test that checks it from the outside, has command line, browser page, mobile app and backend endpoint, and finds the kind by matching words in the name of the slice's surface;
  - an older rule for the surface a piece of work promises has web dashboard, server API, command line, library and internal service;
  - the project set-up step, initialize, not built, will ask about web, mobile, command line and API.
- The product model has no kind for a surface, so where the declared surfaces are kept is not decided. An older decision also left open where a surface's type, the way a person reaches it and what must open are kept, now that the work record that held them is gone.
- The planned work for this capability is tracked and not built: every surface carries its kind, decided by a person with the reason; a written definition tells a surface from an integration point, a place where the product hands something to another system, such as a file it exports; and the profile's list holds only surfaces, and every surface the product needs.

### Benefit hypothesis
- Who it serves: the product owner, who decides where people use the product; and the agents that design, build and test each slice on its surface.
- What we believe: every slice is designed and tested on the right kind of surface from the start, if the work stands on these rules:
  - The surfaces are declared once for the project, not assumed again in each slice.
  - A person confirms each surface's kind, and its reason is written down.
  - Each surface comes from the project's code or memory, or from research a person approved into memory.
  - The surfaces are updated as the project changes, and what held before stays readable with why it changed.
  - Nothing waits for the surfaces.
- How we will know: no slice's surface turns out to be the wrong kind after its design is written, and the surface of each slice is on the declared list or named as a gap.
  - This is not tested today, because nothing declares the project's surfaces.

### Boundary (In / Out / Never)
- In: declaring the project's surfaces: each one's name, its kind, who opens it and what they do there, and why it is that kind.
- In: updating the surfaces as the project changes, keeping what held before and why it changed.
- Out: the first rough list of surfaces, and the rest of the product profile. Specify the product writes the first rough profile when the product is first specified, and sets its quality levels. This capability takes that rough list as a proposal and is where the list is confirmed and kept up to date. It never writes the profile's stage, users or quality levels.
- Out: choosing the one surface of a slice and the person who tests it there. Design slices (Design → Code) owns it, and picks from the declared surfaces.
- Out: designing what a person sees and does on a surface for one slice, such as its screens or its commands. Use the lenses on each slice owns it, and Bring the design together for a vertical slice joins it with the rest of the slice's design. A lens is one view of a slice's design, such as its screens or its architecture.
- Out: how each kind of surface is tested. Design for evaluation and testing owns the eval of each slice and the step library of each kind of surface. A step library is the fixed list of sentences that a test step may use on one kind of surface. It finds the library from the kind declared here.
- Out: the technology each surface is built with, such as its web framework. Design the technology and architecture owns it, and reads the declared surfaces.
- Out: putting the memory and the review rules that fit the surfaces into the project. Seed the memory for the lenses, a part of the project set-up step (initialize), owns it, and reads the declared surfaces.
- Out: writing the decision record behind an update, accepting it and keeping its history. A decision record says what was decided, why, and what else was weighed. Manage ADRs (Orchestration) owns the records; this capability decides what the update says and hands it over.
- Out: moving an approved memory update into Phoenix memory. A memory update goes to the project's short-term memory, and moving it up is a promotion a person makes on purpose, outside this work.
- Out: how the product is deployed (Deployment design), its environments (Environment setup), and locking the design before agents take over (Lock the design, the only gate).
- Never: block work on a missing surface or an open kind. The work goes on from the project's code and memory, and the open surface is named. The reason: the Spec → Design business intent must not block on anything except the lock.
- Never: declare a surface or a kind from what the AI agent knows by itself, or one that no person confirmed. The reason: the kind decides how every slice on that surface is designed and tested, and a kind an agent assumed is found wrong only after the design is written.
- Never: change the declared surfaces in place. An update replaces what held before and keeps it. The reason: slices already designed on the old surfaces must still be explainable.

### Guiding rules
- Once for the project, not once in each slice. The reason: when nobody declares a kind, the first design assumes one, and every later slice inherits the guess.
- The project's memory first, then Garura memory, then Phoenix memory, then research. Each surface and its kind are proposed first from what the project holds: the commands its code installs, the pages it serves, the apps it ships, what a person gave when the product was specified, the business intents with who asks for each, and the rough list in the product profile. Only when no memory has an answer does the agent research it, and it raises what it found as a memory update for a person to approve. A surface is never declared from what the AI agent knows by itself. The reason: a source in the project or in memory can be checked and read back, while the agent's own knowledge cannot.
- Research is used only after a person approves it. Until then the surface or its kind stays open, with no default, and the work goes on. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- A surface the project's code already has is described as it is. The reason: a list that contradicts what runs sends the design after a surface that nobody uses.
- Each proposal names its source: a file of the project, a Source, a memory file or an approved memory update. A Source is a saved copy of what a person gave, such as a prototype or a document. The reason: a person can then check each surface without a search.
- A person confirms each surface's kind, and the reason is written beside it. The reason: a kind has reasons, such as a tool that must read files on a laptop at night and so stays a command line, or a page where a person who is not technical grants access and so is not a command line. Without the reason, the next person cannot tell a choice from an accident.
- Each surface names who opens it and what they do there. The reason: a kind fits a person and a job, so a reader can check the one against the other.
- Only surfaces are declared. A file the product hands out, such as an export, is not a surface. The reason: a list that holds something that is not a surface, or misses one that is, sends design and tests after the wrong thing. Not decided: the written definition that tells a surface from an integration point; until it is written, a person decides each doubtful case.
- A missing surface is a gap, not a stop. A slice can be designed on a surface not yet declared, and the surface is named so a person can declare it. The reason: the business intent's only gate is the lock.
- The surfaces are kept where every agent looks first. Agents gather context from the project's code and from Garura memory before Phoenix memory, and the product model is part of Garura memory. The reason: a list of surfaces that builders do not find is no list. Not decided: the place in the model and the one list of kinds, because the model has no kind for a surface and today four lists of kinds disagree.

## Sources
- The one line the product owner agreed on 2026-11-03: "The project's surfaces are declared: CLI, browser, mobile or other."
- The capability list the product owner locked on 2026-11-03: "Seed the memory for the lenses: The memory each design lens needs is seeded, ready for slices to use. It is part of initialize, not a play.", "Lock the design: A design is locked before agents take over. This is the only gate", "Bring the design together for a vertical slice: The separate parts of the design (UX, technology, aesthetics, surfaces, testing) come together cohesively to deliver one vertical slice."
- .garura/product/product-os/intents/bi-2.md: "The project's positions are set for the whole project: technology and architecture, surfaces, deployment and environments.", "Without shared positions, each builder invents its own answer.", "Each position is written down and can change later.", "Block on anything except the lock, which is the only gate."
- .garura/product/product-os/software-delivery-planning/domain.md: "Its job comes before the build"
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "Out: the project's surfaces (Manage surfaces), how the product is deployed and the platform it runs on (Deployment design), and its environments (Environment setup)."
- .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-domains/feature.md: "Out: one rough product profile, only when none exists: the product's stage, users, way of earning and surfaces (where people use it, such as the web), with coarse quality levels."
- core/components/skills/author-domains/SKILL.md: "the `shape` at a rough cut", "(stage / users / monetization / surfaces)", "Omit the profile block if one already exists in the"
- core/components/plays/discover-domains/scripts/persist_seed.py: "the profile block: added ONLY if the live spine has none."
- core/components/plays/discover-capabilities/scripts/rollup_box.py: "proposed = dict(profile)"
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "# web | mobile | cli | api | desktop | embedded", "The profile is THE BOX — the product's committed boundaries."
- core/components/skills/author-slice/SKILL.md: "the thing the outcome names: a screen, a command line command or an endpoint.", "intent page (asked by, outcome), the personas and journeys in the model, and the placement."
- core/components/plays/shape-slice/reference/ice.md: "The surface and the tester are never a gap and never a question: an intent does"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "It has one screen or surface that a person can test end to end."
- standards/schemas/eval/_index.md, in Phoenix memory: "One step library for each surface kind of a slice's eval (ADR 057)", "A library for the browser page, the mobile app and the backend endpoint is added when a slice first needs it."
- core/components/plays/shape-eval/reference/ice.md: "The surface kind comes from the hidden", "A slice whose surface kind has no step library yet gets no eval"
- standards/rules/surface-contract.md, in Phoenix memory: "`surface.type` is exactly one of:", "The surface is declared once, at the cut, and checked — never re-derived."
- docs/adr/048-the-product-model-and-the-work-are-two-layers.md: "Where the structured surface contract (type, how a person reaches it, what must open) lives after the epic record leaves is"
- .garura/product/product-os/software-delivery-planning/initialize/fn-setup-questions/feature.md: "the surfaces (web, mobile, command line, API)"
- .garura/product/product-os/software-delivery-planning/initialize/fn-review-rule-groups/feature.md: "Surfaces with no web and no mobile: the front-end group is skipped, because there is no screen for its rules to check."
- core/components/skills/author-ux-lens/SKILL.md: "`personas` and `surfaces` (medium each surface runs on,"
- The names agreed with the product owner on 2026-11-03: "/design-surface (was /shape-ux-lens)"
- GitHub #553 (open, under the Spec → Design business intent in the tracker): "an API can be a surface", "Nobody ever asked what kind of screen this is."
- GitHub #559 (open): "Every surface record carries a medium and a reason for it.", "So the medium gets assumed by whichever play designs first.", "It had reasons that belong on the record", "granting access should not require a technical person"
- GitHub #560 (open): "CVS downloads are integration points. we will never expose that as a surface.", "An integration point is something a system calls or a file that leaves the product."
- GitHub #562 (open): "The profile's surface list contains only surfaces, and contains every surface the capability needs."
- core/tools/memory/GUIDE.md: "Never answer from what you already know, and never from the web, without a", "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
- core/tools/memory/GUIDE.md: "An update always goes to the issue's short-term memory, and it is used only after a person", "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
- core/tools/memory/GUIDE.md: "order: `core/memory`, then the product model (`product`)."
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf covers software delivery planning.
