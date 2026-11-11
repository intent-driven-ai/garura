# Feature: Mark each work item by its type, under the right parent, with no label

## What it does
When a play files a work item, or takes one into a plan, the item gets its kind's type in the tracker's type field and hangs under a parent of the right kind by the tracker's own parent and child link, with no label and no type in its title, so a person or an agent sees what the item is, and where it belongs, from the tracker alone.
- The kinds a plan holds, and the type each one gets: an epic is type Epic, a story type Story, a spike type Spike, a chore type Chore and a bug type Bug. A feature item is type Feature: an issue that groups some stories inside one epic. The tracker's type Feature is not a feature of the product model.
- The parent each kind takes: an epic sits at the top of the plan, under no item; a feature item under an epic; a story under an epic or a feature item; a spike, a chore or a bug under a story. A bug hangs under the story whose work brought the defect in.
- The parent is the tracker's own link, made with the child's internal identifier, not its visible number. A mention of the parent in the text is not a link.
- In GitHub, issue types belong to the organization, and a repository under a personal account has none.
- Two plays mark each item this way today:
  - /shape-plan makes each epic as type Epic and each story as type Story under its epic, each in one write, with no label. When it uses an epic or a story that is there already, it sets the right type, takes its labels off and links the story under its epic. Its check then reads each one back and fails on a wrong type, a label or a wrong sub-issue.
  - /update-plan checks each entry of a session before it joins the list: a kind the plan may hold, a parent of the right kind, and no labels on an issue that joins the plan. A new issue is made with its type and its parent in one call; an issue that joins with another type gets its kind's type. A break is shown with what works instead, and the person may say "do it anyway"; the override is recorded in the session's commit.
- Three parts are out of step, with this rule or with the Must not of Orchestration:
  - /start-change files a new issue through the track-issue skill. That skill applies labels on create and sets no type, and /start-change passes it no parent. The agent that calls it passes labels "if determinable from type".
  - /start-change's title check asks for a type tag at the start of the title, such as [BUG] or [FEAT], or a prefix such as `fix:`. This puts the type in the title, which the rule forbids. It is a machine check, and "A non-zero exit is a hard halt regardless of the gate state". The only way past is a new title with a tag, and nothing records what is owed. So it stops a person with no way past.
  - In /shape-plan, an epic that holds work that is not its slice's stops the tracker write until a person files that work in its own place. Unlike a session, there is no override there, so it also stops a person with no way past.
- A play finds which epic stands for a slice, and which story for a feature, by the plan file's mark, never by the type or the title.
- On GitLab, the actions that make an issue with its type and set a type stop with a plain message, and a parent link falls back to a link between equals. So on GitLab no item gets its type or a real parent.
- Examples, in different kinds of project:
  - In a clinic's booking app, /shape-plan files the epic for online booking as type Epic and its three stories as type Story under it, none with a label.
  - In a shop's checkout project, the product owner asks in a session for a chore under the epic, to tidy the payment page. The check shows the break and offers a story it could go under; the product owner names the story, and after "approved" the chore is type Chore under that story.
  - In a bank's payments service, a developer opens a one-off change with /start-change. Today its new issue gets a label, no type and no parent, and its title must start with a tag such as [BUG].
- How it meets the capability: completion status and the backlog can be read from the tracker only when each item says what it is and where it hangs; this feature makes the type field and the parent link say it.

Status: built in part. Built in /shape-plan (#818, the plan play makes the plan file, the epic and one story per feature; #875, the Epic filed as type Epic) and in /update-plan (#730, the plan session). Not built, or open:
- /start-change and the track-issue skill, as above: labels, no type, no parent, and a type tag in the title. No issue is filed for it yet.
- The ontology and ADR 056 keep the label `work-item` on a Spike, a Chore and a Bug, while /update-plan puts no label on any item and managing-work.md says "No labels, for now."
- Initialize's list of the types Garura files names six types, and not the type Feature that a feature item needs (#881, Initialize sets up the tracker's work-item types).
- Only GitHub marks a type. The GitLab path is "UNTESTED here", and Jira and Linear are not reached.

## Inputs / Outputs
- In: the work item to file or take in: its kind, its title and text, and its parent's issue.
- In: for an issue that is there already, its type, labels and parent as the tracker holds them now.
- In: the plan file, for the kind of each item and the parent it sits under.
- In: the types the tracker has.
- Out: the issue in the tracker with its kind's type, under its parent by a real link, with no label.
- Out: for a break of the rules in a session, the break and what works instead, and the person's override when they give one, recorded in the commit.
- Out: in /shape-plan, the check of each epic and story read back from the tracker: their type, their labels and their sub-issues.

