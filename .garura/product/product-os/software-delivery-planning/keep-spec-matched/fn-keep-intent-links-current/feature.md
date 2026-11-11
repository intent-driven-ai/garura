# Feature: Keep an intent's links current

## What it does
As parts are built, moved or removed, the link between each business intent and the parts that serve it stays matched, on both of its sides.
- A business intent is what a person or the organisation wants, in their own words. The parts that serve it are the domains, capabilities and features that the work builds for it. A domain is a big area of the product that groups capabilities, a capability is something the product can do, and a feature is one thing a person can do inside a capability.
- Each link has two sides, and both must say the same thing:
  - On the intent's page, the Touches list names each part that the intent reaches into. Each line links to the part's page and has a mark: adds, changes or removes. A person reads this side.
  - In the model's index, each part's entry names the intents it serves. The index is the model's list of every part, with its parent and its intents. An agent reads this side.
- The link changes when the work changes:
  - When a part is built for an intent, the part is linked to the intent on both sides.
  - When a part moves to a new place, the intent's line goes to the part's new page.
  - When a part is removed, the intent's page stops naming it.
- When a link is found on one side only, it is named with the side that is missing. The gap finder, a check that compares the two sides over the whole model, finds these links.
- The feature exists because a person reads the intent page and an agent reads the index. When the two sides differ, the person and the agent see two different products, and the person cannot see from the intent what was built for it.

Status: built in part. The plays that save intents and domains, the play that fills the parts a slice needs, and the discovery loop's step that closes gaps write the intent's side when they link a part. The gap finder finds a link held on one side only. Not built: the intent's side when the model's two index skills or the capability play link or move a part. Outside the discovery loop, nothing writes the missing side. Today the gap finder finds many links that are in the index and missing from the intent's page.

## Inputs / Outputs
- In: a part linked to an intent, because the work built it for that intent or a person named the intent it serves.
- In: a part that moved to a new place, with its old page and its new page.
- In: a part that was removed.
- In: a link found on one side only, with the side that is missing.
- Out: the link holds on both sides. The intent's page lists the part with its mark and a link to the part's page, and the part's entry in the index names the intent.
- Out: for a part that moved, the intent's line goes to the part's new page. For a part that was removed, the intent's page does not name it.
- Out: each link that is still on one side only, with the side that is missing, for a person to see.

## Rules & behavior
- A link is made only when both sides hold it. The work that writes one side also writes the other side, in the same change. The reason: a person reads the intent page and an agent reads the index, so both must show the same link.
- The link follows the work. A part built for an intent is linked to it, a part that moves keeps its link, and a part that is removed leaves no line behind. The reason: the link shows what was built for the intent, so it must change when the work changes.
- A link never changes the intent's own words. Only the Touches list changes, and every other line of the intent page stays as it was. The reason: the list records which parts serve the intent, but what the person wants stays the person's words.
- A script writes the intent's side, from the same link that the work writes in the index, and an AI model never writes it. The reason: a link is a fact about the model, not a sentence to compose, so it must be the same every time.
- Each line has one fixed form: the part, a link to its page, its kind and its mark. The mark says what the intent does to that part: it adds a new part, changes a part that was there, or removes one. The reason: a fixed form lets a check read the list back and compare it with the index, and the mark tells the person what the intent does to the product.
- A link on one side only is named, never left. The gap finder names the link and the side that is missing. Inside the discovery loop, the step that closes gaps writes that side. The reason: a link on one side only shows the person and the agent two different products.
- Not built: the intent's side from the index skills and the capability play. One index skill adds a part and its intents to the index, and one moves a part from one intent to another. The capability play writes a new capability's intents in the index. None of them writes the Touches list. So a part linked or moved through them is missing from its intent's page, and outside the discovery loop nothing writes the missing side.
- Not decided: whether the Touches list may name a feature. The model's rules say a feature is reached through its parent capability, but the tools accept a feature on the list. Until this is decided, a feature's link may be held on one side only.

## Acceptance criteria
- Given a capability built for an intent and linked to it, when the change lands, then the intent's page lists the capability with its mark and a link to its page, and the capability's entry in the index names the intent.
- Given a part whose page moved to a new place, when the move lands, then the intent's line goes to the new page.
- Given a part linked to an intent, when the link is written, then no line of the intent page changes except the Touches list.
- Given a part whose entry names an intent whose page does not list it, when the gap finder runs over the whole model, then it names that link with the intent's side missing.
- Given an intent page whose Touches list names a part that does not serve it, when the gap finder runs, then it names that link with the index side missing.
- Given a capability linked to an intent through an index skill outside the discovery loop, when the link lands, then the intent's page lists the capability. This is not built.

## Out of scope
- The rules for which kind of part links to which, and links inside the model with no work in them. Manage the model owns them.
- The words of an intent or a part. Update the spec to match what's built (fn-update-spec-to-match-built) changes them.
- Moving the parts of a replaced or retired intent to a new one. Replace or retire an intent (fn-replace-or-retire-intent) moves them, and this feature then keeps the new intent's side.
- Finding drift between the spec and the work. Find where the spec and what's built no longer match (fn-find-spec-drift) will do it.

## Sources
- The capability page the product owner approved on 2026-11-07: "Every link between an intent and a part is held on both sides.", "A link is made only when both sides hold it."
- core/components/plays/discover-domains/scripts/intent_touches.py: "Any play that links a node to an intent writes both sides; this module writes the", "It is never written by an LLM."
- core/components/plays/discover-intent/scripts/persist_intent.py: "Its Touches list is written later, by the plays that link a part to the"
- core/components/plays/discover-domains/scripts/persist_seed.py: "in this run, `changes` when it was already there"
- core/components/plays/shape-slice/scripts/persist_fills.py: "import intent_touches as touches"
- core/components/skills/link-model-gaps/SKILL.md: "and adds each `intents` link on both sides (the spine and the intent page's Touches list,"
- core/components/skills/find-model-gaps/scripts/find_gaps.py: "A link is made only when both sides hold it"
- core/components/skills/find-model-gaps/SKILL.md: "Every `one_way` entry is a gap: a link is made only when both"
- core/components/skills/link-model-part/SKILL.md: "Put a domain, capability or feature into the product model's spine", "It never writes a page's words"
- core/components/skills/remove-model-part/SKILL.md: "It never writes a page's words"
- core/components/plays/discover-capabilities/scripts/persist_understand.py: '"intents": intents, "status": "proposed",'
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Every domain and capability it reaches into, each marked adds, changes or removes, with a link to that part's page", "It does not name features; a feature is reached through its parent capability"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "A play that makes one side writes the other."
- The gap finder, run read only over the model on 2026-11-07: every link it found on one side only was in the index and missing from the intent's page.
