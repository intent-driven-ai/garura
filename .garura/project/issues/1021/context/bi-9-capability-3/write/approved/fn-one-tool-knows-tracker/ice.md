## Intent
- Goal: One tool reads the project's settings for the tracker of business intents, the tracker of agent work and the code host, and makes every read and write of an intent or a work item there, so no play, skill or sub-agent names a tracker or calls its command line, and changing a setting changes the tracker with no other edit.
- Limit: Only the tool names a tracker or calls its command line; no play, skill or sub-agent does.
- Limit: The tool learns where each tracker is from the project's settings only: the tracker of business intents, the tracker of agent work and the code host.
- Limit: One setting names who owns each tracker, and no second setting names another owner.
- Fails if: A play, skill or sub-agent names a tracker or calls its command line, and the check passes it.
- Fails if: Changing a tracker setting needs an edit to a play, skill or sub-agent.
- Fails if: An intent or a work item is read from, or written to, a tracker other than the one the settings name for it.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the project's settings for the trackers and the code host, the adapter's named actions and the copies of its script, the plays, skills and sub-agents that call a tracker's command line or name a tracker, and the parts that wait for the tool.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, a person or an AI agent who builds the code, who moves the parts that reach the tracker onto the tool; and the product owner, who chooses the team's tracker as a setting.
- Scope: In: the tool, the settings it reads, moving the parts onto it, fixing the older owner setting, and the check that fails a part that names a tracker. Out: what each setting means and the rule itself, making the tracker's types, what each type means, the link from the work to its intent, landing approved writes once, and a way past the wait for the tool.

## Expectation
- Scenario: In a clinic's booking app, the settings name GitHub for the business intents and for the work. /shape-plan files an epic and its stories through the tool, and no play holds a GitHub command. The team then moves its work to GitLab: a person changes the setting of the work tracker, and the next session's closes reach GitLab with no play, skill or sub-agent edited. A developer adds a skill that calls the GitHub command line, and the check fails it by name.
- Done means: Someone other than the one who built the tool reads the plays, skills and sub-agents, the settings and both trackers before and after the change of setting, and finds no tracker named or called outside the tool, every item in the tracker the settings name for it, no part edited for the move, and the check failing the skill that calls the command line.
