---
name: create-loop
description: >
  Builds a "loop" — a higher-order play that runs other plays in rounds, in any order, until
  its intent is met (ADR 029, ADR 043) — from its ICE. Interviews for the intent triple and the loop's
  own parts (its plays, the questions it asks first, its checker and runner settings, how it
  ends), generates the expectation and the Done means, and writes the compiled loop into
  core/components/loops/<loop>/ (a SKILL.md that points to the Shared Loop Run, its
  stop-condition.yaml and its stamped scripts). Use when the user wants to create, build or
  compile a loop, or to review a loop for gaps — or says "new loop", "create-loop",
  "build the Discovery loop", "turn these plays into a loop". To change a loop that exists,
  use edit-loop.
user-invocable: true
model: best
---

# create-loop

The loop builder for garura. A loop runs other plays in rounds, in any order, on one issue and
one branch (ADR 043: no play takes another's output, and the loop closes the gaps between
them after each round), asks its questions first, has a checker judge the result, and lands one pull request
(ADR 029). It carries no product rules of its own — every rule lives in its plays; the run
steps between plays live in the Shared Loop Run (ADR 044). So a loop is small:
its own values, and a pointer to the run every loop shares.

`/create-play` builds plays; this builds loops. Companion: `/edit-loop` changes a loop
that exists. Like `/create-play`, this skill is written by hand — it is a builder, so nothing
builds it — and it runs its pipeline itself.

## What a built loop is

A folder `core/components/loops/<loop>/`:

- `reference/ice.md` — the loop's ICE (the source; see step 1–2).
- `SKILL.md` — the compiled loop. Frontmatter `kind: loop`, `position: both`. It holds the
  play sections (Compiled From, Role, Pre-flight, Task DAG, Workflow, Scenario Validation,
  Recovery, Pause and Resume, Compilation Metadata), the **Shared Loop Run** anchor pair with
  the loop's values between them, its steps (each owned by the loop, its checker, one of its
  plays, or a change play), and the Standard Play Close anchor pair.
- `stop-condition.yaml` — baked from the ICE's Done means. Required for a loop.
- `scripts/` — the shared run's scripts, stamped unchanged (step 4).

The worked example is [`references/compiled-loop-example/`](references/compiled-loop-example/):
match its shape. The run every loop shares is `core/components/loops/_shared/loop-run.md`
(installed as `../_shared/loop-run.md`); never copy its steps into a loop.

## Structural gate (do this first)

A loop is buildable when:
- it names **at least one play**, and every play exists and runs inside a loop (its SKILL.md
  checks a loop contract — `check_loop_contract.py`). A play that cannot is fixed first,
  through its own ICE and `/edit-play`; the loop does not work around it;
- its intent has at least one constraint and one failure condition, and a Done means can be
  composed;
- it does no work of its own. If a wished-for step is real work (writing a doc, judging a
  design), it belongs in a play: say which play, or that one is missing, and stop.

## Identity & mode

| State | Mode | What happens |
|-------|------|--------------|
| No loop folder | **new** | Interview → build |
| ICE exists, no SKILL.md | **new** | Skip the interview; build from the ICE |
| Both exist, user wants a check | **review** | Report gaps only — change nothing |

To change a loop that exists, use `/edit-loop`.

## Pipeline (new)

Run in order. Interactive by default: interview and ask for approval by typed reply (never
`AskUserQuestion`). With no person reachable, state each assumption and record that approval
was assumed.

### 1 — Intent and the loop's parts
Write `reference/ice.md` like the example's:
- **Intent** — the goal (one line: what the loop turns into what), constraints C-n and failure
  conditions F-n, implementation-agnostic. Write it as `/create-play` step 1 says
  (`../create-play/SKILL.md`). A loop's constraints are about the run: one issue and one
  branch, questions first, order and done checks, the checker.
- **Plays** — a table: the order they run in (any order works; no play takes another's
  output), play, what it gets from the contract (`inputs.<play>`) and which
  answers it gets (`answers.<play>`). Every input comes from the loop — the source, the
  person's write-up or the questions — never from another play's output (ADR 043; shared run,
  R5 step 6).
  Check each play exists and runs inside a loop, and that it reads every input the loop hands
  it: `<key>` of `inputs.<play>.<key>` appears in the play's SKILL.md. A key the play does not
  read is not handed — drop it, or change the play first.
- **Questions first** — each question the loop asks before any play runs, and the
  `answers.<play>.<key>` it fills; or `none`. A question a play would otherwise ask mid-run
  belongs here when the loop can know it up front (ADR 029 §2).
