# Feature: Keep `.garura/` to its written list, and check it

## What it does
A project's `.garura/` folder holds only what its written list names, and a check compares the folder with the list, so a person and an agent know where each thing in it is, and a file in the wrong place is seen.
- What the written list holds, as ADR 039 (every memory write goes to short-term memory) drew it and later decisions changed it:
  - `core/`: the settings file `config.yaml`, `engine-state.json`, Garura memory in `memory/`, and the laid tools in `tools/`, one folder for each;
  - `product/`: the product model, with its pages and its spine;
  - `project/issues/`: short-term memory, one folder for each issue, with "only 5 structure keys": specs, evidence, checkpoint, context and review;
  - `project/plans/`: one file for each plan and its folder, added by ADR 049 (a slice is shaped, then planned, then given its eval);
  - at the top: the install record `install-manifest.json`, `defect-report/` and `user-provided/`.
- The list is drawn in three places: the tree of ADR 039 §5, which ADR 017 (the `.garura/` folder whitelist) points to; `docs/components/memory.md`; and the glossary's Whitelist row.
- Where the disk disagrees with the list, from a listing of this repository's `.garura/` on 2026-11-11:
  - The plans folder. ADR 049 adds it to the list in words, the settings name it, and it holds seven plan files. None of the three drawn layouts names it.
  - Garura memory and git. ADR 039 says: "`.garura/core/memory/` is Garura memory. It is kept in git, not ignored." `.gitignore` line 152 still ignores it, and `CLAUDE.md` line 28 says "They are gitignored." The folder is not there in this repository.
  - `engine-state.json`. The list keeps it in `core/`, and the file is there, but no script in `core/` or `installer/` reads or writes it.
  - The old global gate ledger. `.garura/core/gate-evals.jsonl` is kept in git with 4 lines, while the gate rule says a ledger "at `.garura/core/gate-evals.jsonl`, is not read". `defect-report/evidence/` holds run records with no issue around them.
  - Folders that are not issues. Short-term memory also holds `_adr`, `_plans`, `_start` and `capture-report`, and each issue's folder holds a `status/` folder. None of them is among the five keys.
  - A file no list names. The install writes `.garura/.gitignore`, which keeps the run status markers out of git.
  - The check that is gone. A rule in Phoenix memory says: "`write-evidence` skill validates every write path against the six stage folders + three lifecycle folders. Writes outside this whitelist are rejected." No skill of that name is among Garura's 74 skills, and two of the six folders it names left the layout with ADR 050 (the retired intent-epic pipeline is deleted).
- Nothing checks the folder against the list today. The glossary calls the list "a design-time contract enforced in the skill", and that skill is gone.
- In Garura's own repository, `.garura/` is an installed copy. So a fix to the list, or to the folder, is built in the install's source, never by hand in `.garura/`.
- Examples, in different kinds of project:
  - In a clinic's booking app, a play starts to write its records in a new folder at the top of `.garura/`; the check names the folder, and that the list does not hold it.
  - In a bank's payments service, a decision adds a folder for the team's plans; the list gains it in the same change, and the check passes.
  - In an open-source library, the check finds an old ledger file that nothing reads, and names it for a person to move or drop.
- How it meets the capability: `.garura/` is where Garura keeps everything it holds in a project, and its list is the written "where".

Status: built in part. The list is written, in three places that all leave out the plans folder and disagree with the disk, and no check runs. Not built, or open:
- One list that the three written layouts agree on, with the plans folder in it.
- The check of `.garura/` against the list.
- Each disagreement above, fixed in the list or on the disk.

## Inputs / Outputs
- In: the written list of `.garura/`, and the decisions that change it.
- In: the folders and files in a project's `.garura/`.
- Out: one list, with each folder and file and what it holds.
- Out: the check's report, which names each folder or file the list does not hold.

## Rules & behavior
- `.garura/` holds only what its list names. The reason: "The `.garura/` tree allows ONLY these folders."
- An issue's folder holds the five keys. The reason: "Per ADR 017, only 5 structure keys are permitted: specs, evidence, checkpoint, context, review."
- A new folder joins the list by a decision. The reason: ADR 049 added the plans folder that way: "This adds `plans/` under `.garura/project/`, which the folder list of ADR 017 §1 does not name."
- A tool checks the list, not a person's care. The reason: ADR 017 says "Folder compliance is checked once, automatically, at the write boundary".
- In Garura's own repository, a change to the list is built in the install's source. The reason: "An ADR about `.garura/` is built in the install's source, not by hand here."
- Not decided: whether the check runs at the install, in the review of each change, or when a play writes into `.garura/`.
- Not decided: whether the check warns or stops a change, and what its way past records.
- Not decided: whether `engine-state.json` stays on the list.

