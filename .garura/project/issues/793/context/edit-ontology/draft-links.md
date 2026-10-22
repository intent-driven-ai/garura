# Draft — the properties, links and rules (stage `links`, steps 5–6) — #793

**Need:** the delivery plays work on work items, not on the spine's slices and epics. The questions (Q1–Q26) and the 13 kinds are agreed. This draft gives each kind what it holds, how it links to the other kinds, and what must always be true. Four points were left open at the kinds stage; each has a proposed answer at the end, for you to accept or change.

## Every link, on one screen

Product layer on the left, work layer on the right, the Plan between them.

```
PRODUCT LAYER                                   THREAD            WORK LAYER (label work-item)

Source ──── shows (N:N) ────► Business Intent ◄── is given (1) ── Plan
                              (label product)  ◄──────────── serves (1..N) ─────── Epic
Capability ── serves (N:N) ─► Business Intent
Business Intent ── has, marked change/add/remove (N:N) ──► Capability
Business Intent ── touches, for search only (N:N) ──► Domain
Business Intent ── identified by (N:N) ──► Business Intent

Domain ── has (1:N) ──► Capability              (a capability sits in at most one domain)
Capability ── needs (N:N) ──► Capability
Capability ── identified by (N:N) ──► Capability
Capability ── has (1:N) ──► Feature             (a feature has exactly one capability)
ICE ── is for (1:1) ──► Capability  or  Feature
Slice ── groups, in order (N:N) ──► Feature

                                                Plan ── picks (1:N) ──► Slice
                                                Plan ── creates (1:N) ──► Epic
                                                Plan ── needs (N:N) ──► Plan

                              Slice ◄──────── represents (1:1) ─────────────────── Epic
                              Feature ◄────── represents (1 feature : N stories,
                                                one story per feature in each epic) ── Story
                              ICE ◄────────── written from (2: its feature's and
                                                its capability's) ───────────────── Story
                                                                         Epic ── holds (1:N) ──► Story
                                                    Story ── has child (1:N) ──► Spike, Chore, Bug
                    Business Intent, Feature, Story ◄── led to (0..N) ── Spike
```

No work item links to a Domain or a Capability. A Spike, Chore or Bug links to no Feature: it reaches its Feature, Epic and Business Intent through its parent Story.

## The kinds

### Business Intent — product layer — in the tracker as an issue labelled `product`

**Properties:** as in v6, with no change: Title, Outcome, Why, Asked by, Proof it is met, Stage (all required); Must not, Rules (not required); Confirmed by and when (required once confirmed); Touches (domains and capabilities only, each marked adds, changes or removes; not required until a part is linked); What was done (the finished work items, with links; not required until work finishes). "Functionality" becomes "feature" in their text.

**Links:**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| other → this | Source | many | A source shows what it wants |
| other → this | Capability | many | A capability serves it |
| this → other | Capability | many | It has a capability, marked change, add or remove on its Touches list |
| this → other | Domain | many | It touches a domain — for search only |
| this → other | Business Intent | many | It was identified by another business intent — never a dependency |
| other → this | Plan | one | Its one plan is given it |
| other → this | Epic | many | An epic serves it |

**Rules:** as in v6. It is the only kind with the label `product`. It holds no ICE. The v6 link to "Tracker Issue" goes: its line "In the tracker as" takes its place. A work item reaches it through its Epic.

### Source — product layer — not in the tracker

No change from v6. Shows (many) Business Intent; kept as it was read.

### Domain — product layer — not in the tracker

**Properties:** Name and one line (required); Page depth, light or full (required); Intents, the business intents that touch it, for search only (not required).

**Links:** has (many) Capability; touched by (many) Business Intent.

**Rules:** It holds no ICE. It is never in a plan and never stops work. No work item links to it. It has one or more capabilities.

### Capability — product layer — not in the tracker

**Properties:** as in v6: Name and one line, ICE, Serves, Needs, Identified by, Domain. One new: **Done** — worked out each time it is asked, never stored (see parked point 1).

**Links:** serves (many) Business Intent; has (many) Feature; has (one) ICE; needs (many) Capability; identified by (many) Capability; sits in (at most one) Domain.

