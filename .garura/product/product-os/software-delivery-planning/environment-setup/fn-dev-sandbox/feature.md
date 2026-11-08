# Feature: Set up a dev sandbox on a builder's machine

## What it does
It sets up a dev sandbox on a builder's own machine, a place where the builder runs the project's code while building it, with each part of the project running on the machine itself and no container platform or cloud service needed, so a builder can try a change before it goes to dev.
- A builder is a person or an agent who writes the project's code. The dev sandbox is the builder's own machine, such as a laptop, set up to run the project. Each builder has their own.
- It is not an environment. It is not one of the project's environments and not in the path a change takes through dev, testing and pre-production (Declare the environments and how each is set up, fn-declare-environments). But it is needed, so it is set up here too.
- What it is for: running the project's code while building it, trying a change by hand, and running the project's own checks, such as a test written to prove a fix, before the change is pushed.
- No cloud-like setup. Running the sandbox needs no container platform, such as Docker, and no cloud service. Each part runs as the machine runs it: for example, a service as a program the builder starts with one command, a browser page from the project's own development server, or a command line tool from the project's folder.
- For each part of the approved architecture, the setup says:
  - how it starts and stops on the machine;
  - its data: made-up records written for the tests, kept with the project's code or made by a step that fills them. Never data copied from production;
  - its settings: the names from the project's example settings file, with values for the sandbox. A secret's value is never written into the setup;
  - for each part, its reason, its source and the person who confirmed it.
- For each part, an agent proposes how it runs and where it gets what it needs:
  - A project that already has code shows much of it there: its run scripts, the commands its readme gives, its example settings file, and its test data with the steps that fill it. The proposal describes them as they are, with the files that show them.
  - Where the code does not settle it, the proposal comes from what the project's memory holds: the approved architecture, with its parts and their technology, the declared surfaces, and the deployment design.
  - Then it comes from Garura memory, the memory Garura keeps for the project, and then from Phoenix memory, the shared memory on the machine that every project draws from, and its architecture and technology learnings for running a part on a builder's machine.
  - Only when no memory has an answer does the agent research it. It raises what it found as a memory update, a proposed addition to memory, for a person to approve. Until the person approves it, that part stays open.
  - Nothing comes from what the AI agent knows by itself. A part that nothing backs stays open, with no default, and the person decides it.
- When the project's files run a part on the machine only through a container platform, that is described as it is, and a way to run the part without it is proposed from the code or memory. A part that has no such way is named as not decided.
- A part that cannot run without a cloud service, such as a managed data store or an outside service it calls, is not set up with one and not guessed. It is named as not decided.
- It is not where the path's tests are counted. A builder may run any of the project's own checks in the sandbox, but a change moves along the path only on the tests that run in dev, testing and pre-production, as the deployment design says.
- It never holds a slice's eval, and it never reaches production.
- A person confirms how each part runs there. As the project changes, such as when it gains a part, the setup is updated the same way, and what held before stays readable with why it changed.
- How it meets the capability: the capability sets up where the project runs, the environments of the path and, for each builder, the sandbox on their own machine. A builder tries each change there before it reaches dev, and no laptop carries a cloud-like setup.

Status: not built. What exists covers only parts of it, and some of it does not apply:
- The design play for a slice's run is stale. Its first environment is a builder's copy, "local", recorded with how to bring it up, by one command or a compose file, and an optional step that fills it with test data. Its template's example runs the copy against test files, with no cloud and no secrets, started with one compose command. What applies: one command to bring it up, a step for test data, no cloud and no secrets. What does not: the compose file as a way in, and the copy counted as the slice's first environment.
- The skill that brings that copy up is stale. Its example starts it with Docker compose and takes it down the same way; its other example is the project's own development command. It checks that the copy answers, records the address and how to take it down, keeps only test users' credentials, and never touches a cloud environment. What applies: the check that it answers, no cloud, and no real credentials. What does not: Docker. As built, a container platform is allowed and shown by example, never required.
- The agent that operates environments, in its local mode, and the play that brings a slice up for a person to accept, are stale. They bring the copy up only for a person's acceptance walk and take it down after it. A builder's sandbox is for building, not for that walk; where the walk runs is for user acceptance testing to decide.
- The fix play, which is live, writes a test that fails before the fix and runs it in the project's own folder. That is the kind of check a builder runs in the sandbox.
- Phoenix memory's examples run a slice on a laptop with no outside services, from test files. Memory has nothing on running a part that needs a cloud service on a builder's machine.
- The review checks that every setting an environment needs is written down in an example settings file. It reads what was built.

