# BI-7 (Install and distribute): what Garura has for getting into a project, upgrading it and serving each tool

Research only, 2026-11-10, for #1021 (the chore that reorganises Garura's business intents around the phases and their
transitions). Nothing under `.garura/product/`, `.garura/core/` or `.claude/`, on GitHub or in git was changed. No
memory update was raised and no decision trace was recorded, because the brief allowed this one file only.

Scope: BI-7 only. Its page: "A team gets Garura into its project, upgrades it knowing what changes, and uses it on
whichever coding tool it has." The agreed capabilities are Install into a project, Upgrade a project and Support each
coding tool (`capabilities.md` lines 71-74). Intelligent model routing "Also serves Install and distribute" (line 93);
it is noted here as a boundary, not held.

## In one paragraph

A team can get Garura into a project today with one command, but only for Claude Code, and by default that command
gives it an old release: v3.0.0, from 7 October, which has neither the memory system nor the current plays. Garura has
two installers, and they do different things. The one-line installer that the README offers downloads a release,
records its version and shows "from → to" on an upgrade, but it keeps no list of what it laid. So it never removes a
part Garura dropped, it gives no choice of what to install, and nothing can take it out again. The install play, run
from a copy of Garura's source, keeps that list. It removes dropped and renamed parts, offers two kinds of install and
has an uninstall play, but it records no version, and no project ever receives it. Both installers keep the team's
settings file and instructions file whole. The team's values survive, but new settings never arrive. An installed
Garura part that a person edited is replaced whole. Neither installer changes a project's product model; a person can
move an older model by hand, with a script that only a copy of the source holds. Codex has an install that is stopped
until it is redesigned (#863). Factory was supported once and was removed. GitHub Copilot and Antigravity have nothing,
not even an issue. Initialize, the set-up step after the install, is designed in the model but not built, and it names
no intent. Nothing in the model names BI-7 today.

## Words used here

- **Install**: put Garura's parts into a project so its coding tool can run them. **Upgrade**: install a newer Garura
  over an older one. **Uninstall**: take Garura's parts out again.
- **The one-line installer**: `installer/install.sh`, run as one `curl ... | bash` command in the project's folder
  (README lines 141-148). It downloads Garura from GitHub. No copy of Garura's source is needed.
- **The install play** and **the uninstall play**: `/install-garura` and `/uninstall-garura`. They are written by hand,
  and scripts do their work (`core/components/plays/install-garura/scripts/install.py`,
  `core/components/plays/uninstall-garura/scripts/uninstall.py`). They run from a copy of Garura's source (a checkout).
- **Install record**: `.garura/install-manifest.json`, the list of every file and folder the install play laid. Only the
  install play writes it.
- **Install kind** (the code says scope): which parts a project gets. Today there are two. `full` is every live part
  except Garura's own build plays. `harness` is only Garura's own build and change plays and the workers they call.
- **Adapter**: the part of the install play that lays Garura in one coding tool's own shape
  (`scripts/adapters/claude.py`, `codex.py`).
- **Coding tool**: the agent tool a team works in. The agreed list names Claude Code, Codex, GitHub Copilot,
  Antigravity and Factory.
- **Installed part**: a play, loop, agent, skill, script, shared file or tool as it is laid in a project (`.claude/`,
  `.garura/core/tools/`). **Stale** or **deprecated**: a part marked so in its front matter; no install lays it.
- **Release**: a tagged version of Garura on GitHub (v0.9.0, v2.0.0, v3.0.0), with its notes.
- **Engine thing**: the product owner's word for something that runs as part of Garura itself, not as a play (ADR 066
  §5; `names.md` line 33; `capabilities.md` line 73). No source says more about it.
- **Product model**, **spine**, **ICE**, **Phoenix memory**, **Garura memory** and **short-term memory**: as in the
  earlier inventories.

States: **Live** (both installers) · **Live, one-line installer only** · **Live, install play only** · **Stopped** ·
**Removed** · **Planned only** (an open issue) · **Neither** (no build and no issue).

## 1. Two installers, side by side

| | One-line installer (`installer/install.sh`) | Install play (`install.py`) |
|---|---|---|
| How a team runs it | One command in the project's folder. Needs curl, Python 3 and the network (README lines 135-148). | From a Garura checkout: `python3 core/components/plays/install-garura/scripts/install.py --target <path>` (install-garura `SKILL.md` lines 134-138). |
| Which Garura | The latest release by default, a named release, or `main` (lines 5-13, 81-100). A version that does not exist stops it (README line 164). | The checkout as it is. |
| Version recorded | `.garura/core/garura-version` (lines 378-380, 477-478). | None. The record's `"version": 2` is the record's own format (line 519). This repo has no version file. |
| Coding tool | Claude Code only: every path it writes is under `.claude/` (lines 312-346). | `--tool claude`. `--tool codex` stops at once (lines 78-89). |
| What the project gets | No choice: every part that is not stale or deprecated (lines 252-302). Garura's own build plays come too, because `EXCLUDED_SKILLS` is empty (line 18). | `full` or `harness` (lines 214-320). `full` leaves out the seven build plays and `author-product-ontology` (lines 214-218). |
| Install record | Not written. | Written (lines 516-523). |
| Removes what Garura dropped or renamed | No: it copies over what is there (lines 417-451). | Yes, from the last record and from the rename map (lines 440-513). |
| Agents' shared files (the memory reading protocol, the copy script, the failure format) | Not laid: only the agents' own files are copied (lines 275-285). Read from the script; no test covers it. | Laid in `.claude/skills/_shared/` (`adapters/common.py` lines 57-80). |
| Project instructions | Garura's own development guide, the repository's `CLAUDE.md`, cut down (lines 153-208). On a first install it is written over any `CLAUDE.md` the project has (line 371). On an upgrade it goes to `CLAUDE.md.new` (lines 466-471). | `project-instructions.md`, a short guide to running plays (`install.py` lines 412-418), so "how Garura is built" does not reach every agent of the project. `CLAUDE.md.new` beside an existing one (`claude.py` lines 128-138). |
| Settings file | Written fresh on a first install; `config.yaml.new` beside it on an upgrade (lines 354-360, 459-464). | Kept whole unless `--force-config` (lines 394-401). |
| Memory system and tools | The play's own two scripts (lines 210-239). | The same two scripts (`install.py` lines 420-435). |
| Other | Makes an empty `src/` folder (line 365). Copies all of memory into a machine-wide folder in the home folder (lines 348-352, 453-457). | Copies all of memory into the same machine-wide folder (lines 379-385). |
| Take it out again | Nothing. | `/uninstall-garura`, from the record. |

