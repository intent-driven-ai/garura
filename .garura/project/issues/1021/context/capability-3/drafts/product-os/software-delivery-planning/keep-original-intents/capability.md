# Capability: Keep the original business intents

## Directional intent
Everything a person gives is kept exactly as given, and the intents stay up to date as the product evolves, with no drift.
A business intent is what a person or the organisation wants, in their own words, and only a person confirms or drops it. Each one has a page in the product model and an issue in the tracker that holds intents. The product model is the shared map of the product that people and agents read. This capability keeps each intent true after it is first written: its words change only through words a person approved, it stays in step with the parts of the product that serve it, and where an intent and the product no longer agree, the drift is named. It also proves that what a person gave can still be read as given.
It matters to software delivery planning because that domain turns a business intent into work that agents can build. Agents build from the model, so an intent that is lost, rewritten without approval or out of date sends the work after the wrong thing.

What makes it unique: most tools lose the intent once the work starts. Here the intent stays the person's record, in their words, while the product changes around it.

Features:
- Write an intent from approved words (fn-write-intent-page): writes or rewrites a business intent's page from words a person approved, and keeps its record of what was done.
- Keep an intent current (fn-keep-intent-current): keeps the list of parts each intent touches in step with the model, as parts are linked to it.
- Replace or retire an intent (fn-replace-intent): moves the parts that serve an old intent to a new one, and removes the old page once nothing names it, on a person's named approval.
- Keep intents in their own tracker (fn-intents-tracker): a setting names the tracker that holds business intents, apart from agent work, and each intent page names its issue there.
- Name an intent's drift (fn-name-intent-drift): finds where an intent and the product no longer agree, and names the drift to a person.
- Read back what a person gave (fn-read-back-given): proves that each Source a person gave can still be read exactly as it was when read.

What is not built yet:
- Name an intent's drift is not built. Older records send drift to an "Alignment loop", which is not built and has no approved name or place. Today only the discovery loop's gap finder finds two kinds of it, and only during discovery.
- Read back what a person gave is not built. Each capture records a fingerprint of every saved file, and no step checks the files against it later.
- A rewrite of an intent page drops its list of Sources, so a rewritten intent loses its link to what the person gave.
- The two skills that change the model's index outside a play do not write an intent's list of the parts it touches. A part linked or moved through them is missing from its intent's page.
- Nothing records what was done for an intent as work finishes, and nothing marks an intent met when its proof holds.
- No tool reads the intents tracker setting yet. No play files an intent there, and nothing keeps the issue's words and the page's words the same.

### Benefit hypothesis
- Who it serves: the product owner, who confirmed the intents and needs them kept as they said them, and the agents that build from the model, which need intents that match the product.
- What we believe: an intent stays useful across sessions and changes, if the work stands on these rules:
  - Only a person's approved words change an intent. No agent rewrites what a person wants.
  - Every link between an intent and a part is held on both sides, so the person's page and the agent's index show the same thing.
  - Drift is named to a person, never fixed in silence.
- How we will know: a person reads an intent long after confirming it, next to what they gave, and both still say what they said. And when the product changes so that an intent no longer fits it, the drift is named before anyone builds on it.
  - Neither is tested today, because the read-back and the drift check are not built.
  - What can be tested today: the gap finder, run over the whole model, finds every link to an intent that is held on one side only.

### Boundary (In / Out / Never)
- In: changing an intent's page after it is first written, only from words a person approved. Whoever drafts the intent writes its first page; after that, this capability keeps it.
- In: keeping what each intent touches in step with the model's index. The index is the model's list of every part with its parent and the intents it serves, kept in one file, `_spine.yaml`.
- In: moving the parts that serve an old intent to a new one, and removing the old intent's page, on a person's named approval.
- In: where intents are kept: a tracker of their own, apart from agent work.
- In: naming drift between an intent and the product, and proving later that what a person gave still reads as given.
- Out: capturing what a person gives and keeping it as a Source at the moment it is read. A Source is a saved copy of a file, a project folder, a deployed site, a document or a person's own words. Specify the product captures it, through its Specify-from features; this capability checks later that it still reads as given.
- Out: drafting an intent from what a person gave, and sorting new input against the intents that exist. Specify the product owns both.
- Out: the rules for which part links to which, and finding the link a loose part needs. Manage the model owns them. This capability keeps the intent's own page in step once a link is made.
- Out: merging one capability into another and removing a slice. The same removal skill does them, and Manage the model owns them.
- Out: drift with no intent in it, such as two ICE for one part or a story out of date with its ICE. An ICE is the agent's intent for one capability or feature. Manage the model and Turn intents into agent work own those.
- Never: change a person's words without their approval. A rewrite that names no confirming person goes back to proposed. The reason: the intent is the person's interface to the product, so an agent that rewrote it would build what the agent wants.
- Never: lose the record of what was done for an intent when its words change. The reason: the words are new, but what happened to the intent is history.
- Never: remove an intent while any part still names it. The reason: that part would then serve an intent that no longer exists.

