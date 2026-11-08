# Environment setup: research and drafts (issue 1021, BI-2 capability 4)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are under `.garura/project/issues/1021/context/bi-2-capability-4/drafts/product-os/software-delivery-planning/environment-setup/`: the capability page and its ICE page, and three feature pages, each with its ICE page. All four ICE pages carry the thin mark, because nothing of the capability is built for the whole project.

What this run did besides reading:
- It copied what it read from memory through the memory tool into `bi-2-capability-4/memory/`, with `manifest.json`.
- It ran no placement: the domain (software delivery planning) was decided by the product owner.
- It read GitHub issues (no write) to find planned work.
- It checked each page with the structure check, each ICE page with a small shape check, and every quote in a Sources section against its file. The record is `lint.json`.
- The decisions this run made from memory are in `cite-request.json`, for the caller to record with `memory.py cite` (recording them writes outside `bi-2-capability-4/`).
- The pages were written by hand in short-term memory, as the brief asked and as the first three BI-2 capabilities were. No skill drafts pages of the approved shape into short-term memory: the page skills (`enrich-capability-ice`, `enrich-grounding`) write only into the live model. That missing skill is named here, not worked around further.

## What is built, and what is only planned

In one line: nothing declares or builds the environments of the whole project. What exists is a record of each environment inside one slice's run design, in a stale play; a stale agent with two stale skills that bring one environment up, check it, and take it down; two stale plays that use them; review rules that read files about environments; and a few Phoenix memory learnings. Nothing in the tracker plans this capability.

Built, but stale (marked stale and "rebuilt when their stage comes", ADR 053):
- **The design play for a slice's run** (`core/components/plays/shape-run-lens/`, skill `author-run-lens`; stale: "waits for the rebuild of the design plays after the shaping loop (#855, ADR 053)"). It writes "the slice-level design (rollout, migrations, config/secrets, CI/CD) once, and ONE environment per call", and "Incremental: re-run to add or edit an environment; the rest are preserved." Its schema (`standards/schemas/product-os/lens/run.yaml`, Phoenix memory) opens with "How the SLICE is deployed and runs." For each environment it records:
  - a name from a fixed list, "unique — local | dev | qa | stage | prod", in a fixed order, "order: 0 local, 1 dev, 2 qa, 3 stage, 4 prod." (the resolver: "known tiers: local=0, dev=1, qa=2, stage=3, prod=4"). So the list ends with production, and has no testing or pre-production;
  - whether it is a builder's machine (local) or a cloud;
  - its own settings, "per-env config; secrets via secrets-manager, NEVER in repo";
  - for a local one, "how to bring it up locally (command / compose file)" and an "optional — test-data seed step";
  - for a cloud one, its provider and region, where each part runs with its size ("optional — instances / size / scaling"), managed services with what drives their cost, its network ("public | internal | load-balanced", "ingress/egress rules — ports, sources, allow/deny"), identity ("service accounts / roles / workload identity"), the secrets binding, its controls and its deploy command.
  - Its check (`validate_run.py`) needs, for a cloud one, the provider, region, compute, networking and security, and refuses a secret's value in the record.
- **The agent that operates environments** (`core/components/agents/environment-operator.md`, "domain: environments", stale: "waits for the rebuild of /release-epic and /release-increment (#855); only stale plays dispatch it"). It "brings an increment up on ONE environment the run lens declares", "proves it reachable, captures the deploy record, and tears it down when asked". If the run design "doesn't declare it, you don't build it." On a failed attempt it must "leave the environment in its prior state". It never may "Declare done without reachability evidence in the record", and never "Print, log, or store a secret value". "Production is never your target".
  - Its skill for a builder's machine (`deploy-local-environment`, stale) brings the copy up from its declared command, fills it with test data when declared ("test data when the local environment declares a seed step."), records how to take it down ("Record the teardown path with the deploy."), keeps only test users' credentials ("credentials only for seeded TEST users."), and "Tears the environment down when asked (the reverse contract)."
  - Its skill for a cloud (`deploy-cloud-environment`, stale) runs the declared deploy command, reads secrets only from their store, checks health on its own ("Do NOT trust the deploy command's exit code."), and on failure leaves things as they were ("it never auto-rolls-back"). It also has a take-down mode ("(tear down a prior deploy of this env)").
