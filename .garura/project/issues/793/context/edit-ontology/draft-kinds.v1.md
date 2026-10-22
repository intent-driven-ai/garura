# Draft — the kinds (stage `kinds`, steps 2–4) — #793

**Need:** the delivery plays work on work items, not on the spine's slices and epics. The model has two layers side by side, the product layer and the work layer, with the Plan as the thread between them. The questions are agreed (checkpoint 1). This draft says which kinds there are, what each one is, and what changes from version 6. The properties, links and rules in full come at the next stage (`links`).

## The kinds on one screen

| Kind | Layer | Tracker issue? | What it is | From v6 |
|------|-------|----------------|------------|---------|
| Business Intent | product | yes, label `product` — the only one in the product layer | What a person wants, in their words, with its proof | changed |
| Source | product | no | What a business intent was drawn from, kept as it was read | same |
| Domain | product | no — model only | A big area of the product that groups capabilities | new as a full kind (v6 named it under "Not yet defined") |
| Capability | product | no — model only | Something the product can do; has one ICE | changed |
| Feature | product | no — model only | One thing a person can do inside one capability; has one ICE (the old Functionality) | changed (renamed) |
| Slice | product | no — model only | An ordered group of features, from any capabilities, that gives one vertical a person can test end to end | new |
| ICE | product | no — model only | The agent's intent for one capability or one feature | changed |
| Plan | thread | no — a file in the repo | Given one business intent, it picks a slice and creates its epic | changed |
| Work | work | yes, label `work-item` — every work item | A tracked piece of work: Epic, Story, Spike, Chore or Bug | changed |
| Tracker Issue | both | — it is the issue itself | One issue in the team's tracker, labelled `product` or `work-item` | new as a full kind (v6 named it under "Not yet defined") |

The picture, in five lines:

1. A Plan is given one Business Intent; it picks a Slice; it creates one Epic for that Slice.
2. An Epic holds Stories; each Story sits inside exactly one Epic.
3. A Story delivers one Feature, and with it that Feature's part of its Capability.
4. A Spike, Chore or Bug is a child of one Story, and reaches the Feature, the Epic and the Business Intent through it.
5. Domains and Capabilities are in the product model only; no work item links to them.

## Step 2 — What we reuse, and where it clashes

**Reused as they are**

