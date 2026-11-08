# Deployment design: research and drafts (issue 1021, BI-2 capability 3)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are under `.garura/project/issues/1021/context/bi-2-capability-3/drafts/product-os/software-delivery-planning/deployment-design/`: the capability page and its ICE page, and two feature pages, each with its ICE page. All three ICE pages carry the thin mark, because nothing of the capability is built.

What this run did besides reading:
- It copied what it read from memory through the memory tool into `bi-2-capability-3/memory/`, with `manifest.json`.
- It ran no placement: the domain (software delivery planning) was decided by the product owner.
- It checked each draft page with the structure check, each ICE page with a small shape check, and every quote in a Sources section against its file. The record is `lint.json`.
- It read GitHub issues (no write) to find planned work. The decisions this run made are in `cite-request.json`, for the caller to record with `memory.py cite`.
- The pages were written by hand in short-term memory, as the brief asked and as the first two BI-2 capabilities were. No skill drafts pages of the approved shape into short-term memory.

## What is built, and what is only planned

In one line: nothing designs how the product is deployed for the whole project. What exists is a design of deployment for one slice at a time, in a stale play; two stale plays that carry that slice design out; an older skill nobody calls; a few Phoenix memory learnings; and review rules that read deploy files. Nothing in the tracker plans this capability.

Built, but stale (marked stale and "rebuilt when their stage comes", ADR 053):
- **The design play for a slice's run** (`core/components/plays/shape-run-lens/`, skill `author-run-lens`, stale: "waits for the rebuild of the design plays after the shaping loop (#855, ADR 053)"). For one slice it writes "the slice-level design (rollout, migrations, config/secrets, CI/CD) once, and ONE environment per call". The schema (`standards/schemas/product-os/lens/run.yaml`, Phoenix memory) opens with "How the SLICE is deployed and runs." and holds:
  - how a release goes live: switches on risky changes (`flags`) and a strategy, "blue/green | canary | rolling";
  - `migrations`: how stored data changes;
  - `cicd`: the pipeline;
  - each environment, one per call (local, dev, qa, stage, prod), and for a cloud one: the cloud, the region, where each part runs (each "MUST match an architecture-lens component name (no dangling target)"), managed services, ingress and firewalls, identity, the secrets binding ("secrets via secrets-manager, NEVER in repo") and the deploy command;
  - `tco`, the cost picture, required since #435 (closed: "TCO is a core run decision."): the cloud chosen ("the cloud/provider the cloud environments run on") with its region, reason and alternatives; at least three sizes of use; a monthly range with drivers, exclusions and sensitivity; and cost guardrails.
  - The skill reuses a choice an earlier slice recorded ("reuse an existing material decision", `author-run-lens/SKILL.md`). So, as built, the first slice would set the cloud and the way of releasing for the whole product, which is the failure BI-2 names ("Without shared positions, each builder invents its own answer.").
- **The play that deploys a slice to a cloud environment** (`/release-increment`, stale: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)"), through the `environment-operator` agent and the skill `deploy-cloud-environment` (both stale). It runs only what the slice's run design declares ("Reads the structured run.yaml (its environments[]) as its only infrastructure truth."), needs a person's typed yes before every deploy (pinned: "environment is outward-facing — always requires a human", `standards/rules/gate-config.md`), counts a deploy done only on "a real green, not that the deploy command exited 0.", leaves a failed deploy in its earlier state ("environment is left in its prior state — not half-deployed — the failure is reported"), and "stops below production (prod stays with CD from main)". Continuous delivery from main is not built.
- **The play that brings a slice up for a person to accept** (`/release-epic`, to be named `/validate-uat`, stale), through `deploy-local-environment` (stale), on the slice's local environment; "prod follows from main via CD".
- **The older surface contract** (ADR 022, `standards/rules/surface-contract.md`, Phoenix memory): "The deploy record's reachable target must match the surface." An address for a page or an endpoint, "the command and the env it runs in" for a command line, and for a library "n/a (no deploy surface; launch records the package/import)". ADR 048 removed the epic record it was written for.

Built, and in no flow:
- **An older skill, `author-technical-approach`**, wrote a whole-project architecture whose `deployment` section held, "For each service/unit: service name, platform (hosting), purpose." No play calls it (the approved architecture page says the same of it).

