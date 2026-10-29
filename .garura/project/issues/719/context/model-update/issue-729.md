# #729 List every plan, from the plan files alone

> **Design agreed, 2026-10-29 (the product owner).** The design is `.garura/project/issues/719/specs/design.md`; this section holds the part for this issue. Built in one change with #628 and #806, opened on #719.

Functionality: one list of every plan — its ID, its business intent, what is now, and who it waits on.

## Agent intent (ICE)
- Goal: Anyone sees every active plan at once.
- Limit: Reads the plan files only.
- Fails if: a plan in the plans folder is missing from the list.
- Checked by: a test folder with three plans lists all three.

## Links
- Serves: #717
- Identified by: found on its own

Design: `.garura/project/issues/621/specs/plan-design.md` and `change-list.md` (agreed with Kapil, 2026-10-21).


## Design (agreed 2026-10-29)

- `/list-plans` prints one line per plan, from the plan files alone: its number, title, branch, `Done` count against the open count, what is `Now` or `In Progress`, and the plans it waits on (`needs_plans`).
- The layout is in the `plan-view.md` template; the plan tool prints it with no model call.
- Statuses in every plan: `Not Started`, `In Progress` (started, no one on it in an open change), `Now` (worked in an open change), `Done`, `Blocked`, `Dropped` (closed as not planned; hidden in every view). `next` and `later` go and become `Not Started`.


