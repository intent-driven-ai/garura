# Managing Work on Garura

How work on Garura itself gets described, tracked, picked up, handed back, and
closed. This is the convention for this repository's issue tracker. It is
loaded in every session so that no one — human or agent — has to ask, guess, or
invent one.

---

## First: two planes that must never be confused

This repository contains two different hierarchies. They look similar and mean
entirely different things. Confusing them is the mistake this document exists
to prevent.

**How we build Garura.** Three levels: a Feature at the top, with Stories and
Bugs beneath it. That is the whole model, and it governs this repository's
tracker. It is deliberately simple because developing Garura is not complex
enough to warrant more.

**What Garura offers.** The product model Garura gives *other* teams for
building *their* products: domain → capability → functionality → epic. This is
Garura's capability — something the framework provides to its users. It is not
Garura's own process, and it never describes work on this repository.

So: statements such as "an epic is the grain a GitHub issue is cut at" belong
entirely to the second plane. They describe products being built *with* Garura.
They say nothing about how issues are cut here. When you are filing or working
an issue on Garura, only the first plane applies — Feature, Story, Bug. There is
no domain, capability, functionality, or epic in this tracker.

---

## What am I filing?

| | What it is | Filed when |
|---|---|---|
| **Feature** | A capability of Garura that needs a decision before anyone builds. It states a problem, a boundary, and what "done" looks like — not an implementation. | Something new is wanted and the shape of it is still open. |
| **Story** | A shippable slice of a Feature. One coherent change that can be built, reviewed, and merged on its own. | The Feature's decision is settled and a slice of it is ready to build. |
| **Bug** | A defect in something already shipped: it behaves differently from what was intended. | Observed behaviour departs from expected behaviour. |

A Feature is never worked directly. It gets decomposed into Stories first. If
you find yourself writing code against a Feature issue, the decomposition step
was skipped — go back and do it.

A Bug is not "something is missing." Missing capability is a Feature or a
Story. A Bug requires something that already exists and does the wrong thing.

## Where does it hang?

Every Story and every Bug hangs under the Feature whose capability it belongs
to, as a real parent/child link in the tracker — not as a mention in the body,
not as a shared label. The link is what makes a Feature's progress readable at a
glance and what lets a working session pull its own context.

A Feature has no parent. Stories and Bugs always do. If a Story has no plausible
parent Feature, that usually means the Feature was never filed — file it.

## How does that land in the tracker?

- **Type lives in the type field.** Feature and Bug use their native issue
  types. There is no Story type in this repository, so a Story is filed as
  **Task** — Task is the Story slot. Never encode the type as a title prefix
  (`[Story]`, `Bug:`); the field is the only place it belongs.
- **Labels carry severity only.** Not type, not status, not area. Severity is
  what a label is for here.
- **Title states the outcome**, in the language a reader operates in — what
  changes and for whom — not the files being touched.

## Is it ready to work?

Before a Story or Bug is handed to a session, it has to stand on its own. The
session working it reads the issue and its parent, and nothing else.

**A Story is ready when it has** a parent Feature linked, acceptance criteria
(what must be true for this to be done), and a scope boundary (what this issue
deliberately does *not* touch).

**A Bug is ready when it has** a reproduction — the steps and the actual
behaviour — and a statement of the expected behaviour.

**A Feature is ready when** it states the problem, the boundary, and the "done
when." It is then decomposed; it is never worked directly.

An issue that fails these tests is not blocked on effort — it is blocked on
being written. Finish writing it before anyone picks it up.

## How does work get picked up?

Planning and decomposition happen in an **orchestrator session**: reading the
backlog, shaping Features, cutting Stories, ordering them. No implementation
happens there.

Each Story or Bug then goes to **its own session**. That session:

1. Reads the issue and its parent from the tracker itself — it is not briefed by
   hand, and a chat summary is never the source of truth.
