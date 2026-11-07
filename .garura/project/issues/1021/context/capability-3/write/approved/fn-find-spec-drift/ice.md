## Intent
- Goal: Every place where the spec no longer matches what the agents built and planned is named to a person, with what each side says and where it comes from.
- Limit: It never changes an intent, a page or a work item itself; each fix lands only after a person's yes, through the part that owns it.
- Limit: It compares the spec with the agents' work only, never with what users say or do once the product runs.
- Fails if: The spec and the work disagree, and nothing names it.
- Fails if: A page or a work item changes during the check.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the intent pages and their stages, the model's index and pages, each part's ICE, the plan files, the work items and the intents' issues in the tracker, the code and its history, and the rules for what must agree once the model is aligned.
- Persona: the product owner, who decides what to do about each drift.
- Scope: In: naming each difference between the spec and what the agents built or planned. Out: making the fixes, drift inside the model with no work in it, and what users say or do once the product runs (Run → Product).

## Expectation
- Scenario: A feature is built and filed as a story with no page in the model, and the check names the story and the missing page.
- Done means: Plant known drift in a copy of the project, and a check run by someone other than its author names each one.
