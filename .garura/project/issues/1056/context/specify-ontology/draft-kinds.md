# Draft — the kinds: the feature's state (issue 1056)

Stage: kinds (steps 2, 3 and 4 of the ontology method). It rests on the questions you agreed at the first checkpoint (Q10, Q50, Q52 changed; Q64 to Q71 new). Today the ontology is version 17; this change makes it version 18.

## Opening

This draft says which parts of the product ontology this change reuses, which kinds change, and why. You decide three things at the end: that no new kind is needed, which six kinds change, and that the Domain kind stays as it is. When you say yes, the next stage writes the exact properties, links and rules of each changed kind.

## Words used in this draft

- **Kind** — one type of thing in the product ontology, for example Feature or Plan. The ontology says what each kind is, what it holds and how it links to other kinds.
- **The whole-model rule** — the paragraph at the top of the ontology that holds for every part of the model. Today it says "no part of the model holds a work status".
- **The spine** — the index of the product model: one entry for each domain, capability and feature.
- **The five states** — Unplanned, Planned, In progress, Completed, Dropped.

---

## Step 2 — What we reuse, and where words clash

### What we reuse

- **The Feature kind** holds the state. It already has a property for "built", which is worked out each time through the tracker. That property becomes the stored state. No new kind is made.
- **The Feature issue** stays the one tracker issue for a feature. Its close as completed is still what makes a feature built; now the close also sets the state in the model.
- **The Capability's Done** stays a value that is worked out each time and never stored. Only its test changes: every feature Completed or Dropped.
- **The plays that already own each moment** set each state: the play that adds a feature, `/shape-plan` and `/reshape-plan` for plans, `/start-work` when work starts, merge-work and `/reshape-plan` when a Feature issue closes. No new play is made.
- **The ready check of the ICE** stays as it is, with the new test for Done.

### Where words clash, and how each clash is settled

| Word | Where it already means something | How it is settled |
|------|----------------------------------|-------------------|
| status | The spine's old field on every domain, capability and feature entry: proposed, active or deprecated | The old field goes (decision record of 2026-11-12, ADR 070). In the spine, "status" then means only the feature's state |
| status | The plan file: the plan's Status, each slice's status and each item's status | These stay in the plan file. They are about the work. The feature's state is about the product, and it lives in the model. The two are different fields in different places, and neither is worked out from the other |
| In progress / In Progress | The plan file writes "In Progress" for a plan or a slice | The feature's state is written "In progress", as the decision record writes it. It is a different field, so the two spellings do not meet |
| Completed / Done | A plan item is "Done" when its issue closes as completed | The feature's state is "Completed". The plan item for the feature's Feature issue shows Done at the same moment. Different field, same event |
| Planned / Not Started | A slice or a plan item is "Not Started" in the plan file | "Planned" is the feature's state when a plan holds it and no work has started. "Not Started" stays the plan file's word |
| Dropped | A plan, a slice or a plan item can be Dropped; a business intent's stage can be dropped | The same word, for the same idea: it will not be done. Each kind keeps its own; a dropped plan does not drop its features (Q68) |
| built | Used across the ontology for a feature whose Feature issue closed as completed | It stays, and it means Completed (Q52) |

---

## Step 3 — The terms

- **Nouns:** feature, state, the five state names, spine entry, Feature issue, capability, Done, plan, slice, work branch, clean-up, warning, check.
- **Verbs:** add (a feature to the model), take into a plan, start work, finish, close as completed, close as not planned, drop, bring back, leave a plan, open again, warn.

Each noun is a kind the ontology already has, or a property of one. Each verb is a move from one state to another, made by a named play or by a person.

---

## Step 4 — The kinds

**No new kind.** The five states are a property of the Feature kind, with a States section that shows each move.

### Kinds that change

#### Feature — changes

- **What changes:** The property "Built" (worked out through the tracker, never stored) becomes the stored property **Status**: one of the five states, required, kept on the feature's spine entry only and not on its page (Q71). A new **States** section shows each move and who makes it (Q65). The rules say: only a feature has a state; In progress is set only by `/start-work`, which asks and never blocks on an Unplanned feature; a Completed feature stays Completed when more work starts; a Dropped feature stays out of new slices and plans until a person brings it back as Unplanned (Q67); a feature that leaves its last plan goes back to Unplanned, or stays In progress if work started (Q68); a drop runs a check that warns and never blocks (Q70); the state is written on the work's branch; the state names no plan, no tracker issue and no decision record. "Lives at" names the spine entry's `status`. The three examples show a state.
- **Why:** The product owner needs the model, read alone, to say what is built (Q64). The tracker is only the agentic part.
- **Its part of the log line:** "Feature: Built becomes the stored Status, on its spine entry only, with its States and who sets each."

