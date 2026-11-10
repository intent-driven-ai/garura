# Feature: Give the user experience verdict, and send each finding to the developer or to a person

## What it does
Once the tools have run and the walk is done, this feature gives one user experience verdict for the built work against each surface's properties and guidelines and the screen design in force, and sends each finding back as a handoff plan, to the developer when the builder can fix it alone or to the product owner when a person must decide, so the product owner knows whether a person meets on each surface what its declaration promises and what its screen design shows, and each difference reaches the one who can fix it.
- The verdict gives each property and guideline of the surface, and each screen of the screen design at each size the surface names, a pass or a fail, with how it was checked, by a tool or by a person's walk, and where; it names each part not tested or not walked with its reason, and is a pass only when every part passes.
- When no surface is declared and the work has no screen design, the verdict says so, and is neither a pass nor a fail; the product owner sees it. When only one of the two is there, that one is tested, and the verdict names the other as missing.
- It joins the results of the tools and of the walk with the evidence it takes and does not run again: the record of the review of each change, and the record of the build's separate test run.
- Each finding becomes a handoff plan: what a person meets that differs from the surface or the screen design, on which surface and screen and at which size, and the way back, what must be true again, as guidance and never code. It never names the test, its rule, its id or its tool, never gives a figure measured, and never hands over a picture the test kept. For example:
  - in a shop: on a phone-size screen, a shopper must scroll sideways to reach the pay button on the checkout page; the page must fit the phone's width, as one layout that reflows;
  - in a clinic's booking page: the button that confirms a visit is not the design system's main button that the screen design shows; it must be;
  - in a coding agent's play: it asks two things in one question; it must ask one thing at a time, as its surface's guideline says.
- Who gets it follows the recovery rule's test, whether the builder can fix it from what it already has:
  - the developer, when the way back is a change of the code the builder controls, such as a page that does not reflow, or a screen built from a part other than the one the design system has for it;
  - the product owner, when it needs judgment or authority the builder does not hold, such as a design system that has no part the screen design needs, a screen design that cannot fit the smallest size its surface names, a part the builder does not control, for example a map another company shows inside the page, a surface's declaration, property or guideline, a built screen that departed from the design with no update confirmed, or a part not walked because no person was named;
  - a person, whenever it is in doubt.
- The developer gets it through Build the work test first, whose test writer writes a test for it first, as for every handoff plan. After the work was accepted, a finding is a defect for Fix defects test first, which takes in "a finding in a review".
- The product owner decides each finding a person must decide: it is fixed, a surface is updated through Manage surfaces, the design is updated through Design the work, or someone is named to walk. Nothing lets a finding through any other way.
- The verdict and the walks' records are kept where no part that builds the work reads them.
- How it meets the capability: every part of each surface and of the screen design gets an answer, and each difference goes back without the builder seeing the tests, as Code → Validation asks; it must not "Let a builder grade itself, weaken a check to pass".

Status: not built. What exists covers only part of it:
- The old slice check, /validate-epic, is stale. It gave a verdict, validated or fix required, from all its checks, with a fix report that "names each failure by check and location", which a handoff plan must not. It had no check of a layout or a design.
- The review of each change has a row that matches a colour, a padding or a margin written as a fixed value in the lines a change adds; it belongs to Check the code against its standards.
- The recovery rule that decides who fixes is written in memory; nothing applies it to a user experience finding.
- Nothing writes a handoff plan, and where it is kept, and how it reaches the developer, is not decided.

## Inputs / Outputs
- In: the results of the tools and of the walk, with how and where each part was checked, at which size, who walked, and each part not tested or not walked, with its reason.
- In: the declared surfaces with their properties and guidelines, and the confirmed updates of them.
- In: the screen design in force, with its confirmed updates, and what the builder controls, to see whether a way back changes them.
- In: the record of the review of each change, and the record of the build's separate test run.
- In: whether the work was already accepted.
- Out: the verdict: a pass or a fail for each part, with how and where it was checked, each part not tested or not walked with its reason, and whether the whole passed, or that nothing is declared to test against.
- Out: for each finding, a handoff plan to the developer through Build the work test first, to the product owner, or, after acceptance, to Fix defects test first as a defect; and, in the verdict, where each one went.

