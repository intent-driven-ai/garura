# Draft — the properties, links and rules (stage `links`, steps 5–6) — #816

At this checkpoint you decide what each of the five changed kinds holds, how they link, and what must always be true. The main decisions: a slice says which business intents it serves; each business intent has one plan, which holds those slices and does no slice work again; each slice has one eval and one usage guide, and a builder never reads the eval. The two open points from the kinds draft are settled below as rules (Slice, items S6 and S8), for you to say yes or change.

The kinds are agreed (checkpoint 2). Only Slice, Plan, Business Intent, Epic and Story change. ICE, Feature, Capability, Source, Domain, Spike, Chore and Bug do not change. No new kind is made.

## Slice

### S1 — Property, new: the business intents it serves

**What:** A slice names one or more business intents that it serves. The first one in the list is the intent it was first shaped for. `/shape-slice` writes this link when it shapes the slice. It writes nothing else: no plan, no epic, no story, no eval.
**Why:** Q25 (which slices serve an intent) and Q27 (which intents a slice serves). The first-in-list order is needed by S6 and S8.
**Example:**
- Clinic — "Self-booking" serves "Patients book their own appointments online".
- Shop — "Pay without an account" serves "Shoppers can check out without an account".
- Bank — "Upload once" serves "Small businesses get a loan decision in one day" (first) and "Customers give their documents only once".

### S2 — Link, new: a slice serves a business intent

**What:** Slice → Business Intent, many. "It serves this business intent." It is the same verb, with the same meaning, as "a capability serves a business intent" and "an epic serves a business intent". The link is kept on the slice's entry in the product model.
**Why:** Q25, Q27, Q30.
**Example:**
- Clinic — "Self-booking" serves "Patients book their own appointments online"; "Cancel online" serves it too.
- Shop — "Pay without an account" serves "Shoppers can check out without an account".
- Bank — "One-day decision" and "Upload once" both serve "Small businesses get a loan decision in one day".

### S3 — Link, changed: a plan holds it

**What:** Plan → Slice, many. "A plan picks it" becomes "a plan holds it". A slice that serves two intents is held by two plans.
**Why:** Q7 and Q30. "Picks" and its two tests go (agreed at checkpoint 2).
**Example:**
- Clinic — plan 340 holds "Self-booking" and "Cancel online".
- Shop — plan 120 holds "Pay without an account".
- Bank — "Upload once" is held by plan 51 and by the plan for "Customers give their documents only once".

### S4 — Rule, moved to Slice: a person can test it end to end

**What:** A slice has one screen or surface that a person can test end to end. A thing with no such surface is not a slice, and `/shape-slice` does not shape it. This rule takes the place of "a slice with no surface fails the Plan's first test, and is never picked".
**Why:** The need, item 3; the kinds draft moved this rule from the Plan to the Slice.
**Example:**
- Clinic — "Self-booking" has the booking page in a browser.
- Shop — "Pay without an account" has the checkout in the mobile app.
- Bank — "Rate tables" changes only tables that no person sees, so it is not a slice.

### S5 — Property, new: its eval

**What:** A slice has one eval. The eval play builds it, right after the plan play made the epic and its stories. The eval tests, from the outside, on the built product, what the slice's epic delivers as its stories describe it: every intent and expectation the stories carry is met, and no failure condition they name happens.
**Why:** Q28 (where it is kept) and Q29 (what it tests).
**Example:**
- Clinic — the eval for "Self-booking" tests that a patient books a free slot and gets a reminder, and that no slot is booked twice.
- Shop — the eval for "Pay without an account" tests that a shopper with no account pays and gets a receipt, and that no card is charged twice.
- Bank — the eval for "One-day decision" tests that a small business gets a decision on the same day, and that no decision goes out without a score.

### S6 — Rule, new (open point a, settled): where the eval is kept, when a slice is in two plans

**What:** The eval is kept in the folder of the plan for the intent the slice was first shaped for: in that plan's evals folder, in one folder for the slice. A slice has one eval, also when two plans hold it. The other plan points to that folder. It never copies it.
**Why:** Q28. Two copies of one eval can say different things, and then the slice has two tests for one outcome.
**Example:**
- Clinic — the eval for "Self-booking" is in plan 340's evals folder, in the folder "self-booking".
- Shop — the eval for "Pay without an account" is in plan 120's evals folder, in the folder "pay-without-an-account".
- Bank — "Upload once" was first shaped for "Small businesses get a loan decision in one day", so its eval is in plan 51's evals folder. The plan for "Customers give their documents only once" points to that folder.

