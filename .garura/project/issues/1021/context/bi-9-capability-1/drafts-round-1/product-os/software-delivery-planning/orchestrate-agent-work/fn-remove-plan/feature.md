# Feature: Remove a plan on a person's approval

## What it does
Once a person has approved it, one or more plans are deleted from the plans folder, each plan's file and its folder whole, and a report says what each plan held; nothing else changes, so plans that are no longer wanted go without touching the tracker or the product model.
- The request names the play or run that asks, the person who approved, and the plans by their numbers.
- Every check runs before the first change. Any one of these refuses the whole request, and nothing changes:
  - no name of the person who approved, or an empty list;
  - a plan id that is not digits only, or the same plan twice;
  - a plan with no file, or a file that does not read as a plan;
  - a plan whose file names a branch;
  - a plan that stays and names a plan being removed among the plans it needs.
- Then each plan's file and folder move into one temporary folder beside the plans folder, the report is written, and that folder is deleted last. On any failure, everything moves back as it was, with the permissions it had.
- A plan's folder holds the evals of its slices, which no one here may read. The removal counts and deletes those files by name only, and never opens a file under the folder.
- Git keeps every deleted file, so a plan removed by mistake comes back from git.
- It never touches the tracker or the product model: issues stay open or closed as they are, and the model is not changed.
- The report: who asked, who approved, and for each plan its id, its title, its status, its items counted by status, how many files its folder held, and what was deleted.
- Examples, in different kinds of project:
  - In a shop's checkout project, the product owner approves removing two old plans whose work moved to new intents; both files and folders go, and the report shows that one held 12 Done items and the other 3 Dropped.
  - In a clinic's booking app, a request names a plan whose file still names its branch; it is refused, naming the branch, and nothing changes.
  - In a bank's payments service, a request removes the plan for the account data feed while the plan for new statements still needs it; it is refused, naming both plans.
- How it meets the capability: "sees every plan and where it stands" stays true only when the plans no longer wanted can go, on a person's word.

Status: built, in the remove-plan skill, which the issue sub-agent runs. It came with #1019 (three skills let an approved reorganisation remove model parts, write intent pages and delete plans, closed), by ADR 065 (a person may approve deleting a plan). No play runs it, and it has not been run yet. Not built, or open:
- After a plan pauses and its branch lands on main, its file still names the branch until a person sets it to none by hand, and the removal refuses a plan whose file names a branch. Pause a plan and start it again (fn-pause-plan) is not built.
- A refused request stops the person with no way past it: the person changes the request or the plan file. The way past is Give every gate a way past's, in Orchestration.
- A plan made again after a removal can make a second set of stories for the same features until the plan play reuses an open story.

## Inputs / Outputs
- In: the request: who asks, who approved, and the plan ids.
- In: the plans folder: each named plan's file, and the plans that stay, for the plans they need.
- Out: the report of who asked, who approved, and what each plan held and lost.
- Out: the named plans' files and folders gone, and nothing else changed.
- Out, on a refusal: nothing changed, no report, and an error that names the plan and why.

## Rules & behavior
- Never without the person's name. The reason: "A plan leaves the plans folder only when a person said so and when no other plan still needs it."
- All or nothing. The reason: "One bad plan refuses the whole request.", so no request is ever half done.
- The evals are never opened. The reason: "A plan's folder holds evals no one here may read: files are counted and deleted by name only".
- A plan whose file names a branch stays. The reason: a branch means its work is in progress: "While its work is in progress, a plan has its own branch, `plan/<id>/base`, and the plan changes only there."
- A plan that another plan needs stays. The reason: a plan may go only "when no other plan still needs it".
- Git keeps the files. The reason: "A deleted plan comes back from git, so the skill keeps no copy."
- Never the tracker or the model. The reason: "Plans sit outside the model and come and go, so no model page may depend on one.", and "Issues stay open or closed as they are, and the model is not touched."
- Plan ids are digits only. The reason: "Plan ids are digits only, so no path can leave the folder."

## Acceptance criteria
- Given a request the product owner approved for two plans with no branch that no other plan needs, when it runs, then both files and folders are gone, the report lists both with their items by status, and nothing in the tracker or the model changed.
- Given a request with no name of the person who approved, when it runs, then it is refused and nothing changes.
- Given two plans of which one names a branch, when the request runs, then it is refused whole, naming that branch, and neither plan is deleted.
- Given a plan that stays and needs a plan being removed, when the request runs, then it is refused, naming both.
- Given a plan whose folder holds eval files, when it is removed, then the report counts them, and no file under the folder was opened.
- Given a removed plan, when its file is taken back from git, then it reads as it did before the removal.

## Out of scope
- Deciding which plans go. A person decides, before the request.
- Closing or changing the plan's issues in the tracker. Track execution in the team's tracker owns it.
- Removing parts of the product model. Product model owns it.
- Making a plan again for a business intent. Cut an intent into epics and stories (fn-cut-intent-into-work), in Turn intents into agent work, does it.
- A way past a refused request. Give every gate a way past, in Orchestration, owns it.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "A person chooses what is delivered next as a slice, sees every plan and where it stands, and sets the order and status of the work as it runs."
- core/components/skills/remove-plan/SKILL.md: "A plan leaves the plans folder only when a person said so and when no other plan still needs it.", "One bad plan refuses the whole request.", "A plan's folder holds evals no one here may read: files are counted and deleted by name only", "A deleted plan comes back from git, so the skill keeps no copy.", "Issues stay open or closed as they are, and the model is not touched.", "Plan ids are digits only, so no path can leave the folder."
- core/components/skills/remove-plan/scripts/remove_plans.py: "Every check runs before the first change."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "A whole plan, with its folder, may be deleted on a person's named approval, through `remove-plan`.", "Plans sit outside the model and come and go, so no model page may depend on one.", "Deleting a plan deletes its evals, and rebuilding it can make a second set of stories until `/shape-plan` is fixed."
- docs/adr/061-a-plans-branch-is-cut-by-the-play-that-starts-its-work-main-first.md: "No script writes `branch: null` when a plan's branch lands on main"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "While its work is in progress, a plan has its own branch, `plan/<id>/base`, and the plan changes only there."
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- GitHub #1019 (closed): "Three skills let an approved reorganisation remove model parts, write intent pages and delete plans"
