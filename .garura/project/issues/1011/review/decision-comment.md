Harness verdict (gate off per gates.plays.check-change): approve

No finding blocks the merge. Three categories reviewed: the #721 product-model page, the plan file and the run records.

Checked by hand (no linter exists for these): only the page's four named lines changed (direction, Goal, Fails if, Checked by); the heading and the Limit line are unchanged; only #1011's status line changed in plan 717; the run records parse and hold no home paths.

Grounded on the base ref: the page now agrees with ADR 060 (Decisions 2 and 4), the merge-change ICE (C9, F9, S6) and the #673 page, in plain words with no names.

One small note (P4), outside this change's four lines and recorded only: line 4's clause "start-change cuts a plan's branch" is half true since ADR 061 (the play that starts the plan's work cuts it: /update-plan today, start-change once #989 is built).
