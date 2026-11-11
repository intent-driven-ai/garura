# Capability: Keep the spec matched to what's built

## Directional intent
As the product is built and changed, the spec (the intents, domains, capabilities and features) is kept matched to what's implemented and planned, and any drift between them is named and fixed.
This is about the inside of the work: what the agents build and plan is brought back into the spec. What users say once the product runs is not part of it. Run → Product handles that.
The spec is what the product model says the product is for and what it does. The product model is the shared map of the product that people and agents read. The spec has four kinds of part:
- A business intent is what a person or the organisation wants, in their own words. Only a person confirms or drops one.
- A domain is a big area of the product that groups capabilities.
- A capability is something the product can do.
- A feature is one thing a person can do inside a capability.

What is built is the code and the work that landed. What is planned is the work items in the team's tracker, the tool where a team keeps its issues, such as GitHub, and the plan files that hold them as a tree. Drift is a difference between the spec and what is built or planned. For example, a feature is built and has no page in the model, a page says something the work no longer does, or an intent and a part that serves it name each other on one side only.
This capability keeps the spec true after it is first written. It finds drift and names it to a person. It changes an intent or a model part only from words a person approved. It keeps each intent's links to the parts that serve it, replaces or retires intents, and keeps an intent's words in the tracker matched to its page.
It matters to software delivery planning because that domain turns a business intent into work that agents can build. Agents decide from the spec, so a spec that falls behind the work sends them after the wrong thing.

What makes it unique: most tools write the spec once and lose it once the work starts. Here the spec is kept matched to the product while it is built and changed.

Features:
- Update the spec to match what's built (fn-update-spec-to-match-built): when the work changes what the product does, the pages of the spec that it makes out of date are updated to say what the product now does.
- Keep an intent's links current (fn-keep-intent-links-current): as parts are built, moved or removed, the link between each business intent and the parts that serve it stays matched, on both of its sides.
- Replace or retire an intent (fn-replace-or-retire-intent): when the work shows that an intent has been replaced or is no longer wanted, and the person approves it, the spec is changed to match.
- Keep the tracker's words matched to the model (fn-keep-tracker-matched): each intent's issue in the tracker says what the intent's page in the product model says.
- Find where the spec and what's built no longer match (fn-find-spec-drift): finds the places where the spec no longer matches what the agents built and planned, and names each one to a person.

What is not built yet:
- Find where the spec and what's built no longer match is not built. Older records send drift to an "Alignment loop", which has no approved name or place. Today only the discovery loop's gap finder finds a few kinds of drift inside the model, and only during discovery.
- A rewrite of an intent page drops its list of Sources. A Source is a saved copy of what a person gave, such as a file, a document or their own words. A rewritten intent then loses its link to what the person gave.
- The two skills that change the model's index outside a play, and the play that writes capabilities, do not write an intent's list of the parts it touches. A part linked or moved through them is missing from its intent's page.
- Nothing records what was done for an intent as work finishes, and nothing marks an intent met when its proof holds. So no page of the spec says what was built for an intent.
- Nothing keeps an intent's issue in the tracker matched to its page. No tool reads the setting that names the tracker for intents.

### Benefit hypothesis
- Who it serves: the product owner, who approved the spec and needs it to say what the product really does; and the agents that build from the model, which decide from the spec.
- What we believe: agents keep building the right thing while the product changes, if the work stands on these rules:
  - What was built is the ground truth for the domains, capabilities and features. Their pages are brought up to match the work.
  - An intent changes only from a person's approved words. A difference between an intent and the work goes to that person.
  - Every link between an intent and a part is held on both sides.
- How we will know: a review run after work lands names every place where the spec and the work disagree, before anyone builds on it.
  - This is not tested today, because the drift check is not built.
  - What can be tested today: the gap finder, run over the whole model, finds every link to an intent that is held on one side only.

### Boundary (In / Out / Never)
- In: finding where the spec and what is built or planned no longer match, and naming each difference to a person.
- In: updating an intent or a model part when the implementation changes, only from words a person approved. Whoever first specifies a part writes its first page; after that, this capability keeps it.
- In: keeping each intent's links to the parts that serve it current. The link has two sides: the intent page's Touches list, and the part's entry in the model's index. The index is the model's list of every part with its parent and the intents it serves, kept in one file, `_spine.yaml`.
- In: replacing an intent with another, or retiring it, on a person's named approval.
- In: keeping an intent's words in the tracker matched to its page.
- Out: the first specification of the product, which turns what a person gives into the first intents, domains, capabilities and features. Specify the product owns it. Keeping what a person gave stays there too: Specify the product saves each copy, a Source, when it reads it.
- Out: cutting the spec into the work items agents execute, and changing a work item that no longer matches the spec. Turn intents into agent work owns both. This capability names the drift; that capability changes the work item.
- Out: learning from real users once the product runs, where what happens in use is compared with what was intended. The Run → Product business intent (BI-6) asks for it.
- Out: the rules for which part links to which, and drift inside the model with no work in it, such as two ICE for one part or the same part written twice. An ICE is the agent's intent for one capability or feature. Manage the model owns them, and also merges capabilities and removes slices.
- Never: change a person's intent without their approval. A rewrite that names no confirming person goes back to proposed. The reason: the intent is what the person wants, so an agent that rewrote it to match the code would build what the agent wants.
- Never: fix drift in silence. Each difference is named to a person, and its fix lands only after their yes. The reason: the spec is what the person approved and what agents decide from, so a silent fix changes both without anyone knowing.
- Never: lose the record of what was done for an intent when its words change. The reason: the words are new, but what happened to the intent is history.
- Never: remove an intent while any part still names it. The reason: that part would then serve an intent that no longer exists.

