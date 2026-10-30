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

### How it was checked

Unit tests, all pass: update-plan 37, plan tool 31, track-plan-changes 13, link-model-part 22, change_lines 19, the adapter 58, the install 75, edit-ontology 11, /shape-slice 391, /shape-plan 119, /shape-eval 41, the ICE readiness check 46, the component linter 96. Both rebuilt plays pass the play linter. A test run in a throwaway copy covered every case of the design. A live run on plan 717 with real GitHub (fa6f514, merged in) landed #720 and #730 In Progress and #931's feature fn-931, and its agreement check held.

### Self-review

# Self-review: #720 (manage a plan with /update-plan), round 4

Rules: the base self-review rules (`~/.phoenix/core/memory/standards/rules/self-review.md`, no project override), resolved in `resolved-rules.json`.
Diff: `origin/plan/717/base...HEAD` on `plan/717/720-update-plan` (42 commits, 232 files, +107674 / -156). This re-raise of PR #998 follows the round 3 review.
This checklist is information for the reviewer. It is not the approve/reject gate.

Summary: 0 blocking findings, 5 notes for the reviewer.

## Since round 3

The branch adds these changes (and the records of the round 3 review runs):

- ADR 062 (accepted, 2026-10-30). It amends ADR 026 and ADR 058, in part. `/update-plan` writes the product model only after the person's plain "approved" for the whole list, and a feature found mid-plan may join a slice in progress. ADR 026 and ADR 058 gained a forward pointer, and the ADR index a line. The ADR check (`adr.py lint`) reads valid.
- The plan tool's `plan_branch.py go` checks uncommitted work first, on every path, the plan's own branch included (a staged file always counts). `abort` now finishes a second time after a refused delete: it finds main's revert of the cut, skips the revert and only deletes. The tool's docstring and README moved with the code. Two tests were added to `core/tools/plan/test_plan_branch.py`.
- `/update-plan` was rebuilt (recompiled through its ICE): the new script `session_files.py` (the plan's issue numbers, the restore on "abort", the guard run), the stamped `scoped_write_guard.py` (the same content as the 15 other stamped copies), `verify.json` written by the script itself, a question screen in four parts, the thin warning on the confirm screen of a new feature, and a slice-in-progress line that names each epic past ready with its status. `place_feature.py` marks a slice in progress and asks, instead of silently swapping, when the capability the person named is not in the model. The ICE has a new failure condition (F13, the guard put a path back) and two new step evals (SE-17, SE-18). The `author-plan-changes` and `track-plan-changes` skills and the `plan-update` template moved with it.
- The component linter accepts a declared exception for `/update-plan` in rule L-DMW-4 (no model-only clean check and no `feat(model)` commit), named in `direct-model-write.md` and in `core/tools/lint-components/lib/rules/structural.js`, with a test.
- #997 (the Thin line no longer names /shape-slice) is built here: the new wording "Thin: proposed from the person's words; deepen with `/discover-capabilities`." is in /shape-slice (SKILL.md, its ICE, `persist_fills.py`, `slice_check.py`, `write_hidden_file.py`), in `link-model-part` (`link_part.py`) and in their tests; the eleven thin model pages and the spine were re-marked through `link-model-part`. The spine schema comment states the rule.
- Wording: the glossary names the plan status Not Started (not active) and describes the feature item; `/shape-plan`'s SKILL.md, brief script and tests use Not Started.
- The round 3 records under `.garura/project/issues/720/` (review runs 2 and 3, design and thin re-mark evidence) and the ADR run folder under `.garura/project/issues/_adr/`.

## Scope checks

- [PASS] Matches the issue. Every changed file belongs to the feature: the update-plan play (#730, with the findings of #917 and the new-feature step of #931), the plan-branch script in the plan tool, the two new skills (author-plan-changes, track-plan-changes), the adapter's reopen-issue verb and close reason, link-model-part's slice step, the plan-update template, ontology v14, plan 717's Done marks with the new story #997 (now also Done), ADRs 061 and 062 with their pointers and index lines, the install manifest, #720's short-term records, and the fixes of rounds 1 to 3. The round 3 changes answer the review's findings: ADR 062 records the two decisions (the model written only after "approved"; a feature added to a slice in progress), and the play's ICE (`reference/ice.md`) was changed through `/edit-play` for them, as the pipeline rule asks for an intent change.
- [PASS] No scope creep. The /shape-slice, /shape-plan, /shape-eval and `create-play` files touched this round change only the Thin wording or the Not Started status word (one to ten lines each, tests included), which #997 and the glossary change ask for. The linter change is 9 lines plus a test and is the exception ADR 062 records. The agent files, the pipeline-next rule, the templates index and the install scope list are the wiring the new play and skills need.
- [NOTE] Reasonable size. The change is large (232 files, +107674) because it adds a whole play, two skills and a tool script with their tests, then the records of four review rounds. About 98,200 of the added lines (103 files) are #720's short-term records under `.garura/project/issues/720/`, and 2,185 more (34 files) are the ADR run folders under `.garura/project/issues/_adr/`. Three diff copies kept as review evidence make up most of that: `.garura/project/issues/720/review/run-3/pr.diff` (51,740 lines), `.garura/project/issues/720/review/run-2/pr.diff` (23,774 lines) and `.garura/project/issues/720/review/run-1/pr.diff` (9,442 lines). The code and prose to review is 74 files and about 6,910 lines under `core/`, plus ADR 061 and ADR 062 (153 lines each). Since round 3 the reviewable change is about 3,060 added lines in 100 files, of which 1,800 are records. Review the play (`core/components/plays/update-plan/`), the plan-branch script, ADR 062 and the linter exception first; the records are evidence only.
- [PASS] No stray artifacts. No `__pycache__`, `.pyc`, `.orig`, `.tmp` or scratch files are in the diff. No absolute path, scratch path or user name appears in any line this branch adds, taken as a whole (diff copies included). No TODO or FIXME was added under `core/` or `docs/`. No commented-out blocks were added.
- [NOTE] Absolute paths remain in one commit's history. Round 1 commit 8e09877e added `.garura/project/issues/720/review/lint-components.json` with absolute file paths in it (a machine path and a user name). The later commit 18f1ad00 scrubs it, so the file at HEAD, and the net diff of this PR, carry none. The commit 8e09877e itself still holds them in this branch's history. The product owner chose a new scrubbing commit over a history rewrite, so this is accepted and recorded here for the reviewer. It is not a defect of the final tree.
- [PASS] Copies agree. The platform adapter is copied into eight places (seven plays and the new track-plan-changes skill); all eight are byte-identical, and no round 3 commit touched them. The stamped `scoped_write_guard.py` in `/update-plan` is byte-identical to its source `core/components/plays/create-play/references/scoped_write_guard.py` and to the 14 other stamped copies. The thin wording is one text in every place that writes it (three scripts and a skill script), in the ontology and the spine schema comment, and the eleven re-marked pages all carry that one line with a matching `thin: true` on their spine entries (11 pages, 11 marks).

## Quality checks

- [PASS] Tests present. New tests came with the new behaviour and the fixes of each round, and all pass: update-plan scripts (37 tests with `unittest`; 13 added since round 3: `verify` writes its own record, a second run replaces its own questions, a slice in progress is named with its epic, the in-progress statuses match /shape-slice's list, a named capability the model lacks is asked and not swapped, a missing model index stops cleanly, the confirm screen warns "thin" and names the slice, the question screen shows four parts, `numbers`, `restore` (and its refusal of a folder outside the repository), and the guard's two cases), track-plan-changes (13), link-model-part (22), enrich-grounding (19), plan tool (35: 18 in `test_plan_branch.py`, 2 added this round for the check on the plan's own branch and for the second abort; 17 in `test_plan.py`), the linter (7 test files, 1 added for the declared exception), and the scripts of the plays whose wording moved (shape-slice 130 and 26 checks, shape-plan 11, 9, 12 and 21, shape-eval 41, create-play's `check_ice_workable` 46, all run directly because they are not `unittest` files).
- [PASS] Commits are clean. All 42 commits use conventional format except the merge of `origin/plan/717/base` into the branch (a merge commit); 41 name #720, and the merge is the one that does not. No commit carries a Claude trailer. The `chore(stm)` commits each record one run's records; every round 4 code commit is one concern (ADR 062, the plan tool, the play, the linter, the Thin wording, the model re-mark, the glossary wording, the plan marks).
- [PASS] No secrets. A scan of added lines for keys, tokens, passwords and private-key headers found nothing.
- [PASS] Docs in step. The plan tool README and docstring, the plan-update template, the ontology (v14), the spine schema comment, `direct-model-write.md` (a third declared-exception paragraph and the L-DMW-4 "Not a finding" case), the glossary, the `update-plan` SKILL.md (script table now 17 scripts, step evals SE-1 to SE-18, recovery entries 13, and every script named in the file), the `author-plan-changes` and `track-plan-changes` SKILL.md files, `link-model-part`'s SKILL.md, ADR 026 and 058 (forward pointers), ADR 060's status line and the ADR index moved with the change.
- [PASS] Nothing obviously broken. The component linter reports 37 findings (36 errors, 1 warning) across the whole component tree, the same count as round 3, none in a file this change touches; they are older findings in other plays and skills. `/update-plan` no longer raises the two L-DMW-4 errors its guard would have caused. ADR 062 checks valid. No failing tests found.
- [NOTE] The list of epic statuses that mean "in progress" has three copies. `/update-plan` (`place_feature.py`) and `/shape-slice` (`find_serving_slice.py`) are tied by a new test, so they cannot drift apart. A third copy in `persist_slice.py` (`/shape-slice`'s own) is not read by that test. ADR 062 says so and keeps it out of scope.
- [NOTE] The linter's exception for `/update-plan` is a fixed list of play names (`DMW4_DECLARED_EXCEPTIONS`, one name). A later play that needs the same exception must be added to that list and named in `direct-model-write.md`, with an ADR. This is deliberate (a declared exception, like those of ADR 031), not a defect.
- [NOTE] ADR 062 holds one stale phrase. In its third finding it says the code of `go` is "not yet committed on this branch"; commit e6520ba5 has since committed it. The ADR is accepted, so the phrase is left as written; it does not change the decision.
- [NOTE] Follow-up already filed. ADR 061 notes that start-change cuts a plan's branch through the same script once #989 is built; until then ADR 060's line about start-change stands. This is known and planned, so it is not a defect of this change. (#997, the Thin wording, was listed here in round 3; it is built in this change and marked Done in plan 717.)

## Blocking findings

None.
