# Self-review — #613 (planned partial landing)

Run on branch `feature/613-the-kickoff-drive` against `origin/main` (9 commits, 25 files). Driven by `/Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md` (base file, no project override), plus the analyze-pr quality rules for a prompting project. This review is informational. Under the rules file it never blocks the raise; `review-change` owns approve and reject.

## In plain words

This change lands the decisions made so far on the Kickoff drive, before the memory work starts from main. It adds one accepted decision record (ADR 034: inside a drive, a play answers from memory and asks only when memory holds nothing), a pointer to it from ADR 029, the plans for #613 and #606, the memory review, and a draft plan for the memory system. It changes no code, no plays, no skills and no agents.

The change fits that description. Nothing rides along, no secrets were found, there are no merge conflicts, and every commit is conventional and names #613. Nothing blocks the raise.

There are 7 non-blocking notes. The two that matter most: the live drive rules still carry the old wording until the follow-up work lands, and ADR 034 points at plan item numbers that have since moved.

Blocking: 0. Non-blocking: 7.

## Branch info

- Branch: `feature/613-the-kickoff-drive` (pattern: feature, standard priorities)
- Base: `origin/main` (merge base is `origin/main` itself; branch is 9 ahead, 0 behind)
- Commits: 9. Files: 25. Lines: +1,322 / -12
- Suggested PR title: `docs(adr): ADR 034, inside a drive a play answers from memory; plans and memory review for #613`
- The PR must say it refers to #613 and must not close it. The diff contains no "closes", "fixes" or "resolves" wording (scan returned nothing).

## Scope checks

| Check | Status | Evidence |
|-------|--------|----------|
| Matches the issue | PASS | Files fall into the groups the scope names and nothing else: ADR 034 + ADR 029 pointer + index row (3 files under `docs/adr/`), the #613 and #606 plans, the memory review and draft memory plan (`.garura/project/issues/613/specs/`), the `/adr` run records (`.garura/project/issues/_adr/20261018-071440/`, 11 files), and play run records (`.garura/project/issues/613/context/`, 7 files). `git diff --name-only` shows no path under `core/`, `.claude/` or any play, skill or agent. |
| No scope creep | PASS, see note 5 | Every file maps to the planned partial landing. The one stretch is the draft memory system plan, which belongs to a feature that has no issue yet (note 5). |
| Reasonable size | REVIEW, see note 4 | 25 files, +1,322 lines. Count: `docs/adr/` adds 114 + 1 + 1 = 116 lines; the other 1,322 - 116 = 1,206 lines (91%) are plans and run records under `.garura/project/`. The reviewable decision is the 116 lines in `docs/adr/`. Size must be justified in the PR description. |
| No stray artifacts | PASS | No TODO, FIXME, XXX, HACK, debug print or commented-out block in added lines (scan returned nothing). The `_adr/` and `context/` files are run records the scope names as in scope. Note: the working tree holds one untracked file, `.garura/project/issues/613/context/resolved-rules.json`, plus this file once written. Both are this play's own outputs, not accidents; `commit-change` recorded `tree_clean: true` before this play ran. |

## Quality checks

| Check | Status | Evidence |
|-------|--------|----------|
| Tests present | PASS (none needed) | No behavior change: docs, plans and run records only. Rule `tests-pass` is disabled for this project (no automated tests in prompting projects). |
| Commits are clean | PASS with note 3 | All 9 subjects are conventional (`chore(stm)` x8, `docs(adr)` x1) and all end with `(#613)`. Each commit is one concern (checked per commit with `git show --stat`). Three subjects run past 72 characters (note 3). |
| No secrets | PASS | Pattern scan of every added line for cloud keys, private-key headers, GitHub and Slack tokens, `sk-` keys, bearer and JWT strings, and `password`, `secret`, `token`, `api_key` assignments: no hits. One local absolute path is present (note 7); it is not a credential. |
| Docs in step | REVIEW, see note 1 | The ADR index row and the ADR 029 forward pointer are in. The live rules ADR 034 says it changes are not yet rewritten (note 1). |
| Nothing obviously broken | PASS with notes 1, 2, 6 | All 12 JSON and YAML files parse; front matter in the three plans parses. Every path cited in ADR 034 exists on `origin/main`. Paths cited in the plans resolve (the ones that did not match are short forms, such as `standards/rules/...`, and the git-ignored `.garura/core/memory/` that the review describes). No known-failing path is introduced. |

