# Feature: Set up the tracker's work-item types

## What it does
As part of Initialize, it finds the tracker the project uses and the issue types that tracker has, lists the types Garura files with their meanings and says which are missing, makes each missing type after the product owner's typed yes, and records a stand-in, also after a typed yes, where the tracker cannot make one, so no play stops the first time it files a work item.
- Words this page uses. The tracker is the system where the project's team keeps its work items (GitHub, Jira, Linear or another). The adapter is the one piece that reads and writes the tracker, so neither initialize nor any play calls a tracker directly. The brief is the message Initialize shows the product owner, where they type yes or no. The mapping is the record that tells the plays which of the tracker's own types to use for each type they file. A stand-in is a type the tracker already has that the mapping names in place of a type the tracker cannot make.
- It reads which tracker the project uses and the issue types that tracker already has, and compares them with the issue types Garura files: Business Intent, Epic, Story, Bug, Chore and Spike. Business Intent is the one product-layer type among them: it holds a need the product meets for its user, while the other five are work items, the work done to meet it.
- A project's settings can name one tracker for its business intents and another for its work, as Garura's own settings do. Each type is set up in the tracker that holds it: Business Intent in the intents tracker, the five work-item types in the work tracker.
- Every tracker comes through the same adapter, and inside it each tracker has its own way to make a type, so a play never needs to know which tracker the project uses.
- It lists each needed type with its one-line meaning and says which are there, which are missing and which the tracker cannot make. After the product owner's typed yes, it makes each missing type and records what it made. What each type means is for Track execution in the team's tracker, in Orchestration, to say; the brief shows its words.
- Where a tracker cannot make a type, it proposes a stand-in and writes it to the mapping only after the product owner's typed yes. The plays read that mapping, so they file each work item as the right type or its named stand-in.
- It exists because a tracker does not always have these types: on 2026-10-25 Garura's own GitHub organization had no Epic type, so /shape-plan could not file an Epic as an Epic. Every project meets the same gap the first time a play writes to its tracker.
- Examples, in different kinds of project:
  - A shop's team on GitHub whose organization has no Epic and no Spike type: the brief marks both missing, and each is made only after the yes.
  - A bank's team whose tracker has a fixed list of types that a project cannot add to: the brief says the tracker cannot make the missing types, proposes a stand-in for each, and writes each to the mapping only after the yes.
  - A school's team that keeps its business intents in one tracker and its work in another: Business Intent is set up in the first, and the five work-item types in the second.
- How it meets the capability: the capability's fifth check, "The tracker holds each issue type Garura files, or a stand-in the product owner said yes to", is met here.

Status: not built. The adapter reaches GitHub and GitLab. On GitHub it makes an issue of a type the organization has, and stops when the type is missing: "An `issue_type` the repository does not have stops with exit 1, and nothing is made." No step lists a tracker's types or makes one. Its GitLab entry sets no type at all ("GitLab has no issue types here."), and Jira and Linear have no entry. Garura's own GitHub organization holds the six types and a Feature type, each with a description, all made by hand, the Epic type on 2026-10-25. No play reads a mapping, because none exists.

## Inputs / Outputs
- In: which tracker the project uses, read from the project's settings, which can name one tracker for business intents and another for work.
- In: the issue types each tracker has now, and whether it lets a new type be made, both read through the adapter.
- In: the list of types the plays need, each with the one-line meaning the brief shows, as Track execution in the team's tracker gives it.
- In: the product owner's typed yes, for each type to make and each stand-in to record.
- Out: a brief that lists each needed type, its meaning, and whether it is there, missing (and can be made), or cannot be made (with the proposed stand-in and why it is the closest).
- Out: each missing type made in the tracker, after the yes.
- Out: the mapping: each needed type and the tracker type it is filed as, its own or a stand-in the product owner said yes to.
- Out: a record of what was made and what was mapped, which a later run and a person both find where the plays read the mapping: each type, made / already there / stand-in / failed / still missing, the date, and for a failure what failed.

## Rules & behavior
- Nothing is made in the tracker and no stand-in is written to the mapping before the product owner's typed yes. A tracker is an outside system, and a new type there, or a work item filed as some other type, is seen by the whole team.
- When every needed type is already there, initialize says so and makes nothing, because a second copy of a type would split the team's work items between two types.
- "Cannot make" and "making failed" are two different cases, and the adapter tells them apart before anything is tried. A tracker cannot make a type when the adapter says the tracker has no way to add a type of its own, for example a tracker with a fixed list of types; that type gets a proposed stand-in. Making failed when the tracker has a way to add a type but the try did not work, for example the account has no right to add a type to the GitHub organization; that type gets no stand-in and stays unmapped, because a person with the right can still make the real type.
- Who picks a stand-in: initialize proposes it, and the product owner decides. Initialize proposes the tracker's own type closest in meaning, shows it in the brief with why it is the closest, and writes it to the mapping only on the product owner's typed yes. The product owner can name a different type instead. A first stand-in needs the same typed yes as a later change to the mapping, because both decide how the team's work items are filed.
- Not decided: what a stand-in for an Epic or a Story can be, since an Epic and a Story are marked by their type and "Neither has a label."; how a work item is marked is for Track execution in the team's tracker to decide.
- When the product owner says no to a proposed stand-in, the type stays unmapped, and the brief names it, so a play that needs it stops with the message below.
- GitHub works first. Jira and Linear come through the same adapter, each with its own way to make a type, so adding a tracker adds one entry to the adapter and changes no play. The reason: Standards, structure, settings and memory must not "Name a tracker in a play, skill or sub-agent, because they only know the tool."
- The mapping is what the filing plays are to read. A play that writes to the tracker is to read the mapping before it writes, and when a type it needs is missing and not mapped, stop with a plain message that points to initialize; it is never to file the item as some other type on its own, because the product owner never agreed to that type. The change to the filing plays that makes them do this is a later story of Initialize, not this feature (see Out of scope); this feature writes the mapping they read and names, in the brief and the record, each type that is still missing.
- Not decided: where the mapping and its record are kept. Initialize and the install "never write the same files", and the install and the upgrade write Garura's settings file.
- When the person says no to the whole brief, nothing is made and nothing is mapped, and the brief names each type that is still missing so the plays that need it stop with the message above.
- When the person says yes to only some of the missing types, initialize makes only those. The rest stay missing and unmapped, and the brief names each of them, because a yes to one type is not a yes to another.
- When making a type fails, initialize says in plain words what failed and why, tries nothing further for that type, and leaves it unmapped, so a play that needs it stops with the message that points to initialize. It goes on with the other approved types, because one failure says nothing about them.
- When a mapping already exists from an earlier run, initialize keeps it, shows it in the brief, and changes it only on a new typed yes, because the plays already file work by it. The rest of a re-run, such as a change of tracker, belongs to Update the setup as the project changes (fn-rerun-initialize).

