## Intent
- Goal: The plans a person approved removing are deleted from the plans folder, each plan's file and folder whole, with a report of what each plan held, and nothing else changes.
- Limit: Nothing is removed without the name of the person who approved, and one bad plan refuses the whole request before anything changes.
- Limit: No file under a plan's folder is opened; its files are counted and deleted by name only.
- Limit: A plan whose file names a branch, or a plan that a plan that stays still needs, is never removed.
- Limit: The tracker and the product model are never touched.
- Fails if: A plan is deleted without the name of the person who approved, or a plan on a branch, or one that another plan needs, is deleted.
- Fails if: A file under a plan's folder is opened, or the tracker or the model changed.
- Fails if: Part of a request is applied when another part of it was refused, or a failure leaves a plan half deleted.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the request and the name of the person who approved it, each named plan's file and whether it names a branch, the plans that stay and the plans they need, and the names of the files in each named plan's folder.
- Never read: any file under a plan's folder, any memory file by its path, and any ICE page.
- Persona: the product owner, who approves removing a plan and reads the report.
- Scope: In: the checks, the removal of each plan's file and folder, putting everything back on a failure, and the report. Out: deciding which plans go, the plan's issues in the tracker, the product model, making a plan again, and a way past a refused request.

## Expectation
- Scenario: In a shop's checkout project, the product owner approves removing two old plans: one with 12 Done items and a folder of 5 eval files, one with 3 Dropped items and no folder. Both are removed, and the report lists both. A second request in the same week names a plan whose file still names its branch, and it is refused whole.
- Done means: Someone other than the one who ran it reads git, the plans folder, the tracker and the report, and finds both plans' files and the folder gone and back in git's history, the report's counts equal to the old files, no file under the folder opened, no issue changed, and, for the second request, every plan file as it was.
