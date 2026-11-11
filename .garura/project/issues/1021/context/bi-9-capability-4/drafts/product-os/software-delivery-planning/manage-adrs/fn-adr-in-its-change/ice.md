Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Run by hand on the branch of a change that is already open, the decision play records the ADR on that branch, in that change, and opens no issue, branch or pull request of its own; run with no change open, it opens its own change as today; and a test shows both, so a decision lands with the work it decides.
- Limit: Only a person accepts the ADR, in whichever change it is recorded.
- Limit: The loop's contract stays for loops; a play run inside a change does not pass as a loop.
- Limit: Every other rule of the decision play holds: the one template, what the ADR overrides and changes in plain view, and its business-intent check.
- Fails if: Run on an open change's branch, the decision play opens a new issue, branch or pull request, or the change lands without its ADR.
- Fails if: Run with no change open, the decision play records the ADR on a branch that is not its own change.
- Fails if: An ADR recorded in a change reads accepted with no person's typed answer on record.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the decision brief, the branch the decision play runs on and the change it belongs to, the decision play's two modes and its first step, the loop's contract rule, the ADR template, how a change that adds an ADR is reviewed, and the approved facts on keeping an ADR in the change of its work.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead or the developer, who records a decision on the branch of the change that makes it; and the product owner or the technical lead, who accepts it.
- Scope: In: recording the ADR in an open change, opening its own change when none is open, and the test of both. Out: drafting and checking the ADR, accepting it, the points for the person who accepts, opening and landing the change, and reviewing it.

## Expectation
- Scenario: In a shop's checkout service, a developer's change moves guest carts into the database. On that change's branch, the technical lead runs the decision play by hand; the ADR is written on that branch, no new issue, branch or pull request is opened, and the pull request holds both the code and the ADR. In a clinic's booking app, with no change open, the technical lead runs the decision play, and it opens its own change, as today.
- Done means: Someone other than the one who recorded it reads the code host, the branches and the run's records, and finds for the shop one pull request that holds both the code and the ADR, no other issue, branch or pull request from the decision play, and no accept without the person's typed answer on record; for the clinic a change of the decision play's own; and one test that shows both cases.