## Acceptance criteria
- Given a GitHub project whose organization has no Epic type, when initialize runs, then the brief lists the six types with their meanings and marks Epic as missing.
- Given a GitHub organization with no Epic type and a brief that marks Epic missing, when the product owner types yes, then the Epic type is made in the organization and the record names it.
- Given a GitHub organization with no Epic type and a brief that marks Epic missing, when the product owner does not type yes, then no type is made in the tracker.
- Given a tracker whose adapter entry says it cannot make the Spike type, when initialize runs, then the brief says so in plain words and proposes a stand-in for Spike with why it is the closest.
- Given a brief that proposes a stand-in for Spike, when the product owner types yes, then the mapping names that stand-in for Spike; when the product owner says no, then the mapping holds nothing for Spike and the brief names Spike as unmapped.
- Given a tracker where all six types exist, when initialize runs, then it makes nothing and says every type is there.
- Given a type that is missing and not mapped after the run, when the mapping and the record are read, then the mapping holds nothing for that type and the record names it as still missing, which is all a filing play needs to stop and point to initialize.
- Given Epic and Spike are missing, when the product owner types yes for Epic only, then only Epic is made, and the brief and the record name Spike as still missing.
- Given the account has no right to add a type to the organization, when initialize tries to make Epic, then it says in plain words that the make failed and why, proposes no stand-in, and Epic stays unmapped.
- Given settings that name one tracker for business intents and another for work, when initialize runs, then the brief checks Business Intent in the first and the five work-item types in the second.
- Given a mapping from an earlier run, when initialize runs again and the product owner types no change, then the brief shows that mapping and the mapping is unchanged.

## Out of scope
- Turning an intent into epics, stories and other work items, and filing them (Turn intents into agent work owns it).
- What each type means and how a work item is marked (Track execution in the team's tracker, in Orchestration, owns them).
- Changing the filing plays (/shape-plan and the plays that file work items) to read the mapping before they write, and to stop with a plain message that points to initialize when a type they need is missing and not mapped: a later story of Initialize owns it, outside this feature, because it changes those plays and not initialize. This feature only writes the mapping and the record they read. The reason: the product owner's review of the change that first recorded this page asked that "the [Set up the tracker's work-item types] page must name the later story that changes the filing plays".
- How Jira and Linear each make a type inside the adapter, which comes after GitHub; this feature fixes only what the adapter must answer for every tracker (the types there, whether a type can be made, and making it).
- Asking the other setup questions (Ask the setup questions, fn-setup-questions, owns them).
- Moving to a different tracker on a later run (Update the setup as the project changes, fn-rerun-initialize, owns it).

## Sources
- The product owner's verdict in round 1 of the review of the change that first recorded this page: "the [Set up the tracker's work-item types] page must name the later story that changes the filing plays"
- docs/adr/048-the-product-model-and-the-work-are-two-layers.md, Decision 1: "Only the Business Intent is a product-layer tracker issue, labelled `product`."
- docs/adr/056-an-epic-and-a-story-are-marked-by-their-issue-type-with-no-label.md: "Neither has a label.", "An Epic is never filed as type Feature.", "A later change decides how these four kinds are marked."
- core/config.yaml, the trackers: "Tools read this; plays, skills and sub-agents never name a tracker.", "business intents", "agent work: epics, stories, bugs, chores, spikes"
- core/components/skills/platform-adapter/reference/github/verbs.md: "An `issue_type` the repository does not have stops with exit 1, and nothing is made."
- core/components/skills/platform-adapter/reference/gitlab/verbs.md: "GitLab has no issue types here."
- .garura/product/product-os/intents/bi-10.md: "Name a tracker in a play, skill or sub-agent, because they only know the tool."
- .garura/product/product-os/software-delivery-planning/install-into-project/capability.md: "the two never write the same files"
- .garura/product/product-os/software-delivery-planning/initialize/capability.md: "The tracker holds each issue type Garura files, or a stand-in the product owner said yes to"
- The issue types of Garura's own GitHub organization, read through GitHub on 2026-11-10: Story, Bug, Feature, Business Intent, Chore, Spike and Epic, each with a description.
- Shelf: none; no knowledge shelf in memory covers setting up a software project.
