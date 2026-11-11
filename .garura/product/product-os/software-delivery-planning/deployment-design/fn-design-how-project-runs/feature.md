# Feature: Design how the project runs

## What it does
It turns the approved architecture into a physical architecture, which services run, on what container platform and on which cloud, and designs the path a change takes through the environments Environment setup declares, with the one design each environment is built from, the pipeline for continuous integration and continuous delivery, the tests in each environment, how a release goes live and is rolled back, where secrets and settings are kept, and what running the environments in the path costs on each cloud, each with its reason, so every change runs the same way.
- It is the design for the whole project. Nothing about how the project runs is designed in a slice. A slice is an ordered group of features that one person can test end to end on one surface.
- The design holds these parts, each with its reason, its source and the person who confirmed it:
  - The physical architecture. For each part of the approved architecture, the service or services it runs as, the container platform those services run on, and the cloud the project runs on, with what each offers and how it behaves, such as whether it starts more copies as use grows. A container is a packed copy of a service with everything it needs to run. A container platform runs containers, for example Docker on a server, Kubernetes, or a cloud's own service that runs containers.
  - The path. The environments Environment setup declares, at least dev, testing and pre-production, in that order, with what each is for, the checks a change must pass before each step, and who says yes. An environment is one place where a copy of the project runs. Each environment is built and managed on its own, from one design of its underlying technology that is reused for every environment, and it is built only when a deployment to it is needed. The path ends at pre-production, and nothing here touches production, the live product that people use.
  - The pipeline. Continuous integration builds and tests each change together with the rest; continuous delivery takes each accepted change along the path automatically, and no further than pre-production.
  - The tests in each environment. Which tests run in dev, in testing and in pre-production, what a change must pass to move on, and how the team knows a release came up healthy: by a check that it answers, not by the deploy command ending without an error.
  - Release and rollback. How a release goes live in each environment, how it is taken back to the version before, and how stored data survives it.
  - Secrets and settings. Where secrets, such as passwords and keys, are kept, and where the settings that differ between environments are kept. Never their values.
  - The cost on each cloud. What running the environments in the path costs on AWS, on GCP and on Azure, each worked out from that cloud's cartridge for the same sizes of use, such as a first group of users, a wider trial and full use, with what drives each cost and what it leaves out, so a person can choose the cloud. Production is never touched, so its cost is not estimated. A cartridge is one ready pack for one cloud that the design reads (Prepare a dedicated cartridge for each cloud: AWS, GCP and Azure, fn-cloud-cartridges).
  - The rules every release must keep, each following from what the cloud and the platform offer, or from a quality level or a compliance need in the product profile. The product profile is the record of the product's shape and the quality levels it commits to.
- These parts are designed together, in one step, because each depends on the others: the cloud decides which services and container platforms are on offer, the platform decides how a release can go live and be taken back, the way back decides how stored data may change, and the tests decide when a change moves along the path.
- It runs before the slices are designed, once the architecture and the surfaces are known as far as they are. A slice that needs something the design does not cover names it as a gap, and the design is updated (fn-update-deployment).
- For each part, an agent proposes an answer:
  - A project that already runs somewhere shows much of it in its files: its container files, its Kubernetes files, its pipeline files, its deploy scripts, its infrastructure files and its hosting settings. The proposal describes them as they are, with the files that show them.
  - Where the files do not settle it, the proposal comes from what the project's memory holds: the approved architecture, with its parts and their technology; the declared surfaces; the product profile with its quality levels and its compliance needs; and the project's set-up answers, such as whether it keeps a service running, once the set-up step (initialize) is built.
  - Each cloud's services, container platforms and costs come from that cloud's cartridge.
  - Then the proposal comes from Garura memory, the memory Garura keeps for the project, and then from Phoenix memory, the shared memory on the machine that every project draws from. Phoenix memory's architecture and technology learnings are matched to the project's conditions, such as its architecture, its stage and its users. A learning that ends its path in production gives everything up to pre-production, and its production step is left out.
  - Only when no memory has an answer does the agent research it. It raises what it found as a memory update, a proposed addition to memory, for a person to approve. Until the person approves it, that part stays open.
  - Nothing comes from what the AI agent knows by itself. A part that nothing backs stays open, with no default, and the person decides it.
