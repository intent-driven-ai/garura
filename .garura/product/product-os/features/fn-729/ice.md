## Intent
- Goal: Anyone sees every plan of the project at once: one card for each plan, in the order of the plan numbers, with its direction, number and title, its Status, Branch and Waits on, and each epic with its Progress, printed from the plan files alone by one template, with each Status and Direction exactly as a person set it.
- Limit: It reads only the plan files, and git for a plan's branch; it never reads the tracker or the product model, and no model call makes the cards.
- Limit: It writes no plan file, no issue and no branch.
- Limit: A plan file it cannot read, or one with a status, a plan status or a direction the template does not know, stops it with the file named, and no card is shown.
- Fails if: A plan in the plans folder is missing from the cards, or is there twice.
- Fails if: A card shows a Status or a Direction that is not the one in the plan file, or one worked out from the work under the plan.
- Fails if: Two runs on the same plan files print differently, or a plan file changed.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the plan files in the plans folder, the plan-view template's marks and layout, and git's branches for a plan whose file names none.
- Never read: any memory file by its path, any ICE page, and any plan's evals folder.
- Persona: the product owner, who looks at where all the work stands; and the developer, a person or an AI agent who builds the code, who picks the work up after time away.
- Scope: In: the cards, the legend, the plain line when there are no plans, the stop on a plan file the template does not know, and the check of the print. Out: the graph against main, one plan as a tree, setting statuses and the direction, working out the plans a plan waits on, and the run's closing report.

## Expectation
- Scenario: A clinic's booking app has three plans. The product owner runs /list-plans and sees three cards in number order: online check-in, ⏵, In Progress on its branch, its epic at 4 done and 3 open; reminders, ⏵⏵⏵, Paused, on main; and payments, with no direction line, Not Started, waiting on reminders. Later a fourth plan file is added with the status Started; the next run stops, names that file and shows no card.
- Done means: Someone other than the one who ran it reads the plan files, git and the printed cards, and finds every plan once and in order, each Status and Direction as its file holds it, each Branch as the file and git say, the same cards on a second print, no plan file changed, and, for the file with the unknown status, no card and the file named.
