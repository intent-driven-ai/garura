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

## Review round 1 fixes

- A slice that already serves the intent is reused even when the new shape differs (`persist_slice --reuse`). It keeps its features and surface, gains the intent, and the run shows the differences at the checkpoint.
- The slice record matches `slice.yaml` v2: `slice {id, slug, name, outcome, feature_refs, vertical, intents}` and `surface {id, name, persona_ref, user_action}`. The slice check tests every record.
- Ids and paths cannot leave the model, and the spine is written safely (a temp file, then a replace).
- The question record matches answered questions by their text, `check` fails on an unanswered question, and two glue steps are now scripts.
- A script (`record_approval.py verify`) checks for the yes right before the commit. A "change" undoes this run's intent-page edits.
- Decisions keep a memory trace (`memory.py cite`). The play points to #838, and template-manager is counted.
- The rule files agree: the live shape loop is named, and the older chain is labelled (#837).

## Review round 2 fixes

- A slice whose record was written before `slice.yaml` v2 is brought to v2 when a run reuses it. Its facts come from the spine entry; name and outcome come from the shaped slice; the surface moves to the top level. If a part is still missing, the run stops and names it. `slice.yaml` now says this.
- The spine is written back with its comments and layout (new `spine_text.py`). Only the changed slice or fill entries change.
- The slice check fails only for this run's slice. A defect in another slice is a warning, so one bad slice no longer blocks every run.
- The question record reads only a bare "skip" (or "defer") as deferred. A reply like "Skip the dashboard, use the CLI" is marked unclear and asked again. A new `record_questions.py message` check tests the message before it is sent (the opening, and the four parts of each question), and the shape test now also catches a question that does not stand alone.
- Each proposed answer keeps its memory trace (`memory.py cite`). The Done means has a new clause, D5: the trace check must name no changed source. This went through the ICE first, and the fingerprint is updated.
- An undo no longer leaves an empty "Touches" heading on the intent page.

## Known gap (not fixed here)

The old-chain plays still read or write slice fields this PR removes: `/shape-scope`, `/shape-roadmap`, `/shape-measure-lens` and `/shape-run-lens`. `/build-epic`'s ready check still needs a "realized" slice and a spine epic, and nothing makes those now. So `/build-epic` cannot start from a shaped slice until the plan play (#818) makes the epic. All of this is tracked in #837 and noted on #818.

## Checks

| Check | Result |
|---|---|
| Acceptance check (written first; it failed before each build round; round 2 added 14 checks that failed first) | 143 passed, 0 failed |
| lint_play on shape-slice | PASS, 0 gaps |
| shape-slice tests (grill_budget, find_serving_slice, persist_slice, scripts) | all pass |
| All play, skill and linter tests | pass |
| Old-name check | 0 |
| lint-components | 135 → 124 errors (the deleted parts carried old errors); none on shape-slice |

Follow-ups: #837 (the old-chain plays: rebuild or drop), #838 (an author-slice skill), #839 (review the agent's memory). #818, #798, #796 and #794 are rewritten for the three-play shaping loop.

## Self-review

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

🤖 Generated with [Claude Code](https://claude.com/claude-code)