#### Capability — changes

- **What changes:** Its Done property and its Done rule read "every feature Completed or Dropped" in place of "every feature built". A new rule says it has no state of its own and nothing rolls up from its features (Q66). A capability with no features is still not done. The bank example uses the states.
- **Why:** A dropped feature must not keep its capability from being done for ever, and Done is read from the model, not the tracker (Q10).
- **Its part of the log line:** "Capability: no state of its own; Done means every feature Completed or Dropped, still worked out each time."

#### ICE — changes in wording only

- **What changes:** The ready check's sentence "A needed capability is done when every feature in it is built" reads "... is Completed or Dropped". The bank example ("its Feature issue is open") names the feature's state.
- **Why:** The ready check uses the Capability's Done (Q10).
- **Its part of the log line:** "ICE: the ready check in wording."

#### Slice — changes

- **What changes:** It takes in only features that are not Completed and not Dropped, and `/design-slice` reads the state from the model, with no tracker search (Q50). "What it is", the rule and the clinic and bank examples follow. "Whether its work is in progress is read from the plan files" stays: that is the slice's work, not a feature's state.
- **Why:** Reading "built" from the tracker is what the change removes.
- **Its part of the log line:** "Slice: leaves out Completed and Dropped features, read from the model."

#### Plan — changes

- **What changes:** The plan play takes in only features that are not Completed and not Dropped, read from the model (Q50). The play that takes a feature into a plan sets it to Planned: `/shape-plan` when it makes the plan, `/reshape-plan` when it adds the feature later (Q65). When a feature leaves the plan, or the plan is Dropped, `/reshape-plan` sets the feature's new state in the list the person approves (Q68). The rule "the status of each slice and of each item lives in the plan file only" stays, with one added line: the feature's state is not a plan status; it is the feature's own, in the model.
- **Why:** The plan is where a feature is taken into work, so the plan's plays are the ones that set Planned and undo it.
- **Its part of the log line:** "Plan: leaves out Completed and Dropped features, read from the model; the play that takes a feature in sets Planned, and `/reshape-plan` sets the state of a feature that leaves."

#### Feature issue — changes

- **What changes:** Its State property says that closing as completed sets its feature to Completed. Its rule "only closed as completed means built" stays. The rule about closing as not planned is rewritten: `/reshape-plan` "drop" closes the issue as not planned and sets the feature to Dropped; a person who closes it as not planned by hand changes no state, because the model tracks only the five states and nothing looks for that close later (Q70). When a dropped feature comes back and a plan takes it in, the same Feature issue is opened again, never a second one (Q69). Its States add: closed as completed by merge-work at a merge; opened again for a Completed feature, which goes back to In progress. "Files one only for a feature that is not yet built" reads "... not Completed and not Dropped".
- **Why:** The Feature issue's close is the event that sets Completed, and its open-again is the event that undoes it.
- **Its part of the log line:** "Feature issue: its close as completed sets Completed; a hand close as not planned changes no state; the same issue opens again when a dropped feature comes back."

#### The whole-model rule — changes

- **What changes:** "No part of the model holds a work status" becomes "Each feature holds its own state, `status`, one of five; no other part holds one, and nothing rolls up." The spine still has no `epics` list. The flow line "a person closes the Feature issue, and its Feature is built" adds "and the feature becomes Completed".
- **Why:** The decision record amends that sentence of the rule (ADR 070, which amends ADR 069 §2).
- **Its part of the log line:** "The whole-model rule and the flow line change."

### Kinds that do not change

- **Domain** — listed in the need, but it does not change. Its kind never named the old field; it holds no state and is never in a plan. The old field is removed from the domain entry in the spine schema, which is a separate file, outside the ontology. The whole-model rule already says that only a feature has a state. **Domain can come off the need's Touches list.**
- **Story** — not in the need, and it does not change. Its line "its feature is built only when a person closes the Feature issue" stays true, because "built" means Completed (Q52).
- **Business Intent, Source, Epic, Spike, Chore, Bug** — not in the need, and they do not change. A business intent keeps its stage, which is not a work state.

### Which kind answers each new question

