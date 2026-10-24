# Capability: Write the hidden eval

## Directional intent
Write the eval that checks, from the outside, that a business intent is met on its slice's surface. The eval is written before the build, from what the plan wrote: the epic, its stories and the slice's hidden file. It never reads an ICE page itself, so the ICE has only one reader. The eval is kept in the plan's evals folder, and no builder, no skill that builds the software and no context sub-agent reads that folder. It matters because a builder that sees the test can build to the test, and then a pass proves nothing.

> To be deepened later: written by /shape-slice for bi-788 at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.

## Sources
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md, Decisions 1.3, 3 and 4.
- docs/philosophy/garura-reference-implementation.md, The Builder/Validator Barrier.
- Gojko Adzic, Specification by Example (Manning, 2011).
- GitHub #798 (open).

> Thin ICE: proposed by /shape-slice for bi-788 (#844, decision 7); deepen with /discover-capabilities.

## Agent intent (ICE)
- Goal: Each slice has one eval that says, from the outside, if its business intent is met on the slice's surface.
- Limit: Read the epic, its stories and the hidden file; never an ICE page, the usage guide or the code.
- Limit: Write only in the plan's evals folder: .garura/project/plans/<plan-id>/evals/<slug>/.
- Fails if: a builder can read the eval.
- Fails if: the eval checks something the business intent does not ask for.
- Fails if: the eval play reads an ICE page, the usage guide or the code.
- Context: serves the product owner, who wants proof that the intent is met, and the running eval after the build; reads what /shape-plan and /shape-slice wrote; until #828 only a read rule keeps the folder from builders; out are running the eval and encrypting it.
- Checked by: /shape-eval run after /shape-plan writes the eval in the plan's evals folder, and no build play's inputs name that folder.
