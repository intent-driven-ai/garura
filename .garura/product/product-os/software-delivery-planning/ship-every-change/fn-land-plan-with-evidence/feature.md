# Feature: Land a plan's branch on main with evidence that every commit was reviewed

## What it does
When a plan pauses and its branch is raised to main, the landing shows the product owner, before the merge, that every commit on the plan's branch was reviewed and that the plan, its epics and the commits agree, so the landing neither reviews again what each pull request already reviewed nor lets anything reach main unreviewed.
- A plan's branch reaches main after many reviewed pull requests, one for each issue that landed on it. As asked: "The review that lands it should not repeat that work, and should not miss anything either."
- What the landing shows the product owner, before the merge:
  - Every commit was reviewed. Each commit on the plan's branch that is not on main came in through a reviewed pull request, or is listed as skipped. A skipped commit is reviewed in the landing, before the merge. A plan session's own commit on the plan's branch is one such commit, because it has no pull request of its own.
  - The plan, its epics and the commits agree. Every item the plan marks Done is closed on the code host, under its epic, and has the commits that did its work. Open items are allowed, because a plan does not need to be finished to land, and each one is named as open.
  - Main does not break. When main is brought into the plan's branch, all the tests and linters run on the plan's branch then, because that is where a break shows. Once they pass, the landing cites that run as its evidence and does not run them again.
- The landing still goes through the same steps as any change: the raise, the outside review and the merge with the person's yes.
- Examples, in different kinds of project:
  - In a bank's payments service, a plan for new statements pauses with nine stories done and two open. The landing lists the nine with their pull requests and the two as open, and the review reads only one commit no pull request reviewed.
  - In a clinic's booking app, a plan's branch holds a plan session's commit that added a story. The landing lists it as skipped and reviews it before the merge.
  - In a shop's checkout project, one story is marked Done in the plan but its issue is still open. The landing names the disagreement, and nothing is merged until it is fixed.
- How it meets the capability: a plan's branch is a change too; this keeps its landing the same as any other, with the review reading only what no review read before.

Status: not built. The landing itself is built: a paused plan's branch is raised to main, reviewed as one whole change and merged after the person's yes, in Merge each change where it lands, on the review's approval and a person's yes (fn-673). Nothing shows which commits were reviewed, nothing checks that the plan, its epics and the commits agree, and the review reads the plan's whole branch again. Planned.

## Inputs / Outputs
- In: the commits on the plan's branch that are not on main.
- In: the pull requests that landed on the plan's branch, with their reviews.
- In: the plan file, its epics and their issues on the code host.
- In: the record of the tests and linters run on the plan's branch after main was brought in.
- Out: the landing's evidence: each commit with the pull request and review that covered it, or listed as skipped; each Done item with its closed issue and its commits; each open item named; and the test and linter run it cites.
- Out: the review of the skipped commits only, before the merge.

## Rules & behavior
- Every commit that reaches main was reviewed once. The reason: "Anything skipped is reviewed as part of the landing, before the merge."
- What a pull request already reviewed is not reviewed again. The reason: it is left out, "reviewing again what a pull request already reviewed", because the work and its cost were already paid.
- Open items never hold the plan off main; they are named. The reason: "Open items are allowed (a plan does not need to be finished to land), and each one is named as open."
- A disagreement between the plan, its epics and the commits stops the landing until it is fixed. The reason: the plan file is the person's view of the work, and a wrong view on main misleads the next reader.
- Not decided: how the landing tells a commit that came in through a reviewed pull request from one that did not, such as by the pull requests' merge commits or by the run records.

## Acceptance criteria
- Given a plan's branch whose commits all came in through reviewed pull requests, when it is raised to main, then the landing lists each with its pull request and the review reads no commit again. This is not built.
- Given a plan's branch with one commit that no pull request reviewed, when it is raised, then that commit is listed as skipped and is reviewed before the merge. This is not built.
- Given a plan whose file marks an item Done while its issue is open, when the branch is raised, then the landing names it and nothing is merged. This is not built.

## Out of scope
- The merge of the plan's branch and the person's yes. Merge each change where it lands, on the review's approval and a person's yes (fn-673) does it.
- The review of the skipped commits. Check the code against its standards, in Code → Validation, does it.
- Pausing a plan and changing its items. Turn intents into agent work, in Product → Spec, and Orchestration own them.

## Sources
- The product owner on 2026-11-10: "Ship every change the same way: Every change goes from opening to merge through the same steps, with a self-review, an outside review and a person's yes.", "yes, record it with self-review dropped"
- docs/adr/060-a-plans-branch-merges-into-main-when-the-plan-pauses.md: "When the plan pauses, its branch merges into main through the change plays"
- core/components/plays/update-plan/SKILL.md: "the plan's branch reaches main later through the change plays"
