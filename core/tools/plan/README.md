# Plan tool

Prints the plans from the plan files alone (`.garura/project/plans/<id>.yaml`): no tracker read,
no model call, and the same files print the same way every time (#719).

    python3 plan.py list  --template <plan-view.md> [--plans-dir D]
    python3 plan.py show  --template <plan-view.md> [--plans-dir D] --plan <id>
    python3 plan.py graph --template <plan-view.md> [--plans-dir D] [--repo R]

- `list` — one card for each plan: its direction (⏵, ⏵⏵, ⏵⏵⏵), number and title; its Status,
  Branch and Waits on; then each of its epics with its Progress. Status and Direction are read
  from the plan file as a person set them. Used by `/list-plans`.
- `show` — one plan as a tree, with the plans it needs after it. Done and Dropped are hidden and
  counted. Used by `/show-plan`.
- `graph` — each plan's branch against main, with commits ahead and behind. Used by
  `/list-plans --graph`.

Every mark and line comes from the `plan-view.md` template (its ```yaml plan-view block). A play
gets the template from `template-manager` and passes the copy's path with `--template`.

The six statuses of a plan's node are Not Started, In Progress, Now, Done, Blocked and Dropped.
A plan file with any other status is refused (exit 2), so an old file is never shown wrongly.

## The plan file

A plan file holds, at the top: `id` (the business intent's issue number), `title`, `status`
(Not Started, In Progress, Paused, Done or Dropped — set by a person), `direction` (1, 2, 3 or
none — set by a person), `branch` (`plan/<id>/base` while its work is in progress), `started`,
`updated`, `epic`, `identified_by`, `needs_plans` and `tree`. It keeps no history: each
`/update-plan` landing is one commit whose message names what was asked, the overrides and what
is owed.

Each node of the tree has `issue`, `kind`, `title` and `status`, and may have `represents` (the
slice or feature it stands for) and `children`. A plan may hold six kinds of item, each under one
kind of parent (#917):

| Kind | Sits under |
|------|------------|
| `epic` | the plan itself (the top of the tree) |
| `feature` | an epic |
| `story` | an epic or a feature |
| `spike`, `chore`, `bug` | a story |

Older plan files also use the kind `issue`, and have some items under another parent (a bug under
a feature). The tools still print them; `/update-plan` names such an item when an instruction
touches it and offers the right kind or parent, and never changes it unasked.

## Getting onto a plan's branch

    python3 plan_branch.py go   --plan <id> [--plans-dir D] [--ignore <folder>] --out <record.json>
    python3 plan_branch.py back  --record <record.json> [--ignore <folder>]
    python3 plan_branch.py abort --record <record.json> [--ignore <folder>]

The one way a play gets onto a plan's branch: it stays there, stops on uncommitted work (naming
the files), switches, or — for a plan with no branch — sets main's plan file to In Progress with
the branch named, commits that on main, and cuts the branch from it. `back` returns to the branch
the session started on. `abort` undoes a branch the session cut (deletes it, and reverts main's
plan file commit) when nothing else has landed on it, then goes back. Used by `/update-plan` (#730), and by `start-change` once #989 is built.

An install lays the tool in the project's `.garura/core/tools/plan/`, without its tests. Later
users: `/update-plan` (#730), `/shape-plan`'s stop when a plan exists (#896), `start-change`.

Tests: `python3 -m unittest test_plan test_plan_branch` from this folder.
