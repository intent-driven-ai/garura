Ontology v10 keeps the IDD routing table true (`docs/philosophy/idd-principles.md`). In v9 a Story said "what must never happen", and the builder reads the Story, so failure conditions reached the builder. v10 fixes that.

Closes #826 (on merge into the plan branch, by merge-change).

## What changes

- **Story.** Holds the goal, the constraints, the expectations and a new **Context guidance** property (the four Context lines of its two ICE). It never holds a failure or a recovery condition. The build play's context sub-agent reads the guidance, collects the context at run time and puts it in the issue's short-term memory; the builder reads that and never opens an ICE page.
- **Slice.** Each slice has one hidden file, `.garura/project/plans/<plan-id>/evals/<slug>/failure-and-recovery.md`: each story's failure conditions, with exactly one recovery condition each, marked "the builder can fix this alone" or "a person must decide". The eval is read at two times: the eval play reads the epic, the stories and the hidden file before the build; the running eval reads the eval, the usage guide and the recovery conditions. A failure gives a handoff plan that names the symptom, never the condition.
- **Plan.** The plan play writes the hidden file from the same two ICE as each story, so each ICE is interpreted once.
- **ICE.** Its parts do not change. Its rule now names the plan play as the one reader of the ICE; no work item carries it.
- Questions: Q26 and Q29 changed; Q32–Q35 added.
- `standards/rules/expectation-generation.md` gains "A story's recovery (product ICE)".

## Checks

| Check | Result |
|---|---|
| Ontology check | valid |
| Change check | scope ok (Story, Slice, Plan only), version 9 → 10 with one log line, no real names |
| Review round 1 | reviewer asked for fixes: ICE rule names the plan play as reader; running eval reads only recovery parts; Story says 'limits'; story recovery added to `standards/rules/expectation-generation.md`; a real first name replaced |
| Checkpoints | questions, kinds (after one change), links: all agreed by the product owner |

## Self-review

# Self-review: issue 826 (ontology v9 to v10), refreshed after review round 1

Rules used: the resolved self-review rules for this project.
Diff: `git diff plan/788/base...HEAD`.

Result: 0 blocking findings. The review is for information only. The check-change play gives the verdict.

## Scope checks

- [PASS] Matches the issue. Two product files changed. The product ontology schema moves from version 9 to 10 so that failure conditions stay off the Story and the IDD routing table holds. The expectation-generation rules gain a section for a Story's recovery. Both serve the issue.
- [PASS] No scope creep. The product owner's review word put ICE in the touched kinds, and the round 1 wording fixes follow that word. All other changed files are run records for issue 826 in its short-term memory folder. One run record for issue 816 changed: a real first name was replaced by "the product owner". This is a clean-up that the repo rules require.
- [PASS] Reasonable size. Two product files: 69 lines added, 27 removed. A person can review it in one sitting.
- [PASS] No stray artifacts. No debug prints, no commented-out blocks, no scratch files in the product change.

## Quality checks

- [PASS] Tests present. These are rule documents, not code. Their checks were run: the ontology check reads valid, and the change check reports scope, version and names all true.
- [PASS] Commits are clean. Ten commits: one feat(ontology), one fix(ontology), one docs(standards) and seven chore(stm). Each has one concern and each names issue 826.
- [PASS] No secrets. A scan of added lines found no credentials, tokens or home-folder paths.
- [PASS] Docs in step. The ontology now agrees with the IDD routing table in the philosophy docs. The new Story recovery section is in the expectation-generation rules.
- [NOTE] Round 1 fixes (commit 8bf0160b): the ICE rule names the plan play as the reader of failure conditions; the running eval reads only the recovery parts; the word "limits" is used; a real first name became "the product owner". Reviewers should read these lines for plain wording.
- [NOTE] The plan play and the eval play must still follow Q33 to Q35 (hidden file `failure-and-recovery.md`). Their own changes are outside this issue and are not in this diff.

## Blocking findings

None.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
