# Links and rules draft — ontology v11 (#846, plan 788)

You decide the exact words that change in five kinds — Slice, Plan, Epic, Story and ICE — and in the flow line, link line 1 and eight question lines. Each change below quotes the v10 text ("before") and gives the new text ("after"), so the write stage applies it word for word. Everything follows the questions and kinds you agreed (K1–K4 as proposed); one point needs your choice, L1, at the end.

Sources: `draft-questions.md` (yes, 2026-10-24), `draft-kinds.md` (yes, 2026-10-24, K1–K4 as proposed), `need.md`, ontology v10.

Not touched: every other kind, Q1–Q28, Q30–Q32, Q35, the "Not yet defined" list and older log lines. No new kind is listed under "Not yet defined".

---

## A. Head of the ontology

**A1 — How it flows**

Before: "… → a **Slice** groups Features from any Capabilities, in order, into one vertical a person can test end to end → the plan play makes a **Plan** right after `/shape-slice`: the Plan is given the Business Intent, holds every Slice that serves it, and creates one **Epic** for each, with its Stories → the Epic holds one **Story** for each Feature of the Slice; each Story delivers its Feature …"

After: "… → a **Slice** groups Features from any Capabilities, in order, into one vertical a person can test end to end; `/shape-slice` writes the link "slice serves business intent", a thin ICE for each part the slice needs that has no ICE, and the slice's hidden file, with one entry for each Feature → the plan play makes a **Plan** right after `/shape-slice`: the Plan is given the Business Intent, holds every Slice that serves it, and creates one **Epic** for each, with its Stories, and writes nothing in the evals folder → the Epic holds one **Story** for each Feature of the Slice, and keeps the map from each Feature to its Story; each Story delivers its Feature …"

(The text before and after the quoted part does not change.)

**A2 — Link line 1**

Before: "1. A Plan is made by the plan play right after `/shape-slice`. It is given one Business Intent; it holds every Slice that serves that intent; it creates one Epic for each Slice, with its Stories (three actions, in this order)."

After: "1. A Plan is made by the plan play right after `/shape-slice`. It is given one Business Intent; it holds every Slice that serves that intent; it creates one Epic for each Slice, with its Stories (three actions, in this order). It writes nothing in the evals folder."

---

## B. Slice

**B1 — What it is (two sentences)**

Before: "It serves one or more business intents: `/shape-slice` writes that link when it shapes the slice, and writes nothing else (no plan, no epic, no story, no eval)."
After: "It serves one or more business intents: `/shape-slice` writes that link when it shapes the slice, with a thin ICE for each part the slice needs that has no ICE, and the slice's hidden file; it writes no plan, no epic, no story and no eval."

Before: "one **hidden file**, beside the eval, which holds its stories' failure conditions and recovery conditions;"
After: "one **hidden file**, beside the eval, which holds its features' failure conditions and recovery conditions;"

**B2 — Lives at (last sentence)**

Before: "… where `<plan-id>` is the issue number of its first business intent — worked out, never stored"
After: "… where `<plan-id>` is the issue number of its first business intent — worked out, never stored. `/shape-slice` makes the eval folder, also when no plan file exists yet"

**B3 — Property row "Eval"**

Before: "Built by the eval play from the epic, the stories and the hidden file the plan play wrote; kept in its home plan's evals folder, beside the hidden file"
After: "Built by the eval play from the epic (with its feature-to-story map), the stories and the hidden file `/shape-slice` wrote; kept in its home plan's evals folder, beside the hidden file"

**B4 — Property row "Hidden file"**

