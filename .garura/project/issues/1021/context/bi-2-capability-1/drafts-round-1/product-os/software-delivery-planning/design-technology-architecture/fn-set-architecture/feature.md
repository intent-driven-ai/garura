# Feature: Set the project's architecture

## What it does
It sets the shape of the whole system, its style, its main parts and how they connect, so every slice builds on the same shape.
- An architecture position is one choice about that shape, written down with its reasons. There are three kinds:
  - The style. For example: one deployable unit split into modules with firm borders between them, separate services that each team deploys on its own, or a static site with no server behind it.
  - The main parts and the job of each. A part here is a layer that slices pass through, such as what the person sees, the processes behind it, the business logic and data of each area, and what every area shares. Each part has one job, so two slices never build the same job in two places.
  - How the parts connect, to each other and to outside systems: each seam between two parts and what crosses it.
- Each part is named by its job, not by the product that runs it. A part is "the store of orders", not the name of a database. The product that runs it is a technology position (fn-set-technology).
- For each choice, an agent proposes an answer the same way as for the technology: from the project's code and settings when it has any, else from memory's architecture learnings for a product in the same conditions, such as its stage, its number of users, its team size and how often it deploys. Memory is where agents look for what is known. Where nothing backs a proposal, the choice stays open, with no default.
- The person confirms or corrects each proposal. Only a confirmed choice becomes a position.
- How it meets the capability: these are the architecture half of the project's positions. A slice's own design then picks which of these parts it passes through, end to end, and does not draw a new shape.

Status: not built. What exists covers only parts of it:
- An older skill writes an architecture for the whole project, with its layout of deployable units and how they talk. No play calls it, and the files it reads were deleted with the retired planning chain.
- An older chain of skills drew a logical and a physical architecture for the whole project. It was deleted with the retired planning chain.
- The play that designs architecture is stale and waits for a rebuild. It designs one slice's parts, picking each from what the slice's features talk to, never inventing one. It has no shape for the whole project to pick from.
- Memory holds the learnings to propose from: which style fits a product in given conditions, and which style comes next when it is outgrown.

## Inputs / Outputs
- In: the project's code and its settings, when it has any.
- In: the product profile: the product's shape, such as its stage, its users and its surfaces, and the quality levels it commits to, such as how fast, how reliable and how easy to change it must be.
- In: memory's architecture learnings, each with the conditions it fits and the style that comes after it.
- In: the person's confirmation or correction of each proposal.
- Out: the proposals, each with the choice, its reasons, its source and the options that lost.
- Out: the confirmed architecture positions for the whole project: the style, each main part with its job, and each seam with what crosses it, each with its source and the person who confirmed it.
- Out: each choice left open, named as a gap.

## Rules & behavior
- The project's code comes first. A project already deployed as one unit is proposed that one unit. The reason: a shape that contradicts the running system sends every builder into a rebuild nobody asked for. Moving to a new shape is a change of position (fn-change-position).
- Each proposal names its source, and a choice that nothing backs stays open. The reason: a shape picked by taste looks like a decision, and nobody can judge it.
- The proposal follows memory's learning for the product's conditions. For most new products that learning is one deployable unit with firm module borders, and separate services only once many teams deploy on their own schedules. The reason: a shape too big for the product costs the team in running it, and a shape too small for it fails under load.
- Each part has one job, and each seam says what crosses it. The reason: when two slices need the same job, both use the one part, and the seams are where slices can break each other.
- A part is named by its job, not by a product. The reason: replacing the database product then changes one technology position, not the shape of the system.
- A person confirms each position. The reason: the shape binds every builder in the project, so an agent never sets it alone.
- Nothing waits for a position. A slice can be designed and built with no style set: the builder goes by the project's code and memory and names what it chose, so the open choice can be settled later. The reason: the Spec → Design business intent must not block on anything except the lock.
- Not decided: where the positions are kept, and whether each is a decision record. The model has no kind for a position yet.

## Acceptance criteria
- Given a new internal tool for a small team, when its style is proposed, then the proposal names the memory learning that fits those conditions and gives its reasons.
- Given a project whose code is deployed as one unit, when its style is proposed, then the proposal is that one unit and names the files that show it.
- Given the confirmed architecture positions, when an agent that did not set them reads them, then it can name the style, each main part with its job, and each seam with what crosses it, without asking a person.
- Given a part named after a database product, when the positions are checked, then the part is renamed by its job and the product moves to a technology position.
- Given no style is set, when a slice is designed and built, then the work goes on and the open choice is named.

## Out of scope
- The products that run each part, with their versions. Set the project's technology (fn-set-technology) sets them.
- Changing a confirmed position. Change a position as the project evolves (fn-change-position) does it.
- Which parts one slice passes through, and what crosses each seam for it. Use the lenses on each slice designs it.
- The platform the product runs on and its environments. Deployment design and Environment setup own them.
- The quality levels in the product profile. Specify the product sets them.

## Sources
- The one line the product owner agreed on 2026-11-03: "The technology and architecture for the whole project are set here and can evolve. Nothing blocks on them."
- .garura/product/product-os/intents/bi-2.md: "Without shared positions, each builder invents its own answer.", "Block on anything except the lock, which is the only gate."
- docs/adr/028-agentic-lifecycle-five-loops.md: "These set the project's guidelines, rules, and guardrails. Every slice follows them."
- docs/adr/014-three-axis-project-profiling.md: "Rejected because architecture is product-scoped, not epic-scoped.", "An architecture chosen per-epic would risk inconsistency across epics."
- GitHub #426 (closed): "Decide the unit for architectural traceability deliberately"
- core/components/skills/author-technical-approach/SKILL.md: "`topology` — ASCII diagram or structured description of the system topology showing deployment units and communication patterns", "`deployment_units` — list of named units with responsibility and communication protocol/pattern"
- docs/adr/050-the-retired-intent-epic-pipeline-is-deleted.md: "the `derive-*` skills for capability selection, design patterns, logical architecture, NFR spec, physical architecture, quality vision, systems inventory and tech stack"
- core/components/plays/shape-architecture-lens/reference/ice.md: "is SELECTED, not invented — a system one of the slice's features talks to, or a surface"
- standards/schemas/product-os/lens/architecture.yaml, in Phoenix memory: "A component is a HORIZONTAL platform/tier; a capability is a VERTICAL threading", "experience | process | domain | cross-cutting"
- standards/rules/architecture.md, in Phoenix memory, written for the deleted chain: "System-level decisions (monolith / microservice / serverless) are patterns and live there too.", "swapping Postgres for Dynamo should not require a new architecture.yaml."
- knowledge/_index.md, in Phoenix memory: "`architecture/` — product-condition → best-fit architecture ladders"
- knowledge/architecture/modular-monolith.md, in Phoenix memory: "Modular monolith: one deployment, enforced module boundaries — the default start", "The right starting point for most new products."
- knowledge/architecture/microservices.md, in Phoenix memory: "Microservices: independently deployable services — earned, not started with", "deploy-cadence: independent-per-team"
- knowledge/architecture/single-user-throwaway.md, in Phoenix memory: "Single-user throwaway: static on GCP, no backend"
- core/components/plays/record-decision/SKILL.md: "Only a person accepts an ADR."
- docs/adr/028-agentic-lifecycle-five-loops.md, Open question 3: "Where do the project-wide design outputs live in the product model?"
