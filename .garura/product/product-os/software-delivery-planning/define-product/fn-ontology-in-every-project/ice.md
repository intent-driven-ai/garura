## Intent
- Goal: Every project's agents read the same current map, named in the settings by its place in memory and read through the memory tool, from Phoenix memory when the project's own memory holds no copy, and each skill reads only the part its sub-agent copied into the issue's short-term memory, so that every project writes and checks its model by the version Garura's source holds.
- Limit: The map is named by its place in memory, never by a path on a machine.
- Limit: An agent reads the map only through the memory tool; a skill reads only the copy in short-term memory.
- Limit: This feature never writes to Phoenix memory or to Garura memory.
- Fails if: An agent reads the map by its path, or a skill reads it from anywhere other than the copy its sub-agent made.
- Fails if: The map the memory tool answers differs from the map in Garura's source.
- Fails if: A play finds no map, because neither the project's memory nor Phoenix memory answers it.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the settings' place of the map in memory, the tier that answers it and its fingerprint, the map's version in Garura's source, and the plays that hand the map to their agents.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, a person or an AI agent who builds the code, whose play's agent reads the map; the technical lead, who keeps the project on a version of Garura.
- Scope: In: naming the map by its place in memory, reading it through the memory tool, and the copy a skill reads. Out: keeping Phoenix memory in step with Garura's source and its versions, what the map says, and the memory tool itself.

## Expectation
- Scenario: In a clinic's booking app, whose own memory holds no copy of the map, the sub-agent that drafts a new intent looks the map up through the memory tool; Phoenix memory answers it at version 15, the same as Garura's source, and the sub-agent copies the Business Intent kind into the issue's short-term memory for the skill. In a bank's payments service, the same lookup gives the same version and the same fingerprint.
- Done means: Someone other than the one who ran the play reads the memory tool's answer and the run's short-term memory, and finds the map answered by Phoenix memory at the version Garura's source holds, the same text word for word, and the skill's copy taken from that answer, with no memory file read by its path.
