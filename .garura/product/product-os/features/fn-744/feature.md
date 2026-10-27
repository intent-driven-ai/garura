# Feature: Rename the change, plan, knowledge and record plays

## What it does
review-change → check-change, refactor → refactor-code, build-knowledge → research-knowledge, review-knowledge → check-knowledge, adr → record-decision; the planned plan plays take draft-plan, show-plan, update-plan, list-plans.

## Agent intent (ICE)
- Goal: These families follow the standard.
- Limit: next and focus stay one word.
- Fails if: an old name is still referenced.
- Checked by: the old-name check finds none of these names.
