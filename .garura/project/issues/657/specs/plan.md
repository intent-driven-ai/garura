---
plan_for: 657
kind: story
serves: "#657 — the memory tool finds memory across short-term, Garura and Phoenix memory the way Claude Code searches"
status: active
updated: 2026-10-18
now: 1
serves_plan: 653
serves_item: 4
---

# Plan — #657: the memory tool's search, read and pull

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own step.

## What we are trying to reach

One command-line tool that agents call to find memory (ADR 035 §4). It looks in
the current issue's short-term memory, then Garura memory (the project's
`.garura/`), then Phoenix memory, and stops at the first tier that answers
(ADR 035 §3, ADR 036 §1). It searches the way Claude Code does: find files,
search their text, read exact lines. A piece it finds only in Phoenix memory is
brought into Garura memory, so the next lookup answers from the project. Every
result names its tier, file, lines and fingerprint. Today the tool has its
contract (#655, `core/tools/memory/contract/v1.json`) and `pull` / `pulled`
(#656, `core/tools/memory/pull.py`); the search and read side is not built.

## When this plan is done

- `find`, `search`, `read` and `health` work across the three tiers, in order,
  as the contract says, and `pull` / `pulled` are commands of the same tool.
- Kapil's test passes on a fresh test project with a copy of Phoenix memory
  (Kapil, 2026-10-18):
  - a simulated login story finds nothing in short-term or Garura memory, finds
    it in Phoenix memory, and the piece is pulled into the project;
  - a re-run reads it all from Garura memory;
  - a change-password story gets part from Garura memory and the rest from
    Phoenix memory;
  - with the project memory removed, the tool goes to Phoenix memory, or gives
    the empty answer that is the cue for a memory update a person approves.
- The issue's own done-when holds: tests pass on sample memory in all three
  tiers; a missing tier is an error, not an empty answer; a lookup never reads
  another issue's short-term memory and refuses `../` paths (`bad_request`);
  a lookup of Garura or Phoenix memory works without an issue (a contract
  change, with its version); nothing in the tool's folder names Garura;
  pointing it at Griffin later means changing one setting.
- It works the same from Claude Code and Codex (a plain command, JSON in and
  out).

## Where we are now

The change is open on `feature/657-memory-tool-search`. Its first commit closed
out five finished plans. Next: item 1, two questions for Kapil.

## The plan, in order

### Done

- **0. Opened** — #657. Branch `feature/657-memory-tool-search` off main
  (`7a61f424`); five finished plans closed out (#617, #632, #654, #655, #656)
  as Kapil chose on 2026-10-18.

### 1. Decide two open questions — now

**Issue:** #657.
**What:** (a) Memory updates: the issue says the tool writes approved updates,
but the approval flow is #658, and Kapil's removed-memory case ends in "raise a
memory update". Do `propose` and `apply` belong here or in #658? (b) When does a
Phoenix answer get pulled into Garura memory: on every hit, or only when a file
is read?
**Why here:** both change what items 2 to 5 build.
**Done when:** Kapil answers both.
**Needs:** nothing.

### 2. The lookups: health, find, search, read

**Issue:** #657.
**What:** one tool entry for every command, reading each tier's place from one
settings source; the tier order, the issue's own short-term folder only, the
refusals and errors, and fingerprints, all as the contract says. `pull` and
`pulled` from #656 become commands of the same entry.
**Why here:** everything else calls these.
**Done when:** the contract's samples pass through the tool, and tests cover
each tier, going up a tier, a missing tier, and a refused path.
**Needs:** item 1.

### 3. Bring a Phoenix answer into the project

**Issue:** #657.
**What:** when a lookup is answered by Phoenix memory, the piece is pulled into
Garura memory (as item 1b decides) and recorded in the pulled list.
**Why here:** Kapil's test needs the re-run to answer from Garura memory.
**Done when:** a test shows the first lookup answered by Phoenix memory and the
second by Garura memory.
**Needs:** item 2.

### 4. The contract change

**Issue:** #657.
**What:** a lookup of Garura or Phoenix memory works without an issue (PR #666
review, TIC-3); the `../` refusal is written down (TIC-7); the contract gets a
new version, and its samples and check follow.
**Why here:** after the tool exists, the change is tested against it.
**Done when:** the contract check passes on the new version.
**Needs:** item 2.

### 5. Kapil's test on a fresh project

**Issue:** #657.
**What:** an empty test project and a copy of Phoenix memory (its
`knowledge/domains/user-management.md` covers sign-in and passwords); run the
login story, the re-run, the change-password story and the removed-memory case,
and keep the record in this issue's short-term memory.
**Why here:** it is the done-when of the story, shown end to end.
**Done when:** all four cases behave as written above.
**Needs:** items 3 and 4.

### 6. Land the change

**Issue:** #657.
**What:** in the last commit before the merge, mark this plan done and item 4 of
the #653 plan done; then commit, raise, review and merge. Story texts these
answers change (#657, #658) are fixed only when Kapil asks.
**Done when:** merged to main.
**Needs:** item 5.

## Log

- 2026-10-18 — Created at the start of #657 from the issue, the contract
  (`core/tools/memory/contract/v1.json`, its README), ADR 035 §3–§4, ADR 036
  §1–§3, the #653 plan item 4 and Kapil's test from the #656 plan (item 1d).
