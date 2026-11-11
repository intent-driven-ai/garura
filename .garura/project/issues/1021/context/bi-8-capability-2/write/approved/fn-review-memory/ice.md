## Intent
- Goal: In the Memory section, the person sees what Garura memory holds and, for a picked issue, what its short-term memory holds, and approves or rejects each memory update that waits for a person, one at a time and in their own words; Garura records each decision through the memory tool as made in the review tool, and writes an approved update only to its issue's short-term memory, so nothing enters memory without a person's word.
- Limit: Only a person decides an update, one at a time, with their own words; none is decided in bulk or by an agent.
- Limit: An approved update is written only to its issue's short-term memory; nothing moves up to Garura memory or Phoenix memory from here.
- Limit: What an answer does is the memory tool's to carry out, by Memory's rules; Argus only takes the answer.
- Fails if: An update reads approved or rejected with no person's words on record, or more than one was decided by one action.
- Fails if: An approved update is written anywhere but its issue's short-term memory, or a rejected one is written at all.
- Fails if: The decision on record does not say it was made in the review tool.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the memory updates that wait for a person, with what was missing, the draft, where it came from, its sources and whether it blocks; what Garura memory and the picked issue's short-term memory hold; and the memory tool's commands for recording a decision and writing an approved update.
- Never read: any memory file by its path, any memory update that still waits as a source to decide from, any ICE page, and production.
- Persona: the product owner, who controls what enters memory.
- Scope: In: what memory holds, each waiting update with its approve or reject in the person's words, and carrying the answer to the memory tool; Ask memory as a mock only. Out: what an update is and who may decide it, moving memory up, the traces of agent decisions, and applying the answers in one commit.

## Expectation
- Scenario: A shop's checkout run raised two memory updates. The product owner approves the first, on how long a guest's cart is kept, with "yes, thirty days, as our policy says", and rejects the second, on how long a password reset link lasts, with "ask our security lead first". After the answers are applied, the memory tool shows the first approved by him with his exact words, decided in the review tool, and written to the issue's short-term memory; the second is rejected, nothing is written, and the work waiting on it stays stopped.
- Done means: Someone other than the one who built it compares each update's record in the memory tool with the person's answer in Argus, and finds the same words, one decision for each update, made in the review tool, each approved update in its issue's short-term memory only, and nothing written for a rejected one.
