# BI-10 (Standards, structure, settings and memory): what Garura has for its standards, building a harness, where things live, settings, memory and model choice

Research only, 2026-11-11, for #1021 (the chore that reorganises Garura's business intents around the phases and their
transitions). Nothing under `.garura/product/`, `.garura/core/`, `.claude/` or `core/`, on GitHub or in git was changed.
No memory update was raised or decided, and no decision trace was recorded, because the brief allowed this one file
only. Two read-only checks were run from the repository root on 2026-11-11: the component linter on the source, and the
old-name check. Memory was read only through the memory tool.

Scope: BI-10 only. Its page: Outcome "A project runs on one foundation. Everything is built on the ICE model with
written standards, the structure says where everything lives, settings hold what can be turned on or off, agents decide
from three tiers of memory, and each part runs on the right model. Teams can build their own harness on it." Proof:
"The checks hold every part to the standard.", "Every tool reads its settings.", "Nothing an agent decides from sits
outside memory." Must not: "Name a tracker in a play, skill or sub-agent, because they only know the tool."
(`intents/bi-10.md` lines 3, 10-12 and 14). The agreed six capabilities are in `capabilities.md` lines 110-115.

## In one paragraph

Garura has most of a foundation, built for its own repository and not yet for a team's. A written harness standard
holds eleven principles and the naming rules. Every play and the one loop is compiled from its ICE, except the six plays
that build and install Garura, which are written by hand; skills and sub-agents carry no ICE and follow written
standards for their kind. The checks exist (a component linter with eight rule families, a play linter, a loop linter
and an old-name check), but they run only inside the review of a change and only on what it changed, and today the
source fails 36 of them, all in the six hand-written plays and five older skills. ADR 066 set new names and five roles
on 2026-11-03; the rule files and the linter still hold the older names, and no issue files the rename. The builders
(/create-play, /edit-play, /create-loop, /edit-loop) write into Garura's own source folders, so a team can use them only
in a repository laid out like Garura's, and no part builds a skill or a sub-agent. Where things live is set across three
ADRs and two docs, and they disagree with the disk in several places, among them the plans folder, which no layout
lists. One settings file holds about 20 blocks; at least six are read by no script or only by a stale play, and seven
settings that approved pages need do not exist yet. The memory tool is live: three tiers, a person approves every
memory update, and every decision can keep its trace. But in this repository Garura memory is only the product model,
Phoenix memory differs from Garura's source in 60 places, nothing moves a page up a tier, and agents also decide from
files outside memory. Model choice is a fixed tier that each part names in its source: Claude Code keeps it on
sub-agents and drops it on skills, and nothing chooses a model by the job, measures speed or token cost per part, or is
planned to. Nothing in the model names BI-10 yet. About 120 lines on 84 approved pages of other intents already hand
work to these six. The old parts filed under the closed intent `bi-734` (the harness standard) are all built and
belong to Standards.

## Words used here

- **Business intent**: what a person wants, in their words. Written **BI-n** when it lives in the intents tracker
  (`intent-driven-ai/garura-intents`). A work issue is written **#n** and lives in `intent-driven-ai/garura`.
- **Part**: one play, loop, sub-agent, skill, script, shared file or tool. **Source** is where a part is written
  (`core/`); the **installed copy** is what an install lays in a project (`.claude/` and `.garura/core/`).
- **ICE source**: a play's or loop's `reference/ice.md` (Intent, Context, Expectation). The **compiled play** is the
  `SKILL.md` built from it, which records a **fingerprint** of the ICE (`docs/standards/harness-standard.md` lines
  50-55).
- **Settings file**: `core/config.yaml` in the source, laid in each project as `.garura/core/config.yaml` (ADR 040 §1).
- **Memory tiers**: **short-term memory** (one issue's folder under `.garura/project/issues/`), **Garura memory** (the
  project's own: `.garura/core/memory/`, then the product model), **Phoenix memory** (the global memory, its own git
  repository, one copy on each machine). A **memory update** is a draft answer a person approves before it is used. A
  **promotion** moves a page up a tier. A **trace** names the memory lines a decision rested on.
- **Model tier**: the `model:` hint in a part's source (`best`, `opus`, `sonnet`, `haiku`), folded to deep, standard or
  fast by the install (`install-garura/scripts/adapters/common.py` lines 11-22). **Effort** is how hard a model
  reasons, where a tool lets a part set it.
- **Gate**, **key**, **owed**, **pinned**, **machine wall**: as in the BI-9 stock-take (`bi-9-inventory/inventory.md`
  lines 51-56).
- **Paths**: a path that starts with an issue number, such as `1021/context/...`, is under `.garura/project/issues/`. A
  model page written as `<folder>/capability.md` is under `.garura/product/product-os/software-delivery-planning/`. Old
  parts live under `.garura/product/product-os/capabilities/` and `.../features/`. Phoenix memory files are named by
  their memory path and were read through the memory tool.

States: **Live** · **Live, out of step** (works, but disagrees with a later rule or decision) · **Designed only** (an ADR
or doc, no build) · **Planned only** (an open issue) · **Read by nothing** (a setting no script reads) · **Practice
only** (done by people, no part does it) · **Neither** (no build and no issue).

## 1. Standards

The agreed line: "Everything is built on the ICE model, with written standards for parts, sub-agents and naming, and
checks that hold them. (unique)" (`capabilities.md` line 110).

### 1.1 Built: the written harness standard

- `docs/standards/harness-standard.md` (170 lines). It is "written so that a team can take it and build its own harness
  the same way. Each principle names the decision record (ADR) it comes from" (lines 3-5).
- **The parts** (lines 13-20): loop, play, agent, skill, script, memory.
- **Eleven principles** (lines 24-138): people run loops; plays orchestrate, agents gather context, skills do the work;
  mechanical work is a script; every part is built from its intent; build the eval first; nothing is blocked; the
  business intent is the root of all work; branches follow the plan; agents work only from memory; one name, one
  meaning; installed parts never touch the source.
- **How it is kept** (lines 160-170): the rule files, the checks, and "A change to the standard is a decision: it goes
  through `/record-decision` as an ADR".
- Out of step:
  1. Loops are `complete-<phase>` (line 144). ADR 066 §3 replaced this with `loop-<from>-<to>` (ADR 066 line 77).
  2. The lifecycle verb table (lines 149-158) still names the phase "Product → Intent" and the verbs `discover`,
     `shape`, `build`, `validate`, `release`, `learn`. ADR 066 §1 gives the verbs to five roles and §8 names the second
     phase Spec (lines 59-69, 97-99).
  3. Tools are not a part. The parts table has no row for a tool (lines 13-20), while six tools live in
     `core/tools/` (lint-components, lint-play, memory, naming, plan, rebuild-eval), beside a review-tool prototype.
  4. Principle 5 names a person, not an ADR, as its source (line 63).
  5. Principle 6 "Nothing is blocked" speaks of the product model only (lines 68-75). #992 (the harness principle that
     a person is never stopped and every gate has a key) asks to widen it "to people and every gate"; not written yet.
- *State:* Live, out of step.

### 1.2 Built: the ICE model for plays and loops

- 31 of 37 plays have an ICE source, and so does the one loop (`core/components/loops/complete-discovery/reference/
  ice.md`). The six without one are /create-play, /edit-play, /create-loop, /edit-loop, /install-garura and
  /uninstall-garura (a listing of `core/components/plays/*/reference/ice.md`). `CLAUDE.md` says "`create-play` itself
  has no ICE source (it is the compiler bootstrap)".
- 13 of the 37 plays are marked stale: the old build chain, /refactor-code and the seven lens plays (#855, mark the
  old-chain plays stale, closed).
- Skills and sub-agents have no ICE: no skill has a `reference/ice.md`. A sub-agent is audited against eleven
  principles instead (`create-play/references/agent-audit.md` lines 1-13).
- The ICE kind of the product model (ontology version 15, each ICE on its own page) is BI-11's "Define what a product is
  made of", not this capability's (`intents/bi-11.md` line 3).
- *State:* Live for plays and loops; skills and sub-agents follow written standards only.

### 1.3 Built: written standards for each kind of part

| Standard | Where | State |
|---|---|---|
| Plays, loops, agents, skills, memory | `docs/components/plays.md`, `loops.md`, `agents.md`, `skills.md`, `memory.md` | Live; `plays.md` "lists six plays that are gone" (`capabilities.md` line 92) |
| Sub-agent audit, P1-P11 | `create-play/references/agent-audit.md` | Live, used by /create-play only |
| The close every play shares | `core/components/plays/_shared/play-close.md`; each play holds an anchor pair the linter checks | Live |
| The run every loop shares | `core/components/loops/_shared/loop-run.md` | Live |
| How an agent reads memory, and how it fails | `core/components/agents/_shared/memory-reading.md`, `failure-format.md`, `copy_memory.py` | Live |
| How a part asks a person | `core/components/skills/_shared/asking-a-person.md` (ADR 054) | Live for five parts only (section 1.6) |
| Rules in memory | 30 files under `core/components/memory/standards/rules/` | Live; 3 are in no memory tier (section 5.5) |
| Model choice for a skill | `docs/components/skills.md` lines 251-259 | Live, out of step (section 6.2) |

- *State:* Live, spread over five places.

### 1.4 Built: naming

- **The rules.** `core/components/memory/standards/rules/naming.md` (for people) and `naming.yaml` (for the linter):
  "a name that breaks a rule cannot land" (line 4); loops `complete-<phase>` (lines 32-34); the phase table still says
  "Product → Intent" (lines 39-46); "No name is, or starts with, a built-in command of Claude Code or Codex" (lines
  25-27). The rename map is `rename-map.yaml` (82 lines).
- **The decisions.** ADR 046 (one naming standard) superseded ADR 006 and ADR 018 (both read "superseded by ADR 046",
  line 3 of each). ADR 066 (accepted 2026-11-03) gives the play verbs to five roles, names loops `loop-<from>-<to>`,
  lets a name start with a tool's command, drops two design plays and names the second phase Spec (lines 59-99). The
  agreed names are in `1021/context/names.md` lines 5-39.
