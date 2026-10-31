Harness verdict (gate off per gates.plays.check-change): approve

Review of #1005 (/show-plan shows the finished children of an open parent). Nothing blocks the merge.

Checks run
- Play linter on show-plan: pass, 0 gaps; Next-line check pass.
- Component linter (source layout): 37 problems, none in a changed file (there before).
- ruff on the changed files: clean. Plan tool tests 20 OK; show-plan check tests 2 OK; the check agrees with the tool on plans 717, 788 and 722.

Fixed in this round
- H1 / M1 (P3): the rule tested whether any node below a child was open, not the children's own status, so a finished story with an open bug under it kept its finished siblings hidden. The rule now checks the children's own status, as the design and the ICE say; a new test covers that case.

Left (small, recorded, not fixed)
- H2 (P4): the check's own tests cover the all-finished case, not the two limits; the plan tool's tests cover them.
- M2 (P4): the template's hiding line above the new rule has no pointer to it.
- The standards scan's P2/P3 rows on plan.py and test_plan.py are path-level checklist rows; none points to a defect on a changed line.

Outside this change's scope (recorded): the template's example does not show the new rule; the play's scripts row does not list test_check_tree.py.
