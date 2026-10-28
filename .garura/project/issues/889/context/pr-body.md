Fixes #889: `/check-change` can now review a pull request of any size.

GitHub gives one diff for at most 300 files, and its paged file list stops at 3,000. The plan 788 landing (PR #916) changed 3,192 files, so the review stopped at its first step. Now, when the one diff is refused, the review reads the compare diff of the pull request's two branches. GitHub returns that with every file and its full text. A very large diff can drop the connection, so the call gets three tries, a few seconds apart. A failure no retry can fix stops at once. For a pull request from a fork, the call names the fork's owner with its branch. If it still fails, the review falls back to the paged file list, as before. The count check is unchanged: if the files found don't match GitHub's count, the review stops.

- The code-host helper gets one new command, `compare-diff`, in all 7 copies. It is GitHub only, and on GitLab it stops with a plain message.
- The review's context script tries the commands in the new order, in both copies.
- New tests cover a pull request over 3,000 files, a dropped call tried again, the fallback, and a count that does not match.
- The helper's docs and its GitHub and GitLab pages name the new command.

Round 2 fixes the six severity-3 findings of review round 1: the helper's instructions now say 23 commands everywhere, list all 23, and give the five older GitHub-only commands their entries; the compare wording is right; the play builder's test copy has the new cases; and the waits, early stop and fork handling are in. The five severity-4 findings are chore #919.

## Self-review

Rules used: standards/rules/self-review.md (base, no project override). This list is information for the reviewer. It is not the approve or reject gate, and nothing here stops the raise.

Summary: no blocker. Round 1's review asked for six fixes (.garura/project/issues/889/review/round-1/decision.yaml: H-1, H-2, H-3, Q-001, Q-002, Q-003); commit 486e6c65 makes them. Two small points for the reviewer.

## Scope checks

- [PASS] Matches the issue. The change makes /check-change read a pull request with more than 300 files: the compare diff of the two branches first (three tries, a few seconds apart), the paged file list (up to 3,000 files) second, and the count check unchanged.
- [PASS] The six round 1 fixes are in, and nothing else rides along. The fetch script waits 5 seconds between compare tries and stops at once on HTTP 404/422 or the adapter's exit 2. It names a fork's head as owner:branch. The adapter's view-pr now asks for isCrossRepository and headRepositoryOwner. The platform-adapter docs say 23 verbs everywhere, the unknown-verb message lists all 23, compare-diff is described as the first try over 300 files, and each of the five GitHub-only verbs has an entry on the GitHub page and on the GitLab page. The five small ones are filed as #919.
- [PASS] No scope creep. Source files touched (15): the fetch script (2 copies), the adapter (7 copies), the test files (3), and the platform-adapter SKILL.md plus its GitHub and GitLab verb pages. The rest is run records under this issue's folder.
- [PASS] The copies agree. The adapter is byte-identical in all 7 plays (one checksum for the 7 files), and the fetch script is byte-identical in its 2 places. The two fetch test files differ on purpose: they are two different test files that were written separately, each carrying its own new cases.
- [REVIEW] Size. About 440 lines added and 68 removed in source files, but 7 of the 15 files are the same adapter change copied. The real change is small: one verb, one fallback step, a wait and a stop rule, tests, docs. Fine to review in one sitting.
- [PASS] No stray artifacts. No commented-out code, debug prints (the one print( in the added lines is a test heading), TODO or FIXME. The working tree is clean.
- [REVIEW] Issue text. Issue 889's text was updated and covers the compare diff first, three tries, and the file list second. It does not yet say that the tries wait between them, that a failure no retry can fix stops at once, or that a fork's head is named owner:branch. The behaviour is in the code, tests and docs; the work order lags it by those three lines.

## Quality checks

- [PASS] Tests present. All run from the repo root.
  - check-change/scripts/test_fetch_pr_context.py: 17 passed, 0 failed. New cases: compare diff used; 3,192 files (past the list limit); a 404 stops at once and falls back; three drops fall back; exit 2 is not tried again; a fork names its head owner:branch; a same-repo PR names the branch only; a dropped call is tried again; no head branch skips the compare; the count check holds on the compare path.
  - create-play/references/test_fetch_pr_context.py: 17 passed, 0 failed (compare used, dropped then ok, three drops fall back, not found stops at once).
  - create-play/references/test_platform_adapter.py: 53 passed, 0 failed (compare-diff command, GitLab stops with exit 2, 23 verbs).
- [REVIEW] Test gap, small. The fork head naming is tested in the check-change test file only, not in the create-play copy. The adapter's view-pr field list (isCrossRepository, headRepositoryOwner) has no test of its own; the fork test feeds those fields in by hand. Not a blocker; the call and the field names match GitHub's view output.
- [PASS] Linter, lint-components (node core/tools/lint-components/index.js --target core/components): 36 errors and 1 warning. Main gives the same 36 errors and 1 warning, and the findings are the same. Nothing new from this change. Old gap, not this change's.
- [PASS] Linter, play linter (python3 core/components/plays/create-play/scripts/lint_play.py <SKILL.md> --next-map core/components/memory/standards/rules/pipeline-next.md) on the 7 plays whose files changed, compared to main: check-change has 1 gap (no-unbacked-recommendation) on both; create-play has 6 gaps on both; merge-change, propose-change, shape-eval, shape-plan and shape-slice pass on both. Old gaps, not this change's.
- [PASS] Commits are clean. 11 commits since main: 2 fix(check-change) commits that carry the code, tests and docs (33a84e05 first, 486e6c65 for the round 1 fixes), and 9 chore(stm) run-record commits. All reference (#889).
- [PASS] Docs in step. No "16" or "22" verb count is left in the platform-adapter skill, the adapter docstrings or the helper copies. The fetch script's header describes compare-diff, the wait and stop rule, the fork head, and the file list as the second try.
- [PASS] No secrets. The added lines hold no credentials, tokens or keys.
- [PASS] Hygiene. In every line added since main, no home-folder path, scratchpad path, company or personal name. The only hits are file names (CLAUDE.md, AGENTS.md) and the words of the hygiene checks themselves in run records. No Claude attribution, Co-Authored-By line or personal name in any commit message since main.
- [REVIEW] Cosmetic. In the fetch script's header, one sentence runs on a long line (about 150 characters) where the fork sentence was joined to the next; it reads fine. Branch names are still not escaped in the compare address (Q-004, logged in round 1 as not fixed).
- [PASS] Nothing obviously broken. The one-diff path is unchanged and tested; a failed compare never skips the count check; a 404 or 422 no longer costs two extra calls; GitLab stops with a plain message, runs nothing, and the caller falls back to the file list. The deployed copy under .claude/skills/platform-adapter is not tracked here and is refreshed by the install; it is not part of this change.

Blocking issues: none.
