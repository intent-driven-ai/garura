# Draft — the properties, links and rules (stage: links, steps 5 and 6) — #826

You decide if the properties and rules below are correct for the three kinds that change: the Story, the Slice and the Plan. They put your two agreed answers into the ontology: the Story holds the goal, the constraints, the Context guidance and the expectations, and never a failure or a recovery condition; the plan play writes those conditions into one hidden file in the slice's eval folder. One point needs your choice (Decision 3): which reader of the eval gets which part, so that the eval-author and validator columns of the routing table also stay true word for word. No relationship changes, and no other kind changes.

How to read this draft: for each property or rule that changes, the v9 text and the proposed v10 text are side by side. "(new)" means v9 has no text there. Text that does not change is not shown.

## Story (changes)

### Properties

| Property | v9 | v10 (proposed) | Required |
|----------|----|----------------|----------|
| Scope of work | "Its own words for its work, written when it is made from its feature's ICE and its capability's ICE, on the issue — in place of the v6 ICE copy. It says what the feature must do, what is expected, and what must never happen; its slice's eval tests those things" | "Its own words for its work, written by the plan play when it makes the story from its feature's ICE and its capability's ICE, on the issue. It says what the feature must do (the goals), inside which limits (the constraints), and what is expected (the scenarios, what "done" means, and the quality needs). It never says what must never happen, and it holds no recovery condition. Its slice's eval tests those things" | yes |
| Context guidance | (new) | "The four Context lines of its two ICE, in its own words, on the issue: what to read, what never to read, the persona, and what is in and what is out. It says where to look; it holds no facts. The build play's context sub-agent reads it and collects the context; the eval play reads it" | yes |
| Written from | "The two ICE it read" | no change | yes |

The Context guidance is its own property, not a part of "Scope of work". So the word "Scope" (the ICE Context line: what is in and out) and "Scope of work" (this property) stay apart. Neither is renamed.

### Relationships

No change. The story is still written from two ICE. The collected context and the hidden file are files, not kinds, so no new link is needed.

### Rules

| v9 | v10 (proposed) |
|----|----------------|
| (new) | It never holds a failure condition or a recovery condition — not in its scope of work, its Context guidance, its title or its examples. The plan play puts them in its slice's hidden file. |
| (new) | It holds the Context guidance, never the context itself. |
| (new) | When the build play runs, its context sub-agent reads the story's Context guidance, collects the context, and puts it in the issue's short-term memory, `.garura/project/issues/<issue>/`. The sub-agent never opens an ICE page and never reads a plan's evals folder, also when the guidance names it. The builder reads the story and that collected context, and never an ICE page. |
| "Its two ICE are the ICE of its feature and the ICE of that feature's capability. The ICE pages stay the source; the scope is the story's own words." | "Its two ICE are the ICE of its feature and the ICE of that feature's capability. The ICE pages stay the source; the scope of work and the Context guidance are the story's own words." |
| "When one of those ICE changes after the story is made, the scope is drift for the Alignment loop; it is not changed without a word." | "When one of those ICE changes after the story is made, its scope of work, its Context guidance and its entry in the slice's hidden file are drift for the Alignment loop. They are not changed without a word, and they are made again together, from the same two ICE, so the story and the hidden file never disagree." |

### What it is (one sentence changes)

- v9: "it reads its Feature's ICE and that Feature's Capability's ICE, and writes its own scope of work from them. Its Slice's eval reads that scope of work to test it."
- v10: "it is written from its Feature's ICE and that Feature's Capability's ICE: its scope of work (goals, constraints, expectations) and its Context guidance. The failure and recovery conditions of those two ICE go to its slice's hidden file, never to the story. Its Slice's eval play reads the story to build the eval."

### Example (v10)

