# Draft — properties, links and rules (#720, stage: links)

You decide what a plan holds, how it links to the other kinds, and which rules always hold for a
plan and for a thin ICE. Each answer you confirm is written into the ontology at the last stage,
word for word, with its example; nothing else in the ontology changes. Type yes to keep this draft,
or say which line or question to change.

Only two kinds change: the Plan and the ICE, plus the one sentence of the opening you agreed at the
kinds (K4). Every line below shows its old words and its new words. A line that is not shown stays
word for word.

## What changes, in one view

- **Plan — properties.** Status gets its five values. Direction, Branch and Item kinds are new. Now
  is required "while In Progress". The Tree shows the feature item.
- **Plan — relationships.** No row changes. A feature item is not a kind, so it has no row.
- **Plan — rules.** One rule changes (who manages a plan, and the branch). Seven rules are new: who
  sets the status and the direction, the item kinds and their parents, the feature item, older plan
  files, the branch, no history, and nothing operational in the product model. Every other rule stays.
- **Plan — states.** New: the five statuses, moved by a person.
- **ICE.** The Thin line, the Thin mark property, the thin-ICE rule, the warning rule and the
  two-places rule. The relationships and every other rule stay.

## The opening (K4, agreed at the kinds)

**Old:** In the tracker, an Epic is an issue of type Epic and a Story an issue of type Story, each
with no label. […] A Feature and a Slice are not issue types: in the tracker, a Story represents a
Feature and an Epic represents a Slice. Domain, Capability, Source and ICE are in the model only; a
Plan is a file. […]

**New:** the same, with one sentence added after "an Epic represents a Slice.": "The tracker's type
Feature is not the Feature kind: in a plan, an issue of type Feature is a feature item, a group of
stories inside an epic (see Plan)."

## Plan

### What it is (agreed at the kinds, shown for the record)

**Old (the end of the paragraph):** "… Its ID is its business intent's issue number. It is not
Claude Code's plan mode and not a design."

**New (the end of the paragraph):** "… Its ID is its business intent's issue number. A person sets
its Status (Not Started, In Progress, Paused, Done or Dropped) and its Direction (1, 2, 3 or none);
nothing works them out. Its tree holds six item kinds, each under one kind of parent: epic, feature,
story, spike, chore and bug. While its work is in progress it has its own branch, `plan/<id>/base`,
and main's copy names that branch. A person manages it with `/update-plan`, which changes the plan
file, the tracker and the product model together, on one approval. The plan file keeps no history:
each landing is one commit whose message names what was asked, the overrides and what is owed.
Status, direction, branch and item kinds are operational: they live in the plan files only, never in
the product model's index or pages. It is not Claude Code's plan mode and not a design."

The rest of the paragraph (the plan play makes it right after `/shape-slice`; its three actions; its
folder) stays word for word.

### Lives at

**Old:** `.garura/project/plans/<id>.yaml`, one file per plan, and its folder
`.garura/project/plans/<id>/` beside it, which holds `evals/` (…) and `guides/` (one guide for each
such slice)

**New:** the same, with this added at the end: "; while its work is in progress, the plan file is
changed only on the plan's own branch, `plan/<id>/base`, and main's copy names that branch"

### Properties

| Property | Old | New | Required (old → new) |
|----------|-----|-----|----------------------|
| ID | The business intent's issue number | unchanged | yes → yes |
| Status | active, done or dropped | Not Started, In Progress, Paused, Done or Dropped. Set by a person, never worked out from the work in the plan | yes → yes |
| Direction | *(new)* | 1 (next), 2 (next in line), 3 (later) or none. Set by a person, never worked out from the work. It is not a ranking: several plans can have the same direction | *(new)* → no — none is an answer |
| Branch | *(new)* | `plan/<id>/base`, the plan's own branch, where every change to the plan is made. Main's copy of the plan file names it, and may be behind it | *(new)* → while its work is in progress |
| Item kinds | *(new)* | The six kinds of item its tree may hold, each under one kind of parent: an epic at the top; a feature item under an epic; a story under an epic or a feature item; a spike, a chore or a bug under a story | *(new)* → yes — every item names its kind |
| Tree | Business Intent → Slice → Epic → Story (with its Feature) → Spike, Chore, Bug — each work item with its tracker issue and its state | Business Intent → Slice → Epic → (feature item →) Story (with its Feature) → Spike, Chore, Bug — each item with its tracker issue, its kind and its state | yes → yes |
| Now | The work item being worked on | unchanged | while active → while In Progress |
| Needs plans | The other plans it needs — worked out from its features' capabilities' needs, never set by hand | unchanged | no → no |
| Folder | (…) | unchanged | yes, once it holds a slice → unchanged |

