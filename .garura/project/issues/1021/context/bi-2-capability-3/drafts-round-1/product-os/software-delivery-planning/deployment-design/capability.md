# Capability: Deployment design

## Directional intent
How the product gets deployed is designed.
The deployment design says where the product runs, how a change gets to the people who use it, and how a release goes live and is taken back, written down with the reason for each choice. It holds:
- the platform the product runs on, and where each part of the architecture runs and in what form, with what the platform offers and how it behaves. For example, a part may run as a container on a managed service, and the screens as files served from a content network; a platform may start more copies as use grows, stop when nobody uses the product, or move users from one version to the next a few at a time;
- the path a change takes to the people who use it: the environments it passes through in order, the checks it must pass before each step, and who says yes before the last step. An environment is one place where a copy of the product runs, such as a test copy or the live product;
- how a release goes live, such as to everyone at once or to one group of users first, and how the team knows it came up healthy;
- how a release is rolled back, which means taken back to the version before, such as by turning the new behaviour off, and how stored data survives it;
- where secrets, such as passwords and keys, are kept, and where the settings that differ between environments are kept;
- what running the product costs at a few sizes of use, what drives the cost, and the other platforms weighed;
- the rules every release must keep, each following from what the platform offers or from what the product profile commits to;
- for each part, its reason, its source and the person who confirmed it.

The design is set once for the project, before the slices are designed, and it is updated as the project changes. A slice is an ordered group of features that one person can test end to end on one surface. Each slice is then built and released the way the design says, and does not choose its own way. A product that keeps nothing running, such as a command a person installs, still has a deployment design: it says how the product reaches the people who use it, or that there is nothing to deploy, with the reason.
An agent proposes each choice, and a person confirms it. The agent looks first at what the project already holds, its code, its settings and its own records, then at Garura memory, then at Phoenix memory. Garura memory is the memory Garura keeps for the project, and it holds the product model, the shared map of the product that people and agents read. Phoenix memory is the shared memory on the machine that every project draws from; its architecture and technology learnings say which platform and which way of releasing fit a product in given conditions, and when each is outgrown. Only when none of them has an answer does the agent research it. It then raises what it found as a memory update, a proposed addition to memory, and a person approves it before it is used. Nothing comes from what the AI agent knows by itself.
It matters to software delivery planning because that domain prepares the work before agents build it. Without one deployment design for the project, each builder invents how its part is shipped, and a release can go out that nobody can take back.

Features:
- Design how the product is deployed, released and rolled back (fn-design-deployment): sets where the product runs and in what form, the path a change takes to the people who use it, how a release goes live and is rolled back, how stored data survives it, where secrets are kept and what running it costs, each with its reason, so every release follows the same design.
- Update the deployment design as the project changes (fn-update-deployment): when the project outgrows its deployment design, or a part of it must change, a person confirms an update, and what held before stays readable with why it changed.

What is not built yet:
- Neither feature is built. Nothing designs how the product is deployed for the whole project.
- As built, each slice's own run design decides it alone. The design play for a slice's run is stale and waits for a rebuild. For its own slice, it records how a release goes live and is rolled back, how stored data changes, how the slice is built, tested and shipped, what running it costs on the chosen cloud with the alternatives weighed, and its environments, one at a time. It reuses a choice an earlier slice recorded as a decision, so the first slice would set the platform for the whole product.
- The plays that bring a slice up for a person to accept, and that deploy it to a cloud environment, are stale. They do only what the slice's run design declares, and never deploy to the live product. They leave the live product to continuous delivery from the main line of the code, which is not built.
- An older skill wrote a hosting platform for each part inside a whole-project architecture. No play calls it.
- Reading memory first exists only in parts. Phoenix memory has learnings for deploying and releasing in some conditions: one deployable unit on one cloud, releasing to a known group of users, agents, content sites, web front ends and a throwaway tool. Nothing joins them into one step for the project, and memory has nothing for a product that is installed rather than kept running.
- The product model has no kind for the deployment design. An older decision left the place of project-wide design to the model's ontology, the agreed list of the kinds of things a product is made of, and the ontology has not answered it.
- No work for this capability is planned in the tracker.

