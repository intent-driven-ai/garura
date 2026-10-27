Fixes #889: `/check-change` can now review a pull request of any size.

GitHub gives one diff for at most 300 files, and its paged file list stops at 3,000. The plan 788 landing (PR #916) changed 3,192 files, so the review stopped at its first step. Now, when the one diff is refused, the review reads the compare diff of the pull request's two branches. GitHub returns that with every file and its full text. A very large diff can drop the connection, so the call gets three tries. If it still fails, the review falls back to the paged file list, as before. The count check is unchanged: if the files found don't match GitHub's count, the review stops.

- The code-host helper gets one new command, `compare-diff`, in all 7 copies. It is GitHub only, and on GitLab it stops with a plain message.
- The review's context script tries the commands in the new order, in both copies.
- New tests cover a pull request over 3,000 files, a dropped call tried again, the fallback, and a count that does not match.
- The helper's docs and its GitHub and GitLab pages name the new command.

## Self-review


Rules used: standards/rules/self-review.md (base, no project override). This list is information for the reviewer. It is not the approve or reject gate, and nothing here stops the raise.

Summary: no blocker. Three points for the reviewer (one scope note, one issue-text note, one edge case).

## Scope checks

- [PASS] Matches the issue. The change makes /check-change read a pull request with more than 300 files, which is what issue 889 is about. The count check is unchanged.
- [REVIEW] Same goal, different route than the issue text. Issue 889 says to read GitHub's paged file list and to fill a file that has no patch from local git. The change reads the compare diff of the two branches first (up to three tries) and uses the paged file list second. The reason is in the code: the paged file list stops at 3,000 files, and the compare diff has no file limit. A file with no patch is not filled from local git; the existing behaviour is kept (the file keeps its header and a note). The issue text should be updated to say this, so the work order matches what was built.
- [PASS] No scope creep. Every file touched is one of: the fetch script and its copy, the adapter library (seven identical copies), the two test files, the three adapter docs, and the run records for this issue.
- [PASS] The copies agree. The adapter file is byte-identical in all 7 plays, and the fetch script is byte-identical in its 2 places.
- [REVIEW] Size. 14 source files and about 230 added lines, but most of it is the same 19-line adapter change copied 7 times, so the real change is small (one verb, one fallback step, tests, docs). Fine to review in one sitting.
- [PASS] No stray artifacts. No commented-out code, debug prints, TODO or FIXME in the added lines. One untracked file is left over from this run: .garura/project/issues/889/context/resolved-rules.json (the run record of this self-review; the play handles it).

## Quality checks

- [PASS] Tests present. check-change/scripts/test_fetch_pr_context.py: 13 passed, 0 failed (compare diff used; 3,192 files past the list limit; failed compare falls back to the file list after 3 tries; a dropped call is retried; no head branch skips the compare; count check holds for both new paths; other failures still stop). create-play/references/test_platform_adapter.py: 53 passed, 0 failed (compare-diff command, GitLab stops with exit 2, verb count 23).
- [PASS] Linter, lint-components (node core/tools/lint-components/index.js --target core/components): 36 errors and 1 warning, the same 37 findings as on main. Nothing new from this change. Old gap, not this change's.
- [PASS] Linter, play linter on the 7 plays whose files changed (check-change, create-play, merge-change, propose-change, shape-eval, shape-plan, shape-slice): same verdict as on main for each. Old gaps, not this change's: check-change has 1 gap (no-unbacked-recommendation) and create-play has 6 gaps, both the same on main. The other five pass.
- [PASS] Commits are clean. 3 commits since main: one fix(check-change) commit with the code, tests and docs together (one concern, one issue), and two chore(stm) run-record commits. All three reference (#889).
- [PASS] Docs in step. platform-adapter SKILL.md (verb count 22 to 23, new table row, the unknown-verb message), the GitHub verbs page and the GitLab verbs page all describe compare-diff. The script header comments and the "23 verbs" text in the adapter agree with them.
- [PASS] No secrets. The added lines hold no credentials, tokens or keys.
- [PASS] Hygiene. No home-folder path, scratchpad path, company or personal name in the added lines or the run records. No Claude attribution or Co-Authored-By line in any commit message since main.
- [REVIEW] Edge case worth a look. The compare call uses only the head branch name. A pull request from a fork has a head branch that does not exist in the base repository, so the compare call fails; after 3 tries the play falls back to the paged file list, so it still works up to 3,000 files. The failed compare is retried on any error, including a plain 404, which costs two extra calls and no more. Not a blocker.
- [PASS] Nothing obviously broken. The one-diff path is unchanged and tested; a failed compare never skips the count check; GitLab stops with a plain message and runs nothing, and the caller falls back to the file list.
- [PASS] Compared against main. The installed copy under .claude/skills/platform-adapter still says 22 verbs, but that folder is a deployed copy that is not tracked here and is refreshed by the install; it is not part of this change.

Blocking issues: none.
