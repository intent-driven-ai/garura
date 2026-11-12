# Draft — the questions the ontology must answer: the feature's state (issue 1056)

Stage: scope (step 1 of the ontology method), second draft. It takes in the product owner's answers at the first checkpoint (2026-11-12). Need: each feature in the product model records its own state.

## Opening

This draft lists the questions the product ontology must answer once each feature records its own state. You decide one thing: that the eleven new and changed questions below are the right ones. Their answers are already decided, in the decision record of 2026-11-12 (ADR 070) and in your answers at the first checkpoint, so you do not answer them again. When you say yes, the next stage writes the kinds from these questions, and every later stage is tested against them.

## Words used in this draft

- **Feature** — one thing a person can do in the product, for example "pay without an account". It sits inside one capability.
- **Capability** — a larger thing the product can do, for example "Checkout". It holds many features.
- **Feature issue** — the one tracker issue that stands for a feature. Its text names the feature. The feature does not name it.
- **Slice** — an ordered group of features that a person can test end to end.
- **Plan** — the file that holds the work for one business intent: its slices, its one epic and its Feature issues.
- **The spine** — the index of the product model: one entry for each domain, capability and feature.
- **The five states** — Unplanned (in the model, and no plan holds it), Planned (a plan holds it, and no work on it has started), In progress (some of its work is done and some is open), Completed (it is built), Dropped (it will not be built).

The ontology has 63 questions today (Q1 to Q63). Three of them change (Q10, Q50 and Q52). The other 60 stay as they are. Eight questions are new (Q64 to Q71).

---

## Part 1 — New and changed questions, with the answers already decided

### Q64 (new)

- **Question:** Given a feature, what is its state, read from the product model alone?
- **Answer:** Each feature holds one of five states: Unplanned, Planned, In progress, Completed or Dropped. The state is kept in the model, so a person can read it with no tracker open. Only a feature has a state. The model tracks the five states and nothing more: it holds no workflow.
- **Why it matters:** The product model is the record of the product that can be sent to someone. If the model cannot say what is built, the reader must open the tracker. Features built before Feature issues existed then stay invisible.
- **Example:**
  - A clinic: "Send a reminder" is In progress. Its work for the text message is done. Its work for the email is still open.
  - A shop: "Pay without an account" is Completed. Shoppers use it today.
  - A bank: "Paper application form" is Dropped. The bank takes loan applications online only.

### Q65 (new)

- **Question:** Given a feature in a state, which step put it in that state?
- **Answer:** Each state has a named step that sets it:
  - **Unplanned** — the play that adds the feature to the model. Also the plan-session play (`/reshape-plan`) when a person brings back a dropped feature (Q67), or when a feature leaves its last plan without being dropped (Q68).
  - **Planned** — the play that takes the feature into a plan: `/shape-plan` when it makes the plan, `/reshape-plan` when it adds the feature later.
  - **In progress** — only `/start-work`, when work on the feature first starts. Work starts when a person starts the Feature issue, a Story inside it, or a Bug or a Spike under that Story. A start of the plan, or of a Chore under the plan's epic, changes nothing. Design, slicing and planning are never work. Also `/reshape-plan`, when a person opens again the Feature issue of a Completed feature.
  - **Completed** — when the Feature issue closes as completed: through `/reshape-plan` "finish", through merge-work when it closes the Feature issue at a merge, or through `/reshape-plan` when it finds a Feature issue that a person closed as completed by hand. Also one time only, through the clean-up of the model, for the features built before Feature issues existed; the person confirms the whole list first.
  - **Dropped** — a person, when they set the feature to Dropped (not planned), by whatever means. At that moment a check warns them of what is known (Q70). No step looks for it later.

  When work starts on an Unplanned feature, `/start-work` says so, goes on only when the person says yes, and records that the work started with no plan. It never blocks the work. A Completed feature stays Completed when more work starts on it. Each state is written on the branch of the work that sets it, and main shows it when that work lands.
- **Why it matters:** When a state is wrong, a person must know which step to look at. A state that no named step sets drifts, and nobody can say where it came from.
- **Example:**
  - A shop: the shop owner starts the Story "Pay by card" inside the Feature issue of "Pay without an account". The feature moves from Planned to In progress.
  - A clinic: the clinic manager starts the plan for online booking. No feature changes state. Each stays Planned until work on it starts.
  - A bank: a developer starts work on "Upload documents" before any plan holds it. `/start-work` says the feature is Unplanned. The developer says yes, the work goes on, and the record says the work started with no plan.

