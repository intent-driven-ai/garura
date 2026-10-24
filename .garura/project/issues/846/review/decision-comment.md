Reviewer verdict (human): reject

Round 2 of the review. P1 0, P2 0. The 4 P3 and 8 P4 standards findings are path reminders on the ADR files. All round-1 findings DF-1 to DF-8 are fixed. The computed recommendation was approve; the product owner rejected so that the small round-2 items are fixed too:

- R2-1 (P4): the /shape-slice play and its write guard follow v10 until /edit-play runs. Add the plans/<id>/evals write scope and the write guard to #842.
- R2-2 (P4): ADR 052's last "Work This Creates" bullet says the pointers come after acceptance; they are done. Drop it.
- R2-3 (P4): the pointers on ADR 047 and ADR 049 name only some sections; old lines remain in their bodies (ADR 047 "reports richness", ADR 049's ICE impact and "does not change" list). Name those parts in the pointers; the bodies stay as written.
- R2-4 (P4): the ontology says the #760 ready check is "not built yet"; it is built and reads the thin mark.
- R2-5 (P4): check_ice_workable.py treats the text "false" in `thin` as thin; read only the value true.
