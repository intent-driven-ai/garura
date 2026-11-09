# Feature: Run the evals again as the product changes

## What it does
When the built product changes, this feature runs the evals again: a slice's whole eval after its work is fixed or more of it is built, and the evals of the slices that passed before, so that nothing that passed breaks; and when the same failure comes back after the rounds the project allows, it goes to a person instead of round again to the builder.
- The built product changes, for example, when:
  - the developer fixed the work from a handoff plan;
  - another story of the slice is built;
  - another slice is built on the same product;
  - a defect found after the work was accepted is fixed.
- Each run is a new verdict, kept beside the earlier ones and never written over them. A scenario that passed before and fails now is named as broken by the change.
- The eval may have grown since the last run, because Write the evals that check the work only adds scenarios. Each run uses the eval as it is now, and the yardstick never moves to let a build pass.
- A round is one change to the built work and one run of the eval. When the same failure comes back after the rounds the project allows, the next handoff plan goes to a person, with each round's verdicts and handoff plans.
- When each run starts belongs to the plan's run: the loop that runs building and validation in rounds, or a person who names the built work.
- How it meets the capability: the capability takes in automated functional testing, "What the product does is tested automatically.", and a pass stays true only while the product passes each time it changes.

Status: not built. What exists covers only part of it:
- The old slice check, /validate-epic, is stale. It ran in rounds with the build: each fix report was the exact list of the work, what was delivered before was checked again within what the change touched, and after three rejections it stopped for a person with every round's findings.
- The loop that would run building and validation in rounds, /loop-code-validation, is a name only.
- The loops that run today stop and ask a person after a set number of rounds, which a setting holds, three when the project has not set it.

## Inputs / Outputs
- In: what changed: a fix from a handoff plan, a story of the slice built, another slice built, or a defect fixed.
- In: the slice's eval as it is now, and the evals of the slices that passed before.
- In: the earlier verdicts and handoff plans of each slice.
- In: the project's setting for how many rounds of the same failure come before a person decides.
- Out: a new verdict for each eval run, kept beside the earlier ones, with each scenario that passed before and fails now named.
- Out: once the rounds the project allows are used up, the handoff plan to a person, with each round's verdicts and handoff plans.

## Rules & behavior
- The whole eval, every time. Each run runs every scenario of every story, also after a fix. The reason: "The eval passes only when every scenario of every story below passes.", so a pass on part of it is no pass.
- Nothing that passed breaks. The evals of the slices that passed before run again, and a scenario that passed before and fails now is named. The reason: the old slice check re-verified "prior delivered behavior inside that scope", and the build already holds the same rule for its own tests: "Nothing that passed before breaks."
- Each verdict is kept, never written over. The reason: a person who decides after the rounds needs the history, as the old slice check gave it: "the escalation record lists each round's findings and fixes."
- Rounds have an end. When the same failure comes back after the rounds the project allows, it goes to a person, not round again to the builder. The reason: the old slice check stopped "after 3 rejections on the same epic", and the build already holds the same rule for its own tries: "Stuck goes back, never round in circles."
- The number of rounds is a project setting. The reason: "Everything that can be turned on or off lives in settings." The old slice check and the loops use three; that is what is built, not a rule here.
- The yardstick does not move. A run never changes, skips or leaves out a scenario to reach a pass. The reason: "A fixed yardstick: a later run cannot weaken an eval to make a build pass."
- When each run starts is the plan's. The reason: running the work is Orchestration's, and the loop for this step, /loop-code-validation, runs the plays of Code → Validation.
- Not decided: which evals of the slices that passed before run again on each change: all of them, or only those the change could touch. Memory's current answer for the old slice check is the second, "never the full suite by default"; it is not written here as a rule.
- Not decided: how many rounds a project allows, and what counts as the same failure coming back.

## Acceptance criteria
- Given a slice whose eval failed and a fix made from its handoff plan, when the eval runs again, then every scenario of every story runs, and a new verdict is kept beside the first.
- Given a new slice built on a product whose other slice passed before, when the evals run again, then a scenario of the other slice that passed before and fails now is named as broken by the change.
- Given the same failure back after the rounds the project allows, when the eval runs again, then the next handoff plan goes to a person with each round's verdicts, and not to the developer.
- Given an eval that gained scenarios since the last run, when it runs again, then the run uses all of them.

## Out of scope
- Fixing the work. Build the work test first does it before the work is accepted, and Fix defects test first after.
- Starting each run, choosing what runs when, and the loop that runs building and validation in rounds. Orchestrate agent work through planning and Run plays as loops own them.
- Adding scenarios to an eval. Update the evals as the work changes, in Write the evals that check the work, does it.
- Running the code-level tests the project already had. Build the work test first's separate check does it.
- Running the eval and giving one verdict, and writing each handoff plan. The other two features of this capability do them.

## Sources
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "each slice's eval runs on the built work", "Automated functional testing (planned): What the product does is tested automatically."
- The capability list the product owner agreed on 2026-11-03, in the same file: "Settings: Everything that can be turned on or off lives in settings.", "Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met."
- standards/templates/eval-slice.md, in Phoenix memory: "The eval passes only when every scenario of every story below passes."
- docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md: "A fixed yardstick: a later run cannot weaken an eval to make a build pass."
- core/components/plays/validate-epic/SKILL.md: "Implement ↔ validate is expected to loop — scope narrows per round, 3 rejections halt to a human."
- core/components/plays/validate-epic/reference/ice.md: "prior delivered behavior inside that scope is re-verified as baseline regression", "C10 — Loop cap: after 3 rejections on the same epic, halt to a human instead of looping again.", "the escalation record lists each round's findings and fixes."
- core/components/loops/_shared/loop-run.md: "the most rounds before the loop asks (default 3)."
- .garura/project/issues/1021/context/names.md: "/loop-code-validation"
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md: "A loop has no role. There is one for each transition between the phases"
- .garura/product/product-os/software-delivery-planning/build-work-test-first/capability.md: "Nothing that passed before breaks.", "Stuck goes back, never round in circles."
- .garura/product/product-os/software-delivery-planning/write-work-evals/fn-update-evals/feature.md: "A scenario that is there is never changed or deleted, and a recorded story line is never changed."
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-update-tests-and-code/feature.md: "the eval, run later in Code → Validation, finds that the product does something wrong, and its handoff plan says the builder can fix it alone."
- knowledge/architecture/regression-by-blast-radius.md, in Phoenix memory: "never the full suite by default"
