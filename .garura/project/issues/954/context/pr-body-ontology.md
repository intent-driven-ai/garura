## What this changes

**Product ontology v17: the plan is where the product model meets the work** (ADR 069). The product owner agreed all three checkpoints through /specify-ontology.

- **Plan.**
  - Shows its business intent at the top, then a tree that starts at its **one Epic** (marked `epic: <issue number>`).
  - Records each slice with a status a person sets: Not Started, In Progress, Done or Dropped.
  - Has **one eval** for all its slices. A done plan lands only when that eval passes, run by hand until #801 exists.
- **Epic:** one per plan, with no unplanned epic. It holds the Feature issues of every slice, plus plan-wide chores.
- **Slice:** names no plan, folder, epic, eval or hidden file, and has no form in the tracker. Whether it is in progress is read from the plan files.
- **Business Intent:** its page has no Tracker line, and What was done links no work item.
- **Chore:** sits under a story when it's that story's work, otherwise under the plan's epic.
- **The whole model knows no plan, no tracker and no decision record.** The Product Profile is listed as not yet defined.

Refs #954

## How to review it

- `core/components/memory/standards/schemas/product-os/ontology.md`: the only source change (26 hunks).
- The ontology check passes, and the change check passes: only the agreed kinds changed, the version is up by one with one log line, and no real names appear.
- Everything else is run records: the three agreed drafts, the decisions, the checks and memory copies.

## Self-review

# Self-review for #954 (ontology v17: the plan is where the product model meets the work)

Branch: feature/954-ontology-plan-meets-work, against main. Rules: the base self-review rules,
resolved to `standards/rules/self-review.md` (no project override; see
`.garura/project/issues/954/context/resolved-rules.json`).

This is an information checklist for the reviewer. It does not approve or reject the change.
It is the second self-review in this folder; the first, `self-review.md`, covers the earlier
ADR 069 change and is not touched.

## What the change is

It brings the product ontology to version 17, as ADR 069 (already on main) decided. The product
owner agreed the three checkpoints (the questions, the kinds, the links and rules); the third
was agreed after one change: the plan tree may start at the epic, and the plan template must
still show which business intent the plan serves. The ontology now says the plan is the one place
where the product model meets the work, and that the model itself knows no plan, tracker or
decision record. The six kinds it changes are Business Intent, Slice, Plan, Epic, Feature issue
and Chore.

18 files, +2645 / -99, in 2 commits. Where the lines are:

| Part | Files | Notes |
|------|-------|-------|
| Product ontology | 1 (143 added, 99 removed) | `core/components/memory/standards/schemas/product-os/ontology.md`, the only file outside `.garura/` |
| Run records for the ontology run | 11 | under `.garura/project/issues/954/context/specify-ontology/`: need, three drafts, decisions, the version before, the two checks |
| Memory copies | 3 | two templates and a manifest, under `.garura/project/issues/954/context/memory/` |
| Start-work records | 5 | under `.garura/project/issues/954/context/start-work-2/` |
| Citations | 1 | two lines added |

## Scope checks

- [ok] Matches the issue. The change is the model half of the decision #954 needed settled
  (the plan and the model split) before the later `/shape-plan` fix. It changes the ontology
  and nothing that uses it.
- [ok] No scope creep. The one file outside `.garura/project/issues/954/` is the ontology. No
  play, skill, agent, tool, schema file, `CLAUDE.md`, ADR or glossary is touched.
- [ok] Only the needed areas changed. `change-check.json` reads `scope_ok: true`,
  `version_ok: true` and `names_ok: true`. The kinds changed are Business Intent, Chore, Epic,
  Feature issue, Plan and Slice. All six are in the allowed list, and `out_of_scope` is empty.
- [ok] Version up by one with one log line. The file goes from version 16 to 17, the log has
  one new line (dated 2026-11-12, naming #954 and ADR 069), and `new_log_lines` is 1.
- [ok] The ontology check passes. Running `check_ontology.py` on the file now reads
  `valid: true`.
- [ok] The product owner's change is carried. The Plan text says the plan shows its business
  intent, by title and id, at the top of the plan file, and that the plan-view template used by
  `/view-plan` and `/list-plans` shows it there. The tree starting at the epic is also written.
- [ok] The three checkpoints are recorded. `decisions.json` holds a yes for the questions and
  the kinds, one "change" and then a yes for the links, and `all_agreed: true`.
- [note] Size. The change is large by line count, but about 2,500 of the 2,650 lines are run
  records. The part to read is the ontology diff (26 hunks, mostly the Plan, Slice and Business
  Intent sections and the log line).
- [note] The run records keep three copies taken for the run: the ontology as it was before
  (970 lines) and two templates from memory (the plan-view template and the ontology format).
  They are evidence, in the same way earlier "record ... memory copies" commits are. The
  citations file notes that the committed copy of the ontology format is newer than the memory
  copy, and says which one the run used.
- [note] The product owner's words said "business intent(s)". The ontology says a plan serves
  one business intent, which fits ADR 069 (one plan for each business intent). A reviewer who
  wants a plan to show several intents should say so; it would be a later change.
- [ok] No stray artifacts. No debug output, commented-out blocks or scratch files. The working
  tree was clean before this step.

## Quality checks

- [ok] Tests. None are needed: the diff is one document and run records. The ontology has its
  own check, and it passes.
- [ok] Commits. Two commits, both in conventional format and both naming #954:
  `chore(stm): record start-work workspace context for the ontology change (#954)` and
  `feat(ontology): v17 — the plan is where the product model meets the work (#954)`. The
  second mixes the ontology and its run records, which is how earlier ontology changes were
  committed, so each is still one concern (one ontology change).
- [ok] No attribution lines. No tool-credit line and no co-author line in either commit or in
  any added text. The PR body must not add one.
- [ok] No secrets. A scan of the added lines for keys, tokens, passwords and private-key
  headers found nothing.
- [ok] No personal references. The added lines hold no person's name, no absolute path, no
  home folder, no temporary path and no account name.
- [ok] No merge conflicts with main (`git merge-tree` writes a clean tree).
- [ok] Docs in step. This change is the doc. The plays, templates and guides that the new
  ontology makes out of date are named by ADR 069 and are fixed by the work that follows it,
  not here, as intended.
- [ok] Nothing obviously broken. No TODO, TBD or FIXME in the added ontology text.
- [ok] Rules for the ADR 069 change checked: the docs-only commit type rule is met, because
  the only non-record file is a Markdown file.

## For the PR description

- #954 stays open, because this PR records the ontology half and the later `/shape-plan` fix
  is still to come. Use "Refs #954" in the PR body and in any commit added later.

## Findings

Blocking findings: none.

Notes for the reviewer (none stops the raise):

1. The PR is large by line count; read the ontology diff, not the run records.
2. The three copies in the run records are evidence, not standards.
3. A plan shows one business intent, not several, as ADR 069 decides.
4. Use "Refs #954" in the PR body.

Verdict: ready to raise.
