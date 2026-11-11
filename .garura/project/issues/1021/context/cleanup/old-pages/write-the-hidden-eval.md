# Capability: Write the hidden eval

## Directional intent
Write the eval that checks, from the outside, that a business intent is met on its slice's surface. The eval is written before the build, from what the plan wrote: the epic, its stories and the slice's hidden file. It never reads an ICE page itself: each line of an ICE has one reader, /shape-slice for the "Fails if" lines and the plan play for the rest (ontology v11, ADR 052). The eval is kept in plain text in the plan's evals folder, and no builder, no skill that builds the software and no context sub-agent is given that folder: the build is given the business intent, never the eval, and a check flags each build session that read the folder and records the flag in that build run's evidence (fn-898). It matters because a builder that sees the test can build to the test, and then a pass proves nothing.

Features: fn-798 (/shape-eval writes the hidden eval) and fn-898 (the build is given the business intent, never the eval; a check flags each build session that read the evals folder, in that build run's evidence).

> To be deepened later: written by /shape-slice for bi-788 at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.

## Sources
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md, Decisions 1.3, 3 and 4.
- docs/philosophy/garura-reference-implementation.md, The Builder/Validator Barrier.
- Specification by Example: How Successful Teams Deliver the Right Software (Manning, 2011, https://oreilly.com/library/view/specification-by-example/9781617290084).
- GitHub #798 (open).
- GitHub #898 (open): the build is given the business intent, never the eval, and a check flags each build session that read the evals folder.
- ADR 057 (docs/adr/057-a-slices-eval-is-plain-text-gherkin-that-runs-with-no-agent.md), its Context and section 7: the product owner dropped encryption and #828 on 2026-10-26. The eval stays in the repo in plain text. The build is given the business intent through the stories, never the eval.

Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Agent intent (ICE)
- Goal: Each slice has one eval that says, from the outside, if its business intent is met on the slice's surface.
- Limit: Read the epic, its stories and the hidden file; never an ICE page, the usage guide or the code.
- Limit: Write only in the plan's evals folder: .garura/project/plans/<plan-id>/evals/<slug>/.
- Fails if: a builder is given the eval, or a build session read the evals folder and that build run's evidence has no flag that names the read.
- Fails if: the eval checks something the business intent does not ask for.
- Fails if: the eval play reads an ICE page, the usage guide or the code.
- Context: serves the product owner, who wants proof that the intent is met, and the running eval after the build; reads what /shape-plan and /shape-slice wrote; the build is given the intent, never the eval, and fn-898's check flags a build session that read the folder, in that build run's evidence; out are running the eval, blocking a read by hook (#893) and the drift checks and evidence warnings in Griffin; encryption (#828) was dropped by the product owner on 2026-10-26.
- Checked by: /shape-eval run after /shape-plan writes the eval in the plan's evals folder, and no build play's inputs name that folder.
