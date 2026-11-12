# Draft — the questions (stage `scope`, step 1)

Need: #1050 (the ontology change for ADR 068: each product feature has one Feature issue that names it). Kinds it touches: Feature, Story, Epic, Plan, Slice.

## Opening

You decide which questions the ontology must answer for this need. There are four changed questions (Q19, Q20, Q26, Q43) and six new ones (Q48 to Q53). When you say yes, the next stage tests every change to the Feature, Story, Epic, Plan and Slice kinds against these ten questions. When you change a question, this stage is done again with your words before the next stage starts.

The two new questions of the earlier draft (Q48, a feature names its story, and Q49, a new story for each epic) came from ADR 067. ADR 068 replaces ADR 067, so this draft drops them.

## Changed questions

### Q20 — Given a tracker issue, which kind is it?

- **Question:** What does an issue of type Feature stand for?
- **Answer (proposed):** It is a Feature issue: it stands for exactly one product feature, and its text names that feature in one line, `Represents: <feature id>`. The old meaning, a "feature item" that only groups stories, goes.
- **Why it matters:** Today the type Feature means a group of stories, not the Feature kind. Agents then read one word in two ways.
- **Example:**
  - A clinic: Feature issue #40 has the line `Represents: fn-12` ("Send a reminder").
  - A shop: Feature issue #71 has the line `Represents: fn-3` ("Guest checkout").
  - A bank: an old issue of type Feature groups four features, so it is given another type.

### Q19 — Given a feature, which slices group it?

- **Question:** How many slices and plans can hold one feature?
- **Answer (proposed):** Many. Slices and plans only group features, so one feature can be in two slices and in two plans. It still has only one Feature issue.
- **Why it matters:** If each slice or plan files its own issue for a feature, the tracker holds the same work two times.
- **Example:**
  - A clinic: "Send a reminder" is in the slice "Book a visit" and in the slice "Follow-up visits".
  - A school: "Mark attendance" is in two plans, one for teachers and one for parents.
  - A shop: "Guest checkout" is in two slices, and both use Feature issue #71.

### Q43 — Given an item in a plan, which kind of item can hold it?

- **Question:** Where does a Story sit?
- **Answer (proposed):** Always inside the Feature issue of its feature. The tree is: Epic, then Feature issue, then Story, then Spike, Chore or Bug.
- **Why it matters:** A Story straight under an epic is not linked to a feature, so no one knows which feature it builds.
- **Example:**
  - A bank: Epic "Open an account" holds Feature issue "Upload documents", which holds the Story "Check the file size".
  - A clinic: the Story "Send the reminder by text" sits in Feature issue "Send a reminder".
  - A shop: a Bug about a wrong total sits under the Story "Show the total", in Feature issue "Guest checkout".

The answers of Q1, Q4, Q7, Q18, Q22 and Q23 follow this tree: each names the Feature issue between the Epic and the Story, and none names a feature item.

### Q26 — Given a story, what is its scope of work?

- **Question:** Which tracker issue holds a feature's scope of work and its Context guidance?
- **Answer (proposed):** The Feature issue. It is written from the feature's ICE and its capability's ICE, and it never holds a failure condition or a recovery condition. A Story is one piece of the work inside it.
- **Why it matters:** If the scope is on each Story, the builder and the eval can read different scopes for one feature.
- **Example:**
  - A school: Feature issue "Mark attendance" holds the goal "a teacher marks a class in one minute".
  - A bank: Feature issue "Upload documents" holds the limit "files up to 10 MB".
  - A clinic: the builder of the Story "Send the reminder by text" reads the Context guidance on Feature issue "Send a reminder".

The answers of Q13, Q29, Q32, Q36, Q37 and Q39 change the same way: each reads "Feature issue" where it reads "story". The epic's feature-to-story map names Feature issues, one line for each feature.

## New questions

### Q48 — Given a feature, which tracker issue stands for it?

