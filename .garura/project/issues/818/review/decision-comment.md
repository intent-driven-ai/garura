**Approve** — the product owner's verdict (human), check-change round 2.

- Round 2 fixed DF-2, DF-3, DF-4 and DF-5, and most of DF-1: one-call typed create, the record after every write, and a partial record still marks the plan file. The adapter's five new verbs are in all six identical copies; the 16 old verbs are untouched; all tests pass.
- Standards scan: 0 findings on 83 paths; `ruff` clean. Lint: no new error against the base. Memory: no finding. Hidden acceptance checks: 21 / 21.
- The /shape-plan play-lint gap ("no entry in pipeline-next.md") is the entry this PR adds; the review map is the base's.
- Left for chore #874: NF-2 (an uncaught error leaves the record "ok"; a partial plan file is left uncommitted), NF-3 (round-2 evals not yet in the ICE), NF-1 (the adapter page and verb references still name 16 verbs), and the P4s. DF-6 (the ontology's label line) is its own /edit-ontology change.

Records: `.garura/project/issues/818/review/`.
