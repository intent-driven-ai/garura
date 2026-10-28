# Decisions — /shape-slice 788 (#844), with the product owner, 2026-10-24

1. **No loop.** The slice is run as three plays, one after the other: /shape-slice → /shape-plan → /shape-eval. The loop and its one approval (#796) are left out. /shape-slice's confirmation shows the slice only.
2. **Names.** The plan play is /shape-plan (#818). The eval play is /shape-eval (#798).
3. **Left out:** eval encryption (#828), the author-slice skill (#838).
4. **The view.** The slice is shown as: what you run, who tests it, features grouped under capability with each capability linked to its domain, and what is left out. One confirmation, yes or change — not a list of questions first.
5. **The model.** Reuse what exists, fill what exists in part, add what is missing (domains and capabilities), with research.
6. **The hidden file moves to /shape-slice.** /shape-plan only plans (plan file, epic, stories). /shape-slice writes the slice's hidden failure-and-recovery file. (Changes ontology v10 and ADR 049, which say the plan play writes it.)
7. **Option C — thin ICE.** For a new capability or feature, /shape-slice proposes a thin ICE itself (at least a goal, limits and one "fails if" line), and writes the hidden file from it. It warns that thin ICE leads to problems later and advises /discover-capabilities; it never forces the person to go back. (The ontology already allows work from an ICE that is "partly ready".)
8. **The model check's older problems (2026-10-24).** The whole-model check reports 70 problems; all 70 were there before this run (compared one by one: lint-before-run.json vs slice-check.json), in 17 older feature pages and 2 ICE lines of other plans. None is in a page this run wrote. The product owner chose to go on ("1"). The play fix: the model check fails only on the parts the run wrote, and shows older problems as warnings.