## Rules & behavior
- A pass only when every part passes, and not tested or not walked is a fail. The reason: "An unmeasured bar is not a passed bar.", and a pass on part of the yardstick is no pass.
- Nothing declared is said plainly, never read as a pass. The reason: a surface nobody declared and a design nobody wrote were never tested; the product owner approved the same rule for performance, "neither a pass nor a fail".
- Records are evidence, not run again. The reason, from the product owner's approved list: "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again."
- What a person meets, where and the way back, never the test or its rule. The reason: a handoff plan "never names the failure condition, its id or the check", and the builder never gets the tests' results.
- The way back is guidance, never code. The reason: the way back is "the inverse of the failure, as guidance, never code", and how to build it is the developer's.
- The builder only when it can fix it alone; a person otherwise, and whenever it is in doubt. The reason: the recovery rule's test, "Can the builder fix this from information it already has, deterministically?", and its rule that "any irreversible / outward-facing decision" needs a person.
- A finding whose way back changes the design system, the screen design, a surface's declaration, property or guideline, or a part the builder does not control goes to the product owner. The reason: each needs a person the builder is not, as "A person confirms each surface, property and guideline" and "the technical lead confirms or changes each choice" of the design; and the product owner approved with Test accessibility that "a finding about the design system's colours or the screen design goes to the product owner".
- Only a person moves the yardstick. The reason: a surface changes only when "A person confirms each update.", and the design only from its confirmation: "From its confirmation, the updated design is the one in force."
- Before acceptance to the build, after acceptance to the defect fix. The reason: the approved Fix defects test first takes in "a finding in a review", and Build the work test first takes in each handoff plan before acceptance.
- The verdict stays away from the builder. The reason: "giving it to the builder only invites teaching-to-the-test."
- Not decided: where the verdict and the handoff plan are kept, and how a handoff plan reaches the developer.
- Not decided: the rank of each finding, while #934, one severity from P1 to P4 for findings and defects with a layer for each kind of surface, is open.

## Acceptance criteria
- Given every screen opened by the tools but one part a person must judge that no person walked, when the verdict is given, then it is not a pass, and the part is named with its reason.
- Given no surface declared and no screen design, when the verdict is given, then it says nothing is declared to test against, and it is neither a pass nor a fail.
- Given a checkout page that a shopper must scroll sideways on a phone-size screen, when the handoff plan is written, then it names the screen, the size and the way back, goes to the developer, and names no test, rule, id, tool or figure, and holds no picture.
- Given a finding whose way back is a part the design system does not have, when it is sent back, then it goes to the product owner and not to the developer.
- Given a built screen that departs from the screen design with no confirmed update, when it is sent back, then it goes to the product owner.
- Given a finding after the work was accepted, when it is sent back, then it goes to Fix defects test first as a defect.
- Given a verdict, when the inputs of the parts that build the work are checked, then none of them names it.

## Out of scope
- Opening each screen at each size and walking the build. Test the running build's user experience with tools, in the testing environment (fn-test-user-experience-with-tools) and Walk the running build against its surface and its screen design, in the testing environment (fn-walk-against-screen-design) do it.
- Fixing a finding. Build the work test first does it before the work is accepted, and Fix defects test first after.
- Updating a surface's properties, its guidelines or its design system. Manage surfaces does it, after a person's yes.
- Updating the screen design. Design the work does it, after the technical lead's yes.
- Recording a defect in the tracker. Orchestration owns it.
- Running the tests again and counting the rounds. Test the user experience again as the product changes (fn-retest-user-experience) does it.

## Sources
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/bi-4-capability-4/page-approvals.md: "a finding about the design system's colours or the screen design goes to the product owner"
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/bi-4-capability-3/page-approvals.md: "with the verdict saying so plainly, neither a pass nor a fail, when no performance level is set"
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again."
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or merge without a person."
- .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "A person confirms each surface, property and guideline"
- .garura/product/product-os/software-delivery-planning/manage-surfaces/fn-update-surfaces/feature.md: "A person confirms each update."
- .garura/product/product-os/software-delivery-planning/design-work/capability.md: "the technical lead confirms or changes each choice"
- .garura/product/product-os/software-delivery-planning/design-work/fn-update-work-design/feature.md: "From its confirmation, the updated design is the one in force."
- .garura/product/product-os/software-delivery-planning/fix-defects-test-first/capability.md: "In: taking in a defect reported anywhere: a person's words, a finding in a review, the eval after the work was accepted, or a bug in a plan.", "Out: recording a defect in the tracker"
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-update-tests-and-code/feature.md: "A handoff plan is the exact list of the work it calls for."
- standards/rules/expectation-generation.md, in Phoenix memory: "Can the builder fix this from information it already has, deterministically?", "any irreversible / outward-facing decision", "the inverse of the failure, as guidance, never code"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The handoff plan never names the failure condition, its id or the check."
- standards/rules/pr.md, in Phoenix memory, the review's row on fixed values: "padding:\s*[0-9]+px"
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "names each failure by check and location", "An unmeasured bar is not a passed bar."
- docs/philosophy/idd-principles.md: "giving it to the builder only invites teaching-to-the-test."
- GitHub #934 (open): "Findings and defects get one severity, P1 to P4", "mobile (a misalignment can be P2 on a phone)", "a coding agent (output a person cannot read or act on is at least P2; the same feedback given again raises it)"
