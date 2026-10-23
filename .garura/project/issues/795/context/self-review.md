# Self-review: issues 795 and 836

Rules used: the resolved self-review rules file (base copy).
Diff: plan/788/base...HEAD (15 commits, 111 files).

## Scope checks

- [PASS] Matches the issues. The change builds the new /shape-slice (795) and drops /next (836). Both issues are named in the commits and the PR will close both.
- [PASS] No scope creep. Every file maps to one of the two issues: the new play and its scripts, the two schemas, the keeper agent, the deleted play and skills, the pointer clean-up in other plays, docs and ADR 051. Related work was filed apart as follow-ups 837, 838 and 839.
- [REVIEW] Size. 111 files is large, but most of it is deleted files and one-line pointer edits. The two issues were grouped on purpose. Reviewers should read the new play and its scripts first.
- [PASS] No stray artifacts. No debug prints, scratch files or commented-out blocks found in the diff. The eval files sit in the issue's evidence folder, which is the right place.

## Quality checks

- [PASS] Tests present. The new scripts carry their own tests. Acceptance check: 93 passed, 0 failed. All play and skill tests pass.
- [PASS] Commits are clean. All 15 commits use conventional format, each is one concern, and each names the issue.
- [PASS] No secrets. A scan of the added lines found no keys, tokens or credentials.
- [PASS] Docs in step. Component docs, the philosophy page, CLAUDE.md, AGENTS.md, managing-work and the glossary were updated. No live reference to the deleted play, skills, shelf or page remains outside the ADRs.
- [PASS] Nothing obviously broken. lint_play passes on shape-slice. lint-components shows 124 errors, down from 135, and none are on shape-slice. The old-name check finds 0.
- [PASS] Plain wording and paths. No absolute home paths in the new play files.

## Findings

Blocking findings: none.
Notes for the reviewer: the size item above. The 124 lint errors are old and come from other parts.