What both share: neither changes a project's product model ("The install never changes a product model the project
already has (#813)", `install.py` line 53; the test `test_the_shell_installer_leaves_a_pre_807_model_unchanged`,
`test_install.py` line 1186). Both use the same memory and tools scripts ("Both install paths call this",
`memory_system.py` lines 6-7; `tools_system.py` lines 5-6).

Where the plays can run: `/install-garura` and `/uninstall-garura` are never laid in a project. They are in
`META_PLAYS` (`install.py` lines 214-215), and ADR 055 §5 (lines 55-58) names them source-only. Garura's own repository
installs the harness kind, and its list (lines 220-264) does not name them either; this repository's `.claude/skills/`
has neither. So the README's contributor line, `claude "/install-garura --target /path/to/your-project"` (line 230),
has no installed command to run. The script is run by its path.

## 2. Install into a project

The agreed line: "A team installs Garura, chooses what it gets, and can take it out again."

### Built

- **One command, from a release or from main.** #568 (installing Garura can pick a release version, not just whatever
  is on main), closed 2026-10-07: "(no --version) install the latest published release" (`install.sh` lines 11-13).
  *State:* Live, one-line installer only. The latest release is v3.0.0, tagged on 2026-10-07 (`CHANGELOG.md` line 3;
  `gh release list`), and `main` is 1,790 commits past it (`git rev-list --count v3.0.0..main`). The v3.0.0 plays
  folder holds the old command set (`agentic`, `arch`, `grill`, `next`, `vision` and 25 more; `git ls-tree v3.0.0`).
  v3.0.0 holds no memory system (no `memory_system.py` and no memory tool in `git ls-tree v3.0.0`), so the
  installer says "This release has no memory system; skipped." (`install.sh` lines 217-220). The fix for #860
  (installed parts read Garura's source at run time, so they break after an install), commit eaedd331 of 2026-10-25,
  is not in v3.0.0 (`git merge-base --is-ancestor`). This is read from git; no install of v3.0.0 was run.
- **Install from a checkout, for a chosen tool, with a record.** install-garura `SKILL.md` lines 36-74; `install.py`
  lines 345-437. The record lists each part and its kind (play, loop, skill or agent), the tools, the config and the
  machine-wide memory path (lines 356-366, 374). *State:* Live, install play only.
- **Choose what the project gets: two kinds.** `full`, "every component except the meta harness plays and the
  harness-only skills", and `harness`, "meta plays + harness-only skills + change chain + discover-capabilities +
  their workers only" (`install.py` lines 15-23). #546 (full scope ships the build plays into projects) is closed.
  #478 (a component-scope option so a project can receive a subset) is still open, though the option is built: it was
  added by direct edit (`SKILL.md` lines 207-212), and its criterion 5, "Play recompiled from its ICE", cannot be met
  because the play has no ICE. This repository: kind `harness`, 10 agents, 32 skills and 20 plays
  (`.garura/install-manifest.json`). *State:* Live, install play only.
- **Lay the memory system and check it.** The memory tool, its settings, short-term memory's folder and the memory
  guide. It brings no memory. The check fails when the tool cannot run or cannot reach short-term or Garura memory;
  Phoenix memory not yet on the machine is reported, not failed (`memory_system.py` lines 3-31; ADR 038 §1 and §2,
  lines 24-35; #660, every install carries the memory tool, a memory guide and a check, closed). *State:* Live.
- **Lay every tool and check it loads.** Every tool under `core/tools/` except `memory`, `play-reviewer` and `naming`;
  each tool gets its packages, and a smoke check stops the install and names a tool that does not load
  (`tools_system.py` lines 3-33; ADR 055 §3, lines 39-49; #860, closed). *State:* Live.
- **Leave out what a project must not get.** Stale and deprecated parts are skipped (`adapters/common.py` lines
  101-128; `install.sh` lines 252-273; #855, mark the old-chain plays stale and keep stale parts out of every install,
  and #833, stop the public installer shipping deprecated parts, both closed). Thirteen plays are stale today
  (`build-epic`, `learn-outcomes`, `refactor-code`, `release-epic`, `release-increment`, `validate-epic` and the seven
  `shape-*-lens` plays). Python caches are still copied, because `copy_tree_fresh` has no ignore (`common.py` lines
  146-150), but ignore files the install writes keep them out of git (`common.py` lines 83-93; `install.py` lines
  179-187). #567 (installing Garura copies Python cache files into the target project) is open. *State:* Live, with
  #567 in part.
- **Keep the team's own instructions file.** The install play writes `CLAUDE.md.new` when a `CLAUDE.md` exists
  (`claude.py` lines 128-138). It writes it again on every install (#782, open). The one-line installer writes over the
  team's file on a first install (`install.sh` line 371). *State:* Live, install play only.
- **Take Garura out again.** The uninstall play removes exactly what the record lists, keeps `.garura/project/` (the
  team's work), keeps the machine-wide memory unless `--purge`, never removes Phoenix memory, and `--dry-run` shows
  what would go (uninstall `SKILL.md` lines 24-65, 82-84). With no record, "there is nothing to remove" (lines 29-31),
  so a one-line install cannot be taken out this way. It removes the settings file even when a person edited it
  (`uninstall.py` lines 167-169). *State:* Live, install play only, run from a checkout.

### Planned only

- **More kinds of install.** A sandbox kind: the harness plus named plays, with their workers found by the installer
  (#843, open). "run" and "code" kinds, named in #948 ("`run` and `code` do not exist yet"), which is closed.
- **Guardrails laid by the install.** Hooks so that no agent does a play's work without the play (#893, open, not
  shaped). #775 (Garura's guardrails ship with the harness, each with a switch) was closed as not planned on
  2026-11-02. BI-3's approved page leans on #893: "Blocking a read with a hook is left to the guardrails the install
  will lay (#893), which the install does not lay today." (`write-work-evals/fn-keep-evals-from-builder/feature.md`
  line 16).
- **One step with no checkout, and a choice of parts.** #513 (install and distribution: getting Garura into a project,
  open, a sub-issue of BI-7's tracker issue): "Someone with no prior exposure to Garura can install it into their
  project in one step, and choose a subset of components while doing so." The first half is built in the one-line
  installer. The second half is built only in the install play.
- **The Phoenix install, once per machine.** #883 (all memory in Garura's source is Phoenix memory: one install lays
  it, initialize gives each project its own blocks, open): "The Phoenix install, once per machine. It lays Phoenix
  memory from the `phoenix-memory` repo". Today the memory tool downloads Phoenix memory the first time it needs it
  (`core/tools/memory/pull.py` lines 8-12). This is the boundary with Memory (BI-10).
- **Stop copying all of memory to the machine.** ADR 038, Negative ("The old machine-wide copy is still laid ... until
  it is retired (#653 item 10)", line 74), and ADR 055 §8 ("It stops when the memory tool is fully live", lines 71-73).

### Earlier designs, closed

- #369 (an npx installer, closed as not planned on 2026-10-03): it asked for the tool and the plays and found each
  play's workers; it kept a hash of every installed file, so that "locally modified components, CLAUDE.md, and core
  files are detected by hash mismatch and preserved across reinstall/upgrade"; it staged, then swapped, with a
  rollback; it merged `settings.json`; and it asked before an uninstall. None of it was built. Several of these ideas
  return in #945, #843 and #938.
- #948 (a team gets Garura into its project and keeps it current, closed as not planned on 2026-11-02, the day BI-7 was
  confirmed). It had four ways (first install, upgrade, what to install, which coding agent). Its proof included "the
  report names every part added, kept, merged, replaced or removed". Its must-not had two halves: "change a part a
  project's people changed without asking them; install anything into Claude Code's or Codex's own settings that the
  person did not agree to". BI-7's page keeps three proofs and the first half of that must-not.

### After the install: Initialize

- `cap-initialize`, "After the install, set a project up for Garura: its memory, its review rules, and its tracker's
  work-item types." (`_spine.yaml` lines 188-223). It is detailed, with ICE on its page and NFR needs, and it has six
  features (lines 889-939). It and every feature have `intents: []`. It is not built: "`initialize` (not built yet)"
  (install-garura `SKILL.md` lines 97-98).
- Its page draws the line with the install: "Out: the Garura install, which runs once per project and lays only the
  pieces (the plays, agents, skills, tools and the memory tool) and no memory. Initialize starts where that install
  stops, so a project has no Garura memory of its own until initialize runs, and the two never write the same files."
  (`initialize/capability.md` line 21).
- In the tracker, #862 (a project gets only the memory and the review rules that fit it: initialize asks after the
  install) is a sub-issue of BI-7's tracker issue. #881 and #883 sit under #862. ADR 066 §5: "Initialize, seeding
  memory and upgrade are engine things, not plays." (line 87). Initialize is not on BI-7's agreed list.

## 3. Upgrade a project

The agreed line: "A project moves to a new version knowing what changes, including its model, without losing its own
work. It is an engine thing, like installation, not a play."

### Built

- **Run the installer again.** The one-line installer finds `.garura/core/config.yaml`, switches to upgrade
  (`install.sh` lines 72-77), shows "From: ... To: ..." (lines 408-415) and ends with what it overwrote and what it
  kept (lines 481-497). A re-run of the install play is the same install, which "re-lays the components in place"
  (`SKILL.md` lines 166-173). There is no upgrade play and no upgrade tool. *State:* Live; each installer shows
  something different.
- **Say what changes, per release.** `CHANGELOG.md` has a hand-written entry for each release: what it set out to do,
  what it delivered and the known issues at the tag (lines 3-39, 41-54). The release workflow makes a GitHub release
  with generated notes on each `v*` tag (`.github/workflows/release.yml` lines 3-20). Releases are cut by hand:
  "Cutting a release stays a manual step." (#568, scope boundary). The changelog has no entry after v3.0.0, so 1,790
  commits on `main` have no notes, and `--version main` gets none. During an upgrade, the one-line installer names the
  two versions, and the install play lists the parts it retired (`install.py` lines 469-470). Neither says what changed
  in a part. *State:* Live, at the level of a release only.
- **Remove what Garura dropped or renamed.** The install play removes what the last record listed and this install did
  not lay again (`install.py` lines 440-471). It removes a part under an old name from the rename map only when its file
  still says `name: <old name>` (lines 474-513). #747 (installs follow the renames) and #748 (an install removes old
  names and lays the new ones) closed on 2026-10-21. ADR 046: "An install removes a component left under its old name
  when Garura placed it." (lines 81-82). A project last installed before the record existed keeps dropped parts (#938,
  open). The one-line installer removes nothing, so a dropped play still shows as a command and runs its old way (the
  case #938 describes). *State:* Live, install play only.
- **Keep what the team changed.**
  - The settings file is kept whole by both installers (`install.py` lines 394-401; `install.sh` lines 459-464). New
    settings never arrive. In this repository the installed settings file has 181 lines against the source's 223. It
    has no `trackers`, `plans`, `loops` or `shape-slice` section, and still holds two `product:` keys and
    `review-change: off` (line 168), the old play name of #772 (the install keeps old play names in the project
    config, so the check-change gate is on; open).
  - The memory tool's settings that a person edited are kept (`memory_system.py` lines 18-21; tests at
    `test_install.py` lines 188 and 1148).
  - `CLAUDE.md` is kept, with `CLAUDE.md.new` beside it, in both installers.
  - Claude Code's own settings, `.claude/settings.json`, are not touched (`install.sh` line 497; #945's table).
  - The team's own parts beside Garura's are never touched: "Only manifest-recorded paths are candidates — the user's
    own skills/files are never touched" (`SKILL.md` lines 169-172).
  - The team's work in `.garura/project/` and its product model are kept.
  - Not kept: an installed Garura part that a person edited is replaced whole (`claude.py` line 114 calls
    `copy_tree_fresh`, `common.py` lines 146-150). The play's rule is "Never hand-edit an installed copy" (`SKILL.md`
    lines 193-194). The shared folder `.claude/skills/_shared/` is removed and laid again whole (`common.py` lines
    75-76). The machine-wide memory copy is merged, "overwriting overlapping files" (`common.py` lines 153-156). A
    learned gate policy is lost when its play is renamed: "a project's learned policy for a renamed play starts again
    under the new name" (ADR 046, lines 96-97).
- **Upgrade the model.** No install changes a model. #813 (upgrading Garura moves a project's product model to the
  Feature names, and scripts stop on old keys), closed: "The install does not change an existing product model
  (product owner, 2026-10-23, review of PR #834)." Every script that reads the model stops on an old name and tells a
  person to run the move script (`model_names.py` lines 41-54, the same file in 17 plays). The move script,
  `migrate_model.py`, moves a model made before #807 to the Feature names in one commit, and puts everything back when a
  step fails (lines 3-41). "A person runs this script by hand; nothing runs it on its own" (lines 6-7). It sits in the
  install play's folder, which no project gets, so a team must run it from a checkout. It moves one rename only. The
  spine does not record which shape of the model it follows: its top keys are `domains`, `capabilities`, `features`,
  `profile`, `slices` and `ices`, while the ontology is at version 15 (Phoenix memory
  `standards/schemas/product-os/ontology.md` line 3). So an upgrade can tell an older model only by its old names.
  *State:* Live by hand, for one rename.

### Planned only

- #945 (a reinstall brings a project up to date without losing what its people changed; open, "not to be built
  now"). For each part it knows what was laid last time, what people changed since and what is new. It adds what is
  new, keeps what a person changed, replaces what only Garura wrote, removes what Garura no longer has and merges
  settings. "It shows the person what it will do before it does it, and reports what it did." Done means: "No part is
  overwritten that a person changed, unless the person says so."
- #946 (every settings file other than `config.yaml` lives in one config folder, and each setting names who reads it)
  and #947 (settings named for plays and tools that are gone are renamed or removed). Both open, for later.
- #938 (remove dropped parts with no install record), #772 (settings keys follow the renames), #782 (write `.new` only
  when a rule is missing). All open.
