# Feature: Give the accessibility verdict, and send each finding to the developer or to a person

## What it does
Once the tools have run and the walk is done, this feature gives one accessibility verdict for the built work against the product profile's accessibility level and each surface's accessibility guideline, and sends each finding back as a handoff plan, to the developer when the builder can fix it alone or to the product owner when a person must decide, so the product owner knows whether people can use the product in the ways its level and guidelines name, and each part a person cannot use reaches the one who can fix it.
- The verdict gives each part of the pass bar, each capability's accessibility need and each surface's accessibility guideline a pass or a fail, with how it was checked, by a tool or by a person's walk, and where; it names each part not tested or not walked with its reason, and is a pass only when every part passes.
- When the profile sets no accessibility level, no capability has an accessibility need and no surface's guideline names accessibility, the verdict says so, and is neither a pass nor a fail; the product owner sees it.
- When a surface's guideline asks for less than the profile's level, the verdict names it, answers the profile's level on that surface, and sends the gap to the product owner, whose way back is an update of the guideline through Manage surfaces.
- It joins the results of the tools and of the walk with the evidence it takes and does not run again: the record of the review of each change, and the record of the build's separate test run.
- Each finding becomes a handoff plan: what a person cannot do, on which surface and screen, in which way, such as with a keyboard alone or with a screen reader, and the way back, what must be true again, as guidance and never code. It never names the test, its rule, its id or its tool, and never gives a figure measured. For example:
  - in a shop: a shopper using a keyboard alone cannot leave the address field on the checkout page; the keyboard must move on to the next field;
  - in a clinic's booking page: a patient using a screen reader hears each free slot only as a button; each must say its time.
- Who gets it follows the recovery rule's test, whether the builder can fix it from what it already has:
  - the developer, when the way back is a change of the code the builder controls, such as a button with no name a screen reader can read out, or a dialog the keyboard cannot leave;
  - the product owner, when it needs judgment or authority the builder does not hold, such as the colours of the design system that every screen uses, the screen design, a part the builder does not control, for example a payment form another company shows inside the page, a surface's declaration or guideline, a lower accessibility level, or a part not walked because no person was named;
  - a person, whenever it is in doubt.
- The developer gets it through Build the work test first, whose test writer writes a test for it first, as for every handoff plan. After the work was accepted, a finding is a defect for Fix defects test first, which takes in "a finding in a review".
- The product owner decides each finding a person must decide: it is fixed, a surface's guideline is updated through Manage surfaces, the design is updated through Design the work, someone is named to walk, or the accessibility level is moved by an approved decision. Nothing lets a finding through any other way.
- The verdict and the walks' records are kept where no part that builds the work reads them.
- How it meets the capability: every part of the accessibility level and of each surface's guideline gets an answer, and each part a person cannot use goes back without the builder seeing the tests, as Code → Validation asks; it must not "Let a builder grade itself, weaken a check to pass".

Status: not built. What exists covers only part of it:
- The old slice check, /validate-epic, is stale. It gave a verdict, validated or fix required, from all its checks, its page-audit scores among them, and a fix report that "names each failure by check and location", which a handoff plan must not.
- The review of each change ranks an accessibility finding as minor, one that highlights without blocking, and belongs to Check the code against its standards.
- The recovery rule that decides who fixes is written in memory; nothing applies it to an accessibility finding.
- Nothing writes a handoff plan, and where it is kept, and how it reaches the developer, is not decided.

## Inputs / Outputs
- In: the results of the tools and of the walk, with how and where each part was checked, who walked, and each part not tested or not walked, with its reason.
- In: the product profile's accessibility level and pass bar, each capability's accessibility need, each surface's accessibility guideline, and the decisions that moved them.
- In: the record of the review of each change, and the record of the build's separate test run.
- In: the approved screen design, the declared surfaces with their design system, and what the builder controls, to see whether a way back changes them.
- In: whether the work was already accepted.
- Out: the verdict: a pass or a fail for each part, with how and where it was checked, each part not tested or not walked with its reason, each guideline below the profile's level, and whether the whole passed, or that no accessibility level is set.
- Out: for each finding, a handoff plan to the developer through Build the work test first, to the product owner, or, after acceptance, to Fix defects test first as a defect; and, in the verdict, where each one went.

