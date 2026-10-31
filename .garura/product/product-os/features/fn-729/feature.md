# Feature: List every plan, from the plan files alone

## What it does
Print one list of every plan from the plan files: one line for each plan, with the plan's number and title, its branch, its Done count against its open count, what is Now or In Progress, and the plans it waits on (needs_plans). The marks and the layout come from the plan-view template.

Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Agent intent (ICE)
- Goal: Anyone sees every plan at once.
- Limit: Reads the plan files only.
- Limit: no model call makes the list; the marks and the layout come from the plan-view template.
- Fails if: a plan in the plans folder is missing from the list.
- Context: serves anyone who works on plans, a person or an agent (bi-717); touches the plan files (.garura/project/plans/) only; the six statuses are Not Started, In Progress, Now, Done, Blocked and Dropped; out of scope: the graph of each plan against main (`/list-plans --graph`, fn-806), and one plan as a tree (fn-628).
- Checked by: a test folder with three plans lists all three.
