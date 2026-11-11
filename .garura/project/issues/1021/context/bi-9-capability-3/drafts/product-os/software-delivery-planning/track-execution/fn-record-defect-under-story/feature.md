# Feature: Record a defect under the story that brought it in

## What it does
When a defect is found in a feature that a story delivered, it is recorded in the tracker as an issue of type Bug under the story whose work brought it in, with its severity as its first line and a text that says what the product does wrong and the way back, so the trace of where the defect came from is kept, and the fix can start from the bug.
- A defect is a fault in a feature a user wants: the product model holds the feature, and the product does not do what the feature says. A bug is how a plan keeps a defect as a work item. A missing feature is not a bug; it is a story.
- Where defects are found: the tests of Code → Validation, the check of the code against its standards, the eval after the work was accepted, and what Run → Product learns from use. Each of their approved pages gives recording the defect to Orchestration.
- Built in part: in a plan session, a person can add a bug under a story, in their own words. The entry is checked like any other: a bug sits only under a story, and a new item needs a title. On "approved", the bug is made once as type Bug under that story, with no label, and joins the plan file under the story.
- The bug's text, by the way of working in managing-work.md:
  - Its first line is its severity, "Severity: P<n> — <why, in one line>": one value from P1 to P4, which also says what is fixed first. Until the severity rules exist, the product owner sets it.
  - It says what the product does wrong and the way back, in the words of the handoff plan the defect came from. Those words never name the test, its rule, its id or its tool, because builders read the tracker.
- A defect found after its plan is Done belongs under the story that introduced it, and the done plan is not reopened. Today a session cannot reach a Done plan: the plan tool's branch step stops and says "a person sets its status before work starts again", and the plan's status is set in a session, so no play gives a way past it.
- Three parts of it are not built yet:
  - Filing a bug from a finding. No part takes a test's finding, a review's finding or a failed eval and files it as a bug. The bug fix play starts from an issue that is open, and comments on it.
  - Finding the story that brought the defect in. The person names it; nothing traces it from the feature the defect breaks.
  - Checking the severity line. Nothing reads it.
- Examples, in different kinds of project:
  - In a clinic's booking app, the eval after the work was accepted finds that two patients can book the same 10:00 slot. The product owner adds a bug under the story for choosing a slot, with a P1 severity line, and after "approved" it is type Bug under that story.
  - In a shop's checkout project, the security test finds that one shopper can open another shopper's order. The bug's text names the weakness and the way back, that each shopper sees only their own orders, and never names the test.
  - In a news site whose plan for the weekly digest is Done, a broken link in the digest is found. The bug belongs under the digest's story, but no session can reach a Done plan today.
- How it meets the capability: the backlog holds defects as well as new work, and only a bug under the story that brought it in keeps the trace of where it came from.