**Rules:** as in v6, with "functionality" read as "feature". New: no work item links to it — a Story reaches it through its Feature and reads its ICE from there. Dropped: "a Feature issue carries its ICE". It is done when every feature in it is delivered (parked point 1).

### Feature — product layer — in the tracker as a Story (one Story in each Epic that delivers it)

**Properties:** Name and one line (required); ICE, its one ICE (required, to be ready); Capability, its one parent capability (required, to be ready); Delivered — worked out, never stored: it has at least one closed Story.

**Links:**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Capability | one | Its one parent capability |
| other → this | ICE | one | Its one ICE |
| other → this | Slice | many | A slice groups it, in order |
| other → this | Story | many | A story represents it — one story in each epic that delivers it |

**Rules:** as v6's Functionality: one parent capability, one ICE, never needs and never identified by; its business intents are the ones its capability serves. New: it can be in more than one slice. It is not an issue type.
**Lives at:** the spine's `features` list and its page `feature.md`, under its capability's folder, or the holding folder `features/<id>/` until it names a capability. (These are the names after the rename story that comes next in plan 788. Until that story lands, they are `functionalities`, `functionality.md` and `functionalities/`.)

### Slice — product layer — in the tracker as an Epic (one Epic for the Slice)

**Properties:** Id and name (required); Features — its features in build order, one or more (required); Vertical — the one screen or surface a person can test end to end (required); Record — a pointer to its full record (not required). See parked point 2 for the spine fields that go.

**Links:** groups (many, in order) Feature; represented by (at most one) Epic; picked by (many) Plan.

**Rules:**
- Its features can come from any capabilities.
- Each of its features is small enough that a person can test its result.
- It holds no ICE. It is not an issue type.
- A slice with no screen or surface a person can test end to end fails the Plan's first test, and is never picked.
- It has at most one Epic. A second plan that picks it uses that Epic (see "One more point", below).

### ICE — product layer — not in the tracker

**Properties:** as in v6: Part of the product (one capability or one feature), Intent, Context, Expectation, Ready answer (computed).

**Links:** is for (one) Capability or (one) Feature; written from by (many) Story.

**Rules:** as in v6, with "functionality" read as "feature". Dropped: "a piece of work carries it". New: only a Story reads it: a Story reads its Feature's ICE and that Feature's Capability's ICE. Epic, Spike, Chore and Bug read no ICE. "A capability it needs is not done" in the ready check uses the new done rule (parked point 1).

### Plan — the thread — a file in the repo, not in the tracker

**Properties:** ID, its business intent's issue number (required); Tree — Business Intent → Slice → Epic → Story (with its Feature) → Spike, Chore, Bug, each work item with its issue and its state (required); Now, the work item being worked on (while active); Needs plans, worked out, never set by hand (not required); Status, active, done or dropped (required).

**Links:**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Business Intent | one | It is given one business intent |
| this → other | Slice | many | It picks a slice by the two tests |
| this → other | Epic | many | It creates the epic for each slice it picks, or uses the one that exists |
| this → other | Plan | many | It needs another plan |

**Rules:**
- It does three things, in this order: it is given a business intent, it picks a slice, it creates that slice's epic.
- It picks a slice by two tests: (1) the slice gives a vertical a person can test end to end; (2) of the slices that pass, the one with the most features and capabilities that serve its business intent.
- It finds the work items that exist before it creates new ones.
- It needs another plan when a feature in it belongs to a capability that needs a capability whose features are in that plan.
- As v6: the plan file and the tracker always agree; a plan that needs another cannot land first; two plans that need each other are one plan.
- A bug found after the plan is done sits under the Story that introduced it; the plan is not reopened.
- It holds no capability. A capability shows only through a feature.

### The work layer — what every work item holds

Every Epic, Story, Spike, Chore and Bug is a tracker issue labelled `work-item`, and holds: Issue (its number or key), Kind (Epic, Story, Spike, Chore or Bug), Title, and State (open or closed, as the tracker holds it). All are required. Rules for all five: a work item never needs anything and is never identified by anything; it links to no Domain and no Capability; the `*-change` plays act on work items only.

### Epic — work layer

**Properties (more):** Represents — the id of its one slice (required).

**Links:** represents (one) Slice; serves (one or more) Business Intent; holds (many) Story; created by (one) Plan.

