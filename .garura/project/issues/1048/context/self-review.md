# Self-review: issue #1048 (ADR 067: a play finds a feature's story by the issue the product model names)

Branch: `feature/1048-adr-find-story-through-model` against `main`.
Rules used: `standards/rules/self-review.md` (Phoenix memory), read through the memory tool. The resolved choice is in `.garura/project/issues/1048/context/resolved-rules.json`.
This is an information list. It is not the approve or reject gate; `validate-work` does that.

## What the change is

A new decision record, ADR 067. It says: when no plan file marks a feature's story, a play finds the story by the issue the product model names for that feature (it must be a Story; closed means the feature is already built), and never by title. It amends ADR 056 section 2, ADR 048 section 3 (second bullet) and ADR 049 section 2. The ADR index lists it. The rest is run records for the ADR run.

2 commits, 25 files, +1858 / -6. About 1070 of those lines are copies of two memory files kept as run evidence (the ontology, 893 lines; the ADR template, 178 lines).

## Scope checks

- **Matches the issue.** PASS. ADR 067 is the one new decision file for #1048 and records exactly the three amendments the issue names.
- **No scope creep.** PASS. The only edits to existing ADRs are one line each:
  - `docs/adr/048-the-product-model-and-the-work-are-two-layers.md`: Status line only (1 line changed).
  - `docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md`: Status line only (1 line changed).
  - `docs/adr/056-an-epic-and-a-story-are-marked-by-their-issue-type-with-no-label.md`: Status line only (1 line changed).
  Each is a forward pointer to ADR 067 with the part it amends; the body of each ADR is untouched. `docs/adr/_index.md` gains the ADR 067 row and "67" in the Status column of rows 048, 049 and 056 (3 rows changed, 1 added). Nothing outside `docs/adr/` and `.garura/project/issues/` changed. The run's own guard report (`.garura/project/issues/_adr/20261112T052058Z/guard-report.json`) shows no violations.
- **Reasonable size.** PASS. The one decision file is 144 lines. The large line count is the two memory copies kept as evidence, which are not meant to be read.
- **No stray artifacts.** NOTE, not a problem. The run records hold working drafts (`adr-draft.md`, `adr-check.json`, `porcelain-before.txt`, `porcelain-after.txt`, `hashes-before.json`). They follow the pattern of earlier ADR runs under `.garura/project/issues/_adr/`. No debug prints, commented-out blocks or scratch outside those folders. `.garura/project/issues/1048/context/resolved-rules.json` is still untracked; it is this review's own record and is left for the play to decide.

## Quality checks

- **Tests present.** PASS (none needed). Documents only, no code or play behavior changes. The ADR says plainly that the play changes land later on PR #1047's branch.
- **ADR lint.** PASS. `adr.py lint --adr` returns valid with no problems for ADR 067, and also for ADR 048, 049 and 056 after their pointers.
- **Pointers are true.** PASS. The quoted text exists where the pointers say: ADR 048 section 3 has "There is one story for each feature in each epic" (line 45); ADR 049 section 2 has "one story for each feature of the slice" (line 31); ADR 056 has "A play finds an epic or a story by the plan file" under section 2 (line 27).
- **Index in step.** PASS. `docs/adr/_index.md` rows for 048, 049, 056 and 067 match the Status lines of the files.
- **Commits are clean.** PASS. Two conventional commits, each naming #1048: `docs(adr): ...` for the ADR, pointers and index, and `chore(stm): ...` for the start-work record. No attribution lines in either message.
- **No secrets.** PASS. Search of the diff for keys, tokens and credentials found none.
- **No personal references.** PASS. No home folder, temp path, account name or email in any added line. The only person name is "Kapil Viren Ahuja", in ADR 067's "Decided by" line, which matches the other accepted ADRs (for example ADR 048 and ADR 056). The same name also appears twice as `accepted_by` in the run record `decision.yaml` and `adr-manifest.json`; that is the person who accepted, recorded by the play, and is not in a shipped document.
- **Docs in step.** PASS. The ontology and spine schema changes the ADR lists are named as follow-up work for `/specify-ontology`, not done here, which matches the scope.
- **Nothing obviously broken.** PASS. No TODO or FIXME added. ADR 067 says openly that PR #1047 and the ontology disagree with it until those follow-ups land.

## Findings

1. NOTE (not stopping): the Status lines of ADR 048 and ADR 049 are now very long single lines. This matches how earlier amendments were added to the same lines, so it follows the existing pattern.
2. NOTE (not stopping): the run folder holds full copies of the ontology and the ADR template. They add review weight but no risk; they are the evidence that the draft was checked against the version of the ontology in force on 2026-11-12.

Blocking findings: none.

Verdict: clear to raise.