Before: "| Hidden file | `failure-and-recovery.md` in its eval folder: one entry for each story of its epic — the story (its issue, title and feature), the two ICE it was written from, its failure conditions (each "Fails if" line of the two ICE, in the plan play's words, each with a short id such as F1; "none" when the two ICE have none) and exactly one recovery condition for each (…). Written by the plan play. Read by the eval play (all of it) and by the eval when it runs (…); … | yes, once its epic and stories are made |"
After: "| Hidden file | `failure-and-recovery.md` in its eval folder: one entry for each feature of the slice — the feature (its id and name), its capability, the two ICE it was written from (and which of them is thin), its failure conditions (each "Fails if" line of the two ICE, in `/shape-slice`'s words, each with a short id such as F1; "none" when the two ICE have none) and exactly one recovery condition for each (…). Written by `/shape-slice` when it shapes the slice. Read by the eval play (all of it, joined to the stories through the epic's feature-to-story map) and by the eval when it runs (…); … | yes, once the slice is shaped |"

(The "…" parts — the three recovery parts, the readers that never read it, "The ids never leave the eval folder" — do not change.)

**B5 — New link row** (after the row "this → other | Business Intent")

After: "| this → other | ICE | many | Its hidden file is written from the "Fails if" lines of its features' ICE and their capabilities' ICE; it holds no ICE |"

**B6 — Rules**

Before: "- It serves one or more business intents. `/shape-slice` writes the link when it shapes the slice, and writes nothing else."
After: "- It serves one or more business intents. `/shape-slice` writes the link when it shapes the slice, a thin ICE for each part the slice needs that has no ICE, and the slice's hidden file — no plan, no epic, no story and no eval."

Before: "- Its eval reads four things, at two times. The eval play, when it builds the eval, reads its epic, the stories in that epic (their scope of work and Context guidance) and its hidden file — never the usage guide or the code, which are what the build makes. … Neither reads the ICE of a feature or a capability, so the ICE has one interpretation: the one the plan play wrote into the epic, its stories and the hidden file."
After: "- Its eval reads four things, at two times. The eval play, when it builds the eval, reads its epic (with its feature-to-story map), the stories in that epic (their scope of work and Context guidance) and its hidden file, and joins each entry to its story through that map — never the usage guide or the code, which are what the build makes. … Neither reads the ICE of a feature or a capability, so each line of an ICE has one interpretation: the one `/shape-slice` wrote into the hidden file (the "Fails if" lines) or the one the plan play wrote into the stories (every other line)."

Before: "- It has one hidden file, `failure-and-recovery.md`, in its eval folder. The plan play writes it from the same two ICE as each story: each story of its epic has one entry, with its failure conditions and exactly one recovery condition for each."
After: "- It has one hidden file, `failure-and-recovery.md`, in its eval folder. `/shape-slice` writes it when it shapes the slice, from each feature's ICE and that feature's capability's ICE, by `standards/rules/expectation-generation.md`: each feature of the slice has one entry, with its failure conditions and exactly one recovery condition for each "Fails if" line, marked "the builder can fix this alone" or "a person must decide". When one of the two ICE is thin, the entry says so."

Before: "- When its epic gains a story (its slice gains a feature), the plan play adds that story's entry to the hidden file in the home plan's folder, for whichever plan it runs."
After: "- When it gains a feature, `/shape-slice` adds that feature's entry to the hidden file in the home plan's folder; the plan play then adds the story to the epic, with its line in the feature-to-story map."

New rule (after the rule above): "- `/shape-slice` makes its eval folder, `.garura/project/plans/<plan-id>/evals/<slug>/`, in its home plan's folder, also when no plan file exists yet. The plan play later writes the plan file beside it and finds the folder there."

---

## C. ICE

**C1 — What it is (one sentence becomes three)**

Before: "No work item carries it: the plan play reads a Feature's ICE and that Feature's Capability's ICE when it makes the Story, and writes the Story's scope of work and Context guidance and the slice's hidden file from them."
After: "No work item carries it. Two plays read it, each for its own lines: `/shape-slice` reads the "Fails if" lines and writes the slice's hidden file from them; the plan play reads every other line of a Feature's ICE and that Feature's Capability's ICE when it makes the Story, and writes the Story's scope of work and Context guidance from them. It can be **thin**: proposed by `/shape-slice` from the person's answers, and marked so."