### Relationships

No row is added, removed or changed. The four rows stay word for word: it is given one Business
Intent; it holds many Slices; it creates many Epics; it needs another Plan.

Why no new row: a feature item is the Plan's own word, not a kind (K2), so it links to nothing. A
story under a feature item still sits in the epic above it (K3), so "Epic holds Story" covers it.
Status, Direction and Branch are properties, not links.

### Rules

**Changed rule — who manages a plan, and the branch**

**Old:** "Its plan file and the tracker always agree — its Tree and each epic's feature-to-story map
show the same story for each feature; managing a plan changes both together and never touches
branches or code."

**New:** "Its plan file and the tracker always agree — its Tree and each epic's feature-to-story map
show the same story for each feature. A person manages a plan with `/update-plan`: in one session,
on one approval, it changes the plan file, the tracker and the product model together, and then
checks that the three agree and that nothing else changed. When the plan has no branch, it first
sets main's plan file to In Progress with the branch named, commits that on main, and cuts the
plan's branch from that commit. It cuts no other branch, never merges a branch, and never touches
code."

**New rules**

1. **Status and direction.** "A person sets the plan's Status and its Direction, and the status of
   each item in its tree. Nothing works them out from the work: there are no roll-ups. A plan is not
   Done because its items are done, and an epic can be closed with open stories. A play changes a
   status or the direction only when a person asked for it. The one exception is the branch step
   above: cutting the plan's branch sets main's plan file to In Progress, because the person started
   work on the plan."
2. **Item kinds and their parents.** "Its tree holds six kinds of item, each under one kind of
   parent: an epic at the top of the tree; a feature item under an epic; a story under an epic or a
   feature item; a spike, a chore or a bug under a story (a bug under the story that brought the
   defect in)."
3. **The feature item.** "An item of kind `feature` is a feature item: an issue of type Feature that
   groups some stories inside one epic. It stands for nothing in the product model: it has no
   `represents` mark, no ICE, and no link to a Feature, a Capability or a Domain. It is never read as
   the Feature kind; a play finds the Story of a Feature by the `represents` mark only. A story under
   a feature item sits in the epic above it."
4. **Older plan files.** "Older plan files also hold the item kind `issue`, or an item under another
   parent (for example a bug under a feature item). That is drift, not an error: the tools still
   print them, and `/update-plan` names such an item when an instruction touches it, offers the right
   kind or parent, and never changes it unasked."
5. **The branch.** "While its work is in progress, a plan has its own branch, `plan/<id>/base`, and
   the plan changes only there. Only two copies of the plan file count: the one on the plan's branch
   and main's. Main's copy names the branch and may be behind it; the copy on any other branch is
   ignored."
6. **No history.** "The plan file keeps no history. Each `/update-plan` landing is one commit on the
   plan's branch, and its message names what the person asked, each rule they overrode, and what is
   still owed (for example a slice, a hidden-file entry or an eval). Git keeps the history."
7. **Nothing operational in the product model.** "Its Status, its Direction, its Branch, its item
   kinds, the status of each item and the record of its changes are operational. They live in the
   plan file, and the record in git, only. They are never written in the product model's index or on
   its pages, and no product-layer kind holds them. A part that `/update-plan` adds to the model (a
   new feature, its thin ICE, its place in a slice) is a product fact, not an operational one."

**Rules that stay word for word:** it does three things in this order; a business intent has one
plan; it holds every slice that serves its intent; it finds work items before it makes new ones; the
plan play writes only the plan file, the epic and the stories; the plan play reads every ICE line
except "Fails if"; its folder keeps its slices' hidden files, evals and guides; it needs another plan
when …; two plans that need each other are one plan; a bug found after a plan is done sits under its
Story; it holds no capability.

### States (new)

