# Feature: Walk the running build with a keyboard alone and with a screen reader, in the testing environment

## What it does
Once the built work runs in the testing environment, a person who is not the builder, named by the product owner, uses the slice end to end on its surface the way a person who needs it would, with a keyboard alone, with a screen reader and in any other way the surface's accessibility guideline names, such as with larger text, and records what they could and could not do, where, and how they walked, so the product owner knows what no tool can tell.
- What the person checks comes only from the pass bar, each capability's accessibility need and the surface's accessibility guideline, which say for each part that a person checks it. For example:
  - a shop's checkout: every step can be done with a keyboard alone, with no field the keyboard cannot leave, and a screen reader reads out each error so the shopper knows what to fix;
  - a clinic's booking page: a patient who cannot see the screen books a visit with a screen reader alone;
  - a school's timetable app for phones: a pupil who uses the phone's screen reader finds today's lessons and the room for each;
  - a team's command-line tool: what its guideline says a person checks; a command line whose guideline names nothing for accessibility is named as not tested.
- A slice is an ordered group of features that one person can test end to end on one surface, so the walk follows the slice from its first step to its last, as the person it serves would.
- The person walks the copy in the testing environment, with its made-up data and its own test accounts, never production and never a builder's own machine.
- Each walk records who walked, the surface, each step, the way it was walked, such as a keyboard alone or a screen reader and which one, and what they found at each step, so a second person can walk the same steps and compare.
- A part that a person must check and that no person walked is named as not walked, never as passed. When no person is named to walk, every such part goes to the product owner.
- The walk's record reaches no part that builds the work; a finding reaches the builder only as a handoff plan.
- How it meets the capability: a tool cannot tell whether a person can do each step of the slice in the way they need to. This feature is the part of the test that a person does, so that the verdict answers every part of the accessibility level, and not only what a tool can check.

Status: not built. What exists covers only part of it:
- Nothing walks a built product for accessibility. Memory's one learning on accessibility asks for a person's pass with a keyboard and a screen reader beside automated checks; nothing runs one.
- The quality-check runner, a skill that runs each quality check written down for a slice, is built and no live play runs it. It skips a check a person owns, in view, and names who judges it; nothing records what that person found. Its schema's example of such a check is a walk by a person at the old acceptance step.
- The retired design pipeline's screen pages, whose rules are still in Phoenix memory, held an accessibility section for each screen, with lines such as "Keyboard navigation through all form fields"; nothing walks a built screen against them.
- An agent can already press keys in a browser: the prototype walk clicks, types and presses a key, step by step, to understand a prototype. It does not test accessibility.
- No persona in the model walks a build, and nothing names who walks.

## Inputs / Outputs
- In: the product profile's accessibility level and pass bar with how it is checked, and each capability's accessibility need.
- In: the slice's surface, who opens it, its accessibility guideline, and how it is reached in the testing environment.
- In: the slice's steps, in the order a person does them.
- In: the person the product owner named to walk, for the project or for this run.
- In: the testing environment, with its made-up data and its test accounts.
- Out: for each part a person checks, a pass or a fail, with the step, the screen and the way it was walked; who walked; and each part not walked, with its reason, for Give the accessibility verdict, and send each finding to the developer or to a person (fn-send-accessibility-findings).

