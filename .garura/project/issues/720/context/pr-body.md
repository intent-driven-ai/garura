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

### Round 6 (after round 5, whose reject rested only on the DATA-18 false positive)

Round 5 found a P3 in the HF-12 fix (HF-14): the play passed `model-record.json` to the guard, the agreement check and the commit even when the model step was skipped, so a session with no new feature would have stopped at the guard. Now no record is passed when no model step ran. With it: the model sub-agent's route says each dispatch writes only to its own output (HF-15); the guard refuses a missing or misshapen model-ops file or record instead of reading it as empty or crashing (N4-02, N5-01); tests for the commit and the agreement check with two records (N5-02). update-plan 44 tests.

### How it was checked

Unit tests, all pass: update-plan 44, plan tool 31, track-plan-changes 13, link-model-part 22, change_lines 19, the adapter 58, the install 75, edit-ontology 11, /shape-slice 391, /shape-plan 119, /shape-eval 41, the ICE readiness check 46, the component linter 96. Both rebuilt plays pass the play linter. A test run in a throwaway copy covered every case of the design. A live run on plan 717 with real GitHub (fa6f514, merged in) landed #720 and #730 In Progress and #931's feature fn-931, and its agreement check held.

### Self-review

# Self-review: #720 (manage a plan with /update-plan), round 6

Rules: the base self-review rules (`~/.phoenix/core/memory/standards/rules/self-review.md`, no project override), resolved in `resolved-rules.json`.
Diff: `origin/plan/717/base...HEAD` on `plan/717/720-update-plan` (55 commits, 267 files, +450424 / -157). This re-raise of PR #998 follows the round 5 review.
This checklist is information for the reviewer. It is not the approve/reject gate.

Summary: 0 blocking findings, 7 notes for the reviewer.

## Earlier rounds, in short

Rounds 1 to 3 built the `/update-plan` play, the `author-plan-changes` and `track-plan-changes` skills, the plan-branch script, ADR 061 and ADR 062, the linter exception for `/update-plan`, and the Thin wording of #997, and answered each review's findings. Round 4 found HF-12 (the story-naming step could drop a page the model step wrote). Round 5 checked its fix (two model records read as one) and found HF-14 inside it. Each round's records sit under `.garura/project/issues/720/`.

## Since round 5

One code commit landed (18bca086, with the records of the runs around it). It answers the round 5 findings:

- HF-14: a session with no new feature never runs the model step, so no model record exists. Step 11 and Step 12 of the play now pass no `--model-record` in that case (`<records>` is empty when `model-ops.json` has no parts). Before this, the guard would have stopped such a session.
- HF-15: the model sub-agent's route in `core/components/agents/product-os-keeper.md` now says each dispatch writes its record only to the output path its contract names, never over another dispatch's record (`model-record.json` for Step 8, `model-record-story.json` for the story step). The story record's shape is written in Step 9 of the play.
- N4-02 and N5-01: `session_files.py guard` now refuses a missing `model-ops.json` and one that is not `{parts: [...]}`; `plan_session.model_records` refuses a record that is not `{parts: [...], files: [...]}`, a part that is not an object, and a file that is not a path. Each stops with exit 2 and puts nothing back, and not with a traceback.
- N5-02: tests for the commit and the agreement check with two records.
- Tests: 4 new in `test_update_plan_scripts.py` plus one added check (a session with no new feature passes the guard with no record; the guard refuses a missing or misshapen model-ops file; a misshapen record is refused; the commit takes both records and refuses a missing one; the agreement check holds with the story record added). The file now has 44 tests.

## Scope checks