- #835 (a person on an older Garura or product model can upgrade to a new version; an open business intent with no
  plan). Its questions: "Who may change a project's product model during an upgrade, and with whose yes?"; "Does an
  upgrade change only the structure (keys, file names, headings), or also meaning?"; "Is the upgrade a step of the
  install, its own play, or a script a person runs?"; "How does a person see what changed, and undo it?". ADR 066 §5
  and the agreed line answer the third in part: not a play.
- #921 and #966 (Phoenix memory versioned per release, with its own notes; open). This is the boundary with Memory
  (BI-10).

### Neither

- Undoing an upgrade. #835 asks it; nothing is designed.
- A record, in a project, of which Garura version the install play laid.

## 4. Support each coding tool

The agreed line: "Each team gets an install built for its tool: Claude Code, Codex, GitHub Copilot, Antigravity or
Factory."

- **Claude Code.** The adapter is built (`claude.py` lines 1-19). Agents keep their model, with `best` and `deep` read
  as `opus` (lines 29-39). Skills, plays and loops are laid as skills, with the model line dropped, because "A Claude
  skill has no model field" (lines 15-16). The memory guide is a rules file that "loads at launch, for every session
  and every custom sub-agent" (`memory_system.py` lines 12-14). There are no machine-wide settings to write (lines
  141-143). *State:* Live. It is the only tool that gets an install today.
