# Feature: Build and manage an environment when a deployment needs it

## What it does
When a deployment needs an environment that is not built yet, it builds that environment on its own, from the one design of the underlying technology and the environment's declaration, after a person's yes, checks that it answers, and from then on keeps it apart from the others, applies each confirmed change to it, and takes it down when a person asks.
- An environment is one place where a copy of the project runs, such as dev, testing or pre-production. Its declaration says its data, its size, its network, who can reach it and its own settings (Declare the environments and how each is set up, fn-declare-environments). The one design of its underlying technology, the same for every environment, comes from the deployment design (Deployment design).
- Built only when a deployment needs it. A deployment is a change put on an environment, by continuous delivery or by a play that deploys a slice to an environment. When a deployment needs an environment that is not built yet, that environment is built first. An environment that no deployment needs yet is not built. For example, on a new project dev is built for the first change that passes its checks, testing only when a change first moves on to testing, and pre-production only when a release first moves there.
- Built from the one design. Building one more environment repeats the design and adds only what its declaration says, such as its own data and its own size. Nothing of the underlying technology is designed again.
  - It is built from the files that carry out the design, such as infrastructure files and container files, which Build the work makes. When a file it needs is missing, the gap is named and the environment is not built from a guess.
- A person says yes first. Before an environment is built, the person sees which environment, its declaration and what will be built, and says yes. An environment is taken down only when a person asks.
- Proven to answer. An environment counts as built only when a separate check shows it answers, not because the build command ended without an error. A failed build leaves things as they were, and the failure is reported. A person decides the next step.
- Its data is filled as its declaration says, such as with made-up records written for the tests, and never from production.
- Managed on its own. Each environment is changed and taken down without touching the others. A confirmed update of its declaration, such as a bigger size, is applied to that environment only (Update the environments as the project changes, fn-update-environments).
- Never production. Production, the live product that people use, is never a target here, and a request that names it is refused.
- Each build, change and take-down is recorded: which environment, what was done, from which declaration and which design, the check that shows it answers, who said yes, and where its secrets are kept, never their values.
- How it meets the capability: the environments are declared once and each is built only when a deployment needs it, on its own and from the same design, so a project pays only for the environments it uses and every environment is built the same way.

Status: not built. What exists covers only parts of it:
- The agent that operates environments, and its two skills, are stale and wait for the rebuild of the plays that use them. It operates one environment at a time, the one named to it, and builds only what the slice's run design declares for it. It counts its work done only when a check shows the environment answers, never because the command ended without an error. A failed attempt leaves the environment as it was and is reported, and it never tries again on its own. It reads secrets only from where they are kept and never prints them. It takes an environment down when asked and records how. Production is never its target.
- The play that brings a slice up on a builder's machine for a person to accept is stale. It brings that copy up only for the acceptance walk and takes it down after it, even when the walk is stopped. It halts when the slice's run design declares no such copy.
- The play that deploys a slice to a cloud environment is stale. It needs a person's yes before every deploy, under a rule that pins that step to a person because standing up a live cloud environment is outward-facing. It refuses production, and halts when no cloud environment is declared.
- Nothing builds an environment of the path only when a deployment needs it, and nothing builds from a design made for the whole project.
- Memory has nothing on building an environment only when a deployment needs it, or on taking one down.

## Inputs / Outputs
- In: the deployment that needs an environment, and which environment it needs.
- In: the environment's declaration: its data, its size, its network, who can reach it and its own settings.
- In: the one design of the underlying technology from the deployment design, with where secrets and settings are kept.
- In: the files that carry out the design, such as infrastructure files and container files.
- In: a confirmed update of a declaration, for an environment that is already built.
- In: the person's yes before a build, and a person's request to take an environment down.
- Out: the built environment, answering, with its data filled as declared.
- Out: a record of each build, change and take-down, with the check that shows the environment answers and who said yes.
- Out: a failed build, reported, with things left as they were.
- Out: each gap named, such as a missing file or a property still open.

## Rules & behavior
- Only when a deployment needs it. The reason, in the product owner's words: "we needed these to be done only [when] a deployment is needed".
- Each environment on its own. One environment is built, changed or taken down at a time, and a change to one never changes another. The reason, in the product owner's words: "each env can be built separately and managed separately".
- From the one design, never designed again. The reason, in the product owner's words: "the underlying tech and reusability is important".
- Only what is declared and designed is built. A part that neither the declaration nor the design holds is named as a gap, not guessed. The reason: an environment built on a guess differs from the next one built, and nobody can tell why.
- A person says yes before a build, and an environment is taken down only when a person asks. The reason: standing up a live environment is outward-facing, and Garura's rules already pin that step to a person.
- Proven by a separate check. The reason: a build command can end without an error while nothing answers, and the next deployment would then fail in a way nobody can explain.
- A failed build leaves things as they were, and no build is tried again on its own. The reason: a half-built environment is worse than none, and a person must see why it failed before the next try.
- Never production. A request that names production is refused. The reason, in the product owner's words: "We are never touching production."
- No data from production. An environment's data is filled as its declaration says. The reason: copying production's data touches production, and the review already treats real personal data in an environment other than production as a finding.
- Never a secret's value in a record or a log. The reason: every agent reads the records, so a secret written there is no longer secret.
- Nothing else waits for an environment. Slices are designed and built whether or not an environment is built; only a deployment needs its environment. The reason: the Spec → Design business intent blocks no work, and each design can run at any time.
- Not decided: whether an environment that no deployment has used for a while is taken down on its own, or only when a person asks. As built, an environment is taken down only when asked, and the copy for acceptance after its walk.

