# Self-review: #1001 and #1002 (one change)

Branch: plan/717/1001-update-plan-session-folder-and-model
Compared with: plan/717/base (the PR base)
Rules used: ~/.phoenix/core/memory/standards/rules/self-review.md (the base rules, no project override)
Design: .garura/project/issues/1001/specs/design.md (approved 2026-10-31)

This review is a checklist for the reader. It does not approve or reject the change.

## What the change does, in plain words

#1001 (an /update-plan session leaves files behind): the session now keeps everything it makes
in one session folder from the very start. When the plan is known, the folder moves under the
plan's number. At the close the folder is removed after a landing, an abort, a stop on
uncommitted work, or when no plan was found. A landing that stopped part way keeps its folder so
the next session can carry on.

#1002 (a session cannot reach the product model): when the person's words name a feature, the
session now finds it, makes clean copies of its ICE and its capability's ICE with no "Fails if"
lines, and has the story writer draft the story from them. A check refuses any story text with
a "Fails if" line. The added item records `represents`. "Find this story in the model" gets a
plain answer and no list entry. A feature with no ready ICE gets a story in the person's words,
and the list says so.

## Scope checks

- Matches the issue: pass. All 26 changed files serve the two bugs: the session-folder scripts
  and play text (#1001), the feature lookup, the story writer mode, the list screens and the
  plan-file write (#1002), and the play's ICE and recompiled play for both.
- No scope creep: pass. The only files outside the two bugs are the plan 717 upkeep (the two
  items marked Done, as the plan rules ask) and the run records under the issue's own folder.
- Reasonable size: pass, with a note. About 2,700 lines added, but roughly 1,470 of that are new
  stamped copies of two shared scripts (plan_common.py in two new places, check_ice_workable.py
  in one). The hand-written part is about 1,200 lines, split into clear pieces (scripts, tests,
  play text, ICE).
- No stray artifacts: pass. No debug prints (the print calls are the scripts' JSON output), no
  commented-out blocks, no compiled Python files committed. The run records under
  .garura/project/issues/1001/context/ are the normal record of the change plays.
- Known and recorded, not a finding: a story added this way gets no line in the epic's
  feature-to-story map (design, "Out of scope").

## Quality checks

- Tests present: pass. 64 tests in the play's scripts folder ran and all passed. New tests cover
  the session folder (adopt, clear after a landing, clear after no plan, keep after a part-way
  landing), the feature lookup, the "no guessing" question, the clean copy with no "Fails if"
  lines, the refused story, the model screen, the "says where the text comes from" note, and
  `represents` on the plan file.
- Stamped copies in step: pass. The two shared scripts are byte-for-byte equal in every place
  they live (three copies of one, four of the other; checked by comparing checksums), and the lint rule's shared-scripts list now names
  them.
- Lint of the components: pass for this change. The lint run reports 36 errors, but none is in a
  file this change touches (they are in check-quality, create-loop, create-play, edit-loop,
  edit-play, install-garura and others). Not caused by this change.
- Commits are clean: pass. Eight commits, each in the conventional form, each naming #1001 or
  #1002, each one concern (fix, feat, chore).
- No secrets: pass. A scan of the diff found no keys, tokens or passwords, and no absolute home
  paths in the source files.
- Docs in step: pass. The play's ICE, its compiled play text, the two skills, the agent's
  routing table and the screen template were all updated together, and the play's header counts
  (constraints, failure conditions, scenarios, steps, scripts) match the new totals.
- No merge conflicts: pass. A trial merge against plan/717/base gives a clean result.
- Nothing obviously broken: pass, with the notes below.

## Notes for the reviewer (none stops the raise)

1. One story for each feature is checked only on the new-feature path. A new feature checks
   that its feature does not already have a story under the same epic. The new path for an
   existing feature (an "add" entry that carries `feature`) has no such check, so a second
   story for the same feature under one epic would not be refused. Small, and the person sees
   the list before "approved". Worth a follow-up issue.
2. For an "add" entry that points at a story issue that already exists, the item records
   `represents` in the plan file, but the issue's own text does not get the "Represents:" line
   (only a newly created story gets it). The final agreement check does not look at
   `represents` for this path either, so the plan file and the tracker could differ on it.
   Small; the common case (a new story) is complete.
3. The "Fails if" check runs when the story body is checked (feature_ice.py body). It reads the
   ICE pages only when it is given the model folder; the play text passes it, but the script
   alone would quietly skip the page-based part of the check if called without it. The check on
   the clean copy still holds. Worth making the model folder required later.
4. The self-clean step (Step 16) sits above the Standard Play Close block in the play text but
   says it runs as the close's last action. It reads correctly, but a reader could take the
   order the wrong way round.

## Result

Findings that stop the raise: none.
Checklist: scope 4 of 4 pass, quality 8 of 8 pass, 4 notes for the reviewer.
