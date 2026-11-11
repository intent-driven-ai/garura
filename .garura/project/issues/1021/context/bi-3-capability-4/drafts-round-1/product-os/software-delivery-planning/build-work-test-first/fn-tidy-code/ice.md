Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Once every test for the work passes, the code the work wrote or changed is tidied where it needs it, to the design's patterns and the project's coding standards, without changing what it does, and the check's record after the tidy shows every test for the work and every test the project already had still passing, with no test file changed.
- Limit: A tidy changes how the code is written, never what it does; it stays inside the work, keeps every name and interface the design gave, and sends a change to one to the technical lead as a design update.
- Limit: No test is changed, weakened or taken out by the tidy, and only the check, never the builder, says the tests still pass.
- Limit: The patterns and standards the tidy follows come from the design and the project's code and memory first, then Garura memory, then Phoenix memory, or from research only after a person approves it as a memory update.
- Fails if: After the tidy, the check's record shows a test failing, or a test file differs from the check's first run.
- Fails if: The tidy changed what the code does, changed code outside the work, or changed a name or interface the design gave.
- Fails if: The work moved on with no check run after the tidy, or with a tidy and no line that says why it was needed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the code the work wrote or changed, the design's patterns, names and interfaces, the project's coding standards, and the check's last record.
- Never read: the tests for the work, the test writer's part, the plan's evals folder, the eval, the slice's hidden file and any ICE page.
- Persona: the developer who builds the code, who tidies it once every test passes.
- Scope: In: tidying the code the work wrote or changed, where it needs it, with the check run after, and naming a tidy that would change the design. Out: building the code, running the check, checking the code against the standards, changing the design, and choosing what is built next.

## Expectation
- Scenario: In a team's task tool on the command line, every test for a story passes. The builder sees that two commands parse a date the same way, joins them into one helper inside the work, and writes why. It weighs renaming the add function the design names, and sends that to the technical lead instead of making it. The check runs every test for the work and every earlier test, and its record shows them all passing and every test file the same as at the first run. The work moves on.
- Done means: Someone other than the builder compares the code before and after the tidy and the check's records, and finds every test still passing, no test file changed, no change outside the work or to a name the design gave, and the reason for the tidy written down.
