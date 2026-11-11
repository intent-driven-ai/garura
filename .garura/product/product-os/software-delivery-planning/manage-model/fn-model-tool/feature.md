# Feature: Create and edit the model with one tool that knows its shape

## What it does
One tool is to know the model's shape as the ontology sets it, and to create and edit the model's pages, ICE pages and index entries in that shape, with the templates and the play steps the model lacks today, so the pages stop drifting from the ontology when a language model composes them.
- The product owner asked for it on 2026-11-05: "we need a tool that knows how to create and edit the product model. we will build it later." He set it as a feature of this capability: "Feature to add when this capability is reviewed: a tool that knows how to create and edit the product model (#1030). Not built, and to be built later."
- Why, in #1030: "Today a language model composes the model's pages, and they drift from the ontology." "The page template and the page skill still describe the older shape, and nothing stopped it."
- What the product owner names as missing: "what we are doing here is managing the model, and we have some implementation in place while plays are missing, templates are missing etc." The missing pieces the stock-take found, which belong here or in the first three features of this capability:
  - no template for an ICE page, and page templates that still put the ICE inside the page, as "## Agent intent (ICE) — the last section, at every stage";
  - the page skill's thin mode, which still writes the older ICE lines;
  - the shared step for a part found during work (#979), in Add a part found during work, with its page and its index entry (fn-add-found-part);
  - the --edit option in each play that owns a record (#962), in Change a part from words a person approved (fn-change-part);
  - no skill that removes a feature, a domain or an ICE, in Take a part out on a person's named approval (fn-take-part-out).
- Examples, in different kinds of project:
  - In a clinic's booking app, the developer asks for a new feature under Booking. The tool writes its page and its ICE page in the shape the ontology sets, and its entries, with no section the ontology moved.
  - In a shop's checkout service, the ontology moves a property of the capability kind. The tool writes every new capability page with the property where the ontology now puts it.
  - In a game studio's build, the technical lead edits the Save sync capability's ICE. The tool changes the ICE page's three parts and nothing else.
- How it meets the capability: a living map that agents and people both read stays one map only when every page is written in the ontology's shape.

Status: not built (#1030, a tool that knows how to create and edit the product model). What exists:
- The page skill, the two index skills and the intent-page skill each write a part of the model, through the keeper.
- The page templates for a domain, a capability, an epic, a feature and a functionality, in Phoenix memory; none for an ICE page.

## Inputs / Outputs
- In: the ontology's kinds, what each holds and their rules, at the model's version.
- In: what to create or edit, from a person's approved words or from a play.
- Out: pages, ICE pages and index entries written in the shape the ontology sets. Not built.

## Rules & behavior
- The tool writes the shape the ontology sets. The reason: #1030, "The ontology says an ICE has its own page and its own entry in the model's index, with three parts: Intent, Context and Expectation."
- The model is changed only through a skill or a tool, never by hand. The reason: "You may change any part of it — a page, the spine, an intent page, the profile — but only through a skill".
- Not decided: what the tool covers, how it is built, what it replaces, and when it is built (#1030).
- Not decided: which of the missing templates and play steps the tool holds, and which stay with the first three features of this capability.

## Acceptance criteria
- Given a new feature asked for under a capability that exists, when the tool creates it, then its page and its ICE page are in the shape the ontology sets, with no section the ontology moved. This is not built.
- Given a change to a kind in the ontology, when the tool next writes a part of that kind, then the part follows the new shape. This is not built.
- Given an edit of an ICE page, when the tool makes it, then only the named part of the ICE changes. This is not built.

## Out of scope
- The ontology itself, and the model's recorded shape version. Define what a product is made of, in Product model, owns them.
- Moving a project's model to a new version's shape. Move the product model to the new version's shape, on the person's yes (fn-move-model), in Upgrade a project, does it.
- The words a person approves for a page. Change a part from words a person approved (fn-change-part) does it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 124: "Feature to add when this capability is reviewed: a tool that knows how to create and edit the product model (#1030). Not built, and to be built later."; line 128: "what we are doing here is managing the model, and we have some implementation in place while plays are missing, templates are missing etc."
- GitHub #1030 (open): "we need a tool that knows how to create and edit the product model. we will build it later.", "Today a language model composes the model's pages, and they drift from the ontology.", "The ontology says an ICE has its own page and its own entry in the model's index, with three parts: Intent, Context and Expectation.", "The page template and the page skill still describe the older shape, and nothing stopped it.", "What the tool covers, how it is built, what it replaces, and when it is built."
- standards/schemas/product-os/grounding/capability.md, in Phoenix memory, line 56: "## Agent intent (ICE) — the last section, at every stage"; the folder holds templates for a domain, a capability, an epic, a feature and a functionality, and none for an ICE page (a search through the memory tool on 2026-11-11)
- core/components/skills/enrich-grounding/SKILL.md, lines 50-60: the thin mode's Goal, Limit, Fails if, Context and Checked by lines
- core/components/agents/product-os-keeper.md, lines 176-177: "You may change any part of it — a page, the spine, an intent page, the profile — but only through a skill"
- The stock-take, .garura/project/issues/1021/context/bi-11-inventory/inventory.md, sections 1.4, 2.11 and 4, and Lean 3, feature 12
