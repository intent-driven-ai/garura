# #1021 raised past a failed self-review line, by the product owner's word

2026-11-11, /propose-change, Step 3.

## What the self-review found

- Self-review: `.garura/project/issues/1021/context/self-review.md`, row 9, `subject-length` (must-have, the commit
  rules): 83 of the branch's 108 commit subjects are over 72 characters (81 of the 106 non-merge commits and the 2
  merge commits from main). The longest is 517 characters. Its verdict reads "Ready: no".
- Row 10, `subject-case` (nice-to-have): 36 of 106 non-merge subjects start upper-case after the colon. This line does
  not block.

## What the pre-push check said

- Command: `python3 .claude/skills/propose-change/scripts/check_self_review.py --self-review .garura/project/issues/1021/context/self-review.md`
- Exit code: 0 (`clean: true`, `count: 0`).
- The check looks for `[FAIL]`, `FAIL:` or a blocker word. This self-review writes FAIL in a table cell (`| FAIL |`),
  so the check did not see either line. The push was stopped all the same, because the self-review reads "Ready: no"
  and a push on that "clean" would pass the check without meeting what it is for (F8).

## What the product owner chose

Shown two choices (raise past the line, recorded; or shorten the 83 subjects before the first push, messages only, with
a new id for every commit), he chose: "raise past".

So the branch is pushed and the pull request opened with the must-have line failed. This run of /propose-change does
not close COMPLETED.

## What is owed

- The 83 long subjects stay in the branch's history, and reach main's history through merge-change's merge commit.
- The check that should have stopped the raise misses FAIL written in a table cell.
- A check of this kind has no way past it that a person can use. Orchestration's capability "Give every gate a way
  past" (BI-9) holds that work; it is drafted and not built.
