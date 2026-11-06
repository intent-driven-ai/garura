Reviewer verdict (human): approve

The reviewer approved this change as it is. The play's recommendation was approve (no P1 findings). The findings below are open and were not fixed in this PR.

**Checks**
- Component linter (installed tool, source layout): no finding in a changed file; 37 were there before.
- Test suites, all green: test_write_approved 16, test_link_part 36, and the six suites that share the write helper (19, 50, 63, 119, 26, 34). Acceptance check: 24 of 24.
- Design check of the skill and agent docs, grounded on main (harness standard principles 2, 3 and 11; the ontology's ICE kind; ADR 047): conforms, with the notes below.

**Open findings**
- P2 Q1: a failed write leaves nested new folders behind (`write_approved.py`).
- P2 Q2: a failed undo still reports every page as put back (`write_approved.py`).
- P2 Q3: the report is written after the pages with no guard (`write_approved.py`).
- P2 Q4: a wrongly typed `for` or `doc` crashes instead of refusing (`link_part.py`).
- P2 Q5: adding an ICE drops malformed entries in the `ices` list (`link_part.py`).
- P2 Q6: the folder-undo test cannot fail (`test_write_approved.py`).
- P3 Q7: a path starting "./" skips the intent-page refusal.
- P3 Q8: the intent-page test never reaches that rule.
- P3 Q9: five ICE refusals in `link_part.py` have no test.
- P3 H-1: the docs cite "ontology v15"; the ICE node rule is v6 (#758).
- P3 H-2: "a part's page holds no ICE section" needs to be scoped to approved mode.
- P4 Q10, Q11, Q12, H-3, H-4: line length, two copies of the same checks, test layout, one undocumented refusal, one keeper row that names a step of another file.

Each finding's basis and evidence are in `.garura/project/issues/1031/review/findings.yaml`.
