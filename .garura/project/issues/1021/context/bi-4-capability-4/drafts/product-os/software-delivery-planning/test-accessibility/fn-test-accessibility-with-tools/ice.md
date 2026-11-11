Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Once the built work runs in the testing environment, a part that is not the builder runs on each declared surface a person opens the tools that check what the pass bar, each capability's accessibility need and the surface's accessibility guideline say a tool checks, and records for each part the result, a pass or a fail, and the surface, the screen and the tool, so the product owner knows which parts of the accessibility level a tool found met.
- Limit: Nothing is tested outside the testing environment: not production, not a builder's own machine, and no system the testing environment does not hold; the test uses only the environment's made-up data and test accounts, and writes no secret's value.
- Limit: What to check, that a tool checks it, and which tool, come only from the pass bar, the needs, the guideline and the project's settings, read from memory first; a part with no known tool, a tool that could not run, and a part a person must check are never passed by a tool.
- Limit: Only the accessibility results are kept, each with what was checked and where, so a second run can repeat it; the builder never sees them.
- Fails if: A test reached production, a builder's own machine or a system the testing environment does not hold.
- Fails if: A part that no tool checked, or a part that a person must check, is counted as passed after a tool's clean run.
- Fails if: A tool's own score is counted as a pass that the pass bar does not name, or a result is recorded without what was checked and where.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the product profile's accessibility level and pass bar with how it is checked, each capability's accessibility need, the declared surfaces with who opens each and each one's accessibility guideline, how each surface is reached in the testing environment, the tools the project's settings and code already name, the testing environment's declaration with its data and test accounts, and where the deployment design keeps the testing environment's secrets and which tests it places there.
- Never read: the value of any secret other than the testing environment's own, which a test takes at run time and never writes down; anything in production, such as its data or its traffic; and any ICE page.
- Persona: the product owner, who wants to know which parts of the accessibility level a tool found met.
- Scope: In: running the tools on each declared surface a person opens, in the testing environment, with what was checked and where recorded. Out: the person's walk, the verdict and the handoff plans, the review's accessibility rules, a story's own accessibility lines, layout and the screen design, the speed figures of a page audit, building the environment, and fixing.

## Expectation
- Scenario: A shop's checkout page runs in the testing environment, and its browser guideline says a tool checks that each field has a label a screen reader can read out and that text stands out from its background, and a person checks the rest. The tools find the card number field with no label, and record a fail with the screen and the tool, and a pass for the text. A page audit also gives a speed score, which is not kept here. The parts a person must check are left for the walk, not passed.
- Done means: Someone other than the one who ran the tools runs them again on the same built work, and finds the same pass or fail for each part, every result with what was checked and where, each part not tested named with its reason, no part a person must check counted as passed, and every check inside the testing environment.
