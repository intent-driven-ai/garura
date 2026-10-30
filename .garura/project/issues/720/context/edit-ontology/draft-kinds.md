# Draft — the kinds (#720, stage: kinds)

You decide which kinds this change makes or changes, and how the ontology tells a plan's
"feature" apart from the product's Feature. No new kind is proposed: the Plan kind and the ICE
kind change in place, and nothing else does. Type yes to keep these kinds and answers, or say
which one to change; the next stage then writes each kind's properties, links and rules from them.

## What changes, in one view

- **Plan — changed.** It gains its five statuses, its direction, its six item kinds, its branch,
  "no history: one commit for each landing", and "managed by `/update-plan`". Why: the plan files,
  the plan tool and `/update-plan` already work this way, and the ontology still says "active,
  done or dropped".
- **ICE — changed.** Its Thin line becomes "Thin: proposed from the person's words; deepen with
  `/discover-capabilities`." and the places that say only `/shape-slice` proposes a thin ICE say
  "the play that proposes it". Why: `/update-plan` proposes thin ICE too.
- **Feature item — not a kind.** An item of kind `feature` in a plan is the Plan's own word, inside
  the Plan kind. It is not the Feature kind (K2).
- **Every other kind — unchanged.** Business Intent, Source, Domain, Capability, Feature, Slice,
  Epic, Story, Spike, Chore and Bug keep every line. Two clashes touch Epic and Story; K3 and K6
  ask you about them instead of changing them.

## Step 2 — What we reuse, and where it clashes

**Reused as it is**

- The Plan kind: its ID, Tree, Needs plans and Folder, its links (given one business intent,
  holds slices, creates epics, needs another plan) and its rules.
- The Epic, Story, Spike, Chore and Bug kinds: a plan item of kind `epic`, `story`, `spike`,
  `chore` or `bug` is that kind. Nothing new is made for them.
- The plan-view template (memory): the plan's five statuses and the directions 1 (next),
  2 (next in line) and 3 (later), or none.
- The plan tool's notes and `/update-plan`'s intent: the six item kinds and their parents, the
  branch `plan/<id>/base`, one commit for each landing.
- The ICE's thin mark in two places that agree (the Thin line on the page, `thin: true` in the
  spine entry). The ready check finds the Thin line by its start, "Thin:", so the new words keep
  working with it.

**Clashes found**

1. **One word, two things: "feature".** In the model, a Feature is one thing a person can do inside
   a capability, with its own ICE, and "is not an issue type". In a plan, an item of kind `feature`
   is an issue of type Feature that groups stories inside an epic. In Garura's own plan 717, the
   feature items #718, #719 and #720 line up with the model's capabilities cap-718, cap-719 and
   cap-720, not with any Feature. So a feature item must never be read as the Feature kind. (K2)
2. **A story under a feature item.** Story says "it sits in exactly one epic", and Epic says "it
   holds stories". When a story sits under a feature item, its parent in the tracker is the
   feature item, not the epic. (K3)
3. **The opening of the ontology** says "A Feature and a Slice are not issue types". That stays true
   of the Feature kind, but a reader who sees the type Feature in the tracker has no word for it. (K4)
4. **The Plan's own lines are out of date:** Status "active, done or dropped"; Now "while active";
   Tree "Business Intent → Slice → Epic → Story → Spike, Chore, Bug" (no feature item); and the rule
   "managing a plan changes both together and never touches branches or code" — `/update-plan`
   changes three things (the plan file, the tracker and the model), and cuts the plan's branch when
   the plan has none. These change inside the Plan kind, at the next stage.
5. **The old Thin line is written in many places.** `/shape-slice`'s scripts, the page and spine
   skill that marks a part thin, their tests, the spine schema's note, and eleven pages of
   Garura's own model use the exact old words. (K5, K6)
6. **An epic with no slice.** `/update-plan` may put a new feature's story under an epic the person
   names when the plan holds no slice, and plan 717's epic #956 has no slice. Epic says "it
   represents one slice"; Story says "its feature is one of its epic's slice's features". (K7)

**Seen, and left as it is**

- A plan file's item statuses (Not Started, In Progress, Now, Done, Blocked, Dropped), set by a
  person, sit beside each work item's own state in the tracker (open or closed). The need does not
  touch them.
