## Intent
- Goal: Every choice a team turns on or off, or picks, once for the project lives in one settings file, laid as each project's own copy, with every other settings file in one settings folder beside it; each setting says what it means and who reads it, and a check fails a setting no one reads; each checkpoint is turned on or off there, the learned policy keeps what a person's answers taught, and the evidence file is turned on or off there; the settings other capabilities need are there; and every tool reads the settings meant for it, so a team changes how Garura works by changing a setting, never a play, a skill or a tool.
- Limit: No setting, policy or ledger turns a pinned checkpoint off, and with no setting a checkpoint waits.
- Limit: No access key, password or token is kept in a settings file; a connection names only where its key is kept.
- Limit: A tracker is named only in the settings, never in a play, skill or sub-agent.
- Limit: The learned policy is a setting, not memory, and it never loses a person's permanent pin.
- Limit: In Garura's own repository, a setting is changed in the source, and the installed copy changes only by an install.
- Fails if: A setting is read by no play, script or tool, or is named for a part that is gone, and no check names it.
- Fails if: A checkpoint waits that the settings turn off, or passes that the settings leave on, because the setting's name is not the one its play reads.
- Fails if: A setting an approved page needs is missing from the settings file, or a tool takes a value that a setting holds from somewhere else.
- Fails if: A pinned checkpoint passes because of a setting.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the settings file in the source and each project's installed copy, every block in it and the play, script or tool that reads each, the gate rule with its kinds and its pinned list, the learned policy and each issue's gate history, the evidence rule, the settings that approved pages of other capabilities ask for, the tools and where each takes its settings from, and #946 and #947.
- Never read: any memory file by its path, any ICE page, and the value of any access key or other secret.
- Persona: the product owner or the technical lead, who chooses once for the project how the team works; and the developer, a person or an AI agent who builds the code, whose plays and tools read those choices.
- Scope: In: the one settings file and its installed copy, what each setting means and who reads it, one folder for every other settings file, the checkpoint settings and the learned policy, the evidence setting, the settings other capabilities need, and every tool reading its settings. Out: the way past each gate and the record of each skip, pinning a checkpoint and adding one to a play, the written standards and their checks, where each part lives, which model each part runs on, the tool that reaches the trackers, what each capability does with its setting, and laying or upgrading the settings file in a project.

## Expectation
- Scenario: In a clinic's booking app, the technical lead turns /commit-change's checkpoint off and names the clinic's tracker in the settings; /commit-change no longer waits, the merge onto main still asks for the product owner's yes, and the settings list names both settings with the play and the tool that read them. In a bank's payments service, the check runs on the installed project and fails on a block left from a play that is gone; the technical lead removes it, and the check passes.
- Done means: Someone other than the one who changed the settings reads the project's settings file, the settings list and the check's report, and finds every setting with what it means and a reader that reads it, no setting with no reader, every other settings file in the settings folder, no access key in any of them, the clinic's off checkpoint passing on its own and its merge still asked.
