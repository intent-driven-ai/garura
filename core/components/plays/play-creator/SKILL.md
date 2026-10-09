---
name: play-creator
description: >
  Compiles a deterministic "play" (a multi-step, gated workflow recipe) from an
  intent. Interviews for the intent triple, generates the expectation, identifies
  the skills, scripts, and agents the play needs, selects a workflow structure, generates
  evals, and writes a compiled play (a SKILL.md plus scripts for its mechanical work).
  Use when the user wants to create, build, compile, or review a play — or says
  "create a play", "new play", "compile this into a play", "play-creator", "turn this
  intent into a play", or "review my play for gaps" — even if they don't say "play" but
  describe a repeatable, multi-step, checkpoint-gated workflow they want captured as a
  runnable recipe.
user-invocable: true
model: best
---

# play-creator

The play compiler for garura. It takes an **intent** and produces a
compiled, deterministic **play** — a `SKILL.md` (plus a `scripts/` folder for its
mechanical work) whose pre-flight checks, task graph, step order, eval criteria, and
recovery are all built in, so running the play later requires no re-planning.

This skill is deliberately self-contained: it runs the whole pipeline itself
rather than dispatching to separate builder agents. It is lean to *operate*; the
play it *produces* is full-featured. Keep that split in mind — simplifying the
generated play is under-delivering; adding runtime plumbing to this skill's own
operation is over-building.

Following the harness-led principle — the skill decides, scripts execute — the
**mechanical** checks (coverage counting, orphan detection, fingerprinting) are
offloaded to a script, `scripts/lint_play.py`. Spend tokens on judgment, not
on counting the model can get wrong.

**Hold the play you build to that same standard.** When a step in the play you're
compiling does mechanical, deterministic work — parsing, counting, validating, formatting,
a fixed file transform, hashing — generate a small script for it and have the step *call*
the script, instead of spelling the work out as prose the play re-reasons every run. Keep
judgment (decisions, generation, anything needing context) in the step's prose. So a
compiled play is normally a **folder** — `SKILL.md` plus a `scripts/` folder for its
mechanical work (and `references/` for anything it reads) — not a lone file. Only a
pure-judgment play with no mechanical work stays a single `SKILL.md`. This is the same
move you just read about this skill, applied one level down: every play this compiler writes
should itself be harness-led.

## The mental model: ICE

A play is compiled from a clean **ICE** triple:

- **Intent** — the implementation-agnostic core: a one-line goal, a list of
  **constraints** (rules the play must respect), and **failure conditions** (what
  makes the play's outcome wrong). No tools, no file paths, no step-by-step how.
- **Context** — the surrounding grounding the play draws on (relevant memory,
  prior art, the shape of the codebase it acts on). Often light for simple plays.
- **Expectation** — generated from the Intent: **success scenarios** (per-persona,
  given/then/measure) and exactly one **recovery** entry per failure condition.
  Generated, never hand-authored — hand-authoring scenarios is the pattern ICE rejects.

The compiler's job is to turn that triple into a deterministic recipe and to prove,
via a coverage check, that every constraint, failure condition, and scenario is
enforced by some concrete mechanism in the output.

## Roles & handoffs — how every play you build is wired

A play this compiler builds always uses the same roles and one handoff mechanism. Build
this into every play.

- **Play — the orchestrator.** It owns the workflow and the step order, and does no domain
  work itself. It hands work out and routes the results.
- **Subagent — context and assurance.** A subagent gathers the context a piece of work
  needs *before* it runs and checks that what came back is *right* after. It bookends the
  work; it does not do the building.
- **Skill — the worker.** Skills are where the actual work happens — build, generate,
  transform, produce the artifact.
- **Script — the mechanical hand.** Deterministic work (parse, count, hash, validate) a
  step calls directly, per the principle above.

**The handoff is always a JSON contract — never inline prose or pasted data.** Play →
subagent → skill and back, every hop passes a JSON contract. The real outputs are written
to **files on disk**; the contract carries the *paths*, not the contents. A hop says, in
effect, "your inputs are these files, write your output here," and returns "done — the
output is at this path." The bytes live on disk; the contract moves the references. (A
script a step calls directly follows the same disk discipline — paths in, files out.)

