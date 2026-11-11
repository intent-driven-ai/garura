# Feature: Link the parts by the map's rules: what each serves, what it needs and what led us to find it

## What it does
Each capability and feature is linked by the ontology's rules, the business intents it serves kept on both sides, the capabilities it needs and the capabilities that led us to find it, and each link is to be checked to point at a part that exists, so a search from either side gives the same answer and the ready check reads true links.
- Serves: a capability's index entry names the business intents it serves, and each intent page's Touches list names the capability back, marked adds, changes or removes. The intent page's side is written by one script, in the plays that save intents and domains, in /shape-slice and in the gap closer. A feature serves the intents its capability serves. A slice's link to its intents is kept on the slice's side only.
- Needs: "Other capabilities that must be done first — capabilities only". It is the only link that sets an order of work, and the ready check reads it.
- Identified by: "The other capabilities that led us to find it — capabilities only, and may name more than one; empty when it was found on its own". It records where a part came from, and never sets an order. A part found on its own is not a gap.
- A feature needs nothing and is identified by nothing. Its order of work comes from its capability, and the order of features is kept in the slices. This page once said "A feature can need a capability or another feature"; the ontology since its version 6, and the product owner on 2026-11-11, say it cannot.
- The rename: the index's field for needs is still `depends_on`. #725 renames it `needs`, in the index and in every file that reads it, with every value kept.
- The check: each need and each "identified by" link is to name a capability that exists, and never work, a business intent, a domain or a feature; each one that does not is a finding, never a stop.
- This feature comes from the old capability Link the product model, whose page said: "Each capability links to the business intents it serves. Each feature links to the capability that holds it."
- Examples, in different kinds of project:
  - In a shop's checkout service, the Refunds capability needs the Payments capability, so Refunds is not ready while Payments is not done. Refund to card, a feature of Refunds, holds no need of its own.
  - In a clinic's booking app, the Reminders capability was found while Booking was built, so Reminders names Booking as what led us to find it. Timetable was asked for directly, names nothing, and that is not a gap.
  - In a bank's lending service, Upload documents is built before Score the application inside one slice. No need is written between the two features: the slice keeps their order.
- How it meets the capability: a living map holds together as it grows only when its parts link by one set of rules, the same on both sides.

