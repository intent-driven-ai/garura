## Intent
- Goal: Phoenix memory reaches each machine once, in one place shared by every project: today the memory tool downloads it whole the first time a command needs it, and the Phoenix install, once per machine, is to lay it and, run again, bring it up to date; it is read only at its approved version; a download that fails leaves nothing behind and answers `tier_missing` with the reason; and `health` reports it without downloading, so every project on the machine reads one current Phoenix memory.
- Limit: The Garura install brings no memory into a project.
- Limit: A download is whole or nothing, never waits for a password, and stops after its time limit.
- Limit: Edits on disk and commits that are not merged are never read as Phoenix memory.
- Limit: Laying the tool in a project, building a project's Garura memory and what a version holds stay with their owners.
- Fails if: A cut-off or failed download is left in Phoenix memory's place, or a lookup reads it.
- Fails if: A lookup reads Phoenix memory at a version no person approved, or `health` downloads anything.
- Fails if: A newer approved version exists and a machine has no way to take it.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the memory tool's settings for Phoenix memory's place, source and approved version; how the tool downloads and versions Phoenix memory; what the install's check reports; and the plan for the Phoenix install in #883 (the Phoenix install).
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, a person or an AI agent who builds the code on a machine where Phoenix memory is not there yet, or is out of date.
- Scope: In: the download on first use, the approved version, the one place on the machine, the `health` report; and, not built yet, the Phoenix install and bringing Phoenix memory up to date. Out: laying the tool in a project and the install's check, building a project's Garura memory, what a version of Phoenix memory holds, retiring the machine-wide copy, and what each setting means.

## Expectation
- Scenario: In a clinic's booking app on a new laptop, the developer's agent runs its first search; the tool downloads Phoenix memory whole into its one place and answers from the approved version. In a bank's payments service, the source cannot be reached; the download fails, nothing is left in the place, and the search answers `tier_missing` with the reason. Later, a newer approved version is released, and the developer runs the Phoenix install again on the laptop.
- Done means: Someone other than the one who built it checks the laptop and the bank's machine, and finds on the laptop one whole copy of Phoenix memory read at the approved version, then the newer version after the second Phoenix install; and on the bank's machine an empty place, the `tier_missing` answer with its reason, and no search answered from a partial copy.
