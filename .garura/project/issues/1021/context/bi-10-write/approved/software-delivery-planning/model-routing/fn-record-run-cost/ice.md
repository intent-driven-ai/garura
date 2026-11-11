## Intent
- Goal: Each run of a play or a loop records, for each part it ran, the model and the effort it ran on, how long it took and what it cost in tokens, in the run's issue folder, so a person can see which parts are slow or costly for their job and move a part up or down.
- Limit: A value the run cannot get is left empty and named as such, never made up.
- Limit: The record is per part, not only per run.
- Limit: Where the records live, the evidence setting and moving a part stay with their owners.
- Fails if: A part a run started is missing from its record, or its record lacks the model, the effort, the time or the cost with no word on why.
- Fails if: A value in the record is one the run did not have.
- Fails if: A person cannot tell from the record which part of a run cost the most.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: what the coding tool reports for each sub-agent and skill a run starts; the session stamp a play writes at its close and the evidence setting; the loop's check record; the rebuild eval's record of its agents' cost; and where a run's records live in its issue's folder.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who pays for each run in tokens and waits for it, and wants to see which part costs what.
- Scope: In: the record of each part's model, effort, time and cost, for each run of a play or a loop, and the empty value where the run cannot get one. Out: where the records live, the evidence setting, and moving a part on the record.

## Expectation
- Scenario: In a shop's checkout project, a plan session sends two sub-agents and three skills. At its close, its record names each of the five with its model, effort, time and cost, and shows the drafting skill on `opus` used most of the tokens. In a game studio's build, a loop of three rounds ends; its record lists each round's plays and the parts under each, and the one part whose cost the coding tool did not report shows an empty cost, named as not reported.
- Done means: Someone other than the one who ran them reads the two runs' records and the coding tool's own reports, and finds every part each run started, each with its model, effort, time and cost matching what the tool reported, the empty cost named as not reported, and no value the runs did not have.
