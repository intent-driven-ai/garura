# Feature: Trace a defect to its cause, and design its fix

## What it does
For a bug handed on by Gather the work under a chosen plan item, an AI agent traces the defect from what goes wrong to its cause and designs the smallest fix that removes it, and the technical lead confirms or changes both.
- A bug is a defect. It sits under the story whose work brought it in, also when it is found later. Gather the work under a chosen plan item hands it on, gathered alone when the technical lead names it by its ID ("A chosen chore, bug or spike has nothing under it, so it is gathered alone."), or with the tree when the technical lead names an item above it.
- It reads the bug's text, the story that brought it in, the project's code and its history, the design of the work in force when there is one, and the project's standards, from the project's code and memory first.
- The cause names the file, the logic and why it is wrong, and what goes wrong because of it, in plain words. It is traced from what goes wrong, through the code, to where it starts, and never repeats the bug's own words as the cause.
- The fix design names the fix chosen, at least one other fix weighed and why it lost, each file the fix changes with what changes in it, and each other file the fix could touch. It names what changes, never the steps of the fix and never a test, so the builder picks the order and the tests stay apart.
- The technical lead confirms the cause and the fix, or changes them. A setting decides whether the fix code waits for that yes. When it does not wait, no fix code is written until the cause, the fix design and the failing tests are on record.
- A second defect found while tracing is named for a person to record as its own bug, and is not fixed here. A part of the work's design that the fix shows wrong is named for Design the work.
- When none of the project's code, its memory, Garura memory or Phoenix memory answers a choice, the choice stays open and a memory update is raised for a person to approve. The AI agent never fills it from what it knows by itself.
- How it meets the capability: this is "the cause is traced", the first step of fixing a defect test first. The test writer starts from the cause, and the builder from the cause and the fix design.

Status: built in the bug fix play, /fix-bug, live only in a full install, and against this capability's rules in ways that matter:
- Its design agent traces the cause to "the file, the logic, and why it is wrong", designs the fix with at least one other way weighed and why it lost, and maps each file the fix touches.
- A person's yes on the cause and the fix is a setting. As configured, the play does not wait, and checks instead that the cause, the fix design and a failing test are on record before any fix code. The play names the tech lead as the person who reviews the cause and the fix.
- Where memory gives no answer, the design agent goes on with the AI model's own reasoning, and the play's check accepts that with a reason. Where memory is thin, it researches the web and uses what it finds with no person's approval. Both are against this capability's rule.
- Its fix design hands the code builder ordered steps, and a step's check may point at the test.
- It starts from any open bug issue a person names, not from a bug gathered under a plan item, and it writes the confirmed cause and fix on the bug's issue in the tracker.

## Inputs / Outputs
- In: the bug, with its text and the story that brought it in, from Gather the work under a chosen plan item, in short-term memory, the issue's own folder where a run keeps its working files.
- In: the project's code and its history, the design of the work in force, and the project's standards.
- In: the project's own memory, then Garura memory, then Phoenix memory, through the memory tool, and each memory update a person approved.
- In: the technical lead's confirmation or change, and the project's setting for whether the fix code waits for it.
- Out: the cause: the file, the logic, why it is wrong, and what goes wrong because of it, each with its source.
- Out: the fix design: the fix chosen, each other fix weighed with why it lost, each file the fix changes with what changes in it, and each other file it could touch.
- Out: each choice that nothing answered, with the memory update raised for it.
- Out: each second defect found, named for a person to record, and each part of the work's design the fix shows wrong, named for Design the work.

## Rules & behavior
- The cause is traced, never restated. The reason: what is built already holds that "Restating the issue title or description is not RCA.", where RCA is the root-cause analysis, and the product owner asks of a defect: "Where is the problem happening, and what would it lead to?"
- At least one other fix is weighed, with why it lost. The reason: a fix chosen with nothing weighed cannot be judged, and what is built already says "Every alternative must carry a concrete `rejection_reason`."
- The smallest fix that removes the cause. The reason: a fix that grows changes code nobody chose to change, and what is built already asks for "the minimal intervention that resolves the root cause without widening scope."
- The fix design names what changes in each file, never the steps and never a test. The reason: the Design → Code business intent must not "Tell the builder the steps", and the fix design reaches the builder, who "should not get to see what tests there were".
- The technical lead confirms the cause and the fix, or changes them. The reason: the older agreed line, "its fix is agreed with a person", and the product owner's words, "designs are going to be done by, let's say, a technical lead or an architect, maybe a technical lead."
- Whether the fix code waits for that yes is a setting. The reason: what is built already makes it one ("so the config switch now governs them too."), and the agreed list keeps "Everything that can be turned on or off" in settings.
- Memory first, never the AI agent's own knowledge. The reason: an agent that works through the memory tool "never falls back to the model", and in the guide's words: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
- A second defect is its own bug. The reason: a bug "sits under the story that introduced the defect", so a second defect may belong to another story, and fixing it here hides it from that story.
- Tracing changes nothing: no code, no test, no work item and no status. The reason: what is built already traces "Read-only against the codebase.", and "This intent's job is to execute on the plan".
- Not decided: whether the fix code waits for the technical lead's yes when the project has not set the setting.
- Not decided: whether the confirmed cause and fix are written on the bug's issue in the tracker, as the bug fix play does today. Only the tool that knows the tracker may write it, and tracking is Orchestration's.
- Not decided: where the fix of a defect starts when no story built the code it sits in. A bug "is never made where nothing is built."

