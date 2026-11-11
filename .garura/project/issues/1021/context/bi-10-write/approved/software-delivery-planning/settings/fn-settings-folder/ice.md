## Intent
- Goal: Every settings file other than the one settings file sits in one settings folder beside it, `core/config/` in the source and `.garura/core/config/` in each project, starting with the learned policy, whose pointer in the settings file follows it, while a tool's own settings stay with the tool and a play's own lookup tables stay with the play, so a person and a play know where every settings file is.
- Limit: The one settings file stays where it is, as the entry point.
- Limit: A tool's own settings, a play's own lookup tables, the coding tool's own settings, the install record and the engine state do not move.
- Limit: A pointer in the settings file always names the file's place in the folder.
- Fails if: A settings file other than the one settings file sits outside the settings folder, a tool's own folder or a play's reference folder.
- Fails if: The settings file points to a settings file at a place where it is not.
- Fails if: A tool's own settings are moved away from the tool.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the settings file and every setting in it that points to another file, the learned policy and where the settings say it is, each tool's own settings, each play's lookup tables, and #946.
- Never read: any memory file by its path, any ICE page, and the value of any access key or other secret.
- Persona: the technical lead, who keeps the project's settings and looks for a settings file in one place.
- Scope: In: the settings folder, what goes into it and what stays out, and the pointers to the files in it. Out: moving the folder into existing projects, where every other part lives, what the learned policy holds, and what each setting means.

## Expectation
- Scenario: In a clinic's booking app, the learned policy is written for the first time, into the settings folder, and the settings file names it there. In a game studio's build, the memory tool's own settings stay beside the memory tool, and the play's kind map stays with its play.
- Done means: Someone other than the one who laid the folder lists every file in the source and in an installed project, and finds every settings file other than the one in the settings folder, a tool's own folder or a play's reference folder, and every pointer in the settings file naming a file that is there.