- **Not applied.** "Nothing is renamed by this decision" (ADR 066 line 21). "Until the rename lands, the naming files
  and the linter keep today's rules, so they disagree with this record." (line 131). Skills and agents "keep their
  verbs for now", and the verb `remove` stays undecided, so `remove-model-part` and `remove-plan` "fail the check in
  any project that reads Phoenix memory's copy" (lines 29-31).
- **No issue files the rename.** ADR 066 "Work This Creates" asks for "The rename, as one change" (line 149). A search
  of open issues finds none; #1021 (the reorganisation) lists "the Intent-to-Spec rename in the standard" under "Not in
  this change".
- #1015 (record the harness roles feature in the product model) asks for a feature page under "The harness standard,
  written down", "beside the naming rules (#736) and the harness principles (#737)", with the product owner's words of
  2026-10-31: "The harness for the standard as a business intent for the five rules is correct." No such page exists
  (a read of `_spine.yaml`).
- *State:* Live for ADR 046; Designed only for ADR 066.

### 1.5 Built: the checks

| Check | What it holds | Where |
|---|---|---|
| Component linter | Eight rule families: structural, semantic, cross-reference, naming, asking-a-person, shared-scripts, installed-paths, memory-reading | `core/tools/lint-components/index.js` lines 7-14; seven test files in `test/`; the semantic and cross-reference rules have none |
| Play linter | Coverage of constraints, failures and scenarios; one recovery per failure; no orphans; a real fingerprint | `core/tools/lint-play/lint_play.py` lines 22-35 |
| Loop linter | The same for a loop, and "the fingerprint is the sha256 of reference/ice.md as it is now" | `create-loop/scripts/lint_loop.py` lines 19, 180-190 |
| Old-name check | No old name left, from the rename map | `core/tools/naming/check_old_names.py` lines 1-25 |

What the checks show today (run 2026-11-11, from the repository root):

- **Component linter on the source: 36 errors, 1 warning.** 16 missing sections and 6 missing play-close anchors are
  in the six hand-written plays (/create-play, /edit-play, /create-loop, /edit-loop, /install-garura,
  /uninstall-garura); 8 missing `model` and `allowed-tools` lines are in four skills (`check-quality`,
  `find-matching-issues`, `merge-pr`, `open-pr`); three missing sections are in `propose-kb-node` and three more in
  `check-quality`; the warning is a mixed spelling in /list-focus-issues. No naming, memory or installed-path error.
- **Old-name check: exit 1, 12 hits of 9 old names**, in ADR 062 line 64 and `docs/philosophy/intent-and-adlc.md` lines
  62, 63, 295, 309, 318, 440 and 452.

What the checks do not do:

- **They run only on what a change touched.** /check-change runs both linters, and "Only a violation whose file is in
  `changed_paths` becomes a finding; count the others, and record the count as 'there before'"
  (`check-change/SKILL.md` lines 194-216). No CI runs them: the one workflow, `.github/workflows/release.yml`, only
  creates a release.
- **The play linter does not compare the fingerprint to the ICE.** It checks only that the fingerprint is "not a
  placeholder" (`lint_play.py` lines 310-317). The loop linter checks that it matches (`lint_loop.py` lines 180-190).
  So a compiled play can drift from its ICE unseen, against principle 4 ("so the two never drift apart unseen",
  harness standard line 55).
- **An installed project checks names against Phoenix memory's copy**, fetched through the memory tool (harness
  standard lines 166-168). Today Phoenix memory's `naming.md` and `naming.yaml` differ from the source (section 5.5).
- **The Must not has no check.** No rule fails a part that names a tracker. #1023 (an Agent-work tool reads the tracker
  setting, under BI-9) counts "3 plays, 11 skills and 3 agents hold `gh` commands, and 10 plays, 6 skills and 1 agent
  name GitHub".
- **The layer rule has no check.** #856 (Garura's parts compose; no skill names a play or another skill) found "36 of
  96 skills name a play" on 2026-10-24.
- **Some checks have no tests.** #507 (unit-test the scoped write guard; "14 copies run unguarded") and #508 (unit-test
  the direct-model-write lint checks), both under #511 (component quality and governance).
- *State:* Live, partial cover.

### 1.6 Built in part: the rules every part follows

- **Asking a person.** One shared file, but the linter checks only the parts on its list: two plays (`edit-ontology`,
  `shape-slice`) and three skills (`asking-a-person.js` lines 21-23). #999 (the rule for asking a person is an engine
  rule in core) wants every part bound without naming it.
- **Staying on scope.** #1004 (a finding outside the scope is recorded and the work moves on): "This issue only records
  the rule." Not written.
- **The way of working.** `.garura/user-provided/managing-work.md` is read as rules, but "user-provided is what user
  gave.. that is evidence not to be read as rule" (the product owner, 2026-10-29, in #952, Garura's way of working is
  defined as engine rules and settings). Not sorted.
- **The voice rule.** `standards/rules/user-facing-voice.md` is still in the source after `CLAUDE.md` dropped the rule
  (#774, the long voice rule file is still in memory).
- **The guidance Claude Code reads in this repository.** #768 (guidance that Claude Code reads in this repo), #769
  (CLAUDE.md says each rule once and right) and #770 (merge the installer's memory rule into CLAUDE.md). `CLAUDE.md`
  line 172 still says "49 ADRs, plus two superseded"; there are 64 numbered ADRs.
- *State:* Live in part; the rest Planned only.

### 1.7 Planned only

- #992 (every gate has a key; write the principle into the harness standard), under #735 (the harness standard,
  written down, closed). BI-9's approved page takes the gate work and leaves the writing here (section 7.1).
- #856 (no skill names a play or another skill; a linter rule fails one).
- #952 (the way of working as engine rules and settings), #999 (the rule for asking a person as an engine rule) and
  #1004 (staying on scope as an engine rule); section 1.6.
- #934 (findings and defects get one severity, P1 to P4, in three layers), under #967 (a team builds a harness from a
  written architecture). BI-9's approved page says "#934 holds them, under Standards, structure, settings and memory in
  the tracker" (`track-execution/fn-record-defect-under-story/feature.md` line 53).
- #936 (the naming tools are tested on a name removed with no successor), under #741 (closed).
- #511 (component quality and governance) with #507 (unit-test the scoped write guard), #508 (unit-test the
  direct-model-write lint checks), #458 (align agent contract schemas with real dispatch;
  deprecate orphan agents), #423 (repo-orchestrator stops mid-batch) and #578 (components and docs still describe
  /next scripts).
- #620 (tools become a first-class Garura component), under BI-10 directly.
- #768 (guidance that Claude Code reads in this repo), #769 (CLAUDE.md says each rule once and right), #770 (merge the
  installer's memory rule into CLAUDE.md) and #774 (the voice rule file goes); section 1.6. #839 (review every Claude
  memory for this project) sits under #768.
- #1015 (the harness roles feature).

### 1.8 Neither

- The rename to ADR 066's names (no issue).
- A standard for a tool as a part, beyond the direction of #620 (tools become a first-class component).
- A check that no part names a tracker.
- A verb list for skills and agents (ADR 066 line 150: "A later decision gives skills and agents their own list").

## 2. Build your own harness

The agreed line: "You can keep building your harness with your own plays, loops and sub-agents, in a consistent way.
(unique)" (`capabilities.md` line 111).

### 2.1 Built: the four builders

| Builder | What it does | Where |
|---|---|---|
| `/create-play` | Interviews for the intent, generates the expectation, works out the scripts, skills and sub-agents the play needs, picks a workflow shape, writes the evals and compiles the play; a read-only review mode finds gaps | `create-play/SKILL.md` lines 1-15, 100-116 (463 lines) |
| `/edit-play` | Changes a play by editing its ICE and compiling again | `edit-play/SKILL.md` lines 1-24 (168 lines) |
| `/create-loop` | Builds a loop from its ICE: its plays, its first questions, its checker and runner settings, how it ends | `create-loop/SKILL.md` lines 1-12 (205 lines) |
| `/edit-loop` | Changes a loop through its ICE | `edit-loop/SKILL.md` (98 lines) |

- **Consistency is built in.** /create-play copies the shared scripts unchanged into each play (pre-flight, the
  code-host adapter, the branch and pull-request scripts, the grounding linter), and "Because create-play writes these
  scripts into the play, a rebuild brings them back" (lines 215-271). The linter fails a copy that differs
  (`shared-scripts.js`). It wires the start and end of the change path by the play's position (lines 272-292), and
  points each play at the shared close (line 354).
- **A sub-agent is audited, not built.** "For each, note whether it already exists or must be created"; every agent is
  audited against P1-P11 (lines 177-182).
- **A way past for approvals.** Each builder asks for a typed yes; "If you're running it without a reachable human ...
  record that approval was assumed, and proceed" (`create-play/SKILL.md` lines 120-123; `create-loop/SKILL.md` lines
  70-72; `edit-loop/SKILL.md` lines 27-28).
- *State:* Live, in Garura's own repository.

### 2.2 Built in part: building outside Garura's own source

- **The builders read and write Garura's source folders.** /create-loop "writes the compiled loop into
  core/components/loops/<loop>/" (lines 7-8, 32); /create-play reads its rules by a source path
  (`../../memory/standards/rules/pipeline-position.md`, line 275) and runs its linter with
  `--next-map core/components/memory/standards/rules/pipeline-next.md` (line 388).
- **By design.** The harness standard names them source-only exceptions: "The source-only parts are the exception, by
  design: `create-play`, `edit-play`, `create-loop`, `edit-loop`, `install-garura`, `uninstall-garura`, `edit-ontology`
  and the skill `author-product-ontology`" (lines 129-131; ADR 055 §5).
- **A product project never gets them.** "A product project's ADLC has no use for them, so no target ever receives
  them under `full`" (`install-garura/scripts/install.py` lines 210-215).
