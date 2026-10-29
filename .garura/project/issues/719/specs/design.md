# Design — #719 View plans (with #729, #628, #806)

Agreed with the product owner on 2026-10-29. This is the design the build works from. A change
to it is agreed with the product owner first, and this file is updated in the same step.

## What it is for

Anyone, a person or an agent, sees where every plan stands from the plan files alone
(`.garura/project/plans/<id>.yaml`): no tracker read, and no model call to make the view. The
same files print the same way every time.

## Statuses

Every node of every plan has one of six statuses:

| Status | Meaning |
|---|---|
| `Not Started` | Not started. |
| `In Progress` | Started, but no one works on it in an open change right now. Example: #723, 2 of its 5 stories done. |
| `Now` | Someone works on it in an open change right now. |
| `Done` | Finished. |
| `Blocked` | Cannot go on until something else is settled. |
| `Dropped` | Closed as not planned, or as a duplicate. Kept for the history; hidden in every view. |

`next` and `later` go. Every `next` and `later` node becomes `Not Started`. The two `now` nodes of
2026-10-29 (#723, #794) have no open change, so they become `In Progress`.

No roll-ups (the product owner, 2026-10-29). A node's status is its own; nothing is worked out
from the nodes under it. Done means it landed on main. An epic may be closed with stories still
open. A defect found later is linked under the story it came from, and the story stays Done.
The plan's first line, its business intent, has no mark.

## The parts

1. **The template** — `plan-view.md`, in the templates folder
   (`core/components/memory/standards/templates/`). It holds the status marks and the layout of
   the three views: the list, the tree and the graph. It reaches Phoenix memory by promotion.
   The plays get it from `template-manager`, as every play gets its close templates.
2. **The plan tool** — `core/tools/plan/`. Reads the plan files and prints each view from the
   template. Deterministic: no model call. Later users: `/update-plan` (#730), the stop in
   `/shape-plan` when a plan exists (#896), and `start-change`.
3. **`/list-plans`** (#729) — one line per plan: its number, title, branch, Done count against
   the open count, what is `Now` or `In Progress`, and the plans it waits on. `--graph` (#806) draws each
   plan against main, like a git branch graph: its branch, commits ahead of and behind main, and
   a mark when it has fallen behind. A plan with no branch shows as on main.
4. **`/show-plan <id>`** (#628) — one plan as a tree: one node per line, mark, issue number,
   title; legend first. It shows `Not Started`, `In Progress`, `Now` and `Blocked`. It hides `Done` and `Dropped`,
   and ends with one line that counts them. A plan it needs (`needs_plans`) prints after it.
5. **Statuses in the plan files** — all 7 plan files rewritten to the six statuses; `/shape-plan`
   writes `Not Started` where it wrote `next`.
6. **The #806 feature page** — added to the product model under cap-719 through
   `/discover-capabilities`.

Neither play has an agent: there is nothing to decide. Both are built through `/create-play`,
each from its story's ICE.

Example, `/show-plan 717`:

```
○ Not Started · ◐ In Progress · ▶ Now · ⛔ Blocked

#717  People plan work toward a business intent, and pick it up across days and people
└─ ○ #956  A person builds, views and manages the plan of a business intent
   ├─ ○ #718  Build a plan
   │  └─ ○ #896  /shape-plan stops when the business intent already has a plan
   ├─ ○ #719  View plans
   │  ├─ ○ #729  List every plan
   ...
5 Done · 1 Dropped (not shown)
```

## How it lands

One change, through start-change, commit-change, propose-change, check-change and
merge-change. `/start-change` opens it on #719; it cuts plan 717's branch from main and the
work branch from it. The one pull request lands on plan 717's branch and closes #729, #628,
#806 and #719.

## Replaced

- #628's first text: the GOAL / DONE / NOW / NEXT / WAIT grouping and "decided, built or
  shipped" on each done line. Replaced by the marked tree above (the template the product owner
  agreed on 2026-10-22, with the 2026-10-29 statuses). Rule 19 in
  `core/components/memory/standards/rules/work-plan.md` is updated in the same change to match.

## Not in this change

- The old `work-plan.md` template (the per-issue Markdown plan from before the plan files). It
  is out of date; it is left as it is.
- Changing plans or branches (#720, #730).
