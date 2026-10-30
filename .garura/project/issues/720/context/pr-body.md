## Feature #720 — manage a plan with /update-plan

Closes #720, #730, #917, #931 and #997. Plan 717. One change for the whole feature: one branch, one review, one merge.

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
- **Plan 717's file**: #720, #730, #917, #931 and #997 Done.

### Round 2 (after the review's reject)

The four data-safety P2 findings are fixed, with tests: a staged file always stops the branch step and the cut commits only the plan file; a failed push of main is taken back; the landing commit takes only its own files; a create finds the issue an earlier run made by its marker line, and the run record is tied to the approved list. The component linter now reports repo-relative paths, and the round 1 lint report is scrubbed (round 1 commit 8e09877e still holds the paths in history; a history rewrite was not chosen). The round 1 blocker (DATA-18 on a test repo's throwaway address) is a false positive.

### Round 3 (after round 2's reject)

The remaining design P2 findings are fixed: ADR 061 (accepted by the product owner) records that a plan's branch is cut by the play that starts its work, main first, amending ADR 060; a new feature is now placed by a script and the placement skill, and the model sub-agent drafts nothing itself (the page skill writes the thin ICE at the landing, from the person's words). The scanner's path-only P2 rows have their evidence in the review folder (`code-evidence.md`).

### Round 4 (after round 3's reject, which rested only on the DATA-18 false positive)

The product owner asked for the medium (P3) findings to be fixed too, with an approved fix design (`specs/fix-design-round-3.md`):

- **ADR 062** (accepted): `/update-plan` writes the model only after "approved", a declared exception in the model-write rule, contained by the shared scoped-write guard after the last model write; a new feature may join a slice in progress, and the confirm screen says so and names the epic as out of date (amends ADR 026 and ADR 058). The linter's L-DMW-4 names `/update-plan` as a declared exception (with a test).
- **The plan tool**: uncommitted work stops it on every path, the plan's own branch included; a second abort finishes one that stopped after a refused delete.
- **`/update-plan` rebuilt through `/edit-play`** (F13 added): `session_files.py` (the issue numbers, the abort restore with its record, the guard); `verify.json` written by the approval check; questions in the four parts of the asking rule through a new `question` screen; the confirm screen's thin warning and slice-in-progress line; the placement script's own questions replaced on every run, a clean stop on a missing model index, and no silent swap of a named capability.
- **`track-plan-changes`**: a fake-host test for finding an issue an earlier run made, and what to check after a crash.
- **#997, the new Thin line**: `/shape-slice` rebuilt (C16), its scripts and `link-model-part` write the ontology v14 line and read any "Thin:" line; the eleven thin pages re-marked through `link-model-part`.
- **Words**: the glossary's feature item; `/shape-plan` says Not Started, not "active".
- **An install test** now reads the component linter's paths from the folder it ran in (round 2 made those paths relative; that test had not followed).

### Round 5 (after round 4, whose reject rested only on the DATA-18 false positive)

Round 4 found one new P3 (HF-12): the story-naming step and the model step of `/update-plan` wrote one model record with no rule to add or replace, and that record is the scope guard's allow list. The story step now writes its own record; the guard, the agreement check and the commit read both as one; a missing record is refused, so it never reads as "nothing may change". Three new tests (update-plan 40).

### How it was checked

Unit tests, all pass: update-plan 40, plan tool 31, track-plan-changes 13, link-model-part 22, change_lines 19, the adapter 58, the install 75, edit-ontology 11, /shape-slice 391, /shape-plan 119, /shape-eval 41, the ICE readiness check 46, the component linter 96. Both rebuilt plays pass the play linter. A test run in a throwaway copy covered every case of the design. A live run on plan 717 with real GitHub (fa6f514, merged in) landed #720 and #730 In Progress and #931's feature fn-931, and its agreement check held.

### Self-review

# Self-review: #720 (manage a plan with /update-plan), round 5

Rules: the base self-review rules (`~/.phoenix/core/memory/standards/rules/self-review.md`, no project override), resolved in `resolved-rules.json`.
Diff: `origin/plan/717/base...HEAD` on `plan/717/720-update-plan` (50 commits, 250 files, +221701 / -157). This re-raise of PR #998 follows the round 4 review.
This checklist is information for the reviewer. It is not the approve/reject gate.

