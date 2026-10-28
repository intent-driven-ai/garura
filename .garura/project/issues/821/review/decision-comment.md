Reviewer verdict (human, gate on): approve

PR #832, round 2. The recommended verdict was reject, only because of SEC-07 (`JSON.parse` of the linter's own output in a test). That is a false positive.

Round 1 fixes are in: HA1 (the edit-ontology ICE carries the asking-a-person flow and the play is recompiled), HB2 (the check reads only the play's steps and counts the pointer only there), HC1 (one main copy of `lint_grounding.py` and a drift check), MC1 (no Tether / Orbit / Vanish outside the ADRs). Hidden eval: 43 passed, 0 failed.

Deferred: HB1 (30 plays still lack the pointer) → #831.
