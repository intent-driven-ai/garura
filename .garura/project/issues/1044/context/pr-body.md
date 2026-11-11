## What this changes

Every play and the one loop now carry a name that says who does the work, as ADR 066 decided. Five roles own the play verbs: a specifier specifies, a designer designs, a builder builds, fixes and refactors, a validator validates, and an orchestrator shapes, reshapes, views and lists. Loops are named for the transition they run, `loop-<from>-<to>`, and the second phase is called Spec. 30 parts are renamed; names and references only, no play does anything different.

| Role | Old → new |
|---|---|
| Specifier | discover-intent → specify-intent · discover-domains → specify-domains · discover-capabilities → specify-capabilities · edit-ontology → specify-ontology |
| Designer | shape-slice → design-slice · shape-eval → design-eval · record-decision → design-adr · shape-ux-lens → design-surface · shape-run-lens → design-env · shape-architecture-lens → design-architecture · shape-quality-lens → design-quality · shape-agentic-lens → design-agentic |
| Builder | build-epic → build-work · fix-bug → fix-work · refactor-code → refactor-work · create-play → build-play · edit-play → fix-play · create-loop → build-loop · edit-loop → fix-loop |
| Validator | check-change → validate-work · validate-epic → validate-slice · release-epic → validate-uat |
| Orchestrator | update-plan → reshape-plan · show-plan → view-plan · list-focus-issues → list-issues |
| Loop | complete-discovery → loop-product-spec |
| Work plays (no role) | start-change → start-work · commit-change → commit-work · propose-change → review-work · merge-change → merge-work |

So no one takes the old names for the current ones:
- The ADR index now shows, beside "Accepted", the newer ADR that supersedes or amends each record (41 rows; before, every one read plain "Accepted").
- ADR 066 names this issue on its line "The rename, as one change".
- Closed issues #736, #742, #743, #744 and #745 carry a first line: replaced by ADR 066, the rename is #1044.
- Phoenix memory's naming rules match the source (phoenix-memory 4209021).

## What to read

The change is 838 files, nearly all the rename tool's mechanical rewrite. The hand-written parts:
- The rules: `core/components/memory/standards/rules/naming.md`, `naming.yaml`, `rename-map.yaml`
- The checks: `core/tools/lint-components/lib/rules/naming.js` and its test; `core/tools/naming/check_old_names.py` (ADRs up to 066 are past records) and its test
- The ADR index: `core/components/skills/author-decision/scripts/adr.py` (`index_status`) and its test; `docs/adr/_index.md`; ADR 066 line 149
- The wording: `docs/standards/harness-standard.md`, `docs/components/loops.md`, `CLAUDE.md`, `core/grounding/glossary.md`

## Checks

- Acceptance check (`.garura/project/issues/1044/evidence/eval/check_1044.py`): 3 passed / 48 failed before the build, 82 / 82 after.
- Old-name check: 0 old names left.
- Component linter: no naming error; the 37 structural errors are the same as on main.
- Test suites: 92 of 93 pass. `reshape-plan/scripts/test_feature_ice.py` fails the same way on main.
- Each play's own linter verdict matches main for all 37 plays.

## Worth knowing

- Each renamed play's ICE took its new wording through the rename tool, as #743 to #746 did, not one /edit-play run each as ADR 066 says (the product owner's choice); 31 fingerprints are stamped again. `list-issues` already had a fingerprint out of step on main and is left as it was.
- Internal record file names that carry a play's old name inside a longer word (such as `session-stamp-start-change.json`) are unchanged; each play writes and reads its own under the same name.
- `docs/philosophy/intent-and-adlc.md` named ten plays by names from before ADR 046 (already failing the old-name check on main); the tool brought them to the current names.
- Garura is not reinstalled into this repo; until it is, the commands here keep their old names.

## Self-review

# Self-Review: #1044 Plays and the loop take names that say who does the work (ADR 066)

- Branch: feature/1044-names-say-who-does-the-work (pattern: feature), base: main
- Rules: .garura/project/issues/1044/context/memory/standards/rules/self-review.md (base file, no project override)
- Commits: 9. Files changed: 838 (455 renames, 246 modified, 74 added, 63 deleted). +20523 / -16509.
- Suggested PR title: `refactor(naming): rename 29 plays and the product loop to role-based names (ADR 066) (#1044)`
- Informational only. This checklist does not gate the raise; the review-change gate does.

## Scope checks

