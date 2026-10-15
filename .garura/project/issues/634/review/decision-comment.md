**Harness verdict (gate off per gates.plays.review-change): approve**

No blocking (P1) findings. 2 in all, both fixed in this PR before the merge:
- **P3** — with the lens contracts in, every `lint_grounding.py` copy reported a valid lens doc as an "orphan grounding doc" when run with `--spine` (the spine never points at lens docs; they belong to their slice). Bringing `/understand`'s copy level would have spread that to `/understand`. Fixed in all 12 copies: a lens doc is an orphan only when its slice is not in the spine.
- **P4** — no test covered the lens contracts or the exact-title branch. New `plays/vision/scripts/test_lint_grounding.py`: the orphan check, every lens template's gold example, and all 12 copies identical (12 checks).

Checks: ruff E741 clean on all 69 copies; each script's copies identical; all 16 test suites pass.

Note: review-change's stop condition still checks `review/verdict.yaml`, which the play never writes — that is #536. No `verdict.yaml` was made by hand, so this review closes HALTED on that one clause.

Refs #634
