The plan 788 chores, in one change by the product owner's choice: one branch, one review, one merge. Each issue has its own commit(s).

Closes #841, #851, #854, #837, #855 and #833 (on merge into the plan branch; merge-change closes #841, the others are closed by hand with a note).

## What changes

- **#841 (P1 bug): the review sees every file of a PR.** It read the file list with the one host command that stops at 100 files, and said nothing. It now takes the paths from the diff itself, and compares the count with the PR's own `changedFiles`; when they differ it stops with a plain message (exit 3). Tested on a 150-file PR. This PR is itself reviewed with the fixed script (the harness was installed from this branch first).
- **#851: the review scanner stops flagging ADRs and run records.** A changed ADR or a run record gets no finding (the reason is in `pr.md`). The real cause of the old FE-16 finding is fixed too: the scanner read a `+++` line inside a saved diff as a file name. Its first tests are added.
- **#854: the asking rule leaves memory.** It moves to `core/components/skills/_shared/asking-a-person.md`, laid beside the installed skills like the plays' shared close. Only five parts use it and only those are linted: /edit-ontology, /shape-slice, `author-product-ontology`, `find-slice-gaps`, `author-slice-brief`. The approval template stands alone and names no rule. /shape-slice (C18, F18, REC18, SE-22) and /edit-ontology are recompiled with /edit-play. #831 is closed as not planned.
- **#837: /shape-scope and /shape-roadmap are dropped** (ADR 053, accepted). The two plays and their skills `author-scope` and `author-roadmap` are deleted, and every reference outside the ADRs is removed.
- **#855: the old-chain parts are marked stale, and no install ships them.** `stale: true` with a note on 13 plays (the seven design lenses, build-epic, validate-epic, release-epic, release-increment, learn-outcomes, refactor-code), 24 skills and 3 agents. Both installers skip a stale or deprecated part. No live part names a stale part.
- **#833: the deprecated parts are removed.** 3 agents and 28 skills deleted; no `deprecated: true` is left. Live text names the lint tool by its path.
- **The harness install carries /shape-slice and its skills.** The harness scope never listed them; a clean install removed them from this repo. Now it lists them, with a test.

## For the product owner's eye

1. ADR 053, one line in §5: `/intent` and `/adr` now read `/discover-intent` and `/record-decision` (their current names), so the old-name check passes. The meaning is the same.
2. /shape-slice: when the shared rule file is missing, the run says so in the brief and goes on; it raises no memory update, because the rule is no longer memory.
3. `check-pr-quality` gained `allowed-tools: Read, Write, Bash, Glob, Grep`.
4. A guard-copy test floor went from 14 to 12 copies: two copies went with the deleted plays.
5. Six plays failed the play check before this change (check-change, create-loop, edit-loop, edit-play, install-garura, uninstall-garura; create-play too). This change adds no gap to them. They are not fixed here.

## Checks

| Check | Result |
|---|---|
| Hidden acceptance checks, written before the build and kept from the builder | 30 / 30 pass |
| Script tests (35 files) and install tests | all pass (install: 54 tests) |
| lint-components tests | all pass |
| Old-name check | passes |
| Play check (lint_play) | no new gap on any play |
| Component lint errors | 118 → 37; no asking-a-person error |

Filed on the way: #857 (commit-change never reads its own record as clean).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
