# Feature: Give the security verdict, and send each finding to the developer or to a person

## What it does
Once the code and the running build are tested, this feature gives one security verdict for the built work against the product profile's security level, and sends each finding back as a handoff plan, to the developer when the builder can fix it alone or to the product owner when a person must decide, so the product owner knows whether the product meets its security level, and each weakness reaches the one who can fix it.
- The verdict gives each part of the pass bar and each capability's security need a pass or a fail, names each part not tested with its reason, and is a pass only when every part passes.
- It joins the findings of the two tests with the evidence it takes and does not run again: the record of the review of each change, and the record of the build's separate test run.
- Each finding becomes a handoff plan: what is weak in the product, where it is, and the way back, what must be true again, as guidance and never code. It never names the test, its rule, its id or its tool, and never holds a secret's value. For example, in a clinic: a signed-in patient can open another patient's booking by changing the booking's number in the page's address; make each patient see only their own bookings.
- Who gets it follows the recovery rule's test, whether the builder can fix it from what it already has:
  - the developer, when the way back is a change of the code the builder controls, such as moving to a library version without the weakness;
  - the product owner, when it needs judgment or authority the builder does not hold, such as a change of the architecture, of the deployment design or of an environment, a secret's value found anywhere, because the secret must be changed where it is kept, or a weakness with no known way back;
  - a person, whenever it is in doubt.
- The developer gets it through Build the work test first, whose test writer writes a test for it first, as for every handoff plan. After the work was accepted, a finding is a defect for Fix defects test first, which takes in "a finding in a review".
- The product owner decides each finding a person must decide: it is fixed, or the security level is moved by an approved decision. Nothing lets a finding through any other way.
- The verdict is kept where no part that builds the work reads it, and it holds no secret's value.
- How it meets the capability: every part of the pass bar gets an answer, and each weakness goes back without the builder seeing the tests, as Code → Validation asks; it must not "Let a builder grade itself, weaken a check to pass".

Status: not built. What exists covers only part of it:
- The review of each change gives a verdict on that change: a reject "if any P1 finding (or a runnable suite is red)", each finding citing its file and line. It belongs to Check the code against its standards, and its findings name the rule.
- The old slice check, /validate-epic, is stale. It gave a verdict, validated or fix required, and a fix report that "names each failure by check and location", which a handoff plan must not.
- The recovery rule that decides who fixes is written in memory; nothing applies it to a security finding.
- Nothing writes a handoff plan, and where it is kept, and how it reaches the developer, is not decided.

## Inputs / Outputs
- In: the findings and results of the test of the code and of the test of the running build.
- In: the product profile's security level and pass bar, each capability's security need, and the decisions that moved them.
- In: the record of the review of each change, and the record of the build's separate test run.
- In: the approved architecture and deployment design, to see whether a way back changes them.
- In: whether the work was already accepted.
- Out: the verdict: a pass or a fail for each part of the pass bar and each security need, each part not tested with its reason, and whether the whole passed.
- Out: for each finding, a handoff plan to the developer through Build the work test first, to the product owner, or, after acceptance, to Fix defects test first as a defect; and, in the verdict, where each one went.

