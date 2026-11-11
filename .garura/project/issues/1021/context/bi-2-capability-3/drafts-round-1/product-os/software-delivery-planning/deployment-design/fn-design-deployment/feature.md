# Feature: Design how the product is deployed, released and rolled back

## What it does
It sets where the product runs and in what form, the path a change takes to the people who use it, how a release goes live and is rolled back, how stored data survives it, where secrets are kept and what running it costs, each with its reason, so every release follows the same design.
- The design holds these parts, each with its reason, its source and the person who confirmed it:
  - The platform: where the product runs, and where each part of the architecture runs and in what form. For example: a container on a managed service, files served from a content network, a function that runs only when it is called, or a package a person installs. With what the platform offers and how it behaves, for example whether it starts more copies as use grows, whether it stops when nobody uses the product, and whether it can move users from one version to the next a few at a time.
  - The path: the environments a change passes through, in order, the checks it must pass before each step, and who says yes before the last step. An environment is one place where a copy of the product runs, such as a test copy or the live product.
  - The release: how a new version goes live, for example to everyone at once, to one group of users first, or by switching from the old copy to a new one; and how the team knows it came up healthy, by a check that it answers, not by the deploy command ending without an error.
  - The rollback: how a release is taken back to the version before, for example by turning the new behaviour off or by starting the earlier version again, and how fast.
  - Stored data: how a change to stored data goes out with a release, so that a rollback loses nothing.
  - Secrets and settings: where secrets, such as passwords and keys, are kept, and where the settings that differ between environments are kept. Never their values.
  - The cost: what running the product costs at a few sizes of use, such as a first group of users, a wider trial and full use; what drives the cost; and the other platforms weighed, with why each lost.
  - The rules every release must keep, each following from what the platform offers or from a quality level or a compliance need in the product profile. The product profile is the record of the product's shape and the quality levels it commits to.
- These parts are designed together, in one step, because each depends on the others: the platform decides how a release can go live and be taken back, and the way back decides how stored data may change.
- It runs before the slices are designed, once the architecture and the surfaces are known as far as they are, and again when the project needs something the design does not cover yet. A slice is an ordered group of features that one person can test end to end on one surface.
- For each part, an agent proposes an answer:
  - A project that already deploys shows much of it in its files: its container files, its pipeline files, its deploy scripts, its infrastructure files and its hosting settings. The proposal describes them as they are, with the files that show them.
  - Where the files do not settle it, the proposal comes from what the project's memory holds: the architecture set so far, with its parts and their technology; the declared surfaces; the product profile with its quality levels and its compliance needs; and the project's set-up answers, such as whether it keeps a service running, once the set-up step (initialize) is built.
  - Then the proposal comes from Garura memory, the memory Garura keeps for the project, and then from Phoenix memory, the shared memory on the machine that every project draws from. Phoenix memory's architecture and technology learnings are matched to the project's conditions, such as its architecture, its stage and its users.
  - Only when no memory has an answer does the agent research it. It raises what it found as a memory update, a proposed addition to memory, for a person to approve. Until the person approves it, that part stays open.
  - Nothing comes from what the AI agent knows by itself. A part that nothing backs stays open, with no default, and the person decides it.
- A product that keeps nothing running, such as a command a person installs on a laptop, still gets a design: how it reaches the people who use it, or that there is nothing to deploy, with the reason.
- The person confirms or corrects each part, and gives the reason when the proposal has none. Only a confirmed part is set.
- How it meets the capability: this is how the product's deployment is designed once for the whole project. Each slice is then built and released the way it says, and the steps that deliver and deploy the work carry it out.

Status: not built. What exists covers only parts of it:
- The design play for a slice's run is stale and waits for a rebuild. For its own slice, it records how a release goes live and is rolled back, with the switches it uses; any change to stored data; how the slice is built, tested and shipped; the cost of running it on the chosen cloud at three sizes of use, with the alternatives weighed; and each environment, one at a time, with the cloud, the region, where each part runs, the network, the access, where its secrets are kept and the deploy command. It places every part of the slice's architecture, never writes a secret's value, and reuses a choice an earlier slice recorded as a decision. Nothing designs these for the whole project first.
- The play that deploys a slice to a cloud environment is stale. It does only what the slice's run design declares, needs a person's yes before every deploy, calls a deploy done only when a separate check shows the product answers, leaves a failed deploy in its earlier state, and never deploys to the live product.
- An older skill wrote a hosting platform for each part inside a whole-project architecture. No play calls it.
- An older rule held, for each type of surface, what a reachable deployment of it is: an address for a page or an endpoint, the command and where it runs for a command line, and nothing to deploy for a library. It was written for a work record that no longer exists, and nothing uses it now.
- Phoenix memory has learnings for deploying and releasing in some conditions: one deployable unit on one cloud, releasing to a known group of users, agents, content sites, web front ends and a throwaway tool. It has none for a product that is installed rather than kept running. Nothing joins them into one design for the project.
- The review checks, in each change, the files that deploy the product, and treats a change to stored data with no tested way back as its most serious finding. It reads what was built; nothing gives it a design to compare with.

