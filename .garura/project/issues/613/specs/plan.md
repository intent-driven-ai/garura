---
plan_for: 613
kind: story
serves: "#613 — the Kickoff drive runs /intent, /vision and /understand from a working prototype to a detailed product model"
status: active
updated: 2026-10-20
now: 8
serves_plan: 606
serves_item: 8
---

# Plan — #613: the Kickoff drive

This is a plan, not a design. It says what gets done, in what order, and why
that order. How each item is built is decided in its own issue.

## What we are trying to reach

Today a person runs `/intent`, then `/vision`, then `/understand` by hand, and
each one stops to ask and to be approved. Each of the three can already run
inside a drive (#612, #614, #615), but nothing runs them as one.

Kickoff is that one run. A person gives it a working prototype. Kickoff pulls
the intent out of it and ends with a detailed product model: business intents
(proposed), a domain with its capabilities, and every capability detailed. It
works on one issue and one branch, asks its questions first, does not stop for
the plays' approvals, has a different model or agent check the result, and
writes an evidence record (ADR 029).

This plan builds the **runner** — the drive without its end review. Kapil chose
this order on 2026-10-18 ("A": the runner first, then the review). Until the
review exists (#641–#650), the drive ends with the plays' review records and a
pull request.

**How the plays decide inside the drive** (Kapil, 2026-10-18): the three plays
run with a high level of autonomy. They decide from what memory and the system
give them, and may assume from it. They do not stop at every point to ask. They
never make something up from nothing: *"If you do not give any direction from
the user or the memory, going to the underlying LLM and making a decision is
the wrong move."* When memory and the system hold nothing to go on, they ask.

## When this plan is done

- Given a working prototype, Kickoff runs `/intent` → `/vision` → `/understand`
  on one branch, with no stop except a question nothing in memory can answer.
- It ends with proposed business intents, a domain with its capabilities, every
  capability detailed, each play's saved record (one `/understand` record per
  capability), a passed check by a checker chosen in the config, and evidence.
- It halts when the prototype is missing or does not run, when a play misses its
  own done check, or when the checker rejects the result.
- The runner is merged, and one real run is kept as the example pack the review
  tool needs (#641).

## What this plan leaves out

- **A status plugin for Claude Code** (Kapil, 2026-10-20, "1"): a long drive shows what it is
  doing about once a minute — "Kickoff · round 1 · /understand · 35 min". Decoupled: the drive
  only writes its status file (`standards/rules/run-status.md`, built in #613); a separate
  plugin, installed only when the install chooses Claude Code, reads it and shows the line
  (Claude Code's status line with `refreshInterval`; whether the timer fires while a long play
  runs is still to be proved). Its own business intent; filed when Kapil asks.

- **Review as plays, run as a drive** (Kapil, 2026-10-20, thinking aloud): review split into
  plays — code quality (linters, tests), security, design (UX and technical) — run together as a
  review drive. Kapil (2026-10-20): no separate `REVIEW.md` — our design is plays; the review
  plays adopt the guidelines and best practices of Claude Code's review (parallel reviewers, a
  verification step that filters false positives, dedupe, severity meanings, a cap on nits,
  excluded paths, evidence for each finding). Kapil (2026-10-20): **one review, after the pull
  request** — the self-review before it goes; its checks move into the review plays, and its
  hard checks (no secrets, a clean tree, the issue named) become machine checks before the pull
  request opens. ADR 029 §5 already expects the review to be
  a drive of its own. A business intent of its own; filed when Kapil asks. Kickoff's checker
  (item 6) can later name that drive in its config.

- **Confirmed intents and the review as the drive's last step.** Inside a drive,
  `/intent` saves intents as proposed; the person confirms them in the review.
  That comes with the review stories (#641–#650), and #650 makes it the drive's
  last step.
- **The person's plan and its issues.** ADR 029 says Kickoff also gives the
  person a plan and issues that break the intent into small pieces. None of the
  three plays makes them, and #613 does not ask for them. Waiting on Kapil.
- **One plan for the whole drive** (#626). It needs the plays to write plans
  first (#623).

## Where we are now

The memory milestone is passed (#653 items 1 to 9; the last, #662, merged on 20 October): the
three plays read memory only through their agents, every run lives under its issue, and they
ran from memory alone on a test project. A fresh branch `feature/613-the-kickoff-drive` is cut
from main (`504379ce`). Items 3 to 7 are done. The real runs (Argus mockup, Kapil's pick) found that Kickoff ran as a pipeline, not a drive. Now: item 8, make it loop and make `/intent` fast and right; then item 9, the proof.

## The plan, in order

### Done

- **1. Decided: inside a drive, a play answers from memory** — ADR 034,
  accepted by Kapil on 18 October (`docs/adr/034-plays-answer-from-memory-inside-a-drive.md`).
  A play answers its questions from memory and what the system gives it,
  records where each answer came from, and asks only when nothing supports an
  answer; never from the model alone. It amends ADR 029 §2. Nothing is built.
  Still open: whether a play may answer from a piece not yet approved, and
  where each answer's source is recorded (items 2 and 3).
- **2. Reviewed: the memory the plays answer from** — `specs/memory-review.md`.
  Memory is not ready: three copies of long-term memory that disagree, two kinds
  of memory that cannot answer a question, and nothing that records where an
  answer came from. Kapil chose B: fix the whole memory system first, as its own
  feature with its own issues and branches, and set its model (Phoenix memory as
  the superset; each project pulls the subset it needs; one tool that finds and
  updates memory, searching like Claude Code). Nothing is fixed yet.
- **3. Decided the runner's shape** (20 October) — `specs/runner-design.md`, agreed by Kapil:
  each play runs as a sub-agent (a headless session is a config option); the drive ends at the
  pull request with typed confirmation until the review tool exists, recorded in Kickoff's ICE
  (item 7); the checker is config, both kinds built.
- **4. Made the three plays run back to back without a person** (20 October) — re-checked after
  #661 and #662: the old stops (uncommitted pages after `/intent`, questions one by one,
  `/vision`'s review stop, `/vision`'s input names, `/intent`'s own contract check) no longer stop
  the plays; the #662 run went through all three under one contract. Fixed here: I-2 — the shared
  close's template step is no longer optional, its manifest is named for the play, and a play
  inside a drive closes as a sub-play (the drive writes the one report — drive contract, step 7).
  Moved to item 7: V-4 (the drive commits the issue's run files after each play) and the drive's
  evidence (the config turns evidence off by default, so Kickoff's config must record it).
- **5. Built drives with `/drive-creator` and `/drive-editor`** (20 October; Kapil: their own
  builder and editor, and their own folder, `core/components/drives/`) — one shared drive run
  (`core/components/drives/_shared/drive-run.md`) with its scripts; `lint_drive.py`; the install
  lays drives beside the plays; `lint-components` checks them. Proved by two fresh-agent trials
  in a scratch copy; their findings fixed (`specs/drive-compiler-design.md`, section 5). Left for
  item 7: `/understand` reads no capability list from its contract.
- **6. Built the checker** (20 October) — the `judge-drive-result` skill holds its rules and
  verdict shape; `prepare_check.py` hands it the drive's outputs only (the change, review
  records, answers and their sources, the trace check, the done checks) and the drive's own
  criteria; a sub-agent on a named other model or Codex (read-only) judges; `record_check.py`
  writes `check.yaml` (pass goes on, reject halts, a malformed verdict is never a pass). Proved on
  the #662 run: Sonnet and Codex each passed the full run and rejected it cut short after
  `/vision` (`evidence/checker/`).
- **7. Built the Kickoff drive** (20 October) — `core/components/drives/kickoff/`, built with
  `/drive-creator` from its ICE (Kapil: "the ice looks okay"): the prototype checked before
  anything opens, `/intent` → `/vision` → `/understand`, the checker (default a sub-agent on
  Sonnet), evidence always on, and the stand-in end — the person types confirm or drop per
  intent, recorded in the issue's short-term memory, the model left `proposed` until Argus writes
  the approval (Kapil chose "2"). `lint_drive.py` passes; the full install lays it.

### Milestone: Kickoff's plays work from memory — passed (20 October)

Nothing below starts until the memory system's own milestone is passed: its
items 1 to 9 — the decision, the memory tool, Phoenix memory and the subset a
project pulls, memory updates, every decision naming its memory, the memory
system in every Garura install, and
`/intent`, `/vision` and `/understand` moved onto the tool and tried on a test
project. That work is its own feature, outside this issue
(Feature #653, `.garura/project/issues/653/specs/plan.md`).

### 8. Make Kickoff a real drive, and `/intent` fast and right — now

**Issue:** #613.
**What:** found by the runs on the Argus mockup (`evidence/kickoff-run/findings.md`). Kapil,
2026-10-20: ADR 029 and ADR 035 stand; the drive's scope was read wrong — a question one play
cannot answer belongs to the whole drive. (1) The drive loops: intent → vision → understand →
back again with what it learned, until its done check holds or a round adds nothing new; only
then does it ask the person what is still open, all at once, with the draft. (2) `/intent`
inside a drive saves proposed intents with open questions named instead of stopping, and fills
them on the next round. (3) Context from memory, then research as a memory update (ADR 035).
(4) "Who asks" from the journeys' roles. (5) Questions that make sense to whoever gave the
prototype. (6) The walk fast and cheap: one browser per journey, only what changed per step,
its own agent on Sonnet 5.5; the draft on Opus 5.5. (7) Every main section of a prototype is
some journey's goal (the product model half of Argus was lost).
**Why here:** the proof (item 9) must be a correct run.
**Done when:** each fix is on this branch with its tests and linters, and a rerun shows the
loop.
**Needs:** item 7.

### 9. Prove Kickoff on a real prototype

**Issue:** #613.
**What:** run Kickoff end to end on a real working prototype, in a test project
(not Garura's own product model). Then show the three halts: no prototype, a
prototype that does not run, a checker rejection.
**Why here:** only a real run shows it works; and the review tool takes its
example pack from this run (#641).
**Done when:** the run and the three halts are recorded in this issue's folder,
and the run's output is kept as #641's example pack.
**Needs:** item 7. Kapil picks the prototype.

### 10. Land the runner

**Issue:** #613.
**What:** commit, raise, review and merge the change; post the handoff on #613;
mark step 1 of item 8 done in the #606 plan.
**Done when:** merged to main.
**Needs:** item 9.

## Log

- 2026-10-18 — Created from #613, ADR 029 to 033, the drive contract rule, and a
  read of `/intent`, `/vision` and `/understand` as they run inside a drive.
  Scope is the runner (Kapil's choice "A"). Item 1 added from Kapil's rule on
  how plays decide inside a drive. Item 3's fixes have no issue yet: filing
  them is Kapil's call.
- 2026-10-18 — Kapil approved the plan and chose A for item 3: the play fixes
  are done on this branch, in this change, even though #613 lists play changes
  as out of its scope.
- 2026-10-18 — Item 1 done: ADR 034 accepted ("approved"). Kapil added a review
  of the memory the plays answer from before anything is built on it; it is the
  new item 2, and the items after it moved down one (the runner's shape is now
  item 3, the play fixes item 4, the compiler 5, the checker 6, Kickoff 7, the
  real run 8, landing 9). ADR 034's "#613 plan item 2" now means item 3, and its
  "item 3" now means item 4.
- 2026-10-18 — Item 2 done: the memory review is written. Kapil chose B — fix
  the whole memory system before the drive — as its own feature with its own
  issues and branches (Feature #653), and set its
  model: Phoenix memory is the superset; Garura memory in a project is the
  subset it pulls; one tool finds and updates memory. A milestone now holds
  item 3 until that feature passes its own milestone. Item 4's play fixes
  overlap with the memory feature's item 7; what is left of item 4 after it is
  settled at item 3.
- 2026-10-18 — Kapil chose A: land what this branch holds now (ADR 034, the
  plans, the memory review) as one pull request, so the memory feature can
  start from main. #613 stays open; Kickoff gets a fresh branch when the memory
  milestone is passed. Kapil also made the memory system part of every Garura
  install (memory plan item 7).
- 2026-10-18 — The memory system is filed as Feature #653 (spike #654 for its decision); its plan moved to `.garura/project/issues/653/specs/plan.md`.
- 2026-10-20 — The memory milestone is passed (#662 merged). Fresh branch `feature/613-the-kickoff-drive` off main (`504379ce`); the old one landed as PR #652. Now item 3.
- 2026-10-20 — Item 3: Kapil decided (a) each play runs as a sub-agent (docs allow three layers; a headless session stays a config option), (b) 1 — the drive ends at the PR with typed confirmation, a stand-in recorded in Kickoff's ICE until the review tool, (c) the checker is config, both kinds built. Review-as-a-drive recorded for later.
- 2026-10-20 — Kapil: no separate `REVIEW.md`; the review plays adopt its practices (recorded under what this plan leaves out).
- 2026-10-20 — Items 3 and 4 done. I-2 fixed in the shared close and the drive contract; V-4 and the drive's evidence moved to item 7.
- 2026-10-20 — Kapil: one review, after the pull request; the self-review goes (recorded under what this plan leaves out).
- 2026-10-20 — Item 5 changed (Kapil): drives get their own builder and editor, `/drive-creator` and `/drive-editor`, not a drive kind inside `/play-creator`. Design note written; one question open (where drives live).
- 2026-10-20 — Item 5 done: `/drive-creator`, `/drive-editor`, the shared drive run and `lint_drive.py`; drives live in `core/components/drives/` (Kapil: "1").
- 2026-10-20 — Item 6 done: the checker, both kinds, proved with a pass and a reject each (`evidence/checker/README.md`).
- 2026-10-20 — Item 7: Kapil chose 2 — at Kickoff's end the person's typed confirm or drop is recorded in the issue's short-term memory; intents stay proposed until the review tool writes approval. Kapil: the review tool's Catch up swipe handles ICE differently from business intents (open; recorded in #617's tool plan).
- 2026-10-20 — Item 7 done: Kickoff built and linted (`core/components/drives/kickoff/`).
- 2026-10-20 — Kapil: stop the run; the drive must loop over its three plays and stop only when none can answer; fix `/intent`'s speed and questions; then run again. New item 8; the proof is item 9, landing item 10.
- 2026-10-20 — Kapil: a drive presents its status in a file, and a separate Claude Code plugin shows it ("these two have to be decoupled"); the drive's side is built in item 8, the plugin is later work.