In memory (Phoenix), proposals could be drawn from these, each for its own conditions:
- `knowledge/technology/gcp-modular-monolith-runtime.md`: "How a modular monolith is deployed and run on GCP — the deploy target, the datastore," with environments, gradual rollout, reversible data changes and a security floor; and when it is outgrown.
- `knowledge/technology/run-environments-canary-migrations.md`: "Release discipline for a modular monolith: fixture-only local, sanitized staging, cohort canary, flags as rollback, additive migrations", for a known group of users; and when it is outgrown.
- `knowledge/technology/agent-deploy-dev-uat-prod.md`: "Agent deployment: dev → uat → prod, promotion gated by an eval suite (not just tests)".
- Deploy lines in `knowledge/technology/astro-content-sites.md` ("stateless Node server on Cloud Run with content on a mounted volume"), `knowledge/technology/frontend-react-nextjs.md` ("zero-config vs full control") and `knowledge/architecture/single-user-throwaway.md` ("GCP static hosting behind a CDN. No database, no backend, no auth.").
- Nothing for a product that is installed rather than kept running, such as a command line tool or a library. A search for packages, registries and installers found no learning.

A reader of deployment that is built and live:
- **The review** (`check-change`, through `check-pr-quality`) sorts deploy files as their own kind ("`Dockerfile*`, `Containerfile*`, `**/{deploy,terraform,helm}/**`", `standards/rules/pr.md`) and has a P1 rule for a data change with no way back ("| OPS-24 | P1 |"; its meaning, "Database migrations are backwards-compatible or have a tested rollback path", in `core/components/skills/check-quality/reference/all-requirements.md`). It reads what was built; it has no design to compare with.

Only planned:
- **The agreed capability line**: "Deployment design (planned): How the product gets deployed is designed."
- **BI-2's outcome**: "technology and architecture, surfaces, deployment and environments", and its proof "Each position is written down and can change later."
- **ADR 028**: run is one of the project-wide design areas ("Most of that design — UX rules, architecture, quality bars, run model — is project-wide, not per-slice"). ADR 066 changed other parts of ADR 028 and kept run as a design area.
- **The agreed names**: "/design-env (was /shape-run-lens, covers deployments)". One design play is named for both environments and deployments; where it sits (the whole project or one slice) is not said.
- **Initialize (not built)** asks "whether there is a database, personal data, permissions or a running service", and skips the review's running-service rules "because nothing is deployed or kept running for its rules to check".
- **The tracker**: nothing. The Spec → Design issue has one sub-issue, about surfaces; the Validation → Run issue has none.

Not this capability: installing Garura into a project (Install into a project) is how Garura itself reaches a team, not how a product built with Garura is deployed. Specifying from a deployed site (Specify the product) reads a site someone already deployed.

## The overlaps, and how the line could be drawn

### With "Environment setup" (BI-2, planned: "Which environments exist, how many, and how each is set up.")

As built, both live in one per-slice record: the run design holds the way of releasing and the environments together, and the agreed names give both to one play ("covers deployments").

1. **The path here, the places there.** Environment setup decides which environments exist, how many, in what order, and how each is set up: its data, its size, its network, who can reach it and its own settings. Deployment design decides the platform, where each part runs and in what form, how a change moves through the environments (the checks before each step, who says yes before the last one), how a release goes live and goes back, how stored data survives, where secrets are kept, and the cost. The cost of this line: two capabilities must agree on the list of environments, and the cost picture depends on the environments' number and size, which are set there.
2. **One capability.** Environment setup folds into Deployment design, as the run design and the agreed play name already have it. The cost: reopens the agreed list, which keeps them as two lines.
3. **The platform here, everything per environment there.** Deployment design keeps only the platform and the way of releasing; each environment's cloud, region, parts, network, access and deploy command go to Environment setup. The cost: the path between environments has no clear owner, and where each part runs (the same in every environment) is split by environment.

My lean is option 1. It keeps the agreed list, and matches the split the run design already makes between what is written once for the slice and what is built one environment at a time. The drafts follow it. One line to watch: whether the cost belongs here (the drafts say yes, because it follows from the platform) or with the environments.

### With "Continuous delivery" and "Continuous integration" (Validation → Run, planned)

As built, the stale plays leave the live product to "CD from main", and the run design's `cicd` line holds the pipeline for one slice.