**C2 — Lives at (last two sentences)**

Before: "Its spine entry is one item in the `ices` list in `_spine.yaml` — `id` (opaque, stable), `for` (…), `for_kind` (…), `doc` (…) and `metadata`. The entry holds no business intent ids and no ready answer."
After: "Its spine entry is one item in the `ices` list in `_spine.yaml` — `id` (opaque, stable), `for` (…), `for_kind` (…), `doc` (…) and `metadata` (which holds `thin: true` while the ICE is thin). A thin ICE's page opens, before `## Intent`, with one line: "Thin: proposed by `/shape-slice` from the person's answers; deepen with `/discover-capabilities`." The entry holds no business intent ids and no ready answer."

**C3 — New property row** (before "Ready answer")

After: "| Thin mark | That it is thin: the Thin line at the top of its page and `thin: true` in its spine entry's `metadata`, both set by `/shape-slice` and both removed by the play that deepens it | no — only while it is thin |"

**C4 — Link row "Story"**

Before: "| other → this | Story | many | A story is written from it — a story reads its feature's ICE and that feature's capability's ICE |"
After: "| other → this | Story | many | A story is written from it — a story reads every line of its feature's ICE and that feature's capability's ICE except the "Fails if" lines |"

**C5 — New link row** (after the row above)

After: "| other → this | Slice | many | A slice's hidden file is written from its "Fails if" lines — one entry for each feature of the slice |"

**C6 — Rules**

Before: "- No work item carries it. The plan play reads it: when it makes a Story, it reads the Story's Feature's ICE and that Feature's Capability's ICE, and writes the Story's scope of work and Context guidance and the slice's hidden file from them. The build play's context sub-agent …"
After: "- No work item carries it. Each line of it has one reader that writes from it. `/shape-slice` reads the "Fails if" lines of each feature's ICE and that feature's capability's ICE, and writes the slice's hidden file. The plan play, when it makes a Story, reads every other line of the Story's Feature's ICE and that Feature's Capability's ICE, and writes the Story's scope of work and Context guidance. The build play's context sub-agent …"

(The rest of that rule does not change.)

Before: "  - **Partly ready:** as ready, but with gaps outside the ICE's parts that do not stop work — no domain, no "identified by". Work starts, and the gaps are listed."
After: "  - **Partly ready:** as ready, but with gaps that do not stop work — no domain, no "identified by", or the thin mark (gap: "thin ICE"). Work starts, and the gaps are listed."

Before: "- An ICE starts only with all three parts present. A part that is present can start work however thin or even wrong it is; the ready check does not judge a part's correctness or richness — that is the product owner's job."
After: "- An ICE starts only with all three parts present. A part that is present can start work however short or even wrong it is; the ready check does not count lines and does not judge a part's correctness or richness — that is the product owner's job. It reads only the thin mark."

Before: "- It is written at the depth that is known: a light ICE has one line in each of its three parts; a full one has every line of its three parts."
After: "- It is written at the depth that is known. A **thin ICE** is one that `/shape-slice` proposed from the person's answers, when a part the slice needs has no ICE: at least a goal, a limit and one "Fails if" line in Intent, one line in Context, one line in Expectation, and the thin mark. An ICE is thin because it carries the mark, not because it has few lines: an ICE with few lines and no mark is not thin, and the product owner judges its depth."

New rules (after the rule above):
"- When `/shape-slice` proposes a thin ICE, it warns the person that a thin ICE can cause problems later and that `/discover-capabilities` can deepen it. It never sends the person back to a discovery play, and nothing stops."
"- The thin mark is kept in two places that agree: the Thin line at the top of its page and `thin: true` in its spine entry's `metadata`. The play that deepens the ICE removes both. When only one is there, it is drift for the Alignment loop."

**C7 — States:** no change. Thin is a mark, not a state.

---

## D. Plan

**D1 — What it is (two sentences)**

