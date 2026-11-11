## Intent
- Goal: An ADR becomes accepted only on a person's own typed word: run by hand, the decision play shows the draft exactly as it will read and waits, at a pinned checkpoint, for accept, reject or a change; inside a loop it does not wait and saves the ADR as proposed for the loop's end review; and a proposed ADR is completed later by hand with `/record-decision accept <file>`; an accept writes the ADR as Accepted with its date and the person who accepted it, and a reject writes nothing.
- Limit: No agent, play or setting accepts or rejects an ADR; only a person's typed answer does.
- Limit: Run by hand, the checkpoint is never skipped by any setting, policy or record of earlier answers.
- Limit: Inside a loop, the run never waits for an answer.
- Limit: Only a proposed ADR is accepted, and an accept always names the person.
- Fails if: An ADR reads accepted with no person's typed answer on record, or a rejected ADR is written.
- Fails if: Run by hand, the run goes past the checkpoint without the person's answer.
- Fails if: Inside a loop, the run stops to wait for an answer, or writes the ADR as accepted.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the drafted ADR and its gathered context, whether the run is inside a loop and the loop's contract, the person's typed answer and their name, the setting of each checkpoint, and, for a later accept, the proposed ADR's file and its Supersedes and Amends lines.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner or the technical lead, who accepts each decision on how the project is built.
- Scope: In: showing the draft, the three answers, the pinned checkpoint, writing the accept or nothing, saving as proposed inside a loop, and the later accept by hand. Out: drafting and checking the ADR, the forward pointers and the index, the card in the review tool, the way past the checkpoint, running the loop, and the checkpoint settings.

## Expectation
- Scenario: In a clinic's booking app, the technical lead records a decision by hand; the decision play shows the draft and waits. The product owner types a change, to name what happens to bookings made before the decision; the draft comes back with it, and the product owner types accept, and it reads Accepted with their name and the date. In a data team's reporting service, a loop's run saves an ADR as proposed without waiting; at the end review the person runs `/record-decision accept` on its file and types accept. In a bank's payments service, the product owner types reject.
- Done means: Someone other than the one who ran the decision play reads the ADR folder and each run's records, and finds the clinic's ADR accepted only after the product owner's typed accept, with their exact words on record; the data team's ADR proposed with no answer record until the later accept, then Accepted with the person named; and, for the bank, no new ADR and the run closed halted with the reason rejected.
