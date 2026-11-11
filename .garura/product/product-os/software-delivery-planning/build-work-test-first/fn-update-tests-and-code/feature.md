# Feature: Update the tests and the code as the work changes

## What it does
When the work changes after its tests or its code are written, the test writer updates the tests first and the check shows each new or changed test failing, and then the builder changes the code until every test passes again, under the same rules as the first build.
- The work changes, for example, when:
  - the technical lead confirms a design update that changes a class, function or interface the tests call, such as a renamed function;
  - a story under the chosen item is added, changed or dropped in the plan;
  - the eval, run later in Code → Validation, finds that the product does something wrong, and its handoff plan says the builder can fix it alone. A handoff plan says what the product does wrong and the way back, and never names the failure condition or the check.
- The test writer updates the tests from the changed test writer's part, the updated design or the handoff plan. A new or changed test is shown to fail by the check where the code does not yet do what it asks.
- A test for an expectation that was dropped is taken out by the test writer, with its reason, and the check's record names it.
- Then the builder changes the code, without seeing a test, until the check finds every test passing, and tidies it as the first build does.
- Only what the change touches changes. A handoff plan is the whole list of the work it calls for.
- The usage guide is updated when what it describes changed.
- How it meets the capability: the tests and the code must keep saying what the work asks as the work changes. Changing something later is worded as updating it as the project changes, as the product owner put it for the project's architecture: "this should be reflected as updating arch. as the project changes."

Status: not built. What exists covers only parts of it:
- In the bug fix play, after two failed tries, the design agent revises the fix design and its test, and the fix goes on. It is live only in a full install, and Fix defects test first keeps it.
- The old build play, /build-epic, is stale. When its checker sent the build back, the report was the exact list of the work, as new pieces on the existing plan, with no fresh start.
- Nothing updates a project's tests and code when a design is updated, and the approved design update leaves open how the tests follow a renamed function.

## Inputs / Outputs
- In: what changed: a design update the technical lead confirmed, a story added, changed or dropped, or a handoff plan that says the builder can fix it alone.
- In: the changed test writer's part, for the test writer, and the changed builder's part with its collected context, for the builder, from Gather the work under a chosen plan item.
- In: the design in force, and the tests and code as they are.
- Out: the updated tests, each new or changed one shown to fail on the check's record, and each test taken out, with its reason.
- Out: the changed code, with every test passing on the check's record.
- Out: the updated usage guide, when what it describes changed.
- Out: in the build's record, what changed, why, and from which source.

## Rules & behavior
- Tests first, then code, as in the first build. The reason, in the product owner's words: "we have to do this such that coding is also test driven".
- Only the test writer changes, adds or takes out a test, always with its reason. The builder never does, also when the change is only a name. The reason: a builder that changes a test grades itself, and Code → Validation must not let a builder "weaken a check to pass".
- A test changed because of a design update is shown to fail on the old code where the old code no longer matches, before the builder changes the code. The reason: a changed test that never failed proves nothing about the change.
- Only what the change touches changes. The reason: a part the change does not touch still holds what was built and checked.
- A handoff plan is the exact list of the work it calls for. The reason: the old build play held its fix round to the report, "the /validate-epic fix report is the exact work list", so a fix round does not grow into new work.
- A handoff plan that says a person must decide does not come here; it goes to a person. The reason: the eval's handoff plan goes to the builder only when the builder can fix it alone, and "the handoff plan goes to the builder" in that case only.
- The same rules hold as in the first build: the builder sees no test, a pass counts only on the check's record, and the design is the input. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were".
- Not decided: who starts an update when a story is dropped or changed: the plan's change, the technical lead or the build.
- Not decided: whether a failure the eval finds after the work was accepted comes here or goes to Fix defects test first as a defect.

## Acceptance criteria
- Given a design update that renames a function the tests call, when the work is updated, then the test writer updates those tests, the check shows them failing on the old name, the builder renames the code, the check's record shows every test passing, and the builder changed no test.
- Given a new story added under the chosen epic, when the work is updated, then its tests are written and shown to fail before any of its code.
- Given a handoff plan that says the builder can fix it alone, when it comes back, then a test for what the product does wrong is written and shown to fail before the code is changed, and nothing beyond the handoff plan is built.
- Given an expectation dropped from a story, when the work is updated, then its test is taken out by the test writer, and the check's record names it with the reason.
- Given a handoff plan that says a person must decide, when it is found, then it is not built here and goes to a person.

## Out of scope
- Updating the design. Design the work does it, through Update the design as the work changes.
- Changing the plan and its work items. Turn intents into agent work holds them today.
- Running the eval and writing the handoff plan. Test with evals the builder never sees, in Code → Validation, does them.
- A defect traced to its cause. Fix defects test first does it.
- The first tests, the first code and the first tidy. The other features of this capability do them.

## Sources
- The product owner's words, recorded on 2026-11-09 in .garura/project/issues/1021/context/bi-3-capability-4/page-approvals.md: "we have to do this such that coding is also test driven", "the code, when being written, should not get to see what tests there were"
- The product owner on 2026-11-07, in .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "this should be reflected as updating arch. as the project changes."
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or count a check that did not run as a pass."
- .garura/product/product-os/software-delivery-planning/design-work/fn-update-work-design/feature.md: "Not decided: how the developer's tests are kept in step when an update changes a class or function they were written to.", "Changing the tests and the code to the updated design. Build the work test first does it.", "Not decided: whether an update that a dropped or changed story calls for is started by the plan's change, by the technical lead or by the build."
- .garura/product/product-os/software-delivery-planning/write-work-evals/capability.md: "Out: running the evals, giving the verdict, and writing the handoff plan, which tells the builder or a person what went wrong and the way back. Test with evals the builder never sees, in Code → Validation, owns them."
- core/components/plays/fix-bug/SKILL.md: "`tech-designer` to revise the design/test and resumes — it does not halt blindly."
- core/components/plays/build-epic/reference/ice.md: "the /validate-epic fix report is the exact work list"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "the handoff plan goes to the builder", "The handoff plan never names the failure condition, its id or the check."
