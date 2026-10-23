# Capability: Build a plan

## Directional intent
from a business intent, build the whole plan — Business Intent → Capability → Feature → Spike/Chore/Bug — as a plan file in the repo, with a tracker issue for every node.

## Agent intent (ICE)
- Goal: Given a business intent, a plan file exists with every capability and feature named, each with its ICE and its tracker issue.
- Limit: It never waits for a full product model; missing model pages are written as light pages on the fly.
- Fails if: a node in the plan has no tracker issue, or building stops because a domain or model page is missing.
- Checked by: building the plans for #717 and its partner gives the same trees that were filed by hand on 2026-10-21.
