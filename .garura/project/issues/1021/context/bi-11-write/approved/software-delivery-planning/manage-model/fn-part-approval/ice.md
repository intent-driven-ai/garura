## Intent
- Goal: Each part of the model carries its approval state, approved, changed or in progress, with the fingerprint of the words a person approved, who approved them, when and in which review; an edit moves a part to changed by its fingerprint with no play having to say so; and agents build only from parts a person approved.
- Limit: Approval is kept in the model, and only a person's answer makes a part approved.
- Limit: A rule on approval stops work, never a write.
- Limit: The review tool writes nothing to the model; the state is kept here.
- Fails if: A part reads approved after its words changed, or with no person, time or review on record.
- Fails if: An agent builds from a part that is not approved.
- Fails if: A write to a part is stopped because of its approval state.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: ADR 033 and what ADR 047 amended in it, the review's answers, the index and the pages, the ready check, the intent pages' stage lines, and #964 with #645, #646 and #647.
- Never read: any memory file by its path, any ICE page, and any file in a plan's evals folder.
- Persona: the product owner, who approves each part; and the developer, a person or an AI agent who builds the code, who builds only from approved parts.
- Scope: In: each part's approval state, its fingerprint and record, the move to changed on an edit, and the rule that agents build only from approved parts. Out: the review itself, the approval state as a property of each kind, confirming an intent, and the ready answer.

## Expectation
- Scenario: In a shop's checkout service, the product owner approves Checkout in a review; a play later changes one word of its page, Checkout reads changed, the write is not stopped, and no agent builds from it until the product owner approves it again. In a clinic's booking app, Reminders was approved and not touched, and it reads approved with who, when and which review.
- Done means: Someone other than the one who built it edits an approved part and reads its state, and finds it changed with no play having said so, the write kept, and no agent's work started from it; and finds the clinic's untouched part approved with its record.
