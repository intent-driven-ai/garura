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

1. /shape-slice: when the shared rule file is missing, the run says so in the brief and goes on; it raises no memory update, because the rule is no longer memory.
2. `check-pr-quality` gained `allowed-tools: Read, Write, Bash, Glob, Grep`.
3. A guard-copy test floor went from 14 to 12 copies: two copies went with the deleted plays.
4. Six plays failed the play check before this change (check-change, create-loop, edit-loop, edit-play, install-garura, uninstall-garura; create-play too). This change adds no gap to them. They are not fixed here.

## Review round 1 (rejected; P2 and P3 fixed, P4 to a chore)

The product owner's word: reject; fix every P2 and P3; the P4s go to one chore (#859).

- DR-1 (P2): ADR 053 is back exactly as accepted. The old-name check skips it through a named set (`QUOTING_ADRS`), because it quotes old names on purpose; tested.
- H1, H2, M3 (P3): ADR 054, accepted, records the two decisions: the last deprecated parts are deleted (amends ADR 050 §3 and ADR 035 §10), and the asking rule is a shared skill file, not memory (amends ADR 039 §9).
- M1 (P3): the ADR rows in `pr.md` (ARCH-23, DOC-04, DOC-05) say they give no finding on `docs/adr/**`.
- Q-1 (P3): BE-19 and SEC-18 fire on real SQL and permission code, not on plain words; tested both ways. The proof rules on the four tool files were run and recorded (`.garura/project/issues/841/review/q1-evidence.md`); four real problems were fixed (a 64-line function split, a flag name, a test that left temporary folders, a constant name).
- Answered, not open: M2 (the template stands alone, by the product owner's decision) and DR-3 (the pointers are on the base).
- Found on the way: #860 (P1) — installed parts read Garura's source tree at run time. It is fixed right after this PR.

## Checks

| Check | Result |
|---|---|
| Hidden acceptance checks, written before the build and kept from the builder | 34 / 34 pass |
| Script tests (35 files) and install tests | all pass (install: 54 tests) |
| lint-components tests | all pass |
| Old-name check | passes |
| Play check (lint_play) | no new gap on any play |
| Component lint errors | 118 → 37; no asking-a-person error |

Filed on the way: #857 (commit-change never reads its own record as clean), #859 (the review's P4s), #860 (P1, installed parts read the source tree).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
