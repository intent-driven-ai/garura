# #806 See every plan as a graph: which plan is on which branch, compared to main

> **Design agreed, 2026-10-29 (the product owner).** The design is `.garura/project/issues/719/specs/design.md`; this section holds the part for this issue. Built in one change with #729 and #628, opened on #719. Its feature page is added to the product model in that change, through `/discover-capabilities`.

Functionality: a person sees every plan as a graph, like a git branch graph: each plan's branch, where it was cut from (main or another plan's branch), which plans it returns to or needs, how far each is ahead of and behind main, and which issues have landed on it. So drift between plans and main is visible at a glance.

## Done when
- From the plan files and git alone (no tracker needed for the shape), it draws every active plan as a node on its branch, with the link it was cut from, its `identified_by` / `returns_to` / `needs_plans` links, and its commits ahead of and behind main.
- Each plan node shows its open and landed issues (status + ID + title).
- A plan whose branch is behind its base, or whose base has moved on, is marked.
- It writes nothing.

## Not in this issue
- Changing plans or branches (#720, #730). The plain-words tree of one plan (#628).

## Links
- Serves: #717
- Part of: #719
- Asked for by the product owner while starting plan 788, 2026-10-22: "we may need to build a plan view graph… as to which is on the code branch when in comparison to main. like we see git commits and different branches"



## Design (agreed 2026-10-29)

- `/list-plans --graph` draws each plan against main, like a git branch graph: its branch, commits ahead of and behind main, and a mark when it has fallen behind. A plan with no branch shows as on main.
- Only what the plan files and git hold is drawn: "where it was cut from" and `returns_to` are not in the plan files (#791 was dropped), so they are left out.
- The layout is in the `plan-view.md` template; the plan tool prints it with no model call.

