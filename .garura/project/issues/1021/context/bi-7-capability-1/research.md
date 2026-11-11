# Install into a project: research and drafts (issue 1021, BI-7 capability 1)

Draft only. Nothing under `.garura/product/`, `.garura/core/` or `.claude/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-7-capability-1/drafts/product-os/software-delivery-planning/install-into-project/`: the capability page and its ICE page, and six feature pages, each with its ICE page. They sit under software delivery planning for now, beside Initialize, and the capability page says so.

In one line: Garura has two installers that do different things. The one-line command is the one step with no copy of Garura's source, and it picks, records and shows a version, but it keeps no record of what it laid, gives no choice, removes nothing and cannot be taken out. The install play keeps that record, offers two kinds of install, removes what it laid before and no longer lays, and has a take-out play, but it records no version and runs only from a copy of Garura's source. They share two steps: laying the memory system and laying the tools, with their checks. The agreed direction is one install engine behind both.

What this run did besides reading:
- It re-read the lines of the stock-take it relies on (`bi-7-inventory/inventory.md`, sections 1, 2, 8, 9, 10 and 11) against their files: `installer/install.sh` whole; `core/components/plays/install-garura/SKILL.md` whole; `scripts/install.py` whole; `scripts/adapters/common.py` and `claude.py` (the parts that lay components, the shared folder and the instructions file); the headers of `memory_system.py` and `tools_system.py`; the shell installer's tests in `test_install.py`; `project-instructions.md`; `core/components/plays/uninstall-garura/SKILL.md` and `scripts/uninstall.py`; the file list of `core/components/agents/_shared/`; `README.md` lines 126-231; ADR 038, ADR 055, ADR 066 §5, ADR 054 (lines 35-38 and 62-65) and ADR 021 (lines 66-70); `CHANGELOG.md` and the release tags. Every line it relies on held.
- It found one more pull against the decided rule that a first install never writes over a project's own files (defect 3 below).
- It read GitHub, read only: #513, #478, #843, #893, #567, #782, #568 (closed), #945, #369 (closed as not planned), #775 (closed as not planned), #860 (closed) and #938 (title only).
- It searched memory through the memory tool (`--issue 1021`), in Garura memory and Phoenix memory, for install, uninstall, upgrade, distribution, coding tool, host tool, Copilot, Antigravity and manifest. As the stock-take found, no tier holds a standard or a knowledge page on installing, distributing or taking out a harness. Phoenix memory names only the two verbs: "install: Harness. Put Garura into a project." and "uninstall: Harness. Take Garura out of a project." (`standards/rules/naming.yaml` lines 26-27).
- It copied the memory files it decided from into `bi-7-capability-1/memory/`, with `manifest.json`, all from Phoenix memory: the grounding content standard and the capability and feature templates (`standards/schemas/product-os/grounding/`), and the naming rule (`standards/rules/naming.yaml`).
- It did no web research, so no memory update is drafted. Nothing here needed knowledge from outside the project: every feature rests on what is built, on the product owner's words or on an open issue.
- It recorded no decision trace with `memory.py cite`, because that tool writes outside this run's folder.
- It ran no placement: the domain is settled at BI-7's close and is not reopened here.
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## The name

*Install into a project*, folder `install-into-project`: the product owner's own name on the list he set on 2026-11-10 (`capabilities.md` line 72). Kept as it is.

Words the pages use, and why:
- **Front door**: one way a team starts an install. There are two: the one-line command and the install play. Used so that "one engine" reads plainly.
- **Install engine**: the one set of steps behind both front doors. It is how "an engine thing, like installation, not a play" is read, as the product owner agreed.
- **Install record**: the plain name for `.garura/install-manifest.json`, the list of every part and file the install laid.
- **Kind of install**: the plain name for what the code calls a scope (`full`, `harness`).
- **Take out**: the product owner's words for an uninstall ("can take it out again").

## What is built, and what is only planned