### Benefit hypothesis
- Who it serves: the devops engineer, who decides how the product is deployed, released and rolled back; the product owner, who asked that every builder work from the same design; and the agents that build, release and deliver each slice.
- What we believe: every release of the product reaches its people the same way and can be taken back, if the work stands on these rules:
  - How the product is deployed is decided once for the project, not again in each slice.
  - Each choice comes from the project's code or memory, or from research a person approved into memory, and a person confirms it.
  - The design gives every part of the architecture a place to run, and says how every release is rolled back without losing stored data.
  - The design is updated as the project changes, and what held before stays readable with why it changed.
  - Nothing waits for the design.
- How we will know: two slices released at different times go through the same path to the same platform in the same way, each difference between them traces to the design or to a recorded update of it, and a release that went wrong is rolled back the way the design says.
  - This is not tested today, because nothing designs deployment for the whole project.

### Boundary (In / Out / Never)
- In: designing where the product runs: the platform, and where each part of the architecture runs and in what form, with what the platform offers and how it behaves.
- In: designing the path a change takes to the people who use it, how a release goes live and is checked, how it is rolled back, how stored data survives it, where secrets and settings are kept, what running the product costs, and the rules every release must keep.
- In: updating the deployment design as the project changes, keeping what held before and why it changed.
- Out: which environments the project has, how many, and how each is set up, such as its data, its size, its network and who can reach it. Environment setup owns it. This capability names the order in which a change passes through them and the checks between them.
- Out: the parts of the system and what each is built with, such as its language, its framework, its data store and their versions. Design the technology and architecture owns it. This capability says where each of those parts runs and how it gets there. A change of platform can call for an update of the architecture, and the other way round.
- Out: the project's surfaces, the places where people or other systems use the product. Manage surfaces owns them. This capability makes each declared surface reachable the way its kind needs, such as an address for a browser page or an install for a command line.
- Out: designing how one slice runs, such as the switches on its risky changes and the changes it makes to stored data. The run lens of Use the lenses on each slice (Design → Code) owns it, and follows this design. A lens is one view of a slice's design, such as its screens or its architecture.
- Out: building and testing each change together, and delivering accepted changes to their environments. Continuous integration and Continuous delivery (Validation → Run) own them, and carry out what is designed here.
- Out: bringing one slice up for a person to accept, and deploying a slice to an environment. The plays that do it read the design and never change it.
- Out: making the files that carry out the design, such as container files, pipeline files and infrastructure files. Build the work makes them, from work items.
- Out: the product profile, the record of the product's shape and the quality levels it commits to, such as how reliable it must be. Specify the product sets it. This capability reads its quality levels and its compliance needs to size each choice, and never writes them.
- Out: writing the decision record behind each choice, accepting it and keeping its history. A decision record says what was decided, why, and what else was weighed. Manage ADRs (Orchestration) owns the records; this capability decides what each choice says and hands it over.
- Out: putting the memory that fits the deployment design into the project. Seed the memory for the lenses, a part of the project set-up step (initialize), owns it.
- Out: moving an approved memory update into Phoenix memory. A memory update goes to the project's short-term memory, and moving it up is a promotion a person makes on purpose, outside this work.
- Out: locking the design before agents take over. Lock the design owns the lock, the only gate.
- Never: block work on a missing choice. The work goes on from the project's code and memory, and the open choice is named. The reason: the Spec → Design business intent must not block on anything except the lock.
- Never: make a choice from what the AI agent knows by itself, or write a choice that no person confirmed. The reason: a release made on an agent's guess is found wrong only when it fails in front of the people who use the product.
- Never: write the value of a secret into the design. The design names only where each secret is kept. The reason: every agent reads the design and it is kept with the project's files, so a secret written there is no longer secret.
- Never: change the design's words in place. An update replaces what held before and keeps it. The reason: releases already made on the old design must still be explainable.

