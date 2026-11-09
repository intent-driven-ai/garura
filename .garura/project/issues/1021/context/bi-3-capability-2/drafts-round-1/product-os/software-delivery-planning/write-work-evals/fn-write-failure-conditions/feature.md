# Feature: Write what must never happen, and the way back from each

## What it does
For each feature whose story is under the chosen item, this feature writes the feature's entry in the slice's hidden file: what must never happen when a person uses it, and the way back from each, so the eval checks that none of it happens and nothing of it reaches the builder.
- The hidden file is a file in the slice's evals folder, beside the eval. Its first lines name the slice and the surface a person tests it on. It has one entry for each feature of the slice.
- An entry holds the feature, its capability, the two ICE it was written from and which of them is thin, and each "Fails if" line of the feature's ICE and of its capability's ICE, each with a short id such as F1. An ICE is the agent's intent for one capability or feature, and its "Fails if" lines say what would make the work a failure.
- Each "Fails if" line gets exactly one recovery, in three parts. When: the line said again as a symptom the eval sees from the outside. Way back: the state that must be true again, as guidance, never code. Who fixes: "the builder can fix this alone" or "a person must decide".
- For example, in a shop, "Fails if: a card is charged twice" gives: when, one order has two charges; way back, refund the second charge; who fixes, a person must decide, because money goes out.
- When one of the two ICE is thin, proposed from a person's words and not yet deepened, the entry says so. A line too vague to say what the eval sees still gets one recovery, marked "a person must decide", and the person sees it.
- Before the file is kept, the person sees the "Fails if" lines, how many the builder can fix alone and how many a person must decide, and the lines too vague to judge.
- How it meets the capability: the eval has a scenario for each failure condition that shows it does not happen, and when one happens, the running eval sends the way back, never the failure condition, to the builder or to a person.

Status: built, in the slice play. What differs from this page:
- The slice play, /shape-slice, writes the hidden file when it shapes the slice, before any plan exists. A script lists the lines and later checks and writes the file, and a skill drafts the recoveries. Whether this job moves here, now that slicing leaves Design → Code, is not decided.
- On today's model it finds no "Fails if" lines for the older features, whose ICE is inside their page (#1033).

## Inputs / Outputs
- In: the features whose stories are under the chosen item, found through the epic's map of features to stories.
- In: the "Fails if" lines of each feature's ICE and of its capability's ICE, and the mark that says which of the two is thin.
- In: the slice and the surface a person tests it on, from the product model.
- In: the rule for a feature's recovery, from memory through the memory tool.
- In: the entries the hidden file already has, with their ids.
- Out: each feature's entry in the hidden file, with its failure conditions, their ids and one recovery each.
- Out: for the person: the lines, how many each kind of fixer gets, and the lines too vague to judge.

## Rules & behavior
- Each "Fails if" line gets exactly one recovery. Two lines are never merged and one line is never split. The reason: the eval covers each failure condition with its own scenario, and the running eval needs one way back for each.
- This feature is the one reader of the "Fails if" lines. The writer of the stories reads every other line of the ICE. The reason: "each line of an ICE has one interpretation", so the story and the eval never disagree.
- The way back is guidance a builder or a person can follow, never code, a file name or a command. When the builder can fix it alone, it names what the builder sees and changes in the product, never the evals folder, the eval, the hidden file or the check that found it. The reason: the builder later gets only the handoff plan made from it.
- The recovery says "a person must decide" when the way back needs judgment or authority the builder does not have: money goes out or comes back, a person's data is shown to the wrong person, an approval, a choice the ICE does not settle, or anything that cannot be undone. The reason: these are decisions a builder must not make alone.
- The ids stay in the evals folder. The reason: the eval tags each failure scenario with its id, and the handoff plan never names the failure condition, its id or the check.
- A failure condition is never written in an epic, a story or the plan file, and no part that builds the work reads the hidden file. The reason: "the eval judges the build by these lines, so a builder that saw them would build to pass the check, not to meet the intent."
- Not decided: who writes the hidden file now that slicing leaves Design → Code, for wherever the plan is made. This page follows the lean that this capability writes it, just before the evals.
- Not decided: when the slice's other features get their entries, when only some of its stories are chosen.

## Acceptance criteria
- Given a feature whose ICE has two "Fails if" lines and whose capability's ICE has one, when its entry is written, then it holds three failure conditions, each with its own id and exactly one recovery.
- Given a feature whose ICE is thin, when its entry is written, then the entry says which of the two ICE is thin.
- Given a recovery the builder can fix alone, when it is read, then its way back holds no code, no file name, no command and no name of the eval, the hidden file or the evals folder.
- Given a "Fails if" line too vague to say what the eval sees, when its entry is written, then its recovery says "a person must decide", and the person sees the line before the file is kept.
- Given the stories, the epic and the plan file, when they are searched after the entry is written, then none holds a failure condition or its id.

## Out of scope
- Writing and deepening the ICE and its "Fails if" lines. Specify the product does it.
- Choosing the slice and its features. That leaves Design → Code for wherever the plan is made.
- Changing an entry when the work or the ICE changes. Update the evals as the work changes (fn-update-evals) does it.
- Writing the handoff plan when an eval fails. Test with evals the builder never sees, in Code → Validation, does it.

## Sources
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "Slicing and making the plan leave this intent for wherever the plan is made", "the code, when being written, should not get to see what tests there were"
- core/components/plays/shape-slice/scripts/write_hidden_file.py: "/shape-slice writes the slice's hidden file when it shapes the", "exactly one recovery condition for each"
- core/components/skills/author-failure-recovery/SKILL.md: "line said again as a symptom that the eval can see from the", "the opposite of the failure: the state that must be true again, as", "Never merge two lines into one recovery, and never"
- core/components/skills/author-failure-recovery/SKILL.md: "the way back needs judgment or authority the builder does", "money goes out or comes back, a person's data is shown to the wrong", "the builder can fix this alone", "a person must decide"
- core/components/plays/shape-slice/SKILL.md: "how many the builder can fix alone and how many a person must decide, the lines too vague to judge"
- docs/adr/052-shape-slice-writes-the-hidden-file-and-proposes-a-thin-ice.md: "The plan play writes only the plan file, the epic and the stories. It writes nothing in the evals folder.", "So each line of an ICE has one interpretation."
- docs/adr/052-shape-slice-writes-the-hidden-file-and-proposes-a-thin-ice.md: "First, the plan only plans: it must not write failure conditions."
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/capability.md: "The reason: the eval judges the build by these lines, so a builder that saw them would build to pass the check, not to meet the intent."
- GitHub #1033 (open): "Plays read the whole model by one rule once its index has ICE entries, so older parts break"
- standards/rules/expectation-generation.md, in Phoenix memory: "Example (a shop):", "Fails if: a card is charged twice", "way back: refund the second charge; who fixes: a person must decide (money goes out).", "hidden file or the check that found it."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "the feature (its id and name), its capability, the two ICE it was written from (and which of them is thin)", "The ids never leave the eval folder"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The handoff plan never names the failure condition, its id or the check."
- docs/philosophy/idd-principles.md: "Evals are compiled by a separate agent from failure conditions + scenarios + success, and kept in plain text in the slice's evals folder. The builder is never given them."
