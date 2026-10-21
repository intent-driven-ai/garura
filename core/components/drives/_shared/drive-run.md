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
| `plays` | The plays. Each one runs inside a drive (it checks a drive contract). No play takes another's output as its input (ADR 043); the order is only the order they run in, in turn. |
| `questions` | The questions asked first, and which play's `answers` each one fills; or `none`. |
| `documents` | The documents the person gives first, beside the questions (Kickoff: the write-up); or `none`. |
| `source` | The source the drive reads once for every play (Kickoff: the prototype), or `none`. |
| `runner_key` | `drives.<drive>.runner` — how each play runs: `subagent` (default) or `headless`. |
| `checker_key` | `drives.<drive>.checker` — who checks the result: `kind` (`subagent` or `coding-agent`) and `model`. |
| `end` | How the drive ends (its End section), in one line. |
| `max_rounds` | `drives.<drive>.max_rounds` — the most rounds before the drive asks (default 3). |

## The run

**The drive presents its status as it goes** (`standards/rules/run-status.md`). At each step
below, and when each play starts and ends, it updates `{stm_base}<issue>/status/run-<drive>.json`
— its state, round, play and step in plain words:

```bash
python3 scripts/drive_status.py --file "{stm_base}<issue>/status/run-<drive>.json" \
    [--name <drive> --issue <issue> --run-id <drive_run_id>] \
    --state running --round <n> --play <play> --step "<what it is doing, in plain words>"
```

The drive never shows the status itself and does not know who reads it; a display (for Claude
Code, a separate plugin) reads the file. Before R2 opens the issue, the status waits in the
scratch folder and moves with the rest.

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

Ask the drive's `questions` before any play runs — only what the drive itself needs from the
person to start (for Kickoff, where the prototype is). Ask them in plain words, one at a time,
and wait for typed answers (never `AskUserQuestion`). The drive reads no memory itself (ADR 039,
ADR 041 §8): what memory can answer is for its plays' agents, through the memory tool.
Write the answers to `<working>/answers.json`, keyed by play, as plain values (what the plays
read). Write where each came from to `<working>/answers-sources.json`, with the same keys:

```json
{"intent": {"argument": {"from": "person"}, "may_change_data": {"from": "person"}}}
```

