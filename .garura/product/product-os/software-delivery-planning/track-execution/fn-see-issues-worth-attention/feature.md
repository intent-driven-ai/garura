# Feature: See the issues worth attention now

## What it does
When a person asks what to focus on, /list-focus-issues reads the issues of the work tracker, keeps the ones that one of three fixed modes asks for, and shows at most ten, each with its number, its title, a plain reason built from what selected it, its kind and, only where a fixed table names one, the play to run for it, so a long list of issues is cut to a workable few, the same way every time.
- It knows three fixed modes, and no others:
  - today, the default: open issues a person could pick up now, not blocked, and unassigned or assigned to the one who runs it.
  - review: open work already in flight, assigned, with a linked branch or pull request, or untouched for 14 days or more.
  - recent: issues closed in the last 7 days.
- A mode it does not know stops the run with no list; it never guesses one.
- The order is fixed. In today, the person's own issues come first, then the most recently touched. In review, the stalest come first. In recent, the most recently closed come first. The issue number breaks a tie.
- At most ten are shown. The rest are counted, and the count is shown, never the issues.
- The reason on each entry is built from the very signals that selected it, such as unassigned, not blocked, and how many days ago it was last touched.
- The kind and the play come from a fixed table beside the play, keyed on the issue's labels; the first row that matches wins. Where the table names no play, or no label matches, the entry carries no recommendation at all, and the list says how many such entries it has.
- It is read only. It never writes to an issue, and it never reads the plan files or the product model.
- When a mode matches nothing, it says so and stops. It never tries another mode or widens the window.
- It reads up to 200 issues for each query; a query that fails or is cut short stops the run with no list.
- Six things are out of step with how work is kept today:
  - It reads labels only. Work items now carry no label, so an Epic or a Story reads unlabelled, with no recommendation.
  - It reads blocked from a label. A Blocked status that a person sets in the plan file is not seen, so a blocked item can show in today.
  - Its table recommends the plays grill, refactor and shape. None of them is a play today. The bug fix play, /fix-bug, which the table names for a defect, is a play, but it is built and live only in a full install, and it is not laid in Garura's own repository.
  - In today, an open epic can show as work to pick up, though an epic is never worked directly.
  - It reads only the work tracker the adapter reaches, never the tracker of business intents.
  - The agreed new name, /list-issues, is not applied yet.
- Examples, in different kinds of project:
  - In a recipe app's tracker with 140 open issues, today shows the ten most recently touched unassigned ones that are not blocked, and says how many more matched.
  - In a bank's payments service, review shows first a story that was assigned two weeks ago and is untouched since, as stale.
  - In a harness repository whose work items carry no labels, every entry reads unlabelled with no recommendation, and the list says how many it could not recommend for.
- How it meets the capability: the backlog the agreed line names is, in the tracker, the open work items; this feature is the one view that cuts them down by fixed rules.

Status: built, in /list-focus-issues. Out of step, as above; no issue is filed for it yet. Not built, or open:
- Reading an issue's kind from its type, or from the plan file, in place of its labels.
- A table whose plays all exist.
- The new name /list-issues, one of the renames the product owner agreed for the Orchestrator's plays.

## Inputs / Outputs
- In: the mode: today, review or recent; today when none is given.
- In: the issues of the work tracker, read through the adapter: each one's number, title, address, state, when it was made, touched and closed, its labels and its assignees.
- In: the login of the person who runs it, read through the adapter.
- In: the kind table beside the play.
- Out: the list of at most ten entries, each with its number, title, reason and kind, and a play only where the table names one.
- Out: how many matched, how many are shown, how many more are not listed, and how many carry no recommendation.

