The one-time clean-up of Garura's own product model that ADR 070 calls for, on the product owner's confirmed list (2026-11-13):
- 21 features built before ADR 068 (each with a Story closed as completed) are now Completed.
- The duplicate features fn-727, fn-728 and fn-931 are Dropped.
- fn-818 and fn-798 are reworded to how the plays work now: one epic per plan, one Feature issue per feature, /design-slice and /design-eval.
The other 215 features stay Unplanned. Nothing else in the model changes. Taking issue numbers and decision records out of the model follows in its own change.

Closes #1059

# Self-review, issue 1059

Scope: `git diff main...HEAD` (4 commits). Rules: the self-review rule, found through the memory tool (Phoenix memory, `standards/rules/self-review.md`).

## Verdict

Ready to raise. No blocking findings. 2 small notes.

## Scope check

The change does what it says and nothing more.

- 21 features set to Completed, 3 duplicates (fn-727, fn-728, fn-931) set to Dropped. The model before: 239 features, all Unplanned. The model after: 239 features, 21 Completed, 3 Dropped, 215 Unplanned. Count: 21 + 3 + 215 = 239. Matches the stated counts.
- No feature was added or removed (same 239 ids on both sides). Only the features list of the model index changed; no other top-level section changed.
- In the 24 changed entries, only status and the "updated by" line changed. The one-line text changed for exactly 2 entries: fn-818 and fn-798. Both are the approved rewordings (one epic per plan, one Feature issue per feature, /design-slice, /design-eval).
- The two feature pages (fn-818, fn-798) carry the same rewording: story becomes Feature issue, /shape-slice becomes /design-slice, /shape-eval becomes /design-eval, one eval for the whole plan.
- The other 13 files are run records for issue 1059 under its own working folder. No other product, code or plan file changed.

## Quality check

- No "close", "fix" or "resolve" word sits before an issue number in any added line.
- No absolute path, home folder, personal name or company name in any added line.
- No attribution line in any commit message or added line.
- Words are plain; commit messages are in the conventional form and name the issue.

## Notes (not blocking)

1. Both reworded feature pages still say "written by /shape-slice at the directional depth" in their "To be deepened later" line. The old play name is left in one line each. Not part of the approved wording, so left as is.
2. The working record `resolved-rules.json` (not yet committed) holds a home-folder path (`~/.phoenix/...`). If it is committed, that breaks the no-home-folder rule. Keep it out of the commit or store only the memory-relative path.
