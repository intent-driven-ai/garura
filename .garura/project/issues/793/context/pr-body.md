Ontology version 7: the product layer and the work layer, with the plan as the thread between them. Decided with the product owner through `/edit-ontology`, at three checkpoints (`decisions.json`: all agreed; every change round kept).

## What changes in the ontology

- **Product layer (the model):** Business Intent, Source, Domain, Capability (ICE), **Feature** (ICE; the old Functionality), **Slice** (new: an ordered group of features, from any capabilities, that gives one vertical a person can test end to end). Only the Business Intent is a tracker issue (label `product`).
- **The Plan** is given one business intent, picks the slice(s) that best serve it, and creates one epic for each slice.
- **Work layer (tracker issues, label `work-item`):** **Epic** (represents one slice, holds stories, serves the intent, long-lived, no ICE), **Story** (represents one feature — one per feature in each epic — and writes its scope from the feature's and the capability's ICE), **Spike / Chore / Bug** (children of one story; a spike only after its story is built; a bug under the story that introduced the defect).
- Work is a layer, not a kind. Tracker Issue folds into each kind's "In the tracker as" line. Domain becomes a full kind.
- Dropped v6 rules: one capability has one Feature; a Feature carries its capability's ICE; one functionality has exactly one Story; Spikes, Chores and Bugs sit under a functionality.
- Questions Q1–Q26 (Q17–Q26 new).
- The diagram: the "How product and work fit together" section of the Harness Naming Standard page.

## Checks

| Check | Result |
|---|---|
| `check_ontology.py` | valid, 0 problems |
| `check_ontology_change.py` | scope ok (only the agreed kinds), version 6 → 7 with one log line, no real names |
| Examples | all 13 kinds have one |

## Not in this PR

The on-disk rename (functionality → feature, and `epics` out of the spine) is #807, next in plan 788. The delivery plays change from #795 on.

## Self-review

# Self-review — #793

Rules: the base self-review rules, resolved in `resolved-rules.json` (not an override).
Diff reviewed: `plan/788/base...HEAD` (4 commits, 26 files: 1 source file, 25 run records under `.garura/project/issues/793/context/`).
This review is informational. It does not block the raise. No finding below is blocking.

Blocking findings: none.

## Scope

- [PASS] Matches the issue. The one source change is the ontology (v6 to v7), which is what an /edit-ontology run on #793 produces. Every decision traces to `edit-ontology/need.md`.
- [PASS] No scope creep. The only file outside the run records is `core/components/memory/standards/schemas/product-os/ontology.md`. The on-disk rename (functionality to feature) is left for #807; the ontology says so in the places where it still names the old paths.
- [PASS] Changed kinds stay inside the declared touches: `check_ontology_change.py` reports scope_ok, version_ok (6 to 7, one log line, dated 2026-10-22) and names_ok.
- [NOTE] Size. 442 lines added and 122 removed in one file, plus 25 run records. Large, but it is one document changed as one decision set, and the run records show the three checkpoints. Acceptable.
- [NOTE] Stray artifacts. The run folder holds ten draft files (`draft-questions.md`, `.v1` to `.v9`, `draft-kinds*.md`, `draft-links.md`). They are superseded drafts. They are run records, not code, so this is low risk; they could be pruned or left as the history of the three rounds.

## Quality

- [PASS] Ontology check. `check_ontology.py`: valid, 0 problems. 13 kinds, each with an Example.
- [N/A] Tests. No code changed; the ontology's own checks are the tests and both pass.
- [PASS] Commits. Conventional format and each references #793: the `feat(ontology)` commit for the change, three `chore(stm)` commits for run records.
- [PASS] No secrets. A scan of added lines for keys, tokens, passwords and absolute local paths found none.
- [PASS] Docs in step. The ontology is itself the doc. It states plainly that spine and file names (`features`, `feature.md`) lag until the rename story.
- [PASS] Nothing obviously broken. No leftover TODO or FIXME in the added lines.

## Findings to fix before merge (not blocking)

1. Issue text no longer matches the outcome. Issue #793 is titled "Decide in the ontology what replaces Slice and Epic". The agreed outcome keeps Epic as a work item and makes Slice a product-layer kind. Update the issue title and body to say that. The issue is the work order, so it should read true at merge.
2. A real first name appears in the ontology: the "Nothing is blocked" line (line 23) and the v5 log line (line 752). Both lines were already there in v6 and this change did not add them, but the standing rule is no real names in model pages. Replace them with "the product owner" in this change or in a follow-up. The same lines sit in `edit-ontology/ontology-before.md`, which is a frozen snapshot of v6 and can stay as it is.
3. Raw replies in the run records. `decisions.json` and `need.md` carry the product owner's pasted words, which is the intended record. Confirm they hold no names of third parties before the branch goes wider. A scan for the owner's name and company terms found only the two ontology lines above.

## Observation

The decision removes Work as a kind, takes Epic out of the product model, and adds Slice as a kind. That reshapes the model for every play that reads it. The log line in the ontology records it. The plan may want a decision record (ADR) as well; this is for the plan owner to judge and is not part of this change.

## Where it lands

Into `plan/788/base`. Closes #793 (closed by merge-change). Part of #792, #788.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