- **Question:** How does a play find a feature's issue?
- **Answer (proposed):** First by the plan file's mark. When there is no mark, by the one issue of type Feature, open or closed, whose text has the exact line `Represents: <feature id>`. Two such issues are a duplicate: the run stops and asks the person. A play never finds an issue by its title.
- **Why it matters:** A match by title fails when a person renames an issue, and the play files a second one.
- **Example:**
  - A shop: no plan file marks "Guest checkout", so the play finds #71 by its line `Represents: fn-3`.
  - A clinic: two issues both have `Represents: fn-12`, so the run stops and asks the clinic manager.
  - A bank: an issue titled "Upload documents" has no Represents line, so it is not a match.

### Q49 — Does a feature in the product model name its tracker issue?

- **Question:** Does the product model hold a feature's issue number?
- **Answer (proposed):** No. Only the Feature issue holds the link, and it points to the model. No feature has an `issue` property.
- **Why it matters:** A link kept on two sides drifts, and someone must keep both sides the same.
- **Example:**
  - A clinic: the feature fn-12 has no issue number, and Feature issue #40 names fn-12.
  - A school: Feature issue #55 moves to another tracker project, and nothing in the model changes.
  - A shop: the model page of "Guest checkout" names no tracker issue.

### Q50 — Which features can a new slice or plan take in?

- **Question:** Can a new slice or plan hold a feature that is already built?
- **Answer (proposed):** No. A slice and a plan hold only features that are not built yet.
- **Why it matters:** If a plan holds built features, it shows done work as work to do, and a builder can build it again.
- **Example:**
  - A clinic: "Send a reminder" is built, so the new slice "Follow-up visits" leaves it out.
  - A shop: "Guest checkout" is built, so the plan "Pay in one minute" does not hold it.
  - A bank: "Show the decision" is not built, so the new slice takes it in.

### Q51 — Which epic holds a Feature issue that two epics need?

- **Question:** When a second epic needs a Feature issue, which epic holds it?
- **Answer (proposed):** One epic at a time. The play asks the person which epic it goes under, and does not move it without that answer.
- **Why it matters:** A move with no question takes work out of one plan, and no one sees it.
- **Example:**
  - A school: "Mark attendance" sits under the epic "Teacher day"; the epic "Parent view" also needs it, so the play asks the head teacher.
  - A shop: "Guest checkout" stays under "Fast checkout" until the store manager says to move it.
  - A bank: the branch manager picks "Open an account" for "Upload documents".

### Q52 — When does a feature count as built?

- **Question:** When does a feature count as built?
- **Answer (proposed):** When a person closes its Feature issue, through `/reshape-plan` "finish". Then every slice and plan that holds it counts it as complete. Closed Stories do not close the Feature issue.
- **Why it matters:** If closed Stories close the feature by themselves, a feature with work still to find counts as done.
- **Example:**
  - A clinic: all three Stories of "Send a reminder" are closed, but the feature is built only when the clinic manager finishes #40.
  - A shop: the store manager finishes #71, and both slices that hold "Guest checkout" show it complete.
  - A bank: "Upload documents" has one open Story, so it is not built.

### Q53 — What happens to a Story with no Feature issue?

- **Question:** How does a Story with no Feature issue as its parent get one?
- **Answer (proposed):** A play researches the product model to find the Story's feature, and puts the Story inside that feature's Feature issue. When no feature fits, the feature is made and its Feature issue is filed.
- **Why it matters:** A Story with no feature is work that no slice, plan or eval can see.
- **Example:**
  - A school: the Story "Export attendance to a file" matches the feature "Mark attendance", so it goes inside that Feature issue.
  - A bank: the Story "Freeze a card" matches no feature, so the feature is made and its Feature issue is filed.
  - A clinic: the Story "Cancel by text" matches "Send a reminder", so it goes inside #40.

## Kept for the links stage (not asked here)

This is a design choice about the kinds, not a question a person asks to find something out. The `links` stage proposes an answer from ADR 068, for you to confirm:

- How plan B shows a feature whose Feature issue sits under plan A's epic.
