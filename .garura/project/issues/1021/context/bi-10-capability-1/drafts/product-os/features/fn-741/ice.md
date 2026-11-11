## Intent
- Goal: One rename map lists every old name of a part with its new name, or with none when the part was removed, and a read-only check finds every use of an old name outside past records, by file and line, so a rename is done only when the check exits clean, and the install can take out a part left under an old name.
- Limit: Past records keep their old words: the run records, the changelog, the ADRs before ADR 046, the ADRs that record the renames and the ADRs that quote older words.
- Limit: The check only reads: no git, no network and no model.
- Limit: A name removed with no successor stays in the map, mapped to none, so the check still reports it.
- Fails if: An old name is still used in a part, a doc or a test, and the check exits clean.
- Fails if: The check reports a use in a past record or an accepted ADR.
- Fails if: A rename lands with no line in the map, so the install cannot take out the part under its old name.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the rename map, the old-name check with its rules for one-word names and past records, the rename tool, the tests of the naming tools, the install's step that takes out old names, and the renames an accepted ADR decides.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead, who runs a rename; and the developer, a person or an AI agent who builds the code, who changes the names the check lists.
- Scope: In: the rename map, the old-name check, the rename tool and their tests. Out: the naming rule, each family's rename, the other checks, and taking out old parts in a project.

## Expectation
- Scenario: In a clinic's booking app, the team renames the reminder plays and removes one play with no successor. The map gains a line for each, the check lists two guides that still name the old plays and one that names the removed play, and it exits clean once they are changed; an old ADR that names an old play is not reported. In a harness repository, the rename tool moves every skill the map lists and the check then exits 0.
- Done means: Someone other than the one who ran the rename runs the old-name check, reads the map and the report, and finds every renamed or removed part in the map, each use of an old name named by file and line or none left, no past record or accepted ADR reported, and a test for a name removed with no successor.