`person` is a typed answer; `memory` (written by a play's agent on a later round) names the
tier, the path and the decision trace the memory tool recorded. A person's answer is kept in the issue's short-term memory (ADR 039 §1). With
`questions: none`, write `{}` to both.

**Documents first (ADR 043).** A drive that names `documents` gets them from the person here,
before any play runs. For Kickoff that is the **write-up**: a few lines, beside the prototype,
in five parts — what the product is; who uses it; the field it serves and the job it does
there; what on the screens is only sample data; a walkthrough of the steps a person takes.
When the person did not give it with the drive's argument, ask for it in plain words and wait
for the typed reply. Save it, exactly as given, as a Source in the issue's short-term memory —
`{stm_base}<issue>/context/<drive>/<run-ts>/write-up.md` — with `from: person` in
`answers-sources.json` (`"documents": {"write_up": {"from": "person"}}`). Every play gets it
inside its capture (R4b). A drive never writes the document itself.

### Step R4 — Write the drive contract

```bash
python3 scripts/write_drive_contract.py --drive <drive> --drive-run-id <drive>-<run-ts> \
    --branch "$(git branch --show-current)" --issue <issue> \
    --review-dir "{stm_base}<issue>/review/drive/" --plays <play>,<play>,… \
    --inputs <working>/inputs.json --answers <working>/answers.json \
    --out <working>/contract.json
```

One contract for every play (`standards/rules/drive-contract.md`). Exit 2 halts the drive.

### Step R4b — Read the source once (ADR 043)

A drive that names a `source` reads it once, before any play, and every play reads that one
capture — none captures or walks the source again, and none reads another play's output.
The tools are the ones `/intent` uses run by hand, laid beside the drive at install
(`../intent/scripts/`).

1. **Capture the source and the write-up**, each as a Source kept exactly as read:

   ```bash
   python3 ../intent/scripts/capture_source.py --source <the prototype: file, folder or link> \
       --out-dir "{stm_base}<issue>/evidence/<drive>/capture/source-prototype" \
       --given-by "<git user.name> <<git user.email>>" \
       --manifest "{stm_base}<issue>/evidence/<drive>/capture/source-manifest-prototype.json"
   python3 ../intent/scripts/capture_source.py --statement <working>/write-up.md \
       --out-dir "{stm_base}<issue>/evidence/<drive>/capture/source-write-up" \
       --given-by "<git user.name> <<git user.email>>" \
       --manifest "{stm_base}<issue>/evidence/<drive>/capture/source-manifest-write-up.json"
   ```

   A capture that cannot read or run the source halts the drive.

2. **Walk it once.** Dispatch the `prototype-reader` agent, in the foreground; it plans the
   journeys from the write-up's walkthrough, then covers every main section the screens show:

       { "task":    "walk this prototype in journeys, the way the people it serves would",
         "inputs":  { "source": "<the prototype>",
                      "source_manifest": "<capture>/source-manifest-prototype.json",
                      "write_up": "<working>/write-up.md",
                      "may_change_data": "<true for a file or local prototype; else answers.may_change_data>",
                      "walk_script": "../intent/scripts/walk_prototype.py",
                      "check_script": "../intent/scripts/check_journeys.py" },
         "outputs": { "journeys": "<capture>/journeys.yaml",
                      "evidence_dir": "<capture>/source-prototype/journeys/",
                      "check_report": "<capture>/journeys-check.json" },
         "task_id": "walk-prototype" }

   Its check report must read `ok: true`; else halt.

3. **Hand the capture to every play.** For every play in `plays`, add
   `inputs.<play>.capture = {"source_manifest": "<capture>/source-manifest-prototype.json",
   "write_up_manifest": "<capture>/source-manifest-write-up.json", "write_up":
   "<working>/write-up.md", "journeys": "<capture>/journeys.yaml", "view_texts":
   "<capture>/source-prototype/"}` and run R4 again (same `drive_run_id`). Commit the capture
   with the run files (R5 step 5). A play handed a capture reads it, and the write-up, instead
   of capturing or walking the source again; run by hand, a play still reads its source itself.

### Step R5 — Run the plays, in rounds, until the drive's job is done

A drive runs its plays "repeatedly, until its intent is met" (glossary, Drive; ADR 029,
ADR 043). A **round** runs every play in `plays` — round 1 all of them, a later round only the
plays the gap skills gave work to. No play takes another play's output as its input: each reads
the capture and the write-up, writes its own kind (for Kickoff: `/intent` business intents,
`/vision` domains, `/understand` capabilities and functionalities), and the drive connects them
after the round. The first build runs the plays one after another, in turn; side by side comes
once the scoped-write guard can tell two plays' writes apart. A question one play cannot answer
is the **drive's** question, not a stop: the play records it, does all the work it does not
block, and the drive goes on — the other plays may answer it, and the play fills it on the next
round. The drive stops and asks the person only what no play of the drive can answer (ADR 041). Round 1 starts with the contract's `round: 1`; each later round writes the
contract again (R4) with the next number and any new answers.

For each play in `plays`:

1. **Note the start.** `date +%s` → `<since>`.
2. **Run it with the configured runner.**
   - `subagent` (default): dispatch one sub-agent per play (layer 1), **in the foreground** —
     the drive waits for it to return and never starts it in the background. (A headless
     session ends its turn while a background sub-agent runs, and stops it 10 minutes
     later.) It runs
     `/<play> --contract <working>/contract.json [<argument>]` — `<argument>` is
     `inputs.<play>.argument` when the contract sets it (for example the prototype `/intent`
     reads), handed on the play's command line as a person would type it — and returns only a compact result: its
     status, its stop-condition verdict path, its review record path, and any question it
     stopped on. The play dispatches its own agents and judges (layer 2).
   - `headless`: `python3 scripts/run_play_headless.py --play <play> --contract
     <working>/contract.json [--argument "<argument>"] --out <working>/<play>-run.json`.
3. **A question the play cannot answer goes to the drive.** The play writes it to
   `<review_dir>/open-<play>.json` (drive contract, step 5) and finishes what it can — it does
   not stop to ask. A question that research can answer is drafted as a memory update for a
   person to approve (ADR 035); nothing rests on it until then.
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
6. **No hand-on between plays.** A play's input is the capture, the write-up, the person's
   answers and — on a later round — exactly the work the gap skills gave it
   (`inputs.<play>.targets`). It never takes another play's output as its input (ADR 043).

7. **After the round, close the model's gaps (ADR 043).** The drive holds no judgment of its
   own: dispatch `product-os-keeper` once, in the foreground, to run the two gap skills over
   the whole model, with this contract:

       { "task":    "find the product model's gaps, then close what the model itself can take",
         "inputs":  { "product_base": "<product_base>",
                      "journeys": "<capture journeys.yaml>", "view_texts": "<capture views/>",
                      "write_up": "<working>/write-up.md" },
         "outputs": { "candidates": "<working>/gap-candidates-round-<n>.json",
                      "gaps": "<working>/gaps-round-<n>.json",
                      "close_report": "<working>/close-report-round-<n>.json" },
         "task_id": "close-model-gaps" }

   The agent runs `find-model-gaps` (its script `find_gaps.py`, then its judgment →
   `gaps.json`: the links to make, the duplicates, the work for each play, the screens no node
   covers) and then `close-model-gaps` (`apply_links.py --gaps <gaps> --product-base
   <product_base> --out <close_report>`: it links loose nodes, moves a holding-folder page
   under its parent, links nodes to intents both ways and merges agreed duplicates; the work
   it cannot do in the model goes back in `work_for_plays`). Then commit the round once — the
   run files and the model together:

   ```bash
   python3 scripts/commit_run_files.py --issue-dir "{stm_base}<issue>/" --issue <issue> \
       --branch <the contract's branch> --play round-<n> --also "<product_base>product-os" \
       --out <working>/round-<n>-commit.json
   ```

8. **After the round, decide.**

   ```bash
   python3 scripts/round_state.py --round <n> --max-rounds <drives.<drive>.max_rounds, default 3> \
       --working <working> --review-dir "<review_dir>" --issue-dir "{stm_base}<issue>/" \
       --model-path "<product_base>" --gaps <working>/gaps-round-<n>.json \
       --close-report <working>/close-report-round-<n>.json --out <working>/round-<n>.json
   ```

   - `done` — no question is open, every node is linked and no screen is left uncovered: go
     to R6.
   - `again` — the model, the open questions or the gaps moved: run round n+1, with only the
     plays `round-<n>.json` names in `next`, each handed its work as `inputs.<play>.targets`
     (R4 with `--round n+1`).
   - `ask` — a whole round closed nothing new, or the round limit is reached: the open
     questions and the gaps left are the drive's. Go to R5c, then R5b.

### Step R5c — Find and build the knowledge the round found missing

Before asking anyone, run the knowledge member plays (ADR 042), each as a play runs (the
configured runner, in the foreground, with the contract), in this order:

```bash
/search-knowledge --contract <working>/contract.json
/build-knowledge  --contract <working>/contract.json
```

`/search-knowledge` merges the questions asked again and answers what the drive's sources show
(quoted) and what memory holds (through the memory tool, traced). `/build-knowledge` closes what
it left: a researched knowledge page raised through the memory tool as a memory update waiting
for a person (ADR 035), our proposed answer with its basis and context for what only the person
can confirm, a note for each screen state the prototype lacks, and settled for what the context
already answers. Each play's done check must hold; then commit its run files (R5 step 5).

### Step R5b — Brief the person on what the drive could not close

Only now, and only once per stop, the drive reaches the person — with a brief, never a
questionnaire:

1. Run the member play `/review-knowledge --contract <working>/contract.json`. It writes
   `{stm_base}<issue>/context/review-knowledge/round-<n>/brief.md`: what we understood, what we
   built (the draft first — for Kickoff, each proposed business intent, the domain and its
   capabilities), and where the gaps are — a few themed gaps, each with its context and our
   proposed answer — then the points settled from the context, each with why, the knowledge
   pages waiting for approval, each with its sources and our recommendation, and a pointer to
   the notes for the prototype. Its done check must hold;
   commit its run files.
2. Show `brief.md` as it is, and wait for the typed reply (never `AskUserQuestion`). "yes" takes
   every proposal and every recommendation shown; the person may correct a gap, a settled point
   or a page by its id.
3. Write the reply as `review.json` (`words` verbatim; each gap `accept` or the person's own
   answer; each page `approve` or `reject`) and record it:

   ```bash
   python3 <review-knowledge play dir>/scripts/record_review.py \
       --brief <brief.json> --reply <working>/review.json --build <build.json> \
       --search <search.json> --review-dir <review_dir> --issue-dir "{stm_base}<issue>/" \
       --round <n> --out <working>/review-record.json
   ```

   It writes the answers to the issue's short-term memory (`from: person`, with what each
   accepted proposal rested on) and maps each one back to the questions it closes, per play.
   Record each page decision through the memory tool's `decide` (decided in the session — the
   stand-in for Argus's memory view, ADR 041 §8); an approved page is not yet promoted — a
   person promotes it later. Add the mapped answers to `answers.json` / `answers-sources.json`
   (`from: person`), and run round n+1. The person may type **stop**:
   close HALTED with `exit_reason: stopped_at_question`.

