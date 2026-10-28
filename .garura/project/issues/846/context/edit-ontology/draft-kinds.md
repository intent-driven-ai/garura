# Kinds draft — ontology v11 (#846, plan 788)

You decide which kinds change, and how. Five kinds change: Slice, Plan, Epic, Story and ICE. No kind is added, and no other kind changes. Four points need your choice (K1 to K4); for each, we give our proposed answer.

Sources: the agreed questions draft (`draft-questions.md`, yes on 2026-10-24, C1 as proposed), the need (`need.md`), ontology v10.

---

## 1. What we reuse, and where it clashes

We reuse every kind of v10. We add no kind. Four places clash with the agreed questions:

- **ICE, "light ICE".** v10 says "a light ICE has one line in each of its three parts". C1 gives the same words to "thin ICE". Two words for one thing is drift. See K1.
- **Slice, "writes nothing else".** v10 says `/shape-slice` writes only the link. Now it also writes thin ICE and the hidden file (Q34, Q38, Q40).
- **Plan, "interprets each ICE once".** v10 says the plan play reads all of each ICE. Now two plays read an ICE, and each line has one reader (Q37).
- **Plan, the Tree.** The Plan's Tree already shows "Story (with its Feature)". The new feature-to-story map on the Epic (Q36) holds the same facts. See K3.

Outside the ontology, two more texts name the plan play as the writer of the hidden file: `standards/rules/expectation-generation.md` and ADR 049. They change with this need, in the same change, but they are not kinds.

## 2. Terms

| Term | Plain meaning | New? |
|------|---------------|------|
| thin ICE | An ICE that `/shape-slice` proposed from the person's answers, with at least one line in each of its three parts, and that carries the thin mark. Like thin ice on a lake: you can walk on it, but you can fall through. Work can start; the ready check warns. | new |
| thin mark | The note on an ICE that says it is thin. `/shape-slice` sets it. A play that deepens the ICE takes it away. | new |
| deepen an ICE | Write the ICE again from a full discovery (for example `/discover-capabilities`), so it is no longer thin. | new |
| hidden-file entry | One part of a slice's hidden file, for one feature of the slice: its failure conditions and one recovery condition for each. Was one entry for each story; now one for each feature. | changed |
| feature-to-story map | The list, on an epic, that says which story delivers each feature of its slice. The eval play uses it to join each hidden-file entry to its story. | new |
| home plan | The plan of the business intent the slice was first shaped for. Its folder holds the slice's hidden file, eval and guide. | as v10 |

## 3. The kinds that change

### Slice — changed