## Project rules (analyze-pr quality rules)

| Rule | Priority | Trigger | Status | Evidence |
|------|----------|---------|--------|----------|
| `no-conflicts` | must-have | always | PASS | `git merge-tree --write-tree origin/main HEAD` exit 0, clean tree `d3d0d2254eef78b6545a013038968ed5ec0ee9ff` |
| `no-secrets` | must-have | always | PASS | pattern scan, no hits |
| `adr-structure` | must-have | `docs/adr/*.md` | PASS | ADR 034 has Status, Context, Decision, Consequences (plus Alternatives, Work This Creates, References) |
| `adr-status` | must-have | `docs/adr/*.md` | PASS | `Status: Accepted`, `Decided by: Kapil Viren Ahuja`, 2026-10-18. Acceptance is on record in commit e3b10ca1 ("approved") and in the dispatch scope. The `/adr` lint recorded `valid: true, problems: []` before acceptance (`adr-check.json`); the accepted file differs from the draft only in the Status and Decided-by lines. |
| `config-valid` | must-have | `*.yaml` | PASS | 4 YAML files parse (`analysis.yaml`, `commits.yaml`, `adr-context.yaml`, `decision.yaml`) |
| `adr-numbered` | nice-to-have | `docs/adr/*.md` | PASS | `034-...md`; follows 033, no clash on `origin/main` |
| `docs-only` | nice-to-have | commit type `docs:` | PASS | The `docs(adr)` commit adds no code. It carries JSON, YAML and text run records alongside the Markdown; none is functional. |
| `config-documented` | nice-to-have | `*.yaml` | PASS | The YAML files are run records, not configuration |

Not triggered: agent, skill and play rules (no such file changed), `docs-consistent` (no philosophy, components, README or CLAUDE.md change), `deploy-components` (nothing under `core/components/` changed), `feat-*` and `refactor-*` (no such commit type).

## Findings (all non-blocking)

1. **Live rules still carry the old wording.** ADR 034 is Accepted and says rule 4 of the drive contract, the rules index row and the glossary Drive entry change. On this branch they still read the old way: `core/components/memory/standards/rules/drive-contract.md:64` ("still stops the play"), `core/components/memory/standards/rules/_index.md:43` ("stop on a new question"), `core/grounding/glossary.md:17` ("stops only to ask a question that comes up mid-run"). The three plays are also unchanged. This is the planned gap: ADR 034 lists it under "Work This Creates", and #613 plan items 4 to 9 carry it. The PR description should say so, so main is not read as already following the new rule.
2. **ADR 034 cites plan items by their old numbers.** The #613 plan log (2026-10-18, "Item 1 done") says ADR 034's "item 2" now means item 3 and its "item 3" now means item 4, because the memory review became item 2. The ADR text was not updated: `docs/adr/034-plays-answer-from-memory-inside-a-drive.md` lines 38, 88, 103, 104 and 105. The plan log carries the mapping, so the trail is not lost, but a reader of the ADR alone is pointed to the wrong items.
3. **Three commit subjects are over 72 characters.** `commits.md` sets 72 as the limit (`subject-length`). Lengths: `27d9e035` is 78, `85c6d3fa` is 81, `e3b10ca1` is 112. The self-review rules file only asks for conventional format, one concern and an issue reference, which all 9 meet, so this is a note. The commits are unpushed; rewording needs an explicit ask.
4. **Size and issue link need to be stated in the PR description.** 25 files and +1,322 lines is large, but 91% is plans and run records; say that, and say it is Kapil's chosen partial landing of 2026-10-18. The PR must refer to #613 and leave it open.
5. **The draft memory system plan sits in #613's folder.** `.garura/project/issues/613/specs/memory-system-plan.md` (270 lines) describes a separate feature that no issue holds yet. It is in scope by the dispatch, and the plan and commit messages say why it is here. Once the memory feature is filed, it should move to that feature's own folder.
6. **One line in the #606 plan is older than ADR 034.** `.garura/project/issues/606/specs/plan.md` line 84 (item 8, "What") still says the drive "stops only for a new question". ADR 034 narrows that to a question nothing in memory supports. The new "Order inside this item" lines below it are correct.
7. **A local path is committed.** `.garura/project/issues/613/context/plan-check.json:15` holds `/Users/kapilahuja/cto/builder/garura/...`. It is not a secret, and run records on `origin/main` already hold such paths (for example `.garura/project/issues/241/review/pr.diff`). Noted only.

