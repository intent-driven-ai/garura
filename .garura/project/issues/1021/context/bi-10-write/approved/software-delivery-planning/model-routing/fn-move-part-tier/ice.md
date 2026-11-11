## Intent
- Goal: When the record of its runs shows a part is slow or costly for a simple job, or falls short on a hard one, a person moves the part down or up a tier, and an eval checks that the part still does its job on the new tier before the move lands; the move is recorded with the runs it rests on and the eval's result, and the next install lays the new tier.
- Limit: No move lands without an eval that passed on the new tier.
- Limit: A person makes each move, on the record of the part's runs; nothing moves a tier on its own.
- Limit: The record itself, laying the tier in each coding tool and the evals a play holds stay with their owners.
- Fails if: A part's tier changed with no eval run on the new tier, or with an eval that failed.
- Fails if: A move names no runs it rests on, or no person who made it.
- Fails if: A part runs on a tier that a failed move left in place.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the record of the part's runs; the part's tier in its source and in the project's settings; the evals that can check the part, the play's own step and scenario evals and the rebuild eval; and Phoenix memory's page on choosing a model for each step and on re-running evals on a model change.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner or the technical lead, who reads what each part costs and decides to move it.
- Scope: In: moving a part up or down a tier on the record of its runs, checking the move with an eval, and recording the move. Out: the record of the runs, laying the tier in each coding tool, the evals a play holds, and landing the change.

## Expectation
- Scenario: In a bank's payments service, the record shows a skill that only formats a report runs on `opus`. The technical lead moves it to `haiku`; the skill's eval passes on `haiku`, the move lands with its record, and the next install lays `haiku`. In a news site's publishing tool, a move of the headline skill down to `haiku` fails its eval on two headlines, and the skill keeps `sonnet`.
- Done means: Someone other than the one who made the moves reads the two moves' records, the evals' results and the laid parts, and finds the bank's skill on `haiku` with a passed eval and the runs it rests on named, and the news site's skill still on `sonnet` with the failed eval on record.
