# Feature: See every plan and where it stands

## What it does
Anyone, a person or an agent, runs /list-plans and sees every plan of the project at once, from the plan files alone: one card for each plan, in the order of the plan numbers, so no one has to read every issue to know where the work stands.
- A legend of the direction marks comes first: ⏵ next, ⏵⏵ next in line, ⏵⏵⏵ later.
- Each card opens with a heavy rule, then the plan's number and its business intent's title, then its direction mark on a line of its own. A plan with no direction has no such line.
- Then three rows, each with its label at the left edge:
  - Status: the plan's own status as a person set it in the plan file: Not Started, In Progress, Paused, Done or Dropped.
  - Branch: the plan's branch, or main when it has none. The branch is the one the plan file names, or the plan's branch name when git has that branch.
  - Waits on: each plan this plan needs, with its title. The row is always there, and blank when there is none.
- Then each epic of the plan: its status mark, number and title, and a Progress row with how many items under it are done and how many are open, and how many were dropped when there are any. An item outside every epic is not on the card.
- The Status and the Direction are read from the plan file as a person set them. Nothing is worked out from the work under the plan: a plan whose items are all done still reads the status a person gave it.
- The plan tool prints the cards from the plan-view template, with no tracker read and no model call. A check then rebuilds what the cards must hold from the plan files, and proves that every plan is there once and in order, that each Status and Direction is as set, that two prints are the same, and that no plan file changed.
- It is read only. It writes no plan file, no issue and no branch, and it runs on any branch.
- An empty plans folder prints one plain line that there are no plans.
- Examples, in different kinds of project:
  - In a clinic's booking app, the product owner sees two cards: online check-in, ⏵, In Progress on its own branch, with its epic at 4 done and 3 open; and reminders, ⏵⏵⏵, Paused, on main.
  - In a bank's payments service, a developer back from leave sees that the plan for new statements waits on the plan for the account data feed, so the feed's work comes first.
  - In a team's planning tool, a new team member runs it on the first day and reads the plain line that there are no plans yet.
- How it meets the capability: this is "sees every plan and where it stands": the whole of the work is on one screen, as a person set it.

Status: built, in /list-plans and the plan tool's list. Its first form listed every plan, from the plan files alone. The card came later: each plan as a card with its direction, status, branch, waits on and each epic's progress. Not built, or open:
- The run ends on its run summary, not on the cards, so the person is left looking at the summary.
- Waits on is printed as the plan file holds it. Nothing works it out from the plan's parts; Work out the plans a plan waits on (fn-work-out-waits-on) is not built.
- The plan files that exist today are for older business intents, and the reorganisation of the business intents deletes them. No plan exists yet for the current intents.

## Inputs / Outputs
- In: every plan file in the plans folder, `.garura/project/plans/<id>.yaml`: its id, title, status, direction, branch, needs_plans and tree.
- In: git, to find a plan's branch when its file names none.
- In: a copy of the plan-view template, which holds every mark and line of the cards.
- Out: the cards, shown to the person as the tool printed them, with one plain line before them: how many plans, and which view.
- Out: the check's record: every plan listed once and in order, the template used, each Status and Direction as set, the same print twice, and no plan file changed.

## Rules & behavior
- Only the plan files, and git for a plan's branch. The reason: "The plan files are a cache: they exist so that no one has to read every issue to know where the work stands."
- No model call, and one template for every mark and line. The reason: "the same files print the same way every time", and "Every mark and line comes from the `plan-view.md` template".
- Each Status and Direction is shown as a person set it. The reason: the plan's status is "Set by a person, never worked out from the work.", and the tool reads "Status and Direction are read from the plan file as a person set them, never worked out from the work."
- Direction is a direction, not a rank. The reason: "It is directional, not a ranking: several plans may share a level."
- Every plan is on the list once, in the order of the plan numbers. The reason: a plan missing from the list is work no one sees, and the play fails when "A plan in the plans folder is missing from the output, or is in it twice."
- A plan file that cannot be read, or that holds a status, a plan status or a direction the template does not know, stops the play with the file named, and no card is shown. The reason: "A part of the list is never shown."
  - This stops a person with no way past it: a person fixes the plan file and runs the view again. The way past is Give every gate a way past's, in Orchestration.
- Any argument other than --graph stops the play. The reason: "Any other mode stops the play; it is never guessed."
- Read only. The reason: a view that changed what it shows could not be trusted, and "the play writes no plan file, no issue and no branch".
- Not decided: whether a plan's Waits on is worked out from its parts' needs, set by a person, or dropped.

## Acceptance criteria
- Given a plans folder with three plans, when /list-plans runs, then each of the three has one card, in the order of the plan numbers, with its Status, Branch and Waits on rows and each epic with its Progress.
- Given a plan whose file reads Paused with direction 1 and whose items are all Done, when /list-plans runs, then its card reads Paused with the ⏵ mark.
- Given a plan with no direction, when /list-plans runs, then its card has no direction line.
- Given a plans folder with no plan, when /list-plans runs, then it prints the plain line that there are no plans.
- Given a plan file with a status the template does not know, when /list-plans runs, then the play stops, names the file, and shows no card.
- Given any plans folder, when /list-plans runs twice, then the two prints are the same and no plan file changed.

## Out of scope
- Each plan's branch against main. See every plan's branch against main (fn-806) does it.
- One plan as a tree. See one plan as a tree (fn-628) does it.
- Setting a plan's status and direction. Set each item's status and the plan's status and direction in one approved session (fn-730) does it.
- Working out the plans a plan waits on. Work out the plans a plan waits on (fn-work-out-waits-on) will do it; it is not built.
- The run summary every play prints at its end, and how plays are built. Standards, structure, settings and memory owns them.
- What a plan file holds, as the ontology's Plan kind says. Product model owns it.
- The issues in the tracker. Track execution in the team's tracker owns them.

## Sources
- The product owner on 2026-11-10: "A person chooses what is delivered next as a slice, sees every plan and where it stands, and sets the order and status of the work as it runs."
- core/components/plays/list-plans/reference/ice.md: "The plan files are a cache: they exist so that no one has to read every issue to know where the work stands.", "A part of the list is never shown.", "Any other mode stops the play; it is never guessed.", "the play writes no plan file, no issue and no branch", "A plan in the plans folder is missing from the output, or is in it twice."
- core/tools/plan/README.md: "the same files print the same way every time", "Every mark and line comes from the `plan-view.md` template"
- core/tools/plan/plan.py: "Status and Direction are read from the plan file as a person set them, never worked out from the work."
- standards/templates/plan-view.md, in Phoenix memory: "Set by a person, never worked out from the work.", "It is directional, not a ranking: several plans may share a level."
- The research and drafts for Orchestrate agent work through planning, the page this one replaces as it read on 2026-11-10: "Print one list of every plan from the plan files"
