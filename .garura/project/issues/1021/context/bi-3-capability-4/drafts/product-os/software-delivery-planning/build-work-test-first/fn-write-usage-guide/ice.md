Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: With the build, the slice's one usage guide, in the guides folder of its home plan, says what kind of surface the slice is on, how to reach it, and the steps a person takes there for each built story, with the real names of the commands, pages and fields the work made, so the eval can later reach the built work through it.
- Limit: The builder writes the guide without reading the eval, the hidden file or the evals folder, and the guide holds no test result and no expected result.
- Limit: A slice has one guide, kept once in its home plan's guides folder, beside the evals folder and never in it; another plan points to it and never copies it.
- Limit: A built item adds its part, and a part already there changes only when what it describes changed.
- Fails if: A built story of the slice has no steps in the guide, or the guide names a command, address or field the build did not make.
- Fails if: The builder read the eval, the hidden file or the evals folder while it wrote the guide, or the guide holds a test result or an expected result.
- Fails if: The guide is written in the evals folder, kept twice, or lost a part that described work still built.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the code as built with its real commands, pages, addresses and fields, the design's surface part, the builder's part of each story, the slice's one surface, the guide already there for the slice, and the ontology's rules for the usage guide.
- Never read: the plan's evals folder, the eval, the slice's hidden file, the tests for the work and any ICE page.
- Persona: the developer who builds the code and writes the guide; the eval reads it later, in Code → Validation.
- Scope: In: the slice's usage guide, its surface, how to reach it and the steps for each built story, and adding to it as more of the slice is built. Out: the eval and its names, matching the names to the guide, running the eval, declaring surfaces, and designing the surface.

## Expectation
- Scenario: A clinic's booking slice on a browser page has two stories built. The builder writes the slice's guide in its home plan's guides folder: the surface is a browser page, it is reached at the booking address the build made, and a patient picks a doctor, picks a free slot and gives a phone number; the second story's steps cover the reminder the patient gets. The builder never opens the evals folder. When a third story of the same slice is built later, its steps are added and the first two parts stay as they were.
- Done means: Someone other than the builder compares the guide with the built work and the session's record, and finds every built story with its steps, every name in the guide made by the build, no test or expected result in it, the guide kept once outside the evals folder, and no read of the evals folder.
