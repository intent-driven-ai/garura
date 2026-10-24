You decide the one slice that shows business intent 788 is served: "agents design a named piece of work". I read the model and memory first, and these 7 questions are the gaps that neither one answers. Your answers become facts in the question record, and the run then shapes the slice from them.

### 1. Q-intent-1 (blocking)
**Question** Is the drafted page for business intent bi-788 confirmed as your own intent?
**Answer** No proposed answer yet. Only you can confirm it. Note: the drafted title is "Agents design a named piece of work, and plays then run its build", but the build is now out of scope (#819). Say "yes", or "yes, title: <your words>".
**Why it matters** The page is at stage "proposed". The ready rule treats every part that serves only a proposed intent as not ready, so the slice's new parts stay blocked until you confirm.
**Example** A shop confirms "customers return an item without calling support" before its returns slice is shaped. A clinic confirms "patients book their own follow-up visit" before its booking slice is shaped.

### 2. Q-surface-1 (blocking)
**Question** Which one command starts the shaping loop when you test it end to end?
**Answer** No proposed answer yet. If you skip it, the run assumes `/shape-slice <intent issue>`, which then runs the plan play and the eval play and stops once, at the one approval.
**Why it matters** A slice has exactly one surface. A wrong choice leaves out a feature (for example a new loop command) or tests the loop from the wrong entry.
**Example** A shop's surface is its checkout page. A bank's surface is its POST /transfers endpoint. A data team's surface is its "report run" command.

### 3. Q-capability-1
**Question** Should the four shaping plays sit under one new capability for the shaping loop?
**Answer** No proposed answer yet. If you skip it, the run assumes one new capability (#794) that holds /shape-slice (#795), the plan play (#818), the eval play (#798) and the one approval step (#796).
**Why it matters** No capability in the model serves bi-788, so the run must add one. Splitting the plays across several capabilities changes which ICE each story is planned from.
**Example** A shop's "Returns" capability holds start a return, print a label and track the refund. A clinic's "Booking" capability holds find a slot, book it and move it.

### 4. Q-order-1
**Question** Should the one approval step be built last, after the eval play?
**Answer** Proposed: yes. The build order is /shape-slice (already built), then the plan play, then the eval play, then the approval step. Source: the bi-788 page, line 14 ("one approval, at the end").
**Why it matters** The approval shows the slice, the plan and the eval together. If it is built first, it is tested against parts that do not exist yet.
**Example** A shop builds the order summary page after the cart and the payment step that it sums up. A tax app builds the final review screen after the forms it shows.

### 5. Q-scope-1
**Question** Does the slice need eval encryption (#828) to meet the proof that no builder can read the eval?
**Answer** No proposed answer yet. If you skip it, the run assumes the read rule is enough for this slice, and encryption stays outside it.
**Why it matters** Today only a rule keeps builders out of a plan's evals folder (ADR 049). Encryption adds a feature and moves the build order. Without it, the proof rests on a rule that nothing on disk enforces.
**Example** An exam board uses sealed papers, or a rule that staff do not open the cupboard. A hospital uses an encrypted patient file, or a rule that only the doctor opens it.

### 6. Q-scope-2
**Question** Does the slice need the author-slice skill (#838) for the step that picks the features?
**Answer** Proposed: no. The agent picks the features, surface and tester inside /shape-slice, which is a play, so the step is still run by a play. Source: the bi-788 page, line 15 ("a play runs each step").
**Why it matters** Adding the skill adds a feature to the slice. Leaving it out keeps that choice with the agent, which records why it chose.
**Example** A bakery's head baker picks the daily menu, or a written recipe card picks it. A support desk's lead sorts each ticket, or a set routing rule sorts it.

### 7. Q-test-1
**Question** On which project do you run the shaping loop to test the slice?
**Answer** Proposed: on Garura's own repository, on a real business intent issue. Source: the bi-788 page, line 5 ("no play designs the work for Garura's own work").
**Why it matters** The eval play (#798) names Griffin as the test project for a play. Testing on the wrong project checks the loop against the wrong product model.
**Example** A mobile app is tested on its staging build, not on the live store. A bank tests a new transfer flow in its sandbox, not with real accounts.

---

Settled from the model and memory, not asked: the tester is the product owner; no domain is needed; tracker writes happen only after the one approval; there is no existing slice to reuse.

Assumptions not asked: none (7 questions, within the limit of 25).

Questions with no proposed answer: 4 (1, 2, 3 and 5).

One more thing to approve: memory update **mu-20261024-002**. It copies the shared asking-a-person rule (#820) into this issue's short-term memory. The rule is in no memory tier yet, because it is not on main. Say "mu-002: yes" or "mu-002: no".

Answer by number or id, for example `1. yes` or `Q-scope-1: skip`. Type `skip` to leave a question for later. Blocking questions 1 and 2 cannot be skipped.
