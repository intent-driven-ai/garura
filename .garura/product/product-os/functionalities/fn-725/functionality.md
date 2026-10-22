# Functionality: "Needs" and "identified by" link capabilities and functionalities

## What it does
A capability or a functionality can need another capability or functionality. It can also be identified by one. Any mix is allowed. These links never go on work (a feature, story, spike, chore or bug). The spine is the file that lists each node and its links. Its field is still `depends_on`. This story changes that name to `needs` in all the files that use it (53 today).
- "Needs" says that another node must be done first. It is the only link that sets an order of work, and the ready check (the script that tells if work can start) reads it.
- "Identified by" says which node led us to find this one. It records where a node came from. It never sets an order.
- Any play that writes a node can write these two links on it, in any order. Then the spine linter checks that each link names a capability or functionality that exists.
- The linter rejects a link that names work, a domain, a business intent or nothing.
- The rename makes the field use the word of the ontology (the written model rules). Today the ontology and the pages say "needs", but the spine field is `depends_on`. A reader must translate between the two.

## Inputs / Outputs
- In: the spine entry of each capability and functionality. This is its `depends_on` list (which becomes `needs`) and its `identified_by` value. That value is one id, or empty when the node was found on its own.
- In: the set of capability and functionality ids in the same spine. Each link must point at one of these ids.
- In: the domain ids and business intent ids in the spine. With these, the linter can tell a link to one of them from a link to a missing node.
- In: nothing more. The linter never reads the tracker, so it knows that a link names work only from the shape of the id (see Rules).
- Out: the result of the spine linter. It gives one error for each bad link, and names the node, the field and the value.
- Out: the error text is "points at work" for a bare issue number. It is "points at a business intent" or "points at a domain" for those ids. It is "not in the spine" for any other id that the spine does not hold. Any mix of capability and functionality gives no error.
- Out: after the rename, each file that reads or writes the field uses `needs`. These files are the spine schema and the scripts that read it, such as the ready check. They also include the plays, the skills and the product models in this repo. Thus no reader still looks for `depends_on` on a capability or functionality.

## Rules & behavior
- A capability can need a capability or a functionality. A functionality can need a capability or another functionality. Every mix is allowed, because work across capabilities often needs a part of another capability.
- A node never needs itself, and "identified by" never names the node itself. Either one is an error.
- "Identified by" holds one id at most. Empty means that the node was found on its own. This is normal and gives no warning.
- Work never has these links. A Feature, Story, Spike, Chore or Bug is the order to build a node, so each link goes on the node that the work tracks. A link that names the issue number of work is an error.
- How the linter tells a node from work: today, node ids in Garura's spine start with a kind prefix. A capability is `cap-<n>` and a functionality is `fn-<n>` (for example `cap-723`, `fn-724`). Business intents are `bi-<n>`.
- A link value that is a bare issue number, such as `725` or `#725`, gives "points at work", with no tracker lookup. That error replaces "not in the spine" for the link, so each bad link gets exactly one error.
- A value with a prefix that the spine does not hold, such as `fn-999`, gives "not in the spine".
- Our default — the spine schema calls ids opaque strings and sets no prefix rule. The spine linter (lint_grounding.py) does not check `depends_on` or `identified_by` yet. It checks only that each named parent `domain` and `capability` exists.
- Nothing ever needs a business intent. Business intents connect only by their own "identified by", written on the intent page. They never wait for one another.
- A need that names a node in a different plan makes this plan need that plan. The plan plays find the needs of a plan from the needs of its nodes. Nobody sets them by hand.
- Two nodes that need each other, directly or through other nodes, make a loop. The linter gives an error for the loop and names each node in it. A self-link is the same: it is the shortest loop.
- A loop is an error, not a warning, unlike a missing link. A missing link is a gap that the model fills as it grows. A loop is a link that exists but can never come true. Nothing in it can ever be ready, and no later write fixes it.
- The loop error still never stops or undoes the write that made the loop. To fix it, drop one need, or merge the plans of the nodes into one plan. Our default — the sources say only that two plans that need each other are one plan.
- The rename keeps every value. Each `depends_on` list on a capability or functionality moves to `needs` with no change.
- Slices and epics also use `depends_on` today. The same change renames them too, so one field name has one meaning.
- The linter tells the two phases apart by the `version` in the spine schema file that it checks against (`schema.version` in spine.yaml, 2 today). The rename raises it to 3.
- While the schema is at version 2, the linter reads the old name `depends_on` on a capability or functionality as `needs`. It gives a warning that names the old field, so an old model still loads.
- At version 3 or higher, the old name on a capability or functionality is an error that names the old field. Thus one field name has one meaning. Our default — the sources do not say how old models are carried across, nor that the schema version marks the rename.
- How pages are saved does not change. The rename changes a field name in the spine, not the files or the folders.

