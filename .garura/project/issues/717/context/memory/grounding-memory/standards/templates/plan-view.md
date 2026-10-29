# Plan View Template

The shape of the three views of the plans: the list of every plan, one plan as a tree, and every
plan as a graph against main. The plan tool (`.garura/core/tools/plan/plan.py`) prints each view
from the settings below, from the plan files alone (`.garura/project/plans/<id>.yaml`): no
tracker read and no model call, so the same files print the same way every time.

Consumers: `/list-plans` (the cards and `--graph`), `/show-plan` (the tree). Each play gets a copy
of this file from `template-manager` and passes its path to the plan tool.

## The statuses

Every node of a plan has one of six statuses. The order below is the order of the legend.

| Status | Meaning |
|---|---|
| Not Started | Not started. |
| In Progress | Started, but no one works on it in an open change right now. |
| Now | Someone works on it in an open change right now. |
| Blocked | Cannot go on until something else is settled. |
| Done | Finished. |
| Dropped | Closed as not planned, or as a duplicate. Kept for the history. |

## The tree (`/show-plan <id>`)

- The legend comes first: the mark and name of every status. A hidden status still has its
  mark in the legend, because a hidden node is printed when a shown node sits under it.
- Then the plan: its business intent on the first line, with no mark, and every node under it,
  one node per line, indented under its parent with tree lines. A line is only its mark, its
  issue number and its title.
- No status is worked out from the nodes under it. Each node shows the status its plan file
  gives it: an epic may be Done with stories open, and a story found to have a defect later
  stays Done, with the defect linked under it.
- The tree shows Not Started, In Progress, Now and Blocked. It hides Done and Dropped. A hidden
  node that has a shown node under it is still printed, so the shown node keeps its place.
- The last line counts the nodes that were not printed, for each hidden status.
- A plan that this plan needs (`needs_plans`) prints after it, on the same screen, with a note.

```
○ Not Started · ◐ In Progress · ▶ Now · ⛔ Blocked · ✓ Done · ✗ Dropped

#717  People plan work toward a business intent, and pick it up across days and people
└─ ○ #956  A person builds, views and manages the plan of a business intent
   ├─ ○ #718  Build a plan
   │  └─ ○ #896  /shape-plan stops when the business intent already has a plan, and does not run again
   ...
5 Done · 1 Dropped (not shown)
```

## The list (`/list-plans`)

One card for each plan, in the order of the plan numbers. A legend of the direction icons comes
first. Each card opens with a heavy rule, then the plan's heading — its direction icon (or
blanks), its number and its business intent's title — then labeled rows:

- **Status** — the plan's own status, as the plan file gives it (`status`): Not Started, In
  Progress, Paused, Done or Dropped. Set by a person, never worked out from the work.
- **Branch** — the plan's branch, or `main` when it has none.
- **Waits on** — always shown: each plan it needs, with its title; blank when none.

Then, after a blank line, each of the plan's epics — only the epics; an item outside every epic
is not shown — with its status mark, number and title, and a **Progress** row: done, open, and
dropped when there are any. A dotted rule separates the epics of one plan.

**Direction** is set by a person in the plan file (`direction`: 1, 2, 3 or none) and shown as
⏵, ⏵⏵ or ⏵⏵⏵ before the plan's number. It is directional, not a ranking: several plans may
share a level.

```
⏵ next · ⏵⏵ next in line · ⏵⏵⏵ later

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏵    #717  People plan work toward a business intent, and pick it up across days and people
  Status         Paused
  Branch         main
  Waits on       #722 A product model can be managed, and grows as plans are built

  Epic           ○ #956  A person builds, views and manages the plan of a business intent
  Progress       9 done · 10 open · 2 dropped
```

## The graph (`/list-plans --graph`)

Main first, then each plan that has a branch, as a branch off main, with its commits ahead of and
behind main. A plan behind main has the behind mark. Last, one line names the plans with no
branch: they are on main.

```
main
├─ plan/717/base  2 ahead · 0 behind  #717 People plan work toward a business intent, and pick it up across days and people
└─ plan/788/base  4 ahead · 3 behind ⚠  #788 Agents design the work, then build it through plays and a loop
on main: #606, #722, #734, #756, #767
```

## Settings

The plan tool reads this block. A change to a mark or a line is made here, never in the tool.

```yaml plan-view
statuses:
  - {name: Not Started, mark: "○", shown: true}
  - {name: In Progress, mark: "◐", shown: true}
  - {name: Now, mark: "▶", shown: true}
  - {name: Blocked, mark: "⛔", shown: true}
  - {name: Done, mark: "✓", shown: false}
  - {name: Dropped, mark: "✗", shown: false}
tree:
  legend_join: " · "
  root: "#{issue}  {title}"
  line: "{mark} #{issue}  {title}"
  hidden: "{counts} (not shown)"
  hidden_join: " · "
  needs: "Plan {plan} needs plan {needed}:"
  no_plan: "No plan {plan} in {dir}."
list:
  plan_statuses: [Not Started, In Progress, Paused, Done, Dropped]
  directions: {1: "⏵", 2: "⏵⏵", 3: "⏵⏵⏵"}
  direction_names: {1: next, 2: next in line, 3: later}
  legend_join: " · "
  direction_width: 5
  plan_rule: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  epic_rule: "  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄"
  head: "{direction}#{plan}  {title}"
  row: "  {label}{value}"
  label_width: 15
  labels: {status: Status, branch: Branch, waits: Waits on, epic: Epic, progress: Progress}
  waits_item: "#{plan} {title}"
  waits_join: "; "
  epic: "{mark} #{issue}  {title}"
  progress: "{done} done · {open} open"
  dropped: " · {dropped} dropped"
  none: "No plans in {dir}."
graph:
  main: "main"
  line: "{bar} {branch}  {ahead} ahead · {behind} behind{flag}  #{plan} {title}"
  behind_flag: " ⚠"
  on_main: "on main: {plans}"
```