# Questions draft — ontology v11 (#846, plan 788)

You decide three things in this draft. First: `/shape-slice` writes the slice's hidden file (its failure conditions and recovery conditions), and the plan play writes only the plan, the epic and the stories. Second: the hidden file has one entry for each feature, and the epic keeps the map from each feature to its story, so the eval play can join them. Third: when a part has no ICE, `/shape-slice` proposes a thin ICE, marks it thin and warns the person, and never sends them back.

Each item below is a question the ontology must answer after this change. Each one says if it is new or changed, and gives our proposed answer. One item (C1) needs your choice, because today's rules and decision 7 of #844 do not agree.

Sources: the need (`need.md`), ontology v10, ADR 049, `standards/rules/expectation-generation.md`, and the decisions of the /shape-slice run for #788 (#844, decisions 6 and 7).

---

## F1 — The flow line (changed: "How it flows" and link line 1, under Q1)

**Question:** Given a business intent, which play does what, in which order, from the slice to the stories?

**Answer (proposed):** `/shape-slice` shapes the slice. It writes the link "slice serves business intent", a thin ICE for each part the slice needs that has no ICE, and the slice's hidden file. Then the plan play makes the plan, the epic and one story for each feature. Then the eval play builds the eval. Link line 1 becomes: "A Plan is made by the plan play right after `/shape-slice`. It is given one Business Intent; it holds every Slice that serves that intent; it creates one Epic for each Slice, with its Stories. It writes nothing in the evals folder." Q1's own answer does not change.

**Why it matters:** Each play has one job. If the flow line still says the plan play writes the hidden file, a person and an agent read two different stories.

**Example:**
- Shop: the shopper persona tests "Pay without an account". `/shape-slice` writes the slice and its hidden file. The plan play then makes Epic "Pay without an account" and its stories.
- Clinic: the patient persona tests "Self-booking". `/shape-slice` writes the hidden file entry for "Pick a free slot" before any story exists.
- School: the teacher persona tests "Mark today's attendance". The plan play makes the epic and stories, and writes no file in the evals folder.

---

## Q33 — Where the hidden file is, and what it holds (changed)

**Question:** Given a slice, where are its failure conditions and recovery conditions kept, and what does each entry hold?

**Answer (proposed):** In the slice's hidden file `failure-and-recovery.md`, in its eval folder `.garura/project/plans/<plan-id>/evals/<slug>/`. It has one entry for each feature of the slice (not for each story). Each entry holds: the feature (its id and name), its capability, the two ICE it was written from (and which of them is thin), its failure conditions (each "Fails if" line, with a short id such as F1, or "none") and exactly one recovery condition for each (when, way back, who fixes). A builder never reads it.

**Why it matters:** The stories do not exist yet when `/shape-slice` runs. An entry keyed by story cannot be written then; an entry keyed by feature can.

**Example:**
- Clinic: the entry for feature "Pick a free slot" says "F1 — Fails if: a slot is booked twice. Recovery — When: two bookings are on one slot. Way back: keep the first booking and offer the second patient a new slot. Who fixes: the builder can fix this alone."
- Bank: the entry for feature "Score the application" says "F1 — Fails if: the score uses data the customer did not send. Who fixes: a person must decide."
- School: the entry for feature "Mark a pupil absent" says "Failure conditions: none" because its two ICE have no "Fails if" line.

---

## Q34 — Who writes the hidden file (changed)

**Question:** Who writes the failure conditions and recovery conditions of a slice, and when?

**Answer (proposed):** `/shape-slice` writes the slice's hidden file when it shapes the slice: one entry for each feature, from that feature's ICE and its capability's ICE, with exactly one recovery condition for each "Fails if" line, by `standards/rules/expectation-generation.md`. When the slice gains a feature, `/shape-slice` adds that feature's entry. The plan play writes nothing in the evals folder.

