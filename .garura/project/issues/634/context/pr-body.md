## What this fixes

Two mechanical defects found while building `/intent` (#612) and `/adr` (#632):

- **Shared-script lint.** `preflight.py` and `session_stamp.py` (canonical in `play-creator/references/`, stamped unchanged into every play — 28 and 29 copies) and `lint_grounding.py` (12 copies) carried ruff E741, a variable named `l`. It is renamed to `line` in the canonical copies and every play copy; every copy of each script is still byte-identical. Behaviour is unchanged: each fixed script gives the same output as its `main` version on the same inputs.
- **`/understand`'s grounding linter** was older than the other 11 copies and lacked the realize-lens contracts. It is now identical to the others.

All 15 test suites under `core/components` pass, including `/understand`'s.

Not in this change (found at the same time, owned elsewhere): review-change's `verdict.yaml` stop condition is #536 (next, as its own change); the review-shelf path is #534 (needs a design decision first — not patched here).

Closes #634

## Self-review

# Self-Review: #634 shared-script lint

Rules applied: `~/.garura/core/memory/standards/rules/self-review.md` (base, not a project override).
Range reviewed: `origin/main...HEAD` on `feature/634-shared-script-lint` (6 commits, 75 files, +435 / -105).

Informational only. This is not the approve/reject gate.

## Scope checks

- [PASS] Matches the issue. The change renames the one-letter variable `l` to `line` in the shared scripts so `ruff --select E741` is clean, and brings the `/understand` copy of `lint_grounding.py` level with the other copies.
  - Evidence: the only changed lines under `core/components` are the `l` to `line` renames, plus 19 added lines in `plays/understand/scripts/lint_grounding.py` (the realize-lens contracts it was missing).
- [PASS] No scope creep. 69 of the 75 files are the three shared scripts: `preflight.py` (28 copies), `session_stamp.py` (29), `lint_grounding.py` (12). The 6 others are STM context files under `.garura/project/issues/634/context/`.
  - The canonical copies are `plays/play-creator/references/preflight.py` and `session_stamp.py`. Nothing else changed outside `core/components/plays/*/scripts` and that STM folder.
- [PASS] Copies are byte-identical. Every copy of each script across `core/components` has one checksum.
  - `preflight.py`: 28 copies, 1 distinct checksum.
  - `session_stamp.py`: 29 copies, 1 distinct checksum.
  - `lint_grounding.py`: 12 copies, 1 distinct checksum.
- [PASS] Canonical diff is the rename only. The changed lines in `preflight.py` and `session_stamp.py` are exactly the `l` to `line` swap (one line each in the two scripts). Non-rename diff lines in these files: 0.
- [PASS] `/understand` now equals the others. `plays/understand/scripts/lint_grounding.py` is identical (`cmp`) to `plays/vision/scripts/lint_grounding.py`. Its diff is the rename plus the seven realize-lens contracts and the `exact_title` check. Every other `lint_grounding.py` copy changed by the rename only (4 lines added, 4 removed).
- [PASS] Reasonable size. The diff is large by file count but mechanical: the same 1 to 4 line edit repeated across copies. The PR description should say so.
- [PASS] No stray artifacts. No debug prints, TODO or FIXME markers, or scratch files added in `core/components`.
- [REVIEW] One untracked file sits in the tree: `.garura/project/issues/634/context/resolved-rules.json`. It is the record of which rules file this review used, written by the propose-change run. Decide whether it is committed with the other STM context files. It is not part of the code change.

## Quality checks

- [PASS] Lint clean. `ruff 0.15.20 check --select E741` over all 69 copies reports "All checks passed!".
- [PASS] Tests present and passing. This is a behavior-preserving rename, so no new tests are needed. The existing suites under `core/components` were run (15 files, 0 failures):
  - pytest style, 11 files: 51 passed (`build-product-ontology` 6, `manage-plan` 4, `author-adr` 7, `adr` 10, `understand/test_persist_understand` 8, `play-creator` gate_learning 2, concurrent_fanout 3, platform_adapter 6, chain_checks 2, merge_scripts 3, `intent` 3).
  - Self-running script style, 4 files (pytest collects nothing from these; run directly): `next` 15/15, `grill` 6/6, `.pageindex/test_kb.py` 15/15, `play-creator/test_check_ice_workable.py` 11/11.
- [REVIEW] The 19 lines added to the `/understand` copy (realize-lens contracts, `exact_title`) have no dedicated test in this change. `test_persist_understand.py` passes, but it does not exercise the lens checks. This matches the issue's intent (the copy had drifted), so it is a note rather than a problem.
- [PASS] Commits are clean. All 6 commits use conventional format (`fix(...)` or `chore(stm)`) and each ends with `(#634)`. Each is one concern: canonical rename, `lint_grounding` rename, `/understand` catch-up, STM records.
- [PASS] No secrets. Scan of added lines found no credentials or keys. The only keyword hit is the literal heading text "Config & secrets" in the lens contract for `/understand`, which is not a credential.
- [PASS] Docs in step. No interface or user-facing behavior changed, so no docs or README need updating.
- [PASS] Nothing obviously broken. No known-failing paths introduced; all test suites above pass.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
