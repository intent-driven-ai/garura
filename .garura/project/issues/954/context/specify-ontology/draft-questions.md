# Draft — the questions (stage `scope`, step 1)

Need: #954 (make the product ontology match ADR 069: the plan is where the product model meets the work). Kinds it touches: Plan, Epic, Slice, Business Intent, Feature, Capability, Domain, Feature issue, Story.

## Opening

You decide which questions the ontology must answer after ADR 069. Fourteen questions keep their words but get a new answer, and ten questions are new (Q54 to Q63). When you type yes, the next stage tests each change to the kinds against these 24 questions. When you change a question, this stage is done again with your words before the next stage starts.

How to read a grey block: the "-" line is today's text, shortened; the "+" line is the new text. A new question has "+" lines only. Every question not shown here stays as it is.

## Changed questions

### Q1

**Question:** Given a business intent and the product as it is today, which types of work does it need — Epic, Story, Spike, Chore, Bug — what value does each bring, and when would a type be wrong for it?

**Answer:**
```diff
- Plan holds Slice; Epic represents Slice; Feature issue ... sits under Epic; ... Spike, Chore and Bug are children of a Story
+ Plan holds one or more Slices and has one Epic; the Epic holds the Feature issues of all the plan's Slices; a Story sits inside a Feature issue; a Spike or a Bug is a child of a Story; a Chore sits under a Story or under the plan's Epic
```
**Why it matters:** If a play still makes one epic for each slice, one plan gets many epics, and no single work item shows all the work of the plan.
**Example:** Clinic: one epic for "self-booking" and "cancel online". Shop: one epic for "pay as guest" and "save the card". Bank: one epic for "one-day decision" and "upload once". School: one epic for "enrol online" and "pay the fee online".

### Q7

**Question:** Given a business intent, what does its plan hold?

**Answer:**
```diff
- Plan holds every Slice that serves it; Plan creates one Epic for each Slice, and finds or files the Feature issue of each Feature ...
+ Plan holds every Slice that serves the intent and records each Slice with its status; it has one Epic, which holds the Feature issue of each Feature of all its Slices, and the plan's chores; it has one eval; and its Status, Direction and Branch
```
**Why it matters:** The plan is the one place where the model meets the work. If the plan does not hold its slices, nothing does.
**Example:** Clinic: plan for "patients book online" holds two slices and one epic. Shop: plan for "check out as a guest" holds one slice and a chore to clean the cart table. Bank: plan for "loan decision in one day" holds two slices. School: plan for "parents enrol online" holds one slice.

### Q18

**Question:** Given a slice, which epic delivers it, which Feature issues and stories does that epic hold, and which spikes, chores and bugs are under each story?

**Answer:**
```diff
- Epic represents Slice; Epic holds Feature issue; ...
+ The one Epic of each plan that holds the slice; that Epic holds the Feature issues of this slice and of the plan's other slices. The slice names no epic: the plan file names its slices
```
**Why it matters:** If the slice names its epic, the model must change each time the work changes.
**Example:** Clinic: "self-booking" is delivered by the epic of the booking plan. Shop: "pay in one minute" is in two plans; one plan's epic holds its Feature issues, and the other plan shows them as `held_by`. Bank: "upload once" is delivered by the epic of plan "loan decision in one day". School: "enrol online" is delivered by the epic of the enrolment plan.

### Q20

**Question:** Given a tracker issue, which kind is it?

**Answer:**
```diff
- ... Which Epic stands for a slice is found by the plan file's `represents` mark ...
+ ... A plan's one Epic is found by the plan file's mark; a Feature issue by that mark, else by the exact `Represents:` line — never by type alone and never by title (the rest stays)
```
**Why it matters:** A play that looks for "the epic of a slice" finds nothing, because no epic stands for a slice now.
**Example:** Clinic: the plan file marks issue 341 as its epic. Shop: issue 121 has type Epic and the plan file marks it. Bank: an old epic of a slice is not marked, so it is not the plan's epic. School: the plan file marks one epic only.

### Q28

**Question:**
```diff
- Given a slice, where is its eval kept?
+ Given a slice, which eval tests it?
```

