# Decision brief

## Decision
An item's status in a plan file follows its own GitHub issue. Closed as completed means Done;
closed as not planned means Dropped. There are still no roll-ups: nothing is worked out from the
items under an item, and a parent never changes because its children closed (an epic stays open
when all its stories close, until its own issue closes).

Two plays carry it:
- merge-change: when it closes an issue that landed on its plan's branch, it sets that item Done
  in the plan file, in the same records commit, with the plan tool's plan_status.py.
- /update-plan: when a session starts, each item whose issue is closed on GitHub but still open
  in the plan file goes on the list as "closed on GitHub"; it lands only with the person's
  "approved".

This changes the rule "A person sets the plan's Status and its Direction, and the status of each
item in its tree ... A play changes a status or the direction only when a person asked for it"
(the ontology's Plan kind) and /update-plan's C8, for an item's own issue only. The plan's own
Status and Direction stay the person's.

## Why now
#1005 was merged and its issue closed, but plan 717's file still read Not Started: merge-change
closes the issue and does not touch the plan file, and the rule said only a person may change a
status. The plan file and GitHub disagreed. The product owner: "Each one of these IDs is making
GitHub. If GitHub is updated to be done, then this status here has to be updated. When I said
status cannot be updated, I mean don't do rollups." (#1007)

## Options considered
- Keep "a person sets every status": the person runs /update-plan after each merge. Lost: the
  plan file and GitHub disagree after every merge until a person notices; it already happened
  with #1005.
- Work a parent's status out from its children (roll-ups). Lost: the product owner rules out
  roll-ups; a parent's own issue decides it.
- An item follows its own issue (chosen): merge-change sets it at the merge, and /update-plan
  catches issues closed by hand, shown and approved.

## Decided by
The product owner, 2026-10-31 (#1007 design, "yes"; the story filed on "approved").

## Decided in
#1007, on plan 717's branch.

## Shape
markdown