- A product that keeps nothing running, such as a command a person installs on a laptop, still gets a design: how it reaches the people who use it, or that there is nothing to deploy, with the reason.
- The person confirms or corrects each part, gives the reason when the proposal has none, and chooses the cloud with the three costs in view. Only a confirmed part is set.
- How it meets the capability: this is how the whole project's way of running is designed once. Each slice is then built, tested and released the way it says, continuous integration and continuous delivery carry the pipeline out, and the cost on each cloud is known before the cloud is chosen.

Status: not built. What exists covers only parts of it:
- The design play for a slice's run is stale and waits for a rebuild. For its own slice, it records how a release goes live and is rolled back; any change to stored data; how the slice is built, tested and shipped; the cost of running it on one chosen cloud at three sizes of use, with the other clouds weighed; and each environment, one at a time, with the cloud, the region, the service that runs each part, such as a cloud's container service or its managed Kubernetes, the network, the access, where its secrets are kept and the deploy command. Its list of environments ends with production. It places every part of the slice's architecture, never writes a secret's value, and reuses a choice an earlier slice recorded as a decision. Nothing designs these for the whole project.
- The play that deploys a slice to a cloud environment is stale. It does only what the slice's run design declares, needs a person's yes before every deploy, calls a deploy done only when a separate check shows the product answers, and refuses production outright. It leaves production to continuous delivery from the main line of the code, which is not built.
- An older chain of skills drew a physical architecture for the whole project, and was deleted with the retired planning chain. An older rule, still in Phoenix memory, said the physical architecture names how each part meets each quality need, and where its logs and metrics go. Nothing uses it.
- An older skill wrote a hosting platform for each part inside a whole-project architecture. No play calls it.
- An older rule held, for each type of surface, what a reachable deployment of it is: an address for a page or an endpoint, the command and where it runs for a command line, and nothing to deploy for a library. Nothing uses it now.
- Phoenix memory has learnings for running, testing and releasing in some conditions, most of them on GCP. It has a little for AWS, about agents, nothing for Azure beyond its name in a list, and nothing for a product that is installed rather than kept running. No cartridge exists.
- The review checks, in each change, the files that deploy the project, and treats a change to stored data with no tested way back as its most serious finding. It reads what was built; nothing gives it a design to compare with.

## Inputs / Outputs
- In: the project's code and its settings, when it has any: its container files, Kubernetes files, pipeline files, deploy scripts, infrastructure files and hosting settings.
- In: the approved architecture, with its parts and their technology, and the declared surfaces.
- In: the environments Environment setup declares, at least dev, testing and pre-production.
- In: the quality levels and the compliance needs in the product profile, and the project's set-up answers once initialize is built.
- In: the cartridge of each cloud: AWS, GCP and Azure.
- In: Phoenix memory's architecture and technology learnings for running, testing and releasing a product.
- In: a memory update a person approved, when no memory had an answer and the agent researched it.
- In: the person's confirmation or correction of each proposal, and the person's choice of cloud.
- Out: the proposals: each part of the design, with its reasons and its source. The source is a file of the project, a cartridge entry, a memory file or an approved memory update.
- Out: the cost of running the environments in the path on each of the three clouds, side by side, each with what drives it and what it leaves out.
- Out: a memory update for each part the agent researched, waiting for a person's approval.
- Out: the design of how the whole project runs, each part with its source and the person who confirmed it.
- Out: each part left open, named as a gap.

