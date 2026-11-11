# Feature: Test the running build for security in the testing environment

## What it does
Once the built work runs in the testing environment, this feature tries on the product's declared surfaces what the pass bar and each capability's security need say to try, the way a person or another system meets the product there, and records a pass or a fail for each, so the product owner knows that the product keeps its security level when it runs, not only in its code.
- What it tries comes from the pass bar and from each capability's security need, which says its target and how it is checked. For example:
  - a team's command-line tool that writes to the team's tracker: nothing is written before a person's typed yes, checked against a test tracker organization;
  - a clinic's booking page: one signed-in test patient cannot open another test patient's booking;
  - a shop's endpoint that another system calls: a request with no valid key is refused.
- It reaches the running build only on its declared surfaces, as a person or another system would, with the testing environment's made-up data and its own test accounts.
- A test that needs a secret, such as a test account's password or the key another system uses, takes it at run time from where the deployment design keeps the testing environment's secrets, and writes its value nowhere.
- It never tries anything outside the testing environment: not production, not a builder's own machine, and no system the testing environment does not hold, such as a payment provider's live service.
- Each try is a pass or a fail against what its part of the pass bar or its security need says, with what was seen. A part that no try can reach, or that memory holds no test for, is named as not tested, never as passed.
- How it meets the capability: the product owner moved "Security testing (planned): The product is tested for security before it runs." here, and his list assumed that these tests run "in the testing environment Environment setup declares, never in production." This feature is that test of the running product.

Status: not built. What exists covers only part of it:
- Nothing tests a running build for security. The old slice check, /validate-epic, which is stale, tested the code only: "No penetration-style probing of running systems."
- Garura's own profile already has a pass bar that is a test of the running product, "no tracker or mapping write before the typed yes, on a test GitHub organization; no write to Phoenix memory or another project's memory", and its one capability with a security need says how it is checked: "run initialize on a test GitHub organization with a missing type, answer no, and check the tracker's type list and the mapping are unchanged". Nothing runs either.
- No testing environment is declared or built, and nothing says which tests run in which environment, because Environment setup and Deployment design are not built.
- The old release play, also stale, read secrets from where they were kept and wrote no value: "secrets are read from the manager and no secret literal appears in the logs, the deploy record, or the repo."
- No memory tier holds what a security test of a running product must try.

## Inputs / Outputs
- In: the product profile's security level and pass bar, and each capability's security need with its target and how it is checked.
- In: the declared surfaces, and how each one is reached in the testing environment.
- In: the testing environment, as Environment setup declares and builds it, with its made-up data and its test accounts.
- In: where the deployment design keeps the testing environment's secrets, and which tests it places there.
- Out: a pass or a fail for each part of the pass bar and each security need it tries, with what was seen, and each part not tried, with its reason, for Give the security verdict, and send each finding to the developer or to a person (fn-send-security-findings).

## Rules & behavior
- In the testing environment only. The reason, in the product owner's words: "We are never touching production."; the assumption recorded with his list; and a builder's machine "is not where the path's tests are counted".
- Nothing outside the testing environment. The reason: the old slice check ruled out "probing of running systems" altogether; this feature may try only the copy that was set up to be tested.
- Made-up data and test accounts only. The reason: each environment holds its own data, "such as made-up records written for the tests", and "no environment's data comes from production."
- Secrets at run time, never written. The reason: "The design names only where each secret is kept.", and the old release play's rule that "no secret literal appears in the logs, the deploy record, or the repo."
- What to try comes from the pass bar and the security needs, never from what the AI agent knows by itself. The reason: the pass bar is set for each product through its profile, and Specify the product sets each capability's need with "a target someone can measure and how it is checked".
- Not tested is never passed. The reason: "An unmeasured bar is not a passed bar."
- A part that is not the builder runs it, and the builder never sees what was tried. The reason: with "security scan results", "giving it to the builder only invites teaching-to-the-test."
- Not decided: how the test reaches each surface of the running build: through the slice's usage guide, as the eval does, or through what the deployment design records for each surface.
- Not decided: what a running test must try for a pass bar that names a security standard. No memory tier holds it, so it waits for research that a person approves as a memory update.
- Not decided: where the test runs while no testing environment is declared, as today.

## Acceptance criteria
- Given a pass bar that says nothing is written to the tracker before a person's typed yes, when the test runs the tool against a test tracker organization and answers no, then it checks that the tracker is unchanged and records a pass or a fail.
- Given a capability's security need that says one signed-in person cannot open another person's records, when the test tries it with two test accounts, then it records a pass or a fail with what was seen.
- Given a test that needs a test account's password, when it runs, then it takes the password from where the deployment design keeps the testing environment's secrets, and no record or log holds the value.
- Given a try that would reach a system the testing environment does not hold, when the test runs, then that try is not made and the part is named as not tested.
- Given a part of the pass bar that memory holds no test for, when the test ends, then the part is named as not tested, and not as passed.

## Out of scope
- Testing the code at rest. Test the built code, its settings and its libraries for security weaknesses (fn-test-code-security) does it.
- Declaring and building the testing environment, its data and its test accounts. Environment setup does it.
- Keeping the testing environment's secrets, and placing the tests in environments. Deployment design does it.
- Giving the verdict and sending each finding back. Give the security verdict, and send each finding to the developer or to a person (fn-send-security-findings) does it.
- A person's acceptance walk, and taking accepted changes along the path. User acceptance testing and Continuous delivery, in Validation → Run, do them.

## Sources
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "Test security, against the product profile's security level. Moved here from Validation → Run.", "Assumed: security and performance tests run in the testing environment Environment setup declares, never in production."
- The same file, the line moved here: "Security testing (planned): The product is tested for security before it runs."
- The product owner on 2026-11-07, in .garura/project/issues/1021/context/bi-4-capability-2/page-approvals.md: "We are never touching production."
- .garura/product/product-os/_spine.yaml, Garura's own product profile and its capability with a security need: "no tracker or mapping write before the typed yes, on a test GitHub organization; no write to Phoenix memory or another project's memory", "run initialize on a test GitHub organization with a missing type, answer no, and check the tracker's type list and the mapping are unchanged"
- .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-capabilities/feature.md: "a target someone can measure and how it is checked"
- .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "A surface is a place where a person, or another system, opens the product to use it."
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md: "is not where the path's tests are counted", "such as made-up records written for the tests", "no environment's data comes from production."
- .garura/product/product-os/software-delivery-planning/deployment-design/capability.md: "The design names only where each secret is kept.", "This capability says which tests run in which environment and what a change must pass to move on."
- core/components/plays/validate-epic/reference/ice.md: "No penetration-style probing of running systems."
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "An unmeasured bar is not a passed bar."
- core/components/plays/release-increment/reference/ice.md: "secrets are read from the manager and no secret literal appears in the logs, the deploy record, or the repo."
- core/components/plays/release-increment/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)"
- docs/philosophy/idd-principles.md: "security scan results", "giving it to the builder only invites teaching-to-the-test."
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-write-usage-guide/feature.md: "Matching each name in the eval to the guide, running the eval, and giving the verdict."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
