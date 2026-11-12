# Draft — properties, links and rules: the feature's state (issue 1056)

Stage: links (steps 5 and 6 of the ontology method). It rests on the questions agreed at the first checkpoint (Q10, Q50, Q52 changed; Q64 to Q71 new) and the kinds agreed at the second (no new kind; Feature, Capability, ICE, Slice, Plan and Feature issue change, with the whole-model rule; Domain stays as it is).

## Opening

This draft gives the exact words that change in the product ontology, each shown as the old text (lines that start with "-") and the new text (lines that start with "+"). You approve the words. Nothing here is still open, so you do not answer a question: you say yes, or you name a change. When you say yes, the next stage writes these words into the ontology as version 18, adds the log line and runs the ontology's check.

## What does not change

- No relationship changes, except the meaning line of "Plan → Feature issue".
- The kinds Domain, Business Intent, Source, Epic, Story, Spike, Chore and Bug keep every word.
- Every rule not shown below keeps every word.
- The questions section (Q10, Q50, Q52, and the new Q64 to Q71 with their "Answered by" lines) is written at the next stage, from the agreed questions.

---

## 1. The top of the ontology

### The whole-model rule

```diff
- The spine has no `epics` list, and no part of the model holds a work status: whether a slice is in progress is read from the plan files.
+ The spine has no `epics` list. Only a feature holds a state: the `status` of its spine entry, one of Unplanned, Planned, In progress, Completed or Dropped. No other part holds one, nothing rolls up from features, and the state names no plan, no tracker issue and no decision record. Whether a slice is in progress is still read from the plan files.
```

### The flow line ("How it flows")

```diff
- has one **Epic**, and finds or files the **Feature issue** of each Feature of its Slices that is not yet built, and writes nothing in the evals folder
+ has one **Epic**, and finds or files the **Feature issue** of each Feature of its Slices that is not Completed and not Dropped, sets each Feature it takes in to Planned, and writes nothing in the evals folder
```

```diff
- → a person closes the Feature issue, and its Feature is built →
+ → a person closes the Feature issue, and its Feature's state becomes Completed: it is built →
```

### Link 1 of "The links, in five lines"

```diff
- it has one Epic, and finds or files the Feature issue of each Feature of its Slices that is not yet built (three actions, in this order).
+ it has one Epic, and finds or files the Feature issue of each Feature of its Slices that is not Completed and not Dropped (three actions, in this order).
```

---

## 2. Feature

### What it is (one sentence added after "It can be in more than one slice and in more than one plan.")

```diff
+ It records its own state, one of five: Unplanned, Planned, In progress, Completed or Dropped. It is the only kind in the model that has a state.
```

### Lives at

```diff
- **Lives at:** the spine's `features` list and its page `feature.md` — under its capability's folder, or the holding folder `features/<id>/` until it names a capability.
+ **Lives at:** the spine's `features` list and its page `feature.md` — under its capability's folder, or the holding folder `features/<id>/` until it names a capability. Its state is the `status` of its spine entry, and only there: its page does not show it.
```

### Properties

```diff
- | Built | Whether its Feature issue is closed as completed — worked out each time it is asked, through the tracker tool, never stored | no — it is computed |
+ | Status | Its state, one of five: **Unplanned** (it is in the model, and no plan holds it), **Planned** (a plan holds it, and no work on it has started), **In progress** (some of its work is done, and some is open), **Completed** (it is built), **Dropped** (it will not be built). Stored on its spine entry only. Each state has one named step that sets it (see its rules and states) | yes |
```

### Rules

The rule on "built" is replaced by six rules:

