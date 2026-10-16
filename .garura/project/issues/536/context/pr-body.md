Closes #536.

## What this fixes

`/review-change` could never close COMPLETED. Its stop condition (D2) looked for `review/verdict.yaml`, a file the play never writes. Every run closed HALTED, even when it did the whole job.

## What changed

- **D2 now proves a decision with its decider.** The post step (`post_verdict.py`) reads `review/decision.yaml` first. It posts nothing (exit 2) unless the record holds a decision (approve or reject) and its decider (harness or human). After the post, `posted.json` carries `decision`, `decided_by` and `decision_recorded: true`. D2 checks that field.
- **Intent first.** The change went through `review-change/reference/ice.md` (C9 and D2), then the compiled `SKILL.md` (Step 6, SE-9, new fingerprint) and `stop-condition.yaml`.
- **Tests.** New `play-creator/references/test_post_verdict.py` (23 pass):
  - a posted decision (harness or human) holds the stop condition, so the run closes COMPLETED;
  - a failed post leaves it unmet, so the run closes HALTED;
  - six bad decision records post nothing;
  - a hand-made `verdict.yaml` no longer passes;
  - the two copies of the script stay identical.

## The sweep (last acceptance item)

All stop conditions under `core/components/plays/` were checked. Each clause's file and field was matched, by whole name, against what its play and scripts say they write. The check finds the old D2 bug on main and finds nothing on this branch except the two fix-bug items below.

- **fix-bug D3: real drift, fixed.** The check reads `red_verified` in `regression-test-path.yaml`. The play never said that record holds the field. Step 3 now says the agent writes the test skill's output block there. This is a wording change only; fix-bug's intent and fingerprint stay the same.
- **fix-bug D4: not drift.** `review/merge-gate.json` and `pr_merged` are written by the merge-change step that fix-bug runs.
- **Values other than `true`:** the clauses in commit-change, deploy, focus, grill, implement, propose-change and start-change were each matched to the script that writes the value. All are consistent.

## Not in this change

- `lint_play` still reports one gap on review-change: the "no unbacked recommendation" wiring. That gap is on main already and is tracked by #530.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
