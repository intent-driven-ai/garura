# #613 item 5 — building drives: `/drive-creator` and `/drive-editor`

Kapil, 2026-10-20: "we need to build it like /drive-creator and /drive-editor". A drive gets its
own builder and its own editor, as a play has `/play-creator` and `/play-editor`. This note says
what they build and how a built drive is checked. It rests on ADR 029 (a drive is a
higher-order play: it runs other plays and carries no rules of its own), the drive contract
(`standards/rules/drive-contract.md`) and the runner design (`runner-design.md`).

## 1. The two plays

- **`/drive-creator`** builds a new drive from its ICE: it asks for the intent, generates the
  expectation, and writes the compiled drive. Like `/play-creator`, it also has a read-only
  review mode that reports a drive's gaps.
- **`/drive-editor`** changes an existing drive by editing its ICE and recompiling, never by
  patching the compiled drive.

Both are written by hand, like `/play-creator` and `/play-editor`: they are the builders, so
nothing builds them. Each carries a `scripts/lint_drive.py` copy, as the play builders carry
`lint_play.py`.

## 2. A drive's ICE (`reference/ice.md`)

The same ICE as a play — intent (goal, constraints C, failure conditions F), context,
expectation (scenarios S, one recovery per failure, Done means D) — plus the parts only a drive
has:

| Part | What it says |
|------|--------------|
| Plays | The plays, in order, and what each gets from the contract (`inputs`, `answers`). A play listed must run inside a drive (it checks a drive contract). |
| Questions first | What the drive asks the person before any play runs, and which play's `answers` each fills. |
| Checker | The config key that picks the checker (`drives.<drive>.checker`) and what it checks — the drive's Done means. |
| Runner | The config key that picks how plays run (`drives.<drive>.runner`: `subagent` default, `headless`). |
| End | How the drive ends. Until the review tool exists: the pull request, then typed confirmation (runner design, (b)). |

## 3. A compiled drive

A folder like a play's: `SKILL.md` (frontmatter `kind: drive`, `position: both`),
`stop-condition.yaml`, `scripts/`, `reference/ice.md`. The `SKILL.md` has a play's sections
(header, Compiled From, Role, Pre-flight, Task DAG, Workflow, Scenario Validation, Recovery,
Pause and Resume, Compilation Metadata). Its workflow has only the drive's own values; the run
itself is shared.

**The shared drive run** — `_shared/drive-run.md`, beside `_shared/play-close.md`. Every drive
runs the same steps (runner design, section 3): pre-flight → open the change → questions first →
write the contract → each play in order (run it with the configured runner, check its done
check, commit its run files) → the checker → evidence → end. Like the shared close, a drive
holds an anchor pair, its own values (its plays, its questions, its checker key) and points to
the shared file. Every later drive (#608–#611) uses the same run, so it is written once.

**Shared scripts** — canonical copies in `drive-creator/references/`, copied into each drive's
`scripts/`, as `/play-creator` does for plays:
- `write_drive_contract.py` — writes the one contract from the answers and the plays' inputs, and
  checks it with `check_drive_contract.py`.
- `commit_run_files.py` — commits the issue's run files after each play (V-4), on the drive's
  branch only.
- `check_play_done.py` — reads a play's stop-condition result; a play that is not held halts the
  drive.
- the checker's script comes in item 6.

## 4. The drive linter (`lint_drive.py`)

Everything `lint_play.py` checks (each C, F and S covered, one recovery per failure, no orphans,
required sections, a real fingerprint), plus:
- every play the drive names exists and accepts a drive contract;
- the plays run in a fixed order, and the drive has no step of its own that does a play's work
  (ADR 029 §2);
- the drive-run anchors are there, once each, and the shared file exists;
- the questions-first list is present (it may say "none");
- the checker and runner config keys are named;
- a Done means is present and baked into `stop-condition.yaml`.

`lint-components` learns `kind: drive`, so it checks drives with the drive rules, not the play
rules.

## 5. Done when (item 5)

- `/drive-creator` builds a small sample drive (two existing plays) that passes `lint_drive.py`.
- The linter fails a broken drive: a missing play, a missing anchor, a step that does work itself.
- `/drive-editor` changes the sample drive's ICE, and the recompiled drive passes the linter.
- Kickoff itself is built with `/drive-creator` in item 7.

## 6. Open — for Kapil

Where drives live in the source:
1. `core/components/drives/<drive>/` — a folder of their own. Clear to read; the install and
   `lint-components` must learn a new folder.
2. `core/components/plays/<drive>/` with `kind: drive` — ADR 029 calls a drive a higher-order
   play; the install, the shared files and `lint-components` work as they are.

## Log

- 2026-10-20 — Written after Kapil's "go" on item 5, with `/drive-creator` and `/drive-editor`.
