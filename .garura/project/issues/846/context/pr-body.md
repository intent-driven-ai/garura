Ontology v11: `/shape-slice` writes the slice's hidden file and proposes a thin ICE. Run through `/edit-ontology`, with the product owner's yes at all three checkpoints (questions, kinds, links and rules).

Closes #846 (on merge into the plan branch, by merge-change). Closes finding M1 on PR #845, which merges after this.

## What changes

- **Slice:** `/shape-slice` writes the link "slice serves business intent", a thin ICE for each part the slice needs that has no ICE, and the slice's hidden file. The hidden file has one entry for each feature, not for each story. `/shape-slice` makes the eval folder, also before any plan file exists.
- **Plan:** the plan play writes only the plan file, the epic and the stories, and nothing in the evals folder. It reads every ICE line except the "Fails if" lines.
- **Epic:** gains the feature-to-story map. The plan play writes it; the eval play uses it to join each hidden-file entry to its story. It must agree with the plan's Tree.
- **Story:** its failure and recovery conditions are written by `/shape-slice`. When an ICE changes, the plan play remakes the story and `/shape-slice` remakes the entry, in the same Alignment round.
- **ICE:** each line has one reader. An ICE can be thin: at least a goal, a limit and one "Fails if" line in Intent, one line in Context and one in Expectation, with the thin mark (a Thin line on its page and `thin: true` in its spine entry). A thin ICE is "partly ready" with the gap "thin ICE"; the person is warned and never sent back. "Light ICE" goes.
- **Rule:** `standards/rules/expectation-generation.md`, the section "A feature's recovery (product ICE)", follows the same change.

## Checks

| Check | Result |
|---|---|
| `check_ontology.py` | valid, no problems |
| `check_ontology_change.py` | scope ok (only Slice, Plan, Epic, Story, ICE changed), version 10 → 11, one log line, no names |
| Checkpoints | questions yes, kinds yes, links yes (`decisions.json` all_agreed true) |

## Next

ADR 049 (Decisions 1.2 and 4) is amended through `/record-decision` after this lands. Then PR #845 takes the new base and is reviewed again. `/shape-slice` follows in its own `/edit-play` change.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