1. **Designed here, run there.** This capability designs the path, the checks before each step, and the way a release goes live and goes back. Continuous integration builds and tests each change together; Continuous delivery delivers each accepted change along the designed path, automatically. The cost: neither is built, so nothing automatic reads the design until they are.
2. **Each runner designs its own.** Deployment design stops at the platform and the form of each part; the pipeline, the promotion and the way a release goes live are designed when Continuous delivery is built. The cost: release and rollback are decided in the Run phase, after the build, against BI-2's outcome that the project's design is set before agents take over.
3. **All here.** Deployment design also carries out each deploy. The cost: takes over two agreed capabilities and the release plays.

My lean is option 1. The drafts follow it.

### With the run lens in "Use the lenses on each slice" (Design → Code)

As built, the run lens designs all of deployment for one slice.

1. **The project here, what one slice adds there.** The project's deployment design is set once here. A slice's run lens says only what the slice adds: the switches on its risky changes, its own data changes, and anything it needs that the design lacks, named as a gap for an update here. The cost: the run lens must be rebuilt to read the project design; it is stale and waits for that rebuild anyway.
2. **Slices first, gathered here.** Each slice keeps designing its own deployment; this capability gathers the first slice's choices as the project's. The cost: the first slice decides for every later one, which is what BI-2 is set against.
3. **No run lens.** Everything is designed here; a slice's switches and data changes go into its stories. The cost: drops a lens the agreed names keep, and a slice's own data changes lose their design home.

My lean is option 1, the same line the two approved BI-2 capabilities drew with their lenses. The drafts follow it.

### With "Design the technology and architecture" (BI-2, approved)

Its approved page has "Out: the project's surfaces (Manage surfaces), how the product is deployed and the platform it runs on (Deployment design), and its environments (Environment setup)." Its In holds "the technology of each part: its language, its framework, its data store or an outside platform it uses".

1. **What each part is built with, there; where it runs and how it gets there, here.** The architecture names the parts and their technology, such as a data store and its version. This capability names where each part runs and in what form, such as that data store as a managed service of the platform, and how each part is shipped. A change of platform can call for an update of the architecture, and the other way round. The cost: "an outside platform it uses" must be read as a platform the product calls, such as a payment service, not one it runs on.
2. **Hosting inside the architecture.** Each part's hosting platform is part of its technology, as the older skill had it. The cost: reopens an approved Out line.
3. **Deployment design becomes a feature of the architecture.** The cost: reopens the approved boundary and the agreed list.

My lean is option 1. The drafts follow it.

### The siblings under BI-2, and other neighbours

No decision asked; the drafts draw these lines:
- **Manage surfaces.** Declares what each surface is; this capability makes each one reachable the way its kind needs (from the older surface contract). Out here.
- **Seed the memory for the lenses (part of initialize).** Initialize's "running service" answer is one input; seeding the memory that fits the deployment design is Out, as on the approved pages.
- **Lock the design.** How the deployment design is updated once the design is locked is left as not decided.
- **Build the work.** Makes the container, pipeline and infrastructure files from work items. Out.
- **Manage ADRs.** Writes and keeps the decision records. Out, as on the approved pages.
- **The release plays** (bring a slice up for acceptance; deploy a slice to an environment). They read the design and never change it. Out.

## The persona

The drafts name **the devops engineer**, because what is built says so: the stale run design names the devops engineer as the one who defines the first environment and the next (its scenarios S1 and S2, `core/components/plays/shape-run-lens/reference/ice.md`), and the stale deploy play names the devops engineer as the one who deploys (its S1, S2 and S8, `core/components/plays/release-increment/reference/ice.md`). The same records name an architect (grounding the choices), a release manager, a security reviewer and an SRE for narrower checks, and the product owner once. The first BI-2 capability named the architect, the second the product owner. The product owner stays in the Benefit hypothesis as the one who asked that every builder work from the same design.

## Features found

Two features, neither built. Each ICE is thin. They follow the shape the product owner asked for on the first two capabilities: one job is one feature, and changing it later is an update as the project changes.

