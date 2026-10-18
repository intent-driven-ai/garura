---
plan_for: 657
kind: story
serves: "#657 — the memory tool finds memory across short-term, Garura and Phoenix memory the way Claude Code searches"
status: done
updated: 2026-10-18
now: -
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

Done. The memory tool finds, searches, reads and pulls across the three tiers;
contract version 2; Kapil's test passed; PR #674 approved by Kapil and merged.
This plan is done. Next in the #653 plan: item 5, memory updates (#658).

## The plan, in order

### Done

- **0. Opened** — #657. Branch `feature/657-memory-tool-search` off main
  (`7a61f424`); five finished plans closed out (#617, #632, #654, #655, #656)
  as Kapil chose on 2026-10-18.
- **1. Decided: what the tool writes, and when it pulls** — Kapil, 2026-10-18.
  (a) "memory updates will be a different play. this will be a 3 set of plays - learn: this read STM and learns to proejct mem i.e. garura - promote: this reads project memory and send a version to phoenix-mem for approval. approval for this sits outside of garura. unless memory is approved (outside) the reader cant use that phoenix memory - so the memory updates land in STM only". So this tool writes no memory update to Garura or Phoenix memory:
  updates land in short-term memory (#658), a `learn` play moves them to Garura
  memory, and a `promote` play sends a version to Phoenix memory for an
  approval that sits outside Garura. Those plays are not filed yet. The reader
  uses only approved Phoenix memory: here, what is on the Phoenix memory
  repository's `main` (a promotion arrives as a change a person merges outside
  Garura) — this plan's reading, for Kapil to correct. (b) "yes the file is
  pulled when needed.. .once the memory is used, then it saved in garura /
  proejct memory." A Phoenix answer is pulled when the file is read (used),
  not on every search hit.
- **2. Built: the lookups** — #657. `core/tools/memory/memory.py` is the one entry for
  `health`, `find`, `search`, `read`, `pull` and `pulled`. Settings come from one source (a
  settings file, else the environment); `engine` is the one setting a server engine will
  change. Short-term memory is the issue's folder only, and is not Garura memory when it
  sits inside it. Phoenix memory is read only at `phoenix_ref` (default `origin/main`):
  a branch or an edit on disk is not read. Searches use git grep (extended regular
  expressions, or plain text). A request the contract does not allow is refused before any
  memory is read. Every answer the tests get is put through the contract check, in place
  of replaying the samples (their versions and paths are made up). 29 tests; the 12 pull
  tests, the contract check (boundary included) and its tests pass; ruff is clean.
- **3. Built: memory that is used is saved** — #657. A read from Phoenix memory pulls the
  file into Garura memory (`garura_pull_dir`) and the pulled list; the next lookup answers
  from Garura memory. A search hit alone pulls nothing. `pull` no longer leaves an empty
  pulled list after a refusal (a #656 review note).
- **4. Built: contract version 2** — #657. `core/tools/memory/contract/v2.json`; version 1 is
  kept as it was. A lookup of Garura or Phoenix memory works without an issue: with no
  issue there is no short-term memory, so the lookup goes Garura then Phoenix, and asking for
  short-term memory without one is `bad_request` (TIC-3). A glob, like a path, never starts
  with a slash or holds `..`, so `../613/**` is refused (TIC-7). Written down too: Phoenix
  memory is read only at its approved version, and a file read from it is saved into Garura
  memory. 43 samples moved to version 2 and 2 added; the check, its tests (one test now
  states the version 2 rule), `pull.py` and the tool follow. 33 tool tests, 12 pull tests,
  49 contract tests pass; the contract check (22 samples, 23 broken, boundary) passes.
- **5. Shown: Kapil's test on a fresh project** — #657. A fresh project with empty Garura
  memory and a clone of Phoenix memory at its approved version. Login story: the lookup
  went short-term → Garura → Phoenix and was answered by Phoenix memory
  (`knowledge/domains/user-management.md`); reading it pulled it into the project. Re-run:
  answered by Garura memory. Change-password story: password reset answered by Garura
  memory, password strength by Phoenix memory (`standards/rules/kb-extension.md`), then
  pulled. Project memory removed: the lookup went up to Phoenix memory again; a lookup no
  tier can answer gave the empty answer, the cue for a memory update (#658). Record:
  `evidence/kapil-test.md`; runner: `evidence/kapil_test.py`.
- **6. Shipped: the memory tool** — #657, PR #674. Reviewed with the gate on for that
  run; the machine recommended reject on 17 P1s, all the word "password" in demo test
  data; Kapil approved on 18 October. Two real faults from that review are the first
  fixes of #658. This plan and item 4 of the #653 plan are closed in the last commit
  before the merge.

## After this story (found by the self-review, owned elsewhere)

- ADR 035 and ADR 036 still say every lookup names its issue and that a piece is
  pulled when it is found; they do not record that Phoenix memory is read only
  at its approved version, or that updates land in short-term memory and
  `learn` / `promote` plays move memory up. They need an amendment through
  `/adr`, with the ADR 035 §2 one already owed.
- The contract and the README still describe `apply` writing to Garura and
  Phoenix memory. That text changes with the update flow (#658).
- Nothing moves the approved version forward: the tool never fetches Phoenix
  memory, and no project settings file is written yet. Both belong to the
  install (#660).
- Kapil's no-client-names rule, read by the pre-merge reviews from project
  memory: #672. The merge play's plan check: #673.

## Log

- 2026-10-18 — Created at the start of #657 from the issue, the contract
  (`core/tools/memory/contract/v1.json`, its README), ADR 035 §3–§4, ADR 036
  §1–§3, the #653 plan item 4 and Kapil's test from the #656 plan (item 1d).
- 2026-10-18 — Item 1 done: memory updates land in short-term memory only; `learn` and `promote` plays move them up; the reader uses only approved Phoenix memory; a file is pulled when it is used.
- 2026-10-18 — Items 2 and 3 built: `memory.py`, 29 tests; `pull` reads Phoenix memory at its approved version.
- 2026-10-18 — Item 4 built: contract version 2.
- 2026-10-18 — Item 5 shown: Kapil's test passed on a fresh project.
- 2026-10-18 — Kapil asked who calls the tool: no agent yet. He kept the plan order (agents move in #661 after #658–#660) and said land it.
- 2026-10-18 — Self-review (0 blocking, 12 notes): fixed the command line so every failure answers in JSON, old version-1 wording, tests that left temp folders, and the test record; the rest is placed above.
- 2026-10-18 — Item 6 done: PR #674 approved by Kapil; plan closed before the merge.
