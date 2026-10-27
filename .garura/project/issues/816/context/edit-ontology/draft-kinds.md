# Draft — the kinds (stage `kinds`, steps 2–4) — #816 (second redraft after checkpoint 2)

At this checkpoint you decide which kinds of things in the model change so that a slice knows the business intents it serves, a plan only reads that link, and the slice's eval tests what its epic delivers. This redraft follows your second change: three plays run one after the other, with no stop between them, as the shaping loop. `/shape-slice` only shapes the slice and writes the link "slice serves business intent"; the plan play then makes the plan, the epic and its stories; the eval play then builds the eval from that epic and those stories.

**Need:** a slice serves one or more business intents, and `/shape-slice` writes that link when it shapes the slice. Right after, the plan play makes the plan from that slice (or adds the slice to the one plan its intent already has), and creates the slice's epic and its stories. The plan no longer picks slices by two tests. The slice must have a screen or surface a person can test end to end. Then the eval play builds the slice's eval; the model names where it is kept, what it tests, and how it learns to use the built slice. The questions are agreed (checkpoint 1): Q7, Q25, Q27, Q28, Q29, Q30 and Q31. Only Q29 was corrected after checkpoint 2; its words were aligned again after this change, with no change to its meaning.

## The kinds on one screen

| Kind | This change | Questions that need it |
|------|-------------|------------------------|
| Slice | changed — serves business intents (written by `/shape-slice`); has its eval (built by the eval play; it reads its epic and stories) and its usage guide; the "testable end to end" rule is its own | Q25, Q27, Q28, Q29, Q31 |
| Plan | changed — made by the plan play, right after `/shape-slice`; holds the slices that serve its intent; creates the epic and its stories; keeps the evals; the two tests go | Q7, Q28, Q30 |
| Business Intent | changed — a slice serves it | Q25, Q27, Q30 |
| Epic | changed — the slice's eval reads it to learn what it delivers; "picks" becomes "holds"; it serves the intents its slice serves | Q7, Q29, Q30 |
| Story | changed, in words only — the slice's eval reads its scope of work; its ICE rule does not change | Q29 |
| ICE, Feature, Capability | same — the eval does not read them | — |
| Source, Domain, Spike, Chore, Bug | same — not touched | — |
| New kinds | none | — |

## Step 2 — What we reuse, and where it clashes

**Reused as they are**

