> **Design agreed with the product owner, 2026-10-29 ("lock this in").** Serves business intent #717. Part of #719 (view plans), in plan 717. Follows #983.

**Story:** in `/list-plans`, each card's heading puts the plan's number and title at the left edge, with the direction icon on its own line underneath; the rows start at the left edge too.

## The layout

```
⏵ next · ⏵⏵ next in line · ⏵⏵⏵ later

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#717  People plan work toward a business intent, and pick it up across days and people
⏵

Status         Paused
Branch         main
Waits on       #722 A product model can be managed, and grows as plans are built

Epic           ○ #956  A person builds, views and manages the plan of a business intent
Progress       10 done · 10 open · 2 dropped

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#722  A product model can be managed, and grows as plans are built

Status         Paused
...
```

## Rules

- The heading is the plan's number and title, at the left edge — no icon or padding before it.
- The direction icon (⏵, ⏵⏵ or ⏵⏵⏵) is on its own line under the heading. A plan with no direction has no icon line.
- A blank line, then the rows: Status, Branch, Waits on, and each epic with its Progress — all at the left edge.
- Everything else from #983 stays: the legend, the rules between plans and between epics, Waits on always shown, Status and Direction as set by a person.

## What it touches

The plan-view template, the plan tool (the heading and the icon line), `/list-plans`' check (it finds each plan by its heading) and their tests.

## Not in scope

The tree (`/show-plan`) and the graph (`--graph`).