**What changes:** `/shape-slice` writes three things: the link "slice serves business intent", a thin ICE for each part the slice needs that has no ICE, and the slice's hidden file. It still writes no plan, no epic, no story and no eval. The hidden file has one entry for each feature (was: each story), written by `/shape-slice` (was: the plan play). `/shape-slice` makes the eval folder in the home plan's folder, also when no plan file exists yet. When the slice gains a feature, `/shape-slice` adds its entry. The eval play joins entries to stories through the epic's feature-to-story map.
**Why:** The stories do not exist when `/shape-slice` runs, and the product owner said the plan only plans (#844, decision 6).
**Log-line text:** "Slice: `/shape-slice` writes the link, thin ICE where a part has none, and the hidden file; the hidden file has one entry for each feature, not each story; `/shape-slice` makes the eval folder before any plan file exists."

### Plan — changed

**What changes:** The plan play writes only the plan file, the epic and the stories. It writes nothing in the evals folder; it finds the folder there. It reads the goals, the limits, the Context lines and the Expectation of each ICE, and never the "Fails if" lines. The rule "the plan play reads all of each ICE" goes. The Folder property says the hidden file is written by `/shape-slice`.
**Why:** One play, one job (#844, decision 6). Each ICE line keeps one reader (Q37).
**Log-line text:** "Plan: the plan play writes only the plan file, the epic and the stories, nothing in the evals folder, and reads every ICE line except 'Fails if'."

### Epic — changed

**What changes:** The Epic gains one property, the feature-to-story map: for each feature of its slice, the story that delivers it. The plan play writes it when it makes the stories, and adds a line when a story joins. The eval play reads it.
**Why:** The hidden file is now keyed by feature. Without the map, the eval play guesses which story an entry is for (Q36).
**Log-line text:** "Epic: gains the feature-to-story map, written by the plan play and read by the eval play to join each hidden-file entry to its story."

### Story — changed

**What changes:** Its failure and recovery conditions go to the hidden file, written by `/shape-slice` (was: the plan play). When one of its two ICE changes, two plays remake their parts in the same Alignment round: the plan play remakes the story, `/shape-slice` remakes the hidden-file entry (was: "made again together" by one play). The story still holds no failure condition and no recovery condition.
**Why:** There are now two writers. If only one remakes, the story and the entry disagree (Q39).
**Log-line text:** "Story: its failure and recovery conditions are written by `/shape-slice`; when an ICE changes, the plan play remakes the story and `/shape-slice` remakes the entry, in the same Alignment round."

### ICE — changed

**What changes:**
- Two plays read it, each for its own lines: `/shape-slice` reads the "Fails if" lines and writes the hidden file; the plan play reads every other line and writes the story.
- It can be thin. A thin ICE has at least one line in each of its three parts and carries the thin mark. `/shape-slice` proposes it from the person's answers when a part the slice needs has no ICE, and warns the person. It never sends the person back to a discovery play.
- The ready check reads the thin mark: a thin ICE is "partly ready", with the gap "thin ICE" in its list. Work starts. The check still does not count or judge lines.
- The term "light ICE" goes (see K1).
**Why:** Nothing is blocked, and the person still sees the risk (#844, decision 7; C1 as agreed).
**Log-line text:** "ICE: `/shape-slice` reads its 'Fails if' lines and the plan play reads the rest; an ICE can be thin (one line or more in each part, with the thin mark), proposed by `/shape-slice`, and the ready check then answers 'partly ready' with the gap 'thin ICE'; 'light ICE' becomes 'thin ICE'."

## 4. Other kinds

No other kind changes. Capability and Feature do not change: `/shape-slice` can already add a capability or a feature the slice needs, and the thin mark sits on the ICE, not on its part. See K4.

---

## K1 — One word: "thin" or "light"?

**Question:** v10 says a "light ICE" has one line in each part. Is a thin ICE the same thing, and which word stays?

**Answer (proposed):** One word stays: "thin". "Light ICE" goes. An ICE is thin when it carries the thin mark, not when it has few lines. An ICE with few lines and no mark (for example, written by `/discover-capabilities`) is not thin; the product owner judges its depth, as v10 says.

**Why it matters:** With two words, a person reads two kinds of ICE where there is one. If the ready check counts lines, it judges richness, which v10 forbids.

**Example:**
- Shop: `/shape-slice` proposes the "Gift cards" ICE with one line in each part. It has the mark → partly ready, gap: thin ICE.
- Clinic: `/discover-capabilities` writes the "Booking" ICE with one line in each part. No mark → the thin gap does not show.
- School: the teacher persona's product owner deepens "Send a note home". The mark goes, and so does the gap.

## K2 — Where the thin mark is kept

**Question:** Where does an ICE keep its thin mark, so a person and the ready check both see it?

**Answer (proposed):** In two places that agree: one line at the top of its `ice.md` page ("Thin: proposed by `/shape-slice` from the person's answers; deepen with `/discover-capabilities`"), and `thin: true` in its spine entry's `metadata`. The spine entry still holds no ready answer.

**Why it matters:** The page is what a person reads. The spine is what the ready check reads. If only one holds the mark, a person or the check misses it.

**Example:**
- Bank: the "Score the application" ICE page opens with the Thin line; its spine entry has `metadata: {thin: true}`.
- Shop: the Alignment loop finds a Thin line on the page but no `thin: true` in the spine. That is drift, and the loop fixes it.
- Clinic: after the deepening, both the line and the field go.

## K3 — Where the feature-to-story map is kept

**Question:** The epic keeps the feature-to-story map, and the plan's Tree already shows each story with its feature. Which one does the eval play read?

**Answer (proposed):** The map is on the epic's issue, as a list "feature → story". The eval play reads it there. The plan's Tree keeps showing each story with its feature, and must agree with the epic, by the Plan rule "the plan file and the tracker always agree".

**Why it matters:** The eval play reads the epic, not the plan file. If the map is only in the plan file, the eval play must read one more file.

**Example:**
- Clinic: Epic #341 lists "Pick a free slot → #342; Send a reminder → #343". Plan #340's Tree shows the same.
- Shop: Story "Save the card for next time" joins Epic #121. The plan play adds its line to the epic and to the plan's Tree, in one step.
- Bank: Epic #52's list and Plan #51's Tree disagree on Story #55. That is drift, and managing the plan fixes both together.

## K4 — Does Capability or Feature need a change?

**Question:** `/shape-slice` can make a new capability or feature with a thin ICE. Must the Capability or Feature kind say something about this?

**Answer (proposed):** No. The thin mark belongs to the ICE. The part keeps its own rules (a capability with no domain waits in the holding folder; a feature with no capability waits in `features/`). If you want the part's page to show "its ICE is thin", that changes Capability and Feature, and it goes to a separate need.

**Why it matters:** The need touches five kinds only. A change to a sixth kind needs your word first.

**Example:**
- Shop: new capability "Gift cards" sits in `capabilities/gift-cards/` with no domain; only its ICE has the mark.
- School: new feature "Send a note home" is in Capability Messaging; its page does not change.
- Clinic: the patient persona's product owner wants the Booking page to warn too; that goes to a new need.
