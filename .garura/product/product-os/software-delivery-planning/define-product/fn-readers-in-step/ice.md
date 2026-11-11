## Intent
- Goal: The page templates, the index's schema, the structure check and the glossary say what the map's current version says, an ICE page template among the templates, the fields named as the map names them, no warning for an ICE that is on its own page, and the glossary's words the map's words, and each change to the map brings them with it, so that every page written, every index read and every model checked follows the same map.
- Limit: A page made before a change still passes; what it lacks is a warning to fix later, never an error that stops work.
- Limit: Each of the four changes only to follow the map; none adds a rule the map does not hold.
- Limit: Every copy of the structure check stays the same as the others.
- Fails if: A template puts a section in a part's page that the map moved to its own page, or no template exists for a kind of page the map defines.
- Fails if: The index's schema, the structure check or the glossary names a field, a count or a link in a way the map has replaced.
- Fails if: A change to the map lands, and one of the four still says what the map said before it, with nothing recorded as owed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the map at its current version and its log, the page templates, the index's schema, every copy of the structure check and its last report, the glossary, and the open issues on plays that write ICE pages and on moving Garura's own model.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead and the developer, a person or an AI agent who builds the code, who write a page from a template or read the structure check's report; a newcomer who reads the glossary.
- Scope: In: the page templates, the index's schema, the structure check and the glossary, kept to the map, and the list of what still disagrees. Out: what the map says, running the model's checks around a change, the ready check and the gap finder, renaming the needs field with its link check, the discovery plays, moving a team's model to a new version's shape, and bringing a template to Phoenix memory.

## Expectation
- Scenario: In a clinic's booking app, the map moves the ICE to its own page. In the same release, the capability and feature templates lose their ICE section, an ICE page template is added, the structure check stops asking for an ICE section on a part whose ICE is on its own page, and the glossary says the ICE is its own part. The next capability page written has no ICE section, and its ICE page passes the check. In a bank's payments service, the map lets a capability be identified by more than one other capability, and the index's schema and the structure check both accept two ids there.
- Done means: Someone other than the one who changed them reads the map's last log line, the templates, the index's schema, the structure check and the glossary, runs the structure check on a model whose ICE are on their own pages, and finds each of the four saying what the map says, an ICE page template there, no warning for a missing ICE section, and every copy of the check the same.
