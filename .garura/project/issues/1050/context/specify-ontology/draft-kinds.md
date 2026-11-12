# Draft — the kinds (stage `kinds`, steps 2 to 4)

Need: #1050 (the ontology change for ADR 068: each product feature has one Feature issue that names it). Agreed questions: Q19, Q20, Q26, Q43 (changed) and Q48 to Q53 (new), at checkpoint 1.

## Opening

You decide which kinds change, and what each one now means. Five kinds were expected to change (Feature, Story, Epic, Plan, Slice). This draft proposes one new kind, the Feature issue, and short wording changes to two more kinds, Capability and ICE, and asks you about each at the end. When you say yes, the next stage (`links`) writes the properties, links and rules of these kinds. When you change something, this stage is done again with your words first.

## Step 2 — What we reuse

- **Reused as they are:** Business Intent, Source, Domain, Spike, Chore, Bug. A Spike, Chore or Bug is still a child of one Story. It still reaches its feature, its epic and its business intent through that Story, now through the Story's Feature issue. No agreed question reaches these six kinds.
- **Reused with a change:** Feature, Story, Epic, Plan, Slice (as expected), and Capability and ICE (wording only, see K2).
- **Reused from today's rules:** the plan file's `represents` mark (R3), "never by title", "an Epic is never filed as type Feature" (R1), "no roll-ups" (ADR 064), and "a person closes an item through `/reshape-plan`".
- **Clashes found:**
  - The tracker type Feature means two things today: a "feature item" (a group of stories, the Plan kind, line 625 of the ontology) and nothing in the model. ADR 068 makes it mean one thing: the Feature issue of one product feature (Q20).
  - "Delivered" (a Feature with at least one closed Story, line 394) and "built" (a Feature whose Feature issue is closed, Q50, Q52) would be two words for one state. See K3.
  - "Represents" is in two places: the plan file's `represents` mark and the issue's `Represents: <feature id>` line. Both mean "stands for this feature", so this is one meaning in two places, not two meanings. The plan file is not the product model, so the model still holds no link (Q49).

## Step 3 — The terms

| Term | Kind of word | Meaning now | Change |
|------|--------------|-------------|--------|
| Feature issue | noun | The one tracker issue, of type Feature, that stands for one product feature. Its text names the feature in the line `Represents: <feature id>` | **new** |
| feature item | noun | A group of stories inside an epic, standing for nothing in the model | **goes** |
| tracker type Feature | noun | Was "a feature item". Now: a Feature issue | **meaning changes** |
| `Represents:` line | noun | The exact line `Represents: <feature id>` in a Feature issue's text. The only link between a feature and its work. It points one way, from the tracker to the model | **new** |
| built | adjective | A feature whose Feature issue a person closed through `/reshape-plan` "finish" | **new** (replaces "delivered" for a feature, K3) |
| delivered | adjective | Was "a feature with at least one closed Story". For a feature, it goes | **meaning changes** (K3) |
| orphan Story | noun | A Story that has no Feature issue as its parent | **new** |
| duplicate | noun | Two issues of type Feature with the same `Represents:` line. The run stops and asks the person | **new** |
| feature-to-story map | noun | The epic's list. Each line now names a feature and its Feature issue, one line for each feature | **meaning changes** (name kept, as Q26 agreed) |
| scope of work, Context guidance | noun | Now on the Feature issue, not the Story | **moves** |
| finish | verb | A person closes a Feature issue, in `/reshape-plan` | reused |
| sits inside, sits under | verb | A Story sits inside a Feature issue. A Feature issue sits under one Epic at a time | **changes** |
| groups, holds | verb | Slices and plans group features, many to many | reused |

## Step 4 — The kinds

### Feature issue (new kind, work layer)

- **What changes:**
  - A new work-layer kind: the one issue of type Feature that stands for one product feature, in the whole tracker. Its text has the exact line `Represents: <feature id>`.
  - It holds the feature's scope of work (goals, limits, expectations) and its Context guidance, written from the feature's ICE and its capability's ICE. It never holds a failure condition or a recovery condition.
  - It sits under one Epic at a time, and holds the Stories of its feature. A person closes it through `/reshape-plan` "finish". Then the feature is built.
  - A play finds it by the plan file's mark, else by the exact `Represents:` line on an issue of type Feature, open or closed. Two such issues stop the run. A play never finds it by title.
