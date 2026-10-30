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
