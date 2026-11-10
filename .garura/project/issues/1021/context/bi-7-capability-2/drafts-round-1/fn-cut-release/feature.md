# Feature: Cut a Garura release, with notes on what it changes

## What it does
When Garura's newest work is ready for teams, the product owner of Garura cuts a release from it: a fixed, named version, tagged and published with notes in plain words on what it set out to do, what it changes and what is known to be wrong, so an upgrade has a version to move to and every team can read what that version changes before it takes it.
- A release is a fixed, named version of Garura, such as v3.0.0. Two teams that install the same release a week apart get the same Garura, and a bug report can name it.
- What each release holds, for the teams that take it:
  - its version, tagged from Garura's newest work;
  - its notes, written for the teams that install it: what it set out to do, what it delivered, the known issues at the tag, and what a team must do when it upgrades, such as a move of its product model;
  - its published release, so the one-step install and an upgrade can find it.
- The notes are what Move the project to a new version, seeing first what it changes (fn-upgrade-in-one-step) shows before anything changes.
- Once Phoenix memory has versions of its own, a release also names the Phoenix memory version it goes with. How Phoenix memory is versioned is Memory's.
- Examples, in different kinds of project:
  - A team on a bank's payments service reads the notes of the release it is offered and sees that its product model will move, before it says yes.
  - A team that builds its own harness reads in the notes that two plays it uses were renamed.
  - A recipe app's repository installs the latest release with no version named and gets the one whose notes it can read.
- How it meets the capability: "knowing what changes" rests on each version saying what it changes. The product owner agreed that "Garura's own releases and their notes sit here".

Status: built in part, by hand:
- Each release has a hand-written entry in `CHANGELOG.md`: what it set out to do, what it delivered, and "Known issues at the tag". Each tag that starts with `v` makes a GitHub release with notes GitHub writes from the merged changes (`.github/workflows/release.yml`).
- The last release, v3.0.0 of 7 October 2026, was cut through a release issue (#591, closed): its blockers closed, a changelog entry "in plain language", a tag from main, a GitHub release "marked Latest", and "A fresh install with no version given installs v3.0.0".
- Cutting a release is by hand: "Cutting a release stays a manual step." (#568).
- Not built: notes for Garura's newest work. The changelog has no entry after v3.0.0, and main is 1,790 commits past it, so a team that asks for the newest work gets no notes, and a team that takes the default gets a release that has neither the memory system nor the current plays.
- Not built: a line in the notes for what a team must do on an upgrade, such as a move of its model.
- Not decided: how often a release is cut, and who writes its notes. The lean is by hand, when the product owner decides, with the notes drafted from the work since the last release and approved by him.

## Inputs / Outputs
- In: Garura's newest work, and the work merged since the last release.
- In: the agreed blockers of the release, the known issues at the tag, and any move a team must make on an upgrade.
- In: the product owner's yes to the notes and to cutting the release.
- Out: the tag, the published release and its notes, which the one-step install and an upgrade find.
- Out: the changelog entry for the release, in plain words.

## Rules & behavior
- A fixed, named version. The reason: #568 was filed because "Two people who install a week apart get different Garura.", so nobody could name the version they had.
- Every release has notes in plain words. The reason: a team knows what an upgrade changes only when the version says so; #591 asked for an entry "that says what changed since v2.0.0, in plain language".
- The notes say what a team must do. The reason: a move of the model or a renamed play changes what the team runs, and the notes are what it reads before its yes.
- Cut by hand, on the product owner's yes. The reason: "Cutting a release stays a manual step.", and #568 kept releases on every merge out of its scope.
- A release waits on its blockers. The issues it must not go out without are agreed first, and each is closed before the tag. The reason: #591 was done only when "The blocker list is agreed and every issue on it is closed."
- A fresh install gets it. The reason: #591 counted the release done only when "A fresh install with no version given installs v3.0.0".
- A release is prepared with stricter checks. The reason: Garura's branch rule has a branch for "Release preparation", where "Quality gates elevated to must-have".
- Not decided: how often a release is cut. While the one-step install gives the latest release by default, a release left far behind gives every new team an old Garura, as v3.0.0 does today.

## Acceptance criteria
- Given a release cut, when a team reads its notes, then they say what it set out to do, what it delivered, the known issues at the tag and what a team must do on an upgrade.
- Given a release published, when the one-step install runs with no version named, then it installs that release, and the project records it.
- Given an upgrade to a release, when the upgrade shows what changes, then the notes of that release, and of each release between, are shown. This is not built.
- Given Garura's newest work with no release, when a team asks for it, then the upgrade says that version has no notes. This is not built.

## Out of scope
- Showing the notes during an upgrade. Move the project to a new version, seeing first what it changes (fn-upgrade-in-one-step) does it.
- Which version the one-step install gives by default. Install Garura in one step, with a record of what it laid, in Install into a project, holds it.
- Phoenix memory's own versions and notes. Memory, in Standards, structure, settings and memory, owns them.
- Releasing a team's own product to its users. Validation → Run owns it.

## Sources
- The product owner on 2026-11-10, in .garura/project/issues/1021/context/bi-7-capability-2/page-approvals.md: "Garura's own releases and their notes sit here", "A project moves to a new version knowing what changes"
- CHANGELOG.md: "Known issues at the tag:", "What it set out to do:", "What it delivered:"
- .github/workflows/release.yml: "generate_release_notes: true"
- GitHub #568 (closed): "Two people who install a week apart get different Garura.", "Cutting a release stays a manual step.", "Set up automatic releases on every merge."
- GitHub #591 (closed): "The blocker list is agreed and every issue on it is closed.", "that says what changed since v2.0.0, in plain language", "marked Latest", "A fresh install with no version given installs v3.0.0"
- GitHub #921 (open): "Each Phoenix memory release has a version that matches the Garura release it goes with, and its own release notes"
- standards/rules/git.md, in Phoenix memory: "Release preparation", "Quality gates elevated to must-have"
- The release facts: git tags v0.9.0, v2.0.0 and v3.0.0, v3.0.0 of 2026-10-07 and the last entry in CHANGELOG.md, and `git rev-list --count v3.0.0..main` read 1790 on 2026-11-10.
- The stock-take of the run after Validation, .garura/project/issues/1021/context/bi-5-inventory/inventory.md, section 13: "Garura's own releases"
