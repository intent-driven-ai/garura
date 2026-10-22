Reviewer verdict (human, gate on): approve

PR #784, round 1. Recommended verdict: approve (no P1 findings).

Checks: lint_play on edit-ontology PASS (0 gaps); component linter 121 errors before and after; linter tests pass; edit-ontology script tests 11 passed. No code depends on the old pipeline-position wording.

Findings (non-blocking):
- P3 pipeline-position.md: the condition "a meta play that opens and lands its own change is both" does not mark which meta plays qualify, because every both play opens and lands its own change; the reason (it changes Garura's source with the product owner) was dropped. Approved as it is.
- P4 pipeline-position.md: the /edit-ontology list entry restates the placement, not the reason.
- P4 no review playbook for short-term memory run records.

Next: merge-change into plan/756/base.
