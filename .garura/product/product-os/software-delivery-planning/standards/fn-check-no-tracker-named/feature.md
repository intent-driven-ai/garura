# Feature: Check that no play, skill or sub-agent names a tracker

## What it does
A check reads every play, skill and sub-agent and names each one that names a tracker or calls a tracker's command line, warning while the parts move onto the Agent-work tool and failing after, so this intent's Must not is held by a machine and not by someone reading the parts.
- This intent's Must not: "Name a tracker in a play, skill or sub-agent, because they only know the tool."
- ADR 065, rule 4: "Plays, skills and sub-agents know only the tool, never the tracker. Parts move onto the tool over time."
- A check is to fail any part that names a tracker directly, once the Agent-work tool reads the tracker setting so no play, skill or sub-agent names a tracker. Today 3 plays, 11 skills and 3 agents hold `gh` commands, and 10 plays, 6 skills and 1 agent name GitHub.
- The product owner answered when it comes and how it turns on: "the check that no part names a tracker comes with [the Agent-work tool], warns until the parts have moved, then fails".
- The tool that meets the rule belongs to Track execution in the team's tracker: One tool knows the tracker, and no play, skill or sub-agent names it. This feature is the check that the rule holds.
- Examples, in different kinds of project:
  - In a bank's payments service that uses Jira, a skill still calls GitHub's command line. The check warns while the parts move, and fails once the tool is in.
  - In a clinic's booking app on GitLab, a sub-agent's text names GitLab. The check names the file and the line.
  - In a game studio's build harness that moves from GitHub to Linear, the team changes only the setting, and the check shows that no part needs an edit.
- How it meets the capability: this is one of the "checks that hold" the standard, here the one that holds this intent's Must not.

Status: not built. It is planned with the Agent-work tool that reads the tracker setting. Not built, or open:
- No rule of the component linter reads a part for a tracker's name or command line.
- The parts that name a tracker have not moved onto the tool.

## Inputs / Outputs
- In: every play, skill and sub-agent, in the source or in an installed project.
- In: the tracker names and command lines to look for.
- In: whether the parts have moved onto the Agent-work tool.
- Out: each part that names a tracker, with its file and line, as a warning before the parts have moved and as a failure after.

## Rules & behavior
- No play, skill or sub-agent names a tracker. The reason, this intent's Must not: "Name a tracker in a play, skill or sub-agent, because they only know the tool."
- It warns until the parts have moved, then fails. The reason, in the product owner's answer: "warns until the parts have moved, then fails"; and the harness standard's principle 6: "missing links are warnings to fix later, not stops".
- It comes with the Agent-work tool. The reason, in the product owner's answer: "comes with [the Agent-work tool]".
- Not decided: what counts as naming a tracker: a tracker's command line such as `gh`, a tracker's name in words, or both.
- Not decided: when the check moves from a warning to a failure, and who says the parts have moved.

## Acceptance criteria
- Given a skill that calls a tracker's command line, when the check runs before the parts have moved, then it warns and names the skill and the line. This is not built.
- Given the parts have moved onto the tool, when a sub-agent names GitHub, then the check fails. This is not built.
- Given a part that calls only the Agent-work tool, when the check runs, then it passes. This is not built.

## Out of scope
- The Agent-work tool, and moving the parts onto it. One tool knows the tracker, and no play, skill or sub-agent names it (fn-one-tool-knows-tracker) does it.
- The tracker settings. Settings, in Standards, structure, settings and memory, owns them.
- The other checks. Check every part against the standard (fn-740) does them.

## Sources
- .garura/product/product-os/intents/bi-10.md, line 14: "Name a tracker in a play, skill or sub-agent, because they only know the tool."
- The product owner's answer 8 (2026-11-11): "the check that no part names a tracker comes with [the Agent-work tool], warns until the parts have moved, then fails"
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md, line 143: "Plays, skills and sub-agents know only the tool, never the tracker. Parts move onto the tool over time."
- docs/standards/harness-standard.md, lines 71-72: "missing links are warnings to fix later, not stops"
- .garura/product/product-os/software-delivery-planning/track-execution/fn-one-tool-knows-tracker/feature.md, line 56: "the rule that no play, skill or sub-agent names a tracker. Standards, structure, settings and memory owns them; this feature holds the tool that meets the rule."
- The stock-take (2026-11-11), sections 1.5, 1.8 and 10
