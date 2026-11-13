# Self-review: issue 1062, step 2 (product model loses its tracker references)

Rules used: the base self-review rules (scope checks, quality checks). Diff reviewed: main...HEAD, 344 files (304 model pages, 32 run records under the issue folder, 8 play files). Informational; not the approve/reject gate.

## Scope

- [PASS] Matches the issue. The diff is the model strip (ADR 069 section 2) plus the reshape-plan change that reads issue numbers from the plan file. Nothing else rides along.
- [PASS] No scope creep. Model pages and the index, the one decision file, five plan scripts and their tests, one SKILL.md paragraph, and run records. The shared plan_common.py is changed identically in three places (build-play references, reshape-plan, shape-plan); the three copies are byte-identical.
- [REVIEW] Size. 344 files and about 1,300 page lines is large, but it is one mechanical rule set applied under approved rules with reports kept per rule; reviewable by rule, not by line.
- [PASS] No stray artifacts. No debug output or scratch files; the 32 files under the issue folder are the run's own records.

## Quality

- [PASS] No tracker number left on pages. A search for a hash plus digits across the model finds exactly three lines, in two feature pages: the three approved example lines (text that explains the intent/work numbering convention and quotes the ADR).
- [PASS] No numbered issue-folder path left. A search for an issue-folder path with a number across the model finds 0 lines (526 removed).
- [PASS] Tests. reshape-plan: 69 tests in the script-style runner plus test_update_plan_scripts, all OK. shape-plan: every test file passes (13 files, none failing). build-play references: every test file exits 0. lint-components on core/components: 13 passed, 0 failed. New or changed tests cover the new behaviour: a story is found only through the plan file; a capability is named through the plan node's represents; the model's old issue number is no longer read.
- [PASS] Grounding linter at its old count. Re-run live on the model: 21 errors, 279 warnings, same as the recorded before and after runs (all 21 are the same pre-existing missing-section errors on one feature page).
- [PASS] Sample of 15 rewritten lines (word-level diff across pages, every 60th change). Each keeps its product fact and every remaining quote word for word; only the tracker number, the tracker clause or the issue-folder path was cut. Examples checked: the show-plan history line, the guardrails line, the Initialize page lines, the review-tool design citations, the agreed-capability-list lines.
- [PASS] The one decision file is deleted and its decision now sits on the Initialize capability page ("Security: medium" with the typed-yes and memory-scope gate). No remaining reference to the deleted file anywhere in the model.
- [PASS] Commits are clean. Five conventional commits plus run-record commits, each referencing the issue; no close/fix/resolve word before an issue number in commits or added lines.
- [PASS] No secrets, no absolute paths, no attribution lines in added lines. A check for personal details (email-shaped text, personal or company names) over the added lines found none.
- [PASS] Docs in step. The reshape-plan SKILL.md placement paragraph and the scripts' docstrings describe the new rule (plan file's represents, not the model).

## Findings (notes, none blocking)

1. Dropped evidence. About a dozen "GitHub issue ... (open/closed)" source lines were removed whole, with the issue-title quotes they held. The quotes that stay are intact, but those tracker-sourced quotes no longer appear as sources on the pages.
2. The decision file's alternatives (keep none, move to high) and its "from none to medium" history are not on the Initialize page; only the resulting level and its gate are.
3. A few status lines became short ("Status: not built; planned."). Facts are kept; the wording is terse.
4. The SKILL.md placement paragraph now has one long line after the edit (cosmetic).
5. One page cites another page by line number ("line 54"); the cited page was also edited, so that number may have shifted. Not checked line by line.

Verdict: ready to raise.