- **The play that brings a slice up for a person to accept** (`/release-epic`, to be named `/validate-uat`; stale). It halts unless the slice's run design declares a local copy ("Run lens `run.yaml` declares a local environment"), brings that copy up only for the acceptance walk, and takes it down after: "done; the environment is not needed for the close. (On any abort, teardown still runs.)" This is the only built place where an environment exists only while something needs it.
- **The play that deploys a slice to a cloud environment** (`/release-increment`, stale). It picks the lowest cloud environment the run design declares, or a named one; halts "if no cloud environment is defined at all, halt with NO_CLOUD_ENV (4)"; refuses production ("production is out of scope — refuse it outright (halt)"); and needs a person's yes before every deploy, under the pinned gate rule "environment is outward-facing — always requires a human" (`standards/rules/gate-config.md`, Phoenix memory). It "stops below production (prod stays with CD from main)".

Built and live, a reader:
- **The review** (`check-change`, through `check-pr-quality`) has rules that fire on files about environments (`standards/rules/pr.md`, Phoenix memory), with their meaning in `core/components/skills/check-quality/reference/all-requirements.md`:
  - files under `seed`, `fixtures` or `test-data` ("`path:**/{seed,fixtures,test-data}/**`") against "Non-production environments use masked or synthetic data — no production PII in staging/dev";
  - an example settings file ("`path:.env.example,README.md,docs/setup/**`") against "All required environment variables are documented";
  - pipeline files against "Environment promotion strategy is defined (staging → production gate)".
  - It reads what was built. Nothing gives it declared environments to compare with.

Live, but a different kind of place (not this capability):
- **The test project of an eval.** A slice's eval runs a play "in the test project" (`standards/schemas/eval/steps-command-line.yaml`, Phoenix memory: "a command in the test project and gives it the scripted answers."), set up by the usage guide the build delivers. The runner is "the eval runner (later)". For a product that keeps nothing running, such as Garura itself, this is the nearest thing to a testing environment; the pages name it only in a Not decided line.
- **The git worktree** that `start-change` can set up is a builder's working copy of one change. The product does not run there as a deployment.

In memory (Phoenix), proposals could be drawn from these, each for its own conditions:
- `knowledge/technology/run-environments-canary-migrations.md`: "Three environments, each with a distinct data stance.": local with "fixtures only. No real data on a developer machine, ever; fixtures double", staging with "sanitized production-shaped data", prod with real data; the reason, to keep real data out of the "two places it leaks from most — laptops and test environments."
- `knowledge/technology/agent-deploy-dev-uat-prod.md`: dev, where you "build and iterate on prompts, tools, orchestration; cheap models OK while", uat, "The gate before prod.", and prod.
- `knowledge/technology/gcp-modular-monolith-runtime.md`: "Promote dev → staging → prod.", and "Lock ingress and ports to the minimum the service actually needs".
- The run lens template's example dev environment (`standards/schemas/product-os/grounding/lens/run.md`): "No public ingress yet — a firewall rule", "allows the team VPN only.", "dev is deliberately locked down and cheap because it exists" to prove the path, not to serve users.
- Every learning's ladder ends in production, and none names testing or pre-production. Under the product owner's rule, a proposal drawn from them uses what they say for the other environments and leaves production out.
- Nothing on building an environment only when a deployment needs it, or on taking one down. Nothing on infrastructure files beyond a folder layout in the microservices learning. Nothing on the environments of a product that keeps nothing running.
- Not this capability: the content-management shelf's "Roles & environments — who can do what, across dev/stage/prod." is a feature of a content product a team might build, not the project's own environments.
- Garura memory (the project tier) holds nothing on environments beyond the approved model pages. No tier was missing.

