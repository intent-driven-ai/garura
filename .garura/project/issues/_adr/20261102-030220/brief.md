## Decision

Four rules for how this project is built. This record is only about how the project is built. It says nothing about which business intents exist or what the product model holds; those are requirements, and the product owner changes them directly.

1. The product model's index (the spine) is changed through two skills: `link-model-part` adds or changes a part, and `remove-model-part` takes a part out, with the name of the person who approved it. Each changes only what its request names, stays inside the model, and lists every file it changed. Plays move onto these two skills over time, in place of writing the index with their own scripts. Today's rule, that only a play's own script writes the index, no longer holds.
2. A person can approve deleting a plan. A plan is not only changed through /update-plan; a whole plan, with its folder, may be deleted on a person's named approval, through `remove-plan`.
3. The product model never names a plan. Plans sit outside the model and come and go, so no model page may depend on one.
4. Business intents and agent work each live in a tracker named in the project's settings. Tools read the settings and know how to reach the tracker. Plays, skills and sub-agents know only the tool, never the tracker.

The five loops do not change, and neither does the ontology. The verb `remove` is not decided here: the verbs are being changed next, and the skills keep their names until then.

## Why now

The product owner decided on 2026-11-02 to keep business intents in a tracker of their own, so they have their own short numbers, and to delete the hand-kept plans and rebuild them through the shaping plays. Doing that needed skills that write the model's index outside a play, which the current rule does not allow. The product owner also wants a team to be able to choose GitHub, GitLab, Jira or Linear as a setting, with nothing hard-coded.

## Options considered

- Keep the rule that only a play's script writes the index, and invoke a play for every change. Lost: a play is too heavy for a single index change, and the product owner wants the index changed through skills.
- Many skills or plays that each write the index their own way. Lost: redundant, and that is how it is today. Two skills is the fewest that fits, because taking a part out needs an approver's name and adding one does not.
- Keep the old plans and move their items between plans. Lost: hand-kept trees are harder to keep true than plans rebuilt by the plays.
- Keep intents in the work repo and reserve numbers for them. Lost: GitHub has one running number per repo, shared with pull requests, and cannot reserve any.
- Our own short ID on top of the issue number. Lost: the product owner chose a separate tracker, which gives real numbers and keeps intents and work clearly apart.
- Name the tracker in plays, skills and sub-agents. Lost: every new tracker would mean changing them all.

## Decided by

The product owner, 2026-11-02.

## Decided in

#1021, with the skills landed in #1019.

## Shape

markdown
