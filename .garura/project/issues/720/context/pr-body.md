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

### How it was checked

Unit tests: update-plan 19, plan tool 29, track-plan-changes 8, link-model-part 21, change_lines 19, the adapter 58, the install 75, edit-ontology 11 — all pass. A test run in a throwaway copy covered every case of the design. A live run on plan 717 with real GitHub (fa6f514, merged in) landed #720 and #730 In Progress and #931's feature fn-931, and its agreement check held.

### Self-review

# Self-review: #720 (manage a plan with /update-plan)

Rules: the base self-review rules (`~/.phoenix/core/memory/standards/rules/self-review.md`, no project override), resolved in `resolved-rules.json`.
Diff: `origin/plan/717/base...HEAD` on `plan/717/720-update-plan` (14 commits, 72 files, +8104 / -83).
This checklist is information for the reviewer. It is not the approve/reject gate.

Summary: 0 blocking findings, 2 notes for the reviewer.

## Scope checks

- [PASS] Matches the issue. Every changed file belongs to the feature: the update-plan play (#730, with the findings of #917 and the new-feature step of #931), the plan-branch script in the plan tool, the two new skills (author-plan-changes, track-plan-changes), the adapter's reopen-issue verb and close reason, link-model-part's slice step, the plan-update template, ontology v14, plan 717's Done marks with the new story #997, and #720's short-term records.
- [PASS] No scope creep. The agent files (product-os-keeper, project-orchestrator), the pipeline-next rule, the templates index and the install scope list are the wiring the new play and skills need. The managing-work guide edit belongs to the feature's last docs commit.
- [NOTE] Reasonable size. The change is large (72 files, +8104) because it adds a whole play, two skills and a tool script with their tests. About 2,500 of the added lines are #720's short-term records (memory copies, ontology drafts, build design) under `.garura/project/issues/720/`. Review the play, the two skills and the plan-branch script first; the records are evidence only.
- [PASS] No stray artifacts. No `__pycache__`, `.pyc`, `.orig`, `.tmp` or scratch files are in the diff. The one untracked file, `resolved-rules.json`, is this review's own record. No scratch path and no user name appear in any added line. No TODO or FIXME was added under `core/`.
- [PASS] Copies agree. The platform adapter is copied into nine places (eight plays and the new skill); all nine have the same content (same checksum), so the reopen-issue verb and close reason are the same everywhere.

## Quality checks

- [PASS] Tests present. New tests came with the new behaviour and all pass when run with `unittest`: update-plan scripts (19 tests), track-plan-changes (8), link-model-part (21), plan tool (29). The adapter's own test file was updated for the new verb.
- [PASS] Commits are clean. All 14 commits use conventional format; 13 name #720. The one commit without #720 is the merge of `origin/plan/717/base` into the branch (a merge commit, not a change of concern). No commit carries a Claude trailer.
- [PASS] No secrets. A scan of added lines for keys, tokens, passwords and private-key headers found only ordinary words (for example "token" in prose about parsing and usage records).
- [PASS] Docs in step. The plan tool README, the plan-update template and its index entry, the ontology (v14 with its log line), the pipeline-next rule, the adapter's SKILL.md and both verbs files, and the managing-work guide all moved with the change.
- [PASS] Nothing obviously broken. The component linter reports 37 findings across the whole component tree, none in a file this change touches; they are older findings in other plays. No new leftover paths found.
- [NOTE] Follow-up already filed. The pages and scripts that still say the Thin line names /shape-slice move to the new wording in #997, now in plan 717 as Not Started. This is known and planned, so it is not a defect of this change.

## Blocking findings

None.
