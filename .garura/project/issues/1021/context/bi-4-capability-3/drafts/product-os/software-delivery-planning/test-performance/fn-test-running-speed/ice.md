Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Once the built work runs in the testing environment, a part that is not the builder measures on each declared surface what the pass bar and each capability's performance need name, as one person or one other system meets the product there, the way the pass bar says it is measured, and records for each part the figure, a pass or a fail, and the conditions it was measured in, so the product owner knows how fast the product answers against its performance level.
- Limit: Nothing is measured outside the testing environment: not production, not a builder's own machine, and no system the testing environment does not hold; the test uses only the environment's made-up data and test accounts, and writes no secret's value.
- Limit: What to measure, how many tries and which figure counts come only from the pass bar and each capability's performance need, read from memory first; a part that has no way of measuring, or whose conditions the environment cannot give, is named as not measured, never passed.
- Limit: Each run records its conditions, the environment and its size, the data, the surface and the tries, so a second run can repeat them; only the performance figures are kept, and the builder never sees them.
- Fails if: A test reached production, a builder's own machine or a system the testing environment does not hold.
- Fails if: A part was not measured, or was measured in other conditions than its pass bar names, and is counted as passed.
- Fails if: A figure is recorded without the conditions it was measured in, or a tool's own score is counted as a pass that the pass bar does not name.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the product profile's performance level and pass bar with how it is measured, each capability's performance need with its target and how it is checked, the declared surfaces and how each is reached in the testing environment, the testing environment's declaration with its size, data and test accounts, and where the deployment design keeps the testing environment's secrets and which tests it places there.
- Never read: the value of any secret other than the testing environment's own, which a test takes at run time and never writes down; anything in production, such as its data or its traffic; and any ICE page.
- Persona: the product owner, who wants to know how fast the product answers against its performance level.
- Scope: In: measuring how fast the running build answers on each declared surface, as one person meets it, in the testing environment, with the conditions recorded. Out: measuring under load, the verdict and the handoff plans, a story's own speed lines, the accessibility figures of a page audit, building the environment, and fixing.

## Expectation
- Scenario: A team's command-line tool lists the work of a project, and its capability's performance need says how long the list may take on a project of a named size, measured as the time most of a set number of tries come in under. In the testing environment, with made-up data of that size, the test runs the command the set number of times and records the figure, a pass, and the environment, its size, the data and the tries. A second part of the pass bar names no way of measuring, so it is named as not measured.
- Done means: Someone other than the one who ran the test runs it again on the same built work in the same recorded conditions, and finds the same pass or fail for each part, every figure with its conditions, each part not measured named with its reason, and every try inside the testing environment.