Built, in both front doors (they call the same two scripts: "Both install paths call this", `memory_system.py` line 6 and `tools_system.py` line 5):
- **The memory system and its check.** The memory tool, its settings, the memory guide and the folder for short-term memory are laid. The check runs the tool "the way an agent runs it" and fails when it cannot run or reach short-term or Garura memory; "Phoenix memory not downloaded yet is reported, not failed" (`memory_system.py` lines 3-31). The install brings no memory (ADR 038 §1).
- **Every tool, with its packages and a smoke check.** "A tool that does not load stops the install with a message that names it." (`tools_system.py` line 22; ADR 055 §3).
- **Stale and deprecated parts left out.** `install.sh` lines 252-273; `adapters/common.py` lines 119-128: "neither ships to a project".
- **No change to the product model.** "The install never changes a product model the project already has (#813)." (`install.py` line 53); the test `test_the_shell_installer_leaves_a_pre_807_model_unchanged` (`test_install.py` line 1186).
- But the default release of the one-line command, v3.0.0 of 7 October 2026, is older than the memory system and the tools: "This release has no memory system; skipped." (`install.sh` line 219). So the default install today checks nothing.

Built in the one-line command only (`installer/install.sh`):
- **One step, no copy of Garura's source.** One `curl ... | bash` in the project's folder (README lines 141-148).
- **A version, named or the default, recorded and shown.** "install the latest published release" when no version is named (line 13); `--version main` gives the newest work, recorded with its commit (lines 92-96); the version goes to `.garura/core/garura-version` (lines 378-380); "A version that does not exist stops the install with a message; it never falls back to `main`." (README line 164). From #568, closed.
- The default is v3.0.0, 1,790 commits behind main (`git rev-list --count v3.0.0..main`, run 2026-11-10), with no memory system and without the fix of #860 (installed parts read Garura's source at run time; commit eaedd331 is not in v3.0.0, by `git merge-base --is-ancestor`). Releases are cut by hand: "Cutting a release stays a manual step." (#568).

Built in the install play only (`core/components/plays/install-garura/`), which runs from a copy of Garura's source, by its path; no project receives the play itself (`install.py` lines 214-215; ADR 055 §5):
- **The install record**, with each part and its kind, the tools, the settings file and the machine-wide memory path (`install.py` lines 356-366 and 515-522). No version.
- **Two kinds of install**: `full`, the default, "every component except the meta harness plays and the harness-only skills", and `harness`, "meta plays + harness-only skills + change chain + discover-capabilities + their workers only" (`install.py` lines 19-23). The harness list is kept by hand: "kept play gains a new worker, add it there in the same change." (`SKILL.md` line 154).
- **Garura's instructions beside the team's own file**: `CLAUDE.md.new` when a `CLAUDE.md` exists, "never clobber the user's own" (`claude.py` lines 128-138). It lays a short guide to running plays, not Garura's development guide, "which would put how Garura is built into every agent of the project (#689)" (`install.py` line 414).
- **The agents' shared files**, laid in the shared folder with the plays' (`common.py` lines 57-80).
- **Removal from the record**: a re-run removes what the last record listed and this run does not lay, and reports it as `retired:`; "Only manifest-recorded paths are candidates" (`SKILL.md` lines 169-173); a change of kind "retires the out-of-scope components" (lines 151-153).
- **Take-out**, the uninstall play: it removes exactly what the record lists, "never removes a file it cannot prove the installer placed", keeps the team's work, keeps the machine-wide memory unless `--purge`, never removes Phoenix memory, and shows the list on `--dry-run` (uninstall `SKILL.md` lines 24-65 and 82-84). With no record, "there is nothing to remove" (line 31), so a one-line install cannot be taken out. It removes Garura's settings file even when a person edited it (`uninstall.py` lines 167-169).