## Acceptance criteria
- Given a project's `.garura/` that holds only what the list names, when the check runs, then it passes. This is not built.
- Given a folder at the top of `.garura/` that the list does not name, when the check runs, then it names that folder. This is not built.
- Given the three written layouts, when a person reads them side by side, then they name the same folders, and the plans folder is among them. This is not built.
- Given a decision that adds a folder to `.garura/`, when it is accepted, then every written layout gains the folder in the same change. This is not built.

## Out of scope
- What the product model holds inside its folder. Product model owns it.
- What may enter Garura memory. Memory, in Standards, structure, settings and memory, owns it.
- Where settings files other than `config.yaml` go. Settings, in Standards, structure, settings and memory, owns it.
- Which parts of `.garura/` a review reads. Check the code against its standards, in Code → Validation, owns it.
- Keeping each run's records with its issue. Keep each run's records with its issue, with only repository paths in them (fn-run-records-with-issue) does it.
- The way past the check, once it stops a change. Give every gate a way past, in Orchestration, owns it.

## Sources
- The capability list: "Structure: Where everything lives, in source and once deployed."
- The stock-take of Standards, structure, settings and memory (2026-11-11), sections 3.3 and 3.6, and Lean 4: "Keep `.garura/` to its written list, and check it. Built as ADRs and docs; out of step; no check."
- docs/adr/017-folder-whitelist.md, line 24: "The `.garura/` tree allows ONLY these folders."; line 136: "The `write-evidence` skill (214.1) validates every write against the whitelist.", "Folder compliance is checked once, automatically, at the write boundary"; line 3, its status line, with each amendment
- docs/adr/039-memory-writes-go-to-short-term-memory-plays-read-no-memory.md, lines 74-96, §5 "The `.garura/` layout"; line 93: "`engine-state.json` stays where it is, in `core/`."; line 94: "`.garura/core/memory/` is Garura memory. It is kept in git, not ignored."
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md, line 8: "under `.garura/project/` the whitelist gains `plans/`"; line 47: "This adds `plans/` under `.garura/project/`, which the folder list of ADR 017 §1 does not name."
- docs/adr/050-the-retired-intent-epic-pipeline-is-deleted.md: the product folders `specification/` and `scope/` leave the layout, as ADR 017's status line records
- docs/adr/055-installed-parts-read-only-installed-files.md, line 7: `.garura/core/tools/` holds every tool the install lays, one folder for each; line 81: "ADR 039 §10 made its whitelist the tree of ADR 039 §5."
- docs/components/memory.md, lines 81-105: "The `.garura/` folder (ADR 017, as amended by ADR 039)"
- core/grounding/glossary.md, line 107, the Whitelist row: "The whitelist is a design-time contract enforced in the skill, not filesystem permissions."
- core/config.yaml, line 67: "Per ADR 017, only 5 structure keys are permitted: specs, evidence, checkpoint, context, review."; lines 70-71: the plans folder, `.garura/project/plans/`
- .gitignore, line 152: `.garura/core/memory/`
- CLAUDE.md, line 28: "`.claude/` and `.garura/core/memory/` are NO LONGER tracked in the repository. They are gitignored."
- .garura/CLAUDE.md, lines 11-12: "An ADR about `.garura/` is built in the install's source, not by hand here."
- core/components/plays/install-garura/scripts/install.py, line 408: the install writes `.garura/.gitignore`
- standards/rules/gate-config.md, in Phoenix memory, line 59: "a ledger written before this, at `.garura/core/gate-evals.jsonl`, is not read"
- standards/rules/product.md, in Phoenix memory, line 67: "The `.garura/product/` tree uses six stage folders: `user-provided/`, `specification/`, `scope/`, `architecture/`, `experience/`, `research/`."; line 71: "`write-evidence` skill validates every write path against the six stage folders + three lifecycle folders. Writes outside this whitelist are rejected."
- A listing of `.garura/` on 2026-11-11: seven plan files in `project/plans/`; `core/` with `config.yaml`, `engine-state.json`, `gate-evals.jsonl` and `tools/`, and no `memory/`; `_adr`, `_plans`, `_start` and `capture-report` among the issue folders; a `.gitignore` at the top
- A search of `core/` and `installer/` on 2026-11-11 for `engine-state`: named only in the glossary, read or written by no script
- A listing of core/components/skills/ on 2026-11-11: 74 skills and the shared folder, none named `write-evidence`
