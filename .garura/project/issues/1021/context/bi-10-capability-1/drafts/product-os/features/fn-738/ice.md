## Intent
- Goal: Every change to the harness standard or to its rule files is first an accepted ADR that names each older ADR it supersedes or amends, with the part; each of those older ADRs gains a forward pointer and nothing else; the index lists it; and the standard page and the rule files are changed to match it, or the change is named as owed, so a reader always sees which rule is in force and what it replaced.
- Limit: An accepted ADR is never edited; an older one gains only its forward pointer.
- Limit: A change to a rule file with no ADR behind it is named as owed, never left unsaid.
- Limit: The ADR itself is drafted, checked and accepted through the decision play of Manage ADRs.
- Fails if: The standard or a rule file changes with no ADR behind it, and nothing names it.
- Fails if: An older ADR that a newer one supersedes or amends still reads as the rule in force, with no forward pointer.
- Fails if: An accepted ADR's change is neither made in the standard and the rule files nor named as owed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the harness standard and the rule files with their history, the ADR folder and its index, the older ADRs a change supersedes or amends, each ADR's Work This Creates, and the ADR template and the templates index.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead, who records a change to the standard; and the product owner, who decides it and accepts its ADR.
- Scope: In: that each change to the standard and its rule files is an ADR first, the forward pointers and index rows of those ADRs, that the standard and the rule files follow, and the ADR template and the templates index as standards. Out: drafting, checking and accepting an ADR with the decision play, what the standard and the naming rule say, and Phoenix memory's copies.

## Expectation
- Scenario: In a clinic's booking app, the technical lead renames the reminder plays. An ADR is accepted first; it supersedes the old naming ADR in part and names the part; the old ADR's status line points forward to it; the index lists it; and the naming rule files change in the same change. In a harness repository, a verb is added to the rule file with no ADR behind it, and the change is named as owed in the next decision on the verbs.
- Done means: Someone other than the one who changed the standard reads the history of the standard and the rule files, the ADR folder and the index, and finds an accepted ADR behind each change or the change named as owed, a forward pointer on every older ADR an accepted ADR supersedes or amends, each ADR in the index with its status, and the page and the rule files matching each accepted ADR or the difference named as owed.
