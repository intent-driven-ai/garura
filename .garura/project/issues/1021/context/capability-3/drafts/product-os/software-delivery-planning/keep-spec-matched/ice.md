## Intent
- Goal: The spec matches what the agents build and plan: each intent, domain, capability and feature matches the work, and each difference is named and fixed on a person's approval.
- Limit: An intent's or a model part's words change only through words a person approved, and only a person confirms or drops an intent.
- Limit: A change to an intent's words keeps its record of what was done.
- Limit: Nothing is removed while a part still names it, and every removal names the person who approved it.
- Limit: Drift is named to a person, never fixed in silence, and an intent is never changed to match the work without that person.
- Fails if: An intent's or a part's words change with no person's approval behind them.
- Fails if: A part serves an intent and the intent's page does not show it, or the page shows a part that does not serve it.
- Fails if: The spec and the work disagree, such as a feature built with no page or a page that says something the work no longer does, and nothing names it.
- Fails if: An intent's issue in the tracker says something its page does not, and nothing names it.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the intent pages, the model's index and the intents it links to each part, the pages of the domains, capabilities and features, the plan files and the work items in the tracker, the setting that names the tracker for intents, and the rules of the Business Intent kind.
- Persona: the product owner, who approved the spec and decides each drift.
- Scope: In: finding drift between the spec and what is built or planned, updating intents and model parts from approved words, keeping each intent's links current, replacing and retiring intents, and keeping an intent's words in the tracker matched to its page. Out: the first specification and keeping what a person gave, cutting the spec into work items and changing them, what users tell us once the product runs (Run → Product), the link rules, and drift inside the model with no work in it.

## Expectation
- Scenario: A feature is built and its page still says what it did before; the drift is named, the person approves new words, and the page then matches the work.
- Done means: The gap finder, run over the whole model by someone other than the one who linked the parts, reports no link to an intent held on one side only.
- Done means: Plant a known difference between the spec and the work in a copy of the project, and a review run by someone other than its author names it.
