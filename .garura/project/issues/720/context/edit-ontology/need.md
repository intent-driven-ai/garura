# Need — the Plan kind catches up with how plans are kept and managed (#720)

Issue: #720 (manage a plan with /update-plan), plan 717.

In the product owner's words (2026-10-30): plan, direction and the like go into the ontology, but they are
operational: they must never find their way into the product model.

What changes:
1. A plan's Status is Not Started, In Progress, Paused, Done or Dropped, set by a person (today: "active, done or dropped").
2. A plan has a Direction: 1, 2, 3 or none, set by a person.
3. A plan's tree may hold six item kinds — epic, feature, story, spike, chore, bug — each under its parent kind:
   an epic at the top; a feature under an epic; a story under an epic or a feature; a spike, a chore or a bug under a story.
4. A plan has a branch, plan/<id>/base, while its work is in progress.
5. The plan file keeps no history: each /update-plan landing is one commit whose message names what was asked,
   the overrides and what is owed.
6. Managing a plan is /update-plan: it changes the plan file, the tracker and the product model together, on one approval.
7. The Thin line of a thin ICE reads "Thin: proposed from the person's words; deepen with `/discover-capabilities`." —
   no longer naming /shape-slice, because /update-plan proposes thin parts too.

These live in the Plan kind and the plan files only — never in the product model's index or pages.

Sources: .garura/project/issues/720/specs/design.md, .garura/project/issues/720/specs/build-design.md,
core/tools/plan/README.md, core/components/plays/update-plan/reference/ice.md.

## Touches
Plan
ICE
