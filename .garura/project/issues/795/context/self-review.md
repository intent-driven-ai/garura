# Self-review: issues 795 and 836 (refreshed after review round 1)

Rules used: the resolved self-review rules file (base copy).
Diff: plan/788/base...HEAD (25 commits, 129 files).

New since the last self-review: the round 1 fixes the product owner asked for.
- dc185f79: shape-slice reuses a serving slice and adds the intent to it, and reports the differences. The record matches slice.yaml v2. The slice check validates records. Paths cannot leave the model. Spine writes are atomic. The question record keeps an open list and answers, matches by text, and the check fails on an unanswered question. The approval is verified before the commit. The change undoes Touches lines. The memory search and cite trace is in. A pointer to #838 is added. The template-manager is counted.
- 7b3c7078: slice.yaml and spine.yaml agree. The older chain is labelled.
- be239fc4: the pipeline-next rule has the live loop, the cardinal-rule table and the user-questions fields.

## Scope checks

- [PASS] Matches the issues. The change builds the new /shape-slice (795) and drops /next (836). Both issues are named in the commits.
- [PASS] No scope creep. The round 1 fixes all touch shape-slice, the two schemas and the rules the product owner named. Related work stays in follow-ups 837, 838 and 839.
- [REVIEW] Size. 129 files is large, but most of it is deleted files and one-line pointer edits. The two issues were grouped on purpose. Read the new play and its scripts first.
- [PASS] No stray artifacts. No debug prints, TODO marks or commented-out blocks in the added lines. Run files sit in the issue's evidence folder.

## Quality checks

- [PASS] Tests present. The shape-slice scripts carry four test files: 18, 19, 84 and 72 checks, all passing. The acceptance check passes 128 of 128.
- [PASS] Commits are clean. All 25 commits use conventional format, each is one concern, and each names an issue.
- [PASS] No secrets. A scan of the added lines found no keys, tokens or credentials.
- [PASS] Docs in step. The rules and the model schemas changed with the code. Component docs, glossary and ADR 051 were updated earlier in the change.
- [PASS] Plain wording and paths. No absolute home paths in the added lines.
- [PASS] Lint. lint-components shows 124 errors and 1 warning, the same old count as before, and none are on shape-slice.
- [REVIEW] Known gap, stated in the PR. The old-chain plays and the ready check in build-epic still use slice fields that were removed. This is tracked in #837 and #818. It does not break the goal of this change. A reviewer should confirm that the split is acceptable.

## Findings

Blocking findings: none.
Notes for the reviewer: the size item and the known gap above.
