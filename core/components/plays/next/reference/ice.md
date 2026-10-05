# next — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
play-editor; never hand-edit the compiled SKILL.md.

## Intent

Recommend what to do next on the product — read the product model, build the list of
every action that is runnable or blocked, put it in a fixed order, and show it: one
next-best-action plus the ordered list. That is the whole play. Reading and ordering are
scripts; the play only presents the result.

The product model is the single source of "what could be done": slice status
(proposed → planned → realized), lens presence (the seven lens docs per slice — quality,
ux, agentic, marketing, architecture, run, measure), epic status (ready → in_delivery →
validated / fix_required → delivered) with epic dependencies, the product profile state
(directional → set → locked), capability detail (directional → detailed), and the
roadmap's order and slice dependencies. There is no separate backlog, sprint plan, or
work queue anywhere — and this play must not invent one.

The model is read the way the model-writing plays write it (ADR 026, direct-model-write):
the spine `_spine.yaml` is the index of record for the profile, domains, capabilities,
slices (status, order, effort, depends_on) and epics; lens presence is the slice's
`lens/<type>.md` grounding docs. Per-node records are read only for what the spine does
not carry, and a stale field on a record never overrides the spine. Realization runs in
two tracks (`standards/rules/pipeline-next.md`): the functional track ux → agentic →
marketing and the non-functional track arch → quality → run, with /measure last — and
/measure, once all seven lens docs line up, stamps the slice realized. Track order is
pipeline-next's recommended sequence, not a readiness gate.

