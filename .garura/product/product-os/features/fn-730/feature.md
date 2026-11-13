# Feature: Set each item's status and the plan's status and direction in one approved session

## What it does
In one working session on one plan, /update-plan, a person sets the status of the plan's items, and the plan's own Status and Direction, in their own words; on one plain "approved", every change lands at once in the tracker and the plan file, on the plan's own branch, in one commit, so the order and status of the work are always what a person said, and the plan file and the tracker agree.
- The session opens on one plan, by its number or by a description. A description's match is shown and waits for the person's yes. A plan is never guessed and never made.
- The session first gets onto the plan's branch, and at the end it goes back. Get onto a plan's branch for a session, and come back (fn-go-to-plan-branch) does that.
- What the person can set in a session, in their own words:
  - an item's status: Not Started, In Progress, Now, Blocked, Done or Dropped. Done closes the item's issue as completed, Dropped closes it as not planned, and an open status reopens an issue that is closed;
  - the plan's Status: Not Started, In Progress, Paused, Done or Dropped. It changes the plan file only;
  - the plan's Direction: next, next in line, later, or none. It changes the plan file only, and several plans may share a direction.
- When the session starts, each item whose own issue was closed in the tracker, but is still open in the plan file, goes on the list under the instruction "closed on GitHub": Done for an issue closed as completed, Dropped for one closed as not planned. Its parent is never put on the list. It lands only with the person's "approved", like any other entry.
- Each instruction becomes list entries, and each entry is checked against the plan's rules before it joins the list: a status the plan knows, and an item that is in the plan. An entry that changes nothing is not added. No status or direction is ever added that no instruction named.
- A big change is shown and confirmed before it joins the list: dropping an epic, or closing an item with open work under it.
- A rule break is shown with what works instead. The person may say "do it anyway"; the entry joins, and the landing's commit names the override.
- Only the plain word "approved" lands the list. "Rejected" lands nothing, and the session goes on until the list is ready. "Abort" drops the list, writes nothing, and undoes a plan branch the session cut. Anything else is answered or followed, the list is shown again, and the person is asked again.
- On "approved", the approval is checked to be for the very list the person saw. Then the tracker is written, then the plan file, then a check proves that the plan file, the tracker and the approved list agree and nothing else changed, and then one commit is made on the plan's branch and pushed. Its message names each instruction as the person typed it, each override with the rule it breaks, and what is still owed.
- The session's own working files are removed at the end. A landing that stopped part way keeps them, so the next session carries on.
- Examples, in different kinds of project:
  - In a clinic's booking app, the product owner says the reminder story is done, the payment spike is dropped and the plan is next. On "approved", both issues close, the plan file reads them Done and Dropped and its Direction reads 1, and one commit holds it all.
  - In a bank's payments service, a developer closed a story in the tracker by hand last week. The next session starts with it on the list as "closed on GitHub", Done, while its epic stays as it was.
  - In a shop's checkout project, the product owner sets the plan to Paused while the team waits for a new payment provider, and marks the item being worked on as Blocked.
- How it meets the capability: this is "sets the order and status of the work as it runs": every status and the direction are what a person said, set in one place and on one yes.

Status: built, in /update-plan. Its first form was the /update-plan session: instructions, checks, one approval, one landing on the plan's branch. Putting the items closed in the tracker on the list came later, so an item's status in the plan file follows its own issue. The same session also adds, moves, renames and rewrites work items; Change the work items (fn-change-work-items), in Turn intents into agent work, holds that part. Not built, or open:
- The session names its tracker: its entries read "closed on GitHub", and it reaches GitHub through the tracker skills. One tool that knows the tracker, so no play names one, is planned.
- Setting a plan to Paused does not land its branch on main and does not write its branch field. Pause a plan and start it again (fn-pause-plan) is not built.
- Nothing sets an item to Now when someone starts it; a person sets it here. Choose which item is worked next (fn-choose-next-item) is not built.

## Inputs / Outputs
- In: the plan's number or a description, and the person's instructions in their own words.
- In: the plan file on the plan's branch, and the plan's issues as the tracker holds them now.
- In: copies of the plan-update and plan-view templates, for every screen and every status the plan knows.
- Out: the running list: each entry with its item, its status before and after, where it lands, any rule it breaks with what works instead, and any override.
- Out, after "approved": the issues closed or reopened in the tracker; the plan file's item statuses, Status and Direction changed as the list says; the agreement check's record; and one commit on the plan's branch whose message names what was asked, each override and what is owed.
- Out, on "rejected" or "abort": nothing written, and the record of the answer.

