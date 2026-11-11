## Intent
- Goal: Each use of a way past writes one owed entry, with what was skipped, the gate, who used the way past, when, the issue, the branch and what is still to be done, in the issue folder of the work that made it, landing with that change; and a tool reads every issue's entries back as one list, so a later play or a person finds all that is owed in one place, and Learn finds the changes left for it without opening any issue's short-term memory.
- Limit: Nothing is written to a global file; every entry stays in its issue's folder.
- Limit: Every entry has the same parts, and one is closed only when its debt is paid.
- Limit: Learning a change into the model, the plan views and the tracker writes stay with their owners.
- Fails if: A way past was used and no entry is in its issue's folder, or an entry sits in a file outside the issue folders.
- Fails if: The one list misses an open entry of any issue, or shows a closed one as open.
- Fails if: Learn or a play has to open an issue's short-term memory to find what is owed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: each issue's folder and its owed entries; the gate records each issue already keeps, and how the learner reads them; the places that name what is owed today, such as a plan session's commit, the thin marks, an upgrade's report and initialize's record; and #990's list of changes not yet learned.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who wants to see all that was left owed, and the later play that pays it.
- Scope: In: the entry's one shape, writing it in the issue's folder, landing it with the change, reading every issue's entries as one list, and closing an entry once it is paid. Out: using a way past, learning a change into the model, the plan views, and the tracker writes.

## Expectation
- Scenario: In a clinic's booking app, an upgrade keeps a part the team edited, and a plan session in another issue lands a found feature while its plan holds no slice. Each issue's folder gains one entry, with what was skipped, the gate, who, when, its branch and what is still to be done, and both land with their changes. The one list shows the two entries side by side. A month later the slice is shaped, the plan session's entry reads closed, and the list shows only the kept part as open.
- Done means: Someone other than the one who built it uses a way past in two issues, lands both changes, reads the one list, and finds both entries with every part, nothing written outside the issue folders, and an entry closed only after its debt was paid.
