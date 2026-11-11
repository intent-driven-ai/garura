# Feature: Test the user experience again as the product changes

## What it does
When the built product changes, a surface's properties or guidelines are updated, or the screen design is updated, this feature runs the tools and the walk again on the built work, keeps each run as a new verdict, names each part that passed before and fails now, and sends a finding that keeps coming back to a person once the rounds the project allows are used up.
- The tools run and the person walks again, for example, when:
  - the developer fixed the work from a handoff plan;
  - more work of the product is built, so a screen that laid out well may no longer, such as a checkout page that gains a step for a gift message;
  - a defect found after the work was accepted is fixed;
  - a confirmed update of Manage surfaces changes a surface's properties or guidelines, such as a browser page built for desktop screens that must now serve phones, or a design system that is replaced, so earlier results were checked against another yardstick;
  - a confirmed update of the screen design through Design the work, also when the design is brought up to what the build did after a departure, so the built work is tested against the design now in force.
- Each run answers every property and guideline of the surface and every screen of the screen design, at every size the surface names, as they are now. Each verdict is kept beside the earlier ones and never written over, and a part that passed before and fails now is named as broken by the change.
- A round is one change to the built work and one run of the tools and the walk. When the same finding comes back after the rounds the project allows, the next handoff plan goes to the product owner with each round's verdicts.
- When each run starts belongs to the plan's run: the loop that runs building and validation in rounds, or a person who names the built work.
- How it meets the capability: a pass against a surface and a screen design stays true only while the product passes each time it changes, each time its surface is updated and each time its screen design is updated.

Status: not built. What exists covers only part of it:
- The old slice check, /validate-epic, is stale. It ran in rounds with the build: "Implement ↔ validate is expected to loop — scope narrows per round, 3 rejections halt to a human." It had no check of a layout or a design.
- Manage surfaces plans an update of a surface when the project changes, such as new screen sizes or a new design system, and Design the work plans an update of the design, also after a departure; neither is built.
- Garura's own model declares no surface and holds no screen design, so nothing would run again for it today.
- The loop for this step, /loop-code-validation, is a name only.

## Inputs / Outputs
- In: what changed: a fix from a handoff plan, more work built, a defect fixed, a confirmed update of a surface's properties or guidelines, or a confirmed update of the screen design.
- In: each surface's properties and guidelines as they are now, and the screen design now in force.
- In: the earlier verdicts, with how and where each part was checked, at which size, who walked, and the handoff plans.
- In: the project's setting for how many rounds of the same finding come before a person decides.
- Out: a new verdict for each run, kept beside the earlier ones, with each part that passed before and fails now named.
- Out: once the rounds the project allows are used up, the handoff plan to the product owner, with each round's verdicts.

## Rules & behavior
- Every part as it is now, every time. The reason: a pass on part of the yardstick is no pass, and the yardstick is the surface's and the screen design's as they stand.
- An updated surface is a new test. The reason: an update replaces what held before, and "From its confirmation, the updated surface is the one in force.", so a result checked against the old surface does not answer the new one.
- An updated screen design is a new test. The reason: "From its confirmation, the updated design is the one in force."
- Each verdict is kept, never written over. The reason: the person who decides after the rounds needs the history, as the old slice check gave it: "the escalation record lists each round's findings and fixes."
- Rounds have an end. When the same finding comes back after the rounds the project allows, it goes to a person, not round again to the developer. The reason: the old slice check stopped "after 3 rejections on the same epic".
- The number of rounds is a project setting. The reason: "Everything that can be turned on or off lives in settings." The old slice check uses three; that is what is built, not a rule here.
- The yardstick never moves to let a build pass. The reason: Code → Validation must not "weaken a check to pass".
- When each run starts is the plan's. The reason: running the work is Orchestration's, and the loop for this step, /loop-code-validation, runs the plays of Code → Validation.
- Not decided: which parts run again on each change: every screen at every size and the whole walk, or only what the change could touch. A person's walk costs a person's time each round; the old slice check bounded its re-checks by what changed, and that is not written here as a rule.
- Not decided: what counts as the same finding coming back.

## Acceptance criteria
- Given a checkout page that a shopper had to scroll sideways on a phone, fixed from its handoff plan, when the tools run and the person walks again, then a new verdict is kept beside the first, and it answers every part at every size as it is now.
- Given a confirmed update that adds a phone screen size to a browser surface built for desktop screens, when the tests run again, then each screen is opened and walked at the new size too, and the earlier pass is not kept as the current verdict.
- Given a confirmed update of the screen design, when the tests run again, then each screen is judged against the design now in force.
- Given more work built on a product whose user experience verdict passed before, when the tests run again, then a part that passed before and fails now is named as broken by the change.
- Given the same finding back after the rounds the project allows, when the tests run again, then the next handoff plan goes to the product owner with each round's verdicts, and not to the developer.

## Out of scope
- Fixing the work. Build the work test first does it before the work is accepted, and Fix defects test first after.
- Updating a surface. Manage surfaces does it.
- Updating the screen design. Design the work does it.
- Starting each run, choosing what runs when, and the loop that runs building and validation in rounds. Orchestrate agent work through planning and Run plays as loops own them.
- Opening the screens, walking the build, giving one verdict and writing each handoff plan. The other three features of this capability do them.

## Sources
- The capability list the product owner agreed on 2026-11-03, in .garura/project/issues/1021/context/capabilities.md: "Settings: Everything that can be turned on or off lives in settings.", "Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met."
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or count a check that did not run as a pass."
- .garura/product/product-os/software-delivery-planning/manage-surfaces/fn-update-surfaces/feature.md: "From its confirmation, the updated surface is the one in force.", "a browser page built for desktop screens must now serve phones", "the design system that screens are built from is replaced"
- .garura/product/product-os/software-delivery-planning/design-work/fn-update-work-design/feature.md: "From its confirmation, the updated design is the one in force.", "When the build departs from the design, the design is brought up to what was built, as a new version, once the technical lead confirms it."
- .garura/product/product-os/_spine.yaml: no surface is declared and no part holds a screen design.
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "Implement ↔ validate is expected to loop — scope narrows per round, 3 rejections halt to a human.", "the escalation record lists each round's findings and fixes."
- core/components/plays/validate-epic/reference/ice.md: "C10 — Loop cap: after 3 rejections on the same epic, halt to a human instead of looping", "C6 — Blast-radius scope is drawn from recorded change claims, never invented"
- .garura/project/issues/1021/context/names.md: "/loop-code-validation"
