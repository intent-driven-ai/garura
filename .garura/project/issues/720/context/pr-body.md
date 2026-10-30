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

### Round 3 (after round 2's reject)

The remaining design P2 findings are fixed: ADR 061 (accepted by the product owner) records that a plan's branch is cut by the play that starts its work, main first, amending ADR 060; a new feature is now placed by a script and the placement skill, and the model sub-agent drafts nothing itself (the page skill writes the thin ICE at the landing, from the person's words). The scanner's path-only P2 rows have their evidence in the review folder (`code-evidence.md`).

### How it was checked

Unit tests: update-plan 19, plan tool 29, track-plan-changes 8, link-model-part 21, change_lines 19, the adapter 58, the install 75, edit-ontology 11 — all pass. A test run in a throwaway copy covered every case of the design. A live run on plan 717 with real GitHub (fa6f514, merged in) landed #720 and #730 In Progress and #931's feature fn-931, and its agreement check held.

### Self-review

# Self-review: #720 (manage a plan with /update-plan), round 3

Rules: the base self-review rules (`~/.phoenix/core/memory/standards/rules/self-review.md`, no project override), resolved in `resolved-rules.json`.
Diff: `origin/plan/717/base...HEAD` on `plan/717/720-update-plan` (30 commits, 154 files, +49999 / -87). This re-raise of PR #998 follows the round 2 review.
This checklist is information for the reviewer. It is not the approve/reject gate.

Summary: 0 blocking findings, 4 notes for the reviewer.

## Since round 2

The branch adds three changes and the records of the round 2 review:

- ADR 061 (accepted, 2026-10-30). It amends ADR 060: the plan's branch is cut by the play that starts the plan's work (/update-plan now, start-change once #989 is built), main first, through the plan tool's `plan_branch.py`. ADR 060 gained a pointer to it, and the ADR index a line. The ADR check (`adr.py lint`) reads valid.
- A new feature is placed by fixed rules, not by the model sub-agent. The new script `core/components/plays/update-plan/scripts/place_feature.py` fills the capability (the one the person named, else the one that shares an issue number with the item's parent), the slice (the one slice that serves the intent), the feature id and the one-line, and turns what no rule settles into a question for the person. It drafts no ICE; the page skill writes the thin ICE at the landing, from the person's words. The play's `SKILL.md` (Step 3 and Step 8), the `product-os-keeper` agent route and the `author-plan-changes` skill moved with it. Three tests were added to the play's script tests.
- The round 2 records: the ADR run folder under `.garura/project/issues/_adr/`, and the review, code evidence and commit records under `.garura/project/issues/720/`.

## Scope checks

- [PASS] Matches the issue. Every changed file belongs to the feature: the update-plan play (#730, with the findings of #917 and the new-feature step of #931), the plan-branch script in the plan tool, the two new skills (author-plan-changes, track-plan-changes), the adapter's reopen-issue verb and close reason, link-model-part's slice step, the plan-update template, ontology v14, plan 717's Done marks with the new story #997, ADR 061 with its pointer in ADR 060 and the index line, #720's short-term records, and the fixes of rounds 1 and 2. The play's ICE (`reference/ice.md`) is unchanged: C9 and C11 already say a new feature is placed under its capability and slice and that model changes go through the model sub-agent and its skills; the new script only makes that placement mechanical.
- [PASS] No scope creep. The agent files (product-os-keeper, project-orchestrator), the pipeline-next rule, the templates index and the install scope list are the wiring the new play and skills need. The managing-work guide edit belongs to the feature's last docs commit. The round 1 and round 2 fixes touch only files the feature already added, apart from the component linter (a round 1 fix, 6 lines, named in #720's commits) and ADRs 060 and 061, which record the decision the review asked for.
- [NOTE] Reasonable size. The change is large (154 files, +49999) because it adds a whole play, two skills and a tool script with their tests, then the records of three review rounds. About 42,960 of the added lines (82 files) are #720's short-term records under `.garura/project/issues/720/`, and 927 more (16 files) are the ADR run folder under `.garura/project/issues/_adr/`. Two diff copies kept as review evidence make up most of that: `.garura/project/issues/720/review/pr.diff` (23,774 lines) and `.garura/project/issues/720/review/run-1/pr.diff` (9,442 lines). The code and prose to review is about 5,930 lines in 50 files under `core/`, plus ADR 061 (153 lines). Review the play, the two skills, the plan-branch script, `place_feature.py` and ADR 061 first; the records are evidence only.
- [PASS] No stray artifacts. No `__pycache__`, `.pyc`, `.orig`, `.tmp` or scratch files are in the diff. No scratch path and no user name appear in any line this branch adds, taken as a whole (the three-dot diff and the files at HEAD both read clean, diff copies included). No TODO or FIXME was added under `core/` or `docs/`.
- [NOTE] Absolute paths remain in one commit's history. Round 1 commit 8e09877e added the review file `.garura/project/issues/720/review/lint-components.json` with absolute file paths in it (a machine path and a user name). The later commit 18f1ad00 scrubs it, so the file at HEAD, and the net diff of this PR, carry none. The commit 8e09877e itself still holds them in this branch's history. The product owner chose a new scrubbing commit over a history rewrite, so this is accepted and recorded here for the reviewer. It is not a defect of the final tree.
- [PASS] Copies agree. The platform adapter is copied into eight places (seven plays and the new track-plan-changes skill); all eight have the same content, and no round 2 commit touched them, so the reopen-issue verb and close reason are the same everywhere.

## Quality checks

- [PASS] Tests present. New tests came with the new behaviour and the fixes of each round, and all pass when run with `unittest`: update-plan scripts (24 tests, 3 added since round 2 for `place_feature.py`: capability, slice and id by rule; an existing story keeps its number; what no rule settles becomes a question), track-plan-changes (10), link-model-part (21), plan tool (33: 16 in `test_plan_branch.py` and 17 in `test_plan.py`). The adapter's own test file was updated for the new verb in the first round.
- [PASS] Commits are clean. All 30 commits use conventional format except the merge of `origin/plan/717/base` into the branch (a merge commit); 29 name #720, and the merge is the one that does not. No commit carries a Claude trailer. Several `chore(stm)` commits record separate play runs; each is one concern (one run's records).
- [PASS] No secrets. A scan of added lines for keys, tokens, passwords and private-key headers found nothing.
- [PASS] Docs in step. The plan tool README, the plan-update template and its index entry, the ontology (v14 with its log line), the pipeline-next rule, the adapter's SKILL.md and both verbs files, the track-plan-changes SKILL.md, the managing-work guide, and (since round 2) the update-plan SKILL.md script count and table, the `product-os-keeper` route, the `author-plan-changes` field table, ADR 060's status line and the ADR index all moved with the change.
- [PASS] Nothing obviously broken. The component linter reports 37 findings (36 errors, 1 warning) across the whole component tree, none in a file this change touches; they are older findings in other plays and skills. ADR 061 checks valid. No leftover paths or failing tests found.
- [NOTE] Follow-up already filed. The pages and scripts that still say the Thin line names /shape-slice move to the new wording in #997, now in plan 717 as Not Started. ADR 061 also notes that start-change cuts a plan's branch through the same script once #989 is built; until then ADR 060's line about start-change stands. Both are known and planned, so neither is a defect of this change.

## Blocking findings

None.
