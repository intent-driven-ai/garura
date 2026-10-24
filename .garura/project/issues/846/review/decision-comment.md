Reviewer verdict (human): reject

Round 1 of the review. P1 0, P2 2, P3 3, P4 3. The computed recommendation was approve; the product owner rejected so that every finding is fixed.

The ontology itself is valid and consistent. The texts and the tool around it still follow v10:
- DF-1 (P2): v11 adds "thin ICE" as a partly-ready gap; ADR 047 says partly ready covers only gaps outside the ICE. Needs an ADR amendment.
- DF-2 (P2): ADR 049 still says the plan play writes the hidden file, one entry per story, and cites the renamed rule section.
- DF-3 (P3): the ready-check tool (and its copies and test) still counts lines ("light | full"); v11 says it reads only the thin mark.
- DF-4 (P3): spine.yaml's ices schema and the ICE page shape do not allow `thin: true` or the Thin line.
- DF-5 (P3): slice.yaml, spine.yaml and the /shape-slice play still say /shape-slice "writes nothing else".
- DF-6 (P4): the feature-to-story map sits in three places (agreed in K3).
- DF-7 (P4): Q38 uses the stricter L1 words; say so.
- DF-8 (P4): the flow line misses "except the Fails if lines"; one example gained a sentence.

Plan: DF-3, DF-4, DF-5 (schemas), DF-7, DF-8 in this PR; DF-1 and DF-2 by one /record-decision amending ADR 049 and ADR 047; the /shape-slice play text through /edit-play.