### Guiding rules
- Once for the project, not once in each slice. The reason: most of how a product is deployed is the same for every slice, so deciding it again in each one costs time, and slices that decide alone end up shipped in different ways, with the first slice deciding for every later one.
- The project's memory first, then Garura memory, then Phoenix memory, then research. Each choice is proposed first from what the project holds: its container files, its pipeline files, its deploy scripts and infrastructure files, its hosting settings, and the architecture and surfaces set so far. Then from Garura memory, then from Phoenix memory's architecture and technology learnings, matched to the project's conditions: its architecture, its stage, its users, how often it releases, and the quality levels in the product profile. Only when no memory has an answer does the agent research it, and it raises what it found as a memory update for a person to approve. A choice is never made from what the AI agent knows by itself. The reason: a source in the project or in memory can be checked and read back, while the agent's own knowledge cannot.
- Research is used only after a person approves it. Until then the choice stays open, with no default, and the work goes on. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- What the project already does is described as it is. When the project already deploys, its platform, its pipeline and its way of releasing are read from its files and proposed as they are. The reason: a design that contradicts how the product already ships sends every builder after a release that nobody runs.
- Each proposal names its source: a file of the project, a memory file or an approved memory update. The reason: a person can check each choice without a search, and when a learning in memory changes, the choices built on it can be found.
- Every part of the architecture has a place to run, and every declared surface can be reached the way its kind needs. The reason: a part with no place to run is found only when it fails to start, and a surface nobody can reach cannot be accepted or used.
- The design says how every release is rolled back, and how stored data survives it. The reason: a release with no way back turns one bad change into an outage, and the review already treats a change to stored data with no tested way back as its most serious finding.
- The product profile sizes each choice. The design meets the quality levels and the compliance needs the profile commits to, without going far beyond them. For example, a commitment to be up almost all the time needs a release that can be taken back quickly. The reason: a design below the profile breaks what the product commits to, and one far above it costs every release time and money.
- A person confirms each choice and each update. The reason: the design decides how every release reaches the people who use the product, and putting a release in front of them is never an agent's decision alone.
- A missing choice is a gap, not a stop. The builder goes by the project's code and memory and names what it chose, and the gap stays on record so a later step knows it was skipped, not forgotten. The reason: the business intent's only gate is the lock.
- The design is kept where every agent looks first. Agents gather context from the project's code and the project's own memory, Garura memory, before Phoenix memory, and the product model is part of Garura memory. The reason: a design that builders do not find is no design. Not decided: the place in the model, because the model has no kind for the deployment design.

