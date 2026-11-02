## Decision

How Garura's parts are named changes, so the name says who does the work and what it does. Nothing is renamed by this decision; the plays are renamed later. The full list of names is in `.garura/project/issues/1021/context/names.md`.

1. Five roles: specifier, designer, builder, validator, orchestrator. A verb belongs to one role, and a role can have several verbs. The verb says who does it; the business intent says which move it serves.
2. The fixed verb lists are replaced by each role's verbs, as `names.md` shows.
3. Loops are their own category, with one for each transition between the phases, named `loop-<from>-<to>`. There is no Ship loop.
4. Commands that open, commit, review and merge work are not tied to a role, because anyone can run them. Their final place is still open, and they sit under Developer tooling for now.
5. Installing and removing Garura are product plays with no role. Locking a design is a governance check, and initialize, seeding memory and upgrade are engine things, not plays.
6. A name may not be exactly a tool's built-in command, but it may start with one. `env`, `perf` and `uat` join the allowed short words.

## Why now

The product owner wants the product model fixed with the right verbs before its capabilities and features are written, so each one says which role performs it. Verbs today do not tell who acts: `author` is used by 21 live skills, and `shape` does three different jobs.

## Options considered

- Only five verbs, one per role, for everything. Lost: it reads badly for the orchestrator, whose work is several kinds of thing, and names like `/orchestrate-start` do not say what they do. A builder also builds, fixes and refactors.
- Keep today's verbs and only list them by role. Lost: names still would not tell who does the work.
- Move opening, committing, reviewing and merging into shared steps inside build plays. Lost: anyone can run them, so they are not a builder's, and it would mean a large rebuild.
- Keep loops named for what they do, like Discovery and Execute. Lost: the product owner wants one thing to remember for each transition.
- Keep the ban on starting a name with a built-in command. Lost: it blocks `design-`, which the product owner wants a designer to use.

## Decided by

The product owner, 2026-11-03.

## Decided in

#1021, with the five roles recorded in #1015.

## Shape

markdown