Before: "When it creates the stories of an epic, it also writes the slice's hidden file, from the same two ICE of each story, with exactly one recovery condition for each "Fails if" line. So it interprets each ICE once."
After: "It writes nothing in the evals folder: `/shape-slice` wrote the slice's hidden file there before it. It reads every line of each ICE except the "Fails if" lines."

**D2 — Lives at**

Before: "… which holds `evals/` (one folder for each slice whose eval is kept here, with its hidden file `failure-and-recovery.md` and its eval) and `guides/` (one guide for each such slice)"
After: "… which holds `evals/` (one folder for each slice whose eval is kept here, with its hidden file `failure-and-recovery.md` and its eval; `/shape-slice` can make it before the plan file exists) and `guides/` (one guide for each such slice)"

**D3 — Property row "Folder"**

Before: "Beside the plan file: `evals/<slug>/`, which holds the hidden file `failure-and-recovery.md` (written by the plan play) and the eval (written by the eval play), …"
After: "Beside the plan file: `evals/<slug>/`, which holds the hidden file `failure-and-recovery.md` (written by `/shape-slice`) and the eval (written by the eval play), …; the plan play writes nothing in `evals/` …"

Write stage: put "the plan play writes nothing in `evals/`" as its own sentence before "A slice it holds whose home is another plan …".

**D4 — Rules**

Before: "- When it creates a slice's epic and stories, the plan play writes the slice's hidden file from the same two ICE as each story: for each "Fails if" line, exactly one recovery condition, by `standards/rules/expectation-generation.md`, marked "the builder can fix this alone" or "a person must decide". It puts the goals, limits, Context guidance and expectations in the story, and the failure and recovery conditions in the hidden file, never both in one place."
After: "- The plan play writes only the plan file, the epic and the stories. It writes nothing in the evals folder; `/shape-slice` wrote the slice's hidden file there. It puts the goals, limits, Context guidance and expectations of the two ICE in the story, and the feature-to-story map on the epic. The failure and recovery conditions stay in the hidden file, never in the story."

Before: "- The plan play reads all of each ICE, so it is not a builder. No builder reads what it writes into `evals/`."
After: "- The plan play reads every line of each ICE except the "Fails if" lines, which are `/shape-slice`'s. It is not a builder."

Before: "- Its plan file and the tracker always agree; managing a plan changes both together and never touches branches or code."
After: "- Its plan file and the tracker always agree — its Tree and each epic's feature-to-story map show the same story for each feature; managing a plan changes both together and never touches branches or code."

Link rows and other property rows (Tree included, by K3): no change.

---

## E. Epic

**E1 — What it is**

Before: "The plan play creates it, with its Stories, one for each Feature of its Slice. It serves the business intents its Slice serves. Its Slice's eval reads it, with its Stories, to learn what it delivers."
After: "The plan play creates it, with its Stories, one for each Feature of its Slice, and keeps on it the map from each Feature to the Story that delivers it. It serves the business intents its Slice serves. Its Slice's eval play reads it, with its Stories and its map, to learn what it delivers and which Story each hidden-file entry is for."

**E2 — New property row** (after "Represents")

After: "| Feature-to-story map | For each feature of its slice, the story that delivers it, as a list "feature → story" on the issue. Written by the plan play when it makes the stories; a line is added when a story joins. Read by the eval play to join each hidden-file entry to its story | yes, once it holds a story |"

**E3 — Rules**

Before: "- Its stories are one for each feature of its slice; when its slice gains a feature, a new story joins it. It never holds two stories for one feature."
After: "- Its stories are one for each feature of its slice; when its slice gains a feature, a new story joins it, with its line in the feature-to-story map. It never holds two stories for one feature."

Before: "- Its slice's eval reads it, with its stories, to learn what it delivers. So its title says what a person can see the product do, not how it is built."
After: "- Its slice's eval play reads it, with its stories and its feature-to-story map, to learn what it delivers and which story each hidden-file entry is for. So its title says what a person can see the product do, not how it is built."

