# Managing Work on Garura

How work on Garura itself gets described, tracked, picked up, handed back, and
closed. This is the convention for this repository's issue tracker. It is
loaded in every session so that no one — human or agent — has to ask, guess, or
invent one.

---

## First: Garura is built the way it tells others to build

Since 2026-10-22 Garura's own work follows the product model Garura offers (ontology v7,
`core/components/memory/standards/schemas/product-os/ontology.md`; Kapil: "going forward, our approach
to building Garura will also change"). There is one plane, not two:

```
Product model                          Tracker
Business Intent                 ── issue: Business Intent   (its issue number is its plan's ID)
Capability + its ICE            ── never an issue
└─ Feature + its ICE            ── issue: Story, one in each Epic that delivers it
Slice (features from any        ── issue: Epic, made by the plan play for each slice
       capabilities, in order)     └─ Story, one per feature of the slice
                                      ├─ Spike / Chore   ── issue, when the work needs one
                                      └─ Bug             ── issue, always under the Story that introduced it
```

Domains live in the product model and link loosely to business intents and capabilities; they are
never an issue and never part of a plan. A slice is in the model; its Epic is the work that
delivers it.

---

## What am I filing?

| | What it is | Filed when |
|---|---|---|
| **Business Intent** | What a person wants — an outcome. Tracking only: it holds no ICE and agents never build it. Met by its proof, never closed by finishing its children. | A goal is stated that work will be done to serve. |
| **Epic** | The work order for one slice: an ordered group of features, from any capabilities, that a person can test end to end. It holds one Story for each feature of the slice and has no ICE of its own. | /shape-slice shapes a slice for a business intent; the plan play then makes its Epic. |
| **Story** | The work order for one feature: one thing a person can do inside a capability. Its scope of work is written from its feature's ICE and its capability's ICE, and never holds a failure or recovery condition (ADR 049). One coherent change that can be built, reviewed, and merged on its own. | The plan play makes the Epic of the feature's slice. |
| **Bug** | A defect in a feature: it behaves differently from what was intended. Filed under the Story that introduced it. | Observed behaviour departs from expected behaviour. |
| **Chore** | Upkeep under a Story that changes no behaviour. | Something needs tidying and nothing a user sees will change. |
| **Spike** | A question to answer under a Story. The result is a decision record, not shipped code. | A Story can't be built until something is found out. |

An Epic is never worked directly; its Stories are. A Bug is not "something is missing" —
a missing feature is a Story.

## Where does it hang?

Every Epic serves one or more business intents, every Story hangs under its Epic, and every Bug, Spike
and Chore under a Story — as a real parent/child link in the tracker. A business intent has no parent;
business intents link to each other only by "identified by". Each business intent has exactly one plan; it holds every slice that serves the intent (ADR 049). It is kept
at `.garura/project/plans/<business-intent-issue>.yaml`, and each slice's eval and usage guide sit beside it, in
`plans/<id>/evals/` and `plans/<id>/guides/`. A builder never reads the evals folder. Plays and skills are named by the harness
standard (`docs/standards/harness-standard.md`).

## How does that land in the tracker?

- **Type lives in the type field.** Each of the six types above is an issue
  type in the `intent-driven-ai` organization. Never encode the type as a title
  prefix (`[Story]`, `Bug:`, `[DEF]`); the field is the only place it belongs.
- **No labels, for now.** Not for type, status, area, or severity. A severity
  and priority taxonomy will be designed later; until then, open issues carry
  none. Closed issues keep their old labels as history.
- **Title states the outcome**, in the language a reader operates in — what
  changes and for whom — not the files being touched.

## Phoenix tools and the Phoenix project

Tools built beside Garura — Argus (the review tool), and later Griffin, Sphinx and others —
are Phoenix tools (Kapil, 2026-10-20). Their issues live in this repository with the same
types and parent links, and are tracked in one org project, **Phoenix**
(`intent-driven-ai`, project 1), never a project per tool. Each tool's issues carry the
project's **Garura tools** field set to the tool's name (a project field, not a label — the
no-labels rule above stands). The project is also where Phoenix releases are followed.

## Is it ready to work?

Before a Story or Bug is handed to a session, it has to stand on its own. The
session working it reads the issue and its parent, and nothing else.

**A Story is ready when it has** a parent Epic linked, acceptance criteria
(what must be true for this to be done), and a scope boundary (what this issue
deliberately does *not* touch).

**A Bug is ready when it has** a reproduction — the steps and the actual
behaviour — and a statement of the expected behaviour.

**An Epic is ready when** it names its slice and states the "done when." It is then
decomposed into Stories; it is never worked directly.

An issue that fails these tests is not blocked on effort — it is blocked on
being written. Finish writing it before anyone picks it up.

## How does work get picked up?

Planning and decomposition happen in an **orchestrator session**: reading the
backlog, shaping Epics, cutting Stories, ordering them. No implementation
happens there.

Each Story or Bug then goes to **its own session**. That session:

1. Reads the issue and its parent from the tracker itself — it is not briefed by
   hand, and a chat summary is never the source of truth.
2. Works on one branch for that one issue.
3. Closes the issue with its pull request.

One issue, one session, one branch, one pull request. A session that ends up
carrying two issues has lost the thread of both.

**The one exception is a drive** (ADR 029). A drive works on **one main
issue**, and opens **one branch** for it when it starts. That branch stays the
same for the whole drive, and the drive raises **one pull request** from it.
The plays a drive runs open no branch and no issue of their own; they work on
the drive's branch. Issues **linked** to the main issue — its child issues,
by the real parent/child link in the tracker, never a mention in the body —
are fixed on that same branch, in the same change. The drive writes **one
handoff**, on its main issue.

## How far does my work extend?

**The issue being worked defines the scope. Work never goes beyond it.**
For a drive, that scope is its main issue plus the child issues linked under
it — nothing more.

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

**Four moves end a session, in order: review the change, open the pull
request, write the handoff, stop.** Nothing comes after. Judging the change
and landing it belong to someone else.

**It reviews its own work, and writes the guidelines it reviews against.**
Before the pull request goes up, the session works out what a change like the
one it just made is most likely to have got wrong, and checks against that.
Nobody hands it the criteria — a list written by someone who never saw this
change would not know where to look. The point is hygiene: catch the obvious
breakage here, rather than spend a full cycle downstream on something a
second reading of the diff would have caught.

**That review produces no verdict.** A session already believes its change is
right — believing that is what made it write the change — so its own
assessment reads like assurance while carrying none. Both halves hold at once:
re-reading your own work is worth the time, and your opinion of your own work
is not evidence. The judgement is taken elsewhere, against evals the builder
never sees — anything the builder could read, it would end up writing to.
What a session owes a reviewer is orientation, not a judgement.

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

**Issue types belong to the organization, not the repository.** The six types
are set on `intent-driven-ai`; a repository under a personal account has no
issue types at all, which is why older issues carry title tags instead. Setting
a type goes through the issue's type field (GraphQL `issueType`, or the REST
`type` field), not through a label.

**Applying a label that does not exist creates it.** There is no separate
create-then-apply step, and there is no error to catch. The flip side: a typo in
a label name silently produces a new label rather than failing, so read the
label back after applying it.

---

## Related

- `CLAUDE.md` — project instructions; points here so this loads every session
- `core/grounding/glossary.md` — the product model Garura offers (the *second*
  plane above); it does not describe this tracker
