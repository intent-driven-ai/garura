# Feature: Set up the tracker's work-item types

## What it does
- Words this page uses. The tracker is the system where the project's team keeps its work items (GitHub, Jira, Linear or another). The adapter is the one piece that reads and writes the tracker, so neither initialize nor any play calls a tracker directly. The brief is the message `initialize` shows the product owner, where they type yes or no. The mapping is the record that tells the plays which of the tracker's own types to use for each type they file. A stand-in is a type the tracker already has that the mapping names in place of a type the tracker cannot make.
- Runs as part of `initialize`. It reads which tracker the project uses and the issue types that tracker already has, and compares them with the issue types Garura files: Business Intent, Epic, Story, Bug, Chore and Spike. Business Intent is the one product-layer type among them: it holds a need the product meets for its user, while the other five are work items, the work done to meet it.
- Every tracker comes through the same adapter, and inside it each tracker has its own way to make a type, so a play never needs to know which tracker the project uses.
- It lists each needed type with its one-line meaning and says which are there, which are missing and which the tracker cannot make. After the product owner's typed yes, it makes each missing type and records what it made.
- Where a tracker cannot make a type, it proposes a stand-in and writes it to the mapping only after the product owner's typed yes. The plays read that mapping, so they file each work item as the right type or its named stand-in.
- It exists because a tracker does not always have these types: on 2026-10-25 Garura's own GitHub organization had no Epic type, so /shape-plan could not file an Epic as an Epic (#875). Every project meets the same gap the first time a play writes to its tracker.

