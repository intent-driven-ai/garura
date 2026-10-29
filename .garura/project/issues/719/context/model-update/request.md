# Model updates for #719 (view plans) — what the product owner asked for, 2026-10-29

Capability: cap-719 (View plans), page capabilities/cap-719/capability.md, business intent bi-717.
The agreed design: .garura/project/issues/719/specs/design.md.

1. fn-806 — NEW, THIN. The feature "See every plan as a graph against main" (#806, text in issue-806.md).
   - Page: features/fn-806/feature.md (the holding folder, like fn-729 and fn-628).
   - A thin page with a thin ICE (Goal, Limit, Fails if, Context, Checked by) from the design and #806.
   - Spine: new entry under cap-719, intents [bi-717], issue 806, slug fn-806,
     one_line "See every plan as a graph against main: each plan's branch, and its commits ahead and behind".
2. fn-628 — UPDATE, THIN. "Show one plan as a tree, from its plan file alone" (#628, text in issue-628.md).
   - Its page is out of date: title "goal, done, now, next, wait", legend done / now / next,
     and "Fails if ... a done line does not say decided, built or shipped". All three are replaced
     by the design: six statuses (Not Started, In Progress, Now, Done, Blocked, Dropped), Done and
     Dropped hidden and counted, the plans it needs printed after it, marks and layout from the
     plan-view template. Keep every other line the page has.
   - Spine: one_line "Show one plan as a tree, from its plan file alone"; mark thin.
3. fn-729 — CHECK ONLY. "List every plan, from the plan files alone" (#729, text in issue-729.md).
   Say whether its page still matches the design; change nothing unless the product owner says so.
