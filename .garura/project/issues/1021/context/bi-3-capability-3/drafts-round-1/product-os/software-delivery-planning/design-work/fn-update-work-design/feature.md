# Feature: Update the design as the work changes

## What it does
When the design of the chosen work no longer matches the work, the technical lead confirms an update, and what held before stays readable with why it changed.
- The design is the one design of the work under the item the technical lead named, with a technical part and a surface part for each story, chore and spike. Design the chosen work, how it is built and what its surface shows (fn-design-chosen-work) writes it.
- A design needs an update when the work changes, for example:
  - a story, chore or spike under the chosen item is added, changed or dropped in the plan;
  - a project standard the design follows is updated, such as the project's architecture or a declared surface, or the capability that owns a gap the design named closes it;
  - the developer, while building, finds the design wrong and builds it another way, with the reason written down;
  - the technical lead changes a choice before or during the build.
- The AI agent proposes the update from the same sources as the first design: the project's code and memory first, then Garura memory, then Phoenix memory, then research only through a memory update a person approves. The technical lead confirms it.
- The update changes only the parts the change touches, under the same rules as the first design: no eval or test in it, the project's standards followed, and each gap named.
- From its confirmation, the updated design is the one in force. What held before is kept as it was, marked replaced, with who changed it, when and why.
- When the build departs from the design, the design is brought up to what was built, as a new version, once the technical lead confirms it.
- How it meets the capability: the design is what the developer builds from, so it must keep saying what is built and what is still to be built, as the work changes. Changing something later is worded as updating it as the project changes, as the product owner put it for the project's architecture: "this should be reflected as updating arch. as the project changes."

Status: not built. What exists covers only parts of it:
- The bug fix play sends a failed fix back to its design agent: after two failed tries, the agent revises the fix design and its test, and the fix goes on. It belongs to Fix defects test first.
- In the bug fix play, a check fails a file the builder changed that the design did not name, unless the builder wrote down why. The design itself is not updated.
- Bringing the design up to what was built, as a new version with both versions kept, is recorded and not built (#990). Agreeing a change to a design first, and writing a last change into the design before the build starts, is recorded and not built (#978).

## Inputs / Outputs
- In: the design in force, and what changed: the work items under the chosen item, a project standard, a gap closed, the developer's departure with its reason, or the technical lead's change.
- In: the builder's part of the changed work items and their collected context, from Gather the work under a chosen plan item.
- In: the project's code and its own memory, then Garura memory, then Phoenix memory, through the memory tool, and a memory update a person approved.
- In: the technical lead's confirmation of the update.
- Out: the updated design, in force from its confirmation, with each changed choice, its source and why it changed.
- Out: what held before, kept as it was and marked replaced, with who changed it and when.
- Out: each new gap in the project's standards, named for the capability that owns it.

## Rules & behavior
- An update replaces what held before and never edits it. The reason: "Both versions are kept, with who approved the first, who changed it, and why.", so the work already built on the old design can still be explained.
- An update says why: what changed in the work, in a standard or in the build, with its source. The reason: the next person can then tell a change of the work from a mistake put right.
- Only the parts the change touches change. The reason: an update answers one change, and a part the change does not touch still holds what the technical lead confirmed.
- The same rules as the first design hold: it starts from the builder's part, holds no eval, test, success scenario, story expectation or failure condition, follows the project's standards and names each gap. The reason, in the product owner's words: "the code, when being written, should not get to see what tests there were".
- When the build departs from the design, the design follows what was built, after the technical lead confirms it. The reason: "When the build drifts from the design, the design file is brought up to what was built.", and it is kept "as a new version", so the design never says one thing while the code does another.
- The technical lead confirms each update, and nothing waits for it. The reason: the design is the technical lead's, and "The harness never stops a person."
- An update never changes a project standard, a work item or the plan. A change that needs one is named for the capability that owns it. The reason: the design follows the standards and executes on the plan.
- Not decided: whether an update that a dropped or changed story calls for is started by the plan's change, by the technical lead or by the build.
- Not decided: how the developer's tests are kept in step when an update changes a class or function they were written to.

## Acceptance criteria
- Given a design in force and a new story added under the chosen epic, when the design is updated, then the new story has a technical part and a surface part, every other part is word for word as before, and the earlier version is readable, marked replaced, with why.
- Given the project's architecture updated to a new data store, when the design that follows it is updated, then each choice that named the old store is changed with the reason, and the architecture itself is unchanged by the update.
- Given a developer who built a function in another file than the design named and wrote down why, when the design is updated, then the design names the file that was built, and the earlier version and the reason stay readable.
- Given an update that no one confirmed, when it is asked for, then the design in force does not change.
- Given an updated design, when it is searched for each story's expectations, an eval, a test, a success scenario and the names of the evals folder, the hidden file and the ICE pages, then nothing is found.

## Out of scope
- Writing the first design. Design the chosen work, how it is built and what its surface shows (fn-design-chosen-work) does it.
- Changing the plan and its work items. Turn intents into agent work holds them today.
- Updating a project standard. The capability of Spec → Design that owns it does it.
- Changing the tests and the code to the updated design. Build the work test first does it.
- Putting what the update changes into the product model. Keep the spec matched to what's built does it.

## Sources
- The product owner on 2026-11-07, in .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "this should be reflected as updating arch. as the project changes."
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/bi-3-capability-1b/page-approvals.md: "designs are going to be done by, let's say, a technical lead or an architect, maybe a technical lead."
- The product owner on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "the code, when being written, should not get to see what tests there were", "This intent's job is to execute on the plan"
- .garura/product/product-os/intents/bi-2.md: "Each position is written down and can change later."
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "Never: change the architecture's words in place. An update replaces what held before and keeps it.", "work already built on the old architecture must still be explainable."
- core/components/plays/fix-bug/SKILL.md: "on exhaustion it re-invokes", "`tech-designer` to revise the design/test and resumes — it does not halt blindly."
- core/components/plays/fix-bug/scripts/check_scope.py: "A modified file is in-scope when it appears in design.affected_files, OR it carries a", "non-empty deviation_justification."
- GitHub #990 (open): "When the build drifts from the design, the design file is brought up to what was built.", "as a new version", "Both versions are kept, with who approved the first, who changed it, and why.", "The harness never stops a person."
- GitHub #978 (open): "so the file always says what was agreed.", "A last change is agreed and written into `design.md` before the build starts."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:", "An update always goes to the issue's short-term memory, and it is used only after a person"