| Item | Status | Evidence |
|------|--------|----------|
| Matches the issue | PASS | Every "Done when" line of #1044 is met in the diff or outside it. (1) Old-name check exits 0: `core/tools/naming/check_old_names.py` reports 0 hits, `by_old_name` empty. (2) Linter naming rule changed (`core/tools/lint-components/lib/rules/naming.js` and `test/naming.test.js`); component linter run gives 0 naming errors. (3) `naming.md` phase table says Spec (lines 50, 56-57). (4) ICE files carry the new names; the acceptance check (82/82) covers goal, limit and check unchanged. (5) Phoenix memory copies match source: `~/.phoenix/core/memory/standards/rules/naming.md` and `naming.yaml` are byte-identical to `core/components/memory/standards/rules/`, committed as phoenix-memory 4209021 and not ahead of origin. (6) ADR 066 line 149 now reads "The rename, as one change (#1044)"; `docs/adr/_index.md` shows supersede and amend pointers (adr.py `index_status`); #736, #742, #743, #744 and #745 each start with "Replaced by ADR 066 (2026-11-03); the rename is #1044." and #746 is untouched. |
| No scope creep | PASS | Play directories are exactly the 29 renames plus the loop `loop-product-spec`. `shape-plan`, `list-plans`, `learn-outcomes`, `install-garura`, `uninstall-garura` and `release-increment` keep their names; `release-increment` and `shape-marketing-lens` / `shape-measure-lens` only have references rewritten, not renamed or deleted. None of the new plays the issue excludes (/view-issue, /validate-perf, /validate-security, the five unbuilt loops) was added. No skill or agent directory was renamed; the skill and agent edits are reference rewrites (old play names to new). The `realized` check in /build-work was not removed. Edits to `docs/philosophy/*`, `docs/components/*`, `core/tools/*` and `core/components/skills/*` are old-name rewrites by `apply_renames.py`, which the issue's "every reference" requires. |
| Reasonable size | REVIEW | 838 files is far past one sitting, but 455 are pure renames and most of the rest are mechanical reference rewrites made by `core/tools/naming/apply_renames.py` and verified by the old-name check, the linter (per-play verdicts match main for all 37 plays) and the 82-check acceptance script. The issue asks for one change. Reviewer should read the hand-written parts: `naming.md`, `naming.yaml`, `rename-map.yaml`, `naming.js` and its test, `adr.py` and its test, `harness-standard.md`, `CLAUDE.md`, `loops.md`, glossary, ADR 066 line 149, and `docs/adr/_index.md`. Size is justified here; state it in the PR body. |
| No stray artifacts | PASS | No `__pycache__`, `.pyc`, `.DS_Store`, `.bak` or `.orig` tracked or in the diff. No TODO, FIXME, debug print or breakpoint added outside `.garura/`. `.garura/project/issues/1044/` holds 11 run-record and acceptance-check files (context json/yaml, `evidence/eval/check_1044.py`, result-before and result-after); these are the issue's short-term memory the plays write by design. Two untracked paths remain uncommitted (`context/memory/`, `context/resolved-rules.json`), which are this review's own inputs, not part of the change. |

## Quality checks

| Item | Status | Evidence |
|------|--------|----------|
| Tests present | PASS | Behavior changes carry tests: `core/tools/lint-components/test/naming.test.js` (loop-name and built-in-name cases), `core/tools/naming/test_naming_tools.py`, `core/components/skills/author-decision/scripts/test_adr.py` (index pointers). Run results given for this branch: 92 of 93 suites pass; the one failure, `reshape-plan/scripts/test_feature_ice.py`, fails the same way on main. Acceptance check `check_1044.py` failed before the build (36fbd2de) and passes 82/82 after (result-before.json, result-after.json). |
| Commits are clean | PASS | All 9 commits are conventional (`feat`, `refactor`, `docs`, `test`, `chore`) with a scope and `(#1044)` in the subject; each is one concern (naming standard, rename, docs wording, ADR index, acceptance record, STM records). No "Co-Authored-By" or "Generated with" line in any commit message (0 matches). `commits_rules_path` was not supplied, so the format was judged against the base conventional-commit shape. |
| No secrets | PASS | Pattern scan of added lines outside `.garura/` (AWS key, GitHub token, `sk-` key, private key header, quoted password) found nothing. |
| Docs in step | PASS | Harness standard, `CLAUDE.md`, `docs/components/loops.md`, glossary, `docs/philosophy/*` and ADR 066 are updated in the diff (`docs/standards/harness-standard.md` +40 lines). Phoenix memory copies are promoted. |
| Nothing obviously broken | PASS | Old-name check 0 hits; component linter 0 naming errors and 37 structural errors, the same count as main; per-play verdicts match main for all 37 plays; the single failing test fails on main too. |

## Blocking issues

None. The rules file names no blocking item; the one REVIEW item (size) is justified above.

## Readiness

- Ready: yes
- Blocking count: 0
- Review required: 1 (size, for the reviewer's read of the hand-written files listed above)

Closes #1044
