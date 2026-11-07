# Feature: Replace or retire an intent

## What it does
When the work shows that an intent has been replaced or is no longer wanted, and the person approves it, the spec is changed to match: the parts that served the old intent serve the new one, or none, and the old intent leaves the spec.
- A business intent is what a person or the organisation wants, in their own words. The spec is what the product model says the product is for and what it does. The product model is the shared map of the product that people and agents read.
- The work can show that an intent has changed. For example, the work for it went a different way, one intent turned out to be two needs, or the person no longer wants it. The work only shows this. The person decides it.
- After the person's approval, the spec changes in this order:
  - Each page that names the old intent gets new words first, through Update the spec to match what's built (fn-update-spec-to-match-built).
  - Each part that served the old intent is moved, one part at a time: in the model's index, the new intent takes the old one's place, or the old one is dropped. The index is the model's list of every part and the intents it serves. A part can be a domain, a capability, a feature or a slice. A slice is an ordered group of features that one person can test end to end.
  - When no part and no page names the old intent, its page is removed.
- What is removed, what replaces it and who approved it are all settled before anything changes.
- The feature exists because a part that serves a removed intent serves nothing. An intent that the work left behind also still tells agents and people to build something that nobody wants.

Status: built in part. Moving the parts and removing the old page are built, all or nothing, only with the approver's name. Not built: the new intent's side of each link when the parts move, and the old intent's issue in the tracker. Not decided: what happens to the old intent's record of what was done.

## Inputs / Outputs
- In: what the work shows: a drift that was found, or a change that landed, that says an intent was replaced or is no longer wanted.
- In: the person's approval, with their name and where it is recorded: which intent goes, and for each part that served it, the intent it serves now, or none.
- In: the page of each new intent, written first from approved words, when the old intent is replaced.
- Out: each part that served the old intent now serves the intent the person named, or none, and names each intent once.
- Out: the old intent's page is removed, when no part and no page names it.
- Out: a record of each part that moved, each page that was removed, each file that changed, and the person who approved it.

## Rules & behavior
- The person decides. An agent never replaces or retires an intent itself, even when the work no longer serves it. The difference is named, and the person decides. The reason: only a person confirms or drops a business intent.
- Nothing changes without the person's name. A request that names no approver is refused. The reason: an intent removed by mistake takes its links with it, and the name records who decided.
- The words change first. Before the old intent is removed, each page line that names it gets new words. While a page or an index entry still names the old intent, the removal is refused, and the person is told each place that names it. The reason: nothing must point at an intent that is gone.
- Each new intent must already have a page, and the same request must not remove it. The reason: a part must never serve an intent that does not exist.
- One intent can become several. The parts that served one intent can each go to a different new intent. A moved part names each of its intents once. The reason: the work often shows that one intent was two needs.
- All or nothing. All checks run before the first write, and if a write fails, every file goes back to how it was. The reason: half a move would leave parts that serve two versions of the product's intents.
- It changes only what the approval names. The reason: the approval is for those parts and that intent, and nothing else.
- Not built: the new intent's side of each link. A move changes the index only, so the new intent's page does not list the parts that moved to it. Keep an intent's links current (fn-keep-intent-links-current) owns that side.
- Not built: the old intent's issue in the tracker. The issue stays as it was. Nothing closes it or points it to the new intent. Keep the tracker's words matched to the model (fn-keep-tracker-matched) owns it.
- Not decided: the old intent's record of what was done. When its page is removed, the record goes with the page, and only the repository's history keeps it. Nothing moves it to the new intent.

## Acceptance criteria
- Given the work shows that an intent is no longer wanted, and no person approved its retirement, when the retirement is asked for, then nothing changes.
- Given an intent replaced by a new one with the product owner's approval, when the change lands, then each part that served the old intent names the new one in its place, once, and the old intent's page is gone.
- Given a retirement while a capability page still names the old intent, when it runs, then nothing is removed, and the person is told the page and the line.
- Given a write that fails part of the way through, when the change ends, then every file is as it was before.
- Given an intent replaced by a new one, when the change lands, then the new intent's page lists each part that moved to it. This is not built.

## Out of scope
- Merging one capability into another, and removing a slice. The same tools do them, and Manage the model owns them.
- Choosing which intent replaces which. The person decides it.
- Writing the new intent's page, and changing the words on any page. Update the spec to match what's built (fn-update-spec-to-match-built) does it.
- The new intent's side of each link. Keep an intent's links current (fn-keep-intent-links-current) keeps it.
- The old intent's issue in the tracker. Keep the tracker's words matched to the model (fn-keep-tracker-matched) keeps it.
- Finding that an intent no longer matches the work. Find where the spec and what's built no longer match (fn-find-spec-drift) will do it.

## Sources
- The capability page the product owner approved on 2026-11-07: "In: replacing an intent with another, or retiring it, on a person's named approval.", "Never: remove an intent while any part still names it."
- core/components/skills/remove-model-part/SKILL.md: "**Never without the person's name.** A request with no `approved_by` is refused.", "Every id being removed must be gone from the pages.", "Two parts that shared an intent can go to"
- core/components/skills/remove-model-part/SKILL.md: "**All or nothing.** One bad item refuses the whole request", "It never writes a page's words"
- core/components/skills/remove-model-part/scripts/remove_part.py: "The model never loses a part by accident: a removal names the person who approved it, and it", "Each new intent must have a page at"
- core/components/skills/remove-model-part/scripts/remove_part.py: "remove an intent: its page intents/<id>.md goes, and it must be there."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "The same skill also repoints a part from one business intent to another, which is a change, not a take-out"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Only a person confirms or drops it; an agent never does."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "What was delivered for it and the value each piece brought, with links to the finished work items — updated as work finishes"