Planned only (open issues):
- **#513** (install and distribution, a sub-issue of BI-7's tracker issue): "Someone with no prior exposure to Garura can install it into their project in one step, and choose a subset of components while doing so."
- **#478** (a component-scope option): open, though the option is built by direct edit; its criterion "Play recompiled from its ICE, not hand-edited." cannot be met, because the play has no ICE.
- **#843** (a sandbox kind): the harness kind "plus the plays a person names for testing, with each play's own skills and agents found and added"; "The installer finds each named play's skills and agents itself; the person does not list them."
- **#893** (guardrails laid by the install): "The guardrails are laid by the Garura install, so every project that uses Garura gets them, not only Garura's own repo." Not shaped. #775 (guardrails that ship with the harness and can be turned on or off) was closed as not planned.
- **#945** (a reinstall keeps what people changed), for the shape of a re-run that shows first: "It shows the person what it will do before it does it, and reports what it did." Its own job, keeping a person's edits, belongs to Upgrade a project.
- **#567** (Python caches copied): low, and not on the pages.
- A closed design, not built: #369 (an npx installer, closed as not planned) had "Uninstall removes everything but asks the user first" and a fingerprint of each installed file, so that changed files "are detected by hash mismatch and preserved across reinstall/upgrade".

Found and not filed (the two from the stock-take, both re-checked):
1. **The one-line command's first install writes over a project's own instructions file.** It treats a project as new when Garura's settings file is missing (`install.sh` lines 72-77), and then writes `CLAUDE.md` with no check (line 371). No test covers it (the shell installer's tests, `test_install.py` lines 1118-1186).
2. **The one-line command does not lay the agents' shared files.** It copies only each agent's own `.md` file (`install.sh` lines 275-285), so `core/components/agents/_shared/` (`memory-reading.md`, `failure-format.md`, `copy_memory.py`) never reaches the project, though ADR 055 §3 says "The install lays them in the installed `_shared/` folder, beside the plays' shared files." The plays', loops' and skills' shared folders do reach it, because the play and skill loops copy every folder that is not stale.

Found while drafting, and not filed:
3. **Both front doors replace a part of the project's own that has the same name as a Garura part, on a first install.** The install play removes the folder and lays Garura's (`claude.py` line 114 calls `copy_tree_fresh`, `common.py` lines 146-150; an agent file is copied over, `claude.py` line 87), and the one-line command copies over it (`copy_dir`, `install.sh` lines 130-134). The record then names that path as Garura's, so a take-out removes it too. This pulls against the decided rule that a first install never writes over a project's own files.
4. Also seen, and already in the stock-take: the one-line command lays Garura's own development guide, cut down, as the project's instructions (`install.sh` lines 153-208 and 367-372), lays Garura's own build plays and the install plays, because its list of left-out parts is empty (line 18), and makes an empty `src/` folder (line 365).

## The open points: options and a lean

Each is a proposal with its evidence, for the product owner to decide. The pages name each as not decided.

### 1. Which Garura the one step gives by default, and what it shows

- **Option A, the latest release (today).** A fixed version, the same for two people who install a week apart, that a bug report can name. #568's reasons: "if `main` breaks, every new install breaks. Two people who install a week apart get different Garura." The cost: the latest release must be kept current, and today it is v3.0.0, older than the memory system.
- **Option B, Garura's newest work on main.** Always current, but it changes with every merge, so two teams never know they have the same Garura; #568 was filed to stop exactly this.
- **Option C, the latest release, and the install says plainly when it is behind.** As A, and the report names the release, its date, and that newer unreleased work exists, with how to ask for it.
- What it shows, in every option: the version laid, recorded in the project and shown at the end, with the commit when it is main. This is built in the one-line command (lines 92-96 and 380); the install play records no version today.
- **Lean: A.** #568's reasons hold, and the fix for an old default is a current release, which sits with Upgrade a project ("Garura's own releases and their notes sit here", the agreed list of four, item 2). C adds words to the report that have no source in his words; it is a small step if he wants it.

### 2. What a team chooses, and who the choice is for