## Rules & behavior
- The project's memory first. Each part is proposed from the project's own memory and code first, then from the cartridges and Garura memory, then from Phoenix memory. The reason: a source in the project or in memory can be checked and read back, so the person can judge the proposal from it.
- Research only when no memory has an answer, and only through a memory update. The agent uses what it found only after a person approves the update. Until then that part stays open, and the work goes on. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- Never from the AI agent's own knowledge. A part with no source behind it is not proposed. The reason: a release made on a guess is found wrong only when it fails, and a cloud chosen on a guess is paid for every month.
- What the project's files already show is described as it is. The reason: a design that contradicts how the project already runs sends every builder after a setup that nobody uses. Moving away from it is an update (fn-update-deployment).
- Each part names its source. The reason: a person can check it without a search, and when a source changes, the choices built on it can be found.
- Every part of the approved architecture runs as a named service, on a named container platform, on the chosen cloud, and every declared surface can be reached the way its kind needs. A part or a surface left without one is named as a gap. The reason: a part with no place to run is found only when it fails to start, and a surface nobody can reach cannot be tested or used.
- Each environment is built and managed on its own, from one design of the underlying technology that is reused for every environment, and only when a deployment to it is needed. Building one more environment repeats the design and never invents it again. The reason, in the product owner's words: "each env can be built separately and managed separately, the underlying tech and reusability is important but we needed these to be done only [when] a deployment is needed".
- The path ends at pre-production. No design, pipeline step or deploy here touches production. The reason, in the product owner's words: "We are never touching production."
- Each environment names the tests that run there, and a change moves to the next one only when they pass. The reason: a path with no checks between its steps carries a broken change as fast as a good one.
- Continuous integration and continuous delivery follow the designed path, and only that path. The reason: a pipeline that took another way would carry changes where nobody designed them to go.
- The design says how every release is rolled back and how stored data survives it. The reason: a release with no way back turns one bad change into an outage, and the review already treats a change to stored data with no tested way back as its most serious finding.
- The cost is worked out on all three clouds, from each cloud's cartridge, the same way and for the same sizes of use, and each cost names what it leaves out. A cloud whose cartridge is not ready has its cost named as open, never guessed. The reason: costs worked out in different ways cannot be set side by side, and a cost that hides what it leaves out looks cheaper than it is.
- The product profile's quality levels and compliance needs size each choice, and the design never changes them. The reason: the profile is the box the product commits to, and only an approved decision moves it.
- Never a secret's value. The design names only where each secret is kept. The reason: every agent reads the design, so a secret written there is no longer secret.
- "Nothing to deploy" is an answer only with its reason. The reason: a design nobody made looks the same as one that found nothing to deploy.
- A person confirms each part and chooses the cloud, and the reason is written beside each. The reason: each choice has reasons, and without them the next person cannot tell a choice from an accident.
- Nothing waits for the design. A slice can be designed and built with a part still open: the work goes on, and the builder names what it chose, so a person can set it later. The reason: the Spec → Design business intent blocks no work, and each design can run at any time.
- Not decided: where the design is kept, because the model has no kind for it.

