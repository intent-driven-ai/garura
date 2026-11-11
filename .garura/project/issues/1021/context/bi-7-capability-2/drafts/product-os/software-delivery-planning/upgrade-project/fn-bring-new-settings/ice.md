## Intent
- Goal: When a project moves to a new version, each setting and settings file the new version adds reaches the project, every value the team set stays with the file's comments and order, a setting that names a renamed part moves to its new name with the team's value, a setting the new version dropped goes only on the person's yes, and Garura's instructions go beside the team's instructions file only when a rule is missing, each shown first and named in the report.
- Limit: No value the team set is changed or lost, and no setting of the team's goes without the person's yes for it.
- Limit: The team's instructions file is never written over; Garura's instructions go beside it only when it lacks one of Garura's rules, with that rule named.
- Limit: The upgrade decides nothing about what a setting means or who reads it; it brings in what the new version defines.
- Fails if: After the upgrade, a value the team set is different or gone, or a setting went with no yes.
- Fails if: A setting the new version adds is missing from the project, or a setting still names a part by its old name.
- Fails if: Garura's instructions are written beside a team file that already holds every rule, or the team's own file changed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the team's settings files as they are, the new version's settings files, the rename map, the settings the new version no longer has, the team's instructions file and Garura's instructions of the new version.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who set the team's values and decides which settings go.
- Scope: In: new settings and settings files, the team's values kept, settings for renamed parts, settings the new version dropped, and Garura's instructions beside the team's file. Out: what each setting means and who reads it, where settings files live, the rename map's contents, the first install's instructions, edited installed parts, and the coding tool's own settings.

## Expectation
- Scenario: A bank's payments service named its own tracker in its settings file and turned its review gate off under the review play's old name. On the upgrade, the list shows four new settings to come in, the gate setting to move to the play's new name, and one setting for a play Garura dropped. The product owner says yes. Afterwards the tracker is still named, the four settings are there, the gate is off under the new name, the dropped play's setting is gone, the file's comments are as they were, and nothing is written beside the bank's instructions file, which already holds every rule.
- Done means: Someone other than the one who ran the upgrade compares the settings files and the instructions file before and after with the new version's settings and the list, and finds every team value kept, every new setting in, no old part name left in a setting, nothing gone without a yes, and the instructions file unchanged.
