# Self-Review: #1037 (the model's index tool clears a thin mark, moves a feature to another capability, and moves a part's page)

Driven by the base self-review rules (no project override), the assess-pr quality ruleset and the
commit rules. This checklist is informational; the approve or reject gate is `review-change`.
Each line carries one status: PASS, REVIEW (a person signs off) or FAIL (a must-have rule is broken).

This is the review of the re-raise. PR #1038 is open. Since the last raise the human reviewer rejected it on
finding R-1 (two moves into one folder lost a page); commit d4cb234f fixes R-1, R-2 and R-3 and four doc gaps
(H-L2-1 to H-L2-4). One failed line is known and was raised past by the product owner; one is new.

## Branch Info

- **Branch**: `feature/1037-index-tool-thin-and-moves` (pattern: feature, standard priorities)
- **Base**: `main` (the branch sits on main's tip, main equals origin/main; a trial merge is clean)
- **Remote**: origin holds the branch up to commit 6de7f7c6; the three newest commits (d4cb234f, a8cc4a8a, 090b3e8d) are not pushed yet

## Change Summary

- **Commits**: 12 (5 at the last self-review)
- **Files changed**: 57 (+7275 / -26)
- **Source part**: 4 files under `core/components` (+402 / -26)
- **Acceptance check**: 1 file, 322 lines (`.garura/project/issues/1037/evidence/eval/eval_1037.py`)
- **Run records**: 52 files (+6551) under `.garura/project/issues/1037/`, written by the start, commit, propose and check plays

## Suggested PR Title

```
feat(skills): clear a thin mark and move a feature or a page (#1037)
```

## Context Detected

| Pattern | Files |
|---------|-------|
| Skill definition (`core/components/skills/link-model-part/SKILL.md`) | 1 |
| Agent definition (`core/components/agents/product-os-keeper.md`) | 1 |
| Python (the index script, its tests, the acceptance check) | 3 |
| YAML run records | 14 |
| JSON run records | 14 |
| Markdown and text run records | 22 |
| Other run records (`review/pr.diff`, `review/lint-components.err`) | 2 |

| Commit type | Count | Subject |
|-------------|-------|---------|
| feat | 1 | clear a thin mark and move a feature or a page |
| fix | 1 | refuse moves into a shared folder; name undo gaps |
| test | 1 | the acceptance check, failing before the build |
| chore | 9 | stm run records |

## Scope Checks

- [PASS] **Matches the issue**: the change adds the three updates the issue names to the index script of `link-model-part` (`thin: false`, `capability: <id>`, `doc: <new path>`), with the skill doc, the agent's skill-table and mapping rows, unit tests and the acceptance check. The fix commit d4cb234f answers the review of this same change (R-1, R-2, R-3, H-L2-1 to H-L2-4) and touches only the same four source files. The one adjacent edit, the domain refusal that now also covers `thin: false`, belongs to the same feature and is covered by acceptance scenario E4.
- [PASS] **No scope creep**: all 57 files sit in the issue's own places: the 4 source files named above and 53 files under `.garura/project/issues/1037/` (the acceptance check and 52 run records). No file outside those. Each commit keeps to one concern: the 9 chore commits touch only records, the feat and fix commits touch only the four source files, the test commit touches only the acceptance check.
- [PASS] **Reasonable size**: +7275 / -26 over 57 files, but a reviewer reads 4 source files (+402 / -26) and one acceptance check (322 lines); the other 52 files are run records the pipeline plays wrote on purpose.
- [PASS] **No stray artifacts**: no TODO, FIXME, debug print or commented-out block in the added source lines; no `__pycache__`, backup or scratch file in the diff (the `__pycache__` folder the test runs leave is ignored by git and the tree is clean). The run records and template copies are what the start-change, commit-change, propose-change and check-change plays commit on purpose.

## Quality Checks

- [PASS] **Tests present**: 48 unit tests, 4 of them new in the fix commit (two moves into one folder refused; a failed delete; a failed folder removal; an undo that cannot finish), plus the acceptance check. Run here from the repo root: acceptance check 30 of 30 pass (exit 0); skill unit tests 48 of 48 pass (exit 0). I also removed each piece of the fix in a scratch copy and ran the suite: without the shared-folder refusal the R-1 test fails; without the undo of deleted files two tests fail; without the "names what is not back" error the R-2 test fails. One piece, re-making a removed folder during the undo, is not pinned by any test (see Observations).
- [FAIL] **Commits are clean (known)**: commit 339ddf54 has a subject of 156 characters; the commit rules cap it at 72 (`subject-length`, must-have). The product owner chose to raise past this line, recorded in `.garura/project/issues/1037/context/raise-past-check.md`. This commit is on origin now (PR #1038), so rewording it needs a force push.
- [FAIL] **Commits are clean (new)**: commit 6de7f7c6 has a subject of 82 characters, "chore(stm): record the memory copies and the next-line map the review used (#1037)"; the commit rules cap it at 72 (`subject-length`, must-have). It was made after the last self-review, so the product owner's recorded choice does not name it. It is on origin now (PR #1038). The other ten subjects are 53 to 70 characters.
- [PASS] **Conventional format and issue reference**: all 12 commits use a valid type (`feat`, `fix`, `test`, `chore`) with a scope, each names #1037, each is one concern, no commit has a body, and none carries an attribution trailer.
- [PASS] **No secrets**: the secret pattern from the PR rules (SEC-19) and a scan for private keys and cloud or chat tokens found nothing in the 7251 added lines. No path in the added lines starts at a home folder or a temp folder. The biggest file in the diff is 105 KB, far under the 1 MB limit.
- [REVIEW] **Docs in step**: the interface docs name the three updates and both new report keys (`SKILL.md` description, Input, Output and Rules; the script header; the `product-os-keeper` table row, mapping row and Boundaries bullets), and the four doc gaps of the review (H-L2-1 to H-L2-4) are closed there. Two spots are still out of step, neither new to the rules but both a person should accept: (1) `core/components/skills/link-model-part/SKILL.md` lines 49-50 still say "Nothing is written when the script exits 2", which the R-2 fix made incomplete, because exit 2 can now mean some files are not back (the script header says so; the skill doc does not); (2) `core/components/memory/standards/rules/direct-model-write.md` lines 54-55 say the script writes "the spine entry of a part found during work, and the thin mark", which leaves out the three new updates (this was seen at the last self-review and is unchanged). `docs/components/` has no entry for this skill.
- [PASS] **Nothing obviously broken**: no TODO or known-failing path in the added lines. Both suites are green. The component lint, run from the repo root, reports 36 errors and 1 warning on the branch; run with the same tool on main's copy of `core/components` it reports the same 37 findings (0 new, none in `link-model-part` or `product-os-keeper`). A trial merge into main exits 0.

## Skill Rule Checks (assess-pr ruleset)

Must-have:

- [PASS] `no-conflicts`: `git merge-tree --write-tree main HEAD` exits 0.
- [PASS] `no-secrets`: see the Quality Checks line.
- [PASS] `skill-frontmatter`: `SKILL.md` has name, description, user-invocable and allowed-tools.
- [PASS] `skill-io`: `SKILL.md` has `## Input` and `## Output`.
- [PASS] `agent-frontmatter`: `product-os-keeper.md` has name, domain, role, description, model and tools.
- [PASS] `agent-boundaries`: `product-os-keeper.md` has `## Boundaries`.
- [PASS] `config-valid`: all 14 YAML records and all 14 JSON records parse.
- [PASS] `feat-documented`: the feature is documented in `SKILL.md` and the agent's skill table and mapping rows.
- [REVIEW] `deploy-components`: the installed copies of the script, the skill doc and the agent under `.claude/` differ from the source. The install is the `install-garura` play, a separate step after merge; the installed copies are not tracked by git.

Nice-to-have:

- [PASS] `agent-naming`: `product-os-keeper` follows `{domain}-{role}`.
- [REVIEW] `skill-constraints`: `SKILL.md` has no `## Constraints` heading; its rules sit under `## Rules`. Unchanged by this change.
- [REVIEW] `feat-adr`: the fix commit added a third exception to the agent's "Remove a node, or lose what an existing node holds" boundary (`link-model-part` deletes a page and its ice.md, only when it moves them word for word). No decision record names that exception. A person decides whether a boundary exception of this size needs one; the write boundary itself (only inside the product model) is unchanged.
- [PASS] `config-documented`: not applicable; the YAML files are run records, not configuration.

## Findings

**Blocking count**: 2 (1 known, 1 new)

- Commits are clean, known (commit 339ddf54): the subject is 156 characters against the 72 limit. The product owner raised past this on 2026-11-11; the record is `.garura/project/issues/1037/context/raise-past-check.md`. It stays in history unless the branch is rewritten and force pushed.
- Commits are clean, new (commit 6de7f7c6): the subject is 82 characters against the 72 limit. This is not covered by the product owner's recorded choice. It is a message-only defect on a commit already on origin; the way out is rewording it (with a force push, which rewrites the hashes of every commit above it) or a person accepting it as the first was.

**Observations** (nothing here blocks the raise):

- The fix is verified. R-1: a request with two moves into one folder is now refused ("never share a folder") and the tree is left unchanged; the new test fails without the check. R-2: the undo now runs every step on its own, and when one fails the error names every path that is not back and the run exits 2 with a message that says so. R-3: four new tests cover the delete, folder-removal and undo path.
- The line in the undo that re-makes a removed folder is not pinned by any test: with it removed in a scratch copy all tests still passed. It does no harm, because writing a file back already makes its folder.
- Open and not touched by this commit, as the review record lists them: R-4 to R-12 (P3 and P4 findings on link checking inside a moved page, link forms, function size, the Thin line scan, the `thin` type check, test gaps and a few edge cases) and H-L2-5 to H-L2-9 (P4 doc points). The reviewer's decision names them as open.

## Readiness Assessment

- **Ready**: no
- **Blocking count**: 2 (1 known and raised past by the product owner, 1 new)
- **Review required**: 4 (`Docs in step`, `deploy-components`, `skill-constraints`, `feat-adr`)
- **Recommendation**: Fix first: reword commit 6de7f7c6, or have a person accept it as the 156-character one was. Everything else is clean.

---

## YAML Output

```yaml
analysis:
  branch: feature/1037-index-tool-thin-and-moves
  base: main
  branch_pattern: feature
  commits: 12
  changes: {files: 57, additions: 7275, deletions: 26}
  suggested_title: "feat(skills): clear a thin mark and move a feature or a page (#1037)"
  context:
    commit_types: [{type: feat, count: 1}, {type: fix, count: 1}, {type: test, count: 1}, {type: chore, count: 9}]
  checklist:
    scope:
      - {id: matches-the-issue, status: "PASS"}
      - {id: no-scope-creep, status: "PASS"}
      - {id: reasonable-size, status: "PASS"}
      - {id: no-stray-artifacts, status: "PASS"}
    quality:
      - {id: tests-present, status: "PASS", evidence: "acceptance 30 of 30; unit 48 of 48"}
      - {id: commits-clean-known, status: "FAIL", evidence: "339ddf54 subject is 156 characters, limit 72 (subject-length); raised past by the product owner, see raise-past-check.md"}
      - {id: commits-clean-new, status: "FAIL", evidence: "6de7f7c6 subject is 82 characters, limit 72 (subject-length); not covered by the recorded choice"}
      - {id: conventional-format, status: "PASS"}
      - {id: no-secrets, status: "PASS"}
      - {id: docs-in-step, status: "REVIEW", evidence: "SKILL.md lines 49-50 and direct-model-write.md lines 54-55 are out of step"}
      - {id: nothing-obviously-broken, status: "PASS", evidence: "lint identical to main; trial merge clean; both suites green"}
    must_have_rules:
      - {id: deploy-components, status: "REVIEW", evidence: "installed copies differ from source; deployed by install-garura after merge"}
    nice_to_have_rules:
      - {id: skill-constraints, status: "REVIEW", evidence: "rules sit under ## Rules; unchanged by this change"}
      - {id: feat-adr, status: "REVIEW", evidence: "a third exception to a NEVER boundary was added with no decision record"}
  blocking_issues:
    - item: commits-clean
      commit: 339ddf54
      known: true
      reason: "subject is 156 characters, limit 72; raised past by the product owner"
      trigger: "commit rules, subject-length (must-have)"
    - item: commits-clean
      commit: 6de7f7c6
      known: false
      reason: "subject is 82 characters, limit 72; not covered by the product owner's recorded choice"
      trigger: "commit rules, subject-length (must-have)"
  ready: false
  recommendation: "Fix issues first"
```
