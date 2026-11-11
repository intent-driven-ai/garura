## Intent
- Goal: Once an ADR is accepted, every older ADR it supersedes or amends carries a forward pointer to it, with the part it changes, on its Status line or in its pointer fields and nowhere else; and the index of ADRs is rebuilt from the ADR folder, with a row for every ADR reading its own status, so a reader of any ADR finds what replaced it and the index shows which ADRs hold.
- Limit: No pointer is written while the newer ADR is proposed.
- Limit: An older ADR changes only in its forward pointer, and its status when it is superseded in full.
- Limit: An ADR is superseded in full only once, and no pointer is written twice.
- Limit: The index is made only by its script, from the ADR folder.
- Fails if: An older ADR that an accepted ADR names in its Supersedes or Amends line has no pointer to it, or the run reports it linked when it is not.
- Fails if: An older ADR changes beyond its pointer, or gets a pointer before the newer ADR is accepted.
- Fails if: The index leaves out an ADR in the folder, or lists one with a status its own Status line does not hold.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the accepted ADR and its Supersedes and Amends lines, the older ADRs the gathered context names with their kind and part, the Status line of each older ADR, the ADR folder, and the index.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead or the developer who reads an older ADR and needs to know what replaced it; the person who accepted the newer ADR.
- Scope: In: the forward pointers, their checks before any write, the index and its check. Out: drafting the ADR and naming what it changes, the accept, reviewing older ADRs, the review tool's list of ADRs, and product decisions in the model.

## Expectation
- Scenario: In a logistics app, the product owner accepts an ADR that amends the part of an older ADR on how often the carrier is asked, and supersedes in full a second older ADR. After the run, the first older ADR's Status line reads amended in part by the new ADR, with that part; the second reads Superseded by it; nothing else in either changed; and the index lists the new ADR as Accepted and the second older one as Superseded. In a school's timetable app, a loop's run saves an ADR as proposed, and no older ADR changes until a person accepts it.
- Done means: Someone other than the one who ran it compares each older ADR with its version before the run, and the index with the ADR folder, and finds each older ADR named in the new ADR's lines changed only on its Status line with a pointer to it, the run's linked report true only because each pointer is there, a row in the index for every ADR file with its own status, and, for the school's run, no older ADR changed.