- **Design how the product is deployed, released and rolled back** (fn-design-deployment). Not built. Sets, for the whole project, the platform and where each part runs and in what form, the path a change takes to the people who use it, how a release goes live and is checked, how it is rolled back and how stored data survives it, where secrets and settings are kept, what running it costs, and the rules every release must keep, each with its reason, its source and the person who confirmed it. Sources: the agreed one line; BI-2's outcome; ADR 028's project-wide run area; the agreed name "/design-env (was /shape-run-lens, covers deployments)"; the stale run design and its schema (built for one slice); #435 (the cost picture, closed and built into the schema); the stale deploy play's rules (a person's yes, a real health check, no half-deploy); the older skill's hosting platform for each part; the older surface contract's reachable target for each kind of surface. Release, rollback, data changes, secrets and cost are parts of this one feature, not features of their own, because each depends on the others and the product owner asked that one job stay one feature.
- **Update the deployment design as the project changes** (fn-update-deployment). Not built. When the project outgrows its deployment design, a person confirms an update, and what held before stays readable with why it changed. Sources: BI-2's proof "Each position is written down and can change later."; the run design's re-run, which adds or changes one environment and keeps the rest (built for one slice); the memory learnings' "Evolve when" lines; the decision schema's replace-never-edit rule; initialize's re-run when the project changes (planned).

Candidates not drafted:
- **Estimate what running the product costs.** #435 made it a required part of the run design. Drafted as a part of the design, not a feature of its own, because the cost follows from the platform and the alternatives weighed. The product owner may want it separate.
- **Deploy a slice to an environment, and bring it up for acceptance.** Built (stale), but they carry the design out; they belong with the release plays under Code → Validation and Validation → Run.

## Gaps that matter