- **A harness repository gets them.** The `harness` scope lays the four builders, the change plays and the plan plays,
  and "a harness repo builds loops but runs none: no product loop installs there" (lines 220-265).
- So a team can build its own plays and loops only in a repository laid out like Garura's source. Whether a team
  outside Garura has done so: not confirmed.
- The approved BI-7 page agrees on the owner: "Building a harness with Garura's build plays. Build your own harness, in
  Standards, structure, settings and memory, owns it." (`install-into-project/fn-choose-parts/feature.md` line 56).
- *State:* Live for Garura and harness repositories laid out like it.

### 2.3 Not built: building a sub-agent or a skill

- No Garura part builds a sub-agent or a skill. There is no builder for either among the 37 plays. /create-play notes
  what "must be created" and stops there (line 177).
- The line names sub-agents ("your own plays, loops and sub-agents") but not skills, which is where the work is done
  ("skills do the work", harness standard lines 33-37).
- *State:* Neither.

### 2.4 Planned only

- #699 (loop builders and the loop linter check the loop principles: a checkable goal, what starts the loop, what it
  sees, a record across rounds, a person who reads the output), under BI-10.
- #893 (an agent cannot do a play's work without the play: guardrails laid by the install). Its first part is "A run
  marker. Each play writes a 'this play is running' record when it starts and clears it at its close." Not decided:
  "how a person overrides it on purpose".
- #933 (a team building a Phoenix harness has an architecture memory to build and review against): "the parts and what
  each may do", "what calls what", "the folders: the source, the installed copy, short-term memory", under #967 (a team builds a harness
  from a written architecture).
- #910 (/create-play builds an edit option into each new play that writes the model or work items), under #962 (BI-11).

### 2.5 Neither

- A starter for a new harness repository, or a guide to building one. `docs/usage/` holds only a README and one play
  page (`docs/usage/plays/create-pr.md`).
- The builders on the installed layout.
- A builder for a tool.

## 3. Structure

The agreed line: "Where everything lives, in source and once deployed." (`capabilities.md` line 112).

### 3.1 Built: the source layout

- `CLAUDE.md` "Architecture" (lines 9-30): agents, skills, plays, loops and memory under `core/components/`; tools
  under `core/tools/`; components laid in a project's `.claude/`; memory as a machine-wide folder.
- The settings file names the source folders (`core/config.yaml` lines 33-38).
- *State:* Live.

### 3.2 Built: the installed layout

- Claude Code: each sub-agent to `.claude/agents/<id>.md`; each skill, play and loop to `.claude/skills/<id>/`
  (`adapters/claude.py` lines 4-9); one shared folder beside them, from the plays', loops', skills' and agents'
  `_shared/` (`adapters/common.py` lines 52-60).
- Tools to `.garura/core/tools/<name>/` (ADR 055 §3); the memory guide where the tool loads it for every agent
  (`core/tools/memory/README.md` lines 15-17; in this repository `.claude/rules/garura-memory.md`, ignored by git,
  `.gitignore` line 18); an install record, `install-manifest.json`.
- Each other tool's layout is BI-7's adapters' work (`support-coding-tools/capability.md` line 63 gives "where each part
  lives once laid" to Structure).
- *State:* Live for Claude Code.

### 3.3 Built: the `.garura/` layout, and where it disagrees with the disk

- **Written in three places.** ADR 017 §1 (the folder whitelist), as amended by ADR 039 §5 (lines 74-96);
  `docs/components/memory.md` lines 81-105; the glossary's Whitelist row (`core/grounding/glossary.md` line 107).
  Short-term memory holds "only 5 structure keys": specs, evidence, checkpoint, context, review (`core/config.yaml`
  lines 64-82).
- **Where the disk disagrees** (a listing of `.garura/` on 2026-11-11):
  1. **The plans folder.** `.garura/project/plans/` is in the settings (`core/config.yaml` lines 68-71) and holds seven
     plan files, but none of the three layout lists names it.
  2. **Garura memory and git.** ADR 039: "`.garura/core/memory/` is Garura memory. It is kept in git, not ignored." (line
     94), and its Affects line says the `.gitignore` line "goes" (line 10). `.gitignore` line 152 still ignores it, and
     `CLAUDE.md` line 28 says it is ignored. The folder does not exist in this repository.
  3. **`engine-state.json`.** Listed in `core/` by ADR 039 §5, present in `.garura/core/`, and read or written by no
     script in `core/` or `installer/` (a search).
  4. **The old global gate ledger.** `.garura/core/gate-evals.jsonl` is still there (#943, gate records move into each
     issue's evidence folder).
  5. **Folders that are not issues.** Short-term memory also holds `_adr`, `_plans`, `_start` and `capture-report`, and
     an issue's folder holds a `status/` folder, none of them among the five keys.
  6. **The enforcer is gone.** Phoenix memory's `standards/rules/product.md` line 71: "ADR 017 whitelist. `write-evidence`
     skill validates every write path". No such skill exists among the 74 skills.
  7. **The machine-wide copy.** The install still writes a machine-wide copy of all memory in the home folder: "It stops
     when the memory tool is fully live and Phoenix memory is the home of memory." (ADR 055 §8, lines 71-73).
- *State:* Live, out of step.

### 3.4 Built in part: where a run's records go

- Every issue keeps its own records (the five keys above), and each issue its own gate ledger (`core/config.yaml` line
  222).
- Plays write a person's home-folder path into the records they commit: #982 (plays write a home-folder path into run
  records, and nothing stops the push), under BI-10; #914 (run records carry the person's home-folder paths), under
  #672 (BI-4's side).
- *State:* Live, out of step.

### 3.5 Planned only

- #969 (every run's records are kept in the evidence folder of its issue), under BI-10, with #943 (gate records live in
  the evidence folder of the issue that made them).
- #620 (tools become a first-class component, in `core/components/tools/`).
- #415 (reorganise `core/components` into the harness layout), under #511 (component quality and governance). Its plan names six harnesses (`p2s` to `r2p`)
  and a standard in another repository; it predates ADR 066. Stale.
- #946 (every settings file other than `config.yaml` lives in one config folder) — section 4.6.

### 3.6 Neither

- One written map of where every part lives, in the source and once installed. The nearest are `CLAUDE.md`
  "Architecture", `docs/components/memory.md` and harness standard principle 11.
- A check that the `.garura/` layout holds.

## 4. Settings

The agreed line: "Everything that can be turned on or off lives in settings." (`capabilities.md` line 113).

### 4.1 Built: one settings file, laid in each project

- The source is `core/config.yaml` (223 lines); each project reads its own installed copy (ADR 040 §1-§2).

| Block | What it holds | Read by |
|---|---|---|
| `platform`, `github` (lines 7-12) | The code host | The code-host adapter; `owner` names a personal account (BI-9 stock-take section 3.1) |
| `trackers` (lines 14-23) | Which tracker holds intents and which holds work | Read by nothing (only a docstring, `track-plan-changes/scripts/tracker.py` line 4) |
| `components`, `claude` (lines 33-43) | Source and installed folders | Not confirmed |
| `global-claude`, `factory`, `global-factory` (lines 45-58) | Old install targets | Read by nothing (a search; #947, settings named for gone plays and tools) |
| `ltm` (lines 60-62) | The old memory folder | Passed on by pre-flight as `ltm_project_target` (`create-play/references/preflight.py` line 145); the folder does not exist |
| `plans`, `stm` (lines 68-82) | Plans and short-term memory | The plays' pre-flight and the plan scripts |
| `start-change.worktree` (lines 84-86) | A worktree on start | `start-change/scripts/preflight.py` line 150 |
| `implement.plan-tracking` (lines 88-93) | Publish a build plan | Only the stale /build-epic (`check_ready_epic.py` lines 66-73) |
| `review-pr` (lines 95-102) | Review bypass and reviewers | Named in /check-change's text (lines 313, 352); "read by no play's code" (`capabilities.md` line 92) |
| `craft-ice.hitl` (lines 104-111) | A human checkpoint | Read by nothing; no play of that name |
| `shape-slice.grill-tier` (lines 113-117) | How many questions a slice may ask | `shape-slice/scripts/grill_budget.py` line 39 |
| `loops` (lines 119-138) | Each loop's runner, rounds and checker | `complete-discovery/scripts/loop_preflight.py` lines 101, 134-135 |
| `evidence` (lines 140-144) | Whether a run keeps its evidence | The plays' pre-flight |
| `grounding-eval` (lines 146-158) | The judge's model and gate | Named in /discover-capabilities' text (lines 98, 388); a script reader not confirmed |
| `product` (lines 179-188) | The model's place and the ontology's | The plays' pre-flight |
| `gates` (lines 190-223) | Every checkpoint's switch, the learned policy | The play's own text (18 plays name `gates.plays`); `gate_eval.py` for the ledger |

- So at least six blocks are read by no script or only by a stale play.
- *State:* Live, out of step.

### 4.2 Built: the gate settings

- Three kinds: pinned ("Always fires. No config value, policy, or ledger can turn it off."), conditional (learned per
  project) and off ("the skip is recorded") (Phoenix memory `standards/rules/gate-config.md` lines 10-14).
- Resolution, first match wins, and where the ledger and the policy live (lines 34-60).
- **The learned policy has never been written.** `gates.conditional.policy` names `.garura/core/gate-policy.yaml`
  (`core/config.yaml` line 223); the file is not there, and #946 (every settings file in one
  folder, each setting naming who reads it) says it "has never been written".
- **The pinned list names gone plays**: grill, launch, learn and deploy (gate-config lines 98-104).
- BI-9's approved pages take the way past and leave the settings here (section 7.1).
- *State:* Live, out of step.

### 4.3 Built: the evidence setting

- `evidence.record: false`, with the one loop always on (`core/config.yaml` lines 140-144). A skipped checkpoint is
  recorded only in the evidence file, so with this setting off it is not recorded (BI-9 stock-take section 5).
- *State:* Live.

