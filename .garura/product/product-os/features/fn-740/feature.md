# Feature: Check every part against the standard

## What it does
Machine checks read the parts of the harness and fail each one that breaks a written rule, naming the part and the rule, so a part that breaks the standard is caught by a check, not by someone reading it.
- The component linter, `core/tools/lint-components/`, has eight rule families: structural, semantic, cross-reference, naming, asking a person, shared scripts, installed paths and memory reading. It runs on the source, and on an installed project with `--layout installed`.
- Its naming rules read the rule file: "Every rule's data lives in memory/standards/rules/naming.yaml; this file holds no rule of its own." One list is kept in the linter itself: the shortened words it refuses (`naming.js` line 10).
- The play linter checks a compiled play: each constraint, failure condition and scenario is covered, each failure has one recovery, nothing is an orphan, the required sections are there, and the fingerprint is real. In its own words: "It is NOT a substitute for thought."
- The loop linter gives a loop every check a play gets, and its own, among them "the fingerprint is the sha256 of reference/ice.md as it is now". "It counts; it does not judge."
- The old-name check finds any old name still used (fn-741).
- Where they run: the review of each change runs the component linter and the play linter on the parts the change touched, and "Only a violation whose file is in `changed_paths` becomes a finding"; the others are counted as there before. A person can run any of them by hand.
- What they show on 2026-11-11, run from the repository root:
  - the component linter on the source: 36 errors and 1 warning. 22 errors are in the six plays written by hand, missing sections and close anchors; 14 are in five skills, `check-quality`, `find-matching-issues`, `merge-pr`, `open-pr` and `propose-kb-node`, missing sections and `model` and `allowed-tools` lines. No naming, memory-reading or installed-path error;
  - the old-name check: 12 uses of 9 old names.
- What it took over: this feature was "The component linter fails any name that breaks the standard". It widens here from names to every check.
- Approved pages hand more checks here: a check that fails a gate with no way past, from Give every gate a way past, and the lint that the docs check of Keep the docs and command pages in step with each change runs in.
- Examples, in different kinds of project:
  - In a bank's payments service, a developer's new skill has no `model` line, and the component linter fails it before the change is merged.
  - In a clinic's booking app, a play's failure condition has no recovery, and the play linter names the failure.
  - In a game studio's build harness, a loop's ICE changed after it was built, and the loop linter fails it until the loop is built again.
- How it meets the capability: these are the "checks that hold them" of the line.

Status: built in part, in the component linter, the play linter, the loop linter and the old-name check; the naming checks came first, so the component linter fails any name that breaks the standard, before any rename. Not built, or open:
- They run only on what a change touched, inside the review, and no build server runs them: the repository's one workflow only makes a release. The 36 errors on the source stay.
- The play linter does not compare a play's fingerprint with its ICE.
- In an installed project, the naming rules come only from a copy fetched through the memory tool; with none, the naming check does not run. Phoenix memory's copy differs from the source.
- No check holds the layer rule, that no skill names a play or another skill, a tracker named in a part (fn-check-no-tracker-named), or a gate with no way past.
- Some checks have no tests: the scoped-write guard, whose 14 copies run unguarded, and the direct-model-write lint checks.

## Inputs / Outputs
- In: the parts, in the source or in an installed project.
- In: the rule files, from the source, or in an installed project from a copy fetched through the memory tool.
- In: in the review of a change, the paths it changed.
- Out: each check's report: each break with its part, its rule and its line, and the exit code.
- Out: in the review, the findings on the changed parts and the count of breaks there before.

## Rules & behavior
- A check reads the rule files and holds no rule of its own. The reason: "Every rule's data lives in memory/standards/rules/naming.yaml; this file holds no rule of its own."
- A check counts; it does not judge. The reason: "It counts; it does not judge."
- A check, not a reading, says a rule holds. The reason: "a change judged by reading it is a change nobody proved."
- In the review of a change, only what the change touched becomes a finding. The reason: "Only a violation whose file is in `changed_paths` becomes a finding".
- An installed project checks names against the rules fetched through the memory tool. The reason: "fetched through the memory tool, for the naming rules".
- A new rule's check warns until the parts have moved, then fails. The reason, in the product owner's answer: "warns until the parts have moved, then fails".
- Not decided: where and when the checks run on every part, not only on what a change touched.
- Not decided: whether the six plays written by hand gain the sections the linter asks for, or the linter names them as written by hand.

## Acceptance criteria
- Given a skill in the source with no `model` line, when the component linter runs, then it fails and names the skill.
- Given a play whose failure condition has no recovery, when the play linter runs, then it fails and names the failure.
- Given a loop whose ICE changed after it was built, when the loop linter runs, then it fails.
- Given a change that touches one play, when the review runs the linters, then only that play's breaks are findings, and the others are counted as there before.
- Given the whole source, when every check runs on every part, then all pass. This is not built.
- Given a play whose ICE changed after it was compiled, when the play linter runs, then it fails. This is not built.

## Out of scope
- The review of each change, which runs the checks and gives a verdict. Check the code against its standards, in Code → Validation, owns it.
- The check that the docs and command pages agree with the commands. Keep the docs and command pages in step with each change, in Ship every change the same way, owns it; the lint it runs in is this feature's.
- The check that no part names a tracker. Check that no play, skill or sub-agent names a tracker (fn-check-no-tracker-named) does it.
- The old-name check's rules. Map every old name to its new one, and check that no old name is left (fn-741) does it.
- Keeping Phoenix memory's copy of the rule files in step. Memory, in Standards, structure, settings and memory, owns it.
- The way past a failed check. Give every gate a way past, in Orchestration, owns it.

## Sources
- The product owner's answer 8 (2026-11-11): "the check that no part names a tracker comes with [the Agent-work tool], warns until the parts have moved, then fails"
- .garura/product/product-os/intents/bi-10.md, line 10: "The checks hold every part to the standard."
- core/tools/lint-components/index.js, lines 7-14: the eight rule families
- core/tools/lint-components/lib/rules/naming.js, lines 3-4, 10 and 12-23: "Every rule's data lives in memory/standards/rules/naming.yaml; this file holds no rule of its own.", the list of shortened words, and the installed layout that reads the rules only from a copy handed to it
- core/tools/lint-play/lint_play.py, lines 10 and 22-30: "It is NOT a substitute for thought.", and its checks
- core/components/plays/create-loop/scripts/lint_loop.py, lines 5-24: "the fingerprint is the sha256 of reference/ice.md as it is now", "It counts; it does not judge."
- core/components/plays/check-change/SKILL.md, lines 194-216: "Only a violation whose file is in `changed_paths` becomes a finding"
- docs/standards/harness-standard.md, lines 65 and 164-168: "a change judged by reading it is a change nobody proved.", "fetched through the memory tool, for the naming rules"
- .github/workflows/release.yml: the repository's one workflow
- .garura/product/product-os/features/fn-740/feature.md, the old page, line 1: "The component linter fails any name that breaks the standard"
- .garura/product/product-os/software-delivery-planning/give-every-gate-a-way-past/fn-way-past-every-gate/feature.md, line 58: "A check that fails a play whose gate names no way past."
- .garura/product/product-os/software-delivery-planning/ship-every-change/fn-keep-docs-in-step/feature.md, line 42: "The lint itself and its other rules."
- The component linter on the source and the old-name check, run from the repository root on 2026-11-11: 36 errors and 1 warning; 12 uses of 9 old names
- The stock-take (2026-11-11), sections 1.5 and 8
