---
name: drive-creator
description: >
  Builds a "drive" — a higher-order play that runs other plays in a fixed order until its
  intent is met (ADR 029) — from its ICE. Interviews for the intent triple and the drive's
  own parts (its plays, the questions it asks first, its checker and runner settings, how it
  ends), generates the expectation and the Done means, and writes the compiled drive into
  core/components/drives/<drive>/ (a SKILL.md that points to the Shared Drive Run, its
  stop-condition.yaml and its stamped scripts). Use when the user wants to create, build or
  compile a drive, or to review a drive for gaps — or says "new drive", "drive-creator",
  "build the Kickoff drive", "turn these plays into a drive". To change a drive that exists,
  use drive-editor.
user-invocable: true
model: best
---

# drive-creator

The drive builder for garura. A drive runs other plays, in a fixed order, on one issue and one
branch, asks its questions first, has a checker judge the result, and lands one pull request
(ADR 029). It carries no rules of its own — every rule lives in its plays. So a drive is small:
its own values, and a pointer to the run every drive shares.

`/play-creator` builds plays; this builds drives. Companion: `/drive-editor` changes a drive
that exists. Like `/play-creator`, this skill is written by hand — it is a builder, so nothing
builds it — and it runs its pipeline itself.

## What a built drive is

A folder `core/components/drives/<drive>/`:

- `reference/ice.md` — the drive's ICE (the source; see step 1–2).
- `SKILL.md` — the compiled drive. Frontmatter `kind: drive`, `position: both`. It holds the
  play sections (Compiled From, Role, Pre-flight, Task DAG, Workflow, Scenario Validation,
  Recovery, Pause and Resume, Compilation Metadata), the **Shared Drive Run** anchor pair with
  the drive's values between them, its steps (each owned by the drive, its checker, one of its
  plays, or a change play), and the Standard Play Close anchor pair.
- `stop-condition.yaml` — baked from the ICE's Done means. Required for a drive.
- `scripts/` — the shared run's scripts, stamped unchanged (step 4).

The worked example is [`references/compiled-drive-example/`](references/compiled-drive-example/):
match its shape. The run every drive shares is `core/components/drives/_shared/drive-run.md`
(installed as `../_shared/drive-run.md`); never copy its steps into a drive.

## Structural gate (do this first)

A drive is buildable when:
- it names **at least one play**, and every play exists and runs inside a drive (its SKILL.md
  checks a drive contract — `check_drive_contract.py`). A play that cannot is fixed first,
  through its own ICE and `/play-editor`; the drive does not work around it;
- its intent has at least one constraint and one failure condition, and a Done means can be
  composed;
- it does no work of its own. If a wished-for step is real work (writing a doc, judging a
  design), it belongs in a play: say which play, or that one is missing, and stop.

## Identity & mode

| State | Mode | What happens |
|-------|------|--------------|
| No drive folder | **new** | Interview → build |
| ICE exists, no SKILL.md | **new** | Skip the interview; build from the ICE |
| Both exist, user wants a check | **review** | Report gaps only — change nothing |

To change a drive that exists, use `/drive-editor`.

## Pipeline (new)

Run in order. Interactive by default: interview and ask for approval by typed reply (never
`AskUserQuestion`). With no person reachable, state each assumption and record that approval
was assumed.

### 1 — Intent and the drive's parts
Write `reference/ice.md` like the example's:
- **Intent** — the goal (one line: what the drive turns into what), constraints C-n and failure
  conditions F-n, implementation-agnostic. Write it as `/play-creator` step 1 says
  (`../play-creator/SKILL.md`). A drive's constraints are about the run: one issue and one
  branch, questions first, order and done checks, the checker.
- **Plays** — a table: order, play, what it gets from the contract (`inputs.<play>`) and which
  answers it gets (`answers.<play>`). An input another play makes is written "after `<play>`:
  …" — the drive adds it to the contract before the later play starts (shared run, R5 step 6).
  Check each play exists and runs inside a drive, and that it reads every input the drive hands
  it: `<key>` of `inputs.<play>.<key>` appears in the play's SKILL.md. A key the play does not
  read is not handed — drop it, or change the play first.
- **Questions first** — each question the drive asks before any play runs, and the
  `answers.<play>.<key>` it fills; or `none`. A question a play would otherwise ask mid-run
  belongs here when the drive can know it up front (ADR 029 §2).
