# #1037 raised past a failed self-review check, by the product owner's word

2026-11-11, /propose-change, Step 3.

## What the check found

- Command: `python3 .claude/skills/propose-change/scripts/check_self_review.py --self-review .garura/project/issues/1037/context/self-review.md`
- Exit code: 1 (`clean: false`, `count: 1`).
- The one blocking line: "Commits are clean": commit 339ddf54 has a subject of 156 characters, and the commit rules cap it at 72 (`subject-length`, must-have). The other four subjects are 54 to 70 characters.
- Every other line of the self-review passes, or is a REVIEW line that does not block.

## What the product owner chose

Shown three choices (shorten the subject by rebuilding the four unpushed commits; leave it and raise anyway; or change the check or the rule), he chose to leave it: "B". Asked what that meant (raise past the check by his word, recorded; change the check so a person can accept a blocking line; or relax the rule), he chose: "1".

So the branch is pushed and the pull request opened with the check failed. Step eval SE-8 (the check ran before the push and exited 0) is not met, and this run does not close COMPLETED.

## What is owed

- The 156-character subject of commit 339ddf54 stays in the branch's history.
- The check that stopped the raise has no way past it that a person can use. Orchestration's capability "Give every gate a way past" (BI-9, #1021) holds that work; it is drafted and not built.
- The self-review the product owner dropped on 2026-11-10 ("yes, record it with self-review dropped") still runs in /propose-change as built; taking it out is owed to Raise each change for review against where it lands (fn-raise-change, BI-8).