- **Option A, kinds only.** `full` (the default) and `harness`, plus `sandbox` once built (#843). Simple, and each kind brings its workers.
- **Option B, a kind plus named plays.** Any kind, plus plays a person names, with the install finding each play's workers, which is #843's rule ("the person does not list them") made general. Never a single skill or sub-agent on its own.
- **Option C, any single part.** #478's title asks for "a subset", and #513 for "a subset of components". Most freedom, but a play can arrive without a worker it calls.
- Who it is for: the product owner of a product project, who takes the default; a team that builds its own harness, which takes `harness` (Build your own harness, BI-10); and someone who tests a product play in a harness repository, who adds named plays (#843, asked for by the product owner).
- **Lean: B.** It meets #513's "choose a subset of components" while keeping #843's rule that a chosen play always comes with its workers. The "run" and "code" kinds were named only in the closed #948 ("`run` and `code` do not exist yet"), so the pages do not carry them.

### 3. Taking Garura out: what goes, what stays, and how a person sees it first

- What stays is clear from what is built: the team's work (short-term memory), its product model (no record names it), its own instructions file, its own parts, its coding tool's own settings, Phoenix memory, and the machine-wide copy of memory unless asked.
- **Showing it first.** Option A: every take-out shows the list of what goes and what stays, and waits for the person's yes. Option B: as today, the list only on `--dry-run`, and a plain run removes at once.
- **Garura's settings file after a person edited it.** Option A: ask before it goes. Option B: keep it and say so. Option C: remove it, as today.
- **Lean: show first always, and ask before removing any file Garura laid that a person changed since.** It is what BI-7's Must not says: "Change what a project's people changed without asking them." To know a file was changed, the record needs a fingerprint of each file laid; #369's closed design had one, and #945 asks the install to know "what the project's people changed since". How it knows is left not decided on the page.
- A project with no record, which is every one-line install today, cannot be taken out. With one engine, every new install keeps a record. How an older project gets one is Upgrade a project's (#938); the page says it is not decided here.

### 4. What "one step" includes, and what comes after it

- **Option A, the install alone.** The one step lays the parts, the memory tool and the tools, checks them, keeps the record and the version, and ends by naming the next step, Initialize, once it is built. Initialize's own page draws the line: "Initialize starts where that install stops, so a project has no Garura memory of its own until initialize runs, and the two never write the same files."
- **Option B, install and Initialize as one.** The one command also asks the set-up questions at the end.
- **Option C, the install offers Initialize.** It ends by asking whether to start Initialize now; a no leaves the project installed.
- **Lean: A.** BI-7's proof, "A first install takes one step.", is met by the install alone; Initialize asks the product owner questions, so a step with questions is not the one step; and ADR 038 holds that "install finishes without any memory." C can be added later with no change to the install.

### 5. The defects found and not filed

- **Option A, fold them into the one-engine work.** When the one-line command runs the play's engine, defects 1 and 2 go at once: the play already keeps the team's instructions file and lays the agents' shared files. Defect 3 needs its own change in the engine.
- **Option B, file each as a bug under #513 now**, and fix the one-line command on its own first.
- **Lean: name all three on the pages as not built (done), and file them when the product owner says so**, as bugs under #513, each pointing to the one-engine work that fixes 1 and 2. Defect 1 breaks the Must not today on the path a new team takes, so it is the one to fix first if one is fixed alone. Nothing was filed.

## The persona

- **Lean: the product owner.** No new persona is needed. BI-7 is asked by the product owner; Initialize, which starts where the install stops, already "Serves the product owner who has just installed Garura in a project" (`initialize/capability.md` line 4); and #513 names "Someone with no prior exposure to Garura", which is a first contact, not a role.
- Other options weighed:
  - **The technical lead.** On the approved pages the technical lead designs the work ("who names the plan item and designs the work"). Bringing a harness into a repository is close to how the project is built, but no page so far gives the technical lead a choice about the project's tools.
  - **The devops engineer.** On the approved pages the devops engineer decides the environments and how the project runs; the install works in the project's folder and on the builder's machine, not on an environment.
  - **A new persona, such as a team lead who installs Garura.** It would name the person who runs the command, but no page or issue names such a person, and adding a persona is the product owner's choice.
  - The developer, a person or an agent who builds the code, runs plays after the install; nothing shows the developer choosing what the project gets.
- For the harness kind, the pages say "a team that builds its own harness", which is who that kind serves, not a new persona.

## The features found

Each is a job a person can do inside the capability. Status follows the agreed rule: a part built in one installer only is built in part.

1. **Install Garura in one step, with a record of what it laid** (`fn-install-in-one-step`): one command in the project's folder lays Garura for its coding tool, from the version named or the default, records the version and every part, and writes over no file of the project's own. Built in part: one step and the version in the one-line command (#568); the record, the team's instructions kept and the agents' shared files in the install play; defects 1, 2 and 3 not built. Sources: the agreed line and lean (`page-approvals.md`), BI-7's first proof, #513, #568, `install.sh`, `install.py`.
2. **Choose what the project gets** (`fn-choose-parts`): the team chooses a kind of install, so the project carries the parts it uses and every chosen play runs. Built in part: `full` and `harness`, in the install play only (#478, open); the sandbox kind and named plays planned (#843, #513). Sources: "chooses what it gets", `install.py` lines 15-23 and 194-311, #478, #843, #513.
3. **Check that the installed Garura runs before the team uses it** (`fn-check-install`): the memory tool must run and reach short-term and Garura memory, and each tool must load; what fails is named. Built, in both front doors; the default release is older than it. Sources: `memory_system.py`, `tools_system.py`, ADR 038 §1-2, ADR 055 §3, #860 (closed).
4. **Lay Garura's guardrails with the install** (`fn-lay-guardrails`): the install lays the guardrails that keep an agent from doing a play's work without the play, records them and takes them out with the rest. Not built; planned (#893, open, not shaped). Sources: #893, #945's table, BI-9's Must not, the approved page `write-work-evals/fn-keep-evals-from-builder/feature.md` line 16.
5. **Update what the project gets as the project changes** (`fn-update-parts`): a re-run with a new choice lays what is newly chosen and takes out, from the record, what is no longer chosen and what Garura dropped. Built in part: in the install play only; showing first is not built. Sources: the agreed lean ("removes what Garura dropped"), install-garura `SKILL.md` lines 151-153 and 169-173, `install.py` lines 438-470, #843, #945.
6. **Take Garura out of the project again** (`fn-take-out`): the list is shown, and on the person's yes exactly what the record names goes, while the team's work, its product model and its own files stay. Built in part: in the uninstall play only, from a copy of the source; no take-out for a one-line install; the list only on request; an edited settings file removed with no question. Sources: "can take it out again", uninstall `SKILL.md`, `uninstall.py`, #369 (closed), BI-7's Must not.

Not a feature here, and why:
- Laying the memory system and the tools is part of feature 1 (what is laid) and feature 3 (the check), not a job of its own.
- Releases and their notes, removing renamed parts, the model's move and keeping a person's edits on a reinstall: Upgrade a project.
- Each tool's adapter: Support each coding tool.
- Initialize's six features: Set a project up after the install.
- Python caches copied into a project (#567): a small, low defect, not a job.

## The hand-offs

- **Upgrade a project** (BI-7, next): moving to a new version and knowing what it changes, Garura's own releases and their notes, removing parts Garura renamed, a project installed before the record existed (#938), moving the product model, and keeping a person's edits to an installed part (#945). Install into a project hands it the record and the version.
- **Support each coding tool** (BI-7, next): laying Garura in each tool's own shape, and which tools get an install. This capability names no tool in its rules ("The adapter is the seam."); Claude Code is the one tool that gets an install today, and Codex is stopped (ADR 055 §7).
- **Set a project up after the install (Initialize)** (BI-7, next): the project's own memory, its review rules and its tracker's work-item types. It starts where the install stops.
- **Orchestration (BI-9)**: what a guardrail guards and how a person gets past one.
- **Standards, structure, settings and memory (BI-10)**: what each setting means (Settings); how the memory tool works, when Phoenix memory reaches a machine and when the machine-wide copy of memory stops (Memory); where each part lives once laid (Structure); and who the harness kind serves (Build your own harness).

## Checks

- The structure check (`.claude/skills/discover-capabilities/scripts/lint_grounding.py`) was run on each draft page; the results are in `bi-7-capability-1/checks/lint.json`.
- Every quote in the pages' Sources was checked against its file, its GitHub issue (read only) or its copy in `bi-7-capability-1/memory/`, by a script that looks for each quoted string in its source; the results are in `bi-7-capability-1/checks/quotes.json`.
