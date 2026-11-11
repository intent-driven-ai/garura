# Feature: Give each part a model tier and an effort by a written rule

## What it does
Each part's maker names in its source the model tier, and the effort, that the part's job needs, by one written rule, and a project may change a part's tier in its own settings, so each part runs on the right model and effort for its job.
- What a part names: a `model:` line with a tier, `best`, `opus`, `sonnet` or `haiku`, and, on a sub-agent, an `effort:` line, such as `high` or `medium`. In the install play's words, "That value is a *tier* signal, not a literal host model id."
- What the parts name today, from a read of each part's source on 2026-11-11:
  - 17 of 17 sub-agents name a tier: 12 `sonnet`, 4 `opus` and 1 `haiku`.
  - 70 of 74 skills name a tier: 39 `sonnet`, 23 `opus`, 4 `best` and 4 `haiku`.
  - 4 of 37 plays name a tier: the four that build plays and loops, each `best`. The one loop names none.
  - 4 sub-agents name an effort: two `high` and two `medium`. No skill, play or loop names one.
- The written rule covers skills only. The skills doc gives three tiers: `haiku` for "Execution-only skills — no analysis, no decision-making, fast operations", `sonnet` for "Analysis skills — reasoning, categorization, pattern matching, complex logic", and `opus` for "Judgment-heavy authoring — generative model work where quality dominates cost". The agents doc lists each sub-agent's model with no rule, and no rule says when a part names an effort.
- Some choices give their reason in the part itself, such as the sub-agent that walks a prototype: "High-volume, low-judgment work — runs on Sonnet at medium effort". A decision record sets the knowledge step's agent on a smaller model and names the cost behind it, $4.72 for one step's run on Opus: "The knowledge plays' agent runs on Sonnet".
- Where the tier takes effect: Claude Code keeps the tier and the effort on each sub-agent, and the install drops the tier on each skill, play and loop, because "A Claude skill has no model field". So 70 skills name a tier that never takes effect, while the skills doc tells each skill's maker to name a "Model to use". Claude Code does take a model and an effort on a skill, as approved in memory, and the product owner's answer is that a skill's own tier reaches Claude Code, tried on one skill first and checked. Carrying the tier is Install and distribute's.
- A project's own tier for a part: the product owner's answer is that "a project may change it in its settings". The settings file has no place for it today.
- Examples, in different kinds of project:
  - In a bank's payments service, the skill that only commits files names `haiku`, and the sub-agent that reviews each change names `opus` with `effort: high`.
  - In a clinic's booking app, the team finds a drafting skill slow on `opus` for its short notes, and sets that skill to `sonnet` in the project's settings, while the skill's source keeps `opus`.
  - In a game studio's build, the sub-agent that walks each level names `sonnet` at `medium` effort, because its work is high in volume and low in judgment.
- How it meets the capability: a part runs "on the right model and effort for its job" only when its job decides its tier and effort, and a written rule says how.

Status: built in part. Each part's tier in its source is built for 91 parts, the effort for 4 sub-agents, and the written rule for skills. Not built, or open:
- No written rule for the tier of a sub-agent, a play or a loop, and none for effort on any kind of part.
- 4 skills, 33 plays and the one loop name no tier.
- A skill's tier does not take effect in Claude Code, and nothing tells the team.
- A project cannot change a part's tier in its settings.

## Inputs / Outputs
- In: the part's job, as its maker writes it.
- In: the written rule for tier and effort.
- In: the project's own tier for a part, from its settings.
- Out: the part's `model:` line, and its `effort:` line where the rule asks for one, in its source.
- Out: the tier and effort the part runs on in the project: the project's own where its settings name one, else the source's.

## Rules & behavior
- The part's maker sets its default tier and effort in its source, by a written rule. The reason, in the product owner's answer as recorded: "the part's maker sets a default tier and effort by a written rule".
- A project may change a part's tier in its own settings. The reason: "a project may change it in its settings".
- A part names a tier, never a coding tool's model id. The reason: "That value is a *tier* signal, not a literal host model id."
- A skill that runs commands takes the fast tier, one that reasons takes the standard tier, and one that authors judgment-heavy work takes the deep tier. The reason: "If the skill just runs commands and formats output, use `haiku`. If the skill needs to read, reason, and categorize, use `sonnet`. If it authors judgment-heavy artifacts, use `opus`."
- High-volume, low-judgment work runs on a smaller model. The reason: the memory page on choosing a model gives the small, fast model "the high-volume, low-judgment work", and the prototype walker runs on Sonnet for "High-volume, low-judgment work".
- A skill's own tier and effort take effect in Claude Code, tried first on one skill and checked. The reason, in the product owner's answer as recorded: "a skill's own tier reaches Claude Code, tried on one skill first and checked"; and, as approved in memory, "the skill frontmatter has `model` (for the rest of the current turn) and `effort`".
- Not decided: the written rule for the tier of a sub-agent, a play and a loop, and for effort on any kind of part.
- Not decided: whether a play or a loop names a tier and an effort; today only the four that build plays and loops name one.
- Not decided: where a project's own tier for a part is kept in its settings, and how a person sees it beside the tier the source names.