- The old item kind `issue` is still in plans 606, 717, 756 and 788. The tools print it, and
  `/update-plan` names it and offers the right kind, never changing it unasked. It is not one of
  the six kinds.
- Garura's own spine names an issue on some capabilities (cap-718 → #718). The product model is not
  changed by this need.

## Step 3 — The terms

In the people's own words.

- **Things (nouns):** plan, plan file, main's copy, the plan's branch (`plan/<id>/base`), status
  (Not Started, In Progress, Paused, Done, Dropped), direction (1 next, 2 next in line, 3 later,
  none), tree, item, item kind (epic, feature, story, spike, chore, bug; the old `issue`), parent,
  feature item, session, instruction, the running list, approval ("approved", "rejected",
  "abort"), landing, commit message, what was asked, override, what is owed, thin ICE, Thin line,
  thin mark.
- **Actions (verbs):** a person sets (a status, a direction); an item sits under (its parent); a
  plan is worked on (its branch); a session changes together (the plan file, the tracker, the
  model); a landing is one commit; a person overrides (a rule); a change owes (a slice, a
  hidden-file entry, an eval); a play proposes and deepens (a thin ICE).

## Step 4 — The kinds

### Plan (changed)

**What it is (proposed):** The thread between the product layer and the work layer, kept in the
repo, so that anyone on any day can see where the work for one business intent stands and carry
on. It is given one business intent, holds every slice that serves it, and creates one epic for
each, as today. A person sets its Status (Not Started, In Progress, Paused, Done or Dropped) and
its Direction (1, 2, 3 or none); nothing works them out. Its tree holds six item kinds, each
under one kind of parent: epic, feature, story, spike, chore and bug. While its work is in
progress it has its own branch, `plan/<id>/base`, and main's copy names that branch. A person
manages it with `/update-plan`, which changes the plan file, the tracker and the product model
together, on one approval. The plan file keeps no history: each landing is one commit whose
message names what was asked, the overrides and what is owed. Status, direction, branch and item
kinds are operational: they live in the plan files only, never in the product model's index or
pages. It is not Claude Code's plan mode and not a design.
**Who reads it:** both (as today).
**What changes:** the What it is above; Lives at gains the branch; the next stage writes the
properties Status, Direction, Branch, Item kinds and Now ("while In Progress"), the Tree with the
feature item, and the rules (who sets status and direction, the item kinds and their parents,
`/update-plan` changes three things together, nothing operational in the product model).

### Feature item (the Plan's own word — not a kind)

**What it is (proposed):** An item of kind `feature` in a plan's tree: an issue of type Feature
that groups some stories inside one epic. It sits under an epic and holds stories. It represents
nothing in the product model: it has no `represents` mark, no ICE, and no link to a Feature, a
Capability or a Domain.
**What it is not:** the Feature kind, which is one thing a person can do inside a capability, in
the model, delivered by a Story. A play finds a feature's Story by the `represents` mark only
(rule R3), so it never takes a feature item for it.
**Who reads it:** both. It is defined inside the Plan kind, with the other item kinds.

### ICE (changed)

**What it is:** unchanged, except one sentence. "It can be thin: proposed by `/shape-slice` from
the person's answers" becomes "It can be thin: proposed from the person's words by the play that
needed it — today `/shape-slice` or `/update-plan` — and marked so."
**Who reads it:** agent (as today).
**What changes:** Lives at — the Thin line reads "Thin: proposed from the person's words; deepen
with `/discover-capabilities`."; the Thin mark property — "set by the play that proposes it"; the
example's Thin line. The thin-ICE rule and the warning rule are rules: the next stage words them
from K5.

### Not kinds

- **Status, Direction, Branch** — properties of the Plan.
- **Session, running list, approval, landing, override, what is owed** — how `/update-plan` works.
  The Plan's rules name the session and the commit; the rest stays in the play.
- **History** — git keeps it. The plan file has none.

## Questions for you

### K1 — Do the Plan and ICE kinds change in place?

- **Question:** Must this change keep the Plan kind and the ICE kind, and change them in place,
  with no new kind?
