# Self-Review: #1037 (the model's index tool clears a thin mark, moves a feature to another capability, and moves a part's page)

Driven by the base self-review rules (no project override), the assess-pr quality ruleset and the
commit rules. This checklist is informational; the approve or reject gate is `review-change`.
Each line carries one status: PASS, REVIEW (a person signs off) or FAIL (a must-have rule is broken).

## Branch Info

- **Branch**: `feature/1037-index-tool-thin-and-moves` (pattern: feature, standard priorities)
- **Base**: `main` (the branch sits on main's tip; main equals origin/main; a trial merge is clean)

## Change Summary

- **Commits**: 5
- **Files changed**: 16 (+910 / -20)
- **Source part**: 4 files under `core/components` (+271 / -20), the 322-line acceptance check, and 11 run records (+317)

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
| YAML and JSON run records | 7 |
| Markdown and text run records | 4 |

| Commit type | Count | Subject |
|-------------|-------|---------|
| feat | 1 | clear a thin mark and move a feature or a page |
| test | 1 | the acceptance check, failing before the build |
| chore | 3 | stm run records |

## Scope Checks

- [PASS] **Matches the issue**: the change adds the three updates the issue names to the index script of `link-model-part` (`thin: false`, `capability: <id>`, `doc: <new path>`), with the skill doc, the agent's skill-table row, unit tests and the acceptance check. The one adjacent edit, the domain refusal that now also covers `thin: false`, belongs to the same feature and is covered by acceptance scenario E4.
- [PASS] **No scope creep**: all 16 files sit in the issue's own folders (4 under `core/components`, the acceptance check, 11 records under `.garura/project/issues/1037/context/`). The two untracked paths in the tree (`context/memory/`, `context/resolved-rules.json`) are this raise's own records and are not in the diff.
- [PASS] **Reasonable size**: +910 / -20 over 16 files, but a reviewer reads 4 source files (+271 / -20) and one acceptance check; the other 11 files are run records.
- [PASS] **No stray artifacts**: no TODO, FIXME, debug print or commented-out block in the added source lines; no `__pycache__`, backup or scratch file in the diff. The `context/` records and template copies are what the start-change and commit-change plays commit on purpose.

## Quality Checks

- [PASS] **Tests present**: 8 new unit tests (`TakeInOldPartsTest`) plus the acceptance check, written first (commit 339ddf54). Run here: acceptance check 30 of 30 pass; skill unit tests 44 of 44 pass.
- [FAIL] **Commits are clean**: commit 339ddf54 has a subject of 156 characters; the commit rules cap it at 72 (`subject-length`, must-have). The other four subjects are 54 to 70 characters.
- [PASS] **Conventional format and issue reference**: all five commits use a valid type (`feat`, `test`, `chore`) with a scope, each names #1037, each is one concern, and none carries an attribution trailer.
- [PASS] **No secrets**: a pattern scan of the added lines found no credential. The one hit is a scan-result sentence in `context/analysis.yaml` that names the patterns it looked for. No file is over 1 MB.
- [PASS] **Docs in step**: `SKILL.md` (description, Input, Output and Rules), the script's header and the `product-os-keeper` skill-table row all name the three updates and the new report keys (`unthin`, `moved`). `docs/components/` has no entry for this skill.
- [PASS] **Nothing obviously broken**: no TODO or known-failing path in the added lines. The component lint reports 36 errors and 1 warning on the branch, identical to main (0 new, none in `link-model-part` or `product-os-keeper`).

## Skill Rule Checks (assess-pr ruleset)

Must-have:

- [PASS] `no-conflicts`: `git merge-tree --write-tree main HEAD` exits 0.
- [PASS] `no-secrets`: see the Quality Checks line.
- [PASS] `skill-frontmatter`: `SKILL.md` has name, description, user-invocable and allowed-tools.
- [PASS] `skill-io`: `SKILL.md` has `## Input` and `## Output`.
- [PASS] `agent-frontmatter`: `product-os-keeper.md` has name, domain, role, description, model and tools.
- [PASS] `agent-boundaries`: `product-os-keeper.md` has `## Boundaries`.
- [PASS] `config-valid`: both YAML records and all five JSON records parse.
- [PASS] `feat-documented`: the feature is documented in `SKILL.md` and the agent's skill table.
- [REVIEW] `deploy-components`: the installed copy of the script under `.claude/skills/link-model-part/` differs from the source. The install is the `install-garura` play, a separate step after merge; the installed copy is not tracked by git.

Nice-to-have:

- [PASS] `agent-naming`: `product-os-keeper` follows `{domain}-{role}`.
- [REVIEW] `skill-constraints`: `SKILL.md` has no `## Constraints` heading; its rules sit under `## Rules`. Unchanged by this change.
- [PASS] `feat-adr`: no ADR needed. The request schema only gains optional keys, no new writer is added, and the write boundary (only inside the product model) is unchanged.
- [PASS] `config-documented`: not applicable; the YAML files are run records, not configuration.

## Findings

**Blocking count**: 1

- Commits are clean (commit 339ddf54): the subject is 156 characters against the 72 limit. It is a message-only defect on a commit that is not pushed. Rewording it rewrites the hashes of the three commits above it, which leaves the hashes written in `context/commits.yaml` stale; the other way out is a person accepting the exception. This review changed none of it.

**Observations** (nothing here blocks the raise):

- No committed test covers a move that fails part way. A scratch run forced the second file deletion to fail, then the removal of the old folder to fail; each time every file and folder came back as it was. The behaviour is right; only the test is missing.
- `core/components/memory/standards/rules/direct-model-write.md` (lines 54-55) says `link_part.py` writes "the spine entry of a part found during work, and the thin mark". It now also takes the mark off, files a feature under another capability and moves a page. The write boundary the rule states is unchanged, so the sentence is incomplete, not wrong.
- A move refuses when another page names the old path, but it does not look at links inside the moved page itself. A page whose own relative links point at its old neighbours would break after a move. No capability or feature page in the model today uses a relative link (0 of 45), so nothing breaks now.

## Readiness Assessment

- **Ready**: no
- **Blocking count**: 1
- **Review required**: 2
- **Recommendation**: Fix first: the one commit subject, or have a person accept it. Everything else is clean.

---

## YAML Output

```yaml
analysis:
  branch: feature/1037-index-tool-thin-and-moves
  base: main
  branch_pattern: feature
  commits: 5
  changes: {files: 16, additions: 910, deletions: 20}
  suggested_title: "feat(skills): clear a thin mark and move a feature or a page (#1037)"
  context:
    commit_types: [{type: feat, count: 1}, {type: test, count: 1}, {type: chore, count: 3}]
  checklist:
    scope:
      - {id: matches-the-issue, status: "PASS"}
      - {id: no-scope-creep, status: "PASS"}
      - {id: reasonable-size, status: "PASS"}
      - {id: no-stray-artifacts, status: "PASS"}
    quality:
      - {id: tests-present, status: "PASS", evidence: "acceptance 30 of 30; unit 44 of 44"}
      - {id: commits-clean, status: "FAIL", evidence: "339ddf54 subject is 156 characters, limit 72 (subject-length)"}
      - {id: conventional-format, status: "PASS"}
      - {id: no-secrets, status: "PASS"}
      - {id: docs-in-step, status: "PASS"}
      - {id: nothing-obviously-broken, status: "PASS", evidence: "lint identical to main; trial merge clean"}
    must_have_rules:
      - {id: deploy-components, status: "REVIEW", evidence: "installed copy differs from source; deployed by install-garura after merge"}
    nice_to_have_rules:
      - {id: skill-constraints, status: "REVIEW", evidence: "rules sit under ## Rules; unchanged by this change"}
  blocking_issues:
    - item: commits-clean
      reason: "commit 339ddf54 subject is 156 characters, limit 72"
      trigger: "commit rules, subject-length (must-have)"
  ready: false
  recommendation: "Fix issues first"
```
