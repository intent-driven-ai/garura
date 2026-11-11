## Intent
- Goal: Every setting that Garura's plays, scripts and loops read is in one settings file, written once in Garura's source as `core/config.yaml` with each key once, and laid by the install as each project's own copy at `.garura/core/config.yaml`, which that project's plays read at pre-flight and in which the team sets its own values, so a team has one place where everything that can be turned on or off lives.
- Limit: A project's plays read its installed copy, never Garura's source.
- Limit: In Garura's own repository, a setting is changed in the source, and the installed copy changes only by an install.
- Limit: No key is in the file twice.
- Limit: Paths go in the settings, never in memory.
- Fails if: A play reads a setting from anywhere other than its project's settings file.
- Fails if: The settings file holds a key twice, so one value silently replaces the other.
- Fails if: An installed copy lacks a block of the source, or holds it under an old name, and no one is told.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: Garura's source settings file and each project's installed copy, the blocks and keys each holds, the play pre-flight that reads the file, and the decision that the source is `core/config.yaml` and the copy in `.garura/` is installed.
- Never read: any memory file by its path, any ICE page, and the value of any access key or other secret.
- Persona: the technical lead, who keeps the project's settings; and the developer, a person or an AI agent who builds the code, whose plays read them.
- Scope: In: the one settings file, its source, its installed copy, a team's own values in it and how a play reads it. Out: laying the file in a project, new settings on an upgrade, what each setting means and who reads it, other settings files, and where each part lives.

## Expectation
- Scenario: In a bank's payments service, the install lays the settings file, the technical lead names the bank's own tracker in it, and /start-change reads that copy at its pre-flight. In Garura's own repository, a change to the review setting is made in `core/config.yaml`, and the installed copy shows it only after an install.
- Done means: Someone other than the one who set it up reads the project's settings file, the source file and a play's pre-flight facts, and finds one settings file laid from the source, each key in it once, the team's own values kept, and the play's facts taken from that copy.
