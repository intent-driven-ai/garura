# Self-review — #662 (feature/662-kickoff-runs-from-memory-alone, 9 commits on main)

Rules used: `~/.phoenix/core/memory/standards/rules/self-review.md` (the base file, not a project override; recorded in `resolved-rules.json`).
Scope used: `.garura/project/issues/662/specs/plan.md`.

These rules make the self-review informational. It is not the approve/reject gate (that is `review-change`). So nothing below is marked blocking. Items that deserve a person's eye before the push are marked REVIEW.

## What the change is

Proof run: the three Kickoff plays (`/intent`, `/vision`, `/understand`) ran on a test shop project from memory alone. The run's records are kept as evidence. Five small faults the run found were fixed on this branch. Five more were written down for their own issues.

Size: 168 files. 126 are the run's record under `.garura/project/issues/662/evidence/run/` (a copy of the test project's short-term memory and product model). 38 are the five fixes under `core/` (about 809 lines added, 135 removed). 4 are the issue's own notes and plan.

## Scope checks

- PASS — Matches the issue. The plan's goal is to prove the three plays run from memory and to record the run. The record is in the evidence folder. The five fixes are the "small fixes" the plan allows (item 7). Evidence: plan.md items 3 to 7; `evidence/run/findings.md` "Dispositions".
- PASS — No scope creep. Every file under `core/` traces to one of the five findings:
  - I-1: `plays/intent/SKILL.md`, `plays/intent/scripts/check_drive_contract.py`.
  - V-1: `guidance_block.py` (canonical plus the `/vision` and `/understand` copies), their SKILL.md lines, tests.
  - V-2: `core/config.yaml`, `gate-config.md`, `distill_gate_policy.py` (canonical plus 11 play copies), SKILL.md lines, tests.
  - V-3: `core/tools/memory/contract/v5.json`, its sample, README, test.
  - U-1: `core/tools/memory/citations.py`, GUIDE.md, test.
  The larger findings (I-2, V-4, U-2) were not fixed here, as the plan says.
- PASS — Reasonable size, with the reason stated. Reviewable code is the 38 core files. The 126 evidence files are a record, not code to review, and the plan names them as the deliverable. Suggest the PR description says this in one line.
- REVIEW — Stray artifacts. No scratch, debug, cache or log files are in the diff (checked for `.pyc`, `__pycache__`, `.log`, `.tmp`, `.bak`, `.DS_Store`: none; `__pycache__` on disk is gitignored). Two `print(` lines were added, in a script that prints its own report. Both are intended output. The one open point is that the evidence copy includes a personal email address, see "No secrets" below.

## Quality checks

- PASS — Tests present. Each fix carries a test, and the tests pass when run now:
  - Memory tool: 80 tests pass (`core/tools/memory/test_memory.py`). The V-3 and U-1 tests are in it. The commit says 81; the difference looks like a counting difference between runners. Not a failure.
  - Play-creator references (`test_gate_learning.py`, `test_guidance_block.py`): 13 pass. This includes the check that the two `guidance_block.py` copies match the canonical one.
  - `/intent` scripts: 103 pass. `/vision` scripts: 36 pass.
  - I did not re-run `lint_play` (the I-1 commit reports PASS).
- PASS — The 11 `distill_gate_policy.py` copies and the 2 `guidance_block.py` copies are identical to their canonical versions (compared, ignoring the stamp line). The 3 `check_drive_contract.py` copies are identical.
- PASS — Commits are clean. All 9 use conventional format (`chore(stm)`, `chore(plan)`, `chore(evidence)`, `fix(memory)`, `fix(plays)`, `fix(intent)`) and every one carries `(#662)`. The four fix commits have bodies naming the finding. Each commit is one concern.
- REVIEW — No secrets. A scan of added lines found no credentials, tokens or keys. Words like "token" and "password" appear only in memory-shelf prose about payments and login. Absolute home paths in added lines: 0. One personal item: a personal email address (the `(a personal domain)` one) appears in 2 evidence files: `evidence/run/issue-1/context/intent/20261020-095249/source-manifest-statement.json` and `evidence/run/issue-1/evidence/intent/20261020-095249/source-statement/source.md`. It is the "given by" line the `/intent` run recorded. That address appears nowhere else on main. The project's own rule is that garura's history carries no personal references, and a scan is due before every push. Suggest removing or replacing that line in the two files, then re-scanning, before the push. Not marked blocking: the rules file does not say a finding blocks. Name only ("Kapil Viren Ahuja") already appears elsewhere on main.
- REVIEW — Docs in step. The memory tool's README and GUIDE were updated for V-3 and U-1, and the plays' SKILL.md lines for I-1, V-1, V-2. One place was not updated: the repo's own tracked `.garura/core/config.yaml` (line 180) still points the gate ledger at `.garura/core/gate-evals.jsonl`, while `core/config.yaml` now points at each issue's own ledger. That file is this repo's deployed copy and is changed by the deploy step, so this may be expected. Say so in the PR, or deploy to bring it in line.
- REVIEW — Run record versus the fix. The memory-update record `mu-20261020-001` in the evidence says it was decided in `review-tool`. The run typed the approval in a session, which is the case V-3 later made legal as `session`. The record was written before the fix, so it shows the old value. It is a true record of the run as it happened; worth one line in the PR so a reader is not confused.
- PASS — Nothing obviously broken. No TODO, FIXME or leftover placeholder added in `core/`. The five fixes close their findings. The still-open findings (I-2, V-4, U-2, I-3, U-4) are written down in `findings.md`, not hidden, and none stops this change's own goal.

## Still to do (from the plan, not a defect)

Item 8, land: mark the Kickoff milestone passed in the #653 plan, and close this plan and item 9 of the #653 plan in the last commit before the merge. The plan's "now" is already 8.

## Blocking issues

None. The rules file does not mark any check as blocking.

## Summary

Ready to raise, with one clean-up suggested first: the personal email in two evidence files. Two notes for the PR text: the size is mostly the run's record, and the repo's own `.garura/core/config.yaml` still shows the old ledger path.