### 4.4 Built in part: the installed copy in this repository

- `.garura/core/config.yaml` has 181 lines against the source's 223, with no `loops`, `plans` or `trackers` block.
- It has two `product:` keys (lines 70 and 141). ADR 040 fixed this in the source: "the old file had two `product:`
  keys, and the second silently replaced the first" (ADR 040 line 8).
- It still says `review-change: off` (line 168), so the review's checkpoint is on here (#772, the install keeps old
  play names in the project settings, under #748 (an install removes old names, closed), BI-7's side).
- It still names the global ledger (line 180; #943, gate records in each issue's evidence folder).
- `standards.pr-severity-taxonomy` (lines 74-75) and `ltm.project-target` (line 50) point into `.garura/core/memory/`,
  which does not exist.
- An upgrade keeps the team's settings file whole and brings no new settings (BI-7's
  `upgrade-project/capability.md` line 39).
- *State:* Live, out of step.

### 4.5 Settings that approved pages need, and that do not exist

| Setting | Asked for by | Exists |
|---|---|---|
| The test model: which model or service writes and runs the tests | `build-work-test-first/capability.md` lines 13-14, 35; `fix-defects-test-first/capability.md` line 72 | No ("The test model setting does not exist", line 35) |
| Sample code, design style, screen design | `design-work/capability.md` lines 11-14, 32 | No ("None of the three settings exists", line 32) |
| Which kinds of change may go ahead on their own | `build-or-update-product/capability.md` lines 20, 46; `fn-act-on-its-own/feature.md` line 5 | No |
| Each connection to an outside tool, with where its key is kept | `connect-use-and-market/capability.md` lines 6, 28 | No ("No setting names one", line 28) |
| How many review rounds before a finding goes to a person | `check-code-against-standards/capability.md` line 86; `test-security/capability.md` line 76; `test-accessibility/capability.md` line 84 | No |
| Who decides the review | `check-code-against-standards/capability.md` line 81 | Yes, as `gates.plays.check-change` |
| The question tier, the loop settings, the gate settings, the trackers | `orchestrate-agent-work/fn-795/feature.md` line 70; `run-plays-as-loops/capability.md` line 70; `give-every-gate-a-way-past/capability.md` line 68; `track-execution/capability.md` line 69 | Yes |

- Approved pages already read "turned on or off" widely: "A setting is a choice a team turns on or off, or picks, once
  for the project" (`design-work/capability.md` line 11; `build-work-test-first/capability.md` line 13).

### 4.6 Planned only

- #946 (every settings file other than `config.yaml` lives in one config folder, and each setting names who reads it):
  "A check fails on a key nobody reads, and on a play's setting whose play no longer exists." It sits under #513
  (install and distribution), which sits under BI-7.
- #947 (settings named for plays and tools that are gone are renamed or removed), under #946 (the settings folder).
- #943 (gate records in each issue's evidence folder).
- #952 (sort the way of working into engine rules and settings).

### 4.7 Neither

- A way to see or change the settings other than editing the file.
- A check of a setting's value (its kind, its allowed values).
- "Every tool reads its settings" (BI-10 proof): the memory tool reads its own `settings.json` (`core/tools/memory/
  README.md` lines 33-37); the plan tool takes its folder from a flag with a fixed default (`core/tools/plan/plan.py`
  line 34); the component linter takes the naming rules from a flag (`index.js`); no tool reads `trackers`.

## 5. Memory

The agreed line: "Agents decide from three tiers of memory (Phoenix global, Garura project, short-term), and people
control what enters them." (`capabilities.md` line 114).

### 5.1 Built: the memory tool

- `core/tools/memory/` (contract version 5): `health`, `find`, `search`, `read`, `propose`, `updates`, `decide`,
  `apply`, `cite`, `citations` (README lines 1-12).
- Three tiers, looked up short-term, then Garura, then Phoenix memory, stopping at the first that answers (README lines
  82-90); "A read of another issue's short-term path is refused" (lines 93-95).
- Phoenix memory "arrives on first use", "is read only at its approved version", and "Nothing is copied" (lines 50-63).
  "No command writes Garura or Phoenix memory" (lines 64-66).
- `health` today: all three tiers reachable; Phoenix memory at version `b2e40bff2131`.
- Decided in ADR 035 to ADR 039. Built under #653 (agents work only from memory, through one memory tool; open, ten of
  its eleven children closed).
- *State:* Live.

### 5.2 Built: a person decides what enters

- **Memory updates.** `propose` raises one in the issue's short-term memory; `decide` records "a person's word ...
  approve or reject, who, their exact reply, and where they decided"; "Only a person decides, one update at a time"
  (README line 136); `apply` refuses an update no one approved.
- **Use.** 13 applied, 5 waiting, 1 rejected (`memory.py updates`, 2026-11-11). Three of the waiting five date from
  2026-10-24 and ask where the rule for asking a person lives, which ADR 054 later settled as a shared file. Nothing
  reminds anyone of a waiting update.
- **Traces.** `cite` records each decision with its sources and their fingerprints; `citations --check` names each
  source that changed. Open: #852 (a decision that a later decision replaced cannot be marked, so the check never
  clears), under #659 (closed).
- *State:* Live.

### 5.3 Built in part: every agent reads memory through the tool

- One shared protocol (`agents/_shared/memory-reading.md`) and copy script; the linter's `memory-reading/*` and
  `installed-paths/source-path` rules fail a part that skips the protocol or names a memory folder. Today's source run
  shows no such error.
- #663 (every agent and skill reads memory only through the tool, and lint fails any that names a memory path), under
  #653 (the memory system), is still open; whether all of its Done-when items are met: not confirmed.
- The rule for agents reaches every session through the installed memory guide (`.claude/rules/garura-memory.md`).
- *State:* Live.

### 5.4 Built in part: Garura memory

- The tool reads Garura memory as `core/memory`, then the product model (README line 76).
- In this repository `.garura/core/memory/` does not exist, so Garura memory is only the product model. #942 (a
  project's memory can be managed): "In this repository that folder was removed on 2026-10-26".
- Building a project's own Garura memory is `initialize`, which is not built and is BI-7's ("Set a project up after the
  install"); approved BI-7 pages leave "what may enter each memory tier, and promotion" here
  (`initialize/capability.md` line 58).
- *State:* Live in part.

### 5.5 Built in part: Phoenix memory, and how far it is behind

- Its own repository, read at the approved commit. Its README: "Fed by promotion ... A person approves every
  promotion. Every change here is a commit." and "Pulled, never copied whole" (Phoenix memory `README.md` lines 6-7).
- **It differs from Garura's source in 60 places today** (a file-by-file compare through the memory tool, 2026-11-11):
  42 pages differ, among them `naming.md`, `naming.yaml`, `self-review.md`, `run-status.md` and the slice and lens
  schemas; three are in the source only (`play-orchestration.md`, `play-patterns.md`, `user-questions.md`); 15 are in
  Phoenix memory only. This is the count #949 (Phoenix memory has fallen behind Garura's source in 60 places) gave on
  2026-10-28. The ontology is at version 15 in both, so #868's example (the ontology in no tier) no longer holds.
- **Promotion is by hand.** No play or tool command moves a page up a tier. The memory tool names "/learn-memory and
  /promote-memory plays" (`updates.py` lines 7-8); the glossary: "`/promote-memory` (not built yet)" (line 41).
- *State:* Live, out of step.

### 5.6 What agents decide from that sits outside the tiers

The proof says "Nothing an agent decides from sits outside memory." Today agents also read:

1. **The machine-wide copy of all memory**, still laid by the install (ADR 055 §8). Its retirement is handed to Memory
   (`install-into-project/fn-take-out/feature.md` line 55).
2. **Claude Code's own memory for this project**, outside the repository (#839, review every Claude memory, under #768,
   the guidance Claude Code reads).
3. **Rules in the repository**: `CLAUDE.md`, `.claude/rules/`, `managing-work.md` (#952, the way of working), and the rule for asking a
   person, kept as a shared file on purpose: "it is not memory and not a global rule" (#854, the move of the rule into a shared file,
   quoted in #999, the rule for asking a person as an engine rule).
4. **Each part's own reference files** (its ICE, templates and maps), which are the part itself.
- The product owner on 2026-10-29: "memory is a cartridge … you can't put rules into a cartridge" (#942, a project's memory can be
  managed, item 5; #952, the way of working, "Rules are not memory"). BI-10's page, confirmed on 2026-11-02, says nothing an agent decides from sits outside
  memory. Open question 3.

### 5.7 Planned only

- #653 (the memory system) with #663 (every part reads memory only through the tool), and #664 (the review tool's Memory
  and ADRs section, under #681, Argus the review tool, BI-8's).
- #942 (a project's memory can be managed): every change shows in the review with the memory checks; "A page that is out
  of date, or whose source changed, is named before an agent uses it"; "No linters and no rubric for memory" (found so
  far, item 3).
- #966 (Phoenix memory stays in step with Garura's source, versioned per release) with #921 (the same, with its own
  release notes), #949 (the 60 places) and #868 (current standards in no memory tier).
- #883 (all memory in Garura's source is Phoenix memory: one Phoenix install per machine, then `initialize`), under
  #862 (BI-7's initialize). The approved page gives the Phoenix install to Memory (`initialize/fn-883/feature.md` line
  55).
- #852 (replaced decisions in the trace check); #839 (Claude Code's own memory).
- #611 (decide the Learn loop's recipe: "learn into Garura memory, promote to Phoenix memory, find drift"), under BI-6.

### 5.8 Neither

- A play or command that promotes a page on a person's yes. BI-6's list left "choosing and promoting learnings to Garura
  or Phoenix memory" to "the review of Memory" (`capabilities.md` line 68).
- A reminder or an end date for a waiting memory update.

## 6. Intelligent model routing

The agreed line: "Each part runs on the right model and effort for its job, for speed and token cost, on each harness
that supports it. Also serves Install and distribute. (unique)" (`capabilities.md` line 115).