Only planned:
- **The agreed capability line**: "Environment setup (planned): Which environments exist, how many, and how each is set up."
- **BI-2's outcome**: "technology and architecture, surfaces, deployment and environments", and its proof "Each position is written down and can change later." **BI-5**: "is delivered through CI and CD to its environments".
- **The approved Deployment design**, which already gives this capability its job: "Out: which environments exist, how many, and how each is set up: at least dev, testing and pre-production, each built and managed on its own when a deployment to it is needed, with its data, its size, its network and who can reach it." and "Environment setup owns it, with the minimum of three and their names." Its feature page puts "building and setting up each one when a deployment to it is needed" here too, and its update feature names "a new environment is set up in the path before pre-production." as a change, with "Setting up a new environment. Environment setup owns it."
- **The approved architecture and surfaces pages** both send environments here ("and its environments (Environment setup).").
- **The product owner's words of 2026-11-08** (given on Deployment design): "The environment setups: yes, minimum 3: dev, testing, and then pre-production.", "Production never gets set on this, not in the path of the project. We are never touching production.", and "each env can be built separately and managed separately, the underlying tech and reusability is important but we needed these to be done only [when] a deployment is needed".
- **The agreed names**: "/design-env (was /shape-run-lens, covers deployments)". One play name for this capability and Deployment design; the drafts name no play.
- **ADR 028**: run is a project-wide design area ("run model — is project-wide, not per-slice").
- **The tracker**: nothing. The Spec → Design business intent (garura-intents #2) has one sub-issue, about surfaces (#553); the Validation → Run one (#5) has none. A search of both repositories found no issue about setting up a project's environments; the open issues the word matched are about other things.

## The overlaps, and how the line could be drawn

### With Deployment design (BI-2, approved)

The approved page already draws most of the line. What is left in the grey zone: what each environment is for, the size of each environment and the cost, and who adds an environment.

1. **As the approved Out line has it.** Here: which environments exist and how many (at least the three, by name), each one's own setup (data, size, network, who can reach it, its own settings), building and managing each one, and adding one. There: the path, what each environment is for, the tests in each, the one design of the underlying technology, where settings and secrets are kept, and the cost. The size declared here is what the cost there is worked out for. The cost of this line: two capabilities must agree on the list of environments, and a size change here calls for the cost to be worked out again there.
2. **Everything about one environment on one page.** What each is for and its tests move here. The cost: reopens the approved Deployment design In line ("the path ... with what each environment is for").
3. **Size moves to Deployment design, beside the cost.** The cost: reopens the approved Out line, which puts size here.

My lean is option 1. It changes nothing approved. The drafts follow it.

### With Continuous delivery and the release plays (Validation → Run)

As built, one agent both brings an environment up and puts the slice on it; nothing separates building an environment from deploying a change into it.

1. **Built here, delivered there.** When a deployment needs an environment that is not built yet, this capability builds it first, after a person's yes; continuous delivery and the release plays then put each change on a built environment. The cost: the first deployment to each environment calls this capability and waits for a person's yes.
2. **The pipeline builds an environment as part of its first deployment to it; this capability only declares.** The cost: contradicts the approved Deployment design feature, which gives "building and setting up each one when a deployment to it is needed" to Environment setup, and the agreed line's "how each is set up".
3. **Every declared environment is built up front.** The cost: against the product owner's words, "only [when] a deployment is needed".

My lean is option 1. It matches his words and the approved page, and the stale agent's own split (bring up, check, take down) already sits under one "environments" domain. The drafts follow it.

### With Build the work (Code → Validation)

1. **Files there, building here.** Build the work makes the infrastructure and container files, as the approved Deployment design already says; this capability builds each environment from them when a deployment needs it. The cost: until the files exist, an environment cannot be built, and the gap is named.
2. **This capability writes each environment's infrastructure files.** The cost: reopens the approved Deployment design Out line, and an agent of a design capability would write code.
3. **Build the work also stands each environment up, as part of a work item.** The cost: environments are built when work is built, not when a deployment needs one.

My lean is option 1. The drafts follow it.

### The copy of the project on a builder's own machine

Left open by Deployment design ("A local copy on a builder's machine, which the stale acceptance play uses, is not one of the three; whether it stays is Environment setup's.").

1. **Not one of the environments here.** A copy on a builder's machine is part of building, not a deployment. If user acceptance testing needs such a copy, it is added here as another environment, through an update. The cost: when the acceptance play is rebuilt, its local copy has no owner until that capability asks.
2. **Declared here as an extra environment outside the path.** The cost: one more environment to keep, and the minimum-three rule must say whether it counts.
3. **Treated as dev.** The cost: every builder's machine becomes "dev", so dev is no longer one place built and managed on its own.

My lean is option 1, because his words name three environments in the path, each built when a deployment needs it, and a builder's copy is not a deployment. The drafts follow it.

### Siblings and other neighbours

No decision asked; the drafts draw these lines:
- **The testing capabilities, Test with evals the builder never sees, and Design for evaluation and testing.** They write and run the tests; Deployment design says which tests run in which environment; this capability sets each environment up. Out here.
- **Seed the memory for the lenses (part of initialize).** Initialize's answers (database, personal data, a running service) are inputs; seeding memory is Out, as on the approved pages.
- **Lock the design.** How the environments are updated once the design is locked is left as not decided, as on the other BI-2 pages.
- **Manage ADRs.** Writes and keeps the decision records. Out.
- **Specify the product.** Owns the product profile; its compliance needs bound each environment's data. Read, never written.
- **Design the technology and architecture, Manage surfaces.** Already send environments here. No change.

## How the product owner's words were read

- "minimum 3: dev, testing, and then pre-production": at least these three, by these names, in that order; a project may add more, each before pre-production (from the approved update feature of Deployment design).
- "We are never touching production.": no environment here is production; nothing here builds, changes or deploys to it. **Read further, for him to confirm:** nothing reads from production either, so no environment is filled with data copied from production. The review's rule against real personal data outside production points the same way.
- "each env can be built separately and managed separately": one environment is built, changed or taken down at a time, and a change to one never changes another.
- "the underlying tech and reusability is important": each environment is built from Deployment design's one design; a declaration says only what makes its environment different.
- "only [when] a deployment is needed": an environment is declared up front but built only when a deployment first needs it.

## The persona

The drafts name **the devops engineer**, because what is built says so: the stale run design names the devops engineer as the one who defines the first environment and the next ("(devops engineer, first environment)", "(devops engineer, next environment)", `core/components/plays/shape-run-lens/reference/ice.md`), and the stale deploy play names the devops engineer as the one who deploys ("(devops engineer, default deploy)", `core/components/plays/release-increment/reference/ice.md`). The same records name a security reviewer (no secrets in the code), an SRE (a failed deploy left clean) and the product owner (running the same environment again). Deployment design, approved, also names the devops engineer. The product owner stays in the Benefit hypothesis and the capability's ICE, as the one who set the three environments, kept production out and asked that each be built only when needed.

## Features found

Three features, none built for the whole project. Each ICE is thin. They follow the shape the product owner asked for on the earlier capabilities: one job is one feature, and a later change is an update as the project changes.

- **Declare the environments and how each is set up** (fn-declare-environments). Not built. Declares which environments the project has, at least dev, testing and pre-production and never production, and for each its data, its size, its network, who can reach it and its own settings, each from memory first, with its source and the person who confirmed it. Sources: the agreed one line; the product owner's words of 2026-11-08; the approved Deployment design Out line; the stale run design and its schema (each environment's fields, built for one slice); Phoenix memory's environment learnings; the review's test-data and settings rules.
- **Build and manage an environment when a deployment needs it** (fn-build-environment). Not built. When a deployment needs an environment that is not built yet, builds it on its own from Deployment design's one design and its declaration, after a person's yes, checks that it answers, keeps it apart from the others, applies each confirmed change to it alone, and takes it down when a person asks. Sources: his words "each env can be built separately and managed separately ... only [when] a deployment is needed"; the approved Deployment design feature's Out of scope line; the stale agent and its two skills (one environment at a time, a separate check that it answers, a failed attempt left as it was, no secret printed, take-down when asked); the stale acceptance play (a copy up only for the walk); the pinned gate rule for standing up a live environment.
- **Update the environments as the project changes** (fn-update-environments). Not built. When the project needs another environment, or one's data, size, network, access or settings must change, a person confirms an update, and what held before stays readable with why it changed; an update reaches a built environment only through the build step. Sources: BI-2's proof "Each position is written down and can change later."; the approved Deployment design update feature ("a new environment is set up in the path before pre-production."); the stale run design's re-run, which adds or changes one environment and keeps the rest; the decision schema's replace-never-edit rule; initialize's re-run when the project changes (planned).

