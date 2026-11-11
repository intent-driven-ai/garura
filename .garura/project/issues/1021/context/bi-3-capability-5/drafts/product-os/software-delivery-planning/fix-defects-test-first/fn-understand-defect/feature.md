# Feature: Understand the defect: its feature in the product model, its tests and why they pass, and its root cause

## What it does
From a defect reported anywhere, the developer who will write its tests finds the feature of the product model that the defect breaks, the tests the project already has for that behaviour and why they pass, and the root cause, and writes only what the fix needs. A defect that no feature covers is named as a new need and not fixed.
- A defect report can come from anywhere: a person's own words, a finding in the review of a change, the eval after the work was accepted, or a bug in a plan, which Gather the work under a chosen plan item hands on. In the product owner's words: "Whenever a defect is reported, a defect can be reported anywhere." The report is read as it was given; recording it in the tracker is not this feature's work.
- Match it to the product model. The product model is the shared map of the product that people and agents read, and a feature in it is one thing a person can do inside a capability. It finds the feature the defect breaks, and the capability that holds it. For a bug in a plan, the story the bug sits under names the feature it stands for. For a report from anywhere else, it reads the product model's features against what the report says the product does wrong. In the product owner's words: "There needs to be a matching map to a product model that says this is a feature a user wants, and it's a defect."
- No feature, no fix. When no feature in the product model covers what the report asks for, the defect is not fixed here. It is named as a new need, with the report, for Specify the product, where needs become intents, capabilities and features. In the product owner's words: "If it can't find it in a product model, then it really isn't a defect per se, right, in some of those areas."
- The tests that exist. It finds the tests the project already has for that behaviour, and the separate check runs them on the code as it is. When they pass while the defect is there, it writes down why: for example, no test tries that case, or a test expects the wrong result. In the product owner's words: "Identify whether any tests exist and, if they are passing, why."
- The root cause. From the code, its history and those tests, it traces the defect to its cause: the file, the logic and why it is wrong, and what goes wrong because of it. It never repeats the report's own words as the cause. In the product owner's words: "Find the root cause, which is part of understanding tests and everything and whatnot."
- What the fix changes. It names each file the fix changes, with the change in one line, and nothing more: no design document, no other fixes weighed at length, and no steps for the builder.
- It writes the understanding in two parts. The builder's part holds the feature, the cause and what the fix changes, and names no test. The test writer's part holds all of it, with the tests that exist and why they pass.
- The developer who understands the defect reads the project's tests, so it is never the builder of the same fix. It goes on to write the tests that prove the defect.
- When the project's setting asks for it, the technical lead agrees the cause and what the fix changes before any fix code is written. When it does not, no fix code is written until the understanding and the failing tests are on record.
- A second defect found on the way is named for a person to report, and is not fixed here.
- When none of the project's code, its memory, Garura memory or Phoenix memory answers a point, it stays open and a memory update is raised for a person to approve. Nothing comes from what the AI agent knows by itself.
- How it meets the capability: this is the first step, and it keeps the fix quick. In the product owner's words: "We don't want it to go through the full-blown design and all these and stuff and things like that. It just takes too much time".

Status: not built as one job. Parts of it are built in the bug fix play, /fix-bug, live only in a full install, against this capability's rules in ways that matter:
- Its design agent traces the root cause to "the file, the logic, and why it is wrong". It then writes a full fix design, with another way weighed and ordered steps for the builder, which is the full design the product owner does not want for a fix.
- Nothing matches a defect to the product model, and nothing names a defect that no feature covers as a new need. A story in a plan file names the feature it stands for, but nothing reads that to understand a defect.
- Nothing finds the tests that already check a behaviour and says why they pass. The old skills that listed every test file of a project, and the tests a change could touch, are stale.
- Where memory gives no answer, the design agent goes on with the AI model's own reasoning, and the play's check accepts it with a reason.
- It starts only from an open issue in the tracker. A person's yes on the cause and the fix is a setting, and as configured the play does not wait for it.

## Inputs / Outputs
- In: the defect report as it was given: a person's words, a review finding, the eval's report after the work was accepted, or a bug that Gather the work under a chosen plan item hands on.
- In: the product model's features and capabilities, through the memory tool; for a bug in a plan, the plan file and the story the bug sits under.
- In: the project's code and its history, the tests it already has and how they run, and its own memory, then Garura memory, then Phoenix memory, and each memory update a person approved.
- In: the project's setting for the technical lead's yes, and the yes when it is asked for.
- Out: the builder's part of the understanding: the feature and its capability, the cause with the file, the logic and why it is wrong, and each file the fix changes with the change in one line.
- Out: the test writer's part: all of the builder's part, and each test that exists for the behaviour, whether it passes, and why.
- Out: for a defect that no feature covers, a new need named with the report for Specify the product, and no fix.
- Out: each point that nothing answered, with the memory update raised for it, and each second defect found, named for a person to report.

