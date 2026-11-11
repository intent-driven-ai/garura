# Feature: See every plan's branch against main

## What it does
Anyone runs /list-plans --graph and sees each plan's branch drawn against main, like a branch graph, with the commits it is ahead of main and behind main, so a person sees at a glance which plan is on which branch and how far each plan is from main.
- main is the first line. Each plan that has a branch is a line under it: the branch, its commits ahead and behind, the plan's number and its business intent's title.
- A plan behind main carries the behind mark, ⚠, because work landed on main that the plan's branch does not hold yet.
- The last line names the plans with no branch: they are on main.
- A plan's branch is the one its plan file names. When the file names none, it is the plan's branch name, `plan/<id>/base`, when git has that branch here or on the remote.
- The counts come from git: the commits on each side between main and the plan's branch. When git cannot be run, or the branch is not there, the counts read ? and no mark is shown.
- It reads the plan files and git, never the tracker and never the product model, and makes no model call. Every mark and line comes from the plan-view template.
- It writes no plan file, no issue and no branch.
- A check counts the commits again with git, and fails the run when a number in the graph differs, or when a plan is missing or listed twice.
- Examples, in different kinds of project:
  - In a shop's checkout project, the technical lead sees the plan for guest checkout 6 ahead and 0 behind, and the plan for gift cards named on main.
  - In a bank's payments service, the plan for new statements reads 3 ahead and 5 behind with the ⚠ mark, so the developer knows main has moved on since the plan's last story started.
  - In a city's bus timetable site, every plan is paused, so the graph is main and one line that names all of them as on main.
- How it meets the capability: this is part of "sees every plan and where it stands": where each plan's work sits in the repository, against main.

Status: built, in /list-plans --graph and the plan tool's graph. It was #806 (see every plan as a graph: which plan is on which branch, compared to main, closed), under #719 (view plans: see every plan, and any one plan as a tree, closed). Not built, or open:
- The run ends on its run summary, not on the graph (#1018, open).
- After a plan pauses and its branch lands on main, its plan file still names the branch until a person sets it to none by hand, because no step writes it; the graph then shows the gone branch with counts of ?. Pause a plan and start it again (fn-pause-plan) is not built.

## Inputs / Outputs
- In: every plan file in the plans folder: its id, title and branch.
- In: git: the branches here and on the remote, and the commits on each side of main.
- In: a copy of the plan-view template.
- Out: the graph, shown to the person as the tool printed it.
- Out: the check's record: every plan listed once, and each count equal to the count git gives.

## Rules & behavior
- The counts come from git, never from the plan file. The reason: only git knows the commits, and the play fails when "A number of commits ahead or behind in the graph does not come from git."
- When git cannot tell, the counts read ?, never a guess. The reason: a guessed count would show a plan as level with main when it is not; the tool says that "the graph's counts read ?".
- A plan behind main carries the mark. The reason: "A plan behind main has the behind mark.", because without main's new work "a running plan falls behind main between its issues".
- A plan with no branch is named as on main. The reason: its work, if any, already sits on main: "When the plan pauses, its branch merges into main through the change plays".
- The branch is the one the file names, else the plan's branch name when git has it. The reason: the tool reads "the one its file names, else plan/<id>/base when git has it", so a plan cut before its file was read still shows.
- It does not show where a branch was cut from, or where it goes back to. The reason: "the plan files do not hold them".
- Read only. The reason: a view that changed what it shows could not be trusted, and "the play writes no plan file, no issue and no branch".
- A plan file the template does not know stops the graph too, with the file named. This stops a person with no way past it: a person fixes the file. The way past is Give every gate a way past's, in Orchestration.

## Acceptance criteria
- Given a test repository with one plan on a branch two commits ahead of main and one behind, and one plan with no branch, when /list-plans --graph runs, then the first reads 2 ahead and 1 behind with the ⚠ mark, and the second is named on main.
- Given a plan whose branch holds every commit of main, when the graph runs, then it reads 0 behind with no mark.
- Given a plan file that names a branch git does not have, when the graph runs, then its counts read ? and it carries no mark.
- Given any plans folder, when the graph runs, then every count equals the count git gives, every plan is listed once, and no plan file changed.

## Out of scope
- The cards of every plan. See every plan and where it stands (fn-729) does it.
- Bringing main into a plan's branch, cutting a plan's branch and landing it on main. Ship every change the same way, in Developer tooling, owns them.
- Writing the plan file's branch field when a plan pauses. Pause a plan and start it again (fn-pause-plan) will do it; it is not built.
- How plays are built, and the run summary they end on. Standards, structure, settings and memory owns them.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "A person chooses what is delivered next as a slice, sees every plan and where it stands, and sets the order and status of the work as it runs."
- core/components/plays/list-plans/reference/ice.md: "A number of commits ahead or behind in the graph does not come from git.", "the play writes no plan file, no issue and no branch"
- core/tools/plan/plan.py: "the graph's counts read ?", "the one its file names, else plan/<id>/base when git has it"
- standards/templates/plan-view.md, in Phoenix memory: "A plan behind main has the behind mark.", "they are on main"
- .garura/product/product-os/features/fn-731/feature.md: "a running plan falls behind main between its issues"
- docs/adr/060-a-plans-branch-merges-into-main-when-the-plan-pauses.md: "When the plan pauses, its branch merges into main through the change plays"
- .garura/project/issues/1021/context/bi-9-capability-1/research.md, the page this one replaces as it read on 2026-11-10: "the plan files do not hold them"
- GitHub #806 (closed): "See every plan as a graph: which plan is on which branch, compared to main"
- GitHub #719 (closed): "View plans: see every plan, and any one plan as a tree"
- GitHub #1018 (open): "/list-plans ends on a run summary instead of the plans"
