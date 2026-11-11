# Feature: Keep each run's records with its issue, with only repository paths in them

## What it does
Everything a play run writes goes in the folder of the issue whose work made it, nothing goes in a global file, and every path written in the records starts at the repository's root, so a person finds what each run did and decided with its work, and no record shows where a file sits on a person's machine.
- A run's records are its context, its checks, its evidence, its review records and its gate records. #969 (every run's records kept in its issue's evidence folder) says: "What a run did and decided is kept with the issue that made it, not in a global file." It is filed under Standards, structure, settings and memory in the tracker.
- What exists today, for the records of a run:
  - Each issue has its own folder in short-term memory, with five keys: specs, evidence, checkpoint, context and review.
  - Each issue keeps its own gate ledger, in its `review/` folder, and the gate rule says: "Everything a piece of work writes goes under its issue".
- What is still open, for the records of a run:
  - Some runs keep their records outside any issue's folder. The decision play's working folder is "`{stm_base}_adr/<run-ts>/` — fixed, not keyed on the issue, because run by hand pre-flight runs before start-change has created it"; 31 such folders, with 390 files, are kept in git. A plan session keeps its records in `_plans/update-plan/<id>/`.
  - The old global gate ledger, and the defect reports' evidence folder, hold run records with no issue (#943, gate records live in the evidence folder of the issue that made them).
  - Gate records go in the issue's `review/` folder today, while #943 (gate records live in the evidence folder of the issue that made them) and #969 (every run's records kept in its issue's evidence folder) name the issue's evidence folder.
  - Plays write home-folder paths into the run records they commit (#982, plays write a home-folder path into run records; #914, run records carry the person's home-folder paths). That issue names where: the component linter's output, the plan play's gather script, the eval play's place and check scripts, the self-review's rules file, and the template manager's manifests. So "every change that lands publishes the person's user name and folder layout."
- Examples, in different kinds of project:
  - In a bank's payments service, a decision recorded by hand writes its brief and its checks in the folder of the issue it decides, not in a shared folder with no issue.
  - In an open-source library, the linter's record names each file by its path from the repository's root, so a push of the record shows no user name.
  - In a game studio's build, a person reads one issue's folder and finds every checkpoint answer its runs gave, with nothing in a global file.
- How it meets the capability: a run's records are part of "everything", and this is where they live.

Status: not built (#969, every run's records kept in its issue's evidence folder; #943, gate records live in the evidence folder of the issue that made them; #982, plays write a home-folder path into run records). All three are open. Not built, or open:
- The records kept outside an issue's folder, in `_adr` and `_plans`.
- The old global gate ledger, and the defect reports' evidence with no issue.
- Home-folder paths in committed run records.

## Inputs / Outputs
- In: a play run, with its issue, or with no issue yet.
- In: each path the run writes into a record.
- Out: every record of the run in its issue's folder.
- Out: each path in a record, written from the repository's root.

## Rules & behavior
- What a run writes goes under its issue. The reason: "Everything a piece of work writes goes under its issue".
- No record is kept in a global file. The reason: #943 (gate records live in the evidence folder of the issue that made them) asks that "Nothing is written to a global file.", and in the product owner's words: "eval aka records should go in evidence folder that is it. why do we need a global evidence.. if we do then we need to create a proper structure".
- A path in a record starts at the repository's root. The reason: #982 (plays write a home-folder path into run records) expects that "Every path a play writes into a run record is relative to the repository root, or uses `~` for the home folder."
- Not decided: where a run keeps its records when it has no issue of its own yet, such as a decision recorded by hand, or when it works on a whole plan, such as a plan session.
- Not decided: whether gate records move from the issue's `review/` folder to its evidence folder.
- Not decided: whether a path in the home folder may stay in a record in its `~` form, as #982 (plays write a home-folder path into run records) allows, or is left out.
- Not decided: whether the 4 lines of the old global ledger move into the issues they belong to or are dropped; #943 (gate records live in the evidence folder of the issue that made them) names both.

## Acceptance criteria
- Given a run for issue 12, when it ends, then every record it wrote is in issue 12's folder and none is in a global file. This is not built.
- Given a decision recorded by hand before its issue exists, when the run ends, then its records are in the folder of the issue it belongs to. This is not built.
- Given a run record that names a file, when it is written, then the path starts at the repository's root and holds no home folder. This is not built.

## Out of scope
- The scan that stops a push holding a home-folder path. Scan every push for client, company and personal references (fn-scan-every-push), in Ship every change the same way, does it.
- The record of each skipped checkpoint. Record every skipped checkpoint, even when the evidence file is off (fn-record-every-skip), in Give every gate a way past, does it.
- What is owed, and its one list. Keep what is owed with the work that made it, and read it back as one list (fn-keep-what-is-owed), in Give every gate a way past, does it.
- Whether a run writes its evidence file. Settings, in Standards, structure, settings and memory, owns the evidence setting.
- Which records a review reads (#939, the reviews leave out the agents' working records). Check the code against its standards, in Code → Validation, owns it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 112: "Structure: Where everything lives, in source and once deployed."
- .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 3.4 and 3.5, and Lean 4 (lines 918-919): "Keep each run's records with its issue, with only repository paths in them. Planned (#969, run records in the issue's evidence folder; #943, gate records there; #982, no home-folder paths)."
- GitHub #969 (open), every run's records kept in its issue's evidence folder: "What a run did and decided is kept with the issue that made it, not in a global file."
- GitHub #943 (open), gate records live in the evidence folder of the issue that made them: "Nothing is written to a global file.", "A gate record goes in the evidence folder of the issue whose run made it (today the rule names the issue's `review/` folder).", and the product owner on 2026-10-28: "eval aka records should go in evidence folder that is it. why do we need a global evidence.. if we do then we need to create a proper structure"
- GitHub #982 (open), plays write a home-folder path into run records: "Every path a play writes into a run record is relative to the repository root, or uses `~` for the home folder."
- GitHub, read on 2026-11-11: the parent of #969 (every run's records kept in its issue's evidence folder) and of #982 (plays write a home-folder path into run records) is BI-10, "Standards, structure, settings and memory", in the intents tracker.
- GitHub #914 (open), run records carry the person's home-folder paths: "every change that lands publishes the person's user name and folder layout."
- core/config.yaml, lines 73-82: short-term memory and its five keys; line 222: "ledger: .garura/project/issues/{issue}/review/gate-evals.jsonl"
- standards/rules/gate-config.md, in Phoenix memory, line 49: "Everything a piece of work writes goes under its issue"
- core/components/plays/record-decision/SKILL.md, lines 89-91: "`<working>` is `{stm_base}_adr/<run-ts>/` — fixed, not keyed on the issue, because run by hand pre-flight runs before start-change has created it"
- core/components/plays/update-plan/SKILL.md, lines 72-73: the session folder, `${stm_base}_plans/update-plan/<id>/`
- A count on 2026-11-11: 31 run folders in `.garura/project/issues/_adr/`, with 390 files kept in git
- .garura/product/product-os/software-delivery-planning/give-every-gate-a-way-past/fn-keep-what-is-owed/feature.md, line 57, and fn-record-every-skip/feature.md, line 49: "Where each run's records live in its issue's folder (#969). Structure, in Standards, structure, settings and memory, owns it."
- .garura/product/product-os/software-delivery-planning/ship-every-change/fn-scan-every-push/feature.md, line 15: "The plays write every path in their records relative to the repository's root, so the scan finds nothing to stop in a clean run."