> **Shop — Story #122 "Guest checkout"**, in Epic "Pay without an account". Delivers Feature "Guest checkout", part of Capability Checkout. Scope of work: "A shopper pays by card with an email only; no account is made; returns do not change. Expected: the shopper sees an order number; a guest pays by card in under two minutes." Context guidance: "Read: the payment rules. Never read: saved card data. Persona: the guest shopper on mobile. In: card and wallet; out: saved addresses." Written from: ICE of Feature "Guest checkout", ICE of Capability "Checkout". When the build play runs, its context sub-agent puts the payment rules in `.garura/project/issues/122/`; the builder reads them there.
>
> **Clinic — Story #342 "Pick a free slot"**, in Epic "Self-booking". Scope of work: "A patient picks a free slot and it is booked, only from slots the doctor opened. Expected: the booked slot shows on the confirmation page." Context guidance: "Read: the clinic's opening hours. Never read: patient health records. Persona: the patient on a phone. In: open slots; out: moving a booking." Children: Chore "Add the slots table", Bug "Two patients get the same slot".
>
> **Bank — Story #55 "Score the application"**, in Epic "One-day decision". Scope of work: "Each application gets a score, from the sent documents only. Expected: the score is on the application within one hour." Context guidance: "Read: the lending policy. Never read: other customers' accounts. Persona: the credit officer. In: the documents sent; out: credit bureau data." Written from the ICE of Feature "Score the application" and the ICE of Capability "Credit decision".

v9 text that goes: "no card is charged twice", "no slot is booked twice", "no decision goes out without a score", and "The eval for 'Pay without an account' tests that no account is made and no card is charged twice."

The Bug title "Two patients get the same slot" stays. It names a symptom, as the Symptom-Based Feedback Protocol says (`idd-principles.md`), not a failure condition or a check.

## Slice (changes)

### The hidden file — `failure-and-recovery.md` (a part of the slice's eval, not a kind)

**Where it is:** `.garura/project/plans/<plan-id>/evals/<slug>/failure-and-recovery.md`, in the eval folder of the slice's home plan. There is one for each slice.

| Property | What it holds | Required |
|----------|---------------|----------|
| Slice | The slice it is for | yes |
| Written by | The plan play, when it creates the slice's epic and stories, from the same two ICE as each story | yes |
| Read by | The eval play, all of it, to build the eval. The eval, when it runs, reads the recovery conditions. A person reads all of it when work is sent to a person (the barrier is for agents, not for people) | yes |
| Never read by | A builder; any skill that builds the software; the build play's context sub-agent | yes |
| Entries | One entry for each story in the slice's epic | yes |

What each entry holds:

