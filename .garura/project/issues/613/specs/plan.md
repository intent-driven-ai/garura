---
plan_for: 613
kind: story
serves: "#613 — the Kickoff drive runs /intent, /vision and /understand from a working prototype to a detailed product model"
status: active
updated: 2026-10-18
now: 1
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

The change is open: branch `feature/613-the-kickoff-drive`, cut from main on
2026-10-18. Nothing is built. A read of the three plays found what stops them
running back to back today (item 3). The first step is item 1: record how the
plays decide inside a drive, because it changes an earlier decision.

## The plan, in order

### 1. Decide how a play answers its own questions inside a drive — now

**Issue:** #613.
**What:** record Kapil's rule of 2026-10-18: inside a drive, a play answers from
memory and from what the system gives it, and asks only when nothing there
supports an answer. Say what counts as memory (for example the product model,
the knowledge base, the prototype's sources, the drive's own answers, learned
checkpoint answers), and that every answer taken this way is recorded with where
it came from, so the review can show it.
**Why here:** it changes ADR 029 ("the drive stops and asks; it never picks an
answer for itself") and rule 4 of the drive contract. The runner's question
step and the play fixes in item 3 both depend on it.
**Done when:** the decision is an accepted ADR, made with `/adr`.
**Needs:** nothing.

### 2. Decide the runner's shape

**Issue:** #613.
**What:** settle what the drive is as a component and how it runs end to end:
how it is built and compiled, where its run and records live, how it asks its
questions first under item 1's rule, how the config picks the checker, what
evidence it writes, and how it ends until the review exists.
**Why here:** items 4 to 6 build what this item decides.
**Done when:** a short design note in this issue's `specs/` folder that Kapil
agrees with; anything that changes an earlier decision is an ADR.
**Needs:** item 1.

### 3. Make the three plays run back to back without a person

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
**Needs:** item 1; item 2 for the input names.

### 4. Teach the play compiler what a drive is

**Issue:** #613.
**What:** `/play-creator` builds plays that run their own steps. A drive runs
other plays in a fixed order. The compiler must be able to build one and its
lint must check one.
**Why here:** every play is built through the compiler (CLAUDE.md), so Kickoff
is too; and every later drive (#608–#611) will need the same.
**Done when:** the compiler can build a drive, and its lint passes and fails a
drive as it does a play.
**Needs:** item 2.

### 5. Build the checker

**Issue:** #613.
**What:** at the end of a drive, a different model, sub-agent or coding agent
checks the result, and the config picks which (ADR 029). It passes or rejects,
with reasons written to a file. A rejection halts the drive.
**Why here:** Kickoff's done check needs it, and no checker exists today.
**Done when:** the config names the checker, and a pass and a rejection both
work on a sample result.
**Needs:** item 2.

### 6. Build the Kickoff drive

**Issue:** #613.
**What:** write Kickoff's intent source (ICE) from #613's acceptance criteria and
compile it: questions first, `/intent` → `/vision` → `/understand` (once, for
all capabilities), the checker, the evidence.
**Why here:** it puts items 3 to 5 together.
**Done when:** Kickoff compiles, its lint passes, and its done check is baked in.
**Needs:** items 3, 4 and 5.

### 7. Prove Kickoff on a real prototype

**Issue:** #613.
**What:** run Kickoff end to end on a real working prototype, in a test project
(not Garura's own product model). Then show the three halts: no prototype, a
prototype that does not run, a checker rejection.
**Why here:** only a real run shows it works; and the review tool takes its
example pack from this run (#641).
**Done when:** the run and the three halts are recorded in this issue's folder,
and the run's output is kept as #641's example pack.
**Needs:** item 6. Kapil picks the prototype.

### 8. Land the runner

**Issue:** #613.
**What:** commit, raise, review and merge the change; post the handoff on #613;
mark step 1 of item 8 done in the #606 plan.
**Done when:** merged to main.
**Needs:** item 7.

## Log

- 2026-10-18 — Created from #613, ADR 029 to 033, the drive contract rule, and a
  read of `/intent`, `/vision` and `/understand` as they run inside a drive.
  Scope is the runner (Kapil's choice "A"). Item 1 added from Kapil's rule on
  how plays decide inside a drive. Item 3's fixes have no issue yet: filing
  them is Kapil's call.
- 2026-10-18 — Kapil approved the plan and chose A for item 3: the play fixes
  are done on this branch, in this change, even though #613 lists play changes
  as out of its scope.
