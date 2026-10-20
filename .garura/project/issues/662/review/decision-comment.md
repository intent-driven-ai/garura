Harness verdict (gate off per gates.plays.review-change): approve — round 1

No blocking finding. Three Major findings (P2) will be fixed on the branch before the merge, with a round 2:
- **M2** — the gate ledger path's `{issue}` is not filled in by every play (`/run` and `/quality` pass the config value as it is), so a line could land in a folder named `{issue}`.
- **TC-1** — the contract's `decided_in: session` was added to v5 in place as 5.1.0, with no minor-version rule and no record of 5.1.0.
- **H-1** — `/intent`'s new shared contract checker is not named in its ICE source, so a rebuild would drop it.

The rest (17 P3, 11 P4) are in `.garura/project/issues/662/review/findings.yaml`; the cheap P3s are fixed in the same pass.

Checks: every test suite passes; `lint_play` passes on `/intent`, `/vision` and `/understand`; `lint-components` gives the same findings as on main; `ruff check` passes; no memory path is left in the scope.
