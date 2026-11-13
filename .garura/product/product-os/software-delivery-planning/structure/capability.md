# Capability: Structure

## Directional intent
Structure: Where everything lives, in source and once deployed.
These are the agreed words for the third capability of Standards, structure, settings and memory. On 2026-11-11 the product owner took the proposed list and its answers as approved: "continue as most of this is based on built. please proceed with creae pages and ICE as per the process and standards and consider them approved. show me only when you are ready for commit and cp". So this page is written from what Garura has built, and what is not built is drafted from the issues and gets a thin ICE. Two readings of the line are made plain here, as the proposed list said: "deployed" means installed in a project, and a run's records are part of "everything". The words this page uses:
- A part is one play, loop, sub-agent, skill, script, shared file or tool. A play is a command a person or an agent types to run one piece of work from start to end. A loop is a command that runs plays in rounds until its goal is met.
- The source is where Garura's parts are written: the `core/` folder of Garura's own repository, with the installer beside it. The installed copy is what an install lays in a project: the parts in the coding tool's own folder, such as `.claude/` for Claude Code, and Garura's own folder, `.garura/`.
- Deployed means installed in a project. A project is a team's repository with Garura installed in it. In Garura's own repository, `.garura/` is an installed copy too: "But `.garura/` in this repository is the installed copy. It is what an install laid here. The source is `core/`."
- The written list of `.garura/` is the list of the folders and files that folder may hold. The decision records call it the whitelist.
- An issue folder is the short-term memory of one piece of work, `.garura/project/issues/<issue>/`. A run's records are what a play run writes there: its context, its checks, its evidence, its review records and its gate records.

This capability does three jobs that are built, one of them in part:
- Lay out Garura's source: one folder for each kind of part, one for the tools, the memory source and the one settings file.
- Lay out an installed project: where each part lands, the shared files, the tools and the memory guide. Built for Claude Code.
- Keep `.garura/` to its written list, and check it. The list is written; it is out of step with the disk, and nothing checks it.

And one job that is not built:
- Keep each run's records with its issue, with only repository paths in them.

Structure says where each thing lives; the other capabilities of this intent say what it is. Standards says what each kind of part is and how it is built, and holds the checks, among them the linter's rule that an installed part names no path in the source. Settings says what each setting means, who reads it, and where each settings file other than the one settings file goes. Memory says what enters each tier of memory, keeps the memory tool, and decides when the install stops writing the machine-wide copy of all memory.
Approved pages of other intents already hand this work here. Install and distribute leaves "where each installed part lives (Structure)", "where each part lives (Structure)" and "where each part lives once laid (Structure)" to this capability, and lays what it defines: "the install lays what they define". Give every gate a way past, in Orchestration, leaves "Where each run's records live in its issue's folder" here, and keeps the skip records and what is owed for itself.
It matters because Garura's parts and people find each other's files by path. A part that reaches into the source "works only inside Garura's own repository, and fails everywhere else", and a run's records are "the audit trail of the work": "A record kept where nothing reads it is lost without anyone noticing". It sits in software delivery planning with the other capabilities of Standards, structure, settings and memory, and the domain's first paragraph says so.

Features:
- Lay out Garura's source: where each kind of part, tool, memory and setting lives (fn-source-layout): Garura's own repository keeps each kind of part in one known folder under `core/components/`, each tool under `core/tools/` and the settings in `core/config.yaml`, so a developer knows where a part goes and the install knows where to take it from.
- Lay out an installed project: where each part lands, the shared files, the tools and the memory guide (fn-installed-layout): an install lays every part in one fixed place in the project, so each installed part finds the others by an installed path and never needs Garura's source. Built for Claude Code.
- Keep `.garura/` to its written list, and check it (fn-garura-folder-list): a project's `.garura/` folder holds only what its written list names, and a check names each folder or file the list does not hold. Built in part: the list is written, and no check runs.
- Keep each run's records with its issue, with only repository paths in them (fn-run-records-with-issue): everything a play run writes goes in the folder of the issue whose work made it, nothing goes in a global file, and every path in the records starts at the repository's root. Not built.

What is not built yet:
- No one written map says where every part lives, in the source and once installed. The nearest are `CLAUDE.md`'s "Architecture", `docs/components/memory.md` and the harness standard's principle 11.
- A tool is not a kind of part of its own. The harness standard's table of the parts has no row for a tool, and a `core/components/tools/` folder is planned for tools as a first-class component.
- The written list of `.garura/` disagrees with the disk in several places, among them the plans folder, which no drawn layout names; `.gitignore` line 152, which still ignores `.garura/core/memory/` against ADR 039 (every memory write goes to short-term memory); and `engine-state.json`, which no script reads.
- Nothing checks `.garura/` against its list. The skill a rule in Phoenix memory names as its check, `write-evidence`, does not exist.
- Some runs keep their records outside any issue's folder: the decision play's runs and the plan sessions. An old global gate ledger is still kept.
- Plays write home-folder paths into the run records they commit.
- Only Claude Code has an install. The Codex install is stopped; an install built for Codex is planned.
- The install still writes a machine-wide copy of all memory in the home folder (ADR 055 §8, the machine-wide memory copy stays for now).