### 6.1 Built: each part names a tier in its source

| Kind | Name a tier | The tiers | Name an effort |
|---|---|---|---|
| Sub-agents | 17 of 17 | 12 `sonnet`, 4 `opus` (`adr-keeper`, `business-intent-keeper`, `product-os-keeper`, `test-engineer`), 1 `haiku` (`template-manager`) | 4: `business-intent-keeper` high, `knowledge-builder` high, `prototype-reader` medium, `result-checker` medium |
| Skills | 70 of 74 | 39 `sonnet`, 23 `opus`, 4 `best`, 4 `haiku` | none |
| Plays | 4 of 37 | 4 `best` (the four builders); `shape-slice` has an empty `model:` line | none |
| Loops | 0 of 1 | — | none |

(A read of each part's front lines, 2026-11-11.)

- **The written rule** is for skills only: "`haiku` | Execution-only skills ... `sonnet` | Analysis skills ... `opus` |
  Judgment-heavy authoring" (`docs/components/skills.md` lines 251-259). The agents doc lists each agent's model
  (`docs/components/agents.md` line 60 and the rows after it). The linter requires a `model` line on every source
  skill (`structural.js` lines 66-69).
- **Some choices give their reason.** `prototype-reader`: "High-volume, low-judgment work — runs on Sonnet at medium
  effort" (its line 5). ADR 042: "The knowledge plays' agent runs on Sonnet; Kickoff run 6's search-and-build step cost
  $4.72 on Opus." (lines 100-102).
- *State:* Live, set by hand, part by part.

### 6.2 Built in part: the tier reaches the coding tool

- The install folds each tier to deep, standard or fast (`adapters/common.py` lines 29-49). Claude Code keeps it on
  each sub-agent and drops it on each skill, play and loop: "A Claude skill has no model field — the agent that invokes
  the skill carries the model." (`adapters/claude.py` lines 11-16). The adapter rewrites only the `model` line (lines
  42-56), so the four agents' `effort` reaches Claude Code as written.
- **Claude Code does take a model and an effort on a skill.** The approved memory update mu-20261110-001: "A skill can
  name its model: the skill frontmatter has `model` (for the rest of the current turn) and `effort`", and a sub-agent
  takes `effort` (`1021/context/bi-7-capability-3/answers/coding-tool-claude-code.md` lines 7, 9). So 70 skills name a
  tier that never takes effect, and `docs/components/skills.md` says they choose one.
- The Codex adapter mapped each tier to a model and an effort ("deep": `xhigh`, "standard": `medium`, "fast": `low`,
  `adapters/codex.py` lines 45-51); it is stopped (#863, Codex projects get an install built for Codex).
- Carrying the tier is BI-7's: "The tier is carried, never chosen." (`support-coding-tools/fn-map-model-tier/feature.md`
  line 36), with its own status: "Effort is not carried: the fold reads only the tier" (line 24).
- *State:* Live in part.

### 6.3 Built: a step on another model, chosen by a setting

- The loop's checker: "A subagent checker must name its model, one other than the session's" (`core/config.yaml` lines
  119-123); the loop stops at pre-flight when it is not set (`loop_preflight.py` lines 134-135).
- The grounding judge: `model: inherit  # inherit | a claude model id` (`core/config.yaml` line 157).
- The rebuild eval: "Every agent runs on Sonnet 5.5 at high effort ... The plays under test run on their own models"
  (`core/tools/rebuild-eval/README.md` lines 41-42), and it records each agent's cost (`run_eval.py` lines 17, 74).
- *State:* Live, one setting for each step.

### 6.4 Not built

- **Choosing by the job.** Nothing picks a model or an effort from what a step must do; each part keeps the tier its
  maker wrote.
- **Knowing the cost.** No play or loop records the model, effort, time or tokens of each part it ran. Only the rebuild
  eval records cost, for its own agents.
- **Moving a part up or down.** No rule says when. The one memory page on it is written for products being built, not
  for Garura's own parts: Phoenix memory `knowledge/technology/agent-model-selection.md` ("Match the model to the job,
  per step", "Route, don't over-provision", "Re-run evals on any model change"; lines 24-39, 48-50), whose conditions
  are an agentic feature on Bedrock or Vertex (lines 4-8).
- **The test model setting** that BI-3's approved pages need (section 4.5).
- No issue plans any of it: a search of the work tracker for model routing, effort, Sonnet, Opus and Haiku finds no open
  issue about model choice.
- *State:* Neither.

## 7. What approved pages hand to these six

About 120 lines on 84 approved pages and ICE pages name one of the six, the intent, or its Must not (a search of
`.garura/product/product-os/`, 2026-11-11). These are promises BI-10's pages must keep. The main ones, by capability:

### 7.1 To Standards

- "The play checker's rules, such as a check that fails a gate with no way past, and the written harness standard.
  Standards, in Standards, structure, settings and memory, owns them." (`give-every-gate-a-way-past/capability.md` line
  69); "Writing the principle into the harness standard. Standards ... owns the written standards."
  (`fn-way-past-every-gate/feature.md` line 60; also line 58; `fn-way-past-every-gate/ice.md` line 7).
- "The loop names and the naming rule. Standards ... (BI-10), owns them." (`run-plays-as-loops/fn-loop-per-transition/
  feature.md` line 57); "The rule for fan-out and the scoped-write guard, as standards." (`fn-run-plays-side-by-side/
  feature.md` line 57).
- "The plays' names, and the rename to /list-issues. Standards ... owns them." (`track-execution/fn-see-issues-worth-
  attention/feature.md` line 66).
- "The severity rules, P1 to P4. #934 holds them, under Standards, structure, settings and memory in the tracker."
  (`track-execution/fn-record-defect-under-story/feature.md` line 53).
