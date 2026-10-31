# The Harness Standard

How Garura builds an agentic harness, why it is built that way, and how its parts are named. Garura
follows this standard in full, and it is written so that a team can take it and build its own harness
the same way. Each principle names the decision record (ADR) it comes from, in `docs/adr/`.

A **harness** is the set of parts that let agents do a team's work to a known standard: the plays
people run, the loops that run plays for them, the agents that gather context, the skills that do the
work, the scripts that do the mechanical parts, and the memory they all read.

## The parts

| Part | What it is | Who uses it |
|------|------------|-------------|
| Loop | A run of plays, in rounds, until its phase is done — the main thing people run | a person |
| Play | One repeatable workflow with checkpoints, written from its intent | a person or a loop |
| Agent | A domain expert that gathers context and writes it to files | a play |
| Skill | One capability that does the work and writes an artifact | an agent |
| Script | The mechanical part of a step: a fixed sequence with no judgment | a play or a skill |
| Memory | What every agent reads: short-term (one issue), project, and shared memory | agents, through one tool |

## The principles

### 1. People run loops; plays fade behind them

A loop runs its plays in rounds until its phase is complete, and asks a person only what no play or
memory can answer (ADR 029, ADR 041, ADR 045). People should mostly run loops, so loop names are the
shortest and clearest in the harness.

*Why:* every stop to ask a person costs their time. A loop that owns its questions asks once, with
context, instead of each play asking on its own.

### 2. Plays orchestrate, agents gather context, skills do the work

A play owns the order of steps. It hands each agent a contract of file paths, never the data itself.
The agent gathers context and calls skills, and each skill writes its artifact to disk (ADR 001,
ADR 005, ADR 016).

*Why:* each layer can be tested and replaced on its own, and the record of what happened is on disk,
not in a conversation.

### 3. Mechanical work is a script, judgment is a model

