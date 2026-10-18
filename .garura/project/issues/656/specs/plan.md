---
plan_for: 656
kind: story
serves: "#656 — Phoenix memory has its own repository, and each project pulls only the subset it needs into Garura memory"
status: active
updated: 2026-10-18
now: 2
serves_plan: 653
serves_item: 3
---

# Plan — #656: Phoenix memory's own home, and the subset a project pulls

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own step.

## What we are trying to reach

ADR 035 §2 gives Phoenix memory one home: its own git repository, outside
Garura's code. A project no longer holds a copy of all memory. It pulls the
subset it needs into its own Garura memory and records what it pulled and from
which version. Today memory sits in three places that drift apart:
`core/components/memory/` (151 files, the source), `~/.garura/core/memory/`
(241 files: the source plus shelves deleted in #434 — `knowledge/arch/`,
`knowledge/quality/`, `standards/rules/feature-expectation-generation.md` —
and 12 files that differ) and the project copy `.garura/core/memory/` (41 files,
gitignored, partly stale). The memory tool (#657) needs one known place per
tier.

## When this plan is done

- The Phoenix memory repository exists and holds the seeded content, at a
  version (its commit).
- An install into a test project pulls only the starting set into Garura
  memory and writes the list of what it pulled, with versions.
- A piece pulled later arrives on request; a check shows which pulled pieces
  are behind Phoenix memory.
- Neither stale copy (`~/.garura/core/memory/`, the old project copy) is
  written or read any more.
- A project with nothing extra pulled still runs its plays (ADR 035 §3).
- The memory keys in `.garura/core/config.yaml` (`components.memory`,
  `ltm.source`, `ltm.project-target`, `ltm.global-target`,
  `review-pr.standards_order`) point at Phoenix memory and Garura memory, here
  and in every project the installer writes.

## Where we are now

The change is open on `feature/656-phoenix-memory-repository`. Kapil answered
the three questions. Next: item 2, create and seed Phoenix memory.

## The plan, in order

### Done

- **1. Decided: where Phoenix memory and Garura memory live** — #656. Kapil,
  2026-10-18 ("1A 2A 3 …"): (a) Phoenix memory is a **private** repository,
  `intent-driven-ai/phoenix-memory`. (b) Garura memory is the project's
  `.garura/` folder, without `.garura/project/issues/` (that is short-term
  memory); the pieces pulled from Phoenix memory go to `.garura/core/memory/`,
  now tracked in git, with the list of what was pulled; the product model stays
  in `.garura/product/`. (c) `core/components/memory/` **stays in Garura's
  repository**. It is not moved. Phoenix memory is seeded from it as a copy, and
  later changes reach Phoenix memory by promotion — short-term memory to Garura
  memory to Phoenix memory — never by moving anything out.

### 2. Create Phoenix memory and seed it — now

**Issue:** #656.
**What:** create the repository (per 1a), seed it from
`core/components/memory/` — the shelves deleted in #434 stay out, because they
exist only in the stale machine copy — with a short README that names it
Phoenix memory and says it is the superset, fed by promotion. Clone it onto the
machine at one known place (`~/.garura/phoenix-memory/`), which replaces
`~/.garura/core/memory/`.
**Why here:** the pull in item 3 needs a source with versions.
**Done when:** the repository holds the seeded content; a check shows Phoenix
memory holds every file of `core/components/memory/` unchanged (the superset
check), and lists any Garura piece not promoted yet.
**Needs:** item 1.

### 3. Garura memory in a project, and the pull

**Issue:** #656.
**What:** the Garura memory folder (per 1b: `.garura/core/memory/`, no longer
gitignored) and its pulled list: each piece
pulled, the Phoenix version it came from, and a fingerprint. The starting set
is Garura's rulebook (`standards/`: rules, templates, schemas) and the memory
guide (its text is #660), plus anything a play still reads by path until items
8 to 10 move it onto the tool (today the review guides, `knowledge/review/`).
Pulling one more piece on request, and a check that lists pulled pieces behind
Phoenix memory. One implementation, in the memory tool's folder, that the tool
(#657) reuses for its `pull` and `pulled` commands.
**Why here:** the installer (item 4) calls it.
**Done when:** a pull into an empty test folder writes the starting set and
the list; a second pull adds one piece; after a change in Phoenix memory the
check names that piece as behind.
**Needs:** item 2.

### 4. The installer pulls instead of copying

**Issue:** #656.
**What:** `core/components/plays/install-garura/scripts/install.py` stops
copying all memory to `~/.garura/core/memory/`. It clones or updates Phoenix
memory on the machine, pulls the starting set into the project's Garura memory,
and writes correct memory keys into the project's config (today it leaves
`ltm.project-target` pointing at nothing). The uninstall play removes what the
install wrote. Garura's own `.garura/core/config.yaml` keys move the same way.
**Why here:** this is where the two stale copies come from.
**Done when:** an install into a test project leaves no `~/.garura/core/memory/`
write and no full copy; the project's config keys point at Phoenix memory and
Garura memory; `review-pr.standards_order` reads the same order as the memory
tool.
**Needs:** item 3.

### 5. Prove it on a test project

**Issue:** #656.
**What:** install into a fresh test project and run a play that reads memory by
path (a play's close reads its templates), with nothing pulled beyond the
starting set. Pull one more piece by hand; change it in a Phoenix test copy and
run the behind check. Search for any writer or reader of the two stale copies.
**Why here:** the done-when of the story, shown on a real install.
**Done when:** all of the above pass, and the search finds no reader or writer
of the stale copies outside the uninstall clean-up.
**Needs:** item 4.

### 6. Land the change

**Issue:** #656.
**What:** commit, raise, review and merge; close #656; mark item 3 of the #653
plan done; fix any story text these answers change (#657, #660, #663).
**Done when:** merged to main.
**Needs:** item 5.

## Log

- 2026-10-18 — Created at the start of #656 from the issue, ADR 035 §2, ADR 036,
  ADR 017 and a look at the three memory copies and the installer.
- 2026-10-18 — Kapil answered: "1A 2A 3 Why would it leave Garura's repo? It
  would not. It would stay there. That is the whole point. It can be promoted
  to Phoenix memory, but then Phoenix memory, as I said, is a superset of the
  Garura memory. There is a learning stage from short-term to Garura memory to
  Phoenix memory, but it never leaves it." Item 1 done. The third question
  rested on a wrong reading: ADR 035 says `core/components/memory/` seeds
  Phoenix memory, not that it moves out.
