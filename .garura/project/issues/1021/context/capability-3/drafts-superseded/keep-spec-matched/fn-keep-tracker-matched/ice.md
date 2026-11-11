## Intent
- Goal: Each intent's issue in the intents tracker says what its page says: the same title, outcome, why, asked by, proof and limits.
- Limit: The page's approved words are the source; an issue's words never replace a page's without a person's approval.
- Limit: Nothing is written to the tracker before a person's yes, and no play, skill or sub-agent names a tracker; only a tool that reads the settings does.
- Limit: An intent page's id is always its issue's number in the intents tracker.
- Fails if: An intent's issue and its page say different things, and nothing names it.
- Fails if: A page's id does not match its issue, or an intent's issue is read from the work tracker.
- Fails if: An issue or a page is changed to match the other with no person's yes.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the intent pages and their Tracker lines, the project's tracker settings and the code host's setting, the intents' issues as the tracker holds them, and the rule for writing an intent's number.
- Persona: the product owner, who reads an intent in the tracker and in the model.
- Scope: In: comparing an intent's issue with its page, changing the issue to the page's approved words, naming each difference, and the page's Tracker line and id. Out: the tracker settings, the tool for agent work and its tracking, making issue types, choosing an intent's words, and filing or closing an intent's issue.

## Expectation
- Scenario: An intent page is rewritten from approved words, and after the person's yes its issue in the intents tracker shows the same words.
- Done means: Someone other than the one who changed the page opens the issue the page names in the intents tracker and finds the same title and words.
