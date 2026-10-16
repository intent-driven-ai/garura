**Harness verdict (gate off per gates.plays.review-change): approve**

No blocking (P1) findings. 23 in all, from 6 categories: the /vision play and the rule files were design-checked against main's committed rules (ADR 029, ADR 031, gate-config.md, pipeline-position.md, /intent's in-drive path), and the scripts and tests by the standards linter, with every suite re-run. 17 are fixed in this PR, including all 3 P2s. 6 stay open; none blocks.

Fixed in this PR:
- **P2**: the learner reset a run of approvals when a later line answered a "deferred to the drive's review" line. Fixed: the deferred line is skipped first, answered or not (`dce14390`).
- **P2**: /vision's own failure rule still called a commit before approval a failure, which the drive path now does on a recorded deferral. Fixed in the intent file and recompiled (`92e588b5`).
- **P2**: the drive rule did not say what a pinned checkpoint does inside a drive. Fixed: a pinned checkpoint is never deferred by a contract; it is asked up front or it stops the play, unless the play's own intent names the exception (`e8cfab0c`).
- **P3/P4**: inside a drive, a config skip or a policy auto-pass is now recorded as by hand, and only a would-wait gate is deferred; the contract checker and review writer reject bad values and never leave a half record; 12 more test cases; the learning-script copies are now checked to stay identical; the rule names its Checkpoint Decisions row, says the play's own commit still runs, and is linked from the index and the two rules it touches (`dce14390`, `3893bc30`, `92e588b5`, `e8cfab0c`).

Open, not blocking:
- **P3**: /vision's done checks cannot tell a drive run from a run by hand; the drive behaviour is proven by step evals only.
- **P3**: the rule does not say where a play lists its up-front questions, or what a question id is. That belongs to the Kickoff drive's design (#613).
- **P3**: play-creator and the component linter do not yet emit or check the drive skips; only /vision's play carries them.
- **P4**: /vision reads the contract's answers but no step uses them yet; the "wired so far" list in pipeline-position.md; the PR body and self-review were written before the fixes.

Checks run: all 21 test files under `core/` pass (`test_drive_contract.py` 26, `test_gate_learning.py` learner 11/11 and copies identical). `lint_play` passes on /vision and its fingerprint matches its intent file. ruff is clean on the changed scripts. Every shared-script copy is byte-identical.