## Rules & behavior
- The type is the tracker's type field, never a label and never a tag in the title. The reason: "Type lives in the type field.", "Never encode the type as a title prefix", and "the field is the only place it belongs."
- An epic is type Epic and a story type Story, never type Feature. The reason: "Neither has a label.", and "An Epic is never filed as type Feature.", so the word Feature means one thing in the model.
- Each kind sits under one kind of parent. The reason: "Its tree holds six kinds of item, each under one kind of parent", so each item is found where it belongs.
- The parent is a real link in the tracker. The reason: every story, bug, spike and chore hangs under its parent "as a real parent/child link in the tracker", and "Linking a child to a parent needs the internal identifier, not the issue number."
- An epic or a story is found by the plan file's mark. The reason: "It never finds one by its issue type or by its title."; a type or a title can change, and the mark says what the item stands for.
- In a session, a break is shown with what works instead, and the person may override it. The reason: "A break is shown with what works instead.", and "the override is recorded."; the Must not of Orchestration: "Stop a person. Every gate has a way past it that records what's owed."
- In /shape-plan, other work under an epic stops the write. The reason: "Anything else under an epic is misplaced work", and the play "writes nothing until a person files it in its own place". There is no override.
- A type tag in the title, at /start-change, is a machine check with no way past. The reason it is there: it is a "machine replacement for start-change's confirm-new-issue gate (#467)", a person's check of the title by eye, and it came before the rule that the type lives in the type field.
- Not decided: whether a Spike, a Chore and a Bug carry the label `work-item`, as the ontology and ADR 056 say, or no label, as managing-work.md and /update-plan do.
- Not decided: what marks an epic or a story in a tracker that has no type for it. Initialize's page leaves it here: "how a work item is marked is for Track execution in the team's tracker to decide."

## Acceptance criteria
- Given a slice with two features, when /shape-plan writes its work items, then the epic is type Epic, each story is type Story and a sub-issue of the epic, and none has a label.
- Given a story that is there already with the type Feature and a label, when /shape-plan uses it, then its type becomes Story, its label comes off and it is a sub-issue of its epic.
- Given an issue with a label, when a session puts it into the plan, then the entry shows the break and that its labels come off first, and it joins the list only after "do it anyway", which the commit records.
- Given a chore asked under an epic in a session, when the entry is checked, then the break is shown with a story it could go under.
- Given a new bug under a story in a session, when the list lands, then the tracker holds one issue of type Bug, under that story, with no label.

## Out of scope
- Making the epics and stories of an intent, and changing work items in a session. Turn intents into agent work, in Product → Spec, owns them; this feature holds the rule for each item's type and parent.
- Opening a change's issue and its branch. Open each change where it will land (fn-731), in Developer tooling, does it.
- Making the types in a project's tracker. Initialize, in Install and distribute, owns it.
- Saying what each type means. Say what each work-item type means (fn-say-what-each-type-means) does it, and it is not built.
- Knowing the tracker in one tool. One tool knows the tracker (fn-one-tool-knows-tracker) does it, and it is not built.
- The way past /start-change's title check and /shape-plan's stop. Give every gate a way past, in Orchestration, owns it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, the product owner on 2026-11-10: "Anything that already exists, like managing ADRs and execution tracking, just use what is already built to do that."
- core/components/plays/shape-plan/scripts/write_work_items.py: "becomes an issue of type Epic, with no label, in one write.", "becomes an issue of type Story, with no label and with the epic as its parent, in one write."
- core/components/plays/shape-plan/scripts/check_tracker.py: "each epic has type Epic and each story type Story, and none has a label;"
- core/components/plays/shape-plan/reference/ice.md: "Anything else under an epic is misplaced work", "writes nothing until a person files it in its own place"
- core/components/plays/update-plan/scripts/check_entries.py: "no labels on an issue that joins the plan", "a spike, a chore or a bug under a story"
- core/components/plays/update-plan/reference/ice.md: "A break is shown with what works instead.", "the override is recorded."
- core/components/skills/track-plan-changes/SKILL.md: "a new type, a new parent, a new issue with its type and parent"
- core/components/skills/track-issue/SKILL.md: "Comma-separated labels to apply on create", "parent/child hierarchy is not supported"
- core/components/agents/project-orchestrator.md: "labels: {if determinable from type}"
- core/components/plays/start-change/SKILL.md: "A non-zero exit is a hard halt regardless of the gate state"
- core/components/plays/start-change/scripts/validate_issue.py: "title carries a type tag: [ENH] [BUG] [FEAT] [DOCS] [TASK]", "machine replacement for start-change's confirm-new-issue gate (#467)"
- core/components/skills/platform-adapter/SKILL.md: "Create an issue with its type and its parent in one call (GitHub only; GitLab stops with a plain message)", "Set an issue's type (GitHub only; GitLab stops with a plain message)"
- core/components/skills/track-plan-changes/scripts/platform_adapter.py: "UNTESTED here"
- .garura/user-provided/managing-work.md: "Type lives in the type field.", "Never encode the type as a title prefix", "the field is the only place it belongs.", "No labels, for now.", "as a real parent/child link in the tracker", "Linking a child to a parent needs the internal identifier, not the issue number.", "a repository under a personal account has no issue types at all"
- docs/adr/056-an-epic-and-a-story-are-marked-by-their-issue-type-with-no-label.md: "Neither has a label.", "An Epic is never filed as type Feature.", "It never finds one by its issue type or by its title.", "A Spike, a Chore and a Bug keep the label `work-item`."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Its tree holds six kinds of item, each under one kind of parent", "in a plan, an issue of type Feature is a feature item, a group of stories inside an epic", "the label `work-item` on a Spike, a Chore or a Bug only"
- .garura/product/product-os/software-delivery-planning/initialize/fn-881/feature.md: "how a work item is marked is for Track execution in the team's tracker to decide."
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- The history in git: validate_issue.py was added on 2026-07-04 (#467), and the rule "Never encode the type as a title prefix" reached managing-work.md on 2026-08-27.
- GitHub #818 (closed): "The plan play makes the plan file, the epic and one story per feature"
- GitHub #875 (closed): "a slice's Epic must be type Epic"
- GitHub #730 (closed): "The /update-plan session"
- GitHub #881 (open): "Initialize sets up the tracker's work-item types"
