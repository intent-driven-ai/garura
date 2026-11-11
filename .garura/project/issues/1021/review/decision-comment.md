Reviewer verdict (human): approve

The reviewer approved this change as it is, and asked that the four P2 findings be recorded so they are addressed properly. The play's recommendation was approve: no finding is P1, and every finding cites a source committed before this branch. Totals: 4 P2, 17 P3, 11 P4.

**Checks**
- Six kinds of work: decision records (14 paths), memory rules (3), config maps (2), the product model (577), plan records (13 deletions), run records (2,275, which get no review because they are run evidence and no playbook covers them; that is not a pass).
- Component linter (installed tool, source layout): no finding in a changed file; 37 were there before. No play changed, so the play linter did not run. No code, config, tests or docs-prose category, so the standards scan was not dispatched.
- By hand: both new ADRs have their sections and are in the index; the two new memory rules are in the rules index; all 74 paths in the install record resolve.
- Design review, grounded on main (the ontology, the ICE schema, ADRs 035, 047, 048, 052, 060 and 063, the discover-intent play): memory, the product model and the plan records.

**The four P2s, to be recorded and addressed**
- DF-1: ten intent pages list 238 features under Touches; the ontology says a business intent does not name features (ontology.md:194, 243-246). The intent-page skill accepts features, so skill and ontology disagree on main.
- DG-MEM-02: the new ICE rubric says "exactly one goal, not negotiable"; the ontology and ice.yaml allow several goals that share the context (ontology.md:482, 493; ice.yaml:58-65).
- DG-MEM-01: the new intent-depth rule lets a part of the source become no intent; /discover-intent and check_intent.py refuse that (discover-intent ice.md:92-96, 179-181; check_intent.py:187-206).
- PLAN-1: deleting five paused plans leaves 90 open issues in no plan; ADR 060 says a paused plan's open issues stay in the plan (ADR 060:101-103).

**Other open findings** (P3 and P4, not fixed in this PR): L1-ADR-1, DG-MEM-03 to DG-MEM-10, PLAN-2 to PLAN-7, DF-2 to DF-14, as listed in `.garura/project/issues/1021/review/findings.yaml`.