## Inputs / Outputs
- In: the project's code: its run scripts, the commands its readme gives, its example settings file, and its test data with the steps that fill it.
- In: the approved architecture, with its parts and their technology; the declared surfaces; and the deployment design.
- In: Phoenix memory's architecture and technology learnings for running a part on a builder's machine.
- In: a memory update a person approved, when no memory had an answer and the agent researched it.
- In: the person's confirmation or correction of each proposal.
- Out: the sandbox setup: for each part, how it starts and stops on the machine, its data and its settings, each with its source and the person who confirmed it.
- Out: each part that cannot run without a container platform or a cloud service, named as not decided.
- Out: a memory update for each part the agent researched, waiting for a person's approval.

## Rules & behavior
- Not an environment, and not in the path. The reason, in the product owner's words: "local machine is dev sandbox and not an environment - but we do need this."
- No container platform and no cloud service needed to run it. The reason, in the product owner's words: "we don't need to burden a local laptop with cloud like setup - for example things like docker etc."
- The project's memory first. Each part is proposed from the project's own memory and code first, then from Garura memory, then from Phoenix memory. The reason: a source in the project or in memory can be checked and read back, so the person can judge the proposal from it.
- Research only when no memory has an answer, and only through a memory update. The agent uses what it found only after a person approves the update. Until then that part stays open, and the work goes on. The reason: research is new knowledge that nobody has checked yet, and the person's approval is the check.
- Never from the AI agent's own knowledge. A part with no source behind it is not proposed, and no stand-in for a cloud service is made up. The reason: a setup that an agent assumed fails on the next builder's machine, and nobody can tell why.
- What the project's code already does is described as it is, and a part it runs only through a container is named as not decided until a way without it is confirmed. The reason: a setup that contradicts the code sends builders after commands nobody uses, and the product owner ruled the container out.
- Each part names its source. The reason: a person can check it without a search, and when a source changes, the setup built on it can be found.
- Never data copied from production. The sandbox holds only made-up data. The reason: copying production's data touches production, and the review already treats real personal data outside production as a finding.
- Never a secret's value in the setup. The reason: every builder reads the setup and it is kept with the project's files, so a secret written there is no longer secret.
- Not where the path's tests are counted. The reason: a change moves on only when the tests named for an environment pass there, so it never moves on because it worked on one machine.
- Never a slice's eval. The reason: the builder never reads the evals, which test each slice from the outside.
- A person confirms how each part runs there, and the reason is written beside it. The reason: each choice has reasons, and without them the next builder cannot tell a choice from an accident.
- Nothing waits for the sandbox. A builder can build with a part still open: the work goes on, and the open part is named. The reason: the Spec → Design business intent must not block on anything except the lock.
- Not decided: how a part that needs a cloud service, such as a managed data store or an outside service it calls, runs in the sandbox.
- Not decided: where the sandbox setup is kept, because the model has no kind for it.

## Acceptance criteria
- Given a project with one service and a browser page whose readme starts each with one command, when the sandbox is proposed, then each part runs on the machine with that command, and the files that show it are named.
- Given a project whose only way to run on a machine is a compose file for a container platform, when the sandbox is proposed, then the compose file is named, a way to run each part without it is proposed from the code or memory, and a part with no such way is named as not decided.
- Given a part that needs a managed data store on a cloud, when the sandbox is proposed, then no cloud service is set up, and the part is named as not decided.
- Given a proposal with no source behind it, when the proposals are checked, then it is taken out and the part is named as open.
- Given test data proposed as a copy of production's data, when it is checked, then it is refused and named.
- Given a draft setup that holds a secret's value, when it is checked, then the value is taken out and only the setting's name stays.
- Given a change whose checks pass in a builder's sandbox, when it is to move on, then it moves to testing only when the tests named for dev pass in dev.
- Given a sandbox, when its files are listed, then no slice's eval is among them.
- Given a new builder on a machine with no container platform and no cloud account, when they follow the setup, then each part runs, or is named as not decided.
- Given no sandbox setup yet, when a builder starts work, then the work goes on and what is missing is named.