## Rules & behavior
- A person sets every status and the direction, and nothing rolls up. The reason: "A person sets every status and the plan's direction. Nothing is worked out from the work under an item: no roll-ups."
- An item whose own issue closed goes on the list when the session starts, and lands only on "approved". The reason: "An item's status in a plan file follows its own GitHub issue.", and the person still decides on the whole list.
- A parent never goes on the list because its children closed. The reason: "A parent never changes because its children closed".
- Only the plain word "approved" lands the list, and only the list the person saw. The reason: "What lands is exactly the list the person saw when they approved it."
- A rule break is shown with what works instead, and "do it anyway" lands it, recorded in the commit. The reason: "The principle that a person is never stopped without a choice, and an override is recorded". This is the one way past a gate this session has, and it records what is owed.
- A big change is confirmed before it joins the list. The reason: closing an item with open work under it, or dropping an epic, changes more than one item's meaning, so it "is shown and confirmed before it joins the list".
- The plan's Status and Direction live in the plan file only. The reason: "Status, direction, branch and item kinds are operational: they live in the plan files only, never in the product model's index or pages."
- One commit, and no history in the plan file. The reason: "The plan file keeps no history; git does."
- Nothing is written before "approved", other than the step that gives a plan with no branch its branch. The reason: the person decides once, on the whole list, and the branch step is "the one write a plan session makes before the person approves anything".
- Uncommitted work on any branch stops the session before anything changes. This stops a person with no way past it: in the product owner's words, "a stop on uncommitted work is the person's to clean up". The way past is Give every gate a way past's, in Orchestration.
- Not decided: whether writing the plan's branch field as none when the plan pauses stays owed on the /update-plan session or becomes its own work.

## Acceptance criteria
- Given a plan on its branch, when the product owner finishes one item, drops another, sets the plan's Direction to next and types "approved", then the first issue is closed as completed and the second as not planned, the plan file reads them Done and Dropped with Direction 1, the agreement check reads ok, and one commit is on the plan's branch.
- Given a story whose issue was closed in the tracker while its item is still open, when a session starts, then the list holds it as "closed on GitHub" with Done, its parent is not on the list, and only after "approved" does the plan file read it Done.
- Given an epic with open stories, when the person asks to close it, then the list shows it as big, and it joins only after the person confirms.
- Given an entry that breaks a rule, when the person says "do it anyway" and approves, then it lands and the commit message names the override.
- Given a list, when the person types "rejected", then nothing lands and the session goes on; when they then type "abort", then nothing is written and the session ends on the branch it started on.
- Given a session in which no instruction names the Direction, when it lands, then the Direction is the same as before.

## Out of scope
- Adding, moving, renaming, rewriting or changing the kind of a work item, and a feature found during work. Change the work items (fn-change-work-items) and Add a feature found during work (fn-add-found-feature), in Turn intents into agent work, do them.
- Getting onto the plan's branch and back. Get onto a plan's branch for a session, and come back (fn-go-to-plan-branch) does it.
- Making each approved tracker write once, and picking it up after a stop. Track execution in the team's tracker owns it.
- Setting a landed issue's own item Done at the merge. Merge each change where it lands, on the review's approval and a person's yes (fn-673), in Ship every change the same way, does it.
- Landing a paused plan's branch on main. Ship every change the same way, in Developer tooling, owns it.
- Choosing which item is worked next. Choose which item is worked next (fn-choose-next-item) will do it; it is not built.

## Sources
- The product owner on 2026-11-10: "A person chooses what is delivered next as a slice, sees every plan and where it stands, and sets the order and status of the work as it runs."
- core/components/plays/update-plan/reference/ice.md: "A person sets every status and the plan's direction. Nothing is worked out from the work under an item: no roll-ups.", "What lands is exactly the list the person saw when they approved it.", "The principle that a person is never stopped without a choice, and an override is recorded", "is shown and confirmed before it joins the list", "a stop on uncommitted work is the person's to clean up"
- core/components/plays/update-plan/SKILL.md: "The plan file keeps no history; git does."
- core/components/plays/update-plan/scripts/check_entries.py: "No status or direction is ever added that the draft does not name (no roll-ups)."
- core/components/plays/update-plan/scripts/closed_on_github.py: "Nothing is worked out from the items under it (no roll-ups)."
- core/tools/plan/plan_branch.py: "the one write a plan session makes before the person approves anything"
- docs/adr/064-an-items-status-in-a-plan-follows-its-own-issue-with-no-roll-ups.md: "An item's status in a plan file follows its own GitHub issue.", "A parent never changes because its children closed"
- docs/adr/061-a-plans-branch-is-cut-by-the-play-that-starts-its-work-main-first.md: "whether writing `branch: null` on a pause stays owed under [the /update-plan session], or becomes its own issue."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Status, direction, branch and item kinds are operational: they live in the plan files only, never in the product model's index or pages."
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/fn-change-work-items/feature.md: "The same session also sets each item's status and the direction of the work. Those parts track the work, so Orchestrate agent work through planning owns them."
- The research and drafts for Orchestrate agent work through planning, the page this one replaces and the old page of Manage a plan with /update-plan, as they read on 2026-11-10: "gives instructions in their own words, and approves", "Orchestration only."
