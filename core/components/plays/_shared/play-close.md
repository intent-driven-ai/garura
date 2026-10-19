# Standard Play Close

The close every play runs as its final step. It writes the machine-readable evidence file and
the user-facing delivery report from templates — never hand-authored prose.

This is a **shared block** (ADR 039 §9): it lives once, here, beside the plays
(`core/components/plays/_shared/play-close.md`; the install lays it as
`_shared/play-close.md` next to the installed plays). A play does not carry this text. Its
close section holds only the two anchor lines, its own values (where its evidence goes, its
session stamp marker, its stop-condition paths) and any close step of its own, and points
here. `/play-creator` emits exactly that, so a direct edit and a rebuild converge.

## Why this is a non-intent change

The close changes nothing a play *decides* or *guarantees* — no constraint, failure
condition, scenario, eval, agent, or skill. It only standardizes how a completed run is
reported. Per the play-pipeline boundary rule it is a direct edit, not an ICE → rebuild cycle.

## A play reads no memory here either

The templates the close fills are memory. The play does not read them: it asks the
`template-manager` agent (ADR 039 §8), which finds each one through the memory tool and puts a
copy in the run's short-term memory. The close then reads the copies.

## The steps

Run these in order, with the values the play's close section sets.

### Step L — Load the templates

Dispatch `template-manager`:

    { "task":    "load these templates into the issue's short-term memory",
      "inputs":  { "issue": <issue, or null for a run with no issue>,
                   "templates": ["standards/templates/evidence-file.md",
                                 "standards/templates/delivery-report.md",
                                 "standards/rules/pipeline-next.md"] },
      "outputs": { "out_dir": "<the run's short-term folder>/context/templates/",
                   "manifest": "<the run's short-term folder>/context/templates/manifest.json" },
      "task_id": "load-templates" }

The run's short-term folder is `${stm_base}${issue}/` for a run with an issue, else the
play's own working base under `${stm_base}` (for example `${stm_base}_realize/<play>/`). A
second close in the same issue finds the copies already there.

```bash
templates="<the run's short-term folder>/context/templates/"
evidence_template=$(cat "${templates}standards/templates/evidence-file.md")
delivery_template=$(cat "${templates}standards/templates/delivery-report.md")
next_map="${templates}standards/rules/pipeline-next.md"
ts=$(date -u +%Y%m%d-%H%M%S)
evidence_dest="${evidence_base}${ts}.md"
mkdir -p "$(dirname "$evidence_dest")"
```

`template-manager` returning `failed` with `template_missing` does not block the close: write
the evidence and the report in the template's known shape, and name the missing template in
the report.

### Step S — The play's own close lines

Run the lines the play's close section carries, in its order: the session identity stamp's
close phase (`scripts/session_stamp.py --phase close` with the play's marker), the
stop-condition check (`scripts/check_stop_condition.py` with the play's manifest, base and
out), and any step of the play's own (for example the conditional-gate policy refresh,
`scripts/distill_gate_policy.py`).

### Step C0 — Bind the verdict

When the play carries a baked `stop-condition.yaml`, `sc_exit == 0` (held) permits
`status: COMPLETED`. Anything else closes `HALTED` with `exit_reason: stop_condition_unmet`,
and the evidence's Stop Condition section names every unmet clause. An unevaluable verdict
(exit 2) is never a pass. A play with no manifest is legacy: it stamps
`stop_condition: not_defined` and closes as before, until its recompile bakes one.

### Step C1 — Write the evidence file

Gated by `evidence.record` (see below). When it resolves false, skip the write, record
`evidence skipped (record=false)` in the report's pointer line, and still do C2. Otherwise
fill the `evidence-file.md` slots and write the result to `$evidence_dest`. Do NOT
hand-author the body — fill slots:

- frontmatter: `play: <play>`, run_id `<play>-${ts}`, issue or product slug, started_at /
  completed_at, status (`COMPLETED` | `HALTED` | `ABORTED`), exit_reason, and the session
  identity stamp fields from `$session_stamp` (#463): `session_id`, `ledger_file`,
  `ledger_start_offset`, `ledger_end_offset` (null when the ledger could not be resolved; the
  close never blocks on it). Plus the stop-condition verdict (#464):
  `stop_condition: held | unmet | not_defined`.
- Artifacts Produced: every artifact this run wrote (from `$evidence_base`, the play's output
  paths, and any commit SHAs), and the play's own artifact list where its close names one.
- Step Eval Results / Scenario Eval Results: every eval the play defines; `PASS`/`FAIL`, or
  `N/A` for a path not exercised. A play with no evals writes `none defined`.
- Checkpoint Decisions: one row per checkpoint cycle, including a gate skipped by config;
  `none` if the play has no gates.
- Commit Reference: self-commit SHA(s), or `N/A — commit failed` / `N/A — no commit step`.

### Step C2 — Render the delivery report

Fill the `delivery-report.md` slots and **output the filled report to the user**. Do NOT
hand-author prose:

- `## <Play-Name> Delivered — <slug or context>`
- Run Summary table: Play, Issue/Slug, Status, Started, Completed.
- Pipeline Steps table: built from the task DAG (mapping below).
- Artifacts Produced table: the named artifacts and SHAs from C1.
- **Next** (always, unless the play is `meta_exempt`): resolve this play in the Next-line map
  (`$next_map`, from `template-manager`) and render
  `**Next:** /<command> — <why>. Or run /next to see all recommended actions.` When the
  play's mapped `command` is `null`, render only the `/next` pointer, or omit the line.
- Next Steps (optional): other real follow-ons, and any the play's close names.
- End with a pointer to the evidence file at `$evidence_dest`.

## Pipeline Steps source — the generic mechanism

The Pipeline Steps table is derived from the play's **task DAG**, which every play builds at
start:

| Task DAG state | Pipeline Steps row |
|----------------|--------------------|
| task `completed` | status `PASS`, description = task subject (T-id stripped) |
| task `completed` + skipped note | status `SKIP`, reason from the skip note |
| task not reached / play halted before it | status `SKIP` (halted) |
| task failed / play aborted at it | status `FAIL`, detail = failure reason |

The "Key Output" column is best-effort, filled from run context; leave it `—` when there is
nothing reliable. The Artifacts Produced table carries the authoritative artifact list.

## Cross-cutting rules (not optional)

**`evidence.record` gate.** Resolve the flag at pre-flight, first match wins:
(1) `evidence.plays.<play>`; (2) else `evidence.record`; (3) else `true`. C1 honors it; C2 is
always emitted — it is the user's surface, not audit evidence. Policy (plays only, never
agents or skills) lives in `standards/rules/evidence-recording.md`.

**Stop-condition gate (#464).** A play ends because "done" was proven, not because its step
list ran out. `scripts/check_stop_condition.py` (canonical copy:
`play-creator/references/check_stop_condition.py`) evaluates the baked manifest as pure disk
assertions. Held permits COMPLETED; unmet or error closes HALTED.

**Session identity stamp (#463).** `scripts/session_stamp.py` (canonical copy:
`play-creator/references/session_stamp.py`) binds the run to its session ledger: the start
phase runs at pre-flight, the close phase reads the marker. Soft-fail: an unresolved ledger
gives null fields, never a blocked close.

**`started_at` source (never fabricate).** In order: (1) the timestamp the play recorded at
its own pre-flight; (2) else the earliest checkpoint or evidence timestamp of this run;
(3) else the first task's move to `in_progress`. If none is known, write
`started_at: unknown`.

## Sub-plays

A parent's JSON contract to a sub-play always carries `parent_run_id`. **Present ⇒ running as
a sub-play ⇒ skip C2** (emit C1 and a compact result for the parent). **Absent ⇒ run by the
user ⇒ do both C1 and C2.**

## Non-blocking

Both C1 and C2 are non-blocking. If the evidence write or an optional commit fails, the run
still closes; the failure is recorded in the evidence file's Recovery Attempts section.

## Enforced

`lint-components` checks every compiled play's SKILL.md for the close's two anchor lines,
each exactly once, opener before closer, and that the shared file exists:

- opener: `# --- Standard Play Close (shared; see ../_shared/play-close.md) ---`
- closer: `# --- end Standard Play Close ---`

A play's close section keeps only its own values and steps between them. A rebuild that drops
the anchors, or drift that alters them, fails lint.

## Related

- `standards/templates/delivery-report.md` — the report's shape (C2), from `template-manager`
- `standards/templates/evidence-file.md` — the evidence file's shape (C1), from `template-manager`
- `standards/rules/pipeline-next.md` — the Next-line map, from `template-manager`
- `standards/rules/evidence-recording.md` — who may record evidence