**Why it matters:** The product owner said the plan only plans (#844, decision 6). The rule in `expectation-generation.md` and ADR 049 still name the plan play; they change with this answer.

**Example:**
- Shop: `/shape-slice` adds "Save the card for next time" to the slice, and adds one entry for it to the hidden file. The plan play then adds one story to the epic.
- Clinic: the plan play runs for "Self-booking" and leaves `evals/self-booking/` as `/shape-slice` left it.
- School: a second intent reuses the slice "Mark today's attendance". The entries stay in the home plan's folder; no copy is made.

---

## Q36 — Which story an entry is for (new)

**Question:** Given an entry in a slice's hidden file, which story of the epic is it for?

**Answer (proposed):** The epic keeps a map from each feature of its slice to the story that delivers it. The eval play reads that map and joins each hidden-file entry (by its feature) to its story. The story itself still holds no failure condition and no recovery condition.

**Why it matters:** The eval play must test each story against the right failure conditions. Without the map, the join is a guess.

**Example:**
- Clinic: Epic #341 maps "Pick a free slot" to Story #342 and "Send a reminder" to Story #343. The eval play joins entry "Pick a free slot" to Story #342.
- Shop: a later slice includes "Guest checkout" again. That slice's epic gets its own story and its own map line, so the entry joins to the right story.
- Bank: Epic "One-day decision" maps "Score the application" to Story #55.

---

## Q29 — What the eval reads (changed)

**Question:** Given a slice, what does its eval read, and when?

**Answer (proposed):** As today, at two times. One change: the eval play reads the epic (with its feature-to-story map), the stories and the hidden file, and joins each entry to its story through that map. The running eval reads the same things as today: the eval, the usage guide, the Context guidance in the eval and only the recovery parts of the hidden file.

**Why it matters:** The hidden file is now keyed by feature. The eval play must say how it finds the story for each entry.

**Example:**
- Shop: the eval play reads Epic "Pay without an account", finds "Guest checkout → Story #121", and puts entry F1 under Story #121's checks.
- Clinic: the running eval sees two bookings on one slot and reads only "When / Way back / Who fixes".
- School: the eval play finds no "Fails if" line for "Mark a pupil absent" and tests only its goals and expectations.

---

## Q37 — Who reads which part of an ICE (new)

**Question:** Given an ICE, which play reads each part of it, so each part has one interpretation?

**Answer (proposed):** `/shape-slice` reads the "Fails if" lines (and what it needs to write their recovery) and writes the hidden file. The plan play reads the goals, the limits, the Context lines and the Expectation, and writes each story's scope of work and Context guidance. Each line of an ICE has one reader that writes from it. A builder reads neither.

**Why it matters:** ADR 049 says only one place interprets the ICE. With two plays now reading it, the rule must say which play owns which lines, or two plays can read one line in two ways.

**Example:**
- Bank: "Fails if: the score uses data the customer did not send" is read by `/shape-slice` only. "Goal: each application gets a score within one hour" is read by the plan play only.
- Clinic: "Never read: other patients' records" is a Context line; the plan play copies it into the story's Context guidance.
- Shop: "Fails if: a guest is asked to sign up before paying" never reaches Story "Guest checkout".

---

## Q38 — A part with no ICE (new)

**Question:** When a slice needs a capability or a feature that has no ICE, what ICE does it get, and how does a person know it is thin?

**Answer (proposed):** `/shape-slice` proposes a thin ICE itself, from the person's answers: at least a goal, its limits and one "Fails if" line. It marks the ICE thin, writes the hidden file from it, and warns the person that thin ICE can cause problems later and that `/discover-capabilities` can deepen it. It never forces the person to go back. The mark stays until a play deepens the ICE.

**Why it matters:** "Nothing is blocked" holds, and the person still sees the risk. Without a mark, a thin ICE looks the same as a full one.

**Example:**
- School: the slice needs feature "Send a note home", which has no ICE. `/shape-slice` proposes "Goal: a parent gets the teacher's note the same day. Limit: no pupil's marks in the note. Fails if: a note goes to the wrong parent." It marks it thin and warns the teacher persona's product owner.
- Shop: new capability "Gift cards" gets a thin ICE. The person says go on; the slice is shaped and nothing stops.
- Clinic: later, `/discover-capabilities` deepens the "Booking" ICE, and the thin mark goes.

---

## C1 — Can work start from a thin ICE? (new — your choice)

**Question:** Can work start on a thin ICE, and what does the ready check say about it?

**Answer (proposed):** A thin ICE has all three parts, with at least one line each: the goal, the limits and one "Fails if" line in Intent, one line in Context, and one line in Expectation. So the ready check can answer "partly ready", with the gap "thin ICE" in its list, and work starts.

**Why it matters:** Today an ICE with a missing part is "not ready", and work stops. Decision 7 of #844 asks for only a goal, limits and one "Fails if" line, and says "partly ready" allows work. Those two do not agree: an ICE with Intent only is "not ready". If we keep the decision's words, the warning becomes a stop, which the product owner said must not happen. The other choice is to add "thin ICE, Intent only" as a new reason for "partly ready", which changes the ready check (ADR 047).

**Example:**
- Shop: thin ICE of "Gift cards" with Context "Persona: the shopper" and Expectation "Done means: a shopper pays with a gift card" → partly ready, gap: thin ICE.
- Bank: thin ICE with Intent only, no Context, no Expectation → today, not ready; work on the story stops.
- School: thin ICE of "Send a note home" with one line in each part → partly ready; the plan play makes the story.

---

## Q39 — When an ICE changes after the hidden file and story are made (changed: today a Story rule, "made again together")

**Question:** When an ICE changes after its hidden-file entry and its story are made, which play makes each again?

**Answer (proposed):** The entry and the story are drift for the Alignment loop. `/shape-slice` makes the hidden-file entry again, and the plan play makes the story again, from the same two ICE. Both are made again in the same alignment round, so the story and the entry never disagree. When the change removes the thin mark, the entry's thin note goes too.

**Why it matters:** Today one play remakes both at once. With two writers, the rule must say both are made again, or one goes stale.

**Example:**
- Clinic: the "Booking" ICE gains "Fails if: a reminder goes to a cancelled booking". The Alignment loop adds F2 to the entry and leaves the story's scope of work as it is, because no goal changed.
- Shop: the "Guest checkout" ICE gets a new limit. The plan play remakes the story; the entry is checked and kept.
- Bank: the thin ICE of "Score the application" is deepened. The entry and the story are both made again.

---

## Q40 — The hidden file before any plan exists (new)

**Question:** Where does `/shape-slice` write the hidden file when the business intent has no plan yet?

**Answer (proposed):** At the same place: `.garura/project/plans/<plan-id>/evals/<slug>/failure-and-recovery.md`, where `<plan-id>` is the issue number of the slice's first business intent, worked out, never stored. `/shape-slice` makes the folder. The plan play later writes the plan file beside it and finds the folder already there. The slice rule "writes nothing else" changes to "writes the link, thin ICE where needed and the hidden file; no plan, no epic, no story, no eval".

**Why it matters:** The path names the plan. Without this answer, a play could think the folder must wait for a plan file.

**Example:**
- Clinic: intent #340 has no plan. `/shape-slice` writes `plans/340/evals/self-booking/failure-and-recovery.md`; the plan play then writes `plans/340.yaml`.
- Shop: intent #120 has plan #120. `/shape-slice` writes the new slice's file in `plans/120/evals/`.
- School: a slice first shaped for intent #77 also serves intent #90. Its hidden file stays in `plans/77/evals/`; plan #90 points to it.

---

## Questions that do not change

Q1 (its answer), Q2–Q28, Q30–Q32 and Q35 keep their words. Q28 and Q32 still hold: the eval and hidden file stay in the home plan's evals folder, and a builder never reads it.