## Acceptance criteria
- Given a spine where a capability needs a functionality of a different capability, when the spine linter runs, then it passes with no error for that link.
- Given a spine where the need of a functionality names a Story issue number instead of a node id, when the linter runs, then it fails with an error that names that link.
- Given a spine where `identified_by` names an id that is not in the spine, when the linter runs, then it fails with an error that names the missing id.
- Given a node whose `identified_by` is empty, when the linter runs, then there is no error and no warning for it.
- Given a node that needs itself, or two nodes that need each other, when the linter runs, then it fails with an error that names the self-link or each node in the loop.
- Given the spine schema at version 2 and a capability whose spine entry has `depends_on`, when the linter runs, then it warns, names the old field, and reads the values as needs.
- Given the same entry with the spine schema at version 3, when the linter runs, then it fails with an error that names the old field.
- Given the rename is done, when the repo is searched for `depends_on` on capability and functionality entries, then none is left, and the ready check reads `needs`.
- Given Garura's own model (#717, #722, #734) after the rename, when the linter and the ready check run, then cap-742 and cap-747 still need cap-739, and fn-727 still needs fn-724, with no value lost.

## Out of scope
- The ready answer itself. A capability or functionality is ready without a domain (fn-724) owns how needs decide readiness.
- Finding which plans a plan needs, and the merge order between plan branches. Build a plan (cap-718), Manage a plan (cap-720) and Start and land work against a plan (cap-721) own those.
- The links between business intents. They are on the intent pages, as the ontology defines (fn-597).
- The links from domains. Domains link to business intents and capabilities (fn-726) owns those.

## Sources
- core/components/memory/standards/schemas/product-os/ontology.md (v5), kind Capability: "\"Needs\" and \"identified by\" link only capabilities and functionalities — never work."
- Ontology kind Work: "Work never needs anything and is never identified by anything; those links sit on its capability or functionality."
- core/components/memory/standards/schemas/product-os/spine.yaml: "depends_on: [string] # \"needs\" (ontology v5) … Field renamed to `needs` under #725."
- .garura/project/issues/621/specs/change-list.md: "The spine field is `depends_on` in 53 files today (epics and slices use it too)."
- .garura/project/issues/621/specs/plan-design.md: "No loops: if A depends on B and B depends on A, they are one plan".
- GitHub #725: "\"Needs\" and \"identified by\" link capabilities and functionalities".
- Shelf: none. No domain shelf holds the product model of a framework itself (routing for #723).

## Agent intent (ICE)
- Goal: Anyone can see what a node needs and what led us to find it.
- Goal: The spine field is called `needs`, matching the ontology, with no value lost in the rename.
- Limit: Links sit only on capabilities and functionalities.
- Limit: The rename changes a field name only, never how pages are saved.
- Fails if: a need or identified-by link points at work, or at a node that does not exist.
- Fails if: a `depends_on` value is dropped or changed by the rename.
- Context: serves the plays that write and read links (build-plan, /discover-capabilities, the ready check, the Alignment loop) and the plan owner reading a plan; touches the spine schema, lint_grounding.py's spine check, check_ice_workable.py and every file that names `depends_on`; in are the two links and the rename, out are plan needs and business intent links.
- Checked by: the spine linter rejects a link to a story and accepts capability → functionality.
- Checked by: after the rename no capability or functionality entry in the repo carries `depends_on`, and Garura's own model keeps every need it had.
- Quality need: zero links that point at nothing or at work across Garura's own model, checked by the spine linter.