Slices are the core unit of work. Once a slice exists, the aim is to realize it until it
is implementation-ready and then build it — so the order finishes one slice before the
others advance (user direction, 2026-09-11, #533). Other slices that are ready still show
in the list, below the slice being finished, as parallel lanes; they are never hidden.

The output is advice, never action: one next-best-action and the ordered list of
alternatives, every entry carrying the exact command and a plain-language explanation of
why it is recommended.

### Constraints

- C1 — Recommendations derive solely from the product model (slices, lenses, epics,
  profile, roadmap order and dependencies). No separate backlog or project store is
  consulted, and none is created.
- C2 — Recommend only: the play never modifies the model, never creates work items, and
  never launches another play. Multiple people and parallel agents may act on its output
  independently.
- C3 — Every entry names the exact command to run and explains, in plain language, why
  it is recommended.
- C4 — Output is one next-best-action plus an ordered list — at most 11 entries total,
  including the next-best-action; anything past the cap is named as cut, never silently
  dropped.
- C5 — A model inconsistency that blocks downstream work (e.g. a slice stamped realized
  with a lens missing) is a repair action, and repair takes the next-best-action slot
  when present.
- C6 — Cross-slice look-ahead is permitted, gated only by the roadmap: slice order and
  declared dependencies decide which other-slice actions may appear, and they appear
  below the slice being finished as parallel lanes.
- C8 — Derivation and ordering are deterministic scripts: the same model state always
  yields the same ordered list. The play's only judgment is how it words the
  presentation — it never reorders, adds, or drops an entry.
- C9 — Coverage spans the full loop: strategy (vision, understand, shape, roadmap),
  realization (the seven lens docs across the functional and non-functional tracks, then
  /measure), grilling, execution (implement, validate, launch), learning (learn), and
  strategy refresh once everything is delivered.
- C10 — The play leaves no working artifacts behind. Its only durable product is the
  recommendation presented to the user (plus, when evidence recording is on, the
  evidence record). All transient working files written during the run are deleted
  once the recommendation has been presented. The evidence record is never deleted.
- C11 — A slice carrying a `delivered` epic whose required user-facing surface was not
  actually delivered is in **surface debt** (`surface-contract.md` — "Surface debt:
  what /next must block"): the next execute epic in that slice is withheld and the
  surface-repair action takes priority, so later epics stop inheriting and compounding
  the downgrade. Surface debt is a blocking model inconsistency — it rides the same
  repair-takes-the-NBA-slot machinery as C5, detected mechanically from the model
  (never inferred).
- C12 — The play ends by proving its Done means at close (gated, #464): the ordered list
  was derived and the recommendation was presented — never by its step list running out.
  The proof is evaluated at close, before the self-clean (C10) removes the working
  folder; the verdict's durable copy is the evidence record.
- C13 — The model is read as the model-writing plays write it: the spine index of record
  for profile, domains, capabilities, slices and epics, and `lens/<type>.md` docs for lens
  presence (ADR 026). A model with no spine is reported as an inconsistency, never read
  from legacy per-node files. That reading is proven by the quick regression test file,
  which carries its own independent reader over the spine and lens folders — never by
  re-running the same scanner at runtime, because a check that shares its subject's
  reader can only confirm itself (#533).
- C14 — The list is ordered to finish a slice first: (1) repair, anywhere; (2) the focus
  slice — the lowest roadmap-order slice with work left (a lens, /measure, /grill, or live
  epics) — whose steps run functional-track head → non-functional-track head → /measure →
  /grill → epics by their order; (3) strategy; (4) every other slice's steps, by roadmap
  order, flagged as parallel lanes; (5) learning; (6) strategy refresh. Every step of the
  focus slice ranks above every step of any other slice (user direction 2026-09-11, #533;
  track sequence from `standards/rules/pipeline-next.md`).

### Failure conditions

- F1 — A recommended action's preconditions don't actually hold — the operator runs it
  and it halts at its own gate.
- F2 — A blocking inconsistency exists in the model but isn't detected and reported;
  downstream work stays silently stuck.
- F3 — The play mutates state or launches a play.
- F5 — The output is a dump: over the cap, or entries without plain-language
  explanation.
- F6 — A genuinely runnable lane is missed — the list disagrees with what the readiness
  gates over the model actually permit.
- F7 — Working files survive the run, lingering on disk as a stale recommendation after
  the model moves on.
- F8 — A slice carries surface debt — a delivered epic whose required user-facing surface
  was not delivered — yet /next recommends the next execute epic in that slice, so later
  epics keep building on a downgraded surface and compound the debt instead of repairing
  it.
- F9 — The close proves nothing — the play closes COMPLETED without the Done means
  held.
- F10 — The model snapshot disagrees with the model as the writing plays record it (the
  spine and the lens docs) — a stale or wrong-layout read — so every recommendation built
  on it is confidently wrong (e.g. finished roadmap or profile work recommended again).
- F11 — The order spreads work instead of finishing a slice: a step of a later slice, a
  strategy step, or a learning/refresh step ranks above a step of the focus slice (repair
  aside), so slices stall half-realized.

## Expectation

### Success scenarios

- S1 — (builder, product mid-delivery) Given a slice stamped realized but missing one
  lens, with ready epics queued behind it, then the repair (the missing lens play) takes
  the next-best-action slot and every blocked epic appears in the list with the missing
  lens named as its blocker. Measure: the NBA is the repair action AND each blocked
  entry names its blocker — checkable from the output alone.
- S4 — (founder, fresh start) Given no product model exists yet, then the
  next-best-action is /vision, explained as a cold start. Measure: the NBA equals
  /vision.
- S5 — (product owner, everything delivered) Given all slices realized and all epics
  delivered, then the play recommends the close of the loop — learning if pending, then
  strategy refresh (re-shaping from deferred functionality, re-planning the roadmap).
  Measure: the list contains a learning or strategy-refresh action with a plain-language
  explanation, not "nothing to do".
- S6 — (team running parallel agents) Given slice 1 with work left and slice 2 planned
  with its roadmap dependencies satisfied, then slice 2's next step still appears, below
  every slice-1 step, flagged as a parallel lane. Measure: a slice-2 action appears, is
  flagged parallel, ranks below all slice-1 actions, and cites the roadmap order.
- S7 — (product owner, roadmap merged) Given a spine with the profile set, every
  capability detailed, four slices planned at roadmap order 1–4, and the functional-track
  lens docs (ux, agentic, marketing) present on the order-2 slice, then no /roadmap and no
  /understand is recommended, each planned slice carries its next lens or /measure action,
  and the independent reader confirms the snapshot matches the spine. Measure: the list
  holds no strategy action, the order-2 slice's action is from the non-functional track,
  and the agreement check passes.
- S8 — (builder finishing a slice) Given slice 1 realized with a ready epic and slice 2
  planned with no lens docs, then building slice 1's epic is the next-best-action and
  slice 2's first lens ranks below it. Measure: rank 1 is slice 1's /implement and every
  slice-2 step has a larger rank.

### Done means

Paths are relative to the run's working folder (`<working>` =
`${product_base}_status/next/`). Derived from the artifacts every completed run
writes — the ordered candidate set and the presented report. Evaluated at close (Step
C0), BEFORE the self-clean (C10) deletes the working folder; the verdict's durable copy
is the evidence record.

- D1 — says: "the ordered candidate set exists (ordered candidates + capped entries + inconsistency report)"
  check: { type: artifact_exists, path: "candidates.json" }
- D2 — says: "the presented recommendation report exists"
  check: { type: artifact_exists, path: "recommendations.md" }

### Recovery (one per failure condition)

- REC1 (F1) — trigger: a recommended command would halt at its own gate. direction:
  record the divergence between the tree's rule and the target play's gate, fix the
  tree, and add a regression case. handoff: human.
- REC2 (F2) — trigger: downstream work halts on an inconsistency the run reported
  nothing about. direction: record the missed inconsistency class, extend the
  consistency scan, add a regression case. handoff: human.
- REC3 (F3) — trigger: anything in the model changed, or a play was launched, during the
  run. direction: halt immediately and surface exactly what changed — nothing is
  auto-reverted. handoff: human.
- REC5 (F5) — trigger: more than 11 entries, or an entry with no explanation. direction:
  re-run the ordering script, which caps the list and templates every explanation.
  handoff: autonomous.
- REC6 (F6) — trigger: the readiness gates admit an action the list lacks. direction:
  re-run derivation; if the action is still missing, the derivation rules are
  incomplete — record the gap and add a regression case. handoff: autonomous.
- REC7 (F7) — trigger: working files remain after the run completes. direction: delete
  the working folder; the already-presented recommendation is the only product. handoff:
  autonomous.
- REC8 (F8) — trigger: a slice has surface debt (a delivered epic with unmet required
  user-facing surface) and /next would recommend its next execute epic. direction: surface
  the debt as a blocking inconsistency, recommend the surface-repair action for that slice
  in the next-best-action slot, and withhold every further execute epic of that slice until
  the debt clears. handoff: autonomous.
- REC9 (F9) — trigger: the close would report COMPLETED without the Done means held.
  direction: evaluate the stop condition and surface the unmet clauses; re-run the
  producing step (derivation or presentation) to restore the missing artifact, or close
  HALTED with the verdict recorded. handoff: autonomous.
- REC10 (F10) — trigger: the regression test file fails a read or agreement case.
  direction: halt before presenting — nothing built on the wrong read is shown; surface
  the failing cases so the scanner is fixed. handoff: human.
- REC11 (F11) — trigger: an ordering case fails, or a presented list ranks another
  slice's step above the focus slice's. direction: halt before presenting, surface the
  mis-ordered entries, and fix the ordering script. handoff: human.
