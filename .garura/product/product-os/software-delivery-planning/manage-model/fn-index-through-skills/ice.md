## Intent
- Goal: Every change to the model's index, adding, changing or taking out a part, goes through link-model-part or remove-model-part, each changing only what its request names, all or nothing, with every file listed and the index's comments and layout kept; the live plays and the gap closer move onto them, and the skills grow what the plays still need, a new slice, the product profile and an epic's status.
- Limit: A take-out through the skills names the person who approved it.
- Limit: Until a skill can make a change, the play's own script keeps making it, and a stale play moves only when it is rebuilt.
- Limit: Each play moves through its own ICE, rebuilt, never by a hand edit of its compiled file.
- Fails if: A play or a skill writes the index with a script of its own for a change the two skills can make.
- Fails if: A change through the skills changes something its request did not name, or leaves a file out of its report.
- Fails if: A moved play's ICE does not say that it changes the index through the two skills.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: ADR 065's first rule, the two index skills and their request shapes, the keeper's routes, the plays that write the index with their own scripts and which are stale, the gap closer, what the skills cannot write yet, and the need that plays change the model's index through the two index skills.
- Never read: any memory file by its path, any ICE page, and any file in a plan's evals folder.
- Persona: the technical lead, who moves each play onto the two skills; and the developer, a person or an AI agent who builds the code, who writes the index from a play.
- Scope: In: the two index skills as the one way into the index, moving the live plays and the gap closer onto them, and growing the skills for a new slice, the product profile and an epic's status. Out: the words of each page, rebuilding a play from its ICE, Phoenix memory's copy of the rule, and what a take-out may remove.

## Expectation
- Scenario: In a clinic's booking app, /shape-slice, once moved, writes a new slice for "patients book online" by asking the keeper, and link-model-part writes the slice's entry, lists every file it changed and keeps the index's comments. In a shop's checkout service, /discover-capabilities saves three capabilities the same way, and its ICE says it changes the index through the two skills.
- Done means: Someone other than the one who moved the plays reads each live play's scripts, its ICE and the skills' reports, and finds no script of its own that writes the index for a change the skills can make, every file the clinic's and the shop's runs changed named in the reports, and each moved play's ICE naming the two skills.
