# Capability: Every name moved to the standard, one family at a time

## Directional intent
rename every play, skill and loop to the standard, in batches, each batch done when its checks pass.

## Agent intent (ICE)
- Goal: Garura's own parts all follow the standard.
- Limit: No change to what any part does; names and references only.
- Fails if: a rename changes behaviour, or a batch lands with its checks failing.
- Checked by: after the last batch, the linter and the old-name check pass across all components.
