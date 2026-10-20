# review-change context notes — #613 / PR #682

- `fetch_pr_context.py` lists at most 100 changed paths (a known limit); the PR changes 130.
  `changed_paths` is the full list from `git diff --name-only main...HEAD`;
  `changed_paths_capped_by_script` keeps the script's count.
- `review_shelf` from config points at the installed copy (`./.garura/core/memory/`), which has
  no `knowledge/review/`. The shelf is read from Phoenix memory's machine copy,
  `~/.phoenix/core/memory/knowledge/review/` — committed, external to the branch.
- About 4,000 added lines are shared drive scripts stamped into each drive and the worked
  example; `lint_drive.py` checks every stamped copy against its source.
- Run records under `.garura/project/issues/613/evidence/` and `.garura/project/issues/680/`
  are records, not grounding.