Status: built in part, in /update-plan (#730, the plan session): a person adds a bug under a story in a session. Not built: filing a bug from a finding, finding its story, checking its severity line (#934, findings and defects get one severity, P1 to P4, open), and a bug under the story of a plan that is Done.

## Inputs / Outputs
- In: the defect: what the product does wrong and the way back, in a person's words or in a handoff plan's.
- In: the story whose work brought it in, and that story's plan.
- In: its severity, P1 to P4, with why in one line.
- Out: one issue of type Bug under that story, with no label, its severity as its first line, made once.
- Out: the bug as an item under its story in the plan file.

## Rules & behavior
- A bug hangs under the story that brought the defect in. The reason: "Each Bug still hangs under the Story that introduced it, so the trace of where it came from is kept."
- A bug is type Bug, under its story by a real link, with no label. The reason: "Type lives in the type field.", and a bug sits under a story: "a spike, a chore or a bug under a story".
- A bug's first line is its severity. The reason: "A Bug carries its severity in its text.", "one value, P1 to P4, that also says what is fixed first."; and "Until the severity rules exist (#934), the product owner sets it."
- A bug's text never names the test or the check that found it. The reason: "anything the builder could read, it would end up writing to.", and the handoff plans it comes from already follow the rule: "It never names the test, its rule, its id or its tool", and "It never names the failure condition, its id, the scenario, its steps or the check."
- A bug is a defect, not missing work. The reason: "a missing feature is a Story."
- It lands only on the person's "approved", once. The reason: it is one entry of a session's list, and "What lands is exactly the list the person saw when they approved it."
- A plan that is Done is not reopened for a bug. The reason: "A bug found after a plan is done sits under the Story that introduced it; no new plan is made, and the done plan is not reopened." Today the plan tool stops at a Done plan with no way past.
- Not decided: how a bug is recorded under the story of a plan that is Done, since the done plan is not reopened and no session can reach it.
- Not decided: whether the understanding of the defect is written on its bug, as the bug fix play writes its comment on the issue today.
- Not decided: which part files a bug from a finding: the part that found it, or a person in a session.

## Acceptance criteria
- Given a story in a plan in progress, when a person adds a bug under it in a session and types "approved", then the tracker holds one issue of type Bug under that story, with no label, and the plan file shows it under the story.
- Given a bug asked under an epic, when the entry is checked, then the break is shown with a story it could go under.
- Given a bug the landing made before it stopped, when the landing runs again, then no second bug is made.
- Given a bug the product owner adds with a severity line as its first line, when the list lands, then the bug's text starts with that line.

## Out of scope
- Finding the defect, and the handoff plan each test sends. The tests and the check of the code, in Code → Validation, and the eval after the work was accepted own them.
- Understanding and fixing the defect. Fix defects test first, in Design → Code, owns it.
- Changing work items in a session, and where a bug is placed in a plan. Turn intents into agent work, in Product → Spec, owns them; this feature holds the rule for the bug itself.
- The severity rules, P1 to P4. #934 holds them, under Standards, structure, settings and memory in the tracker.
- A way past the stop at a Done plan. Give every gate a way past, in Orchestration, owns it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, the product owner on 2026-11-10: "Anything that already exists, like managing ADRs and execution tracking, just use what is already built to do that."
- .garura/product/product-os/software-delivery-planning/fix-defects-test-first/capability.md: "A defect is a fault in a feature a user wants", "A bug is how a plan keeps a defect as a work item", "recording a defect in the tracker, as a bug under the story that brought it in, with its text and its severity. Orchestration owns it", "The bug fix play starts only from an open issue in the tracker"
- .garura/product/product-os/software-delivery-planning/fix-defects-test-first/fn-understand-defect/feature.md: "Not decided: whether the understanding is written on the defect's issue in the tracker, as the bug fix play does today.", "Only the tool that knows the tracker may write it, and tracking is Orchestration's."
- .garura/product/product-os/software-delivery-planning/test-security/fn-send-security-findings/feature.md: "Recording a defect in the tracker. Orchestration owns it.", "It never names the test, its rule, its id or its tool"
- .garura/product/product-os/software-delivery-planning/test-product-with-evals/fn-send-handoff-plan/feature.md: "Recording a defect in the tracker. Orchestration owns it.", "It never names the failure condition, its id, the scenario, its steps or the check."
- .garura/product/product-os/software-delivery-planning/understand-consumers-and-competition/capability.md: "recording it in the tracker, which Orchestration owns"
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/fn-change-work-items/feature.md: "a bug, which is a defect a story's work brought in"
- core/components/plays/update-plan/reference/ice.md: "What lands is exactly the list the person saw when they approved it."
- .garura/product/product-os/software-delivery-planning/ship-every-change/fn-land-several-issues/feature.md: "Where a bug is placed in a plan. Turn intents into agent work, in Product → Spec, and Orchestration own it."
- core/components/plays/update-plan/scripts/check_entries.py: "a spike, a chore or a bug under a story", "a new item needs a title"
- core/components/plays/fix-bug/SKILL.md: "confirm the issue is open"
- core/tools/plan/plan_branch.py: "A plan that main's file marks Done or Dropped gets no branch", "a person sets its status before work starts again"
- .garura/user-provided/managing-work.md: "A Bug carries its severity in its text.", "Severity: P<n> — <why, in one line>", "one value, P1 to P4, that also says what is fixed first.", "Until the severity rules exist (#934), the product owner sets it.", "Each Bug still hangs under the Story that introduced it, so the trace of where it came from is kept.", "a missing feature is a Story.", "Type lives in the type field.", "anything the builder could read, it would end up writing to."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "A bug found after a plan is done sits under the Story that introduced it; no new plan is made, and the done plan is not reopened."
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- GitHub #730 (closed): "The /update-plan session"
- GitHub #934 (open): "Findings and defects get one severity, P1 to P4"
