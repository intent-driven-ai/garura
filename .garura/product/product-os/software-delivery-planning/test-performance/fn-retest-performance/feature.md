# Feature: Test performance again as the product changes

## What it does
When the built product changes, the performance level it must meet goes up, or the environment it is measured in changes size, this feature runs the performance tests again on the built work, keeps each run as a new verdict, names each part that passed before and fails now, and sends a finding that keeps coming back to a person once the rounds the project allows are used up.
- The tests run again, for example, when:
  - the developer fixed the work from a handoff plan;
  - more work of the product is built, so a page or an endpoint that was fast may now be slow;
  - a defect found after the work was accepted is fixed;
  - an approved decision raises the profile's performance level or a capability's performance need, so the built work is measured against the new level, and an earlier pass no longer counts;
  - a confirmed update of Environment setup changes the size of the environment the tests run in, so earlier figures were measured in other conditions.
- Each run answers every part of the pass bar as it is now, in the conditions it names. Each verdict is kept beside the earlier ones and never written over, and a part that passed before and fails now is named as broken by the change.
- A round is one change to the built work and one run of the tests. When the same finding comes back after the rounds the project allows, the next handoff plan goes to the product owner with each round's verdicts.
- When each run starts belongs to the plan's run: the loop that runs building and validation in rounds, or a person who names the built work.
- How it meets the capability: a pass against the performance level stays true only while the product passes each time it changes, each time the level it must meet goes up, and each time the place it is measured in changes.

Status: not built. What exists covers only part of it:
- The old slice check, /validate-epic, is stale. It ran in rounds with the build, its page audits among its checks: "Implement ↔ validate is expected to loop — scope narrows per round, 3 rejections halt to a human."
- Garura's own profile sets no performance level, so nothing would run again for it today.
- The loop for this step, /loop-code-validation, is a name only.

## Inputs / Outputs
- In: what changed: a fix from a handoff plan, more work built, a defect fixed, an approved decision that raised the performance level or a capability's performance need, or a confirmed change of the size of the environment the tests run in.
- In: the product profile's performance level and pass bar as they are now, and each capability's performance need.
- In: the earlier verdicts, with their conditions, and the handoff plans.
- In: the project's setting for how many rounds of the same finding come before a person decides.
- Out: a new verdict for each run, kept beside the earlier ones, with each part that passed before and fails now named.
- Out: once the rounds the project allows are used up, the handoff plan to the product owner, with each round's verdicts.

## Rules & behavior
- Every part of the pass bar as it is now, every time, in the conditions it names. The reason: a pass on part of the bar is no pass, and the bar is the profile's as it stands.
- A raised level is a new test. The reason: "The box moves ONLY by an approved decision.", and a pass against the old level says nothing of the new one.
- A changed environment is a new test. The reason: a figure counts only for the conditions it was measured in, and Environment setup applies a change of size, "such as a bigger size", to that environment alone.
- Each verdict is kept, never written over. The reason: the person who decides after the rounds needs the history, as the old slice check gave it: "the escalation record lists each round's findings and fixes."
- Rounds have an end. When the same finding comes back after the rounds the project allows, it goes to a person, not round again to the developer. The reason: the old slice check stopped "after 3 rejections on the same epic".
- The number of rounds is a project setting. The reason: "Everything that can be turned on or off lives in settings." The old slice check uses three; that is what is built, not a rule here.
- The bar never moves to let a build pass. The reason: Code → Validation must not "weaken a check to pass".
- When each run starts is the plan's. The reason: running the work is Orchestration's, and the loop for this step, /loop-code-validation, runs the plays of Code → Validation.
- Not decided: which tests run again on each change: all of them, or only those the change could touch. The old slice check bounded its re-checks by what changed; that is not written here as a rule.
- Not decided: what counts as the same finding coming back.

## Acceptance criteria
- Given a slow part fixed from its handoff plan, when the tests run again, then a new verdict is kept beside the first, and it answers every part of the pass bar in the conditions it names.
- Given an approved decision that raises the performance level from medium to high, when the tests run again, then the built work is measured against the pass bar of the high level, and the earlier pass is not kept as the current verdict.
- Given more work built on a product whose performance verdict passed before, when the tests run again, then a part that passed before and fails now is named as broken by the change.
- Given a confirmed update that makes the environment for load tests bigger, when the tests run again, then the new figures name the new size, and the earlier ones keep theirs.
- Given the same finding back after the rounds the project allows, when the tests run again, then the next handoff plan goes to the product owner with each round's verdicts, and not to the developer.

## Out of scope
- Fixing the work. Build the work test first does it before the work is accepted, and Fix defects test first after.
- Changing an environment's size. Environment setup does it.
- Starting each run, choosing what runs when, and the loop that runs building and validation in rounds. Orchestrate agent work through planning and Run plays as loops own them.
- Setting and moving the performance level. Specify the product sets it, and an approved decision moves it.
- Measuring, giving one verdict and writing each handoff plan. The other three features of this capability do them.

## Sources
- The capability list the product owner agreed on 2026-11-03, in .garura/project/issues/1021/context/capabilities.md: "Settings: Everything that can be turned on or off lives in settings.", "Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met."
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or count a check that did not run as a pass."
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "The box moves ONLY by an approved decision."
- .garura/product/product-os/_spine.yaml, Garura's own product profile: it holds reliability, maintainability and security, each "level: medium", and no performance level.
- .garura/product/product-os/software-delivery-planning/environment-setup/fn-build-environment/feature.md: "A confirmed update of its declaration, such as a bigger size, is applied to that environment only"
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "Implement ↔ validate is expected to loop — scope narrows per round, 3 rejections halt to a human.", "the escalation record lists each round's findings and fixes."
- core/components/plays/validate-epic/reference/ice.md: "C10 — Loop cap: after 3 rejections on the same epic, halt to a human instead of looping", "C6 — Blast-radius scope is drawn from recorded change claims, never invented"
- .garura/project/issues/1021/context/names.md: "/loop-code-validation"
