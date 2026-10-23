Reviewer verdict (human, gate on): approve

PR #834, round 2. Recommended verdict: approve (no P1, P2 or P3).

Round 1 fixes are in: the install never changes an existing product model; `migrate_model.py` is a script a person runs by hand, refuses paths outside the project, and undoes its moves on a failed step; the guard names `migrate_model.py` and also stops on old page file names; `check_kept` and `check_sources` are guarded; ADR 050 says "amends". Hidden eval: 58 passed, 0 failed.

Parked: the upgrade strategy (#835). Later: other deprecated parts (#833), the 30 asking-a-person pointers (#831).
