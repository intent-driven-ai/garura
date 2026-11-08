# Capability: Design the technology and architecture

## Directional intent
The technology and architecture for the whole project are set here and can evolve. Nothing blocks on them.
The project's architecture is the shape of the whole system and what it is built with, written down with the reason for each choice. It holds:
- the overall style, such as one deployable unit split into modules, or separate services that each team deploys on its own;
- the main parts, each with one job, and how they connect to each other and to outside systems;
- the technology of each part: its language, its framework, its data store or an outside platform it uses, each with its version.

The architecture is set once for the project, before the slices are designed, and it is updated as the project changes. A slice is an ordered group of features that one person can test end to end on one surface. Each slice is then designed and built on the project's architecture, and does not choose its own.
An agent proposes each choice and a person confirms it. The agent reads Phoenix memory first. Phoenix memory is the shared memory on the machine that every project draws from; its architecture and technology learnings say which shape and which technology fit a product in given conditions, and when each is outgrown. Only when Phoenix memory has no answer does the agent research the choice. It then raises what it found as a memory update, a proposed addition to memory, and a person approves it before it is used.
It matters to software delivery planning because that domain prepares the work before agents build it. Without one architecture for the project, each builder invents its own answer, and two slices of one product end up built on different technology for the same job.

Features:
- Set the project's architecture (fn-set-architecture): sets the shape of the whole system and what it is built with, its style, its main parts and how they connect, and the technology of each part with its version, so every slice builds on the same architecture.
- Update the architecture as the project changes (fn-update-architecture): when the project outgrows its architecture, a person confirms an update, and what held before stays readable with why it changed.

What is not built yet:
- Neither feature is built. Nothing in the current flow sets an architecture for the whole project.
- Today an agent learns the project's technology only from its code and its memory. So a new project gets whatever its first builder picks.
- The play that designs architecture is stale: it waits for a rebuild. It designs one slice at a time, and it records the slice's technology as a decision that later slices reuse. So, as built, the first slice would set the technology of the whole project.
- An older skill writes an architecture for the whole project, with its technology. No play calls it, and the files it reads were deleted with the retired planning chain.
- Reading memory first and then researching exists only in parts. A stale skill searches memory's learnings for the best fit, a skill researches on the web when memory has too little, and the memory tool raises a memory update for a person. Nothing joins them into one step for the architecture.
- The product model has no kind for the project's architecture. The product model is the shared map of the product that people and agents read. An older decision left the place of project-wide design to the model's ontology, the agreed list of the kinds of things a product is made of, and the ontology has not answered it.

### Benefit hypothesis
- Who it serves: the architect, who decides the project's architecture and its technology; the product owner, who asked that every builder work from the same architecture; and the agents that design and build each slice.
- What we believe: the slices of one project fit together and stay buildable as the product grows, if the work stands on these rules:
  - The architecture, with its technology, is decided once for the project, not again in every slice.
  - Each choice comes from Phoenix memory, or from research a person approved into memory, and a person confirms it.
  - The architecture is updated as the project changes, and what held before stays readable with why it changed.
  - Nothing waits for the architecture.
- How we will know: two slices built at different times use the same technology for the same job, and each difference between them traces to the architecture or to a recorded update of it.
  - This is not tested today, because nothing sets an architecture for the whole project.

### Boundary (In / Out / Never)
- In: setting the project's architecture: its style, its main parts with one job each, how the parts connect, and the technology of each part with its version.
- In: updating the architecture as the project changes, keeping what held before and why it changed.
- Out: designing one slice: for architecture, the parts the slice passes through and what crosses between them. Designing each slice (Design → Code) owns it, and builds on the project's architecture.
- Out: the product profile. The profile holds the product's shape, such as its stage, its users and its surfaces, and the quality levels it commits to, such as how fast, how secure and how reliable it must be. Specify the product sets it and rolls it up. This capability reads it to size each choice and never writes it.
- Out: writing the decision record behind each architecture choice, accepting it and keeping its history. A decision record says what was decided, why, and what else was weighed. Manage ADRs (Orchestration) owns the records; this capability decides what each choice says and hands it over.
- Out: putting the memory that matches the architecture into the project. It belongs to the play that starts the build, not to the product model.
- Out: moving an approved memory update into Phoenix memory. A memory update goes to the project's short-term memory, and moving it up is a promotion a person makes on purpose, outside this work.
- Out: the project's surfaces (Manage surfaces), how the product is deployed and the platform it runs on (Deployment design), and its environments (Environment setup).
- Never: block work on a missing choice. The work goes on from the project's code and memory, and the open choice is named. The reason: the Spec → Design business intent blocks no work, and each design can run at any time.
- Never: make a choice from what the AI agent knows by itself, or write a choice that no person confirmed. The reason: a choice with no memory behind it is the agent's taste, nobody can check it, and every builder after it would build on a guess.
- Never: change the architecture's words in place. An update replaces what held before and keeps it. The reason: work already built on the old architecture must still be explainable.

