## What this changes

Two rows in Garura's memory indexes described their files as they were before #920. Agents find memory pages by reading these indexes, so an agent working from the index alone missed two facts:

- **The rename map** (`core/components/memory/standards/rules/_index.md`): a name can now map to `null` — removed, with no successor (ADR 059). The old-name check still reports such a name, and the install has nothing to lay for it.
- **The decision record** (`core/components/memory/standards/schemas/product-os/_index.md`): since #930 it has `for_the_accepter`, the points for the person who accepts it.

Also: plan 606 brought up to date after #920 landed (PR #932) — the epic's Bugs and Story done, Chore #929 blocked on the Phoenix memory promotion.

The product owner rated wrong memory P2. Sending these pages to Phoenix memory is Chore #929.

Closes #937

## Self-review

