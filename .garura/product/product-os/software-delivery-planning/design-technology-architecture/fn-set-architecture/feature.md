# Feature: Set the project's architecture

## What it does
It sets the shape of the whole system and what it is built with, its style, its main parts and how they connect, and the technology of each part with its version, so every slice builds on the same architecture.
- The project's architecture holds these choices, each written down with its reason:
  - The style. For example: one deployable unit split into modules with firm borders between them, separate services that each team deploys on its own, or a static site with no server behind it.
  - The main parts and the job of each. A part here is a layer that slices pass through, such as what the person sees, the processes behind it, the business logic and data of each area, and what every area shares. Each part has one job, so two slices never build the same job in two places.
  - How the parts connect, to each other and to outside systems: each seam between two parts and what crosses it.
  - The technology of each part: its language, its framework, its data store, or an outside platform it uses, such as a payment platform, each with its version.
- A part is named by its job, not by the product that runs it: "the store of orders", not the name of a database. Its technology is written beside it.
- It runs before the slices are designed, and again when a new kind of choice comes up, such as the first time the project needs a database. A slice is an ordered group of features that one person can test end to end on one surface.
- For each choice, an agent proposes an answer:
  - A project that already has code shows its current architecture and technology in that code and in its settings. The proposal describes them as they are, with the files that show them, so a project written in Java and deployed as one unit is proposed Java and one unit.
  - Every choice the code does not settle comes from Phoenix memory first. Phoenix memory is the shared memory on the machine that every project draws from. Its architecture and technology learnings say which shape and which technology fit a product in given conditions, such as its stage, its number of users, its team size, how often it deploys and the quality levels it commits to, and when to avoid each.
  - Only when Phoenix memory has no answer does the agent research the choice. It raises what it found as a memory update, a proposed addition to memory, for a person to approve. Until the person approves it, the choice stays open.
  - No choice comes from what the AI agent knows by itself. A choice that nothing backs stays open, with no default.
- The person confirms or corrects each proposal. Only a confirmed choice becomes part of the project's architecture.
- How it meets the capability: this is how the project's architecture, with its technology, is set once for the whole project. A slice's own design then picks which of these parts it passes through, end to end, with their technology, and does not draw its own shape or choose its own technology.

Status: not built. What exists covers only parts of it:
- An older skill writes an architecture for the whole project: its layout of deployable units, how they talk, and a technology section that names each product and the reason for it. No play calls it, and the files it reads were deleted with the retired planning chain.
- An older chain of skills drew a logical and a physical architecture and a technology stack for the whole project. It was deleted with the retired planning chain.
- The play that designs architecture is stale and waits for a rebuild. It designs one slice: it picks each part from what the slice's features talk to, never inventing one, and it picks the slice's technology and records it as a decision that later slices reuse. Its choices must rest on a memory learning or a recorded gap in memory, never on the AI model's taste. As built, the first slice would set the technology of the whole project.
- Reading memory first and then researching exists in parts. A stale skill searches memory's learnings for the best fit for a product's conditions. A skill researches on the web when memory has too little, for the agent that designs technical changes. The memory tool raises a memory update for a person to approve. Nothing joins them into one step for the architecture.
- The project set-up step, initialize, will ask about the technology standards, tools and frameworks, to choose the memory the project gets. It is not built.

## Inputs / Outputs
- In: Phoenix memory's architecture and technology learnings, each with the conditions it fits, when to avoid it and the choice that comes after it.
- In: the project's code and its settings, when it has any.
- In: the product profile: the product's shape, such as its stage, its users and its surfaces, and the quality levels it commits to, such as how fast, how secure, how reliable and how easy to change it must be.
- In: a memory update a person approved, when Phoenix memory had no answer and the agent researched the choice.
- In: the person's confirmation or correction of each proposal.
- Out: the proposals, each with the choice, its version when it is technology, its reasons, its source and the options that lost. The source is a Phoenix memory learning, an approved memory update or a file of the project.
- Out: a memory update for each choice the agent researched, waiting for a person's approval.
- Out: the confirmed architecture of the whole project: the style, each main part with its job and its technology with the version, and each seam with what crosses it, each with its source and the person who confirmed it.
- Out: each choice left open, named as a gap.

