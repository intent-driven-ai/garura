# Feature: Create or link a tracker issue for every node in a plan

## What it does
every business intent, capability, feature, spike, chore and bug in the plan gets an issue — or is linked to one that exists — in the same parent order, in whichever tracker the project uses.

## Agent intent (ICE)
- Goal: Every node in the plan file names its issue, and the tracker shows the same parent order.
- Limit: Uses the platform adapter; no tracker is assumed.
- Fails if: a node has no issue, or an issue sits under the wrong parent.
- Checked by: a script compares the plan file with the tracker and finds no difference.
