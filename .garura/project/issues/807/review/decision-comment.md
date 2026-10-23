Reviewer verdict (human, gate on): approve

PR #810, round 1. Recommended verdict: approve (no P1; 2 P3, 15 P4).

Checks: hidden eval 45 of 45 (22 of 45 failed before the build); old-name check 0 hits; all test suites pass; lint_play and the component linter show no new error; every changed play's fingerprint matches its ICE; the play changes are wording only; Garura's 21 features moved whole; the epics list stays (decision 1a).

Note: check-change's context and diff were built locally with git, because the host refuses a diff of more than 300 files (#811).

P3 findings, filed and approved as they are here:
- The old-name check's ADR cut-off now also skips ADR 047 → #812.
- Projects that installed Garura before this change keep the old model names, which the scripts now read as empty → #813.

Next: merge-change into plan/788/base.
