# Feature: Rename the skills to the standard

## What it does
Every skill is renamed so that its first word is a verb from the skill verbs, each with one meaning, with every reference to it changed in the same batch, so two skills never use one verb for two jobs or two names for one job.
- Under ADR 046, built: every skill took a verb from the skill verbs: `author`, `infer`, `derive`, `scan`, `check`, `judge`, `assess`, `find`, `link`, `enrich`, `propose`, `research`, `rank`, `recommend`, `collect`, `walk`, `deploy`, `track`, and the git verbs `commit`, `open`, `merge` and `cut`. ADR 046 counts "69 skills" renamed.
- What the rename fixed: before it, `author-`, `draft-`, `write-` and `build-` all made a document, and "two skills had near-same names for different jobs (`kb-search`, `search-kb`)". They became `find-architecture-learnings` and `find-work-placement`, and the skill `manage-plan`, which "clashed" with a planned play of that name, became `author-plan-file`.
- `platform-adapter` stays as the one named exception.
- ADR 046 also renamed two sub-agents: `env-operator` became `environment-operator`, and `loop-checker` became `result-checker`, because Claude Code has `/loop`.
- After ADR 046, the verb `remove` was added to the source's skill verbs, for `remove-model-part` and `remove-plan`, with no ADR behind it.
- Under ADR 066, decided: skills and sub-agents keep their verbs for now. "Decided: skills and agents keep their verbs for now, and get their own list in a later decision. `remove` stays undecided, in that later decision." So `author`, which "starts 21 live skills", still does not say who acts.
- Examples, in different kinds of project:
  - In a bank's payments service, two skills named `get-rates` and `rates-fetch` do one job. The rename keeps one, as `find-exchange-rates`, and the old-name check finds neither old name left.
  - In a clinic's booking app, the skills that write a letter, a summary and a reminder all take the verb `author`, so a person reading the list knows each writes a document.
  - In a harness repository, a new skill that takes a part out of the model needs a verb the list does not have, and it waits on the later decision on skill verbs.
- How it meets the capability: the skills, where the work is done, follow the same naming rule as the plays.

Status: built, under ADR 046, by #746 (rename the skills, closed), landed in PR #749, which published the standard. Not built, or open:
- The later decision on the verbs of skills and sub-agents is not made, and the roles of #1015 are not given to them.
- The verb `remove` is in no decision, and Phoenix memory's copy of the naming rules does not have it, so `remove-model-part` and `remove-plan` "fail the check in any project that reads Phoenix memory's copy".

## Inputs / Outputs
- In: the rename map's skill and sub-agent lines, and the skill verbs with their meanings.
- In: every reference to an old skill name, in the plays, the sub-agents, the docs and the tests.
- Out: the skills under their new names, with every reference changed.
- Out: the old-name check's report, with no old skill name left.

## Rules & behavior
- Names and references only. The reason: "Names and references only: no behaviour changes."
- One verb, one meaning, for skills too. The reason: before the rename, "two skills had near-same names for different jobs (`kb-search`, `search-kb`)".
- A verb that says where its input comes from is not repeated. The reason: "`scan-test-surface`, not `scan-test-surface-from-code`".
- Skills and sub-agents keep their verbs until their own decision. The reason: "Decided: skills and agents keep their verbs for now, and get their own list in a later decision."
- Not decided: the verb list of skills and sub-agents, which roles they take, and the verb `remove`.

## Acceptance criteria
- Given ADR 046's rename, when the old-name check runs, then it finds none of `kb-search`, `search-kb` or `manage-plan`.
- Given a skill whose first word is not a skill verb, when the component linter runs, then it fails.
- Given two skills with one verb, when their meanings are compared, then the verb means the same thing for both.
- Given the later decision on skill verbs, when it is accepted, then each skill's verb belongs to one role, or the decision says why not. This is not built.
- Given a project that reads Phoenix memory's copy of the naming rules, when the linter runs on `remove-model-part`, then it passes. This is not built.

## Out of scope
- The rule the names follow, and the later decision on skill verbs. Name every part by one rule, with five roles owning the verbs (fn-736) does it.
- The rename map and the check. Map every old name to its new one, and check that no old name is left (fn-741) does it.
- Building a skill. Build your own harness, in Standards, structure, settings and memory, owns it.
- Keeping Phoenix memory's copy of the naming rules in step. Memory, in Standards, structure, settings and memory, owns it.

## Sources
- core/components/memory/standards/rules/rename-map.yaml, lines 41-82: the old skill and sub-agent names and their new ones
- core/components/memory/standards/rules/naming.md, lines 52-56: the skill verbs, "`scan-test-surface`, not `scan-test-surface-from-code`", and the one named exception
- core/components/memory/standards/rules/naming.yaml, line 56: the verb `remove`
- standards/rules/naming.md, in Phoenix memory, read through the memory tool on 2026-11-11: its skill verbs, with no `remove`
- core/tools/naming/apply_renames.py, line 12: "Names and references only: no behaviour changes."
- docs/adr/046-one-naming-standard-for-every-harness-part.md, lines 9, 16-21 and 51-52: "69 skills", "two skills had near-same names for different jobs (`kb-search`, `search-kb`)", "A planned `manage-plan` play clashed with an existing `manage-plan` skill.", "The agent `loop-checker` becomes `result-checker`"
- docs/adr/066-names-say-who-does-the-work-five-roles-own-the-verbs.md, lines 19, 29 and 31: "`author` starts 21 live skills", "fail the check in any project that reads Phoenix memory's copy", "Decided: skills and agents keep their verbs for now, and get their own list in a later decision. `remove` stays undecided, in that later decision."
- .garura/product/product-os/features/fn-746/feature.md, the old page, line 4: "every skill renamed to the skill verb list (to be agreed with the product owner), including the duplicates kb-search / search-kb and the manage-plan skill."
- GitHub #746 (closed): "Rename the skills"; PR #749 (merged)
- GitHub #1015 (open): "Every verb gets one role."
- The stock-take, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 1.4 and 8
