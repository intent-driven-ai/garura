# Capability: Intelligent model routing

## Directional intent
Intelligent model routing: Each part runs on the right model and effort for its job, for speed and token cost, on each harness that supports it. Also serves Install and distribute.
These are the agreed words for the sixth capability of Standards, structure, settings and memory, set by the product owner on 2026-11-11. Of the list and its proposed answers, the product owner said: "continue as most of this is based on built. please proceed with creae pages and ICE as per the process and standards and consider them approved. show me only when you are ready for commit and cp". So this page is written from what is built, and from the product owner's answers for what is not. It serves two business intents, as the list records, "Intelligent model routing serves bi-10 and bi-7": Standards, structure, settings and memory (BI-10), where it decides which model and effort each part runs on and records what that costs; and Install and distribute (BI-7), whose coding tools carry each part's tier. The words this page uses:
- A part is one play, loop, sub-agent, skill, script, shared file or tool of Garura. A play is a command a person or an agent types to run one piece of work from start to end; a loop runs plays in rounds until its goal is met. A sub-agent gathers what a piece of work needs and checks it; a skill does the work.
- A model tier is the kind of model a part asks for in its source, on a `model:` line: `best`, `opus`, `sonnet` or `haiku`. The install folds it to deep, standard or fast. In the install play's words, "That value is a *tier* signal, not a literal host model id."
- Effort is how hard a model reasons on a step, such as `high` or `medium`, where a coding tool lets a part set it.
- A harness that supports it is a coding tool that takes a model, or an effort, for a kind of part. Claude Code takes both on a sub-agent and on a skill; where each other tool takes one is recorded in Support each coding tool.
- The session's model is the model the person's own session runs on. A step sent apart from it runs on another model.
- A run's record is what a run of a play or a loop writes about itself in its issue's folder.

This capability does two jobs that are built in part:
- Give each part a model tier and an effort by a written rule.
- Send a step to the model a setting names, apart from the session's.

And three jobs that are not built:
- Record each run's model, effort, time and cost for each part.
- Move a part up or down a tier on that record, and check the move with an eval.
- Choose the model and effort by the job at run time. It comes later, only if the records show it pays.

The product owner set who chooses, in the answers recorded on 2026-11-11: "the part's maker sets a default tier and effort by a written rule, a project may change it in its settings, each run records model, effort and cost per part, a run-time router comes later only if the records show it pays"; and "a skill's own tier reaches Claude Code, tried on one skill first and checked". Today 91 parts name a tier and 4 sub-agents name an effort, each set by hand. Claude Code keeps the tier on each sub-agent and the install drops it on each skill, play and loop, so 70 skills name a tier that never takes effect.
How it sits with the other capabilities:
- Install and distribute carries the tier this capability decides. Support each coding tool says, "Out: which model and effort each part runs on. Intelligent model routing owns it", and its feature Map each part's model tier onto each tool's own setting (fn-map-model-tier) says, "The tier is carried, never chosen." When a part's tier changes here, that feature lays the new tier at the next install. Each tool's own install feature says the same: "Which tier each part runs on. Intelligent model routing decides it."
- A model used beside the coding tool is a setting, not an install: "A model used beside the installed tool, such as the model that checks a loop or writes tests. It is a setting of those plays, not an install." Settings, in this intent, keeps every setting. This capability decides which steps run apart from the session's model and which models and services a setting may send them to. The capability whose step it is reads the setting and sends the step: in Design → Code, Build the work test first "reads the setting and sends the tests where it says", and Fix defects test first does the same; in Orchestration, Run plays as loops sends a finished loop's check to its checker's model; and in Product → Spec, Specify the product sends each model page to the model its judge's setting names.
- Standards, in this intent, holds the written standard for each kind of part and the checks; its linter requires a `model` line on each skill and sub-agent. Which tier and effort a part names, and the rule for it, are this capability's.

