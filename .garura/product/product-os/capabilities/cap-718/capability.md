# Capability: Build a plan

## Directional intent
from a business intent, build the whole plan — Business Intent → Capability → Feature → Spike/Chore/Bug — as a plan file in the repo, with a tracker issue for every node.

Added by /shape-slice for bi-788 (ontology v9 and v10, ADR 049): a business intent has one plan, and never a second; the plan's ID is the intent's issue number. The plan holds every slice that serves its intent, found from the link "slice serves business intent", and it takes the slice that was shaped; it does not pick or test slices. For each slice it makes one epic, or uses the one that exists, and one story for each feature of the slice. A story's scope of work holds the goal, the limits and the expectations from its feature's ICE and that feature's capability's ICE, and its Context guidance is its own property. A story never holds a failure condition. The plan play does not write the slice's hidden file; /shape-slice writes it (decision 6 of #844, which changes ADR 049 Decisions 1.2 and 4). Note: under ontology v7 a capability and a feature are never tracker issues, so the first paragraph's "a tracker issue for every node" is out of date; it is kept until a person agrees the change.

> To be deepened later: written by /shape-slice for bi-788 at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.

## Sources
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md, Decisions 1.2, 2 and 4.
- docs/adr/048-the-product-model-and-the-work-are-two-layers.md, Decision 1.
- GitHub #818 (open).

> Thin ICE: proposed by /shape-slice for bi-788 (#844, decision 7); deepen with /discover-capabilities.
> In the section below, the first four lines were there before and are kept as they are; the lines from the second Goal on were added by /shape-slice for bi-788.

## Agent intent (ICE)
- Goal: Given a business intent, a plan file exists with every capability and feature named, each with its ICE and its tracker issue.
- Limit: It never waits for a full product model; missing model pages are written as light pages on the fly.
- Fails if: a node in the plan has no tracker issue, or building stops because a domain or model page is missing.
- Checked by: building the plans for #717 and its partner gives the same trees that were filed by hand on 2026-10-21.
- Goal: A business intent has exactly one plan, and the plan holds one epic for each slice that serves the intent and one story for each feature of that slice.
- Limit: The plan does not pick, rank or test slices; the person chose the slice at /shape-slice.
- Limit: The plan play writes only the plan file, the epic and the stories; the slice's hidden file and its failure and recovery conditions are /shape-slice's (decision 6).
- Fails if: a story holds a failure condition, or a second plan is made for one business intent.
- Fails if: the plan play writes a failure condition, a recovery condition or the eval into the plan's evals folder.
- Context: serves the product owner, who runs and tracks the plan; reads the slice and the two ICE of each story once; writes .garura/project/plans/<intent>.yaml and the tracker's epic and stories; out are picking slices, the hidden file and the eval.
- Checked by: /shape-plan run after /shape-slice on a real business intent writes the plan file, one epic and one story for each feature of the slice.
