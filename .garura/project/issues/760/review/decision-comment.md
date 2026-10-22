Reviewer verdict (human, gate on): approve

PR #789, round 1. Recommended verdict: approve (no P1 findings; 3 P3, 11 P4).

Checks: test_check_ice_workable 41 passed; discover-intent test_intent_scripts 116 passed; both copies identical; component linter 121 errors before and after; Garura's model 30 workable before and after.

Design: the three answers match ontology v6 and ADR 047 §6/§8.

P3 findings, approved as they are:
1. Without --done, needs are not judged and a capability with an open need is answered ready, with nothing in the answer saying needs were not checked; create-play's rule does not tell plays to pass --done (two findings, harness).
2. assess_ice mixes four jobs in about 55 lines (code).

Next: merge-change into plan/756/base.
