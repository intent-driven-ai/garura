# Feature: Measure how fast the running build answers, in the testing environment

## What it does
Once the built work runs in the testing environment, this feature measures on each declared surface, by a part that is not the builder, what the pass bar and each capability's performance need name, as one person or one other system meets the product there, and records each figure with the conditions it was measured in, so the product owner knows how fast the product answers against its performance level.
- What it measures comes only from the pass bar and from each capability's performance need, which says its target and how it is checked. For example:
  - a shop's product page: how long the page takes to load, on the kind of device and connection the pass bar names;
  - a clinic's booking endpoint that another system calls: how long it takes to answer a request for free slots;
  - a team's command-line tool: how long a command takes to finish on a project of the size the need names;
  - a team's support assistant, an agent that answers customers' emails: how long it takes to reply.
- How many tries a measure takes, and which figure of them counts, come from how the pass bar says it is measured, for example the time that 95 of 100 tries come in under. A part whose pass bar does not say how it is measured is named as not measured.
- Each run uses the same conditions, and records them: the environment and its declared size, its made-up data, the surface, and the tries. A second run on the same built work repeats them, so the two can be compared.
- It reaches the running build only on its declared surfaces, with the testing environment's made-up data and its own test accounts. A test that needs a secret, such as a test account's password, takes it at run time from where the deployment design keeps the testing environment's secrets, and writes its value nowhere.
- Each figure is compared with its part of the pass bar or its performance need. A tool's own score counts only when the pass bar names that score. One run of a page-audit tool may also give an accessibility figure; this feature keeps only the figures the performance pass bar names.
- A part that the environment cannot give the conditions for, such as an amount of data it does not hold, or that no way of measuring is known for, is named as not measured with its reason, never as passed.
- How it meets the capability: the product owner moved "Performance testing (planned): The product is tested for how it performs." here, and his list assumed that these tests run "in the testing environment Environment setup declares, never in production." This feature is that test of how fast the running product answers.

Status: not built. What exists covers only part of it:
- The old slice check, /validate-epic, is stale. Its page-audit runner, a "frontend audit tool class (lighthouse, pa11y, axe).", ran only on a local page, "Code-level + local-page audits only (C5).", read every score the audit gave, so one run could give both a performance score and an accessibility score, and compared each with a target written for the slice. A target with no number was only checked to be there.
- The quality auditor, an agent, can "Run Lighthouse audits (if threshold defined and URL provided)" when a check asks; only the stale plays ask.
- Nothing measures how fast an endpoint answers, a command finishes or an agent replies.
- Garura's own profile sets no performance level, and no capability in its model has a performance need.
- No testing environment is declared or built, because Environment setup is not built.
- No memory tier holds what a performance test must measure for any kind of product, or how many tries a measure takes.

## Inputs / Outputs
- In: the product profile's performance level and pass bar with how it is measured, and each capability's performance need with its target and how it is checked.
- In: the declared surfaces, and how each one is reached in the testing environment.
- In: the testing environment, as Environment setup declares and builds it, with its size, its made-up data and its test accounts.
- In: where the deployment design keeps the testing environment's secrets, and which tests it places there.
- Out: for each part of the pass bar and each performance need it measures, the figure, the pass or the fail, and the conditions it was measured in; and each part not measured, with its reason, for Give the performance verdict, and send each finding to the developer or to a person (fn-send-performance-findings).