That is why a subagent never returns a wall of prose and a skill never takes a prose
prompt: the wiring is files + contracts, so any step can be resumed, re-run, or handed off
without re-deriving anything.

## Structural gate (do this first)

Before anything else, decide whether the requested play has enough structure to
compile. A play is compilable when its intent defines **at least one constraint and
at least one failure condition**, and it has (or can generate) **at least one success
scenario**. If the user only has a vague wish with no constraints and no failure
modes, it is structureless — do not invent a play. Say what's missing and help them
pin down: what must always hold (constraints) and what would count as the play
getting it wrong (failure conditions). Then proceed.

Ideas that describe runtime-assembling workflows, dynamic intent resolution, or
self-modifying DAGs are out of scope — this compiler produces *static, deterministic*
plays only. Acknowledge and redirect; don't reject outright.

## Identity & mode

Ask for (or infer) the **play name** and check whether `intent`/`SKILL.md` already
exist for it.

| State | Mode | What happens |
|-------|------|--------------|
| Nothing exists | **new** (default) | Build from scratch: gather intent → compile |
| Intent exists, no play | **new** | Skip the interview, compile from the existing intent |
| Both exist, user wants a check | **review** | Diagnose gaps only — **read-only, never modify** |

Review mode is the one exception to "this skill produces a play" — it produces a
gap report and stops. See [Review mode](#review-mode-read-only) below.

## Pipeline (new)

Run these in order. Each step's output feeds the next.

This pipeline is interactive by default — it interviews and asks for approval. If you're
running it without a reachable human (an automated or test run), don't block: state your
assumptions explicitly at each interview and approval point, record that approval was
assumed, and proceed.

### 1 — Intent (the clean triple)
Interview the user (or read an existing intent) and write the triple: a one-line
`intent`, a numbered list of `constraints` (each with an id like C1 and a rule),
and a numbered list of `failure_conditions` (each with an id like F1 and a condition).
Keep it implementation-agnostic — strip any mention of specific tools, technologies,
file paths, or ordered how-to steps; those belong in the compiled play, not the intent.
Present it back and get explicit approval before moving on.

### 2 — Expectation (generate, then confirm)
From the approved intent, generate the expectation:
- One or more **success scenarios**, each with an id (S1…), a persona, a `given`,
  a `then`, and a binary-testable `measure`.
- Exactly **one recovery entry per failure condition** (F1→REC1, …), each naming the
  trigger symptom, the corrective direction, and a `handoff` of `autonomous` (the fix
  can loop back without a human) or `human` (needs a person to decide).
- A **"### Done means" section (#464)** — the play's stop condition: 2–6 clauses, each
  with an id (D1…), a plain-language `says`, and a mechanical `check` drawn from the
  closed clause set (`artifact_exists` | `field_equals` | `gate_outcomes_pass`).
  Compose the clauses from the scenarios' measures and the artifact-verifiable
  constraints — the done statement is what the measures already promise, made
  evaluable against the run's artifacts at close. A done that cannot be composed
  mechanically is a sign the measures are not binary — fix the measures, don't
  hand-wave the done.
Derive these from the intent — do not ask the user to write them. Present the generated
expectation for a quick approve/revise.

### 3 — Skills, scripts & agents the play needs
From the intent, work out what the play actually has to *do*, and split each piece of work
by its nature — this split is where the token savings live:
- **Scripts** — programs in the play's `scripts/` for the **mechanical, deterministic** actions (parse,
  count, validate, transform, hash, format, threshold/precedence logic). The step calls
  the script; the script does the work. Prefer a script for anything a script can do
  reliably. **Two hard rules for scripts:**
  - **Split by judgment versus mechanical work, not by git versus non-git.** Fixed
    git/gh/host work — a command sequence with no decisions in it (cut a branch, push,
    open or merge a PR, fetch a diff, post a comment, read merge state) — runs in a script
    through the code-host adapter (`references/platform_adapter.py`), not in an agent.
    An agent takes about 10× as long to run the same fixed commands. Real **judgment**
    about repo or host state stays with a skill or agent: grouping changes by concern,
    matching an issue from a description, assessing review categories, checking a design.
    Rule of thumb: if you could write the exact commands ahead of time, it is a script; if
    it needs a decision, it is an agent. Scripts do no judgment. (#484)
  - **Give fixed rules to scripts, not to the model.** If a step's work is a fixed rule — a
    threshold verdict, a most-specific-wins choice, a table lookup, a count, or a
    diff-scope check — write it as a script. A subagent or prose doing this work breaks
    the harness-led principle; flag it and convert it.
- **Skills** — where the actual work happens: build, generate, transform, produce the
  artifact.
- **Subagents** — gather the context a skill needs and verify that what the skill produced
  is right; they bookend the work, they don't do it. Add one only when the work genuinely
  needs gathered context or an independent correctness check.
For each, note whether it already exists or must be created. Remember the handoffs are JSON
contracts over files on disk (see **Roles & handoffs** above). **Short-circuit rule:**
if a piece's only output is something derivable deterministically from context (a
branch name, a path, a config value), don't spawn an agent for it — the play computes
it inline. Audit every agent the play will use against the 11 agent principles in
[`references/agent-audit.md`](references/agent-audit.md) (P1–P11); list any that fail
so the user can fix or drop them. A fully deterministic play — pure git, file, or
config operations the play can compute itself — may legitimately need **zero agents**.
That is correct, not a gap. The compiled-play example uses agents, but yours need not;
don't invent an agent just to match the template.

### 4 — Workflow structure
Pick the shape that fits the work. The four structures (full-checkpoint A, fast B,
chained C, readiness-only) and when each applies are in
[`references/workflow-structures.md`](references/workflow-structures.md). Derive the
play's **pre-flight checks** here too: every constraint that is really an environmental
precondition ("must be on a feature branch", "config must exist") becomes a pre-flight
check with an action-on-failure (hard halt, graceful exit, or hard block).

**Concurrent read-only fan-out (#468).** When a step does the same read-only work over N
independent items — one isolated sub-agent per doc, one runner per check — write it as a
concurrent fan-out (one batch, then join), not a serial loop, provided the three safety
conditions hold (read-only over shared inputs, distinct output paths, no sibling
dependency). The form and the required declaration are in
[`references/workflow-structures.md`](references/workflow-structures.md) and
`standards/rules/concurrent-fanout.md`. A step whose sub-tasks write to the repo stays
serial (#488).

**Pre-flight script.** The start-up facts a play needs are always worked out the same way,
so a script finds them, not the model. A script gives the same answer every run; reasoning
in prose can drift. In each compiled play:

1. Copy [`references/preflight.py`](references/preflight.py) unchanged to
   `scripts/preflight.py`. The Pre-flight phase calls it.
2. Before the call, the play runs the only two live git reads — `git branch --show-current`
   and `git status --porcelain` — and passes the results in with `--branch` and
   `--porcelain-file`. The script itself never runs git or gh, so it works offline.
3. The script returns one JSON object with these facts:
   - the folder paths from config;
   - whether to record evidence (the play's own setting, else the global one, else true);
   - the issue number, read from the branch name;
   - `on_default_branch` — whether the branch is main;
   - `changes_present` — whether there are changes to work on.
4. Copy [`references/session_stamp.py`](references/session_stamp.py) unchanged to
   `scripts/session_stamp.py`. Run it with `--phase start` right after `preflight.py`. It
   leaves a marker that the close step (`play-close.md`) reads later. If it fails, carry
   on — it never stops the play.
5. The play's Pre-flight table holds only its own rules: for each fact, stop, exit quietly,
   or block. These differ per play. For example, "no changes" means *nothing to do, exit
   quietly* for `commit-change`, but it is the clean start that `propose-change` needs.
6. Checks that need the code host (is a PR open, can it merge, does a worktree exist) go
   through the code-host adapter below, not through an agent.

Skip this only for a play that just talks to the user and checks nothing about the
project. Any play that reads config, the branch, the issue, or the changes must use it.
(#434, #463)

**Code-host scripts.** Fixed git and GitHub jobs are run by scripts, not by agents. An agent
is slow and adds nothing when the steps never change. Agents are kept for jobs that need
judgment: grouping changes, matching an issue, sorting a change into categories, and
checking a design.

1. Use this for any play that makes a branch, pushes, opens or merges a PR, fetches a diff,
   posts a comment, or reads merge state. That includes `start-change`, `propose-change`,
   `review-change`, and `merge-change`.
2. Copy [`references/platform_adapter.py`](references/platform_adapter.py) unchanged into
   the play's `scripts/`. It is one adapter for GitHub and GitLab. It reads which host to
   use from config.
3. Copy the job scripts the play needs from `references/`: `setup_branch.py`,
   `submit_pr.py`, `read_merge_state.py`, `merge_pr.py`, `fetch_pr_context.py`,
   `post_verdict.py`. Each one is built on the adapter.
4. The play's step runs the script directly.

Because play-creator writes these scripts into the play, a rebuild brings them back. The
play does not slip back to the slow agent way. (#484)

### 4b — Pipeline position (D2)
Read the play's declared `position` (frontmatter: `start | end | both | none`, default
`none`) and fold in the standard delivery machinery per
[`standards/rules/pipeline-position.md`](../../memory/standards/rules/pipeline-position.md):

- **start** → prepend a first step that runs the `start-change` sub-play (resolve/create
  the issue, cut the branch off fresh main, optional worktree, init STM).
- **end** → append the end sequence as ordered closing steps, before Evidence & Close, in
  order: `commit-change` → `propose-change` → `review-change` → `merge-change`.
- **both** → both of the above, bracketing the play's own work (the self-contained
  "start, do everything, close the loop" shape).
- **none** → inject nothing (strategic/model-building and standalone plays).

Inject as **explicit, named sub-play steps** wired as JSON contracts over files on disk
and dispatched with `parent_run_id` (sub-play evidence convention, `play-close.md`), woven
into the Task DAG — `start-change` at the head, the four end plays as the closing chain
(each `blockedBy` the previous) right before the Evidence & Close step. Never collapse the
end sequence into one opaque step. The six **member** plays (`start-change`;
`commit-change` / `propose-change` / `review-change` / `merge-change`) are the building
blocks: never inject a sequence into one of its own members, and never let a consumer play
hand-roll issue/branch/PR/merge steps that duplicate a member — those come only via
injection.

**Durable model writes ride the end pipeline (D2b, #437).** A play that persists durable product-model artifacts (an Apply/Persist phase, an `apply_*.py` call) must declare `position: end` or `both` — or record an explicit `| position_exception | <reason> |` metadata row. `lint_play.py` fails the play otherwise.

### 4c — The cardinal rule: no unbacked recommendation
If the play **recommends, suggests, advises, or ranks** anything for the user, wire
[`standards/rules/no-unbacked-recommendation.md`](../../memory/standards/rules/no-unbacked-recommendation.md)
into it. Silence beats a wrong answer: every recommendation must trace to a source the
play can name, and where it cannot, the entry carries **no** recommendation — never a
default, a generic pointer, or another play's name. Write four things into the play:

- a **constraint** stating the rule, including that the count of un-recommendable entries
  is reported to the user (an invisible gap is the same failure one step later);
- a **failure condition** for an entry that was given a recommendation the play cannot back;
- a **step eval** that fails when any such entry carries one, when the substituted text
  names a play, or when the count is wrong or missing from the output;
- a **recovery** whose direction is to **strip** the recommendation — never to pick a
  different one. Absence is the correct answer, so recovery must not repair it into a guess.

`/focus` is the reference implementation (C12 / F10 / S8 / REC10). `lint_play.py`'s
`no-unbacked-recommendation` check fails any recommending play that does not carry this
wiring, so add it here rather than discover it at step 7.

### 5 — Evals
Generate the checks that prove the play works. Do not hand-wave these — each must be
objectively checkable:
- **Step evals (SE-n)** — one or more per **failure condition** and per
  *artifact-verifiable* constraint, placed right after the step they validate. Each
  cites its source: `SE-1 (F1/C3): <check>`.
- **Scenario evals (SCE-n)** — one per **success scenario**, sourced from that
  scenario's `measure`: `SCE-1 (S1 — <persona>): <check>`.
First **classify every constraint** into one of three buckets, because the bucket
decides how it's enforced:

| Bucket | Meaning | Enforced by |
|--------|---------|-------------|
| pre-flight | environmental precondition checkable before work | a pre-flight check |
| artifact-verifiable | observable property of an output | a step eval (SE-n) |
| structural | a rule about the play's own shape | the play structure itself |

### 6 — Compile the play
Write the play. If it has mechanical steps, write a **folder** — `<play-name>/SKILL.md` plus
`<play-name>/scripts/` for the scripts those steps call (and `references/` for anything it
reads); a pure-judgment play can be a single `SKILL.md`.

**Work only on workable ICE (ontology v3, #612).** When the play plans, breaks down or
builds from an ICE, copy [`references/check_ice_workable.py`](references/check_ice_workable.py)
unchanged to `scripts/` and call it on the node before that work. An ICE is workable only when
its node's spine `intents` names a confirmed business intent; a non-zero exit skips that node
(recorded in the run, never a halt) — the ICE stays as written. Writing an ICE is never gated
by this check.

**Add the stop condition (#464).** When the ICE has a "### Done means" section, write
`<play-name>/stop-condition.yaml` (schema `{name: stop-condition}`, `content.done` =
the clause list, unchanged) and copy
[`references/check_stop_condition.py`](references/check_stop_condition.py) unchanged to
`scripts/check_stop_condition.py`, the same way as `preflight.py` and `session_stamp.py`.
The Standard Play Close's Step C0 (play-close.md) checks the manifest at close: held allows
COMPLETED, unmet forces HALTED. A play whose ICE has no Done means gets no manifest
and closes as legacy (`stop_condition: not_defined`). Write each mechanical step's
script into `scripts/` and have that step run it by relative path; keep the script's logic
out of the step's prose. Copy the pre-flight script as step 4 says. Wire every step that dispatches to a subagent or skill as a
**JSON contract**: it names the input file paths and the output file path, the piece writes
to disk and returns the path, never inline data (see the worked example). The `SKILL.md` is
a **full compiled play** and must carry every required section — match the worked example in
[`references/compiled-play-example.md`](references/compiled-play-example.md):

Frontmatter (incl. the `position` field — D2) · Header · Compiled-From notice · Role +
agent boundaries · Pre-flight · Task DAG (a `TaskCreate` per step with `blockedBy`,
including any injected start/end sub-play steps per step 4b) · Workflow (steps grouped by
phase, each with owner, dependency, and its step evals; with the position-injected
`start-change` / end-sequence steps shown explicitly by name) · Scenario Validation ·
Recovery (one entry per failure condition) · Pause-and-Resume · Compilation Metadata.

Determinism rules for the output: steps are sequential with named phases (no runtime
reordering); the task DAG is fixed in the play; nothing is resolved "at runtime". Record a
content fingerprint of the intent + expectation in the metadata so later drift is
detectable and forces a fresh compile. Compute it mechanically — run
`shasum -a 256` over the intent + expectation text and paste the digest. Don't invent a
hash; the model can't compute one in its head, so a made-up fingerprint is worse than none.

### 7 — Verify coverage (run the linter)
Let the script count, not the model: hand-counting burns tokens and miscounts. Run
`scripts/lint_play.py` on the play you just wrote:

```
python3 scripts/lint_play.py <path-to-the-compiled-play>
```

It mechanically checks the wiring: every constraint/failure/scenario is covered by its
eval, exactly one recovery per failure, no orphan references, all required sections
present, and a real (non-placeholder) fingerprint. It prints a PASS/GAP report and exits
non-zero on any gap. For each GAP, fix the wiring — add the missing eval, write the
missing recovery, reclassify the constraint — and re-run until it's clean. The script
counts; the fix is still yours.

The linter checks an eval *exists*, not that it is *meaningful* — that part stays with
you. In particular it can't see one thing: every eval must be **executable from what
earlier steps actually capture**. If a step eval inspects data — a commit tip, a file
list, a prior value — that no earlier step recorded, the eval can't run. The fix is to
make the earlier step capture that input, not to weaken the eval.

## Review mode (read-only)

When asked to review an existing play, report gaps — **change nothing**.

Start with the linter; it does the mechanical half for free:

```
python3 scripts/lint_play.py <path-to-the-play>
```

That covers coverage, one-recovery-per-failure, orphan references, required sections, and
whether the fingerprint is real. Then add the judgment-only checks the script can't make:

- Every agent the play references actually exists, and every skill it names exists.
- Every agent passes the 11 principles in [`references/agent-audit.md`](references/agent-audit.md) (P1–P11).
- The fingerprint still *matches* the current intent + expectation — recompute it with
  `shasum -a 256` and compare. The linter only confirms the fingerprint is real, not that
  it's current.
- The evals are meaningful and executable, not merely present.

Present a short PASS/GAP table combining the linter's findings and yours, then stop. If
the user wants the gaps fixed, they correct the intent and re-run the skill (or use
`play-editor`).

## Hard rules

- Build only a play with structure: at least one constraint, one failure condition, and
  one success scenario. If any is missing, name what is missing and stop.
- Make every compiled play static and deterministic: its task graph and intent are fixed
  at compile time, not worked out at run time.
- Generate scenarios from the intent, and evals from the constraints, failures, and
  scenarios, so each one traces back to its source. Hand-written fillers break that trace.
- Give the generated play every required section. Full output is the point.
- Build plays the harness-led way: a step's mechanical work goes into a script in
  `scripts/` that the step runs; judgment stays in prose.
- Copy the pre-flight script into every play that checks its environment (step 4), and have
  the Pre-flight phase call it. Config, branch, issue, and change facts come from the
  script, not from the model. The Pre-flight table keeps only the halt policy.
- Wire every play as JSON-contract handoffs over files on disk: the play orchestrates,
  subagents gather context and verify, skills do the work. Each piece does only its own
  job and passes file paths, not inline data.
- In review mode, only read. Change no files.
- Honor the declared `position` (D2): inject `start-change` for `start`, the
  `commit-change → propose-change → review-change → merge-change` end sequence for `end`,
  both for `both`, nothing for `none`. Inject them as explicit named sub-play steps, one per
  sub-play, and only into consumer plays — member plays get none
  (`standards/rules/pipeline-position.md`).
- Wire the cardinal rule (`no-unbacked-recommendation.md`) into any play that recommends,
  suggests, advises, or ranks: constraint + failure condition + step eval + a recovery that
  strips the recommendation. A default offered where the play cannot back an answer is
  worse than the gap it hides.
- Classify constraints before generating evals. Run the linter (`scripts/lint_play.py`)
  and clear every gap before calling the play done.
- Wire the **Next** command. Every user-invocable compiled play needs an entry in
  `standards/rules/pipeline-next.md` (the successor map) — add one if the play is new —
  or a listing there under `meta_exempt`. The Standard Play Close (step C2) renders the
  play's Next line from that map (`**Next:** /<command> — <why>. Or run /next…`); the
  linter's `next-command (pipeline-next)` check fails a positioned play that is in
  neither the map nor the exempt list.
