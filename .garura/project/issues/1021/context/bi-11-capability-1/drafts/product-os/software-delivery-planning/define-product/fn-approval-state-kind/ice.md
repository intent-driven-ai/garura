Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: The map names one approval state that every kind of the model carries, approved, changed or in progress, with what an approval keeps, the fingerprint of the words, who approved them, when and in which review, and maps confirmed, accepted and active onto approved, so a page and its approval state never disagree.
- Limit: Changed is worked out from the fingerprint; no play has to remember to set it.
- Limit: A rule of approval stops work, never a write.
- Limit: Only a person approves; the map gives no kind a way for an agent to approve.
- Fails if: A kind of the model has no approval state in the map, or two kinds map the same state differently.
- Fails if: The map lets a write be refused because a piece is approved.
- Fails if: The map lets an agent approve a piece.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the approval decision and its three states, the states each kind holds today, the map's kinds and their format, and the open issues on the approval state and on how approval is recorded outside the review step.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who approves pieces in a review and agrees the change to the map; the developer, a person or an AI agent who builds the code, who reads a piece's state before building from it.
- Scope: In: the approval state in the map for every kind, what an approval keeps, and the mapping of today's states. Out: keeping the state on each part and agents building only from approved parts, writing approval in the review, and confirming a business intent.

## Expectation
- Scenario: In a clinic's booking app, the product owner approves the Reminders capability's ICE in a review; a reader of the map finds that an approved ICE keeps the fingerprint, the person, the date and the review. In a bank's payments service, a play rewrites an approved feature page; by the map's rule the feature reads changed, and the write went through.
- Done means: Someone other than the one who changed the map reads every kind in it, and finds an approval state on each, what an approval keeps, confirmed, accepted and active mapped onto approved, and no rule that refuses a write or lets an agent approve.