## Acceptance criteria
- Given a new skill that only runs commands and formats output, when its maker writes its source by the rule, then it names `haiku`.
- Given a sub-agent whose source names `opus` and `effort: high`, when it is laid for Claude Code, then its laid file names `opus` and `high`.
- Given a sub-agent, a play or a loop, when its maker chooses its tier and effort, then a written rule says which. This is not built.
- Given one skill whose source names `haiku`, when it is laid for Claude Code and run, then it runs on the fast tier and the check of that one skill reads pass before any other skill's tier is laid. This is not built.
- Given a project whose settings set one part to `sonnet` while its source names `opus`, when the part runs, then it runs on `sonnet`. This is not built.

## Out of scope
- Carrying each part's tier and effort into each coding tool. Map each part's model tier onto each tool's own setting (fn-map-model-tier), in Support each coding tool, does it.
- The rest of each kind's written standard, and the linter that requires a `model` line on each skill and sub-agent. Standards, in Standards, structure, settings and memory, owns them.
- Keeping the settings file and each setting in it. Settings, in Standards, structure, settings and memory, owns it.
- Moving a part up or down on the record of its runs. Move a part up or down a tier on that record, and check the move with an eval (fn-move-part-tier) does it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, line 115: "Intelligent model routing: Each part runs on the right model and effort for its job, for speed and token cost, on each harness that supports it."; line 118, the product owner's answers 4 and 5 as recorded on 2026-11-11: "the part's maker sets a default tier and effort by a written rule", "a project may change it in its settings", "a skill's own tier reaches Claude Code, tried on one skill first and checked"
- The count of tiers and efforts: the `model:` and `effort:` lines of each part's front lines under core/components (agents, skills, plays, loops), read on 2026-11-11; the same counts as the stock-take, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, section 6.1
- docs/components/skills.md, line 208: "Model to use"; lines 255-259: "Execution-only skills — no analysis, no decision-making, fast operations", "Analysis skills — reasoning, categorization, pattern matching, complex logic", "Judgment-heavy authoring — generative model work where quality dominates cost", "If the skill just runs commands and formats output, use `haiku`. If the skill needs to read, reason, and categorize, use `sonnet`. If it authors judgment-heavy artifacts, use `opus`."
- docs/components/agents.md, line 60 and the rows after it: each sub-agent's model, with no rule
- core/components/agents/prototype-reader.md, line 5: "High-volume, low-judgment work — runs on Sonnet at medium effort"; lines 6-7 of prototype-reader.md, business-intent-keeper.md, knowledge-builder.md and result-checker.md: the four efforts
- docs/adr/042-a-drive-finds-builds-and-reviews-the-knowledge-it-lacks.md, lines 102-103: "The knowledge plays' agent runs on Sonnet", and the cost of $4.72 on Opus
- core/components/plays/install-garura/SKILL.md, line 31: "That value is a *tier* signal, not a literal host model id."
- core/components/plays/install-garura/scripts/adapters/claude.py, line 15: "A Claude skill has no model field"; lines 42-57: only the `model` line is rewritten, so a sub-agent's `effort` line is laid as written
- 1021/context/bi-7-capability-3/answers/coding-tool-claude-code.md, in short-term memory, memory update mu-20261110-001, approved by the product owner on 2026-11-10, read through the memory tool, line 9: "the skill frontmatter has `model` (for the rest of the current turn) and `effort`"
- knowledge/technology/agent-model-selection.md, in Phoenix memory, read through the memory tool, line 28: "the high-volume, low-judgment work"
- core/config.yaml: no setting names a part's tier (read on 2026-11-11)
- .garura/product/product-os/software-delivery-planning/support-coding-tools/fn-map-model-tier/feature.md, line 47: "Which tier and effort each part runs on, and changing it. Intelligent model routing, in Standards, structure, settings and memory, owns it."
- core/tools/lint-components/lib/rules/structural.js, lines 68 and 144: the `model` field required on each source skill and sub-agent
