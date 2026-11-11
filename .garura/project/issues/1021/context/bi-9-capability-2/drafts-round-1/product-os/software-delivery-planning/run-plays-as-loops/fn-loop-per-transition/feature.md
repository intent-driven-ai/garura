# Feature: Run each transition between phases as its own loop

## What it does
Each of the six transitions between the phases, product to spec, spec to design, design to code, code to validation, validation to run, and run back to product, is to have one loop of its own, named for the two phases it joins, that runs that transition's plays by the shared run until the transition's goal is met. One is built, the Discovery loop, which runs product to spec.
- The names, agreed on 2026-11-03: /loop-product-spec (now /complete-discovery), /loop-spec-design, /loop-design-code, /loop-code-validation, /loop-validation-run and /loop-run-product. There is no Ship loop. A loop's full name is its command, and only a loop's name starts with loop. Nothing is renamed yet.
- A loop is a folder of its own: its compiled command, its ICE, its done check and its scripts. Its command holds only its own values between two anchor lines that point to the shared run, and a check looks for those lines.
- A loop runs only plays that check a loop contract. Each play stays usable by hand.
- The Discovery loop is the one built. From a working prototype and its write-up, it reads the prototype once and runs the three writers of Product → Spec on that reading, in rounds: the business intents, the domains, and the capabilities and features. It has the model's gaps closed after each round, and it ends at the pull request, where the person types confirm or drop for each intent. Until the review tool exists, that typed decision stands in for the review. Its done check has eight parts, from its contract to every node linked.
- The other five loops are names only. The spikes for their recipes sit under the transitions they serve:
  - #608 (decide the Slice loop's recipe) and #609 (decide the Execute loop's recipe), under BI-3, to be rewritten under the new names;
  - #611 (decide the Learn loop's recipe), under BI-6, to be rewritten under the new name;
  - #610 (decide the Ship loop's recipe), under BI-4, which decides a loop that no longer exists.
- Approved pages of the transitions already count on these loops. Code → Validation says the loop for its step runs its plays, and that when each run starts is the plan's.
- A project that builds its own harness, such as Garura's own repository, is laid no loop: it builds loops but runs none.
- Examples, in different kinds of project:
  - In a clinic's booking app, the product owner gives /complete-discovery, to be /loop-product-spec, a working prototype and its write-up, and gets business intents, domains, capabilities and features, all linked, on one branch.
  - In a shop's checkout project, /loop-code-validation is to run the plays of Code → Validation on a built slice, in rounds, until its tests pass or a person is asked. It is not built.
  - In a team's planning tool, /loop-run-product is to run the plays of Run → Product, taking what is learned in use back into the model. It is not built.
- How it meets the capability: one goal for each transition: a person gives the loop of a transition its goal, and the loop runs that transition's plays until it is met.

Status: built in part. One loop is built, the Discovery loop, as /complete-discovery. Not built, or open:
- The other five loops are not built. The recipes of three of them are open: #608 (decide the Slice loop's recipe), #609 (decide the Execute loop's recipe) and #611 (decide the Learn loop's recipe). #610 (decide the Ship loop's recipe) is overtaken.
- Nothing is renamed: the Discovery loop keeps its old name, and the loop docs list five loops under their old names.
- The Alignment loop, which older records send drift to, joins no two phases. It is unapproved and unnamed.

## Inputs / Outputs
- In: for each transition, its plays, each of which checks a loop contract; the questions it asks first; the documents and the source it reads; and how it ends.
- In: the loop's ICE: its goal, its constraints, its failure conditions and its Done means.
- In: the shared run every loop points to.
- Out: one loop for each transition, named loop-<from>-<to>, with its done check and its scripts, pointing to the shared run.
- Out: today, one loop: the Discovery loop.

## Rules & behavior
- One loop for each transition. The reason: "the product owner wants one thing to remember for each transition."
- A loop is named loop-<from>-<to>, always in full. The reason: "a loop's full name is its command", and the full name "keeps a loop apart from Claude Code's `/loop` command and from the agent loop."
- There is no Ship loop. The reason: opening, committing, reviewing and merging are commands anyone runs, and "the change chain stays as commands."
- A loop's plays stay its transition's. The reason: "The drive's one rule is to run its plays. Every other rule lives in the plays."
- A loop holds only its own values and points to the shared run. The reason: the builder "emits exactly that, so a direct edit and a rebuild converge."
- A loop runs only plays that check a loop contract. The reason: without it a play would open its own change and stop at its checkpoints: "these plays cannot run inside a loop (they check no loop contract)".
- Each play stays usable by hand. The reason: "Neither path is a fault: the plays stay usable on their own, and the drive is how the loop closes without the person."
- No loop is laid in a project that builds its own harness. The reason: "a harness repo builds loops but runs none".
- Not decided: whether each loop belongs to this capability or to the transition whose plays it runs.
- Not decided: whether Garura's own repository runs its own loops.
- Not decided: the recipe of each loop not built: which plays it runs, what it asks first, and how it ends.