New rule (after the rule above): "- Its feature-to-story map and its plan's Tree always agree. When they do not, it is drift, and managing the plan fixes both together."

Link rows: no change.

---

## F. Story

**F1 — What it is**

Before: "The failure and recovery conditions of those two ICE go to its slice's hidden file, never to the story."
After: "The failure and recovery conditions of those two ICE go to its slice's hidden file, in its feature's entry, written by `/shape-slice`, never to the story."

**F2 — Property row "Scope of work"**

Before: "Its own words for its work, written by the plan play when it makes the story from its feature's ICE and its capability's ICE, on the issue."
After: "Its own words for its work, written by the plan play when it makes the story from every line of its feature's ICE and its capability's ICE except "Fails if", on the issue."

**F3 — Rules**

Before: "- It never holds a failure condition or a recovery condition — not in its scope of work, its Context guidance, its title or its examples. The plan play puts them in its slice's hidden file."
After: "- It never holds a failure condition or a recovery condition — not in its scope of work, its Context guidance, its title or its examples. `/shape-slice` puts them in its slice's hidden file, in its feature's entry."

Before: "- When one of those ICE changes after the story is made, its scope of work, its Context guidance and its entry in the slice's hidden file are drift for the Alignment loop. They are not changed without a word, and they are made again together, from the same two ICE, so the story and the hidden file never disagree."
After: "- When one of those ICE changes after the story is made, its scope of work, its Context guidance and its feature's entry in the slice's hidden file are drift for the Alignment loop. They are not changed without a word. In the same Alignment round, the plan play makes the story again and `/shape-slice` makes the entry again, from the same two ICE, so the story and the hidden file never disagree. When the change removes the thin mark, the entry's thin note goes too."

Link rows: no change.

---

## G. Examples the write stage must fix (step 7, same kinds only)

These v10 examples say the plan play writes the hidden file, or key an entry by story. At the write stage they change to match:
- Slice, Clinic example: "The hidden file's entry for Story #342 "Pick a free slot"" → "The hidden file's entry for Feature "Pick a free slot", written by `/shape-slice` before Story #342 existed"; and "The eval play reads Epic #341, …" gains "and joins the entry to Story #342 through the epic's map".
- Plan, Clinic example: "(written by the plan play)" → "(written by `/shape-slice`)".
- Epic, Clinic example: add "Map: Pick a free slot → #342; Send a reminder → #343."
- ICE: add one example of a thin ICE (School, "Send a note home", with the Thin line, `thin: true`, ready answer "partly ready — gap: thin ICE").

---

## H. Question lines

**Q29 — changed**

Before: "- **Q29** — Given a slice, what does its eval test?
  **Answered by:** Slice (its eval, at two times: the eval play reads its Epic, the Stories in that Epic and its hidden file to build the eval; the eval, when it runs …); Epic (what it delivers); Story (…); Slice hidden file (…)"
After: "- **Q29** — Given a slice, what does its eval read, and when?
  **Answered by:** Slice (its eval, at two times: the eval play reads its Epic with its feature-to-story map, the Stories in that Epic and its hidden file, and joins each entry to its Story through that map, to build the eval; the eval, when it runs …); Epic (what it delivers, and its feature-to-story map); Story (…); Slice hidden file (…)
  **Status:** answered"

**Q33 — changed**

Before: "- **Q33** — Given a slice, where are the failure conditions and recovery conditions of its stories kept?
  **Answered by:** Slice (its hidden file `failure-and-recovery.md`, in its eval folder `.garura/project/plans/<plan-id>/evals/<slice>/`, one entry for each story of its epic); a builder never reads it"
