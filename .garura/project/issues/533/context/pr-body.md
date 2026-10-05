## What this changes

`/next` now reads the product spine (`_spine.yaml`) as the source of truth. Before, it read the per-slice record files, which lag the spine. So it recommended work that was already done: it sent griffin back to `/roadmap` after the roadmap had merged, and to `/understand` on a firm profile.

Closes #533.

## How

- **Spine read.** `scan_model.py` reads slice status, order, effort, depends_on and the profile block from the spine. It falls back to per-node records only where the spine is silent.
- **An independent check.** The issue noted that the old self-check shared the scanner's reader, so it could never catch a wrong read. The new `check_model_agreement.py` reads the model on its own. It runs inside the regression test file `test_derive_candidates.py` (15/15 pass).
- **Finish one slice first (C14).** The list now puts every step of the focus slice first. That is the lowest-order slice with work left. Other slices show as parallel lanes. They are shown, never hidden.

## Why two scripts were deleted

This was a simplification the user asked for on 2026-09-11. `/next` is now read → build and order → show.

- `classify_work.py` (operator fit) was removed with its constraint, failure condition, scenarios and recovery.
- `check_output.py` was the runtime re-scan and output check. It went through the same reader as the scanner, so it confirmed a wrong answer as clean. That is the exact failure in #533. The independent agreement reader replaces it.

This is an intent change. It went through `reference/ice.md` and a play-editor recompile. The fingerprint was recomputed, and the recompile note in `SKILL.md` records the change. Constraint, failure and scenario ids stay stable, so the numbered sets have gaps where items were removed.

## Self-review

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


🤖 Generated with [Claude Code](https://claude.com/claude-code)