## Rules & behavior
- Phoenix memory first. Each choice the code does not settle is proposed from Phoenix memory's architecture and technology learnings, matched to the project's conditions. The reason: a learning in memory has been checked and anyone can read it, so the person can judge the proposal from its source.
- Research only when Phoenix memory has no answer, and only through a memory update. The agent researches the choice, raises what it found as a memory update, and uses it only after a person approves it. Until then the choice stays open, and the work goes on. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- Never from the AI agent's own knowledge. A choice with no Phoenix memory learning and no approved memory update behind it is not proposed. The reason: the agent's own knowledge can be neither checked nor read back, and every builder after it would build on a guess.
- What the project's code already shows is described as it is. When the project already uses a technology or a shape for a job, the proposal for that job is what the code uses. The reason: an architecture that contradicts the running code sends every builder into a rewrite nobody asked for. Moving away from it is an update (fn-update-architecture).
- Each proposal names its source. The reason: a person can then check each choice without a search.
- The product profile sizes each choice, the shape and the technology alike. A choice must meet the quality levels the profile commits to, without going far beyond them. The reason: a small internal tool does not need the architecture of a public payments product, and a public product cannot run on the architecture of a throwaway.
- Each part has one job, and each seam says what crosses it. The reason: when two slices need the same job, both use the one part, and the seams are where slices can break each other.
- A part is named by its job, and its technology names a real product and its version, not a kind of product. The reason: replacing the database product then changes one line of technology, not the shape of the system; and a builder told "a relational database" must still choose one, and the next builder may choose another.
- One answer for each job. The reason: two answers to one choice are no answer, and two builders would each take a different one.
- A person confirms each choice. The reason: the architecture binds every builder in the project, so an agent never sets it alone.
- Nothing waits for the architecture. A slice can be designed and built with a choice still open: the builder goes by the project's code and memory and names what it chose, so the open choice can be settled later. The reason: the Spec → Design business intent blocks no work, and each design can run at any time.
- Not decided: where the project's architecture is kept, and whether each choice is a decision record. The model has no kind for it yet.

## Acceptance criteria
- Given a new internal tool for a small team, when its style is proposed, then the proposal names the Phoenix memory learning that fits those conditions and gives its reasons.
- Given a new project and a Phoenix memory learning that fits its conditions, when its framework is proposed, then the proposal names the learning, the framework and its version.
- Given a choice that Phoenix memory has no learning for, when the proposals are made, then the agent researches it, raises a memory update with what it found, and the choice stays open until a person approves the update.
- Given a proposal with no Phoenix memory learning, no approved memory update and no project file behind it, when the proposals are checked, then it is taken out and the choice is named as open.
- Given a project whose code is written in Java and deployed as one unit, when its architecture is proposed, then the proposal is Java and one unit, and names the files that show them.
- Given the person corrects a proposal, when the architecture is written, then it holds the person's choice and names the person.
- Given the confirmed architecture, when an agent that did not set it reads it, then it can name the style, each main part with its job and its technology, and each seam with what crosses it, without asking a person.
- Given a part named after a database product, when the architecture is checked, then the part is renamed by its job and the product is written as its technology.
- Given no database is chosen, when a slice that stores data is designed and built, then the work goes on and the open choice is named.

## Out of scope
- Updating the confirmed architecture as the project changes. Update the architecture as the project changes (fn-update-architecture) does it.
- Which parts one slice passes through, and what crosses each seam for it. Designing each slice (Design → Code) designs it.
- The platform the product runs on and its environments. Deployment design and Environment setup own them.
- The quality levels in the product profile. Specify the product sets them.
- Putting the memory that matches the architecture into the project. It belongs to the play that starts the build, not to the product model.
- Moving an approved memory update into Phoenix memory. A person does it on purpose, as a promotion, outside this work.

