# Kinds — #1007 (an item's status in a plan follows its own issue)

You decide whether the Plan kind's rule on who sets a status changes to the new words below. If
you say yes, the next step checks the Plan kind's links and rules against this one line. If you
give other words, this step is done again with them.

## Reuse

The Plan kind stays. No kind, property or link is added, and no other kind changes. Its Tree
property already holds "each item with its tracker issue, its kind and its state", so an item's
issue is already there to follow. One clash: the rule now says a person sets the status of each
item, and ADR 064 says an item follows its own issue.

## Terms

item, its own issue, closed as completed, closed as not planned, Done, Dropped, open, a person
sets, roll-up, parent, children, the plan's Status, Direction.

## Kinds

Plan — changed: one rule line only. Nothing else in the Plan kind changes.

Old line:

> A person sets the plan's Status and its Direction, and the status of each item in its tree. Nothing works them out from the work: there are no roll-ups. A plan is not Done because its items are done, and an epic can be closed with open stories. A play changes a status or the direction only when a person asked for it. The one exception is the branch step above: cutting the plan's branch sets main's plan file to In Progress, because the person started work on the plan.

New line:

> A person sets the plan's Status and its Direction. Each item in its tree follows its own issue: when the issue is closed as completed, the item is Done; when it is closed as not planned, the item is Dropped; while the issue is open, a person sets the item's status. Nothing works a status out from the items under it: there are no roll-ups. A parent does not change because its children closed: a plan is not Done because its items are done, and an epic stays open until its own issue closes, and can be closed with open stories. Apart from an item whose issue closed, a status or the direction changes only when a person asks for it. The one other exception is the branch step above: cutting the plan's branch sets main's plan file to In Progress, because the person started work on the plan.

Log line:

> - 2026-10-31 — v15 (#1007, ADR 064, plan #717, with the product owner): an item's status in a plan follows its own issue. Closed as completed is Done; closed as not planned is Dropped; while the issue is open, a person sets it. There are still no roll-ups: a parent does not change because its children closed, and the plan's Status and Direction stay the person's. Only the Plan kind's status rule changes; no question, kind, link or property changes.

## Question

1. **Question** — Does the Plan kind's status rule change to the new line above?
2. **Answer** — Proposed: yes. A person still sets the plan's Status and Direction. An item takes
   its status from its own issue once the issue closes, and a person sets it while the issue is
   open. Nothing is worked out from the items under it.
3. **Why it matters** — If the old line stays, the ontology says only a person sets an item's
   status. An agent that reads it then treats an item marked Done after its issue closed as a
   broken rule, and the plan file and the tracker disagree again.
4. **Example** — A clinic's plan: the "Book a visit" story's issue closes as completed, so the
   story shows Done; its epic stays open until its own issue closes. A shop's plan: the "Gift
   wrap" story's issue closes as not planned, so the story shows Dropped; the plan's Status stays
   In Progress until the shop owner changes it. A bank's plan: the "Freeze a card" story's issue
   is open, so the bank's product owner sets it to In Progress by hand.
