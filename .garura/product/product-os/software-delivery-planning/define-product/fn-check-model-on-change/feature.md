# Feature: Run the model's checks before and after every change to the map, and show what the change breaks, as findings, never a stop

## What it does
Every change to the map runs the model's checks before it and after it, and shows the product owner what the change breaks in the model, as findings recorded as owed and never as a stop, so that a change to the map never leaves the model broken without anyone knowing.
- The product owner's answer to the stock-take's question 3: "Yes, every ontology should run the model before and after." The record reads it: "every ontology change runs the model's checks before and after".
- Question 3 asked whether the map's play should "run the model's checks before and after the change and show each new finding at its last checkpoint, as findings to fix later and never a stop".
- This intent's first proof: "A person changes the ontology through one play and the model still passes its checks." Today no step tests it. The map's play checks only the map and its change, and runs none of the model's checks.
- The model's checks are the structure check, the ready check and the gap finder. Manage the model holds them: "Managing the model should hold any checks of the model as well." This feature runs them around a change to the map, and compares the two runs.
- The model fails its structure check before any change today: 21 errors and 263 warnings on 2026-11-11. So a finding that is new after a change is told apart from one that was there before.
- Examples, in different kinds of project:
  - In a shop's checkout service, the product owner renames a kind. Before the change lands, the findings list every page, key and heading of the model that still uses the old name, and each is recorded as owed.
  - In a bank's payments service, the product owner adds a Regulation kind. The findings show that 12 capabilities have no link to it yet; the change lands, and the 12 links are owed.
  - In a news site's publishing tool, the product owner changes the lines of the ICE's Context part. The findings name the 30 ICE pages that still read the old way, and the work of the day goes on.
- How it meets the capability: a map "changed only on purpose" is changed knowing what it does to the model.

Status: not built. No issue asks for it.

## Inputs / Outputs
- In: the model, before the change to the map and after it.
- In: the reports of the model's checks, run before and after.
- Out: the findings that are new after the change, each with its part and its line, shown to the product owner.
- Out: a record of each finding as owed, kept where a later play finds it.

## Rules & behavior
- The model's checks run before and after every change to the map. The reason, in the product owner's words: "Yes, every ontology should run the model before and after."
- A finding never stops the change or the work. The reason: this intent must not "Block work because the model is incomplete", and "missing links are warnings to fix later, not stops".
- What the change leaves owed is recorded. The reason: Orchestration's Must not, "Stop a person. Every gate has a way past it that records what's owed."
- The checks are Manage the model's; this feature only runs them around a change. The reason, in the product owner's words: "Managing the model should hold any checks of the model as well."
- Not decided: at which point of the map's play the findings are shown, and where what is owed is kept.
- Not decided: whether the structure check is brought in step with the map, and the model's 21 errors are fixed, before this feature is built.
- Not decided: which model the checks run on in a harness repository: its own model, a model kept for the test, or both.

## Acceptance criteria
- Given a change to the map, when the map's play reaches its end, then the model's checks have run before and after the change. This is not built.
- Given a change that leaves pages in the old shape, when the checks run after it, then each such page is shown as a new finding, apart from the findings that were there before. This is not built.
- Given new findings, when the product owner sees them, then the change still lands, and each finding is recorded as owed. This is not built.

## Out of scope
- The model's checks themselves, and fixing the model's parts. Manage the model, in Product model, owns them.
- Keeping the structure check in step with the map. Keep every part that reads the map in step with it: the page templates, the index's schema, the structure check and the glossary (fn-readers-in-step) does it.
- Moving a team's model to a new version's shape. Upgrade a project, in Install and distribute, owns it, through Move the product model to the new version's shape (fn-move-model).
- Where what is owed is kept for every gate. Give every gate a way past, in Orchestration, owns it.

## Sources
- The product owner's answers of 2026-11-11: "Yes, every ontology should run the model before and after.", "Managing the model should hold any checks of the model as well."; as read: "3, every ontology change runs the model's checks before and after"
- The stock-take of Product model (2026-11-11), question 3: "run the model's checks before and after the change and show each new finding at its last checkpoint, as findings to fix later and never a stop"; its examples; sections 1.6 and 2.7.
- .garura/product/product-os/intents/bi-11.md, lines 10 and 15: "A person changes the ontology through one play and the model still passes its checks.", "Block work because the model is incomplete"
- .garura/product/product-os/intents/bi-9.md, line 13: "Stop a person. Every gate has a way past it that records what's owed."
- docs/standards/harness-standard.md, lines 70-72: "missing links are warnings to fix later, not stops"
- core/components/plays/edit-ontology/SKILL.md, lines 214-231: the change check reads only the map's scope, version and names; and the play's steps run no check of the model.
- core/components/plays/shape-slice/scripts/lint_grounding.py, run on the whole model with its index on 2026-11-11: 21 errors, 263 warnings.
