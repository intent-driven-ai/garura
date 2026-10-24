# Self-review: issue 860 (every installed part reads only installed files)

Rules file: the base self-review rules (no project override), at ~/.garura/core/memory/standards/rules/self-review.md. Branch plan/788/860-installed-parts-read-installed-copy against origin/plan/788/base (the plan base). Informational only; the approve or reject decision belongs to check-change.

Blocking items: none. The rules file marks nothing as blocking: the self-review does not block the raise on its own, and no check below failed.

The branch carries one issue (#860, a priority-one change) with 9 commits: the tools install, the installed lint tools, the memory reads, the play recompiles, the stamped-script notes, ADR 055, and three run-record commits.

## Scope checks

- [PASS] Matches the issue. Each part of the diff maps to a section of the build contract or to a decision in decisions.md:
  - Section 1 (tools are deployed): install-garura and the public installer lay every tool except the prototype, and uninstall removes them; lint_play.py moved to its own tool, with the copies in create-play and edit-play identical to it (3 files, one checksum).
  - Section 2 (uses name the installed place): check-change, its two review playbooks and discover-intent name the installed tools; check-change also hands the Next-line map to the installed play lint (decision 12).
  - Section 3 (memory through the memory tool): check-pr-quality, quality-auditor, check-change's fetch script, intent-resolver (decision 15) and the architecture-learnings search script no longer read memory by path; the standards entry for the severity taxonomy left core/config.yaml.
  - Section 4 (pointers and notes of origin): the origin notes are gone from the installed parts and the stamped scripts; the pointers (list-focus-issues, track-issue, close step, shape-slice) name installed files.
  - Section 5 (check, rule, test): the new installed-paths/source-path lint rule and its tests, the installed layout of lint-components, the rule in CLAUDE.md and in the harness standard, and the empty-project install tests.
  - Round 2 (decisions 10 to 13): no pointer to Garura's docs, the Codex installer stops with a message that names #863, the copies of lint_play.py are kept identical by a lint check with a test, and ADR 055 holds the rule.
- [PASS] Deleted notes in start-, propose- and merge-change are the ones decision 16 names.
- [REVIEW] Scope creep. 18 files sit outside core, installer, docs and CLAUDE.md. They are run records under the project folder: 8 for this issue and 10 for the ADR run (the _adr folder). They are the run records the commits name, not product code. Reviewers may confirm they want them in the PR.
- [REVIEW] Size. 273 files, 4,399 lines added and 880 removed. Large, but 192 of the files are plays and about 100 of those change by a few lines each (a stamped script or a deleted origin note). The new logic is in a few files: the installed-paths lint rule, the installed layout of lint-components, the lint-play tool, and the install scripts. The commits are split by concern so each can be read alone.
- [PASS] No stray artifacts. The added lines hold no TODO, FIXME, debug print or leftover block. The only console output in added lines is the pass report of the new test file. No file under the deployed copies (.claude, .garura/core) was touched.

## Quality checks

- [PASS] Tests present and green. New tests cover the installed-paths rule (23 checks) and the shared-scripts rule; the other lint-components test files pass (18, 16, 13, 2 checks). The install test passes in full (60 tests), including the empty-project tests and the Codex stop. The check-change fetch script test passes (13 checks).
- [PASS] Lint. The component linter, run from the repo root, gives 36 errors and 1 warning on the branch against 102 errors on the base. No error is new: every one of the 36 is also on the base, and none is an installed-paths/source-path error.
- [PASS] Play lint. For each of the 18 plays the change touches, the lint output shows the same count of gap lines as on the base. No play gains a gap. check-change passes every listed check.
- [PASS] Old-name check. check_old_names.py reports no finding.
- [PASS] Source-path rule. The new rule finds no installed part, outside the named exceptions, that names core/components/ or core/tools/.
- [PASS] Commits are clean. 9 commits, all conventional format, all naming #860.
- [PASS] No secrets. The added lines hold no credential or key patterns.
- [PASS] Public repo hygiene. The added lines hold no local home path and no real person name.
- [PASS] Merge. A trial merge with origin/plan/788/base gives no conflict.
- [PASS] Docs in step. CLAUDE.md, the harness standard (principle 11), the memory tool README, ADR 055 with its index entry, and one earlier ADR carry the rule and its pointer.
- [REVIEW] Not run here: the hidden acceptance checks and a full-repo pass of every script test beside a touched script. The ones named above were run.
