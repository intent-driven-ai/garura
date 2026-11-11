# Feature: Replace or retire an intent

## What it does
Moves the parts that serve an old intent to a new one, and removes the old page once nothing names it, on a person's named approval.
- A business intent is what a person or the organisation wants, in their own words. A person may replace one intent with another, split one into several, or retire one, as their view of the product changes.
- Each domain, capability, feature or slice that served the old intent is then repointed, one part at a time: in its entry in the model's index, the new intent takes the old one's place, or the old one is dropped. The index is the model's list of every part and the intents it serves. A slice is an ordered group of features that one person can test end to end.
- Once no part and no page names the old intent, its page is removed.
- The skill remove-model-part does it with one script, all or nothing. What goes, what replaces it and who approved it are decided before it runs.
- The feature exists because a part that serves a removed intent serves nothing, and a person reading the old intent would see work that no longer belongs to it.

Status: built.

## Inputs / Outputs
- In: a request: the play or run that asks, the person who approved it, the parts to repoint with each old intent mapped to its new one or to nothing, and the intents to remove.
- Out: the model's index with each part repointed, and each old intent's page removed.
- Out: a report that lists each part repointed, each intent removed, and every file changed or deleted.

## Rules & behavior
- Never without the person's name. A request that names no approver is refused. The reason: the model never loses a part by accident, and the name records who decided it.
- The words come first. Before the removal, the page skill changes each line that names the old intent. While any page or index entry still names it, the whole request is refused, and the error names each path and line. The reason: nothing is left pointing at an intent that is gone.
- Each new intent must have a page, and must not be one the same request removes. The reason: a part never serves an intent that does not exist.
- Two parts that served the same intent can go to different new ones. A repointed part keeps its order of intents, with no duplicates. The reason: an old intent is often split into several.
- All or nothing, on a copy. Every check runs before the first write, and when a write fails part way every file is put back as it was. The reason: half a move would leave parts serving two versions of the product's intents.
- It writes only inside the product model, and it writes no page words. The index keeps its comments and layout. The reason: the words of each page are the page skill's, so each kind of change has one writer.
- Not built: the Touches lists. A repoint changes the index only, so the new intent's page does not list the part until the gap-closing step or a page change adds it.
- Not built: the tracker. The old intent's issue stays as it is in the tracker; nothing closes it or points it at the new one.

## Acceptance criteria
- Given a request that names no approver, when it runs, then it is refused and nothing is written.
- Given a request to remove an intent that a capability still names, when it runs, then it is refused and the error names that capability.
- Given a capability repointed from one intent to another, when the request lands, then its index entry names the new intent in the old one's place, once.
- Given a write that fails part way, when the request ends, then every file is as it was before the request.

## Out of scope
- Merging one capability into another, and removing a slice. The same skill does them, and Manage the model owns them.
- Choosing which intent replaces which. The person decides it.
- Writing the new intent's page, and changing the words on any page. Update an intent from approved words (fn-update-intent-from-approved-words) does it.
- The Touches list of the new intent. Keep an intent's links current (fn-keep-intent-links-current) keeps it.

## Sources
- core/components/skills/remove-model-part/SKILL.md: "**Never without the person's name.** A request with no `approved_by` is refused.", "Every id being removed must be gone from the pages.", "Two parts that shared an intent can go to"
- core/components/skills/remove-model-part/SKILL.md: "**All or nothing.** One bad item refuses the whole request", "It never writes a page's words"
- core/components/skills/remove-model-part/scripts/remove_part.py: "The model never loses a part by accident: a removal names the person who approved it, and it", "Each new intent must have a page at"
- core/components/skills/remove-model-part/scripts/remove_part.py: "remove an intent: its page intents/<id>.md goes, and it must be there."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "The same skill also repoints a part from one business intent to another, which is a change, not a take-out"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Only a person confirms or drops it; an agent never does."
