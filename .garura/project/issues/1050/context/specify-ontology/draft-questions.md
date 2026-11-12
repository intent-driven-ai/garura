# Draft — the questions (stage `scope`, step 1)

Need: #1050 (the ontology change for ADR 067: a play finds a feature's story through the product model when no plan file marks it). Kinds it touches: Feature, Story, Plan.

## Opening

You decide which questions the ontology must answer for this need. There are two changed questions (Q19 and Q20) and two new ones (Q48 and Q49). When you say yes, the next stage tests every change to the Feature, Story and Plan kinds against these four questions, and only against them. When you change a question, this stage is done again with your words before the next stage starts.

## Changed questions

### Q20 — Given a tracker issue, which kind is it? (changed answer)

- **Question:** When no plan file marks a feature's story, how does a play find that story?
- **Answer (proposed):** It takes the issue that the feature names in the product model, and that issue must be a Story; a play never finds a story by its title.
- **Why it matters:** Without this answer, a play with no plan file finds no story and files a second one. If a play matches by title, it files a renamed story again.
- **Example:**
  - A clinic: the plan for self-booking is lost. The feature "Send a reminder" names Story #343, so the play finds #343.
  - A shop: the plan file marks Story #122 for "Guest checkout". The play uses that mark first.
  - A bank: the plan marks no epic for a slice. The play makes a new epic, because an epic is found only by the plan file.

### Q19 — Given a feature, which slices group it, which story delivers it, and which epic holds that story? (changed answer)

- **Question:** When a slice holds a feature that is already built, does the plan hold that feature?
- **Answer (proposed):** No. A plan, when it is made or updated, holds only pending work. A feature whose `issue` names a closed Story is already built. It gets no story in the plan, and the epic's feature-to-story map has no line for it. The brief names it only as left out, because it is built. Each other feature of the slice gets one Story in the slice's epic.
- **Why it matters:** The ontology now says each epic gets its own story for each feature. ADR 067 says a built feature gets no new story. If the ontology does not change, agents read two rules that disagree. If a plan holds built features, it shows done work as work to do, and a builder can do it again.
- **Example:**
  - A clinic: "Send a reminder" is built, and its Story #343 is closed. The new slice "Follow-up visits" also holds it. The plan and the epic "Follow-up visits" do not hold it. The brief says: left out, already built.
  - A shop: "Guest checkout" is built under closed Story #122. The plan for "Pay in one minute" does not hold it.
  - A bank: "Upload documents" names closed Story #53. The epic "Upload once" has no line for it in its feature-to-story map.

## New questions

### Q48 — Given a feature, which story was filed for it in the tracker?

- **Question:** Given a feature in the product model, which tracker story was filed for it?
- **Answer (proposed):** The feature's `issue`: the Story filed for that feature, as one issue number or key. It keeps the link between a feature and its story's issue number. It is optional; a feature can name no issue. It names a story, never a plan or an epic.
- **Why it matters:** Today the model writes this field for some features, but the ontology and the spine schema do not define it. So each play can read it in a different way. Without a meaning, a play cannot trust it as the way to a feature's story when the plan file is gone.
- **Example:**
  - A clinic: the feature "Send a reminder" names issue #343, a Story.
  - A shop: the feature "Guest checkout" names issue #122, a Story.
  - A school: the feature "Mark attendance" names no issue yet, because no story was filed for it.

### Q49 — When a new slice holds a feature, does its epic need a new story for that feature?

- **Question:** A new slice holds a feature, and no plan file marks a story for it. Does the slice's epic need a new story?
- **Answer (proposed):** Only when the feature names no story. The issue that the feature names decides:
  - An open story: no new story. The play moves that story under the new epic. The brief shows the move and the old parent before the yes.
  - A closed story: no new story. The feature is built, so the plan leaves it out (see Q19).
  - No issue: the play makes a new story.
  - ICE not ready: the play does not use the named story.
  - The run stops before any tracker write when the named issue is not in the tracker, is not a Story, is named by two features, or when the feature is in two slices of one plan.
- **Why it matters:** If the play makes a story for every feature, it files stories for work that exists or is done. If it moves a story without showing it, a person loses track of it. If it uses a wrong issue, the epic holds work that is not the feature.
- **Example:**
  - A shop: "Guest checkout" names closed Story #122. The new epic gets no story for it.
  - A clinic: "Send a reminder" names open Story #343. The play moves it under the new epic and shows the old parent.
  - A bank: "Show the decision" names no issue. The play makes a new story.
  - A delivery firm: "Track a parcel" names #88, a Chore. The run stops before any tracker write.

## Kept for the links stage (not asked here)

This is a design choice about the kinds, not a question a person asks to find something out. The `links` stage proposes an answer from ADR 067, for you to confirm:

- Whether a story that already sits under another plan's epic also stops the run, or the move shown in the brief is enough.