**Answer:**
```diff
- Slice (its eval, in the evals folder of the Plan for its first Business Intent: `.garura/project/plans/<plan-id>/evals/<slice>/`)
+ The one eval of each plan that holds it, kept in that plan's evals folder. A slice has no eval of its own, and it names no eval and no folder
```
**Why it matters:** If each slice keeps its own eval, a plan is never tested as one whole before it lands.
**Example:** Clinic: the booking plan's eval tests "self-booking" and "cancel online". Shop: two plans hold "pay in one minute", and each plan's eval tests it. Bank: the eval of the loan plan tests both its slices. School: the enrolment plan's eval tests "enrol online".

### Q29

**Question:**
```diff
- Given a slice, what does its eval read, and when?
+ Given a plan, what does its eval read, and when?
```

**Answer:**
```diff
- Slice (its eval, at two times: the eval play reads its Epic with its feature-to-story map, the Feature issues that map names and its hidden file ...)
+ Plan (its eval, at two times: the eval play reads the plan's Epic, its map and its Feature issues, and the hidden file of each slice the plan holds; the running eval reads the eval, the usage guides, the Context guidance in the eval, and only the recovery parts of the hidden files)
```
**Why it matters:** If the eval reads less than the whole plan, a done plan can land with a slice that no one tested.
**Example:** Clinic: the eval reads one epic and two hidden files. Shop: the eval reads one epic and one hidden file. Bank: the eval reads one epic and the hidden files of two slices. School: the eval reads one epic and one hidden file, never the code.

### Q30

**Question:** When a new slice is shaped for a business intent that already has a plan, which plan holds it?

**Answer:**
```diff
- Plan (one plan for each Business Intent; the new Slice and its Epic are added to it)
+ That one plan. /reshape-plan adds the slice: the plan file records it, and its Feature issues go under the plan's one Epic. No second epic and no second plan
```
**Why it matters:** If the new slice gets its own epic, the plan has two epics and its eval reads only one of them.
**Example:** Clinic: "cancel online" joins the booking plan's epic. Shop: "save the card" joins the guest plan's epic. Bank: "upload once" joins the loan plan's epic. School: "pay the fee online" joins the enrolment plan's epic.

### Q31

**Question:**
```diff
- Given a built slice, how does its eval learn to use it?
+ Given a built slice, how does the plan's eval learn to use it?
```

**Answer:**
```diff
- Slice (its usage guide, delivered by the build, in the guides folder of its home Plan)
+ Plan (the usage guide the build delivers, in the plan's guides folder; how the guides are laid out is left to the /design-eval rework). The slice names no guide
```
**Why it matters:** Without a guide, the eval cannot reach the built product, and the plan cannot pass.
**Example:** Clinic: the guide says "open the booking page and pick a slot". Shop: "in the app, tap Pay as guest". Bank: "upload a file on the loan form". School: "open the enrolment form and add a child".

### Q32

**Question:** Given a story, what does the agent that builds it see?

**Answer:**
```diff
- ... Slice (a builder never reads its eval folder)
+ ... Plan (a builder never reads a plan's evals folder)
```
**Why it matters:** A builder that reads the eval builds to pass the test, not to meet the intent.
**Example:** Clinic: the builder of "pick a slot" reads its Feature issue only. Shop: the builder of "guest checkout" never opens the plan's evals folder. Bank: the builder reads the Context guidance, not the hidden file. School: the builder reads the story and its collected context.

### Q33

**Question:** Given a slice, where are its failure conditions and recovery conditions kept, and what does each entry hold?

**Answer:**
```diff
- Slice (its hidden file `failure-and-recovery.md`, in its eval folder `.garura/project/plans/<plan-id>/evals/<slice>/`, ...)
+ Plan (the slice's hidden file `failure-and-recovery.md`, in `evals/<slug>/` of the plan for the intent the slice was first shaped for; the plays work out the place, and the slice names no hidden file); each entry holds what it holds today
```
**Why it matters:** If the slice names the file, the model points at the work side, which ADR 069 forbids.
**Example:** Clinic: the hidden file of "self-booking" is in the booking plan's folder. Shop: "pay in one minute" is in two plans, and its hidden file is in the first plan's folder only. Bank: the hidden file of "upload once" is in the loan plan's folder. School: the hidden file of "enrol online" is in the enrolment plan's folder.

### Q35

**Question:**
```diff
- When a slice's eval finds a failure, what does the builder get back?
+ When a plan's eval finds a failure, what does the builder get back?
```