- **Answer (proposed):** Yes. Every new word (status, direction, branch, item kinds, the session,
  the Thin line) is a property, a rule or a line of one of these two kinds. A new kind would hold
  operational facts that belong to the plan.
- **Why it matters:** A new kind for "plan status" or "plan session" would sit beside the Plan and
  say part of what it is. Two kinds that say one thing drift apart.
- **Example:** The shop's plan 120 gets "In Progress, direction 1, on `plan/120/base`" as three
  properties of one plan. The clinic's plan 340 gets "Paused". The school's thin ICE for "send a
  note home" keeps its kind; only its first line changes.

### K2 — How does the ontology tell a plan's feature item apart from the Feature kind?

- **Question:** Must an item of kind `feature` in a plan stay the Plan's own word, always written
  "feature item", and never become a kind of the ontology?
- **Answer (proposed):** Yes. A feature item is an issue of type Feature that groups stories inside
  an epic. It is defined inside the Plan kind. It represents nothing in the model: no `represents`
  mark, no ICE, no link to a Feature, a Capability or a Domain. The bare word "Feature" in the
  ontology always means the product's Feature. Two other ways were weighed and are not proposed:
  a new work-layer kind (it adds a kind for a grouping that holds no work of its own), and a new
  name for the item kind in the plan files (it changes every plan file and the plan tool, outside
  this need).
- **Why it matters:** If one word means two things, an agent links a story to the wrong thing. In
  Garura's own plan, the feature item #720 lines up with a capability, not a Feature: read as a
  Feature, it would get a Story and an ICE it must never have.
- **Example:** In the clinic's plan, the feature item "book online" holds three stories; the
  clinic's model has the Feature "pick a free slot", delivered by one of those stories. In the
  shop's plan, the feature item "pay faster" holds two stories; the Feature "guest checkout" is a
  part of the product with its own ICE. In the bank's plan, a feature item groups the stories of
  "upload once" and has no ICE.

### K3 — Does a story under a feature item still sit in one epic?

- **Question:** Must the Story and Epic kinds stay as they are when a story sits under a feature
  item?
- **Answer (proposed):** Yes, no change to Story or Epic. The Plan kind says: a feature item sits
  inside an epic, so a story under it sits in that epic. "A story sits in exactly one epic" means
  the epic above it in the plan's tree, through a feature item or not. Its parent in the tracker
  may be the feature item. If you want the Story and Epic kinds to say this in their own words,
  say so: then those two kinds change too.
- **Why it matters:** If "sits in" meant only "the direct parent", every story under a feature item
  would break the Story kind, and every check would report it.
- **Example:** The clinic's story "pick a free slot" sits under the feature item "book online",
  which sits under the epic "self-booking": it is in that epic. The shop's story "send receipt"
  sits straight under its epic. The bank's story "score the application" sits under a feature item
  of the epic "one-day decision".

### K4 — Does the opening of the ontology name the type Feature?

- **Question:** Must the opening paragraph about the tracker gain one sentence about the type
  Feature?
- **Answer (proposed):** Yes, one sentence and no more: "The tracker's type Feature is not the
  Feature kind: in a plan, an issue of type Feature is a feature item, a group of stories inside
  an epic (see Plan)." It changes no kind. Q20's answer says the same.
- **Why it matters:** A reader who starts at the top reads "a Feature is not an issue type", then
  finds issues of type Feature in every plan. Without the sentence they guess.
- **Example:** The shop's product owner sees an issue of type Feature and reads that it is a
  group of stories. The clinic manager's agent reads the same line and never looks for its ICE. The
  bank's tester finds the Feature kind in the model and its Story in the tracker, not under the
  type Feature.

### K5 — Which plays does the ICE kind name for a thin ICE?

- **Question:** Must the ICE kind say "the play that proposes it" for a thin ICE, instead of
  naming `/shape-slice` alone?
- **Answer (proposed):** Yes. The Thin line names no play that proposes. What it is names the two
  plays that do it today, `/shape-slice` and `/update-plan`. The Thin mark property and the
  thin-ICE rule say "the play that proposes it". The rule that the play warns the person is worded
  at the next stage, with the other rules.