Candidates not drafted as features of their own:
- **Fill an environment with its data**, **check that an environment answers** and **take an environment down**. Each is built in part (stale), but each is a step of building and managing one environment, so they sit inside fn-build-environment, as one job.
- **Bring a slice up on a builder's machine for a person to accept.** Built (stale); left out under the lean on the builder's copy, and it belongs to user acceptance testing.
- **Deploy a slice to an environment.** Built (stale); it carries the design out and belongs with continuous delivery and the release plays.

## Gaps that matter

- **Nothing declares or builds the environments of the whole project.** As built, each slice's run design records its own environments, so the first slice would set them for every later one.
- **The built names do not match his.** The stale run design knows local, dev, qa, stage and prod; it has no testing or pre-production, and its list ends with production. Whoever rebuilds it needs this.
- **The model has no place for an environment.** The ontology (v15) says "None. Every kind a question or a relationship names is defined above." The pages say "Not decided".
- **Memory has nothing on building an environment only when a deployment needs it, or on taking one down**, and every environment ladder in memory ends in production under other names (staging, uat, qa, stage). A proposal for these steps would go to research and a memory update.
- **A product that keeps nothing running** (Garura itself is one): how the three environments look for it is not decided. Its eval already runs in a test project.
- **A person's yes and "must not block".** BI-2 must block on nothing but the lock, and Garura's gate rules pin a person's yes on standing up a live environment. The drafts keep design and build free of the yes: only building an environment waits for it, and only a deployment needs that environment.

