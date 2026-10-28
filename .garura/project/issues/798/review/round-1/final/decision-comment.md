**Reviewer verdict (human): reject** — fix the P2 and P3 findings, then re-raise.

The recommended verdict was approve (no P1, every test suite green, no linter problem in a changed file). The product owner asked for the 2 P2 and 21 P3 findings to be fixed first.

- P2: an unused variable in `core/components/plays/shape-eval/scripts/test_shape_eval_scripts.py:334` (ruff F841).
- P2: the eval drafts and a full copy of the hidden file stay in the change's short-term memory, beside where the stories are built.
- P3 (21): text left behind on the spine, fn-818, fn-898 and bi-788; the eval's scenarios that check less than they say; two recoveries in the hidden file; the play's shared-slice case and summary opening; the agents doc; the eval templates' rules section, the step library's validation block.

The full list, each with its committed source: `.garura/project/issues/798/review/round-1/findings.yaml`.
