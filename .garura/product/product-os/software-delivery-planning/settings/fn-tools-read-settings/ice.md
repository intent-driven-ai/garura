## Intent
- Goal: Each of Garura's tools reads the settings meant for it from where they live, the project's settings file for what a project chooses and the tool's own settings file for the tool's own, with no value fixed in the tool that a setting is meant to hold, so a team changes what a tool does by changing a setting, never the tool or the command that runs it, and this intent's proof, "Every tool reads its settings.", holds.
- Limit: A tool's own settings stay with the tool, and the install writes them.
- Limit: A tool that reaches a tracker takes it only from the trackers setting.
- Limit: A tool never fixes in its own code a value that a setting holds.
- Fails if: A tool uses a fixed default in place of the setting a project chose, such as a plans folder other than the one the plans setting names.
- Fails if: A tool reaches a tracker that the trackers setting does not name.
- Fails if: A team must change a tool, or every command that runs it, to change what the tool does.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: each of Garura's tools and where it takes each value from, its own settings file where it has one, the project's settings it is meant to read, the plays that run each tool and what they pass to it, and #946 and #1023.
- Never read: any memory file by its path, any ICE page, and the value of any access key or other secret.
- Persona: the technical lead, who changes a setting and expects every tool to follow it; and the developer, a person or an AI agent who builds the code, whose plays run the tools.
- Scope: In: every tool reading the settings meant for it, from the project's settings file or its own. Out: building the Agent-work tool, where each tool lives, laying a tool and its settings, how the memory tool finds memory, and what each setting holds.

## Expectation
- Scenario: In a clinic's booking app, the team keeps its plans in another folder and changes the plans setting; the plan tool, run with no folder given, shows the plans from there. In a bank's payments service, the memory tool's own settings name where Phoenix memory is kept on the machine, and an agent's memory lookups read from there with no settings of their own.
- Done means: Someone other than the one who changed the settings runs each tool with no value given on the command, and finds the clinic's plan tool showing the plans from the folder the setting names, the bank's memory tool reading from the place its settings name, and no tool using a fixed value where a setting is meant to hold it.
