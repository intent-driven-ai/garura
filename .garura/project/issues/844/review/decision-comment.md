Reviewer verdict (human): reject

Round 5 of the review, after ontology v11 (#846, PR #849, ADR 052) landed on the base. M1 and N4 are closed. P1 0, P2 0, P3 1, P4 7. The standards check has 0 findings; the slice check has 0 problems.

To fix:
- R1 (P3): the hidden file's three entries say "Story: (filled in by /shape-plan)", and F12's way back keeps "the story numbers /shape-plan added". Under v11 the plan play writes nothing in the evals folder; the epic's feature-to-story map is the join.
- R2 (P4): fn-795's title says "/shape-slice writes the slice only".
- R3 (P4): two Thin lines in fn-795 say the hidden file and the thin ICE are "not set yet".
- R4 (P4): the hidden file names the old rule section; entries do not say which of the two ICE is thin.
- R5 (P4): shape-eval says "the ICE has only one reader"; under v11 each line has one reader.
- R6 (P4): fn-818 and fn-798 do not name the epic's feature-to-story map.
- R7 (P4): cap-718 and shape-slice should cite ADR 052.
- R8 (P4): the pages carry the Thin line; the six spine entries lack `thin: true`.
