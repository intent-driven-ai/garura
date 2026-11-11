# Feature: Write down what a product is made of: the kinds, what each holds, how they link, the rules and a real example of each

## What it does
One written map, the ontology, says what a product is made of in Garura, its kinds, what each holds, how they link, the rules that hold once the product is aligned, a real example of each and the questions it must answer, so that a person and an agent who read it use the same words for the same things.
- The map is at version 15, updated on 2026-10-31. It is 893 lines long. Garura's source holds it, and Phoenix memory holds the same text, word for word.
- It defines thirteen kinds in two layers, with the Plan between them: the product layer, which is Business Intent, Source, Domain, Capability, Feature, Slice and ICE; the Plan; and the work layer, which is Epic, Story, Spike, Chore and Bug. Its list of kinds not yet defined reads "None."
- Each kind says what it is, who reads it, where it lives and what it is in the tracker, and has a table of its properties, a table of its links to other kinds, its rules and an example. Twelve of the thirteen have an example from a shop, a clinic and a bank; the Source has one, a shop's checkout prototype.
- It holds 47 questions that the map must answer, each with the kinds that answer it and its status. 45 are answered. Q3, whether two intents that want opposite things from one part are shown to a person before work starts, is answered in part. Q4, which work agents finished on their own and where a person stepped in, is not answered yet, because "no kind yet holds where a person stepped in".
- Its opening rules hold for every kind: nothing is blocked, and a plan can be built before the model is complete; no play owns a kind; a rule says what holds once the product is aligned and never stops a write; and only a person confirms or drops a business intent.
- Its log has a dated line for each change, from the first version, of 2026-10-08, to version 15, of 2026-10-31.
- A script checks its format: the front matter, its four sections, each question's answer and status, each kind's parts, and that each link points at a kind that is defined. On 2026-11-11 the check read it valid, with no problems.
- This feature first delivered version 5 (#597, rebuild the product model as an ontology, closed). Version 5 defined the Capability, the Feature, then named Functionality, Work and the Plan. Later versions made the ICE its own kind with its own page (version 6), set the two layers and the Slice (version 7), and changed the Plan's rules (versions 13 to 15). The Domain is now defined, and nothing is left under "Not yet defined".
- Examples, in different kinds of project:
  - In a clinic's booking app, the agent that writes the Reminders capability reads the Capability kind, and writes its ICE on its own page beside the capability's page, because the map says the ICE is "never a section of the capability page".
  - In a bank's payments service, the technical lead wants the feature Upload documents built before the feature Score the application. The Feature kind says a feature "never needs anything", so the order is kept in the slice, not as a link between the two features.
  - In a game studio's build, a developer finds a crash in a new level and files it as a Bug, a child of the Story whose work brought it in, as the Bug kind says.
- How it meets the capability: this is the "one agreed map of what a product is made of" itself, written down so that people and agents can share it.

Status: built, at version 15. Not built, or open:
- Q3 is answered in part, and Q4 is not answered yet.
- The Capability rule still says that a missing "identified by" "is a gap, and its ICE is partly ready". The product owner answered the stock-take's question 4, whether a part found on its own is a gap: "I'll go with your proposal of no." The change goes through Change the map through one play, one need at a time, with the product owner's yes at three points (fn-change-ontology).
- The map defines no kind for the product profile or the product decision (fn-profile-decision-kinds), and no approval state (fn-approval-state-kind).
- Where the project-wide design outputs live in the model was to be answered by this feature, and ADR 028 still holds it as "Deferred".

## Inputs / Outputs
- In: a need from the product owner, in plain words, through the map's play.
- In: the questions the map must answer, and the kinds, links and rules the product owner agreed at the play's three points.
- Out: the ontology: its front matter with the version and the date, its questions, its kinds, its list of kinds not yet defined, and its log.
- Out: the check report, which says whether the map is valid and names each problem.

## Rules & behavior
- A person and an agent read the same map. The reason: "A person and an agent reading it use the same words for the same things."
- Every kind holds the same parts, and the check fails a kind that lacks one. The reason: the check holds that every defined kind has, among its parts, "at least one Rule, and an Example".
- Each link points at a kind that is defined. The reason: the check holds that "every relationship points at a kind that is defined or listed as not yet defined".
- A rule says what holds once the product is aligned and never stops a write. The reason: "What a rule can stop is work, never a write".
- Nothing waits for the model to be complete. The reason: "A plan can be built and worked on before the product model is complete".
- Only a person confirms or drops a business intent. The reason: "only a person confirms or drops a business intent."
- A feature never needs another feature; their order is kept in the slices. The reason: the Feature kind's rule "It never needs anything and is never identified by anything. Its order of work comes from its parent capability.", and the product owner: "a feature doesn't need another feature. All of that is managed in the slices."
- The ICE is its own kind, on its own page. The reason: "The ICE is on its own page, never a section of the capability page."
- Each version has its log line. The reason: "The ontology version goes up by one, the date is set, and one log line says what changed and why."
- Not decided: where a project's design outputs, such as its architecture, sit in the map.
- Not decided: which kind holds where a person stepped in on the work of an intent, which Q4 asks for.

## Acceptance criteria
- Given the ontology, when its check runs, then it reads valid with no problems.
- Given any of the thirteen kinds, when a reader opens it, then it says what the kind is, who reads it and where it lives, and has its properties, its links, its rules and an example.
- Given the 47 questions, when a reader reads each, then it names the kinds that answer it and its status, and an answered question leans only on kinds that are defined.
- Given the log, when a reader looks for a version, then each version from the first to version 15 has its own dated line.
- Given a capability found on its own, when a reader reads the Capability rules, then an empty "identified by" is not a gap. This is not built.
- Given a project's architecture, when a reader looks for its kind in the map, then the map says where it sits. This is not built.

## Out of scope
- Changing the map. Change the map through one play, one need at a time, with the product owner's yes at three points (fn-change-ontology) does it.
- Bringing the map to every project. Bring the current map to every project (fn-ontology-in-every-project) does it.
- Keeping the page templates, the index's schema, the structure check and the glossary in step with the map. Keep every part that reads the map in step with it (fn-readers-in-step) does it.
- The kinds for the product profile and the product decision. Define the product profile and the product decision as kinds of the map (fn-profile-decision-kinds) does it.
- The model's parts written to the map, the links between them, and the model's checks. Manage the model, in Product model, owns them.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 122: "Define what a product is made of: People and agents share one agreed map of what a product is made of, changed only on purpose."
- .garura/project/issues/1021/context/capabilities.md, line 125, the product owner's answers of 2026-11-11: "I'll go with your proposal of no.", "a feature doesn't need another feature. All of that is managed in the slices."
- The stock-take of Product model, .garura/project/issues/1021/context/bi-11-inventory/inventory.md, section 9, question 4: "Is a part "found on its own" a gap?", proposed "no"; sections 1.1 and 1.5.
- standards/schemas/product-os/ontology.md, in Phoenix memory, the same as Garura's source word for word on 2026-11-11, lines 3-4: "version: 15", "updated: 2026-10-31"; line 9: "It defines thirteen kinds in two layers", "A person and an agent reading it use the same words for the same things."; line 23: "A plan can be built and worked on before the product model is complete"; line 25: "No play owns a kind.", "What a rule can stop is work, never a write", "only a person confirms or drops a business intent."
- The same, lines 35-40: Q3 "**Status:** partly", Q4 "no kind yet holds where a person stepped in", "**Status:** not yet"; line 362: "The ICE is on its own page, never a section of the capability page."; line 369: "is a gap, and its ICE is partly ready"; line 409: "It never needs anything and is never identified by anything. Its order of work comes from its parent capability."; lines 868-870: "None. Every kind a question or a relationship names is defined above."; lines 872-893, the log, from "2026-10-08 — First version" to "2026-10-31 — v15".
- A read of each kind of the map on 2026-11-11: each has its "In the tracker as" line and an example; twelve have a shop's, a clinic's and a bank's, and the Source has one, "Source — checkout prototype".
- core/components/skills/author-product-ontology/scripts/check_ontology.py, lines 12-16: "at least one Rule, and an Example", "every relationship points at a kind that is defined or listed as not yet defined"; run on 2026-11-11: "valid": true, 13 kinds, 45 questions answered, one partly, one not yet.
- core/components/plays/edit-ontology/reference/ice.md, lines 27-28: "The ontology version goes up by one, the date is set, and one log line says what changed and why."
- docs/adr/028-agentic-lifecycle-five-loops.md, line 94: "Where do the project-wide design outputs live in the product model?", "**Deferred.** The product model is to be rebuilt as an ontology"
- GitHub #597 (closed, rebuild the product model as an ontology): "The ontology is written down and agreed.", "It answers where project-wide design outputs live (ADR 028, open question 3), and ADR 028 is updated with the answer."
- The old page of this feature, .garura/product/product-os/features/fn-597/feature.md, before this rewrite, line 10: "This feature delivered version 5 (2026-10-21)."; and the copy of the old capability's page, .garura/project/issues/1021/context/bi-11-write/old-pages/link-the-product-model.md, line 33: "The ontology (fn-597): the written rules for each kind of part and its links, with examples from more than one field."
- Shelf: none covers how a framework keeps the map of what a product is made of.
