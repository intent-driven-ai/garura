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
