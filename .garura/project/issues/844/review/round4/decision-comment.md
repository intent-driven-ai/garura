Reviewer verdict (human): reject

Round 4 of the review. P1 0, P2 0, P3 1, P4 1. The computed recommendation was approve; the product owner rejected so that both open items are fixed.

Fixed since round 3: N3 (fn-728 gives a tracker issue to the epic, the stories and the work under them; a capability and a feature get none).

To fix:
- N4 (P4): fn-728's "Fails if" names only the epic and the stories. Add a spike, chore or bug under a story.
- M1 (P3): ontology v10 and ADR 049 (Decisions 1.2 and 4) say the plan play writes the slice's hidden file, one entry per story. Decisions 6 and 7 of #844 say /shape-slice writes it, one entry per feature, and a thin ICE is proposed for a new capability or feature. The ontology change runs through /edit-ontology as its own change on plan/788/base; the ADR is amended; then this PR takes the base and is reviewed again.

Standards check: 0 findings. Slice check: 0 problems. Model check: the same 70 older errors (decision 8).
