# Capability: Track execution in the team's tracker

## Directional intent
Track execution in the team's tracker: The product's execution is tracked in the tracker Garura connects to, for completion status and the backlog.
These are the product owner's words for the third capability of Orchestration. On how it is drafted, his words were: "Anything that already exists, like managing ADRs and execution tracking, just use what is already built to do that." So this page says what is built, as it is built, and names what is not built. The words this page uses:
- The tracker is the tool where a team keeps its issues, such as GitHub, GitLab, Jira or Linear. A project's settings can name one tracker for its business intents and another for its work, as Garura's own settings do.
- A work item is an issue in the tracker that people or agents work: an Epic, a Story, a Bug, a Chore or a Spike. Its type is the tracker's issue-type field. Its parent is the issue it hangs under, by the tracker's own parent and child link.
- A plan is the tree of work items toward one business intent, kept as a plan file in the repository. Each item in the tree names its issue, its kind and its status.
- A plan session is one run of /update-plan: a person gives instructions in their own words, each becomes an entry on a list, and on one plain "approved" the whole list lands.
- The adapter is the one piece that turns a named action, such as making an issue with its type and its parent, into the tracker's own commands. Today it knows GitHub and GitLab.

This capability does eight jobs:
- Mark each work item by its type, under the right parent, with no label.
- Keep each item's status in its plan file in step with its own issue, with no roll-ups.
- Land every approved tracker write once, and pick it up after a stop.
- Show the issues worth attention now.
- Record a defect as a bug under the story that brought it in.
- Know the tracker in one tool, so no play, skill or sub-agent names it.
- Link each piece of work to its intent, across trackers.
- Say what each work-item type means.

The first five are built, in full or in part. The last three are not built.
What is built today: the adapter, with 25 named actions over the command lines of GitHub and GitLab; the plan plays /shape-plan and /update-plan, which file each epic and story by its type with no label; the plan tool, which sets an item Done or Dropped from its own issue; the writer of an approved session, which records each write as it is made; and /list-focus-issues, the read-only view of the issues worth attention. The adapter reads the settings' `platform:` line, which names GitHub here; the GitLab path is written but "UNTESTED here".
The line with the other capabilities of Orchestration: Orchestrate agent work through planning shows the plans, and there a person sets the plan's status and direction and the status of an open item; this capability keeps the tracker side true. Making the epics and stories, and keeping the plan file's list of work items in step with the tracker, is Turn intents into agent work's, in Product → Spec.
It matters because a person and an agent can only read where the work stands from the tracker when each item says what it is, where it hangs and whether it is done, and when what the plays write there is exactly what a person approved. It sits in software delivery planning with the other capabilities of Orchestration, and the domain's first paragraph says so.

Features:
- Mark each work item by its type, under the right parent, with no label (fn-mark-item-type): when a play files a work item or takes one into a plan, the item gets its kind's type and a parent of the right kind by a real link, with no label and no type in its title.
- An item's status follows its own issue, with no roll-ups (fn-status-follows-issue): when a work item's own issue closes, its item in the plan file reads Done or Dropped, and nothing is worked out from the items under it.
- Every approved tracker write lands once, and is picked up after a stop (fn-land-tracker-writes-once): the tracker writes of an approved session are made one by one through the adapter, each recorded as it is made, so a run again goes on from its record and never makes an issue twice.
- See the issues worth attention now (fn-see-issues-worth-attention): one of three fixed modes cuts the work tracker's issues to at most ten, each with a reason, its kind and a play only where a fixed table names one.
- Record a defect under the story that brought it in (fn-record-defect-under-story): a defect is recorded as an issue of type Bug under the story whose work brought it in, with its severity and its text.
- One tool knows the tracker (fn-one-tool-knows-tracker): one tool reads the settings and reaches the tracker, and no play, skill or sub-agent names a tracker. Not built.
- Link each piece of work to its intent across trackers (fn-link-work-across-trackers): each piece of work hangs under the business intent it serves by a real parent and child link, also when the intents live in another tracker. Not built.
- Say what each work-item type means (fn-say-what-each-type-means): each type the plays file has one agreed meaning, which Initialize's brief shows. Not built.

