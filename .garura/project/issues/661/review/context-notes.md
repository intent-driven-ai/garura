# review-change context notes — #661 / PR #678

- `fetch_pr_context.py` lists at most 100 changed paths (a known limit); the PR changes 195
  files. `changed_paths` is the full list from `git diff --name-only main...HEAD`;
  `changed_paths_capped_by_script` keeps the script's count.
- `review_shelf` from config points at the installed copy (`./.garura/core/memory/`), which has
  no `knowledge/review/`. The shelf is read from Phoenix memory's machine copy,
  `~/.phoenix/core/memory/knowledge/review/` — committed, external to the branch.
