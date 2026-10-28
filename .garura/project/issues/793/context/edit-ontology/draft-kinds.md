# Draft — the kinds (stage `kinds`, steps 2–4) — #793

**What changed from the last draft (v1), at the product owner's word:**

1. The column "Tracker issue?" is now **"In the tracker as"**. It says which tracker issue represents each kind. A Business Intent is an issue labelled `product`. A Feature is represented by a **Story** issue. A Slice is represented by an **Epic** issue. Domain, Capability, Source and ICE are in the model only. A Plan is a file.
2. **Work is not a kind; it is a layer.** The "Work" row and the "Work" block are gone. Epic, Story, Spike, Chore and Bug are now kinds of their own in the **work layer**, each with its own row and its own short block.
3. **Tracker Issue is not a kind.** With the new column it adds nothing: its two labels are now in the column. It is folded in, and said so below.
4. The log lines, the list of v6 rules that are dropped, and the one version 7 log line are changed to match.

The two proposals at the end are not answered yet. They are kept as they were.

**Need:** the delivery plays work on work items, not on the spine's slices and epics. The model has two layers side by side, the product layer and the work layer, with the Plan as the thread between them. The questions are agreed (checkpoint 1). This draft says which kinds there are, what each one is, and what changes from version 6. The properties, links and rules in full come at the next stage (`links`).

## The kinds on one screen

| Kind | Layer | In the tracker as | What it is | From v6 |
|------|-------|-------------------|------------|---------|
| Business Intent | product | an issue labelled `product` | What a person wants, in their words, with its proof | changed |
| Source | product | none — model only | What a business intent was drawn from, kept as it was read | same |
| Domain | product | none — model only | A big area of the product that groups capabilities | new as a full kind (v6 named it under "Not yet defined") |
| Capability | product | none — model only | Something the product can do; has one ICE | changed |
| Feature | product | a **Story** issue (one Story for the Feature in each Epic) | One thing a person can do inside one capability; has one ICE (the old Functionality) | changed (renamed) |
| Slice | product | an **Epic** issue (one Epic for each Slice) | An ordered group of features, from any capabilities, that gives one vertical a person can test end to end | new |
| ICE | product | none — model only | The agent's intent for one capability or one feature | changed |
| Plan | thread | none — it is a file in the repo | Given one business intent, it picks a slice and creates its epic | changed |
| Epic | work | an issue labelled `work-item` | The work item that represents one Slice; holds Stories | new as a kind (was a Work type) |
| Story | work | an issue labelled `work-item` | The work item that represents one Feature and delivers it | new as a kind (was a Work type) |
| Spike | work | an issue labelled `work-item` | A proof on a built Story; a child of that Story | new as a kind (was a Work type) |
| Chore | work | an issue labelled `work-item` | Upkeep work; a child of one Story | new as a kind (was a Work type) |
| Bug | work | an issue labelled `work-item` | A defect; a child of the Story that introduced it | new as a kind (was a Work type) |

**How to read "In the tracker as":** a Feature is **not** itself an issue type. In the tracker, a Feature is represented by a Story. A Slice is not itself an issue type either. In the tracker, a Slice is represented by an Epic. The Feature and the Slice stay in the product model; the Story and the Epic are the issues that stand for them. Only two labels exist: `product` (a Business Intent, and nothing else) and `work-item` (an Epic, a Story, a Spike, a Chore or a Bug).

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
- **Work's types Story, Spike, Chore and Bug** — reused, each now as a kind of its own. The v6 kind "Work" itself is not kept as a kind; its name stays as the name of the layer.
- **Spine `slices` list** (`spine.yaml`) — reused as the place a Slice lives. Its `functionality_refs` already holds what a Slice groups (a list of feature ids).

**Clashes** — the same word meaning two things, or a v6 rule that the decisions break

