# Feature: Open each change where it will land

## What it does
A person names the change, and it is opened where it will land: its issue is found or filed, its branch is cut from the branch it will merge into, and the issue's working folder is made, so every play that runs after it starts from a known issue on the right branch.
- What a person names: an issue number, a short description, or `plan <id>`. "Nothing typed starts nothing": with nothing typed, the run stops with one line and starts nothing. The change is never taken from the branch the session is on.
- The issue: a number names it. A description is matched to an open issue, of any kind, a bug, a chore, a story or a feature, or a new issue is filed. Before a new issue is filed, its title is checked to be present, at least 15 characters long and tagged with its kind, such as [BUG] or [FEAT], and its description to be complete. A failed check stops the run, and nothing is filed.
- Where it will land is read from the plan files, never guessed. They are read from the latest main in git, and from the plan's own branch when it has one, never from the copy the session has open, because a plan session writes on the plan's branch first.
  - A one-off change, for an issue in no plan: a branch from an up-to-date main, `feature/<issue>-<slug>`.
  - An issue in a plan: a branch from the plan's branch, `plan/<id>/<issue>-<slug>` from `plan/<id>/base`. The latest main is merged into the plan's branch first, so a running plan never falls behind main. A merge conflict stops the run for a person.
  - The first issue of a plan whose work has not started: the plan's branch is cut first, main first. Main's plan file is set to In Progress with the branch named, committed and pushed on main, and the plan's branch is cut from that commit, through the one script that makes every cut.
  - An issue in a plan that main marks Done or Dropped, such as a bug found after the plan closed: a one-off change from main, with the closed plan named in the record. A closed plan's branch is never cut again.
  - A plan's branch that is gone on the code host but still on the machine: deleted and cut fresh only when every commit on it is on main; otherwise the run stops and names the commits that are not.
- `plan <id>` on its own starts a plan's work: main's plan file first, then the plan's branch, and it stops. No issue is looked up, no issue's branch is cut, and nothing is committed on the plan's branch.
- A second checkout of the repository in its own folder, a worktree, is set up only when the project's setting asks for it.
- The working folder is the issue's own folder in short-term memory, made with its five parts: specs, evidence, checkpoint, context and review. The start's own record, the issue, the branch and what was typed, is committed on the new branch, so the change opens with a clean tree.
- Running it again for the same issue picks up the issue, the branch and the folder that exist; it never makes a second one.
- A loop opens one change for its whole run in the same way, and the plays it runs open nothing of their own.
- Examples, in different kinds of project:
  - In a shop's checkout project, a developer types a short description of a payment bug. The open issue that matches is found, and a branch is cut from the latest main.
  - In a bank's payments service whose plan for new statements is running, a developer starts the plan's third story. Main is merged into the plan's branch, and the story's branch is cut from it.
  - In a team's planning tool, the product owner types `plan <id>` to start a plan's work. Main's plan file reads In Progress, and the plan's branch is cut from that commit, with no story branch yet.
- How it meets the capability: this is the opening in "Every change goes from opening to merge through the same steps". Every change starts in the same way, of any kind and for any issue, on the branch it will merge into.

