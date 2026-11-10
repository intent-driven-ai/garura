Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: A developer names several ready issues, or takes the ones the path proposes, and one run of the path lands them all through one branch, one pull request, one review and one merge, with each issue's commits kept apart and every issue closed by the merge.
- Limit: Grouping never moves an issue between plans, slices or epics, and each issue stays its own issue.
- Limit: Only issues with no order between them are grouped.
- Limit: Each commit names exactly one issue of the group.
- Fails if: An issue of the group is still open after the merge.
- Fails if: One commit holds the work of two issues.
- Fails if: An issue's plan, slice or epic changed because it was grouped.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the ready issues and their places in the plans, the files and areas each one touches, any order between them, and the work guide's rule on one issue for each change.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, who groups several ready issues while working, to pay for one run of the path instead of several.
- Scope: In: grouping ready issues into one change, keeping their commits apart, one pull request and one merge for all, and closing each. Out: placing a bug in a plan, adding a feature found during work, and opening a change for one issue.

## Expectation
- Scenario: In a shop's checkout project, a developer groups three ready bugs in the payment form. One run of the path opens one branch, commits each bug's fix apart, raises one pull request naming all three, is reviewed once and merged after the product owner's yes; the three bugs are closed, each still under its own story.
- Done means: Someone other than the developer reads the branch's commits, the pull request and the three issues, and finds one pull request and one review, each commit naming one bug, all three bugs closed, and each still under its own story.
