# Capability: Design the technology and architecture

## Directional intent
The technology and architecture for the whole project are set here and can evolve. Nothing blocks on them.
A position is one choice that holds for the whole project, written down with its reasons. This capability sets two kinds of position:
- A technology position names what the project is built with: a programming language, a framework, a data store or an outside platform, each with its version.
- An architecture position names the shape of the whole system: its style, such as one deployable unit split into modules or separate services; its main parts and the job of each; and how the parts connect to each other and to outside systems.

The positions are set once for the project, before the slices are designed, and they change as the project grows. A slice is an ordered group of features that one person can test end to end on one surface. Each slice is then designed and built on the positions, and does not choose its own.
A person confirms each position. An agent proposes it from what is already known: the project's own code when it has some, or memory. Memory is where agents look for what is known; for this capability it holds learnings about which technology and which system shape fit a product in given conditions, and when each choice is outgrown.
It matters to software delivery planning because that domain prepares the work before agents build it. Without shared positions, each builder invents its own answer, and two slices of one product end up built on different technology for the same job.

Features:
- Set the project's technology (fn-set-technology): sets what the whole project is built with, its languages, frameworks, data stores and outside platforms, each confirmed by a person with its source and reasons.
- Set the project's architecture (fn-set-architecture): sets the shape of the whole system, its style, its main parts and how they connect, so every slice builds on the same shape.
- Change a position as the project evolves (fn-change-position): when the project outgrows a position, a person replaces it with a new one, and the old one stays readable with why it changed.

What is not built yet:
- None of the three features is built. Nothing in the current flow sets a position for the whole project.
- Today an agent learns the project's technology only from its code and its memory. So a new project gets whatever its first builder picks.
- The play that designs architecture is stale: it waits for a rebuild. It designs one slice at a time, and it records the slice's technology as a decision that later slices reuse. So, as built, the first slice would set the technology of the whole project.
- An older skill writes an architecture for the whole project, with its technology. No play calls it, and the files it reads were deleted with the retired planning chain.
- The product model has no kind for a position. The product model is the shared map of the product that people and agents read. An older decision left the place of project-wide design to the model's ontology, the agreed list of the kinds of things a product is made of, and the ontology has not answered it.

### Benefit hypothesis
- Who it serves: the architect, who decides the project's technology and architecture; the product owner, who asked that every builder work from the same positions; and the agents that design and build each slice.
- What we believe: the slices of one project fit together and stay buildable as the product grows, if the work stands on these rules:
  - The technology and architecture are decided once for the project, not again in every slice.
  - Each position comes from the project's code or from memory, and a person confirms it.
  - A position can change, and the old one stays readable with why it changed.
  - Nothing waits for a position.
- How we will know: two slices built at different times use the same technology for the same job, and each difference between them traces to a position or to a recorded change of one.
  - This is not tested today, because nothing sets a position for the whole project.

### Boundary (In / Out / Never)
- In: setting the technology positions for the whole project: its languages, frameworks, data stores and outside platforms, each with its version.
- In: setting the architecture positions for the whole project: its style, its main parts and the job of each, and how the parts connect.
- In: changing a position as the project grows, keeping the old one and why it changed.
- Out: designing one slice through the lenses. A lens is one view of a slice's design, such as its screens or its architecture: for architecture, the parts the slice passes through and what crosses between them. Use the lenses on each slice (Design → Code) owns it, and builds on the positions set here.
- Out: the product profile. The profile holds the product's shape, such as its stage, its users and its surfaces, and the quality levels it commits to, such as how fast, how secure and how reliable it must be. Specify the product sets it and rolls it up. This capability reads it to size each position and never writes it.
- Out: writing the decision record behind a position, accepting it and keeping its history. A decision record says what was decided, why, and what else was weighed. Manage ADRs (Orchestration) owns the records; this capability decides what each position says and hands it over.
- Out: putting the memory that matches the positions into the project. Seed the memory for the lenses, a part of the project set-up step (initialize), owns it.
- Out: the project's surfaces (Manage surfaces), how the product is deployed and the platform it runs on (Deployment design), and its environments (Environment setup).
- Out: locking the design before agents take over. Lock the design owns the lock, the only gate.
- Never: block work on a missing position. The work goes on from the project's code and memory, and the open choice is named. The reason: the Spec → Design business intent must not block on anything except the lock.
- Never: write a position that no person confirmed, or one with no source. The reason: a position with no source is the agent's taste, and every builder after it would build on a guess.
- Never: change a position's words in place. A change is a new position that replaces the old one. The reason: work already built on the old position must still be explainable.

