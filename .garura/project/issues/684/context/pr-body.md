Closes #684.

Old review records on main held local temp-folder paths: some carried the author's home-folder name, two carried the machine user number. Each of the 8 lines now reads `<scratchpad>`; nothing else in those records changed. The repository is public, so files keep no personal or local-machine references.

- 1 line in #498, 1 in #500, 2 in #614, 4 in #632 (records and the saved diff).
- A search of the branch for the temp-folder pattern and the home-folder name finds nothing.
- Git history keeps the old lines; rewriting history is out of scope.

## Self-review

## Blocking findings

None. Nothing here should stop this change from being raised.

## What the change does

Eight lines in six old review records held a local temp-folder path. Some of those paths carried the author's home-folder name; two carried the machine user number. Each one is now the neutral marker `<scratchpad>`, and the rest of each line is unchanged.

The other six files in the change are this run's own record files under the issue 684 folder (what was analysed, which branch, which commits, the issue text).

## Scope checks

- Matches the issue: pass. The issue asked for eight lines in the records of #498, #500, #614 and #632 to be replaced with a placeholder. That is exactly what changed: 1 line in #498, 1 in #500, 2 in #614, and 4 in #632 (2 in the saved diff file, 1 in each of the two trial decision files). That is 1 + 1 + 2 + 4 = 8 lines.
- No scope creep: pass. No other old record was touched, and no wording in any record changed beyond the path.
- Reasonable size: pass. 8 one-line swaps plus 6 small run records. Easy to read in one sitting.
- No stray files: pass. No commented-out text, debug output or leftovers. One run file (the resolved-rules file) sits untracked on disk and is not part of the diff; it belongs to this run and is the commit step's concern, not a problem with the change.

## Quality checks

- Tests: not needed. These are records, not behaviour. The issue's own check ("a search of main for the temp-path pattern finds nothing in the review records") was run against the branch: the search for the temp-folder pattern and for the home-folder name found nothing anywhere in the committed files.
- Commits: pass. All four use the chore(stm) form and each names issue 684. Each is one concern: workspace record, the path replacement, the run artifacts, and moving the commit record.
- Secrets: pass. No keys, tokens or personal details were added. The new text contains no home-folder path and no personal email.
- Docs in step: pass. Nothing user-facing changed.
- Nothing broken: pass. The replacement is plain text in records; the only mild effect is that the saved diff file (#632) now differs slightly from the real diff it recorded on those two lines. That is expected for this clean-up and is the point of the issue.

## Notes (not blocking)

- Two earlier-looking mentions of generic temp folders in the #659 records remain. They describe temp folders in general terms and carry no home-folder name or user number, so they are outside this issue.
- Old commits in the history still hold the original paths. The issue lists rewriting history as out of scope.
- The review-change play that saves full paths in its records is a separate fix, also out of scope per the issue.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
