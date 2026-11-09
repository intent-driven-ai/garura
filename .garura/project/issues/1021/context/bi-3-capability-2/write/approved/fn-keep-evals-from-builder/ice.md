## Intent
- Goal: No part that builds the chosen work is given the evals, the hidden file or the plan's evals folder, a check fails any part whose inputs name them, and each build session that read the evals folder has a flag that names the read in that build run's evidence.
- Limit: Every part that builds the work is checked; only the parts that write the evals and the hidden file, and the eval when it runs, may name the evals folder.
- Limit: The ledger check flags a read and never stops a build; the flag goes only into that build run's evidence for now.
- Limit: A clean build session gets no flag.
- Fails if: A part that builds the work has inputs that name the evals folder, an eval or the hidden file, and the lint check passes.
- Fails if: A build session read the evals folder, and that build run's evidence has no flag that names the read.
- Fails if: A clean build session gets a flag, or the check stops a build.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the inputs of each part that builds the work, its hand-offs and its context files, each build run's evidence with its session and ledger file, and the session's ledger between the run's start and end.
- Never read: the eval files and the hidden file themselves.
- Persona: the product owner, who trusts an eval pass only when the build aimed at what was asked.
- Scope: In: the lint check over the inputs of the parts that build, and the ledger check with its flag in the build run's evidence. Out: blocking a read with a hook, encrypting the evals, splitting the stories, and handing each agent of the build its part.

## Expectation
- Scenario: A build of a clinic's booking story reads the plan's evals folder once. The ledger check finds the read through the session named in the build run's evidence and writes one flag there that names it; the build was not stopped. A second build session reads nothing there and gets no flag. The lint check fails a helper whose hand-off names the hidden file.
- Done means: Someone other than the builder runs both checks on a session that read the evals folder and on a clean one, and finds one flag for the first, none for the second, no stopped build, and a lint failure for each part whose inputs name the evals.