## Blocking issues

None. The rules file states this review does not block the raise.

## Readiness

- Ready: yes
- Blocking count: 0
- Non-blocking count: 7
- Review required (rows marked REVIEW): 2 (size, docs in step), both settled by wording in the PR description
- Recommendation: raise the PR

---

## YAML output

```yaml
analysis:
  branch: feature/613-the-kickoff-drive
  base: origin/main
  branch_pattern: feature
  commits: 9
  changes:
    files: 25
    additions: 1322
    deletions: 12
  suggested_title: "docs(adr): ADR 034, inside a drive a play answers from memory; plans and memory review for #613"
  rules_file: /Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md
  rules_file_is_override: false
  context:
    file_patterns_matched:
      - { name: adr, files: 3, trigger: "docs/adr/*.md" }
      - { name: yaml, files: 4, trigger: "*.yaml" }
      - { name: stm_plans_and_records, files: 22, trigger: ".garura/project/issues/**" }
    commit_types:
      - { type: chore, count: 8 }
      - { type: docs, count: 1 }
    branch_modifiers: []
  checklist:
    scope:
      - { item: matches_the_issue, status: PASS }
      - { item: no_scope_creep, status: PASS, note: "finding 5" }
      - { item: reasonable_size, status: REVIEW, note: "finding 4" }
      - { item: no_stray_artifacts, status: PASS }
    quality:
      - { item: tests_present, status: PASS, note: "none needed, no behavior change" }
      - { item: commits_are_clean, status: PASS, note: "finding 3" }
      - { item: no_secrets, status: PASS }
      - { item: docs_in_step, status: REVIEW, note: "finding 1" }
      - { item: nothing_obviously_broken, status: PASS, note: "findings 1, 2, 6" }
    must_have:
      - { id: no-conflicts, status: PASS }
      - { id: no-secrets, status: PASS }
      - { id: adr-structure, status: PASS }
      - { id: adr-status, status: PASS }
      - { id: config-valid, status: PASS }
    nice_to_have:
      - { id: adr-numbered, status: PASS }
      - { id: docs-only, status: PASS }
      - { id: config-documented, status: PASS }
  findings:
    blocking: []
    non_blocking:
      - { n: 1, summary: "live drive rules and plays still carry the old wording until the follow-up lands (planned)" }
      - { n: 2, summary: "ADR 034 cites plan items by their old numbers (lines 38, 88, 103, 104, 105)" }
      - { n: 3, summary: "3 of 9 commit subjects exceed 72 characters (27d9e035, 85c6d3fa, e3b10ca1)" }
      - { n: 4, summary: "PR description must justify size and refer to #613 without closing it" }
      - { n: 5, summary: "draft memory system plan sits in #613's folder for a feature with no issue yet" }
      - { n: 6, summary: "606 plan item 8 'What' line says 'stops only for a new question', older than ADR 034" }
      - { n: 7, summary: "plan-check.json commits a local absolute path (precedent on main); not a secret" }
  blocking_issues: []
  blocking_count: 0
  non_blocking_count: 7
  ready: true
  recommendation: "Create PR"
```
