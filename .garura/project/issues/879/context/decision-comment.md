Reviewer verdict (the product owner, round 1): reject

The rule stays: an epic holds only the work of its own slice (its stories, and the chores and other work that serve that slice). Work found along the way goes under its own epic; a plan may hold several epics when they serve the same business intent. Work that blocks the plan gets its own epic, is delivered, and merges back where it spawned.

This PR taught `/shape-plan` to accept other children under an epic (finding H-1), which is the opposite of that rule. #879 is reworked: the play keeps the rule, its brief names an epic's misplaced work by title as work that belongs under its own epic, and the check fails with that message; plan 788's extra items under #794 move to their own epic(s) after the product owner's yes; and the blocker rule is written into the work guide.

Other findings of this round (H-2, H-3, H-4, CODE-1, CODE-10) are folded into the rework or dropped with it.
