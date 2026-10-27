The first run of `/shape-plan 788`. It ran in the middle of plan 788, a plan that already existed and was running. It used the work items the plan file marks, and made no new issue.

Closes #878.

## What the run wrote

After the product owner's yes, four issues changed in GitHub:
- #794, the slice's work order: type Feature, the line "Represents: sl-intent-to-design", and its feature-to-story map (fn-795 → #795, fn-818 → #818, fn-798 → #798).
- #795, #818 and #798, the three stories: type Story, and two new sections, "Scope of work" and "Context guidance". Every line already there stayed.

The plan file did not change: it already marked all four issues. No feature was skipped.

## What this change holds

- The run's records under `.garura/project/issues/878/`: the gather, the find, the drafts, the brief, the yes with the hashes of what was shown, the tracker record and the checks.
- The install record: the install laid `/shape-plan` and `author-work-items` (#876).

## Checks

| Check | Result |
|---|---|
| Draft check | ok, 0 problems |
| Plan check | ok |
| Write guard | ok: nothing in the product model or the plans folder changed |
| Every old line kept on the four issues | yes |
| Tracker check | unmet: #794 also holds 16 older children from the hand-made tree |

## The product owner's decision

The tracker check fails only because plan 788 was built by hand before the play existed, and a plan keeps evolving after it is built. The product owner accepted the run as closed and okay. Bug #879 changes the check so a work order can hold more than its slice's stories. See `.garura/project/issues/878/context/decisions.md`.

## Found by this run

- #879: the tracker check on a plan that was already running.
- Two story lines come from feature ICE pages that are out of date (#795's hidden-file line, #818's "not built yet"). The ICE pages must change first.
- The gather step writes full paths in its records; noted on chore #874. The paths in this change were made relative before the commit.
