---
name: vision
position: both
description: 'Turn business intents, a business goal, or both into the seed of the product model — or grow the model already there — a detailed domain grounding doc, directional capability grounding docs with their agent intent, the spine entries that wire them, the links to the business intents both ways, and a directional product profile — written directly in place on the live model. Builds on whatever /intent or any play already wrote (light domain pages, capabilities waiting in the holding folder, proposed intents) and never waits for another play. The CXO conversation of the ProductOS command model. Use when starting or growing a product area, before /understand and /shape. Run by hand, it opens its own change and lands it on main — no later play is needed to finish it; handed a drive''s contract, it opens nothing, does not stop at its checkpoint, works on the drive''s branch and leaves a review record for the drive''s end review.'
user-invocable: true
---

# vision

Turn business intents, a business goal, or both into the **seed** of the product model —
or grow the model already there: a **detailed domain** grounding doc, **directional
capability** grounding docs with their `## Agent intent (ICE)`, the **spine** entries that
wire them (domain + capability nodes), the links to the business intents (both ways), and a
**directional** product profile. /vision is
the **CXO conversation** — what you take to a CXO and get back: strategic, directional,
CXO altitude. The domain is named and detailed; each capability is named and given
directionality only. The deeper work — detailing the capabilities and introducing their
functionalities (/understand, the product-manager step), then breaking the model into
deliverable end-to-end verticals and epics (/shape, the product-owner step) — is not done
here.

