# Feature: Create or link the epic and the story issues of a plan

## What it does
the plan's epic (one for each slice), its stories (one for each feature of the slice), and each spike, chore and bug under a story get an issue — or are linked to one that exists — in the same parent order, in whichever tracker the project uses. The business intent's issue is there before the plan; its number is the plan's ID. A capability and a feature get no tracker issue.

> Changed with the product owner's yes on 2026-10-24 (#844): the old text gave a tracker issue to every node, a capability and a feature too. That rule is from before ontology v7. Under ontology v7 and later only the epic, the stories and the spikes, chores and bugs under them are tracker issues.

## Agent intent (ICE)
- Goal: The plan file names the issue of its epic, of each story, and of each spike, chore and bug, and the tracker shows the same parent order.
- Limit: Uses the platform adapter; no tracker is assumed.
- Fails if: the epic or a story has no issue, or an issue sits under the wrong parent.
- Checked by: a script compares the plan file with the tracker and finds no difference.
