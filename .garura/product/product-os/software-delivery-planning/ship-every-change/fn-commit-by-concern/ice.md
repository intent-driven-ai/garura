## Intent
- Goal: All the work of a change is committed on its branch, in commits of one concern each, each in the conventional form with exactly one issue named, with every changed file committed or set aside with its reason, no sensitive file in any commit, and nothing pushed, so the tree is clean for the raise.
- Limit: Nothing is committed on main.
- Limit: A file named like a key or credentials, or a secret's pattern in code, stops the commit, and no setting lifts the stop.
- Limit: It never pushes.
- Limit: It runs at most five rounds, and after the fifth it stops and names what is left.
- Fails if: A commit mixes unrelated concerns, or its message does not name the issue.
- Fails if: A changed file is left uncommitted with no recorded reason.
- Fails if: A sensitive file is committed, or anything is pushed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the uncommitted changes and the branch, the issue the branch names or the open issues that match the work, the patterns of sensitive file names and secrets, the repository's ignore rules, and the setting of the commit's checkpoint.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, a person or an AI agent who builds the code and commits it.
- Scope: In: grouping the changes by concern, the messages, the sensitive-file stop, the warnings, and the play's own run records. Out: opening the change, pushing and raising it, scanning for client, company and personal references, and testing the code for security.

## Expectation
- Scenario: In a clinic's booking app, a developer's fix to the cancel button changes the button's code, its tests and a page of the help. The work is committed as three commits, each in the conventional form naming the fix's issue, and the run records as a fourth; the tree is clean and nothing is pushed. In a bank's payments service, a change that also holds a `.env` file stops before any commit.
- Done means: Someone other than the one who committed reads the log and the record, and finds each commit holding one concern and naming exactly one issue, every changed file committed or set aside with its reason, a clean tree, the branch on the code host unchanged, and, for the bank's change, no commit at all.
