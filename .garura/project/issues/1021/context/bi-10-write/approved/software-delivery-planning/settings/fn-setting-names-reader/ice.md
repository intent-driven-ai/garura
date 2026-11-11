## Intent
- Goal: Every setting in the settings file, in the source and in each installed project, is in one list with what it means and the play or tool that reads it, and a check fails, naming it, every setting no one reads and every play's setting whose play no longer exists, so no setting stays that changes nothing when a person changes it.
- Limit: A reader is looked for in a play's text as well as in its scripts.
- Limit: A setting for a part that is gone is renamed or removed only once why it was added is known.
- Limit: The check runs on the source and on each installed project.
- Fails if: A setting that no one reads, or one named for a part that is gone, passes the check.
- Fails if: A setting is in the file and not in the list, or the list names a reader that does not read it.
- Fails if: A setting that a play really reads is removed as unread.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the settings file in the source and in an installed project, the text and scripts of every play and every tool that reads a setting, the plays, loops and tools that exist and their old names, and #946 and #947.
- Never read: any memory file by its path, any ICE page, and the value of any access key or other secret.
- Persona: the technical lead, who keeps the project's settings and wants none that change nothing.
- Scope: In: the list of settings with their meaning and readers, and the check of settings no one reads and settings for parts that are gone. Out: renaming settings on an upgrade, where other settings files live, and the checks of plays, skills and sub-agents.

## Expectation
- Scenario: In a clinic's booking app, the check runs on the installed project and fails on a setting left from a removed play, and on a checkpoint setting under a play's old name; the technical lead removes the first and renames the second, and the check passes. In a bank's payments service, a new play's setting is in the list with the play as its reader, and the check passes on the first run.
- Done means: Someone other than the one who ran the check reads the list, the settings file and the check's report, and finds every setting in the list with its meaning and a reader that really reads it, and no setting that the check passed and no one reads.