## Sources
- The one line the product owner agreed on 2026-11-03: "The technology and architecture for the whole project are set here and can evolve. Nothing blocks on them."
- The product owner on 2026-11-07, on the first drafts: "set the project arch will include the tech parts too.", "we need to read the phoenix memory and if not found then go about research."
- .garura/product/product-os/intents/bi-2.md: "Without shared positions, each builder invents its own answer.", "Block other work. Each design can be run at any time."
- docs/adr/028-agentic-lifecycle-five-loops.md: "These set the project's guidelines, rules, and guardrails. Every slice follows them.", "A skipped area can be built up later at runtime by the execution trinities"
- docs/adr/014-three-axis-project-profiling.md: "Rejected because architecture is product-scoped, not epic-scoped.", "An architecture chosen per-epic would risk inconsistency across epics."
- docs/adr/014-three-axis-project-profiling.md: "prepare-architecture → reads profiles      → selects technology stack and quality standards"
- GitHub #426 (closed): "Decide the unit for architectural traceability deliberately"
- core/components/skills/author-technical-approach/SKILL.md: "`topology` — ASCII diagram or structured description of the system topology showing deployment units and communication patterns", "`deployment_units` — list of named units with responsibility and communication protocol/pattern"
- core/components/skills/author-technical-approach/SKILL.md: "Concrete technology selections -- specific named products.", "NEVER use vague technology references -- every component must name a specific product, library, framework, or platform", "ALWAYS include rationale for every technology selection"
- core/components/skills/author-technical-approach/SKILL.md: "`features_yaml_path` — (required) Path to features.yaml"
- docs/adr/050-the-retired-intent-epic-pipeline-is-deleted.md: "the `derive-*` skills for capability selection, design patterns, logical architecture, NFR spec, physical architecture, quality vision, systems inventory and tech stack"
- core/components/plays/shape-architecture-lens/reference/ice.md: "is SELECTED, not invented — a system one of the slice's features talks to, or a surface", "The stack is a material choice recorded as a slice-level decision the whole product", "it is sized by the profile box, not invented per slice", "reuse the product decision if one exists"
- core/components/plays/shape-architecture-lens/reference/ice.md: "best-fit learning on the KB's architecture/technology shelf (matched via find-architecture-learnings) or to a", "recorded KB-learning-gap proposal — never the model's taste.", "F8 — An architecture choice rests on neither a matched KB learning nor a recorded proposal."
- core/components/skills/find-architecture-learnings/SKILL.md: "Search the empirical Knowledge Base for the best-fit architecture and technology learnings given a product's conditions."
- core/components/skills/research-domain-context/SKILL.md: "Research vertical domain knowledge via web when LTM is insufficient"
- core/components/agents/tech-designer.md: "When LTM is insufficient, invoke `research-domain-context` skill:", "Extract technology markers (e.g., \"Python\", \"React\", \"Postgres\", \"serverless\", \"microservices\")"
- core/tools/memory/GUIDE.md: "Never answer from what you already know, and never from the web, without a", "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- core/tools/memory/GUIDE.md: "Your work goes on while the update waits, unless you cannot go on without it.", "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
- .garura/product/product-os/software-delivery-planning/initialize/fn-setup-questions/feature.md: "the technology standards, the tools and frameworks", "In: what the project already shows, for the proposed answers: its files and its config."
- .garura/product/product-os/software-delivery-planning/initialize/fn-setup-questions/feature.md: "Where nothing backs a proposal, the question carries no proposed answer and the person answers it; there is never a default in place of a source"
- core/components/plays/record-decision/SKILL.md: "Only a person accepts an ADR."
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "The profile is THE BOX — the product's committed boundaries."
- standards/schemas/product-os/lens/architecture.yaml, in Phoenix memory: "A component is a HORIZONTAL platform/tier; a capability is a VERTICAL threading", "experience | process | domain | cross-cutting"
- standards/rules/architecture.md, in Phoenix memory, written for the deleted chain: "System-level decisions (monolith / microservice / serverless) are patterns and live there too.", "swapping Postgres for Dynamo should not require a new architecture.yaml."
- knowledge/_index.md, in Phoenix memory: "`architecture/` — product-condition → best-fit architecture ladders", "`technology/` — specific technology/stack choices and the conditions they fit."
- knowledge/architecture/modular-monolith.md, in Phoenix memory: "Modular monolith: one deployment, enforced module boundaries — the default start", "The right starting point for most new products."
- knowledge/architecture/microservices.md, in Phoenix memory: "Microservices: independently deployable services — earned, not started with", "deploy-cadence: independent-per-team"
- knowledge/architecture/single-user-throwaway.md, in Phoenix memory: "Single-user throwaway: static on GCP, no backend"
- knowledge/technology/backend-java-spring.md, in Phoenix memory, one of the technology learnings: "Java/Kotlin + Spring Boot: enterprise-grade backend", "### When to choose"
- docs/adr/028-agentic-lifecycle-five-loops.md, Open question 3: "Where do the project-wide design outputs live in the product model?"
