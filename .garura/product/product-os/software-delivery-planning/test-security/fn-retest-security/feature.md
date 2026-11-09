# Feature: Test security again as the product changes

## What it does
When the built product changes, or the security level it must meet goes up, this feature runs the security tests again on the built work, keeps each run as a new verdict, names each part that passed before and fails now, and sends a finding that keeps coming back to a person once the rounds the project allows are used up.
- The tests run again, for example, when:
  - the developer fixed the work from a handoff plan;
  - more work of the product is built;
  - a defect found after the work was accepted is fixed;
  - an approved decision raises the profile's security level or a capability's security need, so the built work is tested against the new level, and an earlier pass no longer counts.
- Each run answers every part of the pass bar as it is now. Each verdict is kept beside the earlier ones and never written over, and a part that passed before and fails now is named as broken by the change.
- A round is one change to the built work and one run of the tests. When the same finding comes back after the rounds the project allows, the next handoff plan goes to the product owner with each round's verdicts.
- When each run starts belongs to the plan's run: the loop that runs building and validation in rounds, or a person who names the built work.
- How it meets the capability: a pass against the security level stays true only while the product passes each time it changes, and each time the level it must meet goes up.

Status: not built. What exists covers only part of it:
- The old slice check, /validate-epic, is stale. It ran in rounds with the build, its security pass among its checks: "Implement ↔ validate is expected to loop — scope narrows per round, 3 rejections halt to a human."
- Garura's own security level was raised from none to medium by an approved decision, so that "a later capability's security need is compared against medium, not none"; nothing tests the built product against either level.
- The loop for this step, /loop-code-validation, is a name only.

## Inputs / Outputs
- In: what changed: a fix from a handoff plan, more work built, a defect fixed, or an approved decision that raised the security level or a capability's security need.
- In: the product profile's security level and pass bar as they are now, and each capability's security need.
- In: the earlier verdicts and handoff plans.
- In: the project's setting for how many rounds of the same finding come before a person decides.
- Out: a new verdict for each run, kept beside the earlier ones, with each part that passed before and fails now named.
- Out: once the rounds the project allows are used up, the handoff plan to the product owner, with each round's verdicts.

## Rules & behavior
- Every part of the pass bar as it is now, every time. The reason: a pass on part of the bar is no pass, and the bar is the profile's as it stands.
- A raised level is a new test. The reason: "The box moves ONLY by an approved decision.", and after a move a capability's need "is compared against medium, not none", so a pass against the old level says nothing of the new one.
- Each verdict is kept, never written over. The reason: the person who decides after the rounds needs the history, as the old slice check gave it: "the escalation record lists each round's findings and fixes."
- Rounds have an end. When the same finding comes back after the rounds the project allows, it goes to a person, not round again to the developer. The reason: the old slice check stopped "after 3 rejections on the same epic".
- The number of rounds is a project setting. The reason: "Everything that can be turned on or off lives in settings." The old slice check uses three; that is what is built, not a rule here.
- The bar never moves to let a build pass. The reason: Code → Validation must not "weaken a check to pass".
- When each run starts is the plan's. The reason: running the work is Orchestration's, and the loop for this step, /loop-code-validation, runs the plays of Code → Validation.
- Not decided: which tests run again on each change: all of them on the whole built work, or only those the change could touch. The old slice check bounded its re-checks by what changed; that is not written here as a rule.
- Not decided: what counts as the same finding coming back.

## Acceptance criteria
- Given a finding fixed from its handoff plan, when the tests run again, then a new verdict is kept beside the first, and it answers every part of the pass bar.
- Given an approved decision that raises the security level from medium to high, when the tests run again, then the built work is tested against the pass bar of the high level, and the earlier pass is not kept as the current verdict.
- Given more work built on a product whose security verdict passed before, when the tests run again, then a part that passed before and fails now is named as broken by the change.
- Given the same finding back after the rounds the project allows, when the tests run again, then the next handoff plan goes to the product owner with each round's verdicts, and not to the developer.

## Out of scope
- Fixing the work. Build the work test first does it before the work is accepted, and Fix defects test first after.
- Starting each run, choosing what runs when, and the loop that runs building and validation in rounds. Orchestrate agent work through planning and Run plays as loops own them.
- Setting and moving the security level. Specify the product sets it, and an approved decision moves it.
- Running the tests, giving one verdict and writing each handoff plan. The other three features of this capability do them.

## Sources
- The capability list the product owner agreed on 2026-11-03, in .garura/project/issues/1021/context/capabilities.md: "Settings: Everything that can be turned on or off lives in settings.", "Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met."
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or merge without a person."
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "The box moves ONLY by an approved decision."
- .garura/product/product-os/decisions/dec-cap-initialize-security-none-medium.yaml: "a later capability's security need is compared against medium, not none"
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "Implement ↔ validate is expected to loop — scope narrows per round, 3 rejections halt to a human.", "the escalation record lists each round's findings and fixes."
- core/components/plays/validate-epic/reference/ice.md: "C10 — Loop cap: after 3 rejections on the same epic, halt to a human instead of looping", "C6 — Blast-radius scope is drawn from recorded change claims, never invented"
- .garura/project/issues/1021/context/names.md: "/loop-code-validation"
