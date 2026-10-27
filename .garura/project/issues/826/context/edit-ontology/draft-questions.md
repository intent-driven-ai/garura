# Draft — the questions (stage: scope, step 1) — #826

You decide which questions the product model must answer about stories, slices and their evals. Today the model breaks one rule of Intent-Driven Development: the agent that builds a story can read what counts as failing, because a story's scope of work says "what must never happen". This change exists to keep the routing table in `docs/philosophy/idd-principles.md` ("The Routing Table") true, word for word: the builder never gets the failure conditions, the recovery conditions or the evals. When you say yes to these questions, the next stage changes the Story and Slice kinds so that the model answers them.

Each question is marked **new**, **changed** or **stays**. Q28 and Q31 stay word for word as agreed under #816. Q29 changes only where this need requires it. Answers marked "proposed" are not agreed yet.

## New

### Q32 (new)

**Question:** Given a story, what does the agent that builds it see?
**Answer (what the model gives back):** The story's goal, its constraints and its expectations (the success scenarios). The story never holds failure conditions or recovery conditions, so the builder never sees them. The builder also never sees the slice's eval.
**Why it matters:** If the builder sees what counts as failing, it builds to avoid those checks, and not to meet the goal. Then a pass on the eval no longer shows that the product works.
**Example:**
- Clinic. Asked: "What does the builder of the story 'Pick a free slot' see?" → Answer: goal "a patient picks a free slot and books it"; constraint "only slots the doctor opened"; expectation "the patient sees the booked slot on the confirmation page". It does not see "a slot is never booked twice".
- Shop. Asked: "What does the builder of the story 'Guest checkout' see?" → Answer: goal "a shopper with no account pays"; constraint "card data goes only to the payment provider"; expectation "the shopper sees an order number". It does not see "a card is never charged twice".
- Bank. Asked: "What does the builder of the story 'Score the application' see?" → Answer: goal "each application gets a score"; constraint "use only the documents the business sent"; expectation "the score is on the application within one hour". It does not see "no decision goes out without a score".

### Q33 (new)

**Question:** Given a slice, where are the failure conditions and recovery conditions of its stories kept?
**Answer (what the model gives back):** In one hidden file in the slice's eval folder, `.garura/project/plans/<plan-id>/evals/<slice>/`. The file lists each story of the slice with its failure conditions and its recovery conditions. A builder never reads this folder. (Proposed: the name of the file is set at the links stage.)
**Why it matters:** If these conditions have no place, they get put in the story, where the builder reads them. Or they are lost, and the eval cannot test that nothing fails.
**Example:**
- Clinic. Asked: "Where are the failure and recovery conditions for 'Self-booking'?" → Answer: in the hidden file in `.garura/project/plans/340/evals/self-booking/`. For "Pick a free slot": fails if a slot is booked twice; to recover, free the second booking and tell the patient.
- Shop. Asked: "Where are the failure and recovery conditions for 'Pay without an account'?" → Answer: in the hidden file in `.garura/project/plans/120/evals/pay-without-an-account/`. For "Guest checkout": fails if a card is charged twice; to recover, refund the second charge.
- Bank. Asked: "Where are the failure and recovery conditions for 'One-day decision'?" → Answer: in the hidden file in `.garura/project/plans/51/evals/one-day-decision/`. For "Score the application": fails if a decision goes out with no score; to recover, hold the decision until a score exists.

### Q34 (new)