**Rules:** It has no ICE and knows no capability. Its stories are one for each feature of its slice; when its slice gains a feature, a new story joins it. It stays open: it is not closed when its stories are done.

### Story — work layer

**Properties (more):** Represents — the id of its one feature (required); Scope of work — written when the story is made, from its feature's ICE and its capability's ICE (required; see parked point 4); Written from — the two ICE it read (required).

**Links:**

| Direction | Other kind | Count | Meaning |
|-----------|-----------|-------|---------|
| this → other | Feature | one | It represents and delivers one feature, with that feature's part of its capability |
| this → other | Epic | one | It sits in exactly one epic |
| this → other | ICE | two | It was written from its feature's ICE and that feature's capability's ICE |
| other → this | Spike, Chore, Bug | many | A child is reported for it |

**Rules:**
- One story per feature in each epic: an epic never holds two stories for one feature.
- Its feature is one of its epic's slice's features.
- Its two ICE are the ICE of its feature and the ICE of that feature's capability.
- When one of those ICE changes after the story is made, the scope is drift for the Alignment loop; it is not changed without a word.
- Closed means delivered.

### Spike — work layer

**Properties (more):** Parent — its one story (required); Started from — the suggestion it came from (required); Led to — what it led to (not required; see parked point 3).

**Links:** child of (one) Story; led to (none or many) Business Intent, Feature or Story.

**Rules:** Its parent story is closed (built) when the spike is made. It holds no ICE and links to no feature as its parent.

### Chore — work layer

**Properties (more):** Parent — its one story (required).
**Links:** child of (one) Story.
**Rules:** It holds no ICE.

### Bug — work layer

**Properties (more):** Parent — the one story whose work introduced the defect (required).
**Links:** child of (one) Story.
**Rules:** It sits under the story that introduced the defect, and so in that story's epic, even when it is found later. It holds no ICE. It is never made where nothing is built.

## Which links answer each question

| Question | Answered by | Status |
|----------|-------------|--------|
| Q1 — which types of work an intent needs | Plan picks Slice; Epic represents Slice; Story represents Feature; Spike, Chore, Bug child of Story (a Spike or Bug needs a built Story) | answered |
| Q2 — which parts it touches, change / add / remove | Business Intent has Capability and touches Domain (Touches list); Capability has Feature | answered |
| Q3 — a clash between two intents | Business Intent has Capability, marked, compared across intents | partly (as v6) |
| Q4 — what agents finished alone, where a person stepped in | Plan tree gives the closed work items; no kind yet holds who stepped in | not yet |
| Q5 — what it was drawn from | Source shows Business Intent | answered |
| Q6 — is it met | Business Intent: Proof it is met, Stage | answered |
| Q7 — its plan, end to end | Plan is given Business Intent; picks Slice; creates Epic; Epic holds Story; Story represents Feature; children of Story | answered |
| Q8 — the one ICE of a part | ICE is for Capability or Feature | answered |
| Q9 — an ICE's business intents | ICE is for Feature → has Capability → serves Business Intent | answered |
| Q10 — can work start on this ICE | ICE ready check; Capability serves Business Intent; Capability needs Capability; Capability done (point 1) | answered |
| Q11 — capabilities needed first | Capability needs Capability; Feature has one Capability | answered |
| Q12 — which capability led to this one | Capability identified by Capability | answered |
| Q13 — a feature's ICE: its story, epic, children | ICE is for Feature; Story represents Feature and is written from the ICE; Story sits in Epic; children of Story | answered |
| Q14 — a second intent changes a capability | Capability has one ICE, updated to cover both | answered |
| Q15 — which ICE agents work on for an intent | Business Intent has Capability; Capability has Feature; ICE is for each | answered |
| Q16 — a capability's domain | Capability sits in at most one Domain; Domain has Capability | answered |
| Q17 — a slice's features, in order | Slice groups Feature, in order; Feature has Capability | answered |
| Q18 — a slice's epic, stories, children | Epic represents Slice; Epic holds Story; children of Story | answered |
| Q19 — a feature's slices, story, epic | Slice groups Feature; Story represents Feature; Story sits in Epic | answered |
| Q20 — a tracker issue: which kind | Label `product` = Business Intent; label `work-item` + Kind | answered |
| Q21 — a spike: its story, suggestion, what it led to | Spike child of Story; Started from; Spike led to (point 3) | answered |
| Q22 — a work item's business intent | Story sits in Epic → Epic serves Business Intent; a child goes through its Story; Plan created the Epic | answered |
| Q23 — an epic's open and closed work | Epic holds Story; children of Story; State | answered |
| Q24 — a bug's story and epic | Bug child of the Story that introduced it; Story sits in Epic | answered |
| Q25 — the slices a plan picks, the epics it made | Plan picks Slice (two tests); Plan creates Epic; Epic represents Slice | answered |
| Q26 — a story's scope and its two ICE | Story represents Feature; Story written from ICE (two); Scope of work | answered |