### Q66 (new)

- **Question:** Given a capability, which of its features are Unplanned, Planned, In progress, Completed or Dropped?
- **Answer:** Each feature of the capability shows its own state. The capability itself has no state. A domain and a business intent have no state either. Nothing rolls up from the features: a capability is something the product has, not something we build. The old field "status" in the spine (proposed, active or deprecated) goes from every domain, capability and feature entry. After that, the word "status" in the spine means only the feature's state.
- **Why it matters:** A state stored on a capability goes out of date when one of its features changes, and then two values disagree. One word with two meanings confuses readers and plays.
- **Example:**
  - A clinic: the capability "Booking" shows no state. Its feature "Pick a free slot" is Completed and "Send a reminder" is In progress.
  - A shop: the domain "Commerce" shows no state. Its capability "Cart" has one feature Planned and one Unplanned.
  - A bank: the business intent "Small businesses get a loan decision in one day" keeps its stage (proposed, confirmed, met or dropped). The stage is the person's view of the intent. It is not a work state.

### Q67 (new)

- **Question:** How does a dropped feature come back into the product's work?
- **Answer:** A Dropped feature stays out of every new slice and every new plan. A person brings it back in a `/reshape-plan` session, which sets it to Unplanned. After that, a new slice or plan can take it in again.
- **Why it matters:** Without a way back, a person who changes their mind must add the same feature a second time, and the model then holds two features for one thing.
- **Example:**
  - A bank: the bank dropped "Paper application form". A year later it must serve customers with no internet. The loan officer brings the feature back, and it is Unplanned.
  - A shop: the shop owner dropped "Gift wrap" before the summer sale. Before the winter sale the shop owner brings it back.
  - A clinic: the clinic manager dropped "Book by phone call-back", then brings it back when patients ask for it.

### Q68 (new)

- **Question:** When a feature leaves a plan but is not dropped, which state does it go to?
- **Answer:** It goes back to Unplanned when no other plan holds it. It stays Planned when another plan still holds it. When its work has already started, it stays In progress. A feature leaves a plan when a person moves it out of the plan, or when a person sets the whole plan to Dropped. `/reshape-plan` sets the new state, in the list the person approves.
- **Why it matters:** With no rule, a feature stays Planned with no plan. The next plan play and every reader then think someone will build it.
- **Example:**
  - A shop: the shop owner moves "Gift wrap" out of the winter-sale plan to do later. No other plan holds it, so it goes back to Unplanned.
  - A clinic: the clinic manager drops the plan for follow-up visits. "Send a reminder" is also in the self-booking plan, so it stays Planned.
  - A bank: the loan officer drops the plan "One-day decision" after work on "Upload documents" started. The feature stays In progress.

### Q69 (new)

- **Question:** When a dropped feature comes back and a plan takes it in again, what happens to its closed Feature issue?
- **Answer:** The same Feature issue is opened again. A second Feature issue for the feature is never filed. While the feature is Unplanned and no plan holds it, its Feature issue stays closed.
- **Why it matters:** A second Feature issue for one feature breaks the rule of one Feature issue per feature. A closed issue that stays closed hides the new work.
- **Example:**
  - A bank: "Paper application form" comes back, and the plan "Serve offline customers" takes it in. Its old Feature issue opens again.
  - A shop: "Gift wrap" comes back but no plan holds it yet. Its Feature issue stays closed.
  - A clinic: "Book by phone call-back" comes back into the plan for phone patients. Its old Feature issue opens again, and no new one is made.

### Q70 (new)