A fixed sequence, like cutting a branch, checking a file or counting gaps, runs as a script the step
calls. A model is used only where judgment is needed (ADR 025, #484).

*Why:* a script gives the same answer every time and costs nothing to run again. A model asked to do
mechanical work drifts, and it costs tokens on every run.

### 4. Every part is built from its intent

A play or loop is compiled from its ICE: the Intent (goal, constraints, failure conditions), the
Context, and the Expectation (scenarios, recovery, what done means). A change to what a part
guarantees is made in the ICE, and the part is compiled again. The compiled part records a
fingerprint of its ICE, so the two never drift apart unseen (ADR 027).

*Why:* the intent is what the team agreed. A part edited away from its intent stops doing what was
agreed, and nobody can see that it changed.

### 5. Build the eval first

The check that proves a change is done is built before the change, and it is run first against
today's code, where it must fail. The change is done when the check passes (Kapil, #734).

*Why:* a change judged by reading it is a change nobody proved. A check that never failed may not
check anything at all.

### 6. Nothing is blocked

Work never waits for a model to be complete. A plan can be built from a business intent before the
product model exists. The model grows as the plans are built, and missing links are warnings to fix
later, not stops (ontology v5, #722, #724).

*Why:* waiting for a complete model first is how work stops for days. The model fills in as work
shows what it needs.

### 7. The business intent is the root of all work

A person's business intent is tracked as an issue. Its plan breaks it into capabilities and
features, and each one holds the agent intent (ICE) an agent builds from. Bugs always sit under
a feature. A plan's ID is its business intent's issue number (ADR 031, ontology v5).

*Why:* every piece of work traces up to what a person asked for, and every defect shows which intent
it touches.

### 8. Branches follow the plan

When work on a plan starts, the plan gets its own branch, `plan/<plan-id>/base`. Each issue in the
plan is cut as a sub-branch from it, `plan/<plan-id>/<issue>-<slug>`, and lands back on it. When the
plan pauses, its branch merges into main, even with issues still open, and the branch is deleted;
when work on the plan starts again, a new plan branch is cut from main. The only reason to hold a
plan's branch off main is that it would break main; the plans a plan needs (`needs_plans`) do not
hold it off main either (ADR 060, decision 4). A one-off fix outside any plan branches from
main (#731, #673).

*Why:* a plan's work stays together while it runs, and no paused plan falls behind main.

### 9. Agents work only from memory

An agent answers from memory and from what it is given. When no memory answers, it raises a memory
update for a person to approve, and only then decides. It never answers from the model alone, and every
decision names the memory it came from (ADR 034, ADR 035, ADR 037).

*Why:* an answer with no source cannot be checked, and it repeats the model's guesses as if they were
the team's knowledge.

### 10. One name, one meaning

Every part is named by one rule: the verb first, then the object, with each verb holding one meaning.
No name is, or starts with, a built-in command of the coding tool. The full rules are in
`core/components/memory/standards/rules/naming.md`, and the component linter enforces them (ADR 046).

*Why:* people learn the words once and type them every day. One rule, with no exceptions to explain,
is the easiest to learn and to teach.

### 11. Installed parts never touch the source

Installed parts never touch `core/components/` or `core/tools/`: that is precompiled code. Once
Garura is installed, every play, loop, agent, skill, script, reference file, shared file and tool
reads, runs and names only the installed copy — `.claude/skills/`, `.claude/agents/`, the
installed `_shared/` folder, and `.garura/core/tools/<name>/`. A pointer in an installed file
points to another installed file, never to Garura's own `docs/`: the install never copies it, so
the text a part needs goes in the part (or its `reference/` folder), and a background pointer is
deleted. Repo layout is not a pointer: a project's own `docs/adr/`, the folders a review grounds
on (`docs/adr/**`, `docs/philosophy/**`) and a `docs/*` branch prefix stay. Memory is never read by a path: an agent fetches
it through the memory tool into the issue's short-term memory, and the skill reads that copy. A note
of origin ("source of truth: core/...", "canonical copy: ...") is deleted, not reworded.

The source-only parts are the exception, by design: `create-play`, `edit-play`, `create-loop`,
`edit-loop`, `install-garura`, `uninstall-garura`, `edit-ontology` and the skill
`author-product-ontology`; the dev tests; and the text that sorts the paths of the repo under review
(the changeset analysis of `commit-change`, the review playbooks' signal globs, the artifact-type
globs of the PR severity taxonomy, the trigger in `assess-pr`'s quality rules). The component
linter's rule `installed-paths/source-path` enforces this in both layouts (#860). ADR 055 records
this decision.

*Why:* a project that installs Garura has no `core/` folder. A part that reaches into the source
works only inside Garura's own repository, and fails everywhere else.

## Naming, in short

| Kind | Shape | Examples |
|------|-------|----------|
| Loop | `complete-<phase>` | `complete-discovery` |
| Play | `<verb>-<object>` | `discover-domains`, `shape-slice`, `build-epic`, `start-change` |
| Skill | `<verb>-<object>` | `author-slice`, `find-model-gaps`, `check-quality` |
| Agent | `<domain>-<role>` | `adr-keeper`, `quality-auditor` |

The lifecycle plays take the verb of the phase they move a product through:

| Phase | Verb |
|-------|------|
| Product → Intent | `discover` |
| Intent → Design | `shape` |
| Design → Code | `build` |
| Code → Validation | `validate` |
| Validation → Run | `release` |
| Run → Product | `learn` |

## How the standard is kept

- **The rule files:** `core/components/memory/standards/rules/naming.md` (for people) and
  `naming.yaml` (for the linter).
- **The checks:** run `node core/tools/lint-components/index.js --target core/components` from the
  repo root, and `python3 core/tools/naming/check_old_names.py` for any name changed by the rename map.
  In an installed project, run `node .garura/core/tools/lint-components/index.js --layout installed
  --target .claude` (give `--naming <naming.yaml>`, fetched through the memory tool, for the naming
  rules).
- **A change to the standard** is a decision: it goes through `/record-decision` as an ADR, and the
  rule files and this page change with it.