Summary: 0 blocking findings, 6 notes for the reviewer.

## Earlier rounds, in short

Rounds 1 to 3 built the `/update-plan` play, the `author-plan-changes` and `track-plan-changes` skills, the plan-branch script, ADR 061 and ADR 062, the linter exception for `/update-plan`, and the Thin wording of #997, and answered each review's findings. Round 4 reviewed that work and found one new defect (HF-12). Each round's records sit under `.garura/project/issues/720/`.

## Since round 4

One fix landed (commit 39f52b8f, with the records of the review and commit runs around it). It answers round 4 finding HF-12: the story-naming step of `/update-plan` wrote the same model record as the model step, so it could drop a page the model step had written, and that record is the guard's list of allowed files.

- The story-naming dispatch now writes its own record, `model-record-story.json`. It never changes `model-record.json`.
- A new function `plan_session.model_records` reads any number of records as one: parts are joined by feature, files are joined with no repeat. The scoped-write guard (`session_files.py guard`), the agreement check (`check_agreement.py`) and the commit (`commit_plan.py`) each take `--model-record` once for every record and use it.
- A missing record is refused. `guard` now takes `--model-ops`; when that file lists parts and no record is given or a given record is not on disk, it stops with exit 2 and puts nothing back, so a missing record never reads as "nothing may change". `commit_plan.py` and `check_agreement.py` also refuse a record path that is not on disk; before this fix `commit_plan.py` skipped one.
- The play's SKILL.md follows: Step 9's story dispatch names the new record, the Step 11 and Step 12 commands use `<records>`, the exit-2 case is written down, the model record's paths are stated as relative to the repository root, and the SE-18 step eval now also checks that `model-record.json` still names each page after the story step.
- Tests: 3 new in `test_update_plan_scripts.py` (the guard reads both records so the second never drops the page; the guard refuses a missing record and puts nothing back; two records read as one). The file now has 40 tests.

## Scope checks