**Answer:**
```diff
- Slice (its eval writes a handoff plan from the recovery condition ...)
+ Plan (its eval writes the handoff plan from the recovery condition, as today: what the product does wrong and the way back, never the failure condition)
```
**Why it matters:** If the answer stays on the slice, no kind owns the handoff after the slice eval goes.
**Example:** Clinic: "two patients can book one slot; show the second that it is gone". Shop: "a guest sees a sign-up page; go to payment". Bank: two charges on one loan fee go to a person. School: "a child is enrolled twice; keep the first".

### Q36

**Question:** Given an entry in a slice's hidden file, which Feature issue of the epic is it for?

**Answer:**
```diff
- Epic (its feature-to-story map, written by the plan play, names the Feature issue of each feature)
+ The plan's one Epic (its map has one line for each feature of each slice the plan holds); the eval play joins each entry to its Feature issue by the entry's feature
```
**Why it matters:** If the map holds only one slice, the entries of the other slices join no Feature issue.
**Example:** Clinic: the map names "pick a slot → 342" and "cancel a visit → 350". Shop: "guest checkout → 122 (under epic 121)". Bank: "upload documents → 53" and "score the application → 55". School: "add a child → 610".

### Q40

**Question:** Where does /design-slice write the hidden file when the business intent has no plan yet?

**Answer:**
```diff
- Slice (at `.garura/project/plans/<plan-id>/evals/<slug>/failure-and-recovery.md`, `<plan-id>` worked out from its first business intent ...); Plan (the plan play finds the folder there)
+ In the folder of the plan the intent will have, `evals/<slug>/`, worked out from the slice's first intent; /design-slice makes it, and the plan play finds it there. Nothing in the model stores the place
```
**Why it matters:** If the place is stored in the model, the model names the work side.
**Example:** Clinic: the folder of plan 340 is made before the plan file. Shop: the folder of plan 120 is made by /design-slice. Bank: the folder of plan 51 exists before its epic. School: the folder of the enrolment plan is made first.

### Q43

**Question:** Given an item in a plan, which kind of item can hold it?

**Answer:**
```diff
- ... an epic at the top; a feature (a Feature issue) under an epic; a story under a feature; a spike, a chore or a bug under a story
+ ... the plan's one epic at the top; a feature (a Feature issue) under the epic; a story under a feature; a spike or a bug under a story; a chore under a story or under the epic
```
Assumed: this also changes the Chore kind (ADR 069 §3, "A plan's chores sit in the plan, under its one epic"), which the need's list of kinds does not name.
**Why it matters:** If a chore must have a story, upkeep for the whole plan has no place to sit.
**Example:** Clinic: "move the slots table" sits under the plan's epic. Shop: "clean the old cart data" sits under the epic. Bank: "update the rate config" sits under a story. School: "archive last year's forms" sits under the epic.

## New questions

### Q54

**Question:** Can a part of the product model name a plan, an epic, an eval, a hidden file, a tracker issue or the tracker?

**Answer:**
```diff
+ No. The model is about the business. The links run one way, from the work side to the model: a plan names its slices, and a Feature issue names its feature.
+ A part about plans may still describe plans in general.
```
**Why it matters:** If the model names the work, each change in the tracker makes the model wrong.
**Example:** Clinic: the "Booking" page says no issue number. Shop: the slice "pay as guest" names no plan and no epic. Bank: no page cites an issue as a source. School: the "Enrolment" capability names no eval.

### Q55

**Question:** How many epics does a plan have?

**Answer:**
```diff
+ One. It holds the Feature issues of all the plan's slices, with their stories inside them, and the plan's chores.
+ A bug still sits under the story that brought the defect in.
```
**Why it matters:** With one epic for each slice, a plan's work is split, and a person cannot see the plan as one piece of work.
**Example:** Clinic: two slices, one epic. Shop: three slices, one epic. Bank: two slices, one epic. School: one slice, one epic.

### Q56

**Question:** Given a plan, which eval tests its work?

**Answer:**
```diff
+ One eval for the plan. It covers every feature of every slice the plan holds, also a feature whose Feature issue sits under another plan's epic (`held_by`).
+ When two plans hold one slice, each plan's eval tests its features.
```
**Why it matters:** If an eval covers less than the plan, a feature can land with no test.
**Example:** Clinic: one eval for "patients book online". Shop: "guest checkout" is tested by the evals of both plans that hold it. Bank: one eval tests both slices of the loan plan. School: one eval for the enrolment plan.

