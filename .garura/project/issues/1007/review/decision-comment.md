Harness verdict (gate off per gates.plays.check-change): approve

Review of #1007 (an item's status in the plan file follows its own GitHub issue, no roll-ups; ADR 064). Nothing blocks the merge.

Checks run
- Play linter on merge-change and update-plan: pass, 0 gaps. Component linter: nothing in a changed file (36 problems there before).
- ruff clean on the changed code. Plan tool, merge-change and update-plan tests all pass (48 update-plan tests).
- ADR 064 lint valid; ontology v15 check valid, change limited to the Plan kind's status rule.

Fixed in this round (all in #1007's scope)
- H1 (P3): an issue closed as a duplicate (or with no reason) is now Dropped (or Done) and is never closed again on GitHub.
- H2 (P3): merge-change commits the plan file with its records only when the item actually changed.
- H3, H6 (P3/P4): merge-change's ICE names the plan file in the records commit and the plan item in REC9.
- H4 (P3): the new /update-plan scenario's check proves the landing (plan-write and agreement ok, the item Done).
- H5 (P4): a failed plan step leaves the item open and is named in the report, never silent.
- H7 (P4): /update-plan's Forbidden list and F7 row name the "closed on GitHub" exception.

Left (small, recorded): two wording notes on the new ontology line (ONT-1 timing, ONT-2 readability). The standards scan's P2/P3 rows are path-level checklist rows with no defect on a changed line.

Outside this change's scope (recorded): older ontology lines still name plays; the GitHub capability roll-up in merge-change. Owed after merge, on the product owner's word: a reinstall, and copying ontology v15 to Phoenix memory.