| Part | What it holds | Required |
|------|---------------|----------|
| Story | The story's issue and title, and its feature | yes |
| Written from | The two ICE (the same as the story's "Written from") | yes |
| Failure conditions | Each "Fails if" line of the two ICE, in the plan play's words, each with a short id (F1, F2, …). The id is for the eval and for people only; it never leaves this folder. When the two ICE have no "Fails if" line, the entry says "none", so a missing entry and an empty one are not the same | yes |
| Recovery condition | Exactly one for each failure condition (Decision 1, by `standards/rules/expectation-generation.md`): **when** — what the eval sees when it fails, as a symptom; **way back** — how to get back to a good state, as guidance, never as code; **who fixes** — "the builder can fix this alone" or "a person must decide" | yes, one for each failure condition |

Example of one entry, for each persona:

> **Clinic — `.garura/project/plans/340/evals/self-booking/failure-and-recovery.md`**, entry for Story #342 "Pick a free slot" (Feature "Pick a free slot"; written from the ICE of "Pick a free slot" and of "Booking").
> F1 — Fails if: a slot is booked twice.
> Recovery — When: two bookings are on one slot. Way back: keep the first booking, free the second, tell the second patient. Who fixes: the builder can fix this alone.
>
> **Shop — `.garura/project/plans/120/evals/pay-without-an-account/failure-and-recovery.md`**, entry for Story #122 "Guest checkout" (written from the ICE of "Guest checkout" and of "Checkout").
> F1 — Fails if: a guest is asked to sign up before paying. Recovery — When: a sign-up page shows before the payment page. Way back: go to the payment page with the email only. Who fixes: the builder can fix this alone.
> F2 — Fails if: a card is charged twice. Recovery — When: one order has two charges. Way back: refund the second charge. Who fixes: a person must decide, because money goes out.
>
> **Bank — `.garura/project/plans/51/evals/one-day-decision/failure-and-recovery.md`**, entry for Story #55 "Score the application" (written from the ICE of "Score the application" and of "Credit decision").
> F1 — Fails if: a decision goes out without a score. Recovery — When: a decision has no score. Way back: hold the decision until the score exists. Who fixes: the builder can fix this alone.

### Properties and "Lives at"

| Item | v9 | v10 (proposed) |
|------|----|----------------|
| Eval (property) | "Its one eval: it tests, from the outside, on the built product, what its epic delivers as its stories describe it — every intent and expectation the stories carry is met, and no failure condition they name happens. Built by the eval play from the epic and stories the plan play wrote; kept in its home plan's evals folder" | "Its one eval: it tests, from the outside, on the built product, what its epic delivers — every goal and expectation its stories carry is met, and no failure condition in its hidden file happens. Built by the eval play from the epic, the stories and the hidden file the plan play wrote; kept in its home plan's evals folder, beside the hidden file" |
| Lives at (one sentence) | "Its eval is at `.garura/project/plans/<plan-id>/evals/<slug>/` and its usage guide at …" | "Its eval and its hidden file `failure-and-recovery.md` are at `.garura/project/plans/<plan-id>/evals/<slug>/` and its usage guide at …" (the rest stays) |

### Relationships

No change.

### Rules

| v9 | v10 (proposed) |
|----|----------------|
| "A builder agent, or any skill that builds the software, never reads its eval, and never reads a plan's evals folder." | "A builder agent, any skill that builds the software, or the build play's context sub-agent never reads its eval or its hidden file, and never reads a plan's evals folder." |
| "Its eval reads only its epic, the stories in that epic and its usage guide. It never reads the ICE of a feature or a capability, so the ICE has one interpretation: the one the plan play wrote into the epic and its stories. It never reads the code. It reads the guide when it runs, after the build." | (proposed, see Decision 3) "Its eval reads four things, at two times. The eval play, when it builds the eval, reads its epic, the stories in that epic (their scope of work and Context guidance) and its hidden file — never the usage guide or the code, which are what the build makes. The eval, when it runs after the build, reads the eval, the usage guide, the Context guidance the eval play put in the eval, and the recovery conditions in the hidden file — and reaches the built product only through the guide. Neither reads the ICE of a feature or a capability, so the ICE has one interpretation: the one the plan play wrote into the epic, its stories and the hidden file." |
| (new) | "It has one hidden file, `failure-and-recovery.md`, in its eval folder. The plan play writes it from the same two ICE as each story: each story of its epic has one entry, with its failure conditions and exactly one recovery condition for each." |
| (new) | "When its eval finds a failure, it writes a handoff plan from the recovery condition: what the product does wrong, as a symptom, and the way back. The handoff plan never names the failure condition, its id or the check. When the recovery condition says "the builder can fix this alone", the handoff plan goes to the builder; when it says "a person must decide", it goes to a person. Where the handoff plan is kept, and how it reaches the builder, is not part of this ontology change." |
| (new) | "When its epic gains a story (its slice gains a feature), the plan play adds that story's entry to the hidden file in the home plan's folder, for whichever plan it runs." |
| "It has one eval and one usage guide, also when two plans hold it. Both are kept in the folder of its home plan … Another plan that holds it points to them and never copies them." | "It has one eval, one hidden file and one usage guide, also when two plans hold it. All three are kept in the folder of its home plan … Another plan that holds it points to them and never copies them." |

### Example (v10, the Clinic sentence that changes)

- v9: "Eval: `.garura/project/plans/340/evals/self-booking/` — it reads Epic #341 and its Stories "Pick a free slot" and "Send a reminder", and tests that a patient books a free slot and gets a reminder, and that no slot is booked twice. … The builder of "Pick a free slot" reads its Story, never the eval."
- v10: "Eval: `.garura/project/plans/340/evals/self-booking/`, beside its hidden file `failure-and-recovery.md`. The eval play reads Epic #341, its Stories "Pick a free slot" and "Send a reminder" and the hidden file, and builds an eval that tests that a patient books a free slot and gets a reminder, and that no slot is booked twice. When the eval finds two bookings on one slot, the builder gets: "Two patients can book the same 10:00 slot when they book at the same time. Make the second one see that the slot is gone." The builder of "Pick a free slot" reads its Story and the context in `.garura/project/issues/342/`, never the eval folder."

## Plan (changes)

| Item | v9 | v10 (proposed) |
|------|----|----------------|
| What it is (one sentence added after "(3) it creates …") | — | "When it creates the stories of an epic, it also writes the slice's hidden file, from the same two ICE of each story, with exactly one recovery condition for each "Fails if" line. So it interprets each ICE once." |
| Lives at | "… which holds `evals/` (one folder for each slice whose eval is kept here) and `guides/` (one guide for each such slice)" | "… which holds `evals/` (one folder for each slice whose eval is kept here, with its hidden file `failure-and-recovery.md` and its eval) and `guides/` (one guide for each such slice)" |
| Folder (property) | "Beside the plan file: `evals/` (written by the eval play) and `guides/` (written by the build), one entry for each slice whose home plan it is. A slice it holds whose home is another plan is pointed to from its Tree, never copied" | "Beside the plan file: `evals/<slug>/`, which holds the hidden file `failure-and-recovery.md` (written by the plan play) and the eval (written by the eval play), and `guides/` (written by the build), one entry for each slice whose home plan it is. A slice it holds whose home is another plan is pointed to from its Tree, never copied" |

### Rules

| v9 | v10 (proposed) |
|----|----------------|
| (new) | "When it creates a slice's epic and stories, the plan play writes the slice's hidden file from the same two ICE as each story: for each "Fails if" line, exactly one recovery condition, by `standards/rules/expectation-generation.md`, marked "the builder can fix this alone" or "a person must decide". It puts the goals, constraints, Context guidance and expectations in the story, and the failure and recovery conditions in the hidden file, never both in one place." |
| (new) | "The plan play reads all of each ICE, so it is not a builder. No builder reads what it writes into `evals/`." |
| "Its folder keeps the eval and the usage guide of each slice whose home plan it is … it points to that plan's eval and guide, and never copies them." | "Its folder keeps the hidden file, the eval and the usage guide of each slice whose home plan it is … it points to that plan's hidden file, eval and guide, and never copies them." |

### Example (v10, the Clinic folder sentence)

- v9: "Folder: `.garura/project/plans/340/evals/self-booking/`, `evals/cancel-online/`, and their two guides."
- v10: "Folder: `.garura/project/plans/340/evals/self-booking/` and `evals/cancel-online/`, each with its hidden file `failure-and-recovery.md` (written by the plan play) and its eval (written by the eval play), and their two guides."

## Kinds that do not change

- **ICE.** Its rule "No work item carries it. Only a Story reads it" stays true word for word: the plan play reads the two ICE when it makes the story, and writes the hidden file in the same act; the hidden file is not a work item; the context sub-agent reads the story's guidance, not the ICE page.
- **Epic.** It names no failure condition. The eval play reads it, as in v9.
- **Business Intent, Source, Domain, Capability, Feature, Spike, Chore, Bug.** No change.

## Drift and the two-plans case (summary)

- **Drift.** When one of a story's two ICE changes after the story is made, three things are drift: the story's scope of work, its Context guidance, and its entry in the hidden file. The Alignment loop shows them. They are made again together, from the same two ICE, so they never disagree.
- **Two plans hold one slice.** The slice has one hidden file, in its home plan's folder, as its eval and guide are. The other plan points to it and never copies it. When the epic gains a story, that story's entry goes into the home plan's file, whichever plan the plan play runs for.

## Decision 3 — Which reader of the eval gets which part (your choice)

**Question:** The eval has two readers at two times: the eval play, which builds the eval before the build, and the eval itself, which runs on the built product. Should each read only what its column of the routing table gives it?
**Answer (recommended):** Yes. The eval play reads the epic, the stories and the hidden file — all of the ICE as the plan play wrote it — and never the usage guide or the code, because those are what the build makes. The eval, when it runs, reads the eval, the usage guide, the Context guidance (the eval play puts it in the eval) and the recovery conditions; it does not read the stories, so it does not take the goals and constraints straight from them. The other way: keep the v9 words "the eval reads the epic, the stories and the guide", with no split by time.
**Why it matters:** The routing table says the eval author never gets the builder's output, and the usage guide is the builder's output. It also marks the goal and constraints ✗ for the validator. With no split, a strict reader can say that the eval breaks both rows. With the split, each column is true word for word.
**Example:**
- Clinic. The eval play reads Epic #341, Stories #342 and #343 and the hidden file, and builds the checks for "Self-booking" before the booking page exists. After the build, the eval opens https://clinic.example/book by the guide, runs the checks, and finds two bookings on one slot. It reads the recovery condition and tells the builder: "Two patients can book the same 10:00 slot."
- Shop. The eval play builds the checks for "Pay without an account" from Epic #121, its stories and the hidden file. It never sees the mobile app. The eval runs the checks in the app by the guide, finds a double charge, reads "a person must decide", and sends the handoff plan to a person.
- Bank. The eval play builds the checks for "One-day decision" from Epic #52, its stories and the hidden file. The eval calls POST /applications by the guide, finds a decision with no score, and tells the builder: "A decision goes out while the score is still running."

## Check — the routing table and v10

Each row of "The Routing Table" (`docs/philosophy/idd-principles.md`), and how v10 keeps it true. "Builder" is the agent that builds a story. "Eval author" is the eval play. "Validator" is the eval when it runs.

| ICE element | Builder | Eval author | Validator | How v10 keeps it true |
|-------------|---------|-------------|-----------|-----------------------|
| Goal (Intent) | ✓ | ✓ | ✗ | In the story's scope of work, which the builder and the eval play read. The running eval does not read the stories (Decision 3). |
| Constraints (Intent) | ✓ | ✓ | ✗ | The same as the goal. |
| Failure conditions (Intent) | ✗ | ✓ | via evals | Only in the hidden file, which no builder and no context sub-agent reads; never in the story (Story rule). The eval play reads the file and puts them into the eval. |
| Context | ✓ (all) | ✓ | ✓ | The story holds the Context guidance (all four lines of both ICE). The context sub-agent collects the context into the issue's short-term memory for the builder. The eval play reads the guidance in the stories and puts it in the eval for the run. |
| Success scenarios (Expectation) | ✓ | ✓ | via evals | In the story's scope of work, as "what is expected". The eval play puts them into the eval. |
| Recovery (Expectation) | only the handoff plan | — | ✓ (builds the handoff plan) | Only in the hidden file. The running eval reads them and writes the handoff plan, which names the symptom and the way back, never the condition. The builder gets only that plan. |
| Encrypted evals | ✗ never | produces | ✓ (decrypts) | The eval play writes the eval in the eval folder; no builder reads that folder (Slice rule, CLAUDE.md). As in v9, the eval is kept from the builder by that read rule, not by encryption. This change does not touch that. |
| Implementation | produces | ✗ | ✓ | The builder builds and writes the usage guide outside the eval folder. The eval play never reads the guide or the code (Decision 3). The running eval reaches the built product through the guide. |

Also kept: the Symptom-Based Feedback Protocol (the handoff plan names a symptom, never an id), the Convergence Protocol (a recovery marked "a person must decide" goes to a person, where the barrier drops), and the classification rule (the plan play keeps "Fails if" lines out of the story's constraints).

## Carried to the write stage

- Q26 and Q32 gain the Context guidance (agreed at the kinds stage).
- Q26 and Q34: "Checkout" in place of "Payments", "Credit decision" in place of "Lending" (the v9 names).
- If you choose the recommended answer to Decision 3, Q29's answer gains the two times: the eval play reads the epic, the stories and the hidden file; the eval, when it runs, reads the guide, the Context guidance in the eval and the recovery conditions.
- The version goes from 9 to 10, with the one combined log line from the kinds draft (it gains the Context guidance property and, if chosen, the split by time).
- Q35's Shop example sends the double-charge handoff plan to the builder ("Make the second tap do nothing"), but Decision 1 (agreed) marks that recovery "a person must decide". At the write stage, Q35's Shop example says the handoff plan goes to a person, or uses a failure the builder can fix alone (for example, a guest is asked to sign up before paying).
