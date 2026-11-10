## Intent
- Goal: Each project on a machine holds only the memory blocks its own answers called for, from the one Phoenix memory, and each run of Initialize in a project names in its brief each part of those blocks that changed, was added or was taken out in Phoenix memory, and takes a change into that project only on the product owner's typed yes, never as a copy of a Phoenix file.
- Limit: Never write Phoenix memory or another project's memory from initialize, and read memory only through the memory tool.
- Limit: Take a change into a project only when Initialize runs in that project and only on the product owner's typed yes; no install changes a project's Garura memory.
- Fails if: a project holds a memory block its own answers did not call for, or initialize in one project changes another project's memory.
- Fails if: a project's Garura memory holds a whole Phoenix file, or a part of Phoenix memory its answers did not select, after a first run or after a yes to a change.
- Fails if: an install changes a file in a project's Garura memory.
- Fails if: a block changed in Phoenix memory and the next initialize run in a project that holds it does not name the change.
- Fails if: initialize builds a project's memory while Phoenix memory cannot be reached.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the project's own block list and the place in Phoenix memory each part was built from; what each block's selection finds in Phoenix memory now; the project's confirmed answers; and whether Phoenix memory can be reached.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who sets up many projects on one machine and decides what each takes in.
- Scope: In: keeping each project's blocks its own, the block list, naming what changed under each block, and taking a change in on a yes. Out: how Phoenix memory reaches the machine, laying Garura's parts, choosing and building the blocks from the answers, a changed answer on a new run, keeping Phoenix memory itself up to date, and promotion.

## Expectation
- Scenario: One machine holds a shop's checkout service, set up with Java, and a bank's payments service, set up with .NET. Only the first holds the Java standards block, and only the second the .NET block. Phoenix memory's Java standards then change in one section. Nothing in either project changes. When the product owner runs Initialize in the shop's service, its brief names the changed section under the Java standards block; after the yes, the project's memory is rebuilt from that section with no copy of the Phoenix file, and the bank's service is as it was.
- Done means: Someone other than the one who ran it compares both projects' Garura memory and Phoenix memory before and after, and finds the change named in the first project's brief, taken in only after its yes, no whole Phoenix file in either project, and nothing changed in the second project or in Phoenix memory.
