Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: When a paused plan's branch lands on main, the landing shows, before the merge, that every commit on it not on main came in through a reviewed pull request or is reviewed in the landing, that every item the plan marks Done is closed under its epic with the commits that did it and each open item is named, and that the tests and linters passed on the plan's branch after main was brought in.
- Limit: What a pull request already reviewed is not reviewed again.
- Limit: Open items never hold the plan's branch off main; they are named as open.
- Limit: The landing still goes through the raise, the outside review and the person's yes.
- Fails if: A commit reaches main that no review read.
- Fails if: The plan, its epics and the commits disagree, and the landing goes on.
- Fails if: The landing reviews again the commits a pull request already reviewed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the commits on the plan's branch not on main, the pull requests that landed on it with their reviews, the plan file and its epics' issues, and the record of the tests and linters run on the plan's branch.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who pauses a plan and lands its work on main.
- Scope: In: the landing's evidence for a plan's branch and the review of its skipped commits before the merge. Out: the merge and the yes, the review itself, and pausing a plan or changing its items.

## Expectation
- Scenario: A bank's payments service pauses its plan for new statements with nine stories done and two open. The landing lists the nine with their pull requests and reviews, names the two as open, lists one plan session's commit as skipped, and the review reads only that commit before the product owner's yes.
- Done means: Someone other than the one who landed the plan compares the commits on main with the pull requests and reviews on record, and finds every commit covered by a review, the skipped one reviewed in the landing, each Done item closed with its commits, and the two open items named.
