# Feature: See every plan as a graph against main

## What it does
Draw every plan against main, like a git branch graph, from the plan files and git alone: each plan's branch, its commits ahead of main and behind main, and a mark when the plan has fallen behind main. A plan with no branch shows as on main. It runs as `/list-plans --graph`; the marks and the layout come from the plan-view template, and the plan tool prints the graph with no model call. It writes nothing.

Thin: proposed by `/shape-slice` from the person's answers; deepen with `/discover-capabilities`.

## Agent intent (ICE)
- Goal: a person sees at a glance which plan is on which branch, and how far each plan is from main.
- Limit: reads only the plan files and git; never the tracker; writes no plan file, issue or branch.
- Limit: no model call draws the graph; the marks and the layout come from the plan-view template.
- Fails if: a plan on a branch is drawn without its commits ahead of and behind main.
- Fails if: a plan that has fallen behind main carries no mark, or a plan with no branch is not shown as on main.
- Context: serves anyone who works on plans, a person or an agent (bi-717); touches the plan files (.garura/project/plans/) and the git branches; out of scope: where a branch was cut from and where it returns to (the plan files do not hold them), and changing plans or branches (#720, #730).
- Checked by: a test repository with one plan on a branch two commits ahead of main and one behind, and one plan with no branch, draws the first with 2 ahead, 1 behind and the behind mark, and the second as on main.