## Acceptance criteria
- Given a bug that says the total is wrong when a cart holds a discount, when it is traced, then the cause names the file, the logic and why it is wrong, and does not repeat the bug's words.
- Given a fix design, when it is read, then it holds at least one other fix with why it lost and each file the fix changes with what changes, and it holds no list of steps and no test.
- Given a choice that no memory tier answers, when the fix is designed, then the choice is open with a memory update raised, and nothing in the cause or the fix design is without a source.
- Given the setting that the fix code waits for the technical lead's yes, when no yes is given, then no fix code is written.
- Given a second defect found while tracing, when the fix is designed, then it is named for a person to record, and the fix design does not cover it.
- Given a finished trace, when the project is compared before and after, then no code, test, work item or status changed.

## Out of scope
- Recording a defect as a bug, its text and its severity. Turn intents into agent work holds the changes to the plan today.
- Gathering the bug and its story. Gather the work under a chosen plan item does it.
- Writing the tests that prove the defect. Write the tests that prove the defect, and show each one fails (fn-write-defect-tests) does it.
- Updating the cause or the fix when the fix does not hold. Update the cause, the fix and its tests when the fix does not hold (fn-update-defect-fix) does it.
- Updating the design of the work. Design the work does it.
- Writing on the bug's issue in the tracker. Orchestrate agent work through planning does it, through the tool that knows the tracker.

## Sources
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "the cause is traced", "This intent's job is to execute on the plan"
- The capability list the product owner agreed on 2026-11-03, in .garura/project/issues/1021/context/capabilities.md: "Fix defects quickly: A defect is traced to its cause, and its fix is agreed with a person and proven by a test.", "Settings: Everything that can be turned on or off lives in settings."
- The product owner on 2026-11-09, on the persona, in .garura/project/issues/1021/context/bi-3-capability-1b/page-approvals.md: "designs are going to be done by, let's say, a technical lead or an architect, maybe a technical lead."
- The product owner's words, recorded on 2026-11-09 in .garura/project/issues/1021/context/bi-3-capability-4/page-approvals.md: "the code, when being written, should not get to see what tests there were"
- GitHub #902 (open), the product owner on 2026-10-27: "Where is the problem happening, and what would it lead to?"
- .garura/product/product-os/intents/bi-3.md: "Tell the builder the steps, or deliver work that only a later slice makes testable."
- .garura/product/product-os/software-delivery-planning/gather-work-under-item/fn-gather-item-tree/feature.md: "A chosen chore, bug or spike has nothing under it, so it is gathered alone."
- core/components/plays/fix-bug/reference/ice.md: "the file, the logic, and why it is wrong", "Restating the issue title or description is not RCA.", "(tech lead, reviewing the checkpoint)"
- core/components/plays/fix-bug/SKILL.md: "an explicit `llm` fallback with a rationale"
- core/components/skills/author-rca/SKILL.md: "Restating the issue title is NOT a root cause", "Read-only against the codebase."
- core/components/skills/author-fix-design/SKILL.md: "Every alternative must carry a concrete `rejection_reason`.", "the minimal intervention that resolves the root cause without widening scope.", "Ordered steps that a code-builder can follow without additional context.", "may reference the regression test"
- core/components/agents/tech-designer.md: "proceed with LLM reasoning", "When LTM is insufficient, invoke `research-domain-context` skill:"
- core/config.yaml: "so the config switch now governs them too."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
- standards/rules/resolution.md, in Phoenix memory: "never falls back to the model"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "It sits under the story that introduced the defect", "It is never made where nothing is built."
