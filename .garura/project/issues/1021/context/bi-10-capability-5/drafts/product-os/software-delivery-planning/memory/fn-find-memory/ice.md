## Intent
- Goal: An agent finds what it needs through one memory tool, which looks in the named issue's short-term memory, then Garura memory, then Phoenix memory at its approved version, stops at the first tier that answers, skips no tier, says `tier_missing` when a tier cannot be reached, and gives every answer its tier, file, lines and fingerprint, so every agent finds memory the same way and every decision can name what it rested on.
- Limit: Short-term memory is only the folder of the issue the lookup names; another issue's folder is refused.
- Limit: The tool never copies a file from Phoenix memory, and never reads Phoenix memory at a version no person approved.
- Limit: A lookup never returns an update that waits for a person, or a decision record.
- Limit: The tool takes each tier's place from its settings, never from a fixed path.
- Fails if: A lookup answers from a lower tier's miss as "nothing found" while a higher tier was not looked in, or a tier that cannot be reached is not named.
- Fails if: A lookup returns text from another issue's short-term memory, from a waiting update, or from Phoenix memory at a version not approved.
- Fails if: An answer's text comes without its tier, file, lines or fingerprint, or its fingerprint does not match the text.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the memory tool's contract and its answer rules, its settings and where each tier lives, the lookup order inside Garura memory, Phoenix memory's approved version, the folders a lookup must hide, and the memory guide every agent reads.
- Never read: any memory file by its path, and any ICE page; nor another issue's short-term memory.
- Persona: the developer, a person or an AI agent who builds the code and decides from what memory holds.
- Scope: In: the four commands that find memory, the lookup order, the one-issue rule for short-term memory, the approved version of Phoenix memory, the errors, and what every answer carries. Out: memory updates, the trace, the copy into short-term memory and the checks of parts, downloading Phoenix memory, laying the tool in a project, what each setting means, and Ask memory.

## Expectation
- Scenario: In a clinic's booking app, the developer's agent searches for how long a password reset link lasts. The issue's short-term memory and Garura memory have nothing, and Phoenix memory answers from its user-management page at the approved version, with the file, the lines and a fingerprint; the agent then tries to read a note in another issue's folder and is refused. In a bank's payments service, the same search stops at the project's own rule in Garura memory, and Phoenix memory is not looked in.
- Done means: Someone other than the one who built it runs the same searches on the two projects and finds, for the clinic, the answer naming Phoenix memory with its lines and a fingerprint that matches the text, and the read of another issue's folder refused; for the bank, the answer naming Garura memory and Phoenix memory left out of the tiers looked in; and in neither, any waiting update or decision record among the hits.
