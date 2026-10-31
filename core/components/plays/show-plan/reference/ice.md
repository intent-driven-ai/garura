# show-plan — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
edit-play; never hand-edit the compiled SKILL.md.

## Intent

Anyone, a person or an agent, sees one plan as a tree, from its plan file alone, and knows
where it stands after two days away: the work that is not done is shown, the work that is
Done or Dropped is hidden and counted, and each plan it needs is printed after it.

A plan is the work toward one business intent, kept in its plan file. The tree shows what is
left and what is moving; finished work is a count, not a wall of lines.

### Constraints

- C1 — The play reads only the plan files. It never reads the tracker or the product model,
  and the tree is made with no model call.
- C2 — Read only: the play writes no plan file, no issue and no branch. Its working files are
  deleted at the end.
- C3 — The first line is the plan's business intent: its number and title, with no mark. Each
  line under it is a status mark, an issue number and a plain-words title. No line is a bare
  number. Each node shows the status its plan file gives it: no status is worked out from the
  nodes under it (no roll-ups).
- C4 — Not Started, In Progress, Now and Blocked are shown. Done and Dropped are hidden and
  counted on the last line of the plan. A hidden node with a shown node under it is still
  printed, so the shown node keeps its place. A shown node whose children are all Done or
  Dropped prints those children too, one level down, so a person sees what was finished under
  it and can decide on it; they are not counted as hidden.
- C5 — Each plan the plan needs is printed after it, on the same screen.
- C6 — Every mark and every line comes from the plan-view template. The play never makes up a
  layout of its own.
- C7 — The same plan file prints the same tree every time.
- C8 — When no plan has the number asked for, the play says so plainly. A plan file with a
  status the template does not know stops the play with the file named.
- C9 — The play ends by proving its Done means at close, never by its step list running out.

### Failure conditions

- F1 — A Done or Dropped node is shown when no shown node sits under it and its parent has
  an open child or is itself hidden; the children of a shown node that are all Done or Dropped
  are not printed, or are counted as hidden; or the count of hidden nodes is wrong or missing.
- F2 — A line has no title or no issue number.
- F3 — A plan the plan needs is left out.
- F4 — The play writes a plan file, an issue or a branch.
- F5 — The tree comes from the tracker, from a model call, or from a layout that is not the
  template's.
- F6 — Two runs on the same plan file print differently.
- F7 — A plan that does not exist, or a plan with an unknown status, gets a guessed tree
  instead of a plain message or a stop.
- F8 — The close reports COMPLETED without the Done means held.

## Context

- The plan files: `.garura/project/plans/<id>.yaml`, one for each business intent; the ID is
  the business intent's issue number; `needs_plans` names the plans it needs. Six statuses:
  Not Started, In Progress, Now, Done, Blocked, Dropped (#719 design,
  `.garura/project/issues/719/specs/design.md`).
- The plan tool (`.garura/core/tools/plan/plan.py show`) prints the tree from the plan files
  and the template. It is deterministic and makes no model call.
- The template (`standards/templates/plan-view.md`) holds the marks and the layout. The play
  reads no memory: `template-manager` puts a copy in the run's working folder (ADR 039).
- Story #628 (show one plan as a tree, from its plan file alone). Feature #719. Business
  intent #717. The tree format the product owner agreed on 2026-10-22, with the statuses of
  2026-10-29.

## Expectation

### Success scenarios

- **S1 — returning developer, where does it stand.** Given a plan with work Not Started, In
  Progress, Now, Done and Dropped, when `/show-plan <id>` runs, then the tree shows every node
  that is not Done or Dropped, each as mark, number and title, and its last line counts the
  hidden ones. *Measure:* the check record reads `lines_ok: true` and `hidden_ok: true`.
- **S2 — developer, a bug under finished work.** Given a Done story with a Not Started bug
  under it, when `/show-plan` runs, then the story is printed and the bug sits under it.
  *Measure:* the check record reads `lines_ok: true` (the story is in the expected set, and
  not counted as hidden).
- **S3 — lead, a plan that needs another.** Given a plan that needs another plan, when
  `/show-plan` runs, then the needed plan's tree is printed after it. *Measure:* the check
  record reads `needs_ok: true`.
- **S4 — anyone, a wrong number.** Given a number that no plan has, when `/show-plan` runs,
  then it says plainly that there is no such plan and shows no tree. *Measure:* the tool's exit
  record reads 1 and the check record reads `no_plan_plain: true`.
- **S5 — auditor, nothing changed and nothing drifted.** Given any plan, when `/show-plan`
  runs, then two prints are the same, the plan files are unchanged and every line follows the
  template. *Measure:* the check record reads `same_twice: true`, `unchanged: true` and
  `lines_ok: true`.
- **S6 — product owner, a feature whose stories are all finished.** Given an open feature
  whose stories are all Done or Dropped, when `/show-plan` runs, then the feature is printed
  with each of those stories under it, as mark, number and title, and they are not in the
  hidden count. *Measure:* the check record reads `lines_ok: true` and `hidden_ok: true` for a
  plan with such a feature.

### Recovery

| For | Trigger | Direction | Handoff |
|-----|---------|-----------|---------|
| F1 | the check finds a hidden node shown, the finished children of an open parent left out or counted, or a wrong or missing count line | re-run the plan tool and check again; if it still fails, report the node and close HALTED | autonomous |
| F2 | the check finds a line with no title or no number | re-run the plan tool and check again; if the plan file has a node with no title, name it for a person | human |
| F3 | a needed plan is missing from the view | re-run the plan tool and check again; if the needed plan's file is missing, the tree says so with the template's no-plan line | autonomous |
| F4 | a plan file's hash changed during the run, or a write to the tracker or a branch was made | stop, report what changed, and leave it for a person; read only is never repaired by a retry | human |
| F5 | a line of the view does not match the template's layout | load the template again through template-manager and re-run the plan tool with it | autonomous |
| F6 | the two prints differ | re-run both prints; if they still differ, report the difference and close HALTED | autonomous |
| F7 | a missing plan or an unknown status got a tree | show the template's no-plan line, or stop and name the file and its status; never a guessed tree | autonomous |
| F8 | the close would report COMPLETED without the Done means held | surface the unmet clauses and re-run the step that makes the missing record, or close HALTED | autonomous |

### Done means

- D1 — the view exists. *Check:* `artifact_exists` `view.txt`.
- D2 — the tree is what the plan file and the template say. *Check:* `field_equals` `check.json` `tree_ok` = true.
- D3 — the same file printed the same way twice. *Check:* `field_equals` `check.json` `same_twice` = true.
- D4 — no plan file changed. *Check:* `field_equals` `check.json` `unchanged` = true.
