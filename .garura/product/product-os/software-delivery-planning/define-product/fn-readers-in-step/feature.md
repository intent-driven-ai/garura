# Feature: Keep every part that reads the map in step with it: the page templates, the index's schema, the structure check and the glossary

## What it does
When the map changes, the parts that describe or check the model's shape change with it, the page templates, the index's schema, the structure check and the glossary, so that a page written from a template, an index read by its schema and a model checked by the structure check all follow the map's current version.
- The page templates say what each page of the model holds. The capability and feature templates in Phoenix memory still say "## Agent intent (ICE) — the last section, at every stage", while version 6 and later of the map say "The ICE is on its own page, never a section of the capability page." There is no template for an ICE page.
- The index's schema, at version 2, says what the model's index holds. Its field for needs is still `depends_on`, "Field renamed to `needs` under #725". It holds one "identified by" as a string, while the map says a capability's "identified by" "may name more than one". It says that until #765 (each ICE section moves to its own ICE node) moves a model, "the spine has no `ices` list", while Garura's own index has one, with 249 entries.
- The structure check, one script copied into each play that writes the model, checks the shape of the pages and the index. It already checks each ICE entry and its page. It still warns, for each part that serves an intent, "no '## Agent intent (ICE)' yet", also when the ICE is on its own page. Run on the whole model on 2026-11-11, it gave 21 errors and 263 warnings; 249 of the warnings are that one.
- The glossary still calls the model "a 3-level tree Domain → Capability → Feature, plus personas and journeys attached to nodes", says a capability "carries ICE", and says an ICE is "attached to a capability or feature node" and "Workable only when built from a confirmed business intent". The map says the ICE "has no link to a business intent; it finds its business intents through its part." The glossary says the map is "Built with `author-product-ontology`", while it changes through /edit-ontology.
- The plays that write the model follow the map in part. The page skill writes an ICE page when the index has an ICE list. The discovery plays still write the ICE inside the page (#762, /discover-capabilities and its skills write ICE nodes, under #761, plays write ICE nodes).
- Garura's own model is in a half-moved shape: 13 old parts keep their ICE inside their page, and the ready check calls each of them not ready (#764, Garura's own model moves to ICE nodes, with #765, each ICE section moves to its own ICE node; #1033, plays read the whole model by one rule once its index has ICE entries, so older parts break).
- The map's play changes only the kinds its need touches, so nothing moves these parts when the map changes.
- Examples, in different kinds of project:
  - In a clinic's booking app, the map moves the ICE to its own page. The capability and feature templates change in the same release, a new ICE template is added, and the next page written has no ICE section inside it.
  - In a bank's payments service, the map lets a capability be identified by more than one other capability. The index's schema holds a list for it, and the structure check accepts two ids there.
  - In a game studio's build, the map renames a kind. The glossary's row for it changes with it, so a newcomer reads the same word in the glossary as on the pages.
- How it meets the capability: people and agents share "one agreed map" only when the parts that write and check the model say what the map says.

Status: built in part. Built: the structure check reads each ICE entry and its page; the page skill writes an ICE page when the index has an ICE list. Not built, or open:
- The capability and feature templates put the ICE inside the page, and no ICE page template exists.
- The index's schema keeps `depends_on`, one "identified by", and its note that the index has no ICE list.
- The structure check warns for a missing ICE section on 249 parts whose ICE is on its own page.
- The glossary describes the ICE and the model as the map did before version 6.
- The discovery plays write the ICE inside the page (#761, plays write ICE nodes; #762, /discover-capabilities and its skills write ICE nodes; #763, the judges check plain English and the three parts).
- 13 old parts of Garura's own model keep their ICE inside their page (#764, Garura's own model moves to ICE nodes; #765, each ICE section moves to its own ICE node).
- The map's own text, its templates and the index's schema do not yet agree on who writes each kind and where a loose part waits (#694, the model's rules say what ADR 043 changed); that issue still names plays that are gone.

## Inputs / Outputs
- In: the map at its current version, and the log line of its last change.
- In: the page templates, the index's schema, the structure check and the glossary, as they are.
- Out: each of the four, changed to say what the map says, in the same release as the map.
- Out: a list of what still disagrees with the map, each with its part and its line.

## Rules & behavior
- A template, the schema, the check and the glossary say what the map says. The reason: "A person and an agent reading it use the same words for the same things."
- The ICE has its own page, and no template puts it inside a part's page. The reason: "The ICE is on its own page, never a section of the capability page."
- A page made before a change still passes; a gap is a warning. The reason: "missing links are warnings to fix later, not stops".
- The map and the parts that read it go together. The reason, in the product owner's words: "It all has to go hand in hand, but it is extendable, which is fine."
- Not decided: whether these parts change in the same run as the change to the map, or in a later change that follows it, since the map's play changes "only the kinds that need touches".
- Not decided: whether the 13 copies of the structure check become one shared check, or each play that writes the model keeps its own copy.

## Acceptance criteria
- Given the map at version 15, when an agent writes a capability page from its template, then the page has no ICE section, and an ICE page template is there for its ICE. This is not built.
- Given the index's schema, when a reader looks for needs and "identified by", then the field is named as the map names it, and "identified by" may hold more than one capability. This is not built.
- Given a part whose ICE is on its own page, when the structure check runs, then it gives no warning for a missing ICE section. This is not built.
- Given the glossary, when a reader looks up the ICE, then it says the ICE is its own part with its own page and no link to a business intent. This is not built.
- Given an index with an ICE list, when the structure check runs, then it checks each ICE entry, its part and its page.
- Given Garura's own model, when the ready check runs, then no part is not ready only because its ICE is inside its page. This is not built.

## Out of scope
- What the map says. Write down what a product is made of: the kinds, what each holds, how they link, the rules and a real example of each (fn-597) does it.
- Running the model's checks before and after a change to the map. Run the model's checks before and after every change to the map, and show what the change breaks, as findings, never a stop (fn-check-model-on-change) is to do it.
- The model's checks themselves, the ready check and the gap finder, and renaming `depends_on` to `needs` with a check that each link points at a part. Manage the model, in Product model, owns them (#725, needs and identified by link capabilities).
- The discovery plays that write the model's first pages. Specify the product, in Product → Spec, owns them; this feature holds what they must write by the map (#761, plays write ICE nodes).
- Moving a team's model to a new version's shape. Upgrade a project, in Install and distribute, owns it, through Move the product model to the new version's shape (fn-move-model).
- Bringing a changed template to Phoenix memory. Memory, in Standards, structure, settings and memory, owns it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 122: "People and agents share one agreed map of what a product is made of, changed only on purpose."; line 125, the product owner: "It all has to go hand in hand, but it is extendable, which is fine."
- standards/schemas/product-os/grounding/capability.md, in Phoenix memory, line 56, and standards/schemas/product-os/grounding/feature.md, in Phoenix memory, line 47: "## Agent intent (ICE) — the last section, at every stage"; the memory tool's `find` on 2026-11-11 found no ICE template among the page templates.
- standards/schemas/product-os/spine.yaml, in Phoenix memory, line 26: "version: 2"; lines 91-94: "depends_on: [string]", "Field renamed to `needs` under #725.", "identified_by: string"; lines 129-131: "Until #765 moves a model, its ICE", "stays inline in the part's page and the spine has no `ices` list."
- standards/schemas/product-os/ontology.md, in Phoenix memory, line 9: "A person and an agent reading it use the same words for the same things."; line 345: "may name more than one"; line 362: "The ICE is on its own page, never a section of the capability page."; line 482: "It has no link to a business intent; it finds its business intents through its part."
- core/components/plays/shape-slice/scripts/lint_grounding.py, one of 13 copies, lines 20-24, the ICE NODES check; lines 251-252: "no '## {ICE_SECTION}' yet — its spine entry names a business"; run on the whole model on 2026-11-11 with its index: 21 errors, 263 warnings, with counts of 41 capabilities, 221 features and 249 ICE.
- core/grounding/glossary.md, lines 61, 62, 65 and 68: "a 3-level tree Domain → Capability → Feature, plus personas and journeys attached to nodes", "it carries ICE", "attached to a capability or feature node", "Workable only when built from a confirmed business intent", "Built with `author-product-ontology`."
- core/components/plays/edit-ontology/reference/ice.md, line 14: "Every run works on one need, and changes only the kinds that need touches."
- docs/standards/harness-standard.md, lines 70-72: "missing links are warnings to fix later, not stops"
- The stock-take of Product model, .garura/project/issues/1021/context/bi-11-inventory/inventory.md, sections 1.4 and 2.6: the page skill writes `ice.md` when the index has an `ices` list; the 13 old parts the ready check calls not ready.
- GitHub #761 (open): "the plays that write the product model write each ICE as its own node, in plain English, with all three parts"; #762 (open): "/discover-capabilities, enrich-capability-ice and the page templates write an ICE node"; #763 (open): "The judges check plain English and the three parts"; #764 (open): "Move Garura's own model to ICE nodes"; #765 (open): "A before and after check shows that no goal, limit, failure or check is lost."; #1033 (open): "Read each part by its own shape, not the whole model by one rule."; #694 (open): "the ontology text, the spine and every template agree on who writes each kind and where a loose node waits"; #725 (open): "renaming it to `needs` across the files that use it (53 today) is part of this story"
