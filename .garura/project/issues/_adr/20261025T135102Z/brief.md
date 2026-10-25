# Decision brief — the product's security box moves from none to medium

## Decision

The product profile's security level goes from **none** to **medium**, because the new capability cap-initialize ("Initialize a project for Garura") needs it. The capability's security need is: nothing is written to the tracker, and no tracker mapping is written, before the product owner's typed yes; and initialize writes no Phoenix memory and no other project's memory.

## Why now

/discover-capabilities detailed cap-initialize for #882 and rolled its needs into the box. The box was `set` with security `none`. Initialize writes to the project's tracker (it makes the missing issue types, #881) and builds the project's memory, so its security need (medium) is above the box. A capability above the box moves the box, and the move is recorded as its own decision.

## Options considered

- **Keep security at none.** Lost: it would block cap-initialize's security need. Initialize writes to the tracker, and a write that runs without the typed yes is the failure the medium bar guards against.
- **Move security to high.** Lost: no source asks for more than the typed-yes guard and the memory scope. Medium meets the need.

## Decided by

The product owner, at the /discover-capabilities checkpoint for #882: typed "yes" (2026-10-25) in round 1, and "yes" again in round 2 after the review fixes.

## Decided in

#882 (PR #886).

## Shape

yaml — a product decision on the node cap-initialize. Target: `.garura/product/product-os/decisions/dec-cap-initialize-security-none-medium.yaml` (the play's save script wrote a thin proposed record there; this record replaces it with the same id).
