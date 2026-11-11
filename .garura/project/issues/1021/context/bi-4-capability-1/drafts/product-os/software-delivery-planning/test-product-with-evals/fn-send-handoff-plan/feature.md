# Feature: Send each failure back as a handoff plan, to the builder or to a person

## What it does
For each failure the eval finds, this feature writes a handoff plan, which says what the product does wrong, as a symptom, and the way back, and sends it to the builder when the builder can fix it alone, or to a person when a person must decide, so the failure is fixed without anyone who builds the work seeing the eval.
- The slice's hidden file holds, for each failure condition, one recovery in three parts: when, the symptom the eval sees from the outside; way back, the state that must be true again; and who fixes, "the builder can fix this alone" or "a person must decide".
- When a scenario that shows a failure condition does not happen fails, this feature finds that condition's recovery by the id the scenario carries, and reads only its recovery parts. It never reads the failure condition itself.
- When a scenario for a goal or an expectation fails, there is no recovery to read, so the handoff plan names the line of the story that is not met, in the story's words, with what the product did instead. An unmet goal goes to the developer, whose part of the story holds the goals. An unmet expectation goes only to the test writer of Build the work test first, who holds the story's expectations, writes a test for it and shows it fails; the builder then fixes the code against that test, as for every test, and never sees the expectation.
- The handoff plan says, in plain words, what the product does wrong and the way back. It never names the failure condition, its id, the scenario, its steps or the check. For example, in a clinic: "Two patients can book the same 10:00 slot when they book at the same time. Make the second one see that the slot is gone."
- One that the builder can fix alone goes to the developer through Build the work test first, whose test writer writes a test for it first and whose builder then fixes the code. One that a person must decide goes to the product owner, with what was seen.
- A failure found after the work was accepted is a defect. It goes to Fix defects test first, which takes in a defect reported by the eval.
- How it meets the capability: the eval stays a test the builder never sees only if what goes back from it names the symptom and never the check. In the words of the routing table: the builder gets "only the resulting handoff plan".

Status: not built. What exists covers only part of it:
- The recoveries are written. The hidden file holds one recovery for each failure condition, with when, the way back and who fixes. Today the slice play writes it when it shapes the slice.
- Nothing writes a handoff plan, and where it is kept, and how it reaches the builder, is not decided.
- Build the work test first takes in a handoff plan that the builder can fix alone, and Fix defects test first a defect the eval found after acceptance. Neither is built.
- The old slice check, /validate-epic, is stale. Its fix report gave the build the exact list of the work, but it named each failure by its check and where the check fired, which a handoff plan must not.

## Inputs / Outputs
- In: each failing scenario from the verdict, with the id of the failure condition it shows, or the story lines it covers.
- In: the line of the story that a failing goal or expectation scenario covers, in the story's words.
- In: the recovery parts of the slice's hidden file: when, way back and who fixes, for each failure condition's id.
- In: whether the work was already accepted.
- Out: for each failure, a handoff plan with the symptom and the way back, sent to the developer through Build the work test first, to the product owner, or, after acceptance, to Fix defects test first as a defect.
- Out: in the verdict, where each handoff plan went, so the product owner sees it.

## Rules & behavior
- A symptom and a way back, never the check. The reason: a handoff plan "never names the failure condition, its id or the check", so the builder still "cannot teach to a test it cannot see."
- Only the recovery parts of the hidden file are read. The reason: "The running eval reads only the recovery parts of the hidden file, and the builder gets only the handoff plan made from them."
- The way back is guidance, never code. The reason: the way back is "the inverse of the failure, as guidance, never code", and how to build it is the developer's.
- The recovery decides who gets it. The developer gets it only when the recovery says the builder can fix it alone; otherwise a person does. The reason: the handoff plan "goes to the builder when the builder can fix it alone, and to a person when a person must decide".
- The person who decides is the product owner. The reason: the product owner names the work and owns what it is for, and a recovery that needs a person needs "judgment or authority the builder does not hold".
- One handoff plan is the whole of the work it calls for. The reason: Build the work test first builds nothing beyond it: "A handoff plan is the exact list of the work it calls for."
- Before acceptance to the build, after acceptance to the defect fix. The reason: the approved Fix defects test first page leaves "a failure the eval finds before the work is accepted" to Build the work test first, and takes in "the eval after the work was accepted".
- A goal or an expectation not met sends its own line of the story: an unmet goal to the developer, an unmet expectation only to the test writer. The reason: only failure conditions have a recovery, so the story's own line is the way back, and the split of each story holds: "The builder's part holds the story's title, goals, limits and Context guidance", and "The test writer's part holds the story's expectations". The product owner approved on 2026-11-09 that the unmet line of the story goes back.
- Not decided: where the handoff plan is kept, and how it reaches the developer or the person.
- Not decided: whether a way back that changes the design goes to the technical lead, who designs the work, instead of the product owner.
- Not decided: what marks the work as accepted.

