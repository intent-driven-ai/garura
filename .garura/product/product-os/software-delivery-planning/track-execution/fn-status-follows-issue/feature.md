# Feature: An item's status follows its own issue, with no roll-ups

## What it does
When a work item's own issue closes in the tracker, its item in the plan file follows it: closed as completed is Done, and closed as not planned is Dropped. Nothing is ever worked out from the items under an item, so the plan file and the tracker show the same completion status, and no parent changes because its children closed.
- An issue's close reaches the plan file in two ways:
  - At the merge. When the merge closes an issue that landed on its plan's branch, the plan tool sets that item Done, in the same commit as the merge's records. The merge is Ship every change the same way's; the plan tool and its rule are this feature's.
  - At the start of a plan session. Each item whose issue is closed in the tracker, but still open in the plan file, goes on the session's list as "closed on GitHub", Done or Dropped. It changes the plan file only with the person's plain "approved", like every other entry.
- An issue closed as a duplicate counts as not planned, so its item reads Dropped. Any other close reads Done.
- The other way round, in a session: an item a person sets Done or Dropped has its issue closed as completed or as not planned, and an item set back to an open status has its issue reopened. Land every approved tracker write once (fn-land-tracker-writes-once) makes those writes.
- While its issue is open, the item's status is a person's: Not Started, In Progress, Now or Blocked. The tracker has no field for these, and nothing changes them on its own.
- No roll-ups. An epic stays open when all its stories close, until its own issue closes, and an epic can be closed with open stories. The plan's own Status and Direction stay the person's.
- The plan tool changes only that item's status line and the file's updated line, and keeps every other line, comment and order. An item already at that status is left as it is, so running it again changes nothing.
- Examples, in different kinds of project:
  - In a clinic's booking app, the story for choosing a slot merges on its plan's branch. Its issue closes and its item reads Done, while the epic stays open with one story to go.
  - In a news site's plan, an editor closes the story for a weekly digest as not planned, in the tracker, by hand. At the next session it shows on the list as Dropped, and it lands with "approved".
  - In a logistics app, every story of the epic for carrier tracking is closed, and the epic still reads In Progress until the product owner closes its own issue.
- How it meets the capability: completion status is tracked only when the plan file says what the tracker says about each item, and never more than the item's own issue says.

Status: built, in the plan tool's plan_status.py and in /update-plan (ADR 064). Not built, or open:
- The merge also closes the item above a landed issue once every issue under it is closed, such as the epic. This is against the rule that nothing rolls up.
- An issue closed by hand stays open in the plan file until the next session.
- /update-plan's words still say "closed on GitHub". ADR 065 reads them as the tracker, and the play's words are not changed yet.
- On GitLab, the adapter does not pass the close reason when it closes an issue, so a close as not planned cannot be told from a close as completed there.

## Inputs / Outputs
- In: the issue's state and its close reason, as the tracker holds them: open, closed as completed, closed as not planned, or closed as a duplicate.
- In: the plan file, and the item that stands for the issue.
- In: at the merge, the issue that landed on its plan's branch.
- Out: the item's status set Done or Dropped in the plan file, the file's updated line changed, and every other line kept.
- Out: the plan tool's record: the plan, the issue, the status from and to, and whether it changed.
- Out: at a session's start, one entry for each item that is closed in the tracker and open in the plan file, on the list for the person's "approved".

