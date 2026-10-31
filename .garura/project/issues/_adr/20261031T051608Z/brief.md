# Decision brief

## Decision
/shape-plan makes a business intent's one plan, once. When the intent already has a plan file
(in the checkout or on main), /shape-plan stops at pre-flight, before it opens a change or writes
anything, and points to /update-plan. A slice shaped later for an intent that already has a plan
joins that plan through /update-plan (its epic and its stories), not through /shape-plan.

This amends ADR 049: Decision 1.2 (the plan play makes the epic for the slice "or uses the one
that exists"), and the paragraph "When a new slice is shaped for an intent that has a plan, the
plan play adds the slice and its epic to that plan."

Known gap, named here: until #1002 is fixed (an /update-plan session cannot reach the product
model, so it cannot draft a story from a feature's ICE), /update-plan cannot draft a later
slice's stories from its features' ICE. Until then the person words those stories in the
/update-plan session.

## Why now
#896: running /shape-plan on an intent that already had a plan went into update logic (find the
epics and stories that exist, add sections, move features out). A plan is changed in one place
now: /update-plan (#720, ADR 062) is the working session that changes a plan that exists. Two
plays that both change an existing plan drift apart. The review of the #896 change (PR #1003,
finding HF-1) found ADR 049 still promises the old path.

## Options considered
- Keep ADR 049 as it is: /shape-plan also updates an existing plan with a new slice. Lost: two
  plays change an existing plan, and #896 found the update path unreliable; the product owner
  chose one play for it.
- /shape-plan stops on an existing plan and points to /update-plan (chosen).
- /shape-plan stops only when every slice is already planned, and plans a new slice otherwise.
  Lost: it keeps the update path in /shape-plan (finding epics that exist, adding to the plan
  file), which is the part #896 removes.

## Decided by
The product owner, 2026-10-30 (the #896 design, "approve") and 2026-10-31 ("yes go ahead", to
amend ADR 049).

## Decided in
#896, PR #1003, on plan 717's branch.

## Shape
markdown

## Change from the product owner (2026-10-31, at the accept checkpoint)
Keep it simple. The decision is only this:
- /shape-plan makes the intent's one plan, once, and stops at pre-flight when the plan already
  exists, pointing to /update-plan.
- A plan that exists is changed only by /update-plan. In its session the person may add a bug,
  a story or a feature to the plan. On "approved" it reaches GitHub, and a new feature is linked
  to the product model with a thin ICE, through the skills that exist (ADR 062). A plan play does
  not change existing parts of the product model.
- When an /update-plan change adds a feature to a slice, that slice's eval is out of date.
  Updating the eval is a person's later step (perhaps a later "update eval" play), outside this
  decision. A new bug or a new story does not change the slice, unless the story changes the
  feature itself.
Drop from the draft: the "until #1002 the person words a later slice's stories" point; the
/update-plan gaps about marking an epic for its slice and the feature-to-story map; the ADR 052
§7 point; and the long list of other files owed. Work This Creates keeps only: the ontology's
Plan kind and Q30 through /edit-ontology (in this same change), and the forward pointer on
ADR 049 and the index after acceptance.
