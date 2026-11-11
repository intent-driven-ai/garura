## Intent
- Goal: When a loop's rounds end done, a checker that did not run the loop, a sub-agent on a model that is not the session's or Codex in a read-only sandbox, judges every criterion of the loop's goal, constraints and Done means from a bundle of the loop's outputs only, with evidence for each, and the verdict's shape is checked before it is kept; a pass lets the loop land its change, and a reject or a verdict that is missing or malformed halts the loop before any pull request.
- Limit: The checker reads only the bundle, never the loop's reasoning, and writes nothing but its verdict.
- Limit: A criterion passes only on evidence in the bundle, and every criterion asked is judged, no more and no less.
- Limit: A missing or malformed verdict is never a pass, and a missing piece of the bundle fails the criterion that needs it.
- Fails if: A loop ends done, or opens a pull request, without a checker's pass.
- Fails if: The checker reads anything outside the bundle, or runs on the session's own model.
- Fails if: A verdict is kept that leaves a criterion out, passes a criterion with no evidence, or reads pass while a criterion failed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the loop's ICE and its criteria, the change from the point the opening recorded, each play's review record, the answers and their sources, the trace check, each play's done check, the checker setting for the loop, and the judge-loop-result skill with its verdict shape.
- Never read: any memory file by its path, and any ICE page; and, for the checker, anything outside its bundle or the loop's reasoning.
- Persona: the product owner, who relies on a result judged by someone who did not make it before giving the merge their yes; the developer, a person or an AI agent who builds the code, runs the loop and fixes the cause of a reject.
- Scope: In: the bundle, the two kinds of checker, the judging skill, the check of the verdict's shape, and the loop's check record. Out: running the rounds, writing each loop's criteria, the code review against standards, the person's review and the merge, the checker setting's default, and a way past a reject.

## Expectation
- Scenario: In a clinic's booking app, the Discovery loop's rounds end done. The bundle holds its criteria, the change, the three plays' review records, the answers and their sources, the trace check and the three done checks. The result-checker, on a model that is not the session's, finds evidence for every criterion and passes the result, and the loop goes on to its pull request. In a shop's checkout project the same loop's checker finds a capability no domain holds and fails the criterion that every node is linked; the loop halts with that reason. In a bank's payments service the team sets Codex as the checker, and an empty answer from it halts the loop.
- Done means: Someone other than the one who ran the loop reads each run's bundle, verdict and check record and the code host, and finds for the clinic a check record reading pass with evidence for every criterion and a checker model that is not the session's; for the shop a check record reading reject that names the failed criterion and its reason, and no pull request; and for the bank a halt with no check record, and no pull request.
