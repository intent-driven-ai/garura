Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: A check reads every play, skill and sub-agent, names each one that names a tracker or calls a tracker's command line with its file and line, warns while the parts move onto the Agent-work tool, and fails once they have moved, so no play, skill or sub-agent names a tracker.
- Limit: It comes with the Agent-work tool (#1023), not before.
- Limit: It reads the parts and reports; it changes none.
- Limit: It reads plays, skills and sub-agents; the Agent-work tool, which calls the trackers, is not read.
- Fails if: A part that names a tracker passes after the parts have moved.
- Fails if: The check fails a change before the parts have moved, instead of warning.
- Fails if: The check names a part that does not name a tracker.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: this intent's Must not, ADR 065's rule 4, #1023 (an Agent-work tool reads the tracker setting) and its count of parts that name a tracker, the tracker settings, the Agent-work tool, and the component linter's rule families.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead, who turns the check from a warning to a failure; and the developer, a person or an AI agent who builds the code, whose part the check names.
- Scope: In: the check, its warning and its failure. Out: the Agent-work tool, moving the parts onto it, the tracker settings, and the other checks.

## Expectation
- Scenario: In a bank's payments service that uses Jira, the check warns on a skill that still calls GitHub's command line, naming its file and line, while the parts move; once they have moved, the same call fails the check. In a clinic's booking app on GitLab, a part that calls only the Agent-work tool passes.
- Done means: Someone other than the one who built the check runs it before and after the parts move, reads its reports and the parts it names, and finds every part that names a tracker named with its file and line, a warning before and a failure after, and a part that calls only the tool passing.