- **Codex.** The adapter was built, and fixed in July 2026 by pull requests #503, #504 and #505 (`CHANGELOG.md` line 22). It lays skills
  under `.agents/skills/`, lays every agent as a skill because Codex has no named sub-agent, sets the model in
  profiles in the Codex home because it cannot be pinned per skill, and cuts descriptions at 1,024 characters
  (`codex.py` lines 9-29). It never writes over a Codex settings file that exists (lines 233-258). Its memory guide is
  a marked block in `AGENTS.md` (`memory_system.py` lines 15-16). It was stopped on 2026-10-25: "`--tool codex` stops
  with a plain message and writes nothing. The Codex installer is redesigned in #863." (ADR 055 §7, lines 67-69;
  `install.py` lines 78-89). #863 (Codex projects get a Garura install built for Codex, open) says the adapter leaves
  out each play's `reference/` folder, and is done when a Codex install lays every part a play needs, passes the
  installed-layout lint and passes the empty-project install test. ADR 055, Negative: "People who use Codex cannot
  install Garura until the Codex installer is redesigned (#863)." (line 99). The one-line installer never had Codex.
  *State:* Stopped; the redesign is Planned only (#863).
- **Factory.** It was supported once, for Factory Droids. #123 (briefs recipe, sync-droids skill and Factory Droid
  support, closed 2026-03-24): the skill "Transforms Claude Code agent definitions into Factory Droid format (tool
  names, model IDs, frontmatter)". #256 removed the `.factory/` tree (closed 2026-04-19), and #430 removed the sync
  skills on 2026-05-31 (commit 64f3ace9). What is left behind: `core/config.yaml` lines 50-58 ("Factory Droid derived
  locations (populated by /sud:install factory adapter)"), which no script reads (#947); and `AGENTS.md` lines 3 and
  18-34, written "to Factory Droids" and naming a factory adapter that does not exist. *State:* Removed. Nothing plans
  it.
- **GitHub Copilot.** Nothing is built, and no issue names it (issue titles and bodies searched for "copilot").
  A person's brief kept in the model names it: "IDE integrations (Claude Code, Copilot, Cursor, Codex CLI, Factory.ai)"
  and "Installers (npm, Claude Code, Copilot)" (`.garura/product/user-provided/project-brief.md` lines 45 and 51, read
  through the memory tool, Garura tier). The review shelf counts `COPILOT.md` among files that point at other files
  (Phoenix memory `knowledge/review/config-maps.md` line 6). *State:* Neither.
- **Antigravity.** No mention in the repository, in any memory tier or in any issue (searched). Only the agreed line
  names it. *State:* Neither.
- **What the tools share.** One seam for the model: a part's `model:` hint folds to deep, standard or fast, and each
  adapter maps that tier onto its tool (`common.py` lines 11-39). Seventeen agents carry a model (12 `sonnet`, 4
  `opus`, 1 `haiku`). Seventy-five skills and plays carry one too, and the Claude Code adapter drops it on every one.
  The settings file points at each tool's install folders (`install.py` lines 137-142). The naming standard forbids
  the built-in commands of Claude Code and Codex only (ADR 046 line 48; Phoenix memory `standards/rules/naming.yaml`
  lines 59-61). The source is written in Claude Code's terms: "Source files use Claude Code tool names" (`AGENTS.md`
  line 34).