### Step R6 — The checker (ADR 029 §2)

A model or agent that did not run the drive checks the result against the drive's own
criteria — its goal, its constraints and its Done means. It sees the drive's outputs, never
its reasoning. Its rules, prompt and verdict shape are the `judge-drive-result` skill.

1. **Build the bundle** — the only thing the checker reads:

   ```bash
   python3 scripts/prepare_check.py --ice <drive-dir>/reference/ice.md --issue <issue> \
       --issue-dir "{stm_base}<issue>/" --working <working> \
       --base <start-change's base_sha> --out-dir <working>/check/
   ```

2. **Run the checker** the config names (`checker_key`, resolved in R1):
   - `subagent` — dispatch the `drive-checker` agent on `checker.model` (required: a model that
     is not the session's), with this contract and nothing else:

         { "task":    "judge this drive's result with the judge-drive-result skill",
           "inputs":  { "bundle": "<working>/check/" },
           "outputs": { "verdict": "<working>/check/verdict.json" },
           "task_id": "drive-check" }

   - `coding-agent` — Codex, in a read-only sandbox on the bundle:

     ```bash
     python3 scripts/run_checker_codex.py --bundle <working>/check/ \
         --skill ../judge-drive-result/SKILL.md [--model <checker.model>] \
         --out <working>/check/verdict.json
     ```

3. **Record the verdict:**

   ```bash
   python3 scripts/record_check.py --verdict <working>/check/verdict.json \
       --manifest <working>/check/manifest.json --kind <checker.kind> [--model <checker.model>] \
       --out <working>/check.yaml
   ```

   Exit 0 — pass, go on. Exit 1 — reject: halt (`checker_reject`); `check.yaml` names each
   failed criterion and why. Exit 2 — no verdict, or one that does not match the shape: halt;
   it is never a pass.

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
| The checker gives no verdict, or a malformed one | `checker_invalid` |
| The person stops at the drive's questions | `stopped_at_question` |

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
