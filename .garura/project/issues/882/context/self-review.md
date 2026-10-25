# Self-review: issue #882 (record cap-initialize in the product model)

Branch: plan/788/882-record-cap-initialize. Compared with: origin/plan/788/base (the change lands there, not on main).
Rules used: ~/.garura/core/memory/standards/rules/self-review.md (base rules, no project override; see resolved-rules.json).
This review is informational. The approve/reject decision belongs to check-change.

Blocking findings: none.

## Scope checks

- [PASS] Matches the issue. The change records the "Initialize a project for Garura" capability: its capability page, six feature pages, their spine entries, the decision that moves the security box from none to medium, and the product profile's security line.
- [PASS] No scope creep. All 230 changed files sit in the allowed set:
  - 9 model files under .garura/product/product-os/ (capability.md, six feature.md files, the spine, one decision)
  - 219 run records under .garura/project/issues/882/context/ (three discover-capabilities runs, the start-change record, memory and template copies, judge records, citations)
  - 1 ledger line in .garura/core/gate-evals.jsonl
  - 1 line in .garura/install-manifest.json (Phoenix memory version)
  - Nothing is outside .garura/. No source, plays, skills or docs changed.
- [NOTE] The gate-evals.jsonl line is a ledger line the play appends. It is a run record, not a change to installed tooling. The install-manifest line is the Phoenix memory version moving from 3161dcdfe26f to 44e1c4c4799a, one line, as the task describes.
- [NOTE] One unrelated-looking edit in _spine.yaml: the one_line of cap-718 is re-wrapped over two lines. The words are the same. It comes from the spine being written back out, not from a content change. Harmless.
- [NOTE] Size. 9,860 added lines, but most of them are run records (copies of memory files, judge verdicts, drafts from two earlier halted runs). The model change itself is 567 added lines and 1 removed, which is reviewable in one sitting. The size is justified by the three runs the issue needed.
- [PASS] No stray artifacts. No TODO, FIXME, TBD, debug prints or scratch files in the added lines. No deleted files. The earlier halted runs are kept on purpose as run records, and halt.md says why.
- [NOTE] resolved-rules.json is not yet committed (it is untracked). It is a run record for this review, so it should ride in the next commit before the push.

## Quality checks

- [PASS] Tests present. This is a model change with no code. Its checks are the play's own: the shape check and the sources check passed, and the content judge passed all seven pages (the capability and six features) on all five criteria in the last run (20261025T122929Z). The spine and the decision both load as valid YAML (12 capabilities, 30 features).
- [NOTE] The model check (lint.txt) reports missing sections on older feature pages (fn-727, fn-728, fn-673, fn-743, fn-744 and others). None of them is a page this change adds; no line names the initialize folder. These were already in the model before this change.
- [PASS] Commits are clean. The seven commits since the base use conventional format (one feat, six chore) and name #882 in the subject; there is also one merge of plan/788/base. The one feat commit carries the model change; the chore commits carry run records, the install version line and the commit-change record.
- [PASS] No secrets. A scan of the added lines for keys, tokens, passwords and private-key headers found only ordinary words (card tokenisation, token-burn, password reset in feature text).
- [PASS] Docs in step. The capability page and the feature pages are the docs for this change. The spine entries point to each page, and the capability names its sources (#862, #881, #883).
- [PASS] Nothing obviously broken. The decision dec-cap-initialize-security-none-medium is listed on cap-initialize and matches the profile's new security level (medium).

## Public-repo checks (added lines of git diff origin/plan/788/base...HEAD)

- [PASS] No /Users/ home paths in any added line.
- [PASS] No claude-503 in any added line.
- [PASS] No real person names in the added lines. A search for the owner's name, surname and employer found nothing. Personas appear as roles (product owner), not names. Mentions of ~/.garura and ~/.phoenix are tilde paths in prose, not a home path of a person.
- [PASS] No Claude attribution line in any commit message.
- [NOTE] The commit author email is in commit metadata, not in the added lines. It is outside what this review was asked to check.