### Guiding rules
- Once for the project, not once in each slice. The reason: most design is the same for every slice, so deciding it again in each one costs time, and slices that decide alone end up different.
- Phoenix memory first, then research. Each choice is proposed from Phoenix memory's architecture and technology learnings, matched to the project's conditions: its stage, its users, its team size, how often it deploys and the quality levels in the product profile. Only when Phoenix memory has no answer does the agent research the choice, and it raises what it found as a memory update for a person to approve. A choice is never made from what the AI agent knows by itself. The reason: a learning in memory has been checked and anyone can read it, while the agent's own knowledge can be neither checked nor read back.
- Research is used only after a person approves it. Until then the choice stays open, with no default, and the work goes on. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- What the project's code already shows is described as it is. When the project already has code, its current architecture and technology are read from the code and its settings and proposed as they are. The reason: an architecture that contradicts the running code sends every builder into a rewrite nobody asked for.
- Each proposal names its source: a Phoenix memory learning, an approved memory update or a file of the project. The reason: a person can then check each choice without a search.
- The product profile sizes each choice. A choice must meet the quality levels the profile commits to, without going far beyond them. The reason: a small internal tool does not need the architecture of a public payments product, and a public product cannot run on the architecture of a throwaway.
- The technology of a part names a real product and its version, not a kind of product. The reason: a builder told "a relational database" must still choose one, and the next builder may choose another.
- A person confirms each choice and each update. The reason: the architecture binds every builder in the project, so an agent never sets it alone.
- A missing choice is a gap, not a stop. The builder goes by the project's code and memory and names what it chose, and the gap stays on record so a later step knows it was skipped, not forgotten. The reason: the Spec → Design business intent blocks no work, and each design can run at any time.
- The architecture is kept where every agent looks first. Agents gather context from the project's code and the project's own memory, Garura memory, before Phoenix memory, and the product model is part of Garura memory. The reason: an architecture that builders do not find is no architecture. Not decided: the place in the model, because the model has no kind for the project's architecture.

## Sources
- The one line the product owner agreed on 2026-11-03: "The technology and architecture for the whole project are set here and can evolve. Nothing blocks on them."
- The product owner on 2026-11-07, on the first drafts: "set the project arch will include the tech parts too.", "this should be reflected as updating arch. as the project changes.", "we need to read the phoenix memory and if not found then go about research."
- The capability list the product owner locked on 2026-11-03: "Seed the memory for the lenses: The memory each design lens needs is seeded, ready for slices to use. It is part of initialize, not a play.", "Lock the design: A design is locked before agents take over. This is the only gate", "Use the lenses on each slice: Each slice is designed through the lenses", "Manage ADRs: Decisions on how the project is built are recorded closely as they're made"
- .garura/product/product-os/intents/bi-2.md: "The project's positions are set for the whole project: technology and architecture, surfaces, deployment and environments.", "Without shared positions, each builder invents its own answer.", "Each position is written down and can change later.", "Block other work. Each design can be run at any time."
- .garura/product/product-os/software-delivery-planning/domain.md: "Its job comes before the build"
- docs/adr/028-agentic-lifecycle-five-loops.md: "These set the project's guidelines, rules, and guardrails. Every slice follows them.", "re-deriving it per slice is ceremony", "A skipped area can be built up later at runtime by the execution trinities"
- docs/adr/028-agentic-lifecycle-five-loops.md, Open question 3: "Where do the project-wide design outputs live in the product model?", "The product model is to be rebuilt as an ontology"
- docs/adr/014-three-axis-project-profiling.md: "Rejected because architecture is product-scoped, not epic-scoped.", "An architecture chosen per-epic would risk inconsistency across epics."
- docs/adr/050-the-retired-intent-epic-pipeline-is-deleted.md: "the `derive-*` skills for capability selection, design patterns, logical architecture, NFR spec, physical architecture, quality vision, systems inventory and tech stack"
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md: "Locking a design is a governance check. Initialize, seeding memory and upgrade are engine things, not plays."
- core/components/plays/shape-architecture-lens/SKILL.md: "waits for the rebuild of the design plays after the shaping loop (#855, ADR 053)"
- core/components/plays/shape-architecture-lens/reference/ice.md: "The stack is a material choice recorded as a slice-level decision the whole product", "it is sized by the profile box, not invented per slice", "reuse the product decision if one exists", "never the model's taste"
- core/components/skills/find-architecture-learnings/SKILL.md: "Search the empirical Knowledge Base for the best-fit architecture and technology learnings given a product's conditions."
- core/components/skills/research-domain-context/SKILL.md: "Research vertical domain knowledge via web when LTM is insufficient"
- core/components/skills/author-technical-approach/SKILL.md: "e.g., `.garura/product/architecture/`", "NEVER use vague technology references", "ALWAYS include rationale for every technology selection"
- core/components/agents/tech-designer.md: "if LOCKED, use as authoritative (stop descending). If DRAFT, use as advisory (continue descending)."
- core/components/plays/record-decision/SKILL.md: "a product decision, a `decision.yaml` record", "Only a person accepts an ADR."
- core/tools/memory/GUIDE.md: "Never answer from what you already know, and never from the web, without a", "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
- core/tools/memory/GUIDE.md: "An update always goes to the issue's short-term memory, and it is used only after a person", "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
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