## Sources
- The one line the product owner agreed on 2026-11-03: "How the product gets deployed is designed."
- The capability list the product owner locked on 2026-11-03: "Environment setup (planned): Which environments exist, how many, and how each is set up.", "Continuous integration (planned): Changes are built and tested together automatically.", "Continuous delivery (planned): Accepted changes are delivered to their environments automatically.", "Seed the memory for the lenses: The memory each design lens needs is seeded, ready for slices to use. It is part of initialize, not a play.", "Lock the design: A design is locked before agents take over. This is the only gate", "Use the lenses on each slice: Each slice is designed through the lenses", "Build the work: Each work item, whether a slice, a feature, a story or a chore, is built end to end from its design.", "Manage ADRs: Decisions on how the project is built are recorded closely as they're made"
- The names agreed with the product owner on 2026-11-03: "/design-env (was /shape-run-lens, covers deployments)"
- .garura/product/product-os/intents/bi-2.md: "The project's positions are set for the whole project: technology and architecture, surfaces, deployment and environments.", "Without shared positions, each builder invents its own answer.", "Each position is written down and can change later.", "Block on anything except the lock, which is the only gate."
- .garura/product/product-os/intents/bi-5.md: "is delivered through CI and CD to its environments"
- .garura/product/product-os/software-delivery-planning/domain.md: "Its job comes before the build"
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "Out: the project's surfaces (Manage surfaces), how the product is deployed and the platform it runs on (Deployment design), and its environments (Environment setup).", "the technology of each part: its language, its framework, its data store or an outside platform it uses, each with its version."
- .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "Out: how the product is deployed (Deployment design), its environments (Environment setup), and locking the design before agents take over (Lock the design, the only gate)."
- docs/adr/028-agentic-lifecycle-five-loops.md: "Most of that design — UX rules, architecture, quality bars, run model — is project-wide, not per-slice", "These set the project's guidelines, rules, and guardrails. Every slice follows them.", "Where do the project-wide design outputs live in the product model?", "The product model is to be rebuilt as an ontology"
- docs/adr/053-shape-scope-and-shape-roadmap-are-dropped.md: "They are marked stale and rebuilt when their stage comes (#855)."
- core/components/plays/shape-run-lens/SKILL.md: "waits for the rebuild of the design plays after the shaping loop (#855, ADR 053)", "the slice-level design (rollout, migrations, config/secrets, CI/CD) once, and ONE environment per call"
- core/components/skills/author-run-lens/SKILL.md: "reuse an existing material decision"
- standards/schemas/product-os/lens/run.yaml, in Phoenix memory: "How the SLICE is deployed and runs.", "blue/green | canary | rolling", "the cloud/provider the cloud environments run on", "MUST match an architecture-lens component name (no dangling target)", "secrets via secrets-manager, NEVER in repo"
- standards/schemas/product-os/grounding/lens/run.md, in Phoenix memory: "how it goes live, and how it's rolled back if needed.", "how it's built, tested, and shipped automatically; what the build gates on."
- GitHub #435 (closed): "TCO is a core run decision."
- core/components/plays/release-increment/SKILL.md: "stops below production (prod stays with CD from main)", "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)"
- core/components/plays/release-epic/SKILL.md: "prod follows from main via CD"
- core/components/agents/environment-operator.md: "Reads the structured run.yaml (its environments[]) as its only infrastructure truth."
- core/components/skills/author-technical-approach/SKILL.md: "For each service/unit: service name, platform (hosting), purpose."
- standards/rules/surface-contract.md, in Phoenix memory: "The deploy record's reachable target must match the surface.", "the command and the env it runs in", "n/a (no deploy surface; launch records the package/import)"
- standards/rules/pr.md, in Phoenix memory: "`Dockerfile*`, `Containerfile*`, `**/{deploy,terraform,helm}/**`", "| OPS-24 | P1 |"
- core/components/skills/check-quality/reference/all-requirements.md: "Database migrations are backwards-compatible or have a tested rollback path"
- standards/rules/gate-config.md, in Phoenix memory: "environment is outward-facing — always requires a human"
- knowledge/_index.md, in Phoenix memory: "`technology/` — specific technology/stack choices and the conditions they fit."
- knowledge/technology/gcp-modular-monolith-runtime.md, in Phoenix memory: "How a modular monolith is deployed and run on GCP — the deploy target, the datastore,"
- knowledge/technology/run-environments-canary-migrations.md, in Phoenix memory: "Release discipline for a modular monolith: fixture-only local, sanitized staging, cohort canary, flags as rollback, additive migrations"
- knowledge/technology/agent-deploy-dev-uat-prod.md, in Phoenix memory: "Agent deployment: dev → uat → prod, promotion gated by an eval suite (not just tests)"
- knowledge/technology/astro-content-sites.md, in Phoenix memory: "stateless Node server on Cloud Run with content on a mounted volume"
- knowledge/technology/frontend-react-nextjs.md, in Phoenix memory: "zero-config vs full control"
- knowledge/architecture/single-user-throwaway.md, in Phoenix memory: "GCP static hosting behind a CDN. No database, no backend, no auth."
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "The profile is THE BOX — the product's committed boundaries.", "regimes the box admits", "The box moves ONLY by an approved decision."
- standards/schemas/product-os/decision.yaml, in Phoenix memory: "accepted decisions are not edited — supersede or amend with a new record"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "None. Every kind a question or a relationship names is defined above."
- .garura/product/product-os/software-delivery-planning/initialize/fn-setup-questions/feature.md: "whether there is a database, personal data, permissions or a running service"
- .garura/product/product-os/software-delivery-planning/initialize/fn-review-rule-groups/feature.md: "because nothing is deployed or kept running for its rules to check"
- core/components/plays/record-decision/SKILL.md: "Only a person accepts an ADR."
- GitHub #608 (open): "How a skipped design area is recorded, so a later loop knows it was skipped and not forgotten."
- core/tools/memory/GUIDE.md: "Never answer from what you already know, and never from the web, without a", "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
- core/tools/memory/GUIDE.md: "An update always goes to the issue's short-term memory, and it is used only after a person", "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
- core/tools/memory/GUIDE.md: "order: `core/memory`, then the product model (`product`)."
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf covers software delivery planning or designing how a software product is deployed.