- "the rule that no play, skill or sub-agent names a tracker. Standards, structure, settings and memory owns them; the
  tool that meets the rule is this capability's." (`track-execution/capability.md` line 69; `fn-one-tool-knows-tracker/
  feature.md` line 56). The Must not is quoted as a reason on six pages: `initialize/capability.md` lines 79, 95;
  `initialize/fn-881/feature.md` lines 37, 76; `track-execution/fn-one-tool-knows-tracker/feature.md` lines 34, 68;
  `connect-use-and-market/capability.md` line 78; `connect-use-and-market/fn-connect-tools/feature.md` line 60.
- "The ADR template as a standard, and the templates index." (`manage-adrs/fn-show-accepter-findings/feature.md` line
  56; `manage-adrs/capability.md` line 66; `fn-keep-adrs-to-build/feature.md` line 57).
- "The lint itself and its other rules." (`ship-every-change/fn-keep-docs-in-step/feature.md` line 42); "Writing the
  rule and the project's own memory." (`ship-every-change/fn-scan-every-push/feature.md` line 46, the rule of no client
  and no personal reference); "the plays' names" (`ship-every-change/capability.md` line 73).
- "what Garura's parts are and how they are built, and the naming rule with its lists of built-in commands (Standards)"
  (`support-coding-tools/capability.md` line 63), with "Not decided: which tools the naming rule's check of built-in
  commands covers" (line 81).
- "The naming standard and the rename map's contents." (`features/fn-748/feature.md` line 55;
  `upgrade-project/fn-bring-new-settings/feature.md` line 55).
- "The run summary every play prints at its end, and how plays are built." (`features/fn-729/feature.md` line 59;
  `features/fn-806/feature.md` line 50; `orchestrate-agent-work/fn-know-what-next/feature.md` line 50;
  `orchestrate-agent-work/capability.md` line 77). The run summary is the shared close (`play-close.md`).
- "The question setting and the rule for asking a person." (`orchestrate-agent-work/fn-795/feature.md` line 70).

### 7.2 To Build your own harness

- "Out: building and changing a loop, with /create-loop, /edit-loop and the loop linter. Build your own harness ...
  (BI-10), owns it." (`run-plays-as-loops/capability.md` line 69; `fn-run-loop/feature.md` line 82;
  `fn-check-loop-result/feature.md` line 63).
- "Adding what starts a loop when a loop is built, and checking the loop principles in the loop builders and the loop
  linter (#699 ...)." (`fn-start-loop-on-trigger/feature.md` line 49; `fn-loop-per-transition/feature.md` line 56).
- "Adding a gate to a play is Build your own harness's" (`give-every-gate-a-way-past/capability.md` line 69;
  `fn-way-past-every-gate/feature.md` line 59); "Pinning or unpinning a checkpoint, which changes its play's intent."
  (`fn-pinned-yes/feature.md` line 51); "The run marker inside each play, and the check in the review of each change.
  Build your own harness ... and Ship every change the same way ... own them." (`fn-guardrail-way-past/feature.md` line
  55).
- "Building a harness with Garura's build plays." (`install-into-project/fn-choose-parts/feature.md` line 56).

### 7.3 To Structure

- "Where each run's records live in its issue's folder (#969). Structure ... owns it." (`give-every-gate-a-way-past/
  fn-keep-what-is-owed/feature.md` line 57; `fn-record-every-skip/feature.md` line 49; `fn-record-every-skip/ice.md`
  line 7).
- "where each installed part lives (Structure)" (`install-into-project/capability.md` line 65); "where each part lives
  (Structure)" (`upgrade-project/capability.md` line 64); "where each part lives once laid (Structure)"
  (`support-coding-tools/capability.md` line 63).

### 7.4 To Settings

- "what each setting means and who reads it, and where settings files live. Settings ... owns them."
  (`upgrade-project/fn-bring-new-settings/feature.md` line 54; `upgrade-project/capability.md` line 64;
  `install-into-project/capability.md` line 65; `initialize/capability.md` line 62).
- "Where the project's settings live. The review of Settings ... owns it." (`build-or-update-product/fn-act-on-its-own/
  feature.md` line 59).
- The loop settings: `run-plays-as-loops/capability.md` line 70; `fn-run-loop/feature.md` line 82;
  `fn-check-loop-result/feature.md` line 66 ("The default checker and where the setting lives"); `fn-start-loop-on-
  trigger/feature.md` line 50.
- The gate settings and the learned policy: `give-every-gate-a-way-past/capability.md` line 68; `fn-way-past-every-gate/
  feature.md` line 61; `fn-pinned-yes/feature.md` line 52; `fn-record-every-skip/feature.md` line 48;
  `manage-adrs/fn-accept-adr/feature.md` line 71; `ship-every-change/capability.md` line 73.
- The tracker settings: `track-execution/capability.md` line 69; `keep-spec-matched/fn-keep-tracker-matched/feature.md`
  line 45 ("Settings owns the project's settings."); `track-execution/fn-say-what-each-type-means/feature.md` line 60.
- The design and test settings: `design-work/capability.md` line 57; `design-work/fn-design-chosen-work/feature.md` line
  90; `test-user-experience/capability.md` line 60; `build-work-test-first/capability.md` line 67 and its two features
  (`fn-build-code-to-pass/feature.md` line 102; `fn-write-failing-tests/feature.md` line 58);
  `fix-defects-test-first/capability.md` line 72 and its two features.

### 7.5 To Memory

- "how Phoenix memory reaches a machine and is brought up to date, what may enter each memory tier, and promotion.
  Memory ... owns them." (`initialize/capability.md` line 58; `fn-setup-questions/feature.md` line 54;
  `fn-project-memory/feature.md` line 56; `fn-883/feature.md` lines 55, 59).
- "Phoenix memory's own versions and notes." (`upgrade-project/fn-cut-release/feature.md` line 52;
  `upgrade-project/capability.md` line 64).
- "Retiring the machine-wide copy of all memory for every project. Memory ... decides it."
  (`install-into-project/fn-take-out/feature.md` line 55; `fn-check-install/feature.md` line 47).
- "A memory update is decided by the rules of Memory ...: 'Only a person decides, one update at a time.'"
  (`review-agent-work/capability.md` line 34; line 88; `fn-review-memory/feature.md` line 42); "Recording a decision
  and its trace, and checking its sources." (`fn-check-agent-decisions/feature.md` line 42).
- "approving a memory update the knowledge step raises, and promoting a page to Garura or Phoenix memory"
  (`run-plays-as-loops/capability.md` line 74; `fn-brief-open-points/feature.md` line 63).
- "choosing and promoting what is learned into Garura memory or Phoenix memory, which the review of Memory owns"
  (`connect-use-and-market/capability.md` line 53; `build-or-update-product/capability.md` line 73;
  `understand-consumers-and-competition/capability.md` line 65).
- 15 BI-2 and BI-3 pages hand out promotion without naming an owner: "moving it up is a promotion a person makes on
  purpose, outside this work" (for example `design-technology-architecture/capability.md` line 43,
  `manage-surfaces/capability.md` line 53, the four environment-setup pages, the four deployment-design pages, and
  `write-work-evals/fn-add-eval-steps/feature.md`).

### 7.6 To Intelligent model routing

- "Which model each part of the work runs on belongs to the agreed capability Intelligent model routing ... This
  capability reads the setting and sends the tests where it says." (`build-work-test-first/capability.md` line 16; line
  67; `fn-build-code-to-pass/feature.md` lines 59, 102; `fn-write-failing-tests/feature.md` lines 40, 58; the same in
  `fix-defects-test-first/capability.md` line 72 and its two features).
- "Out: which model and effort each part runs on. Intelligent model routing owns it" (`support-coding-tools/
  capability.md` line 62; line 78); "Which tier and effort each part runs on, and changing it. Intelligent model
  routing ... owns it." (`fn-map-model-tier/feature.md` line 47; lines 12, 36, 43; `fn-map-model-tier/ice.md` line 14);
  "Which tier each part runs on. Intelligent model routing decides it." (`fn-install-for-claude-code/feature.md` line
  53; `fn-install-for-codex/feature.md` line 50; `fn-install-for-copilot/feature.md` line 40;
  `fn-install-for-factory/feature.md` line 42; `fn-install-for-antigravity/feature.md` line 37).
- One line keeps a model outside routing: "A model used beside the installed tool, such as the model that checks a loop
  or writes tests. It is a setting of those plays, not an install." (`fn-map-model-tier/feature.md` line 49).

### 7.7 To the intent as a whole

- `orchestrate-agent-work/capability.md` line 77: "the settings, the names of the plays, and how plays and loops are
  built."; `design-work/capability.md` line 96 quotes "settings hold what can be turned on or off" and "Every tool reads
  its settings."

## 8. The old parts, and other parts that belong here

All filed under the closed intent `bi-734` ("Garura publishes a standard for building agentic harnesses",
`intents/bi-734.md`), which #734 (the old intent for the harness standard) closed with "Replaced by garura-intents#10." None has a domain (`domain: ''`), and none
has an ICE page: each keeps a four-line ICE inside its page. Spine lines are in `_spine.yaml`.

| Part | What its page says | How far built | Belongs to |
|---|---|---|---|
| `cap-735` (lines 65-76) | "The harness standard, written down": "one published standard — naming rules, the principles behind how a harness is built, and the practices that follow from them" (`capabilities/cap-735/capability.md` line 4) | Built: `docs/standards/harness-standard.md`; #735 (the harness standard, written down) closed as completed; out of step (section 1.1) | Standards |
| `fn-736` (line 831) | Naming rules: "loops named run-<phase>, plays verb-object (at most two words) ... No exceptions except the two named one-word plays (next, focus)" (lines 4, 8) | Built as `naming.md` and `naming.yaml`, but with `complete-<phase>`, no one-word plays, and /next dropped (ADR 051); ADR 066 decides newer rules | Standards |
| `fn-737` (line 842) | Principles and practices, "each with its reason", eight principles listed (line 4) | Built: eleven principles, each naming its ADR but one (section 1.1) | Standards |
| `fn-738` (line 853) | "a decision record, through /adr, that adopts the naming standard and supersedes ADR 006 ... and ADR 018" (line 4) | Built: ADR 046; ADR 006 and 018 read "superseded by ADR 046"; the page uses the old play name /adr | Standards |
| `cap-739` (lines 77-88) | "The naming checks, built before any rename" (line 4) | Built; #739 (the naming checks) closed | Standards |
| `fn-740` (line 864) | "lint-components checks every play, skill, agent and loop name against the rule file" (line 4) | Built: `lint-components/lib/rules/naming.js`; no naming error today | Standards |
| `fn-741` (line 875) | "one file mapping every old name to its new name, and a check that finds any old name still used" (line 4) | Built: `rename-map.yaml`, `check_old_names.py`; 12 hits today; #936 (tests for a name removed with no successor) open. BI-7's `fn-748` needs it (spine `depends_on: fn-741`) | Standards |
| `cap-742` (lines 89-100) | "Every name moved to the standard, one family at a time" (line 4) | Built for ADR 046; #742 (every name moved to the standard) closed under #958 (the epic of plan 734, closed) | Standards |
| `fn-743` (line 886) | Harness plays and loops: "the Discovery loop's command → run-discovery" (line 4) | Built, but as `complete-discovery`; ADR 066 renames this family again | Standards |
| `fn-744` (line 898) | Change, plan, knowledge and record plays: "the planned plan plays take draft-plan, show-plan, update-plan, list-plans"; "next and focus stay one word" (lines 4, 8) | Built, but /draft-plan became /shape-plan and /focus became /list-focus-issues; ADR 066 renames this family again (/reshape-plan, /view-plan, /list-issues) | Standards |
| `fn-745` (line 910) | Lifecycle and lens plays: "shape → design-scope ... implement → build-feature ... launch → release-feature" (line 4) | Built, but with other names (`shape-*-lens`, `build-epic`, `release-epic`); ADR 066 renames this family again (`specify-*`, `design-*`) | Standards |
| `fn-746` (line 922) | "every skill renamed to the skill verb list (to be agreed with the product owner)" (line 4) | Built for ADR 046 §5; skills keep their verbs under ADR 066 until a later decision | Standards |

- **Other parts.** No other part in the model names `bi-10` or does BI-10's work (a read of `_spine.yaml`: 0 matches for
  `bi-10`). `fn-748` (BI-7's upgrade, "a part under an old name goes once its new name is laid") stays BI-7's; it only
  needs `fn-741`. `fn-597` (rebuild the product model as an ontology) is BI-11's.
- **Owed parts with no page.** The harness roles feature (#1015, record the harness roles feature); the Agent-work tool's rule (the tool itself is BI-9's,
  `fn-one-tool-knows-tracker`).
- **The tracker.** #735 (the harness standard, written down) and #739 (the naming checks) are sub-issues of BI-10. #742
  (every name moved to the standard) hangs under #958 (the epic of plan 734, closed). #992 (every gate has a key) hangs
  under #735.

## 9. Gates with no way past, in the built parts of the six

BI-9's Must not: "Stop a person. Every gate has a way past it that records what's owed."

| Gate | Where | Way past today | What is recorded |
|---|---|---|---|
| A pinned checkpoint | Settings: "No config value, policy, or ledger can turn it off." (gate-config line 12; lines 90-97) | None in settings; "Unpinning is an intent change to that play (edit-play)" | "pinned — config bypass refused" |
| A machine wall: pre-flight halts, sensitive files, stop conditions, eval failures | Settings: "never gated by this block" (gate-config lines 120-124) | None | — |
| An off checkpoint | Settings (`gates.plays.<play>: off`) | Passes on its own | The skip, only when `evidence.record` is on; it is off (`core/config.yaml` line 142) |
| A name that breaks the rules | Standards: "a name that breaks a rule cannot land" (`naming.md` line 4) | Add the verb with its meaning to `naming.yaml` first (lines 23-24, 62), which records it; for skills and agents the verb lists are frozen until a later decision (ADR 066 line 31) | The verb list |
| `remove-model-part` and `remove-plan` in a project | Standards: they "fail the check in any project that reads Phoenix memory's copy" (ADR 066 line 29) | None until the verb `remove` is decided | — |
| A loop whose ICE changed since it was built | Standards: the loop linter fails it (`lint_loop.py` lines 180-190) | Rebuild through /edit-loop | The new fingerprint |
| A builder's approval | Build your own harness | With no person reachable, "record that approval was assumed" | The assumption |
| Building plays in a product project | Build your own harness: "no target ever receives them under `full`" (`install.py` lines 210-215) | Install with `--scope harness`, which drops the product plays | Nothing |
| An edit to a compiled play for an intent change | Standards: "Never hand-edit a compiled `SKILL.md` for an intent change" (`CLAUDE.md`, "Play Pipeline Rules") | A rule only; the hook of #893 (guardrails laid by the install) would enforce it, and "how a person overrides it on purpose" is not decided | — |
| A blocking memory update | Memory: "add `"blocking": true` and stop" (`GUIDE.md` line 58) | A person decides the update | The decision, with who and their reply; nothing reminds anyone (5 waiting, the oldest since 2026-10-24) |
| A waiting memory update | Memory: "Never decide from ... a waiting memory update" (`GUIDE.md` line 87) | A person approves it | As above |
| Phoenix memory cannot be reached | Memory: `tier_missing`, "Say so. It never means 'nothing found'." (`GUIDE.md` line 41) | Point the `phoenix` setting at a copy that can be reached (README lines 33-45) | Nothing |
| Another issue's short-term memory | Memory: "A read of another issue's short-term path is refused" (README lines 93-95) | Promotion, which is not built (section 5.5) | — |
| A loop with no checker model | Settings: `loop_preflight.py` lines 134-135 stop the loop | Set the setting | The setting |

- So the stops with no way past in BI-10's own parts are: the pinned kind and the machine walls (both defined in
  Settings), the frozen verb lists in projects, and building plays in a product project. Whether a pinned yes is a key
  or a stop kept on purpose is BI-9's open question (#992, every gate has a key; `give-every-gate-a-way-past/fn-pinned-yes/feature.md`).

## 10. What is new: not built and planned in no issue

Each would need outside research before it is drafted, except where marked.

1. **Choosing a model and an effort by the job, and checking the choice.** How agent harnesses route steps to cheaper
   or stronger models; how effort levels compare across Claude Code, Codex, Factory, GitHub Copilot and Antigravity
   (the approved BI-7 memory covers where each tool takes a model, not how to choose one); how a run can record the
   model, time and tokens of each part. Research needed.
2. **Building a sub-agent or a skill to the standard.** How other agent frameworks scaffold a new agent or skill and
   check it. Research needed.
3. **Building a harness in a team's own repository.** The builders on the installed layout, and a starter for a new
   harness repository. #933 (an architecture memory for teams building a harness)
   plans the memory only. Research needed on how other frameworks let a team
   extend them.
4. **A check that no part names a tracker** (the Must not). Mechanical; no research needed.
5. **One written map of where every part lives, and a check that `.garura/` holds to it.** Mechanical; no research
   needed.
6. **A way to see and change settings, and a check of each value.** #946 (each setting names who reads it) plans only the
   reader check. Light research on
   settings schemas.
7. **A reminder or an end for a waiting memory update.** Light research on how review queues age items.
8. **A play or command that promotes a page on a person's yes.** Named since ADR 036 and in the glossary, but no issue
   files it outside #611's Learn loop recipe (BI-6). Light research.

## 11. Where BI-10's parts touch other intents

- **Product model (BI-11).** The ICE kind, the ontology, the model's checks and `fn-597` are BI-11's. BI-10 holds the ICE
  of plays and loops.
- **Install and distribute (BI-7).** The install lays what Structure, Settings and Memory define (section 7). It carries
  each tier (`fn-map-model-tier`); routing chooses it. Initialize builds a project's Garura memory; Memory says what may
  enter. The tracker files #946 and #947 (settings) and #883 (the Phoenix install) under BI-7.
- **Developer tooling (BI-8).** Argus shows memory updates and traces; Memory owns their rules. The push scan (#888, the change plays push with no scan for
  client or personal references)
  needs the no-reference rule that Standards writes.
- **Orchestration (BI-9).** The way past every gate is BI-9's; the gate settings and the written principle are here.
  The Agent-work tool (#1023) is BI-9's; the rule it meets is BI-10's Must not. The loop runs are BI-9's; building loops
  is here.
- **Design → Code (BI-3) and Code → Validation (BI-4).** The test model, design and review-round settings live here.
- **Run → Product (BI-6).** Choosing and promoting learnings was left to Memory (`capabilities.md` line 68).

## 12. Leans

Each is a proposal with its evidence, not a decision.

### Lean 1: the six lines

1. **Standards** — keep the product owner's words. They fit what is built, with one reading made plain on the page:
   plays and loops carry their ICE, and skills and sub-agents follow written standards (open question 1).
2. **Build your own harness** — reword lightly, to name skills, where the work is done: "You can keep building your
   harness with your own plays, loops, sub-agents and skills, in a consistent way." Who "you" is stays open (question
   2).
3. **Structure** — keep: "Where everything lives, in source and once deployed." Its page says "deployed" means
   installed, and that a run's records are part of "everything" (#969, every run's records in its issue's evidence
   folder).
4. **Settings** — keep. Approved pages already read "turned on or off" as "turns on or off, or picks, once for the
   project" (section 4.5); the page says so.
5. **Memory** — keep. It fits the build. The rules question (question 3) is settled on the page, not in the line.
6. **Intelligent model routing** — keep. Its spine entry names both `bi-10` and `bi-7`, as "Also serves Install and
   distribute" says.

### Lean 2: the features of Standards, from the evidence only

1. Write the harness standard: the parts, the principles with the decision each comes from, and how it is kept.
   Built; out of step (section 1.1). From `cap-735` and `fn-737`.
2. Record each change to the standard as a decision, with what it replaces. Built (ADR 046, ADR 066). From `fn-738`.
3. Build every play and loop from its ICE, and keep the compiled part matched to it. Built for 31 plays and the loop;
   the play linter does not compare the fingerprint.
4. Write the standard for each kind of part: play, loop, sub-agent, skill, script, shared file and tool. Built in part;
   tools have none (#620, tools become a component); the layer rule is planned (#856, no skill names a play).
5. Name every part by one rule, with five roles owning the verbs. Built for ADR 046; ADR 066 decided, not applied;
   the roles of #1015 (record the harness roles feature). From `fn-736`.
6. Rename each family of parts when the rule changes, with a rename map and a check that no old name is left. Built
   once; ADR 066's rename not filed. From `cap-742`, `fn-741`, `fn-743`, `fn-744`, `fn-745`, `fn-746`, each kept for
   its family.
7. Check every part against the standard. Built; 36 errors on the source; runs only on changed parts. From `cap-739`
   and `fn-740`.
8. Write the rules every part follows: asking a person, staying on scope, the way of working, no client and no personal
   reference. Built in part; planned in #999 (asking a person), #1004 (staying on scope), #952 (the way of
   working) and #982 (home-folder paths in run records).
9. Give findings and defects one severity, P1 to P4. Planned (#934, one severity in three layers).
10. Hold the Must not with a check that no part names a tracker. Neither.

### Lean 3: the features of Build your own harness, from the evidence only

1. Build a play from its ICE (/create-play). Built.
2. Change a play through its ICE (/edit-play). Built.
3. Build a loop from its ICE (/create-loop). Built.
4. Change a loop through its ICE (/edit-loop). Built.
5. Check a loop against the loop principles, including what starts it. Planned (#699, the loop builders check the
   loop principles).
6. Add a gate to a play with its way past, and pin or unpin one. Built in part: the builders write checkpoints, and
   pinning is an intent change; the way past is BI-9's.
7. Mark that a play is running, so a guardrail can tell a play's work from a shortcut. Planned (#893, guardrails laid by the
   install).
8. Build a sub-agent and a skill to the standard. Neither.
9. Build a harness in a team's own repository, against a written architecture. Built in part (the `harness` scope);
   planned in part (#933, the architecture memory).

### Lean 4: the features of Structure, from the evidence only

1. Lay out Garura's source: where each kind of part, tool, memory and setting lives. Built; planned in #620 (tools as a
   component) and #415 (the harness layout, stale).
2. Lay out an installed project: where each part lands, the shared files, the tools and the memory guide. Built for
   Claude Code.
3. Keep `.garura/` to its written list, and check it. Built as ADRs and docs; out of step; no check.
4. Keep each run's records with its issue, with only repository paths in them. Planned (#969, run records in the issue's
   evidence folder; #943, gate records there; #982, no home-folder paths).

### Lean 5: the features of Settings, from the evidence only

1. Keep every setting in one settings file, laid as each project's copy. Built.
2. Say what each setting means and who reads it, and fail a setting no one reads. Planned (#946, each setting names its
   reader; #947, settings for gone parts).
3. Keep every other settings file in one folder. Planned (#946, one settings folder).
4. Turn each checkpoint on or off, and keep the policy learned from a person's answers. Built; the policy file is never
   written; the pinned list names gone plays.
5. Turn a run's evidence on or off. Built; off by default.
6. Hold the settings other capabilities need: the test model, the design settings, the kinds of change that may go ahead
   on their own, the connections, the review rounds, the question tier, the loop settings and the trackers. Built in
   part (section 4.5).
7. Make every tool read its settings. Built in part (section 4.7).

### Lean 6: the features of Memory, from the evidence only

1. Find memory across three tiers through one tool. Built.
2. Let only a person decide a memory update, one at a time. Built; no reminder.
3. Keep each decision's trace and check its sources. Built; #852 (replaced decisions in the trace check) open.
4. Make every agent read memory only through the tool, and fail a part that names a memory path. Built in part (#663, every part
   reads memory through the tool).
5. Keep Phoenix memory in step with Garura's source, versioned per release with its notes. Planned (#966 and #921, Phoenix
   memory in step and versioned; #949, the 60 places);
   60 differences today.
6. Bring Phoenix memory to a machine and keep it current. Built in part (the download on first use); planned (#883, the Phoenix
   install).
7. Move a page up a tier on a person's yes, and choose what is learned. Neither (named only).
8. Check what memory holds: pages out of date, sources that changed. Planned (#942, a project's memory can be managed).
9. Keep what agents decide from inside memory: the machine-wide copy, Claude Code's own memory, and the rules question.
   Planned in part (#839, Claude Code's own memory; ADR 055 §8).

### Lean 7: the features of Intelligent model routing, from the evidence only

1. Give each part a model tier and an effort by a written rule. Built in part (tiers on 91 parts; effort on 4; the rule
   covers skills only).
2. Send a step to the model a setting names, apart from the session's. Built for the loop's checker and the grounding
   judge; the test model is not built.
3. Record each run's model, effort, time and cost for each part. Neither (only the rebuild eval).
4. Move a part up or down a tier on that record, and check the move with an eval. Neither.
5. Choose the model and effort by the job at run time. Neither.

Carrying the tier into each tool stays with BI-7's `fn-map-model-tier`.

### Lean 8: the old parts

- **Merge `cap-735`, `cap-739` and `cap-742` into Standards** once its page is written, with all nine features kept and
  repointed from `bi-734` to `bi-10`, as the work order of #1021 (the reorganisation) says ("Merge the old capabilities in, keeping the 33
  features"). Each page is rewritten to what was built: `fn-736` to the naming rules (with ADR 066), `fn-737` to the
  eleven principles, `fn-738` to recording each change to the standard as a decision, `fn-740` and `fn-741` to the
  checks, and `fn-743` to `fn-746` to the four families ADR 066 renames next. Each gets its ICE on its own page.
- **Keep `fn-741`'s id**, because BI-7's `fn-748` needs it.
- **Write the harness roles feature (#1015, record the harness roles feature)** under Standards, where the product owner placed it on 2026-10-31.
- **Delete `intents/bi-734.md`** once nothing names it, with the other old intent pages (the work order of #1021, the reorganisation).

### Lean 9: the domain

Software delivery planning, with its opening widened to say it also keeps the harness's standards, structure, settings
and memory, as for BI-6 to BI-9 (`software-delivery-planning/domain.md` line 4). The cost: BI-10's work is about the
harness itself, not about delivering a product, so the fit is the weakest of the eleven; the three old capabilities
have no domain today.

### Lean 10: the tracker follows the model

- Move #946 and #947 (settings) from #513 (BI-7's install and distribution) to BI-10. Basis:
  `upgrade-project/fn-bring-new-settings/feature.md` line 54; `initialize/capability.md` line 62.
- Move #883 (the Phoenix install) from #862 (BI-7's initialize) to BI-10. Basis: `initialize/fn-883/feature.md` line 55.
- Move #992 (every gate has a key) from #735 (the harness standard) to BI-9's tracker issue, with its "write it into the harness standard" part
  left here. Basis: `give-every-gate-a-way-past/fn-way-past-every-gate/feature.md` lines 58-61.
- Leave #893 (guardrails) under BI-10: its run marker is Build your own harness's; BI-7 lays the hook and BI-9 owns its
  way past.

### Lean 11: found and not filed, to file when the product owner says so

- The harness standard: loops `complete-<phase>`, the old phase and verb table, no Tool part, principle 5 names a
  person, and principle 6 speaks of the model only (section 1.1).
- The ADR 066 rename has no issue (section 1.4).
- Phoenix memory's `naming.md` and `naming.yaml` differ from the source, so an installed project checks names against
  other rules (section 1.5).
- The play linter does not compare a play's fingerprint to its ICE (section 1.5).
- The source fails 36 linter checks, in the six hand-written plays and five skills; no CI runs the linters (section
  1.5).
- `.gitignore` line 152 still ignores `.garura/core/memory/`, which ADR 039 says "goes"; `CLAUDE.md` line 28 agrees with
  `.gitignore`, not with ADR 039 (section 3.3).
- The plans folder is in no layout list; `engine-state.json` is read by nothing; the `write-evidence` skill a Phoenix
  rule names does not exist (section 3.3).
- The installed settings have two `product:` keys and point at a memory folder that does not exist (section 4.4).
- The plan tool takes its folder from a fixed default, not the `plans` setting (section 4.7).
- Five memory updates wait with no reminder, three since 2026-10-24 on a question ADR 054 settled (section 5.2).
- `docs/components/skills.md` says skills choose their model, but the Claude Code install drops it (section 6.2).
- The skill `author-play-ice` writes the old `intent.yaml` shape, and no part names it (a search of
  `core/components/`).

## 13. Questions only the product owner can answer

Each has our proposed answer and its basis.

1. **Does "Everything is built on the ICE model" cover skills and sub-agents, or plays and loops only?**
   - Proposed: plays and loops carry their ICE; a skill and a sub-agent follow the written standard for their kind and
     are checked against it.
   - Basis: only plays and the loop have an ICE source (section 1.2); "A play or loop is compiled from its ICE" (harness
     standard lines 50-55); a sub-agent "gathers context" and a skill "does the work" (lines 33-37), so the intent sits
     in the play that runs them.
   - Examples: a bank's harness keeps one ICE per payment workflow and none per helper; a game studio gives each build
     agent its own ICE; a news site keeps ICE only for what a person runs.
2. **Who is "you" in Build your own harness: Garura's own makers, in Garura's repository, or any team, in its own
   repository with Garura installed?**
   - Proposed: any team, in its own repository. The builders then run on the installed layout, which changes ADR 055
     §5 ("source-only by design") through a new ADR.
   - Basis: BI-10's Outcome: "Teams can build their own harness on it."; the harness standard is "written so that a team
     can take it" (lines 3-5); today a product project never gets the builders (section 2.2).
   - Examples: a retail team adds a /refund-check play beside Garura's; an insurer builds its own claims loop; an agency
     only uses Garura's plays and builds none.
3. **Are the engine's rules memory?** BI-10's proof says "Nothing an agent decides from sits outside memory"; #952
   (the way of working as engine rules and settings) records "memory is a cartridge … you can't put rules into a
   cartridge".
   - Proposed: the rules stay in Phoenix memory as standards, read through the memory tool, as built, and the proof
     stands. #952 sorts the way of working into rules and settings within that.
   - Basis: the glossary: Standards "Live in Phoenix memory ... Agents read them through the memory tool" (line 47);
     ADR 035; the BI-10 page was confirmed on 2026-11-02, after #952 (2026-10-29).
   - Examples: a hospital keeps its clinical rules in a versioned rule store agents query; a start-up writes its rules
     into the agent's prompt; a platform team keeps rules in code and memory for knowledge only.
4. **Who chooses each part's model and effort: the part's maker in its source, the project in its settings, or a router
   at run time?**
   - Proposed: the maker sets a tier and an effort in the source by a written rule; a project may change a part's tier
     in its settings; each run records the model, effort and cost of each part, so a person can move a part up or down.
     A run-time router comes later, if the records show it pays.
   - Basis: today's tiers on 91 parts (section 6.1); the loop's checker and the test model are already settings
     (sections 4.5, 6.3); Phoenix memory's "Route, don't over-provision" and "Re-run evals on any model change"
     (`agent-model-selection.md` lines 31-36, 48-50); ADR 042's cost note.
   - Examples: a call centre's summariser runs on a small model and its escalation judge on a large one; a legal team
     pins every step to one strong model for audit; a shop lets a router pick per request.
5. **Should a skill's own tier reach Claude Code?** Today the sub-agent's model applies, and 70 skills' tiers do nothing.
   - Proposed: yes, lay the skill's tier and effort, tried first on one skill and checked.
   - Basis: Claude Code takes `model` and `effort` on a skill (mu-20261110-001,
     `1021/context/bi-7-capability-3/answers/coding-tool-claude-code.md` line 9); `fn-map-model-tier` names the gap
     (line 21); `docs/components/skills.md` already tells skill makers to choose one.
   - Examples: a commit skill on a fast model inside a strong reviewer agent; a drafting skill on a strong model inside a
     fast gatherer; every skill on its agent's model, as today.
6. **Is moving a page up a tier, and choosing what is learned, a feature of Memory, done on a person's yes?**
   - Proposed: yes. Memory holds "promote a page on a person's yes"; the person decides in Argus's Memory section
     (BI-8); BI-6 proposes what was learned.
   - Basis: "A person approves every promotion" (Phoenix memory `README.md` line 6); the BI-6 note leaves choosing and
     promoting to "the review of Memory" (`capabilities.md` line 68); `review-agent-work/capability.md` line 88 gives
     "moving memory up" to Memory.
   - Examples: a support team promotes a fixed answer to the shared knowledge base after a lead approves it; a data
     team promotes a schema rule only at release; an open-source project promotes through a pull request.
7. **When does ADR 066's rename run, and is it filed now?**
   - Proposed: file it now under BI-10 as one issue (Standards), and run it after the reviews of BI-10 and BI-11, so each
     page is written once with the new names.
   - Basis: ADR 066: "The rename, as one change" (line 149); no open issue files it (section 1.4); #1021 (the reorganisation) puts it outside
     its own change.
   - Examples: a mobile team renames all screens in one release; a bank renames one module family a sprint; a library
     keeps old names as aliases for a version.
8. **Should a check fail every part that names a tracker now, or only after the Agent-work tool (#1023) lands?**
   - Proposed: add the check with the Agent-work tool (#1023); it warns until the parts have moved, then fails.
   - Basis: ADR 065: "Rule 4 has no tool yet" (BI-9 stock-take section 3.1); 3 plays, 11 skills and 3 agents hold `gh`
     commands today (#1023, the Agent-work tool); principle 6, "missing links are warnings to fix later, not stops" (harness standard lines
     70-72).
   - Examples: a team turns a new lint rule on as a warning for a month; a regulated team fails the build at once; a
     small team fixes all parts in one change and turns it on.