Status: built, in /start-change. Its first form, which cut a plan's branch and each issue's branch from it, was #731 (closed). The cut of a plan's branch main first came after it (ADR 061), and `plan <id>` with the typed change after that (#989, closed). Not built:
- One run opens one issue. Several ready issues in one change are Land several ready issues in one change (fn-land-several-issues), planned (#976).
- Running several changes at once, each in its own worktree with its own chain of plays, is planned (#501).

## Inputs / Outputs
- In: what the person typed: an issue number with an optional note, a short description, or `plan <id>`.
- In: the open issues in the tracker, for a description.
- In: the plan files, read from the latest main and from each plan's branch on the code host.
- In: the project's setting for a worktree.
- Out: the issue, found or filed, and its record.
- Out: the change's branch, cut from where it will land and pushed, and, for a plan whose work starts, the plan's branch and main's plan file set to In Progress.
- Out: the issue's working folder, with the start's record committed on the branch.
- Out: a worktree, only when the setting asks for it.

## Rules & behavior
- The change is what the person typed. The reason: a change taken from the branch the session is on starts work the person did not name, and "Nothing typed starts nothing".
- Every change has an issue before any branch. The reason: each commit and the pull request name the issue, and the merge closes it.
- A new issue's title and description are checked before it is filed, whatever the settings say. The reason: the checkpoint before a new issue is off by setting, and this check carries what the person was checking.
- An issue in a plan works on a branch cut from its plan's branch; a one-off change still branches from main. The reason: a plan's work stays together while it runs, and a one-off change lands on main.
- The plan is read from git, from main and from the plan's own branch, never from the open copy. The reason: an issue added to the plan on main, or by a plan session on the plan's branch, is in the plan before the session's copy shows it.
- Main is merged into a plan's branch before each issue's branch is cut from it. The reason: without it, a running plan falls behind main between its issues.
- A plan's branch is cut main first, through one script. The reason: "Every cut goes through one script", "so every cut is made the same way, whichever play starts the work", and main's plan file says the plan is In Progress before its branch exists.
- A closed plan's branch is never cut again. The reason: a bug found after a plan closed is new work, and it lands on main.
- A local branch with commits found nowhere else is never deleted. The reason: deleting it loses work.
- Running it again resumes. The reason: a second issue or branch for the same work splits it.

## Acceptance criteria
- Given a plan with two issues and no plan's branch yet, when a developer opens the first issue, then main's plan file reads In Progress with the plan's branch named, the plan's branch equals the main commit it was cut from, and the issue's branch is cut from the plan's branch.
- Given a plan whose branch exists, when a developer opens its second issue, then the plan's branch holds the latest main and the second issue's branch is cut from it.
- Given an issue in no plan, when a developer opens it, then its branch is cut from the latest main and named for the issue.
- Given nothing typed, when the play runs, then it stops with one line and no issue, branch or folder is made.
- Given a description of new work whose title would be 10 characters, when no issue matches, then the run stops before any issue is filed.
- Given an issue that is already open on its branch, when it is opened again, then no second issue or branch is made and the session is on the branch that exists.

## Out of scope
- Committing, raising and merging the change. Commit each change by concern, with its issue named and nothing sensitive (fn-commit-by-concern), Raise each change for review against where it lands (fn-raise-change) and Merge each change where it lands, on the review's approval and a person's yes (fn-673) do them.
- Opening several issues as one change. Land several ready issues in one change (fn-land-several-issues) does it.
- Making and changing a plan and its items. Turn intents into agent work, in Product → Spec, and Orchestration own them.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-8-capability-1/page-approvals.md: "Ship every change the same way: Every change goes from opening to merge through the same steps, with a self-review, an outside review and a person's yes.", "yes, record it with self-review dropped"
- core/components/plays/start-change/SKILL.md: "It is never locked to a plan", "the change is what the person typed", "a merge conflict exits 1 and halts for a person", "the workspace opens with a clean tree and its own record"
- core/components/plays/start-change/reference/ice.md: "Nothing typed starts nothing", "a closed plan's branch is never cut", "An issue in a plan works on `plan/<plan-id>/<issue>-<slug>`, cut from its plan's branch `plan/<plan-id>/base`", "Running it again for the same issue resumes the existing context"
- core/components/plays/start-change/scripts/validate_issue.py: "title present and >= 15 characters", "title carries a type tag: [ENH] [BUG] [FEAT] [DOCS] [TASK]", "a work description exists"
- core/components/loops/_shared/loop-run.md: "one issue, one branch for the whole loop"
- standards/rules/loop-contract.md, in Phoenix memory: "The loop opens and lands the change."
- docs/adr/060-a-plans-branch-merges-into-main-when-the-plan-pauses.md: "A one-off fix outside any plan still branches from main."
- docs/adr/061-a-plans-branch-is-cut-by-the-play-that-starts-its-work-main-first.md: "Every cut goes through one script", "so every cut is made the same way, whichever play starts the work."
- The page this one replaces, .garura/product/product-os/features/fn-731/feature.md as it read on 2026-11-10: "Every issue in a plan works on a branch cut from its plan's branch.", "A one-off fix outside any plan still branches from main."
- GitHub #731 (closed): "start-change cuts a plan's branch, and each issue's branch from it"
- GitHub #989 (closed): "start-change starts a plan on its own: it cuts the plan's branch from main, with no story branch"
- GitHub #501 (open): "Self-contained play chains + parallel worktree autonomy"
- GitHub #976 (open): "Several ready issues land in one change: one branch, one pull request, one review"