- **Why it matters:** If the kind names one play, the next play that proposes a thin ICE makes it
  wrong again, as `/update-plan` did.
- **Example:** The clinic's "send a reminder" was proposed in a plan session. The shop's "save the
  card" was proposed while shaping a slice. The school's "send a note home" came from a slice. All
  three carry the same Thin line and the same mark in their spine entry.

### K6 — Do pages with the old Thin line still count as thin?

- **Question:** Must a page that opens with the old Thin line ("Thin: proposed by `/shape-slice`
  from the person's answers; …") still count as thin?
- **Answer (proposed):** Yes. The thin mark on a page is a line that starts "Thin:" before
  `## Intent`, as the ready check reads it today. The old words are drift for the Alignment loop,
  not an error, and no page is changed by this edit. The scripts that write the exact old line
  (`/shape-slice`'s and the spine skill's) owe the new line; that is work for the build, named as
  owed, not part of the ontology.
- **Why it matters:** If only the new words counted, eleven thin pages in Garura's own model
  would stop being thin on the day this lands, and their gaps would vanish from the ready check.
- **Example:** The shop's thin ICE from last month keeps its old line and still reads "partly
  ready — thin ICE". The clinic's new thin ICE gets the new line. The bank's product owner deepens
  an old one: both marks go, as before.

### K7 — Is an epic with no slice part of this change?

- **Question:** Must this change leave the Epic and Story kinds as they are, though a plan may hold
  an epic with no slice?
- **Answer (proposed):** Yes, leave them. The need is about the Plan and the Thin line. An epic
  with no slice comes from plans that never went through the shaping loop, and `/update-plan`
  records a slice as owed when it places a story there. It is named as owed work, for its own
  change.
- **Why it matters:** Changing Epic here widens the change past its need, and the play's check
  fails a change that touches a kind its need did not name.
- **Example:** Garura's plan 717 has an epic with no slice until `/shape-slice` runs for it. The
  clinic's plan has a slice for each epic. The bank's product owner puts a new story under an epic
  with no slice: the commit says a slice is owed.

## Log line (draft, one for the whole change)

- 2026-10-30 — v14 (#720, plan #717, with the product owner): the Plan kind catches up with how
  plans are kept. A plan's Status is Not Started, In Progress, Paused, Done or Dropped (was active,
  done or dropped), and it has a Direction (1, 2, 3 or none); a person sets both, and nothing works
  them out. Its tree may hold six item kinds, each under one kind of parent: an epic at the top, a
  feature item under an epic, a story under an epic or a feature item, a spike, chore or bug under
  a story. A feature item is an issue of type Feature that groups stories inside an epic: the
  Plan's own word, not the Feature kind, and it represents nothing in the model; a story under it
  sits in its epic. While its work is in progress a plan has its own branch, `plan/<id>/base`. The
  plan file keeps no history: each landing is one commit whose message names what was asked, the
  overrides and what is owed. Managing a plan is `/update-plan`, which changes the plan file, the
  tracker and the product model together, on one approval. These stay in the Plan kind and the
  plan files, never in the product model. The ICE's Thin line becomes "Thin: proposed from the
  person's words; deepen with `/discover-capabilities`.", and a thin ICE is proposed by the play
  that needs it (today `/shape-slice` or `/update-plan`); a page with the old line is still thin.
  The opening names the type Feature. Q41–Q47 are added; Q7, Q20 and Q38 change, and Q1, Q4, Q22
  and Q23 name the feature item. No other kind changes.

What each kind adds to that line:

- **Plan:** status, direction, item kinds, feature item, branch, no history, `/update-plan`.
- **ICE:** the Thin line, "the play that proposes it", the old line still counts.

## Q20, settled (proposed answer for the next stages)

**Answered by:** the issue type names the kind: type Epic is an Epic and type Story is a Story,
each with no label (R1, R2); label `product` is a Business Intent; label `work-item` with its kind
is a Spike, a Chore or a Bug. The type Feature names no kind of this ontology: in a plan, an issue
of type Feature is a feature item, a group of stories inside an epic (Plan), never the Feature
kind. Which Epic stands for a slice, and which Story for a feature, is found by the plan file's
`represents` mark, never by type or title (R3).
**Status:** answered.
