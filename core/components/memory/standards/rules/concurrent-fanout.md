# Concurrent Read-Only Fan-Out

Plays run their steps top to bottom, one at a time (ADR 025 — the skeleton is
deterministic). This rule names the **one** exception: a single step may run several
independent sub-tasks **at once** instead of in a serial loop, then join before the next
step reads their outputs. Same work, same guarantees, less wall-clock. It has two kinds:
the **read-only fan-out** (epic #460 Stage 5, #468), and the **scoped-write fan-out**
(#615), where each sub-task writes the model only inside its own folder. Parallel
code-building, where sub-tasks may touch the same files and need worktree isolation, is
#488 and is NOT covered here.

## When a fan-out is allowed — the three safety conditions

A batch of sub-tasks (sub-agent dispatches OR runner subprocesses inside one script) may
run concurrently **only when all three hold**:

1. **Read-only over shared inputs.** Each sub-task only *reads* the shared context (the
   model, the draft, the code) — it makes no mutation and no write to the shared working
   tree. (A run whose sub-tasks WRITE the tree needs isolation — that is #488, not this.)
2. **Distinct output paths.** Each sub-task writes only to its *own* output path — no two
   write the same file. Collisions are impossible, so no lock and no isolation are needed.
3. **No sibling dependency.** No sub-task consumes another's output. They are siblings of
   one parent step, not a chain. If one needs another's result, they are sequential — not
   a fan-out.

If any condition fails, the step stays serial — unless the scoped-write conditions below
all hold. The conditions are a checklist the step declares, not a judgment call.

## The scoped-write fan-out (#615)

Some steps write the live model once per node — for example, `/discover-capabilities` details each of
its target capabilities by writing that capability's own docs. Under direct-model-write
(ADR 026) those writes go straight into the tree, so condition 1 fails. Such a step may
still run its sub-tasks at once **only when all five hold**:

1. **Own write scope, declared before dispatch.** Each sub-task is handed one write scope —
   the folder of the one node it owns (e.g. `product-os/<domain>/<capability>/`) — and
   writes the model nowhere else. The scopes are fixed before any dispatch and checked by a
   script to be distinct: no two scopes are the same folder, and none sits inside another.
2. **No shared file.** No sub-task writes a file that holds more than its own node (the
   spine `_spine.yaml`, the profile, decisions, any index). Each sub-task puts its
   shared-file changes in its own output record, and ONE keyed persist writes them after
   the join (ADR 026 write discipline).
3. **Distinct output paths.** Each sub-task's own records (manifest, routing) go to its own
   path, as in the read-only fan-out.
4. **No sibling dependency.** No sub-task reads another's output.
5. **Guarded after the join, committed only after review.** The model tree is clean at the
   start of the run; after the join and the keyed persist, the scoped write guard
   (`scoped_write_guard.py`) checks the whole delta against the union of the declared
   scopes plus the persist's shared files, and nothing is committed before the step's
   checks and checkpoint pass. No sub-task runs git.

What the guard cannot see: a sub-task that strays into a SIBLING's scope stays inside the
union. Condition 1 keeps that rare (each sub-task is told its one scope), and every node's
content is still checked downstream (the linter, the content judges, the checkpoint) — so a
stray write is caught as a bad doc, not silently kept.

The same bounded join applies: a fixed set of sub-tasks, a barrier before any later step
reads the model, and the outputs collected in input order.

## The bounded join

A fan-out is always **bounded and joined**, never open-ended:

- **Bounded** — the batch is a fixed set known when the step starts (every doc in the
  draft, every check in the manifest). No sub-task spawns more sub-tasks.
- **Joined** — the step waits for **every** sub-task to finish before anything downstream
  reads their outputs. No later step ever sees a partial set.
- **Order-stable result** — outputs are collected in a deterministic order (the batch's
  input order), so the step's result is identical whether the sub-tasks ran concurrently
  or in series. Concurrency changes only timing, never the outcome.

This is what keeps the skeleton deterministic: the fan-out is a closed set with a barrier
at its end, so the step is a single deterministic node from the outside.

## The two forms

- **Sub-agent-dispatch form** — the play's orchestrator dispatches N independent
  read-only sub-agents in one concurrent batch (one message, N dispatches), waits for all,
  then proceeds. Example: the content-quality judge loop in `/discover-domains` and `/discover-capabilities` —
  one isolated judge per grounding doc, each reading only its own doc and writing only its
  own verdict.
- **Script-internal form** — one orchestrating script runs its independent subprocesses
  concurrently (a bounded worker pool), then collects results in input order. Example:
  `/validate-epic`'s `run_checks.py` — each check runs its own runner, writes its own result
  record, reads only the code.

Both forms obey the same three conditions and the same bounded join.

## Declaring it in a play

A step that fans out states, in one line, that it does and that the conditions hold — e.g.
"dispatch one judge per doc as a concurrent batch (concurrent read-only fan-out: each
reads only its doc, writes only its verdict, no judge depends on another — join before
gating; see `standards/rules/concurrent-fanout.md`)." A scoped-write fan-out says so by
name and declares each sub-task's **write scope**, that no sub-task writes a **shared
file**, and the **join** — e.g. "dispatch one agent per capability as a concurrent batch
(scoped-write fan-out: each writes only inside its own write scope, no shared file, no
sibling dependency — join before the keyed persist)." `lint_play.py`
(`check_fanout_declaration`) requires these declarations so the safety conditions are
always visible, never implicit.

## Related

- ADR 025 — the determinism rule; a bounded, joined fan-out is a single deterministic step
- `create-play/references/workflow-structures.md` — step execution model
- ADR 026 / `direct-model-write.md` — the write discipline the scoped-write fan-out keeps
  (per-node docs by the sub-tasks, shared files by one keyed persist, one guard)
- #488 — parallel code-building (build pieces that may share files, worktree isolation)