## Out of scope
- Declaring and building the environments of the path. Declare the environments and how each is set up (fn-declare-environments) and Build and manage an environment when a deployment needs it (fn-build-environment) do it.
- Which tests run in each environment and what lets a change move on. Deployment design owns it, and the testing capabilities run the tests.
- A slice's eval. Test with evals the builder never sees owns it.
- Where a person's acceptance walk runs. User acceptance testing owns it.
- Making the code, the run scripts and the test data. Build the work makes them, from work items.
- The parts of the system and what each is built with. Design the technology and architecture owns them.
- Anything in production. The project never touches it.
- Moving an approved memory update into Phoenix memory. A person does it on purpose, as a promotion, outside this work.

## Sources
- The one line the product owner agreed on 2026-11-03: "Which environments exist, how many, and how each is set up."
- The product owner on 2026-11-08, on the first drafts of Environment setup: "local machine is dev sandbox and not an environment - but we do need this.", "we don't need to burden a local laptop with cloud like setup - for example things like docker etc."
- The product owner on 2026-11-08, on the first drafts of Deployment design: "We are never touching production."
- The capability list the product owner locked on 2026-11-03: "Test with evals the builder never sees: Each slice is tested end to end by evals its builder can't read.", "User acceptance testing (planned): Users test the product and accept it.", "Build the work: Each work item, whether a slice, a feature, a story or a chore, is built end to end from its design."
- .garura/product/product-os/intents/bi-2.md: "Block on anything except the lock, which is the only gate."
- .garura/product/product-os/software-delivery-planning/domain.md: "it never gives a builder the eval"
- .garura/product/product-os/software-delivery-planning/deployment-design/capability.md: "Each environment names the tests that run there, and a change moves to the next one only when they pass."
- standards/schemas/product-os/lens/run.yaml, in Phoenix memory: "how to bring it up locally (command / compose file)", "optional — test-data seed step", "order: 0 local, 1 dev, 2 qa, 3 stage, 4 prod."
- standards/schemas/product-os/grounding/lens/run.md, in Phoenix memory: "the read API and the browser view against fixture files, started with one compose command. No", "cloud, no secrets; fixtures stand in for real sources."
- core/components/skills/deploy-local-environment/SKILL.md: "`npm run dev`, a compose file, etc.", "docker compose -f compose.dev.yaml up -d", "docker compose -f compose.dev.yaml down", "credentials only for seeded TEST users.", "NEVER stands up a cloud environment (dev/qa/stage/prod)"
- core/components/agents/environment-operator.md: "waits for the rebuild of /release-epic and /release-increment (#855); only stale plays dispatch it", "for /release-epic's human testing"
- core/components/plays/release-epic/SKILL.md: "done; the environment is not needed for the close. (On any abort, teardown still runs.)"
- core/components/plays/fix-bug/SKILL.md: "the failing regression test at the repo's canonical eval path", "a regression test proven red before the fix"
- core/components/plays/fix-bug/reference/ice.md: "(developer, end to end)"
- core/components/plays/start-change/reference/ice.md: "(developer, worktree by config)"
- standards/schemas/product-os/grounding/lens/architecture.md, in Phoenix memory: "whole slice runs on a laptop with no external services."
- knowledge/technology/run-environments-canary-migrations.md, in Phoenix memory: "fixtures only. No real data on a developer machine, ever; fixtures double"
- standards/rules/pr.md, in Phoenix memory: "`path:**/{seed,fixtures,test-data}/**`", "`path:.env.example,README.md,docs/setup/**`"
- core/components/skills/check-quality/reference/all-requirements.md: "Non-production environments use masked or synthetic data — no production PII in staging/dev", "All required environment variables are documented"
- core/tools/memory/GUIDE.md: "Never answer from what you already know, and never from the web, without a", "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
- core/tools/memory/GUIDE.md: "Your work goes on while the update waits, unless you cannot go on without it.", "to Garura memory or Phoenix memory is a promotion a person makes on purpose, outside your"
