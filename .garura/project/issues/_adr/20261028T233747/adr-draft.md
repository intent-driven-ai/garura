# ADR 060 — A Plan's Branch Merges Into Main When the Plan Pauses, Even With Issues Still Open

**Status:** Proposed
**Date:** 2026-10-28
**Level:** framework
**Decided by:** Kapil Viren Ahuja · **Decided in:** #717 (plan 717, plans and the change plays), on `plan/717/base`, PR #950 — the review's finding H2 asked for this record
**Affects:** `docs/standards/harness-standard.md` (principle 8 "Branches follow the plan" and its Why line) · `core/components/plays/merge-change/reference/ice.md` (C9, F9, S6, REC9; S7 dropped) and its compiled `SKILL.md` · `core/components/plays/propose-change/reference/ice.md` (S6) · `core/components/plays/start-change/reference/ice.md` (C9) · `.garura/user-provided/managing-work.md` (section "A plan's branch: start, pause, start again", lines 160–177, and the Epic bullet's sentence on blocking work, lines 70–74) · `core/components/memory/standards/schemas/product-os/ontology.md` line 599 (the Plan kind's landing rule; removed in this same change through /edit-ontology, version 12 to 13) · the `branch` field of the plan files in `.garura/project/plans/` (`null` while a plan is paused; plan 788's file corrected in PR #950) · #791 (closed as not planned) · #730 (the plan update will write the `branch` field)
**ICE impact:** Three change plays change in meaning. merge-change lands a plan's branch on main like any approved change, with issues of the plan still open; holding it off main for open work is now a failure (F9, REC9); the only guard is the machine wall (C7 — approved, mergeable, no failing required checks); the "plan done" check and scenario S7 are gone. propose-change S6 opens a pausing plan's PR against main. start-change C9 cuts a plan's branch from the latest main when work starts, so after a pause the next start cuts a new one. In this same change, /edit-ontology removes the Plan kind's landing rule (line 599). No product agent reads branches (line 598: managing a plan never touches branches or code), so no product agent's ICE changes.
**Business intent check:** none — a framework rule about branches; nothing under `.garura/product/product-os/intents/` changes on this branch
**Related:** ADR 030, ADR 046, ADR 049, #717, #721, #730, #731, #673, #791, #879, #949, PR #916, PR #950

## Context

A plan gets its own branch, `plan/<plan-id>/base`, and each issue in the plan is cut from it and
lands back on it. Until now a plan's branch could land on main only when every issue in it was
closed, and after every plan it needs. That rule sat in two places: principle 8 of the harness
standard and merge-change's intent (C9, F9, S6, S7). No ADR ever recorded it.

The rule broke down in practice. On 2026-10-28 five plan branches sat 697 to 791 commits behind
main. The work of #721 (start-change and merge-change know about plans) was built on
`plan/717/base` on 2026-10-22 and never reached main, because plan 717 was not done. Work on the
plans paused while plan 788 ran, and nothing brought main back into the paused branches.

The product owner, 2026-10-28: "start a plan with a branch, and when we want to pause a plan,
merge it. branch should not be stopped to merge just because plan is not complete. and we can just
start the plan again."

The keeper searched every ADR for a rule on plan branches or on when a plan lands on main and found
none. ADR 030 (plan mode) and ADR 049 (one plan for each business intent) say nothing about
branches. ADR 046 was added in the same commit as the harness standard, but its decision is about
names only. So this ADR supersedes and amends no older ADR.

## For the Person Who Accepts This

### No earlier ADR held the rule this one replaces, so it supersedes and amends nothing

- **What and where:** the rule "a plan lands on main only when every issue in it is closed, and after every plan it needs". It was in `docs/standards/harness-standard.md` principle 8, and in merge-change's intent C9, F9, S6 and S7 (`core/components/plays/merge-change/reference/ice.md`).
- **What is wrong, or worth knowing:** every ADR in `docs/adr/` was searched, and none states a rule on plan branches or on when a plan lands. The rule came into principle 8 in commit b1c95fed on 2026-10-22 (#737, #738). That is the same commit that added ADR 046, but ADR 046's decision is naming only; it lists the harness standard under Affects only as a new file. The merge-change rule came in commit e55fe748 on 2026-10-22 (#673). ADR 030 and ADR 049 say nothing about branches.
- **Why it matters:** a reader who looks for the ADR this one replaces finds none. They could think an older ADR still says a plan waits until it is done. The old rule was a line in a standard and a play's intent, not a recorded decision.
- **What this decision does:** records the rule for the first time. No older ADR gets a forward pointer.
- **What you decide:** nothing — unless you hold that ADR 046 owns every principle of the harness standard. Then say so, and this becomes an amendment of ADR 046.

### Fixed in PR #950 — the work-management guide now says blocking work lands on main

- **What and where:** `.garura/user-provided/managing-work.md`, the bullet "An Epic stands for one slice, and holds only that slice's work", lines 70–74.
- **What is wrong, or worth knowing:** the first draft found lines 70–72 saying that work that blocks the plan "merges back into the plan branch it spawned from" (#879). That was the opposite of the guide's new section, lines 160–177. The lines now read: such work gets its own Epic and is delivered there; "It lands on main, not on the blocked plan's branch: the blocked plan pauses and merges into main first, and the blocker is cut from main".
- **Why it matters:** sessions read this guide before they file or work any issue (CLAUDE.md, Work Tracking). The old lines sent blocking work to a plan branch, the landing target this decision drops (#791).
- **What this decision does:** states the rule the fixed lines now follow.
- **What you decide:** nothing. The product owner fixed it in PR #950 (2026-10-29).

### Fixed in PR #950 — plan 788's file no longer names a gone branch or a detour target

- **What and where:** `.garura/project/plans/788.yaml`, the comment on lines 6–8 and `branch` on line 13.
- **What is wrong, or worth knowing:** the first draft found `branch: plan/788/base`, `returns_to: 756`, and a comment saying plan 788 lands back into `plan/756/base`. But PR #916 had merged `plan/788/base` into main on 2026-10-27, and #791 was closed. The file now reads `branch: null` and has no `returns_to`. Its comment says the branch merged with PR #916 and is gone, and that there are no detour plans. From now on, keeping these facts right is the job of the plan update play (#730); a comment on #730 records it (2026-10-29).
- **Why it matters:** the plan file is the person's view of the plan (ADR 030 §0). A wrong branch, or a promised detour landing, misleads a reader or a later start-change run.
- **What this decision does:** says what a paused plan's file reads: `branch: null`, and no detour target.
- **What you decide:** nothing. The product owner fixed it in PR #950 (2026-10-29).

### The ontology's landing rule leaves the ontology in this change, through /edit-ontology

- **What and where:** `core/components/memory/standards/schemas/product-os/ontology.md` line 599 (version 12), and the plan files `.garura/project/plans/717.yaml` lines 9–10 and `722.yaml` line 5.
- **What is wrong, or worth knowing:** line 599 reads: "A plan that needs another cannot land on main until that plan is done: the other plan has landed on main, or has been merged into this plan's branch." Plan 717 needs plan 722 (`needs_plans: [722]`), and plan 722 is `status: active`, not done. So PR #950 lands `plan/717/base` on main against that rule. The product owner decided on 2026-10-29 that the line goes in this same change, through /edit-ontology. It does not belong in the ontology. The ontology says what a plan is and how it links. When a branch lands is a delivery rule, and the harness standard (principle 8) and the plan rules in `.garura/user-provided/managing-work.md` hold it. The ontology's own line 598 says that managing a plan never touches branches. The link "It needs another plan" (line 586, rule on line 597) and the rule "Two plans that need each other are one plan" (line 600) stay: the link gives the order of work, not a gate on landing.
- **Why it matters:** with the line gone in this change, the standard, the change plays and the ontology agree when PR #950 merges. No agent or review that reads the Plan kind finds plan 717 on main against its rule.
- **What this decision does:** removes line 599 in this change, through /edit-ontology (ontology version 13, with one log line).
- **What you decide:** nothing. The product owner decided it on 2026-10-29. The /edit-ontology run asks for its own three yeses (the questions, the kinds, the links and rules).

### Later, in #949 — the memory tool's copy of the ontology is eight versions behind and has no Plan kind

- **What and where:** Phoenix memory, `standards/schemas/product-os/ontology.md`. It is the only memory tier that holds the ontology (checked with `find --every-tier`).
- **What is wrong, or worth knowing:** the memory tool returns version 4 of the ontology (205 lines). The source, `core/components/memory/standards/schemas/product-os/ontology.md`, is version 12, updated 2026-10-25, and holds the Plan kind and its rules (lines 590–604); after this change it is version 13. The memory copy names "plan" only once (line 168). Issue #949 (open) tracks that Phoenix memory is behind the source in 60 places, and names the ontology among them.
- **Why it matters:** agents read the ontology only through the memory tool. Until #949 is done, no agent sees the Plan rules, nor the removal of line 599. For the same reason, this ADR's effect on the Plan kind could not be read from memory; the keeper read it in the source file, as a file the decision changes.
- **What this decision does:** nothing. The gap is outside this decision.
- **What you decide:** nothing now. The product owner will do it later, in #949.

### Recorded on #730 — nothing writes a plan file's branch field yet; it is kept by hand

- **What and where:** the `branch` field of each plan file in `.garura/project/plans/`; start-change's `resolve_plan.py` and `setup_branch.py`; merge-change's `merge_pr.py`; issue #730.
- **What is wrong, or worth knowing:** `resolve_plan.py` builds the branch name from the plan id and never reads or writes `branch`. `merge_pr.py` never writes the plan file. So `branch: null` on a pause, and the branch name on a new start, are written by hand; plan 788's file showed the drift. Plan 717's file (line 7) already reads `branch: null  # plan/717/base merges into main and is deleted on 2026-10-28`, while PR #950 is still open. A comment on #730 (2026-10-29) says the plan update writes `null` when a plan's branch lands and the new name when start-change cuts one, and removes a `returns_to` it finds.
- **Why it matters:** until #730 is built, each pause and each start needs a hand edit, or the plan files and the branches drift apart. Plan 717's `null` is true only once PR #950 merges.
- **What this decision does:** states what the field reads on a pause (`null`). It leaves writing it to #730.
- **What you decide:** nothing. The product owner recorded it on #730.

### Kept — start-change still brings main into a plan branch that exists

- **What and where:** `core/components/plays/start-change/reference/ice.md`, C9 (lines 31–36) and S6 (lines 100–104).
- **What is wrong, or worth knowing:** C9 says that when a plan's branch already exists, "the latest main is merged into it before the issue's branch is cut (#731, Kapil 2026-10-22)", and S6 checks it. The brief lists "Keep plan branches open while paused, and bring main into them on each start" as an option that lost. What lost is keeping a paused branch open. The merge of main into a running plan's branch stays, because a plan's branch now exists only while the plan runs.
- **Why it matters:** a reader of the lost option could take it that start-change no longer brings main in, and remove C9's step. Without it, a running plan falls behind main between its issues.
- **What this decision does:** keeps start-change's C9 and S6 as they are.
- **What you decide:** nothing. The product owner kept it (2026-10-29).

## Decision

### 1. A plan gets its branch when its work starts

When work on a plan starts, the plan gets its own branch, `plan/<plan-id>/base`, cut from main.
Each issue in the plan gets a branch cut from it, `plan/<plan-id>/<issue>-<slug>`, and lands back
on it. A one-off fix outside any plan still branches from main.

### 2. When the plan pauses, its branch merges into main

When the plan pauses, its branch merges into main through the change plays (propose-change,
check-change, merge-change), even with issues of the plan still open. Those issues stay open and
stay in the plan. The branch is then deleted, and the plan file says `branch: null`.

### 3. When work on the plan starts again, a new branch is cut from main

The next start-change for an issue in the plan finds no plan branch and cuts a new
`plan/<plan-id>/base` from the latest main.

### 4. Only breaking main holds a plan's branch back

A plan's branch is never kept off main just because the plan is not done. The only reason to hold
it back is that it would break main. The review (check-change) and the merge checks (approved, no
conflicts, no failing required checks) decide that. Plan order (`needs_plans`) no longer holds a
plan off main.

### 5. No detour plans

A detour plan does not land back on the plan it came from. Pause the plan the detour came from
(merge it into main), cut the detour from main, and land the detour on main. #791, which was to
teach the change plays to land a detour back on its plan, is closed as not needed.

### What this changes

- The harness standard's principle 8 says this rule, and its Why line now reads "a plan's work stays together while it runs, and no paused plan falls behind main".
- merge-change: C9, F9, S6 and REC9 say a plan's branch lands like any approved change; S7 (plan done) is dropped.
- propose-change: S6, a pausing plan's own branch opens its PR against main.
- start-change: C9, a plan's branch is cut from the latest main when work on the plan starts.
- The work-management guide gains the section "A plan's branch: start, pause, start again", and its Epic bullet says blocking work lands on main.
- The ontology's line 599 (the Plan kind's landing rule) goes, in this same change, through /edit-ontology. When a branch lands is a delivery rule, not part of what a plan is.
- Plan files: `branch: null` while a plan is paused, and no `returns_to`.

## Consequences

### Positive

- Finished work reaches main when a plan pauses, instead of waiting for the whole plan.
- No paused plan falls behind main: a paused plan has no branch to fall behind.
- One landing target for a plan's branch (main), instead of main or a parent plan's branch.
- The harness standard, the change plays, the work-management guide and the ontology say the same thing when PR #950 merges.
- Starting a plan again is the same as starting it the first time.

### Negative / Risks

- Main holds part of a plan's work while the rest of its issues are open. Main is releasable only as far as the review and the merge checks make it; nothing checks that a plan's half-done work hangs together.
- A plan that needs another may land before the plan it needs (plan 717 needs plan 722, which is not done, and PR #950 lands plan 717). The ontology no longer forbids this: its line 599 goes in this same change, so the gap closes when PR #950 merges. If PR #950 merged without the /edit-ontology run, the gap would stay open.
- The plan file's `branch` field is kept by hand until #730 is built. No play writes `null` on a pause or the new name on a start, so it can drift from the branches, as plan 788's file did.
- Agents read the ontology through Phoenix memory, which is still at version 4 and has no Plan kind. They do not see this change until #949 brings it up to date.

## Alternatives Considered

- **A plan lands on main only when every issue in it is closed, and after every plan it needs** — the rule this replaces (the harness standard's principle 8, and merge-change's C9 before this change). Lost: a paused plan's branch falls behind main, and its finished work never reaches main. On 2026-10-28 it had stranded five branches.
- **Keep plan branches open while paused, and bring main into them on each start** — #731's own fix (start-change merges the latest main into an existing plan branch). Lost: it keeps finished work off main for as long as the plan pauses, and a plan that never starts again leaves its work stranded. (The merge of main into a running plan's branch stays in start-change's C9.)
- **Detour plans that land back on the plan they came from** (#791) — Lost: not needed once a paused plan merges into main; it added a second landing target and was never built.

## Work This Creates

- In this change (PR #950), before it merges: run /edit-ontology to remove the Plan kind's line 599 (ontology version 13, with one log line).
- #730: the plan update writes `branch: null` when a plan's branch lands and the new name when start-change cuts one, and removes a `returns_to` it finds (recorded on #730, 2026-10-29).
- #949, later: bring Phoenix memory's ontology up to version 13, with the other pages that are behind.
- After acceptance, rebuild the ADR index. No forward pointers: nothing is superseded or amended.

## References

- `.garura/project/issues/_adr/20261028T233747/brief.md` — the decision brief
- `docs/standards/harness-standard.md`, principle 8 (commits b1c95fed and 30b117b0)
- `core/components/plays/merge-change/reference/ice.md` (commits e55fe748 and d2e64f85)
- `core/components/plays/start-change/reference/ice.md`, `core/components/plays/propose-change/reference/ice.md`
- `core/components/memory/standards/schemas/product-os/ontology.md`, lines 586–600 (the Plan kind's links and rules)
- `.garura/user-provided/managing-work.md`
- `.garura/project/plans/717.yaml`, `722.yaml`, `788.yaml`
- #721, #730, #731, #673, #791, #879, #949, PR #916, PR #950
