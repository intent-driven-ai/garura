## Intent
- Goal: When the person presses Finish, the review step reads every answer kept on the run's branch and applies them all in one commit, approval written on each accepted piece with who, when and which review, dropped pieces removed, sent-back pieces left in progress, an edit checked against the ontology's rules, each memory update's and ADR's answer carried out by its owner and the plays' review records marked decided; a run that stopped is resumed or dropped whole; then the change goes to Ship every change the same way to land, with the merge waiting for the person's yes.
- Limit: The commit holds only what the person's answers say; nothing in it comes from an agent's own choice.
- Limit: Argus writes nothing to the model; only the review step writes approval, and each memory update and ADR answer goes through the part that owns it.
- Limit: Landing the change, and the merge with the person's yes, stay with Ship every change the same way.
- Fails if: An answer the person gave is missing from the commit, or the commit holds a change no answer asked for.
- Fails if: A piece reads approved that the person did not accept, or a dropped piece is still in the model.
- Fails if: An edit that breaks the ontology's rules was applied with no reply on its piece.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the answers and the Finish event on the run's branch, the run's pieces with their approval state once it is kept, the plays' review records, the ontology's rules for each kind, the memory tool's commands for a decision and an approved update, the decision play's accept, and, for a stopped run, where it stopped and why.
- Never read: any memory file by its path, any ICE page, the review's web page, and production.
- Persona: the product owner, whose answers must become the run's work exactly as given.
- Scope: In: applying every answer in one commit, writing approval from the answers, removing dropped pieces, checking edits, carrying memory and ADR answers to their owners, a stopped run's resume or drop, and a dropped box-move. Out: landing the change, keeping the approval state as a kind, what a memory update or ADR answer writes, and reworking a piece.

## Expectation
- Scenario: A shop's checkout review ends with two intents accepted, one feature dropped, a capability's sentence edited and a memory update approved. On Finish, one commit on the run's branch marks the intents confirmed and approved by the product owner in this review, removes the feature, applies the edited sentence after it passes the ontology's rules, records the memory update's approval with his words and writes it to the issue's short-term memory, and marks the plays' review records decided. The change then goes to Ship every change the same way, and the merge waits for his yes.
- Done means: Someone other than the one who built it compares the person's answers kept on the run's branch with the one commit, and finds every answer applied once, nothing applied that no answer asked for, approval only on accepted pieces, and no merge without the person's yes.