### Benefit hypothesis
- Who it serves: the developer, a person or an AI agent who builds the code, who adds a part or a tool and must know where it goes; the technical lead, who keeps the layout; every play, sub-agent and skill that finds another part or a record by its path; the product owner and every person who reads what a run did and decided; and the capabilities of Install and distribute, which lay what this capability defines.
- What we believe: when every kind of thing has one written place, in the source and once installed, and every run's records sit in their issue's folder with only repository paths, parts find each other in any project, an install works where there is no source, and a person finds what each run did with its work, if the work stands on these rules:
  - Each kind of thing has one written place, and the settings name it.
  - An installed part names only installed files.
  - The installed copy is never edited to make a change.
  - What a piece of work writes goes under its issue, and no record is kept in a global file.
  - A path in a run record starts at the repository's root.
- How we will know: the component linter finds no installed part that names a path in the source; the written layouts of `.garura/` agree with each other and with the disk, and the check of `.garura/` finds nothing off the list; and every committed run record sits in its issue's folder and holds no home-folder path.
  - The first holds on the source today: the component linter found no installed-path error on 2026-11-11.
  - The other two do not hold today: the layouts disagree with the disk, no check of `.garura/` exists, and committed run records hold home-folder paths.

### Boundary (In / Out / Never)
- In: where each kind of part, each tool, the memory source and the one settings file live in Garura's source.
- In: where each installed part lands in a project: the parts, the shared files, the tools, the memory guide, the settings file and the install record.
- In: the written list of what `.garura/` may hold; and, not built yet, its check.
- In, not built yet: each run's records in its issue's folder, with only repository paths in them.
- Out: what each kind of part is and how it is built, the naming rule, and the checks of the standard, such as the component linter and its rule that an installed part names no source path. Standards, in Standards, structure, settings and memory, owns them.
- Out: what each setting means and who reads it, and where settings files other than the one settings file live. Settings, in Standards, structure, settings and memory, owns them.
- Out: what may enter each tier of memory, how the memory tool finds it, Phoenix memory's place on the machine, and retiring the machine-wide copy of all memory. Memory, in Standards, structure, settings and memory, owns them.
- Out: building parts in a team's own repository. Build your own harness, in Standards, structure, settings and memory, owns it.
- Out: laying the parts, choosing what a project gets, the install record's own shape and the check that the installed Garura runs. Install into a project, in Install and distribute, owns them.
- Out: each coding tool's own folders, and how a part is shaped for each tool. Support each coding tool, in Install and distribute, owns them.
- Out: the record of each skipped checkpoint, what is owed, and the way past any gate, such as a check of `.garura/` once it stops a change. Give every gate a way past, in Orchestration, owns them.
- Out: the scan that stops a push holding a home-folder path. Ship every change the same way, in Developer tooling, owns it.
- Out: which parts of `.garura/` a review reads. Check the code against its standards, in Code → Validation, owns it.
- Out: what the product model holds inside its folder. Product model owns it.
- Out: keeping a plan's evals from everyone who builds the work. Write the evals that check the work, in Design → Code, owns it.
- Never: let an installed part read, run or name a path in Garura's source. The reason: "When an installed part runs, it never reads, runs or names a path under `core/components/` or `core/tools/`."
- Never: edit the installed copy to make a change. The reason: "Nothing under it is edited to make a change."
- Never: keep a run's records in a global file. The reason: "Nothing is written to a global file."
- Never: write a home-folder path into a run record. The reason: "No client reference and no personal reference — not in files, not in history".