- [PASS] Matches the issue. Every changed file belongs to the feature: the update-plan play (#730, with the findings of #917 and the new-feature step of #931), the plan-branch script in the plan tool, the two new skills, the adapter's reopen-issue verb and close reason, link-model-part's slice step, the plan-update template, ontology v14, plan 717's Done marks with story #997, ADRs 061 and 062 with their pointers and index lines, the install manifest, #720's short-term records, and the fixes of rounds 1 to 5.
- [PASS] No scope creep. The round 6 code commit touches five files: four inside `core/components/plays/update-plan/` and one line group in `core/components/agents/product-os-keeper.md` (the route of the model sub-agent, which is the wiring the play needs). The earlier note stands: the /shape-slice, /shape-plan, /shape-eval and `create-play` files touched in this branch change only the Thin wording or the Not Started status word; the linter change is the exception ADR 062 records.
- [NOTE] Reasonable size. The change is large (267 files, +450424) because it adds a whole play, two skills and a tool script with their tests, then the records of six review rounds. 137 files and 440,817 added lines are #720's short-term records under `.garura/project/issues/720/`, and 2,185 more (34 files) are the ADR run folders under `.garura/project/issues/_adr/`. Five diff copies kept as review evidence make up almost all of the records: `.garura/project/issues/720/review/pr.diff` (224,474 lines, the round 5 run), and the older `review/run-4/pr.diff` (110,050), `review/run-3/pr.diff` (51,740), `review/run-2/pr.diff` (23,774) and `review/run-1/pr.diff` (9,442). The current copy is large because each review run embeds the diff of the run before it, so it more than doubled since round 5. The code and prose to review is 75 files and 7,056 added lines under `core/`, plus the ADR files under `docs/` (ADR 061 and ADR 062 are 153 lines each). Since round 5 the reviewable change is the 5 files of the fix (+77 / -9). Review the play (`core/components/plays/update-plan/`), the plan-branch script, ADR 062 and the linter exception first; the records are evidence only.
- [PASS] No stray artifacts. No `__pycache__`, `.pyc`, `.orig`, `.tmp`, `.swp` or `.DS_Store` file is in the diff. No absolute path, scratch path or user name appears in any line this branch adds, taken as a whole (diff copies and records included). No TODO or FIXME was added under `core/` or `docs/`. No commented-out blocks or debug prints were added.
- [NOTE] Absolute paths remain in one commit's history. Round 1 commit 8e09877e added `.garura/project/issues/720/review/lint-components.json` with absolute file paths in it (a machine path and a user name). The later commit 18f1ad00 scrubs it, so the file at HEAD, and the net diff of this PR, carry none. The product owner chose a new scrubbing commit over a history rewrite, so this is accepted and recorded here for the reviewer. It is not a defect of the final tree.
- [PASS] Copies agree. The platform adapter is copied into eight places (seven plays and the `track-plan-changes` skill); all eight are byte-identical. The stamped `scoped_write_guard.py` in `/update-plan` is byte-identical to its source `core/components/plays/create-play/references/scoped_write_guard.py` and to the 14 other stamped copies (16 identical in all). The round 6 fix touched neither.

## Quality checks

- [PASS] Tests present. The new behaviour of round 6 carries its tests, and all pass: update-plan scripts (44 tests with `unittest`), track-plan-changes (13), link-model-part (22), plan tool (35: 18 in `test_plan_branch.py`, 17 in `test_plan.py`), and the linter's 7 test files (7 tests). These suites were run again for this round. The other suites sit in files the fix did not touch, and their earlier results stand.
- [PASS] Commits are clean. All 55 commits use conventional format except the merge of `origin/plan/717/base` into the branch (a merge commit, 3d4294c1); the other 54 all name #720, and the merge is the one that does not. No commit carries a Claude trailer. The round 6 code commit (18bca086) is one concern, the model records of one landing, and says why in its message. The `chore(stm)` commits each record one run's records.
- [PASS] No secrets. A scan of added lines for keys, tokens, passwords and private-key headers found nothing.
- [PASS] Docs in step. The `update-plan` SKILL.md moved with the code (Step 9 states the story record's shape and when `<records>` is empty; Step 11 and Step 12 use `<records>`), the docstring of `session_files.py` states that `model-ops.json` must be there and in shape, and the product-os-keeper route states where each dispatch writes. The earlier docs (plan tool README, plan-update template, ontology v14, glossary, `direct-model-write.md`, ADR pointers and index) are as in round 5.
- [PASS] Nothing obviously broken. The component linter reports 37 findings (36 errors, 1 warning) across the whole component tree, the same count as rounds 3 to 5, none in a file this change touches. No failing tests found. One behaviour changed on purpose in round 6: the guard used to treat a missing `model-ops.json` as "no parts" and now refuses it (Step 7 always writes it), so a lost file stops the landing and puts nothing back.
- [NOTE] The list of epic statuses that mean "in progress" has three copies. `/update-plan` (`place_feature.py`) and `/shape-slice` (`find_serving_slice.py`) are tied by a test, so they cannot drift apart. A third copy in `persist_slice.py` (`/shape-slice`'s own) is not read by that test. ADR 062 says so and keeps it out of scope.
- [NOTE] The linter's exception for `/update-plan` is a fixed list of play names (`DMW4_DECLARED_EXCEPTIONS`, one name). A later play that needs the same exception must be added to that list and named in `direct-model-write.md`, with an ADR. This is deliberate (a declared exception, like those of ADR 031), not a defect.
- [NOTE] ADR 062 holds one stale phrase. In its third finding it says the code of `go` is "not yet committed on this branch"; commit e6520ba5 has since committed it. The ADR is accepted, so the phrase is left as written; it does not change the decision.
- [NOTE] Follow-up already filed. ADR 061 notes that start-change cuts a plan's branch through the same script once #989 is built; until then ADR 060's line about start-change stands. This is known and planned, so it is not a defect of this change.

## Blocking findings

None.
