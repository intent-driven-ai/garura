# Self-review: #1025 (/shape-plan uses the open story a feature's model entry names)

Rules: the base self-review rules (standards/rules/self-review.md), no project override.
Branch: feature/1025-shape-plan-reuses-open-story, against main. 7 commits, 39 files, +1009 -88.

Verdict: ready to raise. No blocking findings. Two non-blocking notes below.

## Scope checks

- Matches the issue: PASS. /shape-plan now uses the open Story that a feature's model entry names, makes it a sub-issue of the slice's epic, and adds only the sections it lacks. A named issue that is missing, closed, not a Story, or named for two features stops the run before any tracker write. This is carried by the play's intent source (constraint C3, failure F14, recovery REC14, scenario S10 and SCE-10, step eval SE-21), the recompiled play file, and the three scripts that gather the model's issue, decide the story's action, and show it in the brief.
- Pieces that ride along are each tied to the issue or to the two named side issues: the adapter's optional replace_parent flag and the tracker helper that asks for it are needed so a reused story leaves its old parent (#1025). The ready check and plan helpers reading each part by its own shape is #1034 and #1035 (same root cause), named in the commit that carries it.
- No scope creep: PASS. The design-slice copy of the whole-model ICE switch (#1033) and the thin mark for a found feature (#1036) are not touched.
- Reasonable size: PASS with a note. 39 files, but 15 are run records under the issue's own folder and 12 more are the repeated copies of three shared scripts (8 adapter, 3 plan helper, 4 ready check). The real hand-written change is about 8 files plus their tests.
- No stray artifacts: PASS. No debug prints, no commented-out blocks, no scratch files, no absolute or home paths added. One untracked file sits in the issue's context folder (the resolved rules record the review-work play writes); it belongs to this run.

## Quality checks

- Tests present: PASS. New tests cover a model-named story used and never made, a story missing sections, the closed, wrong-type and absent cases, one issue named for two features, the whole S10 flow (story moved under the epic, brief wording, plan check ok), the file tracker moving a sub-issue off its old parent, and the ready check and plan helpers on a mixed model (#1034). All shape-plan test files, the reshape-plan files and the ready-check test file pass when run (for example 23 and 27 checks pass in the two main shape-plan suites, 66 in reshape-plan). The earlier failing reshape-plan test (test_feature_ice) passes now.
- Commits are clean: PASS. Five commits are conventional and name #1025 (the adapter, the ready check fix, the shape-plan change, and the run records). Each is one concern. No Claude attribution lines in any commit.
- No secrets: PASS. Scanned the diff for keys, tokens, passwords and private key markers; none found.
- Docs in step: PASS. The play's intent source and compiled play file both carry the new rule, scenario, step eval and recovery, and the play's counts and fingerprint are updated. The adapter flag is documented in its helper's docstring.
- Nothing obviously broken: PASS. No leftover TODOs. The 8 adapter copies, 3 plan helper copies and 4 ready check copies are byte-identical (same checksum in each group). The component linter reports errors, but none are in a file this change touches (they are in the build-play play file, which is not in the diff).

## Non-blocking findings

1. The adapter's new replace_parent flag has no direct test in the adapter's own test file (it is exercised only through the file tracker used in the S10 test, which models the behaviour, not the real command line). A small test that attach-sub-issue with replace_parent "true" adds the flag to the command, and leaves it off otherwise, would pin it. Suggest a follow-up, not a reason to hold the raise.
2. The 12 repeated script copies plus 8 adapter copies make the change look large; reviewers should read one copy of each and trust the checksums. The PR text should say so.
