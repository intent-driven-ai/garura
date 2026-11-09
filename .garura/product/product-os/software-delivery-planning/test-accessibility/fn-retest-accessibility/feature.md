# Feature: Test accessibility again as the product changes

## What it does
When the built product changes, the accessibility level it must meet goes up, or a surface's accessibility guideline is updated, this feature runs the tools and the walk again on the built work, keeps each run as a new verdict, names each part that passed before and fails now, and sends a finding that keeps coming back to a person once the rounds the project allows are used up.
- The tools run and the person walks again, for example, when:
  - the developer fixed the work from a handoff plan;
  - more work of the product is built, so a page, a screen or a step that was usable may no longer be;
  - a defect found after the work was accepted is fixed;
  - an approved decision raises the profile's accessibility level or a capability's accessibility need, so the built work is tested against the new level, and an earlier pass no longer counts;
  - a confirmed update of Manage surfaces changes a surface's accessibility guideline or the design system its screens are built from, so earlier results were checked against another yardstick.
- Each run answers every part of the pass bar, each capability's accessibility need and each surface's accessibility guideline as they are now. Each verdict is kept beside the earlier ones and never written over, and a part that passed before and fails now is named as broken by the change.
- A round is one change to the built work and one run of the tools and the walk. When the same finding comes back after the rounds the project allows, the next handoff plan goes to the product owner with each round's verdicts.
- When each run starts belongs to the plan's run: the loop that runs building and validation in rounds, or a person who names the built work.
- How it meets the capability: a pass against the accessibility level stays true only while the product passes each time it changes, each time the level it must meet goes up, and each time a surface's guideline changes.

Status: not built. What exists covers only part of it:
- The old slice check, /validate-epic, is stale. It ran in rounds with the build, its page audits among its checks: "Implement ↔ validate is expected to loop — scope narrows per round, 3 rejections halt to a human."
- Manage surfaces plans that a raised accessibility level proposes an update of each surface's accessibility guideline; it is not built.
- Garura's own profile sets no accessibility level, so nothing would run again for it today.
- The loop for this step, /loop-code-validation, is a name only.

## Inputs / Outputs
- In: what changed: a fix from a handoff plan, more work built, a defect fixed, an approved decision that raised the accessibility level or a capability's accessibility need, or a confirmed update of a surface's accessibility guideline or design system.
- In: the product profile's accessibility level and pass bar as they are now, each capability's accessibility need, and each surface's accessibility guideline as it is now.
- In: the earlier verdicts, with how each part was checked and who walked, and the handoff plans.
- In: the project's setting for how many rounds of the same finding come before a person decides.
- Out: a new verdict for each run, kept beside the earlier ones, with each part that passed before and fails now named.
- Out: once the rounds the project allows are used up, the handoff plan to the product owner, with each round's verdicts.

## Rules & behavior
- Every part as it is now, every time. The reason: a pass on part of the bar is no pass, and the bar is the profile's and the guideline's as they stand.
- A raised level is a new test. The reason: "The box moves ONLY by an approved decision.", and a pass against the old level says nothing of the new one.
- An updated guideline is a new test. The reason: Manage surfaces proposes "the accessibility guideline of each surface it touches" at a raised level, and a result checked against the old guideline does not answer the new one.
- Each verdict is kept, never written over. The reason: the person who decides after the rounds needs the history, as the old slice check gave it: "the escalation record lists each round's findings and fixes."
- Rounds have an end. When the same finding comes back after the rounds the project allows, it goes to a person, not round again to the developer. The reason: the old slice check stopped "after 3 rejections on the same epic".
- The number of rounds is a project setting. The reason: "Everything that can be turned on or off lives in settings." The old slice check uses three; that is what is built, not a rule here.
- The bar never moves to let a build pass. The reason: Code → Validation must not "weaken a check to pass".
- When each run starts is the plan's. The reason: running the work is Orchestration's, and the loop for this step, /loop-code-validation, runs the plays of Code → Validation.
- Not decided: which parts run again on each change: all the tools and the whole walk, or only what the change could touch. A person's walk costs a person's time each round; the old slice check bounded its re-checks by what changed, and that is not written here as a rule.
- Not decided: what counts as the same finding coming back.

## Acceptance criteria
- Given a dialog the keyboard could not leave, fixed from its handoff plan, when the tools run and the person walks again, then a new verdict is kept beside the first, and it answers every part as it is now.
- Given an approved decision that raises the accessibility level from medium to high, when the tests run again, then the built work is tested against the pass bar of the high level, and the earlier pass is not kept as the current verdict.
- Given a confirmed update that changes a browser surface's accessibility guideline, when the tests run again, then each part is answered against the updated guideline.
- Given more work built on a product whose accessibility verdict passed before, when the tests run again, then a part that passed before and fails now is named as broken by the change.
- Given the same finding back after the rounds the project allows, when the tests run again, then the next handoff plan goes to the product owner with each round's verdicts, and not to the developer.

## Out of scope
- Fixing the work. Build the work test first does it before the work is accepted, and Fix defects test first after.
- Updating a surface's accessibility guideline. Manage surfaces does it.
- Starting each run, choosing what runs when, and the loop that runs building and validation in rounds. Orchestrate agent work through planning and Run plays as loops own them.
- Setting and moving the accessibility level. Specify the product sets it, and an approved decision moves it.
- Running the tools, walking the build, giving one verdict and writing each handoff plan. The other three features of this capability do them.

## Sources
- The capability list the product owner agreed on 2026-11-03, in .garura/project/issues/1021/context/capabilities.md: "Settings: Everything that can be turned on or off lives in settings.", "Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met."
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or merge without a person."
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "The box moves ONLY by an approved decision."
- .garura/product/product-os/_spine.yaml, Garura's own product profile: it holds reliability, maintainability and security, each "level: medium", and no accessibility level.
- .garura/product/product-os/software-delivery-planning/manage-surfaces/fn-update-surfaces/feature.md: "Given an accessibility level that rose in the product profile, when an update is proposed, then the accessibility guideline of each surface it touches is proposed at the new level.", "the design system that screens are built from is replaced"
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "Implement ↔ validate is expected to loop — scope narrows per round, 3 rejections halt to a human.", "the escalation record lists each round's findings and fixes."
- core/components/plays/validate-epic/reference/ice.md: "C10 — Loop cap: after 3 rejections on the same epic, halt to a human instead of looping", "C6 — Blast-radius scope is drawn from recorded change claims, never invented"
- .garura/project/issues/1021/context/names.md: "/loop-code-validation"