- **Per-tool parts planned elsewhere.** A Claude Code status display, "a plugin installed only when the install
  chooses Claude Code" (Phoenix memory `standards/rules/run-status.md` lines 9-10; ADR 041, Work This Creates, item 4).
  Claude Code hooks for the guardrails (#893). A loop's checker can be Codex (`core/config.yaml` lines 119-130); that
  uses Codex beside Claude Code, and installs nothing for it.

## 5. The model today for BI-7

- No domain, capability, feature, slice or ICE names `bi-7` (count of spine parts by intent; BI-7's page says "What was
  done: (nothing yet)").
- `cap-747`, "Installs follow the renames" (`_spine.yaml` lines 142-153), directional, no domain, issue 747, and its
  feature `fn-748`, "An install removes old names and lays the new ones" (lines 832-843). Both name `bi-734` (Garura
  publishes a standard for building agentic harnesses; its tracker issue #734 is closed). Their ICE is a section on
  their own pages, and they have no entry in `ices`. Built (section 3).
- `cap-initialize` and its six features (section 2), with `intents: []`. Not built.
- The tracker and the model disagree. BI-7's tracker issue (#7 in the intents tracker) has four sub-issues: #513
  (install and distribution), #862 (initialize), #747 (installs follow the renames) and #973 (Garura's docs and command
  pages stay in step with what ships). In the model, #862's capability names no intent and #747's names `bi-734`.
- Other parts name the upgrade: `bi-788` (the shaping loop) excludes "the upgrade of an older product model (#835)"
  (`intents/bi-788.md` line 18), and `bi-734`'s proof includes "an install leaves no old name behind in a project"
  (`intents/bi-734.md` line 9).

## 6. ADRs and docs that decide install, upgrade, layout and tool support

- **ADR 017** (the `.garura/` folder whitelist), amended by ADRs 035, 038, 039 and 055: what may sit in `.garura/`.
- **ADR 021**: the install lays the status ignore file and records it, and the uninstall reverses it (lines 68-69).
- **ADR 035 §8** (lines 90-94): "Every install carries the memory system". Its §2 starting set was removed by ADR 038.
- **ADR 038** (the install brings no memory): §1, the install lays the tool, its settings and the guide, and checks
  them; §2, Phoenix memory arrives on first use; §3, `initialize` sets up a project's own memory (an engine thing since
  ADR 066); §4, the tool lives in the project. Negative: "`initialize` does not exist yet" (line 72) and "A tool fix
  reaches a project only when Garura is installed there again." (line 75).
- **ADR 039 §5**: the `.garura/` tree, with `install-manifest.json` in it. Amended by ADR 055 for the tools folder.
- **ADR 040**: the settings file's source is `core/config.yaml`; a project's `.garura/core/config.yaml` is the
  installed copy (lines 30-34).
- **ADR 046**: no name is, or starts with, a built-in command of Claude Code or Codex (line 48); an install removes a
  part left under its old name when Garura placed it (lines 81-82); a project's copies change only on the next install
  (lines 94-95); a learned gate policy restarts under a new name (lines 96-97). ADR 066 §6 later allows a name to start
  with a tool's command.
- **ADR 054**: the install lays the skills' shared folder beside the plays' (line 37); without it, the parts that ask a
  person fall back to the play's floor (line 64).
- **ADR 055** (installed parts read only installed files): §1, no installed part names the source; §3, the install
  lays every tool and the agents' shared files; §5, the install and uninstall plays are source-only; §7, Codex is
  stopped until #863; §8, the machine-wide memory copy stays for now.
- **ADR 059**: "A project installed before this change keeps the three plays until its next install retires them."
  (lines 243-244).
- **ADR 066 §5** (line 87): "`/install-garura` and `/uninstall-garura` are product plays with no role. Locking a design
  is a governance check. Initialize, seeding memory and upgrade are engine things, not plays."
- **Docs**: `docs/standards/harness-standard.md` principle 11 (lines 116-137), installed parts never touch the source.
  `README.md` lines 126-231, install, upgrade and install from source. Three docs no longer match what ships:
  `docs/components/plays.md` line 369 ("for a host tool (Claude Code or Codex)"); the glossary's "Global mode" row,
  "The default Garura deployment: components land in" the home folder's `.claude/` (`core/grounding/glossary.md` line
  164), which no installer builds; and the README's project tree, which shows `.garura/project/specs/` and `src/`
  (lines 172-187), while ADR 039 dropped `project/specs/`.

