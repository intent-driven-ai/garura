Reviewer verdict (human, gate on): reject — fix all findings in this PR, then raise again

PR #834, round 1. Recommended verdict: approve (no P1).

The product owner's decision: the install does not move an existing model. The upgrade strategy for people on an older Garura or an older product model is parked as its own business intent (no ADR now).

To fix in this PR:
- The install (`install.py`, `installer/install.sh`) no longer runs the model migration.
- `migrate_model.py` stays as a script a person runs by hand. It refuses a model path outside the project, and on a failed git step it undoes its moves and reports why (P2, P3).
- The guard message names `migrate_model.py`, not a re-install.
- `check_kept.py` and `check_sources.py` get the guard (P4).
- ADR 050 says "amends" for ADR 035, the same word ADR 035 and ADR 017 use (P4).
