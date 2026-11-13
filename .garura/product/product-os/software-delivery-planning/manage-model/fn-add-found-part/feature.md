# Feature: Add a part found during work, with its page and its index entry

## What it does
When a person or a play finds a domain, capability or feature that the model does not hold while other work goes on, the keeper writes its page and then its index entry through the model's skills, thin when it is thin, so the model keeps up with the work without a full discovery run.
- The page skill writes the page. It writes a new feature under a capability that exists (its new-feature mode), the minimum ICE for a part that has none (its thin mode), or a page a person approved, word for word: a domain, capability, feature or ICE page (its approved mode).
- The index skill, link-model-part, then writes the part's entry: its parent, its intents, its one-line, its page, its issue and the status proposed, marked to be deepened. A thin capability or feature gets the thin mark in two places that agree. An ICE gets its own entry, and a thin ICE carries the mark at the top of its own page and on its own entry.
- The keeper runs the page skill once for each part, "in parallel when there are several", then one index run for all of them.
- Each run is all or nothing, and each skill's report lists every file it changed.
- Who uses it today: Add a feature found during work (fn-add-found-feature), in Turn intents into agent work, through /update-plan; and the reorganisation of the business intents.
- What it is to become, in its design: "A shared step, not a per-play feature." Any play that can find a part points to one common step that asks the keeper, and the page lands in the change already open. "`/start-change` never gets it".
- Examples, in different kinds of project:
  - In a clinic's booking app, the developer builds Booking and finds that patients need a reminder the day before. The keeper writes a thin Send a reminder feature under Booking, its thin ICE page and their entries, in the open change.
  - In a bank's payments service, a planning session names a new Refund to card feature. After the product owner's "approved", its thin page and its entry land with the session.
  - In a game studio's build, the technical lead approves the words of a new Save sync capability page and its ICE page. Both are written word for word, then the capability's entry and its ICE's entry.
- How it meets the capability: this is the map "added to ... as work is done": a part found while work goes on enters the model in the same change.

Status: built in part. Built: the page skill's new-feature, thin and approved modes, and link-model-part's new entries and thin marks, each with its tests (16 passed for the approved-page script and 48 for link-model-part, in the stock-take's run on 2026-11-11). Not built, or open:
- The shared step any play can point to, by which a feature found during work gets a thin page in the product model, inside the open change, without the full discovery. In its design: "The shared play step comes later."
- The thin mode still writes the older ICE lines, Goal, Limit, Fails if, Context and Checked by, and in an ICE page it puts "the Checked by line under `## Expectation`". An ICE page now holds the Read, Never read, Persona and Scope lines under Context, and a Scenario and a Done means under Expectation. Create and edit the model with one tool that knows its shape (fn-model-tool) is to close this.
- A feature found in a planning session cannot land once the model has ICE entries.
- link-model-part writes only the index side of a part's link to its intents; the intent page's Touches list is not written. In the words of Keep the spec matched to what's built: "A part linked or moved through them is missing from its intent's page."

## Inputs / Outputs
- In: the words that name the part, its kind, its parent and the intents it serves, from a person or from the play that found it.
- In: for an approved page, the file that holds its approved text, the person who approved it and where that is recorded.
- In: the model's index, and the pages of the part's parent and its intents.
- Out: the part's page in its folder, and its ICE page beside it.
- Out: its index entry, with status proposed and marked to be deepened, both thin marks when it is thin, and its ICE's entry.
- Out: each skill's report, with every file it changed.

## Rules & behavior
- The page comes first, then the index entry. The reason: "The page skill writes a part's page. This skill puts the part into the spine, so the model knows the page is there".
- A part found during work runs no discovery play. The reason: the keeper's route ends "No discovery play run", and its design: "That is too much for one feature found in the middle of other work, and it breaks the rule of one change for that work."
- The page lands in the change already open. The reason, in its design: "Have the page written on the branch of the change that is already open, so it lands with that change. No second change, no second review."
- The thin mark is two marks that agree. The reason: "`metadata.thin: true` on the spine entry and exactly one Thin line on the page, just before its ICE."
- A part that has an ICE is never marked thin itself. The reason: "A part that has an ICE is never marked thin itself; its mark belongs on its ICE".
- An approved page is written word for word. The reason: "the page is copied as it is: nothing is composed."
- All or nothing, and only inside the model. The reason: "Every check runs before the first write. One bad part refuses the whole request.", and "Only inside the product model."
- Not decided: which plays get the shared step. Its design: "which other plays do is part of this design."

## Acceptance criteria
- Given a feature found during work under a capability that exists, when the keeper adds it, then its page, its thin ICE page and their index entries are written, the two thin marks agree, and the reports list every file changed.
- Given a request whose parent is not in the index, when the index skill runs, then nothing is written and the error names the part.
- Given a page a person approved, when it is added, then the page on disk is the approved text, word for word.
- Given a part added with an intent, when its entry is written, then the intent page's Touches list names the part. This is not built.
- Given a thin ICE written by the page skill, when it is read, then it holds the Read, Never read, Persona, Scope, Scenario and Done means lines. This is not built.
- Given a play with the shared step and an open change, when it finds a feature, then the page and its entry land in that change with no discovery run. This is not built.

## Out of scope
- Placing a feature found in a planning session in its slice and under its epic. Add a feature found during work (fn-add-found-feature), in Turn intents into agent work, does it.
- Deepening a thin part. Specify the product, in Product → Spec, owns it, through /discover-capabilities.
- Changing a part that exists. Change a part from words a person approved (fn-change-part) does it.
- The rules each link follows. Link the parts by the map's rules: what each serves, what it needs and what led us to find it (fn-725) does it.

## Sources
- The capability list: "we have some implementation in place while plays are missing, templates are missing etc."
- core/components/skills/enrich-grounding/SKILL.md, lines 44-60 and 80-81: the new-feature, thin and approved modes; "In an `ice.md`, Goal, Limit and Fails if go under `## Intent`, the Context line under `## Context`, and the Checked by line under `## Expectation`.", "the page is copied as it is: nothing is composed."
- core/components/skills/link-model-part/SKILL.md, lines 11-12, 54-57, 60-61: "The page skill writes a part's page. This skill puts the part into the spine, so the model knows the page is there", "Only inside the product model.", "Every check runs before the first write. One bad part refuses the whole request.", "`metadata.thin: true` on the spine entry and exactly one Thin line on the page, just before its ICE."
- core/components/skills/link-model-part/scripts/link_part.py, lines 30-38 and 68-70: the new entry, status proposed, "deepen: true"; "A part that has an ICE is never marked thin itself; its mark belongs on its ICE"
- core/components/agents/product-os-keeper.md, line 102: "one run per part, in parallel when there are several", "No discovery play run"
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/fn-add-found-feature/feature.md, lines 12-13: "Known break: [a found feature cannot land once the model has ICE entries]. A found feature cannot land, because the thin mark goes to a page with no ICE section."
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/capability.md, line 28: "A part linked or moved through them is missing from its intent's page."
- The stock-take (2026-11-11), section 2.2: the tests, 16 passed for `write_approved.py` and 48 for link-model-part