It matters because the cost of a run, and the time a person waits for it, are set part by part by the model each part runs on. A decision record sets the knowledge step's agent on a smaller model and names the cost behind it, $4.72 for one step's run on Opus: "The knowledge plays' agent runs on Sonnet". The memory page on choosing a model puts it as a rule: "Model choice is a per-task decision". And this intent's outcome asks that "each part runs on the right model". It sits in software delivery planning with the other capabilities of Standards, structure, settings and memory, and the domain's first paragraph says so.

Features:
- Give each part a model tier and an effort by a written rule (fn-tier-by-rule): each part's maker names in its source the tier and the effort its job needs, by one written rule, and a project may change a part's tier in its own settings; today the rule covers skills only, and a skill's tier does not reach Claude Code. Built in part.
- Send a step to the model a setting names, apart from the session's (fn-step-on-set-model): a step whose model a setting names, such as the check of a finished loop or the judge of a model page, runs on that model and not on the session's own; the test model setting is not built. Built in part.
- Record each run's model, effort, time and cost for each part (fn-record-run-cost): each run of a play or a loop records, for each part it ran, the model and effort it ran on, how long it took and what it cost in tokens. Not built.
- Move a part up or down a tier on that record, and check the move with an eval (fn-move-part-tier): when the record shows a part is slow or costly for a simple job, or falls short on a hard one, a person moves it, and an eval checks the part on its new tier before the move lands. Not built.
- Choose the model and effort by the job at run time (fn-choose-model-at-run): a router reads what a step must do and chooses its model and effort, once the records of runs show it pays. Not built.

What is not built yet:
- No written rule gives the tier of a sub-agent, a play or a loop, and none gives the effort of any kind of part. 4 skills, 33 plays and the one loop name no tier.
- 70 skills name a tier that does not take effect in Claude Code, while the skills doc tells each skill's maker to name a "Model to use".
- A project cannot change a part's tier in its settings.
- The test model setting does not exist, and nothing checks that a checker's model is not the session's own.
- No play or loop records the model, effort, time or cost of each part it ran. The rebuild eval records cost for its own agents only, and a play's session stamp, written only when the evidence setting is on, points to where a whole run's spend can be worked out later.
- No rule says when a part moves up or down, and no eval is named to check a move.
- Nothing chooses a model or an effort by the job, and no issue plans any of this capability's work.

### Benefit hypothesis
- Who it serves: the product owner, who pays for each run in tokens and waits for it; the technical lead and the developer, who build a part and name its tier; a team that changes a part's tier for its own project; Install and distribute, whose coding tools carry each part's tier; and the capabilities that send a step to another model: Run plays as loops, Build the work test first, Fix defects test first and Specify the product.
- What we believe: when each part names a tier and an effort by a written rule, each run records what each part ran on and what it cost, and each move up or down is checked by an eval, a project gets each part's job done well at less time and token cost, if the work stands on these rules:
  - A part names a tier, never a coding tool's model id.
  - The part's maker sets the default; the project may change it.
  - A checker runs on a model that is not the session's.
  - No move lands without an eval.
  - No router before the records show it pays.
- How we will know: every part names the tier and effort its written rule gives, or its reason; every run's record holds the model, effort, time and cost of each part it ran; every move names the runs it rests on and the eval that checked it; and every checker ran on a model that is not the session's.
  - The first holds for skills only today, and the second and third cannot be tested, because no run records them.

