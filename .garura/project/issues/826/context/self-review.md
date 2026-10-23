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
