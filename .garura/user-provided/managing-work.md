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

## How is work handed out?

A session is spawned with everything it is ever going to be told. It reads the
issue itself, so the spawn instruction does not restate the work — it names the
issue as the source of truth and adds only what the issue cannot carry.

A spawn instruction states:

- **Which issue**, by number, and that the issue and its parent are what
  govern — not the prompt, and not a summary written by hand.
- **The scope boundary** — that the issue's boundary holds, and that anything
  found outside it is proposed rather than fixed.
- **Where the session stops.** Not implied, not left to good judgement.
  Opening a pull request and merging one are different endings, and a session
  that is not told which one it owns will choose for itself.
- **How to hand back** — where the report goes and who is notified.

One Story or Bug per session, never two. That rule is stated above and is worth
repeating here, because the temptation to bundle arrives at spawn time, when
two small issues look like one small session.

## Can a session be steered once it is running?

**No. There is no channel to a session already in flight.** Nothing reaches it
— no correction, no missing context, no answer to a question it raised. The
only interventions available are interrupting it or archiving it, and both of
them end the run rather than adjust it.

This is the constraint the rest of the protocol is built around. Every
instruction a session needs has to be complete at the moment it is spawned.
Never design a workflow that assumes mid-flight correction; the correction has
nowhere to arrive.

## Where does a session stop?

**A working session raises the pull request and hands back. It does not review
its own work, and it never merges.**

Three moves end a session, in this order: open the pull request, post the
handoff, stop. Nothing comes after. Everything that happens to the change from
that point — reading it, judging it, landing it — belongs to someone else.

**Not reviewing.** A session cannot usefully review its own diff. It already
believes the change is right; believing that is what made it write the change.
Review needs eyes that were not in the room while the work was done, and a
session grading its own homework produces a verdict nobody should trust —
worse, one that reads like assurance. Raise it and hand it over.

**Not merging.** Merging is a separate decision taken with a human looking at
the diff, and it is not the worker's to take — not when the checks are green,
not when the change is obviously correct, not when nobody appears to be
waiting. This is not new policy. The delivery gates were relaxed across the
board, and the merge step was deliberately left pinned to its human beat; the
protocol only says out loud what that decision already assumed.

A session that merged its own work is how this rule was learned. Its
instruction said "open a pull request" and said nothing about stopping there,
so it filled the silence itself. Silence at the stop point is not neutral — it
is an invitation.

What the session *does* owe the reviewer is a way in: the handoff says where
the change came to rest and what a reviewer should know before opening it. That
is orientation, not a verdict.

## How is work handed back?

**Every session owes a handoff before it finishes. Every session, every time —
including one that finished cleanly with nothing left over.**

A clean session that says nothing is indistinguishable from a session that
died. Resolving that ambiguity costs someone an investigation, and the
investigation almost always concludes "it was fine." A clean run says so
explicitly, and the question never has to be asked.

A handoff carries:

- **What was done** — the outcome, in the language a reader operates in.
- **What was deliberately not done, and why** — the boundaries held and the
  temptations declined.
- **What was found that falls outside the issue** — as proposals, never as
  filings.
- **Where the work came to rest** — the branch, the pull request and its
  state, and anything a reviewer needs before picking it up.

## Where does the handoff live?

**The durable record is a comment on the issue that was worked. The live
notification to the orchestrator is a nudge layered on top of it, and it is
sent second.**

The ordering is the entire point. Notification delivery is best-effort: the
trigger carrying it can fail to register, the session can die before it
registers one, and the orchestrator session it targets may be gone by the time
it fires. A report that exists only in a notification is lost the moment any of
those happens. A report on the issue is found by anyone who opens the issue —
today, or in six months, by someone who was in neither session.

So the comment is written first and the notification is sent after it. Comment
lands and notification fails: an acceptable outcome, and the one the design
expects — the record survives and someone finds it. Notification lands and no
comment exists: the report now depends on a message being read before it
scrolls out of view, which is the failure this ordering exists to prevent.

## Who files the follow-ups?

**The worker proposes. The orchestrator files.** A session that finds something
outside its issue writes it into the handoff as a proposal and stops there. It
does not open the issue itself.

Filing is a scoping decision: whether the thing is worth tracking at all, how
it is cut, which Feature it hangs under, and where it sits against everything
else waiting. A session that sees one issue cannot make that call. A worker
that files its own follow-ups has decided scope it was never given.

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

**Notifying an orchestrator session means scheduling a one-shot trigger against
it.** No direct message channel exists between sessions. The return path that
works is a trigger the worker registers before it finishes, targeting the
orchestrator's session identifier and firing a prompt that carries the handoff
text. Name it so its origin is obvious — whoever finds it later should not have
to work out which session left it. Register it *after* the issue comment
exists, never instead of it.

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
