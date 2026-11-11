## Intent
- Goal: Each of the six transitions between the phases has one loop of its own, named loop-<from>-<to> for the two phases it joins and always written in full, that holds only its own values (its plays, its questions, its documents and source, its settings keys and its end), points to the shared run, runs only plays that check a loop contract, and leaves each play usable by hand; the Discovery loop, for product to spec, is built, and no loop is laid in a project that builds its own harness.
- Limit: A loop carries no product rule of its own; its plays stay its transition's.
- Limit: There is no Ship loop, and no command is called just /loop.
- Limit: A loop not built is never written as built, and nothing is renamed before the rename lands as one change.
- Fails if: A loop runs a play that checks no loop contract, or a play can no longer run by hand because a loop runs it.
- Fails if: A loop's command holds more than its own values, or lacks the two anchor lines that point to the shared run.
- Fails if: A loop is laid in a project that builds its own harness.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the agreed loop names, the six phases and their transitions, the compiled loops and their ICE, the shared run and its anchor lines, each transition's plays and whether each checks a loop contract, the recipe spikes of the loops not built, and the kind of install a project has.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who gives the loop of a transition its goal; and the developer, a person or an AI agent who builds the code, who starts that loop and follows it.
- Scope: In: one loop for each transition, its name, its shape as a loop that points to the shared run, the plays it may run, and the one loop built. Out: each loop's plays and what they write, the Discovery loop's own pages, building and changing loops, the naming rule, the review and the merge, when each run starts, and how each loop runs.

## Expectation
- Scenario: In a clinic's booking app, the product owner gives the Discovery loop, the loop for product to spec, a working prototype and its write-up; it runs its three plays in rounds on one branch and ends at a pull request where the product owner types confirm or drop for each intent. Its check finds both anchor lines once each, the opener first. In a harness repository, Garura is installed and no loop is laid. In a shop's checkout project, the team looks for the loop for code to validation and finds it is not built yet.
- Done means: Someone other than the one who built or ran the loops reads the compiled loops, the loop check, the install record and the run's records, and finds for the clinic one loop for product to spec with only its own values between its two anchor lines, three plays that each check a loop contract, and a pull request with the person's typed decision on each intent; for the harness repository no loop laid; and for the shop no loop for code to validation written as built.
