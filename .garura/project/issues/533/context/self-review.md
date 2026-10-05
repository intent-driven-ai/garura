# Self-review: issue 533 (/next reads the product spine)

Rules applied: /Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md (base, not an override).
Diff: main...HEAD, 3 commits. Real change is a0365664 under core/components/plays/next/; the rest is STM run records.

Overall verdict: ready to raise. Zero blocking findings. Four notes for the reviewer.

## Scope

- [PASS] Matches the issue. The spine is now the source for slice status, order, effort, depends_on and the profile block, which is the fix the issue asks for. A separate agreement check reads independently of the scanner, which is the issue's third fix direction.
- [REVIEW] Scope creep risk. The commit also deletes classify_work.py and check_output.py and re-orders the list to "finish one slice first". The issue text does not mention these. They are inside the /next play, so they are not unrelated files, but the PR description should say why they were removed.
- [REVIEW] Size. About 1200 lines added and 860 removed across 9 play files. Large, but concentrated in one play; the PR description should justify it.
- [PASS] No stray artifacts. No commented-out blocks, scratch files or debug output found. The only print calls are the scripts' own JSON output and test runner lines.

## Quality

- [PASS] Tests present. scripts/test_derive_candidates.py was run: 15/15 passed.
- [PASS] Commits clean. Conventional format, each references #533. The two chore(stm) commits are run records.
- [PASS] No secrets. Pattern scan of the added lines found none.
- [REVIEW] Docs in step. These still point at the deleted scripts:
  - core/components/memory/knowledge/_index.md (line 40) and work-intelligence/operator-fit.md (line 6) and work-map.yaml (line 3) cite classify_work.py.
  - core/components/memory/standards/rules/no-unbacked-recommendation.md (line 73) cites check_output.py's C12/F10 check, which no longer exists in /next.
  This is stale documentation, not a broken path in the change's own goal, so it is not marked as a blocker. Worth a follow-up issue or a fix in this PR.
- [REVIEW] The play's intent files (reference/ice.md, stop-condition.yaml) changed. The project rule says intent changes go through /play-editor; the commit history does not show that. The reviewer should confirm.
- [PASS] Nothing obviously broken. No leftover TODOs.

## Blocking findings

None. This is not a blocking review.
