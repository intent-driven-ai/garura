# vision — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
play-editor; never hand-edit the compiled SKILL.md.

## Intent

Given business intents (by id, or /intent's save record), a business goal typed as text, or
both, plant or grow the product model as the **CXO conversation**: what you take to a CXO and
get back. Write a **detailed domain** grounding doc (the problem the domain owns, the bet, its
operating principles, the directional capabilities, the scope), name the candidate
**capabilities and give each only its directionality** (what it is about, the rough direction
of its scope, why it matters), lay down the matching **spine** entries (a domain + its
capabilities), and sketch a **directional product profile**. Ground the domain and
capabilities in the KB domain shelves rather than inventing them. Present the proposed change
at a single human checkpoint and commit it to the product model only on approval.

One model, and nothing waits (#637; ADR 031 parts 2–3; ontology v3). /intent and /vision write
the same tree — domain → capability → functionality, the business intents beside it, one
spine — and neither needs the other to run first. Each play writes what it knows at the depth
it knows it, and a later play adds to it. So /vision starts from whatever the model already
holds:

- **Business intents** — the goal is drawn from the intent pages (title, outcome, why). An
  intent may be only proposed (inside a drive the person confirms at the drive's end review),
  so /vision never waits for a confirmation and never runs the workable check.
- **Capabilities already in the model** — written by /intent or any play, under a domain or,
  when their domain was not known, in the holding folder `capabilities/<id>/capability.md`.
  /vision treats them as candidates that already exist and matches the KB's candidates
  against them, so the same thing is never added twice.
- **Domains already in the model** — a light (directional) domain page is raised to the full
  page, keeping what it said; a full page may be extended.

and it grows them at its own depth: it **places** each capability with no domain — sets the
domain, moves its page unchanged from the holding folder into the domain's folder
(`<domain-slug>/<capability-slug>/capability.md`), points the spine at the new place, and fixes
the link to that page on the intent pages that name it; it may add light, directional detail to
a capability page another play wrote; and every capability it adds names the intents it serves
(`intents`) when it started from intents. Anything it finds missing, thin or odd — an intent
page that is gone, a capability it could not place — is recorded as a warning for the
Alignment drive. A write is never blocked, and nothing another play did or did not do stops
the run.

Everything here is strategic and directional — CXO altitude. Detailing a capability and
introducing its functionalities is the **product manager's** work (/understand, the last
detailing step); breaking the detailed model into deliverable end-to-end verticals and
epics is the **product owner's** work (/shape). The play writes nothing at those
altitudes.

The grounding docs are the unit of meaning: each conforms to its locked template and
must clear the **content-quality eval** (a judge), so a thin or label-only doc cannot
pass. Structure lives in the spine; meaning lives in the docs.

Pipeline position: **both**. /vision stands on its own (ADR 029 §4; #616): run by hand, it opens its own change and lands it. The D2 rule prepends `start-change` — resolve or create the issue, cut the branch off fresh main, optional worktree, init STM — and, after the model delta is committed, appends the close sequence `commit-change → propose-change → review-change → merge-change`, landing the change on main. No later play needs to run for /vision's work to be finished: /understand and the plays after it start from main. It writes the persistent product model **directly, in place** on the started branch — there is no draft copy and no apply/promote step; review is the branch git diff and the end PR. (#437, #500, ADR 026; position changed from start to both in #616.)

Write discipline (ADR 026, `standards/rules/direct-model-write.md`): the LLM authoring skill writes ONLY the per-node grounding docs (`domain.md`, `capability.md`) straight to the live model — new docs, and updates to existing docs at its altitude that keep what was there; it never removes a doc and never writes a shared file. Every shared-file mutation (the spine `_spine.yaml`, including its `profile` block) and every page move is done by the deterministic keyed persist script, in place: it adds entries whose id is absent and the profile only if none exists, makes only the named updates to an existing entry, places holding-folder capabilities, and refuses anything else (the node-level containment the file-level scoped guard cannot see inside the shared spine). Containment is a post-write scoped guard over the full delta (`scoped_write_guard.py`) plus a keep check over every existing doc the run changed, not a draft. Clean tree in, committed delta out: the product-os tree is asserted clean once start-change has cut the fresh branch, and after the approved checkpoint the play commits its own model delta on the branch, so the working-tree diff vs HEAD is exactly this run's delta and the end sequence lands exactly that delta.

### Constraints

- C1 — Conformance: every grounding doc the play writes or changes conforms to its locked
  template (`domain.md` → the Theme template's **detailed** stage; `capability.md` → the
  capability template's **directional** stage) and every spine entry the keyed persist adds
  or updates conforms to the spine schema, with the spine and the docs consistent (each
  entry points at an existing doc of the matching kind and stage). The structural linter
  passes; its "no domain yet" warning is not a failure.
- C2 — Content quality: every grounding doc the play writes or changes clears the
  content-quality eval, not just the linter — each section is self-explaining at CXO
  altitude per the content standard (it names the thing AND explains why it matters), and
  the whole doc passes the stranger test. A label-only or thin doc fails. A page the play
  only moves, unchanged, is not re-judged.
- C3 — Altitude and scope: the play writes the **domain in full** and the
  **capabilities directionally only**. It never writes a functionality, never details a
  capability, never writes acceptance criteria — those belong to /understand and /shape. On
  a capability page another play wrote it may add light directional detail that keeps what
  the page said; the page stays at the directional stage.
- C4 — Directional state: capability entries carry `status: proposed` and
  `detail: directional`; a domain entry the play writes or raises carries `detail: detailed`;
  the profile carries `state: directional` (shape dimensions + rough NFR levels only). The
  play never writes `active`, `set`, `locked`, or a capability at `detail: detailed`, and it
  never lowers an entry's `detail`.
- C5 — Grounded, not invented: domains and capabilities are grounded in the KB domain
  shelves. A capability matching a shelf cites it; a genuinely new domain or capability
  absent from the KB is recorded as a KB-node proposal — never silently invented. This
  covers every capability the run adds, places or changes, its own and the ones another play
  wrote: each is recorded in the seed manifest with its shelf match or its proposal.
- C6 — Keep what is there, enforced by the containment split, the keep check and the
  post-write scoped guard: the LLM authoring skill writes only per-node grounding docs and
  never a shared file; a doc that exists is updated in place, keeping every section it had,
  never removed. The keyed persist script adds spine entries whose id is absent and the
  profile only if none exists; on an existing entry it makes only these updates — set an
  empty `domain`, repoint `doc` to a moved page, raise `detail` (never lower it), refresh
  `one_line`, add to `intents` — and never removes an entry or changes an `id`; moving a
  capability already under one domain to another is alignment work, recorded as a warning; it moves a
  placed capability's page byte-identical from the holding folder into its domain's folder,
  and on an intent page it rewrites only the link to that moved page. After ALL writes and
  before the checkpoint, the bundled keep check (`check_kept.py`) confirms every existing doc
  the run changed kept each section it had, and `scoped_write_guard.py` diffs the model tree
  against HEAD and FAILS the run (reverting the offending paths) if any model path changed
  outside the run's write scope — grounding docs may be added or changed, never removed
  (`--add-only` + `--modify-only`); holding-folder pages may only be removed (`--remove-only`);
  intent pages may only be changed (`--modify-only`); the spine `_spine.yaml` (with its
  profile block) is `--allow`. A re-run with nothing new to add changes nothing.
- C7 — Exactly one human checkpoint, presenting the domain, the directional
  capabilities, and the directional profile. The checkpoint is a **conditional gate**
  (#467; `gate-config.md` three gate kinds — /vision is one of the eleven conditional
  document plays). Resolution order: pinned (n/a here) → the `gates.plays` override →
  the learned policy (classify the working-tree change shape — the model tree's diff vs
  HEAD — with the bundled `classify_change.py` (`--product-base`/`--base-ref HEAD`); a
  shape in `gate-policy.yaml`'s `auto:` and not in `never_auto:`, with NO blocking finding
  — a lint gap or a content-eval fail — auto-passes with the skip and the diff summary
  recorded) → `gates.classes.standard` → `gates.default`. EVERY crossing appends one
  live-eval line via the bundled `gate_eval.py` (shape, predicted gate|auto, the human's
  real action `approved_clean|approved_edited|rejected`, or `auto_pass`). Write-then-review
  (ADR 026): the run writes the full delta to the live model FIRST (docs by the authoring
  skill, the spine + profile by the keyed persist), so the checkpoint presents the real
  model git diff and the change-shape is classified over the full delta; nothing is
  COMMITTED before the gate resolves — a typed approval, a recorded config skip, OR a
  recorded policy auto-pass. On cancel the whole model delta is reverted (`git restore` +
  `git clean` over the model paths via the guard `--restore` with an empty allow set) — the
  branch, issue, and STM that start-change created are its own committed side effects and
  are left as-is. At close the play refreshes the learned policy with the bundled
  `distill_gate_policy.py` (config `gates.conditional`: streak/ledger/policy paths).
- C8 — The play ends by proving its Done means at close (gated, #464): the seed was
  written in place on the live model (the keyed persist record exists and stamps the write
  applied) and the scoped-write guard report reads ok (the allowlist held). The play then
  commits its own model delta on the branch. The close never reads COMPLETED with the
  stop-condition verdict unmet. After the model-delta commit, the injected end sequence
  (commit → propose → review → merge) lands the change on main; each member proves its own
  Done means, and a review reject stops the chain before merge. This per-play Standard Play
  Close (evidence + delivery report) runs after the end sequence and is distinct from it.
- C9 — Clean tree in, committed delta out (ADR 026): once start-change has cut the fresh
  branch, the product-os tree is asserted clean (a dirty model tree halts), so HEAD is a
  correct base for the scoped guard and the change-shape; and after the approved checkpoint
  the play commits its model delta on the branch (`feat(model): … (#<issue>)`), so the end
  sequence lands exactly this run's delta. This model-delta commit is a lightweight persist
  step, distinct from both the end sequence and the Standard Play Close.
- C10 — Starts from whatever is there, and never blocks: the play takes business intents,
  a typed goal, or both (with neither, it asks for a goal, as before). It reads the named
  intents with the bundled `read_intents.py`, accepting a `proposed` intent like a
  `confirmed` one; it never runs the workable check and never waits for a confirmation. It
  never refuses, stops, or fails its close because another play did or did not run first,
  or wrote something light — a missing intent page, a capability it cannot place, or
  anything odd is recorded as a warning in the persist record, for the Alignment drive. A
  KB candidate that matches a capability already in the model is recorded as the same
  thing (`same_as`) and never added again. Every part the run links to an intent is linked
  both ways: the part's spine `intents` names the intent, and the intent page's Touches list
  names the part, marked `adds` (written by this run) or `changes` (already there) — both
  written by the keyed persist script, never by hand. Each capability built from an input
  intent that had no domain is placed under one, or has a warning saying why not.

### Failure conditions

- F1 — A grounding doc fails its template/shape (missing, extra, or out-of-order
  heading; an empty or telegraphic section), or a spine entry fails the spine schema or
  the spine↔doc consistency check.
- F2 — A grounding doc fails the content-quality eval: a section is a label rather than
  an explanation, is written above or below CXO altitude, or the doc fails the stranger
  test.
- F3 — Scope over-reach: a functionality, a detailed (non-directional) capability,
  acceptance criteria, a profile in state `set`/`locked`, or a capability marked
  `detail: detailed` was written, or an entry's `detail` was lowered.
- F4 — A capability is neither grounded in a KB domain shelf nor recorded as a KB-node
  proposal.
- F5 — Allowlist breach: a model path outside the run's write scope changed (a grounding
  doc removed, a holding-folder page changed instead of moved, an intent page added or
  removed, any other file) — the scoped-write guard's report is not ok; or an existing doc
  the run changed lost a section it had — the keep check's report is not ok; or the persist
  changed an existing spine entry beyond the named updates (an entry removed, an `id`
  changed, `detail` lowered, an intent link removed), a moved page's bytes changed, or an
  intent page changed beyond its Touches list and the links to a moved page.
- F6 — The model delta was COMMITTED before the checkpoint gate resolved (no typed
  approval, no recorded config skip, and no recorded policy auto-pass), or a cancelled
  checkpoint left model writes on the working tree instead of reverting them.
- F7 — The close proves nothing — the play closes COMPLETED without the Done means held
  (no persist record, the persist not stamped applied, the scoped-write guard report not
  captured or not ok, or the model delta not committed).
- F8 — A conditional-gate crossing left no live-eval ledger line, or an auto-pass
  fired for a shape the policy does not list as auto (or that carried a blocking
  finding).
- F9 — The play ran against a dirty product-os tree (uncommitted model edits present once
  start-change had cut the branch), so the change-shape and the scoped guard could not be
  trusted to reflect only this run's delta.
- F10 — The play blocked on another play's work: it refused, stopped, waited or closed
  HALTED because an intent was only proposed, an intent page or a domain was missing or
  light, a capability sat in the holding folder, or no intents were given at all — or it ran
  the workable check.
- F11 — A link or a gap was left silent or one-sided: a second capability was added for one
  already in the model; a part linked to an intent is missing from the intent's Touches list,
  or the intent is missing from the part's spine `intents`; a capability built from an input
  intent was left with no domain and no warning saying why.

## Expectation

### Success scenarios

- S1 — (CXO / product strategist, end to end) Given a business goal with no existing
  domain for it, when /vision runs and the checkpoint is approved, then a detailed
  domain doc, a directional capability doc per capability, the matching spine entries, and
  a directional profile are written in place on the live model — all conforming to their
  templates and clearing the content-quality eval. Measure: the spine's `domains` holds one
  entry and its `capabilities` holds at least one with `status: proposed`,
  `detail: directional`, and `domain` set to the domain id; each entry's `doc` exists at its
  pointer and matches its kind and stage; the linter passes; the content eval gate passes
  for every grounding doc; the profile `state` is `directional`; the run's change is landed
  on main by the injected end sequence (merge-change reports the PR merged), with no later
  play needed to finish it; the stop-condition verdict reads held.
- S2 — (architect, grounding audit) Given the seed is written, when capabilities are
  inspected, then each traces to a KB domain shelf or a recorded KB-node proposal.
  Measure: the seed manifest names, for every capability written, either a KB shelf it
  matched or a propose-kb-node proposal created for it; none is left without one.
- S3 — (product owner, re-run keeps what is there) Given a domain already exists for the
  goal, when /vision runs again, then nothing already there is lost: new capabilities are
  added, existing entries change only by the named updates, and every existing doc the run
  touched keeps every section it had. Measure: the persist manifest's `written` list holds
  only newly-added entries, `updated` names each existing entry changed and the fields
  changed — all among the named updates — and every other pre-existing entry appears in
  `skipped`; the keep check and the scoped-write guard reports read `ok`; a re-run with
  nothing new leaves every model file byte-identical.
- S4 — (reviewer, the checkpoint) Given the proposed seed is written in place, when the
  checkpoint is presented, then it shows the domain, the directional capabilities, and the
  directional profile, rendered inline over the real model git diff. Measure: each of those
  sections is present in the checkpoint; no product-model change is COMMITTED before the
  approval, and on cancel the working tree returns byte-clean to HEAD (`git restore` +
  `git clean`) — or, on the auto-pass path (a policy-listed shape), the gate resolves with
  no wait and the recorded auto-pass, the appended ledger line, and the diff summary stand
  in the approval's place.
- S5 — (product strategist, after /intent) Given /intent saved business intents — some
  only proposed — with one capability under a light domain and one in the holding folder,
  when /vision runs from those intents, then the light domain page is raised to the full
  page keeping its intent, the holding-folder capability is placed under a domain and its
  page moved unchanged, every capability /vision adds names the intent it serves, no
  capability is added twice, and each intent page's Touches list names every part linked to
  it. Measure: `read_intents.py`'s record lists every input intent, proposed ones accepted;
  the persist manifest's `placed` list names the holding-folder capability with its old and
  new path and an unchanged hash, and `updated` names the raised domain (`detail` directional
  → detailed); every KB candidate matched to an existing capability is in the seed
  manifest's `same_as` and not in the spine-delta; for every intent, each part whose spine
  `intents` names it is on its Touches list and the reverse; the keep check and the guard
  read `ok`; no warning is needed and none is recorded.
- S6 — (founder, by hand, nothing else run) Given only a typed goal and an empty model, when
  /vision runs, then it seeds the model exactly as before — no intents are needed. Given
  intents whose pages are gone, the run still completes and records one warning per missing
  page. Measure: the run closes COMPLETED in both cases; the second run's persist manifest
  lists the missing pages in `warnings`.

### Done means

Paths are relative to the run's working folder (`<working>`, under
`{stm_base}_shaping/vision/<product_slug>/`). `persist-manifest.json` is the record the
keyed persist script writes after the approved checkpoint (its contract: `applied`,
`written`, `skipped`, `changed`) — the seed's grounding docs written in place on the live
model and the spine/profile merged additively; `guard-report.json` is the captured
`scoped_write_guard.py` output — the play always writes it, and its `ok` field is the
mechanical proof that no model path changed outside the seed's write scope (the allowlist
held); `kept-report.json` is the captured `check_kept.py` output, whose `ok` field proves every
existing doc the run changed kept each section it had. None of the clauses depends on what
another play did: warnings never make a clause unmet. A re-run over an existing domain writes only absent pieces, so `applied` is stamped
`true` even when the profile was skipped — the clauses assert the always-written records,
not per-node docs.

- D1 — says: "the persist record exists — the seed's grounding docs and spine/profile were written in place on the live model"
  check: { type: artifact_exists, path: "persist-manifest.json" }
- D2 — says: "the seed was persisted — the persist record stamps the write applied"
  check: { type: field_equals, file: "persist-manifest.json", field: "applied", equals: true }
- D3 — says: "the scoped-write guard held — no model path changed outside the seed's write scope (the allowlist held)"
  check: { type: field_equals, file: "guard-report.json", field: "ok", equals: true }
- D4 — says: "what was there was kept — every existing doc the run changed still has each section it had"
  check: { type: field_equals, file: "kept-report.json", field: "ok", equals: true }

### Recovery (one per failure condition)

- REC1 (F1) — trigger: a grounding doc fails the linter's shape check, or a spine entry
  fails the schema or spine↔doc consistency. direction: re-emit the failing doc or spine
  entry to conform to its template/schema and restore consistency before the checkpoint.
  handoff: autonomous.
- REC2 (F2) — trigger: a grounding doc fails the content-quality eval. direction:
  rewrite the failing doc to the judge's cited fixes — raise each flagged section to a
  self-explaining, CXO-altitude statement — and re-judge until it passes the gate.
  handoff: autonomous.
- REC3 (F3) — trigger: a functionality, a detailed capability, acceptance criteria, a
  `set`/`locked` profile, a `detail: detailed` capability, or a lowered `detail` appears.
  direction: strip the over-reach — drop the functionality, demote the capability back to
  directional, remove the acceptance criteria, reset the profile to `directional`, restore a
  lowered `detail` — leaving only /vision's scope. handoff: autonomous.
- REC4 (F4) — trigger: a capability has neither a KB shelf match nor a KB-node proposal.
  direction: search the KB to ground it, or record a propose-kb-node proposal; never
  leave it ungrounded. handoff: autonomous.
- REC5 (F5) — trigger: the scoped-write guard or the keep check report is not ok, or the
  persist refused an update outside the named ones. direction: the guard's `--restore`
  already reverted the offending paths; restore any doc that lost a section from HEAD and
  re-apply only the additions; re-run the keyed persist with only the named updates, after a
  human confirms the restore. handoff: human.
- REC6 (F6) — trigger: the model delta was committed before the checkpoint resolved, or a
  cancelled checkpoint left writes on the working tree. direction: revert the premature
  commit and the working-tree writes (guard `--restore`, empty allow set) and re-present
  the checkpoint; commit only after the human approves. handoff: human.
- REC7 (F7) — trigger: the close would report COMPLETED without the Done means held.
  direction: close HALTED with `exit_reason: stop_condition_unmet` and the unmet clauses
  named; fix the state — re-run the keyed persist, re-capture the scoped-write guard
  report, or make the model-delta commit — and re-evaluate; the close stays HALTED until
  the verdict reads held. handoff: autonomous.
- REC8 (F8) — trigger: a crossing left no live-eval ledger line, or an auto-pass fired
  for a shape not listed `auto:` in the policy (or one carrying a blocking finding).
  direction: re-append the missing ledger line for the recorded crossing; when the
  auto-pass was unearned, re-run the gate as a live wait — render the approval prompt
  and wait for the typed response — before proceeding. handoff: autonomous.
- REC9 (F9) — trigger: the product-os tree is dirty once start-change has cut the branch
  (uncommitted model edits present). direction: halt and ask for a clean model tree —
  commit or revert the pending model edits — before /vision proceeds with the seed writes.
  handoff: human.
- REC10 (F10) — trigger: the run refused, stopped, waited or closed HALTED over another play's
  work, or ran the workable check. direction: drop the check or the wait; record what was
  missing or light as a warning in the persist record and carry on with what is there.
  handoff: autonomous.
- REC11 (F11) — trigger: a capability added twice, a one-sided link, or an unplaced capability
  with no warning. direction: drop the duplicate and record `same_as`; re-run the keyed persist
  so it writes the missing side of each link; place the capability or record why it could not
  be placed. handoff: autonomous.
