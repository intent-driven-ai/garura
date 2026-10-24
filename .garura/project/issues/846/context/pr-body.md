Ontology v11: `/shape-slice` writes the slice's hidden file and proposes a thin ICE. Run through `/edit-ontology`, with the product owner's yes at all three checkpoints (questions, kinds, links and rules).

Closes #846 (on merge into the plan branch, by merge-change). Closes finding M1 on PR #845, which merges after this.

## What changes

- **Slice:** `/shape-slice` writes the link "slice serves business intent", a thin ICE for each part the slice needs that has no ICE, and the slice's hidden file. The hidden file has one entry for each feature, not for each story. `/shape-slice` makes the eval folder, also before any plan file exists.
- **Plan:** the plan play writes only the plan file, the epic and the stories, and nothing in the evals folder. It reads every ICE line except the "Fails if" lines.
- **Epic:** gains the feature-to-story map. The plan play writes it; the eval play uses it to join each hidden-file entry to its story. It must agree with the plan's Tree.
- **Story:** its failure and recovery conditions are written by `/shape-slice`. When an ICE changes, the plan play remakes the story and `/shape-slice` remakes the entry, in the same Alignment round.
- **ICE:** each line has one reader. An ICE can be thin: at least a goal, a limit and one "Fails if" line in Intent, one line in Context and one in Expectation, with the thin mark (a Thin line on its page and `thin: true` in its spine entry). A thin ICE is "partly ready" with the gap "thin ICE"; the person is warned and never sent back. "Light ICE" goes.
- **Rule:** `standards/rules/expectation-generation.md`, the section "A feature's recovery (product ICE)", follows the same change.
- **Ready check:** `check_ice_workable.py` (create-play reference and its discover-intent copy) reads only the thin mark: the gap "thin ICE" makes an ICE partly ready, and a mark in only one of its two places is named as drift. It no longer counts lines (the "light | full" report is gone). Tests first: 45 pass.
- **Schemas:** `spine.yaml` allows `metadata.thin` on an ICE entry and names the Thin line; `spine.yaml` and `slice.yaml` say what `/shape-slice` writes now.

## Review round 1 (rejected, all fixed)

- DF-1, DF-2 (P2): ADR 052 (`/record-decision`, accepted by the product owner) amends ADR 049 (§1.1, §1.2, §4, §5) and ADR 047 (§6–§8); both carry its forward pointer.
- DF-3, DF-4, DF-5 (P3): the ready check, `spine.yaml` and `slice.yaml`, above. The `/shape-slice` play's own text follows in its `/edit-play` change.
- DF-6 (P4): the feature-to-story map is in the epic, the plan's Tree and each story's "Represents"; agreed at checkpoint 2 (K3), with the rule that they always agree.
- DF-7 (P4): Q38 uses the stricter words from L1 (a goal, a limit and one "Fails if" line in Intent, one line in Context, one in Expectation), as the product owner agreed at checkpoint 3. The draft's Q38 line said "at least one line in each part"; the ontology follows the agreed L1.
- DF-8 (P4): the flow line now says a story is written from every ICE line except the "Fails if" lines. The Clinic "Booking" example says its parts are "short" and that it has no thin mark, so it does not contradict the thin rule.

## Checks

| Check | Result |
|---|---|
| `check_ontology.py` | valid, no problems |
| `check_ontology_change.py` | scope ok (only Slice, Plan, Epic, Story, ICE changed), version 10 → 11, one log line, no names |
| Checkpoints | questions yes, kinds yes, links yes (`decisions.json` all_agreed true) |

## Next

ADR 049 (Decisions 1.2 and 4) is amended through `/record-decision` after this lands. Then PR #845 takes the new base and is reviewed again. `/shape-slice` follows in its own `/edit-play` change.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
