---
name: discover-capabilities
position: both
description: 'Write the product''s capabilities and features, each with its ICE (ADR 043) — read off a prototype''s screens when a capture is given (a capability with no domain yet waits in the holding folder, not ready until attributed), else every pending capability in the model or the ones the person names (a capability not yet in the model is seeded thinly here from the person''s answers) — promote each grounding from directional to detailed, create and detail its features, set each capability''s own NFR + compliance needs, and roll all those needs up together into the product profile, firming the box and recording a decision for each capability''s out-of-box move. The product-manager step, the last detailing step. Run by hand it needs no earlier play: it opens one change and lands it on main; handed a loop''s contract, it opens nothing, does not stop at its checkpoint, works on the loop''s branch and leaves one review record per capability — every box-move as its own line, its decision proposed — for the loop''s end review.'
user-invocable: true
---

# understand

Write the product's **capabilities and features**, each with its ICE (ADR 043: in
Discovery /discover-intent writes the business intents, /discover-domains the domains, /discover-capabilities the
capabilities and features). Given a prototype's capture, read the capabilities off the
screens first — no other play's seed is needed; one with no domain known waits in the
holding folder, not ready until it is attributed. Then take every target — those, every
pending (`detail: directional`) capability in the model, or the ones the person names — and
**detail them all in one run** (#615: one at a time is too slow).
A capability that is not yet in the model is seeded thinly first, from the person's own
answers (what it is, why it matters, which existing domain it belongs to), asked for — for
all of them at once — before any change is opened; its first `capability.md` is written
straight at the detailed stage. Never invented (#616 D1). /discover-capabilities is the
**product-manager** step, the last detailing step: for each target, promote its
`capability.md` from the directional stage to the detailed stage, **create its
features** (a spine entry plus a detailed `feature.md` each), and set its own
concrete NFR + compliance needs; then roll all the targets' needs up together into the
product profile, each measured against the box as it stood at the start of the run. On a
still-`directional` box the roll-up establishes the box and firms it to `set`; on an
already-`set` box, each capability's need that exceeds the committed ceiling halts for a
human decision that moves the box and records why. One run, one save, one checkpoint, one
commit — all or nothing (C14).

**Pipeline position: both.** /discover-capabilities stands on its own (ADR 029 §4; #616 D2): run by hand, it needs no other play to have run first. **Inside a loop** (ADR 029 §2–3; #615; `standards/rules/loop-contract.md`) the loop hands it a contract (`--contract`); then it runs no `start-change` and no end sequence, does not wait at its checkpoint (Step 6 writes one review record per capability for the loop's end review instead, every box-move as its own line and its decision `proposed`), and commits its model change on the loop's branch. Discovery runs it once for all the capabilities; the run leaves one review record per capability (ADR 029). The D2 rule prepends `start-change` — resolve or create the issue, cut the branch off fresh main, optional worktree, init STM — and, after the model delta is committed, appends the close sequence `commit-change → propose-change → check-change → merge-change`, landing the detailed capability on main. It writes the persistent product model **directly, in place** on its own started branch — there is no draft copy and no apply/promote step; review is the branch git diff and the end PR. (#437, #498, ADR 026; position changed from none to both in #616.)

**Write discipline (ADR 026, `standards/rules/direct-model-write.md`).** The LLM enrichment
skill writes ONLY the per-node docs (`capability.md`, `feature.md`) straight to the
live model; every shared-file mutation (the spine `_spine.yaml`, the profile, the box-move
decisions) is done by the deterministic keyed persist script, in place, keyed to the run's
target capabilities so it cannot touch any other node inside a shared file. The model tree is asserted
clean at entry (F13) and the play commits its own model delta at close (C12), so the
working-tree diff vs HEAD is exactly this run's delta. Containment is a post-write scoped
guard (`scoped_write_guard.py`), not a draft.

## Compiled From

This play was compiled from the understand ICE (`reference/ice.md`) by edit-play
(#466 Batch C, Level 3 rollout per ADR 025; #467 Batch B — the checkpoint upgraded to a
conditional learned gate, see `standards/rules/gate-config.md`; #498 — migrated to
direct-model-write per ADR 026 and `standards/rules/direct-model-write.md`; #616 — stands
alone: seeds an absent capability from the person's answers, and position none → both;
#615 — runs inside a loop, and one run details every pending capability). Intent defines
constraints (C1–C16) and failure conditions (F1–F18); the expectation defines success
scenarios (S1–S9), a Done means (D1–D3, baked to `stop-condition.yaml`), and one
recovery entry per failure condition. To modify this play, update `reference/ice.md`
and recompile with edit-play.
Do NOT edit this file manually — it is a compiled artifact.

## Role

You are the orchestrator. You own the workflow and the step order. You delegate the
domain work — grounded detailing and feature authoring — to the `product-os-keeper`
agent, once per target, via a JSON contract over files on disk, and you run the mechanical work (the shape
linter, the content-quality eval, the monotonic-up roll-up, the keyed in-place persist, and
the post-write scoped guard) through bundled scripts and an isolated judge. You never write
the grounding docs or the spine yourself, you never lower a box dimension, and you never
commit the model delta before the single checkpoint (C9) resolves — a typed approval, a
recorded config skip, a recorded policy auto-pass, or, inside a loop, a recorded deferral to
the loop's review (C13) — which also carries approval of any out-of-box box-move (C8).

**Forbidden:** hand-writing grounding docs or spine entries; touching any capability,
feature, or domain other than the run's targets and their new features (C10);
committing some targets while another failed (C14); measuring a target against a box another
target in the same run raised (C7/C8);
prioritizing — writing a slice or an epic, or flipping the capability to active (C2, that
is /shape-scope); persisting the shared files (spine/profile/decisions) by any route other than
`scripts/persist_understand.py`; committing before the checkpoint resolves; writing a
box-move decision `accepted` inside a loop (C8/C13); filling in a seed answer the person or
the loop did not give (C1/C13); running against
a dirty product-os tree (C12/F13); writing short-term memory outside the issue the run works
on, or before `start-change` gave it (C15/F17); closing COMPLETED without the stop-condition
verdict reading held (C11/F11).

**Agent boundaries:**

| Agent | Domain | Skill it invokes | Phases |
|-------|--------|------------------|--------|
| `product-os-keeper` | For one target per dispatch: recover the capability's KB shelf (re-route), then detail the capability (directional → detailed) writing the docs in place on the live model, author its features, and set its NFR + compliance needs (into its manifest) grounded in that shelf | `find-work-placement`, `enrich-capability-ice` | Enrich |

`product-os-keeper` is the single **domain agent** this play uses (1 of the ≤5
budget), dispatched once per target, all at once as a scoped-write fan-out (C14). No utility agents are needed — the git/issue machinery is the injected `start-change`
head and end sequence, run as sub-plays.
The content-quality judge always runs as an isolated, clean-context sub-agent (optionally
on a configured different model) — never the orchestrator's own context.

## Pre-flight

| Check | Constraint | Action on Failure |
|-------|-----------|-------------------|
| Resolve config + `product_base` (`.garura/core/config.yaml`) | — | Hard halt |
| Resolve `grounding-eval.judge` (optional model override) | C4 | Default: sub-agent on the session model |
| Loop contract: when `--contract <file>` is passed, `check_loop_contract.py` accepts it (valid, complete, current branch = the loop's branch) and writes `run.json` | C13/F14 | Hard halt (REC14) |
| Targets: `pick_targets.py` picks the named capabilities, else every pending (`detail: directional`) one, plus every one the capture's screens show (`--found`, Step 0b) and, inside a loop, every one the contract seeds; a named `detailed` target → halt; nothing pending → end at once; **absent** targets → ask the person for all of them first (Step 0a), before any change opens | C1/C13/F16 | Ask step, end at once, or hard halt (REC1) |
| **Clean model tree** — right after `start-change` (Step 0), or at once inside a loop, `git status --porcelain -- <product_base>product-os` is empty | C12/F13 | Hard halt (REC13) |
| **The run's issue** — inside a loop the contract's `issue`; run by hand the issue `start-change` gives at Step 0. Until then, run by hand, the run works in a scratch folder outside `.garura/` | C15/F17 | Hold in the scratch folder (REC17) |

**Clean-tree assertion (C12/F13, ADR 026).** Right after Step 0 (`start-change`) cuts the
fresh branch (inside a loop, at once — the earlier plays in the loop committed their model
change), before any model write, assert the product-os tree carries no uncommitted edits — `HEAD` is only a correct base for the scoped guard and the
change-shape if the tree is clean at entry:

```
test -z "$(git status --porcelain -- <product_base>product-os)" || { echo "HALT: dirty product-os tree (REC13)"; exit 1; }
```

If dirty, halt and ask for a clean model tree (commit or revert the pending model edits)
before /discover-capabilities proceeds. A dirty tree means uncommitted edits — never a missing
earlier play.

Resolve the pre-flight facts mechanically with the bundled resolver — do not derive
them by inference. The branch and issue come from Step 0 (`start-change`):

```
python3 scripts/preflight.py --play discover-capabilities --config .garura/core/config.yaml
```

It returns one JSON object of facts. /discover-capabilities reads `product_base` (the live model —
the spine `_spine.yaml` and the grounding docs), `stm_base` (working artifacts + evidence), the
resolved `grounding-eval.judge` config, and `evidence_record` (the D1 gate). The **targets**
are picked mechanically, right after the loop-contract check below (C1, #615):

```
python3 scripts/pick_targets.py --spine <product_base>product-os/_spine.yaml \
    --run <working>/run.json --working <working> \
    [--capability <id> ...] [--found <working>/found.yaml] --out <working>/targets.json
```

**Step 0b — Read the capabilities off the screens (ADR 043, C1/C16)** · Owner:
`product-os-keeper` · *only when a prototype's capture is given* (the contract's
`inputs.understand.capture`, or the play argument). Before the pick, dispatch the agent once;
it invokes `enrich-capability-ice` in find mode and writes nothing to the model:

    { "task":    "list every capability the capture's screens show, with the screens and their words",
      "inputs":  { "capture": "<the capture: source manifests, the write-up, journeys, view texts — read the write-up first>",
                   "spine": "<product_base>product-os/_spine.yaml", "mode": "find" },
      "outputs": { "found": "<working>/found.yaml" },
      "task_id": "find-capabilities" }

Each one not yet in the spine becomes a `found` target, seeded from that reading
(`answered_by: screens`): under its domain when one in the spine holds it, else in the
holding folder `capabilities/<id>/` with its domain empty. One already in the spine is
detailed as is; one already detailed is `skipped`.

The play argument names the targets (e.g. `/discover-capabilities checkout refunds`); with none named,
`targets.json` lists every capability in the spine at `detail: directional`, in spine order,
then every `found` one.
Then apply the policy: `refused` non-empty (a named target is already `detailed`) → halt
(REC1), it is not re-detailed; `nothing_pending: true` → end at once, opening nothing, and say
there is nothing to detail; `ask` non-empty → Step 0a asks the person for those, all at once,
before any change opens. A directional target is detailed as is.

**Run by hand or inside a loop (C13).** Check the loop contract first — always, so the run
records which path it takes:

```
python3 scripts/check_loop_contract.py --play discover-capabilities \
    --branch "$(git branch --show-current)" [--contract <contract.json>] \
    --out <working>/run.json
```

`run.json` reads `in_loop: false` with no contract — every step below runs as written. With
a valid contract it reads `in_loop: true` with the loop's `loop_run_id`, `branch`, `issue`,
`review_dir`, and /discover-capabilities's own `inputs` and `answers`. Inside a loop the targets
are picked as by hand, plus every capability the contract seeds; a seed's answers come from
`answers.seeds.<capability>` (`one_line`, `why`, `domain`), gathered by the loop before it
started — `pick_targets.py` writes them verbatim to that capability's `seed.yaml`. A non-zero exit (an invalid contract, or
the current branch is not the loop's) is a hard halt (REC14).

The run's working root (`<working>` below) is `{stm_base}<issue>/context/understand/<run ts>/`
(C15), where `<issue>` is the issue the run works on — the loop contract's `issue` inside a
loop, the issue `start-change` gives at Step 0 run by hand — and `<run ts>` is the run's own
UTC timestamp. **Run by hand, before Step 0** the issue is not known yet, so `<working>` is a
scratch folder outside `.garura/` (`mktemp -d`): the pre-flight and Step 0a write there, and
nothing is written to short-term memory. Right after Step 0 the play moves the scratch's files
into `{stm_base}<issue>/context/understand/<run ts>/` and deletes the scratch; a halt before
Step 0 deletes the scratch, so it leaves nothing behind. Each target has its own folder
`<working>/caps/<capability>/` holding its routing (`routing.yaml`), its enrich manifest
(`enrich-manifest.yaml`) and, when it was absent, its `seed.yaml`. The run-wide files — the
target pick (`targets.json`), the proposed profile, the roll-up report, the change-shape, the
persist record (`persist-manifest.json`), and the captured scoped-guard report
(`guard-report.json`) — live at the root. These are STM,
non-model artifacts (ADR 008/017) — the model itself is written IN PLACE under
`<product_base>product-os/`, never into `<working>`. The stop condition evaluates against
`<working>`. Status markers live at `{stm_base}<issue>/status/`.

Once the issue is known — at pre-flight inside a loop, right after Step 0 run by hand —
record the session identity stamp's start marker (#463 — soft-fail, never a halt):

```
python3 scripts/session_stamp.py --phase start \
    --marker "{stm_base}<issue>/status/session-stamp-understand.json" \
    --cwd "$(pwd)" --branch "$(git branch --show-current)"
```

**Resume check:** resolve the issue from the branch (`preflight.py`); if
`{stm_base}<issue>/status/understand-<run ts>.json` exists for an unfinished run, resume it — skip completed steps, reset any in-progress step to pending,
continue from the first incomplete.

## Task DAG

Create ALL tasks immediately after resolving config — before any domain work.
The play owns this DAG; the agent must not edit its top-level tasks.

Write-then-review (ADR 026): the FULL model delta — the LLM docs AND the keyed persist's
shared-file mutations — is written to the live model BEFORE the checkpoint, so the guard,
the change-shape, and the human all see the real delta. Nothing is COMMITTED before the gate
resolves; cancel reverts the uncommitted writes.

```
[T0p] Pick the targets                                  blockedBy: []
[T0a] Ask for the seeds of absent targets (all at once)  blockedBy: [T0p]
[T0] start-change (injected — start; skipped in a loop) blockedBy: [T0a]
[T1] Enrich every target at once (scoped-write fan-out) blockedBy: [T0]
[T2] Validate the live docs                              blockedBy: [T1]
[T3] Roll up the box                                     blockedBy: [T1]
[T4] Persist (keyed, in place — shared files)            blockedBy: [T2, T3]
[T5] Guard the full delta + classify the shape           blockedBy: [T4]
[T6] Checkpoint (approval over the full git diff)        blockedBy: [T5]
[T7] Commit the model delta                              blockedBy: [T6]
[E1] commit-change (injected — end; skipped in a loop)  blockedBy: [T7]
[E2] propose-change (injected — end; skipped in a loop) blockedBy: [E1]
[E3] check-change (injected — end; skipped in a loop)  blockedBy: [E2]
[E4] merge-change (injected — end; skipped in a loop)   blockedBy: [E3]
[T8] Scenario Validation                                 blockedBy: [E4]
[T9] Close                                               blockedBy: [T8]
```

Mark each task in-progress before its step and completed right after its eval passes.
No runtime reordering. On resume, skip completed and reset in-progress to pending.

## Workflow

### Phase: Ask (only when a target is absent, #616 D1)

**Step 0a — Ask for the seeds of absent targets** · Owner: play · Depends on: pre-flight
*Skip when `targets.json` `ask` is empty.* After recording the answers, run `pick_targets.py`
again (same arguments): the seed files now count as the answers, `ask` must read empty, and
every target gets its `scope`. This runs BEFORE `start-change`, so a stop here leaves no issue or branch behind. For every capability in `ask`, in one message, ask the person — a
plain, typed question, not a tool prompt — three things each: what the capability is (one
line), why it matters, and which existing domain it belongs to (list the domain ids in the
spine). Record each capability's answers verbatim, nothing added, in
`<working>/caps/<capability>/seed.yaml`:

```yaml
seed:
  id: <capability id from the play argument>
  domain: <the domain id the person named>
  one_line: <the person's one line>
  why: <the person's reason>
  answered_by: human
  doc: <domain folder, from the domain's own doc in the spine>/<capability-slug>/capability.md
```

Run by hand, with no answer or a domain not in the spine, halt and say plainly what is needed (REC1) —
never fill the gap yourself; nothing has been opened yet, so there is nothing to clean up.
`answered_by` is `human` only when the person typed the answers; the keyed persist refuses
any other value. **Inside a loop (C13)** do not ask for a capability the contract answered:
`pick_targets.py` already wrote its three answers from `run.json` `answers.seeds.<capability>`
— a person gave them before the loop started — verbatim with `answered_by: human`. A
capability still in `ask` (no answers in the contract, or a domain not in the spine) is the
loop's question (ADR 041): write it to `<review_dir>/open-understand.json` (loop contract,
step 5), detail the other targets, and finish — never fill a gap yourself. Each seed reaches the model only at Step 4, by the keyed persist (`--seed`),
inside this run's reviewed, guarded delta; Step 1 writes the capability's first
`capability.md` straight at the detailed stage from the seed's answers and its KB shelf.

### Phase: Start (injected — D2 position: start)

**Step 0 — start-change** · Owner: `start-change` (sub-play) · Depends on: Step 0a
*Skipped when `run.json` reads `in_loop: true` — the loop opened the change (C13).*
Run the start-of-pipeline member as a sub-play, dispatched with `parent_run_id` so it
emits only its own evidence and this play's close absorbs it. It resolves or creates the
issue for this run, cuts the branch off fresh main, sets up a worktree iff config calls for
it, and initializes the STM workspace. The change it opens is landed by this play's own end
sequence (Steps E1–E4), not by a later play.

    {
      "play":          "start-change",
      "parent_run_id": "<this run id>",
      "inputs":  { "title": "<e.g. 'understand: checkout, refunds'>" },
      "outputs": { "result": "{stm_base}{issue}/context/understand/start/start-change.json" }
    }

`{issue}` is the issue start-change opens or resolves. start-change owns its own evals; they
are not re-checked here. Immediately after it returns, resolve the issue from the branch
(`python3 scripts/preflight.py --play discover-capabilities --config .garura/core/config.yaml --branch
"$(git branch --show-current)"`), move the scratch's files into
`{stm_base}<issue>/context/understand/<run ts>/`, delete the scratch, record the session
stamp's start marker, and run the clean-tree assertion (pre-flight, C12/F13).
**SE-18 (F17/C15):** after Step 0 (at once inside a loop) every file this run wrote to
short-term memory — `run.json`, `targets.json`, each `seed.yaml`, the sub-play results and
the status markers — sits under `{stm_base}<issue>/`; run by hand, nothing was written under
the short-term root before Step 0, and the scratch folder is gone.

### Phase: Enrich

**Step 1 — Enrich each target (detail + features, docs to live)** · Owner: `product-os-keeper` · Depends on: pre-flight
Dispatch the agent once per target in `targets.json`, **all in one concurrent batch** — a
**scoped-write fan-out** (`standards/rules/concurrent-fanout.md`; C14): each dispatch is handed
its target's write scope (`targets.json` `scope`, the target's own folder, checked distinct and
not nested by `pick_targets.py`) and writes the model only inside that write scope, plus its own
manifest under `<working>/caps/<capability>/`; no dispatch writes a shared file (the spine, the
profile, decisions — the keyed persist in Step 4 writes those); no dispatch reads another's
output. **Join** — wait for every dispatch to return before Step 2 reads the model; collect the
manifests in `targets.json` order. The whole delta is guarded once in Step 5.
The persisted model does **not** record which KB shelf a capability came from (/discover-domains
kept that only in STM). So the agent first **re-routes** the capability to its KB shelf
with `find-work-placement`, then invokes `enrich-capability-ice` to detail it — promote the
`capability.md` to the detailed stage, author a `feature.md` per feature it
identifies, set the capability's `nfr_needs` + `compliance_needs`, and emit the implied
per-dimension levels the roll-up consumes. Per ADR 026 the skill writes the per-node docs
**straight to the live model** and emits the spine-delta as structured data in the manifest
(it never writes `_spine.yaml`, `profile.yaml`, or a decision):

    {
      "task":    "re-route this capability to its KB shelf, then detail it (directional->detailed) writing capability.md + feature.md docs in place on the live model, set its nfr_needs; emit implied NFR levels + the spine-delta into the manifest",
      "inputs":  { "issue": "<issue, or null>",
                   "capability": "<id + slug + path to its directional capability.md, or <working>/caps/<capability>/seed.yaml when it was absent>",
                   "write_scope": "<targets.json scope, e.g. product-os/commerce/checkout/>",
                   "product_base": "<product_base>",
                   "capture": "<a prototype's shared capture — source manifest, journeys, view texts — when given (C16)>",
                   "manifest_path": "<working>/caps/<capability>/enrich-manifest.yaml" },
      "outputs": { "routing":         "<working>/caps/<capability>/routing.yaml",
                   "enrich_manifest": "<working>/caps/<capability>/enrich-manifest.yaml" }
    }

The agent passes the shelf `find-work-placement` returned to `enrich-capability-ice` as its
`kb_domain`, with that shelf's short-term copy, so the grounding is the shelf `find-work-placement`
actually resolved. It returns the
contract with the output paths on disk — never inline content. The skill writes the
capability's detailed `capability.md` (over the live directional one) and the new
`feature.md` docs IN PLACE under `<product_base>product-os/`, and writes its
`enrich-manifest.yaml` (with `capability_ref` set to that capability) under
`<working>/caps/<capability>/` (STM) with the spine-delta as structured data. It writes NO
shared model file.
**SE-1 (F1/C1):** every target was a directional seed, or it was absent and
`<working>/caps/<capability>/seed.yaml` holds the person's answers (`answered_by: human`, with
`one_line`, `why`, and a `domain` that is in the spine), recorded before `start-change` ran; an
already-detailed named target, an unanswered seed, or an unknown domain halted the run before
any issue or branch existed (REC1).
**SE-2 (C6):** each target's `enrich-manifest.yaml` records `grounded_in`, and it matches the
shelf `find-work-placement` routed to in its `routing.yaml` — the detail is grounded in the recovered
shelf.
**SE-17 (F16/C1/C14):** `targets.json` lists the named capabilities in the order given, or,
with none named, every `detail: directional` capability in spine order (inside a loop, plus
every contract-seeded one), each with a distinct, non-nested `scope`; every target has its own
`caps/<capability>/enrich-manifest.yaml`; the agent was dispatched once per target in one
concurrent batch, joined before Step 2; every new or changed doc lies inside its target's
`scope`, and no dispatch wrote the spine, the profile or a decision (those change only in Step 4).
**SE-14 (F13/C12):** the product-os tree was clean at entry — the pre-flight assertion
(`git status --porcelain -- <product_base>product-os` empty) passed on a fresh start; a dirty
model tree halted at pre-flight (REC13), so the change-shape and the scoped guard reflect
only this run's delta.

### Phase: Validate + Roll up

**Step 2 — Validate the live docs** · Owner: play · Depends on: Step 1
Run the two guards over the LIVE model before the checkpoint — shape first, then content.
Under direct-model-write the docs are already written in place, and the spine has NOT yet
been mutated for this run (the keyed persist runs after approval). So the linter runs over
the live tree, and the newly written docs are linted; full spine↔doc consistency for the
new feature entries is completed after the keyed persist (Step 6) writes those entries.

```
python3 scripts/lint_grounding.py --root <product_base>/product-os
python3 scripts/check_sources.py --manifest <working>/caps/<capability>/enrich-manifest.yaml \
    [--manifest <one per target>] --product-base <product_base> \
    [--source-text <the capture's view texts, when a capture was given>] \
    --out <working>/sources-check.json
```

Then run the **content-quality eval** over the grounding docs this run wrote or changed
(every target's detailed `capability.md` and every new `feature.md`, at their live
paths — all targets in one batch) as a
**concurrent read-only fan-out** (`standards/rules/concurrent-fanout.md`): dispatch one
isolated, clean-context judge sub-agent PER doc, ALL IN ONE CONCURRENT BATCH — each running
the `judge-grounding` skill, handed only its doc (and parent doc), and the kind's per-section
guidance: the play first asks `template-manager` for each judged kind's template
(`standards/schemas/product-os/grounding/<kind>.md`), cuts its `## Per-section guidance` block
out of that short-term copy, and hands the judge only that block — never the template's gold
example (it sees neither the brief nor the author's reasoning), on the model from
`grounding-eval.judge.model`. The three safety conditions hold: each judge only READS its
own doc, writes only its own verdict JSON, and no judge depends on another. **Join** —
wait for every verdict to return before gating any. Then gate every returned verdict
(order-stable, so the outcome is identical to a serial run). The guidance cut, once per judged
kind, before the batch:

```
python3 scripts/guidance_block.py --template {stm_base}<issue>/context/templates/standards/schemas/product-os/grounding/<kind>.md \
    --stage detailed --out <working>/judge/guidance-<kind>.md   # /discover-capabilities writes the detailed stage
python3 scripts/grounding_gate.py --verdict <verdict.json>
```

**SE-3 (F2/C3):** `lint_grounding.py` exits 0 over the live docs this run wrote — each
detailed `capability.md` conforms to the capability template's detailed stage and every
new `feature.md` conforms to the feature template.
**SE-4 (F3/C4):** the content-quality eval gate (`grounding_gate.py`) passes for EVERY
grounding doc — each section self-explains at product-manager altitude and clears the
stranger test.
**SE-5 (F4/C2):** each target's manifest promotes its capability
(`enrich.capability.detail: detailed`) and every feature it names carries both a manifest
`features` entry and a live `feature.md` doc (the keyed persist in Step 6 writes the entries; the docs are on disk
now). No feature is created without both.
**SE-19 (F18/C16):** `sources-check.json` reads `ok: true` — every page the run wrote carries
`## Sources`, every quote on a screen line is on the prototype, and no page leaves a question
open; the agent's contract reads `completed`, its judgment having found every feature a
whole thing a person does or sees on the screens — no panel made a function of its own.
**SE-6 (F5/C5):** every `nfr_needs.<dimension>` in each manifest's `capability` block is
concrete — a `level`, a measurable `target`, and a `gate` — and the needs sit on the
capability, not globally.
On any GAP, apply the matching recovery (REC2–REC6) and re-run before the checkpoint — a
content-eval fail (SE-4) is REC3: rewrite the doc to the judge's cited fixes and re-judge. A
target that still fails after its recovery halts the whole run and nothing is committed
(C14/REC16): revert the uncommitted delta with the guard's `--restore` and an empty allow set.

**Step 3 — Roll up the box** · Owner: play · Depends on: Step 1
Roll every target's implied levels into the profile together, monotonic-up. The script
reads the box from the live spine and one manifest per target (all non-draft) and measures
each target against the box as it stood at the start of the run (C7). It branches on state:
a `directional` box is established and firmed to `set` (no moves); a `set` box yields one
out-of-box move per target for any dimension or compliance regime that target's need
exceeds — each move names its capability, so no box-move hides behind another's (C8):

```
python3 scripts/rollup_box.py --spine <product_base>/product-os/_spine.yaml \
        --enrich-manifest <working>/caps/<cap-a>/enrich-manifest.yaml \
        [--enrich-manifest <working>/caps/<cap-b>/enrich-manifest.yaml ...] \
        --out-profile <working>/proposed-profile.yaml \
        --out-report <working>/rollup.json
```

**SE-7 (F6/C7):** the roll-up report shows `state_after: set` and never lowers a dimension
(each proposed level is the max of the current box and every need), and lists every target in
`capabilities`. `establishing: true` on a `directional` box yields no box-moves; on a `set` box
every move's `from` is the starting level.

*Note — partial gates are expected.* On the first firm-up, dimensions no capability has
touched yet keep their directional level; the box fills in as more capabilities are
understood. This is incremental firm-up, not a defect.

### Phase: Persist (write the full delta first, ADR 026 write-then-review)

**Step 4 — Persist (keyed, in place)** · Owner: play · Depends on: Steps 2–3
Write-then-review (ADR 026): the FULL model delta is written to the live model BEFORE the
checkpoint, so the guard, the change-shape, and the human all see the real delta. The docs
are already on the live model (Step 1). `persist_understand.py` now writes the SHARED files
in place, keyed to the targets (one `--capability-ref` and one `--enrich-manifest` per target):
it reads the manifests + roll-up output and flips each target's spine entry to
`detail: detailed`, sets its `nfr_needs`/`compliance_needs`, adds its new feature
entries, writes the rolled-up profile, and writes one decision per box-move linked to the
capability the move names — and it REFUSES to touch any capability that is not a target or a
feature not under its manifest's target (this is the node-level containment the
file-level guard cannot provide). Every check runs before any write, so a refusal leaves the
model untouched. No draft, no
doc copy. Nothing is COMMITTED yet — the commit (Step 7) happens only after the gate approves;
on cancel the whole delta is reverted (Step 6):

```
python3 scripts/persist_understand.py \
        --capability-ref <cap-a> --enrich-manifest <working>/caps/<cap-a>/enrich-manifest.yaml \
        [--capability-ref <cap-b> --enrich-manifest <working>/caps/<cap-b>/enrich-manifest.yaml ...] \
        --product-base <product_base> --proposed-profile <working>/proposed-profile.yaml \
        --rollup-report <working>/rollup.json \
        --decided-by /discover-capabilities --date "$(date -u +%Y-%m-%d)" \
        --out-manifest <working>/persist-manifest.json \
        [--seed <working>/caps/<cap>/seed.yaml ...] \
        $( [ "<run.json in_loop>" = "true" ] && echo --decision-status proposed )
```

Pass one `--seed` for each target that was absent or `found` (its `caps/<capability>/seed.yaml`).
Inside a loop (C8/C13) pass `--decision-status proposed`: every box-move decision is written
`proposed`, never `accepted`, because no person says yes inside a loop; the loop's review
accepts or drops it. The persist runs before the gate resolves, so `in_loop` — not the gate's
outcome — decides the status.

With its `--seed`, an absent target is first added as a thin seed from the person's answers
(status `proposed`, `detail: directional`, under the named domain) — or, for a `found` target,
from the screens' reading (`answered_by: screens`, with its intents; under its domain, or in
the holding folder with its domain empty) — then promoted like any seed; the persist record lists it in `seeded`. Without one, an absent target is refused, and
an already-detailed target is always refused.

**SE-9 (F8):** there is one product-level decision per box-move, each carrying its
capability (`node_ref`), its dimension, its from→to, and status `accepted` — `proposed` inside a loop (in
`persist-manifest.json` `box_moves` + the written decision records).
**SE-11 (F10):** no slice and no epic was written, and no target's `status` was flipped to
`active` — prioritization is /shape-scope's.

### Phase: Guard + Classify (over the full delta)

**Step 5 — Guard the full delta + classify the shape** · Owner: play · Depends on: Step 4

**The run's write scope (the per-play guard policy, ADR 026).** The old
`apply_understand.py --capability-ref` encoded understand's write scope by construction;
under direct-model-write that same scope is the `scoped_write_guard.py` policy — for EACH
target resolve `<cap-dir>` as the directory of its `doc` (e.g. `ecommerce/checkout` from
`ecommerce/checkout/capability.md`) and repeat its two lines:

    --allow    'product-os/_spine.yaml'                    # the shared spine + profile block (persist writes it)
    --allow    'product-os/decisions/*'                    # box-move decisions (persist writes them)
    --allow    'product-os/<cap-dir>/capability.md'        # each target's detailed doc (overwrite)
    --add-only 'product-os/<cap-dir>/*/feature.md'   # each target's new feature docs (added, not modified)

**Guard ONCE over the full delta (C10).** After ALL writes (the LLM docs from Step 1 and the
keyed persist's shared-file writes from Step 4), run the scoped guard a single time over the
whole delta. Capture its report — its `ok` field is the stop condition's D3 input (this
replaces the old `check_apply.py` verify). Then re-run the linter over the merged live spine
to complete spine↔doc consistency:

```
python3 scripts/scoped_write_guard.py --product-base <product_base> --base-ref HEAD \
        --allow 'product-os/_spine.yaml' --allow 'product-os/decisions/*' \
        --allow 'product-os/<cap-dir-a>/capability.md' --add-only 'product-os/<cap-dir-a>/*/feature.md' \
        [--allow 'product-os/<cap-dir-b>/capability.md' --add-only 'product-os/<cap-dir-b>/*/feature.md' ...] \
        --out <working>/guard-report.json
python3 scripts/lint_grounding.py --root <product_base>/product-os \
        --spine <product_base>/product-os/_spine.yaml
```

If the guard exits non-zero, re-run with `--restore` to revert the offending paths, apply
REC9 (a capability/feature/domain other than the targets changed), and re-persist before
the checkpoint.

**Classify the full working-tree delta (C9).** Classify the model tree's diff vs HEAD — now
the FULL delta (docs + spine entries + profile bars + decisions), per ADR 026 write-then-review
(no draft dir), so a high-impact run (a two-dimension box-move) yields a materially different
shape key from a prose edit:

```
python3 scripts/classify_change.py --play discover-capabilities \
        --product-base <product_base> --base-ref HEAD --out <working>/shape.json
```

**SE-10 (F9/C10):** the scoped-write guard report reads `ok: true` — the model delta is
confined to the target capabilities (each entry + doc), their new features, the
profile, and decisions; no other capability, feature, or domain changed.

### Phase: Checkpoint (conditional gate, C9)

**Step 6 — Human review (class: standard, conditional)** · Owner: play · Depends on: Step 5
**Inside a loop (C13), this step never waits.** Resolve the gate exactly as below, first match
wins: an explicit config skip is recorded as a skip, and a policy auto-pass as an auto-pass,
exactly as by hand. Only where the gate resolves ON — where a run by hand would wait — render
each target's part of the checkpoint exactly as it would have been shown (the same content as
the "on" path below: that capability, its features, its NFR needs, and every box-move
in `rollup.json` that names it as its own line item, its decision `proposed`) to
`<working>/caps/<capability>/checkpoint.md`, write one review record per target — named for
it, so ADR 029's "one `/discover-capabilities` record per capability" holds — and append the crossing
once as deferred:

