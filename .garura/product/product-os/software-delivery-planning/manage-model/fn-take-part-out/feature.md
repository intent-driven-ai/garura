# Feature: Take a part out on a person's named approval

## What it does
When a person approves taking parts out of the model, the keeper does it through remove-model-part with that person's name, all or nothing, and only once no page still names what goes, so the map is pruned on purpose and no link is left pointing at nothing.
- In the skill's words: "A part leaves the product model only when a person said so and when nothing is left that still names it."
- It does four things, each on a person's named approval:
  - repoint: a domain, capability, feature or slice that served an old business intent serves a new one, or the old one is dropped, part by part;
  - remove an intent's page, once no part and no page names the intent;
  - merge a capability into another: "the capability's features move to the survivor. Whatever was identified by it, or depended on it, now names the survivor, never twice and never the survivor itself. The survivor gains the intents it lacks, in order, and the decisions.";
  - remove a slice and its record.
- A merged capability's quality and compliance needs are not copied: "a merged capability's needs are for a person to look at".
- The words come first. The page skill changes each line that still names the part; while one is left, the script refuses and names each path and line.
- Inside a loop, the gap closer also removes the dropped part of a duplicate marked agreed. Its key is "an agreed gaps.json, not a person's name", and it "stays for now inside a loop and folds into the two skills over time" (ADR 065).
- Examples, in different kinds of project:
  - In a shop's checkout service, the product owner approves merging an old Wishlist capability into Saved items. Wishlist's features, links and intents move to Saved items, its page goes, and its quality needs are listed for the product owner to look at.
  - In a clinic's booking app, an old intent is replaced. Each part that served it is repointed to the new intent, and once nothing names the old intent, its page is removed.
  - In a news site's publishing tool, a slice no one will build is removed with its record, and nothing in the plans folder changes.
- How it meets the capability: this is the "pruned" in "added to, changed and pruned as work is done".

Status: built in part, in remove-model-part and its script (63 tests passed in the stock-take's run on 2026-11-11), and, inside a loop, the gap closer's merge of an agreed duplicate. Not built, or open:
- No skill removes a feature, a domain or an ICE: the script takes out only intents, capabilities and slices.
- A capability that has its own ICE page cannot be merged: "so it cannot be merged here". 38 of the 41 capabilities have one.
- When no skill covers a take-out, the keeper says so and stops, and nothing records what is owed.
- Inside a loop, a part can still be taken out with no person's name, through the gap closer.

## Inputs / Outputs
- In: what goes, what replaces it, and the name of the person who approved it.
- In: the model's index and its pages.
- Out: the index without the parts taken out, with every link that named them repointed or dropped.
- Out: the pages and folders removed, and the report: who asked, who approved, what was repointed, removed and merged, the features moved, the needs to review, and every file changed or deleted.

## Rules & behavior
- No take-out without the person's name. The reason: "Never without the person's name."
- The words are fixed first. The reason: "A mention left on a page refuses the request, so the page skill fixes those words first."
- All or nothing. The reason: "One bad item refuses the whole request, every check runs before the first write, and when a write or a delete fails every file is put back as it was."
- A capability is merged, never simply removed. The reason: "A capability is never simply removed: it merges `into` another."
- A merged capability's needs go to a person, never copied. The reason: "its needs are listed for review, never copied".
- The removed id stays nowhere. The reason: "Anywhere in the changed spine's data it refuses the request, naming the part."
- Nothing under the plans folder is touched. The reason: "Nothing under the plans folder is touched, even for a slice."
- Not decided: the way past when no skill covers a take-out, such as removing a feature, a domain or an ICE.
- Not decided: when the gap closer's take-out inside a loop moves onto the two index skills, and with whose name.

## Acceptance criteria
- Given an approved merge of a capability that has no ICE entry, with the person's name, when it runs, then its features, links, intents and decisions move to the survivor, its page goes, and its needs are listed for review.
- Given a request with no approver's name, when it runs, then nothing is written.
- Given a page that still names a part being removed, when it runs, then nothing is written and the error names the path and the line.
- Given an intent page that no part and no page names, when its removal is approved, then the page goes.
- Given an approved slice removal, when it runs, then its entry and its record go, and nothing under the plans folder changes.
- Given a feature, a domain or an ICE a person approved taking out, when the keeper is asked, then it goes with the person's name in the report. This is not built.
- Given a capability that has its own ICE page, when a person approves merging it, then it merges with its ICE handled. This is not built.

## Out of scope
- Deciding from the work that an intent is replaced or retired. Replace or retire an intent (fn-replace-or-retire-intent), in Keep the spec matched to what's built, does it, with this feature's tool.
- Choosing which of two duplicate parts to keep. Find and close the gaps inside the model (fn-close-model-gaps) does it.
- Fixing the words of the pages that name the part. Change a part from words a person approved (fn-change-part) does it.
- Deleting a plan. Remove a plan on a person's approval (fn-remove-plan), in Orchestrate agent work through planning, does it.

## Sources
- core/components/skills/remove-model-part/SKILL.md, line 3: "its needs are listed for review, never copied"; line 11: "A part leaves the product model only when a person said so and when nothing is left that still names it."; line 35: "A capability is never simply removed: it merges `into` another."; lines 52-53: "a merged capability's needs are for a person to look at"; lines 55-57: "the capability's features move to the survivor. Whatever was identified by it, or depended on it, now names the survivor, never twice and never the survivor itself. The survivor gains the intents it lacks, in order, and the decisions."
- core/components/skills/remove-model-part/SKILL.md, lines 74-83: "Never without the person's name.", "A mention left on a page refuses the request, so the page skill fixes those words first.", "One bad item refuses the whole request, every check runs before the first write, and when a write or a delete fails every file is put back as it was.", "Nothing under the plans folder is touched, even for a slice.", "Anywhere in the changed spine's data it refuses the request, naming the part."
- core/components/skills/remove-model-part/scripts/remove_part.py, lines 78 and 227-228: `REMOVABLE = ("intent", "capability", "slice")`; "has its own entry in the spine's `ices` list, so it cannot be merged here"
- A read of the index, .garura/product/product-os/_spine.yaml, on 2026-11-11: 38 of the 41 capabilities have an entry in its ICE list
- core/components/agents/product-os-keeper.md, lines 183-184: "When no skill covers a change, say so and stop"
- core/components/skills/link-model-gaps/SKILL.md, lines 32-35: it "merges each duplicate marked `agreed: true`"
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md, lines 40 and 43: "Its key is an agreed gaps.json, not a person's name.", "it stays for now inside a loop and folds into the two skills over time."
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/fn-replace-or-retire-intent/feature.md, line 44: "Merging one capability into another, and removing a slice. The same tools do them, and Manage the model owns them."
- .garura/product/product-os/software-delivery-planning/build-or-update-product/capability.md, line 29: "Merging or taking out another part goes to Manage the model."
- .garura/product/product-os/software-delivery-planning/orchestrate-agent-work/fn-remove-plan/feature.md, line 56: "Removing parts of the product model. Product model owns it."
- The stock-take (2026-11-11), sections 2.4, 5 and 6 (item 3): 63 tests passed for remove-model-part