```diff
- It is built when a person closes its Feature issue as completed. Closed Stories do not build it. A built feature counts complete in every slice and every plan that holds it.
+ It records its own state, `status`, on its spine entry and nowhere else. Every feature has a state. A play that adds a feature to the model sets Unplanned.
+ Only `/start-work` sets In progress, when work on the feature first starts: a start of its Feature issue, of a Story inside it, or of a Bug or a Spike under that Story. A start of the plan, or of a Chore under the plan's epic, changes nothing. Design, slicing and planning are never work. When the feature is Unplanned, `/start-work` says so, goes on only on the person's yes, and records that the work started with no plan; it never blocks. A Completed feature stays Completed when more work starts on it.
+ It is built when its state is Completed. It becomes Completed when its Feature issue closes as completed (the Feature issue's rules say how), and one time only, through the model clean-up the person confirms, for a feature built before Feature issues existed. Closed Stories do not build it. A Completed feature counts complete in every slice and every plan that holds it.
+ A person drops it. At that moment a check looks at what is known — whether it is Completed, whether its work started, and whether its work sits on open branches that may be idle — and warns the person. The check never blocks the drop and adds no step. A Dropped feature stays out of every new slice and every new plan until a person brings it back in `/reshape-plan`, which sets it to Unplanned.
+ When it leaves a plan without being dropped, the Plan's rules say its new state. Nothing else moves it back.
+ Its state is written on the branch of the work that sets it, and main shows it when that work lands. Its state names no plan, no tracker issue and no decision record. Its capability, its domain and its business intents have no state, and nothing rolls up from it.
```

### States (a new section, after the rules)

```diff
+ **States**
+
+ Unplanned → Planned, when a plan takes it in (`/shape-plan` when it makes the plan, `/reshape-plan` when it adds the feature later) → In progress, when work on it first starts (`/start-work`) → Completed, when its Feature issue closes as completed. Unplanned → In progress, when work starts with no plan, on the person's yes (`/start-work`). Planned → Unplanned, when it leaves its last plan before work started (`/reshape-plan`). Completed → In progress, when a person opens its Feature issue again (`/reshape-plan`). Any state → Dropped, when a person drops it; a check warns and never blocks. Dropped → Unplanned, when a person brings it back (`/reshape-plan`). One time only, the model clean-up sets Completed on a feature built before Feature issues existed, after the person confirms the list.
```

### Examples

```diff
- The shop owner finished #122, so it is built, and it counts complete in plan #120 and in plan #150.
+ The shop owner finished #122, so its state is Completed, and it counts complete in plan #120 and in plan #150. Its spine entry holds `status: Completed`; its page does not show it.
```

```diff
- Its Stories are closed, but the clinic manager has not finished #343, so it is not built.
+ Its Stories are closed, but the clinic manager has not finished #343, so its state is In progress, not Completed.
```

```diff
- Its Feature issue #53 is closed as completed, so it is built, and Slice "Upload once", shaped later, left it out.
+ Its Feature issue #53 is closed as completed, so its state is Completed. Slice "Upload once", shaped later, read that state in the model and left it out.
```

---

## 3. Capability

### Properties

```diff
- | Done | Whether every feature in it is built — worked out each time it is asked, never stored | no — it is computed |
+ | Done | Whether every feature in it is Completed or Dropped — worked out each time it is asked, from its features' states, never stored. It is not a state: a capability has none | no — it is computed |
```

### Rules

```diff
- It is done when every feature in it is built: each of its features has its Feature issue closed as completed. A capability with no features is not done. An open Story, Bug, Chore or Spike inside a closed Feature issue does not undo it.
+ It is done when every feature in it is Completed or Dropped, read from the features' states in the model. A capability with no features is not done. An open Story, Bug, Chore or Spike inside a closed Feature issue does not undo it.
+ It has no state of its own. Nothing rolls up into it from its features.
```

### Example

```diff
- Has the Features "Upload documents" (built: its Feature issue #53 is closed as completed, under Epic "One-day decision") and "Fill the form" (its Feature issue is open, although its one Story is closed). Not done, so the ICE of "Credit decision", which needs it, is not ready. When a person finishes the Feature issue of "Fill the form" through `/reshape-plan`, it is done.
+ Has the Features "Upload documents" (Completed: its Feature issue #53 is closed as completed, under Epic "One-day decision") and "Fill the form" (In progress: its Feature issue is open, although its one Story is closed). Not done, so the ICE of "Credit decision", which needs it, is not ready. When a person finishes the Feature issue of "Fill the form" through `/reshape-plan`, "Fill the form" is Completed and the capability is done.
```

