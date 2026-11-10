# Feature: Walk the running build against its surface and its screen design, in the testing environment

## What it does
Once the built work runs in the testing environment, a person who is not the builder, named by the product owner, uses the slice end to end on its surface the way the person it serves would, at each screen size the surface names, and judges each screen against the surface's properties, its guidelines and the screen design, with the screen design and the tools' pictures beside them, recording what they found, where, and how they walked, so the product owner knows what no tool can tell.
- What the person judges comes only from the surface's properties and guidelines and from the screen design in force. The screen design is what Design the work shows for each screen: wireframes, simple drawings of each screen in Markdown files, or a prototype built with the project's design system. For example:
  - a shop's checkout, whose browser surface reflows one layout across a phone, a tablet and a desktop screen size: at each size, each checkout screen holds what its wireframe shows, and nothing on it is cut off or reached only by scrolling sideways;
  - a clinic's booking page, whose screen design is a prototype: each screen of the build beside the same screen of the prototype, at the same size, shows the same parts of the clinic's design system in the same places;
  - a school's timetable app, whose surface gives tablets a layout of their own: on a tablet, today's lessons show as the tablet's wireframe shows;
  - a team's release command, or a coding agent's play that a person runs in a terminal: it prints what the surface part of the design says, and asks a person a question and reports back the way its guidelines say.
- Beside the screen design. A wireframe in a Markdown file is read beside the picture of the built screen at each size. A prototype is walked with the same steps as the build and pictured at the same sizes, and the two are judged side by side at each step.
- A slice is an ordered group of features that one person can test end to end on one surface, so the walk follows the slice from its first step to its last, as the person it serves would.
- The person walks the copy in the testing environment, with its made-up data and its own test accounts, never production and never a builder's own machine.
- Each walk records who walked, the surface, each step, each screen size, the screen design it was judged against, and what they found at each step, so a second person can walk the same steps and compare.
- A part that a person must judge and that no person walked is named as not walked, never as passed. When no person is named to walk, every such part goes to the product owner.
- One walk may also serve Test accessibility, such as a walk with a keyboard alone at the same sizes. Each capability reads only what its own yardstick names and keeps its own record.
- The walk's record reaches no part that builds the work; a finding reaches the builder only as a handoff plan.
- How it meets the capability: a tool can open a screen at each size and keep its picture, but not tell whether it lays out as its surface says, keeps to the design system or matches its screen design. This feature is the part of the test a person does, so that the verdict answers every part of the surface and the screen design, and not only what a tool can check.

Status: not built. What exists covers only part of it:
- Nothing walks a built product against its surface or its screen design.
- The quality-check runner, a skill that runs each quality check written down for a slice, is built and no live play runs it. Its schema in Phoenix memory keeps the look of a screen for a person, "Design, UX, and security judgment are never runner-owned:", with the example of a check that the layout matches the approved design, judged by a "HITL walk at /launch; fresh-context reviewer on the PR". The runner skips such a check in view, and nothing records what the person found.
- The rebuild eval, a tool that rebuilds a product from the model, has an agent walk the rebuild against what its prototype does, and it leaves layout out on purpose: "Words, layout and design may differ". It tests the product model, not a build.
- The prototype walk already walks a prototype step by step, "click, type, press a key, go back", keeping a picture of each step, at one screen size. It does not walk a built product.
- The stale design play for a slice's screens drew wireframes from a record of each screen; the retired design pipeline's rules, still in Phoenix memory, ask for a wireframe for each screen. Nothing compares a built screen with either.
- No persona in the model walks a build, and nothing names who walks.

## Inputs / Outputs
- In: the slice's surface, who opens it, its properties, such as the screen sizes it serves, its guidelines, such as the design system, and how it is reached in the testing environment.
- In: the screen design in force for the slice's work: the wireframes in Markdown files or the prototype, as the screen design setting says.
- In: the slice's steps, in the order a person does them.
- In: the pictures, the text and the controls the tools kept for each screen at each size, and for a command or a play, what it printed and asked.
- In: the person the product owner named to walk, for the project or for this run.
- In: the testing environment, with its made-up data and its test accounts.
- Out: for each part a person judges, a pass or a fail, with the step, the screen, the size and the screen design it was judged against; who walked; and each part not walked, with its reason, for Give the user experience verdict, and send each finding to the developer or to a person (fn-send-user-experience-findings).

## Rules & behavior
- A person, never the builder. The reason: "A builder believes its own work, so its opinion isn't evidence."
- What a person judges is what the surface's declaration and the screen design name, and a tool's clean run never stands in for it. The reason: the quality-check runner holds that "Human-owned cards are visibly skipped, never judged.", and "An unmeasured bar is not a passed bar."
- The screen design in force is the yardstick, also after an update. A built screen that departs from it with no update the technical lead confirmed is a finding. The reason: "From its confirmation, the updated design is the one in force."
- At each screen size the surface names. The reason: a browser surface's properties include "which screen sizes (viewports) it serves", and in the product owner's words "web would be responsive, adaptive, view ports etc."
- The product owner names who walks. The reason: a part no person walked has a way back only a person can give, and the product owner decides each finding a person must decide.
- The slice end to end, on its one surface. The reason: a slice is what "one person can test end to end on one surface", and the walk proves that person meets what the surface and the screen design promise.
- In the testing environment only. The reason, in the product owner's words: "We are never touching production."; and a builder's machine "is not where the path's tests are counted".
- Each walk is recorded so another person can walk the same steps. The reason: a verdict that a second walk cannot check proves nothing, and Code → Validation's proof is a pass or a fail from a check the builder never saw.
- The record stays away from the builder. The reason: "giving it to the builder only invites teaching-to-the-test."
- What the person judges never comes from what the AI agent knows by itself. The reason: a source in the project or in memory can be checked and read back, while the agent's own knowledge cannot.
- Not decided: whether an agent that is not the builder may first set the pictures beside the screen design and mark where they differ, so the person sees those places first; the person still judges every part. The rebuild eval already has an agent judge a rebuild against a prototype, with layout left out.
- Not decided: how close a built screen must be to a prototype's screen, or to a wireframe, to count as matching, when the screen design does not say.
- Not decided: what a wireframe must show for a person to judge a built screen against it, while Design the work has no agreed standard for a design.
- Not decided: whether the person walks only the slice's steps, or every screen the built work shows.