- **Checker** — `drives.<drive>.checker`: `kind` (`subagent` on a named model that is not the
  session's, or `coding-agent` — Codex) and `model`. It judges the drive's goal, constraints and
  Done means against the drive's outputs only, with the `judge-drive-result` skill.
- **Runner** — `drives.<drive>.runner`: `subagent` (default) or `headless`.
- **End** — the injected end sequence, plus any step the drive adds before the review (for
  example Kickoff's typed confirmation of intents, until the review tool exists).
Present it and get approval.

### 2 — Expectation (generate, then confirm)
Generate the success scenarios (S-n, per persona, given/then/measure), exactly one recovery per
failure condition, and the **Done means** (D-n, 2–6 clauses from the closed set
`artifact_exists` | `field_equals` | `gate_outcomes_pass`) — as `/play-creator` step 2 says.
A drive's Done means reads its own run folder (`{stm_base}<issue>/context/<drive>/<run-ts>/`):
the contract, every play's `<play>-done.json` (`done` = `true`, one clause per play), the
checker's `check.yaml`. Present for a quick
approve or revise.

### 3 — Steps and evals
A drive's steps are fixed: open (`start-change`) → questions first (drive) → write the contract
(drive, script) → **in rounds**: one step per play (owned by that play), then "after the round:
done, again or ask" (drive, script — `round_state.py`) and "ask the person what the drive could
not answer" (drive, only on ask — after the member play `build-memory` builds the missing
memory, R5c) → the checker → the end sequence → scenario validation →
close. A drive loops over its plays until its job is done; a play's open question is the
drive's, asked only when no play answers it (Shared Drive Run, R5 and R5b). Add only what the End section names. Then generate the evals as
`/play-creator` step 5 says: a step eval (SE-n) per failure condition and per
artifact-verifiable constraint, placed after the step it checks; a scenario eval (SCE-n) per
scenario. Every eval reads a file the shared run writes (`answers.json`,
`answers-sources.json`, `contract.json`, `<play>-done.json`, `<play>-commit.json`,
`check.yaml`).

### 4 — Build the drive
Write the folder:
1. `SKILL.md`, matching the example: frontmatter (`name`, `description`, `user-invocable:
   true`, `kind: drive`, `position: both`); the Workflow opens with the Shared Drive Run block —
   the opener anchor, then exactly these lines, then the closer anchor:

   ```
   drive=<drive>
   plays=<play>,<play>,…
   questions=<key> -> answers.<play>.<key>; …   (or: none)
   runner_key=drives.<drive>.runner
   checker_key=drives.<drive>.checker
   end=<the end, in one line>
   ```

   The anchors' exact text is under "Enforced" in `drive-run.md`. The close is the Standard
   Play Close pointer, as `/play-creator` step 6 says. It reads `../_shared/play-close.md`: that
   path holds once installed (the install lays both shared folders as one); in the source the
   file is `core/components/plays/_shared/play-close.md`, and the linters look there.
2. `stop-condition.yaml` from the Done means (`{name: stop-condition}`, `content.done`).
3. `scripts/`: copy unchanged — from `references/`: `drive_preflight.py`,
   `write_drive_contract.py`, `check_play_done.py`, `commit_run_files.py`,
   `run_play_headless.py`, `round_state.py`, `drive_status.py`, `prepare_check.py`, `run_checker_codex.py`,
   `record_check.py`; from `../play-creator/references/`: `check_drive_contract.py`,
   `session_stamp.py`, `check_stop_condition.py`. A rebuild copies them again, so a drive never
   drifts from the shared run.
4. The fingerprint: run `shasum -a 256 reference/ice.md` and paste the digest. Never invent one.
5. The Next line: add the drive to `standards/rules/pipeline-next.md`.
6. The config, in `core/config.yaml`: under a top-level `drives:` block (the commented template
   there shows it), add

   ```yaml
   drives:
     <drive>:
       runner: subagent            # subagent | headless
       checker:
         kind: subagent            # subagent | coding-agent
         model: sonnet             # required for subagent: not the session's model
   ```

   and under `evidence:` → `plays:`, `<drive>: true` — a drive always records its evidence
   (ADR 029).

### 5 — Verify (run the linter)

From the repository root:

```
python3 core/components/plays/drive-creator/scripts/lint_drive.py core/components/drives/<drive>/SKILL.md
```

It runs every play check (coverage, one recovery per failure, no orphans, required sections,
the close, the stop condition, the fingerprint, the Next line) and the drive's own: `kind`,
`position: both`, the run anchors and the shared file, the values (with `end=`) and their
config keys, every play exists and runs inside a drive, every step's owner, the Done means, the
stamped scripts unchanged from their source, the fingerprint matching `reference/ice.md`, the
config entries (runner, checker kind, evidence on), one step and one done clause per play, and
every handed input read by its play. Fix every GAP and run it again until it passes. Then run
`node core/tools/lint-components/index.js --target core/components --output json` and clear any
error whose file is the drive's. That command exits 1 while other components carry old errors;
that is not this drive's gap. The linter checks that an eval exists, not that it means something: check that
yourself.

## Review mode (read-only)

Run the linter as step 5 says, then add the checks a script cannot make: each play
still does what the drive's Plays table says; the questions really cover what the plays ask;
the fingerprint still matches `reference/ice.md` (`shasum -a 256`); the evals are meaningful.
Report a short PASS/GAP table and stop. To fix gaps, use `/drive-editor`.

## Hard rules

- A drive does no work of its own. Every step is owned by the drive (asking, the contract),
  its checker, one of its plays, or a change play. Real work goes into a play.
- Never copy the shared run's steps or the shared close into a drive; point to them.
- Every play a drive names must run inside a drive. Fix the play, not the drive.
- A drive always has a Done means, baked into `stop-condition.yaml`.
- Stamp the shared scripts unchanged; never edit a stamped copy.
- Run `lint_drive.py` and clear every gap before calling the drive built.
- In review mode, change nothing.