## Rules & behavior
- Closed as completed is Done, and closed as not planned is Dropped. The reason: "An item's status in a plan file follows its own GitHub issue.", "Closed as completed means Done.", "Closed as not planned means Dropped."
- A duplicate counts as not planned. The reason: "Closed as not planned or as a duplicate is Dropped; any other close is Done."; a duplicate is work that will not be done under that issue.
- Nothing rolls up. The reason, in the product owner's words: "If GitHub is updated to be done, then this status here has to be updated. When I said status cannot be updated, I mean don't do rollups."; and "A parent never changes because its children closed".
- An issue closed by hand changes the plan file only on the person's "approved". The reason: "An issue closed by hand is caught at the next /update-plan session and shown before it lands."; a person sees each change to the plan before it is made.
- While its issue is open, an item's status is a person's. The reason: "while the issue is open, a person sets the item's status", and "A person sets every status and the plan's direction."
- Only the item's own lines change. The reason: the plan tool "leaves every other line, comment and order as it is.", and "Nothing rolls up: the item's parent is never changed."
- Running it again is safe. The reason: "An item already at that status is left as it is."
- Not decided: whether the merge keeps closing the item above a landed issue once every issue under it is closed.
- Not decided: whether the list of items closed in the tracker, at a session's start, is this feature's or Orchestrate agent work through planning's, which an approved page of Turn intents into agent work names for "items already closed in the tracker".

## Acceptance criteria
- Given a story in a plan whose change merges on the plan's branch, when the merge closes its issue, then its item reads Done and the epic above it is unchanged.
- Given an item whose issue a person closed as not planned in the tracker, when a session starts, then the list holds that item as Dropped, and the plan file changes only after "approved".
- Given an epic whose stories are all closed and whose own issue is open, when a session starts, then the epic is not on the list and stays as it was.
- Given an item already Done, when the plan tool sets it Done again, then the file is unchanged and the record says it did not change.
- Given an issue closed as a duplicate, when a session starts, then its item goes on the list as Dropped.

## Out of scope
- The merge that closes an issue. Ship every change the same way, in Developer tooling, owns it; Merge each change where it lands (fn-673) runs this feature's plan tool.
- The status a person sets on an open item, and the plan's Status and Direction. Orchestrate agent work through planning, in Orchestration, owns them.
- Keeping the plan file's list of work items in step with the tracker. Turn intents into agent work, in Product → Spec, owns it.
- The tracker writes of a session, such as closing an issue an item was set Done for. Land every approved tracker write once (fn-land-tracker-writes-once) makes them.

## Sources
- The product owner on 2026-11-10: "Anything that already exists, like managing ADRs and execution tracking, just use what is already built to do that."
- docs/adr/064-an-items-status-in-a-plan-follows-its-own-issue-with-no-roll-ups.md: "An item's status in a plan file follows its own GitHub issue.", "Closed as completed means Done.", "Closed as not planned means Dropped.", "A parent never changes because its children closed", "The plan's own Status and Direction stay the person's.", "An issue closed by hand is caught at the next /update-plan session and shown before it lands.", "An issue closed by hand stays open in the plan file until the next /update-plan session."; and the product owner: "If GitHub is updated to be done, then this status here has to be updated. When I said status cannot be updated, I mean don't do rollups."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "now read as its own issue in the tracker"
- core/tools/plan/README.md: "Nothing rolls up: the item's parent is never changed.", "An item already at that status is left as it is."
- core/tools/plan/plan_status.py: "leaves every other line, comment and order as it is."
- core/components/plays/update-plan/scripts/closed_on_github.py: "Closed as not planned or as a duplicate is Dropped; any other close is Done."
- core/components/plays/update-plan/reference/ice.md: "A person sets every status and the plan's direction.", "Nothing is worked out from the work under an item: no roll-ups.", "closed on GitHub"
- core/components/plays/merge-change/SKILL.md: "only that item, no roll-up"
- core/components/skills/track-issue/SKILL.md: "on GitLab, the `reason` argument is silently ignored by the adapter"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "while the issue is open, a person sets the item's status", "an epic stays open until its own issue closes, and can be closed with open stories"
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/fn-keep-tracker-matched/feature.md: "Tracking the agent work's own status in the tracker. Track execution in the team's tracker owns it."
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/fn-change-work-items/feature.md: "The status of each item, the direction of the work, and items already closed in the tracker. Orchestrate agent work through planning owns them."
- .garura/product/product-os/features/fn-673/feature.md: "An issue that landed on its plan's branch is closed by the merge"
