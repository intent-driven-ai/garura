# ADR 062 — /update-plan Writes the Product Model Only After "Approved", and May Add a Feature to a Slice in Progress

**Status:** Accepted
**Date:** 2026-10-30
**Level:** framework
**Decided by:** Kapil Viren Ahuja · **Decided in:** #720 (manage a plan with /update-plan), plan #717, the review of PR #998 into `plan/717/base` (findings HF-3 and HF-4)
**Amends:** ADR 026 — Decision, the write-then-review order and its line "Checkpoint cancel means git restore of the model paths ... Approve means proceed; the writes are already on disk and reviewable": for /update-plan the model is written only after the person's plain "approved" for the whole list, and "rejected" and "abort" write nothing in the model, so there is nothing to revert (a declared exception, like /discover-intent's in ADR 031 and /record-decision's in #632); the scoped-write guard and "Clean tree in, committed delta out" stand · ADR 058 — Decision §2, where the /shape-slice edit option is the only way a slice in progress changes: an /update-plan session the person approves may now also add a feature to a slice in progress (`link-model-part`, `add_features` only; no other part of the slice changes), and its confirm screen says the slice is in progress and names each epic past ready, with its status, as out of date; and its ICE impact's words "no other play's ICE changes": /update-plan's ICE changes (C11). §1 and §3 stand
**Affects:** `core/components/memory/standards/rules/direct-model-write.md` (a third "Declared exception" paragraph after lines 134–146; step 7, lines 82–103, whose line 91 asks for a separate `feat(model)` commit; its lint anchor L-DMW-4, lines 230–232, gains `/update-plan` as a "Not a finding" case) · `core/tools/lint-components/lib/rules/structural.js` (L-DMW-4, lines 250–264, skips `/update-plan`) · `core/components/plays/update-plan/reference/ice.md` (C2, F2, S2, Context lines 88–89, C5/C7 and a failure condition for the guard, C11 and a failure condition for the confirm screen) and its compiled `SKILL.md` (Step 3, Step 8, Step 9's name-story dispatch, a guard run before Step 12, Step 12) · `core/components/plays/update-plan/scripts/scoped_write_guard.py` (new, stamped from `core/components/plays/create-play/references/scoped_write_guard.py`) · `core/components/plays/update-plan/scripts/place_feature.py` (lines 16–18, 57, 108–112), `render_screen.py` (lines 175–182) and `test_update_plan_scripts.py` (their tests, and a new test that fails when `place_feature.py`'s list of in-progress epic statuses differs from `find_serving_slice.py`'s) · `core/components/memory/standards/templates/plan-update.md` (lines 24–26 and line 118) · `core/tools/plan/plan_branch.py` (`go`, lines 149–155; its docstring, lines 16–18, says the uncommitted-work check runs first) with `core/tools/plan/test_plan_branch.py`, and `core/tools/plan/README.md` (lines 54–55, the same order) · `core/components/skills/link-model-part/SKILL.md` (description, "#931 — a slice itself is shaped only by /shape-slice") · `docs/adr/026-direct-to-model-writes.md` and `docs/adr/058-an-edit-the-person-approves-may-change-a-slice-in-progress.md` (their forward pointers, after acceptance). Read, not changed: `core/components/plays/shape-slice/scripts/find_serving_slice.py` (line 53, the list of epic statuses that mean past ready; the new test reads it), `core/components/plays/shape-slice/scripts/persist_slice.py` (line 105, `/shape-slice`'s own second copy of that list), `core/components/plays/shape-slice/reference/ice.md` (C7, C20, F7, F20), `core/components/skills/author-slice/SKILL.md` (lines 100 and 188), `core/components/skills/link-model-part/scripts/link_part.py` (lines 42 and 168), `core/components/memory/standards/schemas/product-os/ontology.md` (version 14, lines 461 and 583)
**ICE impact:** /update-plan's own ICE changes, through /edit-play. C2, F2 and S2: uncommitted work stops the play on every branch, the plan's own branch included. C5 and C7: the model is written only after "approved" (already so), and the shared scoped-write guard runs once after the last model write and before the one commit, and puts back any model path outside the session's parts — a new guarantee, with its failure condition and recovery. C11: a new feature may join a slice in progress, and the confirm screen says so and names each epic past ready, with its status, as out of date — with a failure condition when it does not. /shape-slice's ICE (C7, C20, F7, F20) and the `author-slice` skill do not change: a shaping run still never touches a slice in progress, and its edit option still may. No capability or feature ICE of the product changes, and the ICE kind does not change. Read from the play's ICE source and the source ontology (version 14), because the memory tool's copy of the ontology (Phoenix memory, version 4) has no Plan or Slice kind
**Business intent check:** none — a framework rule on how one play writes the product model and which slices it may add a feature to. It does not change the Business Intent kind, and no page under `.garura/product/product-os/intents/` changes on this branch; `link-model-part` only checks that an intent page exists (`link_part.py` line 238) and writes the intent id on the feature's own spine entry
**Related:** ADR 026, ADR 031, ADR 052, ADR 058, ADR 061, #720, #717, #730, #931, #949, PR #998

