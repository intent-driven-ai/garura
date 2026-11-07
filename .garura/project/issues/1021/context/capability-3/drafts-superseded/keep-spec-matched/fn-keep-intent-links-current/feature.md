# Feature: Keep an intent's links current

## What it does
Keeps the list of parts each intent touches matched to the model's index, as parts are linked to it, moved or taken away.
- A business intent is what a person or the organisation wants, in their own words. Each intent page has a Touches list: every domain and capability the intent reaches into, each marked adds, changes or removes, with a link to that part's page. A domain is a big area of the product that groups capabilities; a capability is something the product can do.
- The same link has a second side in the model's index, `_spine.yaml`. The index is the model's list of every part, and each part's entry names, in `intents`, the intents it serves.
- One script, `intent_touches.py`, writes the intent's side, the same way for every play and never through a model. The plays that link a part to an intent call it: discovery when it saves intents and domains, /shape-slice when it fills a part a slice needs, and the gap-closing step inside the discovery loop.
- The gap finder (the skill find-model-gaps) compares the two sides over the whole model and reports each link held on one side only.
- The feature exists because a person reads the intent page and an agent reads the index. When both sides hold the link, each sees what the other sees.

Status: built in part. The plays above and the discovery loop write the Touches list. Not built: the Touches list from the two index skills and from the play that writes capabilities, and the record of what was done for an intent.

## Inputs / Outputs
- In: the intent page, and each part being linked to it: the part's title, the link to its page, its kind and its mark.
- In, for a part whose page moved: its old link and its new one.
- Out: the intent page with its Touches list added to or relinked, and every other line kept.
- Out, from the gap finder: each link to an intent held on one side only, with the side that is missing.

## Rules & behavior
- Each line has one form: the part's title linked to its page, its kind, and its mark. The kind is domain, capability or feature, and the mark is adds, changes or removes. A bad kind or mark refuses the entry. The reason: a fixed form lets a script read the list back and compare it with the index.
- A domain that a discovery run adds is marked adds, and one that was already there is marked changes. The reason: the mark tells the person what the intent does to that part of the product.
- The list sits just before What was done, on every intent page. On a later round of discovery, a list already on the page is kept. The reason: one place on every page, and no round undoes what another play wrote.
- A link is made only when both sides hold it. The gap finder reports a link held on one side only, and inside the discovery loop the gap-closing step writes the missing side. The reason: a link on one side only shows the person and the agent two different products.
- Not built: the two index skills and the capability play. link-model-part adds a part and its intents to the index, and remove-model-part moves a part from one intent to another. /discover-capabilities writes a new capability's intents in the index. None of them writes the Touches list. So a part linked or moved through them is missing from its intent's page, and outside the discovery loop nothing finds it.
- Not built: what was done. The page is meant to record what was delivered for the intent and the value each piece brought, with links to the finished work items, as work finishes. Every page reads "(nothing yet)", and no step writes it. So nothing on an intent's page links it to what was built for it.

## Acceptance criteria
- Given a domain linked to an intent for the first time in a discovery run, when the run saves, then the intent's Touches list holds that domain marked adds, and no other line of the page changed.
- Given a part whose page moved to a new folder, when it is relinked, then the intent's Touches line points at the new page.
- Given a capability whose index entry names an intent whose page does not list it, when the gap finder runs, then it reports that link with the Touches side missing.
- Given an intent page whose Touches list names a part that does not serve it, when the gap finder runs, then it reports that link with the index side missing.
- Given a capability linked to an intent through link-model-part, when the link lands, then the intent's Touches list names the capability. This is not built.

## Out of scope
- Deciding which part serves which intent, and the rules for links. Manage the model owns them.
- Changing the intent's own words. Update an intent from approved words (fn-update-intent-from-approved-words) does it.
- Moving the parts of an old intent to a new one. Replace or retire an intent (fn-replace-or-retire-intent) does it.
- Finding drift between the spec and the work. Find where the spec and what's built no longer match (fn-find-spec-drift) will do it.

## Sources
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
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Every domain and capability it reaches into, each marked adds, changes or removes, with a link to that part's page"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "What was delivered for it and the value each piece brought, with links to the finished work items — updated as work finishes"