Status: built in part. Built: the serves link on both sides, with the intent page's side written by one script in the plays that save intents and domains, in /shape-slice and in the gap closer; and the rules for needs and "identified by", in the ontology. Not built, or open:
- The rename and the check that each link points at a part that exists (#725, "Needs" and "identified by" link capabilities, open). Today the structure check does not read `depends_on` or `identified_by`.
- 21 serves links are kept on one side only, in the gap finder's run on 2026-11-11. The two index skills and /discover-capabilities write no Touches line: "A part linked or moved through them is missing from its intent's page."
- The index holds six needs from one feature to another: fn-727 needs fn-724, and fn-743, fn-744, fn-745, fn-746 and fn-748 need fn-741. They are facts of the index today; by the ontology and the product owner's answer, a feature does not need another feature.
- The index holds one id for "identified by", while the ontology says it "may name more than one". One capability holds one today.
- No skill writes a need or an "identified by" link on a part that exists. Change a part from words a person approved (fn-change-part) is to do it.
- Orchestration's open point, "whether a feature's own needs count too, as the page of fn-725 says, or only the needs of its capability, as the ontology says", is answered by the product owner's answer of 2026-11-11: only the capability's. Its page, and its name for this feature, are reworded at this intent's close.

## Inputs / Outputs
- In: each capability's and feature's index entry: its intents, its `depends_on` list and its `identified_by`.
- In: each business intent page's Touches list.
- In: the ids of the capabilities, features, domains and business intents in the index.
- Out: each serves link kept on both sides, the index's and the intent page's.
- Out: from the structure check, one finding for each need or "identified by" link that names a part not in the index, work, a business intent, a domain or a feature, or that a feature holds, with the part, the field and the value. Not built.
- Out: after the rename, the field `needs` in the index and in every file that reads it, every value kept. Not built.

## Rules & behavior
- A serves link is kept on both sides. The reason: "Any play that links a node to an intent writes both sides".
- The intent page's side is written by a script, never by a model. The reason: "It is never written by an LLM."
- Needs and "identified by" name capabilities only. The reason: "A capability's "needs" and "identified by" name other capabilities only — never a feature, a business intent or a work item."
- A feature needs nothing; the slices keep the order of features. The reason: "It never needs anything and is never identified by anything. Its order of work comes from its parent capability.", and the product owner: "a feature doesn't need another feature. All of that is managed in the slices."
- An empty "identified by" means found on its own, and is not a gap. The reason, in the product owner's words: "I'll go with your proposal of no."; this page already said: "Empty means that the node was found on its own. This is normal and gives no warning."
- Only needs set an order. The reason: ""Identified by" says which node led us to find this one. It records where a node came from. It never sets an order."
- Work items carry none of these links. The reason: "Work never has these links."
- Business intents never need each other. The reason, from the old capability's page: "Business intents never need each other."
- A slice's link to its intents is kept on the slice's side only. The reason: "A slice serves it — the link is kept on the slice's side only".
- A link that points at nothing is a finding, never a stop. The reason: "missing links are warnings to fix later, not stops".
- The rename keeps every value. The reason: "The rename keeps every value."
- Not decided: what becomes of the six needs from one feature to another that the index holds today.
- Not decided: whether the index's "identified by" holds more than one id, as the ontology allows.

## Acceptance criteria
- Given a capability linked to an intent by a play that saves intents, when the link is written, then the capability's entry names the intent and the intent's Touches list names the capability.
- Given a capability that serves an intent whose page does not list it, when the gap finder runs, then it reports the link as kept on one side only.
- Given a need or an "identified by" link that names an id not in the index, when the structure check runs, then it names the part, the field and the value as a finding, and stops nothing. This is not built.
- Given a feature whose entry needs another feature, when the structure check runs, then it names the feature and the need as a finding, and stops nothing. This is not built.
- Given a capability whose "identified by" is empty, when the checks run, then they give no finding and no gap for it. This is not built.
- Given the index after the rename, when it is searched, then no capability or feature entry holds `depends_on`, and every value the old field held is kept, such as fn-743's need of fn-741, a fact of the index today, though a feature does not need another feature. This is not built.

## Out of scope
- How needs decide the ready answer. Say whether work can start on each part: ready, partly ready or not ready, with the gaps (fn-724) does it.
- Listing what serves an intent, and what sits in a domain. List what serves an intent, and what sits in a domain (fn-726) does it.
- Writing a link on a part that exists. Change a part from words a person approved (fn-change-part) does it.
- Closing a link kept on one side only. Find and close the gaps inside the model (fn-close-model-gaps) does it.
- Keeping an intent's links current as work changes it. Keep an intent's links current (fn-keep-intent-links-current), in Keep the spec matched to what's built, does it.
- Working out which plans a plan waits on, from the needs. Work out the plans a plan waits on (fn-work-out-waits-on), in Orchestrate agent work through planning, does it.
- The links as rules of the ontology. Define what a product is made of, in Product model, owns them.

## Sources
- .garura/product/product-os/features/fn-725/feature.md, the old page, lines 6, 21, 23, 24 and 34: ""Identified by" says which node led us to find this one. It records where a node came from. It never sets an order.", "A feature can need a capability or another feature.", "Empty means that the node was found on its own. This is normal and gives no warning.", "Work never has these links.", "The rename keeps every value."; line 50, the index's needs it names
- .garura/project/issues/1021/context/bi-11-write/old-pages/link-the-product-model.md, the copy of the old page of Link the product model, lines 6 and 29: "Each capability links to the business intents it serves. Each feature links to the capability that holds it.", "Business intents never need each other."
- .garura/project/issues/1021/context/capabilities.md, line 125: "I don't understand question 4. I'll go with your proposal of no.", "Apart from being found on its own, no, a feature doesn't need another feature. All of that is managed in the slices."
- standards/schemas/product-os/ontology.md, in Phoenix memory, lines 205, 344-345, 364 and 409: "A slice serves it — the link is kept on the slice's side only", "Other capabilities that must be done first — capabilities only", "The other capabilities that led us to find it — capabilities only, and may name more than one; empty when it was found on its own", "A capability's "needs" and "identified by" name other capabilities only — never a feature, a business intent or a work item.", "It never needs anything and is never identified by anything. Its order of work comes from its parent capability."
- core/components/plays/shape-slice/scripts/intent_touches.py, lines 12-14: "Any play that links a node to an intent writes both sides", "It is never written by an LLM."
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/capability.md, line 28: "A part linked or moved through them is missing from its intent's page."
- .garura/product/product-os/software-delivery-planning/orchestrate-agent-work/fn-work-out-waits-on/feature.md, lines 42 and 54: "Not decided: whether a feature's own needs count too, as the page of fn-725 says, or only the needs of its capability, as the ontology says."
- docs/standards/harness-standard.md, lines 71-72: "missing links are warnings to fix later, not stops"
- core/components/plays/create-play/references/lint_grounding.py: no line reads `depends_on` or `identified_by` (a search on 2026-11-11)
- A read of the index, .garura/product/product-os/_spine.yaml, on 2026-11-11: six needs from one feature to another, and one capability with an "identified by"
- The gap finder, run from the repository root on 2026-11-11: 21 links kept on one side only
- GitHub #725 (open): "\"Needs\" and \"identified by\" link capabilities"
- The stock-take, .garura/project/issues/1021/context/bi-11-inventory/inventory.md, sections 1.5, 2.5 and 4, and section 9, questions 4 and 5
