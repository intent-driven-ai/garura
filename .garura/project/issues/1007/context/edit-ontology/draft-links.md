# Links and rules — #1007 (an item's status in a plan follows its own issue)

You decide whether the Plan kind's links and rules stay as they are, with only the one status rule
changed to the line below. If you say yes, the next step writes the ontology and checks it. If you
give other words, this step is done again with them.

## Properties

No property or link changes. The Tree property already holds each item with its issue and its
state, so an item's issue is there to follow.

## Rule

The one rule, as agreed at the kinds step:

> A person sets the plan's Status and its Direction. Each item in its tree follows its own issue: when the issue is closed as completed, the item is Done; when it is closed as not planned, the item is Dropped; while the issue is open, a person sets the item's status. Nothing works a status out from the items under it: there are no roll-ups. A parent does not change because its children closed: a plan is not Done because its items are done, and an epic stays open until its own issue closes, and can be closed with open stories. Apart from an item whose issue closed, a status or the direction changes only when a person asks for it. The one other exception is the branch step above: cutting the plan's branch sets main's plan file to In Progress, because the person started work on the plan.

## Checked against the rest of the Plan kind

No other line in the Plan kind contradicts the new rule:

- What it is, the Status and Direction properties, and the States: these speak of the plan's own
  Status and Direction, which a person still sets and nothing works out.
- The rule that the plan file and the tracker always agree: the new rule helps it, because a closed
  issue and its item now say the same thing.
- The rule that each item's status is operational and lives only in the plan file: still true; the
  status follows the issue, but it is kept in the plan file.
- The examples: the shop's epic stays open with its stories done, which the new rule allows.

So there is no question at this step.