## Inputs / Outputs
- In: the project's code and its settings, when it has any: its container files, pipeline files, deploy scripts, infrastructure files and hosting settings.
- In: the architecture set so far, with its parts and their technology, and the declared surfaces.
- In: the quality levels and the compliance needs in the product profile, and the project's set-up answers once initialize is built.
- In: Phoenix memory's architecture and technology learnings for deploying, releasing and running a product.
- In: a memory update a person approved, when no memory had an answer and the agent researched it.
- In: the person's confirmation or correction of each proposal.
- Out: the proposals: each part of the design, with its reasons and its source. The source is a file of the project, a memory file or an approved memory update.
- Out: a memory update for each part the agent researched, waiting for a person's approval.
- Out: the deployment design of the whole project, each part with its source and the person who confirmed it.
- Out: each part left open, named as a gap.

## Rules & behavior
- The project's memory first. Each part is proposed from the project's own memory and code first, then from Garura memory, then from Phoenix memory. The reason: a source in the project or in memory can be checked and read back, so the person can judge the proposal from it.
- Research only when no memory has an answer, and only through a memory update. The agent uses what it found only after a person approves the update. Until then that part stays open, and the work goes on. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- Never from the AI agent's own knowledge. A part with no source behind it is not proposed. The reason: a release made on a guess is found wrong only when it fails in front of the people who use the product.
- What the project's files already show is described as it is. The reason: a design that contradicts how the product already ships sends every builder after a release that nobody runs. Moving away from it is an update (fn-update-deployment).
- Each part names its source. The reason: a person can check it without a search, and when a learning in memory changes, the choices built on it can be found.
- Every part of the architecture has a place to run, and every declared surface can be reached the way its kind needs. A part or a surface left without one is named as a gap. The reason: a part with no place to run is found only when it fails to start, and a surface nobody can reach cannot be accepted or used.
- The design says how every release is rolled back and how stored data survives it. The reason: a release with no way back turns one bad change into an outage, and the review already treats a change to stored data with no tested way back as its most serious finding.
- The design says how the team knows a release is healthy: a check that the product answers. The reason: a deploy command can end without an error while the product does not answer.
- The product profile's quality levels and compliance needs size each choice, and the design never changes them. The reason: the profile is the box the product commits to, and only an approved decision moves it.
- Never a secret's value. The design names only where each secret is kept. The reason: every agent reads the design, so a secret written there is no longer secret.
- The cost names the sizes of use it was worked out for, and what it leaves out. The reason: a cost with no sizes behind it cannot be checked, and one that hides what it leaves out looks cheaper than it is.
- "Nothing to deploy" is an answer only with its reason. The reason: a design nobody made looks the same as one that found nothing to deploy.
- A person confirms each part, and the reason is written beside it. The reason: each choice has reasons, and without them the next person cannot tell a choice from an accident.
- Nothing waits for the design. A slice can be designed and built with a part still open: the work goes on, and the builder names what it chose, so a person can set it later. The reason: the Spec → Design business intent must not block on anything except the lock.
- Not decided: where the deployment design is kept, because the model has no kind for it.

## Acceptance criteria
- Given a project whose files include a container file and a pipeline that deploys it to a managed service, when its deployment is proposed, then the proposal describes that platform and that path and names the files that show them.
- Given an architecture with three parts, when the design is proposed, then each part has a place to run and a form, or is named as a gap.
- Given a declared browser surface and a declared command line, when the design is proposed, then the page has an address and the command line has a way to be installed or run, each with its source.
- Given a Phoenix memory learning that fits the project's architecture and stage, when the release and the rollback are proposed, then each part the learning backs names the learning.
- Given a part that nothing in the project or in memory backs, when the proposals are made, then the agent researches it, raises a memory update with what it found, and the part stays open until a person approves the update.
- Given a proposal with no source behind it, when the proposals are checked, then it is taken out and the part is named as open.
- Given a product profile that commits to a high level of reliability, when the release and the rollback are proposed, then they say how fast a release can be taken back, and they are checked against that level.
- Given a draft design that holds a secret's value, when it is checked, then the value is taken out and only where the secret is kept stays.
- Given the person corrects the proposed platform, when the design is written, then it holds the person's answer with the reason and names the person.
- Given a command that people install on their laptops and nothing kept running, when the design is proposed, then it says how the command reaches them, or that there is nothing to deploy, with the reason.
- Given a set design, when an agent that did not make it prepares a release, then it can name the platform, the path, the checks, the way back and where the secrets are kept, without asking a person.
- Given no deployment design yet, when a slice is designed, then the work goes on and what is missing is named.

