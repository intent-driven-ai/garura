# Feature: Build the plan tree from a business intent

## What it does
read a business intent and whatever product model exists, and write the plan file in `.garura/project/plans/`. Missing model nodes are written on the fly as light pages.

## Agent intent (ICE)
- Goal: The plan file holds the business intent and every capability and feature it needs, each with its ICE.
- Limit: Writes only the plan file and light model pages.
- Fails if: it stops because a domain or a model page does not exist yet.
- Checked by: a plan built with no product model at all still lists its capabilities and features.
