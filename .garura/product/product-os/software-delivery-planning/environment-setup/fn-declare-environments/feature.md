# Feature: Declare the environments and how each is set up

## What it does
It declares which environments the project has, at least dev, testing and pre-production and never production, and for each one its data, its size, its network, who can reach it and its own settings, so every deployment and every test runs in a place that was set up on purpose.
- An environment is one place where a copy of the project runs. Production, the live product that people use, is never one of them. A builder's own machine is not one either: it is a dev sandbox (Set up a dev sandbox on a builder's machine, fn-dev-sandbox). Each declared environment holds:
  - Its name and its place among the others. Dev, testing and pre-production come in that order. A project may add more, each before pre-production, such as an environment of its own for performance tests.
  - What it is for, as the deployment design says. This feature does not set it.
  - Its properties, what the environment offers and how it behaves:
    - its data: what data it holds and where that data comes from. For example, a few made-up records in dev, and a larger made-up set shaped like real use in pre-production;
    - its size: for example, how many copies of each service run, how big its data store is, and whether more copies start as use grows;
    - its network: for example, whether it can be reached from the internet or only from inside the team's network, and which ways in are open;
    - who can reach it: for example, the team in dev, the testers in testing, and the people who accept a release in pre-production;
    - its own settings: the settings whose values differ in this environment, by name. A secret's value is never written. Where settings and secrets are kept is part of the deployment design.
  - For each part, its reason, its source and the person who confirmed it.
- What is the same in every environment is not declared here. The cloud, the container platform and the one design of the underlying technology come from the deployment design (Deployment design). A declaration says only what makes its environment different.
- Declaring is not building. Each declared environment is built only when a deployment to it is needed (Build and manage an environment when a deployment needs it, fn-build-environment).
- It runs before the slices are designed, once the deployment design is known as far as it is, and again when the project needs an environment it does not have. A slice is an ordered group of features that one person can test end to end on one surface.
- For each environment and property, an agent proposes an answer:
  - A project that already deploys shows much of it in its files: infrastructure files that create its environments, pipeline files that name them, container and compose files, and an example settings file. The proposal describes them as they are, with the files that show them.
  - Where the files do not settle it, the proposal comes from what the project's memory holds: the deployment design, with the path and what each environment is for; the approved architecture and the declared surfaces; the compliance needs in the product profile, such as rules for personal data; and the project's set-up answers, such as whether it has a database or holds personal data, once the set-up step (initialize) is built. The product profile is the record of the product's shape and the quality levels and compliance needs it commits to.
  - Then the proposal comes from Garura memory, the memory Garura keeps for the project, and then from Phoenix memory, the shared memory on the machine that every project draws from. Phoenix memory's architecture and technology learnings are matched to the project's conditions, such as its architecture, its stage and its users. A learning whose environments end in production gives what it says for the others, and its production environment is left out.
  - Only when no memory has an answer does the agent research it. It raises what it found as a memory update, a proposed addition to memory, for a person to approve. Until the person approves it, that part stays open.
  - Nothing comes from what the AI agent knows by itself. A part that nothing backs stays open, with no default, and the person decides it.
- The person confirms or corrects each environment and property, and gives the reason when the proposal has none. Only a confirmed part is declared.
- How it meets the capability: this is how the environments of the whole project, and how each is set up, are declared once. Each environment is then built from its declaration when a deployment needs it, and every deployment and test runs in a declared place.

Status: not built. What exists covers only parts of it:
- The design play for a slice's run is stale and waits for a rebuild. For its own slice, it records each environment, one at a time. Its names are fixed, local, dev, qa, stage and prod, in that order, so its list has no testing or pre-production and ends with production. For each environment it records whether it runs on a builder's machine or on a cloud, the settings of that environment, with its secrets kept in a secrets store and never in the code, how a builder's copy is brought up and an optional step that fills it with test data, and for a cloud one its region, the size of what runs, whether it is open to the internet, inside the team's network or behind a load balancer, its firewall rules, and the identity its services use. It never writes a secret's value. Nothing declares these for the whole project.
- Phoenix memory's learnings for running give each environment its own stance on data, such as test records only on a builder's machine and a cleaned copy shaped like real data in the environment before the live one, and show a dev environment that only the team's network can reach, kept cheap because it does not serve users. Their environments end in production, and none of them names testing or pre-production.
- The review checks, in each change, files of test data against the rule that an environment other than production holds masked or made-up data, and an example settings file against the rule that every setting an environment needs is written down. It reads what was built; nothing gives it declared environments to compare with.
- The project set-up step, initialize, will ask whether the project has a database, personal data, permissions or a running service. It is not built.