## Rules & behavior
- A pass only when every part passes, and not tested is a fail. The reason: "An unmeasured bar is not a passed bar.", and a pass on part of the bar is no pass.
- Records are evidence, not run again. The reason, from the product owner's approved list: "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again."
- The weakness, where it is and the way back, never the test. The reason: a handoff plan "never names the failure condition, its id or the check", and a weakness in the code cannot be fixed without knowing where it is.
- The way back is guidance, never code. The reason: the way back is "the inverse of the failure, as guidance, never code", and how to build it is the developer's.
- The builder only when it can fix it alone; a person otherwise, and whenever it is in doubt. The reason: the recovery rule's test, "Can the builder fix this from information it already has, deterministically?", and its rule that "any irreversible / outward-facing decision" needs a person.
- A secret's value found is always a person's. The reason: the builder holds no secret, since a builder's machine "holds only made-up data and no secret's value", and a secret must be changed where the deployment design keeps it, outside the code.
- The person who decides is the product owner. The reason: the product owner set the security level through the profile, and "A capability need above the box stops for the product owner".
- Only a person moves the bar. The reason: "The box moves ONLY by an approved decision."
- Before acceptance to the build, after acceptance to the defect fix. The reason: the approved Fix defects test first takes in "a finding in a review", and Build the work test first takes in each handoff plan before acceptance.
- The verdict stays away from the builder. The reason: with "security scan results", "giving it to the builder only invites teaching-to-the-test."
- A finding whose way back changes the architecture, the deployment design or an environment goes to the product owner, not to the technical lead or the devops engineer. The reason: the product owner approved it with the capability on 2026-11-09, "the product owner as the one who gets a finding that changes the architecture".
- Not decided: where the verdict and the handoff plan are kept, and how a handoff plan reaches the developer.
- Not decided: the rank of each finding, while #934, one severity from P1 to P4 for findings and defects, is open.

## Acceptance criteria
- Given every part of the pass bar passed but one part not tested, when the verdict is given, then it is not a pass, and the part is named with its reason.
- Given a library version with a known weakness and a version without it, when the handoff plan is written, then it names the library, where it is used and the way back, goes to the developer, and names no test, rule, id or tool.
- Given a secret's value found in a settings file, when the handoff plan is written, then it goes to the product owner, names where the value was found, and holds no value.
- Given a finding whose way back changes the deployment design, when it is sent back, then it goes to a person and not to the developer.
- Given a finding after the work was accepted, when it is sent back, then it goes to Fix defects test first as a defect.
- Given a verdict, when the inputs of the parts that build the work are checked, then none of them names it.

## Out of scope
- Running the tests. Test the built code, its settings and its libraries for security weaknesses (fn-test-code-security) and Test the running build for security in the testing environment (fn-test-running-security) do it.
- Fixing a finding. Build the work test first does it before the work is accepted, and Fix defects test first after.
- Setting and moving the security level. Specify the product sets it, and an approved decision moves it.
- Recording a defect in the tracker. Orchestration owns it.
- Running the tests again and counting the rounds. Test security again as the product changes (fn-retest-security) does it.

## Sources
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/bi-4-capability-2/page-approvals.md: "the product owner as the one who gets a finding that changes the architecture"
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "Test security, against the product profile's security level.", "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again."
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or merge without a person."
- standards/rules/expectation-generation.md, in Phoenix memory: "Can the builder fix this from information it already has, deterministically?", "any irreversible / outward-facing decision", "the inverse of the failure, as guidance, never code"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The handoff plan never names the failure condition, its id or the check."
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "The box moves ONLY by an approved decision."
- .garura/product/product-os/decisions/dec-cap-initialize-security-none-medium.yaml: "A capability need above the box stops for the product owner"
- core/components/plays/check-change/SKILL.md: "if any P1 finding (or a runnable suite is red)"
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "names each failure by check and location", "An unmeasured bar is not a passed bar."
- docs/philosophy/idd-principles.md: "security scan results", "giving it to the builder only invites teaching-to-the-test."
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md: "holds only made-up data and no secret's value"
- .garura/product/product-os/software-delivery-planning/deployment-design/capability.md: "The design names only where each secret is kept.", "the devops engineer, who decides how the project runs, is tested and is released"
- .garura/product/product-os/software-delivery-planning/fix-defects-test-first/capability.md: "In: taking in a defect reported anywhere: a person's words, a finding in a review, the eval after the work was accepted, or a bug in a plan.", "Out: recording a defect in the tracker"
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-update-tests-and-code/feature.md: "A handoff plan is the exact list of the work it calls for.", "The test writer updates the tests from the changed test writer's part, the updated design or the handoff plan."
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "the architect, who decides the project's architecture and its technology"
- .garura/product/product-os/software-delivery-planning/domain.md: "the technical lead, who designs it"
- GitHub #934 (open): "Findings and defects get one severity, P1 to P4"
