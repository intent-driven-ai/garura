Two issues from plan 788: the new /shape-slice, and dropping /next.

Closes #795 and #836 (on merge into the plan branch, by merge-change).

## What changes

- **#795: a new /shape-slice, built fresh with /create-play.** The old play cut "realized" slices into epics, and that job is gone (ADR 049). The new play's ICE was approved by the product owner, and its decisions are in `.garura/project/issues/795/context/decisions.md`. The play:
  - takes a business intent's issue number as its entry point, and reads the intent from the product model. If the model has no page for it, it writes one from the issue;
  - reads the model and memory first, and asks only about the gaps, all at once (standards/rules/asking-a-person.md), within the question tier's budget (`grill_budget.py`, #817). Every gap not asked becomes a written assumption. Questions and answers go to the issue's `grounding-questions.md`;
  - picks the features from any capability, in build order, with one surface and its tester, and fills any domain, capability, feature or ICE the model lacks;
  - reuses a slice that already serves the intent (`find_serving_slice.py`);
  - writes the spine slice (`feature_refs`, `vertical`, `intents`, `record`) and its record at `product-os/slices/<id>.yaml` (`persist_slice.py`). A slice links to capabilities and has no domain home;
  - checks the model, guards the write scope, and stops at a typed checkpoint (yes / change / stop) before it commits. Stop undoes every write.
- **#795: what goes with it.** `spine.yaml` and `slice.yaml` follow the new slice. The skills `author-epics` and `check-cut-tensions` are deleted, and `product-os-keeper` lists the new play's skills. After discovery, the Next line now names /shape-slice.
- **#836: /next is dropped.** The play, the `rank-actions` skill, the `work-intelligence` memory shelf and `docs/command-chain.html` are deleted. No play's close says "run /next". **ADR 051** records why: the plan is the work list.
- Docs: CLAUDE.md ("when a play's job is gone, build a new play"; the ADR count), managing-work.md ("How is a change checked?"), AGENTS.md, component docs.

## Checks

| Check | Result |
|---|---|
| Acceptance check (written first; failed 33, then 13 more, before the build) | 93 passed, 0 failed |
| lint_play on shape-slice | PASS, 0 gaps |
| shape-slice tests (grill_budget, find_serving_slice, persist_slice, scripts) | all pass |
| All play, skill and linter tests | pass |
| Old-name check | 0 |
| lint-components | 135 → 124 errors (the deleted parts carried old errors); none on shape-slice |

Follow-ups: #837 (the old-chain plays: rebuild or drop), #838 (an author-slice skill), #839 (review the agent's memory). #818, #798, #796 and #794 are rewritten for the three-play shaping loop.

## Self-review

# Self-review: issues 795 and 836

Rules used: the resolved self-review rules file (base copy).
Diff: plan/788/base...HEAD (15 commits, 111 files).

## Scope checks

- [PASS] Matches the issues. The change builds the new /shape-slice (795) and drops /next (836). Both issues are named in the commits and the PR will close both.
- [PASS] No scope creep. Every file maps to one of the two issues: the new play and its scripts, the two schemas, the keeper agent, the deleted play and skills, the pointer clean-up in other plays, docs and ADR 051. Related work was filed apart as follow-ups 837, 838 and 839.
- [REVIEW] Size. 111 files is large, but most of it is deleted files and one-line pointer edits. The two issues were grouped on purpose. Reviewers should read the new play and its scripts first.
- [PASS] No stray artifacts. No debug prints, scratch files or commented-out blocks found in the diff. The eval files sit in the issue's evidence folder, which is the right place.

## Quality checks

- [PASS] Tests present. The new scripts carry their own tests. Acceptance check: 93 passed, 0 failed. All play and skill tests pass.
- [PASS] Commits are clean. All 15 commits use conventional format, each is one concern, and each names the issue.
- [PASS] No secrets. A scan of the added lines found no keys, tokens or credentials.
- [PASS] Docs in step. Component docs, the philosophy page, CLAUDE.md, AGENTS.md, managing-work and the glossary were updated. No live reference to the deleted play, skills, shelf or page remains outside the ADRs.
- [PASS] Nothing obviously broken. lint_play passes on shape-slice. lint-components shows 124 errors, down from 135, and none are on shape-slice. The old-name check finds 0.
- [PASS] Plain wording and paths. No absolute home paths in the new play files.

## Findings

Blocking findings: none.
Notes for the reviewer: the size item above. The 124 lint errors are old and come from other parts.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
