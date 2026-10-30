---
name: track-plan-changes
description: Read the issues of a plan, and make the tracker writes of an /update-plan session the person approved — close (as completed or as not planned), reopen, a new title, a new text, a new type, a new parent, a new issue with its type and parent — one by one through the platform adapter's verbs, recording each write at once, so a run that stops part way is picked up again and never makes an issue twice. It writes nothing unless the approval reads "approved" for the very list the person saw (the list's sha256). It is mechanical — what to change was decided in the session; this skill decides nothing. Used through project-orchestrator by /update-plan (#730).
user-invocable: false
model: sonnet
allowed-tools: Read, Bash
---

# track-plan-changes

An `/update-plan` session ends with one list the person approved. This skill makes that list's
tracker writes. It also reads the plan's issues, so the session works from what the tracker holds
now. It has no judgment in it: the session worked out each write, and the person approved them.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `mode` | yes | `read` or `apply` |
| `issues` | for `read` | The issue numbers to read, comma separated |
| `ops` | for `apply` | `github-ops.json`, which the play's script wrote from the approved list — see the script's header for each op |
| `changes` | for `apply` | The approved list (`changes.yaml`) |
| `approval` | for `apply` | `answer.json`: `decision` and `list_sha` |
| `read`, `before`, `after` | for `apply` | The plan's issue numbers, and where to write the snapshots read before and after the writes |
| `tracker_file` | no | A JSON file that stands in for the tracker (tests and the test run); without it, the code host |
| `out` | yes | Where to write `snapshot.json` (read) or `github-record.json` (apply) |

## Process

1. **Read.** Run:

   ```bash
   python3 scripts/track_changes.py read --issues <numbers> [--tracker-file <json>] --out <snapshot.json>
   ```

   Each issue's title, type, labels, state and close reason, text, parent and sub-issues. An
   issue the tracker does not have is listed under `missing`.
2. **Apply.** Run:

   ```bash
   python3 scripts/track_changes.py apply --ops <github-ops.json> --changes <changes.yaml> \
       --approval <approval.json> [--tracker-file <json>] \
       --read <the plan's issue numbers> --before <snapshot-before.json> --after <snapshot-after.json> \
       --out <github-record.json>
   ```

   With `--read`, it reads those issues just before its first write and again after its last
   (with the issues it made), so the play can check that nothing else changed.

   Exit 0: every write is made, or was already true. Exit 1: a write failed; the record names
   it and keeps every write made before it — run the same command again once the cause is
   fixed, and it goes on from there. Exit 2: refused, nothing written (not approved, or the list
   changed after the approval).
3. Return the output path and the exit code. Never make a write the ops file does not name, and
   never write to the tracker any other way.

## Output

`snapshot.json` — `{"issues": {"<number>": {number, title, type, labels, state, state_reason,
body, parent, sub_issues}}, "missing": [..]}`.

`github-record.json` — `{"ok", "done": {"<op id>": {op, issue, result, how}}, "failed"}`; `result`
is the number of an issue the op made; `how` is `done`, `made` or `already`.

## Rules

- Only the list the person approved, and only through the platform adapter's verbs.
- Each write is recorded as soon as it is made; a run again never repeats one.
- No labels are added, and nothing is deleted.