What is not built yet:
- No tool knows the tracker. In the words of the plan for the Agent-work tool, "3 plays, 11 skills and 3 agents hold `gh` commands". The settings' `trackers` lines are read by no script, and the older code-host setting names a personal account as the owner, while the trackers name the organization.
- /start-change files a new issue through the track-issue skill, which applies labels and sets no type, and its title check asks for a type tag in the title.
- /list-focus-issues reads labels only, which work items no longer carry, and its table recommends three plays that are gone.
- Nothing files a bug from a finding, and nothing checks a bug's severity line, one severity from P1 to P4 for findings and defects.
- No play links a piece of work to its intent across trackers. The open work of Garura's own intents was moved under them by hand, in the reorganisation of the business intents.
- No part says what each type means, so Initialize's brief has no words to show.
- The merge closes the item above a landed issue once every issue under it is closed, against the rule that nothing rolls up.
- Only GitHub is exercised. On GitLab the actions that set an issue's type stop with a plain message. Jira and Linear are not reached at all.

### Benefit hypothesis
- Who it serves: the product owner, who approves what reaches the tracker and reads where the work stands; the developer, a person or an AI agent who builds the code, who picks up a work item and reads it with its parent from the tracker; the technical lead, who looks at the work in flight; and the plays that file and change work items, which follow its rules.
- What we believe: when every work item says what it is and where it hangs, each item's status follows its own issue, every approved write lands exactly once and the issues worth attention are a short list, a person and an agent can read where the work stands from the tracker and the plan files alone, if the work stands on these rules:
  - The type is in the type field and the parent is a real link, never a label or a title prefix.
  - An item's status follows its own issue, never its children.
  - Nothing reaches the tracker before a person's approval of the exact list, and each write is recorded as it is made.
  - What the issues view shows is chosen by fixed rules, never by judgment.
  - Only one tool knows the tracker.
- How we will know: after each approved session and each merge, the plan file and the tracker agree: each item's issue has its kind's type and its kind's parent, carries no label, and is closed exactly when its item reads Done or Dropped; a landing run again after a stop makes no second issue; and the issues view gives the same list for the same issues and mode.
  - The part on labels and types does not hold today for the issues /start-change files, and the last rule has no tool yet.

### Boundary (In / Out / Never)
- In: the type and the parent of each work item the plays file or take into a plan, and the rule that a work item carries no label and no type in its title.
- In: each item's status following its own issue: Done when it closed as completed, Dropped when it closed as not planned, and the session's list of items closed in the tracker.
- In: landing the tracker writes of an approved list once each, and picking them up after a stop.
- In: showing the issues worth attention now, read only.
- In: recording a defect as a bug under the story that brought it in, with its text and its severity.
- In, not built: the one tool that knows the tracker, the link from each piece of work to its intent across trackers, and the meaning of each type.
- Out: making the epics and stories of an intent, changing work items in a session, and keeping the plan file's list of work items in step with the tracker. Turn intents into agent work, in Product → Spec, owns them.
- Out: seeing the plans, the plan's status and direction, the status a person sets on an open item, the order of the work and the plan's branch. Orchestrate agent work through planning, in Orchestration, owns them.
- Out: the merge that closes an issue. Ship every change the same way, in Developer tooling, owns it; its merge runs this capability's plan tool to set the item Done.
- Out: making the tracker's types in a project. Initialize, in Install and distribute, owns it.
- Out: the tracker settings, and the rule that no play, skill or sub-agent names a tracker. Standards, structure, settings and memory owns them; the tool that meets the rule is this capability's.
- Out: running plays as loops, recording ADRs, and the way past each gate. Run plays as loops, Manage ADRs and Give every gate a way past, in Orchestration, own them.
- Out: finding a defect, and fixing it. The tests of Code → Validation find defects; Fix defects test first, in Design → Code, fixes them.
- Never: write to the tracker before a person's approval of the exact list. The reason: the writer refuses unless the approval is for the list as it is now, "so only the list the person saw lands."
- Never: work a status out from the items under it. The reason, in the product owner's words: "When I said status cannot be updated, I mean don't do rollups."
- Never: mark a type by a label or by a prefix in the title. The reason: "Never encode the type as a title prefix", because "the field is the only place it belongs."
- Never: make an issue twice, add a label, or delete an issue. The reason: "No labels are added, and nothing is deleted.", and a create looks for its own marker first, "so an issue is never made twice."
- Never: write the test or the check that found a defect into its bug. The reason: builders read the tracker, and "anything the builder could read, it would end up writing to."

