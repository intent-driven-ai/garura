## Intent
- Goal: Business intents live in the tracker the settings name for them, apart from agent work, and each intent page names its issue there.
- Limit: No play, skill or sub-agent names a tracker; only a tool that reads the settings does.
- Limit: An intent page's id is always its issue's number in the intents tracker.
- Fails if: An intent is filed in the work tracker, or a page's id does not match its issue.
- Fails if: A bare number is written where it could mean an intent or a work issue.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the project's tracker settings, the code host's setting, the intent pages and their Tracker lines, and the rule for writing an intent's number.
- Persona: the product owner, who looks up an intent by its number.
- Scope: In: the setting that names the intents tracker, the page's issue line and id, and the rule that BI-1 is an intent and #1 is work. Out: the tool for agent work and its tracking, making issue types, and the intent's words.

## Expectation
- Scenario: An intent page for issue 1 of the intents tracker is named bi-1 and names #1 as its issue.
- Done means: A person who did not write the page opens the issue it names in the intents tracker and finds the same intent.
