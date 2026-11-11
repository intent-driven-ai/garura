## Intent
- Goal: Anyone sees each plan that has a branch drawn against main with the commits git counts ahead and behind, a mark on each plan behind main, and every plan with no branch named as on main, from the plan files and git alone, by one template.
- Limit: It reads only the plan files and git; it never reads the tracker or the product model, and no model call draws the graph.
- Limit: It writes no plan file, no issue and no branch.
- Limit: Every count comes from git; when git cannot tell, the count reads ? and is never guessed.
- Fails if: A count in the graph differs from the count git gives.
- Fails if: A plan behind main carries no mark, a plan level with main carries one, or a plan with no branch is not named as on main.
- Fails if: A plan is missing from the graph or is in it twice, or a plan file changed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the plan files and the branch each one names, the plan-view template's graph lines, git's branches here and on the remote, and the commits on each side between main and each plan's branch.
- Never read: any memory file by its path, any ICE page, and any plan's evals folder.
- Persona: the technical lead, who checks which plan is on which branch and how far each is from main; and the developer, a person or an AI agent who builds the code, who knows when main has moved on.
- Scope: In: the graph, its counts, the behind mark, the on-main line, and the check of the counts. Out: the cards, one plan as a tree, bringing main into a branch, cutting and landing a plan's branch, and writing the plan file's branch field.

## Expectation
- Scenario: A shop's checkout project has three plans. Guest checkout is on its branch, 2 commits ahead of main and 1 behind; gift cards is on its branch, 4 ahead and level with main; returns has no branch. The technical lead runs /list-plans --graph and sees guest checkout with 2 ahead, 1 behind and the ⚠ mark, gift cards with 4 ahead, 0 behind and no mark, and returns named on main.
- Done means: Someone other than the one who ran it counts the commits with git and reads the plan files, and finds each number in the graph equal to git's, the mark only on guest checkout, returns named on main, each plan once, and no plan file changed.
