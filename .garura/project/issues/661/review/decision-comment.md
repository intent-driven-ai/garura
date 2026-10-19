Harness verdict (gate off per gates.plays.review-change): reject — round 1

One blocking finding (P1):
- **F1** — `write_drive_review.py` (in `/vision`, `/understand` and the `play-creator` reference copy) accepted only the memory tool's contract version "4". The tool now answers "5". A drive run of `/vision` or `/understand` that records its decisions would write nothing.

Major findings (P2), design:
- **H1 / MEM-1** — eight other plays still tell their judge to use the prompt in `standards/rules/grounding-eval.md`, which now only points to the `judge-grounding` skill (those plays move in #663; accepted by the owner).
- **H2** — `author-shape-bundle` still read its shelf through the removed knowledge router.
- **MEM-2** — Rule 12's old file is still named by deprecated skills.

The rest (P2 from the standards scan, P3, P4) are in `.garura/project/issues/661/review/findings.yaml`. Many standards findings come from test files and JSON samples scanned as runtime code (see `quality-findings.yaml`, coverage notes).

Checks: every test suite passes; `lint-components` gives the same findings as on main; the play checker passes on the changed plays.

Next: fix the cited findings on the branch and review again (round 2).