## Acceptance criteria
- Given a declared testing environment that is not built, and a change that passed dev and must move on to testing, when the deployment needs testing, then testing is built from the same design as dev, with its own data, size, network and access, after a person's yes.
- Given a declared pre-production environment that no deployment has needed yet, when the project's environments are listed, then pre-production shows as declared and not built.
- Given dev is built, when testing is built, then nothing in dev changes.
- Given a build whose command ends without an error but whose environment does not answer, when the build is checked, then it is reported as failed, and things are left as they were.
- Given a request to build production or deploy to it, when it is checked, then it is refused and nothing reaches production.
- Given a declaration whose data would be filled from production, when the build is checked, then it is refused and named.
- Given an infrastructure file the build needs is missing, when the build is asked for, then the gap is named and the environment is not built.
- Given no person's yes, when a build is asked for, then nothing is built.
- Given a confirmed update that doubles the size of testing, when it is applied, then testing alone changes, and the record names the update.
- Given a person asks to take dev down, when it is done, then dev is taken down, the record says how, and testing and pre-production are unchanged.
- Given a build record, when it is read, then it names where each secret is kept and holds no secret's value.

## Out of scope
- Declaring the environments and how each is set up. Declare the environments and how each is set up (fn-declare-environments) does it.
- Updating the declarations. Update the environments as the project changes (fn-update-environments) does it.
- Designing the underlying technology, the path and the tests in each environment. Deployment design owns them.
- Deploying each change into an environment. Continuous delivery does it, and the plays that bring a slice up for a person to accept or deploy a slice to an environment.
- Making the infrastructure files and container files. Build the work makes them, from work items.
- Running the tests in an environment. The testing capabilities and Test with evals the builder never sees do it.
- Setting up the dev sandbox on a builder's machine, which is not an environment. Set up a dev sandbox on a builder's machine (fn-dev-sandbox) does it.
- Anything in production. The project never touches it.

## Sources
- The one line the product owner agreed on 2026-11-03: "Which environments exist, how many, and how each is set up."
- The product owner on 2026-11-08, on the first drafts of Deployment design: "We are never touching production."
- The product owner on 2026-11-08, on the second drafts of Deployment design: "each env can be built separately and managed separately, the underlying tech and reusability is important but we needed these to be done only [when] a deployment is needed"
- The capability list the product owner locked on 2026-11-03: "Continuous delivery (planned): Accepted changes are delivered to their environments automatically.", "Build the work: Each work item, whether a slice, a feature, a story or a chore, is built end to end from its design."
- .garura/product/product-os/intents/bi-2.md: "Block other work. Each design can be run at any time."
- .garura/product/product-os/software-delivery-planning/deployment-design/capability.md: "Each environment is built and managed on its own, from one design of its underlying technology that is reused for every environment, and it is built only when a deployment to it is needed."
- .garura/product/product-os/software-delivery-planning/deployment-design/fn-design-how-project-runs/feature.md: "Declaring which environments exist and how many, and building and setting up each one when a deployment to it is needed. Environment setup owns it, from the design made here.", "Making the container, Kubernetes, pipeline and infrastructure files. Build the work makes them, from work items."
- .garura/product/product-os/software-delivery-planning/deployment-design/fn-cloud-cartridges/feature.md: "Setting up an environment on a cloud. Environment setup owns it."
- core/components/agents/environment-operator.md: "waits for the rebuild of /release-epic and /release-increment (#855); only stale plays dispatch it", "domain: environments", "brings an increment up on ONE environment the run lens declares", "proves it reachable, captures the deploy record, and tears it down when asked", "doesn't declare it, you don't build it.", "Production is never your target", "leave the environment in its prior state", "Declare done without reachability evidence in the record", "Print, log, or store a secret value"
- core/components/skills/deploy-local-environment/SKILL.md: "Tears the environment down when asked (the reverse contract).", "test data when the local environment declares a seed step.", "Record the teardown path with the deploy.", "credentials only for seeded TEST users."
- core/components/skills/deploy-cloud-environment/SKILL.md: "Do NOT trust the deploy command's exit code.", "it never auto-rolls-back", "(tear down a prior deploy of this env)"
- core/components/plays/release-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "Run lens `run.yaml` declares a local environment", "done; the environment is not needed for the close. (On any abort, teardown still runs.)"
- core/components/plays/release-increment/SKILL.md: "stops below production (prod stays with CD from main)"
- core/components/plays/release-increment/reference/ice.md: "(devops engineer, default deploy)", "production is out of scope — refuse it outright (halt)"
- core/components/plays/release-increment/scripts/resolve_deploy_target.py: "if no cloud environment is defined at all, halt with NO_CLOUD_ENV (4)"
- standards/rules/gate-config.md, in Phoenix memory: "environment is outward-facing — always requires a human"
- standards/rules/naming.yaml, in Phoenix memory: "deploy: Put a running increment on an environment."
- core/components/skills/check-quality/reference/all-requirements.md: "Non-production environments use masked or synthetic data — no production PII in staging/dev"
