# ADR 061 — A Plan's Branch Is Cut by the Play That Starts the Plan's Work, Main First, Through One Shared Script

**Status:** Proposed
**Date:** 2026-10-30
**Level:** framework
**Decided by:**  · **Decided in:** #720 (manage a plan with /update-plan), plan 717, on `plan/717/720-update-plan`, PR #998 — the review's findings HF-1 and MEM-1 asked for this record
**Amends:** ADR 060 — §3 "When work on the plan starts again, a new branch is cut from main", its sentence "The next start-change for an issue in the plan finds no plan branch and cuts a new `plan/<plan-id>/base` from the latest main": the play that starts the plan's work cuts it (/update-plan now, start-change once #989 is built), through the plan tool's `plan_branch.py`, main's plan file first; its ICE impact's sentence "No product agent reads branches (line 598: managing a plan never touches branches or code)": managing a plan may now cut the plan's branch, and still never merges a branch and never touches code; and, in "What this changes", the line "start-change: C9, a plan's branch is cut from the latest main when work on the plan starts", which stands until #989 is built. §1, §2, §4 and §5 stand
**Affects:** `core/tools/plan/plan_branch.py` (new in #720) with `core/tools/plan/README.md` (lines 50–57) and `core/tools/plan/test_plan_branch.py` · `core/components/plays/update-plan/reference/ice.md` (C2, C5, C7, F2, F3, S3) and its compiled `SKILL.md` (pre-flight line 58, Step 3, Step 13) · `core/components/memory/standards/templates/plan-update.md` (the `cut_note` screen, lines 100–101) · `core/components/memory/standards/schemas/product-os/ontology.md` (version 14, the Plan kind: rule lines 622, 623, 627 and States line 636; replaces version 13's line 598 "managing a plan ... never touches branches or code") · `core/components/plays/start-change/reference/ice.md` (C9 lines 31–36 and S5 lines 95–99, unchanged until #989) and `core/components/plays/start-change/scripts/setup_branch.py` (lines 107–108, moves to the shared script with #989) · the `status` and `branch` lines of main's plan files in `.garura/project/plans/` · `docs/adr/060-a-plans-branch-merges-into-main-when-the-plan-pauses.md` (its forward pointer, after acceptance)
**ICE impact:** /update-plan's ICE (C2, C5, C7, F2, F3, S3, written in #720 on this branch) holds the cut: for a plan with no branch, main's plan file is set to In Progress with the branch named, committed and pushed on main, and the branch is cut from that commit, as the one write before the person's approval; an abort undoes it. start-change's C9 and S5 do not change now; when #989 is built they change in meaning: start-change cuts the plan's branch through the same script, main first. The ontology's Plan kind (version 14, line 622) already says managing a plan may cut its branch and still never merges a branch or touches code; line 623 makes the cut the one change to a plan's status that a person did not type. No product agent's ICE changes: no product agent reads branches. This was read from the source ontology, because the memory tool's copy (Phoenix memory, version 4) has no Plan kind.
**Business intent check:** none — a framework rule about which play cuts a plan's branch; no page under `.garura/product/product-os/intents/` changes on this branch
**Related:** ADR 060, ADR 030, ADR 046, ADR 049, #720, #730, #717, #731, #949, #989, PR #950, PR #998

## Context

A plan's work is done on its own branch, `plan/<plan-id>/base`. ADR 060 decided that the branch is
cut from main when the plan's work starts, merges into main when the plan pauses, and is cut again
from main when work starts again. It named one play for the cut: "The next start-change for an
issue in the plan finds no plan branch and cuts a new `plan/<plan-id>/base` from the latest main".
Start-change's intent says the same in C9: "A plan's branch is created only when work on the plan
starts — by the first start-change for an issue in it". ADR 060's ICE impact rested on the
ontology's line 598 (version 13): "managing a plan changes both together and never touches
branches or code".

#720 built `/update-plan`, the session in which a person manages one plan. A person may open that
session on a plan that has no branch. The approved design of #720 (2026-10-30) has the session cut
the branch itself, through a new script in the plan tool, `core/tools/plan/plan_branch.py`. Before
the cut it sets main's plan file to `status: In Progress` and `branch: plan/<id>/base`, commits
only that file on main and pushes main. Ontology version 14 (#720) wrote this into the Plan kind
(line 622) and removed the words "never touches branches".

The review of PR #998 found the clash (findings HF-1 and MEM-1): the ontology and `/update-plan`
cut the plan's branch, while ADR 060 and start-change's C9 give the cut to start-change alone, and
no ADR records the change. The product owner chose to record it as an amendment of ADR 060.

The keeper read every ADR that the overlap check named (ADR 060, ADR 029, ADR 028) and the ones
that speak about plans (ADR 030, ADR 046, ADR 048, ADR 049). Only ADR 060 holds a rule on who cuts
a plan's branch. ADR 028 and ADR 029 name start-change only as the first change play; a drive's
branch is not a plan's branch. ADR 030's plan is a change's working plan on disk, not the Plan
kind. ADR 046 is about names only. ADR 048 and ADR 049 say nothing about branches. The harness
standard's principle 8 (`docs/standards/harness-standard.md`, lines 86–95) and the work guide's
section "A plan's branch: start, pause, start again" (`.garura/user-provided/managing-work.md`,
lines 160–177) stay true word for word: the branch is still cut from main when the plan's work
starts; neither names the play that cuts it.

## For the Person Who Accepts This

### Until #989 is built, start-change still cuts a plan's branch its own way, and that cut leaves main's plan file as it was

- **What and where:** start-change's intent, `core/components/plays/start-change/reference/ice.md`, C9 (lines 31–36) and S5 (lines 95–99); its script `core/components/plays/start-change/scripts/setup_branch.py` (lines 107–108 push `plan/<P>/base`); issue #989 (open, "start-change starts a plan on its own: it cuts the plan's branch from main, with no story branch").
- **What is wrong, or worth knowing:** C9 still reads "A plan's branch is created only when work on the plan starts — by the first start-change for an issue in it, cut from the latest main". Today `setup_branch.py` cuts `plan/<P>/base` straight from main and does not call `plan_branch.py`. It writes nothing in main's plan file: the status stays what it was (for example Paused or Not Started), and `branch` stays `null`. The ontology, version 14 line 627, says main's copy of the plan file names the branch. So until #989 there are two ways to cut a plan's branch: /update-plan's (main first, the file names the branch) and start-change's (the file says nothing). C9's word "only" is also no longer true, because /update-plan cuts too.
- **Why it matters:** a person who starts a plan's work with start-change sees, in /list-plans and /show-plan (both read the plan files only), a plan with no branch and its old status while its branch exists. A later /update-plan session finds the branch in git and switches to it, so it does not fix main's file either.
- **What this decision does:** records that start-change will cut through `plan_branch.py` once #989 is built, and leaves C9, S5 and `setup_branch.py` as they are now. The brief says: "start-change's ICE C9 follows when #989 is built".
- **What you decide:** whether C9 and `setup_branch.py` wait for #989 as the brief says, or C9's "only ... by the first start-change" is reworded now (for example "by the first start-change or /update-plan").

### ADR 060's promise on the plan file's branch field is half kept: the cut writes the name, but nothing writes `branch: null` when a plan pauses

- **What and where:** ADR 060, the point "Recorded on #730 — nothing writes a plan file's branch field yet" (lines 75–81); the comment on #730 of 2026-10-29 ("When a plan's branch lands on main (the plan pauses), the field becomes `null`; when start-change cuts a new plan branch, it gets that name"); `core/tools/plan/plan_branch.py` (lines 118–133 write the field); merge-change's scripts and /update-plan's scripts.
- **What is wrong, or worth knowing:** `plan_branch.py` now writes `branch: plan/<id>/base` on main when it cuts. No script writes `branch: null` when a plan's branch lands on main: a search of `core/tools/plan/`, `core/components/plays/merge-change/scripts/` and `core/components/plays/update-plan/scripts/` finds no such write, and /update-plan's intent has no step for it. #730 is open on GitHub, while plan 717's file on this branch (its `updated:` line) lists #730 as Done.
- **Why it matters:** after a pause, main's plan file still names a branch that was deleted, until a person edits it by hand. That is the drift plan 788's file showed (ADR 060). The cut itself is safe: `plan_branch.py go` decides from git, not from the file, so a stale name does not stop it.
- **What this decision does:** nothing — it is about the cut, not the pause.
- **What you decide:** whether writing `branch: null` on a pause stays owed under #730, or becomes its own issue.

### Agents still cannot read the Plan kind through memory: Phoenix memory's ontology is version 4 (#949)

- **What and where:** Phoenix memory, `standards/schemas/product-os/ontology.md`, the only memory tier that holds the ontology (checked with the memory tool's `find --every-tier`); the source, `core/components/memory/standards/schemas/product-os/ontology.md`, is version 14; issue #949 (open).
- **What is wrong, or worth knowing:** the memory tool returns version 4 (updated 2026-10-18), with no Plan kind and no branch rule. The source is version 14 (2026-10-30); its Plan kind holds this cut (line 622) and its status exception (line 623). #949 tracks Phoenix memory falling behind the source in 60 places.
- **Why it matters:** agents read the ontology only through the memory tool, so none of them sees that managing a plan may now cut its branch. This ADR's ICE impact was read from the source file, as a file the decision changes, not from memory.
- **What this decision does:** nothing — the gap is outside this decision.
- **What you decide:** nothing now; it is owed in #949.

## Decision

### 1. The play that starts a plan's work cuts the plan's branch

A plan's branch is cut by the play that starts the plan's work: `/update-plan` now, and
start-change once #989 (start-change starts a plan on its own) is built. Managing a plan may cut
the plan's branch. It still never merges a branch and never touches code.

### 2. One shared script makes every cut

Every cut goes through one script, the plan tool's `plan_branch.py`, so every cut is made the same
way, whichever play starts the work.

### 3. Main's plan file first, then the cut

When the plan has no branch, main's plan file is set to In Progress with the branch named. That
change is committed and pushed on main, and `plan/<id>/base` is cut from that commit. Setting In
Progress here is the one status change a person did not type: starting the plan's work is the
person's act.

### 4. A failed push takes the commit back; an abort undoes a cut that holds nothing else

When the push of main fails, the commit on main is taken back and main's plan file is as it was.
An abort undoes a cut that holds nothing else: the branch is deleted, and main's plan file is put
back by a revert commit.

### What this changes

- ADR 060 §3: the cut is made by the play that starts the plan's work, not by start-change alone.
- ADR 060's ICE impact: "managing a plan never touches branches" no longer holds for the cut; the
  rest of it (no merge, no code) holds.
- /update-plan: its C2, C5, C7, F2, F3 and S3 hold the cut (written in #720).
- The ontology's Plan kind: version 14, lines 622 and 623 (written in #720).
- start-change: C9 and S5 are unchanged until #989 is built; then they cut through `plan_branch.py`.

## Consequences

### Positive

- A person who opens a session on a plan with no branch can start its work there, with no detour
  to another play.
- Main's plan file says the plan is In Progress and names its branch from the moment the branch
  exists, so /list-plans and /show-plan show the truth (for every cut made by `plan_branch.py`).
- One script makes every cut once #989 is built, so the two plays cannot drift apart.
- ADR 060, the ontology and /update-plan say the same thing once this is accepted.

### Negative / Risks

- The cut is a commit pushed straight to main, with no pull request and no review. It changes
  only two lines of one plan file, but it is the one write a plan session makes before the
  person approves anything.
- Until #989 is built, start-change cuts a plan's branch its own way, without the main-first step,
  and its C9 still says the cut is start-change's alone.
- If the push of main succeeds and the push of the branch fails, main names a branch that is not on
  the remote. The script records it so an abort can undo it, but until then main's file is wrong.
- An abort cannot undo a cut once other work has landed on the branch, or when the revert clashes
  with later work on main; the script stops and names it, and a person sorts it out.
- Agents do not see this rule through memory until #949 brings Phoenix memory's ontology up to
  date.

## Alternatives Considered

- **`/update-plan` refuses a plan with no branch and sends the person to start-change first** —
  lost: start-change cuts a story's branch too, and #989 (starting a plan on its own) is not
  built; the person would be sent away for a step the session can do safely.
- **Leave it unrecorded** — lost: the ontology, ADR 060 and start-change's C9 would disagree with
  no record of why.

## Work This Creates

- #989: start-change cuts a plan's branch through `plan_branch.py`, main first; its C9 and S5
  then change through /edit-play.
- After acceptance, the play writes ADR 060's forward pointer and rebuilds the ADR index.

## References

- `.garura/project/issues/_adr/20261030T094556Z/brief.md` — the decision brief
- `core/tools/plan/plan_branch.py` (commits 314fb5ed and 5223135d)
- `core/components/plays/update-plan/reference/ice.md`, `core/components/plays/update-plan/SKILL.md`
- `core/components/memory/standards/schemas/product-os/ontology.md`, version 14 (commit 604df9d5), the Plan kind; version 13's line 598 on main
- `core/components/plays/start-change/reference/ice.md` (C9, S5), `core/components/plays/start-change/scripts/setup_branch.py`
- `docs/adr/060-a-plans-branch-merges-into-main-when-the-plan-pauses.md`
- #720, #730, #949, #989, PR #998 (review findings HF-1 and MEM-1)