---

## 4. ICE (wording only)

### Rules (the ready check)

```diff
- The ready check gives one of three answers. For a feature's ICE, "its capability" is the parent capability. A needed capability is done when every feature in it is built.
+ The ready check gives one of three answers. For a feature's ICE, "its capability" is the parent capability. A needed capability is done when every feature in it is Completed or Dropped.
```

### Example

```diff
- and needs "Loan application", which is not done (its Feature "Fill the form" is not built: its Feature issue is open).
+ and needs "Loan application", which is not done (its Feature "Fill the form" is In progress).
```

---

## 5. Slice

### What it is

```diff
- It takes in only features that are not yet built.
+ It takes in only features that are not Completed and not Dropped.
```

### Rules

```diff
- It takes in only features that are not yet built. To know which are built, `/design-slice` reads the state of each feature's Feature issue through the tracker tool. A feature built after it joined stays in the slice and counts complete.
+ It takes in only features that are not Completed and not Dropped. `/design-slice` reads each feature's state in the model, with no search in the tracker. A feature that becomes Completed after it joined stays in the slice and counts complete.
```

### Examples

```diff
- When "Cancel online" was shaped later, "Pick a free slot" was already built (its Feature issue was closed as completed), so `/design-slice` left it out of that slice.
+ When "Cancel online" was shaped later, "Pick a free slot" was already Completed in the model, so `/design-slice` left it out of that slice.
```

```diff
- When it was shaped, `/design-slice` read the Feature issue of "Upload documents" through the tracker tool: it was closed as completed, so "Upload documents" was built, and the slice left it out.
+ When it was shaped, `/design-slice` read the state of "Upload documents" in the model: it was Completed, so the slice left it out.
```

---

## 6. Plan

### Relationships

```diff
- | this → other | Feature issue | many | It finds or files the Feature issue of each feature of its slices that is not yet built, and shows it in its tree |
+ | this → other | Feature issue | many | It finds or files the Feature issue of each feature of its slices that is not Completed and not Dropped, and shows it in its tree |
```

### Rules

```diff
- it has one epic, which the plan play creates once, and it finds or files the Feature issue of each feature of its slices that is not yet built.
+ it has one epic, which the plan play creates once, and it finds or files the Feature issue of each feature of its slices that is not Completed and not Dropped.
```

```diff
- Many plans can hold one feature, and it still has one Feature issue. The plan play adds only features that are not yet built. A feature built later stays in the plan and counts complete.
+ Many plans can hold one feature, and it still has one Feature issue. The plan play adds only features that are not Completed and not Dropped, read from each feature's state in the model, with no search in the tracker. A feature that becomes Completed later stays in the plan and counts complete.
+ The play that takes a feature into a plan sets it to Planned when it is Unplanned: the plan play when it makes the plan, `/reshape-plan` when it adds the feature later. A feature that is already Planned or In progress keeps its state.
+ When a feature leaves the plan without being dropped — a person moves it out, or sets the whole plan to Dropped — `/reshape-plan` sets its state in the list the person approves: Unplanned when no other plan holds it; it stays Planned when another plan still holds it; it stays In progress when its work has started.
```

```diff
- They are never written in the product model's index or on its pages, and no product-layer kind holds them. A part that `/reshape-plan` adds to the model (a new feature, its thin ICE, its place in a slice) is a product fact, not an operational one.
+ They are never written in the product model's index or on its pages, and no product-layer kind holds them. A part that `/reshape-plan` adds to the model (a new feature, its thin ICE, its place in a slice) is a product fact, not an operational one. So is a feature's state: it is the feature's own, on its spine entry, and the plays that take a feature into a plan or out of it set it.
```

