# Capability: Link the product model

## Directional intent
the product model's kinds and links — capabilities and functionalities link to business intents, to what they need, and to what identified them; domains link loosely to business intents and capabilities.

## Agent intent (ICE)
- Goal: The model can be built in any order and still links up.
- Limit: How pages are saved stays the same.
- Fails if: a node waits on a domain before work can start, or a link points at nothing.
- Checked by: the ontology check and the spine linter pass on Garura's own model built for #717 and #722.