- [PASS] Matches the issue. Every changed file belongs to the feature: the update-plan play (#730, with the findings of #917 and the new-feature step of #931), the plan-branch script in the plan tool, the two new skills, the adapter's reopen-issue verb and close reason, link-model-part's slice step, the plan-update template, ontology v14, plan 717's Done marks with story #997, ADRs 061 and 062 with their pointers and index lines, the install manifest, #720's short-term records, and the fixes of rounds 1 to 4. The round 5 fix touches six files, all inside `core/components/plays/update-plan/`.
- [PASS] No scope creep. The round 5 change is a fix of a round 4 finding inside the play's scripts and SKILL.md and changes no file outside the play. The earlier note stands: the /shape-slice, /shape-plan, /shape-eval and `create-play` files touched in this branch change only the Thin wording or the Not Started status word, the linter change is the exception ADR 062 records, and the agent files, pipeline-next rule, templates index and install scope list are the wiring the new play and skills need.
- [NOTE] Reasonable size. The change is large (250 files, +221701) because it adds a whole play, two skills and a tool script with their tests, then the records of five review rounds. About 212,160 of the added lines (120 files) are #720's short-term records under `.garura/project/issues/720/`, and 2,185 more (34 files) are the ADR run folders under `.garura/project/issues/_adr/`. Four diff copies kept as review evidence make up most of that: `.garura/project/issues/720/review/pr.diff` (110,050 lines, the round 4 run), `.garura/project/issues/720/review/run-3/pr.diff` (51,740), `.garura/project/issues/720/review/run-2/pr.diff` (23,774) and `.garura/project/issues/720/review/run-1/pr.diff` (9,442). The code and prose to review is 75 files and 6,988 added lines under `core/`, plus the ADR files under `docs/` (ADR 061 and ADR 062 are 153 lines each). Since round 4 the reviewable change is the 6 files of the fix (+102 / -28). Review the play (`core/components/plays/update-plan/`), the plan-branch script, ADR 062 and the linter exception first; the records are evidence only.
- [PASS] No stray artifacts. No `__pycache__`, `.pyc`, `.orig`, `.tmp`, `.swp` or `.DS_Store` file is in the diff. No absolute path, scratch path or user name appears in any line this branch adds, taken as a whole (diff copies and records included). No TODO or FIXME was added under `core/` or `docs/`. No commented-out blocks or debug prints were added.
- [NOTE] Absolute paths remain in one commit's history. Round 1 commit 8e09877e added `.garura/project/issues/720/review/lint-components.json` with absolute file paths in it (a machine path and a user name). The later commit 18f1ad00 scrubs it, so the file at HEAD, and the net diff of this PR, carry none. The commit 8e09877e itself still holds them in this branch's history. The product owner chose a new scrubbing commit over a history rewrite, so this is accepted and recorded here for the reviewer. It is not a defect of the final tree.
- [PASS] Copies agree. The platform adapter is copied into eight places (seven plays and the `track-plan-changes` skill); all eight are byte-identical. The stamped `scoped_write_guard.py` in `/update-plan` is byte-identical to its source `core/components/plays/create-play/references/scoped_write_guard.py` and to the 14 other stamped copies (16 identical in all). The round 5 fix touched neither.

## Quality checks

- [PASS] Tests present. The new behaviour of round 5 carries 3 tests, and all pass: update-plan scripts (40 tests with `unittest`), track-plan-changes (13), link-model-part (22), plan tool (35: 18 in `test_plan_branch.py`, 17 in `test_plan.py`). These suites were run again for this round. The other suites (enrich-grounding 19, the linter's 7 test files, shape-slice, shape-plan, shape-eval and create-play's scripts) sit in files the round 5 fix did not touch, and their round 4 results stand.
- [PASS] Commits are clean. All 50 commits use conventional format except the merge of `origin/plan/717/base` into the branch (a merge commit, 3d4294c1); 49 name #720, and the merge is the one that does not. No commit carries a Claude trailer. The round 5 code commit (39f52b8f) is one concern, the model records of one landing, and says why in its message. The `chore(stm)` commits each record one run's records.
- [PASS] No secrets. A scan of added lines for keys, tokens, passwords and private-key headers found nothing.
- [PASS] Docs in step. The `update-plan` SKILL.md moved with the code (Step 9, Step 11, Step 12, SE-18 and the exit-2 case), the docstrings of `session_files.py`, `check_agreement.py` and `commit_plan.py` state the new arguments, and the earlier docs (plan tool README, plan-update template, ontology v14, glossary, `direct-model-write.md`, ADR pointers and index) are as in round 4. ADR 061 and ADR 062 check valid with `adr.py lint`.
- [PASS] Nothing obviously broken. The component linter reports 37 findings (36 errors, 1 warning) across the whole component tree, the same count as rounds 3 and 4, none in a file this change touches. No failing tests found. One behaviour changed on purpose: `commit_plan.py` used to skip a model record that was not on disk and now refuses it, so a landing whose record is lost stops instead of committing without the model files.
- [NOTE] The list of epic statuses that mean "in progress" has three copies. `/update-plan` (`place_feature.py`) and `/shape-slice` (`find_serving_slice.py`) are tied by a test, so they cannot drift apart. A third copy in `persist_slice.py` (`/shape-slice`'s own) is not read by that test. ADR 062 says so and keeps it out of scope.
- [NOTE] The linter's exception for `/update-plan` is a fixed list of play names (`DMW4_DECLARED_EXCEPTIONS`, one name). A later play that needs the same exception must be added to that list and named in `direct-model-write.md`, with an ADR. This is deliberate (a declared exception, like those of ADR 031), not a defect.
- [NOTE] ADR 062 holds one stale phrase. In its third finding it says the code of `go` is "not yet committed on this branch"; commit e6520ba5 has since committed it. The ADR is accepted, so the phrase is left as written; it does not change the decision.
- [NOTE] Follow-up already filed. ADR 061 notes that start-change cuts a plan's branch through the same script once #989 is built; until then ADR 060's line about start-change stands. This is known and planned, so it is not a defect of this change.

## Blocking findings

None.
