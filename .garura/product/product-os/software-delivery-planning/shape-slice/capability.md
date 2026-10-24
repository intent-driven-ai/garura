# Capability: Shape a slice

## Directional intent
Shape the one slice that shows a business intent is served. A slice is an ordered group of features, from any capabilities, that a person can test end to end on one surface. This capability picks those features in build order, the one surface, and the person who tests it. It reads the product model and memory first, and asks the person only what neither answers. It writes the slice, its link "slice serves business intent", the slice record, the model parts the slice lacks (marked to be deepened later), and the slice's hidden file of failure and recovery conditions (decision 6 of #844). It never writes the plan, the epic, the stories or the eval: those are the work of other capabilities. It matters because every later step plans and checks this slice; a slice with no surface a person can test cannot be checked.

> To be deepened later: written by /shape-slice for bi-788 at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.

## Sources
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md, Decision 1.1.
- docs/adr/048-the-product-model-and-the-work-are-two-layers.md, Decision 2: the slice definition.
- User Story Mapping: Discover the Whole Story, Build the Right Product (O'Reilly, 2014, https://www.oreilly.com/library/view/user-story-mapping/9781491904893/): slicing out a minimum release.
- GitHub #795 (closed).

> Thin ICE: proposed by /shape-slice for bi-788 (#844, decision 7); deepen with /discover-capabilities.

## Agent intent (ICE)
- Goal: A business intent has one slice that one person can test end to end on one surface, with its features in build order.
- Goal: The slice's hidden file holds each feature's failure conditions and its capability's, with exactly one recovery for each.
- Limit: Write only the slice, its link "slice serves business intent", its record, the model parts the slice lacks (marked to be deepened), and the hidden file. Never a plan, an epic, a story or an eval.
- Limit: Ask the person only what the model and memory do not answer, within the question tier.
- Fails if: the slice has no surface that a person can test, has no tester, or has more than one surface.
- Fails if: the person is asked a question that the model or memory answers.
- Fails if: a "Fails if" line of a slice feature or of its capability is missing from the hidden file.
- Context: serves the product owner (names the intent, answers, approves) and the plays after it, /shape-plan and /shape-eval, which read the slice; reads the intent page, the spine, the ontology (Slice kind) and memory; writes the spine's slices list, product-os/slices/<id>.yaml and .garura/project/plans/<plan-id>/evals/<slug>/failure-and-recovery.md; out are the plan, the epic, the stories and the eval.
- Checked by: /shape-slice run on a real business intent writes one slice and its hidden file, and no plan, epic, story or eval.
