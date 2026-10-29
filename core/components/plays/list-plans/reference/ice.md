# list-plans — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
edit-play; never hand-edit the compiled SKILL.md.

## Intent

Anyone, a person or an agent, sees every plan of the project at once, from the plan files
alone: one card for each plan, with the plan's direction, its number and business intent, its
Status, its Branch and the plans it Waits on (always shown, blank when none), then each of its
epics with its Progress (done, open, dropped). The plan's Status and Direction are what a person
set in the plan file, never worked out from the work under it (#983). With `--graph`, the same
plans are drawn against main:
each plan's branch with its commits ahead of and behind main, and the plans with no branch
named as on main.

A plan is the work toward one business intent, kept in its plan file. The plan files are a
cache: they exist so that no one has to read every issue to know where the work stands. This
play reads them and nothing else, and prints them the same way every time.

### Constraints

- C1 — The play reads only the plan files and, for the graph, git's branches. It never reads
  the tracker or the product model, and the view is made with no model call.
- C2 — Read only: the play writes no plan file, no issue and no branch. Its working files are
  deleted at the end.
- C3 — Every plan file in the plans folder is in the output once, in the order of the plan
  numbers.
- C4 — Every mark and every line of the view comes from the plan-view template. The play
  never makes up a layout of its own.
- C5 — The same plan files and the same branches print the same output.
- C6 — A plan file that cannot be read, or that has a status, a plan status or a direction
  the template does not know, stops the play with the file named. A part of the list is never
  shown.
- C7 — When the plans folder holds no plan, the play says so plainly.
- C8 — There are two modes: the list (the default) and `--graph`. Any other mode stops the
  play; it is never guessed.
- C9 — The play ends by proving its Done means at close, never by its step list running out.
- C10 — Each card shows the plan's Status and Direction exactly as the plan file holds them,
  set by a person. The play never works either out from the work under the plan.

### Failure conditions

- F1 — A plan in the plans folder is missing from the output, or is in it twice.
- F2 — The play writes a plan file, an issue or a branch.
- F3 — The view comes from the tracker, from a model call, or from a layout that is not the
  template's.
- F4 — Two runs on the same plan files print differently.
- F5 — A plan with an unknown status is shown instead of stopping the play.
- F6 — A number of commits ahead or behind in the graph does not come from git.
- F7 — The close reports COMPLETED without the Done means held.
- F8 — A card shows a Status or a Direction that is not the one in the plan file.

## Context

- The plan files: `.garura/project/plans/<id>.yaml`, one for each business intent; the ID is
  the business intent's issue number. Six statuses: Not Started, In Progress, Now, Done,
  Blocked, Dropped (#719 design, `.garura/project/issues/719/specs/design.md`).
- The plan tool (`.garura/core/tools/plan/plan.py`) prints each view from the plan files and
  the template. It is deterministic and makes no model call.
- The template (`standards/templates/plan-view.md`) holds the marks and the layout. The play
  reads no memory: `template-manager` puts a copy in the run's working folder (ADR 039).
- Stories: #729 (list every plan, from the plan files alone), #806 (see every plan as a graph
  against main), #983 (the list as one card per plan). Feature #719. Business intent #717.

## Expectation

### Success scenarios

- **S1 — developer, every plan at once.** Given a plans folder with three plans, when
  `/list-plans` runs, then each of the three has one card, in the order of the plan numbers,
  with its Status, Branch and Waits on, and each epic with its Progress. *Measure:* the check
  record reads `all_listed: true` and `in_order: true`.
- **S2 — lead, plans against main.** Given a plan whose branch is ahead of or behind main, when
  `/list-plans --graph` runs, then its line shows the commits ahead and behind that git counts,
  and every other plan is named on main. *Measure:* the check record reads
  `graph_numbers_match: true` and `all_listed: true`.
- **S3 — newcomer, no plans yet.** Given an empty plans folder, when `/list-plans` runs, then
  it says plainly that there are no plans. *Measure:* the view holds the template's no-plans
  line and the check record reads `all_listed: true`.
- **S4 — operator, an old plan file.** Given a plan file with a status the template does not
  know, when `/list-plans` runs, then the play stops, names the file, and shows no list.
  *Measure:* the tool's exit record reads 2 and its error names the file; no view is presented.
- **S5 — auditor, nothing changed and nothing drifted.** Given any plans folder, when
  `/list-plans` runs, then two prints of the same files are the same and the plan files are
  unchanged. *Measure:* the check record reads `same_twice: true`, `unchanged: true` and
  `template_used: true`.

- **S6 — product owner, the direction as set.** Given plans whose files hold a status and a
  direction a person set, when `/list-plans` runs, then each card shows that direction's icon
  on its own line under the plan's heading (no icon line when none is set) and that status on
  its Status row. *Measure:* the check record
  reads `as_set: true`.

### Recovery

| For | Trigger | Direction | Handoff |
|-----|---------|-----------|---------|
| F1 | the check finds a plan missing or listed twice | re-run the plan tool over the plans folder and check again; if it still fails, report the plan and close HALTED | autonomous |
| F2 | a plan file's hash changed during the run, or a write to the tracker or a branch was made | stop, report what changed, and leave it for a person; read only is never repaired by a retry | human |
| F3 | a line of the view does not match the template's layout | load the template again through template-manager and re-run the plan tool with it | autonomous |
| F4 | the two prints differ | re-run both prints; if they still differ, report the difference and close HALTED | autonomous |
| F5 | the plan tool exits 2 on a status it does not know | stop, name the plan file and its status, and show no list; a person fixes the plan file | human |
| F6 | a graph number does not equal git's count | re-run the graph and check again; if it still differs, close HALTED with both numbers | autonomous |
| F7 | the close would report COMPLETED without the Done means held | surface the unmet clauses and re-run the step that makes the missing record, or close HALTED | autonomous |
| F8 | a card's Status or Direction differs from the plan file | re-run the plan tool with the template and check again; never correct the card by hand — the plan file is the only source | autonomous |

### Done means

- D1 — the view exists. *Check:* `artifact_exists` `view.txt`.
- D2 — every plan is listed once, in order. *Check:* `field_equals` `check.json` `all_listed` = true.
- D3 — the same files printed the same way twice. *Check:* `field_equals` `check.json` `same_twice` = true.
- D4 — no plan file changed. *Check:* `field_equals` `check.json` `unchanged` = true.
