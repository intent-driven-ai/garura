# Feature: Prepare a dedicated cartridge for each cloud: AWS, GCP and Azure

## What it does
It prepares one ready cartridge for each of three clouds, AWS, GCP and Azure, so the design of how the project runs can map its physical architecture onto any of them and show what running on each would cost.
- A cartridge, in the product owner's word, is one ready pack for one cloud that the design reads. From his words, and from what is already built and in memory for a cloud, each cartridge holds:
  - the cloud's services that a physical architecture maps onto, for example the services that run a part, the managed data stores, the store for secrets, and the way services prove who they are;
  - its container platforms, for example its own service that runs containers, or its managed Kubernetes. A container platform runs containers, packed copies of a service with everything each needs to run;
  - how to work out what running on that cloud costs: what each service is charged for, so a cost can be worked out for a few sizes of use;
  - for each entry, its source and the person who confirmed it.
- Where a cartridge lives, and what more it holds, is not decided.
- The three cartridges answer the same questions in the same shape. So the design can map one physical architecture onto each cloud and set the three costs side by side.
- Each entry is drawn from memory first: the project's own records for that cloud, such as infrastructure files that already use its services, then Garura memory, the memory Garura keeps for the project, then Phoenix memory, the shared memory on the machine that every project draws from, and its learnings for that cloud. Only when memory has no answer is the entry researched. The agent raises what it found as a memory update, a proposed addition to memory, and a person approves it before it is used. Nothing comes from what the AI agent knows by itself.
- An entry that nothing backs stays open, named as a gap. A person confirms each cartridge before the design reads it as confirmed.
- A cartridge holds what one cloud offers and how its cost is worked out, never a project's choice. Choosing the cloud, and mapping the project onto it, is the design's (Design how the project runs, fn-design-how-project-runs).
- How it meets the capability: the design shows the cost of running the project on each of the three clouds and maps the physical architecture onto the chosen one. The cartridges are what it reads to do that.

Status: not built. What exists covers only parts of it:
- No cartridge exists. Nothing in Garura or in memory uses the word; it is the product owner's new idea, given on 2026-11-08.
- What is built for a cloud sits inside the stale run design of one slice. For a cloud environment it names the cloud, its region, the service that runs each part, such as a cloud's container service or its managed Kubernetes, the managed services with what drives their cost, and the store for secrets. Its cost picture names one chosen cloud and the others weighed. Nothing gathers this cloud by cloud.
- Phoenix memory holds learnings for running on GCP: a container service and a managed database, and when to move to its managed Kubernetes. For AWS it holds a learning about building agents on its agent platform. For Azure it holds nothing beyond its name in a list of clouds.
- An older issue asked the run design to give a rough cost range with its assumptions when exact prices are not known, and to raise a memory gap when memory holds no cost pattern. The run design's cost picture was built from it, for one slice.

## Inputs / Outputs
- In: the project's own records for a cloud, when it has any, such as infrastructure files that already use that cloud's services.
- In: Garura memory and Phoenix memory's learnings for each cloud.
- In: a memory update a person approved, when no memory had an answer and the agent researched an entry.
- In: the person's confirmation of each cartridge.
- Out: one cartridge for each of AWS, GCP and Azure, in the same shape, each entry with its source and the person who confirmed it.
- Out: a memory update for each entry the agent researched, waiting for a person's approval.
- Out: each entry left open, named as a gap.

