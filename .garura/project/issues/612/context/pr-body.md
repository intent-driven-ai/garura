## What this adds

`/intent` — a new play that turns what a person shares (a prototype, a project folder, a running site, a document or a plain statement) into two levels of intent:

- **Business intents** — what the person wants for the business, in their words, with why it matters and how we will know it is met. The person confirms or drops each one.
- **ICE** under each intent — the separate things the source lets the person see, decide or do, as goals. Saved in the `ice.yaml` shape, not yet placed under a capability.

The source is kept as a snapshot (screenshots and text of every view, copies of documents, or the exact statement) and linked both ways. The product model is the hand-off to later plays.

## Also in this change

- **Product ontology v3** (`schemas/product-os/ontology.md`) with the Business Intent, Source and ICE kinds. No play owns a kind; rules say what holds once aligned and never block a write; drift goes to an Alignment drive (not yet filed). `ice.yaml` gains `built_from` and allows an ICE before it is placed.
- **`business-intent-keeper`** agent and **`author-business-intent`** skill (draft both levels, check coverage, example answers on every question).
- **`build-product-ontology`** — a meta-utility skill, installed only with `install-garura --scope harness`.
- Plan updates for #606 and #616 (their own commits).

## How it was tried

Two trials on a real prototype (a token-usage dashboard): the first shaped the two-level design with Kapil; an unattended re-run then gave exactly Kapil's four business intents with 13 ICE under them, and the save, guard and stop condition passed. All trial output was removed; the records are under `.garura/project/issues/612/specs/trial-token-burn/`. Tests: 65 (intent scripts) and 23 (ontology check), all passing; `lint_play` passes.

## Still open on #612

Plan item 7 — how `/vision` picks up an intent and its ICE from the model — so this PR refers to the issue and does not close it.

Refs #612

## Self-review

# Self-review — #612 (feature/612-intent-play against origin/main)

Rules used: `/Users/kapilahuja/.garura/core/memory/standards/rules/self-review.md` (base file, no project override — see `resolved-rules.json`).

Diff reviewed: `origin/main...HEAD`. 8 commits, 51 files, about 5,100 lines added. This review is a checklist for the reader. It does not approve or reject.

Result: nothing here stops the raise. Two small documentation gaps are noted below as follow-ups.

## Scope checks

- [PASS] Matches the issue. The branch adds the `/intent` play, its keeper agent and its draft-writing skill, the product ontology and the skill that builds it, the matching schema and template updates, and an install rule that keeps the ontology builder out of product installs. All of it serves #612 (item 3 of the #606 plan).
- [PASS] No scope creep. The only edits outside #612's own work are the two plan updates the caller named: #606 (item 2 marked shipped, item 3 marked current) and #616 (plan marked done). Both carry their own issue refs in their commits. The one-line `intent` entry added to the pipeline-next rule is the hand-off from `/intent` to `/vision`, so it belongs here.
- [PASS] Plan item 7 is still open, so the PR references #612 without closing it. That is intended and is not a gap.
- [NOTE] Size. 5,100 lines is large, but about two thirds are the new play, its scripts and tests, and the ontology. A further 1,600 lines or so are recorded run evidence under `.garura/project/issues/612/` (token-burn trial drafts and checks). The pieces sit in separate commits by concern, so a reader can go commit by commit. Reasonable if the PR description says so.
- [PASS] No stray artifacts. No commented-out code, no leftover debug prints (the `print` calls found are the scripts' deliberate JSON and test output). No scratch files, caches or backup files are tracked. `__pycache__` exists locally but is ignored.
- [NOTE] The untracked `resolved-rules.json` in the working tree is this review's own input file, not part of the change.

## Quality checks

- [PASS] Tests present. The intent play scripts have 65 checks and the ontology checker has 23. I ran both just now and all passed (65 passed, 0 failed; 23 passed, 0 failed). The install change in `install.py` has no new test of its own; it is a small change to which components are selected, and it is visible in `.garura/install-manifest.json`.
- [PASS] Commits are clean. All 8 use the conventional format and each is one concern: start context, the play, the ontology, the install rule, then three record-keeping commits. All reference an issue: #612, and #606 and #616 for their plan updates.
- [PASS] No secrets. Searched every changed file for keys, tokens, passwords and private-key headers. The only hits are the word "token" in the token-burn trial notes (a cost measurement, not a credential).
- [NOTE] Docs in step: partly. The agents doc, the skills doc (meta-utility section and family table for `build-product-ontology`), the schema index and the template index are all updated. Two gaps remain:
  - `docs/components/plays.md` has a Complete Play Roster that lists `vision` and `understand` but not the new `intent` play.
  - `docs/components/skills.md` does not list `author-business-intent` in its family table, although the agents doc lists it in the keeper's pool.
  Both are small and neither changes behaviour. Worth fixing in this PR or the next commit on #612.
- [PASS] Nothing obviously broken. No leftover TODO or FIXME in the added code. The install change is consistent: `build-product-ontology` is excluded from the default install and included in the harness install, and the manifest reflects that (skills 10 to 11).

## Summary

Concerns that stop the raise: none. Follow-ups: the two documentation gaps above.

## After the review

Both documentation gaps were fixed before the push, in commit aaaa70f3: the play roster lists `intent`, and the skills family table lists `author-business-intent`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
