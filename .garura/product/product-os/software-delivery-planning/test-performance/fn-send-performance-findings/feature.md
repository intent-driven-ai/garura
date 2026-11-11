# Feature: Give the performance verdict, and send each finding to the developer or to a person

## What it does
Once the running build is measured, this feature gives one performance verdict for the built work against the product profile's performance level, and sends each finding back as a handoff plan, to the developer when the builder can fix it alone or to the product owner when a person must decide, so the product owner knows whether the product meets its performance level, and each slow part reaches the one who can fix it.
- The verdict gives each part of the pass bar and each capability's performance need a pass or a fail, with the conditions it was measured in, names each part not measured with its reason, and is a pass only when every part passes.
- When the profile sets no performance level and no capability has a performance need, the verdict says so, and is neither a pass nor a fail; the product owner sees it.
- It joins the figures of the two measuring features with the evidence it takes and does not run again: the record of the review of each change, and the record of the build's separate test run.
- Each finding becomes a handoff plan: what is slow, on which surface and in what conditions, and the way back, what must be true again, as guidance and never code. It never names the test, its rule, its id or its tool, and never gives the figures measured. For example, in a shop: the order history page is slower than the level allows when a shopper has many orders; load the orders a page at a time.
- Who gets it follows the recovery rule's test, whether the builder can fix it from what it already has:
  - the developer, when the way back is a change of the code the builder controls, such as a database query that runs once for each item in a list;
  - the product owner, when it needs judgment or authority the builder does not hold, such as a change of the architecture, for example a cache or another service, a change of the deployment design, a change of an environment, for example more copies of a service or a bigger data store, a lower performance level, or a part not measured because the environment cannot give its conditions;
  - a person, whenever it is in doubt.
- The developer gets it through Build the work test first, whose test writer writes a test for it first, as for every handoff plan. After the work was accepted, a finding is a defect for Fix defects test first, which takes in "a finding in a review".
- The product owner decides each finding a person must decide: it is fixed, the environment is changed through Environment setup, or the performance level is moved by an approved decision. Nothing lets a finding through any other way.
- The verdict is kept where no part that builds the work reads it.
- How it meets the capability: every part of the pass bar gets an answer in the conditions it names, and each slow part goes back without the builder seeing the tests, as Code → Validation asks; it must not "Let a builder grade itself, weaken a check to pass".

Status: not built. What exists covers only part of it:
- The old slice check, /validate-epic, is stale. It gave a verdict, validated or fix required, from all its checks, and a fix report that "names each failure by check and location", which a handoff plan must not.
- The review of each change marks a performance finding at most as one that highlights without blocking, and belongs to Check the code against its standards.
- The recovery rule that decides who fixes is written in memory; nothing applies it to a performance finding.
- Nothing writes a handoff plan, and where it is kept, and how it reaches the developer, is not decided.

## Inputs / Outputs
- In: the figures, passes, fails and conditions of the two measuring features, and each part they did not measure, with its reason.
- In: the product profile's performance level and pass bar, each capability's performance need, and the decisions that moved them.
- In: the record of the review of each change, and the record of the build's separate test run.
- In: the approved architecture, the deployment design and the environments' declarations, to see whether a way back changes them.
- In: whether the work was already accepted.
- Out: the verdict: a pass or a fail for each part of the pass bar and each performance need, with its conditions, each part not measured with its reason, and whether the whole passed, or that no performance level is set.
- Out: for each finding, a handoff plan to the developer through Build the work test first, to the product owner, or, after acceptance, to Fix defects test first as a defect; and, in the verdict, where each one went.