- **Nothing designs how the product is deployed for the whole project.** As built, the first slice's run design would set the platform and the way of releasing for every later slice.
- **The model has no place for a deployment design.** ADR 028 deferred where project-wide design lives to the ontology; the ontology (v15) says "None. Every kind a question or a relationship names is defined above." The pages say "Not decided".
- **Memory has nothing for a product that is installed rather than run**, such as a command line tool or a library. Garura itself is one (initialize's model page: "For Garura itself the answers rule out front end, back-end service, database and running service"). The drafts say such a product still gets a design, or "nothing to deploy" with the reason, from the older surface contract and the run template's rule that "none" needs its reason.
- **The live product is left to continuous delivery, which is not built.** The stale deploy play refuses production. Until Continuous delivery is built, nothing carries a release to the live product the way a design says.
- **The memory learnings lean to one cloud.** Three of the six deploy learnings name the same cloud. A proposal for a project on another platform would find little, and would go to research and a memory update. Named, not judged.

## Open points for the product owner

- The line with Environment setup: option 1, 2 or 3. The drafts follow option 1. Within it: does the cost picture sit here or with the environments?
- The line with Continuous delivery and Continuous integration: option 1, 2 or 3. The drafts follow option 1.
- The line with the run lens: option 1, 2 or 3. The drafts follow option 1.
- The line with Design the technology and architecture: option 1, 2 or 3. The drafts follow option 1.
- The persona: the devops engineer, from what is built. The first two capabilities used the architect and the product owner.
- The agreed play name "/design-env (was /shape-run-lens, covers deployments)" names one play for this capability and Environment setup. Whether it designs the project or one slice is not decided; the drafts name no play.
- The capability's name, "Deployment design", is the agreed one and is kept. The other two BI-2 capabilities are named as a job ("Design the technology and architecture", "Manage surfaces").

## Details left out of the pages

Left for an agent that builds these parts to find in the code and memory: the field names of the run design's schema and its cost block; the environment tiers and their numbers; the deploy play's exit codes and target rules; the review's deploy-file patterns and rule IDs; and which memory learnings fit which conditions.

## What this run read from memory

Through the memory tool, copied to `.garura/project/issues/1021/context/bi-2-capability-3/memory/` with `manifest.json`: from Phoenix memory, the run lens schema and its grounding template; the product profile, decision and ontology schemas; the capability and feature grounding templates; the ICE rubric; the surface contract, naming, gate, PR, git and pipeline rules; the knowledge index; the deploy learnings (one deployable unit on one cloud, release discipline, agents, content sites, web front end, throwaway tool) and the modular monolith and microservices learnings. From Garura memory (the product model), the lines read for the decision traces (see `cite-request.json`). No tier was missing.

## Checks

`python3 .claude/skills/discover-capabilities/scripts/lint_grounding.py` on each page: `--kind capability --stage directional` for the capability, `--kind feature` for each feature. All three pages read ok, with no error and no warning, on the first run. The record is `lint.json`.

The structure check has no mode for one ICE page, and its five-word bullet rule does not apply to ICE pages, so a small check in the same record tested each of the three ICE pages: the three sections in order, exactly one Goal, at least one Limit, Fails if and Done means, no more than three Limits and three Fails if (the rubric's limit for a thin ICE), the fixed Read line first, the Context labels in order (Read, Never read, Persona, Scope), a Done means checked by someone other than the doer, the thin mark at the top, and no plan named. All three read ok. Each ICE page has a Never read line, "the value of any secret", drawn from the built rule that the run design never holds a secret's value. No part page has an ICE section.

Every quote in a Sources section was checked against its file, word for word: 133 quotes, none missing. Two did not match on the first pass because the source line breaks inside them; each was replaced by a shorter quote that sits on one line. Two Sources lines carry no quote: the short line beside each feature, and the shelf line. GitHub quotes were checked against the issue texts as read on 2026-11-08.

---

# Addendum, round 2 (2026-11-08): redrafted to the product owner's direction

The round 1 drafts are kept unchanged in `drafts-round-1/`. The drafts in `drafts/` are now round 2. Nothing outside `bi-2-capability-3/` changed.

## The product owner's direction, as given (speech to text)

"First and foremost, this is not a single design play or a single slice play. This is how the entire project is to be run.
- The environment setups: yes, minimum 3: dev, testing, and then pre-production.
- Production never gets set on this, not in the path of the project. We are never touching production.
- Container delivery, container integration: absolutely yes.
- The design and technology architecture needs to get converted into physical architecture.
- Are we running which services?
- How do we test it?
- Is it Kubernetes, Docker, whatnot, and stuff and things?
- Which cloud?
- We need dedicated cartridges for AWS, GCP, and Azure.
- For each one, we need to know what the cost looks like to get this piece figured out, running it across, and whatnot."

How it was read (the coordinator's reading, which the product owner corrects on the pages):
- The capability is how the whole project runs. It is not one play and not per slice. Nothing about how the project runs is designed in a slice; a slice that needs something the design does not cover names it as a gap.
- The path runs through at least three environments, dev, testing and pre-production. This capability designs the path and what each environment is for; Environment setup still sets each one up.
- Production is never in the project's path. The path ends at pre-production.
- "Container delivery, container integration" is read as continuous delivery and continuous integration. The pipeline for both is designed here, and those capabilities carry it out. The pages say "continuous delivery" and "continuous integration".
- The approved architecture is turned here into a physical architecture: which services run, on what container platform (examples only: Docker, Kubernetes, a cloud's own container service), on which cloud, and how each is tested in each environment.
- A dedicated cartridge for each of AWS, GCP and Azure: one ready pack for one cloud that the design reads, with that cloud's services, its container platforms and how to work out its cost. Where it lives and what more it holds is not decided.
- The design shows the cost on each of the three clouds, from each cartridge, so the person can choose the cloud.

## What changed on each page

- **Capability page.**
  - It opens by saying this is how the whole project runs, not one play, and never one slice.
  - It now holds the physical architecture, the path through dev, testing and pre-production, the pipeline for continuous integration and continuous delivery, the tests in each environment, the cost on each cloud and the cartridges, beside release and rollback, stored data, and secrets and settings.
  - There are three features now.
  - "What is not built yet" adds: the stale run design's environments end with production; the stale plays leave production to continuous delivery; the older physical-architecture chain was deleted; memory leans to GCP and has nothing for Azure but its name; memory's learnings end their paths in production; no cartridge exists.
  - New Never: touch production, with his words as the reason.
  - New rules: the path of at least three environments ends at pre-production; the approved architecture comes first; each environment names its tests and a change moves on only when they pass; the cost is shown on all three clouds the same way.
  - The run-lens Out line now says nothing about how the project runs is designed in a slice. Use the lenses on each slice designs the rest of each slice, and a slice names a gap here. The old per-slice switches and data changes are gone from it.
  - New Out line: writing and running the tests belongs to the testing capabilities of Validation → Run, to Test with evals the builder never sees, and to Design for evaluation and testing.
  - The Environment setup Out line now keeps the path, the minimum of three and what each is for here, and leaves setting each one up, and adding more, there.
  - The continuous integration and delivery Out line says they carry the pipeline out "along the path designed here and no further".
  - The Sources gain his words of 2026-11-08 and the new evidence (below).
- **Capability ICE.**
  - The Goal is rewritten around how the whole project runs, with the physical architecture, the path, the pipeline, the tests, the cost on each cloud and the cartridges.
  - A Limit sets the path of at least three environments, ending at pre-production.
  - A Fails if: anything touches production.
  - The third Fails if joins two old ones: a change that runs outside the design, and work that stops for a missing choice.
  - The scenario now maps one product onto three cartridges, chooses a cloud, runs the path and stops before production.
  - A Done means also checks that no step touched production.
  - Still three Limits and three Fails if, still thin, still with the Never read line on secret values.
- **Design how the project runs** (new, `fn-design-how-project-runs`). It replaces "Design how the product is deployed, released and rolled back" (`fn-design-deployment`, deleted from `drafts/`, kept in `drafts-round-1/`). It holds:
  - the physical architecture, the path, the pipeline, the tests in each environment, release and rollback, secrets and settings, the cost on each cloud and the rules every release keeps;
  - how memory learnings that end in production are used (everything up to pre-production, the production step left out);
  - two new not-decided points: where the design is kept, and whether the cost also estimates the live product.

  Its ICE is thin.
- **Prepare a dedicated cartridge for each cloud: AWS, GCP and Azure** (new, `fn-cloud-cartridges`). Not built; thin. Its contents go no further than his words and what the stale run design and memory already hold for a cloud:
  - the services a part maps onto, its container platforms, the managed services and what drives their cost, the secrets store and identity;
  - each entry with its source;
  - the same shape for all three clouds;
  - what a cloud offers, never a project's choice;
  - not decided: where a cartridge lives, what more it holds, and whether other clouds get one.
- **Update the deployment design as the project changes** (`fn-update-deployment`, same folder). It is reworded to cover:
  - the physical architecture, the container platform, a move to another cloud, and a cloud's changed services or prices;
  - a cartridge update carrying through to the costs and parts drawn from it;
  - no update bringing production into the path.

  Its ICE Fails if now names production and stale costs. Still thin.

## New research for round 2

- **Physical architecture, built before.** An older chain drew "logical architecture, NFR spec, physical architecture" for the whole project; it was deleted (ADR 050). Phoenix memory still holds its rule (`standards/rules/architecture.md`, written for the retired `/arch` pipeline and not removed from Phoenix memory): the physical architecture "names the mechanism that delivers each one" of the quality needs, and "physical must name the metrics/logs/traces sink". The page names it as an older rule nothing uses.
- **Container platforms, in memory.** The run schema's runtime examples: "the runtime that runs it (e.g. Cloud Run, ECS, GKE)", and forms of shipping "container | service | function | static | managed". The GCP learning: "Reach for GKE only when you genuinely outgrow Cloud Run". The microservices learning shows each service with "src/ Dockerfile k8s/ README". Nothing chooses a platform for a project; the pages name examples only.
- **Clouds, in memory.** The run schema's provider: "e.g. Google Cloud Platform | AWS | Azure", and a cost picture with one cloud "selected" and "alternatives", each with a "why_not". Learnings: GCP runtime (container service, managed database, managed Kubernetes); AWS appears in the agent platform learning (AWS Bedrock and GCP Vertex AI); Azure appears only as a name in that schema line (and once as a tracker name in the ontology). No cost model for any cloud is in memory; #435 asked for "a KB-learning-gap proposal for the cost model" when memory has none.
- **Testing in each environment, in memory.** The run schema's pipeline: "build -> quality gates -> deploy on green". The release learning's gate list: fixture suites, "a migration dry run, a staging smoke run of the real pipeline", and "a coverage check in prod". The agent learning: "Gate promotion on evals, not just tests." and a uat step that is "The gate before prod." The stale deploy play counts a deploy done only on an independent health check.
- **Production, as built, conflicts with the direction.** The stale deploy play already refuses production ("production is out of scope — refuse it outright (halt)"; the agent: "Production is never your target"). But the stale plays assume production "stays with CD from main", the run schema's tiers end at "4 prod", and the memory learnings put production at the end of their paths (dev → staging → prod; dev → uat → prod). Under the direction, continuous delivery here goes no further than pre-production, and a proposal drawn from those learnings leaves the production step out. Whoever rebuilds the stale plays needs this.
- **Cartridge.** No file in Garura's source, docs, model or memory uses the word. His words are its only source.

## The overlaps, adjusted

- **Environment setup.** Lean 1 kept, with the minimum of three as a rule here. One point is left for the product owner: the agreed Environment setup line says "Which environments exist, how many", and the minimum of three, with their names, now sits here. The drafts keep the path, the minimum and what each environment is for here, and give Environment setup the set-up of each one and any environment beyond the three. A local copy on a builder's machine, which the stale acceptance play uses, is not one of the three; whether it stays is Environment setup's.
- **Continuous integration and continuous delivery.** Designed here, carried out there, and only along the designed path, ending at pre-production. This makes BI-5's "is delivered through CI and CD to its environments" read as the environments up to pre-production.
- **The run lens.** Changed from the round 1 lean. Nothing about how the project runs is designed in a slice; a slice names a gap. A slice's own data changes follow the design's rules and are built by Build the work.
- **Design the technology and architecture.** Lean 1 kept, made sharper: the approved architecture (parts and technology) is turned here into the physical one (services, container platform, cloud). The approved page's Out line already sends "the platform it runs on" here.
- **New: the testing capabilities.** This capability says which tests run in which environment and what a change must pass to move on. The tests themselves are owned by the planned testing capabilities of Validation → Run, by Test with evals the builder never sees, and by Design for evaluation and testing.
- **The agreed play name** "/design-env (was /shape-run-lens, covers deployments)" names one design play. His words, "this is not a single design play", read against one play doing all of it. The drafts name no play.

## New open points for the product owner

- The feature name "Prepare a dedicated cartridge for each cloud: AWS, GCP and Azure": the drafts lead with a verb, as the other features do. His word "cartridge" is kept and explained where it is first used.
- Does the cost on each cloud also estimate running the live product, which the project never touches, or only the environments in the path? The pages leave it not decided.
- Does the minimum of three environments, with their names, now belong here or in Environment setup? The drafts keep it here, as the coordinator read it.
- Where a cartridge lives (for example Phoenix memory, Garura memory or a part the install lays) and what more it holds: not decided.

## Checks, round 2

`python3 .claude/skills/discover-capabilities/scripts/lint_grounding.py` on each page: `--kind capability --stage directional` for the capability, `--kind feature` for each of the three features. The results are in `lint.json` (round 2) and below.

The ICE shape check ran on the four ICE pages: the three sections in order; exactly one Goal; one to three Limits and Fails if; the fixed Read line first; the Context labels in order; a Done means checked by someone other than the doer; the thin mark at the top; no plan named. No part page has an ICE section.

Every quote in a Sources section was checked word for word against its file. The quotes of his words of 2026-11-08 were checked against the direction above, in this file.

Results, round 2:
- Structure check: all four pages read ok, with no error and no warning, on the first run.
- ICE shape check: all four ICE pages read ok. Each has one Goal, three Limits, three Fails if, the fixed Read line and the Never read line on secret values, and each carries the thin mark. The capability ICE has two Done means, each feature ICE one, all checked by someone other than the doer.
- Quotes: 201 quotes checked word for word, none missing. Nothing had to be fixed.
- No page names a plan, a real person or a home-folder path. No page in `drafts/` points to the removed feature `fn-design-deployment`.

---

# Addendum, round 3 (2026-11-08): three small corrections

The round 2 drafts are kept unchanged in `drafts-round-2/`, the round 1 drafts in `drafts-round-1/`. The drafts in `drafts/` are now round 3. Only the lines these three points need changed; every other line is word for word as in round 2.

## The product owner's correction, as given (speech to text)

"each env can be built seperately and managed separately, the underying tech and reusability is imortant but we needed these to be done only a deployment is needed"

The pages quote it with the spelling corrected and one word added in brackets, as the earlier BI-2 pages did with his words: "each env can be built separately and managed separately, the underlying tech and reusability is important but we needed these to be done only [when] a deployment is needed".

## The three points, as the coordinator gave them

1. Each environment is built and managed on its own, apart from the others. They share the same underlying technology, from one design that is reused for every environment, so building one more environment repeats the design rather than inventing it again. An environment is built only when a deployment to it is needed, not all of them up front. Building each environment stays with Environment setup; this capability designs the reusable design each one is built from and says each is built when a deployment needs it.
2. The minimum of three environments and their names (dev, testing, pre-production) move to Environment setup, whose agreed line is "Which environments exist, how many, and how each is set up." This capability keeps the path a change takes through the environments, in order, ending at pre-production, and the rule that nothing ever touches production. Its pages name the three as the environments Environment setup declares.
3. The cost covers running the environments in the path on each of the three clouds. Production is never touched, so its cost is not estimated; that is said once, where the cost is described. The "Not decided" line about the live product's cost is removed.

This closes two round 2 open points: the minimum of three now sits with Environment setup, and the cost covers only the environments in the path.

## The lines that changed, against round 2

Line numbers are those of round 3. Every other line is word for word as in round 2.

- **Capability page** (9 lines changed, 2 added):
  - Line 7, the path bullet: "through the environments Environment setup declares, at least dev, testing and pre-production"; and a new sentence: each environment is built and managed on its own, from one design of its underlying technology reused for every environment, and built only when a deployment to it is needed.
  - Line 12, the cost bullet: "what running the environments in the path costs", and "Production is never touched, so its cost is not estimated".
  - Line 22, the feature's short line: "the path through the environments Environment setup declares, with the one design each environment is built from".
  - Line 40, Benefit hypothesis: "The path runs through the environments Environment setup declares, and ends at pre-production."
  - Line 43, Benefit hypothesis: "The cost of running the environments in the path".
  - Line 51, In: the path through the environments Environment setup declares, and the one design of the underlying technology every environment is built from.
  - Line 54, the Out line on Environment setup: it owns which environments exist, how many and how each is set up, at least dev, testing and pre-production, each built and managed on its own when a deployment needs it, with the minimum of three and their names. This capability holds the path, what each is for, and the one design each is built from.
  - Line 75, the path rule: through the environments Environment setup declares, in order, ending at pre-production; the minimum is gone from its reason.
  - Line 76, new rule: each environment built and managed on its own, from one reused design, only when a deployment needs it; one more environment repeats the design and never invents it again. Its reason is his words.
  - Line 93, new Sources line: his words of the second drafts.
- **Capability ICE** (3 lines): Goal (line 4) and Scope (line 16) say "the environments Environment setup declares" and "the one design each is built from". The path Limit (line 6) says each environment is built and managed on its own from one reused design, only when a deployment needs it. Still three Limits and three Fails if.
- **Design how the project runs** (10 lines changed, 4 added):
  - Line 4, opening: the path through the environments Environment setup declares, with the one design each is built from; "what running the environments in the path costs".
  - Line 8, the path bullet: the same wording as the capability's path bullet.
  - Line 13, the cost bullet: "What running the environments in the path costs", and "Production is never touched, so its cost is not estimated."
  - Line 40, new In: the environments Environment setup declares.
  - Line 47, Out: the cost of running the environments in the path.
  - Line 59: the minimum-of-three rule is replaced by the reuse rule, with his words as its reason.
  - Line 70: the "Not decided" line about the live product's cost is removed.
  - Line 76, acceptance: given the environments Environment setup declares.
  - Line 79, acceptance: the cost of the environments in the path.
  - Lines 81 and 82, two new acceptance criteria: an environment a deployment needs is built from the same design; an environment no deployment needs yet is not built.
  - Line 94, Out of scope: declaring which environments exist and how many, and building each one when a deployment needs it, is Environment setup's, from the design made here.
  - Line 106, new Sources line: his words of the second drafts.
- **Design how the project runs, ICE** (3 lines): Goal (line 4) and Scope (line 16) as on the capability ICE; the path Limit (line 6) gains "each built and managed on its own from one reused design and only when a deployment to it is needed". Still three Limits and three Fails if.
- **Prepare a dedicated cartridge for each cloud** (1 line): line 15, "the cost of running the environments in the path".
- **Cartridges ICE**: unchanged.
- **Update the deployment design** (2 lines): line 5, the path through the environments Environment setup declares, and the one design each environment is built from; line 42, an update keeps the path ending at pre-production and each environment built from the one reused design.
- **Update ICE**: unchanged.

## Checks, round 3

- Structure check: all four pages read ok, with no error and no warning, on the first run.
- ICE shape check: all four ICE pages read ok, each with one Goal, three Limits, three Fails if, the fixed Read line, the Never read line on secret values and the thin mark.
- Quotes: 203 quotes checked word for word, none missing. The two new Sources lines quote his words as corrected above, in this file.
- No page now gives this capability the minimum of three or the names; each names them as the environments Environment setup declares. "Production is never touched, so its cost is not estimated" appears once on the capability page and once on the feature page, where each describes the cost. `drafts-round-1/` and `drafts-round-2/` are untouched.