"Not Started, In Progress, Paused, Done, Dropped. A person moves a plan from any status to any
other; nothing moves it on its own. The usual way is Not Started → In Progress ↔ Paused → Done, or
Dropped from any status. Cutting the plan's branch moves main's plan file to In Progress (rule 1). A
Done plan is not reopened for a bug (see the bug rule)."

## ICE

### What it is (agreed at the kinds, shown for the record)

**Old:** "It can be **thin**: proposed by `/shape-slice` from the person's answers, and marked so."

**New:** "It can be **thin**: proposed from the person's words by the play that needed it — today
`/shape-slice` or `/update-plan` — and marked so."

### Lives at — the Thin line

**Old:** "A thin ICE's page opens, before `## Intent`, with one line: "Thin: proposed by
`/shape-slice` from the person's answers; deepen with `/discover-capabilities`.""

**New:** "A thin ICE's page opens, before `## Intent`, with one line: "Thin: proposed from the
person's words; deepen with `/discover-capabilities`.""

### Properties — Thin mark

**Old:** "That it is thin: the Thin line at the top of its page and `thin: true` in its spine entry's
`metadata`, both set by `/shape-slice` and both removed by the play that deepens it"

**New:** "That it is thin: the Thin line at the top of its page and `thin: true` in its spine entry's
`metadata`, both set by the play that proposes it and both removed by the play that deepens it"

Required stays "no — only while it is thin". No other property changes.

### Relationships

No row changes.

### Rules

**The thin-ICE rule**

**Old:** "It is written at the depth that is known. A **thin ICE** is one that `/shape-slice`
proposed from the person's answers, when a part the slice needs has no ICE: at least a goal, …"

**New:** "It is written at the depth that is known. A **thin ICE** is one that the play that proposes
it — today `/shape-slice` or `/update-plan` — wrote from the person's words, when a part a slice or a
plan needs has no ICE: at least a goal, …" The rest of the rule stays word for word.

**The warning rule**

**Old:** "When `/shape-slice` proposes a thin ICE, it warns the person that a thin ICE can cause
problems later and that `/discover-capabilities` can deepen it. It never sends the person back to a
discovery play, and nothing stops."

**New:** "When a play proposes a thin ICE, it warns the person that a thin ICE can cause problems
later and that `/discover-capabilities` can deepen it. It never sends the person back to a discovery
play, and nothing stops."

**The two-places rule**

**Old:** "The thin mark is kept in two places that agree: the Thin line at the top of its page and
`thin: true` in its spine entry's `metadata`. The play that deepens the ICE removes both. When only
one is there, it is drift for the Alignment loop."

