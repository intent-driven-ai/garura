## Feature #720 — manage a plan with /update-plan

Closes #720, #730, #917 and #931. Plan 717. One change for the whole feature: one branch, one review, one merge.

### What a person gets

`/update-plan <id>` or `/update-plan <a description>` is a working session on one plan. The person gives instructions in their own words. The play checks each one against the plan's rules, keeps a running list, and shows one approval screen: the plan and the business intent it serves, the plan before and after (only the touched parts), and what changed. Only a plain "approved" lands it, all at once: the product model, then GitHub, then the plan file. A check then proves the three agree and nothing else changed, and one commit is pushed on the plan's branch. "Rejected" lands nothing and the session goes on. "Abort" drops the list, undoes a branch the session cut, and goes back.

### What is in it

- **The `update-plan` play** (#730, #931): ICE, compiled play, 13 scripts with tests, its stop condition.
- **The plan tool's `plan_branch.py`**: stay, stop on uncommitted work, switch, main first then cut, back, abort. The plan tool's README now says what a plan file holds and which item kinds it may hold (#917).
- **Two skills** through the issue sub-agent: `author-plan-changes` (an instruction → list entries) and `track-plan-changes` (read the plan's issues; make the approved writes, recorded one by one).
- **The platform adapter**: the `reopen-issue` verb and the close reason on `view-issue` (25 verbs), in every copy.
- **`link-model-part`**: adds features to a slice that exists, and names a feature's issue on update; the model sub-agent's routes for a new feature.
- **The `plan-update` template** (promoted to Phoenix memory), its index line and the Next line.
- **Ontology v14** through `/edit-ontology 720`, agreed at its three checkpoints: the Plan's status, direction, item kinds, feature item, branch, no history, `/update-plan`; the ICE's Thin line. Nothing operational goes into the product model.
- **#917**: the two work-rules lines.
- **Plan 717's file**: #720, #730, #917 and #931 Done; #997 filed under #720 for the Thin line follow-up.

### Round 2 (after the review's reject)

The four data-safety P2 findings are fixed, with tests: a staged file always stops the branch step and the cut commits only the plan file; a failed push of main is taken back; the landing commit takes only its own files; a create finds the issue an earlier run made by its marker line, and the run record is tied to the approved list. The component linter now reports repo-relative paths, and the round 1 lint report is scrubbed (round 1 commit 8e09877e still holds the paths in history; a history rewrite was not chosen). The round 1 blocker (DATA-18 on a test repo's throwaway address) is a false positive.

### How it was checked

Unit tests: update-plan 19, plan tool 29, track-plan-changes 8, link-model-part 21, change_lines 19, the adapter 58, the install 75, edit-ontology 11 — all pass. A test run in a throwaway copy covered every case of the design. A live run on plan 717 with real GitHub (fa6f514, merged in) landed #720 and #730 In Progress and #931's feature fn-931, and its agreement check held.

### Self-review

# Self-review: #720 (manage a plan with /update-plan), round 2

Rules: the base self-review rules (`~/.phoenix/core/memory/standards/rules/self-review.md`, no project override), resolved in `resolved-rules.json`.
Diff: `origin/plan/717/base...HEAD` on `plan/717/720-update-plan` (24 commits, 116 files, +22249 / -86). This re-raise of PR #998 follows the round 1 review.
This checklist is information for the reviewer. It is not the approve/reject gate.

Summary: 0 blocking findings, 4 notes for the reviewer.

## Since round 1

The branch adds fixes for the four data-safety findings the round 1 review raised, plus two smaller changes:

- The plan-branch script (`core/tools/plan/plan_branch.py`): a staged file always stops the branch step, the cut commits only the plan file, a failed push of main is taken back, and abort checks the branch it deletes. Tests added in `core/tools/plan/test_plan_branch.py`.
- The landing commit of /update-plan (`commit_plan.py`): it takes only its own files and refuses paths outside the repository. Tests added to the play's script tests.
- The tracker writes (`track_changes.py`, `tracker.py`): a create finds the issue an earlier run made by its marker, and the record is tied to the approved list. Tests added in `test_track_changes.py`.
- The component linter (`core/tools/lint-components/index.js`): every path is reported relative to where the linter ran.
- The round 1 lint report was scrubbed of absolute paths in a new commit, and the round 1 review's memory copies and the install manifest were recorded.

## Scope checks

- [PASS] Matches the issue. Every changed file belongs to the feature: the update-plan play (#730, with the findings of #917 and the new-feature step of #931), the plan-branch script in the plan tool, the two new skills (author-plan-changes, track-plan-changes), the adapter's reopen-issue verb and close reason, link-model-part's slice step, the plan-update template, ontology v14, plan 717's Done marks with the new story #997, #720's short-term records, and the round 1 fixes above. The one linter change is a round 1 fix in the review's own findings, small (6 lines) and named in #720's commits.
- [PASS] No scope creep. The agent files (product-os-keeper, project-orchestrator), the pipeline-next rule, the templates index and the install scope list are the wiring the new play and skills need. The managing-work guide edit belongs to the feature's last docs commit. The round 1 fixes touch only files the feature already added, apart from the linter.
- [NOTE] Reasonable size. The change is large (116 files, +22249) because it adds a whole play, two skills and a tool script with their tests, and then the records of two review rounds. About 16,450 of the added lines (64 files) are #720's short-term records under `.garura/project/issues/720/` (memory copies, ontology drafts, build design, and the round 1 review including its 9,442-line diff copy). The code and prose to review is about 5,800 lines in `core/`. Review the play, the two skills, the plan-branch script and the round 1 fixes first; the records are evidence only.
- [PASS] No stray artifacts. No `__pycache__`, `.pyc`, `.orig`, `.tmp` or scratch files are in the diff. No scratch path and no user name appear in any line this branch adds, taken as a whole (the three-dot diff and the tree at HEAD both read clean). No TODO or FIXME was added under `core/`.
- [NOTE] Absolute paths remain in one commit's history. Round 1 commit 8e09877e added the review file `.garura/project/issues/720/review/lint-components.json` with absolute file paths in it (a machine path and a user name). The new commit 18f1ad00 scrubs it, so the file at HEAD, and the net diff of this PR, carry none. The commit 8e09877e itself still holds them in this branch's history. The product owner chose a new scrubbing commit over a history rewrite, so this is accepted and recorded here for the reviewer. It is not a defect of the final tree.
- [PASS] Copies agree. The platform adapter is copied into eight places (seven plays and the new track-plan-changes skill); all eight have the same content (same checksum), so the reopen-issue verb and close reason are the same everywhere.

## Quality checks

- [PASS] Tests present. New tests came with the new behaviour and the round 1 fixes, and all pass when run with `unittest`: update-plan scripts (21 tests, 2 added), track-plan-changes (10, 2 added), link-model-part (21), plan tool (16 in `test_plan_branch.py` and 17 in `test_plan.py`). The adapter's own test file was updated for the new verb.
- [PASS] Commits are clean. All 24 commits use conventional format; 23 name #720. The one commit without #720 is the merge of `origin/plan/717/base` into the branch (a merge commit, not a change of concern). No commit carries a Claude trailer. Several `chore(stm)` commits record separate play runs; each is one concern (one run's records).
- [PASS] No secrets. A scan of added lines in `core/` and the user-provided guide for keys, tokens, passwords and private-key headers found nothing.
- [PASS] Docs in step. The plan tool README, the plan-update template and its index entry, the ontology (v14 with its log line), the pipeline-next rule, the adapter's SKILL.md and both verbs files, the track-plan-changes SKILL.md, and the managing-work guide all moved with the change.
- [PASS] Nothing obviously broken. The component linter reports 37 findings (36 errors, 1 warning) across the whole component tree, none in a file this change touches; they are older findings in other plays and skills. Run from the repo root, the linter now prints paths relative to it. No new leftover paths found.
- [NOTE] Follow-up already filed. The pages and scripts that still say the Thin line names /shape-slice move to the new wording in #997, now in plan 717 as Not Started. This is known and planned, so it is not a defect of this change.

## Blocking findings

None.