### Guiding rules
- Anyone writes; align later. Any play may write the intents and parts it finds, in any order, and the model's rules say what holds once it is aligned. A rule never stops a write. The reason: what is found in the middle of work is kept, not lost while it waits for the right step. This is also why drift happens, and why it must be found.
- What was built is the ground truth for the domains, capabilities and features. When their pages and the work disagree, the page is brought up to match the work. The reason: agents decide from the model, so a page that describes work that is no longer there leads them wrong.
- An intent is different. It says what a person wants, not what the code does. So a difference between an intent and the work goes to the person, who decides whether the intent or the work changes. The reason: only a person confirms or drops a business intent.
- Words change only from words a person approved. A whole page is written from approved words, and a few lines change through a request that names each line and where its new words came from. Each is all or nothing. The reason: the meaning comes from the person or an approved design, never from the tool that writes it.
- Each fix is made by the part that owns it: an intent or a model page through Update the spec to match what's built, a link through Keep an intent's links current, and a work item through Turn intents into agent work. The reason: each part then has one writer and one set of checks, so a fix is checked like any other change.
- A link is made only when both sides hold it. The part's entry in the index names the intent, and the intent's page names the part in its Touches list, with a mark: adds, changes or removes. The reason: a person reads the intent page and an agent reads the index, so both must show the same link.
- A removal names the person who approved it, and checks everything before the first write. The reason: an intent removed by mistake takes its links with it.
- The tracker follows the page. An intent's page holds the words a person approved, and its issue in the tracker shows the same words. The reason: people read the issue and agents read the page, so two versions of one intent send them different ways.

## Sources
- The one line the product owner approved on 2026-11-07: "As the product is built and changed, the spec (the intents, domains, capabilities and features) is kept matched to what's implemented and planned, and any drift between them is named and fixed."
- The boundary the product owner approved on 2026-11-07: In, finding drift, updating an intent or a model part only from approved words, keeping an intent's links current, replacing or retiring an intent, and keeping an intent's words in the tracker matched to its page; Out, the first specification, cutting the spec into work, and learning from real users once the product runs.
- .garura/product/product-os/intents/bi-1.md: "The original intents are kept and stay up to date as the product evolves.", "Most tools lose the intent once the work starts.", "An intent that drifts from the product gets named."
- .garura/product/product-os/intents/bi-6.md: "What happens in use flows back."
- .garura/product/product-os/software-delivery-planning/domain.md: "This domain turns a business intent into working code that a check from the outside can prove."
- .garura/product/product-os/software-delivery-planning/specify-product/capability.md: "In: keeping what a person gives as a Source.", "Out: keeping intents up to date as the product changes."
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/capability.md: "In: changing the work items later, and adding a feature found during work.", "A story is not written again when its ICE changes."
- GitHub #977 (open): "The product model falls behind the work.", "Agents decide from the model, so a model that is out of date leads them wrong.", "What was built is the ground truth: the model is brought up to match it, not the other way round"
- GitHub #977 (open): "Approve the fixes, and have them written into the model by the plays that own each part."
- core/components/skills/author-intent-page/SKILL.md: "It drafts nothing.", "It never confirms by itself.", "a rewrite with no stage goes back to proposed, whatever the old page said", "A rewrite keeps the old page's What-was-done"
- core/components/skills/enrich-grounding/SKILL.md: "change of meaning is the person's or an approved design's"
- core/components/plays/discover-domains/scripts/intent_touches.py: "Any play that links a node to an intent writes both sides; this module writes the"
- core/components/skills/find-model-gaps/scripts/find_gaps.py: "A link is made only when both sides hold it"
- core/components/skills/remove-model-part/scripts/remove_part.py: "The model never loses a part by accident: a removal names the person who approved it, and it"
- core/components/plays/discover-intent/scripts/persist_intent.py: 'lines.append("**Sources:**")'
- core/components/plays/discover-capabilities/scripts/persist_understand.py: '"intents": intents, "status": "proposed",'
- core/config.yaml: "# Which tracker holds what. Tools read this; plays, skills and sub-agents never name a tracker."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "No script reads the new `trackers` settings yet"
- docs/adr/031-business-intent-and-ice.md: "(its own drive, not yet designed)"
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md: "the Alignment loop is unapproved and unnamed"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The rules below say what holds once the product is **aligned**; they never stop a write.", "Drift between them is found and fixed by the Alignment loop.", "One thing is never left to alignment: only a person confirms or drops a business intent."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "What was delivered for it and the value each piece brought, with links to the finished work items — updated as work finishes", "It is met by its proof, never because its work is finished.", "Two ICE for one part are drift"
- The capability list the product owner locked on 2026-11-03: "Manage the model: A living map, added to and pruned as work is done"
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf covers software delivery planning.
