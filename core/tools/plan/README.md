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

An install lays the tool in the project's `.garura/core/tools/plan/`, without its tests. Later
users: `/update-plan` (#730), `/shape-plan`'s stop when a plan exists (#896), `start-change`.

Tests: `python3 -m unittest test_plan` from this folder.