## Context

`/update-plan` is the session in which a person manages one plan. The person gives instructions in their own words. The play turns each one into entries on a running list and checks each entry. Nothing lands before the person types the plain word "approved" for the whole list. Then the play writes the product model, the tracker and the plan file, checks that the three agree, and makes one commit on the plan's branch. That order is the approved design of #720: "nothing lands before approved".

The review of PR #998 (feature #720, round 3) found two gaps.

The first gap (HF-3) is about the order of writes. The model-write rule (`standards/rules/direct-model-write.md`, ADR 026) says that a play writes the model first, then shows the change to the person, and on a cancel puts the model back (write-then-review). `/update-plan` does the reverse. No committed record declares that order as an exception. Also, the two checks the rule asks for were not wired: the model folder must be clean when the session starts, and the shared scoped-write guard must run after the model write.

The second gap (HF-4) is about slices in progress. A slice is in progress when its epic is past ready: its status is in_delivery, validated, fix_required or delivered. ADR 058 lets only a person's edit through `/shape-slice` change a slice in progress. But `/update-plan` places a new feature found while the plan is in progress (#931), and it can choose a slice in progress. A feature found mid-plan is most often found exactly while its slice is being built.

The ADR keeper read every older ADR the overlap check named. ADR 026 and ADR 058 are amended, each in part. ADR 061 (who cuts a plan's branch) is not changed: it does not say in what order the branch step checks uncommitted work, so a check on every path only adds a stop. ADR 031 keeps its own exception; this decision adds one beside it. ADR 043 and ADR 044 apply only inside a loop, and `/update-plan` never runs in a loop. ADR 052's rule that `/shape-slice` adds a new feature's hidden-file entry still holds: `/update-plan` names that entry as owed. ADR 048, 049, 055, 057 and 059 share only play names.

At the checkpoint on the first draft, the product owner took the recommendation on each of its three open points. This change names `/update-plan` in the linter's L-DMW-4 exception, corrects the plan tool's docstring and README, and ties `/update-plan`'s list of in-progress epic statuses to `/shape-slice`'s with a test. The points below say so; none of them leaves a choice open.

## For the Person Who Accepts This

### The component linter would fail /update-plan once it carries the guard, because its one commit is not a feat(model) commit

- **What and where:** the linter rule L-DMW-4 in `core/tools/lint-components/lib/rules/structural.js` (lines 250–264); step 7 of `direct-model-write.md` (lines 82–103) and its lint anchor L-DMW-4 (lines 230–232).
- **What is wrong, or worth knowing:** the L-DMW checks run only on a play that bundles `scripts/scoped_write_guard.py` (lines 189–199). This decision makes `/update-plan` bundle it. Then L-DMW-4 asks for two texts in its `SKILL.md`: `git status --porcelain ... product-os` and `feat(model)`. `/update-plan`'s `SKILL.md` has neither today. The clean check is done by `plan_branch.py go` over the whole tree, and this decision says the model change goes in the session's one commit, not in a separate `feat(model)` commit. L-DMW-4's only "Not a finding" case is a play run with a loop contract. L-DMW-3 and L-DMW-6 do not fire today: the `SKILL.md` has no "Checkpoint" heading, no "approval-prompt" and no `persist_*.py`.
- **Why it matters:** the rebuild of `/update-plan` through `/edit-play`, and the review's lint layer, would report two errors on a play that follows this decision. Whoever runs the rebuild would be pushed to add a `feat(model)` commit that this decision says not to make.
- **What this decision does:** it declares the exception in the rule. In this same change, L-DMW-4's "Not a finding" note names `/update-plan`, in the rule (lines 230–232) and in `structural.js` (lines 250–264): its clean-tree check is `plan_branch.py go` over the whole tree, and its model change goes in the session's one commit. So no `feat(model)` commit and no model-only `git status --porcelain` check is asked of it.
- **What you decide:** nothing. You chose this at the checkpoint.

### The guard must run after the second model write, not right after the model step

- **What and where:** `core/components/plays/update-plan/SKILL.md`, Step 8 (lines 264–279) and Step 9 (lines 290–299).
- **What is wrong, or worth knowing:** the session writes the model twice. Step 8 writes each new feature's page, its spine entry and its place in the slice. Then, after the tracker step makes the story, Step 9 sends `product-os-keeper` again to name the story on the feature's spine entry (`link-model-part`, mode update, issue). The brief says the guard runs "once after the model write and before the commit".
- **Why it matters:** a guard placed right after Step 8 would not see Step 9's write. A model path written there outside the session's parts would reach the commit with no check.
- **What this decision does:** it says the guard runs once, after the last model write and before the one commit (Step 12).
- **What you decide:** nothing.

### The plan tool's own words still say "stay" comes before the uncommitted-work check

- **What and where:** `core/tools/plan/plan_branch.py`, its docstring lines 16–18; `core/tools/plan/README.md` lines 54–55; `/update-plan`'s ICE, Context lines 88–89 and C2 line 21.
- **What is wrong, or worth knowing:** the code of `go` (lines 149–155, not yet committed on this branch) now checks uncommitted work first, and only then stays on the plan's branch. The docstring still reads "on the plan's branch already: it stays ...; else, when anything is uncommitted ...: it stops". The README reads "it stays there, stops on uncommitted work ...". The ICE's Context reads "stay, stop on uncommitted work, switch", and C2 reads "On another branch with uncommitted work it stops".
- **Why it matters:** the builder of #989 (start-change cuts a plan's branch through `plan_branch.py`) reads the README and the docstring and learns the old order. The ICE as written would let a rebuilt play stay on a plan branch with uncommitted work.
- **What this decision does:** it makes the check on every path the rule. In this same change, the docstring and the README are corrected with the code: the uncommitted-work check runs first, on every path, the plan's own branch included. The ICE's C2 and Context change with `/edit-play`.
- **What you decide:** nothing. You chose this at the checkpoint.

### /update-plan keeps its own copy of the list of epic statuses that mean "in progress"

- **What and where:** `core/components/plays/update-plan/scripts/place_feature.py` line 57 and `core/components/plays/shape-slice/scripts/find_serving_slice.py` line 53.
- **What is wrong, or worth knowing:** both hold `IN_PROGRESS = ("in_delivery", "validated", "fix_required", "delivered")`. The `place_feature.py` line says "past ready (ADR 058)". Nothing ties the two copies together today. A third copy is inside `/shape-slice` itself, `persist_slice.py` line 105; `edit_slice.py` line 57 imports the list from `find_serving_slice.py`.
- **Why it matters:** if `/shape-slice`'s list changes (for example, a new epic status), `/update-plan` would still treat that slice as not in progress. It would add a feature to it with no warning on the confirm screen — the silent change this decision forbids.
- **What this decision does:** in this same change, a test in `test_update_plan_scripts.py` reads both lists and fails when `/update-plan`'s copy differs from `find_serving_slice.py`'s. The list does not move. The test does not read `persist_slice.py`'s copy, which is `/shape-slice`'s own.
- **What you decide:** nothing. You chose this at the checkpoint.

### Agents will not see this exception through memory until the rule is promoted, and memory's copy is already behind

- **What and where:** Phoenix memory, `standards/rules/direct-model-write.md` (the only tier that holds it, found with the memory tool's `find --every-tier`); its source, `core/components/memory/standards/rules/direct-model-write.md`.
- **What is wrong, or worth knowing:** the memory tool's copy still names the old plays: line 117 reads "Declared exception — `/intent` run by hand (ADR 031)" and line 123 reads "Declared exception — `/adr` run by hand (#632)". The source names `/discover-intent` and `/record-decision`. The memory copy of the ontology is version 4; the source is version 14. #949 tracks Phoenix memory falling behind the source. The fix design (`.garura/project/issues/720/specs/fix-design-round-3.md`, "Order") says the rule is promoted after the merge, on the product owner's word.
- **Why it matters:** agents read rules only through the memory tool. Until the promotion, an agent that checks `/update-plan` against the rule reads write-then-review with no `/update-plan` exception, and may report the session's order as a breach.
- **What this decision does:** nothing — promotion is a person's act, outside this decision.
- **What you decide:** nothing now; the promotion is owed after the merge (#949).

### The confirm screen already cites this record before it is accepted

- **What and where:** `core/components/memory/standards/templates/plan-update.md` line 26 ("(ADR 058, ADR 062)"), with the slice-in-progress lines of `place_feature.py` and `render_screen.py` — all not yet committed on `plan/717/720-update-plan`.
- **What is wrong, or worth knowing:** part 2 of this decision is already built in the working tree. The template names "ADR 062", the number this record takes.
- **Why it matters:** if this record is rejected, those lines name a record that does not exist, and they let `/update-plan` add a feature to a slice in progress with no decision behind it.
- **What this decision does:** nothing to those files.
- **What you decide:** nothing if you accept; on a reject, those lines are taken out before the change lands.

## Decision

### 1. /update-plan writes the product model only after "approved"

`/update-plan` writes the product model only after the person types the plain word "approved" for the whole list. This is a declared exception to the write-then-review order of the model-write rule (ADR 026), like `/discover-intent` and `/record-decision` run by hand. A "rejected" or an "abort" writes nothing in the model, so there is nothing to revert.

The rule's other guarantees still hold:

- **A clean tree at the start.** The model tree must be clean when the session starts. The plan-branch step stops on any uncommitted work, on every path, the plan's own branch included.
- **The guard runs once.** The shared scoped-write guard runs once, after the last model write and before the commit. It puts back any model path outside the session's parts.
- **One commit.** The model change is committed in the session's one commit on the plan's branch, with the plan file, not in a separate `feat(model)` commit. The approved design lands a session as one commit whose message names the instructions, the overrides and what is owed.

### 2. A new feature may join a slice in progress, and the confirm screen says so

A new feature found while the plan is in progress may join a slice that is in progress: its epic is past ready (in_delivery, validated, fix_required or delivered — the rule `/shape-slice` uses).

A new feature is always a big change. It is shown on the confirm screen before it joins the list. When its slice is in progress, that screen says so and names each epic past ready, with its status, as out of date, because work already started from the old slice. Nothing is written before the person's yes on that screen and their "approved" on the whole list.

This amends ADR 058, whose rule let only a person's edit through `/shape-slice` change a slice in progress. An `/update-plan` session the person approves may now add a feature to one. It only adds a feature to the slice's features (`link-model-part`, `add_features`). It changes no other part of the slice.

### What this changes

- ADR 026: write-then-review gains a third declared exception, `/update-plan`. Its other guarantees stand.
- ADR 058 §2: a slice in progress may also gain a feature through an approved `/update-plan` session. §1 (a shaping run never touches a slice in progress) and §3 (the edit brief names the epic as out of date) stand.
- The model-write rule: a "Declared exception — `/update-plan`" paragraph.
- `/update-plan`: C2, F2, S2, C5, C7 and C11, with their failure conditions, through `/edit-play`.
- The linter: L-DMW-4 does not ask `/update-plan` for a `feat(model)` commit or a model-only clean check. Its "Not a finding" note names `/update-plan` in the rule and in `structural.js`.
- The plan tool: its docstring and its README say the uncommitted-work check runs first, on every path, the plan's own branch included.
- `/update-plan`'s list of epic statuses that mean "in progress": a test fails when it differs from `/shape-slice`'s list in `find_serving_slice.py`.

## Consequences

### Positive

- The order `/update-plan` already follows is now on record, so the play, the rule and the review say the same thing.
- A "rejected" or an "abort" leaves the model as it was, with no revert path to get wrong.
- The guard and the clean tree keep a session from committing someone else's model edits: the order changes, the containment does not.
- A feature found while its slice is being built joins that slice, so its tester sees it.
- No change to work in flight is silent: the person sees that the slice is in progress, and which epics are out of date, before they say yes.
- The linter, the rule and the plan tool's own words agree with the play, so a rebuild of `/update-plan` is not pushed to add a `feat(model)` commit, and a builder of #989 (start-change cuts a plan's branch) reads the right order.
- If `/shape-slice`'s list of in-progress statuses changes, a test fails until `/update-plan`'s copy matches.

### Negative / Risks

- The epic and stories of a slice in progress may now disagree with the slice. The screen names them as out of date but changes nothing, so someone must check that work. The new feature's hidden-file entry and eval scenarios are owed until `/shape-slice` and `/shape-eval` run.
- L-DMW-4 now has two exceptions (a loop contract, and `/update-plan`). Each new exception makes the lint anchor longer to read and easier to get wrong.
- Until the rule is promoted to Phoenix memory, agents read write-then-review with no `/update-plan` exception.
- `/update-plan` still holds its own copy of the list of epic statuses that mean "in progress". The test catches drift only when the tests run, and it does not watch `persist_slice.py`'s copy inside `/shape-slice`.

## Alternatives Considered

- **Write the model first, then show the list and revert on a reject (the rule's order)** — lost: the approved design is that nothing lands before "approved". The session's list may hold many entries over many instructions; writing the model on each instruction and reverting on a reject adds churn and a revert path to a session that the person may abort.
- **Declare the exception but skip the guard and the clean-tree check** — lost: the guard and the clean tree are what keep a session from committing someone else's model edits. The order changes; the containment does not.
- **Never add a new feature to a slice in progress: the feature joins no slice, and a slice is named as owed** — lost: a feature found mid-build belongs with the slice being built. Leaving it out hides it from that slice's tester, and ADR 058 already lets a person's approved edit change a slice in progress when the brief says so.
- **Allow it silently** — lost: work already started from the old slice. The person must be told, as ADR 058 requires for an edit.

## Work This Creates

- `/edit-play /update-plan`: C2, F2, S2, Context, C5 and C7 with the guard's failure condition, C11 with its failure condition; stamp `scoped_write_guard.py` into its scripts; the guard step after the last model write.
- `direct-model-write.md`: the `/update-plan` declared exception paragraph, and `/update-plan` named in L-DMW-4's "Not a finding" note — in this change.
- `structural.js`: L-DMW-4 skips `/update-plan` — in this change.
- `plan_branch.py`'s docstring and `core/tools/plan/README.md`: the uncommitted-work check first, on every path — in this change.
- `test_update_plan_scripts.py`: a test that fails when `/update-plan`'s list of in-progress epic statuses differs from `find_serving_slice.py`'s — in this change.
- `link-model-part` `SKILL.md`: its line on who changes a slice.
- Promote `direct-model-write.md` to Phoenix memory after the merge, on the product owner's word (#949).
- After acceptance, the play writes the forward pointers on ADR 026 and ADR 058 and rebuilds the ADR index.

## References

- `.garura/project/issues/_adr/20261030T123415Z/brief.md` — the decision brief
- `.garura/project/issues/720/specs/fix-design-round-3.md` — the approved fix design, B5 and B6
- `core/components/memory/standards/rules/direct-model-write.md`, `core/tools/lint-components/lib/rules/structural.js`
- `core/tools/plan/plan_branch.py`, `core/tools/plan/README.md`
- `core/components/plays/update-plan/scripts/place_feature.py`, `core/components/plays/shape-slice/scripts/find_serving_slice.py`
- `core/components/plays/update-plan/reference/ice.md`, `core/components/plays/update-plan/SKILL.md`
- `docs/adr/026-direct-to-model-writes.md`, `docs/adr/031-business-intent-and-ice.md`, `docs/adr/058-an-edit-the-person-approves-may-change-a-slice-in-progress.md`, `docs/adr/061-a-plans-branch-is-cut-by-the-play-that-starts-its-work-main-first.md`
- #720, #717, #931, PR #998 (review findings HF-3 and HF-4)
