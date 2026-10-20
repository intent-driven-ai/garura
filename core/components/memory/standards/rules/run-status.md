# Run status — what a long run is doing now

A drive can run for an hour. The person needs to see what it is doing without asking. That is
two separate jobs, kept apart (ADR 041 §6):

- **The run presents a status.** It writes one small file and keeps it current. It never shows
  anything itself and does not know who reads the file — it works the same in Claude Code, in
  Codex, or headless.
- **A display shows it.** Something else — for Claude Code, a plugin installed only when the
  install chooses Claude Code — reads the file and shows a line about once a minute. It needs
  nothing from the run except the file.

## The file

`{stm_base}<issue>/status/run-<name>.json` — `<name>` is the drive's name (later, a play's).
The `status/` folder is machine-local and never committed (ADR 021), which is right for a live
status. It also holds the plays' resume and session markers (ADR 021); the run status is the one
file named `run-<name>.json`, written only by `drive_status.py`, and a display reads only it.

```json
{
  "kind": "drive",
  "name": "kickoff",
  "issue": 7,
  "run_id": "kickoff-20261020-145613",
  "state": "running",
  "round": 1,
  "play": "understand",
  "step": "detailing the capabilities",
  "started_at": "2026-10-20T14:56:13Z",
  "updated_at": "2026-10-20T15:34:02Z",
  "note": "6 intents proposed; vision seeded the collaboration domain"
}
```

| Field | Meaning |
|-------|---------|
| `kind` | `drive` (or `play`, later) |
| `name`, `issue`, `run_id` | Which run this is |
| `state` | `running` · `asking` (waiting on the person) · `checking` (the checker) · `landing` (the end sequence) · `done` · `halted` |
| `round` | The drive's round, from 1 |
| `play`, `step` | What runs now, in plain words |
| `started_at`, `updated_at` | UTC; a display shows the time so far, and can tell a stale file from a live one |
| `note` | One plain line on what the run has made so far (optional) |

## Rules

- The run writes the file through `drive_status.py` (canonical in
  `drive-creator/references/`), which replaces it whole, so a reader never sees half a file.
- The run updates it at every step of the Shared Drive Run and when each play starts and ends.
  No timer is needed: a display that refreshes every minute shows the latest step.
- The file holds no secret, no file content and no person's answers — only what the run is
  doing.
- A display reads; it never writes the file and never controls the run.

## Related

- `core/components/drives/_shared/drive-run.md` — where a drive updates it.
- ADR 021 — status markers are machine-local.