## The four parked points

**1 — When a Capability is done**
**Question:** No work item carries a capability now. When does a capability count as done, for "needs" and for the ready check?
**Proposed answer:** A capability is done when every feature in it is delivered: each of its features has at least one closed Story, in any epic. It is worked out each time it is asked, never stored. A capability with no features is not done. An open Bug, Chore or Spike under a closed Story does not undo it.
**Example:** Bank — Capability "Loan application" has Features "Upload documents" (Story closed, in Epic "One-day decision") and "Fill the form" (Story open). Not done, so the ICE of "Credit decision", which needs it, is not ready. When the "Fill the form" Story closes, it is done.

**2 — Which fields of the spine's slice entry stay**
**Question:** The spine's slice entry has `id`, `slug`, `domain_ref`, `status`, `order`, `effort`, `depends_on`, `functionality_refs` and `record`. Now that the Epic is a tracker issue and the Plan picks slices, which stay?
**Proposed answer:** Keep `id`, `slug`, `functionality_refs` (renamed `feature_refs`, in build order) and `record`; add `vertical` (the screen or surface a person tests). Remove `domain_ref` (a slice takes features from any capabilities, so from any domains), and `order`, `effort` and `depends_on` (the Plan picks slices by its two tests, and what must come first comes from the capabilities' needs). Remove `status`: whether a slice is picked is shown by its Epic. The spine's `epics` list goes, as agreed. Which plays still write on the slice record (the lenses) is for the later stories of #792.
**Example:** Clinic — `{id: sl-self-booking, slug: self-booking, feature_refs: [ft-pick-a-free-slot, ft-send-a-reminder], vertical: "the booking screen", record: …}`. No order, no status; Epic "Self-booking" shows it is picked.

**3 — What a Spike "leads to"**
**Question:** Q21 asks what building a spike led to. Is that a new link, or "identified by"?
**Proposed answer:** A new link on the Spike, **led to**: none or many, to a Business Intent, a Feature or a Story. It is a record of what came out, never a dependency. Not "identified by": that link joins two things of the same kind (capability to capability, business intent to business intent), and using it here would make a product-layer kind point at a work item.
**Example:** Clinic — Spike "Do patients read SMS or email?" (child of the closed Story "Send a reminder") led to Business Intent "Patients choose how they get reminders".

**4 — The Story issue holds its scope of work**
**Question:** Does a Story's issue hold its scope of work in place of v6's ICE copy?
**Proposed answer:** Yes. The Story issue holds its scope of work, written when the story is made from its Feature's ICE and its Capability's ICE, and it names the two ICE it was written from. The ICE pages stay the source; the scope is the story's own words for its work. No other work item holds a scope from an ICE. "ICE copy" goes from the work layer.
**Example:** Shop — Story "Guest checkout": "Scope: a shopper pays by card with an email only; no account is made. Written from: ICE of Feature 'Guest checkout', ICE of Capability 'Checkout'."

**One more point, that falls out of "one epic per slice"**
**Question:** A second business intent's plan picks a slice that already has an epic. What happens?
**Proposed answer:** The plan uses that epic (it finds existing work items first), and the epic then serves both business intents. So "Epic serves Business Intent" is one or more.
**Example:** Shop — Epic "Pay without an account" serves "Sell to guests" and, later, "Shoppers pay in one minute".

## For the product owner

Please confirm the links and rules above, and say yes or change to each of the four parked points and the one more point.