- **Why:** Q20 and Q48 need one issue that stands for one feature. Q26 needs one place for its scope of work.
- **Who reads it:** both.
- **What it is not:** not the Feature kind (the Feature is in the model; the Feature issue stands for it in the tracker), and not a feature item (that goes).
- **Log line:** Feature issue (new, work layer): the one issue of type Feature for one product feature; its text names the feature (`Represents: <feature id>`), the only link, one way; it holds the feature's scope of work and Context guidance, sits under one Epic at a time, holds its Stories, and a person closes it through `/reshape-plan` "finish" (Q20, Q26, Q48, Q51, Q52).

### Feature

- **What changes:**
  - "In the tracker as" changes from "a Story, one in each Epic" to "one Feature issue, in the whole tracker". The tracker type Feature now means this kind.
  - A new rule: no feature in the model holds a tracker issue number (no `issue` property). Only its Feature issue names it.
  - "Delivered" (at least one closed Story) becomes "Built": its Feature issue is closed. Closed Stories do not build it. A built feature counts complete in every slice and plan that holds it.
  - Its link to Story goes. A Story reaches its feature through its Feature issue. A feature can be in many slices and plans, and it still has one Feature issue.
- **Why:** Q49 removes the issue number from the model, Q52 says when a feature is built, and Q19 lets many slices and plans hold one feature.
- **Log line:** Feature: in the tracker, one Feature issue that names it, never a Story in each Epic; it holds no tracker issue number; it is built when a person closes its Feature issue, not when its Stories close, and then it counts complete in every slice and plan that holds it (Q19, Q49, Q52).

### Story

- **What changes:**
  - It no longer represents a feature. It is a piece of work that always sits inside one Feature issue, and through it in one Epic. Its `Represents` property goes.
  - Its scope of work, its Context guidance and "written from two ICE" move to the Feature issue. So do the drift rule for a changed ICE and the rule for what the build play's context sub-agent reads.
  - "One Story for each Feature in each Epic" goes. A Feature issue can hold many Stories.
  - "Closed means delivered" becomes "closed means its piece of work is done". A Story with no Feature issue (an orphan) is matched to its feature by research in the model. When no feature fits, the feature is made and its Feature issue is filed.
- **Why:** Q43 puts every Story inside a Feature issue, Q26 moves the scope of work, and Q53 says what happens to an orphan Story.
- **Log line:** Story: a piece of work that always sits inside one Feature issue, and no longer represents a feature; its scope of work, Context guidance and two ICE move to the Feature issue; closed means its work is done, not that its feature is built; an orphan Story is matched to its feature by research in the model (Q26, Q43, Q52, Q53).

### Epic

- **What changes:**
  - It holds Feature issues, with their Stories inside them, not Stories straight under it.
  - Its feature-to-story map names Feature issues, one line for each feature. The eval play joins each hidden-file entry to its Feature issue through it.
  - A Feature issue sits under one Epic at a time. When a second Epic needs it, the play asks the person which Epic it goes under, and does not move it without that answer.
  - It never holds two Feature issues for one feature. R1 ("never filed as type Feature") and R3 stay.
- **Why:** Q43 sets the tree, Q26 changes what the map names, and Q51 says which Epic holds a Feature issue that two Epics need.
- **Log line:** Epic: holds Feature issues, with their Stories inside; its feature-to-story map names Feature issues, one line for each feature; a Feature issue sits under one Epic at a time, and a second Epic that needs it asks the person (Q26, Q43, Q51).

### Plan

