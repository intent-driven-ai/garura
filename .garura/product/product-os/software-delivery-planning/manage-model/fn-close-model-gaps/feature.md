# Feature: Find and close the gaps inside the model

## What it does
The gap finder lists what is loose, written twice or missing inside the model, and says for each the link to make or the play that does the work; the gap closer then makes what the model can take with no new words, so drift inside the model with no work in it is found and closed.
- What the gap finder lists: parts with no parent, parents named that do not exist, capabilities with no feature, intents nothing serves, parts that serve no intent, links kept on one side only, empty domains, likely duplicates, and the screens of a prototype that no page covers.
- Its script counts the candidates, and the skill judges them: "Its script counts the candidates; the judgment (is this really a gap, where does this node belong, which play owns the work) is the skill's." It writes its list only, and never the model.
- What the gap closer makes, in order: it merges each duplicate marked agreed, keeping one and moving the other's intents and children onto it; it files each loose part under its parent, moving a page in a holding folder under its parent's folder, byte for byte; and it writes each intent link on both sides. What needs a play is handed back as the work list for the loop.
- Both run after each round of the Discovery loop, through the keeper.
- Their run on Garura's own model on 2026-11-11: one loose part, the old capability Link the product model, which has no domain; four intents nothing serves (bi-11, bi-5, bi-734 and bi-756); 21 links kept on one side only; no duplicates and no link to nothing.
- Handed here by Keep the spec matched to what's built: "Drift inside the model with no work in it, such as two ICE for one part, a thin mark kept in one place only, or the same part written twice. Manage the model owns it."
- Examples, in different kinds of project:
  - In a shop's checkout service, the Saved cards capability has no domain yet. The gap finder proposes the Payments domain, with why, and the gap closer files it there.
  - In a clinic's booking app, the intent "patients cancel online" has no capability. The gap finder hands it to /discover-capabilities.
  - In a news site's publishing tool, two capabilities, Schedule a story and Plan a story, show the same screen and the same purpose. They are marked agreed, and the gap closer keeps one with the other's intents and features.
- How it meets the capability: a living map stays whole as it grows only when what is loose, missing or written twice is found and closed.

Status: built in part, in find-model-gaps and link-model-gaps with their scripts and tests (7 and 9 passed in the stock-take's run on 2026-11-11), run in the Discovery loop. Not built, or open:
- They run inside a loop only. A change outside the Discovery loop, such as a part added through the two index skills, is not checked for gaps.
- The gap finder does not list two ICE for one part, or a thin mark kept in one place only; today the structure check names the first, and the ready check names the second.
- The gap closer files a loose part only: it does not move a part that already has a parent, and no skill does.
- The gap closer is a third writer of the index, with no person's name; it "stays for now inside a loop and folds into the two skills over time" (ADR 065).

## Inputs / Outputs
- In: the model's index and its pages, read only by the gap finder.
- In, when there is one: a prototype's capture, its view texts and the person's write-up.
- Out: from the gap finder, the list of links to make, each with why; the duplicates, each marked agreed or not; the work for each play; the screens no page covers; and the candidates cleared, with why.
- Out: from the gap closer, each change made, each link skipped with why, every file changed, and the work list for the loop, unchanged.

## Rules & behavior
- The gap finder only reads. The reason: "This skill writes `gaps.json` and nothing else."
- No link without a basis. The reason: "Every link and every merge says why, from the pages, their sources, the capture or the write-up."
- A link is made on both sides, or it is a gap. The reason: "Every `one_way` entry is a gap: a link is made only when both sides hold it."
- A parent is never made up. The reason: "Never invent a parent: when no node fits, it is missing work (step 5), not a link."
- A duplicate is merged only when it is agreed. The reason: "mark it `agreed: true` only when the pages and their sources show the same screen and the same purpose."
- Missing work goes to the play that owns the kind. The reason: "Work goes to the play that owns the kind".
- The gap closer writes no new words, and deletes only a merged duplicate. The reason: "No new content.", and "Delete only a merged duplicate."
- A part that already has a parent is not moved. The reason: "Never move a node already under a parent."
- Not decided: whether the gap finder and the gap closer run on every change that writes the model outside a loop, and through which play.
- Not decided: whether two ICE for one part and a thin mark kept in one place only join the gap finder's list.

## Acceptance criteria
- Given a capability with no domain, when the gap finder runs, then it lists it as loose and proposes its domain with why, or names the play that does the work.
- Given an intent page whose Touches list does not name a capability that serves it, when the gap finder runs, then it lists the link to make, and when the gap closer runs, then the Touches line is written.
- Given two capabilities marked agreed as the same thing, when the gap closer runs, then one is kept with the other's intents and children, and the other's entry and page go.
- Given a feature that already has a capability, when a link names another capability for it, then the gap closer skips it and says why.
- Given an intent nothing serves, when the gap finder runs, then it hands the work to /discover-capabilities.
- Given a change outside a loop that leaves a link on one side only, when it lands, then the gap is found and listed. This is not built.

## Out of scope
- Checking each page's shape. Check the model's structure and links on every change, as findings, never a stop (fn-check-model) does it.
- Taking out a part on a person's named approval. Take a part out on a person's named approval (fn-take-part-out) does it.
- The work the gap finder hands on, new intents, domains, capabilities and features. Specify the product, in Product → Spec, owns it, through the discovery plays.
- Drift between the model and what was built. Find where the spec and what's built no longer match (fn-find-spec-drift), in Keep the spec matched to what's built, does it.
- Running the rounds of a loop. Run plays as loops, in Orchestration, owns it.

## Sources
- core/components/skills/find-model-gaps/SKILL.md, line 3: "Its script counts the candidates; the judgment (is this really a gap, where does this node belong, which play owns the work) is the skill's."; lines 37-59: the candidates, "Every `one_way` entry is a gap: a link is made only when both sides hold it.", "Never invent a parent: when no node fits, it is missing work (step 5), not a link.", "mark it `agreed: true` only when the pages and their sources show the same screen and the same purpose."; lines 79-82: "This skill writes `gaps.json` and nothing else.", "Every link and every merge says why, from the pages, their sources, the capture or the write-up.", "Work goes to the play that owns the kind"
- core/components/skills/link-model-gaps/SKILL.md, lines 32-37 and 58-61: the order of its changes, "No new content.", "Delete only a merged duplicate.", "Never move a node already under a parent."
- core/components/skills/find-model-gaps/scripts/find_gaps.py: the candidates it counts; run from the repository root on 2026-11-11, writing its report outside the repository: 1 loose part, 4 intents nothing serves, 21 links on one side only, no duplicates, no links to nothing
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/fn-find-spec-drift/feature.md, line 51: "Drift inside the model with no work in it, such as two ICE for one part, a thin mark kept in one place only, or the same part written twice. Manage the model owns it."
- .garura/product/product-os/software-delivery-planning/run-plays-as-loops/capability.md, line 73: "Out: the link rules the step after each round applies to the product model. Manage the model, in Product model, owns them."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md, line 43: "it stays for now inside a loop and folds into the two skills over time."
- core/components/plays/create-play/references/lint_grounding.py, line 23, and check_ice_workable.py, lines 16-17: "each part has exactly one ICE", "When only one of the two is there, the gap names the drift."
- The stock-take, .garura/project/issues/1021/context/bi-11-inventory/inventory.md, section 2.8: 7 tests passed for the gap finder and 9 for the gap closer