### S7 — Rule, new: a builder never reads the eval

**What:** A builder agent, or any skill that builds the software, never reads a slice's eval, and never reads a plan's evals folder.
**Why:** Q28. A builder that reads the eval can build only to pass it.
**Example:**
- Clinic — the builder of "Self-booking" reads Story "Pick a free slot", not the eval.
- Shop — the builder of "Guest checkout" never opens plan 120's evals folder.
- Bank — the builder of "Score the application" does not know what the eval for "One-day decision" checks.

### S8 — Property and rule, new (open point b, settled): its usage guide

**What:** The build delivers a usage guide with each slice. The guide says what the surface is (a browser page, a mobile app, a command line command or a backend endpoint), how to reach it, and the steps a person takes. It is kept in the same plan folder as the eval, in a guides folder beside the evals folder but not in it, so the builder writes the guide and never sees the eval. A slice has one guide, also when two plans hold it.
**Why:** Q31 (how the eval learns to use the slice). The need, item 4 (the builder never reads the eval).
**Example:**
- Clinic — guide for "Self-booking", in plan 340's guides folder: "Open the booking page in a browser, pick a doctor, pick a free slot, give a phone number."
- Shop — guide for "Pay without an account", in plan 120's guides folder: "In the mobile app, add an item to the cart, tap 'Pay as guest', give a card."
- Bank — guide for "One-day decision", in plan 51's guides folder: "Send the application to the applications endpoint, then ask for its decision."

### S9 — Rule, new: what the eval reads

**What:** The eval reads only the slice's epic, the stories in that epic, and the slice's usage guide. It never reads the ICE of a feature or a capability. It never reads the code. It reads the guide when it runs, after the build.
**Why:** Q29 and Q31. The plan play makes the one interpretation of the ICE, in the epic and its stories. If the eval read the ICE too, two things could interpret it in different ways. If it read the code, it would not test from the outside.
**Example:**
- Clinic — the eval for "Self-booking" reads Epic 341, Stories "Pick a free slot" and "Send a reminder", and the guide. It does not open the ICE of "Booking".
- Shop — the eval for "Pay without an account" reads Epic 121, Stories "Guest checkout" and "Send receipt", and the guide. It does not read the app's code.
- Bank — the eval for "One-day decision" reads Epic 52, Stories "Upload documents" and "Score the application", and the guide.

### S10 — Rules, changed in words

**What:** Two rules change their words because "picks" goes. (1) "A second plan that picks it uses that Epic" becomes "A second plan that holds it uses that Epic, and the Epic then serves both business intents." (2) "Whether it is picked is shown by its Epic" becomes "Whether its work has started is shown by its Epic." In the tracker it is still one Epic, now made when the plan play adds the slice to a plan.
**Why:** Q7 and Q30.
**Example:**
- Clinic — "Self-booking" has Epic 341; its work has started.
- Shop — "Pay without an account" has Epic 121.
- Bank — "Upload once" is in two plans and has one epic.

## Plan

### P1 — Rule, new: one plan for each business intent

**What:** A business intent has one plan, and never a second one. When a new slice is shaped for an intent that has a plan, the plan play adds the slice and its epic to that plan.
**Why:** Q30.
**Example:**
- Clinic — "Cancel online" is shaped for the clinic's booking intent; the plan play adds it to plan 340.
- Shop — "Save the card for next time" is shaped for the guest checkout intent; plan 120 now holds two slices.
- Bank — "Upload once" is added to plan 51; no second plan is made.

### P2 — Link, changed: it holds the slices that serve its intent

**What:** Plan → Slice, many. "It picks a slice by the two tests" becomes "It holds every slice that serves its business intent." The plan finds them by reading the link "slice serves business intent". It does no slice work again.
**Why:** Q7 and Q25.
**Example:**
- Clinic — plan 340 reads the link and finds "Self-booking" and "Cancel online".
- Shop — plan 120 finds "Pay without an account".
- Bank — plan 51 finds "One-day decision" and "Upload once". It does not rank them or test them.

### P3 — Rule, removed: the two tests