## Rules & behavior
- A person, never the builder. The reason: "A builder believes its own work, so its opinion isn't evidence."
- What a person checks is what the pass bar, a need or the guideline says a person checks, and a tool's clean run never stands in for it. The reason: the quality-check runner holds that "Human-owned cards are visibly skipped, never judged.", and "An unmeasured bar is not a passed bar."
- The product owner names who walks. The reason: a part no person walked has a way back only a person can give, and the product owner decides each finding a person must decide.
- The slice end to end, on its one surface. The reason: a slice is what "one person can test end to end on one surface", and the walk proves that person can.
- In the testing environment only. The reason, in the product owner's words: "We are never touching production."; and a builder's machine "is not where the path's tests are counted".
- Each walk is recorded so another person can walk the same steps. The reason: a verdict that a second walk cannot check proves nothing, and Code → Validation's proof is a pass or a fail from a check the builder never saw.
- The record stays away from the builder. The reason: "giving it to the builder only invites teaching-to-the-test."
- What the person checks never comes from what the AI agent knows by itself. The reason: a source in the project or in memory can be checked and read back, while the agent's own knowledge cannot.
- Not decided: whether an agent that is not the builder may do the keyboard-alone part of the walk, as the prototype walk presses keys in a browser, leaving only the screen reader to a person.
- Not decided: whether the person walks only the slice's steps, or every screen the built work shows.
- Not decided: which screen reader, browser or phone the walk uses when the guideline does not name them.

## Acceptance criteria
- Given a browser guideline that says a person checks that each step works with a keyboard alone, when the named person walks the slice in the testing environment, then each step gets a pass or a fail, with the step, the screen and the way it was walked.
- Given a step where the keyboard cannot leave a field, when the walk ends, then that part is failed and the step is named.
- Given a part that a person must check and no person named to walk, when the run ends, then the part is named as not walked, not as passed, and it goes to the product owner.
- Given a walk, when its record is read, then it names who walked, the surface, each step, the way it was walked and what was found.
- Given a second person who walks the same steps on the same built work, when the two records are compared, then each part has the same pass or fail.
- Given a walk's record, when the inputs of the parts that build the work are checked, then none of them names it.

## Out of scope
- Running the tools. Test the running build for accessibility with tools, in the testing environment (fn-test-accessibility-with-tools) does it.
- Giving the verdict and sending each finding back. Give the accessibility verdict, and send each finding to the developer or to a person (fn-send-accessibility-findings) does it.
- Walking the slice against the screen design and how its pages lay out across screen sizes. Test the user experience on each surface does it; one walk may serve both, and each reads only what its own yardstick names.
- User acceptance testing, where users test the product and accept it. Validation → Run owns it.
- Declaring the surface and its accessibility guideline. Manage surfaces does it.

## Sources
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "Test accessibility, against the product profile's accessibility level and each surface's accessibility guideline.", "User acceptance testing (planned): Users test the product and accept it."
- The product owner on 2026-11-07, in .garura/project/issues/1021/context/bi-4-capability-4/page-approvals.md: "We are never touching production."
- .garura/product/product-os/intents/bi-4.md: "A builder believes its own work, so its opinion isn't evidence.", "Every expected result has a pass or fail from an eval the builder never saw."
- knowledge/technology/ux-accessibility-floor.md, in Phoenix memory: "automated checks (axe) in CI plus a manual keyboard + screen-reader pass on key flows."
- standards/schemas/product-os/lens/quality-gates.yaml, in Phoenix memory: "machine | human", "HITL walk at /launch; fresh-context reviewer on the PR"
- core/components/skills/check-quality-gates/SKILL.md: "Human-owned cards are visibly skipped, never judged.", "visibly skipped; the card's `review` line names the edge that judges it"
- standards/rules/design.md, in Phoenix memory: "A screen without an accessibility section is assumed inaccessible."
- standards/schemas/screen-inventory.yaml, in Phoenix memory: "Keyboard navigation through all form fields", "Screen reader announcements for validation errors"
- .garura/product/product-os/software-delivery-planning/design-work/capability.md: "An older, retired design pipeline wrote one Markdown file for each screen with its wireframe. Its rules are still in Phoenix memory."
- core/components/skills/walk-prototype/SKILL.md: "click, type, press a key, go back"
- .garura/product/product-os/software-delivery-planning/test-product-with-evals/capability.md: "A slice is an ordered group of features that one person can test end to end on one surface"
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md: "is not where the path's tests are counted", "made-up records written for the tests"
- core/components/plays/validate-epic/SKILL.md: "An unmeasured bar is not a passed bar."
- docs/philosophy/idd-principles.md: "giving it to the builder only invites teaching-to-the-test."
