## Intent
- Goal: Every tracker write of a list the person approved lands exactly once, in the list's order, through the adapter, with each write recorded as it is made, so a run that stopped part way goes on from its record, finds any issue it already made by its marker line, and never writes for a list the person did not approve.
- Limit: Nothing is written unless the answer reads "approved" and the list's sha256 is the one approved.
- Limit: No label is added, no issue is deleted, and no write the list does not name is made.
- Limit: The plan file is written only once every write is made.
- Fails if: An issue is made twice, or a write is repeated, after a run again.
- Fails if: A write lands for a list that changed after the approval, or with no approval.
- Fails if: A write is made that the record does not show.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the approved list and the answer with its sha256, the writes the session's script took from it, the record of an earlier run of the same list, the plan's issues as the tracker holds them before and after, and the marker line of each new issue.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who approves the list; and the developer, a person or an AI agent who builds the code, who reads the work items in the tracker afterwards.
- Scope: In: checking the approval, the writes one by one through the adapter, the record, the search for the marker, and the reads before and after. Out: working out and checking the entries, /shape-plan's first epics and stories, the check that the plan file and the tracker agree, the one tool that knows the tracker, and a way past a write that keeps failing.

## Expectation
- Scenario: In a shop's checkout plan, the product owner approves a list that closes two stories and adds a chore under one of them. The tracker fails on the chore. The record holds the two closes and names the chore, and the plan file is not written. Once the tracker works again, the run again skips the two closes, finds no issue with the chore's marker line, and makes the chore once; the plan file is then written.
- Done means: Someone other than the one who ran the landing reads the tracker, the record and the plan file, and finds the two stories closed once, one chore with its marker line under its story, a record that names each write once, and a plan file written only after the last write.