## Acceptance criteria
- Given a failing scenario that shows a failure condition whose recovery says the builder can fix it alone, when the handoff plan is written, then it holds the symptom and the way back, goes to the developer, and names no failure condition, id, scenario or check.
- Given a failing scenario for a goal of a story, when the handoff plan is written, then it names that goal in the story's words and what the product did instead, goes to the developer, and names no scenario, step or check.
- Given a failing scenario for an expectation of a story, when it is sent back, then the expectation's line goes to the test writer of Build the work test first, and nothing the builder is handed names it.
- Given a failing scenario whose recovery says a person must decide, when the handoff plan is written, then it goes to the product owner and not to the developer.
- Given a run of this feature, when its reads are checked, then it read no failure condition of the hidden file.
- Given a failure the eval finds after the work was accepted, when it is sent back, then it goes to Fix defects test first as a defect.

## Out of scope
- Writing the hidden file and its recoveries. Write the evals that check the work does it.
- Fixing the failure. Build the work test first does it before the work is accepted, and Fix defects test first after.
- Recording a defect in the tracker. Orchestration owns it.
- Running the eval and giving the verdict. Run a slice's eval on the built work, and give the verdict (fn-run-slice-eval) does it.
- Counting the rounds of the same failure. Run the evals again as the product changes (fn-rerun-evals) does it.

## Sources
- standards/schemas/product-os/ontology.md, in Phoenix memory: "it goes to the builder when the builder can fix it alone, and to a person when a person must decide", "The handoff plan never names the failure condition, its id or the check.", "Where the handoff plan is kept, and how it reaches the builder, is not part of this ontology.", "Two patients can book the same 10:00 slot when they book at the same time. Make the second one see that the slot is gone."
- standards/rules/expectation-generation.md, in Phoenix memory: "The running eval reads only the recovery parts of the hidden file, and the builder gets only the handoff plan made from them.", "the inverse of the failure, as guidance, never code", "judgment or authority the builder does not hold", "so they name what the builder sees and changes in the product, never the evals folder, the eval, the hidden file or the check that found it"
- standards/rules/eval-format.md, in Phoenix memory: "is the id the hidden file gives it, which stays with its condition."
- standards/rules/builder-isolation.md, in Phoenix memory: "the builder cannot teach to a test it cannot see."
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md: "It says what the product does wrong, as a symptom, and the way back. It never names the failure condition, its id or the check.", "Where the handoff plan is kept, and how it reaches the builder, is not decided."
- .garura/product/product-os/software-delivery-planning/gather-work-under-item/fn-gather-item-tree/feature.md: "The builder's part holds the story's title, goals, limits and Context guidance", "The test writer's part holds the story's expectations"
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/bi-4-capability-1/page-approvals.md: "approved", on the capability page with "the lean that a failing goal or expectation sends the developer the unmet line of the story"
- docs/philosophy/idd-principles.md, The Routing Table: "only the resulting handoff plan", "builds the recovery handoff plan"
- .garura/product/product-os/software-delivery-planning/domain.md: "the product owner, who names the work"
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-update-tests-and-code/feature.md: "A handoff plan is the exact list of the work it calls for.", "A handoff plan that says a person must decide does not come here; it goes to a person.", "The test writer updates the tests from the changed test writer's part, the updated design or the handoff plan."
- .garura/product/product-os/software-delivery-planning/fix-defects-test-first/capability.md: "Out: building stories, chores and spikes, and a failure the eval finds before the work is accepted. Build the work test first owns them.", "In: taking in a defect reported anywhere: a person's words, a finding in a review, the eval after the work was accepted, or a bug in a plan.", "Out: recording a defect in the tracker, as a bug under the story that brought it in, with its text and its severity. Orchestration owns it"
- .garura/product/product-os/software-delivery-planning/write-work-evals/capability.md: "Out: running the evals, giving the verdict, and writing the handoff plan, which tells the builder or a person what went wrong and the way back. Test with evals the builder never sees, in Code → Validation, owns them."
- core/components/plays/shape-slice/scripts/write_hidden_file.py: "/shape-slice writes the slice's hidden file when it shapes the"
- core/components/plays/validate-epic/SKILL.md: "the fix report names each failure by check and location"