**Question:** Who writes the failure conditions and recovery conditions of a slice's stories?
**Answer (what the model gives back):** The plan play. It writes them when it writes the epic and its stories, from the same two ICE each story is written from (its feature's ICE and that feature's capability's ICE). It puts the goal, constraints and expectations in the story, and the failure and recovery conditions in the hidden file. So the plan play interprets each ICE once.
**Why it matters:** If another play writes these conditions, two plays interpret the same ICE, and they can disagree. If no play writes them, the eval has nothing to test failure against.
**Example:**
- Clinic. Asked: "Who writes 'a slot is never booked twice' for 'Pick a free slot'?" → Answer: the plan play, from the ICE of the feature "Pick a free slot" and of the capability "Booking", when it writes Epic #341.
- Shop. Asked: "Who writes 'a card is never charged twice' for 'Guest checkout'?" → Answer: the plan play, from the ICE of the feature "Guest checkout" and of the capability "Payments", when it writes Epic #121.
- Bank. Asked: "Who writes 'no decision goes out without a score' for 'Score the application'?" → Answer: the plan play, from the ICE of the feature "Score the application" and of the capability "Lending", when it writes Epic #52.

### Q35 (new)

**Question:** When a slice's eval finds a failure, what does the builder get back?
**Answer (what the model gives back):** Proposed: only a recovery handoff plan. The eval, when it runs on the built slice, reads the recovery conditions in the hidden file and writes the handoff plan. The plan says what the product does wrong. It does not name the failure condition or the check that failed.
**Why it matters:** If the builder gets the failure condition or the check, it learns the eval and fixes only that check. The routing table lets the builder have only the handoff plan.
**Example:**
- Clinic. Asked: "The eval finds two bookings on one slot. What does the builder get?" → Answer: "Two patients can book the same 10:00 slot when they book at the same time. Make the second one see that the slot is gone."
- Shop. Asked: "The eval finds a card charged twice. What does the builder get?" → Answer: "A shopper who taps 'Pay' twice is charged twice. Make the second tap do nothing."
- Bank. Asked: "The eval finds a decision with no score. What does the builder get?" → Answer: "A decision goes out while the score is still running. Make the decision wait for the score."

## Changed

### Q26 (changed — the question stays; its answer changes)

**Question:** Given a story, what does it deliver, what is its scope of work, and which ICEs was it written from?
**Answer (what the model gives back):** The story delivers one feature. Its scope of work says the goal (what the feature must do), the constraints, and the expectations (what is expected). It no longer says "what must never happen". It is written from two ICE: its feature's ICE and that feature's capability's ICE.
**Why it matters:** Today the scope of work says "what must never happen", and the builder reads the story. So the failure conditions reach the builder, and the routing table is broken.
**Example:**
- Clinic. Asked: "What is the scope of work of 'Pick a free slot'?" → Answer: delivers the feature "Pick a free slot"; must let a patient book a free slot, only from slots the doctor opened; expected: the booked slot shows on the confirmation page. Written from the ICE of "Pick a free slot" and of "Booking".
- Shop. Asked: "What is the scope of work of 'Guest checkout'?" → Answer: delivers the feature "Guest checkout"; must let a shopper with no account pay, with card data sent only to the payment provider; expected: an order number shows. Written from the ICE of "Guest checkout" and of "Payments".
- Bank. Asked: "What is the scope of work of 'Score the application'?" → Answer: delivers the feature "Score the application"; must give each application a score, from the sent documents only; expected: the score is on the application within one hour. Written from the ICE of "Score the application" and of "Lending".

### Q29 (changed)

**Question:** Given a slice, what does its eval test?
**Answer (what the model gives back):** What the slice's epic delivers. The eval reads four things: the epic, its stories, the hidden file of failure and recovery conditions (see Q33) and the slice's usage guide (see Q31). It tests that every goal and every expectation the stories carry is met, and that no failure condition in the hidden file happens. It tests from the outside, on the built product: it does not know how the slice was built. The slice can be a browser page, a mobile app, a command line tool or a backend process. The eval never reads the ICE of a feature or a capability directly. So the eval gets all of the ICE, but only as the plan play wrote it, once, into the epic, the stories and the hidden file.
**Why it matters:** Without it, a slice can be "done" with all its stories closed while the product does not do what the epic says. If the eval read the ICE itself, two things would interpret the same ICE, and they could disagree. And if the eval read only the stories, it would have no failure conditions to test.
**Example:**
- Clinic. Asked: "What does the eval for 'Self-booking' test?" → Answer: what Epic #341 "Self-booking" delivers, as its Stories "Pick a free slot" and "Send a reminder" describe it. A patient books a free slot and gets a reminder (goal and expectation met). From the hidden file: no slot is booked twice.
- Shop. Asked: "What does the eval for 'Pay without an account' test?" → Answer: what Epic #121 "Pay without an account" delivers, as its Stories "Guest checkout" and "Send receipt" describe it. A shopper with no account pays and gets a receipt. From the hidden file: no card is charged twice.
- Bank. Asked: "What does the eval for 'One-day decision' test?" → Answer: what Epic #52 "One-day decision" delivers, as its Stories "Upload documents" and "Score the application" describe it. A small business gets a decision on the same day. From the hidden file: no decision goes out without a score.

## Stays

### Q28 (stays, word for word as agreed under #816)

**Question:** Given a slice, where is its eval kept?
**Answer (what the model gives back):** The path of the slice's eval folder. Each plan has one evals folder under the plan's own folder: `.garura/project/plans/<plan-id>/evals/`. In it, each slice of the plan has its own folder: `.garura/project/plans/<plan-id>/evals/<slice>/`. The plan itself stays the file `.garura/project/plans/<plan-id>.yaml`; the evals sit under the plan, not in a separate place. A builder agent, or any skill that builds the software, never reads this folder. CLAUDE.md says so.
**Why it matters:** Today the model does not name this place, so a builder can read the eval and build only to pass it.
**Example:**
- Clinic. Asked: "Where is the eval for 'Self-booking'?" → Answer: `.garura/project/plans/340/evals/self-booking/`. A builder never reads it.
- Shop. Asked: "Where is the eval for 'Pay without an account'?" → Answer: `.garura/project/plans/120/evals/pay-without-an-account/`. A builder never reads it.
- Bank. Asked: "Where is the eval for 'One-day decision'?" → Answer: `.garura/project/plans/51/evals/one-day-decision/`. A builder never reads it.

### Q31 (stays, word for word as agreed under #816)

**Question:** Given a built slice, how does its eval learn to use it?
**Answer (what the model gives back):** The slice's usage guide. The build delivers this guide with the slice. The guide says what surface the slice is on (a browser URL, a mobile app, a command line command or a backend endpoint), how to reach it, and the steps a person takes. The eval reads only the guide, never the code.
**Why it matters:** The eval does not know how the slice was built. Without the guide, it cannot find the slice to test it, or it must read the code, and then it is no longer a test from the outside.
**Example:**
- Clinic. Asked: "How does the eval for 'Self-booking' learn to use it?" → Answer: from its usage guide: "Open https://clinic.example/book in a browser, pick a doctor, pick a free slot, give a phone number."
- Shop. Asked: "How does the eval for 'Pay without an account' learn to use it?" → Answer: from its usage guide: "In the mobile app, add an item to the cart, tap 'Pay as guest', give a card."
- Bank. Asked: "How does the eval for 'One-day decision' learn to use it?" → Answer: from its usage guide: "Send the application to the endpoint POST /applications, then ask GET /applications/<id>/decision."

### All other questions (stay)

Q1 to Q25, Q27 and Q30 stay as they are. Q13 and Q18 name the Story but not its scope of work, so they do not change. No other question says that a story names "what must never happen".

## Points for the next stages (not questions)

- The ICE kind has no recovery part today: its Intent holds goals, limits and "fails if", and its Expectation holds scenarios, "done" and quality needs. The routing table names recovery conditions as part of the Expectation. So Q33 and Q34 need a source for the recovery conditions. The kinds stage must say where the plan play takes them from, or the person decides it. The ICE itself is not changed by this need.
- The routing table gives the builder "all of Context". The need gives the Story only the goal, constraints and expectations. The kinds stage must say how the builder still gets the Context, so that the table holds word for word.
- Rules for the links stage: "a story never holds failure conditions or recovery conditions"; "the plan play writes them into the slice's hidden file"; "a builder never reads the slice's eval folder" (already a Slice rule in v9). The Eval property of the Slice ("no failure condition they name happens") and the Story's "Scope of work" property change with Q26 and Q29.
