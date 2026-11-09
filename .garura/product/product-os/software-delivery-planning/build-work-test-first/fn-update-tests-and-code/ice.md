Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: When a confirmed design update, a story added, changed or dropped, or an eval's handoff plan that the builder can fix alone changes the work, the test writer updates the tests first and the check shows each new or changed test failing, then the builder changes the code, without seeing a test, until the check's record shows every test passing again, and only what the change touches changes.
- Limit: Only the test writer adds, changes or takes out a test, always with its reason; the builder never does, also for a renamed name.
- Limit: The first build's rules hold: the builder sees no test, the test writer's part, an eval or the hidden file, a pass counts only on the check's record, and the design in force is the input.
- Limit: A handoff plan is the exact list of the work it calls for, and one that says a person must decide goes to a person, not here.
- Fails if: Code was changed for an update before its new or changed tests failed on the check's record.
- Fails if: The builder changed, weakened or took out a test, or a test went away with no reason in the check's record.
- Fails if: An update changed a part the change does not touch, or built work beyond what a handoff plan named.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: what changed and its source, such as the design update the technical lead confirmed, the changed story or the handoff plan; for the test writer, the changed test writer's part and the design in force; for the builder, the changed builder's part, its collected context and the design in force; the tests and code as they are, and the check's records.
- Never read: for the builder, the tests for the work, the test writer's part, the plan's evals folder, the eval, the slice's hidden file and any ICE page; for the test writer, the plan's evals folder, the eval, the slice's hidden file and any ICE page.
- Persona: the developer, as test writer and as builder, who keeps the tests and the code in step with the work; the technical lead confirms the design updates that start it.
- Scope: In: updating the tests first and then the code when the design, a story or an eval's handoff plan changes the work, and updating the usage guide when what it describes changed. Out: updating the design, changing the plan and its work items, running the eval and writing the handoff plan, and a defect traced to its cause.

## Expectation
- Scenario: In a shop's checkout, the technical lead confirms a design update that renames the function that makes a receipt. The test writer changes the two tests that call it, and the check shows both failing on the old name. The builder, who never sees the tests, renames the function in the code, and the check's record shows every test passing. Later the eval finds that a guest sees a sign-up page before payment, and its handoff plan says the builder can fix it alone. The test writer writes a test for that, the check shows it failing, the builder sends the guest straight to payment, and nothing beyond the handoff plan is changed.
- Done means: Someone other than the builder compares the tests, the code and the check's records before and after the update, and finds each new or changed test failing before the code changed and every test passing after, no test changed by the builder, each test taken out with its reason, and no change outside what the update touched.