## Rules & behavior
- A pass only when every part passes, and not measured is a fail. The reason: "An unmeasured bar is not a passed bar.", and a pass on part of the bar is no pass.
- No level set is said plainly, never read as a pass. The reason: the scale starts at none, but a level nobody set was never measured, and "An unmeasured bar is not a passed bar."
- Records are evidence, not run again. The reason, from the product owner's approved list: "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again."
- What is slow, where and the way back, never the test or the figures. The reason: a handoff plan "never names the failure condition, its id or the check", and the builder never gets the tests' results.
- The way back is guidance, never code. The reason: the way back is "the inverse of the failure, as guidance, never code", and how to build it is the developer's.
- The builder only when it can fix it alone; a person otherwise, and whenever it is in doubt. The reason: the recovery rule's test, "Can the builder fix this from information it already has, deterministically?", and its rule that "any irreversible / outward-facing decision" needs a person.
- A finding whose way back changes the architecture, the deployment design or an environment goes to the product owner. The reason: the product owner approved it with Test security on 2026-11-09, "the product owner as the one who gets a finding that changes the architecture".
- A part not measured because the environment cannot give its conditions goes to the product owner. The reason: its way back changes an environment, which Environment setup owns, or the pass bar, which only an approved decision moves.
- Only a person moves the bar. The reason: "The box moves ONLY by an approved decision."
- Before acceptance to the build, after acceptance to the defect fix. The reason: the approved Fix defects test first takes in "a finding in a review", and Build the work test first takes in each handoff plan before acceptance.
- The verdict stays away from the builder. The reason: "giving it to the builder only invites teaching-to-the-test."
- Not decided: whether the test also finds where in the code the time goes, so a handoff plan can name it.
- Not decided: where the verdict and the handoff plan are kept, and how a handoff plan reaches the developer.
- Not decided: the rank of each finding, while #934, one severity from P1 to P4 for findings and defects, is open.

## Acceptance criteria
- Given every part of the pass bar passed but one part not measured, when the verdict is given, then it is not a pass, and the part is named with its reason.
- Given a profile with no performance level and no capability with a performance need, when the verdict is given, then it says no performance level is set, and it is neither a pass nor a fail.
- Given a slow page whose way back is to read the data once instead of once for each item, when the handoff plan is written, then it names the page, the conditions and the way back, goes to the developer, and names no test, rule, id, tool or figure.
- Given a finding whose way back is more copies of a service in the environment, when it is sent back, then it goes to the product owner and not to the developer.
- Given a finding after the work was accepted, when it is sent back, then it goes to Fix defects test first as a defect.
- Given a verdict, when the inputs of the parts that build the work are checked, then none of them names it.

## Out of scope
- Measuring the running build. Measure how fast the running build answers, in the testing environment (fn-test-running-speed) and Measure how fast the running build answers under the load the pass bar names (fn-test-under-load) do it.
- Fixing a finding. Build the work test first does it before the work is accepted, and Fix defects test first after.
- Changing an environment's size. Environment setup does it, after a person's yes.
- Setting and moving the performance level. Specify the product sets it, and an approved decision moves it.
- Recording a defect in the tracker. Orchestration owns it.
- Running the tests again and counting the rounds. Test performance again as the product changes (fn-retest-performance) does it.

## Sources
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/bi-4-capability-2/page-approvals.md: "the product owner as the one who gets a finding that changes the architecture"
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "Test performance, against the product profile's performance level.", "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again."
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or count a check that did not run as a pass."
- standards/rules/expectation-generation.md, in Phoenix memory: "Can the builder fix this from information it already has, deterministically?", "any irreversible / outward-facing decision", "the inverse of the failure, as guidance, never code"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The handoff plan never names the failure condition, its id or the check."
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "level scale: none < low < medium < high < xhigh", "The box moves ONLY by an approved decision."
- .garura/product/product-os/_spine.yaml, Garura's own product profile: it holds reliability, maintainability and security, each "level: medium", and no performance level.
- standards/rules/pr.md, in Phoenix memory: "Highlights without blocking."
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "names each failure by check and location", "An unmeasured bar is not a passed bar."
- docs/philosophy/idd-principles.md: "giving it to the builder only invites teaching-to-the-test."
- .garura/product/product-os/software-delivery-planning/environment-setup/fn-update-environments/feature.md: "When the project needs another environment, or an environment's data, size, network, access or settings must change, a person confirms an update, and what held before stays readable with why it changed."
- .garura/product/product-os/software-delivery-planning/fix-defects-test-first/capability.md: "In: taking in a defect reported anywhere: a person's words, a finding in a review, the eval after the work was accepted, or a bug in a plan.", "Out: recording a defect in the tracker"
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-update-tests-and-code/feature.md: "A handoff plan is the exact list of the work it calls for.", "The test writer updates the tests from the changed test writer's part, the updated design or the handoff plan."
- GitHub #934 (open): "Findings and defects get one severity, P1 to P4"
