# Feature: Know what comes next at the end of every run

## What it does
At the end of every play and every loop, the run's closing report names the one command to run next, with why, from one map, or prints no Next line when the map names none; so a person always knows what comes next, and no second list of work can disagree with the plan.
- The line names one command and why. For /shape-slice the command is /shape-plan, and the why reads "the slice is shaped; make its plan, epic and stories".
- The map is one file, the Next-line map, kept in memory. Each play's entry names its successor and why, or no command. The shared close of every play loads the map through the template sub-agent and prints the line. A loop closes like a play and prints its line the same way.
- Where the map names no command, the close leaves the line out. The person picks the next piece of work from the plan, or from /list-focus-issues, which lists the open issues worth attention. No play recommends what to do across the plans.
- What the map routes today, play by play:
  - The Discovery plays hand on in order, and the Discovery loop and /discover-capabilities hand to /shape-slice.
  - /shape-slice hands to /shape-plan, and /shape-plan to /shape-eval. /shape-eval names no command, because the build that would come next is not built.
  - The change plays hand on in order: /commit-change to /propose-change, /propose-change to /check-change, and /check-change to /merge-change. /merge-change names no command: the plan shows what comes next.
  - /list-plans, /show-plan, /update-plan, /list-focus-issues and /record-decision name no command.
- A check of every compiled play fails a play a person can run that is neither in the map nor named as exempt, or whose close does not print the line. The plays that build, change, install and remove Garura's own parts are exempt.
- Examples, in different kinds of project:
  - In a shop's checkout project, /shape-slice ends with the line that names /shape-plan, so the product owner knows to make the plan's work items next.
  - In a clinic's booking app, a story's change is merged and the close prints no Next line; the developer runs /show-plan to pick the next story from the plan.
  - In a city's bus timetable site, the Discovery loop ends naming /shape-slice for one of the site's business intents.
- How it meets the capability: the order of the work stays the plan's, and every run still says what comes next. In the intent's words: "A person always knows what's happening and what's next."

Status: built, in the shared close of every play, the Next-line map, and the play check that fails a play missing from the map. Its present form came with ADR 051 (the /next play is dropped; the plan is the work list), which deleted the play that used to recommend the next action. Not built, or open:
- The map still names the old build plays, /build-epic, /validate-epic, /release-epic and /release-increment. They are marked stale and kept out of every install (#855, the old-chain plays marked stale, closed), so nothing a project has routes into them.
- /shape-eval names nothing next, because the build is not built (#819, agents design, build, test and check an epic, closed as not planned).
- /shape-slice and /shape-plan, which the map routes to, must not run until the Agent-work tool lands (#1023, open).
- No view shows what comes next across every business intent. Choose which item is worked next (fn-choose-next-item) is not built.

## Inputs / Outputs
- In: the name of the play or loop that is closing.
- In: a copy of the Next-line map, loaded by the template sub-agent.
- Out: the Next line in the closing report: the command and why, or no line when the map names no command.
- Out, from the play check: a failure that names a play a person can run that is not in the map and not exempt, or whose close does not print the line.

## Rules & behavior
- One map, and one place for it. The reason: "This file is the one place that mapping lives."
- No line when the map names none. The reason: "When the map names none, the play prints no Next line.", and "The person picks the next piece of work from the plan, or from `/list-focus-issues`."
- No recommender. The reason: "There is one work list, the plan; no second recommender can disagree with it."
- A view of what comes next, if one is needed, reads the plan files. The reason: "It is built when it is needed, from its own ICE."
- Every play a person can run is in the map, or exempt. The reason: "`lint_play.py` fails any user-invocable compiled play that is neither listed here nor in `meta_exempt`."
- A loop closes like a play. The reason: the map covers "every loop, which closes like a play (ADR 029)".
- The line is printed by the shared close, never worded by the play. The reason: the close resolves "this play in the Next-line map" and renders the line from it.

## Acceptance criteria
- Given /shape-slice closes, when its report is printed, then its Next line names /shape-plan with its why.
- Given /merge-change closes, when its report is printed, then it has no Next line.
- Given a new play a person can run with no entry in the map, when the play check runs on it, then it fails and names the play.
- Given the Discovery loop closes, when its report is printed, then its Next line names /shape-slice.
- Given a play whose map entry has no command, when it closes, then the report has no Next line and names no recommender.

## Out of scope
- Choosing which item is worked next. Choose which item is worked next (fn-choose-next-item) will do it; it is not built.
- The rest of the closing report, and how plays and loops are built and checked. Standards, structure, settings and memory owns them.
- The open issues worth attention, /list-focus-issues. Track execution in the team's tracker owns it.
- The loops and the order in which they run their plays. Run plays as loops, in Orchestration, owns them.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "A person chooses what is delivered next as a slice, sees every plan and where it stands, and sets the order and status of the work as it runs."
- .garura/product/product-os/intents/bi-9.md: "A person always knows what's happening and what's next."
- standards/rules/pipeline-next.md, in Phoenix memory: "This file is the one place that mapping lives.", "`lint_play.py` fails any user-invocable compiled play that is neither listed here nor in `meta_exempt`.", "every loop, which closes like a play (ADR 029)", "the slice is shaped; make its plan, epic and stories"
- core/components/plays/_shared/play-close.md: "this play in the Next-line map"
- core/components/loops/complete-discovery/SKILL.md: "its Next line comes from the Next-line map"
- core/tools/lint-play/lint_play.py: "unless it is meta_exempt"
- docs/adr/051-the-next-play-is-dropped-the-plan-is-the-work-list.md: "When the map names none, the play prints no Next line.", "The person picks the next piece of work from the plan, or from `/list-focus-issues`.", "There is one work list, the plan; no second recommender can disagree with it.", "It is built when it is needed, from its own ICE."
- GitHub #855 (closed): "Mark the twelve old-chain plays and their skills stale, and keep stale parts out of every install"
- GitHub #819 (closed): "After /shape-slice, agents design, build, test and check an epic until it is delivered"
- GitHub #1023 (open): "Until this lands, `/shape-slice`, `/shape-plan` and `/shape-eval` read an intent's issue from the wrong repo, so they must not run and no plan is rebuilt."