After: "- **Q33** — Given a slice, where are its failure conditions and recovery conditions kept, and what does each entry hold?
  **Answered by:** Slice (its hidden file `failure-and-recovery.md`, in its eval folder `.garura/project/plans/<plan-id>/evals/<slice>/`, one entry for each feature of the slice: the feature, its capability, the two ICE and which is thin, its failure conditions with their ids, and one recovery condition for each — when, way back, who fixes); a builder never reads it
  **Status:** answered"

**Q34 — changed**

Before: "- **Q34** — Who writes the failure conditions and recovery conditions of a slice's stories?
  **Answered by:** Plan (the plan play writes the slice's hidden file when it creates the epic and its stories, from the same two ICE as each story, with exactly one recovery condition for each "Fails if" line); Story is written from two ICE"
After: "- **Q34** — Who writes the failure conditions and recovery conditions of a slice, and when?
  **Answered by:** Slice (`/shape-slice` writes its hidden file when it shapes the slice, one entry for each feature, from that feature's ICE and its capability's ICE, with exactly one recovery condition for each "Fails if" line, and adds an entry when the slice gains a feature); Plan (the plan play writes nothing in the evals folder)
  **Status:** answered"

**New, after Q35:**

"- **Q36** — Given an entry in a slice's hidden file, which story of the epic is it for?
  **Answered by:** Epic (its feature-to-story map, written by the plan play); the eval play joins each entry to its story by the entry's feature; Story holds no failure condition and no recovery condition
  **Status:** answered"

"- **Q37** — Given an ICE, which play reads each part of it, so each part has one interpretation?
  **Answered by:** ICE (each line has one reader: `/shape-slice` reads the "Fails if" lines and writes the hidden file; the plan play reads every other line and writes the story); Slice is written from ICE; Story is written from ICE; a builder reads neither
  **Status:** answered"

"- **Q38** — When a slice needs a capability or a feature that has no ICE, what ICE does it get, and how does a person know it is thin?
  **Answered by:** ICE (a thin ICE, proposed by `/shape-slice` from the person's answers, with at least one line in each part; the thin mark on its page and in its spine entry; the warning, never a stop; the mark stays until a play deepens it)
  **Status:** answered"

"- **Q39** — When an ICE changes after its hidden-file entry and its story are made, which play makes each again?
  **Answered by:** Story (both are drift for the Alignment loop; in the same round the plan play makes the story again and `/shape-slice` makes the entry again, from the same two ICE)
  **Status:** answered"

"- **Q40** — Where does `/shape-slice` write the hidden file when the business intent has no plan yet?
  **Answered by:** Slice (at `.garura/project/plans/<plan-id>/evals/<slug>/failure-and-recovery.md`, `<plan-id>` worked out from its first business intent; `/shape-slice` makes the folder); Plan (the plan play finds the folder there)
  **Status:** answered"

C1 (can work start from a thin ICE) is not a question line: it is the ICE's ready-check rule, in C6.

---

## L1 — The thin ICE in Intent: "a goal, a limit and one Fails if", or "at least one line"?

**Question:** What is the least a thin ICE must hold in its Intent part?

**Answer (proposed):** A goal, a limit and one "Fails if" line, as decision 7 of #844 said, plus one line in Context and one in Expectation, as C1 agreed. The kinds draft said "at least one line in each part"; we propose the stricter words in the rule (C6), because a thin ICE with no "Fails if" line gives `/shape-slice` nothing to write in the hidden file.

**Why it matters:** With "at least one line", a thin ICE can have a goal only. Then its hidden-file entry says "none", and the eval tests no failure for that feature, while the person was told the ICE is only thin.

**Example:**
- School: the thin ICE of "Send a note home" has "Fails if: a note goes to the wrong parent", so its entry has F1.
- Shop: a thin ICE of "Gift cards" with a goal only → under the stricter rule, `/shape-slice` proposes one limit and one "Fails if" line from the person's answers, and the person confirms or changes them; nothing stops.
- Bank: a thin ICE of "Score the application" with a goal, a limit and a "Fails if" line, a Persona line and a Done means line → partly ready, gap: thin ICE.
