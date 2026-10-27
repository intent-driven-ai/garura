# Checkpoint Artifact Format

Canonical format for checkpoint files written by plays at each human-approval gate. Every checkpoint-gated play writes one of these per gate.

Consumers: `specify`, `design`, `arch`, every checkpoint-gated play.

## File path convention

```
{product_base}/_checkpoints/{play-name}/{stage-slug}-{YYYYMMDD-HHMMSS}.md
```

For project-scoped plays:

```
{stm_base}/{issue}/checkpoint/{play-name}/{YYYYMMDD-HHMMSS}.md
```

The filename MUST include a timestamp so multiple cycles of the same checkpoint (a new round after a change was asked for) produce separate artifacts — they do NOT overwrite.

## Shape

```markdown
---
play: {play-name}
stage: {stage-slug}
cycle: {1 | 2 | 3 | ...}
created_at: {ISO-8601 timestamp}
status: PENDING_APPROVAL | APPROVED | REJECTED | CHANGE_REQUESTED | COMPLETED
decision: null | yes | change | stop
decided_at: null | {ISO-8601 timestamp}
---

# {Stage Title} — {product or issue slug}

## Context
{3-6 lines describing what this stage produced and why the user needs to review it.}

## Artifacts Under Review
| Artifact | Path | Size |
|----------|------|------|
| {name} | {workspace-relative path} | {bytes or lines} |
| ... | ... | ... |

## Summary
{Quantified summary block — counts, names, coverage percentages. Whatever
helps the user decide yes, change or stop. Never paste artifact content
verbatim; link to the file.}

## Evaluator Output
{Optional. When the stage had a validator pass, include the validator's
status line and any warnings. Blockers are reported here before the user
sees the prompt. Example:
- `validate-intent-epics`: status `passed`, 0 violations, 0 warnings
}

## User Feedback (populated on a change reply)
{Empty until a `change:` reply is read. When populated, contains the
user's typed feedback text verbatim so the re-run step can ingest it as
additional context.}

## Decision Audit
| Field | Value |
|-------|-------|
| Decision | {null until user responds; then yes / change / stop} |
| Decided at | {timestamp} |
| Next action | {Proceed / Cycle back to step {N} / Halt and cleanup} |
```

## Lifecycle

1. **Before the prompt** — Play writes the checkpoint file with `status: PENDING_APPROVAL`. Decision fields are null.
2. **Play emits the approval prompt** — using `templates/approval-prompt.md`. The prompt cites the checkpoint file path.
3. **User responds** — Play reads the plain typed reply (yes / change / stop), as `approval-prompt.md` says.
4. **Play updates the checkpoint**:
   - yes: `status: APPROVED`, `decision: yes`, `decided_at: {now}`, proceed.
   - change: `status: CHANGE_REQUESTED`, `decision: change`, `User Feedback` section populated, re-dispatch producing step(s).
   - stop: `status: REJECTED`, `decision: stop`, `decided_at: {now}`, clean up as the play's intent says, halt.
5. **Play close** — When the full play completes, update `status: COMPLETED` on every checkpoint that belongs to the completed run.

## Retention

Checkpoint files are NOT ephemeral. They are committed as STM evidence (via the play's self-commit step) and retained as the audit trail for every gate decision. The play's evidence section references every checkpoint file written during the run.

## Field rules

| Field | Rule |
|-------|------|
| `play` | Exact play slug (e.g. `specify`, `design`, `arch`). |
| `stage` | Stage slug within the play. Multiple gates per play produce different stage values. |
| `cycle` | 1 for the first attempt at this gate; 2+ for each new round after a change was asked for. |
| `status` | Exactly one of the 5 allowed values. Linear progression PENDING → (APPROVED \| REJECTED \| CHANGE_REQUESTED). COMPLETED is set at play close. |
| `decision` | null while `PENDING_APPROVAL`; then one of yes / change / stop. |

## Related

- `approval-prompt.md` — the prompt text presented to the user (cites this checkpoint's path)
- `evidence-file.md` — the final evidence file written at play close (references every checkpoint)
