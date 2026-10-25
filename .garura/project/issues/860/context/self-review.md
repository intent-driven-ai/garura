# Self-review: issue 860 (every installed part reads only installed files)

Rules file: the base self-review rules (no project override), at ~/.garura/core/memory/standards/rules/self-review.md (recorded in resolved-rules.json). Branch plan/788/860-installed-parts-read-installed-copy against plan/788/base (PR #864). Informational only; the approve or reject decision belongs to check-change.

Blocking items: none. The rules file marks nothing as blocking, and no check below failed.

The branch carries one issue (#860) in 24 commits against the plan base: 325 files, +21,830 and -990 lines. This run looked hardest at the 11 round-4 commits (c7c8c372 to dda82774), which answer the review of PR #864 (decisions 17 to 25 and the "Round 4" work order). Round 4 alone is 84 files, +17,871 and -806 lines.

## Scope checks

- [PASS] Matches the issue. Every round-4 commit maps to a finding group of the work order:
  - SEC-07 narrowed to unsafe loads and request-shaped JSON parsing (decision 18), with a hit and a non-hit test.
  - H1 and H14: the install lays each tool's packages, runs each smoke check, writes the tools ignore file; uninstall removes it (decisions 20, 24).
  - H2 and H5 to H7: check-change lints the changed parts in place, takes review treatment from categories, and loads templates through template-manager; the agents' memory protocol and failure format moved to shared files with a copy script (decisions 19, 21, 22).
  - H4: lint_play needs the Next-line map; the create and edit callers pass it.
  - H8: the naming tool is no longer laid (decision 23). H9: check-pr-quality's guard is back. H10, H11: install and uninstall name what they lay; Codex stop stated in the glossary, CLAUDE.md and README.
  - H12 to H15, M1 to M5: ADR 055 facts, harness-standard principle 11, the review playbooks (harness, memory), the two skills' memory tables. M6: no change, as the work order says.
- [PASS] No unrelated edits. Outside .garura, core, docs, installer, CLAUDE.md and README.md the branch touches no file. Nothing under the deployed copies (.claude, .garura/core) was changed.
- [REVIEW] Size and run records. Round 4 is large mostly because 25 files are run records under .garura/project/issues/860 (+16,389 lines; the review's pr.diff alone is 9,410 lines and findings.yaml 2,925). The product change is 59 files and about 1,480 added lines, split by concern across 8 commits. Reviewers may confirm they want the review run files in the PR.
- [PASS] No stray artifacts. Added product lines hold no TODO, FIXME, debug print or commented-out block. The only console output is the pass report of the new test files.
- [REVIEW] The working tree shows one uncommitted change: .garura/project/issues/860/context/pr-body.md (written by this propose-change run, not part of any commit).

## Quality checks

- [PASS] Tests present and green. Run here: check-pr-quality scan tests 27 passed; lint-components 23, 27, 12, 16, 13 and 2 passed (installed-paths and memory-reading are new or extended); copy_memory 11 tests OK; create-loop lint 39 tests OK; install-garura 74 tests OK (includes the Node tool whose packages are missing from the source, and the failing smoke check).
- [PASS] Component lint, run from the repo root: 36 errors and 1 warning, the same as at the previous review of this branch. All 36 are structural gaps that exist on the base (missing sections in source-only plays and in open-pr and check-quality, which decision 14 hands to #861). None comes from the installed-paths or memory-reading rules.
- [PASS] Play lint. record-decision passes with 0 gaps. check-change shows one gap (the no-unbacked-recommendation wiring) that was also there before round 4, when it showed two; round 4 removed the pre-flight resolver gap. install-garura and uninstall-garura are source-only plays with their old gaps, unchanged.
- [PASS] Fingerprints match. check-change and record-decision carry the sha256 of their current reference/ice.md.
- [PASS] The three copies of lint_play.py (the tool, create-play, edit-play) are byte-identical.
- [PASS] Commits are clean. All 11 round-4 commits use the conventional format and end with (#860). Each is one concern; run-record commits are labelled chore(stm).
- [PASS] No secrets. The added lines hold no credential or key patterns.
- [PASS] Public repo hygiene. The added lines in core, docs, installer, CLAUDE.md and README.md hold no local home path.
- [PASS] Merge. A trial merge with plan/788/base and with origin/main both give no conflict.
- [PASS] Docs in step. ADR 055 carries the four corrections of decision 25 (contract shape change, ADR 038 section 5, intent-resolver Bash for the memory tool only, the shared files and tools ignore file). The glossary, CLAUDE.md, README and harness standard match the Codex stop and the new rule.
- [PASS] Contract of the rule. SEC-07 in the severity taxonomy now fires on pickle, marshal, yaml.load without a safe loader, yaml.unsafe_load and request-shaped JSON.parse, with a one-line reason as the #851 rows do. It still carries its priority-one severity for those unsafe loads, which is intended.
- [REVIEW] Not run here: the hidden acceptance checks, and a live install into a fresh project. Per decision 18, the SEC-07 rule reaches Phoenix memory only after this change merges, so the PR check will still use the old rule for this PR.
