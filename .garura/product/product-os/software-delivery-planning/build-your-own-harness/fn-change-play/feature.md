# Feature: Change a play through its ICE

## What it does
A person changes a play that exists with /edit-play by changing its ICE first and compiling the play again, so the play keeps doing only what its intent says and the change reaches only what it must.
- A change to a play is one of two kinds, and the kind decides the path:
  - an intent change touches what the play decides or guarantees: its goal, a constraint, a failure condition, a scenario, the sub-agents and skills it uses, or its evals. It goes through the play's ICE and /edit-play;
  - a change that alters no guarantee, such as output format, the close's wording or surface prose, is a direct edit to the compiled play. Why it was made goes in the commit and the issue, not in the play.
- It reads the play and its ICE first, and maps every constraint, failure condition, scenario and eval, and which eval covers which. When a play has no separate ICE source, it rebuilds that map from the compiled play.
- It names the change's reach, the smallest set of things the change touches, before it changes anything.
- It changes the ICE first. When that shifts what success or recovery looks like, it generates again only the scenarios and recoveries the change shifts.
- It carries the change only as far as it reaches: the pre-flight checks, the workflow, the evals, the sub-agents and skills (a new sub-agent is audited), and the scripts (new mechanical work goes into a script; a script whose step is gone is deleted).
- It removes every orphan: an eval or a recovery tied to something removed.
- It compiles the play again, computes the fingerprint again, runs the play linter until it is clean, and shows what changed.
- Pinning or unpinning a checkpoint is an intent change of this kind (fn-add-gate).
- When a decision removes what a play was for, the play is not changed: a new one is built with /create-play, and the old one is dropped with an ADR.
- Examples, in different kinds of project:
  - In an insurer's harness repository, the technical lead adds a failure condition to the claims play. /edit-play adds its step eval and its one recovery, computes the fingerprint again, and leaves every other step as it was.
  - In a news site's harness, a developer fixes a typo in a play's brief. It is a direct edit with no change in meaning, and the reason is in the commit.
  - In a bank's harness repository, a constraint is removed from a play's ICE. The eval that pointed to it is removed too, and the linter finds no orphan.
- How it meets the capability: the capability's line asks for building "in a consistent way", and a play changed only through its ICE never drifts from what the team agreed.

Status: built, in /edit-play, with its copy of the play linter. Not built, or open:
- The play linter checks only that a fingerprint is there and is not a placeholder. It does not compare it with the ICE, so a play edited by hand away from its ICE passes. The loop linter does compare. The play checker's rules are Standards'.
- Nothing refuses an edit to a compiled play or its ICE made without /edit-play. The guardrails the install is to lay are to do it, with the run marker of Mark that a play is running, so a guardrail can tell a play's work from a shortcut (fn-mark-play-running).
- It runs only on Garura's source layout, as /create-play does.
- /edit-play is written by hand and has no ICE of its own.

## Inputs / Outputs
- In: the play's compiled `SKILL.md` and its ICE source.
- In: the person's change, in their words.
- In: the agent audit, the workflow shapes and the compiled-play example.
- Out: the changed ICE, the play compiled again with its new fingerprint, the scripts added or deleted, and the play linter's clean report.
- Out: a short summary of which ICE parts changed and which evals, recoveries and sections were added, removed or generated again.

## Rules & behavior
- An intent change goes through the ICE. The reason: "Never hand-edit a compiled `SKILL.md` for an intent change."
- Only wording with no change in meaning is edited directly. The reason: "Pure wording cleanups with no change in meaning are the only safe direct edit."
- Why a direct edit was made is kept outside the play. The reason: "Record why in the commit message and the issue, not in the `SKILL.md`"
- Read before changing. The reason: "You cannot safely edit what you have not read — most bad edits come from changing one thing and missing what depended on it."
- The reach stays small. The reason: "Keep the blast radius minimal — re-derive only what the change reaches; preserve the rest.", and "A play that gets needlessly reshaped on a small edit is a failed edit."
- No orphans are left. The reason: "Leave no orphans: remove every eval and recovery tied to something you deleted, and cover everything you added."
- The play and its ICE stay matched. The reason: "Keep them in lockstep: change the source, then recompile from it.", and "Re-run the linter (`scripts/lint_play.py`), clear every gap, and update the fingerprint (`shasum -a 256`) before declaring the edit done."
- A play whose job is gone is built again, not changed. The reason: "Read the old play only for the parts worth keeping, and build the new one with `/create-play`."
- Not decided: whether the play linter compares a play's fingerprint with its ICE, as the loop linter does.

## Acceptance criteria
- Given a play and a new failure condition, when /edit-play applies it, then the ICE holds it, the play has one new step eval and one new recovery for it, the fingerprint is computed again, and the play linter passes.
- Given a constraint removed from a play's ICE, when the play is compiled again, then no eval or recovery points to it.
- Given a fix of wording with no change in meaning, when it is made, then it is a direct edit to the compiled play, and its reason is in the commit and not in the play.
- Given a change, when /edit-play ends, then every step, eval and script the change does not reach is the same as before.
- Given a compiled play edited by hand away from its ICE, with its old fingerprint kept, when the play linter runs, then it fails the play. This is not built.

## Out of scope
- Building a new play. Build a play from its ICE (fn-build-play) does it.
- The play checker's rules, such as comparing the fingerprint with the ICE. Standards, in Standards, structure, settings and memory, owns them.
- Refusing an edit made without /edit-play. Mark that a play is running, so a guardrail can tell a play's work from a shortcut (fn-mark-play-running) gives the guardrail its marker; Install into a project, in Install and distribute, lays the guardrails.
- The way past a checkpoint whose pin is changed. Give every gate a way past, in Orchestration, owns it.
- Opening and landing the change. Ship every change the same way, in Developer tooling, owns it.

## Sources
- The product owner on 2026-11-11: "You can keep building your harness with your own plays, loops, sub-agents and skills, in a consistent way."
- CLAUDE.md, "Play Pipeline Rules", lines 104-125: "Never hand-edit a compiled `SKILL.md` for an intent change.", "Record why in the commit message and the issue, not in the `SKILL.md`", "Read the old play only for the parts worth keeping, and build the new one with `/create-play`."
- core/components/plays/edit-play/SKILL.md, lines 45, 74-75, 82-83, 145-146, 147, 149-150 and 156-157: "Keep them in lockstep: change the source, then recompile from it.", "You cannot safely edit what you have not read — most bad edits come from changing one thing and missing what depended on it.", "A play that gets needlessly reshaped on a small edit is a failed edit.", "Pure wording cleanups with no change in meaning are the only safe direct edit.", "Keep the blast radius minimal — re-derive only what the change reaches; preserve the rest.", "Leave no orphans: remove every eval and recovery tied to something you deleted, and cover everything you added.", "Re-run the linter (`scripts/lint_play.py`), clear every gap, and update the fingerprint (`shasum -a 256`) before declaring the edit done."
- core/tools/lint-play/lint_play.py, lines 310-317: the fingerprint check, which fails only a missing fingerprint or a placeholder.
- core/components/plays/create-loop/scripts/lint_loop.py, line 180: "The fingerprint must be the sha256 of reference/ice.md as it is now, not just present."
- docs/standards/harness-standard.md, lines 54-55: "The compiled part records a fingerprint of its ICE, so the two never drift apart unseen"
- The stock-take of this intent (2026-11-11), sections 1.2, 1.5 and 2.1.
