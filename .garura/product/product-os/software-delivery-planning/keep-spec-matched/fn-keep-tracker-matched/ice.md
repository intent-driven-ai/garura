## Intent
- Goal: Each intent's issue in the tracker says what its page in the product model says, so people and agents work from the same intent.
- Limit: The page's approved words are the source; an issue's words never replace a page's words without the person's decision.
- Limit: Nothing is written to the tracker before a person's yes, and only a tool that reads the settings reaches the tracker.
- Fails if: An intent's issue and its page say different things, and nothing names it.
- Fails if: An intent's issue is read from the work tracker, or a page's id does not match its issue.
- Fails if: An issue or a page changes to match the other with no person's yes.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the intent pages and their Tracker lines, the intents' issues as the tracker holds them, the project's tracker settings, and the rule for writing an intent's number.
- Persona: the product owner, who reads an intent in the tracker and in the model.
- Scope: In: comparing an intent's issue with its page, naming each difference, changing the issue to the page's approved words, the issue of a replaced or retired intent, and the page's id and Tracker line. Out: the tracker settings, tracking the agent work's status, making issue types, choosing an intent's words, changing work items, and filing a new intent's issue.

## Expectation
- Scenario: An intent's page gets new words from approved words. The difference with its issue is named, and after the person's yes the issue shows the same words as the page.
- Done means: Someone other than the one who changed the page opens the issue that the page names, in the intents tracker, and finds the same title and words.
