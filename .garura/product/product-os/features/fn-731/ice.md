## Intent
- Goal: The change a person names is opened where it will land: its issue is found or filed with a checked title and description, its branch is cut from its plan's branch, holding the latest main, for an issue in a plan, or from an up-to-date main for a one-off change, a plan's branch is cut main first when the plan's work starts, and the issue's working folder is made with the start's record committed on the branch.
- Limit: Nothing starts when nothing is typed, and the change is never taken from the branch the session is on.
- Limit: Which plan an issue is in is read from the plan files in git, on main and on the plan's own branch, never guessed and never read from the open copy.
- Limit: A plan's branch is cut only main first, through the one script that makes every cut, and a closed plan's branch is never cut again.
- Limit: Running it again for the same issue makes no second issue and no second branch, and no local branch with commits found nowhere else is deleted.
- Fails if: An issue in a plan is cut from main, or the plan's branch is behind main when an issue's branch is cut.
- Fails if: Work starts with no issue, or an issue is filed whose title or description fails its check.
- Fails if: A change is started that the person did not name, or a plan's branch is cut without main's plan file set to In Progress first.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: what the person typed, the open issues in the tracker, the plan files on the latest main and on each plan's branch, the branches here and on the code host, the project's setting for a worktree, and any issue folder or branch that already exists for the issue.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, who opens each change; and the product owner, who starts a plan's work.
- Scope: In: reading what was typed, finding or filing the issue, cutting the change's branch where it will land, cutting a plan's branch when its work starts, the worktree, and the working folder. Out: committing, raising and merging, several issues in one change, and making or changing a plan.

## Expectation
- Scenario: A team's planning tool has a plan with two stories and no plan's branch. A developer opens the first story: main's plan file is set to In Progress with the branch named and pushed on main, the plan's branch is cut from that commit, and the story's branch from the plan's branch. A week later, after other work merged into main, the developer opens the second story: main is merged into the plan's branch first, and the second story's branch is cut from it. A one-off bug in the same week gets its branch from the latest main.
- Done means: Someone other than the one who opened the changes reads the branches on the code host and main's plan file, and finds two story branches off the plan's branch, the plan's branch holding the latest main when the second was cut, main's plan file In Progress on the commit the plan's branch was cut from, the bug's branch off main, and one issue and one branch for each change.
