# Feature: Set up the tracker's work-item types

## What it does
- Runs as part of `initialize`. It reads which tracker the project uses (GitHub, Jira, Linear or another) and the work-item types that tracker already has, and compares them with the types Garura's plays file: Business Intent, Epic, Story, Bug, Chore and Spike.
- It lists each needed type with its one-line meaning and says which are missing. After the product owner's typed yes, it makes each missing type and records what it made.
- Where a tracker cannot make a type, it says so in plain words and names the type it uses in its place. The plays read that mapping, so they file each work item as the right type or its named stand-in.
- It exists because a tracker does not always have these types: on 2026-10-25 Garura's own GitHub organization had no Epic type, so /shape-plan could not file an Epic as an Epic (#875). Every project meets the same gap the first time a play writes to its tracker.

## Inputs / Outputs
- In: which tracker the project uses, read from the project's settings.
- In: the work-item types the tracker has now, read from the tracker.
- In: the list of types the plays need, each with the one-line meaning the brief shows (the meanings are our default; #881 names the types but not their meanings):
  - Business Intent: a need the product meets for its user, with the outcome and the proof that it is met.
  - Epic: one slice of a business intent that a person can test end to end, holding its stories.
  - Story: one feature of a slice, with its scope of work, under its epic.
  - Bug: something the product does wrong against what a story said it would do.
  - Chore: work that keeps the product healthy and changes nothing a person sees, such as an upgrade.
  - Spike: a time-boxed look into an unknown, with a finding as its result.
- In: the product owner's typed yes, before any type is made.
- Out: a brief that lists each needed type, its meaning, and whether it is there, missing, or cannot be made.
- Out: each missing type made in the tracker, after the yes.
- Out: the type mapping the plays read: each needed type and the tracker type it is filed as, its own or a named stand-in.
- Out: a record of what was made and what was mapped, kept beside the mapping in the project's settings, so a later run and a person both find it where the plays read the mapping: each type, made / already there / stand-in / failed, the date, and for a failure what failed. Our default; the sources do not say where the record is kept.

## Rules & behavior
- Nothing is made in the tracker before the product owner's typed yes. A tracker is an outside system, and a new type there is seen by the whole team.
- When every needed type is already there, initialize says so and makes nothing.
- When a tracker cannot make a type, initialize says so in plain words, names the type it uses in its place, and records that in the mapping. It never leaves a needed type with no mapping.
- GitHub works first. Jira and Linear come through the same adapter, each with its own way to make a type, so adding a tracker adds one adapter and changes no play.
- A play that writes to the tracker reads the mapping before it writes. When a type it needs is missing and not mapped, the play stops with a plain message and points to `initialize`; it never files the item as some other type on its own.
- Where the mapping is kept is our default: with the project's settings that the plays already read. The sources do not say where.
- When the person says no, nothing is made, and the brief names each type that is still missing so the plays that need it stop with the message above.
- When the person says yes to only some of the missing types, initialize makes only those. The rest stay missing and unmapped, and the brief names each of them, because a yes to one type is not a yes to another.
- When making a type fails (for example the account has no right to add a type to the GitHub organization), initialize says in plain words what failed and why, tries nothing further for that type, and leaves it unmapped, so a play that needs it stops with the message that points to `initialize`. It goes on with the other approved types, because one failure says nothing about them. Our default; the sources do not say what happens when a make fails.
- When a mapping already exists from an earlier run, initialize keeps it, shows it in the brief, and changes it only on a new typed yes, because the plays already file work by it. The rest of a re-run is fn-rerun-initialize's.

## Acceptance criteria
- Given a GitHub project whose organization has no Epic type, when initialize runs, then the brief lists the six types with their meanings and marks Epic as missing.
- Given that brief, when the product owner types yes, then the Epic type is made in the organization and the record names it.
- Given that brief, when the product owner does not type yes, then no type is made in the tracker.
- Given a tracker that cannot make a type, when initialize runs, then it says so in plain words, names the stand-in type, and the mapping holds that stand-in.
- Given a tracker where all six types exist, when initialize runs, then it makes nothing and says every type is there.
- Given a type a play needs is missing and not mapped, when that play writes to the tracker, then it stops with a plain message that points to `initialize`.
- Given Epic and Spike are missing, when the product owner types yes for Epic only, then only Epic is made, and the brief and the record name Spike as still missing.
- Given the account has no right to add a type to the organization, when initialize tries to make Epic, then it says in plain words that the make failed and why, and Epic stays unmapped.
- Given a mapping from an earlier run, when initialize runs again, then the brief shows that mapping and it is unchanged unless the product owner types yes to a change.

## Out of scope
- Filing epics, stories and other work items (/shape-plan and the other filing plays own them).
- Shaping the slice and the plan that the work items come from (/shape-slice and /shape-plan own them).
- The Jira and Linear adapters' own detail, which comes after GitHub through the same adapter.
- Asking the other setup questions (fn-setup-questions owns them).

## Sources
- GitHub #881: "Garura files its work as issues of fixed types: Business Intent, Epic, Story, Bug, Chore and Spike. A tracker does not always have them."
- GitHub #881: "On 2026-10-25 Garura's own GitHub organization had no Epic type, so `/shape-plan` could not file an Epic as an Epic (#875)."
- GitHub #881, Done when: "It makes each missing type only after the person's typed yes, and records what it made"; "Where a tracker cannot make a type, it says so in plain words and names the type it uses in its place; the plays read that mapping"; "GitHub works first. Jira and Linear come through the same adapter"; "A play that writes to the tracker stops with a plain message when a type it needs is missing, and points to `initialize`."
- Shelf: none (routing.yaml, unmatched).

## Agent intent (ICE)
- Goal: After initialize, the project's tracker has each type the plays file (Business Intent, Epic, Story, Bug, Chore, Spike), or a named stand-in recorded in a mapping the plays read.
- Goal: Initialize lists each needed type with its one-line meaning and says which are missing before it makes anything.
- Limit: Make no type in the tracker before the product owner's typed yes, and record every type it makes.
- Limit: GitHub first; Jira and Linear come through the same adapter, with no change to a play.
- Fails if: a type is made in the tracker without the product owner's typed yes.
- Fails if: a needed type is missing after initialize ran and has no stand-in in the mapping.
- Fails if: a play that needs a missing type files the item as another type, or stops without a message that points to `initialize`.
- Context: serves the product owner and every play that writes to the tracker, such as /shape-plan; found in plan 788 while fixing #875; touches the project's tracker through its adapter; out are filing work items and the Jira and Linear adapters' own detail.
- Checked by: run `initialize` on a test GitHub organization with no Epic type, type yes, then check that the Epic type exists, the record names it, and /shape-plan files an Epic as an Epic.