## Inputs / Outputs
- In: the project's code and its settings, when it has any: its infrastructure files, pipeline files, container and compose files, and example settings file.
- In: the deployment design: the path, what each environment is for, and the one design of the underlying technology.
- In: the approved architecture and the declared surfaces.
- In: the compliance needs in the product profile, and the project's set-up answers once initialize is built.
- In: Phoenix memory's architecture and technology learnings on environments.
- In: a memory update a person approved, when no memory had an answer and the agent researched it.
- In: the person's confirmation or correction of each proposal.
- Out: the proposals: each environment with its name, its place, its data, its size, its network, who can reach it and its own settings, each with its reasons and its source. The source is a file of the project, a memory file or an approved memory update.
- Out: a memory update for each part the agent researched, waiting for a person's approval.
- Out: the declared environments of the whole project, each part with its source and the person who confirmed it.
- Out: each part left open, named as a gap.

## Rules & behavior
- The project's memory first. Each environment and property is proposed from the project's own memory and code first, then from Garura memory, then from Phoenix memory. The reason: a source in the project or in memory can be checked and read back, so the person can judge the proposal from it.
- Research only when no memory has an answer, and only through a memory update. The agent uses what it found only after a person approves the update. Until then that part stays open, and the work goes on. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- Never from the AI agent's own knowledge. A part with no source behind it is not proposed. The reason: an environment set up on a guess is found wrong only when a test or a release fails in it.
- What the project's files already show is described as it is. The reason: a declaration that contradicts the environments the project uses sends every builder after places that nobody runs. Moving away from it is an update (fn-update-environments).
- Each part names its source. The reason: a person can check it without a search, and when a source changes, the properties built on it can be found.
- At least dev, testing and pre-production, in that order, and any more before pre-production. The reason, in the product owner's words: "The environment setups: yes, minimum 3: dev, testing, and then pre-production."
- Never production. No environment declared here is production, and no environment's data comes from production. The reason, in the product owner's words: "We are never touching production."
- A declaration says only what makes its environment different, and the rest comes from the deployment design. The reason: what is written twice drifts apart, and the product owner asked that the underlying technology be reused.
- The compliance needs in the product profile bound each environment's data, and a declaration never changes them. The reason: the profile is the box the product commits to, only an approved decision moves it, and the review already treats real personal data in an environment other than production as a finding.
- Never a secret's value. A declaration names a setting, and where its secret is kept comes from the deployment design. The reason: every agent reads the declarations, so a secret written there is no longer secret.
- A person confirms each environment and property, and the reason is written beside it. The reason: each has reasons, and without them the next person cannot tell a choice from an accident.
- Nothing waits for the declaration. A slice can be designed and built with an environment or a property still open: the work goes on, and the open part is named, so a person can set it later. The reason: the Spec → Design business intent blocks no work, and each design can run at any time.
- Not decided: where the declared environments are kept, because the model has no kind for an environment.
- Not decided: how an environment the project already has under another name, such as staging or qa, is matched to dev, testing or pre-production.
- Not decided: how the three environments look for a product that keeps nothing running, such as a command a person installs. The eval of a play already runs the play in a test project.

## Acceptance criteria
- Given a project with no environments yet and a deployment design whose path runs through dev, testing and pre-production, when the environments are proposed, then dev, testing and pre-production are proposed in that order, each with its data, its size, its network, who can reach it and its own settings, and each part names its source.
- Given a project whose pipeline files already deploy to an environment, when its environments are proposed, then that environment is described as it is and the files that show it are named.
- Given a proposal that declares production as an environment, or fills an environment with data taken from production, when the proposals are checked, then it is taken out and named.
- Given a product profile whose compliance needs cover personal data, when the data of testing is proposed, then it holds no real personal data, and the compliance need is named.
- Given a Phoenix memory learning whose environments end in production, when the environments are proposed from it, then what it says for the others is used and named, and its production environment is left out.
- Given a property that nothing in the project or in memory backs, when the proposals are made, then the agent researches it, raises a memory update with what it found, and the property stays open until a person approves the update.
- Given a proposal with no source behind it, when the proposals are checked, then it is taken out and the part is named as open.
- Given a draft declaration that holds a secret's value, when it is checked, then the value is taken out and only the setting's name stays.
- Given a declaration that repeats the cloud or the container platform, when it is checked, then the repeated part is taken out and read from the deployment design.
- Given the person adds an environment for performance tests, when the environments are written, then it sits before pre-production, with the person's reason and name.
- Given a declared environment, when an agent that did not declare it prepares to build it, then it can name its data, its size, its network, who can reach it and its own settings without asking a person.
- Given no environment is declared yet, when a slice is designed, then the work goes on and what is missing is named.