## Rules & behavior
- One of three fixed modes, never guessed. The reason: "An unrecognised mode halts the play; it is never guessed or inferred."
- At most ten entries. The reason: "Output is capped at 10 entries."; a long list is not a workable few.
- The same issues and mode give the same list. The reason: "the same captured issue set and the same mode always yield the same ordered, capped list."
- Kind and play come from the fixed table only. The reason: "The play never infers a kind, never invents a play name, and never derives a recommendation by reading the product model."
- Silence beats a wrong answer. The reason: "The cardinal rule: silence beats a wrong answer."; a default offered in place of an answer still reads as advice.
- Read only. The reason: "Read only: the play never creates, edits, closes, comments on, labels, assigns or otherwise writes to any issue"
- No fallback when nothing matches. The reason: "When a mode matches nothing, the play says so plainly and stops."
- The tracker is the one source. The reason: "No backlog, sprint plan, product model, or work queue is consulted, and none is created."
- Blocked is read from labels. The reason, as built: "Blocked is read from the issue's own labels — never inferred."; it was written with the focus play in 2026-09, before ADR 056 took the labels off the epic and the story.
- Not decided: what it reads an issue's kind from, now that work items carry no label: its type, its plan file, or both.
- Not decided: which plays its table names, now that grill, refactor and shape are not plays.

## Acceptance criteria
- Given 25 open issues that today matches, when it runs, then ten are shown in its fixed order, and it says 15 more matched.
- Given the same issues and the same mode, when it runs twice, then the two lists are the same.
- Given an issue with no label, when it is shown, then it reads unlabelled and carries no recommendation, and the count of such entries is shown.
- Given a mode it does not know, when it runs, then it stops with no list.
- Given a run in any mode, when it ends, then no issue in the tracker changed.

## Out of scope
- Seeing every plan, one plan as a tree, and where each stands. Orchestrate agent work through planning, in Orchestration, owns them.
- The order of the work, and what is built next. Orchestrate agent work through planning, in Orchestration, owns them.
- The plays' names, and the rename to /list-issues. Standards, in Standards, structure, settings and memory, owns them.
- Reaching the tracker of business intents and the work tracker through one tool. One tool knows the tracker (fn-one-tool-knows-tracker) does it, and it is not built.

## Sources
- The product owner on 2026-11-10: "Anything that already exists, like managing ADRs and execution tracking, just use what is already built to do that."
- core/components/plays/list-focus-issues/reference/ice.md: "An unrecognised mode halts the play; it is never guessed or inferred.", "Output is capped at 10 entries.", "the same captured issue set and the same mode always yield the same ordered, capped list.", "The play never infers a kind, never invents a play name, and never derives a recommendation by reading the product model.", "The cardinal rule: silence beats a wrong answer.", "A default offered in place of an answer still reads as advice", "Read only: the play never creates, edits, closes, comments on, labels, assigns or otherwise writes to any issue", "When a mode matches nothing, the play says so plainly and stops.", "No backlog, sprint plan, product model, or work queue is consulted, and none is created."
- core/components/plays/list-focus-issues/scripts/select_focus.py: "Blocked is read from the issue's own labels — never inferred.", "STALE_DAYS = 14"
- core/components/plays/list-focus-issues/reference/kind-map.yaml: "command: fix-bug", "command: grill", "command: refactor", "command: shape", "no recommendation (label it to get one)"
- core/components/plays/list-focus-issues/SKILL.md: "a limit high enough to cover the repo (200)"
- core/components/plays/: the plays today, none of them named grill, refactor or shape.
- The history in git: select_focus.py came with the focus play on 2026-09-08; ADR 056 is dated 2026-10-25.
- docs/adr/056-an-epic-and-a-story-are-marked-by-their-issue-type-with-no-label.md: "finds an issue's kind by its labels"
- .garura/user-provided/managing-work.md: "An Epic is never worked directly; its Stories are."
- .garura/product/product-os/software-delivery-planning/fix-defects-test-first/capability.md: "The bug fix play, /fix-bug, is built and live only in a full install.", "It is not laid in Garura's own repository"
- The names agreed with the product owner on 2026-11-03: "/list-issues (was /list-focus-issues)"
