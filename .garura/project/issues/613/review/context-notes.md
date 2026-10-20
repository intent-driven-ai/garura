# review-change context notes — #613 / PR #682, round 2

- Round 2 re-reviews the whole PR, with focus on the fixes since round 1 (commits after
  `27f40817`: ADR 041, the text fixes, the lint-record path fix). Round 1's record is kept in
  `round-1/`; the fixes' own diff is `round-2-delta.diff`.
- `fetch_pr_context.py` lists at most 100 changed paths (a known limit); the PR changes 168.
  `changed_paths` is the full list from `git diff --name-only origin/main...HEAD`;
  `changed_paths_capped_by_script` keeps the script's count.
- `review_shelf` from config points at the installed copy, which has no `knowledge/review/`.
  The shelf is read from Phoenix memory's machine copy, `~/.phoenix/core/memory/knowledge/review/`
  — committed, external to the branch.
- Linter output saved in this folder uses repository-relative paths (round 1's record leaked
  absolute local paths; fixed in `fbdcdfd0`).