## Rules & behavior
- In the testing environment only. The reason, in the product owner's words: "We are never touching production."; the assumption recorded with his list; and a builder's machine "is not where the path's tests are counted".
- What to measure, and how, comes from the pass bar and the performance needs, never from what the AI agent knows by itself. The reason: "The NUMBERS live in the product profile, per product — never in this KB.", and "A numeric constraint without a source is a hallucination dressed up as a fact."
- The same conditions each run, recorded with each figure. The reason: the pass bar is "(the standard / how it's measured)", and a figure without its conditions cannot be repeated or compared.
- A tool's own score is not the verdict. The reason: "Green is the entry condition, never the verdict".
- Not measured is never passed. The reason: "An unmeasured bar is not a passed bar."
- Only the performance figures. The reason: the approved list tests performance "against the product profile's performance level" and accessibility against its own level, so a tool is not a capability.
- Made-up data, test accounts, and secrets at run time, never written. The reason: each environment holds "made-up records written for the tests", and "The design names only where each secret is kept."
- A part that is not the builder measures, and the builder never sees the figures. The reason: a result checked after the work exists is a failure condition, and "giving it to the builder only invites teaching-to-the-test."
- Not decided: how the test reaches each surface of the running build: through the slice's usage guide, as the eval does, or through what the deployment design records for each surface.
- Not decided: whether a project setting gives the tries and the figure that counts where a pass bar does not say how it is measured.
- Not decided: where the test runs while no testing environment is declared, as today.

## Acceptance criteria
- Given a pass bar that says how long a page may take to load and how that time is measured, when the test runs in the testing environment, then it records the figure, a pass or a fail, and the environment, its size, its data and the tries.
- Given a command-line tool whose capability's performance need names how long a command may take on a project of a named size, when the test runs, then it measures the command on made-up data of that size and records a pass or a fail.
- Given a pass bar that does not say how its time is measured, when the test ends, then the part is named as not measured, and not as passed.
- Given a page-audit run that gives a performance score and an accessibility score, when the figures are recorded, then only the figures the performance pass bar names are kept here.
- Given two runs on the same built work in the same conditions, when their records are read, then they name the same conditions, and each part has the same pass or fail.

## Out of scope
- Measuring under the load the pass bar names. Measure how fast the running build answers under the load the pass bar names (fn-test-under-load) does it.
- Giving the verdict and sending each finding back. Give the performance verdict, and send each finding to the developer or to a person (fn-send-performance-findings) does it.
- A speed line in a story's expectations. The slice's eval tests it, in Test what the product does, with evals the builder never sees.
- The accessibility figures of a page audit. Test accessibility reads them.
- Declaring and building the testing environment, its data and its test accounts. Environment setup does it.

## Sources
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "Test performance, against the product profile's performance level. Moved here from Validation → Run.", "Assumed: security and performance tests run in the testing environment Environment setup declares, never in production.", "Test accessibility, against the product profile's accessibility level and each surface's accessibility guideline."
- The same file, the line moved here: "Performance testing (planned): The product is tested for how it performs."
- The product owner on 2026-11-07, in .garura/project/issues/1021/context/bi-4-capability-3/page-approvals.md: "We are never touching production."
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "speed/latency", "p99 page load", "(the standard / how it's measured)"
- standards/rules/epics.md, in Phoenix memory, the shape of a measure in a story: "p95 under 500ms"
- .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-capabilities/feature.md: "a target someone can measure and how it is checked"
- .garura/product/product-os/_spine.yaml, Garura's own product profile: it holds reliability, maintainability and security, each "level: medium", and no performance level.
- knowledge/technology/validation-floor-profile-benchmarks.md, in Phoenix memory: "The NUMBERS live in the product profile, per product — never in this KB."
- standards/rules/features.md, in Phoenix memory: "A numeric constraint without a source is a hallucination dressed up as a fact."
- core/components/plays/validate-epic/scripts/runners/runner_frontend.py: "frontend audit tool class (lighthouse, pa11y, axe).", "Code-level + local-page audits only (C5)."
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "An unmeasured bar is not a passed bar."
- core/components/plays/validate-epic/reference/ice.md: "Green is the entry condition, never the verdict"
- core/components/agents/quality-auditor.md: "Run Lighthouse audits (if threshold defined and URL provided)"
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md: "is not where the path's tests are counted", "made-up records written for the tests"
- .garura/product/product-os/software-delivery-planning/deployment-design/capability.md: "The design names only where each secret is kept.", "This capability says which tests run in which environment and what a change must pass to move on."
- .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "A surface is a place where a person, or another system, opens the product to use it."
- docs/philosophy/idd-principles.md: "giving it to the builder only invites teaching-to-the-test."
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-write-usage-guide/feature.md: "Matching each name in the eval to the guide, running the eval, and giving the verdict."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
