Ontology v10 keeps the IDD routing table true (`docs/philosophy/idd-principles.md`). In v9 a Story said "what must never happen", and the builder reads the Story, so failure conditions reached the builder. v10 fixes that.

Closes #826 (on merge into the plan branch, by merge-change).

## What changes

- **Story.** Holds the goal, the constraints, the expectations and a new **Context guidance** property (the four Context lines of its two ICE). It never holds a failure or a recovery condition. The build play's context sub-agent reads the guidance, collects the context at run time and puts it in the issue's short-term memory; the builder reads that and never opens an ICE page.
- **Slice.** Each slice has one hidden file, `.garura/project/plans/<plan-id>/evals/<slug>/failure-and-recovery.md`: each story's failure conditions, with exactly one recovery condition each, marked "the builder can fix this alone" or "a person must decide". The eval is read at two times: the eval play reads the epic, the stories and the hidden file before the build; the running eval reads the eval, the usage guide and the recovery conditions. A failure gives a handoff plan that names the symptom, never the condition.
- **Plan.** The plan play writes the hidden file from the same two ICE as each story, so each ICE is interpreted once.
- Questions: Q26 and Q29 changed; Q32–Q35 added. No other kind changes; the ICE kind does not change.

## Checks

| Check | Result |
|---|---|
| Ontology check | valid |
| Change check | scope ok (Story, Slice, Plan only), version 9 → 10 with one log line, no real names |
| Checkpoints | questions, kinds (after one change), links: all agreed by the product owner |

## Self-review

# Self-review: issue 826 (ontology v9 to v10)

Rules used: the resolved self-review rules for this project.
Diff: `git diff plan/788/base...HEAD`.

Result: 0 blocking findings. The review is for information only. The check-change play gives the verdict.

## Scope checks

- [PASS] Matches the issue. The one product file changed is the product ontology schema. It moves from version 9 to 10 so that failure conditions stay off the Story and the IDD routing table holds. Story, Slice and Plan changed. Questions Q26 and Q29 changed. Questions Q32 to Q35 are new.
- [PASS] No scope creep. The other changed files are run records for issue 826 in its short-term memory folder (drafts, checks, decisions, commit record). They belong to this run.
- [PASS] Reasonable size. One product file: 46 lines added, 23 removed. A person can review it in one sitting.
- [PASS] No stray artifacts. No debug prints, no commented-out blocks, no scratch files in the product change.

## Quality checks

- [PASS] Tests present. This is a schema document, not code. Its checks were run: the ontology check reads valid, and the change check reports scope, version and names all true.
- [PASS] Commits are clean. Three commits: one feat(ontology) and two chore(stm). Each has one concern and each names issue 826.
- [PASS] No secrets. A scan of added lines found no credentials, tokens or home-folder paths.
- [PASS] Docs in step. The change makes the ontology agree with the IDD routing table in the philosophy docs. That table needed no edit.
- [NOTE] Version log: the ontology keeps one log line for each version. The check script confirmed version is up by one. Reviewers should read the new log line for plain wording.
- [NOTE] The plan play and the eval play must now follow Q33 to Q35 (hidden file `failure-and-recovery.md`). Their own changes are outside this issue and are not in this diff.

## Blocking findings

None.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