| Clash | In v6 or the spine | Now | What we do |
|-------|--------------------|-----|-----------|
| "Feature" | A work type: the issue that carries its capability's ICE; one capability has one Feature | A product-layer kind: the old Functionality. In the tracker it is represented by a Story | The work type Feature goes. The word Feature now means only the product kind. Said in the log. |
| "Slice" | Spine `slices`: a delivery grouping, stamped `realized` after the lenses, with `depends_on` set by /shape-roadmap | A product-layer kind: an ordered group of features that gives one testable vertical. In the tracker it is represented by an Epic | Kept in the spine as the Slice's place. Which of its delivery fields stay is for the `links` stage. |
| "Epic" | Spine `epics`: an entry in the product model, with its own `epic.md` page, cut from a slice, with a status chain | A work-layer kind: the issue that represents one Slice; holds Stories; no ICE; knows no capability; stays open | An Epic is a tracker issue, not a model node. We propose that the spine `epics` list and the `epic.md` pages leave the model (confirm below). |
| "Work" | A kind, with five types | The name of the layer only | Work is no longer a kind. Its types Epic, Story, Spike, Chore and Bug become kinds. Said in the log. |
| "Tracker Issue" | Named under "Not yet defined" | Its two labels are in the "In the tracker as" column | Not made a kind. Its line under "Not yet defined" goes; the labels live on each kind. Said in the log. |
| "carries ICE" | Every piece of work carries one ICE; Feature and Story issues hold an ICE copy | Only a Story delivers an ICE; it reads its Feature's ICE and its Capability's ICE and writes its own scope of work. Epic, Spike, Chore and Bug carry no ICE | The link between work and ICE changes. |
| "builds" | A Story **builds** one functionality | A Story **delivers** one Feature | New verb, same idea, now with the Capability's part in it. |
| "sits under" | Spikes, Chores and Bugs sit under a functionality | They are children of one Story | The link moves from the Feature to the Story. |
| Plan tree | Business Intent → Capability → Functionality → Spike, Chore, Bug | Business Intent → Slice → Epic → Story (with its Feature) → Spike, Chore, Bug | The tree changes. |

## Step 3 — The terms

In the product owner's words.

**Nouns:** business intent, product layer, work layer, label `product`, label `work-item`, domain, capability, feature, slice, vertical, surface, screen, ICE, scope of work, plan, tree, thread, epic, story, spike, chore, bug, defect, suggestion, density, horizontal layer (database first, then services).

**Verbs:** a plan *is given* a business intent; a plan *picks* a slice; a plan *creates* an epic; a slice *groups* features, *in order*; a capability *has* features; an epic *represents* a slice; an epic *holds* stories; a story *represents* / *delivers* a feature; a story *reads* the feature's ICE and the capability's ICE and *writes* its scope; a spike, chore or bug *is a child of* / *is reported for* a story; a story *introduced* a defect; a spike *starts from* a suggestion and *leads to* more building; a work item *serves* a business intent (through its epic); *-change plays *act on* work items only.

**Two tests the plan uses to pick a slice:** (1) the slice gives a vertical outcome — a screen or a surface a person can test end to end; (2) of the slices that pass, it has the most features and capabilities that serve the business intent.

## Step 4 — The kinds

### Product layer

### Business Intent — changed

**Question:** What is it now?
**Answer:** The same as in v6: what a person or the organisation wants, in their words, with its outcome, why, proof and limits. In the tracker it is **an issue labelled `product`**. It is the only kind with that label. It still holds no ICE, and Garura never works on it directly.
**What changes:** "functionality" becomes "feature" in its text. Its Plan is given it, and the Epics its Plan creates link to it. A work item reaches it through its Epic. "What was done" links the finished work items.
**Who reads it:** person.
**Example:** Shop — "Shoppers can check out without making an account" → one tracker issue, label `product`.
**Log line:** Business Intent is an issue labelled `product`, the only kind with that label; its Plan is given it, and its Epics link to it.

### Source — same

No change. It shows what a business intent wants and is kept as it was read. In the tracker as: none.

### Domain — now a full kind

**What it is:** A big area of the product that groups capabilities. Its page is light or full; it holds no ICE. It links loosely to business intents, for search only. It is in the **model only**: in the tracker as none, never in a plan, never stops work, and **no work item links to it**. It is not a capability (a capability is something the product can do; a domain groups them).
**Who reads it:** both.
**Example:** Bank — Domain "Lending" groups Capabilities "Loan application" and "Credit decision". No tracker issue.
**Log line:** Domain moves from "Not yet defined" to a full kind, in the model only, with no link to any work item.

### Capability — changed

**What it is:** Something the product can do, in the product's own words. It serves one or more business intents, sits in at most one domain, has many features, and has exactly one ICE. It is in the **model only**: in the tracker as none, and **no work item links to it** — a Story reaches it through its Feature and reads its ICE from there.
**What changes:** v6 said a Feature issue carries its ICE ("not a piece of work (the Feature issue that carries its ICE)"); that goes. It "has many features" (was "functionalities"). The examples lose "Feature #125 carries its ICE".
**Example:** Clinic — Capability "Booking", with Features "Pick a free slot" and "Send a reminder". No tracker issue; no work item names it.
**Log line:** Capability is in the model only — no work item carries its ICE or links to it; a Story reads its ICE through its Feature.