- **What changes:**
  - Its item kind `feature` is now a Feature issue that stands for one product feature. The feature item and its rule (ontology line 625) go. A story sits under a Feature issue only, never straight under an epic.
  - Its tree: Business Intent → Slice → Epic → Feature issue → Story → Spike, Chore, Bug. The plan file's `represents` mark is on the Feature issue item.
  - The plan play finds or files one Feature issue for each feature of a slice that is not yet built (Q48 search order). It writes the scope of work and Context guidance on the Feature issue, not the Story.
  - Many plans can hold one feature, and it still has one Feature issue. A built feature counts complete in each plan that holds it. A new plan holds only features that are not built.
- **Why:** Q43 sets the item kinds, Q48 says how the plan play finds a Feature issue, and Q19, Q50 and Q52 say how plans share a feature.
- **Log line:** Plan: its item kind `feature` is a Feature issue that stands for one product feature (the feature item goes); a story sits under a Feature issue only; the plan play finds a Feature issue by the plan file's mark or the exact `Represents:` line, else files one, and writes the scope of work on it; plans share a feature many to many, and hold only features not yet built (Q19, Q43, Q48, Q50, Q52).

### Slice

- **What changes:**
  - It takes in only features that are not yet built. A feature that is built after it joined stays in the slice and counts complete.
  - Its features can be in other slices and plans. Each feature still has one Feature issue, not one for each slice.
  - Its eval play reads the Feature issues in its epic (their scope of work and Context guidance), not the Stories, and joins each hidden-file entry to its Feature issue through the epic's map. When the slice gains a feature, the plan play finds or files that feature's Feature issue.
- **Why:** Q50 limits what a slice takes in, Q19 lets slices share a feature, and Q26 moves what the eval play reads.
- **Log line:** Slice: takes in only features not yet built, and a feature built later counts complete in it; slices share a feature, which has one Feature issue; its eval play reads the Feature issues in its epic, not the Stories (Q19, Q26, Q50, Q52).

### Capability (wording only, see K2)

- **What changes:**
  - "Done" changes from "each of its features has at least one closed Story, in any epic" to "each of its features is built (its Feature issue is closed)".
  - "A Story reaches it through its Feature" becomes "a Feature issue reaches it through its Feature". The Bank example changes to match.
- **Why:** Q52 changes when a feature is built, and the ready check (Q10, Q11) reads "done" from it.
- **Log line:** Capability: done when each of its features is built (its Feature issue is closed), not when each has a closed Story (Q52).

### ICE (wording only, see K2)

- **What changes:**
  - "A story is written from it" becomes "a Feature issue is written from it". The plan play reads every line except "Fails if" and writes the Feature issue. Its three parts and its ready check do not change.
  - Two examples change: "Story 'Guest checkout' read this ICE" and "its Feature 'Fill the form' has no closed Story".
- **Why:** Q26 and Q37 now name the Feature issue as the one reader of every line that is not "Fails if".
- **Log line:** ICE: wording only; the plan play writes each line other than "Fails if" into the Feature issue, not the Story; its parts and ready check do not change (Q26, Q37).

### Kinds that do not change

Business Intent, Source, Domain, Spike, Chore and Bug. No agreed question reaches them.

### Outside the kinds (written at the `write` stage)

The opening count ("thirteen kinds" becomes fourteen, if K1 is yes), the flow line, the five links, the tracker paragraph, and the answers of Q1, Q4, Q7, Q13, Q18, Q22, Q23, Q29, Q32, Q36, Q37 and Q39, as agreed at checkpoint 1.

### The version log entry (one line, drafted)

