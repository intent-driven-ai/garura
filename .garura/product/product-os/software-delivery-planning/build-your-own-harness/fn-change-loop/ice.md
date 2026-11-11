## Intent
- Goal: A change to a loop, its goal, a constraint, a failure condition, a scenario, its plays or their order, its first questions, its checker or runner, or how it ends, is made in its ICE first with the person's typed approval, then carried only through what it reaches; new ids are added and old ones kept, the shared run's scripts are stamped again unchanged, the fingerprint is computed from the changed ICE, and the loop linter passes, so the loop always matches its intent.
- Limit: Only wording with no change in meaning is edited directly in the compiled loop.
- Limit: A play added to a loop runs inside a loop and reads every key handed to it; a play that does not is fixed first through its own ICE.
- Limit: An id that exists is never numbered again.
- Fails if: The compiled loop says something its ICE does not, or its fingerprint does not match its ICE.
- Fails if: An eval or a recovery points to something removed, or a part the change does not reach was changed.
- Fails if: An id that exists was numbered again, or a stamped script differs from its source.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the loop's compiled file, its ICE source and its stop-condition file, the person's change and their typed approval, each play the change adds and whether it checks a loop contract and reads each key, the shared run's scripts and their sources, the loop's settings, and the map of what runs next.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead or the developer, who changes a loop of the team's harness; and the product owner, who approves the change to its intent.
- Scope: In: mapping the loop, naming the change and its reach, changing the ICE with the person's approval, carrying the change through, keeping ids, stamping the scripts again, the fingerprint, the loop linter and the summary. Out: building a new loop, running it, the settings' defaults, the loop principles the linter does not check yet, and the loop names.

## Expectation
- Scenario: In a shop's harness repository, the technical lead adds a question the loop asks first. /edit-loop changes the ICE, the product owner types yes, and the loop's questions and the contract's answers gain it; the scripts are stamped again, the fingerprint is computed again and the loop linter passes. In a game studio's harness repository, a new Done means clause is added as D5, and D1 to D4 keep their ids.
- Done means: Someone other than the one who changed it compares the shop's loop before and after, and finds the new question in the ICE, the loop's questions and the contract's answers and nowhere it does not reach, the product owner's typed yes on record, the fingerprint equal to the hash of the new ICE, every stamped script the same byte for byte as its source, and a passing loop linter; and, for the studio, the new clause as D5 with D1 to D4 unchanged.