### Q57

**Question:** When does a done plan land on main?

**Answer:**
```diff
+ Only when its eval passes. Until the eval runner exists (#801, the runner that runs an eval with no agent), the harness runs the eval by hand before the plan lands.
+ A paused plan still merges into main.
```
**Why it matters:** If a done plan lands with a failing eval, main holds a product that does not meet its intent.
**Example:** Clinic: the booking plan waits until no slot is booked twice. Shop: the guest plan waits until a guest can pay. Bank: the loan plan lands only when a decision comes in one day. School: the enrolment plan pauses for the new term and still merges.

### Q58

**Question:** Given a slice, where do we read whether its work is in progress?

**Answer:**
```diff
+ In the plan file that holds it. The plan records each slice with its status, and a person sets that status.
+ When two plans hold one slice, each plan file records its own status. The model is not asked, and it holds no work status.
```
**Why it matters:** If a play asks the model, it reads a status the model must not hold, and it can change a slice that is in progress.
**Example:** Clinic: the booking plan marks "self-booking" in progress. Shop: one plan marks "pay in one minute" done and the other not started. Bank: the loan plan marks "upload once" not started. School: the enrolment plan marks "enrol online" in progress.

### Q59

**Question:** Given a business intent, how do we find its plan and its tracker issue?

**Answer:**
```diff
+ From the work side only. The plan file names its business intent, and the plan's ID is the intent's issue number.
+ The intent's page has no Tracker line and names no plan. The ids that exist (`bi-<n>`) stay as names.
```
**Why it matters:** When the Tracker line goes, a person needs another way to find the issue and the plan.
**Example:** Clinic: plan 340 names "patients book online". Shop: plan 120 names "check out as a guest". Bank: plan 51 names "loan decision in one day". School: the enrolment plan names "parents enrol online".

### Q60

**Question:** Given a business intent, what was done for it?

**Answer:**
```diff
+ Its What was done says what was delivered and the value it brought, in plain words.
+ It links to no work item: the plan and its issues point back at the intent.
```
**Why it matters:** A link to a work item puts the tracker into a page that a business reader reads.
**Example:** Clinic: "patients now book a slot online; calls to the desk fell". Shop: "guests now pay with an email only". Bank: "small businesses now get a decision on the same day". School: "parents now enrol a child from home".

### Q61

**Question:** Given a part of the model, where do we see where it came from?

**Answer:**
```diff
+ In git history. The spine's `created_by` and `updated_by` name the play or the agent and what it did, never an issue.
+ No spine entry holds an issue number, and no page cites an issue in its Sources.
```
**Why it matters:** An issue number in the model ties the model to one tracker and one piece of work.
**Example:** Clinic: "created by /design-slice, shaped the booking slice". Shop: "updated by /reshape-plan, added a feature". Bank: "created by /specify-capabilities". School: the commit that added "Enrolment" shows why.

### Q62

**Question:** Given a product decision, where is it kept?

**Answer:**
```diff
+ In the part it decides, as that part's content: for example the product profile's security level and its gate, or a business intent's proof.
+ It is the person's answer to a play's question. No decision record lives in the model, and no part links to one. The reason a part changed is in git history.
```
**Why it matters:** A separate record can say one thing while the part says another, and a reader does not know which is true.
**Example:** Clinic: "security level high" is on the profile. Shop: "fewer than 2 in 10 leave at sign-up" is the intent's proof. Bank: a raised security level and its gate are on the profile. School: "parents only, no pupils" is the intent's must-not.

### Q63

**Question:** What does an ADR record, and where is it kept?

**Answer:**
```diff
+ A decision about the code: how the agents and the plays work, and how the product is built.
+ It is kept in the project's ADR folder (`docs/adr/` for Garura), in Markdown, never in the model. An accepted ADR is never edited; a new decision is a new ADR.
```
**Why it matters:** If a product decision goes into an ADR, the model loses the answer, and the ADR folder mixes the product with the code.
**Example:** Clinic: "store bookings in one database" is an ADR. Shop: "pay through one payment service" is an ADR. Bank: "score loans in a separate service" is an ADR. School: "send forms as PDF" is an ADR.

## Not changed

Q2 to Q6, Q8 to Q17, Q19, Q21 to Q27, Q34, Q37 to Q39, Q41, Q42 and Q44 to Q53 keep their words and their answers.
