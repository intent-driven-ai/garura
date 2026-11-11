# Capability: Manage the model

## Directional intent
Manage the model: A living map, added to, changed and pruned as work is done, and the source of what to try next.
These are the product owner's words for the second capability of Product model, locked on 2026-11-03, with one word added: "changed", which the stock-take's first lean proposed so that the line names the second proof of Product model, "Any part can be added, changed or removed." On 2026-11-11 he set what this capability holds: "Managing the model should hold any checks of the model as well. Managing the model should hold the edits as well." He also set it apart from the ontology: "model is implementation of the onology. hence managing ontology is a differnet capability and then managing model is a different capability. what we are doing here is managing the model, and we have some implementation in place while plays are missing, templates are missing etc." So this page is written from what is built, and the plays, templates and tools it lacks are its features, each named with its issue where one exists.
This capability takes in the old capability Link the product model, filed under an older business intent, now closed (A product model can be managed, and grows as plans are built). Its old page said that "work can start before the model is complete, if the model links its parts by these rules". Its ready check is built; its link check and its search by domain are not. Three of its features stay here, with their ids and their folders, each rewritten to what was built: fn-724 is the ready check, fn-725 the links between parts, and fn-726 the list of what serves an intent and what sits in a domain. Its fourth feature, fn-597, the ontology itself, belongs to Define what a product is made of.
The words this page uses:
- The product model is the shared map of the product that people and agents read: its business intents' pages, its domains, capabilities, features, their ICE and its slices. A part is one domain, capability, feature, ICE or slice in it.
- The ontology is the written map of what a product is made of: its kinds, what each holds, how they link, and the rules. The model is its implementation. Define what a product is made of keeps the ontology; this capability keeps the model.
- The index is the model's list of every part, with each part's parent, the business intents it serves, its page and its marks. The Touches list is the list on an intent page of the parts the intent reaches into. A link kept on both sides is in the part's index entry and on the intent's Touches list.
- An ICE, an agent intent, is what an agent works from for one capability or feature: its Intent, its Context and its Expectation, on its own page beside the part's page. A thin part or ICE is one proposed from a person's words and marked to be deepened later.
- A part found during work is one that a person or a play finds while other work goes on, and that the model does not hold yet. A part found on its own is one that no other part led us to find.
- The keeper is the sub-agent that writes the model. It writes only through the model's skills: the page skill, which writes a page's words; the two index skills, one that adds or changes a part's entry and one that takes a part out; the intent-page skill; and the gap finder and the gap closer.
- The structure check reads the model's pages and its index for their shape and their links. The ready check says, for each part, whether work can start on it: ready, partly ready or not ready.
- A business intent is what a person wants, in their words. A play is a command a person or an agent types to run one piece of work from start to end. A loop runs plays in rounds until its goal is met.

This capability does three jobs that are built:
- Change a part from words a person approved.
- Say whether work can start on each part, with the gaps.
- Check the model's structure and links on every change.

Six jobs that are built in part:
- Add a part found during work, with its page and its index entry.
- Take a part out on a person's named approval.
- Link the parts by the ontology's rules, on both sides.
- Find and close the gaps inside the model.
- List what serves an intent, and what sits in a domain.
- Change the model's index only through the two index skills.

And four jobs that are not built:
- Keep each part's approval state.
- Move the model with the work.
- Create and edit the model with one tool that knows its shape.
- Propose what to try next from the model, and record each experiment's result.