**What:** The rule "it picks a slice by two tests" goes. Test 1 (a surface a person can test) is now the Slice's own rule (S4). Test 2 (the slice with the most features that serve the intent) goes with nothing in its place: the person chose the slice at `/shape-slice`.
**Why:** The need, item 2; agreed at checkpoint 2.
**Example:**
- Clinic — plan 340 does not compare "Self-booking" with "Cancel online"; it holds both.
- Shop — plan 120 does not count features.
- Bank — "Rate tables" is never held by a plan, because it is not a slice (S4).

### P4 — Rule, changed: its three steps

**What:** The plan does three things, in this order: (1) it is given one business intent; (2) it holds the slices that serve it; (3) it creates one epic for each slice, or uses the one that exists, and the stories of that epic. The plan play does these steps right after `/shape-slice`, with no stop between them.
**Why:** Q7. Step 3 gains "and the stories of that epic" (decided at checkpoint 2).
**Example:**
- Clinic — plan 340 is given the booking intent, holds "Self-booking", and creates Epic 341 with Stories "Pick a free slot" and "Send a reminder".
- Shop — plan 120 holds "Pay without an account" and creates Epic 121 with Stories "Guest checkout" and "Send receipt".
- Bank — plan 51 holds "Upload once", which already has an epic from the other plan; it uses that epic.

### P5 — Property, new: its folder

**What:** Each plan has one folder, beside its plan file. The folder holds an evals folder (one folder for each slice whose eval is kept here) and a guides folder (one guide for each such slice). The plan file stays where it is. The eval play writes into the evals folder; the build writes into the guides folder.
**Why:** Q28 and Q31, and S6, S8.
**Example:**
- Clinic — plan 340's folder holds the evals for "Self-booking" and "Cancel online", and their two guides.
- Shop — plan 120's folder holds the eval and the guide for "Pay without an account".
- Bank — plan 51's folder holds the evals and guides for "One-day decision" and "Upload once". The other plan's folder holds no copy of the "Upload once" eval.

### P6 — Rule, new: a shared slice's eval is pointed to, never copied

**What:** When a plan holds a slice whose eval is kept in another plan's folder (S6), the plan points to that eval and that guide. It never copies them.
**Why:** Q28 and open point (a).
**Example:**
- Clinic — no shared slice yet; nothing to point to.
- Shop — "Pay without an account" also serves "Shoppers pay in one minute"; that plan points to plan 120's eval.
- Bank — the plan for "Customers give their documents only once" points to plan 51's eval for "Upload once".

## Business Intent

### B1 — Link, new: a slice serves it

**What:** Slice → Business Intent, many. "A slice serves it." The business intent stays a destination: it does not point at its slices. Its slices are found from the slices' side (S2).
**Why:** Q25, Q27 and Q30.
**Example:**
- Clinic — "Patients book their own appointments online" is served by "Self-booking" and "Cancel online".
- Shop — "Shoppers can check out without an account" is served by "Pay without an account".
- Bank — "Small businesses get a loan decision in one day" is served by "One-day decision" and "Upload once".

### B2 — Rule, changed in words: what points at it

**What:** The rule "sources, capabilities, its plan and its epics point at it" becomes "sources, capabilities, slices, its plan and its epics point at it". Its Clinic example loses "Its plan picked Slice ...", and says "It is served by Slice 'Self-booking'; its plan created Epic 'Self-booking'."
**Why:** Q25; "picks" goes.
**Example:**
- Clinic — "It is served by Slice 'Self-booking'."
- Shop — "It is served by Slice 'Pay without an account'."
- Bank — "It is served by Slices 'One-day decision' and 'Upload once'."

## Epic

### E1 — Link, changed in meaning: it serves what its slice serves

**What:** Epic → Business Intent, many, stays. Its meaning is now stated: an epic serves the business intents its slice serves. It does not get its own list of intents apart from its slice.
**Why:** Q7 and Q30.
**Example:**
- Clinic — Epic 341 serves the booking intent, because "Self-booking" does.
- Shop — Epic 121 serves the guest checkout intent and, later, "Shoppers pay in one minute".
- Bank — the epic of "Upload once" serves both intents that "Upload once" serves.

### E2 — Rule, new: its eval reads it, so its title says what a person sees