- 2026-11-12 — v16 (#1050, ADR 068, with the product owner): each product feature has one Feature issue, a new work-layer kind: one issue of type Feature whose text names the feature (`Represents: <feature id>`), the only link, one way, from the tracker to the model; no feature holds an issue number. The Feature issue holds the scope of work and Context guidance (moved from the Story), sits under one Epic at a time (a second Epic asks the person), and holds the Stories; a Story always sits inside one. A play finds it by the plan file's mark, else by the exact line, never by title; two such issues stop the run. A feature is built when a person closes its Feature issue through `/reshape-plan` "finish", and then counts complete in every slice and plan that holds it; slices and plans group features many to many and take in only features not yet built. The feature item goes. Capability and ICE change in wording only. Changed kinds: Feature, Story, Epic, Plan, Slice, Capability, ICE; new kind: Feature issue.

## Kept for the links stage (not asked here)

- How plan B shows a feature whose Feature issue sits under plan A's epic (from checkpoint 1).

## Questions for you

### K1 — Is the Feature issue a kind of its own?

- **Question:** Does the ontology give the Feature issue its own kind in the work layer?
- **Answer (proposed):** Yes. The Feature issue is a new work-layer kind, beside Epic and Story. The product layer keeps the Feature; the work layer gets the Feature issue that stands for it. This is the same as today's pair Slice (in the model) and Epic (in the tracker). It adds one kind to the need's list of five, so the play's "only the needed kinds changed" check must count it.
- **Why it matters:** If the Feature kind holds the scope of work, the issue state and the parent Epic, one kind mixes the model and the tracker, and the two layers that version 7 split come back together.
- **Example:**
  - A shop: Feature "Guest checkout" is in the model; Feature issue #71 is in the tracker and holds its scope of work.
  - A clinic: Slice "Self-booking" has Epic #341; Feature "Send a reminder" has Feature issue #40, in the same way.
  - A bank: the credit officer reads Feature issue "Upload documents" for the limit "files up to 10 MB", and the model page for what the feature is.

### K2 — Do Capability and ICE change too?

- **Question:** Does this change also update the words of the Capability kind and the ICE kind?
- **Answer (proposed):** Yes, in wording only. Capability's "done" reads "each feature is built" in place of "each feature has a closed Story". ICE names the Feature issue, not the Story, as what the plan play writes. Their meaning, properties and links do not change. ADR 068 says the ICE kind does not change; that stays true of its parts, but its words name the Story, which no longer holds the scope of work.
- **Why it matters:** If they keep the old words, the ontology says in two kinds that a closed Story builds a feature, which Q52 says is false.
- **Example:**
  - A bank: "Loan application" is done only when "Fill the form" has its Feature issue closed, not when its last Story closes.
  - A shop: the ICE of "Guest checkout" is read into Feature issue #71, not into a Story.
  - A school: "Attendance" is not done while the Feature issue "Mark attendance" is open, even with all its Stories closed.

### K3 — Does "built" replace "delivered" for a feature?

- **Question:** Does the ontology use "built" for a feature whose Feature issue is closed, in place of "delivered"?
- **Answer (proposed):** Yes. Q50 and Q52 use "built". "Delivered" goes for a feature. A Story's closed state means its piece of work is done.
- **Why it matters:** Two words for one state make an agent ask whether "delivered" and "built" differ, and read them two ways.
- **Example:**
  - A clinic: "Send a reminder" is built when the clinic manager finishes #40.
  - A shop: Story "Show the total" is closed; its feature "Guest checkout" is not yet built.
  - A bank: a new slice leaves out "Upload documents" because it is built.

### K4 — Does a Story still name its feature?

- **Question:** Does a Story keep its own `Represents` property?
- **Answer (proposed):** No. A Story reaches its feature only through its parent Feature issue. One link for each feature, kept on one issue.
- **Why it matters:** If a Story also names its feature, the Story and its Feature issue can name two different features, and someone must keep them the same.
- **Example:**
  - A school: Story "Export attendance to a file" sits inside Feature issue "Mark attendance", and names no feature itself.
  - A bank: Story "Freeze a card" has no Feature issue, so a play finds its feature by research (Q53), not from a line on the Story.
  - A shop: Story "Show the total" moves to Feature issue #71, and nothing on the Story must change.

## Sources

- `docs/adr/068-each-product-feature-has-one-feature-issue-that-names-it.md` — Decision parts 1 to 6, and "What this changes in older ADRs".
- `core/components/memory/standards/schemas/product-os/ontology.md` (version 15) — the tracker paragraph (line 21), Capability (lines 347, 365, 366, 377), Feature (lines 384, 394, 403, 416 to 420), Slice (lines 438, 464, 467), ICE (lines 505, 513, 550, 561), Plan, Epic and Story (lines 581 to 748).
- `.garura/project/issues/1050/context/specify-ontology/draft-questions.md` — the agreed questions.