### Feature — changed (the old Functionality, renamed)

**What it is:** One specific thing a person can do inside one capability. One capability has many features; a feature has exactly one capability. It has its **own** ICE, on the ICE's own page. It never needs anything. It lives in the product model. It can be in more than one Slice.
**In the tracker as:** a **Story**. A Feature is not itself an issue type. In each Epic that delivers it, **one Story** represents it.
**What it is NOT:** not the v6 work type "Feature" (that work type is gone); not a Story (the work item that represents and delivers it); not a Slice (a group of features).
**Who reads it:** both. /discover-capabilities writes features.
**Example:** Shop — Feature "Guest checkout" (in Capability Checkout), with its ICE "a shopper pays with an email only". In the tracker: Story "Guest checkout".
**Log line:** Functionality is renamed Feature: one thing a person can do in one capability, with its own ICE, in the product model; in the tracker it is represented by a Story, one in each Epic that delivers it.

**What the rename touches in the ontology:** "functionality" is written 46 times. The 37 in the body change; the 9 in old Log entries stay as history.

- the opening sentence (the list of kinds) and the "How it flows" paragraph;
- Q2, Q4, Q7, Q8, Q9, Q11, Q13 and Q15 — their questions or "Answered by" lines;
- Business Intent — What it is, the Touches property ("it does not name functionalities"), and the rule "agents work on the ICE of its capabilities and of their functionalities";
- ICE — What it is, Lives at (`{domain}/{capability}/{functionality}/ice.md` and the holding folder `functionalities/`), Part of the product, the relationship row "… or of one functionality", every rule, and the examples;
- Capability — the relationship "a functionality has it as its one parent" and two rules;
- the whole Functionality section, which becomes the Feature section;
- Work and Plan — every rule and the tree (the Work section becomes the five work-layer kinds);
- the Domain line under "Not yet defined".

