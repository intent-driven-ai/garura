## Intent
- Goal: A committed change is raised as one pull request against where its branch lands, its plan's branch for an issue in a plan and main for a plan's own branch or a one-off change, naming its issue and carrying the play's run records, only after the machine checks hold: on a change's branch, a clean tree, and the issue named.
- Limit: No push and no pull request while the tree holds uncommitted work or the change is on main; no setting turns these checks off.
- Limit: The target is read from the branch name, never guessed.
- Limit: A branch has one open pull request; a second run updates it.
- Limit: Nothing reviews or judges the change before the pull request opens; the one review comes after it.
- Fails if: A pull request opens with work left uncommitted, or without its issue named.
- Fails if: The pull request's target is not where its branch lands, such as an issue in a plan raised against main.
- Fails if: A branch has two open pull requests.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the branch name and the issue it names, whether the tree is clean, any pull request open for the branch, the play's run records, and the setting of the raise's checkpoint.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, a person or an AI agent who builds the code and raises it for review.
- Scope: In: the machine checks before the pull request, the target, the push, opening or updating the one pull request, and the run records. Out: committing, the review and its verdict, scanning the push, and merging.

## Expectation
- Scenario: In a team's planning tool, a developer raises a story of a running plan: the tree is clean, the branch is pushed, and one pull request is opened against the plan's branch, naming the story's issue and carrying the run records. The review asks for a fix; after it, the raise runs again and the same pull request is updated. In a shop's checkout project, a raise with a file left uncommitted stops before the push.
- Done means: Someone other than the one who raised the change reads the code host and the run records, and finds one open pull request for the story's branch, its target the plan's branch, its issue named, the run records on the branch, and, for the checkout's change, nothing pushed and no pull request.