**One model, nothing waits (ontology v4, #637).** /intent and /vision write the same tree —
domain → capability → functionality, the business intents beside it, one spine — and either
may run first. /vision starts from whatever the model holds: it accepts proposed intents
(it never runs the workable check and never waits for a confirmation), raises a light domain
page to the full page keeping its intent, places each capability waiting in the holding
folder `capabilities/<id>/` under a domain (moving its page unchanged and fixing the intent
pages' links), adds light directional detail to capabilities another play wrote, and never
adds the same capability twice. Every part it links to an intent is linked both ways — the
part's spine `intents` and the intent page's Touches list — by the persist script. Anything
missing or odd is a warning, never a stop.

**Pipeline position: both.** /vision stands on its own (ADR 029 §4; #616): run by hand, it opens its own change and lands it. **Inside a drive** (ADR 029 §2–3; #614; `standards/rules/drive-contract.md`) the drive hands it a contract (`--contract`); then it runs no `start-change` and no end sequence, does not wait at its checkpoint (Step 6 writes a review record for the drive's end review instead), and commits its model change on the drive's branch. The D2 rule prepends `start-change` — resolve or create the issue, cut the branch off fresh main, optional worktree, init STM — and, after the model delta is committed, appends the close sequence `commit-change → propose-change → review-change → merge-change`, landing the seed on main. No later play needs to run for /vision's work to be finished: /understand and the plays after it start from main. It writes the persistent product model **directly, in place** (additively) on the started branch — there is no draft copy and no apply/promote step; review is the branch git diff and the end PR. (#437, #500, ADR 026; position changed from start to both in #616.)

**Write discipline (ADR 026, `standards/rules/direct-model-write.md`).** The LLM authoring
skill writes ONLY the per-node grounding docs (`domain.md`, `capability.md`) straight to
the live model — new docs, and updates that keep every section and agent-intent line they
had (C6; the keep check proves it); it never removes or moves a doc and never writes a shared
file. Every shared-file mutation (the spine `_spine.yaml` with its `profile` block, and the
intent pages' Touches lists) and every page move is done by the deterministic keyed persist
script, in place: it adds entries whose id is absent and the profile only if none exists,
makes only the named updates to an existing entry (set an empty `domain`, repoint `doc`,
raise `detail`, refresh `one_line`, add to `intents`), places holding-folder capabilities,
and refuses anything else (the node-level containment the file-level scoped guard cannot
see inside the shared spine). The model tree is asserted clean once start-change has cut the
branch (F9) and the play commits its own model delta after approval (C9), so the working-tree
diff vs HEAD is exactly this run's delta. Containment is a post-write scoped guard
(`scoped_write_guard.py`), not a draft.

## Compiled From

This play was compiled from the vision ICE (`reference/ice.md`) by play-editor
(#466 Batch C, Level 3 rollout per ADR 025; #467 Batch B — the checkpoint upgraded to a
conditional learned gate, see `standards/rules/gate-config.md`; #500 — migrated to
direct-model-write per ADR 026 and `standards/rules/direct-model-write.md`; #616 — position
start → both, so /vision lands its own change instead of leaving it for /roadmap; #637;
#614).
Intent defines constraints (C1–C11) and failure conditions (F1–F13); the expectation
defines success scenarios (S1–S7), a Done means (D1–D4, baked to
`stop-condition.yaml`), and one recovery entry per failure condition.
To modify this play, update `reference/ice.md` and recompile with play-editor.
Do NOT edit this file manually — it is a compiled artifact.

## Role

You are the orchestrator. You own the workflow and the step order. You delegate the
domain work — KB grounding and seed authoring — to the `product-os-keeper` agent via
JSON contracts over files on disk, and you run the mechanical work (shape/spine
validation, grounding, the content-quality eval, the keyed in-place persist, and the
post-write scoped guard) through bundled scripts and an isolated judge. You never write
the grounding docs or the spine yourself, you never remove a node or lose what one holds, and you
never persist the shared spine before the single checkpoint (C7) resolves — a typed
approval, a recorded config skip, or a recorded policy auto-pass.

**Forbidden:** hand-writing grounding docs or spine entries; writing the shared spine
(`_spine.yaml`/profile) by any route other than `scripts/persist_seed.py`; committing
the model delta before the Step 6 gate resolves; changing an existing spine entry beyond
the named updates, or removing or cutting down an existing grounding doc (keep what is
there — C6/F5); writing a functionality, a detailed
capability, acceptance criteria, or a `set`/`locked` profile (over-reach — F3); running the
seed writes against a dirty product-os tree (C9/F9); closing COMPLETED without the
stop-condition verdict reading held (C8/F7).

**Agent boundaries:**

| Agent | Domain | Skill it invokes | Phases |
|-------|--------|------------------|--------|
| `product-os-keeper` | Ground the goal in the KB; author the directional seed — the detailed domain doc + directional capability docs written in place on the live model, and the spine-delta (spine entries + directional profile) emitted into the manifest | `search-kb`, `propose-kb-node`, `author-vision-seed` | Grounding, Author |

`product-os-keeper` is the single **domain agent** this play uses (1 of the ≤5
budget). The utility work — cutting the branch and resolving the issue — is `start-change`
(injected head), not a domain agent. The content-quality judge always runs as an isolated,
clean-context sub-agent (optionally on a configured different model) — never the
orchestrator's own context.

## Pre-flight

| Check | Constraint | Action on Failure |
|-------|-----------|-------------------|
| Resolve config + `product_base` (`.garura/core/config.yaml`) | — | Hard halt |
| Resolve `grounding-eval.judge` (optional model override) | C2 | Default: sub-agent on the session model |
| Business intents (ids, or /intent's save record) and/or a business goal present (play argument; with neither, interview the user for a goal) | C10 | Gather (interview), not a halt |
| Drive contract: when `--contract <file>` is passed, `check_drive_contract.py` accepts it (valid, complete, current branch = the drive's branch) and writes `run.json` | C11/F12 | Hard halt (REC12) |
| **Clean model tree** — after start-change (Step 0), or at once inside a drive, `git status --porcelain -- <product_base>product-os` is empty | C9/F9 | Hard halt (REC9) |

Resolve the pre-flight facts mechanically with the bundled resolver — do not derive
them by inference:

```
python3 scripts/preflight.py --play vision --config .garura/core/config.yaml
```

It returns one JSON object of facts. /vision reads `product_base` (the live model — the
spine `_spine.yaml` and the grounding docs), `stm_base` (working artifacts + evidence),
the resolved `grounding-eval.judge` config (the optional judge model override), and
`evidence_record` (the D1 gate). If `product_base` is null, hard halt — there is nowhere
to seed the model. The business intents and the business goal are runtime inputs: take
them from the play argument (intent ids, or the path of /intent's `intent-manifest.json`, or
a goal as text — any of them, or both); with neither, interview the user for a goal before
Step 1.

**Run by hand or inside a drive (C11).** Check the drive contract first — always, so the run
records which path it takes:

```
python3 scripts/check_drive_contract.py --play vision \
    --branch "$(git branch --show-current)" [--contract <contract.json>] \
    --out <working>/run.json
```

`run.json` reads `in_drive: false` with no contract — every step below runs as written. With
a valid contract it reads `in_drive: true` with the drive's `drive_run_id`, `branch`, `issue`,
`review_dir`, and /vision's own `inputs` (intent ids or `/intent`'s save record, and/or a goal)
and `answers`. Inside a drive the intents and goal come from those inputs; if the contract and
the model give neither, the run stops and asks the person (ADR 029: a new question stops the
drive) — it never picks a goal itself. A non-zero exit (an invalid contract, or the current
branch is not the drive's) is a hard halt (REC12).

`<working>` — the run's working folder — is `{stm_base}_shaping/vision/<product_slug>/`;
the grounding, the seed manifest, the change-shape, the persist record
(`persist-manifest.json`), and the captured scoped-guard report (`guard-report.json`) all
live under it. These are STM, non-model artifacts (ADR 008/017) — the model itself is
written IN PLACE under `<product_base>product-os/`, never into `<working>`. The stop
condition evaluates against `<working>`.

**Clean-tree assertion (C9/F9, ADR 026).** start-change cuts the branch off fresh main, so
the product-os tree is clean by construction; still assert it right after Step 0 (inside a
drive, at once — the earlier plays in the drive committed their model change) — `HEAD`
is only a correct base for the scoped guard and the change-shape if the tree is clean
before the seed writes:

```
test -z "$(git status --porcelain -- <product_base>product-os)" || { echo "HALT: dirty product-os tree (REC9)"; exit 1; }
```

If dirty, halt and ask for a clean model tree (commit or revert the pending model edits)
before /vision writes the seed.

Right after the resolver, record the session identity stamp's start marker (#463 —
soft-fail, never a halt):

```
python3 scripts/session_stamp.py --phase start \
    --marker "{stm_base}_shaping/vision/status/session-stamp-vision.json" \
    --cwd "$(pwd)" --branch "$(git branch --show-current)"
```

**Resume check:** if `{stm_base}_shaping/vision/status/<product_slug>.json` exists,
resume — skip completed steps, reset any in-progress step to pending, continue from
the first incomplete.

## Task DAG

Create ALL tasks immediately after resolving config — before any domain work.
The play owns this DAG; the agent must not edit its top-level tasks.

Write-then-review (ADR 026): the FULL model delta — the LLM docs AND the keyed persist's
spine/profile merge — is written to the live model BEFORE the checkpoint, so the guard,
the change-shape, and the human all see the real delta. Nothing is COMMITTED before the
gate resolves; cancel reverts the uncommitted writes.

```
[T0] start-change (injected — start; skipped in a drive) blockedBy: []
[T1] Ground the goal                                blockedBy: [T0]
[T2] Author the seed (docs to live)                 blockedBy: [T1]
[T3] Validate the live docs                         blockedBy: [T2]
[T4] Persist (keyed, in place — spine/profile)      blockedBy: [T3]
[T5] Guard the full delta + classify the shape      blockedBy: [T4]
[T6] Checkpoint (approval over the full git diff)   blockedBy: [T5]
[T7] Commit the model delta                         blockedBy: [T6]
[E1] commit-change (injected — end; skipped in a drive)  blockedBy: [T7]
[E2] propose-change (injected — end; skipped in a drive) blockedBy: [E1]
[E3] review-change (injected — end; skipped in a drive)  blockedBy: [E2]
[E4] merge-change (injected — end; skipped in a drive)   blockedBy: [E3]
[T8] Scenario Validation                            blockedBy: [E4]
[T9] Close                                          blockedBy: [T8]
```

Mark each task in-progress before its step and completed right after its eval passes.
No runtime reordering. On resume, skip completed and reset in-progress to pending.

## Workflow

### Phase: Start (injected — D2 position: start)

**Step 0 — start-change** · Owner: `start-change` (sub-play) · Depends on: pre-flight
*Skipped when `run.json` reads `in_drive: true` — the drive opened the change (C11).*
Run the start-of-pipeline member as a sub-play, dispatched with `parent_run_id` so it
emits only its own C1 evidence and this play's close absorbs it. It resolves or creates
the issue for this /vision run, cuts the branch off fresh main, sets up a worktree iff config
calls for it, and initializes the STM workspace. The change it opens is landed by this
play's own end sequence (Steps E1–E4), not by a later play.

    {
      "play":          "start-change",
      "parent_run_id": "<this run id>",
      "inputs":  { "title": "<the business goal, e.g. 'vision: <goal>'>" },
      "outputs": { "result": "{stm_base}_vision/start/start-change.json" }
    }

start-change owns its own evals (issue anchored, branch off latest main, worktree per
config, STM initialized); they are not re-checked here. Immediately after it returns,
run the clean-tree assertion (pre-flight, C9/F9) so `HEAD` is a correct base for the
guard and the change-shape.
**SE-10 (F9/C9):** the product-os tree was clean once start-change had cut the branch —
the assertion (`git status --porcelain -- <product_base>product-os` empty) passed before
any seed write; a dirty model tree halts (REC9), so the change-shape and the scoped guard
reflect only this run's delta.

### Phase: Grounding

**Step 1 — Ground the goal** · Owner: `product-os-keeper` · Depends on: Step 0
When the run starts from business intents, the play first reads them — mechanically, never
refusing (C10): a proposed intent is accepted, a missing page is a warning:

```
python3 scripts/read_intents.py --product-base <product_base> \
        ( --intent <id> [--intent <id> ...] | --intent-manifest <intent-manifest.json> ) \
        --out <working>/intents.json
```

The goal is then drawn from the intent pages (title, outcome, why) — joined with a typed goal
when both are given. The agent does two things, in order: (1) route the goal to its **domain** with
`search-kb`, then (2) read that domain's full shelf through the KB router
(`python3 $KB shelf <domain>`) to **enumerate the candidate capability set** the
domain offers — breadth, not a single placement. For any capability or whole domain the
KB does not cover, it raises a `propose-kb-node` proposal. It writes the grounding
(domain + the candidate-capability set, each with its KB shelf reference) and any
proposals to disk:

    {
      "task":    "route the goal to its domain, then enumerate the candidate capability set from that domain's shelf; propose KB nodes for gaps",
      "inputs":  { "goal": "<the business goal, or drawn from the intents>",
                   "intents": "<working>/intents.json (when starting from intents)" },
      "outputs": { "grounding": "<working>/grounding.yaml",
                   "proposals_dir": "<working>/proposals/" }
    }

It returns the same contract with the output paths confirmed on disk — never the
routing data inline. The grounding must carry **one or more** candidate capabilities
(a domain seed is rarely a single capability). A net-new domain routes through
`propose-kb-node`'s own review; record that proposal as evidence and proceed — do not
block the seed on a KB-write approval (the single human gate is Step 6).

### Phase: Author (write the docs to the live model, ADR 026)

**Step 2 — Author the seed (docs to live)** · Owner: `product-os-keeper` · Depends on: Step 1
The agent invokes `author-vision-seed` to write or grow the directional seed. Per ADR 026 the
skill writes the per-node docs **straight to the live model** — a **detailed** `domain.md`
(Theme template; a light page is raised, keeping its intent) and a **directional**
`capability.md` per new capability (directional stage, ending in `## Agent intent (ICE)` when
it serves an intent), all at CXO altitude, in place under `<product_base>product-os/`; on a
capability another play wrote it adds only light directional detail, keeping every line —
and emits the spine-delta (new domain and capability entries with their `intents`, the named
`updates` to existing entries — including the `domain` of each holding-folder capability it
places — and the directional `profile` block), `same_as` for each KB candidate that already
exists, and `warnings`, as structured data in `seed-manifest.yaml`. It writes NO shared model
file (`_spine.yaml`, the profile, an intent page) and moves no page — the keyed persist
(Step 4) applies the manifest:

    {
      "task":    "author the directional vision seed from the goal + grounding — write or grow the detailed domain doc + directional capability docs in place on the live model (keeping what is there), emit the spine-delta (new entries, named updates, directional profile), same_as and warnings into the manifest",
      "inputs":  { "goal": "<the business goal>",
                   "grounding": "<working>/grounding.yaml",
                   "proposals_dir": "<working>/proposals/",
                   "intents_path": "<working>/intents.json (when starting from intents)",
                   "product_base": "<product_base>",
                   "manifest_path": "<working>/seed-manifest.yaml" },
      "outputs": { "manifest": "<working>/seed-manifest.yaml" }
    }

The skill reads `product_base` to see what exists — it emits new spine-delta entries only
for ids absent from the live spine, and named `updates` for the rest — and writes the
`domain.md` + `capability.md` docs IN PLACE under `<product_base>product-os/`. It writes
`seed-manifest.yaml` under `<working>` (STM). It writes NO `_spine.yaml`, NO profile, NO
intent page. It returns the contract with the output paths on disk — never inline content.

**Step 3 — Validate the live docs** · Owner: play · Depends on: Step 2
Run the two guards over the LIVE docs this run wrote, before the checkpoint — shape first
(cheap, deterministic), then content quality (the judge). Under direct-model-write the docs
are already written in place, and the spine has NOT yet been mutated for this run (the keyed
persist runs after Step 3). So the linter runs over the live tree, and the newly written
docs are linted; full spine↔doc consistency for the new entries is completed after the keyed
persist (Step 5) writes those entries.

```
python3 scripts/lint_grounding.py --root <product_base>/product-os
python3 scripts/grounding_check.py --manifest <working>/seed-manifest.yaml \
        --proposals-dir <working>/proposals
```

Then run the **content-quality eval** over the grounding docs this run wrote or changed (the
detailed `domain.md` and every directional `capability.md` it wrote or added to, at their live
paths — a page it only moves, unchanged, is not re-judged) as a **concurrent
read-only fan-out** (`standards/rules/concurrent-fanout.md`): dispatch one isolated,
clean-context judge sub-agent PER doc, ALL IN ONE CONCURRENT BATCH — each handed the judge
prompt (`standards/rules/grounding-eval.md`), its doc, and the kind's per-section guidance
(it sees neither the brief nor the author's reasoning), on the model from
`grounding-eval.judge.model` (default the session model). The three safety conditions hold:
each judge only READS its own doc, writes only its own verdict JSON, and no judge depends on
another. **Join** — wait for every verdict to return before gating any. Then gate every
returned verdict (order-stable, so the outcome is identical to a serial run):

```
python3 scripts/grounding_gate.py --verdict <verdict.json>
```

**SE-1 (F1/C1):** `lint_grounding.py` exits 0 over the live docs this run wrote — every
grounding doc conforms to its template (domain → Theme; capability → directional stage);
full spine↔doc consistency for the new entries completes after the keyed persist (Step 5).
**SE-2 (F2/C2):** the content-quality eval gate (`grounding_gate.py`) passes for EVERY
grounding doc — each section self-explains at CXO altitude and the doc clears the
stranger test. A label-only or thin doc fails.
**SE-3 (F3/C3):** no over-reach — no capability doc is in the detailed stage, no
functionality doc appears, no acceptance criteria appear, and the manifest's profile is
not `set`/`locked` (`lint_grounding.py` stage check + manifest scan).
**SE-4 (C4):** directional state — every capability entry in the manifest is
`status: proposed` and `detail: directional`; the profile is `state: directional`.
**SE-5 (F4/C5):** `grounding_check.py` exits 0 — every capability the run adds, places or
changes (another play's included) is listed in the manifest with a KB shelf match or an
existing KB-node proposal; none is ungrounded.
On any GAP, apply the matching recovery (REC1–REC4) and re-run before the checkpoint —
for a content-eval fail (SE-2), REC2 rewrites the doc to the judge's cited fixes and
re-judges until the gate passes.

### Phase: Persist (write the full delta first, ADR 026 write-then-review)

**Step 4 — Persist (keyed, in place — spine/profile)** · Owner: play · Depends on: Step 3
Write-then-review (ADR 026): the FULL model delta is written to the live model BEFORE the
checkpoint, so the guard, the change-shape, and the human all see the real delta. The docs
are already on the live model (Step 2). `persist_seed.py` now writes the SHARED files in
place: it adds spine entries whose id is absent and the profile only if the live spine has
none; it applies only the named `updates` to existing entries and REFUSES the whole run,
before any write, on any other field, an unknown id, a lowered `detail` or a detailed
capability (the node-level containment the file-level guard cannot provide); it moves each
holding-folder capability that now has a domain into the domain's folder, byte-identical;
it adds to each domain the intents of the capabilities under it that the run touched; and it
writes each intent page's Touches list (relinking moved pages; `adds` for parts new in this
run, `changes` for parts already there). A missing intent page or an unplaced capability is a
`warnings` line, never a stop. No draft, no doc copy. Nothing is COMMITTED yet — the commit
(Step 7) happens only after the gate approves; on cancel the whole delta is reverted (Step 6):

```
python3 scripts/persist_seed.py --seed-manifest <working>/seed-manifest.yaml \
        --product-base <product_base> --out-manifest <working>/persist-manifest.json \
        [--intents <working>/intents.json]
```

**SE-6 (F5/C6):** the persist manifest's `written` list contains no entry that already
existed (those appear only in `skipped`), every `updated` entry names only named-update
fields, every `placed` entry reads `unchanged: true`, and the profile is written only when
the live spine had none; the keep check and the scoped guard (Step 5) confirm no existing
doc lost a section and no path outside the run's write scope changed.
**SE-11 (F10/C10):** the run never refused, stopped or waited over another play's work:
`intents.json` lists every input intent, proposed ones `accepted: true`; no workable check
ran; anything missing appears in the persist manifest's `warnings`, and the run continued.
**SE-12 (F11/C10):** links are whole and nothing is added twice: no capability id in the
spine-delta's new `capabilities` is also in the seed manifest's `same_as`; for every
`links` entry the part's spine `intents` names the intent and the intent page's Touches list
names the part; every capability built from an input intent has a domain or a `warnings`
line saying why not.

### Phase: Guard + Classify (over the full delta)

**Step 5 — Guard the full delta + classify the shape** · Owner: play · Depends on: Step 4

**The run's write scope (the per-play guard policy, ADR 026).** /vision adds and grows
grounding docs but never removes one; it moves holding-folder pages; it changes intent pages
only through the persist's Touches list and relinking; the persist merges the spine:

    --add-only    'product-os/*/domain.md'               # a domain page may be added …
    --modify-only 'product-os/*/domain.md'               # … or grown in place — never removed
    --add-only    'product-os/*/*/capability.md'         # a capability page may be added …
    --modify-only 'product-os/*/*/capability.md'         # … or grown in place — never removed
    --remove-only 'product-os/capabilities/*/capability.md'  # a holding-folder page may only leave (placed)
    --modify-only 'product-os/intents/*.md'              # an intent page may only change (Touches, links)
    --allow       'product-os/_spine.yaml'               # the shared spine + profile (the keyed persist)

**Keep check, then guard ONCE over the full delta (C6).** After ALL writes (the LLM docs from
Step 2 and the keyed persist from Step 4), run the keep check — every existing doc the run
changed kept each section and agent-intent line it had; its report is the stop condition's
D4 input — then the scoped guard a single time over the whole delta (its `ok` field is D3).
Then re-run the linter over the merged live spine to complete spine↔doc consistency (a
capability whose spine entry names an intent and has no `## Agent intent (ICE)` is a warning):

```
python3 scripts/check_kept.py --product-base <product_base> --base-ref HEAD \
        --out <working>/kept-report.json
python3 scripts/scoped_write_guard.py --product-base <product_base> --base-ref HEAD \
        --add-only 'product-os/*/domain.md' --modify-only 'product-os/*/domain.md' \
        --add-only 'product-os/*/*/capability.md' --modify-only 'product-os/*/*/capability.md' \
        --remove-only 'product-os/capabilities/*/capability.md' \
        --modify-only 'product-os/intents/*.md' --allow 'product-os/_spine.yaml' \
        --out <working>/guard-report.json
python3 scripts/lint_grounding.py --root <product_base>/product-os \
        --spine <product_base>/product-os/_spine.yaml
```

If the keep check fails, restore the doc from HEAD and re-apply only the additions (REC5). If
the guard exits non-zero (a doc was removed, or a path outside the run's write scope changed),
re-run with `--restore` to revert the offending paths, apply REC5, and re-persist before the
checkpoint.

**Classify the full working-tree delta (C7).** Classify the model tree's diff vs HEAD — now
the FULL delta (docs + spine entries + profile), per ADR 026 write-then-review (no draft
dir):

```
python3 scripts/classify_change.py --play vision \
        --product-base <product_base> --base-ref HEAD --out <working>/shape.json
```

**SE-6 (F5/C6):** the keep-check report and the scoped-write guard report both read
`ok: true` — the model delta is confined to the run's write scope (docs added or grown, never
removed; holding-folder pages only moved out; intent pages only changed; the spine merged by
the keyed persist), and no existing doc lost a section or an agent-intent line.

### Phase: Checkpoint (conditional gate, C7)

**Step 6 — Human review (class: standard, conditional)** · Owner: play · Depends on: Step 5
**Inside a drive (C11), this step does not wait.** Resolve the learned policy exactly as below.
If the shape would auto-pass, record the auto-pass and its ledger line as below. Otherwise,
render the checkpoint exactly as it would have been shown (the same content as the "on" path
below) to `<working>/checkpoint.md`, write it as the drive's review record, and append the
crossing as deferred:

```
python3 scripts/write_drive_review.py --run <working>/run.json \
        --summary <working>/checkpoint.md \
        --attach shape=<working>/shape.json --attach kept=<working>/kept-report.json \
        --attach guard=<working>/guard-report.json --attach persist=<working>/persist-manifest.json \
        --ts <run ts>
python3 scripts/gate_eval.py append --ledger <gates.conditional.ledger> --play vision \
        --issue <the drive's issue> --shape <shape-key> --predicted gate \
        --human deferred_to_drive_review --ts <run ts>
```

Record `checkpoint deferred to the drive's review (drive <drive_run_id>)` as a Checkpoint
Decisions row and proceed to Step 7. Nothing is reverted: a cancel at the drive's review is the
drive's to act on. Run by hand, the rest of this step applies as written.

This checkpoint is a **conditional gate** (#467) per `standards/rules/gate-config.md` —
/vision is one of the eleven conditional document plays. Resolve it first match wins:
pinned (n/a here) → `gates.plays.vision` → the learned policy → `gates.classes.standard`
→ `gates.default` (absent ⇒ on). For the policy lookup, use the shape key classified in
Step 5.

Look the shape key up in the config-resolved policy (`gates.conditional.policy`):
**auto-pass** iff the shape is in the policy's `auto:` block AND not in `never_auto:`
AND Step 3 + Step 5 stand with no blocking finding (a `lint_grounding.py` gap, a
`grounding_gate.py` content-eval fail, or a guard violation). On auto-pass, do NOT wait:
record `gate auto-passed by learned policy (shape: <shape-key>, policy v<version>)` as a
Checkpoint Decisions row, include the working-tree diff summary in the run record, append
the crossing's live-eval ledger line, and proceed to Step 7 (commit):

```
python3 scripts/gate_eval.py append --ledger <gates.conditional.ledger> --play vision \
        --issue <strategy issue> --shape <shape-key> --predicted auto --human auto_pass \
        --policy-version <policy version> --ts <run ts>
```

Anything else resolves the gate on (an explicit `gates.plays.vision: off` instead
records `gate skipped by config (<resolution path>)` as a Checkpoint Decisions row and
proceeds). When on, present the proposed seed **inline over the real model git diff** — the
domain (its intent, the bet, its guiding rules, the directional capabilities; raised from a
light page when it was one), each capability's directional intent and agent intent, the
capabilities placed from the holding folder, the intent links written (each intent's Touches
list), the persist's `warnings`, and the directional profile (shape + rough NFR levels) —
render the approval prompt (`standards/templates/approval-prompt.md`) and wait for the
typed response. Approve → continue to Step 7 (commit). **Cancel → revert the working tree
(ADR 026 step 6):** the full delta is already on disk, so run the guard with `--restore` and
an EMPTY allow set to `git restore` the modified model paths and `git clean`/remove the new
ones (byte-clean back to HEAD), then halt — nothing was committed, and cancel means "revert
what was written" (the branch, issue, and STM start-change created are its own committed
side effects and are left as-is):

```
python3 scripts/scoped_write_guard.py --product-base <product_base> --base-ref HEAD \
        --restore --out <working>/guard-report.json   # empty --allow ⇒ every model path reverted
```

Then append the crossing's live-eval ledger line with the human's real action:

```
python3 scripts/gate_eval.py append --ledger <gates.conditional.ledger> --play vision \
        --issue <strategy issue> --shape <shape-key> --predicted gate \
        --human <approved_clean|approved_edited|rejected> --ts <run ts>
```

`<strategy issue>` is the issue Step 0 resolved for this run.
`<gates.conditional.ledger>` / `<gates.conditional.policy>` resolve from config
`gates.conditional` (defaults `.garura/core/gate-evals.jsonl` /
`.garura/core/gate-policy.yaml`); `<policy version>` is the policy file's `version:`
field. `<run ts>` is the run's own UTC timestamp, derived the same way the close
derives `ts` (`date -u`), passed by the orchestrator.
**SE-7 (F6/C7):** the model delta was written to the live model by Steps 2 + 4 but is
COMMITTED (made durable) only at Step 7 on approval — so no product-model change is
COMMITTED before the gate resolves (a typed approval, a recorded config skip, or a recorded
policy auto-pass); on cancel the whole working-tree delta is reverted before any commit, so
nothing is left on the tree.
**SE-9 (F8):** every crossing of this gate appended exactly one live-eval ledger line
(shape, predicted `gate|auto`, the human's real action or `auto_pass`), and an
auto-pass fired only for a shape the policy lists in `auto:` (and not in `never_auto:`)
with no blocking finding standing.
**SE-13 (F12/C11):** `run.json` records the path taken. Inside a drive (`in_drive: true`): no
`start-change` (Step 0) or end-sequence step (E1–E4) ran, the run did not wait at Step 6, and
every commit is on the contract's branch. By hand (`in_drive: false`): Step 0, Step 6 and
E1–E4 ran as written.
**SE-14 (F13/C11):** inside a drive, when the gate did not auto-pass, a
`<review_dir>/vision-<ts>.json` record exists with `decided: false`, its summary file equals
`<working>/checkpoint.md`, and its attachments exist; the gate ledger holds exactly one line for
the crossing, reading `deferred_to_drive_review` (or `auto_pass` on a policy-listed shape) and
never an approval; no goal or answer was filled in that the contract or the person did not give.

### Phase: Commit (make the delta durable, ADR 026 step 7)

**Step 7 — Commit the model delta** · Owner: play · Depends on: Step 6
The gate approved (or auto-passed / was skipped by config / was deferred to the drive's review
inside a drive). Commit the full model delta on the branch — the drive's branch inside a drive
(C9, ADR 026 step 7) — a lightweight persist step that makes the writes durable
and advances HEAD so the end sequence lands exactly this run's delta; it is NOT the end
sequence itself. A cancelled checkpoint never reaches this step (nor the end sequence) — its
tree was already restored in Step 6:

```
git add -- <product_base>product-os
git commit -m "feat(model): seed <domain> — domain, directional capabilities, profile (#<issue>)"
```
**SE-8 (F7/C8):** the close is stop-condition gated — `check_stop_condition.py` over the
baked `stop-condition.yaml` (D1 the persist record `persist-manifest.json` exists; D2 it
stamps `applied: true`; D3 the captured `guard-report.json` reads `ok: true`; D4 the captured
`kept-report.json` reads `ok: true`) must read **held** before any COMPLETED close, and the
model delta is committed (C9); a run whose persist, keep check or guard did not land closes
HALTED, never COMPLETED (REC7). No clause depends on another play: warnings never make one
unmet.

### Phase: End sequence (injected — D2 position: end)

*Skipped when `run.json` reads `in_drive: true` — the drive lands its own change (C11).*
After the model delta is committed, the D2 rule injects the close sequence — each a sub-play
dispatched with `parent_run_id`, resolving its own context — to commit any remaining change,
raise the PR, take the verdict, and merge the seed to main (C8).

**Step E1 — commit-change** · blockedBy: Step 7

    { "play": "commit-change", "parent_run_id": "<this run id>", "inputs": {}, "outputs": { "result": "{stm_base}_vision/end/commit-change.json" } }

**Step E2 — propose-change** · blockedBy: E1

    { "play": "propose-change", "parent_run_id": "<this run id>", "inputs": {}, "outputs": { "result": "{stm_base}_vision/end/propose-change.json" } }

**Step E3 — review-change** · blockedBy: E2

    { "play": "review-change", "parent_run_id": "<this run id>", "inputs": {}, "outputs": { "result": "{stm_base}_vision/end/review-change.json" } }

**Step E4 — merge-change** · blockedBy: E3

    { "play": "merge-change", "parent_run_id": "<this run id>", "inputs": {}, "outputs": { "result": "{stm_base}_vision/end/merge-change.json" } }

Each end member owns its own evals (commit grouped by concern, PR opened, verdict posted, branch
merged + cleaned); they are not re-checked here. A review-change reject stops the chain before
merge; the land on main keeps its pinned human approval (merge-change C7).

### Phase: Scenario Validation

**Step 8 — Scenario evals** · Owner: play · Depends on: the end sequence
- **SCE-1 (S1 — CXO / product strategist):** the seed this run persisted — a domain entry
  with a detailed `domain.md`, at least one `proposed` + `directional` capability with a
  directional `capability.md`, and a `directional` profile — clears both guards
  (`lint_grounding.py` clean; `grounding_gate.py` passes for every grounding doc) and is
  present in the live spine; the run's change is landed on main by the end sequence
  (`{stm_base}_vision/end/merge-change.json` reports the PR merged), with no later play
  needed to finish it; the stop-condition verdict reads held.
- **SCE-2 (S2 — architect):** every persisted capability traces to a KB shelf or a
  recorded proposal in the seed manifest (`grounding_check.py` is clean).
- **SCE-3 (S3 — product owner, re-run keeps what is there):** on a re-run over an existing
  domain, `written` holds only newly-added entries, `updated` names only named-update fields,
  every other pre-existing entry is in `skipped`, the keep-check and scoped-guard reports read
  `ok`, and a re-run with nothing new leaves every model file byte-identical.
- **SCE-4 (S4 — reviewer):** the Step 6 checkpoint showed the domain, the directional
  capabilities, and the directional profile inline over the real model git diff, and no
  product-model change was COMMITTED before that gate resolved — on cancel the working tree
  returns byte-clean to HEAD — or, on the auto-pass path (a policy-listed shape), the gate
  resolved with no wait and the recorded auto-pass, the appended ledger line, and the diff
  summary stand in the approval's place.
- **SCE-5 (S5 — product strategist, after /intent):** starting from /intent's intents (some
  proposed) with a light domain and a holding-folder capability: `intents.json` accepts every
  input intent; the persist manifest's `placed` names the holding-folder capability with
  `unchanged: true`, `updated` raises the domain to `detailed`; each KB candidate already in
  the model is in `same_as` and not added; every intent's Touches list and every linked part's
  spine `intents` match both ways; the keep check and guard read `ok`; `warnings` is empty.
- **SCE-6 (S6 — founder, by hand, nothing else run):** with only a typed goal and an empty
  model the run seeds as in SCE-1; with intents whose pages are gone the run still closes
  COMPLETED and the persist manifest names each missing page in `warnings`.
- **SCE-7 (S7 — Kickoff drive):** handed a valid contract, `run.json` reads `in_drive: true`
  with the contract's `drive_run_id` and branch; no `start-change` or end-sequence step ran; the
  current branch equals the contract's; a `vision-<ts>.json` review record with
  `decided: false` and its summary exist in the contract's `review_dir`; the ledger line reads
  `deferred_to_drive_review` (or `auto_pass`); the model delta is committed on the drive's
  branch; the stop-condition verdict reads held. The same play run by hand reads
  `in_drive: false` and ran every step.

### Phase: Evidence & Close

**Step 9 — Close** · Owner: play · Depends on: Step 8
Run the Standard Play Close. /vision is a **product-scoped** play (no issue of its own) —
use the product-scoped evidence base and slug. Evidence recording is play-only and
config-gated per the D1 evidence rule (`standards/rules/evidence-recording.md`).
**SE-8 (F7/C8):** the close is stop-condition gated — `check_stop_condition.py` over
the baked `stop-condition.yaml` (D1 the persist record exists; D2 it stamps
`applied: true`; D3 the captured guard report reads `ok: true`; D4 the captured keep-check
report reads `ok: true`) reads **held** before the run closes COMPLETED, and the model delta
is committed (C9); anything else closes HALTED with the unmet clauses named.

```bash
# --- Standard Play Close (canonical; see standards/rules/play-close.md) ---
# Path tokens resolved at pre-flight (resolve here if not already):
#   ltm_project_target  = yq '.ltm.project-target' .garura/core/config.yaml
#   evidence_base, slug:
#     project-scoped play : evidence_base="${stm_base}${issue}/evidence/vision/"   ; slug="#${issue}"
#     product-scoped play : evidence_base="${product_base}_evidence/vision/"        ; slug="${product_slug}"
evidence_template=$(cat "${ltm_project_target}standards/templates/evidence-file.md")
delivery_template=$(cat "${ltm_project_target}standards/templates/delivery-report.md")
ts=$(date -u +%Y%m%d-%H%M%S)
evidence_dest="${evidence_base}${ts}.md"
mkdir -p "$(dirname "$evidence_dest")"
# Session identity stamp (#463) — close phase; start phase ran at pre-flight
session_stamp=$(python3 scripts/session_stamp.py --phase close \
    --marker "${stm_base}_shaping/vision/status/session-stamp-vision.json")
# Stop-condition gate (#464) — Step C0: this play carries a baked manifest, so the
# gate is LIVE. Evaluate the Done means here as the close's authoritative input.
python3 scripts/check_stop_condition.py \
    --manifest "<play-dir>/stop-condition.yaml" \
    --base "<working>/" \
    --out "${stm_base}_shaping/vision/status/stop-condition-vision.yaml"
sc_exit=$?   # 0 held · 1 unmet · 2 error
# Conditional-gate policy refresh (#467) — soft: a distill failure never blocks the close
python3 scripts/distill_gate_policy.py --ledger "<gates.conditional.ledger>" --policy "<gates.conditional.policy>" --streak <gates.conditional.streak> --project "<project name from config>" || true
```

`/vision` is product-scoped: `evidence_base="${product_base}_evidence/vision/"` and
`slug="${product_slug}"` (the seeded domain's slug, e.g. `order-management`).

**Step C0 — bind the verdict.** `sc_exit == 0` (held) permits `status: COMPLETED`.
Anything else closes `HALTED` with `exit_reason: stop_condition_unmet` and the
evidence's Stop Condition section names every unmet clause — fix the state per REC7
(re-run the keyed persist, re-capture the scoped-guard report, or make the model-delta
commit) and re-evaluate; the close stays HALTED until the verdict reads held. An
unevaluable verdict is never a pass.

**Step C1 — Write evidence file.** Gated by the resolved `evidence.record` flag (global
+ per-play `evidence.plays.vision`; first match wins, absent ⇒ record). When false, skip
the write and record `evidence skipped (record=false)` in the report's pointer line.
Otherwise fill the `evidence-file.md` slots (play `vision`, run_id `vision-${ts}`,
product_slug, started_at/completed_at, status per C0, exit_reason; artifacts produced:
`grounding.yaml`, `intents.json` (when starting from intents), `seed-manifest.yaml`, the
persisted spine + grounding-doc paths, the persist manifest (`persist-manifest.json`, with
its placed pages, intent links and warnings), the captured `kept-report.json` and
`guard-report.json`, the
model-delta commit sha, the stop-condition verdict; the content-eval verdicts; step and
scenario eval results SE-1…SE-14 / SCE-1…SCE-7; `run.json` (`in_drive`) and, inside a drive, the review record's path; checkpoint decision from Step 6 (or the
`gate skipped by config` / `gate auto-passed by learned policy` row when the gate
resolved without a wait) plus the gate ledger line(s) appended this run; the session
identity stamp fields from $session_stamp (#463): session_id, ledger_file,
ledger_start_offset, ledger_end_offset (null when unresolved — never blocks the close);
and stop_condition per C0 with the Stop Condition section filled) and write to
`$evidence_dest`. Do NOT hand-author the body.

**Step C2 — Render delivery report.** Also render the **Next** line: resolve this play in `standards/rules/pipeline-next.md` and emit `**Next:** /<command> — <why>. Or run /next to see all recommended actions.` (only /next pointer, or omit, when the mapped command is null), per `play-close.md`. Fill the `delivery-report.md` slots and output the
report: `## vision Delivered — ${product_slug}`, the Run Summary table, the Pipeline
Steps table from the task DAG, the Artifacts Produced table (the seeded domain doc,
directional capability docs, spine entries, and profile), Next Steps (run /understand to
detail the capabilities and introduce their functionalities, and firm the profile), and a
pointer to `$evidence_dest`. Always emitted; never gated.

```bash
# --- end Standard Play Close ---
```

## Scenario Validation

| Scenario | Persona | Eval |
|----------|---------|------|
| S1 — end to end | CXO / product strategist | SCE-1 |
| S2 — grounding audit | architect | SCE-2 |
| S3 — non-destructive re-run | product owner | SCE-3 |
| S4 — the checkpoint | reviewer | SCE-4 |
| S5 — after /intent | product strategist | SCE-5 |
| S6 — by hand, nothing else run | founder | SCE-6 |
| S7 — Kickoff drive | product strategist | SCE-7 |

## Recovery

| For | Trigger | Direction | Handoff |
|-----|---------|-----------|---------|
| F1 | a grounding doc fails its template/shape, or a spine entry fails the schema or spine↔doc consistency | re-emit the failing doc or spine entry to conform and restore consistency before the checkpoint | autonomous |
| F2 | a grounding doc fails the content-quality eval | rewrite the failing doc to the judge's cited fixes — raise each flagged section to a self-explaining, CXO-altitude statement — and re-judge until the gate passes | autonomous |
| F3 | a functionality, a detailed capability, acceptance criteria, a `set`/`locked` profile, a `detail: detailed` capability, or a lowered `detail` appears | strip the over-reach — drop the functionality, demote the capability to directional, remove the acceptance criteria, reset the profile to `directional`, restore a lowered `detail` | autonomous |
| F4 | a capability has neither a KB shelf match nor a KB-node proposal | search the KB to ground it, or record a propose-kb-node proposal; never leave it ungrounded | autonomous |
| F5 | the scoped-write guard or the keep check report is not ok, or the persist refused an update outside the named ones | the guard's `--restore` already reverted the offending paths; restore any doc that lost a section from HEAD and re-apply only the additions; re-run the keyed persist with only the named updates, after a human confirms the restore | human |
| F6 | the model delta was committed before the checkpoint resolved, or a cancelled checkpoint left writes on the working tree | revert the premature commit and the working-tree writes (guard `--restore`, empty allow set) and re-present the checkpoint; commit only after the human approves | human |
| F7 | the close would report COMPLETED without the Done means held | close HALTED (`stop_condition_unmet`) with the unmet clauses named; fix the state — re-run the keyed persist, re-capture the scoped-write guard report, or make the model-delta commit — and re-evaluate; the close stays HALTED until the verdict reads held | autonomous |
| F8 | a conditional-gate crossing left no live-eval ledger line, or an auto-pass fired for a shape the policy does not list as auto (or that carried a blocking finding) | re-append the missing ledger line for the recorded crossing; when the auto-pass was unearned, re-run the gate as a live wait — render the approval prompt and wait for the typed response — before proceeding | autonomous |
| F9 | the product-os tree is dirty once start-change has cut the branch (uncommitted model edits present) | halt and ask for a clean model tree — commit or revert the pending model edits — before /vision writes the seed | human |
| F10 | the run refused, stopped, waited or closed HALTED over another play's work, or ran the workable check | drop the check or the wait; record what was missing or light as a warning in the persist record and carry on with what is there | autonomous |
| F11 | a capability added twice, a one-sided intent link, or an unplaced capability with no warning | drop the duplicate and record `same_as`; re-run the keyed persist so it writes the missing side of each link; place the capability or record why it could not be placed | autonomous |
| F12 | inside a drive the play opened an issue or branch, ran the end sequence, waited at its checkpoint, or worked off the drive's branch; or by hand it skipped a step | inside a drive, close the stray issue and branch, switch to the drive's branch, and write the review record in place of the wait; by hand, run the skipped step | human |
| F13 | no review record, a record that differs from the checkpoint, no ledger line, an approval no person gave, or an answer the play picked itself | re-render the checkpoint and re-write the review record with `write_drive_review.py`; append the missing `deferred_to_drive_review` line, or a correction refuting a made-up approval; drop the picked answer and ask the person | autonomous |

## Pause and Resume

Steps run top to bottom. On entry, resolve config, derive `product_slug` from the goal
or the in-progress run, check the status marker, skip completed steps, reset any
in-progress step to pending, and continue. A fresh start with no marker runs everything
and creates the marker at Step 1. Resuming a run that already wrote model docs enters a
dirty tree; the clean-tree assertion (F9) is scoped to a FRESH start right after
start-change — a resume continues its own in-progress delta. A resume after Step 7
continues at the first end-sequence member that has not finished.

## Compilation Metadata

| Field | Value |
|-------|-------|
| fingerprint | sha256:658fba576ce177d577c73d078b3269acb584d10df8570f8642cc751ec03d8b8e (of `reference/ice.md`) |
| compiled_by | play-editor (#614 runs inside a drive); play-editor (#637 one product model with /intent); play-editor (#616 position both); play-editor (#500 direct-model-write, ADR 026); prior: play-editor (#467 Batch B, #466 Batch C); play-creator (edited via play-editor, #437; spine+grounding+eval model) |
| pipeline_position | both (start-change head; commit → propose → review → merge close — #616) |
| position_exception | model-writing both play — writes the model on the started branch and commits its own model delta (C9) BEFORE the injected end sequence lands it (same shape as /measure) |
| workflow_structure | A (single checkpoint — class: standard, conditional gate per gate-config.md #467; direct-model-write WRITE-THEN-REVIEW per ADR 026 — persist + guard + classify before the gate, commit after; stop-condition gated close) |
| stop_condition | stop-condition.yaml (D1–D4), gate live at Step C0 |
| domain_agents | 1 (product-os-keeper) |
| utility_agents | 0 (start-change is the injected head, not a domain agent) |
| skills_used | search-kb, propose-kb-node, author-vision-seed |
| scripts | 16 (preflight.py, check_drive_contract.py, write_drive_review.py, read_intents.py, lint_grounding.py, grounding_check.py, grounding_gate.py, persist_seed.py, intent_touches.py, check_kept.py, scoped_write_guard.py, classify_change.py, gate_eval.py, distill_gate_policy.py, check_stop_condition.py, session_stamp.py) |
| step_evals | 14 (SE-1…SE-14) |
| scenario_evals | 7 (SCE-1…SCE-7) |
| recovery_entries | 13 (one per failure condition; 10 autonomous / 3 human) |

**Recompiled note (#467 Batch B):** checkpoint upgraded to a conditional learned gate;
see `gate-config.md`.

**Direct-edit deviation note (drop-codex-judge):** the content-quality judge dispatch
was simplified from three modes (subagent / different-model / codex grader) to a single
isolated sub-agent (with an optional model override). This is an execution-mechanism
change only — it touches no constraint, failure, scenario, or eval. The `run_codex_judge.py`
script was removed. A future rebuild from the ICE need not restore the dropped modes.

**Direct-edit deviation note (#468 Stage 5, concurrent fan-out):** the Step 3
content-quality judge loop was changed from a serial per-doc loop to a concurrent
read-only fan-out — one isolated judge per doc dispatched in one batch, joined before
gating (`standards/rules/concurrent-fanout.md`). Execution-timing change only: each judge
stays isolated and read-only, writes only its own verdict, and the gate still runs over
every verdict, so coverage (SE-2) is unchanged. No constraint, failure, scenario, or eval
touched — the ICE (`reference/ice.md`) and fingerprint stand. play-creator emits the same
fan-out form so a rebuild converges.

**Direct-edit deviation note (#500) — INTENT CHANGE, HAND-COMPILED, CONVERGENCE UNVERIFIED:**
This SKILL was updated to the direct-model-write write-then-review shape (ADR 026) by a
**hand-compile from `reference/ice.md`**, NOT by a `/play-editor` run. This is an intent
change (it alters the write path, the containment guarantee, the checkpoint cancel semantics,
and the step order), so the sanctioned path is recompile-via-`/play-editor`; play-editor is
interactive-only (fully gated, human-checkpoint) and cannot run headless in this environment,
so the compiled output was produced by hand to match what play-editor would emit from the
current `reference/ice.md` (fingerprint above). **The `compiled_by` line names play-editor for
provenance intent, but no play-editor run actually occurred and convergence is UNVERIFIED.**
An interactive `/play-editor` convergence run against `reference/ice.md` is **REQUIRED** —
confirming the emitted SKILL matches this hand-compiled body and refreshing the fingerprint.
This mirrors the same caveat on /understand's #498 migration (the ratified reference
implementation): vision is the fan-out of that pattern, and the fan-out itself remains
convergence-unverified until an interactive play-editor run confirms it.
