## Intent
- Goal: The model keeps up with the work as it is done: a story's approved design updates the model through the keeper's skills, each changed part marked in review; at the proposal of a change, the person chooses to update the model now or leave it; and a change left for later is written to one list that Learn reads, so the model never falls behind without a record of what is owed.
- Limit: Leaving the model for later is always allowed, and never stops the change.
- Limit: A part changed by a design is marked in review, never approved, until a person approves it.
- Limit: The model is changed only through the keeper's skills.
- Fails if: A design's approval changes nothing in the model, or a changed part reads approved with no person's answer.
- Fails if: A change is stopped because the person chose to leave the model for later.
- Fails if: A change left for later is missing from the list of changes not yet learned.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: #990's flow and its decisions, the approved design and its record, the keeper's skills, the choice at the proposal of a change, the list of changes not yet learned, and how Learn reads it (#977).
- Never read: any memory file by its path, any ICE page, and any file in a plan's evals folder.
- Persona: the technical lead, who approves a story's design; and the developer, a person or an AI agent who builds the code, who proposes the change and chooses when the model is updated.
- Scope: In: updating the model on a design's approval, marking each changed part in review, and the list of changes not yet learned. Out: the choice at the proposal of a change, the design of a story, where what is owed is kept, and finding drift from what was built.

## Expectation
- Scenario: In a clinic's booking app, the technical lead approves the reminder story's design, and the keeper adds Send a reminder and changes the Booking page, each marked in review. In a shop's checkout service, the developer chooses to leave the model at the proposal of a change; the change goes on and one entry joins the list of changes not yet learned.
- Done means: Someone other than the one who did the work reads the model, the design's record and the list, and finds the clinic's two parts changed and marked in review, none of them approved without a person's answer, and the shop's change on the list with its issue, its branch, what was left, who chose and when.