## Rules & behavior
- Memory first. Each entry comes from the project's own records, then Garura memory, then Phoenix memory. The reason: a source in the project or in memory can be checked and read back.
- Research only when no memory has an answer, and only through a memory update. The agent uses what it found only after a person approves it. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- Never from the AI agent's own knowledge. An entry with no source behind it is not written. The reason: a price or a service an agent assumed is found wrong only after a cloud was chosen on it.
- The same questions in the same shape for all three clouds. The reason: costs worked out in different ways cannot be set side by side, and the person choosing a cloud needs the three side by side.
- What a cloud offers, never a project's choice. The reason: the choice needs the project's conditions, which the design holds, and a cartridge that chose would decide before the person sees the three costs.
- Each entry names its source. The reason: a cloud's services and prices change, and an entry can be checked, and updated, only when its source is known.
- A missing cartridge or entry is a gap, not a stop. The design names that cloud's cost as open, and the work goes on. The reason: the Spec → Design business intent must not block on anything except the lock.
- A person confirms each cartridge. The reason: the design reads the cartridges as the facts behind the choice of cloud, so an unchecked cartridge would make that choice on unchecked facts.
- Never the value of a secret, such as a cloud account's key. The reason: a cartridge is read by every design that maps onto its cloud.
- Not decided: where a cartridge lives, what more it holds, and whether other clouds get one.

## Acceptance criteria
- Given the three cartridges, when the design maps one physical architecture onto each, then every part of it finds a service and a container platform on each cloud, or is named as a gap on that cloud.
- Given the three cartridges, when a cost is worked out for the same sizes of use, then it comes out in the same form for each cloud, and the three can be set side by side.
- Given a Phoenix memory learning for running on a cloud, when that cloud's cartridge is prepared, then each entry the learning backs names the learning.
- Given a cloud that memory holds nothing for, when its cartridge is prepared, then the agent researches it, raises a memory update with what it found, and the entries stay open until a person approves the update.
- Given an entry with no source behind it, when the cartridge is checked, then it is taken out and named as open.
- Given a cartridge entry that names one service as the one a project must use, when the cartridge is checked, then the choice is taken out and left to the design.
- Given a cartridge that no person confirmed, when the design reads it, then its costs are shown as not confirmed.
- Given no cartridge for one cloud yet, when the design is made, then the work goes on and that cloud's cost is named as open.

## Out of scope
- Choosing the cloud and mapping the project's physical architecture onto it. Design how the project runs (fn-design-how-project-runs) does it.
- Updating a cartridge when a cloud's services or prices change. Update the deployment design as the project changes (fn-update-deployment) does it.
- Setting up an environment on a cloud. Environment setup owns it.
- Deploying anything to a cloud. Continuous delivery and the release plays do it, from the design.
- Moving an approved memory update into Phoenix memory. A person does it on purpose, as a promotion, outside this work.

## Sources
- The product owner on 2026-11-08, on the first drafts: "We need dedicated cartridges for AWS, GCP, and Azure.", "For each one, we need to know what the cost looks like to get this piece figured out, running it across, and whatnot.", "Is it Kubernetes, Docker, whatnot, and stuff and things?", "Which cloud?"
- standards/schemas/product-os/lens/run.yaml, in Phoenix memory: "e.g. Google Cloud Platform | AWS | Azure", "the runtime that runs it (e.g. Cloud Run, ECS, GKE)", "the managed service (e.g. Cloud SQL, Memorystore)", "cost_driver: string", "identity: string     # service accounts / roles / workload identity", "secrets: string      # secrets-manager binding — never in repo", "the cloud/provider the cloud environments run on", "# >=1 considered-and-rejected"
- GitHub #435 (closed): "TCO is a core run decision.", "If exact pricing is unavailable, /run still produces a directional range with assumptions and confidence.", "If KB has no matching cost pattern, /run creates a KB-learning-gap proposal for the cost model."
- knowledge/technology/gcp-modular-monolith-runtime.md, in Phoenix memory: "Modular-monolith runtime on GCP: Cloud Run + Cloud SQL Postgres, cache only when it earns it, secure by default", "Reach for GKE only when you genuinely outgrow Cloud Run (long-lived connections, complex"
- knowledge/technology/agent-platform-bedrock-gcp.md, in Phoenix memory: "Agent platform: build on AWS Bedrock and GCP Vertex AI — managed models, tools, and guardrails"
- .garura/product/product-os/intents/bi-2.md: "Block on anything except the lock, which is the only gate."
- core/tools/memory/GUIDE.md: "Never answer from what you already know, and never from the web, without a", "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- core/tools/memory/GUIDE.md: "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
