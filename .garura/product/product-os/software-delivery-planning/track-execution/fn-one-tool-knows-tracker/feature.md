# Feature: One tool knows the tracker, and no play, skill or sub-agent names it

## What it does
One tool, the Agent-work tool, reads the project's settings and reaches the trackers they name, so every play, skill and sub-agent that reads or writes a business intent or a work item calls the tool and never the tracker, and a team changes its tracker by changing a setting, with no other edit.
- The settings it reads are the trackers and the code host. The trackers name one tracker for business intents and one for agent work. The code host, where the pull requests live, is its own setting, "because a team on Jira still keeps pull requests on GitHub or GitLab."
- It starts from the adapter, the piece that today turns 25 named actions into the command lines of GitHub and GitLab.
- The parts that reach a tracker move onto it. Today "3 plays, 11 skills and 3 agents hold `gh` commands, and 10 plays, 6 skills and 1 agent name GitHub." The words of the way of working on how the tracker works move into the settings too: "Anything in `CLAUDE.md` or `managing-work.md` that says how the tracker works comes out and into settings."
- A check fails any play, skill or sub-agent that names a tracker or calls its command line, and names that part.
- It fixes the older code-host setting, whose owner is not the trackers' owner: "The older `github.owner` setting names a personal account while `trackers.work.owner` names the organization. This fixes that."
- GitHub and GitLab come with the adapter. Jira and Linear support "may be its own stories", and the tool does not change which tracker Garura itself uses.
- Other parts already wait on it. Approved pages of other capabilities read the tracker "through the tool that knows the tracker", and until it lands, /shape-slice, /shape-plan and /shape-eval "must not run".
- Examples, in different kinds of project:
  - In a clinic's booking app, the settings name GitHub for the business intents and for the work. /shape-plan files the epic and its stories through the tool, and no play, skill or sub-agent holds a GitHub command.
  - In a bank's payments service, the business intents live in Jira, and the work and the pull requests on GitLab. The plays are the same as the clinic's; only the settings differ.
  - In a game studio that moves its work from GitHub to GitLab, a person changes the setting of the work tracker, and the plays' next writes reach GitLab with no play, skill or sub-agent edited.
- How it meets the capability: the product's execution is tracked "in the tracker Garura connects to"; this feature is the one place where that connection is made, so the tracker can change while the parts that track the work stay as they are.

Status: not built. Today:
- No tool knows the tracker. The adapter is a skill, and ADR 065 counts "eight copies of `platform_adapter.py`" stamped beside the parts that use it.
- The adapter reads the older platform line, and no script reads the trackers settings: the word appears only in a docstring of the session's tracker script.
- The older code-host setting and the trackers name different owners.
- Only GitHub is exercised. The GitLab path is "UNTESTED here", and Jira and Linear are not reached.
- Until the tool lands, the three shaping plays are not to run. No part checks this, and no way past it records what is owed.

## Inputs / Outputs
- In: the project's settings: the tracker for business intents, the tracker for agent work and the code host, each with its platform and where it is.
- In: a request from a play, skill or sub-agent that says what to do to an intent or a work item, and names no tracker and no tracker's command.
- In: the plays, skills and sub-agents themselves, for the check.
- Out: the read or the write, made in the tracker that the settings name for that kind of item, and its result back to the caller.
- Out: the result of the check: each play, skill or sub-agent that names a tracker or calls its command line, by name, or none.
- Out: one setting that says who owns the work tracker, in place of two that disagree.

## Rules & behavior
- Plays, skills and sub-agents know only the tool, never the tracker. The reason: "Plays, skills and sub-agents know only the tool, never the tracker."; the Must not of Standards, structure, settings and memory: "Name a tracker in a play, skill or sub-agent, because they only know the tool."; and, in the product owner's words, "the sub-agents or skills or play call this tool hiding the underlying implementation."
- The tool reads where each tracker is from the settings. The reason: "Tools read this; plays, skills and sub-agents never name a tracker.", and "Tools read the settings and know how to reach the tracker."
- Business intents and agent work each have their own tracker setting, and the two can name different trackers. The reason: "Business intents and agent work each live in a tracker named in the project's settings."
- The code host is its own setting, and the tool reads both. The reason: "The code host is its own setting, and the tool reads both.", "because a team on Jira still keeps pull requests on GitHub or GitLab."
- Changing the setting changes the tracker, with no other edit. The reason: "A team picks its tracker as a setting, and nothing is hard-coded.", and "A team can choose its tracker as a setting, and a new tracker means changing one tool."
- A check fails any part that names a tracker. The reason, as asked: "A check fails any part that names a tracker directly."; without it, a reviewer reads a part that still names the tracker "as not moved yet, not as broken."
- The parts move onto the tool over time, starting from the adapter. The reason: "Parts move onto the tool over time.", and "The tool is the Agent-work tool, starting from the platform-adapter skill, recorded as a feature."
- One setting says who owns the work tracker. The reason: "Two settings for one tracker can disagree, and on the owner they already do."
- Not decided: what the tool does when the tracker lacks a type that a play must file. Initialize's approved page has the filing play "stop with a plain message that points to initialize", and the Must not of Orchestration is "Stop a person. Every gate has a way past it that records what's owed."
- Not decided: whether the pull requests are reached through this tool, or through a second tool for the code host.
- Not decided: whether the tool gives back each tracker's own fields, as the adapter does today ("the adapter does not normalize output across platforms"), or the same fields for every tracker.
- Not decided: where the tool lives: with Garura's tools, where ADR 065 records "the Agent-work tool, recorded as a feature", or in a component of its own for tools, as the direction that tools become a first-class Garura component puts it.
- Not decided: how GitLab, Jira and Linear each hold a work item's type, its parent and its close reason. Today the adapter sets no type on GitLab ("GitLab has no issue types here."), links a parent there only as a related link, and drops the close reason there; it does not reach Jira or Linear. No approved source says what these trackers offer.