## Inputs / Outputs
- In: which tracker the project uses, read from the project's settings.
- In: the issue types the tracker has now, and whether it lets a new type be made, both read through the adapter.
- In: the list of types the plays need, each with the one-line meaning the brief shows (the meanings are our default; #881 names the types but not their meanings):
  - Business Intent: a need the product meets for its user, with the outcome and the proof that it is met.
  - Epic: one slice of a business intent that a person can test end to end, holding its stories.
  - Story: one feature of a slice, with its scope of work, under its epic.
  - Bug: something the product does wrong against what a story said it would do.
  - Chore: work that keeps the product healthy and changes nothing a person sees, such as an upgrade.
  - Spike: a time-boxed look into an unknown, with a finding as its result.
- In: the product owner's typed yes, for each type to make and each stand-in to record.
- Out: a brief that lists each needed type, its meaning, and whether it is there, missing (and can be made), or cannot be made (with the proposed stand-in and why it is the closest).
- Out: each missing type made in the tracker, after the yes.
- Out: the mapping: each needed type and the tracker type it is filed as, its own or a stand-in the product owner said yes to.
- Out: a record of what was made and what was mapped, kept beside the mapping in the project's settings, so a later run and a person both find it where the plays read the mapping: each type, made / already there / stand-in / failed / still missing, the date, and for a failure what failed. Our default; the sources do not say where the mapping or the record is kept.

## Rules & behavior
- Nothing is made in the tracker and no stand-in is written to the mapping before the product owner's typed yes. A tracker is an outside system, and a new type there, or a work item filed as some other type, is seen by the whole team.
- When every needed type is already there, initialize says so and makes nothing, because a second copy of a type would split the team's work items between two types.
- "Cannot make" and "making failed" are two different cases, and the adapter tells them apart before anything is tried. A tracker cannot make a type when the adapter says the tracker has no way to add a type of its own, for example a tracker with a fixed list of types; that type gets a proposed stand-in. Making failed when the tracker has a way to add a type but the try did not work, for example the account has no right to add a type to the GitHub organization; that type gets no stand-in and stays unmapped, because a person with the right can still make the real type.
- Who picks a stand-in: initialize proposes it, and the product owner decides. Initialize proposes the tracker's own type closest in meaning (for example the plain Issue type with a label named after the needed type), shows it in the brief with why it is the closest, and writes it to the mapping only on the product owner's typed yes. The product owner can name a different type instead. A first stand-in needs the same typed yes as a later change to the mapping, because both decide how the team's work items are filed.
- When the product owner says no to a proposed stand-in, the type stays unmapped, and the brief names it, so a play that needs it stops with the message below.
- GitHub works first. Jira and Linear come through the same adapter, each with its own way to make a type, so adding a tracker adds one entry to the adapter and changes no play.
- The mapping is what the filing plays are to read. A play that writes to the tracker is to read the mapping before it writes, and when a type it needs is missing and not mapped, stop with a plain message that points to `initialize`; it is never to file the item as some other type on its own, because the product owner never agreed to that type. The change to the filing plays that makes them do this is a later story of this business intent, not this feature (see Out of scope); this feature writes the mapping they read and names, in the brief and the record, each type that is still missing.
- Where the mapping is kept is our default: with the project's settings that the plays already read, so no play needs a new place to look. The sources do not say where.
- When the person says no to the whole brief, nothing is made and nothing is mapped, and the brief names each type that is still missing so the plays that need it stop with the message above.
- When the person says yes to only some of the missing types, initialize makes only those. The rest stay missing and unmapped, and the brief names each of them, because a yes to one type is not a yes to another.
- When making a type fails, initialize says in plain words what failed and why, tries nothing further for that type, and leaves it unmapped, so a play that needs it stops with the message that points to `initialize`. It goes on with the other approved types, because one failure says nothing about them. Our default; the sources do not say what happens when a make fails.
- When a mapping already exists from an earlier run, initialize keeps it, shows it in the brief, and changes it only on a new typed yes, because the plays already file work by it. The rest of a re-run, such as a change of tracker, is Run initialize again's (fn-rerun-initialize).

## Acceptance criteria
- Given a GitHub project whose organization has no Epic type, when initialize runs, then the brief lists the six types with their meanings and marks Epic as missing.
- Given a GitHub organization with no Epic type and a brief that marks Epic missing, when the product owner types yes, then the Epic type is made in the organization and the record names it.
- Given a GitHub organization with no Epic type and a brief that marks Epic missing, when the product owner does not type yes, then no type is made in the tracker.
- Given a tracker whose adapter entry says it cannot make the Spike type, when initialize runs, then the brief says so in plain words and proposes a stand-in for Spike with why it is the closest.
- Given a brief that proposes a stand-in for Spike, when the product owner types yes, then the mapping names that stand-in for Spike.
- Given a brief that proposes a stand-in for Spike, when the product owner says no, then the mapping holds nothing for Spike and the brief names Spike as unmapped.
- Given a tracker where all six types exist, when initialize runs, then it makes nothing and says every type is there.
- Given a type that is missing and not mapped after the run, when the mapping and the record are read, then the mapping holds nothing for that type and the record names it as still missing, which is all a filing play needs to stop and point to `initialize`.
- Given Epic and Spike are missing, when the product owner types yes for Epic only, then only Epic is made, and the brief and the record name Spike as still missing.
- Given the account has no right to add a type to the organization, when initialize tries to make Epic, then it says in plain words that the make failed and why, proposes no stand-in, and Epic stays unmapped.
- Given a mapping from an earlier run, when initialize runs again and the product owner types no change, then the brief shows that mapping and the mapping is unchanged.

## Out of scope
- Filing epics, stories and other work items (/shape-plan and the other filing plays own them).
- Changing the filing plays (/shape-plan and the plays that file work items) to read the mapping before they write, and to stop with a plain message that points to `initialize` when a type they need is missing and not mapped: a later story of this business intent owns it, not filed yet, outside this feature, because it changes those plays and not initialize. This feature only writes the mapping and the record they read. Our default; #881 says a play that writes to the tracker stops and points to `initialize`, but does not say which story changes the plays.
- Shaping the slice and the plan that the work items come from (/shape-slice and /shape-plan own them).
- How Jira and Linear each make a type inside the adapter, which comes after GitHub; this feature fixes only what the adapter must answer for every tracker (the types there, whether a type can be made, and making it).
- Asking the other setup questions (Ask the setup questions, fn-setup-questions, owns them).
- Moving to a different tracker on a later run (Run initialize again, fn-rerun-initialize, owns it).

## Sources
- GitHub #881: "Garura files its work as issues of fixed types: Business Intent, Epic, Story, Bug, Chore and Spike. A tracker does not always have them."
- GitHub #881: "On 2026-10-25 Garura's own GitHub organization had no Epic type, so `/shape-plan` could not file an Epic as an Epic (#875)."
- GitHub #881, Done when: "It makes each missing type only after the person's typed yes, and records what it made"; "Where a tracker cannot make a type, it says so in plain words and names the type it uses in its place; the plays read that mapping"; "GitHub works first. Jira and Linear come through the same adapter, each with its own way to make a type."; "A play that writes to the tracker stops with a plain message when a type it needs is missing, and points to `initialize`."
- ADR 048, Decision 1 (the product model and the work are two layers): "Only the Business Intent is a product-layer tracker issue, labelled `product`."; "The **work layer** is tracker issues labelled `work-item`: Epic, Story, Spike, Chore and Bug."
- Shelf: none; no knowledge shelf in memory covers setting up a software project.

## Agent intent (ICE)
- Goal: After initialize, the project's tracker has each issue type Garura files (Business Intent, Epic, Story, Bug, Chore, Spike), or a stand-in the product owner said yes to, recorded in a mapping that the filing plays read once a later story of this business intent changes them.
- Goal: Initialize lists each needed type with its one-line meaning and says which are missing before it makes anything.
- Limit: Make no type in the tracker and record no stand-in before the product owner's typed yes, and record every type it makes.
- Limit: GitHub first; Jira and Linear come through the same adapter, with no change to a play.
- Fails if: a type is made in the tracker, or a stand-in written to the mapping, without the product owner's typed yes.
- Fails if: a type whose make failed is given a stand-in, or a type the tracker cannot make is left with no proposed stand-in.
- Fails if: a type that is missing and not mapped after the run is not named as still missing in the brief and the record, or the mapping names a type for it that the product owner never said yes to, so a filing play that reads the mapping could file the item as another type.
- Context: serves the product owner and every play that writes to the tracker, such as /shape-plan; found in plan 788 while fixing #875; touches the project's tracker through the adapter; out are filing work items, the change to the filing plays that makes them read the mapping (a later story, not filed yet), and how Jira and Linear each make a type inside the adapter.
- Checked by: run `initialize` on a test GitHub organization with no Epic type, type yes, then check that the Epic type exists, the record names it, and the mapping names Epic for Epic.
