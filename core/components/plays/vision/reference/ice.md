# vision — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
play-editor; never hand-edit the compiled SKILL.md.

## Intent

Given business intents (by id, or /intent's save record), a business goal typed as text, a
prototype's shared capture (its views and journeys, read once by the `prototype-reader`), or
any mix of them, plant or grow the product model as the **CXO conversation**: what you take to a CXO and
get back. /vision writes **domains only** (ADR 043 part 2): for each domain the product sits in
— the field it serves and the job it does there, often more than one — a **detailed domain**
grounding doc (the problem the domain owns, the bet, its operating principles, the kinds of
capability it covers in plain words, the scope), the domain's **spine** entry linked to the
intents it serves, and a **directional product profile**. Ground each domain in the KB domain
shelves — or, where no shelf holds it, in research that shows the world recognises it — and
never invent one; every domain page says where it comes from (`## Sources`). Present the
proposed change at a single human checkpoint and commit it to the product model only on
approval.

One model, every kind written on its own (ADR 043; ADR 031 parts 2–3; ontology v3–v4). Each
kind has one writer: /intent writes business intents, /vision writes domains, /understand
writes capabilities and functionalities. None needs another to run first; the links between
them are made later — inside a drive by the drive's gap skills, by hand by the person running
the next play. So /vision starts from whatever the model already holds:

- **Business intents** — the goal is drawn from the intent pages (title, outcome, why). An
  intent may be only proposed (inside a drive the person confirms at the drive's end review),
  so /vision never waits for a confirmation and never runs the workable check.
- **Domains already in the model** — a light (directional) domain page is raised to the full
  page, keeping what it said; a full page may be extended.
- **Capabilities already in the model** — read as context only (what the product is known to
  do). /vision never writes, places, moves or details a capability: a capability waiting
  without a domain stays where it is, not ready, until it is attributed (ADR 043).

Anything it finds missing, thin or odd — an intent page that is gone, an input intent no
domain serves — is recorded as a warning. A write is never blocked, and nothing another play
did or did not do stops the run.

Everything here is strategic and directional — CXO altitude. Writing and detailing the
capabilities and their functionalities is the **product manager's** work (/understand); breaking the detailed model into deliverable end-to-end verticals and
epics is the **product owner's** work (/shape). The play writes nothing at those
altitudes.

The grounding docs are the unit of meaning: each conforms to its locked template and
must clear the **content-quality eval** (a judge), so a thin or label-only doc cannot
pass. Structure lives in the spine; meaning lives in the docs.

The play reads no memory itself (ADR 039 §2); its agents and skills do the work. `product-os-keeper` routes the product to its domains and authors the domain pages through `search-kb`, `propose-kb-node` and `author-vision-seed`, reading memory only through the memory tool. The `template-manager` agent hands out every template the play needs — the approval prompt, each judged kind's grounding template, and the close's templates — as copies in the issue's short-term memory. Each content-quality judge is an isolated sub-agent running the `judge-grounding` skill, handed only the doc, its parent doc, and the kind's per-section guidance block cut from the template copy by a bundled script — never the template's gold example.

Pipeline position: **both**. /vision stands on its own (ADR 029 §4; #616): run by hand, it opens its own change and lands it. Inside a drive (ADR 029 §2–3; #614) it is handed the drive's contract (`standards/rules/drive-contract.md`) and opens nothing: no `start-change`, no end sequence, no wait at its checkpoint — it works on the drive's branch, commits its model change there, and keeps what its checkpoint would have shown as a review record for the drive's end review. The D2 rule prepends `start-change` — resolve or create the issue, cut the branch off fresh main, optional worktree, init STM — and, after the model delta is committed, appends the close sequence `commit-change → propose-change → review-change → merge-change`, landing the change on main. No later play needs to run for /vision's work to be finished: /understand and the plays after it start from main. It writes the persistent product model **directly, in place** on the started branch — there is no draft copy and no apply/promote step; review is the branch git diff and the end PR. (#437, #500, ADR 026; position changed from start to both in #616.)

Write discipline (ADR 026, `standards/rules/direct-model-write.md`): the LLM authoring skill writes ONLY the domain grounding docs (`domain.md`) straight to the live model — new docs, and updates to existing docs at its altitude that keep what was there; it never removes a doc and never writes a shared file. Every shared-file mutation (the spine `_spine.yaml`, including its `profile` block) is done by the deterministic keyed persist script, in place: it adds domain entries whose id is absent and the profile only if none exists, makes only the named updates to an existing domain entry, and refuses anything else — any capability, functionality, slice or epic entry above all (ADR 043) (the node-level containment the file-level scoped guard cannot see inside the shared spine). Containment is a post-write scoped guard over the full delta (`scoped_write_guard.py`) plus a keep check over every existing doc the run changed, not a draft. Clean tree in, committed delta out: the product-os tree is asserted clean once start-change has cut the fresh branch, and after the approved checkpoint the play commits its own model delta on the branch, so the working-tree diff vs HEAD is exactly this run's delta and the end sequence lands exactly that delta.

### Constraints

- C1 — Conformance: every domain grounding doc the play writes or changes conforms to its
  locked template (`domain.md` → the Theme template's **detailed** stage) and every domain spine
  entry the keyed persist adds or updates conforms to the spine schema, with the spine and the
  docs consistent (each entry points at an existing doc of the matching kind and stage). The
  structural linter passes; its "not ready until it is attributed" warning on a capability or
  functionality another play wrote is not a failure.
- C2 — Content quality: every grounding doc the play writes or changes clears the
  content-quality eval, not just the linter — each section is self-explaining at CXO
  altitude per the content standard (it names the thing AND explains why it matters), and
  the whole doc passes the stranger test. A label-only or thin doc fails. A page the play
  only moves, unchanged, is not re-judged.
- C3 — Altitude and scope: the play writes **domains only**, each in full (ADR 043 part 2). It
  never writes, names as an entry, places, moves or details a capability, never writes a
  functionality, never writes acceptance criteria — those belong to /understand and /shape. A
  domain page's Capabilities section describes, in plain words, the kinds of capability the
  domain covers; it names no capability entry.
- C4 — Directional state: a domain entry the play writes or raises carries
  `detail: detailed`; the profile carries `state: directional` (shape dimensions + rough NFR
  levels only). The play never writes `active`, `set` or `locked`, and it never lowers an
  entry's `detail`.
- C5 — Grounded, not invented: each domain is grounded in a KB domain shelf, or — when no
  shelf holds it — recorded as a KB-node proposal that names the domain as the industry or a
  known product category names it in the research it cites, never a name made from the
  product's own screens, its sample data or the words of the work. Each domain the run adds or
  changes is recorded in the seed manifest with its shelf match or its proposal, and its page
  ends with `## Sources` (its shelf or its research links) (#689).
- C6 — Keep what is there, enforced by the containment split, the keep check and the
  post-write scoped guard: the LLM authoring skill writes only domain grounding docs and never
  a shared file; a doc that exists is updated in place, keeping every section it had, never
  removed. The keyed persist script adds domain entries whose id is absent and the profile only
  if none exists; on an existing domain entry it makes only these updates — raise `detail`
  (never lower it), refresh `one_line`, add to `intents` — and never removes an entry or
  changes an `id`; it refuses any capability, functionality, slice or epic entry or update
  (ADR 043). After ALL writes and before the checkpoint, the bundled keep check
  (`check_kept.py`) confirms every existing doc the run changed kept each section it had, and
  `scoped_write_guard.py` diffs the model tree against HEAD and FAILS the run (reverting the
  offending paths) if any model path changed outside the run's write scope — domain docs may be
  added or changed, never removed (`--add-only` + `--modify-only`); intent pages may only be
  changed (`--modify-only`); the spine `_spine.yaml` (with its profile block) is `--allow`. A
  re-run with nothing new to add changes nothing.
- C7 — Exactly one human checkpoint, presenting each domain and the
  directional profile. (Inside a drive the checkpoint does not wait;
  it becomes a review record for the drive's end review — C11.) The checkpoint is a **conditional gate**
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
  COMMITTED before the gate resolves — a typed approval, a recorded config skip, a
  recorded policy auto-pass, OR, inside a drive, a recorded deferral to the drive's review
  (C11). On cancel the whole model delta is reverted (`git restore` +
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
  a typed goal, a prototype's capture, or any mix (with none, it asks for a goal, as before);
  from a capture it reads the domains from the screens themselves and needs no intents (C12).
  It reads the named intents with the bundled `read_intents.py`, accepting a `proposed` intent
  like a `confirmed` one; it never runs the workable check and never waits for a confirmation.
  It never refuses, stops, or fails its close because another play did or did not run first,
  or wrote something light — a missing intent page, an input intent no domain serves, or
  anything odd is recorded as a warning in the persist record. Every domain the run links to
  an intent is linked both ways: the domain's spine `intents` names the intent, and the intent
  page's Touches list names the domain, marked `adds` (written by this run) or `changes`
  (already there) — both written by the keyed persist script, never by hand.
- C11 — Runs inside a drive without stopping (ADR 029 §2–3; `standards/rules/drive-contract.md`):
  handed a drive's contract (`--contract`), the play checks it first with the bundled
  `check_drive_contract.py` — an invalid contract, or a current branch other than the
  drive's, halts — and records `in_drive` in `run.json`. Inside a drive it runs no
  `start-change` and no end sequence (the drive opens and lands the change); it takes its
  intents and goal from the contract's inputs and its answers from the contract's answers;
  it asserts the clean model tree at once; it resolves its checkpoint (C7) exactly as by
  hand — a config skip or a policy auto-pass is recorded as by hand — and only where the
  gate would WAIT does it not wait: it renders the checkpoint exactly as it would have been shown and writes it, with the files
  it stands on (the shape, the keep check, the guard report, the persist record), as a
  review record into the contract's `review_dir` with the bundled `write_drive_review.py`,
  and appends the crossing to the gate ledger as `deferred_to_drive_review` (the learner
  skips it until the drive's review writes the person's real answer). It still commits
  its model delta on the drive's branch (C9). A question neither the contract nor the model
  answers — no intents and no goal — is the drive's (ADR 041): the play writes it to
  `<review_dir>/open-vision.json` (drive contract, step 5), does what it does not block, and
  finishes; the drive asks the person only what none of its plays can answer. The play
  never picks an answer itself. Run by hand (no contract), every step runs as before.
  Either way, the run's short-term memory is the issue it works on (ADR 036 §1, ADR 039 §1):
  inside a drive the contract's `issue`, run by hand the issue `start-change` opens or
  resolves. The run's working folder is `{stm_base}<issue>/context/vision/<product_slug>/`,
  its status, resume and session-stamp markers sit in `{stm_base}<issue>/status/`, and its
  sub-play results in `{stm_base}<issue>/context/vision/start/` and `…/end/` — so every
  question and the person's answers live where the memory tool finds them. Run by hand,
  nothing is written to disk before `start-change` has given the issue; inside a drive the
  issue is known at pre-flight from the contract.

- C12 — Reads the product, not the sample (Kapil, 2026-10-21: "they can extract the domain and
  do not need intents to do that. looking at screens its easy to know which domain and what
  sort of functionality they need"). Handed a prototype's capture, the play reads what the
  product offers its user from the screens: the domains it sits in. It asks, in order, which
  field the product serves — judged by what its screens are about — and which job it does in
  that field; each may be a domain, so a product often sits in more than one (Kapil, same day,
  on a review tool for AI-built software: SDLC or Developer Experience as the field, Human
  Oversight and Product requirements management as the job), each with its own page and
  `## Sources`. The sample data on the screens is an example of what the product handles,
  never its domain.

### Failure conditions

- F1 — A grounding doc fails its template/shape (missing, extra, or out-of-order
  heading; an empty or telegraphic section), or a spine entry fails the spine schema or
  the spine↔doc consistency check.
- F2 — A grounding doc fails the content-quality eval: a section is a label rather than
  an explanation, is written above or below CXO altitude, or the doc fails the stranger
  test.
- F3 — Scope over-reach: a capability page, a capability or functionality spine entry or
  update, a capability placed or moved, acceptance criteria, or a profile in state
  `set`/`locked` was written, or an entry's `detail` was lowered (ADR 043).
- F4 — A domain is neither grounded in a KB domain shelf nor recorded as a KB-node proposal;
  or it is a name made up for this product — no shelf matched and no research names it — or
  its page has no `## Sources`.
- F5 — Allowlist breach: a model path outside the run's write scope changed (a domain doc
  removed, an intent page added or removed, a capability or functionality page written or
  moved, any other file) — the scoped-write guard's report is not ok; or an existing doc the
  run changed lost a section it had — the keep check's report is not ok; or the persist
  changed an existing spine entry beyond the named updates (an entry removed, an `id` changed,
  `detail` lowered, an intent link removed), or an intent page changed beyond its Touches list.
- F6 — The model delta was COMMITTED before the checkpoint gate resolved (no typed
  approval, no recorded config skip, no recorded policy auto-pass, and — inside a drive — no
  recorded deferral to the drive's review), or a cancelled checkpoint left model writes on
  the working tree instead of reverting them.
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
  light, or no intents were given at all — or it ran the workable check.
- F11 — A link or a gap was left silent or one-sided: a domain was added twice; a domain
  linked to an intent is missing from the intent's Touches list, or the intent is missing from
  the domain's spine `intents`; an input intent no domain serves was left with no warning.
- F12 — Inside a drive, the play opened an issue or a branch, ran the end sequence, waited at
  its checkpoint, or worked on a branch other than the drive's; or, run by hand, it skipped
  its opening, its checkpoint or its end sequence; or, either way, a run file (the working
  folder, a status marker, a sub-play result) lies outside the issue the run works on, or a
  file was written before `start-change` gave the issue.
- F13 — Inside a drive, the checkpoint left no review record in the drive's `review_dir`,
  the record differs from what the checkpoint would have shown, the gate ledger has no line
  for the crossing, or a line records an approval no person gave; or the play picked an
  answer to a question the drive had not answered.

- F14 — Handed a prototype's capture, the play named a domain after the sample data or the
  screens' own words, or missed the field the screens are about.

## Expectation

### Success scenarios

- S1 — (CXO / product strategist, end to end) Given a business goal with no existing
  domain for it, when /vision runs and the checkpoint is approved, then a detailed domain doc
  for each domain the product sits in, the matching domain spine entries, and a directional
  profile are written in place on the live model — all conforming to their templates and
  clearing the content-quality eval — and no capability is written. Measure: the spine's
  `domains` holds at least one entry at `detail: detailed`; each entry's `doc` exists at its
  pointer and matches its kind and stage; the run added no `capabilities` or `functionalities`
  entry; the linter passes; the content eval gate passes for every domain doc; the profile
  `state` is `directional`; the run's change is landed on main by the injected end sequence
  (merge-change reports the PR merged); the stop-condition verdict reads held.
- S2 — (architect, grounding audit) Given the domains are written, when they are
  inspected, then each traces to a KB domain shelf or a recorded KB-node proposal named from
  research. Measure: the seed manifest names, for every domain written, either a KB shelf it
  matched or a propose-kb-node proposal created for it; none is left without one; each domain
  page's `## Sources` names its shelf or a research link.
- S3 — (product owner, re-run keeps what is there) Given a domain already exists for the
  goal, when /vision runs again, then nothing already there is lost: new domains are added,
  existing domain entries change only by the named updates, and every existing doc the run
  touched keeps every section it had. Measure: the persist manifest's `written` list holds
  only newly-added entries, `updated` names each existing entry changed and the fields
  changed — all among the named updates — and every other pre-existing entry appears in
  `skipped`; the keep check and the scoped-write guard reports read `ok`; a re-run with
  nothing new leaves every model file byte-identical.
- S4 — (reviewer, the checkpoint) Given the proposed seed is written in place, when the
  checkpoint is presented, then it shows each domain and the directional profile, rendered inline over the real model git diff. Measure: each of those
  sections is present in the checkpoint; no product-model change is COMMITTED before the
  approval, and on cancel the working tree returns byte-clean to HEAD (`git restore` +
  `git clean`) — or, on the auto-pass path (a policy-listed shape), the gate resolves with
  no wait and the recorded auto-pass, the appended ledger line, and the diff summary stand
  in the approval's place.
- S5 — (product strategist, after /intent) Given /intent saved business intents — some
  only proposed — and a light domain, when /vision runs from those intents, then the light
  domain page is raised to the full page keeping its intent, every domain it writes names the
  intents it serves, no domain is added twice, a capability waiting without a domain is left
  exactly where it is, and each intent page's Touches list names every domain linked to it.
  Measure: `read_intents.py`'s record lists every input intent, proposed ones accepted; the
  persist manifest's `updated` names the raised domain (`detail` directional → detailed); for
  every intent, each domain whose spine `intents` names it is on its Touches list and the
  reverse; the holding-folder capability's page and entry are unchanged; the keep check and
  the guard read `ok`.
- S6 — (founder, by hand, nothing else run) Given only a typed goal and an empty model, when
  /vision runs, then it seeds the model exactly as before — no intents are needed. Given
  intents whose pages are gone, the run still completes and records one warning per missing
  page. Measure: the run closes COMPLETED in both cases; the second run's persist manifest
  lists the missing pages in `warnings`.

- S7 — (Kickoff drive, inside a drive) Given a drive hands /vision its contract — the
  drive's branch, its issue, its `review_dir`, the intents /intent saved and the answers to
  /vision's questions — when /vision runs, then it opens nothing, does not stop at its
  checkpoint, commits its model change on the drive's branch and leaves a review record for
  the drive's review. Measure: `run.json` reads `in_drive: true` with the contract's
  `drive_run_id` and branch; no `start-change` or end-sequence step ran and the current
  branch equals the contract's branch; a `<review_dir>/vision-<ts>.json` record exists with
  `decided: false` and its summary file; the gate ledger's line for the run reads
  `deferred_to_drive_review` (or `auto_pass` on a policy-listed shape); the model delta is
  committed on the drive's branch; the stop-condition verdict reads held; `run.json` sits in
  `{stm_base}<contract issue>/context/vision/<product_slug>/`. Run by hand, the same play's
  `run.json` reads `in_drive: false`, every step ran as before, and it sits in the folder of
  the issue `start-change` gave.

- S8 — (product strategist, from a prototype alone) Given only a prototype's capture — no
  intents, no goal — when /vision runs, then it names every domain the world recognises the
  product sitting in — the field its screens are about and the job it does there — each found
  by a shelf or by research. Measure: `grounding_check.py` run with `--product-base` exits 0 —
  every domain page's `## Sources` names its shelf or a research link and no capability was
  written; the rebuild eval's review reads `recognised: true` for the domain.

### Done means

Paths are relative to the run's working folder (`<working>`,
`{stm_base}<issue>/context/vision/<product_slug>/` — the issue the run works on). `persist-manifest.json` is the record the
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
- REC3 (F3) — trigger: a capability page, entry, update or placement, acceptance criteria, a
  `set`/`locked` profile, or a lowered `detail` appears. direction: strip the over-reach —
  drop every capability and functionality write (they are /understand's), remove the
  acceptance criteria, reset the profile to `directional`, restore a lowered `detail` —
  leaving only domains. handoff: autonomous.
- REC4 (F4) — trigger: a domain has neither a KB shelf match nor a KB-node proposal, is a
  made-up name, or its page lacks `## Sources`. direction: search the KB to ground it, or record
  a propose-kb-node proposal that names the domain from its research; write its sources; never
  leave it ungrounded. handoff: autonomous.
- REC5 (F5) — trigger: the scoped-write guard or the keep check report is not ok, or the
  persist refused an update outside the named ones. direction: the guard's `--restore`
  already reverted the offending paths; restore any doc that lost a section from HEAD and
  re-apply only the additions; re-run the keyed persist with only the named updates, after a
  human confirms the restore. handoff: human.
- REC6 (F6) — trigger: the model delta was committed before the checkpoint resolved, or a
  cancelled checkpoint left writes on the working tree. direction: revert the premature
  commit and the working-tree writes (guard `--restore`, empty allow set) and re-present
  the checkpoint; commit only after the human approves (inside a drive, only after the
  deferral is recorded). handoff: human.
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
- REC11 (F11) — trigger: a domain added twice, a one-sided link, or an input intent no domain
  serves with no warning. direction: drop the duplicate; re-run the keyed persist so it writes
  the missing side of each link; record the unserved intent as a warning. handoff: autonomous.
- REC12 (F12) — trigger: inside a drive the play opened an issue or branch, ran the end
  sequence, waited at its checkpoint, or worked off the drive's branch; or by hand it skipped
  a step; or a run file lies outside the issue the run works on. direction: inside a drive,
  close the stray issue and branch, switch to the drive's branch, and write the review record
  in place of the wait; by hand, run the skipped step; move any run file into the issue's
  folder (`context/vision/<product_slug>/`, `status/`).
  handoff: human.
- REC13 (F13) — trigger: no review record, a record that differs from the checkpoint, no
  ledger line, an approval no person gave, or an answer the play picked itself. direction:
  re-render the checkpoint and re-write the review record with `write_drive_review.py`;
  append the missing `deferred_to_drive_review` line, or a correction refuting a made-up
  approval; drop the picked answer and hand the question to the drive (`open-vision.json`;
  run by hand, ask the person). handoff: autonomous.

- REC14 (F14) — trigger: a domain named after the sample or the screens' words, or the field the
  screens are about missed. direction: route the product the screens offer again — the sample
  set aside — through the shelves and, when none fits, research for the domains the world names:
  the field first, then the job. handoff: autonomous.
