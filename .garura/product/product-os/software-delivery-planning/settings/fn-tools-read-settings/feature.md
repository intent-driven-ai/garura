# Feature: Make every tool read its settings

## What it does
Each of Garura's tools reads the settings meant for it from where they live, the project's settings file or the tool's own settings, so a team changes what a tool does by changing a setting, never the tool or the command that runs it; this is how this intent's proof, "Every tool reads its settings.", is met.
- A tool is a program the plays run, laid in each project under `.garura/core/tools/`, such as the memory tool, the plan tool and the component linter.
- What each tool does today, tool by tool:
  - The memory tool reads its own settings: it "learns where each tier lives from one source: the JSON file `MEMORY_SETTINGS` names, else these environment variables, else `settings.json` beside `memory.py`". The install writes that file, "so an agent in an installed project runs the tool with no settings of its own".
  - The plan tool takes its folder from a flag with a fixed default, `.garura/project/plans`, not from the plans setting. /show-plan and /list-plans read the plans setting and pass it on: "`<plans>` is `plans.base-path` from config, else `.garura/project/plans/`".
  - The component linter takes the naming rules from a flag, and with no flag it skips them: "naming rules skipped: no naming standard given (--naming <naming.yaml>)".
  - No tool reads the trackers. The Agent-work tool is to: "One tool, the Agent-work tool, reads the project's settings and reaches the trackers they name".
- Where a tool's settings live: "Tool settings stay with their tool (for example the memory tool's `settings.json`)." Settings that a project chooses, such as the plans folder or the trackers, are in the project's settings file.
- Examples, in different kinds of project:
  - In a clinic's booking app, the team keeps its plans in another folder; it changes the plans setting, and the plan tool shows the plans from there.
  - In a bank's payments service, the memory tool's own settings name where Phoenix memory is kept on the machine, and a team points it at a copy it can reach.
  - In a game studio's build, the team moves its work to another tracker by changing the trackers setting, and the Agent-work tool reaches the new tracker with no tool and no play changed.
- How it meets the capability: a tool that takes a value from a fixed default, or only from the command that runs it, keeps a choice outside the settings.

Status: built in part: the memory tool reads its own settings. Not built, or open:
- The plan tool reads no setting: its folder comes from a flag with a fixed default, and only the plays that run it read the plans setting.
- The component linter takes its naming rules only from a flag.
- No tool reads the trackers.

## Inputs / Outputs
- In: the project's settings file, for the settings a project chooses, such as the plans folder and the trackers.
- In: a tool's own settings file, where the tool has one, such as the memory tool's.
- Out: each tool run with the values its settings hold, and with no value fixed in the tool that a setting is meant to hold.

## Rules & behavior
- Every tool reads its settings. The reason: this intent's proof: "Every tool reads its settings."
- A tool's own settings stay with the tool. The reason: "Tool settings stay with their tool".
- An install writes a tool's own settings, so an agent runs the tool with none of its own. The reason: the install writes it, "so an agent in an installed project runs the tool with no settings of its own".
- A tool that reaches a tracker takes it from the trackers setting. The reason: "Tools read this; plays, skills and sub-agents never name a tracker."
- Not decided: whether a tool reads the project's settings file itself, or takes each value from the play that runs it, as the plan tool does today.
- Not decided: whether the component linter's naming rules are a setting of the project, or a fixed part of the standard it checks against.

## Acceptance criteria
- Given a memory tool settings file that names where Phoenix memory is, when an agent runs the memory tool, then the tool reads Phoenix memory from there.
- Given the plans setting names another folder, when /show-plan runs the plan tool, then the plan tool shows the plans in that folder.
- Given the plans setting names another folder, when the plan tool runs with no folder given, then it shows the plans in that folder. This is not built.
- Given the trackers setting changed to another tracker, when the Agent-work tool runs, then it reaches the new tracker, and no tool or play was changed. This is not built.

## Out of scope
- Building the Agent-work tool that reads the trackers. Track execution in the team's tracker, in Orchestration, owns it, through One tool knows the tracker, and no play, skill or sub-agent names it (fn-one-tool-knows-tracker).
- Where each tool lives in the source and once laid. Structure, in Standards, structure, settings and memory, owns it.
- Laying a tool and its own settings in a project. Install into a project, in Install and distribute, owns it.
- How the memory tool finds memory across its tiers. Memory, in Standards, structure, settings and memory, owns it.
- What each setting a tool reads holds. Hold the settings other capabilities need: the test model, the design settings, the kinds of change that may go ahead on their own, the connections, the review rounds, the question tier, the loop settings and the trackers (fn-settings-others-need) holds them.

## Sources
- .garura/product/product-os/intents/bi-10.md, line 11: "Every tool reads its settings."
- core/tools/memory/README.md, lines 33-35: "The tool learns where each tier lives from one source: the JSON file `MEMORY_SETTINGS` names, else these environment variables, else `settings.json` beside `memory.py` (an install writes it, so an agent in an installed project runs the tool with no settings of its own)."
- core/tools/plan/plan.py, lines 34 and 283: `DEFAULT_PLANS = os.path.join(".garura", "project", "plans")`, and the `--plans-dir` flag with that default.
- core/components/plays/show-plan/SKILL.md, lines 63-64: "`<plans>` is `plans.base-path` from config, else `.garura/project/plans/`"; core/components/plays/list-plans/SKILL.md, lines 119-122: the plays pass the folder to the plan tool.
- core/tools/lint-components/index.js, lines 40-43 and 69: the `--naming` flag, and "naming rules skipped: no naming standard given (--naming <naming.yaml>)".
- core/config.yaml, line 14: "Tools read this; plays, skills and sub-agents never name a tracker."
- .garura/product/product-os/software-delivery-planning/track-execution/fn-one-tool-knows-tracker/feature.md, line 4: "One tool, the Agent-work tool, reads the project's settings and reaches the trackers they name"; line 56: "What each setting means, and the rule that no play, skill or sub-agent names a tracker. Standards, structure, settings and memory owns them; this feature holds the tool that meets the rule."
- The stock-take (2026-11-11), section 4.7 and Lean 11: "The plan tool takes its folder from a fixed default, not the `plans` setting"; and Lean 5, item 7.
