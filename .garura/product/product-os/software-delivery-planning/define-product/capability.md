# Capability: Define what a product is made of

## Directional intent
Define what a product is made of: People and agents share one agreed map of what a product is made of, changed only on purpose.
These are the agreed words for the first capability of Product model. The product owner set them in the list he locked on 2026-11-03, and kept them after the stock-take of what Garura has built. On the two capabilities of this intent he wrote, on 2026-11-11: "model is implementation of the onology. hence managing ontology is a differnet capability and then managing model is a different capability." So this capability manages the ontology, the map. The model is the ontology's implementation. Manage the model, the other capability of Product model, manages it, with its checks and its edits. This page is written from what is built. What is not built is drafted from his answers to the stock-take's questions and from the issues, and each part of it is named as not built.
This capability takes in one feature of an older capability, Link the product model, which was filed under the closed intent bi-722 (A product model can be managed, and grows as plans are built): Rebuild the product model as an ontology (fn-597). It keeps its id and its folder. Its page is rewritten to what was built: the map at version 15.
The words this page uses:
- The ontology is the written map of what a product is made of: the kinds of things, what each holds, how they link, and what must always be true. This page calls it the map.
- A kind is one sort of thing in the map, such as a Business Intent, a Capability, a Feature, a Slice, an ICE or a Story. A property is one thing a kind holds. A rule is what must be true once the product is aligned. Each kind has an example from a real kind of product.
- The model is a project's product model: its parts, each written to a kind of the map. A part is one domain, capability, feature, ICE or slice. The index is the model's list of every part. An ICE, an agent intent, is what an agent works from for one capability or one feature; it has its own page beside its part's page.
- The model's checks are the structure check, which checks the shape of the pages and the index; the ready check, which says whether work can start on a part; and the gap finder, which finds loose parts and links kept on one side only. Manage the model holds them.
- The map's play is /edit-ontology. A play is a command that a person or a loop runs to do one piece of work from start to end. A pinned checkpoint is a point where a play waits for a person's typed yes, and no setting turns the wait off.
- A harness repository is a repository that builds a harness, such as Garura's own. A product project is a team's project that uses Garura to build its product.
- Phoenix memory is the global memory that every project reads through the memory tool.

This capability does three jobs that are built:
- Write down what a product is made of: the kinds, what each holds, how they link, the rules and a real example of each.
- Change the map through one play, one need at a time, with the product owner's yes at three points.
- Bring the current map to every project.

One job that is built in part:
- Keep every part that reads the map in step with it: the page templates, the index's schema, the structure check and the glossary.

