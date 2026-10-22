# Functionality: A capability or functionality is ready without a domain

## What it does
the new ready rule. A capability is ready when it serves a confirmed business intent and nothing it needs is open; a functionality when its capability is ready and nothing it needs is open. A missing domain is a warning, never a block.

## Agent intent (ICE)
- Goal: A plan can build from capabilities and functionalities that have no domain yet.
- Limit: No change to how pages are saved.
- Fails if: the ready check says "no domain yet" for a node that serves a confirmed business intent.
- Checked by: the ready check's tests: no domain + confirmed intent = ready; no confirmed intent = not ready; an open need = not ready.