**For the product owner to confirm (rename):** the ontology says Feature everywhere from now on. We propose that the spine names (the `functionalities` list, `functionality_refs`, `for_kind: functionality`), the page `functionality.md` and the folder `functionalities/` stay as they are for now, with a note in the ontology, and are renamed in their own issue later — the same way the spine field `depends_on` waits for its rename to `needs` (#725). Without this, this change also has to rename files in every product model.

### Slice — new

**What it is:** An ordered group of features, taken from any capabilities, that together give one vertical outcome a person can test end to end — a screen or a surface. Each feature is small enough that its result can be tested by a person. A feature can be in more than one slice. A slice lives in the product model.
**In the tracker as:** an **Epic**. A Slice is not itself an issue type. When the Plan picks it, one Epic represents it.
**What it is NOT:** not an Epic: the Slice is in the model; the Epic is the work item that represents and delivers it.
**Who reads it:** both.
**Lives at:** the spine's `slices` list (reused), with its features in order.
**Question:** How is a slice turned into work?
**Answer:** The Plan picks it (by the two tests) and creates one Epic for it. Because the Slice names its Features, the Epic gets one Story for each of them.
**Example:** Clinic — Slice "Self-booking": 1 Feature "Pick a free slot" (Capability Booking), 2 Feature "Send a reminder" (Capability Notifications). In the tracker: Epic "Self-booking".
**Log line:** Slice is new: an ordered group of features from any capabilities that gives one vertical a person can test end to end, in the product model, reusing the spine's `slices` list; in the tracker it is represented by one Epic.

### ICE — changed

**What it is:** The agent's intent for **one capability or one feature**: its own node, its own page, three parts, and the three-answer ready check. All of that stays. In the tracker as: none.
**What changes:** it is for a capability or a **feature** (was functionality). No work item "carries" it any more. A **Story** delivers its Feature's ICE: when the Story is made, it reads its Feature's ICE and that Feature's Capability's ICE, and writes its own scope of work from them. Epic, Spike, Chore and Bug carry no ICE.
**Who reads it:** agent.
**Example:** Bank — ICE of Feature "Score the application" and ICE of Capability "Credit decision" → Story "Score the application" read both and wrote its scope.
**Log line:** ICE is for one capability or one feature; no work item carries it — a Story reads its Feature's ICE and its Capability's ICE and writes its own scope of work.

### The thread

### Plan — changed

**What it is:** The thread between the product layer and the work layer. It does three things, in this order: (1) it **is given** one Business Intent; (2) it **picks** a Slice by the two tests; (3) it **creates** one Epic for that Slice — and so knows the Stories, one for each Feature of the Slice. It finds the work items that already exist before it creates new ones. Its ID is still its business intent's issue number. In the tracker as: none — it is a file in the repo.
**What changes:** its tree becomes Business Intent → Slice → Epic → Story (with its Feature) → Spike, Chore, Bug. It no longer holds capabilities; a Capability shows only through its Feature. A bug found after the plan is done sits under the Story that introduced it (was "under its functionality").
**Who reads it:** both.
**Example:** Bank — plan for "Small businesses get a loan decision in one day" → picks Slice "One-day decision" → creates Epic "One-day decision" → Stories "Upload documents" and "Score the application".
**Log line:** Plan is the thread between the two layers: given one business intent, it picks a slice and creates its epic; its tree is Business Intent → Slice → Epic → Story → Spike, Chore, Bug.

### Work layer

The work layer is the name of the layer, not a kind. It holds five kinds. Each one is a tracker issue labelled `work-item`. The *-change plays act on these kinds only.

### Epic — new as a kind

**What it is:** The work item that represents one Slice: one Epic for each Slice the Plan picks. It holds Stories. It links to the Business Intent. It knows no capability. It has **no ICE**. It is long-lived: it stays open when its work is done, and new Stories can join it.
**In the tracker as:** an issue labelled `work-item`.
**What it is NOT:** not a Slice (the Slice is in the model; the Epic is the work that delivers it); not the v6 spine entry `epics` with its `epic.md` page (see proposal 1).
**Who reads it:** both.
**Example:** Clinic — Epic "Self-booking", for Slice "Self-booking", holds Stories "Pick a free slot" and "Send a reminder".
**Log line:** Epic is a kind in the work layer: it represents one slice, holds stories, links to the business intent, has no ICE and stays open.

### Story — new as a kind

**What it is:** The work item that represents one Feature and delivers it, and with it that Feature's part of its Capability. Its scope of work is written from the Feature's ICE and the Capability's ICE. It sits in exactly one Epic. There is one Story for each Feature in each Epic.
**In the tracker as:** an issue labelled `work-item`.
**What it is NOT:** not the Feature (the Feature is in the model; the Story stands for it in the tracker).
**Who reads it:** both.
**Example:** Shop — Story "Guest checkout" delivers Feature "Guest checkout", in Epic "Pay without an account".
**Log line:** Story is a kind in the work layer: it represents one feature and delivers it, one story per feature in each epic, and writes its scope from its feature's and capability's ICE.

### Spike — new as a kind

**What it is:** A prototype or proof on something already built, started from a suggestion, that leads to more building. It is a child of one Story, and it comes only after that Story is built. No ICE.
**In the tracker as:** an issue labelled `work-item`.
**Who reads it:** both.
**Example:** Bank — Spike "Try a faster scoring model", child of the built Story "Score the application".
**Log line:** Spike is a kind in the work layer: a child of one story, only after that story is built; no ICE.

### Chore — new as a kind

**What it is:** Upkeep work for a Story. It is a child of one Story. No ICE.
**In the tracker as:** an issue labelled `work-item`.
**Who reads it:** both.
**Example:** Clinic — Chore "Update the reminder message library", child of Story "Send a reminder".
**Log line:** Chore is a kind in the work layer: upkeep work, a child of one story; no ICE.

### Bug — new as a kind

**What it is:** A defect. It is a child of the Story whose work introduced it — so it sits in that Story's Epic, even when it is reported later. No ICE.
**In the tracker as:** an issue labelled `work-item`.
**Who reads it:** both.
**Example:** Shop — Bug "Card fails on mobile", child of Story "Guest checkout".
**Log line:** Bug is a kind in the work layer: a defect, a child of the story that introduced it; no ICE.

### Not a kind any more, or not made a kind

- **Work** — v6 had it as a kind with five types. It is now only the name of the layer. Its types Epic, Story, Spike, Chore and Bug are kinds. **Feature is no longer a work type**; it is a product-layer kind, represented in the tracker by a Story.
- **Tracker Issue** — v6 named it under "Not yet defined". It is not made a kind: once the "In the tracker as" column says, for each kind, which issue represents it and with which label (`product` or `work-item`), a Tracker Issue kind adds nothing more. Its line under "Not yet defined" goes. The tracker can still be GitHub, Jira, Azure, Linear or a custom one; that is a fact about the tracker, not a kind.

**Log line:** Work is no longer a kind but the name of the layer, and its types become kinds; Tracker Issue is not made a kind — its labels live on each kind as "In the tracker as".

**v6 rules that are dropped** — said plainly in the log:

- "Work" as a kind with types — gone: Work is the name of the layer; Epic, Story, Spike, Chore and Bug are kinds.
- "One capability has one Feature." — gone: the Feature work type is gone.
- "A Feature carries its capability's ICE." — gone: no work item carries a Capability's ICE.
- "One functionality has exactly one Story." — replaced by "one Story per Feature **in each Epic**": when a later Slice includes a Feature again, its Epic gets its own Story for that Feature.
- "Spikes, Bugs and Chores sit under a functionality and carry its ICE. A Bug always sits under a functionality." — replaced: they are children of one Story and carry no ICE; a Bug sits under the Story that introduced the defect.
- "Each piece of work carries one ICE" and "It reaches its part and its business intents through its ICE." — replaced: a Story reaches its Feature directly and its Business Intent through its Epic; a child reaches all of them through its Story.
- "Business Intent → Feature → Story → Spike, Chore or Bug" (the tracker parent order) — replaced by Business Intent → Epic → Story → Spike, Chore or Bug.
- "Tracker Issue" under "Not yet defined" — gone: its labels are on each kind.

## The one log line for version 7

Version 6 → 7, one dated line, made from the lines above:

> 2026-10-22 — v7 (#793, plan #788, with the product owner): the model has two layers with the Plan as the thread, and each kind says what it is in the tracker as. Product layer: Business Intent (an issue labelled `product`, the only kind with that label), Source, Domain, Capability, ICE, Feature (Functionality renamed; in the tracker represented by a Story) and the new Slice (an ordered group of features from any capabilities that gives one vertical a person can test; in the tracker represented by an Epic); Feature and Slice are not issue types; Source, Domain, Capability and ICE are model only, and Domain and Capability have no link to any work item. Work layer: Work is no longer a kind but the name of the layer, and Epic, Story, Spike, Chore and Bug are kinds, each an issue labelled `work-item`; Feature is no longer a work type. A Plan (a file) is given one business intent, picks a slice and creates one epic for it; an Epic represents one slice, holds stories, links to the business intent, has no ICE and stays open; a Story represents and delivers one feature, one per feature in each epic, and writes its scope from its feature's and capability's ICE; Spikes, Chores and Bugs are children of one story and carry no ICE — a Spike only after its story is built, a Bug under the story that introduced the defect. Domain becomes a full kind; Tracker Issue is not made a kind, its labels live on each kind. Dropped: Work as a kind, "one capability has one Feature", "a Feature carries its capability's ICE", "one functionality has exactly one Story", "Spikes, Bugs and Chores sit under a functionality".

## Left for the `links` stage

These are links and rules, not kinds. They are listed so they are not lost; none of them reopens a decision.

- When is a Capability "done" (for "needs"), now that no work item carries it? For example: when the Story of each of its features is done.
- Which fields of the spine `slices` entry stay (its `realized` status, its lenses, its `depends_on` from /shape-roadmap).
- What a Spike "leads to" (a new Story, Feature or Business Intent): a new link, or "identified by".
- Whether the Story's issue holds its scope of work in place of the v6 ICE copy.
- The "represents" links: Story represents Feature (one in each Epic), Epic represents Slice (one for each picked Slice).

## For the product owner

Please confirm the kinds: thirteen kinds in two layers, with the Plan as the thread. Product layer: Business Intent, Source, Domain, Capability, Feature, Slice, ICE. Work layer: Epic, Story, Spike, Chore, Bug. Feature is the old Functionality and is represented in the tracker by a Story; Slice is new and is represented by an Epic. Work is the name of the layer, not a kind; Tracker Issue is folded into the "In the tracker as" column. Two proposals need your yes or no:

1. **Epic leaves the model.** The spine's `epics` list and the `epic.md` pages leave the product model, because an Epic is now a tracker issue that knows no capability. Example: Clinic — Epic "Self-booking" is issue #350, label `work-item`, and the plan file names it; the spine no longer lists it.
2. **The spine and file names wait.** The ontology says Feature from now on, but the spine names, `functionality.md` and the `functionalities/` folder are renamed in a later issue. Example: Shop — Feature "Guest checkout" still lives at `orders/checkout/guest-checkout/functionality.md` until that issue is done.
