# Upgrade a project: research and drafts (issue 1021, BI-7 capability 2)

Draft only. Nothing under `.garura/product/`, `.garura/core/` or `.claude/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-7-capability-2/drafts/product-os/software-delivery-planning/upgrade-project/`: the capability page and its ICE page, and six feature pages, each with its ICE page. They sit under software delivery planning for now, beside Install into a project and Initialize, and the capability page says so.

In one line: there is no upgrade of its own today. A team upgrades by running an installer again. The one-line command names the version before and after and records the new one, but it copies over what is there, removes nothing, writes a new settings file and instructions file beside the team's for a person to merge by hand, and lists only folders it overwrote. The install play takes out what its last record listed and what the rename map shows Garura renamed, but records no version and lists only what it retired. Neither shows anything before it changes it, neither finds a person's edit to an installed part, neither brings a new setting in, and neither moves the product model. One move of the model exists, run by hand from a copy of Garura's source. Garura's releases are cut by hand; the latest, v3.0.0, is 1,790 commits behind main and is the last with notes.

What this run did besides reading:
- It re-read the stock-take's lines it relies on (`bi-7-inventory/inventory.md`, sections 3, 5, 8, 9, 10 and leans 4 to 7) against their files: `installer/install.sh` (the mode, the version, the upgrade branch, lines 60-130 and 395-498); `core/components/plays/install-garura/SKILL.md` (lines 20-215); `scripts/install.py` (its header and lines 340-579: the install, `retire_stale`, `retire_renamed`, the record); `scripts/memory_system.py` (header and `lay`); `scripts/adapters/common.py` and `claude.py` (the whole-copy, the shared folder, the instructions file); `scripts/migrate_model.py` (header); the old-name guard `model_names.py` (22 copies across plays and skills, all alike); the install tests on renames, kept settings and the model; `README.md` lines 195-218; `CHANGELOG.md`; `.github/workflows/release.yml`; ADR 038 (Negative), ADR 046 (§6 and Negative), ADR 055 (§1, §3, §5), ADR 059 (lines 243-244), ADR 066 §5; the installed settings file against the source; the install record's keys; the release tags. Every line it relies on held, with two corrections:
  - The old-name guard is in 22 copies, not 17 (`find core/components -name model_names.py`).
  - The line numbers in `_spine.yaml` moved with capability 1's write: `cap-747` is at lines 142-153 and `fn-748` at lines 848-859.
- It read GitHub, read only: #945, #835, #938, #772, #782, #946, #947, #921, #966, #568 (closed), #813 (closed), #591 (closed, the v3.0.0 release), #747 and #748 (closed), and #369 and #948 (both closed as not planned). It read the commit of #748, 736bbff3.
- It searched memory through the memory tool (`--issue 1021`), in Garura memory and Phoenix memory, for upgrade, release notes, changelog, rename map, install record, version, migration and rollback. No tier holds a standard or a knowledge page on upgrading a harness, versioning it, writing its release notes or undoing an upgrade. What it found:
  - Phoenix memory's branch rule has `release/*` for "Release preparation" (`standards/rules/git.md` line 14), and release branches get "Quality gates elevated to must-have" (lines 32-33).
  - Phoenix memory's naming rule lists `upgrade` among the built-in commands of the coding tools (`standards/rules/naming.yaml` line 221, under `reserved:` at line 62). A side fact only: an upgrade is not a play anyway.
  - Garura memory holds the approved pages of capability 1, which hand this capability its work.
- It copied the memory files it decided from into `bi-7-capability-2/memory/`, with `manifest.json`, all from Phoenix memory: the grounding content standard and the capability and feature templates, the product ontology, the naming rule and the branch rule.
- It did no web research, so no memory update is drafted. Every feature rests on what is built, on the product owner's words, on an open issue or on an old model page.
- It recorded no decision trace with `memory.py cite`, because that tool writes outside this run's folder.
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## The name

*Upgrade a project*, folder `upgrade-project`: the product owner's own name on the list he set on 2026-11-10 (`capabilities.md` line 73). Kept as it is.

