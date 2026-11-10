# Feature: Land several ready issues in one change

## What it does
While working, a developer groups several ready issues, often bugs, into one change, so one run of the path lands them all: one branch, one pull request, one review and one merge, with each issue kept as its own issue and closed by the merge.
- Why: each run of the path costs a review, tests, records and the person's time, and running it once for each small issue multiplies that cost. In the product owner's words: "We need to group as many things as we can do together so that the overhead cost of running the entire change pipeline is reduced."
- How a group is made: when work starts, the developer names several ready issues, or the path proposes the ones that can go together, because they touch the same files or area and have no order between them.
- Each issue stays its own issue. Each bug is still logged on its own, under the story that brought it in, and grouping never changes that.
- The commits stay apart: one group of commits for each issue, each commit naming its one issue.
- The one pull request names every issue in the group, and the one merge closes each of them.
- The person's checkpoints are grouped too: the designs of all the grouped issues are shown in one step.
- Grouping never moves an issue between plans, slices or epics. A slice is an ordered group of features one person can test end to end. One change is one run of the path, not a statement about where an issue belongs.
- Examples, in different kinds of project:
  - In a shop's checkout project, three small bugs in the payment form are landed in one change, and the merge closes all three.
  - In a clinic's booking app, two bugs found under two different stories of a plan share one change on the plan's branch, and each stays under its own story.
  - In a team's planning tool, the path proposes two of four ready bugs that touch the same screen, and the developer adds a third.
- How it meets the capability: the steps stay the same; one run of them carries more than one issue, at the cost of one review.

Status: not built. Today one run opens one issue, each commit names exactly one issue, and the merge closes one issue. A loop already lands the child issues of its one main issue on its one branch, but that is one issue and its children, not a group of ready issues. The work guide still says "One issue, one session, one branch, one pull request"; this feature changes that rule, and the guide is the product owner's to update. Planned (#976, open).

## Inputs / Outputs
- In: the ready issues the developer names, or the ones the path proposes.
- In: each issue's place in its plan, slice and epic, which does not change.
- Out: one branch, with the commits of each issue kept apart.
- Out: one pull request that names every issue in the group.
- Out: after the merge, every issue in the group closed, each in its own place.

## Rules & behavior
- Each issue stays its own, in its own place. The reason: "Grouping never moves an issue between plans, slices or epics."
- Only issues with no order between them are grouped. The reason: an issue that must come after another cannot land in the same step without breaking that order.
- Each commit names one issue. The reason: the history still shows which commit did which issue, and one issue can be taken back on its own.
- The one merge closes every issue in the group. The reason: an issue left open after its work landed reads as work still to do.
- Not decided: where a group lands when its issues sit in two different plans, or one in a plan and one in no plan, since each issue lands where its own branch belongs.

## Acceptance criteria
- Given three ready bugs a developer names, when one run of the path lands them, then there is one branch, one pull request and one review, and each bug is closed after the merge. This is not built.
- Given a grouped change, when its commits are read, then each commit names exactly one of the issues. This is not built.
- Given two bugs under two stories of a plan, when they land in one change, then each stays under its own story. This is not built.

## Out of scope
- Where a bug is placed in a plan. Turn intents into agent work, in Product → Spec, and Orchestration own it.
- Adding a new feature found during a plan. Add a feature found during work (fn-add-found-feature) does it.
- Opening one change for one issue. Open each change where it will land (fn-731) does it.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-8-capability-1/page-approvals.md: "Ship every change the same way: Every change goes from opening to merge through the same steps, with a self-review, an outside review and a person's yes.", "yes, record it with self-review dropped"
- GitHub #976 (open): "while working, a person groups several ready issues (often bugs) into one change, so one run of the change pipeline lands them all.", "We need to group as many things as we can do together so that the overhead cost of running the entire change pipeline is reduced.", "Each bug is still logged on its own, as its own issue, under the story that introduced it.", "The person's checkpoints are grouped too", "One run of the change pipeline lands several issues, and each one is closed by it.", "Grouping never moves an issue between plans, slices or epics."
- .garura/user-provided/managing-work.md: "One issue, one session, one branch, one pull request."
- core/components/plays/commit-change/SKILL.md: "exactly one issue reference"