- **Question:** When a person sets a feature to Dropped, what does the person learn before it is done?
- **Answer:** At that moment a check looks at what is known about the feature and warns the person: whether the feature was built (Completed), whether work on it started (In progress), and whether its work sits on open branches that may be idle. The check never blocks the drop. It adds no step to `/reshape-plan`, and no step looks later for a Feature issue closed as not planned by hand. The model only tracks the five states; this is a warning, not a workflow.
- **Why it matters:** A person who drops a feature may not know that part of it is built or that work on it waits on a branch. Without a warning, that work is lost from sight. A workflow of extra steps would make each plan session slower for a rare case.
- **Example:**
  - A shop: the shop owner drops "Pay by cheque". The check warns that a branch with its first Story has been idle for three weeks. The drop goes on.
  - A clinic: the clinic manager drops "Send a reminder". The check warns that the feature is In progress and that its text-message work is done. The clinic manager drops it anyway.
  - A bank: the loan officer drops "Fax upload". The check finds no work and no branch, so it gives no warning.

### Q71 (new)

- **Question:** Where does a reader see a feature's state?
- **Answer:** Only in the feature's entry in the spine. The spine is the single source of truth for the state. The feature's page does not show it.
- **Why it matters:** A state kept in two places can drift, and then the two disagree. With one place, every reader and every play reads the same value.
- **Example:**
  - A clinic: the clinic manager opens the page of "Send a reminder" and reads what it does. "In progress" shows in the spine's list of features, not on the page.
  - A shop: a new team member reads the spine and sees, in one pass, which checkout features are Completed.
  - A bank: an auditor gets the model and asks which features are built. The spine answers. The page of each feature says what it does.

### Q10 (changed in wording)

- **Question:** Can work start on this ICE now — is it ready, partly ready or not ready — and what stops it?
- **Answer:** The ready check does not change, except one test. A capability that another capability needs is done when every one of its features is Completed or Dropped (it was: when every feature is built, its Feature issue closed as completed). This is worked out each time someone asks, and nothing is written on the capability. A capability with no features is still not done.
- **Why it matters:** When the test reads the tracker and not the model, the model alone cannot say whether work can start. A dropped feature that counts as not done blocks the capability that waits for it, for ever.
- **Example:**
  - A bank: "Loan application" has "Upload documents" Completed and "Paper application form" Dropped. It is done, so it no longer stops the ICE of "Credit decision".
  - A clinic: "Booking" has "Send a reminder" In progress. It is not done, so the ICE of "Follow-up visits", which needs Booking, is not ready.
  - A shop: "Cart" has no features yet. It is not done.

### Q50 (changed)

- **Question:** Which features can a new slice or a new plan take in?
- **Answer:** Every feature that is not Completed and not Dropped: Unplanned, Planned and In progress features. The play reads the state from the model, with no search in the tracker. A feature that becomes Completed after it joined a slice or a plan stays there and counts as complete.
- **Why it matters:** A slice that takes in a built feature plans the same work twice. A slice that takes in a dropped feature builds what the person said no to.
- **Example:**
  - A shop: the new slice "Pay in one minute" takes in "Save a card" (Unplanned) and "Pay by card" (In progress in another plan). It leaves out "Pay without an account" (Completed).
  - A clinic: the new plan for follow-up visits leaves out "Paper sign-in sheet" (Dropped).
  - A bank: "Upload documents" becomes Completed while the plan "One-day decision" is in progress. It stays in that plan and counts as complete.

### Q52 (changed)

- **Question:** When does a feature count as built?
- **Answer:** When its state in the model is Completed. It becomes Completed when its Feature issue closes as completed. Closed Stories do not build it, and a Feature issue closed as "not planned" does not build it. The features built before Feature issues existed become Completed one time, through the clean-up the person confirms. Every slice and plan that holds a Completed feature counts it as complete. Nothing rolls up.
- **Why it matters:** "Built" decides what a new slice leaves out and when a capability is done. If plays read "built" from two places, they can disagree.
- **Example:**
  - A clinic: every Story of "Send a reminder" is closed, but the clinic manager has not finished its Feature issue. It is In progress, not Completed.
  - A shop: the shop owner finishes the Feature issue of "Pay without an account" in a `/reshape-plan` session. It is Completed in both plans that hold it.
  - A bank: "Upload documents" was built before Feature issues existed. The clean-up lists it from its old closed Story. The loan officer confirms the list, and it becomes Completed.

---

## Part 2 — Open points for the product owner

None open. The first checkpoint settled all four earlier open points: Q68 (a feature that leaves a plan), Q69 (the Feature issue of a feature that comes back), Q70 (the warning when a person drops a feature) and Q71 (the spine as the one place for the state).
