Harness verdict (gate off per gates.plays.check-change): approve

No finding blocks the merge (no P1). Six categories reviewed: the plays (harness), the scripts (code), the tests, the #673 product-model page, the run records and the plan file.

What ran: the three test suites pass (18, 12, 10); the play linter passes on start-change and merge-change with the Next-line check; the component linter has 36 errors, all there before and none in a changed file; the script copies match; ruff's 12 E702 warnings in two test files were all there before.

The plan lookup never reads the checkout (checked by hand with a broken checkout copy). Gaps found in this change, to fix before the merge:
- Q18 (P3): a plan branch pushed and then deleted on GitHub from another clone, never merged, passes the safe-delete check and is deleted; its commits end up nowhere. The rule narrows to the one #953 asked for: delete only when every commit is on main.
- HS1 (P2): no test makes a push fail.
- HS2 (P3): the start-change check for the stale delete and for a failed fetch cannot fail; the record needs the facts it reads.
- HS3 (P3): the plan recovery now ends in a person's decision in three of its four cases, but is still marked autonomous.
- Q17/HS4: a plans folder given as an absolute path, or a run from a sub-folder, reads as "no plans".
- Q19/HS7 (P2): the network git calls have no time limit and can prompt for a login.
- Q20/HS6 (P4): the branch delete's result is not checked. Q08 (P3): the branch-setup function grew past 100 lines.
- HS8 (P4): merge_pr.py's description still says the records land "on main itself".
- DM-1 (P3): the model index entry for #673 still has the page's old one-line name.

Recorded for the product owner, outside this change's design: DM-2 (the #721 capability page still states the old landing rule). The P2 rows on the scripts are checklist rows with no defect.
