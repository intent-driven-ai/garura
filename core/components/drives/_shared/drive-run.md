# Shared Drive Run

The steps every drive runs, in order. A drive is a higher-order play: it runs other plays
until its intent is met or it fails, and carries no rules of its own (ADR 029). So the run is
the same for every drive and lives once, here (`core/components/drives/_shared/drive-run.md`;
the install lays it in the installed `_shared/` folder beside the plays' shared close). A
compiled drive holds only the two anchor lines, its own values — its plays in order, its
questions, its config keys, its end — and points here. `/drive-creator` emits exactly that, so
a direct edit and a rebuild converge.

## The drive's own values

The drive's Workflow section sets these between the anchors:

| Value | What it is |
|-------|-----------|
| `drive` | The drive's name (e.g. `kickoff`). |
| `plays` | The plays, in order. Each one runs inside a drive (it checks a drive contract). |
| `questions` | The questions asked first, and which play's `answers` each one fills; or `none`. |
| `runner_key` | `drives.<drive>.runner` — how each play runs: `subagent` (default) or `headless`. |
| `checker_key` | `drives.<drive>.checker` — who checks the result (item 6 of #613). |
| `end` | How the drive ends (its End section), in one line. |

## The run

### Step R1 — Pre-flight

```bash
git branch --show-current
python3 scripts/drive_preflight.py --config .garura/core/config.yaml --drive <drive> \
    --skills-root .. --plays <play>,<play>,… --branch "$(git branch --show-current)" \
    --out <working>/preflight.json
```

It returns the facts as JSON: `stm_base`, `runner`, `checker`, `evidence_record` (the drive's
own `evidence.plays.<drive>`, else `evidence.record`, else true), and `plays_ok` with any play
that is missing or does not accept a drive contract. Exit 2 is a hard halt. Then run the
drive's own pre-flight rows (for example Kickoff's prototype check).

### Step R2 — Open the change

Run `start-change` as a sub-play (`parent_run_id`): one issue, one branch for the whole drive.
Everything the drive and its plays write goes under that issue (ADR 039 — the issue ID
governs). The working folder is `{stm_base}<issue>/context/<drive>/<run-ts>/`.

### Step R3 — Questions first (ADR 029 §2, ADR 034)

Ask the drive's `questions` before any play runs. Ask them in plain words, one at a time, and
wait for typed answers (never `AskUserQuestion`). Look in memory first, through the memory
tool: a question memory already answers is not asked; record where the answer came from.
Write the answers to `<working>/answers.json`, keyed by play, as plain values (what the plays
read). Write where each came from to `<working>/answers-sources.json`, with the same keys:

```json
{"intent": {"who_asks": {"from": "person"},
            "proof":    {"from": "memory", "tier": "phoenix", "path": "knowledge/…", "trace": "<citation id>"}}}
```

`person` is a typed answer; `memory` names the tier, the path and the decision trace the memory
tool recorded. A person's answer is kept in the issue's short-term memory (ADR 039 §1). With
`questions: none`, write `{}` to both.

### Step R4 — Write the drive contract

```bash
python3 scripts/write_drive_contract.py --drive <drive> --drive-run-id <drive>-<run-ts> \
    --branch "$(git branch --show-current)" --issue <issue> \
    --review-dir "{stm_base}<issue>/review/drive/" --plays <play>,<play>,… \
    --inputs <working>/inputs.json --answers <working>/answers.json \
    --out <working>/contract.json
```

One contract for every play (`standards/rules/drive-contract.md`). Exit 2 halts the drive.

### Step R5 — Run each play, in order

For each play in `plays`:

1. **Note the start.** `date +%s` → `<since>`.
2. **Run it with the configured runner.**
   - `subagent` (default): dispatch one sub-agent per play (layer 1). It runs
     `/<play> --contract <working>/contract.json` and returns only a compact result: its
     status, its stop-condition verdict path, its review record path, and any question it
     stopped on. The play dispatches its own agents and judges (layer 2).
   - `headless`: `python3 scripts/run_play_headless.py --play <play> --contract
     <working>/contract.json --out <working>/<play>-run.json`.
3. **A question stops the drive.** When the play stops on a question nothing in memory or the
   contract answers, bring it to the person in plain words and wait for the typed answer. The
   answer goes to the issue's short-term memory. Then resume the same play with the answer (the
   same sub-agent, or `run_play_headless.py --resume <session>`), so it keeps its context.
4. **Check its done check.**

   ```bash
   python3 scripts/check_play_done.py \
       --verdict "{stm_base}<issue>/status/stop-condition-<play>.yaml" --not-before <since> \
       --out <working>/<play>-done.json
   ```

   Exit 0 — held, go on. Anything else halts the drive: the play missed its done check.
5. **Commit its run files** (the play commits only its own product change).

   ```bash
   python3 scripts/commit_run_files.py --issue-dir "{stm_base}<issue>/" --issue <issue> \
       --branch <the contract's branch> --play <play> --out <working>/<play>-commit.json
   ```

   Exit 0 — committed (or nothing to commit) and the tree is clean. Exit 1 — files outside the
   issue's folder are still changed: halt, so the next play does not start on an unclean tree.
   Exit 2 — wrong branch, or something else was already staged: halt.
6. **Hand on what later plays need.** When a later play's input is what this play made (for
   example `/vision` takes the intents `/intent` saved), add it to `<working>/inputs.json` under
   that play and run R4 again, with the same `drive_run_id`. The contract stays one file; it is
   written again before the next play starts, and each play reads it when it starts. Nothing a
   play has already read changes.

### Step R6 — The checker (ADR 029 §2)

A different model or coding agent, picked by `checker_key`, checks the result against the
drive's Done means. It gets only the drive's outputs — the product change, the plays' review
records, the trace check — never the drive's reasoning. It writes `pass` or `reject`, with
reasons, to `<working>/check.yaml`. A reject halts the drive. (The checker's script comes with
item 6 of #613.)

### Step R7 — End

Run the drive's `end`. The pieces it uses are the injected end sequence (`commit-change` →
`propose-change` → `review-change` → `merge-change`, each a sub-play with `parent_run_id`),
the merge keeping its pinned human approval. A drive whose End section adds a step (Kickoff:
the person confirms each proposed intent by typing, before the review) runs it where the End
section says.

### Step R8 — Close

Run the Standard Play Close (`../_shared/play-close.md` once installed; in the source it lives
with the plays, `core/components/plays/_shared/play-close.md`) with the drive's values. The
evidence names every play's compact result (status, done check, commit), the contract, the
answers and the checker's verdict. The drive writes the one delivery report for the run.

## Halts

| When | Exit reason |
|------|-------------|
| Pre-flight fails, or a play is missing | `preflight` |
| A play misses its done check | `play_not_done` |
| Files outside the issue's folder stay changed after a play | `unclean_tree` |
| The checker rejects | `checker_reject` |
| The person stops at a question | `stopped_at_question` |

A halted drive closes HALTED with its exit reason. Its run stays under the issue, so a re-run
resumes from the first play not done.

## Enforced

`lint-components` and `lint_drive.py` check every drive's SKILL.md for the two anchor lines,
each exactly once, opener before closer, and that this file exists:

- opener: `# --- Shared Drive Run (shared; see ../_shared/drive-run.md) ---`
- closer: `# --- end Shared Drive Run ---`

## Related

- ADR 029 — Drives. `standards/rules/drive-contract.md` — how a play runs inside a drive.
- `../_shared/play-close.md` — the close every play and every drive runs.
