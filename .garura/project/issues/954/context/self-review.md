# Self-review for #954 (one epic for each plan)

Branch: feature/954-one-epic-per-plan, against main. Rules: the base self-review rules,
resolved to `standards/rules/self-review.md` (no project override; see
`.garura/project/issues/954/context/resolved-rules.json`).

This is an information checklist for the reviewer. It does not approve or reject the change.

## What the change is

It records one decision, ADR 069 ("The plan is where the product model meets the work"),
accepted by the product owner after five rounds. It retires ADR 049 and ADR 057 in full and
changes parts of 14 other ADRs. It changes no model file, play, skill, agent or tool. The work
the decision creates is listed in the ADR's "Work This Creates" section and is not in this PR.

39 files, +2400 / -32, in 2 commits. Where the lines are:

| Part | Files | Notes |
|------|-------|-------|
| ADR 069 | 1 (272 lines) | the decision itself |
| Older ADRs | 16 | one line each: the Status line only |
| ADR index | 1 | rebuilt; one new row, 16 changed rows |
| Run records for the ADR run | 18 | under `.garura/project/issues/_adr/20261112T093635Z/` |
| Run records for the issue | 5 | under `.garura/project/issues/954/context/` |

## Scope checks

- [ok] Matches the issue. The change is the decision #954 asked for (one epic for a plan, which
  needed the plan-and-model split settled first). Nothing in it implements that decision.
- [ok] No scope creep. Every changed file is under `docs/adr/` or under
  `.garura/project/issues/954/` or `.garura/project/issues/_adr/`. No file in `core/`,
  `.claude/`, `CLAUDE.md` or `docs/` outside `docs/adr/` is touched.
- [ok] Only forward pointers on the 16 older ADRs. Each of the 16 diffs is 1 line added and
  1 line removed, and the line is the Status line. For ADR 049 and ADR 057 the status now reads
  "Superseded by ADR 069". The other 14 read "amended in part by ADR 069" with the part named.
  The design-adr guard report lists no violations.
- [ok] The index is current. Rebuilding it with the design-adr script gives a file identical to
  `docs/adr/_index.md`.
- [ok] The ADR passes its lint (`valid: true`, no problems).
- [note] Size. The change is large by line count, but about 1,950 of the 2,400 lines are run
  records. The part to read is ADR 069 (272 lines) and the 16 one-line Status edits.
- [note] The run records include two copies taken from memory for the ADR run: the product
  ontology (about 890 lines) and the ADR template (about 180 lines). They are run evidence in the
  same way earlier "record ... memory copies" commits are, so they are kept. They are not
  standards to review.
- [note] `.garura/project/issues/954/context/resolved-rules.json` and this file are not yet
  committed. They are written by this step, so the tree is not clean until the play's next
  commit step.
- [ok] No stray artifacts. No debug output, commented-out blocks or scratch files. Session
  stamps and other status files are not in the diff.

## Quality checks

- [ok] Tests. None are needed: the diff is documents and run records only. There is no code.
- [ok] Commits. Two commits, both in conventional format and both naming #954:
  `chore(stm): record start-work workspace context (#954)` and
  `docs(adr): ADR 069 — the plan is where the product model meets the work (#954)`.
- [ok] No attribution lines. No tool-credit line and no co-author line in the commits or
  in any added text. The PR body must not add one.
- [ok] No secrets. A scan of the added lines for keys, tokens, passwords and private-key headers
  found nothing.
- [ok] No personal references beyond the naming convention. The only personal name in the diff
  is the product owner's name in the "Decided by" line of ADR 069 and in the `accepted_by` field
  of the ADR run records. No absolute path, home folder, temporary path or account name is in the
  added text.
- [ok] No merge conflicts with main (`git merge-tree` writes a clean tree).
- [ok] ADR structure. ADR 069 has Status (Accepted, dated 2026-11-12), Context, Decision,
  Consequences, Alternatives Considered, Work This Creates and References, and a section for the
  person who accepts it. The file name follows the `NNN-slug.md` pattern.
- [ok] Docs in step. This change is the docs. The files the decision makes out of date (the
  ontology, `CLAUDE.md`, `managing-work.md`, the glossary and the plays) are named in the ADR's
  "Affects" list and are fixed by the work it creates, not here, as intended.
- [note] Readability. The "Affects" and "Amends" lines of ADR 069 are each one very long line.
  That follows the ADR template, so it is not a defect here, but a reviewer will find the "Work
  This Creates" section easier to read than those lines.
- [ok] Nothing obviously broken. No leftover TODO, TBD or FIXME in ADR 069.

## For the PR description

- #954 stays open, because this PR records the decision and the later /shape-plan fix is still
  to come. Use "Refs #954", not "Closes #954".

## Findings

Blocking findings: none.

Notes for the reviewer (none stops the raise):

1. The PR is large by line count; read ADR 069 and the 16 Status lines, not the run records.
2. The two memory copies in the ADR run records are evidence, not standards.
3. Two files from this step are still untracked until the next commit.
4. Use "Refs #954" in the PR body.

Verdict: ready to raise.