## Acceptance criteria
- Given a browser surface that names three screen sizes and a screen design of wireframes, when the named person walks the slice in the testing environment, then each screen at each size gets a pass or a fail, with the step, the screen, the size and the wireframe it was judged against.
- Given a pay button that, at the phone size, sits past the edge of the screen, when the walk ends, then that part is failed, with the screen and the size.
- Given a screen design that is a prototype, when the person walks, then each screen of the build is judged beside the same screen of the prototype, at the same size.
- Given a part that a person must judge and no person named to walk, when the run ends, then the part is named as not walked, not as passed, and it goes to the product owner.
- Given a walk, when its record is read, then it names who walked, the surface, each step, each size and what was found.
- Given a second person who walks the same steps at the same sizes on the same built work, when the two records are compared, then each part has the same pass or fail.
- Given a walk's record, when the inputs of the parts that build the work are checked, then none of them names it.

## Out of scope
- Opening each screen at each size and keeping its picture. Test the running build's user experience with tools, in the testing environment (fn-test-user-experience-with-tools) does it.
- Giving the verdict and sending each finding back. Give the user experience verdict, and send each finding to the developer or to a person (fn-send-user-experience-findings) does it.
- A walk with a keyboard alone and with a screen reader, against the accessibility level and each surface's accessibility guideline. Test accessibility does it; one walk may serve both.
- What the product does against each story. The slice's eval tests it.
- User acceptance testing, where users test the product and accept it. Validation → Run owns it.
- Declaring the surface, and writing or updating the screen design. Manage surfaces and Design the work do them.

## Sources
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "Test the user experience on each surface, against the surface's properties and guidelines (for a browser page, how it lays out across screen sizes) and the screen design from Design the work.", "User acceptance testing (planned): Users test the product and accept it."
- The product owner, in .garura/project/issues/1021/context/bi-4-capability-5/page-approvals.md, spelling tidied: "web would be responsive, adaptive, view ports etc.", "We are never touching production."
- The product owner's approval of Test accessibility on 2026-11-09, in .garura/project/issues/1021/context/bi-4-capability-4/page-approvals.md: "the line with the user experience on each surface drawn by the yardstick"
- .garura/product/product-os/intents/bi-4.md: "A builder believes its own work, so its opinion isn't evidence.", "Every expected result has a pass or fail from an eval the builder never saw."
- .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "which screen sizes (viewports) it serves"
- .garura/product/product-os/software-delivery-planning/design-work/capability.md: "either as wireframes, simple drawings of each screen, written in Markdown files, or as a prototype built with the project's design system."
- .garura/product/product-os/software-delivery-planning/design-work/fn-update-work-design/feature.md: "From its confirmation, the updated design is the one in force."
- .garura/product/product-os/software-delivery-planning/design-work/fn-design-chosen-work/feature.md: "Not decided: one standard for a design, with its parts and where it is kept."
- .garura/product/product-os/software-delivery-planning/test-accessibility/fn-walk-with-keyboard-and-screen-reader/feature.md: "Walking the slice against the screen design and how its pages lay out across screen sizes. Test the user experience on each surface does it; one walk may serve both, and each reads only what its own yardstick names."
- .garura/product/product-os/software-delivery-planning/test-product-with-evals/capability.md: "A slice is an ordered group of features that one person can test end to end on one surface"
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md: "is not where the path's tests are counted", "made-up records written for the tests"
- standards/schemas/product-os/lens/quality-gates.yaml, in Phoenix memory: "Design, UX, and security judgment are never runner-owned:", "HITL walk at /launch; fresh-context reviewer on the PR", "Layout matches the UX lens's approved direction"
- core/components/skills/check-quality-gates/SKILL.md: "Human-owned cards are visibly skipped, never judged."
- core/tools/rebuild-eval/prompts/compare.md: "Words, layout and design may differ; judge whether a person can do the same thing and see the same result."
- core/tools/rebuild-eval/README.md: "Design, layout and code may differ; what a person can do and see may not."
- core/components/skills/walk-prototype/SKILL.md: "click, type, press a key, go back"
- core/components/plays/shape-ux-lens/SKILL.md: "waits for the rebuild of the design plays after the shaping loop (#855, ADR 053)"
- standards/rules/design.md, in Phoenix memory: "Every screen MD file has a `## Wireframe` section"
- core/components/plays/validate-epic/SKILL.md: "An unmeasured bar is not a passed bar."
- docs/philosophy/idd-principles.md: "giving it to the builder only invites teaching-to-the-test."