2. Works on one branch for that one issue.
3. Closes the issue with its pull request.

One issue, one session, one branch, one pull request. A session that ends up
carrying two issues has lost the thread of both.

## How far does my work extend?

**The issue being worked defines the scope. Work never goes beyond it.**

Anything you discover along the way that falls outside the issue — a bug in
neighbouring code, a refactor that would be nice, a doc that is stale — becomes
its own issue. It does not get folded into the current change, and it does not
get fixed quietly "while you're in there." Note it, hand it back, move on —
who turns that note into an issue is settled below.

This is not fussiness. A change that stays inside its issue can be reviewed
against that issue. A change that wandered cannot be reviewed against anything.

## How is a session briefed?

A session is told only what the issue cannot carry: the scope boundary, and
where it stops.

Say the stop point explicitly. Opening a pull request and merging one are
different endings, and a session that is not told which one it owns will pick
for itself — which is how a session came to merge its own work to main.

**Nothing reaches a session once it is running.** There is no channel to it: no
correction, no missing context, no answer to a question it raised. It can be
interrupted or archived, and that is all. The brief therefore has to be
complete when the session starts. Do not plan on steering it later.

## Where does a session stop?

**Three moves end a session, in order: open the pull request, write the
handoff, stop.** Nothing comes after. Reading the change, judging it, and
landing it belong to someone else.

**It does not review its own work.** A session already believes its change is
right — believing that is what made it write the change — so its own verdict
reads like assurance while carrying none. What it owes a reviewer is
orientation, not a judgement.

**It does not merge.** Merging is a decision taken with a human looking at the
diff: not when the checks are green, not when the change is obviously correct,
not when nobody appears to be waiting. This is not new policy — when the
delivery gates were relaxed across the board, the merge step was deliberately
left pinned to its human beat.

## How is work handed back?

**Every session writes a handoff before it finishes — every session, every
time, including one that finished cleanly with nothing left over.** A clean run
that says nothing is indistinguishable from a run that died, and telling those
apart costs an investigation that almost always concludes it was fine.

The handoff is **a comment on the issue that was worked**, and that is the
whole mechanism. Nothing notifies anyone. The comment waits on the issue, where
whoever picks the work up will look — today, or in six months. A report
delivered any other way needs someone present to catch it.

It says:

- **What was done** — the outcome, in the language a reader operates in.
- **What was deliberately not done, and why.**
- **What was found that falls outside the issue** — as proposals. A session
  never files them itself. Whether a proposal becomes an issue, how it is cut,
  and where it hangs are scoping decisions, and a session that sees one issue
  cannot make them.
- **Where the work came to rest** — the branch, the pull request and its state,
  and what a reviewer should know before opening it.

Keep it short enough to read in one pass. A handoff nobody finishes reading has
not handed anything back.

---

## Working the tracker: notes that save an hour

These are mechanics an agent needs and will otherwise rediscover the hard way.
The mechanism is deliberately tool-agnostic — command line, API, whichever is
available. What matters is the convention and the traps.

**Linking a child to a parent needs the internal identifier, not the issue
number.** The sub-issue operation takes the child's internal database
identifier. Passing the human-visible issue number fails with
`403 Resource not accessible by integration`, which reads exactly like a
permissions problem and is not one. Do not conclude you lack access — you are
passing the wrong value. The identifier comes back on any issue create or
update, so capture it there rather than hunting for it later.

**There is no Story issue type in this repository.** Only Feature, Task, and
Bug exist. Story occupies the Task slot. Do not attempt to create a Story type.

**Applying a label that does not exist creates it.** There is no separate
create-then-apply step, and there is no error to catch. The flip side: a typo in
a label name silently produces a new label rather than failing, so read the
label back after applying it.

---

## Related

- `CLAUDE.md` — project instructions; points here so this loads every session
- `core/grounding/glossary.md` — the product model Garura offers (the *second*
  plane above); it does not describe this tracker
