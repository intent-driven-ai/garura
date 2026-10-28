# Draft — the questions (stage: scope, step 1) — #816

These are the questions a person or an agent can ask the product model. The model must be able to answer each of them.

Every question is agreed. Q1 to Q26 are agreed and locked. Q7, Q25, Q27, Q28, Q29, Q30 and Q31 were agreed at checkpoint 1. Only Q29 was corrected after checkpoint 2, with the product owner's words: the eval reads the slice's epic and its stories, not the ICE. After the product owner's second change at checkpoint 2 (three plays run one after the other as the shaping loop: `/shape-slice`, then the plan play, then the eval play), Q29's words were aligned to name the plan play; its meaning did not change. Every other question is word for word as agreed.

## Agreed at checkpoint 1; Q29 corrected after checkpoint 2

### Q28 (new, agreed)

**Question:** Given a slice, where is its eval kept?
**Answer (what the model gives back):** The path of the slice's eval folder. Each plan has one evals folder under the plan's own folder: `.garura/project/plans/<plan-id>/evals/`. In it, each slice of the plan has its own folder: `.garura/project/plans/<plan-id>/evals/<slice>/`. The plan itself stays the file `.garura/project/plans/<plan-id>.yaml`; the evals sit under the plan, not in a separate place. A builder agent, or any skill that builds the software, never reads this folder. CLAUDE.md says so.
**Why it matters:** Today the model does not name this place, so a builder can read the eval and build only to pass it.
**Example:**
- Clinic. Asked: "Where is the eval for 'Self-booking'?" → Answer: `.garura/project/plans/340/evals/self-booking/`. A builder never reads it.
- Shop. Asked: "Where is the eval for 'Pay without an account'?" → Answer: `.garura/project/plans/120/evals/pay-without-an-account/`. A builder never reads it.
- Bank. Asked: "Where is the eval for 'One-day decision'?" → Answer: `.garura/project/plans/51/evals/one-day-decision/`. A builder never reads it.

### Q29 (corrected after checkpoint 2; words aligned after checkpoint 2)

**Question:** Given a slice, what does its eval test?
**Answer (what the model gives back):** What the slice's epic delivers, as its stories describe it. The eval tests that every intent and every expectation the stories carry is met, and that no failure condition they name happens. It tests from the outside, on the built product: it does not know how the slice was built. The slice can be a browser page, a mobile app, a command line tool or a backend process. The eval reaches it through the slice's usage guide (see Q31). The eval reads the epic and its stories. It never reads the ICE of a feature or a capability directly. So there is one interpretation of the ICE: the one the plan play wrote into the epic and its stories.
**Why it matters:** Without it, a slice can be "done" with all its stories closed while the product does not do what the epic says it delivers. And if the eval read the ICE itself, two things would interpret the same ICE, and they could disagree.
**Example:**
- Clinic. Asked: "What does the eval for 'Self-booking' test?" → Answer: what Epic #341 "Self-booking" delivers, as its Stories "Pick a free slot" and "Send a reminder" describe it. A patient books a free slot and gets a reminder (intent and expectation met), and no slot is booked twice (no failure condition).
- Shop. Asked: "What does the eval for 'Pay without an account' test?" → Answer: what Epic #121 "Pay without an account" delivers, as its Stories "Guest checkout" and "Send receipt" describe it. A shopper with no account pays and gets a receipt, and no card is charged twice.
- Bank. Asked: "What does the eval for 'One-day decision' test?" → Answer: what Epic #52 "One-day decision" delivers, as its Stories "Upload documents" and "Score the application" describe it. A small business gets a decision on the same day, and no decision goes out without a score.

### Q31 (new, agreed)

**Question:** Given a built slice, how does its eval learn to use it?
**Answer (what the model gives back):** The slice's usage guide. The build delivers this guide with the slice. The guide says what surface the slice is on (a browser URL, a mobile app, a command line command or a backend endpoint), how to reach it, and the steps a person takes. The eval reads only the guide, never the code.
**Why it matters:** The eval does not know how the slice was built. Without the guide, it cannot find the slice to test it, or it must read the code, and then it is no longer a test from the outside.
**Example:**
- Clinic. Asked: "How does the eval for 'Self-booking' learn to use it?" → Answer: from its usage guide: "Open https://clinic.example/book in a browser, pick a doctor, pick a free slot, give a phone number."
- Shop. Asked: "How does the eval for 'Pay without an account' learn to use it?" → Answer: from its usage guide: "In the mobile app, add an item to the cart, tap 'Pay as guest', give a card."
- Bank. Asked: "How does the eval for 'One-day decision' learn to use it?" → Answer: from its usage guide: "Send the application to the endpoint POST /applications, then ask GET /applications/<id>/decision."