## Out of scope
- Building and managing each environment. Build and manage an environment when a deployment needs it (fn-build-environment) does it.
- Updating the declared environments as the project changes. Update the environments as the project changes (fn-update-environments) does it.
- The path, what each environment is for, the tests in each, the one design of the underlying technology, the cloud, where settings and secrets are kept, and the cost. Deployment design owns them.
- The dev sandbox on a builder's own machine. It is not an environment and is not declared here. Set up a dev sandbox on a builder's machine (fn-dev-sandbox) does it.
- The product profile and its compliance needs. Specify the product owns them.
- Anything in production. The project never touches it.
- Moving an approved memory update into Phoenix memory. A person does it on purpose, as a promotion, outside this work.

## Sources
- The one line the product owner agreed on 2026-11-03: "Which environments exist, how many, and how each is set up."
- The product owner on 2026-11-08, on the first drafts of Deployment design: "The environment setups: yes, minimum 3: dev, testing, and then pre-production.", "We are never touching production."
- The product owner on 2026-11-08, on the second drafts of Deployment design: "the underlying tech and reusability is important"
- .garura/product/product-os/intents/bi-2.md: "Without shared positions, each builder invents its own answer.", "Block other work. Each design can be run at any time."
- .garura/product/product-os/software-delivery-planning/deployment-design/capability.md: "at least dev, testing and pre-production, each built and managed on its own when a deployment to it is needed, with its data, its size, its network and who can reach it.", "This capability holds the path a change takes through them, what each is for, and the one design each is built from.", "where the settings that differ between environments are kept"
- .garura/product/product-os/software-delivery-planning/deployment-design/fn-design-how-project-runs/feature.md: "A learning that ends its path in production gives everything up to pre-production, and its production step is left out."
- core/components/plays/shape-run-lens/SKILL.md: "waits for the rebuild of the design plays after the shaping loop (#855, ADR 053)", "the slice-level design (rollout, migrations, config/secrets, CI/CD) once, and ONE environment per call"
- core/components/plays/shape-run-lens/scripts/resolve_target_env.py: "known tiers: local=0, dev=1, qa=2, stage=3, prod=4"
- standards/schemas/product-os/lens/run.yaml, in Phoenix memory: "order: 0 local, 1 dev, 2 qa, 3 stage, 4 prod.", "per-env config; secrets via secrets-manager, NEVER in repo", "how to bring it up locally (command / compose file)", "optional — test-data seed step", "optional — instances / size / scaling", "public | internal | load-balanced", "ingress/egress rules — ports, sources, allow/deny", "service accounts / roles / workload identity"
- core/components/plays/shape-run-lens/reference/ice.md: "(devops engineer, first environment)", "(devops engineer, next environment)", "(security reviewer, no secrets in repo)"
- knowledge/technology/run-environments-canary-migrations.md, in Phoenix memory: "Three environments, each with a distinct data stance.", "fixtures only. No real data on a developer machine, ever; fixtures double", "sanitized production-shaped data", "two places it leaks from most — laptops and test environments."
- knowledge/technology/agent-deploy-dev-uat-prod.md, in Phoenix memory: "build and iterate on prompts, tools, orchestration; cheap models OK while", "The gate before prod."
- knowledge/technology/gcp-modular-monolith-runtime.md, in Phoenix memory: "Promote dev → staging → prod.", "Lock ingress and ports to the minimum the service actually needs"
- standards/schemas/product-os/grounding/lens/run.md, in Phoenix memory: "No public ingress yet — a firewall rule", "allows the team VPN only.", "dev is deliberately locked down and cheap because it exists"
- standards/rules/pr.md, in Phoenix memory: "`path:**/{seed,fixtures,test-data}/**`", "`path:.env.example,README.md,docs/setup/**`"
- core/components/skills/check-quality/reference/all-requirements.md: "Non-production environments use masked or synthetic data — no production PII in staging/dev", "All required environment variables are documented"
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "The box moves ONLY by an approved decision."
- .garura/product/product-os/software-delivery-planning/initialize/fn-setup-questions/feature.md: "whether there is a database, personal data, permissions or a running service", "Where nothing backs a proposal, the question carries no proposed answer and the person answers it; there is never a default in place of a source"
- standards/schemas/eval/steps-command-line.yaml, in Phoenix memory: "a command in the test project and gives it the scripted answers."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "None. Every kind a question or a relationship names is defined above."
- core/tools/memory/GUIDE.md: "Never answer from what you already know, and never from the web, without a", "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- core/tools/memory/GUIDE.md: "Your work goes on while the update waits, unless you cannot go on without it.", "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
