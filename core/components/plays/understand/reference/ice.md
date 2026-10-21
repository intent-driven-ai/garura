# understand — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
play-editor; never hand-edit the compiled SKILL.md.

## Intent

Given the pending capabilities — every capability seeded by /vision (named, directional,
no functionalities) that nobody has detailed yet, or the capabilities the person names,
including ones not yet in the model — **detail them all in one run** (Kapil, #615: one at a
time is too slow). When a named capability is not yet in the model, /understand asks the
person what it is, why it matters, and which existing domain it joins — for every such
capability at once, before it opens any change, so a stop leaves nothing behind — and seeds
it thinly from those answers: a spine entry, enough for the detailing to start, whose first
`capability.md` is then written straight at the detailed stage. Never invented (#616 D1).
/understand is the **product-manager** step, the last detailing step: for each target,
promote its `capability.md` from the directional stage to the detailed stage (benefit
hypothesis, boundary, guiding rules, functionalities), **create its functionalities** (a
spine entry plus a detailed `functionality.md` for each), and set the capability's own
concrete NFR + compliance needs. Then roll all the targets' needs up together into the
product profile box, each measured against the box as it stood at the start of the run: on
a still-directional box the roll-up establishes the box and firms it to `set`; on an
already-set box, each capability's need that exceeds the committed ceiling is an
out-of-box event that halts for a human decision moving the box and recording why. One run,
one save, one human checkpoint that approves every target's detailed grounding and every
box-move before anything is committed, one commit. The grounding docs are gated by the
structural linter (shape) and the content-quality eval (a judge).

Pipeline position: **both**. /understand stands on its own (ADR 029 §4; #616 D2): run by hand, it needs no other play to have run first. Inside a drive (ADR 029 §2–3; #615) it is handed the drive's contract (`standards/rules/drive-contract.md`) and opens nothing: no `start-change`, no end sequence, no wait at its checkpoint — it works on the drive's branch, commits its model delta there, and keeps what its checkpoint would have shown, every box-move included, as review records for the drive's end review. Kickoff runs it once for all the capabilities; the run leaves one review record per capability (ADR 029: "one `/understand` record per capability"). The D2 rule prepends `start-change` — resolve or create the issue, cut the branch off fresh main, optional worktree, init STM — and, after the model delta is committed, appends the close sequence `commit-change → propose-change → review-change → merge-change`, landing the detailed capability on main. It writes the persistent product model directly, in place, on its own started branch — there is no draft copy and no apply/promote step; review is the branch git diff and the end PR. (#437, #498, ADR 026; position changed from none to both in #616.)

Write discipline (ADR 026, `standards/rules/direct-model-write.md`): the LLM enrichment skill writes ONLY the per-node docs (`capability.md`, `functionality.md`) straight to the live model; every shared-file mutation (the spine `_spine.yaml`, `profile.yaml`, the box-move decisions) is done by the deterministic keyed persist script, in place, keyed to the run's target capabilities so it cannot touch any other node inside a shared file. The model tree is asserted clean at entry and the play commits its own model delta at close, so the working-tree diff vs HEAD is exactly this run's delta.

Agents and skills (ADR 039 §2, §7, §8): the play reads no memory. `product-os-keeper` (domain agent) re-routes each target with `search-kb` and details it with `enrich-capability-ice`, reading memory only through the memory tool. `template-manager` (utility agent) hands the play the approval prompt, each judged kind's grounding template and the shared close's templates, copied into the issue's short-term memory. Each content-quality judge is an isolated sub-agent running the `judge-grounding` skill, handed only its doc (and parent doc) and the kind's `## Per-section guidance` block, which the bundled `guidance_block.py` cuts from the template copy — the judge never sees the template's gold example (`standards/rules/grounding-eval.md`).

### Constraints

- C1 — One run details every target (#615). The targets are the capabilities the person
  names (the play argument), in the order given; with none named, every capability in the
  spine at `detail: directional` — seeded and not yet detailed — in spine order. The pick is
  made by the bundled `pick_targets.py`, before any change opens; with nothing pending the
  play ends at once, opening nothing. A target in the spine as a directional seed is detailed
  as is. For each **absent** target the play — before it opens any change, and for all of
  them in one round of questions — asks the person what the capability is, why it matters,
  and which existing domain it belongs to, records the answers verbatim
  (`<working>/caps/<capability>/seed.yaml`, `answered_by: human`), and seeds it thinly: a
  spine entry at `status: proposed`, `detail: directional`, under that domain, whose first
  `capability.md` this run writes straight at the detailed stage. The seed carries only the
  person's answers, nothing invented; the keyed persist refuses a seed not marked
  `answered_by: human`. Run by hand, with no answer or a domain that is not in the spine, it
  halts — before any issue or branch exists — and says plainly what it needs; inside a drive
  that capability is the drive's question instead, and the play details the others (C13). A named target that
  is already `detailed` halts the run; it is not re-detailed. Inside a drive (C13) the
  answers come from the contract (the drive asked them before it started); the seed records
  them with `answered_by: human` only because a person gave them up front. With no answers
  in the contract, the play stops and asks the person before any model write — it never
  fills them in itself.
- C2 — It promotes each target capability `directional → detailed` and CREATES its
  functionalities (each a spine `functionalities` entry plus a detailed `functionality.md`).
  This is the structure /understand owns — the last detailing step. It never touches a
  capability outside the run's targets or a domain, and never prioritizes (no slices, no
  epics, no capability status flip — that is /shape).
- C3 — The detailed `capability.md` is complete to its template (benefit hypothesis,
  boundary In/Out/Never, guiding rules, and a Functionalities index whose entries link to
  real functionality ids), and every `functionality.md` is complete to its template (what
  it does, inputs/outputs, rules & behavior, acceptance criteria, out of scope). No
  required section is empty, and the spine and docs stay consistent (the linter passes).
- C4 — Content quality: every grounding doc (the detailed capability and each
  functionality) clears the content-quality eval, not just the linter — each section is
  self-explaining at product-manager altitude and the doc passes the stranger test.
- C5 — The capability's NFR needs are per-capability and concrete: each dimension it
  constrains carries a `level` (none<low<medium<high<xhigh), a measurable `target`, and a
  `gate` (how it is checked); `compliance_needs` are listed. No vague adjective.
- C6 — Detail is grounded in the capability's KB shelf (personas, systems, NFR hints,
  scope, functionality baseline) and, when a prototype's capture is given, in its screens
  (C16) — it does not invent what the shelf already covers.
- C7 — Profile roll-up is monotonic-up: each dimension's committed level becomes the
  greater of the current box and every target's required level; no dimension is ever
  lowered. Every target is measured against the box as it stood at the start of the run
  (the bundled `rollup_box.py` takes one manifest per target), never against a box another
  target in the same run already raised. On a still-directional box the roll-up establishes it and firms it to `set`.
  /understand never writes `locked`.
- C8 — Against an already-`set` box, a need (an NFR level or a compliance regime) that
  exceeds the committed ceiling is an out-of-box event: it halts for human approval. Each
  target whose need exceeds the starting box gets its own box-move (the capability, the
  dimension, from the starting level to its need), so no capability's box-move hides behind
  another's; each box-move is written as its own product-level decision (ADR), linked to its
  capability, and COMMITTED only on approval (on cancel the write is reverted with the rest of the delta). A need inside the
  box never halts. Inside a drive (C13) each box-move is written with its decision at
  status `proposed` — never `accepted`, because no person at a checkpoint says yes inside a
  drive — and appears as its own line in the review record when the checkpoint is
  deferred; the drive's review accepts or drops it (Kapil, #615).
- C9 — Exactly one human checkpoint for the whole run, presenting each target's detailed
  capability, its functionalities and its NFR needs, and the profile changes — every
  box-move as its own line item (capability, dimension, from→to, the decision it creates). The checkpoint is a
  **conditional gate** (#467; `gate-config.md` three gate kinds — /understand is one of
  the eleven conditional document plays). Resolution order: pinned (n/a here) → the
  `gates.plays` override → the learned policy (classify the working-tree change shape —
  the model tree's diff vs HEAD — with the bundled `classify_change.py`
  (`--product-base`/`--base-ref HEAD`); a shape in `gate-policy.yaml`'s `auto:` and not
  in `never_auto:`, with NO blocking finding — a lint gap or a content-eval fail —
  auto-passes with the skip and the diff summary recorded) → `gates.classes.standard` →
  `gates.default`. EVERY crossing appends one live-eval line via the bundled
  `gate_eval.py` (shape, predicted gate|auto, the human's real action
  `approved_clean|approved_edited|rejected`, or `auto_pass`). Write-then-review (ADR 026):
  the run writes the full delta to the live model FIRST (docs by the skill, shared files by
  the keyed persist), so the checkpoint presents the real model git diff and the change-shape
  is classified over the full delta; nothing is COMMITTED before the gate resolves — a typed
  approval, a recorded config skip, a recorded policy auto-pass, OR, inside a drive, a
  recorded deferral to the drive's review (C13). On cancel the whole delta
  is reverted (`git restore` + `git clean`). Box-move approvals ride this same gate, so the
  recorded skip or auto-pass stands in evidence for them too. (Inside a drive the checkpoint
  does not wait; it becomes a review record for the drive's end review — C13.) At close the play refreshes the
  learned policy with
  the bundled `distill_gate_policy.py` (config `gates.conditional`: streak/ledger/policy
  paths).
- C10 — Non-destructive to the rest of the model, enforced by the post-write scoped guard:
  the run writes only the target capabilities (each doc + spine entry), their new
  functionalities (docs + entries), the firmed profile, and the box-move decisions. After the
  writes and before the checkpoint, the bundled `scoped_write_guard.py` diffs the model tree
  against HEAD and FAILS the run (reverting the offending paths) if any model path outside
  that scope changed. No capability outside the targets, and no other functionality or
  domain, is changed; the monotonic-up
  roll-up guarantees no other capability's need is undercut. Node-level containment inside
  the shared spine/profile is kept by the keyed persist script (only it writes those files),
  not the guard.
- C11 — The play ends by proving its Done means at close (gated, #464): the keyed persist
  record exists (every target's detailed grounding, its functionality docs, and the profile
  roll-up were written in place on the live model), the persist record stamps the roll-up as
  written, and the scoped-write guard report reads ok (the allowlist held). The play then
  commits its own model delta on the branch, and the injected end sequence (commit →
  propose → review → merge) lands it on main; each member proves its own Done means, and a
  review reject stops the chain before merge. Inside a drive the end sequence does not run
  — the drive lands the change (C13). The close never reads COMPLETED with the
  stop-condition verdict unmet.
- C12 — Clean tree in, committed delta out (ADR 026): the product-os tree is asserted clean
  at entry (pre-flight halts on a dirty model tree), and after the approved checkpoint the
  play commits its model delta on the branch (`feat(model): … (#<issue>)`), so HEAD is a
  correct base for the guard and the change-shape, and the end sequence lands exactly this
  run's delta. The tree is asserted clean right after `start-change` cuts the fresh branch
  (inside a drive, at once — the earlier plays in the drive committed their model change),
  so a dirty tree means uncommitted edits, never a missing earlier play. This model-delta
  commit is a lightweight persist step, distinct from both the end sequence and the
  per-play Standard Play Close (evidence + delivery report).
- C13 — Runs inside a drive without stopping (ADR 029 §2–3; `standards/rules/drive-contract.md`):
  handed a drive's contract (`--contract`), the play checks it first with the bundled
  `check_drive_contract.py` — an invalid contract, or a current branch other than the
  drive's, halts — and records `in_drive` in `run.json`. Inside a drive it runs no
  `start-change` and no end sequence (the drive opens and lands the change); it takes the
  targets as by hand (C1) — the named capabilities, else every pending one — plus every
  capability the contract seeds, with a seed's answers from the contract's
  `answers.understand.seeds.<capability>` (`one_line`, `why`, `domain`); it asserts the
  clean model tree at once; it resolves its checkpoint (C9) exactly as by hand — a config
  skip or a policy auto-pass is recorded as by hand — and only where the gate would WAIT
  does it not wait: it renders each target's part of the checkpoint exactly as it would have
  been shown, that capability's box-moves each as its own line, and writes it, with the
  files it stands on (the roll-up, the shape, the guard report, the persist record), as that
  capability's review record into the contract's `review_dir` with the bundled
  `write_drive_review.py` — one record per capability, named for it — and appends the
  crossing to the gate ledger once as `deferred_to_drive_review` (the learner skips it until the drive's review
  writes the person's real answer). Inside a drive every box-move decision is written
  `proposed` (C8) — the keyed persist runs before the gate resolves, so it is told by
  `in_drive`, not by the gate's outcome. It still commits its model delta on the drive's branch (C12). A
  question neither the contract nor the model answers — an absent capability with no seed
  answers — is the drive's (ADR 041): the play writes it to `<review_dir>/open-understand.json`
  (drive contract, step 5), details what it can, and finishes; the drive asks the person only
  what none of its plays can answer. The play never picks an answer itself. Run
  by hand (no contract), every step runs as before.
- C14 — One run, all or nothing, the targets at once (#615). The run opens one change,
  saves once, guards once, has one checkpoint and makes one model-delta commit for all its
  targets. The enrichment runs for every target at once, as a **scoped-write fan-out**
  (`standards/rules/concurrent-fanout.md`; Kapil, #615: "B"): `pick_targets.py` gives each
  target its write scope — its own folder in the model — and refuses two targets whose
  folders overlap; each dispatch writes only that target's docs inside its write scope and
  its own manifest, no dispatch writes a shared file (the spine, the profile, decisions —
  those go to the one keyed persist), and the batch is joined before any later step reads
  the model. The content-quality judges, which only read, run as one concurrent read-only
  batch over every doc of every target. If any target cannot pass its checks after its
  recovery, the whole run halts and nothing is committed — no target lands alone.
- C15 — The run's short-term memory lives in the issue it works on (ADR 036 §1, ADR 039 §1;
  Kapil, 2026-10-19: "the issue that we are working on is where the short-term memory is going
  to get created. Doesn't matter whether it is drive play or whatnot"). Inside a drive that is
  the contract's `issue`; run by hand it is the issue `start-change` opens or resolves (Step 0).
  The run's working root is `{stm_base}<issue>/context/understand/<run ts>/` (inside the
  issue's `context/` key, ADR 017), so the person's answers (`caps/<capability>/seed.yaml`)
  are in the issue's short-term memory, where the memory tool finds them. Its status, resume
  and session-stamp markers sit at `{stm_base}<issue>/status/`; its sub-play results under
  `{stm_base}<issue>/context/understand/start/` and `…/end/`. Run by hand, nothing is written
  to short-term memory before `start-change` gives the issue: what the pre-flight and the
  questions (Step 0a) record is held in a scratch folder outside `.garura/`, moved into the
  working root right after Step 0, and deleted on a halt before it — so a stop before Step 0
  still leaves no issue, no branch and no stray files. Resume finds the run through the
  branch's issue.

- C16 — The screens decide the functionalities (Kapil, 2026-10-20, after Kickoff run 7:
  "you engineered a functionality called 'Build-from vs waiting split' — where on the
  prototype is this functionality?"). Handed a prototype's capture, each functionality is
  something a person does or sees on its screens, named in its users' words; one panel, count
  or label is a part of the functionality that shows it, never a functionality of its own;
  nothing the screens do not show and no shelf holds is written. Every page the run writes
  carries `## Sources`: each screen it is seen on with the exact words there. A behaviour the
  screens do not show is written as our default, marked as ours — never left as an open
  question; only a business rule an agent intent cannot be written without, and that nothing
  shows or holds, is the drive's question (C13).

### Failure conditions

- F1 — The run details a capability with no basis: an absent capability was seeded without
  the person's recorded answers (or under a domain not in the spine), or a capability that
  is already `detailed` was re-detailed.
- F2 — A grounding doc fails its template/shape, or a spine entry fails the spine schema or
  the spine↔doc consistency check.
- F3 — A grounding doc fails the content-quality eval.
- F4 — The capability was not promoted (its entry left `detail: directional`), or a
  functionality was created without both a spine entry and a detailed `functionality.md`.
- F5 — An NFR need is non-concrete (no level, no measurable target, or no gate), or NFR
  needs were written globally instead of on the capability.
- F6 — A profile dimension was lowered, or the box was firmed to a state other than `set`
  (left `directional`, or written `locked`).
- F7 — Against a `set` box, an out-of-box need was persisted without the checkpoint gate
  resolving for it — no typed approval, no recorded config skip, no recorded policy
  auto-pass, and — inside a drive — no recorded deferral to the drive's review; or, inside
  a drive, a box-move decision was written `accepted` instead of `proposed`.
- F8 — A box-move was persisted without its own decision record, or a decision omits the
  dimension or the from→to it represents.
- F9 — Allowlist breach: a capability, functionality, or domain other than the targets (and
  their new functionalities) was changed during the run.
- F10 — Over-reach into prioritization: a slice or an epic was written, or a target
  capability's status was flipped to active — that is /shape's job.
- F11 — The run closed COMPLETED without the Done means held (no persist record, the
  profile roll-up not stamped as written, the scoped-write guard report not captured or not
  ok, or the model delta not committed).
- F12 — A conditional-gate crossing left no live-eval ledger line, or an auto-pass fired
  for a shape the policy does not list as auto (or that carried a blocking finding).
- F13 — The play ran against a dirty product-os tree (uncommitted model edits present at
  entry), so the change-shape and the scoped guard could not be trusted to reflect only
  this run's delta.
- F14 — Inside a drive, the play opened an issue or a branch, ran the end sequence, waited at
  its checkpoint, or worked on a branch other than the drive's; or, run by hand, it skipped
  its opening, its checkpoint or its end sequence.
- F15 — Inside a drive, the checkpoint left no review record in the drive's `review_dir`,
  the record differs from what the checkpoint would have shown (a box-move missing as its
  own line), the gate ledger has no line for the crossing, or a line records an approval no
  person gave; or the play picked an answer — a seed's what, why or domain — that the drive
  had not given.
- F16 — The run left out a pending capability it should have taken (none named, yet a
  `detail: directional` capability was not a target), took one the person did not name, or
  measured a target against a box another target in the same run had raised (a box-move
  hidden); or it committed some targets while another failed its checks; or an enrichment
  dispatch wrote outside its target's write scope or wrote a shared file.
- F17 — The run wrote short-term memory outside its issue's folder: a working file, a person's
  answer, a status marker or a sub-play result under any other folder of the short-term root,
  or, run by hand, anything written to short-term memory before `start-change` gave the issue.

- F18 — A functionality is one panel, count or label of a screen made into a function of its
  own, or something no screen shows and no shelf holds; a page the run wrote has no
  `## Sources`, or quotes words the prototype does not have; or a behaviour the screens do not
  show was left as an open question instead of a marked default.

## Expectation

### Success scenarios

- S1 — (product manager, detail + functionalities) Given directional capabilities, when
  /understand runs and the checkpoint is approved, then each is detailed (its
  `capability.md` promoted, its spine entry `detail: detailed`) and its functionalities are
  created (each a spine entry plus a detailed `functionality.md`), all conforming to their
  templates and clearing the content-quality eval. Measure: every target entry is
  `detail: detailed` and carries `nfr_needs`; each target has at least one functionality
  entry with `capability` set to it and its doc present; the linter is clean; the content eval
  gate passes for every grounding doc; the run's change is landed on main by the injected
  end sequence (merge-change reports the PR merged); the stop-condition verdict reads held.
- S2 — (product strategist, first firm-up) Given a still-directional profile, when
  /understand runs and is approved, then the roll-up establishes the box and firms it to
  `set` with no per-dimension ADR. Measure: the profile `state` is `set`; no decision
  record was written this run.
- S3 — (architect, out-of-box move) Given an already-`set` box and targets whose needs
  exceed it on a dimension, when /understand runs, then it halts at the checkpoint
  surfacing each capability's box-move as its own line item, and on approval the box is
  raised and a product-level decision records each move. Measure: for each target over the
  starting box, a decision exists with level `product`, its `node_ref` that capability, a
  from→to on the named dimension starting at the run's starting level, and status
  `accepted`; the profile's level on that dimension equals the highest need.
- S4 — (product owner, non-destructive) Given several capabilities already detailed, when
  /understand runs on more, then only the targets (each doc + entry), their new
  functionalities, the profile, and the box-move decisions change — and no dimension of the
  box is lowered. Measure: a before/after diff of the spine shows changes only to the target
  capabilities, their new functionalities, the profile, and decisions; every profile dimension
  level is greater than or equal to its pre-run value.
- S5 — (reviewer, the checkpoint) Given the detailed grounding and the profile changes are
  ready, when the checkpoint is presented, then it shows each detailed capability, its
  functionalities, its NFR needs, and, for each box-move, an explicit line naming the
  capability, the dimension, the from→to levels, and the ADR it will create — rendered inline,
  over the full written delta. Measure: each box-move appears as its own line item; no
  product-model change is COMMITTED before the approval, and on cancel the working tree
  returns byte-clean to HEAD (`git restore` + `git clean`) — or, on the auto-pass path (a
  policy-listed shape), the gate resolves with no wait and the recorded auto-pass, the
  appended ledger line, and the diff summary stand in the approval's place.
- S6 — (product manager, nothing run first) Given a capability that is not in the model and
  no earlier play run, when /understand runs by hand and the person answers what the
  capability is, why it matters, and its domain, then it seeds the capability thinly from
  those answers, details it in the same run, and lands the change on main. Measure:
  `<working>/seed.yaml` holds the person's answers; the persist record reads `seeded: true`;
  the spine entry exists under the named domain with `detail: detailed`; merge-change reports
  the PR merged; the stop-condition verdict reads held.
- S7 — (Kickoff drive, inside a drive) Given a drive hands /understand its contract — the
  drive's branch, its issue, its `review_dir`, and any seed answers — when /understand runs,
  then it details every pending capability in one run, opens nothing, does not stop at its
  checkpoint, commits its model delta on the drive's branch and leaves one review record per
  capability for the drive's review, with every box-move as its own line and its decision
  `proposed`. Measure: `run.json` reads `in_drive: true` with the contract's `drive_run_id`
  and branch; no `start-change` or end-sequence step ran and the current branch equals the
  contract's branch; for each target a `<review_dir>/understand-<ts>-<capability>.json`
  record exists with `decided: false` and its summary file; the gate ledger's line for the run reads `deferred_to_drive_review` (or
  `auto_pass` on a policy-listed shape); every decision in `persist-manifest.json`
  `box_moves` reads `proposed`; the model delta is committed on the drive's branch; the
  stop-condition verdict reads held. Run by hand, the same play's `run.json` reads
  `in_drive: false` and every step ran as before.
- S8 — (product manager, many at once) Given three capabilities /vision seeded and nobody
  has detailed, and two of them need more security than the set box allows, when
  /understand runs with none named, then one run details all three, shows both box-moves at
  one checkpoint and makes one commit. Measure: `targets.json` lists the three in spine
  order; every one reads `detail: detailed`; `rollup.json` holds one box-move per capability
  over the box, each from the starting level; `persist-manifest.json` `changed.capabilities`
  lists the three; one `feat(model)` commit holds the whole delta; the stop-condition verdict
  reads held.

- S9 — (product manager, from a prototype) Given capabilities to detail and a prototype's
  capture, when /understand runs, then each functionality is something a person does or sees
  on the screens, every page says where it is seen, and nothing is left as an open question.
  Measure: `check_sources.py` over every target's manifest, with `--source-text`, exits 0;
  the rebuild eval's review reads no functionality `invented` or `panel`.

### Done means

Paths are relative to the run's working root (`{stm_base}<issue>/context/understand/<run ts>/`, C15).
`persist-manifest.json` is the record the keyed persist script writes before the checkpoint
(its contract: `written`, `capability_refs`, `seeded`, `changed.{capabilities,
functionalities_added, profile, decisions}`, `box_moves`) — every target's detailed
grounding, its functionality docs, and the profile roll-up, all written in place on the
live model; `guard-report.json` is the captured `scoped_write_guard.py` output — the play
always writes it, and its `ok` field is the mechanical proof that no model path changed
outside the targets' scope (the allowlist held). Node-level promotion, concrete needs,
monotonic-up box to `set`, and each box-move's accepted decision are stamped in the persist
record.

- D1 — says: "the persist record exists — every target's detailed grounding, its
  functionality docs, and the roll-up were written in place on the live model"
  check: { type: artifact_exists, path: "persist-manifest.json" }
- D2 — says: "the profile roll-up was persisted — the persist record stamps the firmed box"
  check: { type: field_equals, file: "persist-manifest.json", field: "changed.profile", equals: true }
- D3 — says: "the scoped-write guard held — no model path changed outside the targets' scope"
  check: { type: field_equals, file: "guard-report.json", field: "ok", equals: true }

### Recovery (one per failure condition)

- REC1 (F1) — trigger: an absent capability has no recorded answers, its domain is not in the
  spine, or the target is already `detailed`. direction: ask the person what the capability
  is, why it matters, and which existing domain it belongs to, and record the answers before
  seeding; with no answer or no such domain, halt and say plainly what is needed — inside a
  drive, write it to `open-understand.json` as the drive's question and detail the other
  targets (C13); for an already-detailed capability, halt — it is not re-detailed. handoff: human.
- REC2 (F2) — trigger: a grounding doc fails shape, or a spine entry fails the schema or
  spine↔doc consistency. direction: re-emit the failing doc or spine entry to conform and
  restore consistency before the checkpoint. handoff: autonomous.
- REC3 (F3) — trigger: a grounding doc fails the content-quality eval. direction: rewrite
  the failing doc to the judge's cited fixes — raise each flagged section to a
  self-explaining, product-manager-altitude statement — and re-judge until the gate passes.
  handoff: autonomous.
- REC4 (F4) — trigger: the capability stayed directional, or a functionality lacks its entry
  or its doc. direction: complete the promotion (flip the entry to `detail: detailed`) and
  emit the missing functionality entry or doc before the checkpoint. handoff: autonomous.
- REC5 (F5) — trigger: an NFR need has no level/target/gate, or needs were written off the
  capability. direction: re-draft each need on the capability as a concrete level + target +
  gate. handoff: autonomous.
- REC6 (F6) — trigger: a dimension was lowered, or the box was firmed to a non-`set` state.
  direction: recompute the roll-up monotonic-up (max per dimension) and firm to `set`; never
  lower a dimension. handoff: autonomous.
- REC7 (F7) — trigger: an out-of-box need against a `set` box was persisted with no approved
  decision. direction: revert the box change, surface the move at the checkpoint, and persist
  only after a human approves it (inside a drive, re-write the decision as `proposed` and
  record the deferral). handoff: human.
- REC8 (F8) — trigger: a box-move lacks its decision record, or a decision omits the
  dimension or from→to. direction: write (or complete) the product-level decision for each
  move with its dimension and from→to before persisting. handoff: autonomous.
- REC9 (F9) — trigger: a capability, functionality, or domain other than the targets was
  changed. direction: restore the other artifact and re-run writing only the target
  capabilities and their functionalities, after a human confirms the restore. handoff: human.
- REC10 (F10) — trigger: a slice, an epic, or a capability status flip was written.
  direction: strip the prioritization over-reach — remove the slice/epic, reset the status —
  leaving only /understand's detailing scope. handoff: autonomous.
- REC11 (F11) — trigger: the run is about to close COMPLETED with the Done means unmet.
  direction: close HALTED with `exit_reason: stop_condition_unmet` and the unmet clauses
  named; fix the state — re-run the keyed persist, re-capture the scoped-write guard report,
  or make the model-delta commit — and re-evaluate; the close stays HALTED until the verdict
  reads held. handoff: autonomous.
- REC12 (F12) — trigger: a crossing left no live-eval ledger line, or an auto-pass fired
  for a shape not listed `auto:` in the policy (or one carrying a blocking finding).
  direction: re-append the missing ledger line for the recorded crossing; when the
  auto-pass was unearned, re-run the gate as a live wait — render the approval prompt
  and wait for the typed response — before proceeding. handoff: autonomous.
- REC13 (F13) — trigger: the product-os tree is dirty at entry (uncommitted model edits
  present). direction: halt at pre-flight and ask for a clean model tree — commit or revert
  the pending model edits — before /understand proceeds. handoff: human.
- REC14 (F14) — trigger: inside a drive the play opened an issue or branch, ran the end
  sequence, waited at its checkpoint, or worked off the drive's branch; or by hand it skipped
  a step. direction: inside a drive, close the stray issue and branch, switch to the drive's
  branch, and write the review record in place of the wait; by hand, run the skipped step.
  handoff: human.
- REC15 (F15) — trigger: no review record, a record that differs from the checkpoint (a
  box-move missing as its own line), no ledger line, an approval no person gave, or an
  answer the play picked itself. direction: re-render the checkpoint and re-write the review
  record with `write_drive_review.py`; append the missing `deferred_to_drive_review` line, or
  a correction refuting a made-up approval; drop the picked answer and hand the question to
  the drive (`open-understand.json`; run by hand, ask the person).
  handoff: autonomous.
- REC16 (F16) — trigger: a pending capability left out, an unnamed one taken, a target
  measured against a box raised in the same run, a part of the run committed while another
  target failed, or a dispatch that wrote outside its write scope or a shared file.
  direction: re-pick the targets with `pick_targets.py`, re-run the roll-up with every
  target's manifest against the starting box, and re-render the checkpoint; when a target
  failed or a dispatch strayed, revert the uncommitted delta and halt the whole run.
  handoff: autonomous.
- REC17 (F17) — trigger: a working file, an answer, a marker or a sub-play result sits outside
  `{stm_base}<issue>/`, or something was written to short-term memory before Step 0 gave the
  issue. direction: move it into the issue's working root (or status folder), delete the stray
  copy, and continue; when the issue is not known yet, hold it in the scratch folder until
  Step 0. handoff: autonomous.


- REC18 (F18) — trigger: a panel made a functionality, a functionality no screen shows, a page
  with no sources or a quote not on the prototype, or a question left open. direction: fold
  the panel into the functionality that shows it; drop what nothing shows; write each page's
  sources with the screen's own words; replace the open question with our default, marked as
  ours. handoff: autonomous.
