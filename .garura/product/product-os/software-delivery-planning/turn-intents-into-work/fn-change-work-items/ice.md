## Intent
- Goal: Every change to the work items that the person approved reaches the tracker and the plan file in one landing, and the two agree afterwards.
- Limit: Nothing is written before a plain "approved", and what lands is exactly the approved list.
- Limit: Each entry is checked against the rules for work items, and a break lands only with a recorded override.
- Fails if: The tracker and the plan file disagree after the landing, or something lands that the person did not approve.
- Fails if: A story for a feature with a ready ICE is not drafted from it, or a feature is guessed from words that fit none or more than one.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the plan file, the work items in the tracker, the rules for each kind and its parent, the person's words, and for a model feature, its two ICE.
- Never read: the folder that holds the evals.
- Persona: the product owner, who manages an intent's work items in a session.
- Scope: In: adding, moving, renaming, rewriting and changing the kind of work items. Out: status and direction, plan branches, and a feature not yet in the model.

## Expectation
- Scenario: A session with a rename, a new chore and a story for a model feature, approved once, ends with the tracker and the plan file in agreement.
- Done means: The agreement check reads ok: the plan file matches the tracker and the approved list, and nothing else changed.