- **Slice** — its features in build order, its one vertical (the screen or surface), its one epic, its place on the spine.
- **The "serves" link** — a capability already "serves" a business intent, and an epic already "serves" one. The slice uses the same verb, with the same meaning, so the model has one word for it.
- **The two-sided link** — a capability's spine entry already lists its business intents, and the intent's page lists the parts it touches. The slice's link is kept on its spine entry the same way.
- **Plan** — its file, its ID (the business intent's issue number), its tree, Now, Needs plans and Status. "One plan for each business intent" is already true (the plan's ID is the intent's number); Q30 only makes it a stated rule. "A plan creates the epic" stays as it is.
- **Epic** — one epic for each slice, shared when the slice is in two plans; a plan creates it. Its title already says "what it delivers in one line"; the eval uses that.
- **Story** — its scope of work, written from its feature's ICE and that feature's capability's ICE when its epic is made. This is where the ICE, as interpreted, already sits. The eval reads it.
- **ICE** — its rule "only a Story reads it" stays as it is. The eval does not read the ICE, so there is one interpretation of it.
- **The surface a person reaches** — ADR 048 left open where "how a person reaches the surface" lives once the epic record is gone (ADR 022). The slice's usage guide fills that gap.

**Clashes**

| Clash | Today (v8) | Now | What we do |
|-------|-----------|-----|-----------|
| "picks" | A plan picks a slice by two tests: (1) a testable surface, (2) the most features that serve the intent | `/shape-slice` shapes the slice for an intent; the plan holds every slice that serves its intent | The verb "picks" and both tests go. Test 1 becomes a Slice rule. Test 2 goes with no replacement: the person chose the slice at `/shape-slice`. Said in the log. |
| The surface rule | "A slice with no testable surface fails the Plan's first test, and is never picked" | "A slice has a screen or surface a person can test end to end" | The rule moves to the Slice. A thing with no such surface is not a slice. |
| Who makes the plan | A plan "is given" a business intent, and then picks | The plan play makes the plan from the slice `/shape-slice` shaped, right after it, with no stop to ask — or adds the slice to the plan that exists | "Is given" stays: the plan still belongs to one intent. What changes is who makes it and how it finds its slices. |
| Who writes the epic and its stories | A plan creates the epic; each story is written from its two ICE when it is made | The same: the plan play creates the epic and its stories | No clash. `/shape-slice` writes no epic and no story, so the work is not done twice. |
| What the eval reads | Nothing (the model has no eval) | The eval play builds the eval; it reads the slice's epic and its stories, never the ICE | No clash with the ICE rule: "only a Story reads it" stays. The epic and the story each gain one reader, the eval. |
| ADR 048 §2 | "The Plan picks slices by two tests" | The plan reads the link | The ADR must be amended through `/record-decision` (the issue's done-when says so). Not an ontology change. |

## Step 3 — The terms

In the product owner's words.

**Nouns:** business intent, slice, plan, epic, story, work item, configuration (how many questions to ask), eval, evals folder, black-box product test, intent, expectation, failure condition, usage guide, surface (a browser page, a mobile app, a command line tool, a backend process or endpoint), builder agent, the product, ICE, interpretation, the shaping loop, the plan play, the eval play.

**Verbs:** `/shape-slice` *gets* a business intent, *reads* a configuration, *grills* the person, *assembles* the slice, *writes* the link "serves", and *stops*; the shaping loop *goes on* to the plan play, then to the eval play, with no stop; the plan play *makes* the plan or *adds* the slice to it, *creates* the epic, *interprets* the ICE and *writes* the stories; the eval play *builds* the eval; a slice *serves* a business intent; a plan *holds* the slices; a plan *executes*; the eval *understands* what the epic delivers; the eval *tests* the work item against the product, from the outside; the build *delivers* a usage guide; the eval *learns to use* the slice from the guide; a builder *never reads* the eval.

**Not kinds:** the configuration (how many questions `/shape-slice` asks) is a play setting (#817), not part of the model. "Grill" is a step of the play. "Interpretation" is what the plan play does when it writes the stories from the ICE; it is not a thing the model keeps apart from them. The shaping loop, the plan play and the eval play are plays, not kinds.

## Step 4 — The kinds

### Slice — changed

**Kind:** Slice.
**What changes:**
1. It **serves** one or more business intents. `/shape-slice` writes the link when it shapes the slice, on both sides. That is all `/shape-slice` writes: no plan, no epic, no story, no eval.
2. The rule "it has a screen or surface a person can test end to end" is now the Slice's own rule. It is no longer a test the plan runs.
3. It gains its **eval**: the folder where its eval is kept, under the plan that holds it, and what the eval tests. The eval play builds it, from the epic and the stories the plan play wrote. The eval reads the slice's epic and its stories, understands what the epic delivers, and tests that against the built product from the outside, on the slice's surface: every intent and expectation the stories carry is met, and no failure condition they name happens. It never reads the ICE of a feature or a capability. A builder never reads it.
4. It gains its **usage guide**: what the surface is, how to reach it, and the steps a person takes. The build delivers it with the slice. The eval reaches the product only through the guide, never through the code.
5. "A plan picks it" becomes "a plan holds it". "Whether it is picked is shown by its epic" becomes "whether its work has started is shown by its epic".
**Why:** Q25 and Q27 (which slices serve an intent; which intents a slice serves), Q28 (where its eval is kept), Q29 (what its eval tests), Q31 (how the eval learns to use it).
**Why a part of the Slice, and not a new kind:** the eval and the guide each belong to one slice, every question about them starts from the slice, and nothing else links to them. As parts of the Slice they answer every question with fewer moving parts. If the eval later gets a life of its own (runs, results, states), it becomes a kind then.
**Example:**
- Clinic — `/shape-slice` shapes Slice "Self-booking" and writes that it serves "Patients book their own appointments online". The eval play keeps its eval at `.garura/project/plans/340/evals/self-booking/`. It reads Epic #341 "Self-booking" and its Stories "Pick a free slot" and "Send a reminder", and tests that a patient books a free slot and gets a reminder, and that no slot is booked twice. Its usage guide: "Open the booking page in a browser, pick a doctor, pick a free slot, give a phone number."
- Shop — Slice "Pay without an account" serves "Shoppers can check out without an account". Its eval is at `.garura/project/plans/120/evals/pay-without-an-account/` and reads Epic #121 and its Stories "Guest checkout" and "Send receipt". Its usage guide: "In the mobile app, add an item, tap 'Pay as guest', give a card."
- Bank — Slice "Upload once" serves two intents: "Small businesses get a loan decision in one day" and "Customers give their documents only once". "Rate tables" has no surface a person can test, so it is not a slice; `/shape-slice` does not shape it.
**Log line:** Slice serves one or more business intents (written by `/shape-slice`, which writes nothing else); the testable-surface rule is the Slice's own; it gains its eval (built by the eval play, kept under its plan, never read by a builder; it reads the slice's epic and stories and tests what the epic delivers against the built product from the outside, never reading the ICE) and its usage guide (delivered by the build, the eval's only way in).

**Points for the links stage (not asked now, shown so you know they come):**
- A slice that serves two intents is in two plans, but it has one eval. Proposal: the eval is kept under the plan it was first shaped for; the other plan points to that folder, and never copies it.
- Where the usage guide is kept. Proposal: in the plan's folder, beside the evals folder but outside it (for example `.garura/project/plans/<plan-id>/guides/<slice>.md`), so the builder can write it without reading the eval.

**Decided with this change (no longer open):** who writes the epic and its stories — the plan play. It keeps today's rule "a plan creates the epic", and each story is still written from its feature's ICE and its capability's ICE. The Plan's third step and the Epic's "a plan created it" link stay as they are, with "and the stories of that epic" added to the step.

### Plan — changed

**Kind:** Plan.
**What changes:**
1. It is **made by the plan play, right after `/shape-slice`**, from the slice `/shape-slice` shaped, with no stop between them. When a plan already exists for that business intent, the new slice is **added** to it. A business intent never has a second plan.
2. It **holds** every slice that serves its business intent, and finds them by reading the "serves" link. It does no slice work again.
3. The two tests go, and "it picks a slice" goes with them. Its three steps become: it is given one business intent; it holds the slices that serve it; it creates one epic for each slice, or uses the one that exists, and the stories of that epic.
4. It **keeps the evals**: its own folder, beside the plan file, holds one evals folder with one folder for each slice. The eval play writes them there. The plan file stays where it is.
**Why:** Q7 (what the plan holds), Q30 (which plan holds a new slice), Q28 (the evals sit under the plan).
**Example:**
- Clinic — plan #340 for "Patients book their own appointments online". The plan play made it right after `/shape-slice` shaped "Self-booking", and created Epic #341 with its Stories "Pick a free slot" and "Send a reminder". Later "Cancel online" was shaped for the same intent, and the plan play added it and its epic to plan #340. Its evals folder holds `self-booking/` and `cancel-online/`.
- Shop — plan #120 holds "Pay without an account". When "Save the card for next time" is shaped for the same intent, the plan play adds it to plan #120 and creates its epic and stories. No second plan is made.
- Bank — plan #51 holds "One-day decision" and "Upload once". It does not rank them or test them; it reads which slices serve its intent and does the work.
**Log line:** Plan is made by the plan play, right after `/shape-slice`, from the slice `/shape-slice` shaped, or that slice is added to the one plan its business intent already has; it holds the slices that serve its intent, read from the link; it creates one epic for each slice, or uses the one that exists, and the stories of that epic; the two tests and "picks" go; its folder keeps one eval folder for each slice.

### Business Intent — changed

**Kind:** Business Intent.
**What changes:** it gains one link pointing at it: a slice **serves** it (many slices). It stays a destination: it points at no slice. Its Clinic example loses "Its plan picked Slice …".
**Why:** Q25 (which slices serve it), Q27 (the other side), Q30 (its one plan holds them all).
**Example:**
- Clinic — "Patients book their own appointments online" is served by Slices "Self-booking" and "Cancel online".
- Shop — "Shoppers can check out without an account" is served by Slice "Pay without an account".
- Bank — "Small businesses get a loan decision in one day" is served by Slices "One-day decision" and "Upload once".
**Log line:** Business Intent: a slice serves it; it points at no slice.

### Epic — changed (more than words)

**Kind:** Epic.
**What changes:**
1. It gains a reader: the slice's **eval reads it**, with its stories, to learn what it delivers. What it delivers is then tested against the built product. So its title ("what it delivers, in one line") must say what a person can see the product do, not how it is built.
2. "When a second plan picks the same slice, it uses this epic" becomes "When the slice is in a second plan, that plan uses this epic".
3. Its "serves" link stays, and is now said to follow from its slice: an epic serves the business intents its slice serves.
Its "a plan created it" link does not change: the plan play creates it, with its stories. It still has no ICE and knows no capability.
**Why:** Q29 (the eval tests what the epic delivers), Q7 and Q30 (the plan holds the slice and its one epic); with "picks" gone, the old words would be wrong.
**Example:**
- Clinic — Epic #341 "Self-booking" delivers "a patient books a free slot online and gets a reminder". The plan play created it; the eval for Slice "Self-booking" reads it and tests that on the booking page.
- Shop — Epic #121 "Pay without an account" is the one epic of its slice, in plan #120. The eval reads it and tests that a shopper with no account can pay in the mobile app.
- Bank — "Upload once" serves two intents, so it is in plan #51 and in the plan for "Customers give their documents only once"; both use its one epic, and its one eval reads it.
**Log line:** Epic: still created by a plan (the plan play); the slice's eval reads it, with its stories, to learn what it delivers, so its title says what a person can see the product do; "picks" becomes "holds"; an epic serves the business intents its slice serves.

### Story — changed, in words only

**Kind:** Story.
**What changes:** it gains a reader: the slice's **eval reads its scope of work**, because the scope carries the intent, the expectations and the failure conditions the story took from its two ICE. Its rules do not change: the plan play writes it when it creates the epic, from its feature's ICE and that feature's capability's ICE, and the ICE rule "only a Story reads it" stays as it is.
**Why:** Q29 (the eval tests every intent and expectation the stories carry, and that no failure condition they name happens).
**Example:**
- Clinic — Story #342 "Pick a free slot": the eval reads its scope and tests that no slot is booked twice.
- Shop — Story #122 "Guest checkout", scope "A shopper pays by card with an email only; no account is made": the eval tests that no account is made and no card is charged twice.
- Bank — Story #55 "Score the application": the eval reads its scope and tests that no decision goes out without a score.
**Log line:** Story: written by the plan play, as today, from its two ICE; the slice's eval reads its scope of work; its ICE rule does not change.

### ICE, Feature, Capability — same

Reused as they are. The eval does not read their ICE. The ICE rule "only a Story reads it" stays word for word.

### Source, Domain, Spike, Chore, Bug — same

Not touched by this need.

## What the version 9 log line will say

2026-10-23 — v9 (#816, plan #788, with the product owner): a Slice serves one or more business intents, written by `/shape-slice`, which writes nothing else (no plan, no epic, no story, no eval); the rule "a slice has a screen or surface a person can test end to end" is the Slice's own; the Slice gains its eval (built by the eval play, kept under its plan, never read by a builder; it reads the slice's epic and its stories and tests what the epic delivers against the built product from the outside, on its surface, never reading the ICE) and its usage guide (delivered by the build; the eval's only way in). The Plan is made by the plan play, right after `/shape-slice`, from the slice `/shape-slice` shaped, or that slice is added to the one plan its business intent already has; it holds the slices that serve its intent, read from the link; it still creates one epic for each slice, or uses the one that exists, and now also the stories of that epic; the two tests and "picks" go. A Business Intent is served by slices. An Epic is read by its slice's eval and serves what its slice serves. A Story is written by the plan play from its two ICE, as before, and its scope of work is read by its slice's eval. The ICE does not change. Q7 and Q25 change; Q27–Q31 are added; Q29 was corrected after checkpoint 2. Dropped: "a plan picks a slice by two tests", "a slice with no surface fails the plan's first test".

## Not an ontology change (for the write stage)

- A line in CLAUDE.md: a builder agent, or any skill that builds the software, never reads a plan's evals folder.
- ADR 048 §2 ("the Plan picks slices by two tests") is amended through `/record-decision`.
- The shaping loop runs `/shape-slice`, the plan play and the eval play in order; their names and the loop are set in plan 788's stories, not in the ontology.
- The need's "Touches" list names Slice, Plan and Business Intent. This draft also changes Epic and Story. The write stage's check counts the changed kinds, so the list must name them.

Question for the product owner: are these the right kinds, and the right changes to them?