## Acceptance criteria
- Given a project whose files include a container file and Kubernetes files, when its physical architecture is proposed, then it describes that container platform as it is and names the files that show it.
- Given an approved architecture with three parts, when the physical architecture is proposed, then each part runs as a named service on a named container platform, or is named as a gap.
- Given a declared browser surface and a declared command line, when the design is proposed, then the page has an address and the command line has a way to be installed or run, each with its source.
- Given the environments Environment setup declares, at least dev, testing and pre-production, when the path is proposed, then it holds them in that order, each with what it is for and the tests that run there, and it ends at pre-production.
- Given a proposal or a pipeline step that would deploy to production, when the design is checked, then it is taken out and named.
- Given a Phoenix memory learning whose path ends in production, when the path is proposed from it, then everything up to pre-production is kept, the production step is left out, and the learning is named.
- Given the three cartridges, when the costs are proposed, then the cost of the environments in the path is shown on AWS, GCP and Azure for the same sizes of use, in the same form, each naming its cartridge, what drives it and what it leaves out.
- Given no cartridge for one of the clouds yet, when the costs are proposed, then that cloud's cost is named as open and the work goes on.
- Given a deployment that needs an environment not built yet, when that environment is built, then it is built from the same design of the underlying technology as the others, and nothing of that technology is designed again.
- Given no deployment to an environment is needed yet, when the design is set, then that environment is not built.
- Given a part that nothing in the project, the cartridges or memory backs, when the proposals are made, then the agent researches it, raises a memory update with what it found, and the part stays open until a person approves the update.
- Given a proposal with no source behind it, when the proposals are checked, then it is taken out and the part is named as open.
- Given a draft design that holds a secret's value, when it is checked, then the value is taken out and only where the secret is kept stays.
- Given the person chooses a cloud other than the cheapest, when the design is written, then it holds the person's choice with the reason and names the person.
- Given a command that people install on their laptops and nothing kept running, when the design is proposed, then it says how the command reaches them, or that there is nothing to deploy, with the reason.
- Given a set design, when an agent that did not make it prepares a release to testing, then it can name the services, the container platform, the cloud, the path, the tests, the way back and where the secrets are kept, without asking a person.
- Given no design yet, when a slice is designed, then the work goes on and what is missing is named.

## Out of scope
- Updating the design as the project changes. Update the deployment design as the project changes (fn-update-deployment) does it.
- Preparing each cloud's cartridge. Prepare a dedicated cartridge for each cloud: AWS, GCP and Azure (fn-cloud-cartridges) does it.
- Declaring which environments exist and how many, and building and setting up each one when a deployment to it is needed. Environment setup owns it, from the design made here.
- The parts of the system and what each is built with. Design the technology and architecture owns it.
- Carrying out the pipeline. Continuous integration and Continuous delivery do it, from this design.
- Writing and running the tests. The testing capabilities of Code → Validation and Validation → Run own them, and Write the evals that check the work writes each slice's eval.
- Making the container, Kubernetes, pipeline and infrastructure files. Build the work makes them, from work items.
- Anything in production. The project never touches it.
- The product profile and its quality levels. Specify the product owns them.
- Moving an approved memory update into Phoenix memory. A person does it on purpose, as a promotion, outside this work.