Words the pages use, and why:
- **Upgrade**: a run of the one install engine over a project that already has Garura, to a newer version. The product owner's words: "It is an engine thing, like installation, not a play."
- **Install engine**, **front door**, **install record**, **installed part**: as on Install into a project's approved pages, so the two capabilities read the same.
- **Release**: a fixed, named version of Garura (v0.9.0, v2.0.0, v3.0.0), tagged in git and published on GitHub. **Release notes**: what a release changes, written for the teams that install it (today `CHANGELOG.md` and the notes GitHub makes on each tag).
- **Rename map**: the list of every old part name and its new name (`core/components/memory/standards/rules/rename-map.yaml`), which the install play reads.
- **Shape of the model**: the keys, file names, folder names and headings a version of Garura reads in the product model. Used for what #835 calls "the structure", so that "meaning" stays a separate word.
- **Fingerprint**: a short value worked out from a file's content, which changes when the file changes. Used only in the options below and named as not decided on the pages; #369's closed design used one ("An install manifest records every installed file with an MD5 hash").

## What is built, and what is only planned

Built in the one-line command only (`installer/install.sh`):
- **An upgrade is a re-run.** It treats a project as an upgrade when Garura's settings file is there (lines 72-77). Its header calls it "UPGRADE MODE — Non-destructive update" (line 404).
- **From and to.** It shows "From:" and "To:" (lines 413-415), with "unknown (installed before versions were recorded)" when no version file is there (line 408), and ends "Garura upgraded successfully: $PREVIOUS_VERSION -> $INSTALLED_VERSION" (line 482). It records the new version in `.garura/core/garura-version` (line 478). From #568, closed: "An upgrade of an existing install shows which version was there before and which version is there now."
- **A fixed list at the end**: "Updated (overwritten):" agents, skills and plays, and memory; "Preserved (not touched):" the team's work, its settings file, its instructions file and its coding tool's settings (lines 484-497). It is the same list on every upgrade; it names no part.
- **Copies over what is there.** `copy_dir` is `cp -R` into the folder (lines 130-134), so a part Garura dropped or renamed stays, and a file a part no longer has stays inside it.
- **Writes a new settings file and a new instructions file beside the team's**, every time: "Writing config.yaml.new (review and merge manually)..." (line 461) and "Writing CLAUDE.md.new (review and merge manually)..." (line 468). The README: "Review the `.new` files and merge any changes you want to keep." (line 218).
- **Keeps the memory tool's settings a person edited** (the shared memory step, below; the test `test_an_upgrade_keeps_settings_a_person_edited`, `test_install.py` line 1148).

