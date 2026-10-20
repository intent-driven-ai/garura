---
plan_for: 613
kind: story
serves: "#613 — the Kickoff drive runs /intent, /vision and /understand from a working prototype to a detailed product model"
status: active
updated: 2026-10-20
now: 3
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

- **Review as plays, run as a drive** (Kapil, 2026-10-20, thinking aloud): review split into
  plays — code quality (linters, tests), security, design (UX and technical) — run together as a
  review drive, adopting Claude Code's review method (parallel reviewers, a verification step that
  filters false positives, severity ranking, a `REVIEW.md` of the repo's own review rules). ADR 029
  §5 already expects the review to be a drive of its own. A business intent of its own; filed when
  Kapil asks. Kickoff's checker (item 6) can later name that drive in its config.

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
from main (`504379ce`). Now: item 3, the runner's design note — Kapil decided its three points (2026-10-20).

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

### Milestone: Kickoff's plays work from memory — passed (20 October)

Nothing below starts until the memory system's own milestone is passed: its
items 1 to 9 — the decision, the memory tool, Phoenix memory and the subset a
project pulls, memory updates, every decision naming its memory, the memory
system in every Garura install, and
`/intent`, `/vision` and `/understand` moved onto the tool and tried on a test
project. That work is its own feature, outside this issue
(Feature #653, `.garura/project/issues/653/specs/plan.md`).

### 3. Decide the runner's shape — now

**Issue:** #613.
**What:** settle what the drive is as a component and how it runs end to end:
how it is built and compiled, where its run and records live, how it asks its
questions first under ADR 034, how the config picks the checker, what evidence
it writes, and how it ends until the review exists.
**Why here:** items 5 to 7 build what this item decides.
**Done when:** a short design note in this issue's `specs/` folder that Kapil
agrees with; anything that changes an earlier decision is an ADR.
**Needs:** items 1 and 2, and the milestone above.

### 4. Make the three plays run back to back without a person

**Settled since (#661, #662):** `/intent` checks the drive contract with the shared checker
(I-1); every run, its answers and evidence live under the drive's issue (ADR 039); the plays
read memory only through their agents. Still open from the #662 run: the plays leave the
issue's run files uncommitted inside a drive (V-4 — the drive commits them), and the close does
not ask `template-manager` for its templates (I-2). Re-check the rest of this list in item 3.

**Issue:** #613 — the fixes ride on this branch (Kapil's choice A, 2026-10-18).
**What:** fix what stops the plays running one after another. Found so far:
`/intent`'s commit leaves new domain pages and capability docs uncommitted, so
`/vision` stops on an unclean model; `/intent` asks its questions one by one
instead of answering from memory first; `/vision`'s proposal for a new domain
can stop for a review; the names `/vision` reads its input under are not fixed;
`/intent` checks the drive contract its own way. Each change to a play goes
through its ICE source and `/play-editor`.
**Why here:** the runner cannot be proven end to end while any of these stop it.
**Done when:** each fix is on this branch and each play's own checks pass.
**Needs:** items 1 and 2; item 3 for the input names.

### 5. Teach the play compiler what a drive is

**Issue:** #613.
**What:** `/play-creator` builds plays that run their own steps. A drive runs
other plays in a fixed order. The compiler must be able to build one and its
lint must check one.
**Why here:** every play is built through the compiler (CLAUDE.md), so Kickoff
is too; and every later drive (#608–#611) will need the same.
**Done when:** the compiler can build a drive, and its lint passes and fails a
drive as it does a play.
**Needs:** item 3.

### 6. Build the checker

**Issue:** #613.
**What:** at the end of a drive, a different model, sub-agent or coding agent
checks the result, and the config picks which (ADR 029). It passes or rejects,
with reasons written to a file. A rejection halts the drive.
**Why here:** Kickoff's done check needs it, and no checker exists today.
**Done when:** the config names the checker, and a pass and a rejection both
work on a sample result.
**Needs:** item 3.

### 7. Build the Kickoff drive

**Issue:** #613.
**What:** write Kickoff's intent source (ICE) from #613's acceptance criteria and
compile it: questions first, `/intent` → `/vision` → `/understand` (once, for
all capabilities), the checker, the evidence.
**Why here:** it puts items 4 to 6 together.
**Done when:** Kickoff compiles, its lint passes, and its done check is baked in.
**Needs:** items 4, 5 and 6.

### 8. Prove Kickoff on a real prototype

**Issue:** #613.
**What:** run Kickoff end to end on a real working prototype, in a test project
(not Garura's own product model). Then show the three halts: no prototype, a
prototype that does not run, a checker rejection.
**Why here:** only a real run shows it works; and the review tool takes its
example pack from this run (#641).
**Done when:** the run and the three halts are recorded in this issue's folder,
and the run's output is kept as #641's example pack.
**Needs:** item 7. Kapil picks the prototype.

### 9. Land the runner

**Issue:** #613.
**What:** commit, raise, review and merge the change; post the handoff on #613;
mark step 1 of item 8 done in the #606 plan.
**Done when:** merged to main.
**Needs:** item 8.

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
