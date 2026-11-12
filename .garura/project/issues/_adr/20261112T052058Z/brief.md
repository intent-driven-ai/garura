## Decision

A play finds the Story of a Feature by the plan file's `represents` mark. When the plan file marks no story for the feature (for example, when there is no plan file), the play finds it by the `issue` that the feature's entry in the product model names: the Story filed for that feature. That issue must be of type Story. When it is open, the play uses it, makes it a sub-issue of the slice's epic, and shows that move (with the parent it leaves) before the person's yes. When it is closed, the feature is already built: the play makes no story for it and leaves the closed one as it is. A feature whose ICE is not ready never takes the model's story. An issue the model names that the tracker does not have, that is not of type Story, that is named for two features, or whose feature sits in two slices of one plan stops the run before any tracker write. A play never finds a story by its title. This amends ADR 056 §2.

## Why now

All plan files were deleted on 2026-11-02 (#1021), so the `represents` mark finds nothing. ADR 065 requires /shape-plan to be fixed before the first plan rebuild, so that a rebuilt plan files no second set of stories, but it left ADR 056 as it is. PR #1047 (#1025) adds the model route; its review found that the code now conflicts with ADR 056 §2 and that nothing committed defines a feature's `issue`. The plan rebuild for business intent 1 waits on this.

## Options considered

- **The model's `issue` as the second way (chosen).** The model already holds a feature's issue number for the features that have a story, and the model is the agents' record of the product.
- **Rebuild the plan files by hand first, so the marks exist again.** Lost: the plan files were deleted on purpose, and rebuilding them is the work /shape-plan itself does; a hand-made plan file would carry no checks.
- **Match a story by its title.** Lost: ADR 056 rules it out because titles change; a renamed story would be filed again.
- **Leave /shape-plan as it is and close the duplicate stories afterwards.** Lost: it files the second set of stories that ADR 065 forbids, and every person who saw the duplicates would have to sort them out.

## Decided by

The product owner, 2026-11-12, in the review of PR #1047.

## Decided in

Issue #1048 (a Chore under #1025, "/shape-plan reuses an open story for a feature instead of filing a second one").

## Shape

markdown