---

## 7. Feature issue

### What it is

```diff
- A person closes it through `/reshape-plan` "finish", and then the feature is built.
+ A person closes it, through `/reshape-plan` "finish" or by merging a change that closes it, and then its feature's state becomes Completed.
```

### Properties

```diff
- | State | open or closed, as the tracker holds it. Closed as completed means its feature is built | yes |
+ | State | open or closed, as the tracker holds it. Closing it as completed sets its feature's state to Completed | yes |
```

### Rules

```diff
- The plan play files one only for a feature that is not yet built, and only when the search finds none.
+ The plan play files one only for a feature that is not Completed and not Dropped, and only when the search finds none.
```

```diff
- A person closes it, through `/reshape-plan` "finish". Nothing closes it because its Stories closed: there is no roll-up. It can stay open with all its Stories closed.
+ A person closes it: through `/reshape-plan` "finish", or by merging a change that closes it (merge-work). When it closes as completed, its feature becomes Completed: `/reshape-plan` or merge-work sets the state, on the work's branch. When a person closes it as completed by hand, outside both, the next `/reshape-plan` session of a plan that holds it finds the close and sets Completed in the list the person approves. Nothing closes it because its Stories closed: there is no roll-up. It can stay open with all its Stories closed.
+ When a person opens it again after it closed as completed, `/reshape-plan` sets its feature back to In progress.
```

```diff
- Only "closed as completed" means its feature is built. When it is closed as not planned, its feature is not built: a new slice can take the feature in, and the plan play then shows the closed issue to the person, who opens it again or leaves the feature out. The play never files a second one.
+ Only "closed as completed" makes its feature Completed. `/reshape-plan` "drop" closes it as not planned and sets its feature to Dropped. A person who closes it as not planned by hand, outside `/reshape-plan`, changes no state in the model: the model tracks only the five states, and no play looks for that close later. When a plan takes in a feature whose Feature issue is closed as not planned — a Dropped feature that a person brought back, or a feature whose issue was closed by hand — the plan play shows the closed issue to the person and, on their yes, opens the same issue again. The play never files a second one.
```

### States

```diff
- open → closed as completed (its feature is built), by a person through `/reshape-plan` "finish"; open → closed as not planned, by a person through `/reshape-plan` "drop". A closed Feature issue is opened again only by a person.
+ open → closed as completed (its feature becomes Completed), by a person through `/reshape-plan` "finish" or by merging a change that closes it; open → closed as not planned, by a person through `/reshape-plan` "drop" (its feature becomes Dropped), or by hand (no state changes). A closed Feature issue is opened again only by a person: when it was closed as completed, its feature goes back to In progress; when it was closed as not planned, it opens when a plan takes its feature in, and the plan sets the feature to Planned.
```

### Examples

```diff
- The shop owner finished #122 in `/reshape-plan`, so it is closed as completed, and "Guest checkout" is built in plan #120 and in plan #150.
+ The shop owner finished #122 in `/reshape-plan`, so it is closed as completed, and "Guest checkout" is Completed: it counts complete in plan #120 and in plan #150.
```

```diff
- Feature issue #88 "Video visit" was closed as not planned last year, so "Video visit" is not built: when the slice "Remote care" took it in, the plan play showed #88 to the clinic manager, who opened it again, and no second issue was filed.
+ Feature issue #88 "Video visit" was closed as not planned last year, when the clinic manager dropped the feature, so "Video visit" was Dropped. This year the clinic manager brought it back, and it became Unplanned. When the slice "Remote care" took it in, the plan play showed #88 to the clinic manager, who said yes: #88 opened again, no second issue was filed, and "Video visit" became Planned.
```

---

## Open points for the product owner

None open. Every word above follows from the agreed questions (Q64 to Q71, Q10, Q50, Q52), the agreed kinds, and the decision record of 2026-11-12 (ADR 070).