## Agreed, no change

These four are agreed and locked. Their text is kept here word for word.

### Q7 (changed)

**Question:** Given a business intent, what does its plan hold?
**Answer (what the model gives back):** The one plan for that business intent. It holds every slice that serves the intent, one epic for each slice, the stories in each epic, the spikes, chores and bugs under each story, and the state of each one. The plan is a file; the link "slice serves business intent" tells it which slices to hold.
**Why it matters:** Today the plan "picks" a slice by two tests, so it does the slice work again. With this, the plan reads the links and only does the work.
**Example:**
- Clinic. Asked: "What does the plan for 'Patients book their own appointments online' hold?" → Answer: two slices, "Self-booking" and "Cancel online", with one epic each; in "Self-booking", the story "Pick a free slot" is done and "Send a reminder" is open.
- Shop. Asked: "What does the plan for 'Shoppers can check out without an account' hold?" → Answer: one slice, "Pay without an account", with its epic; the story "Guest checkout" is done and has one open bug, "Card fails on mobile".
- Bank. Asked: "What does the plan for 'Small businesses get a loan decision in one day' hold?" → Answer: two slices, "One-day decision" and "Upload once", with one epic each; the story "Score the application" is in work now.

### Q25 (changed)

**Question:** Given a business intent, which slices serve it?
**Answer (what the model gives back):** The list of slices that have the link "serves" to that business intent. `/shape-slice` writes this link when it shapes the slice.
**Why it matters:** Today nothing in the model links a slice to a business intent, so a plan must work out the slices again each time.
**Example:**
- Clinic. Asked: "Which slices serve 'Patients book their own appointments online'?" → Answer: "Self-booking" and "Cancel online".
- Shop. Asked: "Which slices serve 'Shoppers can check out without an account'?" → Answer: "Pay without an account".
- Bank. Asked: "Which slices serve 'Small businesses get a loan decision in one day'?" → Answer: "One-day decision" and "Upload once".

### Q27 (new)

**Question:** Given a slice, which business intents does it serve?
**Answer (what the model gives back):** The list of business intents the slice has the link "serves" to. A slice can serve more than one business intent.
**Why it matters:** Without it, nobody can see why a slice exists, or which intents a change to the slice touches.
**Example:**
- Clinic. Asked: "Which business intents does 'Send a reminder by text' serve?" → Answer: "Patients book their own appointments online" and "Fewer patients miss their appointment".
- Shop. Asked: "Which business intents does 'Pay without an account' serve?" → Answer: "Shoppers can check out without an account".
- Bank. Asked: "Which business intents does 'Upload once' serve?" → Answer: "Small businesses get a loan decision in one day" and "Customers give their documents only once".

### Q30 (new)

**Question:** When a new slice is shaped for a business intent that already has a plan, which plan holds it?
**Answer (what the model gives back):** The one plan that already exists for that business intent. The plan adds the new slice and its epic. A business intent never has a second plan.
**Why it matters:** Without it, a second slice for the same intent can start a second plan, and the work for one intent is split in two.
**Example:**
- Clinic. Asked: "'Cancel online' is shaped for 'Patients book their own appointments online'. Which plan holds it?" → Answer: plan #340, the plan for that intent; it now holds "Self-booking" and "Cancel online".
- Shop. Asked: "'Save the card for next time' is shaped for 'Shoppers can check out without an account'. Which plan holds it?" → Answer: plan #120; it now holds two slices.
- Bank. Asked: "'Upload once' is shaped for 'Small businesses get a loan decision in one day'. Which plan holds it?" → Answer: plan #51; it now holds "One-day decision" and "Upload once".

## What stays, and what is not a question

Q1 to Q6, Q8 to Q24 and Q26 stay as they are. The answers to Q1 and Q6 will name the new links in a later stage; their words do not change.

Some parts of the need are rules, not questions. They are set at the links stage:
- "A slice has a screen or surface a person can test end to end" becomes a Slice rule.
- "A builder never reads the slice's eval" becomes a rule.
- "The build delivers a usage guide with each slice" becomes a rule.
- The plan's "two tests" go.

One action is for the write stage, and it is not an ontology change: add a line to CLAUDE.md that says a builder agent, or any skill that builds the software, never reads a plan's evals folder (`.garura/project/plans/<plan-id>/evals/`).

Who does what, in the shaping loop: `/shape-slice` shapes the slice and writes the link "slice serves business intent" (Q25), and stops; the plan play makes the plan or adds the slice to it (Q30), and creates the epic and its stories (Q7); the eval play builds the slice's eval from that epic and those stories (Q28, Q29).