### Boundary (In / Out / Never)
- In: the written rule for each kind of part's tier and effort, the default each part's maker sets in its source, and a project's own tier for a part in its settings.
- In: which steps run on a model a setting names, apart from the session's, and which models and services a setting may send a step to.
- In, not built yet: the record of each run's model, effort, time and cost for each part; moving a part up or down a tier on that record, checked by an eval; and choosing the model and effort by the job at run time, once the records show it pays.
- Out: carrying each part's tier into each coding tool, and laying the parts. Support each coding tool, in Install and distribute, owns it, through Map each part's model tier onto each tool's own setting (fn-map-model-tier).
- Out: keeping each setting in the settings file. Settings, in Standards, structure, settings and memory, owns it.
- Out: the rest of each kind's written standard, and the linter that checks it. Standards, in Standards, structure, settings and memory, owns them.
- Out: where a run's records live in its issue's folder. Structure, in Standards, structure, settings and memory, owns it.
- Out: reading a step's setting and sending the step. Run plays as loops (Orchestration) owns the loop's check, Build the work test first and Fix defects test first (Design → Code) own the tests, and Specify the product (Product → Spec) owns the page judge.
- Out: the evals a compiled play holds, and building a play with them. Build your own harness, in Standards, structure, settings and memory, owns them.
- Never: name a coding tool's model id in a part's source. The reason: "That value is a *tier* signal, not a literal host model id."
- Never: run a checker on the session's own model. The reason: "A subagent checker must name its model, one other than the session's".
- Never: move a part's tier with no eval to check it. The reason: "Re-run evals on any model change."
- Never: build a router that chooses at run time before the records show it pays. The reason: "a run-time router comes later only if the records show it pays".
- Never: write a model, effort, time or cost in a run's record that the run did not have. The reason: "never fabricate".

### Guiding rules
- Match the model to the job, step by step. The reason: "Match the model to the job, per step", from the memory page on choosing a model for each step of an agent.
- Do not run a step on more model than it needs. The reason: "Route, don't over-provision."
- The part's maker sets the default; the project may change it. The reason: "the part's maker sets a default tier and effort by a written rule, a project may change it in its settings".
- The tier travels with the part, and which tier is this capability's. The reason: "The tier travels with the part; which tier is routing's."
- Try a change on one part first, and check it. The reason: "a skill's own tier reaches Claude Code, tried on one skill first and checked".
- A different model checks. The reason: "At the end, a different model, sub-agent, or coding agent checks the result. Configuration picks which."
- Not decided: the written rule for the tier of a sub-agent, a play and a loop, and for effort on any kind of part.
- Not decided: whether a move is made in the part's source, by its maker, or in the project's settings, by the team.
- Not decided: what "pays" means for a router: which saving in time or tokens, against which loss of quality, is enough.
- Not decided: one shape for every setting that sends a step to a model: a tier, a model id, or a service.

