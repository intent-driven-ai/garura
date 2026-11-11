# Feature: Map every old name to its new one, and check that no old name is left

## What it does
One file maps every old name of a part to its new name, and a check searches the repository for any old name still used outside past records, so a rename is called done by a check, not by reading it.
- The rename map, `rename-map.yaml`, lists the old and new names of plays, loops, skills and sub-agents. "A name mapped to `null` was removed with no successor: the check still reports it." The first two are `build-knowledge` and `review-knowledge`, removed with ADR 059.
- The old-name check, `check_old_names.py`, reads the map and searches the source, the docs, the installer and the top-level guides:
  - an old name with a `-` in it, such as `review-change`, is found anywhere as a whole word;
  - an old name of one word, such as `vision`, is found only where it can mean the part: as a command, a part's folder, a play field, or the words "`vision` play", because "A one-word old name (vision, run, quality) is an everyday word, so plain prose is not searched for it."
- Past records keep their old words: "Past records keep their old words and are not searched: .garura/, CHANGELOG.md, the ADRs before ADR 046, and ADR 046 and ADR 048 (they record the renames)." ADR 053 and ADR 059 are left out too, because they quote older words and "An accepted ADR is not edited".
- It only reads: "Read only: no git, no network, no LLM." It exits 0 when no old name is left and 1 when some are, with each file and line.
- The rename tool, `apply_renames.py`, reads the same map, moves each part to its new name and changes every reference the check finds: "Names and references only: no behaviour changes."
- The install reads the same map: a part a Garura install laid under its old name "is removed once its new name is laid". This is how Take out the parts Garura renamed or dropped (fn-748), in Upgrade a project, works, and why this feature keeps its id.
- Examples, in different kinds of project:
  - In a bank's payments service, the team renames the play `pay-check` to `check-payment`. The map gains the line, and the check lists the three guides that still name the old play until they are changed.
  - In a clinic's booking app, a play is removed with no successor. The map marks it `null`, and the check still finds a guide that names it.
  - In a harness repository, an old ADR names an old play. The check leaves it, because an accepted ADR is not edited.
- How it meets the capability: this is one of the "checks that hold" the naming standard: a rename is done when the check says so.

Status: built, in `rename-map.yaml`, `check_old_names.py` and `apply_renames.py`, by #741 (a rename map, and a check that no old name is left, closed), before any family was renamed. Not built, or open:
- On 2026-11-11 the check exits 1: 12 uses of 9 old names, in ADR 062 and `docs/philosophy/intent-and-adlc.md`.
- The handling of a name removed with no successor has no test: "Neither behavior has a test in `core/tools/naming/test_naming_tools.py`; both were checked by hand only." (#936, open).
- ADR 066's renames are not in the map; they join it with the rename.
- No play runs the check; a person runs it by hand. The harness standard says to run it "for any name changed by the rename map".

## Inputs / Outputs
- In: the rename map, which pairs every old name with its new name.
- In: the repository's source, docs, installer and top-level guides.
- Out: the check's report: each use of an old name, with its file, its line, the old name and the new one, and its exit code.
- Out: from the rename tool, the parts moved to their new names and their references changed.

## Rules & behavior
- One map holds every rename. The reason: "`core/tools/naming/check_old_names.py` fails while any old name is still used outside past records."
- A rename is done when the check passes, not when someone reads it. The reason: "a change judged by reading it is a change nobody proved."
- The check is built before the rename and fails first. The reason: "The check that proves a change is done is built before the change, and it is run first against today's code, where it must fail."
- A name removed with no successor stays in the map. The reason: "`null` keeps the old name caught by the old-name check; the install has no new name to lay."
- A one-word old name is searched only where it can mean the part. The reason: "A one-word old name (vision, run, quality) is an everyday word, so plain prose is not searched for it."
- Past records keep their old words. The reason: "An accepted ADR is not edited (only a forward pointer may be added), so the check does not search these."
- The check only reads. The reason: "Read only: no git, no network, no LLM."

## Acceptance criteria
- Given a guide that names an old play with a `-` in its name, when the old-name check runs, then it exits 1 and names the file and the line.
- Given an ADR before ADR 046 that names an old play, when the check runs, then it does not report it.
- Given a name mapped to `null` that a guide still names, when the check runs, then it reports the guide.
- Given a name mapped to `null`, when the tests of the naming tools run, then one test shows the check reports it and one shows the rename tool runs clean. This is not built.
- Given ADR 066's names in the map and the rename landed, when the check runs, then it exits 0. This is not built.

## Out of scope
- Taking out a part under an old name in a project. Take out the parts Garura renamed or dropped (fn-748), in Upgrade a project, does it.
- The naming rule itself. Name every part by one rule, with five roles owning the verbs (fn-736) does it.
- Each family's rename. Rename the harness plays and the loop to the standard (fn-743), and the three other rename features (fn-744, fn-745, fn-746), do it.
- The other checks. Check every part against the standard (fn-740) does them.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 117: "fn-741 keeping its id for BI-7's fn-748"
- core/components/memory/standards/rules/rename-map.yaml, lines 1-3 and 23-26: "A name mapped to `null` was removed with no successor: the check still reports it.", "`null` keeps the old name caught by the old-name check; the install has no new name to lay."
- core/tools/naming/check_old_names.py, lines 5-23 and 46-49: "A one-word old name (vision, run, quality) is an everyday word, so plain prose is not searched for it.", "Past records keep their old words and are not searched: .garura/, CHANGELOG.md, the ADRs before ADR 046, and ADR 046 and ADR 048 (they record the renames).", "Read only: no git, no network, no LLM.", "An accepted ADR is not edited (only a forward pointer may be added), so the check does not search these."
- core/tools/naming/apply_renames.py, lines 3 and 12: "move every component to its new name and update every reference (#743-#746)", "Names and references only: no behaviour changes."
- core/components/plays/install-garura/scripts/install.py, lines 472-480: "is removed once its new name is laid"
- docs/standards/harness-standard.md, lines 62-65 and 164-165: "The check that proves a change is done is built before the change, and it is run first against today's code, where it must fail.", "a change judged by reading it is a change nobody proved.", "for any name changed by the rename map"
- docs/adr/046-one-naming-standard-for-every-harness-part.md, lines 80-81: "`core/tools/naming/check_old_names.py` fails while any old name is still used outside past records."
- .garura/product/product-os/_spine.yaml, the entry of fn-748: "depends_on: - fn-741"
- .garura/product/product-os/features/fn-741/feature.md, the old page, line 1: "A rename map, and a check that no old name is left"
- The old-name check, run from the repository root on 2026-11-11: exit 1, 12 uses of 9 old names
- GitHub #741 (closed); GitHub #936 (open): "Neither behavior has a test in `core/tools/naming/test_naming_tools.py`; both were checked by hand only."
- The stock-take, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 1.5 and 8