## Open points for the product owner

- The line with Deployment design: option 1, 2 or 3. The drafts follow option 1.
- The line with Continuous delivery and the release plays: option 1, 2 or 3. The drafts follow option 1.
- The line with Build the work: option 1, 2 or 3. The drafts follow option 1.
- The copy on a builder's own machine: option 1, 2 or 3. The drafts follow option 1.
- "We are never touching production" read as also never copying production's data into an environment. The drafts say so on every page.
- Whether an environment no deployment uses any more is taken down on its own, or only when a person asks: not decided on the pages. As built, only when asked.
- How an environment a project already has under another name (staging, qa) is matched to dev, testing or pre-production: not decided on the pages.
- The persona: the devops engineer, from what is built, as on Deployment design.
- The feature names, each led by a verb as on the other BI-2 capabilities: "Declare the environments and how each is set up", "Build and manage an environment when a deployment needs it", "Update the environments as the project changes".

## Details left out of the pages

Left for an agent that builds these parts to find in the code and memory: the run design's field names and tier numbers, the agent's failure codes, the deploy play's exit codes, the review's rule IDs and globs (named only in Sources), and which memory learning fits which conditions.

## What this run read from memory

Through the memory tool, copied to `.garura/project/issues/1021/context/bi-2-capability-4/memory/` with `manifest.json`: from Phoenix memory, the run lens schema and its grounding template; the quality lens schema and template (which leave environments to the build); the capability and feature grounding templates; the product profile, decision and ontology schemas; the gate, naming, PR and surface contract rules; the eval index, the command-line step library and the eval format rule; the knowledge index; and the release, agent deployment, GCP runtime and content-management learnings. From Garura memory and short-term memory, the lines read for the decision traces (see `cite-request.json`). No tier was missing.

## Checks