## 7. Memory

Searched through the memory tool with `--issue 1021`, in every tier, for install, upgrade, version, Codex, Copilot,
Antigravity, Factory, coding tool and distribution.

- No tier holds a standard or a knowledge page on installing, upgrading or distributing a harness, or on supporting a
  coding tool. The ten domain shelves (Phoenix memory `knowledge/domains/`) cover product fields such as commerce and
  payments. The nearest page is a release discipline for a product's own data, "Migrations are additive-only per
  release." (Phoenix memory `knowledge/technology/run-environments-canary-migrations.md` line 59), which is about a
  product's database, not a Garura project.
- Phoenix memory names the two verbs: "install: Harness. Put Garura into a project." and "uninstall: Harness. Take
  Garura out of a project." (`standards/rules/naming.yaml` lines 26-27).
- The review shelf runs the linter in the installed layout and notes "(The Codex install, to `.agents`, is stopped for
  now, #863.)" (Phoenix memory `knowledge/review/harness.md` lines 31-32).
- Garura memory holds the person's brief that names Copilot, Cursor and Factory.ai (section 4), and the approved pages
  quoted in section 10.

## 8. What the evidence puts in doubt on BI-7's page

- **"A first install takes one step."** It holds in form: the one-line installer is one command (README lines
  141-148). But:
  - By default that step lays v3.0.0, without the memory system, without the current plays and without the #860 fix
    (section 2). The current Garura needs `--version main`, which is still one step.
  - It holds only for Claude Code.
  - The install play needs a checkout and a command run by its path: more than one step.
  - When Initialize is built, a project has no Garura memory of its own until it runs (ADR 038, line 72: "Until it
    does, every lookup in a new project goes up to Phoenix memory"). Whether that set-up counts as part of the first
    install is not said anywhere.
- **"An upgrade loses nothing the team changed."** It holds for the team's own parts, the values in its settings and
  instructions, its memory tool settings, its work and its model. It does not hold for an installed Garura part a
  person edited, a file put in `.claude/skills/_shared/`, the machine-wide memory copy, or a learned gate policy of a
  renamed play (section 3). An upgrade also brings no new settings (#945, #772), and the one-line installer leaves
  dropped parts in place (#938's case).
- **"Each tool gets what it supports."** One of the five named tools gets an install (section 4).
- **The outcome, "upgrades it knowing what changes".** An upgrade shows two version names or a list of retired parts.
  The changelog has no entry since v3.0.0.
- **What pulls against the must-not, "Change what a project's people changed without asking them":**
  1. The one-line installer's first install writes over a `CLAUDE.md` the project already has (`install.sh` line 371,
     with no check before it). No issue names this.
  2. Both installers replace an installed Garura part whole, with no check for a person's edit (`common.py` lines
     146-150).
  3. The shared folder is removed and laid again whole (`common.py` lines 75-76).
  4. All of memory is merged over the machine-wide copy, which every project on the machine shares (`common.py` lines
     153-156; `install.sh` lines 351 and 456).
  5. The uninstall removes a settings file a person edited without a question; `--dry-run` exists, and the play says
     "Prefer `--dry-run` when unsure" (`uninstall.py` lines 167-169; uninstall `SKILL.md` lines 108-109).
  6. The guardrail hooks of #893 need `.claude/settings.json`, which is the team's own file. No install touches it
     today (#945's table), so laying them means a merge with the team's yes.
  - Not a pull: `--force-config` writes over the settings only when a person passes it, which is asking. The Codex
    adapter never writes over a Codex settings file that exists (`codex.py` lines 233-258).
- **Words that pull against each other.** The agreed line calls upgrade "an engine thing, like installation, not a
  play" (`capabilities.md` line 73), and `names.md` line 33 says the same. But ADR 066 §5 and `names.md` line 30 keep
  `/install-garura` and `/uninstall-garura` as plays ("product plays with no role", "both stay"). ADR 055 §5 and
  `install.py` lines 214-215 make them source-only, so no project ever receives these "product plays".

## 9. Issues, by capability

Open: #513 (install and distribution), #478 (component scope), #843 (sandbox scope), #567 (caches copied), #782
(`CLAUDE.md.new` again), #893 (guardrails laid by the install), #862, #881 and #883 (initialize), #945 (reinstall
keeps what people changed), #946 and #947 (settings folder, stale settings), #938 (remove dropped parts with no
record), #772 (old play names kept in the settings), #835 (upgrade an older Garura or model), #921 and #966 (Phoenix
memory versioned per release), #863 (Codex install redesign), #973 (docs and command pages in step with what ships),
with #529 (the command cheat sheet drifts from the plays) under it.

Closed: #568 (pick a release version), #546 (full scope ships build plays), #660 (memory system in every install),
#860 (installed parts read the source), #855 and #833 (stale and deprecated parts left out), #747 and #748 (installs
follow the renames), #753 and #876 (parts added to the harness scope), #813 (scripts stop on old model names; the move
script), #584 (the installer, config and docs pointed at the old GitHub address), #591 (release v3.0.0), #503, #504
and #505 (Codex install fixes, merged pull requests), #260 (a sync-codex skill), #123 (Factory Droid support), #256 (remove `.factory/`),
#430 (remove the sync plays), #23 (npm install from GitHub, 2026-02). Closed as not planned: #369 (npx installer),
#948 (the old install intent), #775 (guardrails with a switch), #899 (the source, Phoenix memory and the projects stay
in step).

