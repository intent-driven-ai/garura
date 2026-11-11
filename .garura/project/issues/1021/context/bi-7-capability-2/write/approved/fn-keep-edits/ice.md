## Intent
- Goal: When a project moves to a new version, the upgrade finds each installed part and shared file a person changed since Garura laid it, shows the person what they changed and what the new version changes in it, and replaces it only on the person's yes for that part, naming each choice in the report and each part kept on the older version as owed.
- Limit: No installed part or shared file a person changed is replaced, moved or removed without the person's yes for that part; no choice is made for the person.
- Limit: Only files the install record says Garura laid are checked; the project's own parts beside Garura's are never touched.
- Limit: A part the person keeps is named in the report as not moved to the new version.
- Fails if: After an upgrade, an installed part or shared file a person changed is different, and no yes of the person's for it is on record.
- Fails if: A part a person changed was not shown on the list before the upgrade changed anything.
- Fails if: A part the person kept is not named in the report.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the install record and what Garura laid in each file, each installed part and shared file as it is now, the new version's copy of each edited part, and the person's choice for each.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who decides what happens to each part a person edited.
- Scope: In: finding each edited installed part and shared file, showing the change, asking, and naming each choice. Out: the settings file and the instructions file, the list and the report themselves, taking out renamed and dropped parts, and the take-out of all of Garura.

## Expectation
- Scenario: A bank's payments service added a step to an installed play that names its own tracker, and put a file of its own in Garura's shared folder. On the upgrade, the list shows the edited play with the bank's step and the new version's change, and names the file. The product owner keeps the edited play. Afterwards the play is as the bank left it, the file is still there, and the report names the play as not moved to the new version.
- Done means: Someone other than the one who ran the upgrade compares every installed part and shared file a person changed, before and after, with the list and the report, and finds each one shown first, each kept or replaced as the person chose with the yes on record, and each kept part named as owed.
