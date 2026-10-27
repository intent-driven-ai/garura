The run records of a dry run of `/shape-plan 788`, for #879's last "done when" item. The product owner asked for a dry run before landing, and then: "just land it.. dont touch the existing plans".

Part of #879 (plan #788). No plan file, no source file and no product-model file changes.

## What the dry run showed

- The installed plan play (with #879's change, PR #894) found epic #794 as type Epic holding exactly its slice's three stories (#795, #818, #798), with no misplaced work and nothing to move out.
- The write step ran against a local copy of the tracker read from GitHub: 0 created, 0 updated, 0 moved out; the copy came out byte for byte as it went in. The plan-file step ran on a copy: no change.
- The plan check, the tracker check and the write guard all read ok; the play's Done means (D1–D5) held over the dry-run records; the second-run scenario (no copies) held.
- Skipped, because they cannot be undone: writes to GitHub (none were needed), the plan-file commit (no change), and landing the run. The full record: `.garura/project/issues/879/simulation/shape-plan/dry-run.md`.

Recorded alongside: #896, the enhancement "/shape-plan stops when the business intent already has a plan, and does not run again" (business intent #717).

## Self-review

# Self-review: #879, dry run of /shape-plan 788 (plan/788/879-shape-plan-rerun)

Rules: ~/.garura/core/memory/standards/rules/self-review.md (base file, no project override).
Diff reviewed: `git diff plan/788/base...HEAD` (4 commits, 38 files, 1303 added lines, 54 removed).
Scope given by the product owner: "just land it.. dont touch the existing plans". This change carries only the records of a dry run of `/shape-plan 788`. The dry run wrote nothing to the tracker and nothing to the plan file.

Verdict: ready to raise. No finding stops the raise. Three notes for the reviewer are listed at the end.

## Scope checks

- [PASS] Matches the issue. Every changed file sits under `.garura/project/issues/879/`: the start-change records, the shape-plan run records (`context/shape-plan/**`, the template copies) and the simulation records (`simulation/shape-plan/**`). The commit-change records (analysis, commits, mappings, porcelain) are the run's own state.
- [PASS] No plan file touched. A path filter over the diff finds nothing under `.garura/project/plans/`. Plan 788 is not changed, as the product owner asked.
- [PASS] No source touched. Nothing under `core/`, nothing under `.garura/product/` (the product model), and nothing under the installed copies in `.claude/` or `.garura/core/`.
- [PASS] No scope creep. Zero files outside `.garura/project/issues/879/`. The dry-run record states the run made 0 created, 0 updated and 0 moved-out tracker items, that the tracker copy is byte for byte unchanged, and that the plan-file copy matches its before-hash.
- [PASS] Reasonable size. 38 files, all run records. Large in lines, but nothing in it needs line-by-line review; the reviewer reads the dry-run summary (`simulation/shape-plan/dry-run.md`) and the stop-condition record.
- [PASS] No stray artifacts. No cache files, compiled files, binary files or editor files. The working tree is clean.

## Quality checks

- [PASS] Tests present. No behavior changes and no code in the diff, so no tests apply. The tests for the play were run in an earlier change.
- [PASS] Commits are clean. All four commits are `chore(stm): ...` and end with (#879). No Claude attribution line in any commit message.
- [PASS] No secrets. A scan of the added lines for tokens, keys, private-key headers, passwords and bearer strings finds nothing, and there are no email addresses.
- [PASS] No real names. The persona lines in the drafts say "The product owner" and the later plays; no person is named. The one personal detail is the machine user folder in absolute paths (see notes).
- [PASS] Docs in step. Nothing user-facing or interface-related changes, so no docs apply.
- [PASS] Nothing obviously broken. No TODO or FIXME blocks the change's goal. The approval record holds the product owner's typed yes for the dry run and the hashes of the brief, work items and drafts it covers.

## Notes for the reviewer (none of them stops the raise)

- Absolute paths such as `/Users/<machine user>/cto/builder/garura/...` appear in `clean_ice` fields of the shape-plan records. Earlier issue records on the base branch already carry the same kind of path, so this adds no new kind of exposure. No real person's name appears.
- `context/issue.json` now shows #879's title as the round 2 wording ("/shape-plan stops when an epic holds work that is not its slice's: an epic stands for one slice"); this is a record of the issue as it reads now, not a change to the issue.
- The approval's typed yes covers a dry run ("run it as a dry run to test the play before we land this work"). Because it was a dry run, no real write happened. If the play is run for real later, it needs its own typed yes.
