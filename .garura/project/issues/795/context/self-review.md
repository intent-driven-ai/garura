# Self-review: issues 795 and 836 (refreshed after review round 2)

Rules used: the resolved self-review rules file (base copy).
Diff: origin/plan/788/base...HEAD (34 commits, 146 files).

What the whole change does: builds the new /shape-slice (795), which grills the person and then assembles the slice, and drops /next (836). Round 1 fixes (dc185f79, 7b3c7078, be239fc4) were reviewed in the last self-review and still hold: a serving slice is reused, the record matches slice.yaml v2, paths stay inside the model, spine writes are atomic, and the question record and approval are checked.

## New since origin's branch tip (commits 9e5508dd..HEAD, the review round 2 fixes)

- 9e5508dd: old slice records are brought to v2 when a slice is reused. The spine is written back with its comments kept (new spine_text.py). Defects in other slices are warnings in the slice check, not failures. The question record reads a bare "skip" only; "skip + more" is unclear and is asked again. A new message-shape check tests each question. Proposed answers keep a memory trace.
- cc538b0f: Done means now includes D5, the trace check, and the play runs the message check step.
- 1dc0b567: the slice schema has a note on how records written before v2 are read.
- 3f6c32ac: round-2 acceptance checks were added.
- Undo removes an empty Touches heading (part of the round-2 fix set).
- The remaining commits (1684d7ef, 9967272c, e8b5bf2d, b4d173a1) only record run files under the issue's folder.

## Scope checks

- [PASS] Matches the issues. Every round-2 change is on shape-slice, its two schema notes, its stop condition, or its tests. Each commit names issue 795.
- [PASS] No scope creep. Round 2 only answers the review findings. Related work stays in follow-ups 837, 838 and 839.
- [REVIEW] Size. 146 files is large, but most of it is deleted files (the /next play, the old epic skills) and one-line pointer edits. The two issues were grouped on purpose. Round 2 itself touches only four source files outside run records. Read the new play and its scripts first.
- [PASS] No stray artifacts. No debug prints, TODO marks or commented-out blocks in the added lines. The only print calls are the scripts' JSON output. Run files sit in the issue's evidence folder.

## Quality checks

- [PASS] Tests present. The shape-slice scripts carry four test files and all pass: 18, 19, 89 and 80 checks. The acceptance check passes 143 of 143 (was 128 before round 2).
- [PASS] Commits are clean. All 34 commits use conventional format, each is one concern, and each names an issue.
- [PASS] No secrets. A scan of the added lines found no keys, tokens or credentials.
- [PASS] Docs in step. The slice schema, the play steps, its ICE and its stop condition changed together with the code.
- [PASS] Plain wording and paths. No absolute home paths in the added lines.
- [PASS] Lint. lint-components shows 124 errors and 1 warning, the same old count as before, and none are on shape-slice.
- [REVIEW] Known gap, stated in the PR. The old-chain plays and the ready check in build-epic still use slice fields that were removed. This is tracked in #837 and #818. It does not break the goal of this change. A reviewer should confirm that the split is acceptable.

## Findings

Blocking findings: none.
Notes for the reviewer: the size item and the known gap above.