### Guiding rules
- Once for the project, not once in each slice. The reason: most design is the same for every slice, so deciding it again in each one costs time, and slices that decide alone end up different.
- Each proposal comes from what is known: the project's code and its settings first, then memory's learnings for a product in the same conditions. Each proposal names its source, and a choice that nothing backs stays open, with no default. The reason: a default looks like a fact, and nobody can judge it.
- The product profile sizes each position. A position must meet the quality levels the profile commits to, without going far beyond them. The reason: a small internal tool does not need the technology of a public payments product, and a public product cannot run on the technology of a throwaway.
- A technology position names a real product and its version, not a kind of product. The reason: a builder told "a relational database" must still choose one, and the next builder may choose another.
- A person confirms each position and each change. The reason: a position binds every builder in the project, so an agent never sets one alone.
- A missing position is a gap, not a stop. The builder goes by the project's code and memory and names what it chose, and the gap stays on record so a later step knows it was skipped, not forgotten. The reason: the business intent's only gate is the lock.
- Positions are kept where every agent looks first. Agents gather context from the project's code and the project's own memory, Garura memory, before Phoenix memory, the global memory, and the product model is part of Garura memory. The reason: a position that builders do not find is no position. Not decided: the place in the model, because the model has no kind for a position.

## Sources
- The one line the product owner agreed on 2026-11-03: "The technology and architecture for the whole project are set here and can evolve. Nothing blocks on them."
- The capability list the product owner locked on 2026-11-03: "Seed the memory for the lenses: The memory each design lens needs is seeded, ready for slices to use. It is part of initialize, not a play.", "Lock the design: A design is locked before agents take over. This is the only gate", "Use the lenses on each slice: Each slice is designed through the lenses", "Manage ADRs: Decisions on how the project is built are recorded closely as they're made"
- .garura/product/product-os/intents/bi-2.md: "The project's positions are set for the whole project: technology and architecture, surfaces, deployment and environments.", "Without shared positions, each builder invents its own answer.", "Each position is written down and can change later.", "Block on anything except the lock, which is the only gate."
- .garura/product/product-os/software-delivery-planning/domain.md: "Its job comes before the build"
- docs/adr/028-agentic-lifecycle-five-loops.md: "These set the project's guidelines, rules, and guardrails. Every slice follows them.", "re-deriving it per slice is ceremony", "A skipped area can be built up later at runtime by the execution trinities"
- docs/adr/028-agentic-lifecycle-five-loops.md, Open question 3: "Where do the project-wide design outputs live in the product model?", "The product model is to be rebuilt as an ontology"
- docs/adr/014-three-axis-project-profiling.md: "Rejected because architecture is product-scoped, not epic-scoped.", "An architecture chosen per-epic would risk inconsistency across epics."
- docs/adr/050-the-retired-intent-epic-pipeline-is-deleted.md: "the `derive-*` skills for capability selection, design patterns, logical architecture, NFR spec, physical architecture, quality vision, systems inventory and tech stack"
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md: "Locking a design is a governance check. Initialize, seeding memory and upgrade are engine things, not plays."
- core/components/plays/shape-architecture-lens/SKILL.md: "waits for the rebuild of the design plays after the shaping loop (#855, ADR 053)"
- core/components/plays/shape-architecture-lens/reference/ice.md: "The stack is a material choice recorded as a slice-level decision the whole product", "it is sized by the profile box, not invented per slice", "reuse the product decision if one exists", "never the model's taste"
- core/components/skills/author-technical-approach/SKILL.md: "e.g., `.garura/product/architecture/`", "NEVER use vague technology references", "ALWAYS include rationale for every technology selection"
- core/components/agents/tech-designer.md: "if LOCKED, use as authoritative (stop descending). If DRAFT, use as advisory (continue descending)."
- core/components/plays/record-decision/SKILL.md: "a product decision, a `decision.yaml` record", "Only a person accepts an ADR."
- core/tools/memory/GUIDE.md: "order: `core/memory`, then the product model (`product`)."
- .garura/product/product-os/software-delivery-planning/specify-product/capability.md: "In: setting each capability's quality and compliance needs, and rolling them up into the product profile."
- .garura/product/product-os/software-delivery-planning/initialize/fn-setup-questions/feature.md: "the technology standards, the tools and frameworks"
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "The profile is THE BOX — the product's committed boundaries.", "The box moves ONLY by an approved decision."
- standards/schemas/product-os/decision.yaml, in Phoenix memory: "accepted decisions are not edited — supersede or amend with a new record"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "A plan can be built and worked on before the product model is complete"
- knowledge/_index.md, in Phoenix memory: "`architecture/` — product-condition → best-fit architecture ladders", "`technology/` — specific technology/stack choices and the conditions they fit."
- GitHub #608 (open): "How a skipped design area is recorded, so a later loop knows it was skipped and not forgotten."
- GitHub #426 (closed): "Decide the unit for architectural traceability deliberately"
- The names agreed with the product owner on 2026-11-03: "/design-architecture (was /shape-architecture-lens)"
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No domain shelf in memory covers designing a software project's technology and architecture (the placement run found none).
