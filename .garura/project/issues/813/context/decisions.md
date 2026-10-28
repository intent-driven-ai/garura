# Decisions — #813 + #809 (product owner, 2026-10-23, reply: "yes")

Q1 #809 — delete the old parts (git keeps history). A short ADR records why and points ADR 017 (scope/ layout) and ADR 035 (§10 "retired agents are left as they are") forward.
Q2 #809 scope — the items #809 names, plus the same chain that reads intent epics: the derive-* skills (except derive-blast-radius, which the live test-engineer agent uses and which does not read intent epics), the rules epics.md, scenarios.md, design.md, architecture.md, and the agents product-keeper, market-analyst, epic-expectation-crafter. Other deprecated skills not in this chain: their own issue.
Q3 — rules/product.md: Rule 12 becomes its own rule file; the rest is deleted. research/arch.md and research/standards/play-orchestration.md move into memory standards. user-provided/project-brief.md stays.
Q4 #813 — every script that loads the model gets the guard: one shared file (main copy in create-play/references/, kept the same by the shared-scripts drift check), one call where each script loads the model; writers first.
