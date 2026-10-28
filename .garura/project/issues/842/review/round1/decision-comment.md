Reviewer verdict (human): reject

Round 1 of the review. P1 0, P2 0, P3 3, P4 2. The computed recommendation was approve; the product owner rejected so that every finding is fixed and one rule is applied across the play:

"The agent's job is only to collect context. It is not supposed to do actual work. That is the skill's job."

To fix:
- DF-1 (P3): two step evals share the id SE-6.
- DF-2 (P3): hidden-lines.json and hidden-recoveries.json keep the "Fails if" text and ids in the issue folder, outside the evals folder.
- Q-1 (P3): render_brief.py writes the brief without the temp-file-and-replace step.
- Q-2 (P4): the safe-write helper is repeated in three scripts.
- DF-3 (P4) and the rule above: every step where product-os-keeper does work itself (choosing the slice, the early brief, and any other) moves into a skill; the author-slice skill (#838) is built in this change.