**What:** The slice's eval reads the epic, with its stories, to learn what it delivers. So its title (what it delivers, in one line) says what a person can see the product do, not how it is built.
**Why:** Q29.
**Example:**
- Clinic — Epic 341: "A patient books a free slot online and gets a reminder." Not: "Add the slots table and the text service."
- Shop — Epic 121: "A shopper with no account pays and gets a receipt."
- Bank — Epic 52: "A small business gets a loan decision on the same day."

### E3 — Rule, changed in words: a second plan

**What:** "When a second plan picks the same slice, it uses this epic" becomes "When the slice is in a second plan, that plan uses this epic, and the epic serves both business intents." Its link "a plan created it" does not change: the plan play creates it, with its stories. In the "What it is" line, "each Slice a Plan picks" becomes "each Slice a Plan holds".
**Why:** Q7 and Q30; "picks" goes.
**Example:**
- Clinic — Epic 341 is used by plan 340 only.
- Shop — when "Shoppers pay in one minute" gets its plan, that plan uses Epic 121.
- Bank — plan 51 and the plan for "Customers give their documents only once" use the one epic of "Upload once".

## Story

### T1 — Property, changed in words: its scope of work is what the eval tests

**What:** The scope of work stays the story's own words, written when the plan play makes it, from its feature's ICE and that feature's capability's ICE. Its description now says what it carries: what the feature must do, what is expected, and what must never happen. The slice's eval reads it to test those things.
**Why:** Q29. The eval tests every intent and expectation the stories carry, and that no failure condition they name happens.
**Example:**
- Clinic — Story 342 "Pick a free slot": "A patient picks a free slot and it is booked; no slot is booked twice."
- Shop — Story 122 "Guest checkout": "A shopper pays by card with an email only; no account is made; no card is charged twice."
- Bank — Story 55 "Score the application": "Each application gets a score; no decision goes out without a score."

### T2 — Rules, no change

**What:** The Story's rules stay as they are. Only the plan play writes it. The ICE rule "only a Story reads it" stays word for word.
**Why:** Q29: one interpretation of the ICE, in the stories.
**Example:**
- Clinic — Story 342 is still written from the ICE of "Pick a free slot" and of "Booking".
- Shop — Story 122 is still written from the ICE of "Guest checkout" and of "Checkout".
- Bank — Story 55 is still written from the ICE of "Score the application" and of "Credit decision".

## Not defined, and not changed

- No kind is named that is not defined. "Eval" and "usage guide" are parts of the Slice, not kinds (agreed at checkpoint 2).
- Not an ontology change (for the write stage): the line in CLAUDE.md that a builder never reads a plan's evals folder; ADR 048 section 2 amended through `/record-decision`.

## Appendix — field names and paths (for the write stage)

| Item | Kind | Field or path |
|------|------|---------------|
| S1, S2 | Slice | spine `slices[].intents` — ordered list of business intent ids; `intents[0]` = first shaped for. Written by `/shape-slice` only |
| S3, P2 | Slice, Plan | relationship row `Plan → Slice, many, holds` (replaces `picks it by the two tests`) |
| S5, S6 | Slice | eval path, worked out, not stored: `.garura/project/plans/<issue of intents[0]>/evals/<slice slug>/` |
| S8 | Slice | guide path, worked out, not stored: `.garura/project/plans/<issue of intents[0]>/guides/<slice slug>.md` |
| S10 | Slice | "In the tracker as" line: "made when a Plan picks it" → "made when the plan play adds it to a plan"; Lives at gains `intents` in the spine field list |
| P5 | Plan | folder `.garura/project/plans/<id>/` beside `.garura/project/plans/<id>.yaml`; holds `evals/` and `guides/` |
| P6 | Plan | a shared slice's entry in the plan's Tree points to the home plan's `evals/<slug>/` and `guides/<slug>.md` |
| B1 | Business Intent | relationship row `other → this, Slice, many, A slice serves it`; no field on the intent page |
| E1 | Epic | relationship row `this → other, Business Intent, many` meaning gains "the ones its slice serves" |
| T1 | Story | property `Scope of work` description |
| S7 | — | CLAUDE.md line (write stage, not ontology) |

Why no stored path: a plan's ID is its business intent's issue number, and the slice's first intent is the one it was first shaped for. So the home plan, and with it the eval and guide paths, follow from the slice's `intents` list. One less field to keep in step.

Question for the product owner: are these the right properties, links and rules?
