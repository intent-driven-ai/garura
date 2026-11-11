## Intent
- Goal: Every play and every loop a person can run ends with the one command that comes next and why, printed by the shared close from the one Next-line map, or with no Next line when the map names none, so a person always knows what comes next and no second work list disagrees with the plan.
- Limit: The line comes only from the map, through the shared close; no play words its own Next line.
- Limit: Where the map names no command, the close prints no line and points to no recommender.
- Limit: Every compiled play a person can run is in the map or named as exempt.
- Fails if: A play a person can run closes with no entry in the map and is not exempt, and the play check passes it.
- Fails if: A Next line names a command that is not the map's entry for that play.
- Fails if: A close prints a Next line, or a recommender, where the map names no command.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the Next-line map and its exempt list, the shared close's step that prints the report, the play check of the map, and the name of the play or loop that is closing.
- Never read: any memory file by its path, any ICE page, and any plan's evals folder.
- Persona: the product owner, who reads at the end of each run what to do next; and the developer, a person or an AI agent who builds the code, who picks the next piece of work from the plan when no command is named.
- Scope: In: the Next line, the map's entries, the plain absence of a line, and the play check. Out: choosing which item is worked next, the rest of the closing report, how plays and loops are built, the issues worth attention, and the order in which loops run their plays.

## Expectation
- Scenario: In a shop's checkout project, the product owner runs /shape-slice and its report ends with the Next line that names /shape-plan; the next day a developer's change is merged and /merge-change's report has no Next line. A new play is added to the project with no entry in the map, and the play check fails it and names it.
- Done means: Someone other than the one who ran the plays reads the two reports, the map and the play check's result, and finds /shape-slice's line equal to its map entry, no Next line in /merge-change's report, and the new play named in the check's failure.