Once per target, in `targets.json` order, then once for the run:

```
python3 scripts/write_loop_review.py --run <working>/run.json \
        --summary <working>/caps/<capability>/checkpoint.md \
        --attach rollup=<working>/rollup.json --attach shape=<working>/shape.json \
        --attach guard=<working>/guard-report.json --attach persist=<working>/persist-manifest.json \
        --ts <run ts>-<capability>
python3 scripts/gate_eval.py append --ledger <gates.conditional.ledger> --play discover-capabilities \
        --issue <the loop's issue> --shape <shape-key> --predicted gate \
        --human deferred_to_loop_review --ts <run ts>
```

Record `checkpoint deferred to the loop's review (loop <loop_run_id>)` as a Checkpoint
Decisions row and proceed to Step 7. Nothing is reverted: a cancel at the loop's review is the
loop's to act on. Run by hand, the rest of this step applies as written.

This checkpoint is a **conditional gate** (#467) per `standards/rules/gate-config.md` —
/discover-capabilities is one of the eleven conditional document plays. Resolve it first match
wins: pinned (n/a here) → `gates.plays.understand` → the learned policy →
`gates.classes.standard` → `gates.default` (absent ⇒ on). For the policy lookup, use the
shape key classified in Step 5.

Look the shape key up in the config-resolved policy (`gates.conditional.policy`):
**auto-pass** iff the shape is in the policy's `auto:` block AND not in `never_auto:`
AND Step 2 + Step 5 stand with no blocking finding (a `lint_grounding.py` gap, a
`grounding_gate.py` content-eval fail, or a guard violation). On auto-pass, do NOT wait: record
`gate auto-passed by learned policy (shape: <shape-key>, policy v<version>)` as a
Checkpoint Decisions row, include the working-tree diff summary in the run record, append
the crossing's live-eval ledger line, and proceed to Step 7 (commit):

```
python3 scripts/gate_eval.py append --ledger <gates.conditional.ledger> --play discover-capabilities \
        --issue <strategy issue> --shape <shape-key> --predicted auto --human auto_pass \
        --policy-version <policy version> --ts <run ts>
```

Anything else resolves the gate on (an explicit `gates.plays.understand: off` instead
records `gate skipped by config (<resolution path>)` as a Checkpoint Decisions row and
proceeds — box-move approvals ride this same gate, so the recorded skip or auto-pass
stands in evidence for them too). When on, present each target's detailed capability, its
features, the per-capability NFR needs, and the profile changes **inline over the real
model git diff**, one section per target — for each box-move in `rollup.json`, render its
**own explicit line item** (the capability, the dimension, the from→to levels, and the
product-level decision (ADR) it will create),
distinct from the grounding approval — render the approval prompt — the template
`standards/templates/approval-prompt.md`, which the play asks `template-manager` for (it never
reads it from memory) — and wait for the typed response. Approve →
continue to Step 7 (commit). **Cancel → revert the working tree (ADR 026 step 6):** the full
delta is already on disk, so run the guard with `--restore` and an EMPTY allow set to
`git restore` the modified model paths and `git clean`/remove the new ones (byte-clean back
to HEAD), then halt — nothing was committed, and cancel means "revert what was written":

```
python3 scripts/scoped_write_guard.py --product-base <product_base> --base-ref HEAD \
        --restore --out <working>/guard-report.json   # empty --allow ⇒ every model path reverted
```

Then append the crossing's live-eval ledger line with the human's real action:

```
python3 scripts/gate_eval.py append --ledger <gates.conditional.ledger> --play discover-capabilities \
        --issue <strategy issue> --shape <shape-key> --predicted gate \
        --human <approved_clean|approved_edited|rejected> --ts <run ts>
```

`<strategy issue>` is the issue the run's branch carries (opened by this run's
start-change; inside a loop, the loop's issue from `run.json`). `<gates.conditional.ledger>` / `<gates.conditional.policy>`
resolve from config `gates.conditional` (defaults `.garura/project/issues/<issue>/review/gate-evals.jsonl` (the run's issue) /
`.garura/core/gate-policy.yaml`); `<policy version>` is the policy file's `version:`
field. `<run ts>` is the run's own UTC timestamp, derived the same way the close
derives `ts` (`date -u`), passed by the orchestrator.
**SE-8 (F7/C8/C9):** when the box is `set` and `out_of_box: true`, each move was written to
the model by the Step 4 keyed persist but is COMMITTED (made durable) only here on approval
(inside a loop, on the recorded deferral, with its decision `proposed`) —
every box-move appears as its own line item, so an out-of-box move is never COMMITTED without
an explicit, un-rubber-stamped approval (or, when the gate resolves off by config or
auto-passes by learned policy, without the recorded skip/auto-pass row standing in evidence
for it); on cancel the whole delta — box-move decisions included — is reverted before the
commit, so nothing out-of-box becomes durable.
**SE-13 (F12):** every crossing of this gate appended exactly one live-eval ledger line
(shape, predicted `gate|auto`, the human's real action or `auto_pass`), and an
auto-pass fired only for a shape the policy lists in `auto:` (and not in `never_auto:`)
with no blocking finding standing.
**SE-15 (F14/C13):** `run.json` records the path taken. Inside a loop (`in_loop: true`): no
`start-change` (Step 0) or end-sequence step (E1–E4) ran, the run did not wait at Step 6 or
Step 0a, and every commit is on the contract's branch. By hand (`in_loop: false`): Step 0,
Step 6 and E1–E4 ran as written.
**SE-16 (F15/F7/C13/C8):** inside a loop, when the gate did not auto-pass, for each target a
`<review_dir>/understand-<ts>-<capability>.json` record exists with `decided: false`, its summary
file equals `<working>/caps/<capability>/checkpoint.md` and names every box-move in `rollup.json`
for that capability as its own line, and its attachments exist; the gate ledger holds exactly
one line for the crossing, reading
`deferred_to_loop_review` (or `auto_pass` on a policy-listed shape) and never an approval;
every decision in `persist-manifest.json` `box_moves` was written `proposed`; and a seed's
`one_line`, `why` and `domain` equal the contract's answers — none filled in by the play.

### Phase: Commit (make the delta durable, ADR 026 step 7)

**Step 7 — Commit the model delta** · Owner: play · Depends on: Step 6
The gate approved (or auto-passed / was skipped by config / was deferred to the loop's review
inside a loop). Commit the full model delta — every target at once, one commit (C14) — on the
branch — the loop's branch inside a loop
(C12, ADR 026 step 7) — a lightweight persist step that makes the writes durable
and advances HEAD so the end sequence lands exactly this run's delta; it is NOT the end
sequence itself. A cancelled checkpoint never reaches this step (nor the end sequence) — its
tree was already restored in Step 6:

```
git add -- <product_base>product-os
git commit -m "feat(model): detail <capability>, <capability>… — capabilities, features, profile roll-up (#<issue>)"
```
**SE-12 (F11/C11):** the close is stop-condition gated — `check_stop_condition.py` over the
baked `stop-condition.yaml` (D1 the persist record `persist-manifest.json` exists; D2 it
stamps `changed.profile: true`; D3 the captured `guard-report.json` reads `ok: true`) must
read **held** before any COMPLETED close, and the model delta is committed (C12); a run whose
persist or guard did not land closes HALTED, never COMPLETED (REC11).

### Phase: End sequence (injected — D2 position: end)

*Skipped when `run.json` reads `in_loop: true` — the loop lands its own change (C13).*
After the model delta is committed, the D2 rule injects the close sequence — each a sub-play
dispatched with `parent_run_id`, resolving its own context — to commit any remaining change,
raise the PR, take the verdict, and merge the detailed capability to main (C11).

**Step E1 — commit-change** · blockedBy: Step 7

    { "play": "commit-change", "parent_run_id": "<this run id>", "inputs": {}, "outputs": { "result": "{stm_base}{issue}/context/understand/end/commit-change.json" } }

**Step E2 — propose-change** · blockedBy: E1

    { "play": "propose-change", "parent_run_id": "<this run id>", "inputs": {}, "outputs": { "result": "{stm_base}{issue}/context/understand/end/propose-change.json" } }

**Step E3 — check-change** · blockedBy: E2

    { "play": "check-change", "parent_run_id": "<this run id>", "inputs": {}, "outputs": { "result": "{stm_base}{issue}/context/understand/end/check-change.json" } }

**Step E4 — merge-change** · blockedBy: E3

    { "play": "merge-change", "parent_run_id": "<this run id>", "inputs": {}, "outputs": { "result": "{stm_base}{issue}/context/understand/end/merge-change.json" } }

Each end member owns its own evals (commit grouped by concern, PR opened, verdict posted, branch
merged + cleaned); they are not re-checked here. A check-change reject stops the chain before
merge; the land on main keeps its pinned human approval (merge-change C7).

### Phase: Scenario Validation

**Step 8 — Scenario evals** · Owner: play · Depends on: the end sequence
- **SCE-1 (S1 — product manager, detail + features):** every target is detailed
  (its `capability.md` promoted, its entry `detail: detailed`, with `nfr_needs`) and its
  features are created (each a spine entry + a `feature.md`), all clean on
  `lint_grounding.py` and passing the content-eval gate; the change is landed on main by the
  end sequence (`{stm_base}<issue>/context/understand/end/merge-change.json` reports the PR
merged); and the
  stop-condition verdict reads held.
- **SCE-2 (S2 — product strategist, first firm-up):** on a `directional` box, the roll-up
  established and firmed it to `set` with no decision written this run.
- **SCE-3 (S3 — architect, out-of-box move):** on a `set` box exceeded on a dimension, the
  run halted at the checkpoint surfacing each capability's box-move as its own line item, and
  on approval each box-move was committed with a product-level `accepted` decision whose
  `node_ref` is its capability, recording the from→to from the starting level
  (written by the keyed persist, made durable only by the Step 7 commit; reverted on cancel).
- **SCE-4 (S4 — product owner, non-destructive):** the scoped-guard report reads `ok`, so the
  working-tree model delta is confined to the target capabilities, their new features,
  the profile, and decisions, and no dimension was lowered.
- **SCE-5 (S5 — reviewer, the checkpoint):** each detailed capability, its features,
  its NFR needs, and each box-move (capability, dimension, from→to, ADR) appeared inline over the full
  written delta, and no SHARED model change was COMMITTED before approval — the full delta
  written in place (docs + spine/profile/decisions) shows as the branch diff and is reverted
  byte-clean on cancel (ADR 026 step 6) — or, on the auto-pass path (a policy-listed shape),
  the gate resolved with no wait and the recorded auto-pass, the appended ledger line, and
  the diff summary stand in the approval's place.
- **SCE-6 (S6 — product manager, nothing run first):** for a target that was absent,
  `<working>/caps/<capability>/seed.yaml` holds the person's answers (`answered_by: human`), the
  persist record lists it in `seeded`, the spine entry sits under the named domain with `detail: detailed`,
  `{stm_base}<issue>/context/understand/end/merge-change.json` reports the PR merged, and the
  stop-condition
  verdict reads held.
- **SCE-7 (S7 — Discovery loop):** handed a valid contract, `run.json` reads `in_loop: true`
  with the contract's `loop_run_id` and branch; every pending capability was a target of the
  one run; no `start-change` or end-sequence step ran; the current branch equals the
  contract's; for each target an `understand-<ts>-<capability>.json` review record with
  `decided: false` and its summary exist in the contract's `review_dir`, the summary naming
  each of that capability's box-moves as its own line; the ledger line reads
  `deferred_to_loop_review` (or `auto_pass`); every box-move decision reads `proposed`; the
  model delta is committed on the loop's branch; the stop-condition verdict reads held. The
  same play run by hand reads `in_loop: false` and ran every step.
- **SCE-8 (S8 — product manager, many at once):** with none named and three pending
  capabilities, two over the set box on security, `targets.json` lists the three in spine
  order; every one reads `detail: detailed`; `rollup.json` holds one box-move per capability
  over the box, each `from` the starting level; `persist-manifest.json` `changed.capabilities`
  lists the three; one `feat(model)` commit holds the whole delta; the stop-condition verdict
  reads held.
- **SCE-9 (S9 — product manager, from a prototype):** with a capture given and no capability in
  the model, `targets.json` lists a `found` target per capability in `found.yaml`, each with
  its scope (its domain's folder or `capabilities/<id>/`), and `sources-check.json`
  reads `ok: true` over every target's manifest — each page has `## Sources`, every screen
  quote is on the prototype, no page leaves a question open.

### Phase: Evidence & Close

**Step 9 — Close** · Owner: play · Depends on: Step 8
Run the Standard Play Close. /discover-capabilities's evidence lives in the issue being worked on
(the loop's issue inside a loop, `start-change`'s by hand) — use that evidence base and
the product's slug. Evidence recording is play-only and
config-gated per the D1 evidence rule (`standards/rules/evidence-recording.md`).

```bash
# --- Standard Play Close (shared; see ../_shared/play-close.md) ---
# Run the close in ../_shared/play-close.md. Its Step L loads the templates through
# template-manager and sets ts and evidence_dest; then run this play's own lines below;
# then Steps C0-C2.
#   evidence_base, slug:
#     evidence_base="${stm_base}${issue}/evidence/understand/"   ; slug="${product_slug}"

# Session identity stamp (#463) — close phase; start phase ran at pre-flight
session_stamp=$(python3 scripts/session_stamp.py --phase close \
    --marker "${stm_base}${issue}/status/session-stamp-understand.json")
# Stop-condition gate (#464) — Step C0: this play carries a baked manifest, so the
# gate is LIVE. Evaluate the Done means as the close's authoritative input.
python3 scripts/check_stop_condition.py \
    --manifest "<play-dir>/stop-condition.yaml" \
    --base "${stm_base}${issue}/context/understand/<run ts>/" \
    --out "${stm_base}${issue}/status/stop-condition-understand.yaml"
sc_exit=$?   # 0 held · 1 unmet · 2 error
# Conditional-gate policy refresh (#467) — soft: a distill failure never blocks the close
python3 scripts/distill_gate_policy.py --ledger "<gates.conditional.ledger>" --policy "<gates.conditional.policy>" --streak <gates.conditional.streak> --project "<project name from config>" || true
```

`/discover-capabilities`'s evidence lives in the issue being worked on:
`evidence_base="${stm_base}${issue}/evidence/understand/"`
and `slug="${product_slug}"` (the product's slug).

**Step C0 — bind the verdict.** `sc_exit == 0` (held) permits `status: COMPLETED`.
Anything else closes `HALTED` with `exit_reason: stop_condition_unmet` and the evidence's
Stop Condition section names every unmet clause — fix the state per REC11 (re-run the keyed
persist, re-capture the scoped-guard report, or make the model-delta commit) and re-evaluate;
the close stays HALTED until the verdict reads held. An unevaluable verdict is never a pass.

**Step C1 — Write evidence file.** Gated by the resolved `evidence.record` flag (global
+ per-play `evidence.plays.understand`; first match wins, absent ⇒ record). When false,
skip the write and record `evidence skipped (record=false)` in the report's pointer line.
Otherwise fill the `evidence-file.md` slots (play `understand`, run_id `understand-${ts}`,
product_slug, started_at/completed_at, status per C0, exit_reason; artifacts produced: the
target pick (`targets.json`), each detailed `capability.md`, the new `feature.md` docs, the spine entries written, the
firmed profile, any decision records, the persist manifest (`persist-manifest.json`), the
captured `guard-report.json`, the model-delta commit sha, the stop-condition verdict; the
content-eval verdicts; step and scenario eval results
SE-1…SE-19 / SCE-1…SCE-9; `run.json` (`in_loop`) and, inside a loop, each review record's
path; checkpoint decision from Step 6 including each approved box-move
(or the `gate skipped by config` / `gate auto-passed by learned policy` row when the gate
resolved without a wait) plus the gate ledger line(s) appended this run; the session identity
stamp fields from $session_stamp (#463): session_id, ledger_file, ledger_start_offset,
ledger_end_offset (null when unresolved — never blocks the close); and stop_condition per
C0 with the Stop Condition section filled) and write to `$evidence_dest`. Do NOT
hand-author the body.

**Step C2 — Render delivery report.** Also render the **Next** line: resolve this play in the Next-line map (`$next_map`, from `template-manager`) and emit `**Next:** /<command> — <why>. Or run /next to see all recommended actions.` (only /next pointer, or omit, when the mapped command is null), per `play-close.md`. Fill the `delivery-report.md` slots and output the
report: `## understand Delivered — ${product_slug}`, the Run Summary table, the Pipeline
Steps table from the task DAG, the Artifacts Produced table (the detailed capabilities, their
features, the firmed profile, any decisions), Next Steps (run /shape-scope to prioritize
the detailed features into end-to-end verticals and epics), and a pointer to
`$evidence_dest`. Always emitted; never gated.

```bash
# --- end Standard Play Close ---
```

## Scenario Validation

| Scenario | Persona | Eval |
|----------|---------|------|
| S1 — detail + features | product manager | SCE-1 |
| S2 — first firm-up | product strategist | SCE-2 |
| S3 — out-of-box move | architect | SCE-3 |
| S4 — non-destructive | product owner | SCE-4 |
| S5 — the checkpoint | reviewer | SCE-5 |
| S6 — nothing run first | product manager | SCE-6 |
| S7 — Discovery loop | product manager | SCE-7 |
| S8 — many at once | product manager | SCE-8 |
| S9 — from a prototype | product manager | SCE-9 |

## Recovery

| For | Trigger | Direction | Handoff |
|-----|---------|-----------|---------|
| F1 | an absent capability has no recorded answers, its domain is not in the spine, or the target is already `detailed` | ask the person what the capability is, why it matters, and which existing domain it belongs to, and record the answers before seeding; with no answer or no such domain, halt and say plainly what is needed — inside a loop, write it to `open-understand.json` as the loop's question and detail the other targets (C13); an already-detailed capability is not re-detailed | human |
| F2 | a grounding doc fails its template/shape, or a spine entry fails the schema or spine↔doc consistency | re-emit the failing doc or spine entry to conform and restore consistency before the checkpoint | autonomous |
| F3 | a grounding doc fails the content-quality eval | rewrite the failing doc to the judge's cited fixes — raise each flagged section to a self-explaining, product-manager-altitude statement — and re-judge until the gate passes | autonomous |
| F4 | the capability stayed directional, or a feature lacks its entry or its doc | complete the promotion (flip the entry to `detail: detailed`) and emit the missing feature entry or doc before the checkpoint | autonomous |
| F5 | an NFR need has no level/target/gate, or needs were written off the capability | re-draft each need on the capability as a concrete level + target + gate | autonomous |
| F6 | a profile dimension was lowered, or the box firmed to a state other than `set` | recompute the roll-up monotonic-up (max per dimension) and firm to `set` | autonomous |
| F7 | an out-of-box need against a `set` box was persisted with no approved decision (inside a loop, no recorded deferral), or a box-move decision was written `accepted` inside a loop | revert the box change, surface the move at the checkpoint, persist only after a human approves it (inside a loop, re-write the decision as `proposed` and record the deferral) | human |
| F8 | a box-move lacks its decision record, or a decision omits its dimension or from→to | write or complete the product-level decision for each move with its dimension and from→to before persisting | autonomous |
| F9 | a capability, feature, or domain other than the targets was changed (scoped-guard violation) | the guard's `--restore` already reverted the offending paths; re-run writing only the target capabilities and their features, after a human confirms the restore | human |
| F10 | a slice, an epic, or a capability status flip was written | strip the prioritization over-reach — remove the slice/epic, reset the status — leaving only /discover-capabilities's detailing scope | autonomous |
| F11 | the run is about to close COMPLETED with the Done means unmet | close HALTED (`stop_condition_unmet`) with the unmet clauses named; fix the state — re-run the keyed persist, re-capture the scoped-guard report, or make the model-delta commit — and re-evaluate; the close stays HALTED until the verdict reads held | autonomous |
| F12 | a conditional-gate crossing left no live-eval ledger line, or an auto-pass fired for a shape the policy does not list as auto (or that carried a blocking finding) | re-append the missing ledger line for the recorded crossing; when the auto-pass was unearned, re-run the gate as a live wait — render the approval prompt and wait for the typed response — before proceeding | autonomous |
| F13 | the product-os tree is dirty right after start-change (uncommitted model edits present) | halt and ask for a clean model tree — commit or revert the pending model edits — before /discover-capabilities proceeds | human |
| F14 | inside a loop the play opened an issue or branch, ran the end sequence, waited at its checkpoint, or worked off the loop's branch; or by hand it skipped a step | inside a loop, close the stray issue and branch, switch to the loop's branch, and write the review record in place of the wait; by hand, run the skipped step | human |
| F15 | no review record, a record that differs from the checkpoint (a box-move missing as its own line), no ledger line, an approval no person gave, or an answer the play picked itself | re-render the checkpoint and re-write the review record with `write_loop_review.py`; append the missing `deferred_to_loop_review` line, or a correction refuting a made-up approval; drop the picked answer and hand the question to the loop (`open-understand.json`; run by hand, ask the person) | autonomous |
| F16 | a pending capability left out, an unnamed one taken, a target measured against a box raised in the same run, or a part of the run committed while another target failed | re-pick the targets with `pick_targets.py`, re-run the roll-up with every target's manifest against the starting box, and re-render the checkpoint; when a target failed, revert the uncommitted delta and halt the whole run | autonomous |
| F17 | a working file, an answer, a marker or a sub-play result sits outside `{stm_base}<issue>/`, or something was written to short-term memory before Step 0 gave the issue | move it into the issue's working root (or status folder), delete the stray copy, continue; before the issue is known, hold it in the scratch folder until Step 0 | autonomous |
| F18 | a panel made a feature, a feature no screen shows, a page with no sources or a quote not on the prototype, or a question left open | fold the panel into the feature that shows it; drop what nothing shows; write each page's sources with the screen's own words; replace the open question with our default, marked as ours | autonomous |

## Pause and Resume

Steps run top to bottom. On entry, resolve config and the run's issue from the branch (C15),
resolve the targets from the in-progress run's `targets.json` under
`{stm_base}<issue>/context/understand/<run ts>/` (or pick them fresh), check the status marker
at `{stm_base}<issue>/status/`, skip completed
steps, reset any in-progress step to pending, and continue. A fresh start with no marker
runs everything and creates the marker at Step 1. Resuming a run that already wrote model
docs enters a dirty tree; the clean-tree assertion (F13) is scoped to a FRESH start right
after start-change (or, inside a loop, to the start of the run) — a resume continues its own
in-progress delta. A resume after Step 7
continues at the first end-sequence member that has not finished; a resume after Step 0a
reuses each `<working>/caps/<capability>/seed.yaml` rather than asking again.

## Compilation Metadata

| Field | Value |
|-------|-------|
| fingerprint | sha256:4e857bb65c75fb3b545e77467ab87571b97933aa5c46dcb9108e40efffa7c889 (of `reference/ice.md`) |
| compiled_by | edit-play (#689 ADR 043: writes the capabilities and features, read off the screens, holding folder when no domain: C1, C2, C16); edit-play (#689 the screens decide the features, every page with its sources: C16); edit-play (#661 reads no memory; the run lives in its issue); edit-play (#615 runs inside a loop; one run details every pending capability); edit-play (#616 stands alone); edit-play (#498 direct-model-write, ADR 026); prior: edit-play (#467 Batch B, #466 Batch C) |
| pipeline_position | both (start-change head; commit → propose → review → merge close — #616) |
| position_exception | model-writing both play — writes the model on its own started branch and commits its own model delta (C12) BEFORE the injected end sequence lands it (same shape as /shape-measure-lens and /discover-domains) |
| workflow_structure | A (single checkpoint carrying box-move approvals — class: standard, conditional gate per gate-config.md #467; direct-model-write WRITE-THEN-REVIEW per ADR 026 — persist + guard + classify before the gate, commit after; stop-condition gated close) |
| stop_condition | stop-condition.yaml (D1–D3), gate live at Step C0 |
| domain_agents | 1 (product-os-keeper) |
| utility_agents | 1 (template-manager — the approval prompt, the kinds' templates, the shared close's templates) |
| skills_used | find-work-placement, enrich-capability-ice, judge-grounding (run by each isolated judge) |
| scripts | 16 (check_sources.py — every page says where it is seen (C16), preflight.py, check_loop_contract.py, pick_targets.py, write_loop_review.py, lint_grounding.py, grounding_gate.py, rollup_box.py, persist_understand.py, scoped_write_guard.py, classify_change.py, gate_eval.py, distill_gate_policy.py, check_stop_condition.py, session_stamp.py, guidance_block.py) |
| step_evals | 19 (SE-1…SE-19) |
| scenario_evals | 9 (SCE-1…SCE-9) |
| recovery_entries | 18 (one per failure condition; 14 autonomous / 4 human) |
| concurrency | Step 1 scoped-write fan-out (one agent per target); Step 2 read-only fan-out (one judge per doc) |

**Recompiled note (#498, direct-model-write / ADR 026):** migrated from draft-then-apply to
direct-model-write. The old draft model tree and the apply/check promotion scripts are
removed; the enrichment skill writes per-node docs straight to the live model; the new keyed
`persist_understand.py` writes the shared files (spine/profile/decisions) in place; containment
is the post-write `scoped_write_guard.py` (its `guard-report.json` is D3); `classify_change.py`
reads the working-tree git diff (`--product-base`/`--base-ref HEAD`); checkpoint cancel reverts
the working tree via the guard `--restore`; the play asserts a clean product-os tree at entry
(F13) and commits its own `feat(model)` delta after approval (C12). Order is
**write-then-review** (ADR 026 "Order of operations"): the full delta — LLM docs AND the keyed
persist's shared-file mutations — is written to the live model FIRST (Steps 1+4), then guarded
ONCE and classified over the full delta (Step 5), then the gate resolves over the real git diff
(Step 6), and only an approved gate COMMITS (Step 7). Nothing out-of-box is COMMITTED before
approval; cancel reverts the uncommitted writes. This ordering is why a two-dimension box-move
produces a materially different shape key from a prose edit — the shared-file delta is on disk
at classify time, not still in the manifest. See `standards/rules/direct-model-write.md`.

**Recompiled note (#467 Batch B):** checkpoint upgraded to a conditional learned gate;
see `gate-config.md`.

**Direct-edit deviation note (#468 Stage 5, concurrent fan-out):** the Step 2
content-quality judge loop was changed from a serial per-doc loop to a concurrent
read-only fan-out — one isolated judge per doc dispatched in one batch, joined before
gating (`standards/rules/concurrent-fanout.md`). Execution-timing change only: each judge
stays isolated and read-only, writes only its own verdict, and the gate still runs over
every verdict, so coverage (SE-4) is unchanged. No constraint, failure, scenario, or eval
touched — the ICE (`reference/ice.md`) and fingerprint stand. create-play emits the same
fan-out form so a rebuild converges.

**Direct-edit deviation note (#498) — INTENT CHANGE, HAND-COMPILED, CONVERGENCE UNVERIFIED:**
This SKILL was updated to the direct-model-write write-then-review shape (ADR 026) by a
**hand-compile from `reference/ice.md`**, NOT by a `/edit-play` run. This is an intent change
(it alters the write path, the containment guarantee, the checkpoint cancel semantics, and the
step order), so the sanctioned path is recompile-via-`/edit-play`; edit-play is
interactive-only (fully gated, human-checkpoint) and cannot run headless in this environment,
so the compiled output was produced by hand to match what edit-play would emit from the
current `reference/ice.md` (fingerprint above). **The `compiled_by` line names edit-play for
provenance intent, but no edit-play run actually occurred and convergence is UNVERIFIED.**
An interactive `/edit-play` convergence run against `reference/ice.md` is **REQUIRED** —
confirming the emitted SKILL matches this hand-compiled body and refreshing the fingerprint —
**before this direct-model-write pattern is fanned out to the other 12 model-writing plays**;
the fan-out must not proceed on an unverified reference. Note also: `reference/ice.md` C12
distinguishes the model-delta commit from the Standard Play Close (evidence + delivery report)
that /discover-capabilities still runs; the close anchor block is retained (required by `check-components`
structural.js and the create-play G12 emit on every play), and the `feat(model)` commit is the
separate lightweight persist step, so both coexist as C12 describes.