**New:** the same, with this added at the end: "The Thin line is any line that starts "Thin:" before
`## Intent`, whatever words follow it. A page that still opens with the old line ("Thin: proposed by
`/shape-slice` from the person's answers; …") is thin. Its old words are drift for the Alignment
loop, not an error."

Every other ICE rule stays word for word.

## Left for the last stage

- The examples: the Plan's three examples gain their Status, Direction and Branch, and one shows a
  feature item; the school's thin ICE example shows the new Thin line in place of the old one.
- Each question's status (Q1–Q47), the version (14), the date, and the one log line agreed at the
  kinds.

## Owed, outside the ontology

The ontology changes no script or page. These are named as owed, for the build:

- The scripts that write the exact old Thin line (`/shape-slice`'s and the spine skill's that marks a
  part thin), their tests, and the spine schema's note owe the new line.
- `/update-plan` does not warn the person when it proposes a thin ICE today (its screens carry no
  warning). Under the new warning rule it owes that warning (L11).
- Eleven thin pages in Garura's own model keep the old line; that is drift for the Alignment loop.

## Questions for you

### L1 — Who sets a plan's status and its direction?

- **Question:** Must only a person set a plan's status and its direction, with nothing worked out
  from the work?
- **Answer (proposed):** Yes. A person sets the plan's status, its direction and each item's status.
  There are no roll-ups: a plan is not done because its items are done, and an epic can be closed
  with open stories. A play changes a status or the direction only when a person asked for it.
- **Why it matters:** If a play worked a status out, a plan would show Done or Paused when nobody
  decided it, and a person would stop work that is still owed.
- **Example:** The shop owner closes every story but keeps the plan In Progress, because the launch
  is next week. The clinic manager sets a plan to Paused while the new calendar is bought. The bank's
  product owner closes an epic with one story still open, and the plan stays as it was.

### L2 — Can cutting a plan's branch set the plan to In Progress?

- **Question:** When a play cuts a plan's branch, may it set main's plan file to In Progress, though
  no one typed that status?
- **Answer (proposed):** Yes, and that is the only exception to L1. The person ran `/update-plan`
  (or, later, `/start-change`) on a plan with no branch, so the person started its work. Main's file
  is set to In Progress with the branch named, committed, and the branch is cut from that commit.
- **Why it matters:** Without it, main's copy says Not Started while the work goes on, on a branch
  that main's copy does not name.
- **Example:** The shop owner runs a session on plan 120, which has no branch: main's file reads In
  Progress on `plan/120/base`. The clinic manager starts a story in plan 340: the same happens. The
  bank's product owner aborts the session before anything lands: the branch is deleted and main's
  file is put back.

### L3 — Which kind of item may sit under which?

- **Question:** Must a plan's tree hold only six item kinds, each under one kind of parent?
- **Answer (proposed):** Yes. An epic is at the top. A feature item sits under an epic. A story sits
  under an epic or a feature item. A spike, a chore or a bug sits under a story; a bug under the story
  that brought the defect in.
- **Why it matters:** If any item can sit anywhere, a bug ends up under an epic, and nobody finds the
  story that brought it in.
- **Example:** In the shop's plan, the bug "card fails on mobile" sits under the story "pay as a
  guest". In the clinic's plan, the story "pick a free slot" sits under the feature item "book
  online". In the bank's plan, the chore "move the scoring rules" sits under the story "score the
  application".

### L4 — What happens to older plan files that break L3?

- **Question:** Must an older plan file with the old kind `issue`, or an item under another parent,
  count as drift and not as an error?
- **Answer (proposed):** Yes. The tools still print it. `/update-plan` names the item when an
  instruction touches it, offers the right kind or parent, and never changes it unasked.
- **Why it matters:** If it were an error, every older plan would stop the tools on the day this
  lands. If a play changed it on its own, a person would find their plan changed with no instruction.
- **Example:** The shop's old plan has a closed item of kind `issue`: it prints as before. The
  clinic's old plan has a bug under a feature item: the manager moves a story nearby, and the session
  names the bug and offers to put it under its story. The bank's plan has no such item: nothing is
  said.

### L5 — Does a feature item stand for anything in the product model?

- **Question:** Must a feature item stand for nothing in the product model?
- **Answer (proposed):** Yes. A feature item is an issue of type Feature that groups stories inside
  one epic. It has no `represents` mark, no ICE, and no link to a Feature, a Capability or a Domain. A
  play finds the story of a Feature by the `represents` mark only. A story under a feature item sits
  in the epic above it.
- **Why it matters:** If an agent read a feature item as a Feature, it would give it an ICE and a
  story it must never have, and two things would claim one part of the product.
- **Example:** The clinic's feature item "book online" holds three stories; the Feature "pick a free
  slot" is delivered by one of them. The shop's feature item "pay faster" holds two stories and has
  no ICE. The bank's feature item lines up with a capability, and still has no link to it.

### L6 — How is a plan changed, and what does one change touch?

- **Question:** Must a plan be changed with `/update-plan`, which changes the plan file, the tracker
  and the product model together, on one approval?
- **Answer (proposed):** Yes. Nothing is written before a plain "approved", except the branch step of
  L2. On "approved", the model changes first, then the tracker, then the plan file; then a check
  shows the three agree and nothing else changed. It never merges a branch and never touches code.
- **Why it matters:** A change made in one place only makes the plan, the tracker and the model
  disagree, and the next person trusts the wrong one.
- **Example:** The shop owner says "guest checkout is done" and approves: the plan file and the
  tracker both show it. The clinic manager adds a new feature: its thin page, its story and its plan
  item land together. The bank's product owner types "rejected": nothing changes anywhere.

### L7 — Where does the plan's work happen while it is in progress?

- **Question:** Must a plan in progress change only on its own branch, `plan/<id>/base`?
- **Answer (proposed):** Yes. Only two copies of the plan file count: the one on the plan's branch
  and main's. Main's copy names the branch and may be behind it. The copy on any other branch is
  ignored.
- **Why it matters:** A person who changes a plan on another branch makes a third copy that
  disagrees with the other two, and no one knows which is right.
- **Example:** The shop's plan 120 changes only on `plan/120/base`. The clinic manager is on a story
  branch of plan 340: the session switches to the plan's branch and back. The bank's plan 51 is Done:
  no branch holds work for it.

### L8 — Where is the record of each change to a plan?

- **Question:** Must the plan file keep no history, with each landing's commit message as the
  record?
- **Answer (proposed):** Yes. Each `/update-plan` landing is one commit on the plan's branch. Its
  message names what the person asked, each rule they overrode, and what is still owed. Git keeps the
  history.
- **Why it matters:** A history inside the file grows with every change and can disagree with the
  commits.
- **Example:** The shop owner closes a story and renames another: one commit names both. The clinic
  manager puts a story under the wrong kind of item on purpose: the commit names the override. The
  bank's product owner adds a feature to a plan with no slice: the commit says the slice is owed.

### L9 — Can a plan's operational facts go into the product model?

- **Question:** Must a plan's status, direction, branch, item kinds, item statuses and change record
  stay out of the product model?
- **Answer (proposed):** Yes. They live in the plan file, and the record in git, only. They are never
  written in the product model's index or on its pages, and no product-layer kind holds them. A new
  feature that a session adds to the model is a product fact, and goes in as usual.
- **Why it matters:** The product model says what the product is. If it held "Paused" or "direction
  1", it would change every time a person moved the work, and the model and the plan would drift
  apart.
- **Example:** The shop's plan moves to Paused: no page of the shop's model changes. The clinic's
  plan gets direction 1: the model's index is the same. The bank's session adds a new feature: its
  page and its entry go into the model, and its plan item stays in the plan file.

### L10 — Do the Plan's relationships change?

- **Question:** Must the Plan's four relationships stay as they are, with no new row?
- **Answer (proposed):** Yes. A plan is given one business intent, holds many slices, creates many
  epics, and needs other plans. A feature item is not a kind, so it has no row. A story under a
  feature item still sits in its epic.
- **Why it matters:** A new row for the feature item would make it a kind by the back door, against
  your answer at K2.
- **Example:** The shop's plan holds one slice and its epic, as before. The clinic's plan holds a
  feature item inside its epic: no new link. The bank's plan holds two slices, read from the link, as before.

### L11 — Must every play that proposes a thin ICE warn the person?

- **Question:** Must the warning about a thin ICE come from every play that proposes one, not only
  from `/shape-slice`?
- **Answer (proposed):** Yes. The play warns the person that a thin ICE can cause problems later and
  that `/discover-capabilities` can deepen it, and nothing stops. `/update-plan` does not warn today,
  so its warning is named as owed work.
- **Why it matters:** A person who adds a feature in a plan session gets a thin ICE with no word
  about it, and finds the gap only when a build goes wrong.
- **Example:** The clinic manager adds "send a reminder" in a plan session and is warned. The shop
  owner shapes a slice that needs "save the card" and is warned, as today. The bank's product owner
  sees the warning and deepens the ICE later.

### L12 — Who sets the thin mark?

- **Question:** Must the Thin mark property say "set by the play that proposes it"?
- **Answer (proposed):** Yes. The play that proposes the thin ICE sets the Thin line on its page and
  `thin: true` in its spine entry. The play that deepens it removes both, as today.
- **Why it matters:** If the property names one play, the next play that proposes a thin ICE breaks
  the ontology again, as `/update-plan` did.
- **Example:** The clinic's "send a reminder" is marked by `/update-plan`. The shop's "save the card"
  is marked by `/shape-slice`. The school's "send a note home" loses both marks when it is deepened.

### L13 — Is a page with the old Thin line still thin?

- **Question:** Must a page that still opens with the old Thin line count as thin?
- **Answer (proposed):** Yes. The Thin line is any line that starts "Thin:" before `## Intent`,
  whatever words follow, as the ready check reads it today. The old words are drift for the
  Alignment loop, not an error.
- **Why it matters:** If only the new words counted, the old thin pages would stop being thin on the
  day this lands, and their gaps would vanish from the ready check.
- **Example:** The shop's thin ICE from last month keeps its old line and still reads "partly ready —
  thin ICE". The clinic's new thin ICE gets the new line. The bank's product owner deepens an old one:
  both marks go, as before.
