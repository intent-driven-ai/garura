# Need — #758 (plan #756)

The agent intent (ICE) becomes its own kind of node in the product model, not a section inside a capability or functionality page.

Decided by the product owner, 2026-10-22:
- One ICE for each pair of business intent and capability or functionality. A second business intent on the same capability gets its own ICE.
- The ICE has its own page and its own spine entry.
- Three parts: Intent (goals, limits, fails if); Context (the rules handed to the sub-agent that gathers context: what to read, what never to read, the persona, the scope); Expectation (scenarios, done means, quality needs).
- Two links: "built from" (one business intent) and "is for" (one capability or functionality).
- A business intent connects to the ICE nodes built from it, not to capabilities.

Sources: issue #756 and #758; the ontology (core/components/memory/standards/schemas/product-os/ontology.md, version 5); the spine schema (core/components/memory/standards/schemas/product-os/spine.yaml); the page templates (core/components/memory/standards/schemas/product-os/grounding/capability.md, functionality.md); the glossary (core/grounding/glossary.md, "ICE (ProductOS)").

## Touches
ICE
Business Intent
Capability
Functionality
Work