Built in the install play only (`core/components/plays/install-garura/`), run from a copy of Garura's source by its path:
- **A re-run is the upgrade.** "re-running re-lays the components in place and refreshes shared memory, but preserves an existing config unless forced" (`SKILL.md` lines 166-167).
- **Dropped parts go, from the record.** `retire_stale` removes what the last record listed and this run did not lay, and reports each as `retired:` (`install.py` lines 440-471; `SKILL.md` lines 169-173: "Only manifest-recorded paths are candidates").
- **Renamed parts go, by the rename map.** `retire_renamed` (`install.py` lines 474-513, from #748): a part under an old name "is removed once its new name is laid", and "only when its file still says `name: <old name>` — proof Garura placed it". It "covers projects installed before the install manifest existed". Tests: `test_old_names_go_and_the_project_s_own_folders_stay` and `test_every_old_name_of_one_new_name_goes` (`test_install.py` lines 388 and 405). A name mapped to `null` (removed with no successor) has "no new name to lay" (`rename-map.yaml`), so the rename step does not remove it.
- **No version.** The record's `"version": 2` is the record's own format (`install.py` line 519); this repository has no version file.

Built in both front doors (the shared scripts):
- **The memory tool is replaced whole, its settings kept**, and the new copy "is made whole beside the old one, then swapped in: a copy that stops part way leaves the old tool and its settings where they were" (`memory_system.py` lines 116-117; test at `test_install.py` line 200).
- **A tool laid by an older install in an older place is removed**, and its settings written new (`memory_system.py` lines 20-21). This is the one move of Garura's own files to a new place that an upgrade makes today.
- **Neither changes the product model.** "The install never changes a product model the project already has (#813)." (`install.py` line 53); the tests `test_an_install_leaves_a_pre_807_model_unchanged` and `test_the_shell_installer_leaves_a_pre_807_model_unchanged` (`test_install.py` lines 427 and 1186).

Built by hand, outside any install:
- **One move of the model.** `migrate_model.py` moves a model made before #807 to the Feature names: spine and slice keys, path values, folders and files, page headings; "Prose is left alone, and IDs (fn-...) never change." "A person runs this script by hand; nothing runs it on its own" (lines 3-20). It makes one commit, and when a step fails "it puts every file and folder back as it was" (lines 26-31). It sits in the install play's folder, which no project receives.
- **Scripts stop on the old shape.** Every script that reads the model carries the guard `model_names.py`: on an old key it names the key and the file and exits, with "To upgrade the model to the new names, a person runs the script that moves it" and the path `<install-garura>/scripts/migrate_model.py` (lines 41-44), which a project does not have.
- **The model records no shape.** The spine's top keys are `domains`, `capabilities`, `features`, `profile`, `slices` and `ices` (`.garura/product/product-os/_spine.yaml` lines 1, 18, 608, 2481, 2495, 2507); no key names the version of the shape. The ontology carries one in its front matter ("version: 15", Phoenix memory `standards/schemas/product-os/ontology.md` line 3).
- **Releases.** `CHANGELOG.md` has a hand-written entry for each release: what it set out to do, what it delivered, and the known issues at the tag (lines 3-39 for v3.0.0). The workflow makes a GitHub release with generated notes on each `v*` tag (`.github/workflows/release.yml`, `generate_release_notes: true`). #591 (closed) shows how v3.0.0 was cut: a release issue with its blockers, a changelog entry "in plain language", a tag from main, a GitHub release "marked Latest", and "A fresh install with no version given installs v3.0.0". #568: "Cutting a release stays a manual step." The changelog has no entry after v3.0.0, and `git rev-list --count v3.0.0..main` read 1790 on 2026-11-10, so the newest work has no notes, and `--version main` gets none.

Not kept on an upgrade today (each re-checked):
- An installed part a person edited is replaced whole: the install play removes the folder and lays a fresh copy (`claude.py` line 114, `common.py` lines 146-150: "Replace dest with a fresh copy of src"); the one-line command copies over it. The play's rule is "Never hand-edit an installed copy" (`SKILL.md` line 193).
- The shared folder is removed and laid again whole (`common.py` lines 75-76).
- New settings never arrive. In this repository the installed settings file has 181 lines against the source's 223; the source has `loops`, `plans`, `shape-slice` and `trackers` sections the installed one lacks, and the installed one still sets `review-change: off` (line 168), the old name of `/check-change` (#772).
- A learned gate policy is lost when its play is renamed: "a project's learned policy for a renamed play starts again under the new name" (ADR 046, lines 96-97).
- The project's instructions file gets Garura's beside it again on every install, even when it already holds every rule (#782).

Planned only (open issues):
- **#945** (a reinstall keeps what people changed; "not to be built now"): for each part it knows "what it laid down last time", "what the project's people changed since" and "what is new in the source", and from that it will "add what is new, keep what a person changed, replace what only Garura wrote, and remove what Garura no longer has"; for a settings file, "new keys come in, the project's own values stay"; "It shows the person what it will do before it does it, and reports what it did." Done means: "No part is overwritten that a person changed, unless the person says so." and "The report names every part added, kept, replaced, merged and removed."
- **#938** (dropped parts go even with no record): "by the rename map's names mapped to `null`, and by names it can prove it placed (the `name:` line in the part's file), never a file the project owns." Filed as belonging with the capability Installs follow the renames (#747).
- **#772** (settings keys follow the renames): "every config key that holds a play, loop, skill or agent name uses its current name, from the rename map".
- **#782** (the instructions file): "The install writes the `.new` file only when the existing file is missing a rule from the installer's text."
- **#946** and **#947** (Settings, BI-10): one folder for every settings file but `config.yaml`, "Each setting names who reads it", and sections named for parts that are gone. #946: #945 "moves the folder into existing projects", which is this capability's part.
- **#835** (an open business intent with no plan): its four questions; the third is answered ("not a play"), the second is decided for this capability (structure only).
- **#921** and **#966** (Memory, BI-10): Phoenix memory "versioned per release", with "a version that matches the Garura release it goes with, and its own release notes".
- Closed designs, not built: #369 had a fingerprint of each installed file, so that "locally modified components, CLAUDE.md, and core files are detected by hash mismatch and preserved across reinstall/upgrade", and "Atomic install (stage to temp, then swap) with rollback on failure"; #948's proof "the report names every part added, kept, merged, replaced or removed", and "An upgrade over a project whose people changed its settings keeps every changed value."

Neither built nor planned:
- Undoing an upgrade. #835 asks "How does a person see what changed, and undo it?"; no source answers it.
- A version recorded by the install play.
- A record for a project the one-line command installed: it keeps none, so every one-line project is a project with no record.

## The open points: options and a lean

Each is a proposal with its evidence, for the product owner to decide. The pages name each as not decided.

### 1. What "knowing what changes" shows the team, and when

- **Option A, the release notes only.** The upgrade names the two versions and points to the notes of each release between them. Built in part: the two versions, and the notes exist per release. It says nothing about this project: an edited part, a new setting or the model's move are not in the notes.
- **Option B, a list of this project's changes only.** Built from the record and the new version: each part to be added, kept, replaced, merged or removed, each setting to come in, and the model's move, shown before anything changes; the report after names the same (#945; #948's proof). It says what happens, but not why.
- **Option C, both, before anything changes.** The two versions, the notes of each release between them, and the list of this project's changes, shown first; the person's yes; then the report of what was done.
- When the version moved to has no notes, such as Garura's newest work on main today, the list says so; it never makes notes up.
- **Lean: C.** "Knowing what changes" needs the why (the notes) and the what (the list), and #945 already asks that it "shows the person what it will do before it does it, and reports what it did". A alone breaks the Must not's spirit for an edited part; B alone hides why a part is replaced.

### 2. How a person's edit to an installed part is found, and what the person sees and chooses

How it is found:
- **Option A, a fingerprint of each laid file in the install record**, taken when the file is laid, and compared at the upgrade. #369's closed design had one, and Install into a project's take-out already leans on it for the same question. It needs a record, so a project with none falls back to B.
- **Option B, a comparison with the earlier version's own files.** The version a project has is recorded (one-line installs since #568), so the upgrade can fetch that version and compare. It needs no fingerprint, but a fetch of the old version, and it does not work for the install play, which records no version.
- **Option C, the project's history in git**: a file changed since the commit that laid it. Not every project is in git, and Garura does not always commit what it lays (the one-line command commits nothing).
- **Lean: A, with B for a project installed before fingerprints existed.** It is one check for the upgrade and the take-out, which both need it.

What the person sees and chooses, for each edited part:
- What the person sees: the part, what the person changed against what Garura laid, and what the new version changes in it.
- **Option A, three choices for each part**: keep the edited part as it is (the report names it as not moved to the new version), take the new version with the person's copy kept beside it, or stop the upgrade with nothing changed. No choice is made for the person.
- **Option B, one choice for all edited parts at once.** Fewer questions, but one answer may not fit every part.
- **Option C, keep every edited part on its own and say so in the report**, with no question. Fewest questions, but the person may not know an old part now runs beside new ones.
- **Lean: A.** It is what #945 says ("unless the person says so") and what the product owner agreed: "an upgrade finds a person's edit to an installed part and asks before replacing it". Risk to name: a kept part from an older version may not run with the newer parts beside it; the report should say so, and Check that the installed Garura runs before the team uses it (Install into a project) still runs.
- This adds a question to the upgrade, which is a gate. The way past it is the choice to keep the part, which the report records as owed (Orchestration's Must not: "Every gate has a way past it that records what's owed").

### 3. New settings: how they reach the team's settings file while its values stay

- **Option A, a merge in place.** New keys come in with the new version's values; every value the team set stays; a key that names a renamed part follows its new name by the rename map (#772); a key the new version no longer has is shown and removed only on the person's yes (#947 names such keys). The file's comments and order stay, as the model's move keeps them ("The YAML is rewritten line by line, so the file's other content and its comments stay as they are.", `migrate_model.py` lines 19-20). Shown first.
- **Option B, as today: a `.new` file beside the team's**, for a person to merge by hand. Nothing is lost, but nothing new arrives unless a person does the work, and in this repository it has not.
- **Option C, write the new file, then move the team's values into it.** The same result as A for the values, but the team's comments and order are lost.
- New settings files (#946's folder) are laid as new files when the project has none; Garura's instructions are written beside the team's file only when a rule is missing (#782).
- **Lean: A.** It is #945's own words ("new keys come in, the project's own values stay"), and #948's proof ("An upgrade over a project whose people changed its settings keeps every changed value"). What each setting means and who reads it stays with Settings (BI-10).

### 4. The model's move

Which moves exist: one, `migrate_model.py`, for the #807 rename (Functionality became Feature).

How an upgrade tells which shape a model has:
- **Option A, by its old names**, as the guard does today: each move carries its own test of whether it applies, and "Exit 0 when moved or nothing to move" (`migrate_model.py` line 38). Works for a rename; cannot tell a change that adds a required key and renames nothing.
- **Option B, the model records the version of its shape**, for example a mark in the spine set by the last move. Exact, but the mark is part of the model's shape, which is Product model's (BI-11) to define.
- **Option C, the install record keeps the version of Garura that last moved the model.** No change to the model, but the model then does not say its own shape, and a model copied to another project loses it.
- **Lean: A for now, and ask Product model for B.** A is what is built and it works for the one move there is; B is the lasting answer, and it is BI-11's to add.

Where the moves are laid so a project can run them:
- **Option A, laid with every install as a tool**, in the project's own tools folder (ADR 055 §3: "The installer lays each tool under `core/tools/` in `.garura/core/tools/<name>/`"), so the upgrade runs them from there and the guard can name a path the project has.
- **Option B, run by the upgrade from the version it downloaded, and not laid.** Nothing new in the project, but a person who said no at the upgrade has no way to run the move later without a copy of Garura's source.
- **Option C, as today, in the install play's folder**, from a copy of the source only.
- **Lean: A.** Installed parts read only installed files ("A pointer in an installed file points to another installed file.", ADR 055 §1), and the guard's message today points to a script no project has.

How it is shown and confirmed (decided: structure only, shown first, on the person's yes): each key, file, folder and heading to move, shown before; on the yes, one commit, as `migrate_model.py` makes; on a no, nothing moves and the upgrade records the move as owed, so the guard's message is the way past.

### 5. A project installed before the install record existed (#938)

- **Option A, by proof in the file**, as #938's scope says: a part goes when its file still carries the name Garura gave it and the version no longer has it, including names the rename map maps to `null`; never a file the project owns.
- **Option B, by the recorded version.** A one-line install records its version, so the upgrade fetches that version's list of parts and treats a part as Garura's when it matches that version's file. It also gives the earlier files for the edit check (open point 2, option B).
- **Option C, show the person what looks like Garura's and ask.**
- In every option, the upgrade writes the record afterwards, so the next upgrade has one.
- **Lean: B where a version is recorded, else A, and the list shown first in both** (C is the showing step, which every upgrade does anyway). Every one-line install today is such a project, so this is the common case, not the rare one.

### 6. How often releases are cut, and who cuts them

- **Option A, by hand, when the product owner decides** (today; #568: "Cutting a release stays a manual step."), each with its notes, its tag and its GitHub release, and a fresh install checked to get it, as #591 did for v3.0.0.
- **Option B, on a fixed rhythm**, for example once a month. No source asks for it.
- **Option C, on every merge to main.** #568 kept it out of scope ("Set up automatic releases on every merge."), and two teams a day apart would get different Garura, which #568 was filed to stop.
- What a release holds, in every option: the notes in plain words, the version the next upgrade moves to, and, once Memory versions it (#921, #966), the Phoenix memory version that goes with it.
- **Lean: A, with the product owner's yes on the notes.** It is what is decided. How often stays his choice; but while the one-step install's default is the latest release (Install into a project's lean), a release left far behind main gives every new team an old Garura, as v3.0.0 does today. Who writes the notes is not decided; the lean is that the release's own run drafts them from the work since the last release, and the product owner approves them.

### 7. Undoing an upgrade

No source answers it; #835 only asks. The pages name it as not decided. What exists that a later design could use: an upgrade to a named earlier version is possible from the one-line command (`--version v2.0.0`), but it would not put back a merged setting or a moved model; the model's move is one commit, which git can revert; the memory tool keeps the old copy until the new one is whole. No lean.

## The persona

- **Lean: the product owner**, for every feature, as on Install into a project. BI-7 is asked by the product owner; the decisions in an upgrade are the product owner's (whether to keep an edited part, whether the model moves, which settings to drop); and the product model's meaning is a person's, which is why it moves only on a yes. For cutting a release, the persona is the product owner of Garura itself, who decides when a release is cut and approves its notes.
- Other options weighed:
  - **The technical lead.** The model's move and the settings are close to how the project is built, but no approved page gives the technical lead a choice about the project's tools or its model.
  - **The devops engineer.** Releases sound like running a service, but a Garura release is a version teams install, not an environment; on the approved pages the devops engineer decides the environments and how the project runs.
  - **The developer.** A person who edited an installed part may be a developer, and is the one whose edit is kept; but the choice about it is shown to the person who runs the upgrade.
  - **A new persona, such as a maintainer of Garura, for the release.** No page or issue names one, and adding a persona is the product owner's choice.

## What of "Installs follow the renames" (cap-747) and fn-748 is kept

What the two old pages hold (`.garura/product/product-os/capabilities/cap-747/capability.md` and `features/fn-748/feature.md`, each ten lines, with the ICE as a section on the page):
- cap-747: "an install in a project that already has Garura removes the old names and lays the new ones, using the rename map."; Goal "A project never ends up with an old and a new name side by side."; Limit "Removes only components Garura installed."; Fails if "an install leaves an old-name folder next to its new one."; Checked by "install over a test project with the old names leaves only the new ones."
- fn-748: "install-garura reads the rename map, removes each old-name component it installed, and lays the new one; uninstall-garura knows both names."; Goal "Installed projects follow the renames with no manual clean-up."; Limit "Never removes a component the project wrote itself."; Fails if "an old-name component survives an install."; Checked by "an install test over a project with old names: only new names remain, project files untouched."

Kept:
- The job: on an upgrade, a part under an old name goes once its new name is laid, from the rename map. It is fn-748's job, now one feature of Upgrade a project.
- The id `fn-748` and its issue #748 (closed), so the tracker link holds. The draft sits at `upgrade-project/fn-748/`.
- Both limits, as one rule: only a part whose file proves Garura laid it is taken out, never one the project wrote.
- cap-747's goal, as fn-748's: no old name beside its new one.
- Both checks, as acceptance criteria: an upgrade over a project with old names leaves only the new ones, and the project's own files are untouched. It is what the built tests check.

Changed:
- The title becomes the job a person does: "Take out the parts Garura renamed or dropped" (it was "An install removes old names and lays the new ones").
- It gains what the same job needs: parts Garura dropped, which go through the step Install into a project's "Update what the project gets" already uses; a project with no record (#938); and the one-line front door, which removes nothing today.
- It is shown first, like every change of an upgrade.
- "uninstall-garura knows both names" is dropped: it was not built (commit 736bbff3 changed only `install.py` and its test), and taking Garura out is Install into a project's "Take Garura out of the project again", whose open point on a project with no record covers it.
- Config keys that name a renamed part are named here and owned by "Bring in new settings, keeping the team's values" (#772).
- Its ICE moves from a section on its page to its own ICE page beside it.
- Its intent moves from bi-734 to BI-7. bi-734's proof line "an install leaves no old name behind in a project" stays bi-734's own words.

What the write will need (for the product owner's yes, not done here):
- Repoint cap-747 and fn-748 from bi-734 to bi-7 before the merge. The removal skill's merge says "The survivor gains the intents it lacks", so merging first would add bi-734 to Upgrade a project.
- Fix the line on `features/fn-725/feature.md` (line 50) that names cap-747 ("then cap-742 and cap-747 still need cap-739"), because the removal skill refuses while a page still names a part being removed.
- cap-747 needs cap-739 (`depends_on`); the merge moves its links to the survivor, so Upgrade a project would need cap-739 (the naming checks). Whether to keep that link is a choice at the write.
- fn-748's page sits in the holding folder `features/fn-748/`; whether it moves beside its capability, as the drafts place it, is a choice at the write.

## The features found

Each is a job a person can do inside the capability. A part built in one front door only, or by hand only, is built in part.

1. **Move the project to a new version, seeing first what it changes** (`fn-upgrade-in-one-step`): one run of the install engine over the earlier install shows the two versions, the notes between them and the list of this project's changes, and on the person's yes moves it, records the version and reports what changed. Built in part: the two versions and the recorded version in the one-line command (#568); the list of retired parts in the install play; nothing shown before; no yes. Sources: the agreed line, #568, #945, #948 (closed), `install.sh` lines 404-497, `install.py`.
2. **Cut a Garura release, with notes on what it changes** (`fn-cut-release`): the product owner of Garura cuts a fixed, named version from main with notes in plain words, so an upgrade has a version to move to and a team can read what it changes. Built in part, by hand: `CHANGELOG.md`, the tag and the release workflow; no notes since v3.0.0. Sources: the agreed lean ("Garura's own releases and their notes sit here"), #568, #591 (closed), `CHANGELOG.md`, `release.yml`, Phoenix memory `standards/rules/git.md`.
3. **Take out the parts Garura renamed or dropped** (`fn-748`, merged from cap-747): on an upgrade, a part under an old name goes once its new name is laid, and a part the new version no longer has goes, each only when the record or the file proves Garura laid it. Built in part: in the install play (#747, #748, closed); not in the one-line command; not for a project with no record (#938). Sources: cap-747 and fn-748's pages, `install.py` lines 440-513, ADR 046, #938.
4. **Keep a person's edits to an installed part** (`fn-keep-edits`): the upgrade finds each installed part a person changed since it was laid, shows the change, and asks before replacing it. Not built: an edited part is replaced whole. Sources: the agreed lean, #945, BI-7's Must not, #369 (closed).
5. **Bring in new settings, keeping the team's values** (`fn-bring-new-settings`): new settings keys and settings files arrive, every value the team set stays, keys that name a renamed part follow its new name, and Garura's instructions go beside the team's file only when a rule is missing. Built in part: values kept whole in both front doors, a `.new` file beside in the one-line command, the memory tool's settings kept; new keys never arrive. Sources: #945, #772, #782, #946, #947, `install.py` lines 394-401, `install.sh` lines 459-471.
6. **Move the product model to the new version's shape, on the person's yes** (`fn-move-model`): the upgrade shows each key, file name, folder and heading of the model that the new version reads differently, and on the person's yes moves them, never the meaning. Built in part, by hand: one move for one rename (#813), and the guard that stops on the old shape. Sources: the agreed lean, #835, #813 (closed), `migrate_model.py`, `model_names.py`.

Not a feature here, and why:
- Undoing an upgrade: no source plans it; #835 asks. Named as not decided.
- A whole upgrade that stops part way leaving the project as it was: a rule of feature 1, built today only for the memory tool and the model's move.
- Phoenix memory's own versions and notes (#921, #966): Memory's (BI-10). A release names the Phoenix memory version it goes with once there is one.
- Moving the machine-wide copy of all memory: Memory's (BI-10).
- Each coding tool's shape on an upgrade: Support each coding tool.
- Setting the project up again when a new version asks something new: Initialize's "Run initialize again".

## The hand-offs

- **Install into a project** (BI-7, approved): the install engine, its two front doors, the install record and the version it keeps are this capability's inputs. Its "Update what the project gets as the project changes" is the step through which a dropped part goes on an upgrade. Its "Take Garura out of the project again" has the same open point as this capability's edit check (a fingerprint of each laid file), and leaves a project with no record to this capability. Its "Install Garura in one step" leans on the latest release as the default, which this capability's releases must keep current.
- **Support each coding tool** (BI-7, next): laying each part in each tool's own shape on an upgrade, and which tools an upgrade serves. This capability names no tool in its rules. Today only Claude Code gets an install, and the Codex adapter "never writes over a Codex settings file that exists" (stock-take section 4).
- **Set a project up after the install (Initialize)** (BI-7, next): the project's own memory, its review rules and its tracker's work-item types. An upgrade never writes them, as the install never does ("the two never write the same files"). When a new version changes what Initialize asks, running it again is Initialize's "Run initialize again" (fn-rerun-initialize); whether the upgrade's report names it as the next step is not decided.
- **Standards, structure, settings and memory (BI-10)**: what each setting means and who reads it (Settings, #946, #947); how Phoenix memory is versioned and reaches a machine, and the machine-wide copy (Memory, #921, #966); where each part lives (Structure), which an upgrade follows when it changes.
- **Product model (BI-11)**: the model's shape itself, and a mark of its version in the model if one is added.
- **Orchestration (BI-9)**: each question an upgrade asks is a gate with a way past it that records what's owed.

## Checks

- The structure check (`.claude/skills/discover-capabilities/scripts/lint_grounding.py`) was run on each draft page; the results are in `bi-7-capability-2/checks/lint.json`.
- Each ICE page was checked for its shape (one Goal, the Limits and Fails if, the fixed Read line, Never read, Persona, Scope, a Scenario and a Done means checked by someone other than the doer, and the thin mark only where the part is not built); the results are in `bi-7-capability-2/checks/ice-shape.json`.
- Every quote in the pages' Sources was checked against its file, its GitHub issue (read only) or its copy in `bi-7-capability-2/memory/`, by a script that looks for each quoted string in its source; the results are in `bi-7-capability-2/checks/quotes.json`.