- **Structure check** (`python3 .claude/skills/discover-capabilities/scripts/lint_grounding.py`): `--kind capability --stage directional` on the capability page, `--kind feature` on each of the three feature pages. All four read ok, with no error and no warning, on the first run.
- **ICE shape check** on the four ICE pages: the thin mark first; Intent, Context and Expectation in order; exactly one Goal; three Limits and three Fails if on each (the rubric's limit for a thin ICE); the fixed Read line first; Context labels in order (Read, Never read, Persona, Scope); a Scenario; each Done means checked by someone other than the doer. All four read ok. Each has a Never read line on secret values and on anything in production. No part page has an ICE section.
- **Quotes**: 178 quotes in the Sources sections, checked word for word against their files (memory quotes against this run's short-term copies, the product owner's words against `bi-2-capability-3/research.md` and the approved Deployment design page, which holds his corrected quote), and 11 of his words quoted in the page bodies. None missing. Three Sources lines carry no quote: the tracker line, the short line beside each feature, and the shelf line.
- No page names a plan, a real person or a home-folder path, and none holds a secret's value. The record is `lint.json`.

---

# Addendum, round 2 (2026-11-08): the dev sandbox

The round 1 drafts are kept unchanged in `drafts-round-1/`. The drafts in `drafts/` are now round 2. Nothing outside `bi-2-capability-4/drafts/` and this addendum changed in this round.

## The product owner's answer, as given

"1, 2 are right. local machine is dev sandbox and not an environment - but we do need this. however we dont need to burden a local laptop with cloud liek setup - for example things like docker etc. rest is also okay"

The pages quote it in two parts, with the spelling tidied as on the earlier BI-2 pages: "local machine is dev sandbox and not an environment - but we do need this." and "we don't need to burden a local laptop with cloud like setup - for example things like docker etc."

What stands, as the coordinator gave it: the line with Deployment design (overlap 1); built here and delivered there, with an environment built first, after a person's yes, when a deployment needs it (overlap 2); Build the work makes the infrastructure files (overlap 3); the persona of the capability, the devops engineer; the reading that no environment gets data copied from production; and the one wait, a person's yes before an environment is built.

What changed: overlap 4. A builder's own machine is a dev sandbox. It is not one of the project's environments and not in the path, but it is needed, and running it needs no Docker or other container platform and no cloud service. It is drafted as its own feature, because setting up a builder's machine is a different job from declaring and building the environments.

## What is built for a copy on a builder's machine, and what of it applies

- **The run design's local entry** (stale). The first environment of a slice is "local", recorded with "how to bring it up locally (command / compose file)" and an "optional — test-data seed step". Its template's example runs "the read API and the browser view against fixture files, started with one compose command. No" / "cloud, no secrets; fixtures stand in for real sources." Applies: one command to bring the copy up, a step that fills test data, no cloud and no secrets. Does not apply: the compose file as a way in, and counting the copy as the slice's first environment (tier 0).
- **The skill that brings the copy up** (`deploy-local-environment`, stale). Its examples: "`npm run dev`, a compose file, etc.", and a record whose bring-up is "docker compose -f compose.dev.yaml up -d" and take-down "docker compose -f compose.dev.yaml down". It checks that the copy answers, records the address and how to take it down, keeps "credentials only for seeded TEST users.", and "NEVER stands up a cloud environment (dev/qa/stage/prod)". Applies: the check that it answers, no cloud, and no real credentials. Does not apply: Docker. **Container use, as built: allowed and shown by example, never required.** The sandbox rules it out as a need.
- **The environment-operator's local mode and the acceptance play** (stale). The copy is brought up "for /release-epic's human testing", only for a person's acceptance walk, and taken down after it ("done; the environment is not needed for the close. (On any abort, teardown still runs.)"). The play's check treats every other name, including dev, as beyond its reach. Does not apply: a builder's sandbox is for building, not for a person's acceptance walk. Where that walk runs is now left to user acceptance testing (Validation → Run). The capability page's old Out line on the builder's copy is replaced by an Out line saying so.
- **The live fix play** writes "the failing regression test at the repo's canonical eval path" and needs "a regression test proven red before the fix". That is the kind of check a builder runs in the sandbox, and it is why the sandbox is for running the project's own checks.
- **Phoenix memory.** The architecture template's example slice "whole slice runs on a laptop with no external services.", and the release learning says local is "fixtures only. No real data on a developer machine, ever; fixtures double". Memory has nothing on running a part that needs a cloud service on a builder's machine, so the pages name that as not decided.
- **The review** checks an example settings file against "All required environment variables are documented"; the sandbox takes its setting names from that file.
- **Not used:** `start-change` can set up a git worktree, a separate copy of the code for one change. It does not run the project, and the pages do not tie the sandbox to it.

## How his words were read (for him to correct on the pages)

- "not an environment": the sandbox is not declared as an environment, is not in the path, and is not where the path's tests are counted; a change moves on only on the tests named for dev, in dev.
- "we don't need to burden a local laptop": running the sandbox needs no container platform and no cloud service. When a project's code runs a part on the machine only through a container platform, that is described as it is, and a way to run the part without it is proposed from the code or memory; a part with no such way is named as not decided. A part that cannot run without a cloud service is named as not decided, never guessed.
- The sandbox holds only made-up data and no secret's value, never reaches production, and never holds a slice's eval (the domain "never gives a builder the eval").
- Updating the sandbox setup as the project changes is a line inside the same feature, not a feature of its own, as the coordinator asked for one feature.
- The persona of the sandbox feature is **the developer**, a person or an agent who builds the project's code on their own machine, from the live plays that name it ("(developer, end to end)" in the fix play, "(developer, worktree by config)" in start-change). The capability's persona stays the devops engineer; the developer is added to the capability's "Who it serves".

## What changed on each page

- **Capability page** (9 lines added and 4 changed, one of them the replaced Out line; every other line as in round 1):
  - Opening: a new bullet: a builder's own machine is not an environment and not in the path; it is a dev sandbox, needed, set up here with no container platform or cloud service needed.
  - Feature list: the new feature, Set up a dev sandbox on a builder's machine (fn-dev-sandbox).
  - What is not built yet: "three features" becomes "four features"; a new bullet: as built, a builder's copy is the run design's first environment, brought up by one command or a compose file, with Docker compose in the examples, allowed but not required.
  - Who it serves: adds the developer.
  - Boundary: a new In line for setting up the dev sandbox; the Out line on the builder's copy is replaced by an Out line on where a person's acceptance walk runs (user acceptance testing); a new Never line: needing a container platform or a cloud service to run the sandbox, with his words as the reason.
  - Guiding rules: a new rule: a builder's machine is a dev sandbox, not an environment; it runs the code on the machine, holds only made-up data and no secret's value, and is not where the path's tests are counted; his words as the reason.
  - Sources: his words of this round; the local skill's examples; the fix play's developer; the run schema's local bring-up line.
- **Capability ICE** (3 lines): the Goal adds the dev sandbox; the Scope moves the sandbox into In and replaces "a copy on a builder's own machine" in Out with "where a person's acceptance walk runs"; the Scenario adds one sentence on a developer's sandbox. Still three Limits and three Fails if.
- **Declare the environments and how each is set up** (2 lines): the opening line on what an environment is adds that a builder's own machine is not one, but a dev sandbox; the Out of scope line on the builder's copy now names the dev sandbox and fn-dev-sandbox. Its ICE: one word group in the Scope's Out line.
- **Build and manage an environment when a deployment needs it** (1 line added): an Out of scope line for the dev sandbox. Its ICE: the Scope's Out line adds the dev sandbox.
- **Update the environments as the project changes** (1 line added): an Out of scope line for updating the dev sandbox. Its ICE: the Scope's Out line adds it.
- **Set up a dev sandbox on a builder's machine** (new, `fn-dev-sandbox`), page and thin ICE: what the sandbox is for; no container platform or cloud service needed; for each part, how it starts and stops, its data (made-up, never from production) and its settings (names from the example settings file, never a secret's value); memory first, research only through an approved memory update, never the AI agent's own knowledge; a container-only part described and named as not decided; a part that needs a cloud service named as not decided; not where the path's tests are counted; never a slice's eval; never production; a person confirms; the setup updated as the project changes. Its ICE has three Limits and three Fails if.

