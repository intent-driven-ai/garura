# Feature: Set the project's technology

## What it does
It sets what the whole project is built with, its languages, frameworks, data stores and outside platforms, each confirmed by a person with its source and reasons.
- A technology position is one such choice, written down with its version and the reason for it. For example: the language of the server code, the framework of the screens, the database, or a payment platform the product uses. It holds for the whole project.
- It runs before the slices are designed, and again when a new kind of choice comes up, such as the first time the project needs a database. A slice is an ordered group of features that one person can test end to end on one surface.
- For each choice, an agent proposes an answer from what is already known:
  - A project that already has code shows its technology in that code and in its settings. The proposal reads them, so a project written in Java is proposed Java, with the files that show it.
  - A new project has no code. The proposal then comes from memory, where agents look for what is known. Memory holds learnings about which technology fits a product in given conditions, such as its stage, its number of users and the quality levels it commits to, and when to avoid each choice.
  - Where nothing backs a proposal, the choice stays open for the person, with no default.
- The person confirms or corrects each proposal. Only a confirmed choice becomes a position.
- How it meets the capability: these are the technology half of the project's positions. Every slice is built with them, and does not choose its own.

Status: not built. What exists covers only parts of it:
- An older skill writes an architecture for the whole project with a technology section, which names each product and the reason for it. No play calls it, and the files it reads were deleted with the retired planning chain.
- The play that designs architecture is stale and waits for a rebuild. It picks the technology for one slice and records it as a decision that later slices reuse. So, as built, the first slice would set the technology of the whole project.
- The project set-up step, initialize, will ask about the technology standards, tools and frameworks, to choose the memory the project gets. It is not built.

## Inputs / Outputs
- In: the project's code and its settings, when it has any.
- In: the product profile: the product's shape, such as its stage, its users and its surfaces, and the quality levels it commits to, such as how fast, how secure and how reliable it must be.
- In: memory's technology learnings, each with the conditions it fits and when to avoid it.
- In: the person's confirmation or correction of each proposal.
- Out: the proposals, each with the choice, its version, its reasons, its source and the options that lost.
- Out: the confirmed technology positions for the whole project, each with its version, reasons, source and the person who confirmed it.
- Out: each choice left open, named as a gap.

## Rules & behavior
- The project's code comes first. When the project already uses a technology for a job, the proposal for that job is that technology. The reason: a position that contradicts the running code sends every builder into a rewrite nobody asked for. Moving away from it is a change of position (fn-change-position).
- Each proposal names its source: a file of the project, a memory learning or the person's earlier answer. A choice that nothing backs gets no proposal and stays open. The reason: a default looks like a fact, and nobody can judge it.
- The product profile sizes each choice. A choice must meet the quality levels the profile commits to, without going far beyond them. The reason: a small internal tool does not need the technology of a public payments product, and a public product cannot run on the technology of a throwaway.
- Each position names a real product and its version, not a kind of product. The reason: a builder told "a relational database" must still choose one, and the next builder may choose another.
- One position for each job. The reason: two answers to one choice are no position, and two builders would each take a different one.
- A person confirms each position. The reason: a position binds every builder in the project, so an agent never sets one alone.
- Nothing waits for a position. A choice left open does not stop design or build: the builder goes by the project's code and memory and names what it chose, so the open choice can be settled later. The reason: the Spec → Design business intent must not block on anything except the lock.
- Not decided: where the positions are kept, and whether each is a decision record. The model has no kind for a position yet.

## Acceptance criteria
- Given a project whose code is written in Java, when its language is proposed, then the proposal is Java and names the files that show it.
- Given a new project with no code and a memory learning that fits its conditions, when its framework is proposed, then the proposal names the learning, the framework and its version.
- Given a choice that neither the code nor memory backs, when the proposals are shown, then that choice has no proposal and is named as open.
- Given the person corrects a proposal, when the positions are written, then the position holds the person's choice and names the person.
- Given no database position is set, when a slice that stores data is designed and built, then the work goes on and the open choice is named.

## Out of scope
- The shape of the system: its style, its main parts and how they connect. Set the project's architecture (fn-set-architecture) sets it.
- Changing a confirmed position. Change a position as the project evolves (fn-change-position) does it.
- The platform the product runs on and its environments. Deployment design and Environment setup own them.
- The quality levels in the product profile. Specify the product sets them.
- Putting the memory that matches the technology into the project. Seed the memory for the lenses, part of initialize, does it.
- How one slice uses the technology. Use the lenses on each slice designs it.

## Sources
- The one line the product owner agreed on 2026-11-03: "The technology and architecture for the whole project are set here and can evolve. Nothing blocks on them."
- .garura/product/product-os/intents/bi-2.md: "Without shared positions, each builder invents its own answer.", "Block on anything except the lock, which is the only gate."
- docs/adr/028-agentic-lifecycle-five-loops.md: "These set the project's guidelines, rules, and guardrails. Every slice follows them.", "A skipped area can be built up later at runtime by the execution trinities"
- docs/adr/014-three-axis-project-profiling.md: "prepare-architecture → reads profiles      → selects technology stack and quality standards"
- core/components/skills/author-technical-approach/SKILL.md: "Concrete technology selections -- specific named products.", "NEVER use vague technology references -- every component must name a specific product, library, framework, or platform", "ALWAYS include rationale for every technology selection"
- core/components/skills/author-technical-approach/SKILL.md: "`features_yaml_path` — (required) Path to features.yaml"
- docs/adr/050-the-retired-intent-epic-pipeline-is-deleted.md: "the `derive-*` skills for capability selection, design patterns, logical architecture, NFR spec, physical architecture, quality vision, systems inventory and tech stack"
- core/components/plays/shape-architecture-lens/reference/ice.md: "The stack is a material choice recorded as a slice-level decision the whole product", "it is sized by the profile box, not invented per slice", "reuse the product decision if one exists", "never the model's taste"
- core/components/agents/tech-designer.md: "Extract technology markers (e.g., \"Python\", \"React\", \"Postgres\", \"serverless\", \"microservices\")"
- .garura/product/product-os/software-delivery-planning/initialize/fn-setup-questions/feature.md: "the technology standards, the tools and frameworks", "In: what the project already shows, for the proposed answers: its files and its config."
- .garura/product/product-os/software-delivery-planning/initialize/fn-setup-questions/feature.md: "Where nothing backs a proposal, the question carries no proposed answer and the person answers it; there is never a default in place of a source"
- core/components/plays/record-decision/SKILL.md: "Only a person accepts an ADR."
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "The profile is THE BOX — the product's committed boundaries."
- knowledge/_index.md, in Phoenix memory: "`technology/` — specific technology/stack choices and the conditions they fit."
- knowledge/technology/backend-java-spring.md, in Phoenix memory, one of the technology learnings: "Java/Kotlin + Spring Boot: enterprise-grade backend", "### When to choose"
- docs/adr/028-agentic-lifecycle-five-loops.md, Open question 3: "Where do the project-wide design outputs live in the product model?"
