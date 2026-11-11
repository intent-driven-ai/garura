# Feature: Check the code again as the product and its standards change

## What it does
When a change is fixed after its review, more work is built, a standard changes, or an approved decision raises a level, this feature reviews the change again or checks the whole built work again, keeps each run as a new verdict, names each standard that passed before and fails now, and sends a finding that keeps coming back to a person once the rounds the project allows are used up.
- The checks run again, for example, when:
  - the developer or the test writer fixed a change from its handoff plans and raised it again;
  - more work of the product is built, so the whole built work may no longer keep to a bar that held before, such as a size limit for each part of the code;
  - a defect found after the work was accepted is fixed;
  - a standard changes by its owner's confirmed update: a rule of the review, a project's coding standard, the architecture, such as one deployable unit split into services, or the design of the work, so earlier results were checked against another yardstick;
  - an approved decision raises the maintainability or the reliability level, such as a payments product moving maintainability from medium to high.
- Each run answers every standard as it is now. Each verdict is kept beside the earlier ones and never written over, and a standard that passed before and fails now is named as broken by the change.
- A round is one change to the code and one run of the review or the check. When the same finding comes back after the rounds the project allows, the next handoff plan goes to the product owner with each round's verdicts.
- When each run starts belongs to the plan's run: the loop that runs building and validation in rounds, a person who raises a change again, or a person who names the built work.
- How it meets the capability: a pass against the project's standards stays true only while the code passes each time it changes, each time a standard changes, and each time a level is raised.

Status: built in part. The review of each change runs again on a change raised again after its findings were fixed, and posts the current decision. Not built:
- Each run writes over the last one's record: a run again "re-posts the current decision rather than adding a conflicting second one", and earlier rounds are kept only where someone saved them by hand.
- Nothing counts rounds, or sends a finding that keeps coming back to a person.
- Nothing checks the whole built work again when more work is built, when a standard changes, or when a level is raised; the whole-work check is not built.
- The old slice check, /validate-epic, is stale. It ran in rounds with the build: "3 rejections halt to a human."
- The loop for this step, /loop-code-validation, is a name only.

## Inputs / Outputs
- In: what changed: a fix from a handoff plan, more work built, a defect fixed, a standard's confirmed update, or an approved decision on a level.
- In: the standards and the levels as they are now.
- In: the earlier verdicts, with how and where each standard was checked, and the handoff plans.
- In: the project's setting for how many rounds of the same finding come before a person decides.
- Out: a new verdict for each run, kept beside the earlier ones, with each standard that passed before and fails now named.
- Out: once the rounds the project allows are used up, the handoff plan to the product owner, with each round's verdicts.

## Rules & behavior
- Every standard as it is now, every time. The reason: a pass on part of the yardstick is no pass, and the yardstick is the standards as they stand.
- An updated standard is a new check. The reason: an update replaces what held before, and for the design, "From its confirmation, the updated design is the one in force."
- A raised level is a new check. The reason: "The box moves ONLY by an approved decision.", so a result checked against the old level does not answer the new one.
- Each verdict is kept, never written over. The reason: the person who decides after the rounds needs the history, as the old slice check gave it: "the escalation record lists each round's findings and fixes."
- Rounds have an end. When the same finding comes back after the rounds the project allows, it goes to a person, not round again to the developer. The reason: the old slice check stopped "after 3 rejections on the same epic".
- The number of rounds is a project setting. The reason: "Everything that can be turned on or off lives in settings." The old slice check uses three; that is what is built, not a rule here.
- The yardstick never moves to let code pass. The reason: Code → Validation must not "weaken a check to pass".
- When each run starts is the plan's. The reason: running the work is Orchestration's, and the loop for this step, /loop-code-validation, runs the plays of Code → Validation.
- Not decided: which parts of the whole built work are checked again on each change: all of it, or only what the change could touch.
- Not decided: what counts as the same finding coming back.

## Acceptance criteria
- Given a change rejected for a search query built from what a shopper typed, fixed from its handoff plan and raised again, when it is reviewed again, then a new verdict is kept beside the first.
- Given more work built on a product whose whole built work passed before, when it is checked again, then a standard that passed before and fails now is named as broken by the change.
- Given a confirmed update of the architecture, when the whole built work is checked again, then it is checked against the architecture now in force, and the earlier pass is not kept as the current verdict.
- Given an approved decision that raises the maintainability level, when the whole built work is checked again, then it is checked against the new level and its pass bar.
- Given the same finding back after the rounds the project allows, when the review runs again, then the next handoff plan goes to the product owner with each round's verdicts, and not to the developer.

## Out of scope
- Fixing the code. Build the work test first does it before the work is accepted, and Fix defects test first after.
- Updating a standard, the architecture or the design, or moving a level. Their owners do it, after a person's yes.
- Starting each run, choosing what runs when, and the loop that runs building and validation in rounds. Orchestrate agent work through planning and Run plays as loops own them.
- Reviewing a change, checking the whole built work, giving one verdict and writing each handoff plan. The other three features of this capability do them.

## Sources
- The capability list the product owner agreed on 2026-11-03, in .garura/project/issues/1021/context/capabilities.md: "Settings: Everything that can be turned on or off lives in settings.", "Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met."
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or merge without a person."
- .garura/product/product-os/software-delivery-planning/design-work/fn-update-work-design/feature.md: "From its confirmation, the updated design is the one in force."
- core/components/plays/check-change/SKILL.md: "re-posts the current decision rather than adding a conflicting second one"
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "3 rejections halt to a human.", "the escalation record lists each round's findings and fixes."
- core/components/plays/validate-epic/reference/ice.md: "C10 — Loop cap: after 3 rejections on the same epic, halt to a human instead of looping"
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "The box moves ONLY by an approved decision."
- .garura/project/issues/1021/context/names.md: "/loop-code-validation"
