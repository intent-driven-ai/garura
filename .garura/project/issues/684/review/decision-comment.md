Harness verdict (gate off per gates.plays.review-change): approve

No P1 finding, so the computed recommendation is approve (`compute_verdict.py`). One kind of work: old run records under `.garura/project/issues/`. No design-bearing category.

**Checks run:** every changed JSON and YAML file still parses; no file on the branch holds a local temp-folder or home-folder path. The 8 lines in #498, #500, #614 and #632 now read `<scratchpad>`, and nothing else in those records changed.

**Open (P4):** the review shelf has no playbook for run records, so they get only these objective checks — already known from PR #682.

Full record: `.garura/project/issues/684/review/findings.yaml`.