### Guiding rules
- The type is the tracker's type field, and the parent is a real link. The reason: "Type lives in the type field.", and "A reader sees what an issue is from its type, as the tracker shows it."
- A play finds which epic stands for a slice, and which story for a feature, by the plan file's mark. The reason: "It never finds one by its issue type or by its title."
- An item's status follows its own issue, and nothing rolls up. The reason: "An item's status in a plan file follows its own GitHub issue.", and "A parent never changes because its children closed".
- Only the list the person approved lands, and only through the adapter. The reason: "Only the list the person approved, and only through the platform adapter's verbs."
- Each write is recorded as it is made, and a run again goes on from the record. The reason: a landing that stops part way must neither lose a write nor make it twice.
- What the issues view shows comes from fixed rules, and it says nothing where the rules name nothing. The reason: "The cardinal rule: silence beats a wrong answer."
- Only tools know the tracker, and the parts move onto the tool over time. The reason: "Plays, skills and sub-agents know only the tool, never the tracker.", and "A team can choose its tracker as a setting, and a new tracker means changing one tool."
- Not decided: whether a Spike, a Chore and a Bug carry the label `work-item`, as the ontology and ADR 056 say, or no label, as managing-work.md and /update-plan do.
- Not decided: what "the backlog" of the agreed line is: the open work items in the tracker, or the open items of the plan files.

## Sources
- The capability list the product owner locked on 2026-11-03: "Track execution in the team's tracker: The product's execution is tracked in the tracker Garura connects to, for completion status and the backlog."; and his words of 2026-11-10: "Anything that already exists, like managing ADRs and execution tracking, just use what is already built to do that."
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed.", "Any work traces up to its intent and down to its result."
- core/config.yaml: "Tools read this; plays, skills and sub-agents never name a tracker.", "platform: github"
- core/components/skills/platform-adapter/SKILL.md: "Exposes exactly 25 verbs", "Create an issue with its type and its parent in one call (GitHub only; GitLab stops with a plain message)"
- core/components/skills/track-plan-changes/scripts/platform_adapter.py: "UNTESTED here"
- core/components/skills/track-plan-changes/scripts/track_changes.py: "so only the list the person saw lands."
- core/components/skills/track-plan-changes/SKILL.md: "No labels are added, and nothing is deleted.", "so an issue is never made twice.", "Only the list the person approved, and only through the platform adapter's verbs."
- core/components/skills/track-issue/SKILL.md: "Comma-separated labels to apply on create"
- core/components/plays/start-change/scripts/validate_issue.py: "title carries a type tag: [ENH] [BUG] [FEAT] [DOCS] [TASK]"
- core/components/plays/list-focus-issues/reference/ice.md: "The cardinal rule: silence beats a wrong answer."
- core/components/plays/list-focus-issues/reference/kind-map.yaml: "command: grill", "command: refactor", "command: shape"
- core/tools/plan/README.md: "Nothing rolls up: the item's parent is never changed."
- .garura/user-provided/managing-work.md: "Type lives in the type field.", "Never encode the type as a title prefix", "the field is the only place it belongs.", "No labels, for now.", "anything the builder could read, it would end up writing to."
- docs/adr/056-an-epic-and-a-story-are-marked-by-their-issue-type-with-no-label.md: "A reader sees what an issue is from its type, as the tracker shows it.", "It never finds one by its issue type or by its title.", "A Spike, a Chore and a Bug keep the label `work-item`."
- docs/adr/064-an-items-status-in-a-plan-follows-its-own-issue-with-no-roll-ups.md: "An item's status in a plan file follows its own GitHub issue.", "A parent never changes because its children closed", and the product owner: "When I said status cannot be updated, I mean don't do rollups."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "Plays, skills and sub-agents know only the tool, never the tracker.", "A team can choose its tracker as a setting, and a new tracker means changing one tool.", "Two settings for one tracker can disagree, and on the owner they already do."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "the label `work-item` on a Spike, a Chore or a Bug only"
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/capability.md: "In: keeping the plan file's list of work items in step with the tracker."
- .garura/product/product-os/software-delivery-planning/ship-every-change/capability.md: "an issue in a plan is closed with its item set Done."
- .garura/product/product-os/software-delivery-planning/initialize/capability.md: "what each tracker type means is for Track execution in the team's tracker, in Orchestration, to say"
- .garura/product/product-os/software-delivery-planning/fix-defects-test-first/capability.md: "recording a defect in the tracker, as a bug under the story that brought it in, with its text and its severity. Orchestration owns it"
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/fn-keep-tracker-matched/feature.md: "Tracking the agent work's own status in the tracker. Track execution in the team's tracker owns it."
- The stock-take of Orchestration (2026-11-10), sections 3, 6.3, 6.4, 9, 10 and 11 (lean 5).
- The short line beside each built feature: the opening words of that feature's own page.
- Shelf: none. No knowledge shelf in any memory tier covers how a team tracks its work in a tracker.
- .garura/product/product-os/software-delivery-planning/domain.md: "It also orchestrates the work: it chooses and orders what runs next, runs plays as loops, tracks the work in the team's tracker, records each decision on how the project is built as an ADR, and gives every gate a way past."
