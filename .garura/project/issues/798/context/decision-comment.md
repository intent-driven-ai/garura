**Reviewer verdict (human): approve.**

Round 6's two fixes hold: a resume keeps the start copies, and every malformed start copy tried (29) is refused cleanly before any write. One severity-3 finding of round 7 (a fresh run after a stop on the same change issue reuses the old start copies) and one severity-4 finding are kept in the review record, to fix on main. The linters, the play linter and the tests pass.

Findings with their committed sources: `.garura/project/issues/798/review/findings.yaml`.