## New open points for the product owner

- Where a person's acceptance walk runs, now that a builder's machine is a sandbox. The pages leave it to user acceptance testing.
- How a part that needs a cloud service, such as a managed data store or an outside service it calls, runs in the sandbox. Not decided on the pages.
- A project whose code runs on a machine only through containers: the pages describe it as it is and propose a way without them, or name the part as not decided. He may want a firmer rule.
- The feature name, "Set up a dev sandbox on a builder's machine", and the persona of that feature, the developer.

## Checks, round 2

- Structure check: the capability page (`--stage directional`) and all four feature pages read ok, with no error and no warning.
- ICE shape check: all five ICE pages read ok, each with the thin mark, one Goal, three Limits, three Fails if, the fixed Read line, the Context labels in order, a Scenario and Done means checked by someone other than the doer. No part page has an ICE section.
- Quotes: 222 quotes in the Sources sections and 15 of his words in the page bodies, checked word for word against their files, none missing. His tidied words of this round are checked against this addendum, and as given against `page-approvals.md`. The one quote from the architecture template was checked through the memory tool, because this round made no new memory copy. Three Sources lines carry no quote, as in round 1.
- No page names a plan, a real person or a home-folder path, and none holds a secret's value.
- `lint.json` still holds the round 1 record: this round writes only under `drafts/` and this addendum. `drafts-round-1/` is untouched.
