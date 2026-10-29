> **Design agreed with the product owner, 2026-10-29.** Serves business intent #717 (people plan work toward a business intent). Part of #719 (view plans), in plan 717.

**Story:** `/list-plans` shows each plan as a card a person can read at a glance: the plan's direction, its business intent, its status, its branch, the plans it waits on, and each of its epics with how far along it is.

## The layout

```
⏵ next · ⏵⏵ next in line · ⏵⏵⏵ later

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏵    #717  People plan work toward a business intent, and pick it up across days and people
  Status         Paused
  Branch         main
  Waits on       #722 A product model can be managed, and grows as plans are built

  Epic           ○ #956  A person builds, views and manages the plan of a business intent
  Progress       9 done · 10 open · 2 dropped

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏵⏵   #788  Agents design the work, then build it through plays and a loop
  Status         Paused
  Branch         main
  Waits on

  Epic           ◐ #794  The shaping loop turns a business intent into a testable slice, its plan and its eval
  Progress       7 done · 10 open
```

## Rules

- **Direction** — set by a person in the plan file (1, 2, 3, or none), shown as ⏵, ⏵⏵ or ⏵⏵⏵ before the plan's number; blank when none. It is directional, not a ranking: several plans may share a level. Never worked out from the work.
- **Status** — the plan's own status, set by a person in the plan file: Not Started, In Progress, Paused, Done, Dropped. Never worked out from the work under it (no roll-ups).
- **Branch** — the plan's branch, or `main` when it has none.
- **Waits on** — always shown; each plan it needs, with its title (never a bare number); blank when none.
- **Epics** — only the plan's epics are shown, each with its status mark, number and title, and a **Progress** row: done · open · dropped (dropped only when there are any). Items that sit outside any epic are not shown.
- **Separators** — a heavy rule between plans; a dotted rule between the epics of one plan.
- **Order of the list** — the plans in the order of their numbers.
- The marks and the layout live in the plan-view template; the plan tool prints them with no model call.
- `/update-plan` (#730) is how a person changes a plan's Status and Direction; until it exists, they are set by hand in the plan file.

## Today's values

Every plan Paused. #717 ⏵, #788 ⏵⏵, the rest none.

## Not in scope

- The tree of one plan (`/show-plan`) and the graph (`/list-plans --graph`).
- Changing the plan files' tree.