## Acceptance criteria
- Given settings that name GitHub for the work, when a play files a story through the tool, then the story is made in that tracker and the play holds no tracker command. This is not built.
- Given the setting of the work tracker changed to another tracker the tool reaches, when the same play runs again, then its items are made in the new tracker, and no play, skill or sub-agent was edited. This is not built.
- Given settings that name one tracker for business intents and another for agent work, when a play reads an intent and files its epic, then the intent is read from the first tracker and the epic is made in the second. This is not built.
- Given a skill that calls a tracker's command line, when the check runs, then it fails and names that skill. This is not built.
- Given the tool in place, when a person reads the settings, then one setting names who owns the work tracker, and no other setting names another owner. This is not built.

## Out of scope
- What each setting means, and the rule that no play, skill or sub-agent names a tracker. Standards, structure, settings and memory owns them; this feature holds the tool that meets the rule.
- Making the tracker's types in a project. Set up the tracker's work-item types (fn-881), in Initialize, does it.
- Saying what each type means. Say what each work-item type means (fn-say-what-each-type-means) does it, and it is not built.
- Linking each piece of work to its intent. Link each piece of work to its intent across trackers (fn-link-work-across-trackers) does it, and it is not built.
- Landing the writes of an approved session once each. Every approved tracker write lands once, and is picked up after a stop (fn-land-tracker-writes-once) does it; it moves onto this tool with the other parts.
- A way past the rule that the shaping plays wait for this tool. Give every gate a way past, in Orchestration, owns it.

## Sources
- The capability list the product owner locked on 2026-11-03: "Track execution in the team's tracker: The product's execution is tracked in the tracker Garura connects to, for completion status and the backlog."; and his words of 2026-11-10: "Is there anything new? If so, then do research for that."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "Plays, skills and sub-agents know only the tool, never the tracker.", "Tools read the settings and know how to reach the tracker.", "Business intents and agent work each live in a tracker named in the project's settings.", "The code host is its own setting, and the tool reads both.", "Parts move onto the tool over time.", "The tool is the Agent-work tool, starting from the platform-adapter skill, recorded as a feature.", "Two settings for one tracker can disagree, and on the owner they already do.", "as not moved yet, not as broken.", "A team can choose its tracker as a setting, and a new tracker means changing one tool.", "eight copies of `platform_adapter.py`", "the Agent-work tool, recorded as a feature"
- core/config.yaml: "Tools read this; plays, skills and sub-agents never name a tracker."
- .garura/product/product-os/intents/bi-10.md: "Name a tracker in a play, skill or sub-agent, because they only know the tool."
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- core/components/skills/platform-adapter/SKILL.md: "Exposes exactly 25 verbs", "the adapter does not normalize output across platforms", "Attach a child issue to a parent (GitHub only; GitLab falls back to related-link)"
- core/components/skills/platform-adapter/reference/gitlab/verbs.md: "GitLab has no issue types here."
- core/components/skills/track-plan-changes/scripts/platform_adapter.py: "UNTESTED here"
- core/components/skills/track-issue/SKILL.md: "on GitLab, the `reason` argument is silently ignored by the adapter"
- core/components/skills/track-plan-changes/scripts/tracker.py: the one file under the plays, skills, agents and tools whose text holds the word trackers, in a docstring (searched on 2026-11-10).
- core/components/plays/: no part of /shape-slice, /shape-plan or /shape-eval checks for the tool (searched on 2026-11-10).
- .garura/product/product-os/software-delivery-planning/gather-work-under-item/fn-gather-item-tree/feature.md: "It reads each gathered item's text from the tracker, through the tool that knows the tracker"
- .garura/product/product-os/software-delivery-planning/write-work-evals/capability.md: "The plays that read the plan must not run until the Agent-work tool, the one tool that knows the tracker, lands."
- .garura/product/product-os/software-delivery-planning/initialize/fn-881/feature.md: "stop with a plain message that points to initialize"
- The research for this capability's new features, T1, "One tool knows the tracker": its open points are the Not decided lines here.
- Shelf: none. No knowledge shelf in any memory tier covers how a team tracks its work in a tracker.
