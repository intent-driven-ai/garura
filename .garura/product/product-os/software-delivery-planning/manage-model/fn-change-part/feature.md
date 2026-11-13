# Feature: Change a part from words a person approved

## What it does
When a person approves new words or a new place for a part that exists, the keeper changes it through the model's skills, all or nothing and keeping everything else as it was, so any part of the model can be changed on purpose, and never by hand.
- Named lines of any page, a domain, capability, feature or intent page: the page skill changes "only those lines, to the words it gives", through its script, and keeps every other line word for word.
- A whole page a person approved, a domain, capability, feature or ICE page: the page skill writes the approved text word for word, in place of the page that was there.
- An intent page: the intent-page skill writes it again from its draft. A rewrite keeps the old "What was done" block, and the old Touches block unless the draft gives one. It writes the stage confirmed only when the caller names the person who confirmed it.
- A part's entry in the index: link-model-part, in its update mode, replaces the one-line, adds intents, names the issue, and sets the thin mark. To take in an old part a person approved, it also takes a thin mark off, files a feature under another capability, and moves a page with its ICE page to a new folder.
- The edit standard: "One way to change a business intent, a domain, a capability, a feature, an ICE, a plan, an epic or a story that already exists: `/<play> #<id> --edit: <their words>`, through the play that owns the record." It is built for /shape-slice. The product owner set the edits here: "Managing the model should hold the edits as well."
- Examples, in different kinds of project:
  - In a shop's checkout service, the product owner rewords the checkout intent's outcome after a talk with sales. The two named lines of the intent page change, and every other line stays as it was.
  - In a hospital's appointment system, the technical lead approves a new page for the Reminders capability. The page is written word for word, in place of the old one.
  - In a bank's payments service, the technical lead approves moving the Upload documents feature under the Applications capability. Its page and its ICE page move to the new folder, its entry follows, and no link breaks.
- How it meets the capability: this is the "changed" in "added to, changed and pruned as work is done".

