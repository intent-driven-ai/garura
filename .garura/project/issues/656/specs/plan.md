---
plan_for: 656
kind: story
serves: "#656 — Phoenix memory has its own repository, and each project pulls only the subset it needs into Garura memory"
status: active
updated: 2026-10-18
now: 5
serves_plan: 653
serves_item: 3
---

# Plan — #656: Phoenix memory built, ready for the memory tool

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own step.

## What we are trying to reach

ADR 035 §2 gives Phoenix memory one home: its own git repository, outside
Garura's code. Garura's memory (`core/components/memory/`, 147 files git
tracks) moves there. The memory tool (#657) is built next and proves it; only
then is the old folder removed and everything that pointed at it fixed.

Memory is read in one order (ADR 035 §3): short-term memory first, then Garura
memory (the project's `.garura/` folder), and only then Phoenix memory.

## When this plan is done

- The Phoenix memory repository holds everything that was in
  `core/components/memory/`, at a version (its commit).
- `pull` and `pulled` are built and tested, ready for the memory tool.
- Garura's config has no dead memory settings, and the PR review rules are read
  from `.garura/`.
- ADR 035 §2 says the installer pulls nothing.
- The rest has a home: the tool and its test in #657; removing
  `core/components/memory/` and fixing what pointed at it after the tool.
- `.garura/` is not touched beyond its config. Its clean-up is #670.

## Where we are now

Phoenix memory is built and checked. The dead config settings are gone, and the
PR review rules are read from `.garura/`. Kapil: build the tool first. Next:
land this change (item 5), then the tool (#657) on its own branch.

## The plan, in order

### Done

- **1. Decided: where memory lives** — #656. Kapil, 2026-10-18 ("1A 2A 3 …"):
  (a) Phoenix memory is a **private** repository,
  `intent-driven-ai/phoenix-memory`. (b) Garura memory is the project's
  `.garura/` folder, without `.garura/project/issues/` (that is short-term
  memory); the product model stays in `.garura/product/`. (c) Changed by item
  1c below: this plan first read Kapil's answer as "`core/components/memory/`
  stays in Garura". It does not stay. It moves into Phoenix memory and is then
  removed.
- **1b. Decided: the installer pulls nothing** — #656. Kapil, 2026-10-18:
  "installer doesnt need to pull starting set.. we will build a trinity of plays
  that will setup initial memory." And: "2 is not needed. it install with no
  memory." The installer needs no change: it copies memory only when
  `core/components/memory/` exists (`install.py`, step 3 of the install). Three
  plays, not filed yet, will set up a project's first memory. This changes ADR
  035 §2 ("At install, a project pulls a starting set"); the ADR is amended in
  item 5.
- **1c. Decided: the order, and what skills read** — #656. Kapil, 2026-10-18:
  "first we move the memory into phoenix memory ensuring it works. this folder
  is core/components. the .garura is working copy and shoudl not be touched …
  once this memory is moved to phoenic, we can remove it. we clean up adrs, and
  links and fix skills and agents." And: "35 skills using memory is wrong
  design. they should referring to stm only or calling sub-agents to load the
  context." And: "first source if stm, then garura mamory which is .garara and
  only then phoenix memory." The `.garura/` clean-up is recorded as #670
  (Business Intent, not approved to build).
- **1d. Decided: the tool first, and how to test it** — Kapil, 2026-10-18:
  "that skill shold point to .garura location. clean up deal setting. then
  build the tool first." The test that proves the tool, in his words: in an
  empty project, simulate a story such as login. "Nothing would be in STM. It
  would go to project memory. Nothing would be there. Then it is going to go to
  the Phoenix memory, which should have stuff … It should be able to pull the
  memory down into the project … Re-running that test should now read everything
  from Garura or project memory. Then, let's say you go from login to change
  password. Something should come from the Garura project memory, and the
  pending stuff should go to the Phoenix memory." This replaces the
  empty-memory install test this plan had as its item 3. It is the tool's test
  (#657).
- **2. Phoenix memory created and seeded: built and pushed** — #656. Before
  seeding, three commits took client and personal references out of memory
  (`cedfdef2`, `d65770f8`, `10f10c79`). The repository
  `intent-driven-ai/phoenix-memory` holds the seed at commit `3f3347b`, on
  GitHub and cloned at `~/.garura/phoenix-memory/`. Check, 2026-10-18: all 147
  files git tracks in `core/components/memory/` match Phoenix memory byte for
  byte; Phoenix memory adds only its README.
  Also built on this branch: `pull` and `pulled`
  (`core/tools/memory/pull.py`, 12 tests pass). `pull` copies a piece from
  Phoenix memory into Garura memory and records it in `pulled.json`; `pulled
  --behind` names pieces that changed in Phoenix memory since. The memory tool
  (#657) uses it.
- **3. Dead config settings removed: built (not merged)** — #656. Nothing in
  Garura read `components.memory`, `ltm.source` or `ltm.global-target`; all
  three are gone from `.garura/core/config.yaml`, and the installer no longer
  rewrites a `memory:` line into projects' config. The config still loads and
  the installer's config rewrite still runs.

- **4. The PR review rules are read from `.garura/`: built (not merged)** —
  #656. `standards.pr-severity-taxonomy` (read by the `quality-check-scoped`
  skill) now points at `.garura/core/memory/standards/rules/pr.md`. Nothing was
  copied or pulled by hand. Kapil, 2026-10-18: "Skill should always point to
  .Garura core memory … If nothing exists because it hasn't been pulled, it will
  actually fail, and that is the whole point. That pull has to go to the root
  and build it." And: "The file will get into garura when the pull tool
  executes." Known for now: the copy there is old (30 May), without the July
  fixes from #454, and git ignores the folder; #670 and the tool's test settle
  it.

- **4b. Review fixes (PR #671): built (not merged)** — #656. The first review
  of PR #671 (harness verdict: reject) found one P1 and 9 memory wording
  defects. The 9 are fixed in `core/components/memory/` and in Phoenix memory
  (commit `5fcd88e`, pushed): person fields in the ADR template and the ontology
  example name a made-up person ("Alex Example"); "the owner" is gone; the
  2026-09-08 rule is stated without a quote; the ux files say "accepted"; the
  ontology Log has a dated line; the knowledge template says provenance names
  a source, never a person or a client. The P1 is rule DATA-18 on
  `core/tools/memory/test_pull.py` — the fake git address `t@example.com` in a
  temp repository. Kapil, 2026-10-18: "approve. capture these are demos emails,
  and part of tool that is using this as sample data. this is exception that
  is approved". A comment at the line records the exception.

### 5. Land the change — now

**Issue:** #656.
**What:** commit, raise, review and merge; close #656; mark item 3 of the #653
plan done; amend ADR 035 §2 through `/adr` (the installer pulls nothing; the
set-up plays fill a project's first memory). Story texts that these answers
change (#656, #657, #661, #663) are fixed only when Kapil asks.
**Done when:** merged to main.
**Needs:** item 4.

## After this story (test cases for the tool)

- Kapil, 2026-10-18: "If somebody removes the project memory, then it needs to
  raise an issue or go to Phoenix memory or put it in banks. Then an approval is
  needed." A case for the tool's test (#657). Not yet clear: what "put it in
  banks" means.

## After this story

- **The memory tool** (#657), on its own branch. Its done-when is Kapil's test
  in item 1d.
- **Remove `core/components/memory/`, and fix what pointed at it**, once the
  tool exists: ADRs and docs point at Phoenix memory; 35 skills read only
  short-term memory or call an agent for context; 7 agents load context through
  the tool (short-term memory, then `.garura/`, then Phoenix memory); 2 scripts
  (`commit-change/scripts/analyze_changeset.py`,
  `kb-search/scripts/kb_search.py`). The #653 plan already moves agents and
  skills onto the tool in #661 and #663; the folder goes last, when nothing
  names it.

## Log

- 2026-10-18 — Created at the start of #656 from the issue, ADR 035 §2, ADR 036,
  ADR 017 and a look at the three memory copies and the installer.
- 2026-10-18 — Kapil answered: "1A 2A 3 Why would it leave Garura's repo? It
  would not. It would stay there. That is the whole point. It can be promoted
  to Phoenix memory, but then Phoenix memory, as I said, is a superset of the
  Garura memory. There is a learning stage from short-term to Garura memory to
  Phoenix memory, but it never leaves it." Item 1 done. This plan read "it" as
  `core/components/memory/`; item 1c corrects that.
- 2026-10-18 — Item 2 done: memory cleaned of client and personal references,
  Phoenix memory created, seeded and pushed; check passed. `pull` and `pulled`
  built, 12 tests pass.
- 2026-10-18 — Kapil: the installer pulls no starting set (item 1b).
- 2026-10-18 — Kapil set the order and the skill rule (item 1c). #670 filed
  for the `.garura/` clean-up.
- 2026-10-18 — Kapil: the PR rules skill reads from `.garura/`, dead settings
  go, the tool comes first, with his test (item 1d). Item 3 done. The
  empty-memory install test, the folder removal and the fixes moved after the
  tool.
- 2026-10-18 — Item 4 done: the PR rules setting points at `.garura/`; the
  file arrives when the pull tool runs (Kapil). Removed-memory case added for
  the tool's test.
- 2026-10-18 — PR #671 reviewed: reject on one P1 (DATA-18, a demo address in a
  test). Kapil approved it as an exception; 9 memory wording fixes made (item
  4b). Small issue found, not fixed: `test_pull.py` never deletes its temp
  folders.