### Guiding rules
- A part takes its paths from the settings, never from a path fixed inside it. The reason: the settings file says of short-term memory's paths: "All agents, plays, and skills resolve these from config — never hardcode paths."
- The issue governs: what a piece of work writes goes under its issue. The reason: "Everything a piece of work writes goes under its issue".
- A shared place gets a written structure first. The reason: if a record ever has to be global, it gets a defined structure first (where it sits, what it holds, who reads it), written as a rule; and in the product owner's words: "why do we need a global evidence.. if we do then we need to create a proper structure".
- A pointer in an installed part points to an installed file. The reason: "A pointer in an installed file points to another installed file."
- A change is made in the source, and an install carries it to a project. The reason: "A change is made in `core/`."
- In Garura's own repository, a decision about `.garura/` is built in the install's source. The reason: "An ADR about `.garura/` is built in the install's source, not by hand here."
- Not decided: whether tools become a kind of part of their own, in `core/components/tools/`, or stay in `core/tools/`.
- Not decided: whether the planned harness layout of `core/components` is still wanted; it was planned before ADR 066 (names say who does the work, five roles own the verbs).
- Not decided: where a run keeps its records when it has no issue of its own yet, such as a decision recorded by hand, or when it works on a whole plan, such as a plan session.
- Not decided: whether the check of `.garura/` warns or stops a change, and what its way past records.

## Sources
- The capability list: "Structure: Where everything lives, in source and once deployed."; the product owner on 2026-11-11: "continue as most of this is based on built. please proceed with creae pages and ICE as per the process and standards and consider them approved. show me only when you are ready for commit and cp"; "Pages and ICE are drafted from what is built and taken as approved by these words"
- The stock-take of Standards, structure, settings and memory (2026-11-11), Lean 1, item 3: "Its page says "deployed" means installed, and that a run's records are part of "everything"."; Lean 4, the four features; sections 3.1 to 3.6, 7.3, 9 and 10 (item 5: "One written map of where every part lives, and a check that `.garura/` holds to it."); section 1.5: "No naming, memory or installed-path error."
- .garura/product/product-os/intents/bi-10.md, line 3: "the structure says where everything lives"
- docs/adr/040-config-source-is-core-config-yaml.md, line 19: "But `.garura/` in this repository is the installed copy. It is what an install laid here. The source is `core/`."; line 39: "Nothing under it is edited to make a change."; line 40: "A change is made in `core/`."
- docs/adr/055-installed-parts-read-only-installed-files.md, line 33: "When an installed part runs, it never reads, runs or names a path under `core/components/` or `core/tools/`.", "A pointer in an installed file points to another installed file."; §8, line 73: "It stops when the memory tool is fully live and Phoenix memory is the home of memory."
- docs/adr/039-memory-writes-go-to-short-term-memory-plays-read-no-memory.md, line 94: "`.garura/core/memory/` is Garura memory. It is kept in git, not ignored."
- .gitignore, line 152: `.garura/core/memory/`
- .garura/CLAUDE.md, lines 11-12: "An ADR about `.garura/` is built in the install's source, not by hand here."
- docs/standards/harness-standard.md, lines 13-20: the table of the parts, with no row for a tool; line 138: "works only inside Garura's own repository, and fails everywhere else."
- core/config.yaml, line 66, on short-term memory's paths: "All agents, plays, and skills resolve these from config — never hardcode paths."
- standards/rules/gate-config.md, in Phoenix memory, line 49: "Everything a piece of work writes goes under its issue"
- standards/rules/product.md, in Phoenix memory, line 71: "`write-evidence` skill validates every write path against the six stage folders + three lifecycle folders."
- .garura/product/product-os/software-delivery-planning/install-into-project/capability.md, line 65: "where each installed part lives (Structure)", "the install lays what they define"
- .garura/product/product-os/software-delivery-planning/upgrade-project/capability.md, line 64: "where each part lives (Structure)"
- .garura/product/product-os/software-delivery-planning/support-coding-tools/capability.md, line 63: "where each part lives once laid (Structure)"
- .garura/product/product-os/software-delivery-planning/give-every-gate-a-way-past/fn-keep-what-is-owed/feature.md, line 57, and fn-record-every-skip/feature.md, line 49: "Where each run's records live in its issue's folder. Structure, in Standards, structure, settings and memory, owns it."; fn-record-every-skip/ice.md, line 7: "where a run's records live stays with Structure"
- The product owner on 2026-10-28: "why do we need a global evidence.. if we do then we need to create a proper structure"
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. A search of Phoenix memory on 2026-11-11 for a folder or repository layout finds only the product rule's "Rule 8: Stage-Centric Folder Layout" (standards/rules/product.md, line 63), which is out of step (fn-garura-folder-list), and knowledge/review/harness.md, line 31, which says only where a review finds the installed parts: "The installed target is `.claude`."
- .garura/product/product-os/software-delivery-planning/domain.md: the domain this capability sits in; its first paragraph does not name the capabilities of Standards, structure, settings and memory yet.
- .garura/product/product-os/software-delivery-planning/domain.md: "It also keeps the foundation every part stands on: the written standards and their checks, the builders a team uses for its own plays and loops, where everything lives, the settings, three tiers of memory, and the model each part runs on."
