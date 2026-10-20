# review-change context notes — #684 / PR #685

- The PR removes local temp-folder paths, so its raw diff shows them on the removed lines.
  The raw diff is kept outside the repository; `pr.diff` here is a copy with those removed
  paths shown as `<old-temp-path>`. Reviewers read the raw diff.
- `review_shelf` is read from Phoenix memory's machine copy (`~/.phoenix/core/memory/knowledge/review/`).
