# Self-review: issue 844

Rules used: the resolved self-review rules file (base copy).
Diff: origin/plan/788/base...HEAD (6 commits, 72 files).

What the whole change does: runs /shape-slice for business intent 788. It adds the slice sl-intent-to-design with its record, a new domain, two new capabilities, a filled capability cap-718, three features with thin ICE, the confirmed intent page bi-788, the slice's hidden file under the plan's evals folder, and the run's records under the issue's folder.

## Scope checks

- [PASS] Matches the issue. Every added file is a model page for this slice, the slice's hidden file, or a run record under the issue folder. Commits name issue 844.
- [PASS] No scope creep. No source code, play or script is touched.
- [REVIEW] Size. 72 files and about 5,960 added lines, but almost all are run records and the copied memory under the issue folder. The model delta is 11 files. Read the spine, the slice page and the three features first.
- [REVIEW] The hidden file (plans/788/evals/intent-to-design/failure-and-recovery.md) is written by this run although the current play does not yet allow it (decisions.md items 6 and 7). The play fix follows. A reviewer should confirm the order.
- [PASS] No stray artifacts. No debug prints, TODO marks or commented-out blocks in the added lines.

## Quality checks

- [PASS] Tests present. No behavior code changed. The model checks for this slice pass.
- [REVIEW] Known and accepted: 70 older model-check problems in other plans' pages (decisions.md item 8). They are not caused by this change.
- [PASS] Commits are clean. All 6 use conventional format, one concern each, and name issue 844.
- [PASS] No secrets. A scan of the added lines for keys, tokens, passwords and private keys found nothing.
- [PASS] Docs in step. The intent page, capabilities, features and slice page were written together.
- [PASS] Local paths and names. The model-check baseline (shape-slice/lint-before-run.json) held a local scratch path with the machine user name in 70 lines. Fixed before the push: the prefix is stripped (commit "strip a scratch path from the model-check baseline"). No local path or real name is in the added lines now.

## Findings

Blocking findings: 0 (the scratch path was fixed before the push).
Notes for the reviewer: the size item, the hidden-file order, and the 70 older problems.