### Guiding rules
- Anyone writes; align later. Any play may write the intents and parts it finds, in any order, and the model's rules say what holds once it is aligned. A rule never stops a write. The reason: what is found in the middle of work is kept, not lost while it waits for the right step. This is also why drift happens, and why it must be named.
- A link is made only when both sides hold it. The part's entry in the index names the intent, and the intent's page names the part in its Touches list, with a mark: adds, changes or removes. The reason: a person reads the intent page and an agent reads the index, so both must show the same link.
- Words change only from words a person approved. A whole page is rewritten from an approved draft, and a few lines change through a request that names each line and where its new words came from. Each is all or nothing. The reason: the meaning comes from the person or an approved design, never from the tool that writes it.
- A removal names the person who approved it, and checks everything before the first write. The reason: an intent removed by mistake takes its links with it.
- Only tools know the tracker. Plays, skills and sub-agents name no tracker; a setting names where intents and agent work live, and a tool reads it. The reason: a team can choose its tracker, and a new tracker then means changing one tool.
- BI-1 means a business intent and #1 means a work issue. The reason: each tracker numbers its own issues from one, so a bare number could mean two things.
- Drift is named to a person and never fixed in silence. The reason: only a person confirms or drops a business intent, and a fix to an intent's words is a change to what they want.

## Sources
- The one line the product owner approved on 2026-11-03: "Keep the original business intents: Everything a person gives is kept exactly as given, and the intents stay up to date as the product evolves, with no drift. (unique)"
- .garura/product/product-os/intents/bi-1.md: "The original intents are kept and stay up to date as the product evolves.", "Most tools lose the intent once the work starts.", "Everything a person gave can still be read as given.", "An intent that drifts from the product gets named."
- .garura/product/product-os/software-delivery-planning/domain.md: "This domain turns a business intent into work that agents can build"
- .garura/product/product-os/software-delivery-planning/specify-product/capability.md: "In: keeping what a person gives as a Source.", "Out: keeping intents up to date as the product changes. This capability does not do it, and no capability in the model owns it yet."
- core/components/skills/author-intent-page/SKILL.md: "It drafts nothing.", "It never confirms by itself.", "a rewrite with no stage goes back to proposed, whatever the old page said", "A rewrite keeps the old page's What-was-done"
- core/components/skills/enrich-grounding/SKILL.md: "change of meaning is the person's or an approved design's"
- core/components/plays/discover-domains/scripts/intent_touches.py: "Any play that links a node to an intent writes both sides; this module writes the"
- core/components/skills/find-model-gaps/scripts/find_gaps.py: "A link is made only when both sides hold it"
- core/components/skills/remove-model-part/scripts/remove_part.py: "The model never loses a part by accident: a removal names the person who approved it, and it"
- core/components/plays/discover-intent/scripts/persist_intent.py: 'lines.append("**Sources:**")'. A rewrite through author-intent-page keeps only the Touches and What-was-done blocks, so this list goes; tried on a throwaway copy of such a page.
- core/components/plays/discover-intent/scripts/capture_source.py: "keep a Source exactly as it was when read", "def sha256(path):"
- core/config.yaml: "# Which tracker holds what. Tools read this; plays, skills and sub-agents never name a tracker."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "Business intents and agent work each live in a tracker named in the project's settings.", "No script reads the new `trackers` settings yet", "BI-7 means an intent and #7 means work, in text."
- docs/adr/043-kickoff-plays-read-independently-and-the-drive-closes-the-loop.md: 'The doctrine "anyone writes; align later"'
- docs/adr/031-business-intent-and-ice.md: "(its own drive, not yet designed)"
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md: "the Alignment loop is unapproved and unnamed"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The rules below say what holds once the product is **aligned**; they never stop a write.", "Drift between them is found and fixed by the Alignment loop.", "One thing is never left to alignment: only a person confirms or drops a business intent."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "What was delivered for it and the value each piece brought, with links to the finished work items — updated as work finishes", "proposed → confirmed (the person who asked confirms it says the right thing) → met (its proof holds)"
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf covers software delivery planning.