## Rules & behavior
- Matched to a feature before anything else. The reason, in the product owner's words: "There needs to be a matching map to a product model that says this is a feature a user wants, and it's a defect."
- No feature, no fix: a new need goes to Specify the product. The reason, in the product owner's words: "it really isn't a defect per se", and Specify the product is where the model's parts are written: "In: writing business intents, domains, capabilities and features."
- The tests that exist are found and run, and why they pass is written down. The reason, in the product owner's words: "Identify whether any tests exist and, if they are passing, why."; a test that passes while the defect is there is part of how the defect got through.
- The cause is traced, never restated. The reason, in the product owner's words: "Find the root cause, which is part of understanding tests and everything and whatnot.", and what is built already holds that "Restating the issue title or description is not RCA.", where RCA is the root-cause analysis.
- Only what the fix needs, with no full design and no steps. The reason, in the product owner's words: "we want it to be really quick", and the Design → Code business intent must not "Tell the builder the steps".
- The builder's part names no test and no reason a test passes. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were".
- The one who understands the defect is never its builder. The reason: understanding reads the tests, and the builder "cannot teach to a test it cannot see."
- The technical lead agrees the fix only when the project's setting asks for it. The reason: the older agreed line, "its fix is agreed with a person", and what is built already makes that yes a setting: "so the config switch now governs them too."
- Memory first, never the AI agent's own knowledge. The reason: an agent that works through the memory tool "never falls back to the model", and in the guide's words: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
- A second defect is named, not fixed. The reason: a fix that grows changes code nobody chose to change, and "This intent's job is to execute on the plan".
- Understanding changes nothing: no code, no test, no work item and no status. The reason: what is built already traces "Read-only against the codebase."
- Not decided: when the code exists but no feature in the product model covers it, whether it is a new need for Specify the product, or a part missing from the model for Keep the spec matched to what's built. The product owner's words leave room: "in some of those areas".
- Not decided: whether the fix waits for the technical lead's yes when the project has not set the setting.
- Not decided: whether the understanding is written on the defect's issue in the tracker, as the bug fix play does today. Only the tool that knows the tracker may write it, and tracking is Orchestration's.

## Acceptance criteria
- Given a bug in a plan under a story that stands for a feature, when the defect is understood, then the understanding names that feature and its capability.
- Given a person's report that asks the product for something no feature covers, when it is understood, then it is named as a new need for Specify the product, and no test and no code are written.
- Given two tests that exist for the behaviour and pass while the defect is there, when the defect is understood, then each is named with why it passes.
- Given an understanding, when it is read, then the cause names the file, the logic and why it is wrong, and does not repeat the report's words.
- Given the builder's part, when it is searched, then it holds no test, no test name and no reason a test passes.
- Given the setting that asks for the technical lead's yes, when no yes is given, then no fix code is written.
- Given a finished understanding, when the project is compared before and after, then no code, test, work item or status changed, and no design document or list of steps was written.

## Out of scope
- Recording the defect in the tracker, with its text and its severity. Orchestration does it, and Turn intents into agent work holds the changes to the plan today.
- Turning a new need into intents, capabilities and features. Specify the product does it.
- Adding a built part the product model is missing. Keep the spec matched to what's built does it.
- Writing the tests that prove the defect. Write the tests that prove the defect, and show each one fails (fn-write-defect-tests) does it.
- Changing the code, and understanding the defect again when the fix does not hold. Fix the code and run every test, then tidy it, without seeing the tests (fn-fix-defect-code) sends it back here.
- Designing the work. Design the work does it; a fix never goes through it.

## Sources
- The product owner on 2026-11-09, on the first overlap brief for this capability, in .garura/project/issues/1021/context/bi-3-capability-5/page-approvals.md: "Whenever a defect is reported, a defect can be reported anywhere.", "Identify whether any tests exist and, if they are passing, why.", "Find the root cause, which is part of understanding tests and everything and whatnot.", "There needs to be a matching map to a product model that says this is a feature a user wants, and it's a defect.", "If it can't find it in a product model, then it really isn't a defect per se, right, in some of those areas."
- The same file: "We don't want it to go through the full-blown design and all these and stuff and things like that. It just takes too much time", "we want it to be really quick", "it really isn't a defect per se", "in some of those areas"
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "This intent's job is to execute on the plan"
- The capability list the product owner agreed on 2026-11-03, in .garura/project/issues/1021/context/capabilities.md: "Fix defects quickly: A defect is traced to its cause, and its fix is agreed with a person and proven by a test."
- The product owner's words, recorded on 2026-11-09 in .garura/project/issues/1021/context/bi-3-capability-4/page-approvals.md: "the code, when being written, should not get to see what tests there were"
- .garura/product/product-os/intents/bi-3.md: "Tell the builder the steps, or deliver work that only a later slice makes testable."
- .garura/product/product-os/software-delivery-planning/specify-product/capability.md: "In: writing business intents, domains, capabilities and features."
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/capability.md: "any drift between them is named and fixed"
- .garura/product/product-os/software-delivery-planning/gather-work-under-item/capability.md: "a bug gathered here is handed on to it."
- core/components/plays/fix-bug/reference/ice.md: "the file, the logic, and why it is wrong", "Restating the issue title or description is not RCA.", "C1 — Anchored to an existing open defect issue."
- core/components/plays/fix-bug/SKILL.md: "an explicit `llm` fallback with a rationale"
- core/components/skills/author-rca/SKILL.md: "Read-only against the codebase."
- core/components/skills/author-fix-design/SKILL.md: "Ordered steps that a code-builder can follow without additional context.", "Every alternative must carry a concrete `rejection_reason`."
- core/components/skills/scan-test-surface/SKILL.md: "Enumerate every test file in a codebase", "waits for the rebuild of /refactor-code (#855)"
- core/components/skills/derive-blast-radius/SKILL.md: "compute directly and transitively impacted tests", "waits for the rebuild of the test skills of /refactor-code (#855)"
- core/components/agents/tech-designer.md: "proceed with LLM reasoning"
- core/tools/plan/README.md: "may have `represents` (the"
- core/config.yaml: "so the config switch now governs them too."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
- standards/rules/builder-isolation.md, in Phoenix memory: "the builder cannot teach to a test it cannot see."
- standards/rules/resolution.md, in Phoenix memory: "never falls back to the model"