## Sources
- The one line the product owner agreed on 2026-11-03: "How the product gets deployed is designed."
- The product owner on 2026-11-08, on the first drafts: "This is how the entire project is to be run.", "The environment setups: yes, minimum 3: dev, testing, and then pre-production.", "Production never gets set on this, not in the path of the project. We are never touching production.", "Container delivery, container integration: absolutely yes.", "The design and technology architecture needs to get converted into physical architecture.", "Are we running which services?", "How do we test it?", "Is it Kubernetes, Docker, whatnot, and stuff and things?", "Which cloud?", "For each one, we need to know what the cost looks like to get this piece figured out, running it across, and whatnot."
- The product owner on 2026-11-08, on the second drafts: "each env can be built separately and managed separately, the underlying tech and reusability is important but we needed these to be done only [when] a deployment is needed"
- The capability list the product owner locked on 2026-11-03: "Continuous integration (planned): Changes are built and tested together automatically.", "Continuous delivery (planned): Accepted changes are delivered to their environments automatically.", "Test with evals the builder never sees: Each slice is tested end to end by evals its builder can't read."
- .garura/product/product-os/intents/bi-2.md: "Without shared positions, each builder invents its own answer.", "Block other work. Each design can be run at any time."
- docs/adr/028-agentic-lifecycle-five-loops.md: "Most of that design — UX rules, architecture, quality bars, run model — is project-wide, not per-slice"
- core/components/plays/shape-run-lens/SKILL.md: "waits for the rebuild of the design plays after the shaping loop (#855, ADR 053)", "the slice-level design (rollout, migrations, config/secrets, CI/CD) once, and ONE environment per call", "a cloud environment — provider, region, compute, services, firewalls, security, deploy command —"
- core/components/skills/author-run-lens/SKILL.md: "reuse an existing material decision", "is allowed only with its reason."
- standards/schemas/product-os/lens/run.yaml, in Phoenix memory: "order: 0 local, 1 dev, 2 qa, 3 stage, 4 prod.", "e.g. Google Cloud Platform | AWS | Azure", "the runtime that runs it (e.g. Cloud Run, ECS, GKE)", "how it ships — container | service | function | static | managed", "pipeline: build -> quality gates -> deploy on green", "MUST match an architecture-lens component name (no dangling target)", "secrets via secrets-manager, NEVER in repo", "# >=3: at least seed, pilot, expanded", "# what the estimate does NOT cover (HA, heavy logging, ...)"
- standards/schemas/product-os/grounding/lens/run.md, in Phoenix memory: "how it goes live, and how it's rolled back if needed.", "how it's built, tested, and shipped automatically; what the build gates on."
- GitHub #435 (closed): "TCO is a core run decision.", "hyperscaler decision with region and rejected alternatives", "If exact pricing is unavailable, /run still produces a directional range with assumptions and confidence."
- core/components/plays/release-increment/SKILL.md: "stops below production (prod stays with CD from main)"
- core/components/plays/release-increment/reference/ice.md: "production is out of scope — refuse it outright (halt)", "a real green, not that the deploy command exited 0."
- standards/rules/gate-config.md, in Phoenix memory: "environment is outward-facing — always requires a human"
- docs/adr/050-the-retired-intent-epic-pipeline-is-deleted.md: "the `derive-*` skills for capability selection, design patterns, logical architecture, NFR spec, physical architecture, quality vision, systems inventory and tech stack"
- standards/rules/architecture.md, in Phoenix memory: "names the mechanism that delivers each one.", "physical must name the metrics/logs/traces sink"
- core/components/skills/author-technical-approach/SKILL.md: "For each service/unit: service name, platform (hosting), purpose."
- standards/rules/surface-contract.md, in Phoenix memory: "The deploy record's reachable target must match the surface.", "the command and the env it runs in", "n/a (no deploy surface; launch records the package/import)"
- standards/rules/pr.md, in Phoenix memory: "`Dockerfile*`, `Containerfile*`, `**/{deploy,terraform,helm}/**`", "| OPS-24 | P1 |"
- core/components/skills/check-quality/reference/all-requirements.md: "Database migrations are backwards-compatible or have a tested rollback path"
- knowledge/technology/gcp-modular-monolith-runtime.md, in Phoenix memory: "How a modular monolith is deployed and run on GCP — the deploy target, the datastore,", "Reach for GKE only when you genuinely outgrow Cloud Run (long-lived connections, complex", "Environments + rollout."
- knowledge/technology/run-environments-canary-migrations.md, in Phoenix memory: "a migration dry run, a staging smoke run of the real pipeline", "privacy scan on anything exported, and a coverage check in prod."
- knowledge/technology/agent-deploy-dev-uat-prod.md, in Phoenix memory: "Gate promotion on evals, not just tests.", "sample transcripts. The gate before prod."
- knowledge/technology/agent-platform-bedrock-gcp.md, in Phoenix memory: "Agent platform: build on AWS Bedrock and GCP Vertex AI — managed models, tools, and guardrails"
- knowledge/architecture/microservices.md, in Phoenix memory: "src/ Dockerfile k8s/ README"
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "regimes the box admits", "The box moves ONLY by an approved decision."
- .garura/product/product-os/software-delivery-planning/initialize/fn-setup-questions/feature.md: "whether there is a database, personal data, permissions or a running service", "Where nothing backs a proposal, the question carries no proposed answer and the person answers it; there is never a default in place of a source"
- core/tools/memory/GUIDE.md: "Never answer from what you already know, and never from the web, without a", "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- core/tools/memory/GUIDE.md: "Your work goes on while the update waits, unless you cannot go on without it.", "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