And five jobs that are not built:
- Run the model's checks before and after every change to the map, and show what the change breaks.
- Record which version of the map a model is built to, so an upgrade knows what to move.
- Let a team extend the map, with the plays changed with it.
- Define the product profile and the product decision as kinds of the map.
- Define the approval state each kind carries. This one is planned (#645, every piece of the model carries its approval state).

The map and the model go hand in hand. The product owner, on a team's own kinds: "Changing the ontology will break the place. It all has to go hand in hand, but it is extendable, which is fine." The record of his answers reads "the place" as the plays. So a change to the map is done only when the parts that read it follow it. And every change runs the model's checks before and after it: "Yes, every ontology should run the model before and after." The checks give findings and never stop the work, because this intent must not "Block work because the model is incomplete".
When the map changes, an upgrade moves a project's model to the new version. In his words: "as ontology changes, installing a new version will mean adding freature to upgrade and handle the changes to the model too". That feature is Move the product model to the new version's shape, on the person's yes (fn-move-model), in Upgrade a project, in Install and distribute. This capability gives it what it lacks: a record of which version of the map a model is built to.
How it sits with the other capabilities: Manage the model adds, changes, links, checks and takes out the model's parts; this capability says what a part is and what it holds. Memory, in Standards, structure, settings and memory, owns keeping Phoenix memory in step with Garura's source, and that is how a new version of the map is to reach every project; today a change reaches Phoenix memory only by hand. Standards holds the ICE of plays and loops; the ICE as a kind of the model is this capability's. Specify the product, in Product → Spec, owns the discovery plays that write the model's first pages. Review what agents make (Argus), in Developer tooling, writes a person's approval from their answers; the approval state that each kind carries is defined here.
Approved pages of other intents hand work here:
- what each kind is in the product model, and changing it, from Say what each work-item type means, for Initialize's brief, in Track execution in the team's tracker; and the kinds and their links, from Link each piece of work to its intent across trackers;
- the ICE as a kind of the model, with its rules, from Standards and from Build your own harness;
- the shape of the product model and how it is versioned, from Upgrade a project and its Move the product model to the new version's shape;
- where a project's setup answers sit in the product profile, from Set a project up after the install (Initialize);
- product decisions in the model, from Manage ADRs, in Orchestration;
- what the product model holds inside its folder, from Structure and from Memory;
- the kinds of the model and the rules of its pages and its index, from Orchestrate agent work through planning;
- the Plan kind, from See one plan as a tree and See every plan and where it stands;
- where the project's architecture sits in the model, from Take in each design choice that Spec → Design hands over.
Changing the map stops at three pinned checkpoints. The product owner types yes or a change, and no setting turns them off. Orchestration's Must not reads: "Stop a person. Every gate has a way past it that records what's owed." Whether the typed yes is the way past these gates, or a stop kept on purpose, is open (#992, every gate has a key). The list of pinned yeses and the way past them belong to Give every gate a way past, in Orchestration. A product project cannot change the map at all today, because the map's play is installed only in a harness repository.
It matters because the model only says what a product is when its parts mean the same to everyone who reads them. This intent's Why: "GitOps records changes but doesn't know what the product is. The model keeps intent connected to the product after the work closes." The map is what makes that hold: "A person and an agent reading it use the same words for the same things." It sits in software delivery planning with the other capability of Product model, and the domain's first paragraph says so.

Features:
- Write down what a product is made of: the kinds, what each holds, how they link, the rules and a real example of each (fn-597): the map, at version 15, defines thirteen kinds in two layers, each with its properties, links, rules and a real example, answers 45 of its 47 questions, and logs each version.
- Change the map through one play, one need at a time, with the product owner's yes at three points (fn-change-ontology): /edit-ontology changes only the kinds one need touches, waits for the product owner's typed yes at the questions, the kinds, and the links and rules, ends only when a script reads the map valid, and lands through the change plays; it runs only in a harness repository.
- Bring the current map to every project (fn-ontology-in-every-project): the settings name the map by its place in memory, Phoenix memory holds version 15, the same as Garura's source, and each play's agent reads it through the memory tool.
- Keep every part that reads the map in step with it: the page templates, the index's schema, the structure check and the glossary (fn-readers-in-step): each part that describes or checks the model's shape follows the map's current version; today each still describes an older map. Built in part.
- Run the model's checks before and after every change to the map, and show what the change breaks, as findings, never a stop (fn-check-model-on-change): each change to the map shows the product owner what it breaks in the model, recorded as owed. Not built.
- Record which version of the map a model is built to, so an upgrade knows what to move (fn-model-shape-version): the model says which version it is built to, so Move the product model to the new version's shape (fn-move-model) knows which moves it needs. Not built.
- Let a team extend the map, with the plays changed with it (fn-extend-ontology): a team adds its own kinds or rules to the map Garura provides, and changes the plays that read them with it. Not built.
- Define the product profile and the product decision as kinds of the map (fn-profile-decision-kinds): the profile and the product decision that the model already holds get their kinds, properties, links and rules in the map. Not built.
- Define the approval state each kind carries (fn-approval-state-kind): the map names one approval state for every kind, and maps the states of today onto it. Not built (#645, every piece of the model carries its approval state).

What is not built yet:
- Nothing runs the model's checks when the map changes. The model fails its own structure check today: 21 errors and 263 warnings, and 249 of the warnings ask for an ICE section that the map moved to its own page.
- The page templates, the index's schema, the structure check and the glossary still describe an older map: the ICE inside its part's page, one "identified by", and the ICE "attached" to its part. There is no template for an ICE page (#761, plays write ICE nodes; #764, Garura's own model moves to ICE nodes).
- The model records no version of its shape. The map and the index's schema each have a version, and the model's index has none, so an upgrade can tell a model's shape only by its old names.
- A product project cannot change or extend the map.
- The model holds a product profile and a product decision, and the map defines neither.
- No kind carries an approval state (#645, every piece of the model carries its approval state).
- Two of the map's 47 questions are open: Q3 is answered in part, and Q4 not yet.
- The Capability rule still counts a missing "identified by" as a gap, and the product owner answered that a part found on its own is not one.
- No kind says where a project's design outputs, such as its architecture, sit in the model.

### Benefit hypothesis
- Who it serves: the product owner, who agrees each change to the map; the technical lead and the developer, whose plays and agents write and check the model by the map; the agents and plays that read the map through the memory tool; and the capabilities that build on the map: Manage the model, which writes and checks the model's parts, Move the product model to the new version's shape, which moves a model to a new version, and the capabilities whose approved pages hand the kinds here.
- What we believe: when one written map says what a product is made of, changes only through one play with the product owner's yes, reaches every project at the same version, and every part that reads it follows it, people and agents use the same words for the same things, if the work stands on these rules:
  - One map, which every play reads through the memory tool.
  - The map changes only through its play, one need at a time, and the product owner agrees each change.
  - A script decides whether the map is valid.
  - Every change to the map runs the model's checks before and after it, and its findings never stop the work.
  - A rule of the map never stops a write.
  - Only a person confirms or drops a business intent.
- How we will know: the ontology check reads valid after every change; Phoenix memory holds the same version of the map as Garura's source; each change made through the play has the product owner's three typed yeses on record, one version step and one log line; and the model's checks, run before and after each change, show what it breaks.
  - The first two hold today: the check read valid on 2026-11-11, and Phoenix memory holds version 15, the same as the source, word for word.
  - The last does not hold, because nothing runs the model's checks when the map changes, and the model fails them before any change.

### Boundary (In / Out / Never)
- In: the map: its kinds, what each holds, how they link, its rules, a real example of each, the questions it must answer, its version and its log.
- In: changing the map through /edit-ontology, one need at a time, with the product owner's yes at three points, checked by a script and landed through the change plays.
- In: bringing the current map to every project, by its place in memory.
- In: keeping every part that reads the map in step with it: the page templates, the index's schema, the structure check and the glossary.
- In, not built yet: running the model's checks before and after each change to the map, a recorded version of the map a model is built to, a team's own extension of the map, the product profile and the product decision as kinds, and the approval state each kind carries.
- Out: the model itself: adding, changing, linking and taking out its parts, the model's checks, and keeping each part's approval state. Manage the model, in Product model, owns them.
- Out: moving a project's model to a new version's shape. Upgrade a project, in Install and distribute, owns it, through Move the product model to the new version's shape (fn-move-model).
- Out: keeping Phoenix memory in step with Garura's source, and its versions. Memory, in Standards, structure, settings and memory, owns it.
- Out: the ICE of plays and loops, and the standard each kind of harness part follows. Standards, in Standards, structure, settings and memory, owns them.
- Out: building and changing a play, a loop, a sub-agent or a skill. Build your own harness, in Standards, structure, settings and memory, owns it.
- Out: the discovery plays that write the model's first pages. Specify the product, in Product → Spec, owns them.
- Out: the list of pinned yeses, and the way past each gate. Give every gate a way past, in Orchestration, owns them.
- Out: writing a person's approval from their answers in the review. Review what agents make (Argus), in Developer tooling, owns it.
- Out: opening and landing the change that holds a change to the map. Ship every change the same way, in Developer tooling, owns it.
- Never: change the map outside its play. The reason: "This play is the only way to run the `author-product-ontology` skill."
- Never: let a rule of the map stop a write. The reason: "What a rule can stop is work, never a write".
- Never: let an agent confirm a business intent. The reason: "only a person confirms or drops a business intent."
- Never: write a change to the map as agreed before the product owner's yes. The reason: "Nothing is written as agreed before that yes."

### Guiding rules
- One need at a time, and only the kinds it touches change. The reason: "Every run works on one need, and changes only the kinds that need touches."
- Reuse before you invent. The reason: "Reuse before you invent. An existing kind is never redefined without a log line that says so."
- A script decides whether the map is valid. The reason: "A script decides whether the ontology is valid, not the model."
- Each change raises the version by one, with one log line. The reason: "The ontology version goes up by one, the date is set, and one log line says what changed and why."
- The map and the plays that read it change together. The reason, in the product owner's words: "It all has to go hand in hand, but it is extendable, which is fine."
- Every change to the map runs the model's checks before and after it. The reason, in the product owner's words: "Yes, every ontology should run the model before and after."
- Findings from the model's checks never stop the work. The reason: this intent must not "Block work because the model is incomplete", and "missing links are warnings to fix later, not stops".
- Nothing waits for the model to be complete. The reason: "A plan can be built and worked on before the product model is complete".
- Not decided: whether the three pinned yeses of the map's play are the way past that Orchestration's Must not asks for, or stops kept on purpose (#992, every gate has a key).
- Not decided: whether the version a model records is the map's own version, the index's schema version, or a version of the model's shape of its own.
- Not decided: how a team's own kinds are kept apart from the kinds Garura provides, so that an upgrade loses nothing the team added.
- Not decided: where a project's design outputs, such as its architecture, sit in the map; ADR 028 left it "Deferred".

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 1: "The capabilities, locked by the product owner on 2026-11-03"; line 122: "Define what a product is made of: People and agents share one agreed map of what a product is made of, changed only on purpose."
- .garura/project/issues/1021/context/capabilities.md, line 125, the product owner's answers of 2026-11-11 to the stock-take's eight questions: "Changing the ontology will break the place. It all has to go hand in hand, but it is extendable, which is fine.", "Yes, every ontology should run the model before and after.", "Managing the model should hold any checks of the model as well. Managing the model should hold the edits as well."; line 126, as read: "a team can extend the ontology Garura provides, and extending it means changing the plays with it ("Corona" and "the place" read as Garura and the plays)", "8, read as yes, the product profile and the product decision become kinds of the ontology"
- .garura/project/issues/1021/context/capabilities.md, line 128, the product owner on 2026-11-11: "model is implementation of the onology. hence managing ontology is a differnet capability and then managing model is a different capability.", "as ontology changes, installing a new version will mean adding freature to upgrade and handle the changes to the model too"; line 129, as read: "Define what a product is made of manages the ontology; Manage the model manages the model, the ontology's implementation, with its checks and its edits", "Question 8 stays yes (the product profile and the product decision become kinds of the ontology).", "Define gives it the model's recorded shape version it lacks."
- .garura/product/product-os/intents/bi-11.md, lines 5, 10 and 15: "GitOps records changes but doesn't know what the product is. The model keeps intent connected to the product after the work closes.", "A person changes the ontology through one play and the model still passes its checks.", "Block work because the model is incomplete"
- .garura/product/product-os/intents/bi-9.md, line 13: "Stop a person. Every gate has a way past it that records what's owed."
- standards/schemas/product-os/ontology.md, in Phoenix memory, the same as Garura's source word for word on 2026-11-11, lines 3, 9, 23, 25 and 868-893: "version: 15", "A person and an agent reading it use the same words for the same things.", "A plan can be built and worked on before the product model is complete", "What a rule can stop is work, never a write", "only a person confirms or drops a business intent.", "None. Every kind a question or a relationship names is defined above."
- core/components/plays/edit-ontology/reference/ice.md, lines 14-19, 25 and 27-28: "Every run works on one need, and changes only the kinds that need touches.", "Nothing is written as agreed before that yes.", "Reuse before you invent. An existing kind is never redefined without a log line that says so.", "A script decides whether the ontology is valid, not the model.", "The ontology version goes up by one, the date is set, and one log line says what changed and why."
- core/components/plays/edit-ontology/SKILL.md, lines 15 and 147-148: "This play is the only way to run the `author-product-ontology` skill.", "**pinned** — the product owner decides, C2; never skipped by config"
- core/components/skills/author-product-ontology/SKILL.md, line 15: "It is installed only in a harness repo, never into a product project."
- core/config.yaml, lines 181-183: "The ontology — the shape of the product model — by its place in memory.", "ontology: standards/schemas/product-os/ontology.md"
- docs/standards/harness-standard.md, lines 70-72, principle 6, Nothing is blocked: "missing links are warnings to fix later, not stops"
- docs/adr/028-agentic-lifecycle-five-loops.md, line 94, its open question 3, "Where do the project-wide design outputs live in the product model?": "**Deferred.** The product model is to be rebuilt as an ontology"
- .garura/product/product-os/software-delivery-planning/upgrade-project/capability.md, line 65: "Out: the shape of the product model itself, which Product model defines."; upgrade-project/fn-move-model/feature.md, lines 24 and 52: "Not decided: how the upgrade tells which shape a model is in. The spine records no version of its shape, so today only the old names tell.", "The model's shape itself and how it is versioned. Product model owns it."
- .garura/product/product-os/software-delivery-planning/track-execution/fn-say-what-each-type-means/feature.md, line 59: "Define what a product is made of, in Product model, owns the ontology."; track-execution/fn-link-work-across-trackers/feature.md, line 62: "Define what a product is made of, in Product model, owns the kinds and their links."
- .garura/product/product-os/software-delivery-planning/standards/capability.md, lines 32 and 33: "The ICE as a kind of the product model, with its rules, belongs to Define what a product is made of, in Product model; this capability holds the ICE of plays and loops.", "Build your own harness holds the builders that make and change a play or a loop, and building a sub-agent or a skill."; build-your-own-harness/capability.md, line 82: "Out: the ICE kind of the product model. Define what a product is made of, in Product model, owns it."
- .garura/product/product-os/software-delivery-planning/initialize/capability.md, line 61: "where the setup answers sit in the profile (Product model)"; initialize/fn-project-memory/feature.md, line 35: "Its shape has no place for them today, and Product model defines it."
- .garura/product/product-os/software-delivery-planning/manage-adrs/capability.md, line 63: "Out: product decisions in the product model, such as a move of the product profile, kept as a `decision.yaml` record. Product model owns them."; manage-adrs/fn-take-design-choices/feature.md, line 46: "Where the project's architecture sits in the product model. Product model owns the model's kinds."
- .garura/product/product-os/software-delivery-planning/structure/capability.md, line 66: "Out: what the product model holds inside its folder. Product model owns it."; memory/capability.md, line 86: "Out: what the product model holds and how it is written. Product model (BI-11) owns it"
- .garura/product/product-os/software-delivery-planning/orchestrate-agent-work/capability.md, line 78: "Out: the product model: its kinds, its pages, its index and their rules. Product model owns them."; orchestrate-agent-work/fn-795/feature.md, line 69: "The kinds of the model, the rules of its pages and its index, and the model's checks. Product model owns them."
- .garura/product/product-os/features/fn-628/feature.md, line 57: "What a plan file holds, as the ontology's Plan kind says. Product model owns it."
- .garura/product/product-os/software-delivery-planning/review-agent-work/capability.md, line 36: "The review step writes it from the person's answers"
- .garura/product/product-os/software-delivery-planning/memory/capability.md, line 42: Keep Phoenix memory in step with Garura's source, versioned per release with its notes (fn-phoenix-in-step); line 49: "A change reaches Phoenix memory only by hand"
- .garura/project/issues/1021/context/bi-11-write/old-pages/link-the-product-model.md, the copy of the old capability's page, line 33: "The ontology (fn-597): the written rules for each kind of part and its links, with examples from more than one field."
- The stock-take of Product model, .garura/project/issues/1021/context/bi-11-inventory/inventory.md, sections 1.1 to 1.8, 3.1, 3.3, 4, 5, 6, 7 and lean 2; the structure check's run on the whole model on 2026-11-11 (21 errors, 263 warnings), repeated for this page with the same result.
- GitHub #645 (open, every piece of the model carries its approval state, under #964, each piece carries its approval state and agents build only from approved pieces), #761 (open, plays write ICE nodes), #764 (open, Garura's own model moves to ICE nodes) and #992 (open, every gate has a key): the work named under What is not built yet.
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none covers how a framework keeps the map of what a product is made of. knowledge/domains/experience.md, in Phoenix memory, line 31, says "The ontology is the IP; storage is an implementation detail." of an experience product's own ontology, a loose match only.
- .garura/product/product-os/software-delivery-planning/domain.md, line 4: the domain's first paragraph, which does not name Product model yet.
- .garura/product/product-os/software-delivery-planning/domain.md: "It also defines what a product is made of, and keeps each product's model as a living map: added to, changed and pruned as work is done, and the source of what to try next."