None names GitHub Copilot or Antigravity.

## 10. Where BI-7's parts touch other intents' parts

- **Standards, structure, settings and memory (BI-10).**
  - Structure, "Where everything lives, in source and once deployed": the `.garura/` tree (ADR 039 §5, ADR 055 §3) and
    the installed-paths rule (ADR 055 §1; harness standard principle 11). Structure says where things live; the install
    lays them there, and an upgrade moves them when Structure changes.
  - Settings, "Everything that can be turned on or off lives in settings": #946 and #947 are filed under #513 but
    describe Settings. An upgrade bringing new settings in (#945) is BI-7's; what each setting is, and who reads it, is
    Settings'.
  - Memory: the install lays the memory tool and guide (ADR 038 §1, §4); how they work is Memory's. The Phoenix install
    (#883), Phoenix memory releases (#921, #966) and retiring the machine-wide copy (ADR 055 §8) sit on this line.
  - Intelligent model routing: noted only. The adapters already map each part's tier onto a tool (`common.py` lines
    11-39), and Codex "can't be *pinned*" per skill (`codex.py` lines 18-22).
  - Standards: the naming rule lists only Claude Code's and Codex's built-in commands (ADR 046 line 48). A new tool
    adds its own.
  - Build your own harness: the `harness` kind of install and the source-only build plays (ADR 055 §5).
- **Initialize** (no intent). Approved pages of other intents name it as "the project set-up step": BI-2's
  `design-technology-architecture/capability.md` line 71 and `fn-set-architecture/feature.md` line 25,
  `manage-surfaces/capability.md` line 26, `environment-setup/capability.md` line 116 and
  `deployment-design/capability.md` lines 124-125; BI-4's `check-code-against-standards/capability.md` line 24 and
  `fn-review-each-change/feature.md` line 22; BI-6's `connect-use-and-market/fn-connect-tools/feature.md` line 18.
  None of them says which intent holds it, so moving it changes no word on them.
- **Design → Code (BI-3).** `write-work-evals/capability.md` line 48 and `fn-keep-evals-from-builder/feature.md` line 16
  leave blocking a read of the evals folder to "the guardrails the install will lay (#893)". The test model setting may
  name Codex, and "which model each part runs on belongs to Intelligent model routing"
  (`build-work-test-first/fn-write-failing-tests/feature.md` line 40): Codex used as a second tool, not installed for.
- **Code → Validation (BI-4).** `check-code-against-standards/capability.md` line 139 and
  `fn-send-code-findings/feature.md` line 97 cite #772 (the install keeps old play names in the settings): an upgrade
  defect that the review meets.
- **Orchestration (BI-9).** Its must-not, "Every gate has a way past it that records what's owed", bears on the
  guardrails an install lays (#893; #992, a person is never stopped). A loop's checker may be Codex.
- **Developer tooling (BI-8).** Changes to the installers land through "Ship every change the same way", like any
  change. Nothing more.
- **Product model (BI-11).** The model's shape changes by version (the ontology is at version 15). Defining that shape
  is BI-11's; moving a project's model to the new shape on upgrade is BI-7's, as the agreed line says ("including its
  model"). The model tool (#1030) is BI-11's.
- **The harness standard (`bi-734`, closed).** `cap-747` and `fn-748` (section 5).
- **Validation → Run (BI-5, parked).** The BI-5 inventory placed Garura's own releases with BI-7: "Garura's own
  releases (the version tag, the changelog, the installer) sit with Install and distribute (BI-7)"
  (`bi-5-inventory/inventory.md` line 442).

## 11. Leans

Each is a proposal with its evidence, not a decision.

### Lean 1: one install engine behind both front doors

The two installers differ in more than ten ways (section 1). The one-line installer already runs the play's memory and
tools scripts, "laid by the same script the install-garura play uses" (`install.sh` lines 210-239). The agreed line
calls installation an engine thing (`capabilities.md` line 73), and ADR 066 §5 keeps the two plays.

- **Option A, one engine:** the one-line command and the install play run the same install scripts. The one-line
  install then gets the record, the removal of dropped parts, the kinds of install, the agents' shared files and the
  project's own instructions, and it can be taken out again. The play stays the way to install from a checkout.
- **Option B, keep two installers** and fix each one's gaps separately.
- **Option C, keep only the play.** This loses the one-step install with no checkout, BI-7's first proof.

**Lean: A.** It is the one option that makes the first proof and the must-not hold on the path a new team takes.

### Lean 2: the features of each capability, from the evidence only

Install into a project:
1. Install in one step, from a release or from main, with the version recorded. Built in the one-line installer
   (#568); #513.
2. Choose what the project gets. Built: `full` and `harness`, in the play. Planned: sandbox (#843); "run" and "code"
   are named only in the closed #948.
3. Lay the memory system and the tools, and check they run. Built (ADR 038, ADR 055, #660, #860).
4. Lay the guardrails. Planned (#893). What they guard and how a person gets past one is BI-9's.
5. Take Garura out again. Built in the play, from the record; not for a one-line install.

Upgrade a project:
1. Upgrade in one step, showing the version before and after. Built in the one-line installer (#568).
2. Remove what Garura dropped or renamed. Built in the play (#747, #748); planned for projects with no record (#938).
3. Keep what the team changed, and bring in what is new. Built in part; planned (#945, #772, #782, #946, #947).
4. Move the project's product model to the new version, with the person's yes. Built by hand for one rename (#813);
   planned (#835).
5. Say what changes in each version. Built per release (the changelog, the release workflow); a report of each part
   is planned in #945; Phoenix memory's own notes are planned in #921 and #966.

Support each coding tool, one feature per tool, each laid by its own adapter on one shared core ("The adapter is the
seam", install-garura `SKILL.md` lines 30-34):
1. Claude Code. Built.
2. Codex. Stopped; planned (#863).
3. GitHub Copilot. Neither; named only by the agreed line and the brief.
4. Antigravity. Neither; named only by the agreed line.
5. Factory. Removed; named by the agreed line, the brief and the leftovers in `core/config.yaml` and `AGENTS.md`.

One rule of the install capability rather than a feature: keep the team's own files on a first install (section 8,
pull 1).

### Lean 3: where Initialize goes

- **Option A, BI-7, as its own capability** ("set a project up after the install"), with its six features as they are.
  The tracker already files #862 under BI-7's tracker issue. ADR 066 §5 groups it with upgrade and installation as
  engine things. Its moment is right after the install, and BI-7's outcome is that "A team gets Garura into its
  project". The memory rules it follows stay BI-10's.
- **Option B, BI-10.** It builds the Garura memory tier, and BI-10's Memory says "people control what enters them".
  It also records the review rule groups and the tracker's types, which other intents read.
- **Option C, leave it with no intent** until BI-10 is reviewed.

**Lean: A.** The tracker and ADR 066 already put it beside the install and upgrade. The cost: the agreed list of three
becomes four.

### Lean 4: "Installs follow the renames" joins Upgrade a project

`cap-747` and `fn-748` name `bi-734`, a closed intent, while the tracker files #747 under BI-7. Removing old and renamed
parts is feature 2 of Upgrade a project in lean 2.

- **Option A:** merge `cap-747` into Upgrade a project, so `fn-748` becomes its feature, and repoint the intent to
  `bi-7`. `bi-734`'s proof line stays its own.
- **Option B:** keep `cap-747` as its own capability under BI-7.
- **Option C:** leave it with `bi-734`.

**Lean: A.** It is one job inside the upgrade, and the tracker already puts it under BI-7.

### Lean 5: what the must-not covers for an installed Garura part

- **Option A, an installed part is Garura's.** The upgrade replaces it whole and says so in its report. The must-not
  covers what the team owns: its own parts, settings, instructions, work and model. This is the rule today ("Never
  hand-edit an installed copy").
- **Option B, find the edit and ask.** The record keeps a fingerprint of each laid file (as #369 proposed). An upgrade
  that finds a person's edit to an installed part shows it and asks before replacing it (#945: "No part is overwritten
  that a person changed, unless the person says so.").

**Lean: B.** It is what the must-not's words say, and #945 already asks for it. A also needs the team to know that
edits are lost, which nothing tells them today.

### Lean 6: the model upgrade waits for the person's yes

- **Option A:** the upgrade moves the model's structure only (keys, file names, headings), shows each change and waits
  for the person's yes. It never changes meaning.
- **Option B:** a person runs a script by hand, as now.
- **Option C:** the install moves the model on its own.

**Lean: A.** It answers #835's first two questions in the way BI-7's must-not and BI-11's must-not ("let an agent
confirm an intent") point. For it, the move scripts must be laid where a project can run them. Today `model_names.py`
tells a person to run `<install-garura>/scripts/migrate_model.py` (lines 41-44), which no project has.

### Lean 7: Garura's own releases sit under Upgrade a project

Releases, their versions and their notes are on no agreed list. "Knowing what changes" rests on them, and the BI-5
inventory placed them with BI-7 (line 442). Lean: they are part of Upgrade a project (feature 5 in lean 2), not a fourth
capability.

### Lean 8: the domain

- **Option A, software delivery planning**, with its opening changed to say it also gets Garura into a project. This is
  what was done for BI-6 ("the three capabilities stay in software delivery planning, whose opening now says so",
  commit 153f118f), and `cap-initialize` already sits there.
- **Option B, a domain of its own.** The domain's intent today is to turn "a business intent into working code that a
  check from the outside can prove" (`software-delivery-planning/domain.md` line 4), and installing a harness is not
  that.

**Lean: A**, for one domain until a second is needed, as with BI-6.

### Lean 9: two defects found, to file when the product owner says so

No issue names these. Neither was filed here.
- The one-line installer's first install writes over a `CLAUDE.md` the project already has (`install.sh` line 371).
- The one-line installer does not lay the agents' shared files, which ADR 055 §3 says the install lays. An agent that
  reads memory looks for them in `.claude/skills/_shared/` (`product-os-keeper.md` lines 114-116).

## 12. Open questions (no source answers them)

1. What an "engine thing" is for installation and upgrade: a tool under `.garura/core/tools/`, a step inside the
   installer, or something else. ADR 066 §5, `names.md` line 33 and `capabilities.md` line 73 use the words; nothing
   defines them.
2. Whether "A first install takes one step" includes Initialize, so that a project counts as "in" only once it is set
   up.
3. Which Garura a one-step install should give by default, the latest release or `main`, and how often a release is
   cut. Today releases are cut by hand (#568), and the latest is 1,790 commits behind `main`.
4. Which products "Antigravity" and "Factory" name. Assumed here: Factory means Factory.ai's Droids, from `AGENTS.md`
   line 3 and the brief's line 45. Nothing in the repository or memory names Antigravity. Also, in what order the tools
   come after Claude Code and Codex.
5. Whether a team may edit an installed Garura part and expect an upgrade to keep it. Lean 5 depends on this.
6. Whether a machine-wide install, for every project of one person, is wanted. The glossary calls it the default (line
   164) and `core/config.yaml` keeps `global-claude` (lines 45-48), but no installer builds it.
7. Where #973 (Garura's docs and command pages stay in step with what ships) goes. It is under BI-7's tracker issue,
   but on no agreed list.