The work is split between parts: a play or a person names the change, the keeper gathers what it needs, a skill writes it, and scripts do the fixed steps, each all or nothing. The keeper's rule: "You may change any part of it — a page, the spine, an intent page, the profile — but only through a skill".
Two of today's built parts are out of step with the product owner's answers of 2026-11-11. A part found on its own is not a gap ("I'll go with your proposal of no."), but the ready check still counts a missing "identified by" as a gap, so no part reads ready. A feature does not need another feature ("a feature doesn't need another feature. All of that is managed in the slices."), but the index still holds six needs from one feature to another.
This capability and Define what a product is made of work as a pair. Define keeps the ontology, and so the kinds, what each holds and the rules for their links; this capability keeps the model that follows it, its checks and its edits. Every change to the ontology runs the model's checks before and after ("every ontology should run the model before and after"); the checks are this capability's. When the ontology changes, Move the product model to the new version's shape (fn-move-model), in Upgrade a project, moves a project's model.
Approved pages of other intents hand work here:
- the rules for which part links to which, drift inside the model with no work in it, merging capabilities and removing slices, from Keep the spec matched to what's built, in Product → Spec;
- merging or taking out another part, from Build features or update the product model, on its own or at least as recommendations, in Run → Product;
- the link rules the step after each round of a loop applies, from Run plays as loops;
- how the model takes in a change left for later (#990), from Give every gate a way past;
- the needs links and their name in the index, and removing parts of the model, from Orchestrate agent work through planning;
- the approval state on each piece of the model (#964), from Review what agents make (Argus), in Developer tooling.
This intent's Must not reads: "Block work because the model is incomplete, let an agent confirm an intent, or name a plan." Orchestration's reads: "Stop a person. Every gate has a way past it that records what's owed." Four stops in this capability have no way past today: removing a feature, a domain or an ICE; merging a capability that has its own ICE page; the 13 older parts the ready check calls not ready; and /shape-slice's model check, which does not go on until it reads valid. The third breaks this intent's own Must not. The way past each, and where what is owed is kept, belong to Give every gate a way past.
It matters because agents decide from the model: "Agents decide from the model, so a model that is out of date leads them wrong." Product model's own why: "The model keeps intent connected to the product after the work closes."
It sits in software delivery planning with the other capability of Product model, and the domain's first paragraph says so.

Features:
- Add a part found during work, with its page and its index entry (fn-add-found-part): the keeper writes the page of a domain, capability or feature found while other work goes on, then its index entry, thin when it is thin, all or nothing. Built in part.
- Change a part from words a person approved (fn-change-part): named lines of any page, a whole page, an intent page, a part's one-line, intents and parent, and the edit standard every play that owns a record follows (#962).
- Take a part out on a person's named approval (fn-take-part-out): repoint parts from an old intent, remove an intent page, merge a capability, remove a slice, with the name of the person who approved it. Built in part.
- Link the parts by the map's rules: what each serves, what it needs and what led us to find it (fn-725): each link by the ontology's rules, kept on both sides, and checked to point at a part that exists. Built in part.
- Say whether work can start on each part: ready, partly ready or not ready, with the gaps (fn-724): the ready check gives one answer for each part, the same for the same model.
- Check the model's structure and links on every change, as findings, never a stop (fn-check-model): the structure check reads the pages and the index for their shape and their links.
- Find and close the gaps inside the model (fn-close-model-gaps): loose parts, links on one side only, intents nothing serves and the same part written twice are found, and what the model can take is closed. Built in part.
- List what serves an intent, and what sits in a domain (fn-726): from any intent, a person lists the parts and slices that serve it; from a domain, its intents and capabilities. Built in part.
- Keep each part's approval state, so agents build only from approved parts (fn-part-approval): each part says whether a person approved it, it changed, or it is in progress. Not built (#964, each piece of the model carries its approval state).
- Move the model with the work (fn-model-moves-with-work): a design approval updates the model, and a change left for later is listed for Learn. Not built (#990, the product model moves with the work).
- Change the model's index only through the two index skills (fn-index-through-skills): every play adds, changes and takes out parts through the two index skills, not its own script. Built in part.
- Create and edit the model with one tool that knows its shape (fn-model-tool): one tool writes the model's pages and entries in the shape the ontology sets, with the plays and templates it lacks. Not built (#1030, a tool that knows how to create and edit the product model).
- Propose what to try next from the model, and record each experiment's result (fn-try-next): the model proposes an idea with its evidence, a person confirms or drops it, and an experiment records what was tried and its result. Not built.

What is not built yet:
- No skill removes a feature, a domain or an ICE, and a capability that has its own ICE page cannot be merged: 38 of the 41 capabilities.
- The shared step any play can point to for a part found during work (#979).
- The --edit option in each play that owns a record, other than /shape-slice (#962).
- A check that each need and "identified by" link points at a part that exists, and the field's name `needs` (#725).
- A command that lists what serves an intent, and a search by domain (#726).
- The approval state on each part (#964), the model moving with the work (#990), and the tool that knows the model's shape (#1030).
- Today the model does not pass its own checks: the structure check finds 21 errors and asks 249 pages for an ICE section the ontology moved to its own page, and the ready check calls no part ready.
- Nothing proposes an idea from the model or records an experiment, and no issue plans it.

### Benefit hypothesis
- Who it serves: the product owner, who confirms intents and approves each change and each take-out; the technical lead and the developer, a person or an AI agent who builds the code, who find parts during work and read the model to build from it; the plays, loops and agents that read and write the model, such as /shape-slice, /shape-plan, /update-plan and the Discovery loop; and the capabilities that hand their model work here.
- What we believe: when every change to the model goes through one keeper and its skills, from words a person approved, all or nothing, with its links kept on both sides and its checks giving findings on every change, people and agents can trust the map as the work moves, and it can show what to try next, if the work stands on these rules:
  - A rule stops work, never a write.
  - A missing domain, a missing link or a thin page never stops work, and a part found on its own is not a gap.
  - Only a person confirms an intent, and only a person approves a take-out.
  - A feature never needs another feature; the order of features is kept in the slices.
  - Every link is kept on both sides.
  - No model page or entry names a plan.
- How we will know: Product model's proofs hold for the model: "Any part can be added, changed or removed.", "From any intent, you can list what serves it.", "The model proposes an idea with its evidence, a person confirms it, and an experiment records the result.", and, after a change to the ontology, "the model still passes its checks".
  - Today a feature, a domain or an ICE cannot be removed, and no command lists what serves an intent.
  - Today the model does not pass its checks: 21 errors in the structure check, and 0 parts ready.
  - The fourth is not tested, because nothing proposes an idea yet.

### Boundary (In / Out / Never)
- In: adding a part found during work, its page and its index entry, thin when it is thin.
- In: changing a part from words a person approved, and the edit standard each play that owns a record follows.
- In: taking a part out on a person's named approval.
- In: the links between parts by the ontology's rules, on both sides.
- In: the model's checks: the ready check, the structure check, and the gap finder and closer.
- In: listing what serves an intent, and what sits in a domain.
- In: changing the index only through the two index skills.
- In, not built yet: each part's approval state, moving the model with the work, one tool that creates and edits the model, and proposing what to try next with each experiment's result.
- Out: the ontology: its kinds, what each holds, the rules for their links, and the step that runs the model's checks before and after a change to it. Define what a product is made of, in Product model, owns them.
- Out: the model's first pages, written when a product is first specified, and the rebuild eval. Specify the product, in Product → Spec, owns them.
- Out: drift between the model and what was built, and replacing or retiring an intent the work left behind. Keep the spec matched to what's built, in Product → Spec, owns them, with this capability's tools.
- Out: moving a project's model to a new version's shape. Upgrade a project, in Install and distribute, owns it.
- Out: changes worked out from what happens in use. Build features or update the product model, on its own or at least as recommendations, in Run → Product, owns them.
- Out: the way past each gate, and where what is owed is kept. Give every gate a way past, in Orchestration, owns them.
- Out: choosing a slice and the order of its features. Orchestrate agent work through planning, in Orchestration, owns it.
- Out: the review where a person answers each piece. Review what agents make (Argus), in Developer tooling, owns it; the approval state it writes is kept here.
- Never: let an agent confirm an intent. The reason: Product model's Must not, "let an agent confirm an intent", and the ontology: "only a person confirms or drops a business intent."
- Never: block work because the model is incomplete. The reason: Product model's Must not, "Block work because the model is incomplete", and the harness standard: "missing links are warnings to fix later, not stops".
- Never: name a plan on a model page or in the index. The reason: "The product model never names a plan", and Product model's Must not, "name a plan".
- Never: change the model by hand. The reason: "You may change any part of it — a page, the spine, an intent page, the profile — but only through a skill".
- Never: take a part out without the name of the person who approved it. The reason: "Never without the person's name."
- Never: lose what a page holds when it is grown. The reason: "a doc another play wrote is grown in place, keeping every section and agent-intent line it had".

### Guiding rules
- A rule stops work, never a write. The reason: "What a rule can stop is work, never a write".
- Every change is all or nothing, and every check runs before the first write. The reason: "Every check runs before the first write. One bad part refuses the whole request."
- Every link is kept on both sides. The reason: "Every `one_way` entry is a gap: a link is made only when both sides hold it."
- A part found on its own is not a gap. The reason, in the product owner's words on the stock-take's fourth question: "I'll go with your proposal of no.", and that proposal: "An empty "identified by" means found on its own and is not a gap".
- A feature does not need another feature; their order is kept in the slices. The reason, in the product owner's words: "Apart from being found on its own, no, a feature doesn't need another feature. All of that is managed in the slices."
- The checks and the edits of the model belong here. The reason, in the product owner's words: "Managing the model should hold any checks of the model as well. Managing the model should hold the edits as well."
- When no skill covers a change, the missing skill is built, never worked around. The reason: "When no skill covers a change, say so and stop: the missing skill is built, never worked around."
- Ideas and experiments are features of the model, nothing new. The reason, in the product owner's words: "Yeah, experimentations are only features. There is nothing new."
- Not decided: how experiments are run, as A/B tests or in another way. The product owner: "Whether they need to be built as A/B testing or whatnot is something which we can decide later".
- Not decided: the way past each of the four stops named above (#992, every gate has a key).
- Not decided: which capability of Product model writes the product profile and the product decisions once they are kinds of the ontology.
- Not decided: which plays get the shared step for a part found during work (#979).

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 1: "The capabilities, locked by the product owner on 2026-11-03"; line 123: "Manage the model: A living map, added to and pruned as work is done, and the source of what to try next. (unique)"; line 124: "a tool that knows how to create and edit the product model (#1030). Not built, and to be built later."; line 106, which leaves Link the product model and its features to BI-11
- .garura/project/issues/1021/context/capabilities.md, line 125, the product owner's answers of 2026-11-11: "Yeah, experimentations are only features. There is nothing new.", "Whether they need to be built as A/B testing or whatnot is something which we can decide later", "Yes, every ontology should run the model before and after.", "I don't understand question 4. I'll go with your proposal of no.", "Apart from being found on its own, no, a feature doesn't need another feature. All of that is managed in the slices.", "Managing the model should hold any checks of the model as well. Managing the model should hold the edits as well."
- .garura/project/issues/1021/context/capabilities.md, line 128: "model is implementation of the onology. hence managing ontology is a differnet capability and then managing model is a different capability. what we are doing here is managing the model, and we have some implementation in place while plays are missing, templates are missing etc."; line 129, read as: "the plays and templates it lacks are features of it", and the upgrade's feature "Move the product model to the new version's shape (fn-move-model, BI-7)"
- .garura/product/product-os/intents/bi-11.md, lines 5, 11-13 and 15: "The model keeps intent connected to the product after the work closes.", "Any part can be added, changed or removed.", "From any intent, you can list what serves it.", "The model proposes an idea with its evidence, a person confirms it, and an experiment records the result.", "Block work because the model is incomplete, let an agent confirm an intent, or name a plan."; line 10: "A person changes the ontology through one play and the model still passes its checks."
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- .garura/project/issues/1021/context/bi-11-write/old-pages/link-the-product-model.md, the copy of the old page of Link the product model, lines 1, 5 and 31-35: "Link the product model", "work can start before the model is complete, if the model links its parts by these rules", and its four features
- .garura/project/issues/1021/context/bi-11-inventory/inventory.md, the stock-take: section 2 (2.1 to 2.12), 3.2, 3.3, 4, 5, 6 and 7; Lean 1: "added to, changed and pruned"; Lean 3, the features; question 4's proposal, line 770: "An empty "identified by" means found on its own and is not a gap"
- core/components/agents/product-os-keeper.md, lines 176-177, 183-186: "You may change any part of it — a page, the spine, an intent page, the profile — but only through a skill", "When no skill covers a change, say so and stop: the missing skill is built, never worked around.", "a doc another play wrote is grown in place, keeping every section and agent-intent line it had"
- core/components/skills/link-model-part/SKILL.md, lines 56-57: "Every check runs before the first write. One bad part refuses the whole request."
- core/components/skills/remove-model-part/SKILL.md, line 74: "Never without the person's name."
- core/components/skills/find-model-gaps/SKILL.md, lines 43-44: "Every `one_way` entry is a gap: a link is made only when both sides hold it."
- core/components/skills/remove-model-part/scripts/remove_part.py, lines 78 and 227-228: `REMOVABLE = ("intent", "capability", "slice")`, "so it cannot be merged here"; a read of the index on 2026-11-11: 38 of 41 capabilities have their own ICE entry
- core/components/plays/shape-slice/SKILL.md, lines 607-608: "the run does not go on until it reads valid"
- standards/schemas/product-os/ontology.md, in Phoenix memory, line 25: "What a rule can stop is work, never a write", "only a person confirms or drops a business intent."
- docs/standards/harness-standard.md, lines 71-72: "missing links are warnings to fix later, not stops"
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md, line 137: "The product model never names a plan"
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/capability.md, lines 44 and 51: "Whoever first specifies a part writes its first page; after that, this capability keeps it.", "Manage the model owns them, and also merges capabilities and removes slices."
- .garura/product/product-os/software-delivery-planning/build-or-update-product/capability.md, line 29: "Merging or taking out another part goes to Manage the model."
- .garura/product/product-os/software-delivery-planning/run-plays-as-loops/capability.md, line 73: "Out: the link rules the step after each round applies to the product model. Manage the model, in Product model, owns them."
- .garura/product/product-os/software-delivery-planning/give-every-gate-a-way-past/fn-keep-what-is-owed/feature.md, line 54: "Manage the model, in Product model, owns how the model takes in the work (#990)."
- .garura/product/product-os/software-delivery-planning/orchestrate-agent-work/fn-work-out-waits-on/feature.md, line 54, and fn-remove-plan/feature.md, line 56: "The needs links on capabilities and features, and their name in the model's index. Product model owns them", "Removing parts of the product model. Product model owns it."
- .garura/product/product-os/software-delivery-planning/review-agent-work/capability.md, line 36: "The approval state kept on each piece of the model, and the rule that agents build only from approved pieces, are Product model's (#964)."
- The ready check, the structure check and the gap finder, run from the repository root on 2026-11-11, each writing its report outside the repository: 0 ready, 249 partly ready, 13 not ready; 21 errors and 263 warnings; 1 loose part, 4 intents nothing serves, 21 links on one side only
- GitHub #977 (open): "Agents decide from the model, so a model that is out of date leads them wrong."
- GitHub #962, #964, #979, #990, #1024, #1030, #725, #726 and #992 (open): the planned work named under What is not built yet and in the features.
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf in any memory tier covers how a team keeps a product model; the ten domain shelves in Phoenix memory cover product fields, such as payments and e-commerce.
- .garura/product/product-os/software-delivery-planning/domain.md, line 4: the domain's first paragraph, which does not name Product model yet
- .garura/product/product-os/software-delivery-planning/domain.md: "It also defines what a product is made of, and keeps each product's model as a living map: added to, changed and pruned as work is done, and the source of what to try next."