- **Checker** — `loops.<loop>.checker`: `kind` (`subagent` on a named model that is not the
  session's, or `coding-agent` — Codex) and `model`. It judges the loop's goal, constraints and
  Done means against the loop's outputs only, with the `judge-loop-result` skill.
- **Runner** — `loops.<loop>.runner`: `subagent` (default) or `headless`.
- **End** — the injected end sequence, plus any step the loop adds before the review (for
  example Discovery's typed confirmation of intents, until the review tool exists).
Present it and get approval.

### 2 — Expectation (generate, then confirm)
Generate the success scenarios (S-n, per persona, given/then/measure), exactly one recovery per
failure condition, and the **Done means** (D-n, 2–6 clauses from the closed set
`artifact_exists` | `field_equals` | `gate_outcomes_pass`) — as `/create-play` step 2 says.
A loop's Done means reads its own run folder (`{stm_base}<issue>/context/<loop>/<run-ts>/`):
the contract, every play's `<play>-done.json` (`done` = `true`, one clause per play), the
checker's `check.yaml`. Present for a quick
approve or revise.

### 3 — Steps and evals
A loop's steps are fixed: open (`start-change`) → questions first (loop) → write the contract
(loop, script) → **in rounds**: one step per play (owned by that play), then "after the round:
done, again or ask" (loop, script — `round_state.py`) and, only on ask, "the knowledge step"
(loop — the `knowledge-builder` agent finds, builds and briefs the missing knowledge, R5c) and
"brief the person on what the loop could not answer" (loop, R5b) → the checker → the end sequence → scenario validation →
close. A loop loops over its plays until its job is done; a play's open question is the
loop's, asked only when no play answers it (Shared Loop Run, R5 and R5b). Add only what the End section names. Then generate the evals as
`/create-play` step 5 says: a step eval (SE-n) per failure condition and per
artifact-verifiable constraint, placed after the step it checks; a scenario eval (SCE-n) per
scenario. Every eval reads a file the shared run writes (`answers.json`,
`answers-sources.json`, `contract.json`, `<play>-done.json`, `<play>-commit.json`,
`check.yaml`).

### 4 — Build the loop
Write the folder:
1. `SKILL.md`, matching the example: frontmatter (`name`, `description`, `user-invocable:
   true`, `kind: loop`, `position: both`); the Workflow opens with the Shared Loop Run block —
   the opener anchor, then exactly these lines, then the closer anchor:

   ```
   loop=<loop>
   plays=<play>,<play>,…
   questions=<key> -> answers.<play>.<key>; …   (or: none)
   runner_key=loops.<loop>.runner
   checker_key=loops.<loop>.checker
   end=<the end, in one line>
   ```

   The anchors' exact text is under "Enforced" in `loop-run.md`. The close is the Standard
   Play Close pointer, as `/create-play` step 6 says. It reads `../_shared/play-close.md`: that
   path holds once installed (the install lays both shared folders as one); in the source the
   file is `core/components/plays/_shared/play-close.md`, and the linters look there.
2. `stop-condition.yaml` from the Done means (`{name: stop-condition}`, `content.done`).
3. `scripts/`: copy unchanged — from `references/`: `loop_preflight.py`,
   `write_loop_contract.py`, `check_play_done.py`, `commit_run_files.py`,
   `run_play_headless.py`, `round_state.py`, `loop_status.py`, `prepare_check.py`, `run_checker_codex.py`,
   `record_check.py`, `group_questions.py`, `check_knowledge.py`, `record_review.py`; from `../create-play/references/`: `check_loop_contract.py`,
   `session_stamp.py`, `check_stop_condition.py`. A rebuild copies them again, so a loop never
   drifts from the shared run.
4. The fingerprint: run `shasum -a 256 reference/ice.md` and paste the digest. Never invent one.
5. The Next line: add the loop to `standards/rules/pipeline-next.md`.
6. The config, in `core/config.yaml`: under a top-level `loops:` block (the commented template
   there shows it), add

   ```yaml
   loops:
     <loop>:
       runner: subagent            # subagent | headless
       checker:
         kind: subagent            # subagent | coding-agent
         model: sonnet             # required for subagent: not the session's model
   ```

   and under `evidence:` → `plays:`, `<loop>: true` — a loop always records its evidence
   (ADR 029).

### 5 — Verify (run the linter)

From the repository root:

```
python3 core/components/plays/create-loop/scripts/lint_loop.py core/components/loops/<loop>/SKILL.md \
    --next-map core/components/memory/standards/rules/pipeline-next.md
```

It runs every play check (coverage, one recovery per failure, no orphans, required sections,
the close, the stop condition, the fingerprint, the Next line) and the loop's own: `kind`,
`position: both`, the run anchors and the shared file, the values (with `end=`) and their
config keys, every play exists and runs inside a loop, every step's owner, the Done means, the
stamped scripts unchanged from their source, the fingerprint matching `reference/ice.md`, the
config entries (runner, checker kind, evidence on), one step and one done clause per play, and
every handed input read by its play. Fix every GAP and run it again until it passes. Then run
`node core/tools/lint-components/index.js --target core/components --output json` and clear any
error whose file is the loop's. That command exits 1 while other components carry old errors;
that is not this loop's gap. The linter checks that an eval exists, not that it means something: check that
yourself.

## Review mode (read-only)

Run the linter as step 5 says, then add the checks a script cannot make: each play
still does what the loop's Plays table says; the questions really cover what the plays ask;
the fingerprint still matches `reference/ice.md` (`shasum -a 256`); the evals are meaningful.
Report a short PASS/GAP table and stop. To fix gaps, use `/edit-loop`.

## Hard rules

- A loop does no work of its own. Every step is owned by the loop (asking, the contract),
  its checker, one of its plays, or a change play. Real work goes into a play.
- Never copy the shared run's steps or the shared close into a loop; point to them.
- Every play a loop names must run inside a loop. Fix the play, not the loop.
- A loop always has a Done means, baked into `stop-condition.yaml`.
- Stamp the shared scripts unchanged; never edit a stamped copy.
- Run `lint_loop.py` and clear every gap before calling the loop built.
- Check the loop against the loop principles (`docs/components/loops.md`, "The loop principles").
  The linter does not check them all yet (#699); check the rest by hand.
- In review mode, change nothing.
