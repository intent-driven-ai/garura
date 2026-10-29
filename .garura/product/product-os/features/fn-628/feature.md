# Feature: Show one plan as a tree, from its plan file alone

## What it does
Print one plan as a tree from its plan file: one node per line, each line a status mark, the issue ID and the title; the legend first, with the marks of Not Started, In Progress, Now and Blocked; Done and Dropped nodes hidden and counted on the last line; each plan it needs (needs_plans) printed after it. The marks and the layout come from the plan-view template.

Thin: proposed by the #719 change (view plans) from the person's words; deepen with `/discover-capabilities`.

## Agent intent (ICE)
- Goal: a reader coming back after two days knows where a plan stands from the tree alone.
- Limit: read only; prints from the plan file, no tracker reads.
- Limit: no model call makes the tree; the marks and the layout come from the plan-view template.
- Fails if: a line is only an issue number, or a Done or Dropped node with no open work under it is shown, or the last line does not count the Done and Dropped nodes it hides.
- Context: serves anyone who comes back to a plan, a person or an agent (bi-717); touches the plan files (.garura/project/plans/) only; the six statuses are Not Started, In Progress, Now, Done, Blocked and Dropped; out of scope: changing the plan format, and listing every plan (fn-729).
- Checked by: the tree for plan #717 matches its plan file.