## Sources
- The capability list: "Intelligent model routing: Each part runs on the right model and effort for its job, for speed and token cost, on each harness that supports it. Also serves Install and distribute. (unique)"; the product owner on 2026-11-11: "continue as most of this is based on built. please proceed with creae pages and ICE as per the process and standards and consider them approved. show me only when you are ready for commit and cp"; "Intelligent model routing serves bi-10 and bi-7"; answers 4 and 5: "the part's maker sets a default tier and effort by a written rule, a project may change it in its settings, each run records model, effort and cost per part, a run-time router comes later only if the records show it pays", "a skill's own tier reaches Claude Code, tried on one skill first and checked"
- .garura/product/product-os/intents/bi-10.md, line 3: "each part runs on the right model"; .garura/product/product-os/intents/bi-7.md, line 1: "Install and distribute"
- The stock-take (2026-11-11), sections 6.1 to 6.4, 7.6, 7.7, 10 (item 1) and 12 (Lean 7)
- core/components/plays/install-garura/SKILL.md, line 31: "That value is a *tier* signal, not a literal host model id."
- core/components/plays/install-garura/scripts/adapters/common.py, lines 29-49: the fold to deep, standard and fast; adapters/claude.py, line 15: "A Claude skill has no model field"
- 1021/context/bi-7-capability-3/answers/coding-tool-claude-code.md, in short-term memory, memory update mu-20261110-001, approved by the product owner on 2026-11-10, read through the memory tool, lines 7 and 9: a sub-agent's "`effort` sets the effort level", and "the skill frontmatter has `model` (for the rest of the current turn) and `effort`"
- docs/components/skills.md, line 208: "Model to use"; lines 251-259: the written rule for skills
- docs/adr/042-a-drive-finds-builds-and-reviews-the-knowledge-it-lacks.md, lines 102-103: "The knowledge plays' agent runs on Sonnet", and the cost of $4.72 for one step's run on Opus
- core/config.yaml, line 121: "A subagent checker must name its model, one other than the session's"
- docs/adr/029-drives.md, line 38: "At the end, a different model, sub-agent, or coding agent checks the result. Configuration picks which."
- core/tools/rebuild-eval/run_eval.py, line 17: "Every agent's command, exit and cost go to `run.json`."
- standards/templates/evidence-file.md, in Phoenix memory, read through the memory tool, line 140: "never fabricate"
- knowledge/technology/agent-model-selection.md, in Phoenix memory, read through the memory tool: "Model choice is a per-task decision" (line 16), "Match the model to the job, per step" (line 25), "Route, don't over-provision." (line 31), "Re-run evals on any model change." (line 50); its conditions, an agentic feature on Bedrock or Vertex (lines 4-8), make it a page written for agents built into a product
- The hand-offs from approved pages, each under .garura/product/product-os/software-delivery-planning/: support-coding-tools/capability.md, line 62: "Out: which model and effort each part runs on. Intelligent model routing owns it", line 78: "The tier travels with the part; which tier is routing's."; support-coding-tools/fn-map-model-tier/feature.md, line 12: "This feature carries only the tier the part already names, and never chooses one.", line 36: "The tier is carried, never chosen.", line 43: "Given a part whose source tier is changed by Intelligent model routing, when Garura is installed again, then the new tier is laid.", line 47: "Which tier and effort each part runs on, and changing it. Intelligent model routing, in Standards, structure, settings and memory, owns it.", line 49: "A model used beside the installed tool, such as the model that checks a loop or writes tests. It is a setting of those plays, not an install."; support-coding-tools/fn-map-model-tier/ice.md, line 14: "which tier and effort each part runs on (Intelligent model routing)"; support-coding-tools/fn-install-for-copilot/feature.md line 40, fn-install-for-factory/feature.md line 42 and fn-install-for-antigravity/feature.md line 37: "Which tier each part runs on. Intelligent model routing decides it."; fn-install-for-claude-code/feature.md line 53 and fn-install-for-codex/feature.md line 50: "Which tier each part should run on. Intelligent model routing decides it."
- More hand-offs, under the same folder: build-work-test-first/capability.md, line 16: "This capability reads the setting and sends the tests where it says.", line 67: "Settings, where everything that can be turned on or off lives, and Intelligent model routing own them; this capability reads the setting."; build-work-test-first/fn-build-code-to-pass/feature.md, lines 59 and 102, and fn-write-failing-tests/feature.md, lines 40 and 58: "which models and services there are to choose from. Settings and Intelligent model routing do them."; fix-defects-test-first/capability.md, line 72: "Settings and Intelligent model routing own them; this capability reads them.", and its two features, fn-fix-defect-code/feature.md line 79 and fn-write-defect-tests/feature.md line 58
- The hand-offs to this intent as a whole, section 7.7 of the stock-take: orchestrate-agent-work/capability.md, line 77: "the settings, the names of the plays, and how plays and loops are built."; design-work/capability.md, line 96: "settings hold what can be turned on or off"
- core/tools/lint-components/lib/rules/structural.js, lines 68 and 144: the `model` field required on each source skill and sub-agent
- GitHub, a search of the open issues on 2026-11-11 for model tier, effort, Sonnet, Opus, Haiku and routing: no issue plans model choice
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none. No domain shelf in any memory tier covers choosing a model for each part of an agent harness; knowledge/technology/agent-model-selection.md, in Phoenix memory, covers choosing a model for each step of an agent built into a product, a loose match only.
- .garura/product/product-os/software-delivery-planning/domain.md, line 4: the domain's first paragraph, which names Install and distribute's work ("gets Garura itself into a project") and not yet this intent's
- .garura/product/product-os/software-delivery-planning/domain.md: "It also keeps the foundation every part stands on: the written standards and their checks, the builders a team uses for its own plays and loops, where everything lives, the settings, three tiers of memory, and the model each part runs on."