## Acceptance criteria
- Given the Discovery loop, when a person gives it a working prototype and its write-up, then it runs its three plays in rounds on one branch and ends at a pull request where the person types confirm or drop for each intent.
- Given the compiled Discovery loop, when its check runs, then its two anchor lines are each there once, the opener before the closer, and the shared run exists.
- Given a loop that names a play that checks no loop contract, when the loop's pre-flight runs, then it halts and names that play.
- Given a harness repository, when Garura is installed there, then no loop is laid.
- Given the six loops once named, when their commands are listed, then each is loop-<from>-<to> for two phases next to each other, and none is called just /loop. Nothing is renamed yet.

## Out of scope
- The plays each loop runs and what they write. The transition intents (BI-1, BI-3, BI-4 and BI-6) own them.
- The Discovery loop's own pages, and pages a person can use from its run (#972, a person runs the Discovery loop and gets pages they can use). Specify the product, in Product → Spec (BI-1), owns them.
- Building and changing a loop, and checking it against the loop principles (#699, the loop builders check the loop principles). Build your own harness, in Standards, structure, settings and memory (BI-10), owns them.
- The loop names and the naming rule. Standards, in Standards, structure, settings and memory (BI-10), owns them.
- The review each loop ends in, and the merge. Review what agents make (Argus) and Ship every change the same way, in Developer tooling (BI-8), own them.
- When each run starts. Orchestrate agent work through planning owns it.
- How each loop runs. Run any loop the same way (fn-run-loop) does it.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md, line 97: "Run plays as loops: A person gives one goal, and a loop runs its plays until the goal is met."
- .garura/project/issues/1021/context/names.md, lines 22-24: "/loop-product-spec (was /complete-discovery) · /loop-spec-design · /loop-design-code · /loop-code-validation · /loop-validation-run · /loop-run-product", "There is no Ship loop."
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md, lines 77-79, 105, 143 and 153: "a loop's full name is its command", "Only a loop's name starts with `loop`.", "The Alignment loop is unapproved and unnamed", "the change chain stays as commands", "the product owner wants one thing to remember for each transition.", "#610 decides a Ship loop that no longer exists."
- docs/adr/045-a-drive-is-now-called-a-loop.md, line 48: "keeps a loop apart from Claude Code's `/loop` command and from the agent loop."
- docs/adr/029-drives.md, line 37: "The drive's one rule is to run its plays. Every other rule lives in the plays."
- docs/adr/043-kickoff-plays-read-independently-and-the-drive-closes-the-loop.md, line 81: "Neither path is a fault: the plays stay usable on their own, and the drive is how the loop closes without the person."
- core/components/loops/complete-discovery/SKILL.md, lines 3-13 and 104-120: "ends at the pull request where the person types confirm or drop for each intent", "# --- Shared Loop Run (shared; see ../_shared/loop-run.md) ---"
- core/components/loops/complete-discovery/stop-condition.yaml, lines 1-27: "the model's gaps are closed: every node linked, no screen uncovered"
- core/components/loops/_shared/loop-run.md, lines 9-11 and 424-430: "emits exactly that, so a direct edit and a rebuild converge.", "opener before closer"
- core/components/loops/complete-discovery/scripts/loop_preflight.py, line 126: "these plays cannot run inside a loop (they check no loop contract)"
- core/components/plays/install-garura/scripts/install.py, line 265: "a harness repo builds loops but runs none"
- docs/components/loops.md, lines 71-79: "To build (#608)", "To build (#609)", "To build (#610)", "To build (#611)"
- docs/adr/041-a-drive-runs-in-rounds-and-owns-its-questions.md, line 72: "The intents stay proposed until Argus's review step writes approval"
- .garura/product/product-os/software-delivery-planning/test-security/fn-retest-security/feature.md, line 35: "When each run starts is the plan's.", "the loop for this step, /loop-code-validation, runs the plays of Code → Validation."
- The stock-take of Orchestration, .garura/project/issues/1021/context/bi-9-inventory/inventory.md, sections 2.2 and 2.6, and section 12, questions 7 and 12: "Who owns each loop: Run plays as loops, or the transition whose plays it runs?", "Should Garura's own repository run its own loops?"
