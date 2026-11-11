## Intent
- Goal: Every setting that an approved page of another capability asks for is in the settings file with what it means and who reads it: the question tier, the loop settings, who decides the review and the trackers, which exist, and the test model, the three design settings, the kinds of change that may go ahead on their own, the connections and the review rounds, which do not yet; and each capability reads its choice from there, so a team makes each choice once for the project.
- Limit: A tracker is named only in the settings; a connection names only where its access key is kept, never the key.
- Limit: Every kind of change starts as one that waits for a person, until the team sets it to go ahead on its own.
- Limit: A loop's sub-agent checker names a model that is not the session's.
- Limit: This feature keeps the setting; what is done with its value stays with the capability that reads it.
- Fails if: A setting that an approved page asks for is not in the settings file, or is there with no reader.
- Fails if: A settings file holds an access key, password or token.
- Fails if: A capability takes a choice that a setting holds from anywhere other than the settings.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the approved pages that ask for a setting and the capability that reads each, the settings file's question tier, loop, review and tracker settings, the scripts and plays that read them, and the settings asked for that do not exist yet.
- Never read: any memory file by its path, any ICE page, and the value of any access key or other secret.
- Persona: the product owner or the technical lead, who makes each choice once for the project; and the developer, a person or an AI agent who builds the code, whose plays read those choices.
- Scope: In: keeping each setting another capability needs, with what it means and who reads it. Out: what each capability does with its setting, which models there are to choose from, the tool that reaches the trackers, the checkpoint and evidence settings, and making every tool read its settings.

## Expectation
- Scenario: In a game studio's build, the team sets the question tier to s and names a checker model for its loop that is not the session's; /shape-slice asks at most 12 questions, and the loop's check runs on that model. In a bank's payments service, the settings name Jira for the business intents and GitLab for the work, a connection names where its key is kept, and two review rounds come before a finding goes to a person.
- Done means: Someone other than the one who set the values reads the settings file and each reading capability's run records, and finds every setting an approved page asks for with what it means and its reader, the studio's runs using the tier and the checker model, the bank's trackers and review rounds in the settings, and no access key in any settings file.