- **Source** — all of it. Nothing in this need touches it.
- **Business Intent** — its page, its properties, its stages, its Touches list and its rules. Only the words about functionalities, the tracker label and the new links to the Plan and the Epic change.
- **ICE** — its own node, its own page, its three parts (Intent, Context, Expectation), and its three-answer ready check (ADR 047). Only what it is *for* (a capability or a feature) and who reads it change.
- **Capability** — its page, its one ICE, "needs" and "identified by" between capabilities only, at most one domain.
- **Functionality** — all of it, under the new name Feature: one parent capability, one ICE, no "needs", the holding folder.
- **Plan** — its file, its ID (the business intent's issue number), Now, Needs plans, Status, and the rule that the plan file and the tracker agree.
- **Work** — the kind, and the types Story, Spike, Chore and Bug.
- **Spine `slices` list** (`spine.yaml`) — reused as the place a Slice lives. Its `functionality_refs` already holds what a Slice groups (a list of feature ids).

**Clashes** — the same word meaning two things, or a v6 rule that the decisions break

| Clash | In v6 or the spine | Now | What we do |
|-------|--------------------|-----|-----------|
| "Feature" | A work type: the issue that carries its capability's ICE; one capability has one Feature | A product-layer kind: the old Functionality | The work type Feature goes. The word Feature now means only the product kind. Said in the log. |
| "Slice" | Spine `slices`: a delivery grouping, stamped `realized` after the lenses, with `depends_on` set by /shape-roadmap | A product-layer kind: an ordered group of features that gives one testable vertical | Kept in the spine as the Slice's place. Which of its delivery fields stay is for the `links` stage. |
| "Epic" | Spine `epics`: an entry in the product model, with its own `epic.md` page, cut from a slice, with a status chain | A work item in the tracker; holds Stories; no ICE; knows no capability; stays open | An Epic is a tracker issue, not a model node. We propose that the spine `epics` list and the `epic.md` pages leave the model (confirm below). |
| "carries ICE" | Every piece of work carries one ICE; Feature and Story issues hold an ICE copy | Only a Story delivers an ICE; it reads its Feature's ICE and its Capability's ICE and writes its own scope of work. Epic, Spike, Chore and Bug carry no ICE | The Work–ICE link changes. |
| "builds" | A Story **builds** one functionality | A Story **delivers** one Feature | New verb, same idea, now with the Capability's part in it. |
| "sits under" | Spikes, Chores and Bugs sit under a functionality | They are children of one Story | The link moves from the Feature to the Story. |
| Plan tree | Business Intent → Capability → Functionality → Spike, Chore, Bug | Business Intent → Slice → Epic → Story (with its Feature) → Spike, Chore, Bug | The tree changes. |

## Step 3 — The terms

In the product owner's words.

**Nouns:** business intent, product layer, work layer, label `product`, label `work-item`, domain, capability, feature, slice, vertical, surface, screen, ICE, scope of work, plan, tree, thread, epic, story, spike, chore, bug, defect, suggestion, density, horizontal layer (database first, then services).

**Verbs:** a plan *is given* a business intent; a plan *picks* a slice; a plan *creates* an epic; a slice *groups* features, *in order*; a capability *has* features; an epic *holds* stories; a story *represents* / *delivers* a feature; a story *reads* the feature's ICE and the capability's ICE and *writes* its scope; a spike, chore or bug *is a child of* / *is reported for* a story; a story *introduced* a defect; a spike *starts from* a suggestion and *leads to* more building; a work item *serves* a business intent (through its epic); *-change plays *act on* work items only.

**Two tests the plan uses to pick a slice:** (1) the slice gives a vertical outcome — a screen or a surface a person can test end to end; (2) of the slices that pass, it has the most features and capabilities that serve the business intent.

## Step 4 — The kinds

### Business Intent — changed

**Question:** What is it now?
**Answer:** The same as in v6: what a person or the organisation wants, in their words, with its outcome, why, proof and limits. It is the **only kind in the product layer that is a tracker issue**, with the label `product`. It still holds no ICE, and Garura never works on it directly.
**What changes:** "functionality" becomes "feature" in its text. Its Plan is given it, and the Epics its Plan creates link to it. A work item reaches it through its Epic. "What was done" links the finished work items.
**Who reads it:** person.
**Example:** Shop — "Shoppers can check out without making an account" → one tracker issue, label `product`.
**Log line:** Business Intent is the only product-layer kind that is a tracker issue (label `product`); its Plan is given it, and its Epics link to it.

### Source — same

No change. It shows what a business intent wants and is kept as it was read.

### Domain — now a full kind

**What it is:** A big area of the product that groups capabilities. Its page is light or full; it holds no ICE. It links loosely to business intents, for search only. It is in the **model only**: it is never a tracker issue, never in a plan, never stops work, and **no work item links to it**. It is not a capability (a capability is something the product can do; a domain groups them).
**Who reads it:** both.
**Example:** Bank — Domain "Lending" groups Capabilities "Loan application" and "Credit decision". No tracker issue.
**Log line:** Domain moves from "Not yet defined" to a full kind, in the model only, with no link to any work item.

### Capability — changed

**What it is:** Something the product can do, in the product's own words. It serves one or more business intents, sits in at most one domain, has many features, and has exactly one ICE. It is in the **model only**: it is not a tracker issue, and **no work item links to it** — a Story reaches it through its Feature and reads its ICE from there.
**What changes:** v6 said a Feature issue carries its ICE ("not a piece of work (the Feature issue that carries its ICE)"); that goes. It "has many features" (was "functionalities"). The examples lose "Feature #125 carries its ICE".
**Example:** Clinic — Capability "Booking", with Features "Pick a free slot" and "Send a reminder". No tracker issue; no work item names it.
**Log line:** Capability is in the model only — no work item carries its ICE or links to it; a Story reads its ICE through its Feature.

### Feature — changed (the old Functionality, renamed)

**What it is:** One specific thing a person can do inside one capability. One capability has many features; a feature has exactly one capability. It has its **own** ICE, on the ICE's own page. It never needs anything. It is in the **model only**. It can be in more than one Slice. In each Epic that delivers it, **one Story** delivers it.
**What it is NOT:** not the v6 work type "Feature" (that work type is gone); not a Story (the work item that delivers it); not a Slice (a group of features).
**Who reads it:** both. /discover-capabilities writes features.
**Example:** Shop — Feature "Guest checkout" (in Capability Checkout), with its ICE "a shopper pays with an email only".
**Log line:** Functionality is renamed Feature: one thing a person can do in one capability, with its own ICE, in the model only.

**What the rename touches in the ontology:** "functionality" is written 46 times. The 37 in the body change; the 9 in old Log entries stay as history.

- the opening sentence (the list of kinds) and the "How it flows" paragraph;
- Q2, Q4, Q7, Q8, Q9, Q11, Q13 and Q15 — their questions or "Answered by" lines;
- Business Intent — What it is, the Touches property ("it does not name functionalities"), and the rule "agents work on the ICE of its capabilities and of their functionalities";
- ICE — What it is, Lives at (`{domain}/{capability}/{functionality}/ice.md` and the holding folder `functionalities/`), Part of the product, the relationship row "… or of one functionality", every rule, and the examples;
- Capability — the relationship "a functionality has it as its one parent" and two rules;
- the whole Functionality section, which becomes the Feature section;
- Work and Plan — every rule and the tree;
- the Domain line under "Not yet defined".

**For the product owner to confirm (rename):** the ontology says Feature everywhere from now on. We propose that the spine names (the `functionalities` list, `functionality_refs`, `for_kind: functionality`), the page `functionality.md` and the folder `functionalities/` stay as they are for now, with a note in the ontology, and are renamed in their own issue later — the same way the spine field `depends_on` waits for its rename to `needs` (#725). Without this, this change also has to rename files in every product model.

### Slice — new

**What it is:** An ordered group of features, taken from any capabilities, that together give one vertical outcome a person can test end to end — a screen or a surface. Each feature is small enough that its result can be tested by a person. A feature can be in more than one slice. A slice is in the product layer and in the **model only**: it is not a tracker issue. It is not an Epic: the Epic is the work item that delivers one picked Slice.
**Who reads it:** both.
**Lives at:** the spine's `slices` list (reused), with its features in order.
**Question:** How is a slice turned into work?
**Answer:** The Plan picks it (by the two tests) and creates one Epic for it. Because the Slice names its Features, the Epic gets one Story for each of them.
**Example:** Clinic — Slice "Self-booking": 1 Feature "Pick a free slot" (Capability Booking), 2 Feature "Send a reminder" (Capability Notifications). No tracker issue.
**Log line:** Slice is new: an ordered group of features from any capabilities that gives one vertical a person can test end to end, in the model only; it reuses the spine's `slices` list.

### ICE — changed

**What it is:** The agent's intent for **one capability or one feature**: its own node, its own page, three parts, and the three-answer ready check. All of that stays.
**What changes:** it is for a capability or a **feature** (was functionality). No work item "carries" it any more. A **Story** delivers its Feature's ICE: when the Story is made, it reads its Feature's ICE and that Feature's Capability's ICE, and writes its own scope of work from them. Epic, Spike, Chore and Bug carry no ICE.
**Who reads it:** agent.
**Example:** Bank — ICE of Feature "Score the application" and ICE of Capability "Credit decision" → Story "Score the application" read both and wrote its scope.
**Log line:** ICE is for one capability or one feature; no work item carries it — a Story reads its Feature's ICE and its Capability's ICE and writes its own scope of work.

### Plan — changed

**What it is:** The thread between the product layer and the work layer. It does three things, in this order: (1) it **is given** one Business Intent; (2) it **picks** a Slice by the two tests; (3) it **creates** one Epic for that Slice — and so knows the Stories, one for each Feature of the Slice. It finds the work items that already exist before it creates new ones. Its ID is still its business intent's issue number, and it still lives in the repo.
**What changes:** its tree becomes Business Intent → Slice → Epic → Story (with its Feature) → Spike, Chore, Bug. It no longer holds capabilities; a Capability shows only through its Feature. A bug found after the plan is done sits under the Story that introduced it (was "under its functionality").
**Who reads it:** both.
**Example:** Bank — plan for "Small businesses get a loan decision in one day" → picks Slice "One-day decision" → creates Epic "One-day decision" → Stories "Upload documents" and "Score the application".
**Log line:** Plan is the thread between the two layers: given one business intent, it picks a slice and creates its epic; its tree is Business Intent → Slice → Epic → Story → Spike, Chore, Bug.

### Work — changed

**What it is:** A tracked piece of work, in the **work layer**. Every work item is a tracker issue, label `work-item`. The *-change plays act on work items only. There are five types:

| Type | What it is | Holds or sits in | ICE |
|------|-----------|------------------|-----|
| **Epic** | The work item for one picked Slice. It holds Stories. It links to the Business Intent. It knows no capability. It is long-lived: it stays open when its work is done, and new Stories can join it. | holds Stories | none |
| **Story** | Delivers one Feature, and with it that Feature's part of its Capability. Its scope of work is written from the Feature's ICE and the Capability's ICE. One Story per Feature in each Epic. | sits in exactly one Epic | reads both, delivers the Feature's |
| **Spike** | A prototype or proof on something already built, started from a suggestion, that leads to more building. It comes only after its Story is built. | child of one built Story | none |
| **Chore** | Upkeep work for a Story. | child of one Story | none |
| **Bug** | A defect, under the Story whose work introduced it — so it sits under that Story's Epic. | child of one Story | none |

**What it is NOT:** **Feature is no longer a work type**; it is a product-layer kind. An Epic is not a Slice (the Slice is in the model; the Epic is the work that delivers it).
**Who reads it:** both.
**Example:** Shop — Epic "Pay without an account" → Story "Guest checkout" (delivers Feature "Guest checkout") → Bug "Card fails on mobile". Every one is a tracker issue, label `work-item`.
**Log line:** Work types are Epic, Story, Spike, Chore and Bug; Feature is no longer a work type. An Epic is the work item for one slice, holds stories, links to the business intent, has no ICE and stays open; a Story delivers one feature, one story per feature in each epic; Spikes, Chores and Bugs are children of one story — a Spike only after its story is built, a Bug under the story that introduced the defect.

**v6 rules that are dropped** — said plainly in the log:

- "One capability has one Feature." — gone: the Feature work type is gone.
- "A Feature carries its capability's ICE." — gone: no work item carries a Capability's ICE.
- "One functionality has exactly one Story." — replaced by "one Story per Feature **in each Epic**": when a later Slice includes a Feature again, its Epic gets its own Story for that Feature.
- "Spikes, Bugs and Chores sit under a functionality and carry its ICE. A Bug always sits under a functionality." — replaced: they are children of one Story and carry no ICE; a Bug sits under the Story that introduced the defect.
- "Each piece of work carries one ICE" and "It reaches its part and its business intents through its ICE." — replaced: a Story reaches its Feature directly and its Business Intent through its Epic; a child reaches all of them through its Story.
- "Business Intent → Feature → Story → Spike, Chore or Bug" (the tracker parent order) — replaced by Business Intent → Epic → Story → Spike, Chore or Bug.

### Tracker Issue — now a full kind

**What it is:** One issue in the team's tracker (GitHub, Jira, Azure, Linear, or a custom one). It has one of two labels, so each layer can be filtered on its own: **`product`** — always a Business Intent; **`work-item`** — an Epic, a Story, a Spike, a Chore or a Bug. No Domain, Capability, Feature or Slice is ever a tracker issue.
**Who reads it:** both.
**Example:** Shop — issue "Sell to guests" → `product`, Business Intent. Issue "Card fails on mobile" → `work-item`, Bug.
**Log line:** Tracker Issue moves from "Not yet defined" to a full kind, labelled `product` (Business Intent only) or `work-item` (every work item).

## The one log line for version 7

Version 6 → 7, one dated line, made from the lines above:

> 2026-10-22 — v7 (#793, plan #788, with the product owner): the model has two layers with the Plan as the thread. Product layer: Business Intent (the only one that is a tracker issue, label `product`), Source, Domain, Capability, Feature (Functionality renamed) and the new Slice (an ordered group of features from any capabilities that gives one vertical a person can test), all but the Business Intent in the model only; Domain and Capability have no link to any work item. Work layer: Epic, Story, Spike, Chore, Bug, each a tracker issue (label `work-item`); Feature is no longer a work type. A Plan is given one business intent, picks a slice and creates one epic for it; an Epic holds stories, links to the business intent, has no ICE and stays open; a Story delivers one feature, one per feature in each epic, and writes its scope from its feature's and capability's ICE; Spikes, Chores and Bugs are children of one story and carry no ICE — a Spike only after its story is built, a Bug under the story that introduced the defect. Domain and Tracker Issue become full kinds. Dropped: "one capability has one Feature", "a Feature carries its capability's ICE", "one functionality has exactly one Story", "Spikes, Bugs and Chores sit under a functionality".

## Left for the `links` stage

These are links and rules, not kinds. They are listed so they are not lost; none of them reopens a decision.

- When is a Capability "done" (for "needs"), now that no work item carries it? For example: when the Story of each of its features is done.
- Which fields of the spine `slices` entry stay (its `realized` status, its lenses, its `depends_on` from /shape-roadmap).
- What a Spike "leads to" (a new Story, Feature or Business Intent): a new link, or "identified by".
- Whether the Story's issue holds its scope of work in place of the v6 ICE copy.

## For the product owner

Please confirm the kinds: ten kinds, two layers, the Plan as the thread; Feature is the old Functionality; Slice is new; Epic is a work item, not a model node. Two proposals need your yes or no:

1. **Epic leaves the model.** The spine's `epics` list and the `epic.md` pages leave the product model, because an Epic is now a tracker issue that knows no capability. Example: Clinic — Epic "Self-booking" is issue #350, label `work-item`, and the plan file names it; the spine no longer lists it.
2. **The spine and file names wait.** The ontology says Feature from now on, but the spine names, `functionality.md` and the `functionalities/` folder are renamed in a later issue. Example: Shop — Feature "Guest checkout" still lives at `orders/checkout/guest-checkout/functionality.md` until that issue is done.
