# Self-Review — #536 (feature/536-review-stop-condition vs main)

Rules source: /Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md (base file, not a project override).
Diff: `git diff main...HEAD` — 5 commits, 13 files, +378 / -31.
Informational only. The approve/reject gate is review-change's job.

## Branch Info

- Branch: feature/536-review-stop-condition
- Base: main
- Branch pattern: feature
- Suggested PR title: `fix(review-change): prove a decision was recorded with its decider before the review is called done (#536)`

## Scope checks

| Check | Status | Evidence |
|-------|--------|----------|
| Matches the issue | PASS | Issue #536: review-change's Done means named `review/verdict.yaml`, which the play never writes. The diff changes that clause (D2) to read `decision_recorded` in `review/posted.json`, and makes `post_verdict.py` write that field only after reading a valid `decision.yaml`. |
| No scope creep | PASS | Play files all sit in review-change (ice.md, SKILL.md, stop-condition.yaml, scripts/post_verdict.py) plus its play-creator reference copy and test. The one outside file, fix-bug SKILL.md, is the sweep finding the issue's last criterion calls for (fix-bug D3 reads a file the prose never said to write). fix-bug D4 is written by the injected merge-change sub-play, so it is correctly left alone. |
| Reasonable size | PASS | 7 source files carry the change (about 75 lines of play edits, 49 lines of script, 155 lines of test). The other 6 files are STM run records under `.garura/project/issues/536/context/`. |
| No stray artifacts | PASS | No debug prints in play code (the prints in the test are its report output). No TODO or FIXME added. No `__pycache__` tracked (0 tracked). Untracked `resolved-rules.json` is this run's own input, not part of the diff. |
| Intent change went through the ICE | PASS | `reference/ice.md` was edited, and the SKILL.md fingerprint `sha256:91ef6311...c255ed` matches the current hash of ice.md. The fix-bug edit is non-intent prose (it names a file), so a direct edit is the correct path. |

## Quality checks

| Check | Status | Evidence |
|-------|--------|----------|
| Tests present | PASS | New `test_post_verdict.py`: 23 passed, 0 failed (run now). Covers a posted harness decision and a posted human decision (stop condition holds), a failed post (no posted.json, stop condition unmet), six invalid-decision cases (nothing posted, exit 2), a hand-made `verdict.yaml` (still unmet), and the two script copies being identical. |
| Commits are clean | PASS | 5 commits, all conventional format, all reference #536. The fix, the fix-bug doc edit and the STM records are separate concerns. |
| No secrets | PASS | Added lines scanned for key, token, secret, password, private-key and cloud-key patterns: no matches. |
| Docs in step | PASS | SKILL.md (Step 6 and SE-9), ice.md (C9, D2) and the script docstring all describe the new behaviour. No leftover `verdict.yaml` reference except the test that proves it no longer passes. |
| Nothing obviously broken | PASS | No merge conflicts (`git merge-tree --write-tree main HEAD` returned a tree hash). `stop-condition.yaml` parses. The two copies of `post_verdict.py` are byte-identical. |

## Points for the reviewer (non-blocking)

- REVIEW: The "closes COMPLETED" proof is a fixture test with the host and git stubbed. No live `/review-change` run on a real PR was done in this branch.
- REVIEW: The issue asks that the sweep of the other plays' stop-condition.yaml be done. 28 manifests exist; the sweep result (one drift found, in fix-bug D3) is not recorded in a file in this diff. Worth stating the sweep outcome in the PR description.
- REVIEW: `decision_recorded: true` is trusted if someone hand-writes `posted.json`. The script is the only intended writer, and a hand-made verdict file is covered by a test, but a hand-made posted.json is not.
- REVIEW: `post_verdict.py` now needs a new `--decision` argument. The only caller found is review-change's SKILL.md Step 6, which was updated.

## Blocking Issues

None. Blocking findings: 0.

## Readiness Assessment

- Ready: yes
- Blocking findings: 0
- Review items: 4
- Recommendation: Raise the PR.

---

## YAML Output

```yaml
analysis:
  branch: feature/536-review-stop-condition
  base: main
  branch_pattern: feature
  commits: 5
  changes: {files: 13, additions: 378, deletions: 31}
  suggested_title: "fix(review-change): prove a decision was recorded with its decider before the review is called done (#536)"
  rules_file: /Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md
  checklist:
    scope: {matches_issue: PASS, no_scope_creep: PASS, reasonable_size: PASS, no_stray_artifacts: PASS}
    quality: {tests_present: PASS, commits_clean: PASS, no_secrets: PASS, docs_in_step: PASS, nothing_broken: PASS}
  blocking_issues: []
  blocking_count: 0
  ready: true
  recommendation: "Raise the PR"
```