| Question | Answered by |
|----------|-------------|
| Q64 — a feature's state, read from the model | Feature (Status) |
| Q65 — which step set each state | Feature (States); Plan (Planned); Feature issue (its close) |
| Q66 — a capability's features by state | Capability has Feature; Feature (Status); Capability has no state |
| Q67 — how a dropped feature comes back | Feature (States: Dropped → Unplanned) |
| Q68 — a feature that leaves a plan | Feature (States); Plan |
| Q69 — the Feature issue of a returning feature | Feature issue (opened again, never a second one) |
| Q70 — the warning on a drop | Feature (its rule: a check warns, never blocks) |
| Q71 — where the state is seen | Feature (Lives at: its spine entry only) |
| Q10, Q50, Q52 — changed | Capability (Done); Slice and Plan; Feature (Status Completed) |

### The log line for version 18

- 2026-11-12 — v18 (#1056, ADR 070, with the product owner): each feature records its own state in the model — `status` on its spine entry only, one of Unplanned, Planned, In progress, Completed or Dropped — and plays read "built" from the model (Completed), not from the tracker. Who sets each: the play that adds a feature (Unplanned); `/shape-plan`, or `/reshape-plan` later, when a plan takes it in (Planned); only `/start-work`, when work first starts (In progress), which asks on an Unplanned feature and never blocks; the close of its Feature issue as completed (Completed), and once the clean-up for features built before ADR 068; a person (Dropped), with a check that warns and never blocks. A dropped feature comes back through `/reshape-plan` as Unplanned, and its same Feature issue opens again when a plan takes it in; a feature that leaves its last plan goes back to Unplanned unless its work started. Only a feature has a state; nothing rolls up, and the old spine `status` (proposed, active, deprecated) goes. The whole-model rule and the flow line change. Feature: Built becomes the stored Status, with its States. Capability: Done means every feature Completed or Dropped. ICE: the ready check in wording. Slice and Plan: leave out Completed and Dropped features, read from the model; the plan sets Planned. Feature issue: its close as completed sets Completed; a hand close as not planned changes no state. Changed kinds: Feature, Capability, ICE, Slice, Plan, Feature issue. Q10, Q50 and Q52 change; Q64 to Q71 are added.

---

## Questions for the product owner

### K1 — No new kind

- **Question:** Do the five states live on the existing Feature kind, with no new kind made for them?
- **Answer (proposed):** Yes. The state is one property of the Feature, stored on its spine entry, with a States section that shows each move. A separate kind would be a second thing to keep in agreement with the feature it describes.
- **Why it matters:** A new kind for the state would need its own entry, its own links and its own rules, and it could drift from the feature. If the state is not on the Feature, a reader who opens a feature's entry does not see it.
- **Example:**
  - A clinic: the spine entry of "Send a reminder" holds `status: In progress`, beside its name and its capability.
  - A shop: the spine entry of "Pay without an account" holds `status: Completed`.
  - A bank: the spine entry of "Paper application form" holds `status: Dropped`.

### K2 — The kinds that change

- **Question:** Are these the kinds this change rewrites: Feature, Capability, ICE (in wording only), Slice, Plan and Feature issue, with the whole-model rule?
- **Answer (proposed):** Yes. Each one holds a sentence that reads "built" from the tracker, says no part holds a state, or sets or undoes a state. Every other kind stays as it is.
- **Why it matters:** A kind left out keeps an old sentence that says the opposite of the new rule, and an agent that reads it acts on the old rule. A kind added without need changes words that are still right.
- **Example:**
  - A clinic: the Slice's rule today says `/design-slice` asks the tracker whether "Pick a free slot" is built. After the change it reads the feature's state in the model.
  - A shop: the Capability's Done today counts only built features. After the change "Cart" is done when each feature is Completed or Dropped.
  - A bank: the Story kind says a Story's close does not build its feature. That stays true, so the Story kind is not changed.

### K3 — Domain stays as it is

- **Question:** Does the Domain kind stay unchanged, so that it comes off the list of kinds this change touches?
- **Answer (proposed):** Yes. The Domain kind never named the old field, holds no state and is never in a plan. The old field is removed from the domain entry in the spine schema, a separate file. The whole-model rule says that only a feature has a state.
- **Why it matters:** If Domain stays on the list, the change claims to touch a kind it does not change, and a reviewer looks for an edit that is not there.
- **Example:**
  - A clinic: the domain "Appointments" reads the same before and after the change.
  - A shop: the domain "Orders" loses the old `status: proposed` from its spine entry, but its kind in the ontology is unchanged.
  - A bank: a reader asks "is the domain Lending done?" The whole-model rule answers: a domain has no state.
