# Feature: Measure how fast the running build answers under the load the pass bar names

## What it does
When the pass bar or a capability's performance need names a load, such as a number of people using the product at once, this feature puts that load on the running build with made-up users, in the environment the deployment design places the load tests in and at the size Environment setup declares for it, measures what the bar names under that load, and records each figure with the load and the conditions, so the product owner knows that the product keeps its performance level when many use it at once.
- The load comes only from the pass bar or a capability's performance need, never from what the AI agent knows by itself. For example:
  - a shop's checkout: how long the checkout page takes when the number of shoppers the pass bar names buy at once;
  - a school's timetable app for phones: how long the day's timetable takes to open when the number of pupils the need names open it in the same minute;
  - a clinic's booking endpoint that another system calls: how long it takes to answer at the number of requests each second the need names.
- A product that one person uses at a time, such as a command-line tool on one person's computer, may name no load, and then this feature has nothing to do.
- The load runs where the deployment design places the load tests: the testing environment, or an environment of its own for performance tests that Environment setup declares before pre-production, with "a size fit for the load the tests need". The test never makes an environment bigger or smaller.
- The made-up users are the environment's own test accounts, working on its made-up data. No load reaches anything outside the environment: not production, not a builder's own machine, and no system the environment does not hold, such as a payment provider's live service or a service another team shares.
- How long the load runs, how many tries count and which figure counts come from how the pass bar says it is measured. Each run records its conditions: the load, how long it ran, the environment and its declared size, and its data.
- When the environment cannot carry the load the pass bar names at its declared size, the part is named as not measured, with its reason. No figure for the named load is worked out from a smaller one.
- The cost of the load tests is part of what Deployment design works out for the environments in the path, on each of the three clouds. Each run records how long it ran and what load it put on, so the cost can be checked against it.
- How it meets the capability: a capability's performance need is checked, in the model's own example, by a "load test", and the approved Environment setup pages already plan an environment of its own for performance tests.

Status: not built. What exists covers only part of it:
- Nothing puts load on a build. The old slice check, /validate-epic, which is stale, had no runner for it.
- The scored quality check, built and never used, asks for a "Load testing tool present in repo or CI pipeline" and that "At least one load test scenario covers the critical user path"; the standard it reads for them is in no memory tier.
- The review of each change only notes, at its lowest rank, which is hidden by default, that a change touched a folder of load tests.
- Environment setup plans "such as an environment of its own for performance tests.", added before pre-production; it is not built.
- Deployment design plans the cost of the environments in the path on each cloud, "for the same sizes of use"; it is not built, and no cost is worked out today.
- No memory tier holds how a load test is run or how long, for any kind of product.

## Inputs / Outputs
- In: the load the pass bar or each capability's performance need names, what is measured under it, and how it is measured.
- In: where the deployment design places the load tests, and the cost it worked out for that environment on each cloud.
- In: the environment, as Environment setup declares and builds it, with its declared size, its made-up data and its test accounts.
- In: where the deployment design keeps that environment's secrets.
- Out: for each part that names a load, the figure under that load, a pass or a fail, and the conditions; each part not measured, with its reason; and how long each run ran and what load it put on, for Give the performance verdict, and send each finding to the developer or to a person (fn-send-performance-findings).

