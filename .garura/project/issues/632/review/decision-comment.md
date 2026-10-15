**Harness verdict (gate off per gates.plays.review-change): approve**

No blocking (P1) findings. 33 in all — P2: 3, P3: 15, P4: 15 — across standards (code, tests, docs, config), harness design and memory design. Runnable checks: `lint_play` pass; tests 33 + 20 pass; ruff clean; the two `adr.py` copies identical.

The three P2s:
- **H1** — run by hand, the play's working folder and session stamp are keyed on an issue that start-change has not created yet.
- **F1** — `apply_adr.py` writes the ADR before resolving the older ADRs; a crash after the write leaves a half-applied ADR that a re-run refuses.
- **F2** — `apply_adr.py` does not check the draft is Proposed, so a draft already marked Accepted would bypass "only a person accepts".

A fix round follows before the merge; findings in `.garura/project/issues/632/review/findings.yaml`.

Refs #632