Status: built, in the page skill's two scripts for named lines and approved pages, the intent-page skill, and link-model-part's update mode, with their tests (19, 16, 50 and 48 passed in the stock-take's run on 2026-11-11). Not built, or open:
- The --edit option in each play that owns a record, other than /shape-slice: /discover-intent, the shared edit rule and its check, /discover-domains, /discover-capabilities and /create-play. Today /discover-intent refuses a page when "an intent page already exists".
- No skill changes a capability's domain once it has one: the gap closer sets a domain only on a loose part, and "Never move a node already under a parent."
- No skill writes a need or an "identified by" link on a part that exists: link-model-part takes "identified by" only for a new part, and has no field for needs.
- No skill takes the thin mark off an ICE: "mode `update` only marks an ICE that is there thin."
- The intent-page skill writes the stage confirmed for any name it is given; nothing checks that the person replied.
- Manage ADRs' page gives "Changing what a business intent says" to Product model, while Keep the spec matched to what's built holds updating an intent when the implementation changes. Rewording that line to name both is owed at this intent's close.

## Inputs / Outputs
- In: the person's approved words or approved page, and where the approval is recorded.
- In: for named lines, each line to change, whole and as it is on the page, with its new words and the request's source.
- In: for an entry, the part's id and what changes: its one-line, intents to add, its issue, its thin mark, its capability or its page's folder.
- Out: the changed pages, every other line kept word for word.
- Out: the changed index entries, with every other field kept.
- Out: each skill's report: each line old and new, each page written, every file changed.

## Rules & behavior
- Only the named lines change. The reason: "Exit 0: every named line changed and every other line kept, word for word, with its own line ending."
- A named line that is not on the page refuses the change. The reason: a request line that does not match a line on the page is refused and named; nothing on that page is written.
- The meaning comes from the person, never from the skill. The reason: "The meaning comes from the request's source, never from this skill: a new intent page is /discover-intent's, and a change of meaning is the person's or an approved design's."
- An intent page is never confirmed by the skill. The reason: "never confirms by itself; the stage is proposed unless the caller names the person who confirmed it".
- A rewrite keeps what was done. The reason: "On a rewrite it keeps the old page's What-was-done block byte for byte".
- A feature moves to another capability only when a person approved it. The reason: "A feature that already has a capability moves to another only through `capability` on `update`, when a person approved taking in an old part".
- A move breaks no link. The reason: "It is refused while any page or record in the model names an old path".
- A record is changed through the play that owns it. The reason: the edit standard sets one way to change a record, through the play that owns the record.
- Not decided: how a confirmed intent page records the person's own reply, beyond the name the caller gives.

## Acceptance criteria
- Given a request that names two lines of a capability page with their new words, when the page skill runs, then those two lines change, every other line is kept word for word, and the report lists each line old and new.
- Given a request line that is not on the page, when the page skill runs, then nothing on that page is written and the error names the line.
- Given an intent page and its new draft with no person named, when it is rewritten, then its stage reads proposed and its "What was done" block is kept byte for byte.
- Given a feature a person approved taking in, when the index skill files it under another capability with its new folder, then its page and ICE page move, its entry and its ICE's entry follow, and no page names the old path.
- Given a person's words to change a capability through /discover-capabilities --edit, when the play runs, then the capability changes through that play, from those words. This is not built.
- Given a capability with a domain, when a person approves moving it to another domain, then its entry names the new domain. This is not built.

## Out of scope
- Updating a page because what was built changed. Update the spec to match what's built (fn-update-spec-to-match-built), in Keep the spec matched to what's built, does it.
- Repointing a part from an old intent, and taking a part out. Take a part out on a person's named approval (fn-take-part-out) does it.
- Writing a new business intent's page from a person's words. Specify the product, in Product → Spec, owns it, through /discover-intent.
- Changing a slice and its hidden file. Orchestrate agent work through planning, in Orchestration, owns it, through /shape-slice.

## Sources
- The capability list: "Managing the model should hold the edits as well."
- core/components/skills/enrich-grounding/SKILL.md, lines 61-63, 73-74, 77-79 and 80-81: "change only those lines, to the words it gives", "Exit 0: every named line changed and every other line kept, word for word, with its own line ending.", "The meaning comes from the request's source, never from this skill: a new intent page is /discover-intent's, and a change of meaning is the person's or an approved design's.", "the page is copied as it is: nothing is composed."
- core/components/skills/author-intent-page/SKILL.md, line 3: "On a rewrite it keeps the old page's What-was-done block byte for byte", "never confirms by itself; the stage is proposed unless the caller names the person who confirmed it"
- core/components/skills/author-intent-page/scripts/write_page.py, line 113: "--stage confirmed needs the person who confirmed it in --confirmed-by"
- core/components/skills/link-model-part/SKILL.md, lines 68-71 and 78-80: "A feature that already has a capability moves to another only through `capability` on `update`, when a person approved taking in an old part", "It is refused while any page or record in the model names an old path"
- core/components/skills/link-model-part/scripts/link_part.py, lines 39-54, 66-67 and 337-338: the update keys; "mode `update` only marks an ICE that is there thin"; `identified_by` is set only on a new entry
- core/components/skills/link-model-gaps/SKILL.md, line 61: "Never move a node already under a parent."
- core/components/plays/discover-intent/scripts/persist_intent.py, line 29: "or an intent page already exists"
- .garura/product/product-os/software-delivery-planning/manage-adrs/fn-keep-adrs-to-build/feature.md, line 54: "Changing what a business intent says. Product model owns the intent pages, and the product owner decides each change."
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/capability.md, line 44: "In: updating an intent or a model part when the implementation changes, only from words a person approved."
- The stock-take (2026-11-11), section 2.3 and section 9, question 7; the tests: 19 passed for the named-lines script, 16 for the approved-page script, 50 for the intent-page skill and 48 for link-model-part
