Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Every change to the map runs the model's checks before and after it, shows the product owner each finding that is new after the change, and records each as owed, so a change to the map never leaves the model broken without anyone knowing.
- Limit: A finding never stops the change to the map or anyone's work.
- Limit: The checks stay Manage the model's; this feature only runs them and compares their reports.
- Limit: A finding that was there before the change is not shown as new.
- Fails if: A change to the map lands with the model's checks not run before and after it.
- Fails if: A new finding is not shown to the product owner, or is not recorded as owed.
- Fails if: A finding stops the change or someone's work.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the map's play and its steps, the model's checks and their reports, the model before and after the change, the product owner's answer on running the checks, and where what is owed is kept.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who changes the map and sees what it breaks; the technical lead, who fixes what is owed.
- Scope: In: running the model's checks before and after a change to the map, the new findings, and recording them as owed. Out: the checks themselves, fixing the model, keeping the structure check in step with the map, moving a team's model, and where what is owed is kept for every gate.

## Expectation
- Scenario: In a bank's payments service, the product owner adds a Regulation kind. Before the change lands, the findings show that 12 capabilities have no link to it yet; the change lands, the 12 links are recorded as owed, and the work of the day goes on. In a shop's checkout service, a rename of a kind shows every page that still uses the old name as a new finding.
- Done means: Someone other than the one who changed the map reads the checks' reports from before and after, the findings shown and the record of what is owed, and finds both runs there, only the findings new after the change shown as new, each recorded as owed, and no work stopped.
