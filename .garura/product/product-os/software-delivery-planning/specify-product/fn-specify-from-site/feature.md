# Feature: Specify from a deployed site

## What it does
Every view a deployed site offers is captured, up to two clicks deep.

Status: built.

## Agent intent (ICE)
- Goal: Every view a deployed site offers is captured, up to two clicks deep.
- Limit: It never changes data or follows a link out of the prototype.
- Fails if: A view it couldn't reach isn't recorded with why.
- Context: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the site.
- Checked by: Each view is saved, or named as unreached.