## Rules & behavior
- Only the load the pass bar or a need names. The reason: "The NUMBERS live in the product profile, per product — never in this KB.", and "A numeric constraint without a source is a hallucination dressed up as a fact."
- Only inside the environment set up for it. The reason, in the product owner's words: "We are never touching production."; and load sent to a system the environment does not hold would reach people and services outside the test.
- Never resize the environment. The reason: Environment setup owns the size, and "The size declared here for each environment is what that cost is worked out for, so a change of size calls for the cost to be worked out again."
- Never worked out from a smaller load or a smaller environment. The reason: no memory holds a rule for it, and "An unmeasured bar is not a passed bar."
- Each run records how long it ran and what load it put on. The reason, in the product owner's words on the design: "For each one, we need to know what the cost looks like to get this piece figured out, running it across, and whatnot."
- Test accounts and made-up data, and secrets at run time, never written. The reason: each environment holds "made-up records written for the tests", and "no environment's data comes from production."
- A part that is not the builder runs it, and the builder never sees the figures. The reason: "giving it to the builder only invites teaching-to-the-test."
- Not decided: whether the profile's scalability level, how much more load the product can take, is also tested here.
- Not decided: whether a project setting caps what one run may cost, above which a person says yes first.
- Not decided: whether a load test waits until the slice's eval passes, so that no money is spent on a build that fails it.

## Acceptance criteria
- Given a pass bar that names how long a page may take when a named number of people use it at once, when the test runs in the environment the deployment design places it in, then it puts that load on with test accounts and records the figure, a pass or a fail, the load, how long it ran, and the environment's declared size.
- Given an environment whose declared size cannot carry the named load, when the test is planned, then the part is named as not measured with its reason, and no figure is worked out from a smaller load.
- Given a load that would reach a system the environment does not hold, such as a payment provider's live service, when the test runs, then that load is not sent, and the part it serves is named as not measured.
- Given a product whose pass bar and performance needs name no load, when the tests run, then this feature puts no load on the build.
- Given a run, when its record is read, then it names how long it ran and what load it put on, and the environment's size is the one Environment setup declared.

## Out of scope
- Measuring how fast the build answers one person. Measure how fast the running build answers, in the testing environment (fn-test-running-speed) does it.
- Declaring, building and resizing the environment for load tests. Environment setup does it.
- Placing the load tests in an environment, and working out what they cost on each cloud. Deployment design does it.
- Giving the verdict and sending each finding back. Give the performance verdict, and send each finding to the developer or to a person (fn-send-performance-findings) does it.
- Testing the product in production. No capability of the project touches production.

## Sources
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "Test performance, against the product profile's performance level. Moved here from Validation → Run.", "Assumed: security and performance tests run in the testing environment Environment setup declares, never in production."
- The product owner, in .garura/project/issues/1021/context/bi-4-capability-3/page-approvals.md: "We are never touching production.", "For each one, we need to know what the cost looks like to get this piece figured out, running it across, and whatnot."
- standards/schemas/product-os/spine.yaml, in Phoenix memory: "load test"
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "(the standard / how it's measured)", "handles 10x load"
- knowledge/technology/validation-floor-profile-benchmarks.md, in Phoenix memory: "The NUMBERS live in the product profile, per product — never in this KB."
- standards/rules/features.md, in Phoenix memory: "A numeric constraint without a source is a hallucination dressed up as a fact."
- standards/rules/pr.md, in Phoenix memory: "path:**/{loadtest,k6,locust,gatling}/**", "Suppressed by default; surfaced only in evidence."
- .garura/product/product-os/software-delivery-planning/environment-setup/fn-declare-environments/feature.md: "such as an environment of its own for performance tests."
- .garura/product/product-os/software-delivery-planning/environment-setup/fn-update-environments/ice.md: "a size fit for the load the tests need"
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md: "The size declared here for each environment is what that cost is worked out for, so a change of size calls for the cost to be worked out again.", "made-up records written for the tests", "no environment's data comes from production."
- .garura/product/product-os/software-delivery-planning/deployment-design/capability.md: "what running the environments in the path costs on each of three clouds", "for the same sizes of use", "This capability says which tests run in which environment and what a change must pass to move on."
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "An unmeasured bar is not a passed bar."
- core/components/skills/check-quality/reference/all-requirements.md: "Load testing tool present in repo or CI pipeline", "At least one load test scenario covers the critical user path", "quality/performance/load-testing-profiling.md"
- docs/philosophy/idd-principles.md: "giving it to the builder only invites teaching-to-the-test."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