## Rules & behavior
- A pass only when every part passes, and not tested or not walked is a fail. The reason: "An unmeasured bar is not a passed bar.", and a pass on part of the bar is no pass.
- No level set is said plainly, never read as a pass. The reason: the scale starts at none, but a level nobody set was never tested; the product owner approved the same rule for performance, "neither a pass nor a fail".
- The profile's level is the floor on every surface. The reason: a guideline below it is "named as below the profile, and the profile's level stands."
- Records are evidence, not run again. The reason, from the product owner's approved list: "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again."
- What a person cannot do, where and the way back, never the test or its rule. The reason: a handoff plan "never names the failure condition, its id or the check", and the builder never gets the tests' results.
- The way back is guidance, never code. The reason: the way back is "the inverse of the failure, as guidance, never code", and how to build it is the developer's.
- The builder only when it can fix it alone; a person otherwise, and whenever it is in doubt. The reason: the recovery rule's test, "Can the builder fix this from information it already has, deterministically?", and its rule that "any irreversible / outward-facing decision" needs a person.
- A finding whose way back changes the design, a surface's declaration or guideline, or a part the builder does not control goes to the product owner. The reason: each needs a person the builder is not, as "A person confirms each surface, property and guideline" and "the technical lead confirms or changes each choice" of the design; and the product owner approved with Test security on 2026-11-09 "the product owner as the one who gets a finding that changes the architecture".
- Only a person moves the bar. The reason: "The box moves ONLY by an approved decision."
- Before acceptance to the build, after acceptance to the defect fix. The reason: the approved Fix defects test first takes in "a finding in a review", and Build the work test first takes in each handoff plan before acceptance.
- The verdict stays away from the builder. The reason: "giving it to the builder only invites teaching-to-the-test."
- Not decided: where the verdict and the handoff plan are kept, and how a handoff plan reaches the developer.
- Not decided: the rank of each finding, while #934, one severity from P1 to P4 for findings and defects, is open.

## Acceptance criteria
- Given every part passed by the tools but one part a person must check that no person walked, when the verdict is given, then it is not a pass, and the part is named with its reason.
- Given a profile with no accessibility level, no capability with an accessibility need and no guideline that names accessibility, when the verdict is given, then it says no accessibility level is set, and it is neither a pass nor a fail.
- Given a guideline that asks for less than the profile's level, when the verdict is given, then it names the guideline, answers the profile's level on that surface, and sends the gap to the product owner.
- Given a button with no name a screen reader can read out, when the handoff plan is written, then it names the screen and the way back, goes to the developer, and names no test, rule, id or tool.
- Given a finding whose way back is a change of the design system's colours, when it is sent back, then it goes to the product owner and not to the developer.
- Given a finding after the work was accepted, when it is sent back, then it goes to Fix defects test first as a defect.
- Given a verdict, when the inputs of the parts that build the work are checked, then none of them names it.

## Out of scope
- Running the tools and walking the build. Test the running build for accessibility with tools, in the testing environment (fn-test-accessibility-with-tools) and Walk the running build with a keyboard alone and with a screen reader, in the testing environment (fn-walk-with-keyboard-and-screen-reader) do it.
- Fixing a finding. Build the work test first does it before the work is accepted, and Fix defects test first after.
- Updating a surface's guideline or its design system. Manage surfaces does it, after a person's yes.
- Updating the screen design. Design the work does it.
- Setting and moving the accessibility level. Specify the product sets it, and an approved decision moves it.
- Recording a defect in the tracker. Orchestration owns it.
- Running the tests again and counting the rounds. Test accessibility again as the product changes (fn-retest-accessibility) does it.

## Sources
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/bi-4-capability-2/page-approvals.md: "the product owner as the one who gets a finding that changes the architecture"
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/bi-4-capability-3/page-approvals.md: "with the verdict saying so plainly, neither a pass nor a fail, when no performance level is set"
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "Test accessibility, against the product profile's accessibility level and each surface's accessibility guideline.", "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again."
- .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "A person confirms each surface, property and guideline"
- .garura/product/product-os/software-delivery-planning/design-work/capability.md: "the technical lead confirms or changes each choice"
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or merge without a person."
- standards/rules/expectation-generation.md, in Phoenix memory: "Can the builder fix this from information it already has, deterministically?", "any irreversible / outward-facing decision", "the inverse of the failure, as guidance, never code"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The handoff plan never names the failure condition, its id or the check."
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "level scale: none < low < medium < high < xhigh", "The box moves ONLY by an approved decision."
- .garura/product/product-os/_spine.yaml, Garura's own product profile: it holds reliability, maintainability and security, each "level: medium", and no accessibility level.
- .garura/product/product-os/software-delivery-planning/manage-surfaces/fn-declare-surfaces/feature.md: "named as below the profile, and the profile's level stands."
- standards/rules/pr.md, in Phoenix memory: "Missing docs, borderline complexity, accessibility, naming.", "Highlights without blocking."
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "names each failure by check and location", "An unmeasured bar is not a passed bar."
- docs/philosophy/idd-principles.md: "giving it to the builder only invites teaching-to-the-test."
- .garura/product/product-os/software-delivery-planning/fix-defects-test-first/capability.md: "In: taking in a defect reported anywhere: a person's words, a finding in a review, the eval after the work was accepted, or a bug in a plan.", "Out: recording a defect in the tracker"
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-update-tests-and-code/feature.md: "A handoff plan is the exact list of the work it calls for.", "The test writer updates the tests from the changed test writer's part, the updated design or the handoff plan."
- GitHub #934 (open): "Findings and defects get one severity, P1 to P4"
