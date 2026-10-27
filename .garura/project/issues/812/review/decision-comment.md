Reviewer verdict (human, gate on): approve

PR #814, round 1. Recommended verdict: approve (no P1; 2 P4).

Checks: test_naming_tools.py 18 passed, 0 failed; the old-name check finds 0 old names in the repo (ADR 047 is now searched and is clean). Categories: code, tests, docs (run records); none design-bearing, so no grounding ran.

Findings (P4, not blocking; filed as a follow-up chore):
- `core/tools/naming/check_old_names.py:44` — `FIRST_NEW_ADR = 46` no longer names the first searched ADR, as ADR 046 is skipped through `RENAME_ADRS`. Basis: code, confusing naming after a rule change.
- `core/tools/naming/test_naming_tools.py` — the new cases do not cover ADR 049 or the `SUPERSEDED-` prefix. Basis: tests, edge cases of the skip rule.

Next: merge-change lands this on plan/788/base.
