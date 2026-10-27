# Design — #807: Functionality becomes Feature on disk

Status: approved by the product owner, 2026-10-22 ("yes"). Order: the eval suite first, run it (it must fail), then build, then the eval passes.

Decisions already given (2026-10-22): **1a** — #807 is the rename only (plus ADR 048 and the glossary); the spine `epics` list and the dropped slice fields leave in the stories that redesign the plays that use them (#795, #799, #801, #803). **2 yes** — the delivery plays are renamed so that "feature" means one thing. **3 keep** — feature IDs keep the `fn-` prefix; new features use `ft-`. **4 out** — the retired intent-epic files stay out; a clean-up chore is filed.

## The order of the work

1. **The check first.** Add the old→new names to `core/components/memory/standards/rules/rename-map.yaml` and run `core/tools/naming/check_old_names.py`. It must FAIL today (the old names are everywhere). The change is done when it passes.
2. **Free the word "feature"** (rename map, as #734 did — `apply_renames.py` where it fits):

   | Old | New | Kind |
   |---|---|---|
   | /shape-features | /shape-slice | play |
   | /build-feature | /build-epic | play |
   | /validate-feature | /validate-epic | play |
   | /release-feature | /release-epic | play |
   | author-features | author-epics | skill |

   Their folders, `name:` lines, cross-references, pipeline rules (`pipeline-next.md`, `pipeline-position.md`), the installer's play lists, docs and the command cheat sheet follow. The installer removes the old names on the next install (#748).
3. **Functionality → Feature**, mechanical, in one commit so nothing is left half-renamed:

   | Area | What changes |
   |---|---|
   | Spine schema `spine.yaml` | `functionalities:` → `features:`, `functionality_refs` → `feature_refs`, `for_kind: functionality` → `feature`, layout `functionalities/` → `features/`, `functionality.md` → `feature.md`. The `epics:` block and the slice fields stay for now (decision 1a). |
   | Grounding templates | `functionality.md` → `feature.md`; its H1 `Functionality:` → `Feature:`; the capability page's `## Functionalities` section → `## Features`; other templates' wording. |
   | Other schemas | `slice.yaml`, `product-os.yaml`, `ice.yaml`, `decision.yaml`, `_index.md`, lens schemas: wording and field names. |
   | Scripts (stamped copies stay byte-identical) | 12 × `lint_grounding.py` (kind table, `ICE_KINDS`, `spine.get("features")`), 8 × `check_ready_slice.py`, 5 × `intent_touches.py`, 2 × `check_ice_workable.py`, the discover-*, shape-scope, lens validators, learn-outcomes, next, find-model-gaps, link-model-gaps, find-work-placement, propose-kb-node, adr.py scripts, and their tests. |
   | Plays (22 ICE sources) | The word changes in `reference/ice.md` and the compiled `SKILL.md`; nothing the play decides or guarantees changes, so each fingerprint is recomputed and `lint_play.py` must pass on every one. The loop `complete-discovery` the same. |
   | Skills, agents, rules, templates, knowledge | Wording: about 425 lines in 36 skills, 26 in 9 agents, rules, templates, knowledge shelves. |
   | Docs, glossary, config | `docs/` (not the ADRs — they are never edited), `core/grounding/glossary.md` (Feature, Slice, Epic rows follow v7), `core/config.yaml`, `CLAUDE.md`, `.garura/user-provided/managing-work.md`, `core/tools/rebuild-eval`. |
   | Garura's own model | `git mv functionalities/ features/` and each `functionality.md` → `feature.md` (21); `_spine.yaml` key and 21 doc pointers; 21 page H1s; the `## Functionalities` sections of two capability pages; intent pages' wording. IDs stay `fn-` (decision 3). |

4. **ADR 048** through `/record-decision`: ontology v7 — two layers, the plan as the thread, Feature for Functionality, Slice in the product layer, Epic a work item, story-centred work. It amends ADR 019 and 024 (the epic record leaves the model, in #795–#803), ADR 028 (the slice's realized stamp; the plan creates epics), ADR 031 §1 (only a story reads an ICE), ADR 043 and ADR 047 (the word Functionality), with a forward pointer on each.
5. **The ontology's own leftovers** through a short `/edit-ontology` run (the ontology changes only through that play): remove the three "until the rename story lands" notes, add the Layer and "In the tracker as" lines to the Source kind, and add both lines to the ontology template.

## How we know it is done

- `check_old_names.py` failed before step 2 and passes at the end.
- Every touched test suite passes (the survey's list: test_lint_grounding, test_lint_ice, test_vision_scripts, test_check_ice_workable, test_intent_touches, test_check_sources, test_persist_understand, test_intent_scripts, test_derive_candidates, test_validate_epics, test_find_gaps, test_apply_links, test_rebuild_eval, test_adr, test_apply_adr, test_install, test_naming_tools).
- `lint_play.py` passes on every recompiled play; the component linter shows no new error (121 today).
- The grounding linter gives Garura's own model the same result as before the rename (same errors, new names).

## Not in this change

- The spine `epics` list, `epic.md` pages and the dropped slice fields (status, order, effort, needs, domain): removed in #795 (/shape-slice), #799 (/build-epic), #801 (/validate-epic) and #803 (/next), each in the story that replaces what used them. /release-epic, /release-increment, /learn-outcomes, /shape-roadmap and /shape-scope read them too: the story that removes a field changes their read in the same change.
- The retired intent-epic files (`.garura/product/scope/`, `intent-epic.yaml`, the feature-catalog skills): a clean-up chore.
- Feature IDs: they stay `fn-`.