## Out of scope
- Updating the design as the project changes. Update the deployment design as the project changes (fn-update-deployment) does it.
- Which environments exist, how many, and how each is set up. Environment setup owns it.
- The parts of the system and what each is built with. Design the technology and architecture owns it.
- How one slice runs, such as the switches on its risky changes and its own changes to stored data. The run lens of Use the lenses on each slice owns it, following this design.
- Building and testing each change, delivering accepted changes, and deploying a slice to an environment. Continuous integration, Continuous delivery and the release plays do it, from this design.
- Making the container, pipeline and infrastructure files. Build the work makes them, from work items.
- The product profile and its quality levels. Specify the product owns them.
- Moving an approved memory update into Phoenix memory. A person does it on purpose, as a promotion, outside this work.

## Sources
- The one line the product owner agreed on 2026-11-03: "How the product gets deployed is designed."
- .garura/product/product-os/intents/bi-2.md: "Without shared positions, each builder invents its own answer.", "Block on anything except the lock, which is the only gate."
- docs/adr/028-agentic-lifecycle-five-loops.md: "Most of that design — UX rules, architecture, quality bars, run model — is project-wide, not per-slice"
- The names agreed with the product owner on 2026-11-03: "/design-env (was /shape-run-lens, covers deployments)"
- core/components/plays/shape-run-lens/SKILL.md: "waits for the rebuild of the design plays after the shaping loop (#855, ADR 053)", "the slice-level design (rollout, migrations, config/secrets, CI/CD) once, and ONE environment per call", "a cloud environment — provider, region, compute, services, firewalls, security, deploy command —"
- core/components/skills/author-run-lens/SKILL.md: "reuse an existing material decision", "is allowed only with its reason."
- standards/schemas/product-os/lens/run.yaml, in Phoenix memory: "blue/green | canary | rolling", "MUST match an architecture-lens component name (no dangling target)", "secrets via secrets-manager, NEVER in repo", "the cloud/provider the cloud environments run on", "# >=3: at least seed, pilot, expanded", "# what the estimate does NOT cover (HA, heavy logging, ...)"
- standards/schemas/product-os/grounding/lens/run.md, in Phoenix memory: "how it goes live, and how it's rolled back if needed.", "any data or schema moves the slice requires"
- GitHub #435 (closed): "TCO is a core run decision.", "Validator fails if no user/load simulation is provided."
- core/components/plays/release-increment/SKILL.md: "stops below production (prod stays with CD from main)"
- core/components/plays/release-increment/reference/ice.md: "a real green, not that the deploy command exited 0.", "environment is left in its prior state — not half-deployed — the failure is reported"
- standards/rules/gate-config.md, in Phoenix memory: "environment is outward-facing — always requires a human"
- core/components/skills/author-technical-approach/SKILL.md: "For each service/unit: service name, platform (hosting), purpose."
- standards/rules/surface-contract.md, in Phoenix memory: "The deploy record's reachable target must match the surface.", "the command and the env it runs in", "n/a (no deploy surface; launch records the package/import)"
- standards/rules/pr.md, in Phoenix memory: "`Dockerfile*`, `Containerfile*`, `**/{deploy,terraform,helm}/**`", "| OPS-24 | P1 |"
- core/components/skills/check-quality/reference/all-requirements.md: "Database migrations are backwards-compatible or have a tested rollback path"
- knowledge/technology/gcp-modular-monolith-runtime.md, in Phoenix memory: "How a modular monolith is deployed and run on GCP — the deploy target, the datastore,"
- knowledge/technology/run-environments-canary-migrations.md, in Phoenix memory: "Release discipline for a modular monolith: fixture-only local, sanitized staging, cohort canary, flags as rollback, additive migrations"
- knowledge/technology/agent-deploy-dev-uat-prod.md, in Phoenix memory: "Agent deployment: dev → uat → prod, promotion gated by an eval suite (not just tests)"
- knowledge/architecture/single-user-throwaway.md, in Phoenix memory: "GCP static hosting behind a CDN. No database, no backend, no auth."
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "regimes the box admits", "The box moves ONLY by an approved decision."
- .garura/product/product-os/software-delivery-planning/initialize/fn-setup-questions/feature.md: "whether there is a database, personal data, permissions or a running service", "Where nothing backs a proposal, the question carries no proposed answer and the person answers it; there is never a default in place of a source"
- core/tools/memory/GUIDE.md: "Never answer from what you already know, and never from the web, without a", "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- core/tools/memory/GUIDE.md: "Your work goes on while the update waits, unless you cannot go on without it.", "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
