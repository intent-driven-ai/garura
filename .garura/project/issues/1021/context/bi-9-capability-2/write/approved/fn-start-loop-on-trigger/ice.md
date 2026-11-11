## Intent
- Goal: A loop is started by what the loop itself says starts it, a person, a schedule or a hook, and takes the steps of the shared run whatever started it; after each round it writes one record of what the round did and whether it worked, and the next round reads that record before it runs, so it knows what to try and what not to repeat.
- Limit: Nothing merges without a person's typed yes, whatever started the run.
- Limit: A start from a schedule or a hook skips no step of the shared run.
- Limit: What starts a loop is one of the loop's own values; it adds no rule about the product.
- Fails if: A loop that says a schedule or a hook starts it does not run when that start comes, or runs when nothing started it.
- Fails if: A round starts without reading the record of the rounds before it, or tries again what an earlier round recorded as not working.
- Fails if: A run that no person started merges without a person's typed yes.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the loop's own values and what it says starts it, the loop principles, the steps of the shared run that wait for a person, the headless runner and the runner setting, the round records and the record across rounds, and the approved facts on the tools that start a run from a schedule or an event.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, a person or an AI agent who builds the code, who says what starts a loop and finds its run later; and the product owner, who gave the loop its goal and gives the merge their yes.
- Scope: In: what starts a loop, a person, a schedule or a hook, and one record across rounds that the next round reads. Out: the steps of the run, the status file, building a loop and checking the loop principles, the loop's settings, choosing which loop runs next, the merge, and a way past a question or a halt.

## Expectation
- Scenario: In a shop's checkout project, the loop for code to validation says a schedule starts it, every night. At night a scheduler runs its command with no person present; the loop takes the steps of the shared run, and after round one it writes what the round did and whether it worked. Round two reads that record and does not try again what round one recorded as not working. The run does not merge; the merge waits for the product owner's typed yes. In a clinic's booking app, a pull request that changes the prototype opens, and the Discovery loop starts from that event.
- Done means: Someone other than the one who set up the loop reads the loop's own values, the run's records and the code host, and finds for the shop a run that started at the scheduled time with no person typing its command, one record across rounds that round two read before it ran, no second try of what round one recorded as not working, and no merge without a typed yes on record; and for the clinic a run that started when the pull request opened.
