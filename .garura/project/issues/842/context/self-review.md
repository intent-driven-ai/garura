# Self-review: issue 842 (/shape-slice follows ontology v11)

Rules file: the base self-review rules (no project override). Branch plan/788/842-shape-slice-follows-v11 against origin/plan/788/base. Informational only; the approve or reject decision belongs to check-change.

Blocking items: none.

## Scope checks

- [PASS] Matches the issue. The change holds the /shape-slice edit (ICE source, recompiled SKILL.md, scripts, stop condition), the new skill author-failure-recovery with its row in the product-os-keeper agent, the write guard change, and one model page (fn-818). Each part serves the issue.
- [PASS] No scope creep. The only files outside the play folders are the new skill, the agent page, the fn-818 page and the issue 842 working files. The write guard change reaches 15 files because every play carries an identical copy; all 15 have the same checksum.
- [REVIEW] Size. About 5,000 added lines, most of it in the play, its scripts and their tests, plus 1,081 lines of working files for the issue. Large for one sitting, but it is one play rebuild; reviewers should read the ICE source first.
- [PASS] No stray artifacts. No debug prints, TODO or FIXME marks in added lines. The scratch files stay outside the repo.

## Quality checks

- [PASS] Tests present and green. All 7 test files in the shape-slice scripts pass (21, 19, 97, 18, 109, 5 and 20 checks). The write guard test passes (15 checks, 14 play copies identical to the canonical one).
- [PASS] Lint. The component linter run from the repo root gives 124 errors and 1 warning on this branch and the same 124 errors and 1 warning on an extract of the base. The set of findings is identical, so no new errors and none fixed.
- [PASS] Commits are clean. 8 commits, all in conventional format, all naming issue 842.
- [PASS] No secrets. The added lines hold no credential or key patterns.
- [PASS] Public repo hygiene. The added lines hold no local home path, no scratch folder name and no real person name (scanned for the owner's name; no hits).
- [PASS] Merge. A trial merge with the base gives no conflict.
- [PASS] Docs in step. The play's ICE source and compiled page changed together; the agent page lists the new skill; fn-818 gained the epic story-map line.
- [REVIEW] The lint_play PASS and the updated fingerprint came from the edit-play run and were not rerun here.
