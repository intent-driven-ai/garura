## What this changes

**/shape-plan now uses the story a feature already has, instead of filing a second one** (#1025, P1). All plan files were deleted on 2026-11-02. Without this change, a rebuilt plan would file new stories next to the open ones. Now, when the plan file doesn't mark a story for a feature, /shape-plan uses the open Story that the feature's entry in the product model names. It moves that story under the slice's epic and adds only the sections the story lacks. If a named issue is missing, closed, not a Story, or named for two features, the run stops before it writes anything to the tracker and names the problem.

**Older parts of the model no longer read as "no ICE"** (#1034, #1035). The ready check and the plan helpers used to switch the whole model to the new ICE shape as soon as any part had an ICE entry. Now each part is read by its own shape: a part that has not moved yet is read from the ICE section inside its own page. On today's model, the 6 features that read "not ready" now read "partly ready", with the gap "ICE still inside its page".

Closes #1025
Closes #1034
Closes #1035

## How to review it

- **The intent change.** /shape-plan's ICE (`reference/ice.md`) changes C3 and adds failure condition F14 with its recovery REC14, scenario S10 with its eval SCE-10, and step eval SE-21. `SKILL.md` was rebuilt from it with fix-play. The play lint passes with 0 gaps.
- **Shared scripts.** These appear as byte-identical copies. Read one of each and check that the copies match:
  - `platform_adapter.py`: 8 copies. attach-sub-issue takes an optional `replace_parent`, so a reused story leaves its old parent.
  - `plan_common.py`: 3 copies. The tracker helper asks for that flag, and each part's ICE is read by its own shape.
  - `check_ice_workable.py`: 4 copies. The ready check reads a part that hasn't moved from its inline ICE.
- **Tests.** New finder, gather, ready-check and S10 end-to-end tests. All 43 test files of the affected plays pass. One /reshape-plan test, `test_feature_ice`, failed on main before this change and passes now.
- **Out of scope.** /design-slice has its own copy of the whole-model ICE switch, which belongs under #1033. The thin mark for a found feature is #1036.

## Notes

- Before the push, the unpushed commits were rewritten to remove a home-folder path from one run record, under the repo's no-personal-references rule. The three code commits kept their IDs. The three run-record commits got new IDs, so commit-work's record still names the old ones.
- Self-review finding 1 says there is no direct test of the adapter flag. There is one: `shape-plan/scripts/test_support.py` checks that the command carries the flag when asked and leaves it off otherwise.

## Self-review

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
