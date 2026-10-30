# Draft — questions the ontology must answer (#720, stage: scope)

You decide which questions the ontology must answer about a plan, and about a thin ICE. Each one
you confirm becomes a test for the next two stages: the kinds, then the links and rules. Type yes to
keep the list, or say which question to change, add or drop.

This need touches two kinds only: the Plan, and the Thin line of the ICE. The plan's status,
direction, item kinds, branch and the record of its changes are operational. They stay in the Plan
kind and in the plan files, never in the product model's index or pages. That is a rule, not a
question: it comes back at the links and rules stage.

## New questions

### Q41 — Given a plan, what is its status?

- **Question:** Must the ontology tell a person the status of a plan?
- **Answer (proposed):** Yes. A plan is Not Started, In Progress, Paused, Done or Dropped. A person
  sets it. It is never worked out from the items in the plan. Today the ontology says only
  "active, done or dropped".
- **Why it matters:** A plan that is paused looks the same as a plan in progress. A person who comes
  back after two days picks up the wrong plan.
- **Example:** The clinic's self-booking plan is Paused while the clinic manager waits for the new
  calendar. The shop's guest-checkout plan is In Progress. The bank's loan-decision plan is Dropped,
  because the bank bought a product that does it.

### Q42 — Given a plan, what is its direction?

- **Question:** Must the ontology tell a person the direction of a plan?
- **Answer (proposed):** Yes. A plan has a direction of 1 (next), 2 (next in line), 3 (later) or
  none. A person sets it. It is not a ranking: several plans can have the same direction. It is never
  worked out from the work.
- **Why it matters:** Without it, a person cannot see which plans come next. If it were worked out,
  the order would change when nobody decided to change it.
- **Example:** The shop owner gives guest checkout direction 1 and gift cards direction 3. The clinic
  manager gives two plans direction 1 at the same time. The bank's product owner gives a plan no
  direction until the budget is known.

### Q43 — Given an item in a plan, which kind of item can hold it?

- **Question:** Must the ontology say which kind of item can sit under which kind, in a plan?
- **Answer (proposed):** Yes. A plan holds six kinds of item. An epic is at the top. A feature sits
  under an epic. A story sits under an epic or a feature. A spike, a chore or a bug sits under a
  story.
- **Why it matters:** If any item can sit anywhere, a bug ends up under an epic, and nobody can find
  the story that brought the bug in.
- **Example:** In the shop's plan, the bug "card fails on mobile" sits under the story "pay as a
  guest". In the clinic's plan, the story "pick a free slot" sits under the feature "book online",
  which sits under an epic. In the bank's plan, a chore "move the scoring rules" sits under the story
  "score the application".

### Q44 — Given a plan, on which branch is its work done?

- **Question:** Must the ontology tell a person the branch of a plan?
- **Answer (proposed):** Yes. While its work is in progress, a plan has its own branch,
  `plan/<id>/base`. Every change to the plan is made there. Main's copy names that branch.
- **Why it matters:** A person who changes a plan on another branch makes a second copy that
  disagrees with the first.
- **Example:** The shop's plan 120 is worked on `plan/120/base`. The clinic's plan 340 is Not
  Started, so it has no branch yet. The bank's plan 51 is Done, so no work is in progress on a branch.

### Q45 — Given a plan, where is the record of each change to it?

- **Question:** Must the ontology tell a person where the changes to a plan are recorded?
- **Answer (proposed):** Yes. The plan file keeps no history. Each time a person changes a plan, the
  change lands as one commit. Its message names what the person asked, the rules they overrode, and
  the work that is still owed.
- **Why it matters:** If the plan file kept its own history, it would grow with every change and
  could disagree with the commits.
- **Example:** The shop owner closes a story and renames another: one commit names both. The clinic
  manager puts a story under the wrong kind of item on purpose: the commit names the override. The
  bank's product owner adds a new feature with no slice: the commit says the slice is owed.

### Q46 — Given a plan, how does a person change it?

- **Question:** Must the ontology say how a person changes a plan?
- **Answer (proposed):** Yes. A person changes a plan with `/update-plan`. In one session it changes
  the plan file, the tracker and the product model together, after one approval.
- **Why it matters:** A change made in only one of the three places makes the plan, the tracker and
  the model disagree.
- **Example:** The shop owner says "guest checkout is done" and approves: the plan file and the
  tracker both show it done. The clinic manager adds a new feature: its thin page, its tracker story
  and its plan item come in together. The bank's product owner rejects the list: nothing changes
  anywhere.

### Q47 — Given an ICE, how does a person know it is thin?

- **Question:** Must the Thin line of a thin ICE stop naming one play?
- **Answer (proposed):** Yes. The page of a thin ICE opens with this line: "Thin: proposed from the
  person's words; deepen with `/discover-capabilities`." Its model entry is also marked thin. Today
  the line names `/shape-slice`, but `/update-plan` proposes thin ICE too. This question takes the
  second half of Q38 (below), so each question asks one thing.
- **Why it matters:** A line that names the wrong play tells a person the wrong place to look for the
  answers the ICE came from.
- **Example:** The clinic's thin ICE for "send a reminder" came from a plan session. The shop's thin
  ICE for "save the card" came from shaping a slice. The bank's thin ICE for "upload once" came from a
  plan session. All three pages open with the same Thin line.

## Changed questions

### Q38 — When a slice or a plan needs a capability or a feature that has no ICE, what ICE does it get?

- **Question:** Must Q38 cover a plan as well as a slice?
- **Answer (proposed):** Yes. Today Q38 reads "When a slice needs a capability or a feature that has
  no ICE, what ICE does it get, and how does a person know it is thin?" It changes to the heading
  above. The answer stays a thin ICE, from the person's words, with at least a goal, a limit, one
  "Fails if" line, one Context line and one Expectation line. Its second half moves to Q47.
- **Why it matters:** A feature found while a plan is in progress gets a thin ICE too. If Q38 names
  only the slice, that path has no question that tests it.
- **Example:** The clinic manager finds "cancel by text message" while the plan is in progress. The
  shop owner finds "split the payment" while shaping a slice. The bank's product owner finds "send the
  decision by post" in a plan session. Each feature gets a thin ICE.

### Q20 — Given a tracker issue, which kind is it?

- **Question:** Must Q20's answer cover a tracker issue of type Feature that sits in a plan?
- **Answer (proposed):** Yes. An issue of type Feature in a plan groups stories under an epic. It is
  an item of the plan, not the Feature of the product model. Today the ontology says a Feature is not
  an issue type. The kinds stage decides how the two are told apart.
- **Why it matters:** If one word means two things, a person or an agent links a story to the wrong
  thing.
- **Example:** In the clinic's plan, the issue "book online" of type Feature holds three stories. In
  the shop's model, the feature "guest checkout" is a part of the product with its own ICE. In the
  bank's plan, an issue of type Feature holds the stories of "upload once".

### Q7 — Given a business intent, what does its plan hold?

- **Question:** Must Q7's answer name the plan's status, direction, branch and feature items?
- **Answer (proposed):** Yes. The question stays. Its answer adds the feature item (Q43) and the
  plan's status, direction and branch (Q41, Q42, Q44). The answers of Q1, Q4, Q22 and Q23 name the
  feature item too, where they list the kinds of work item.
- **Why it matters:** A plan that holds a feature item that no answer names fails the check at the
  last stage.
- **Example:** The shop's plan shows: In Progress, direction 1, on `plan/120/base`, an epic with a
  feature and two stories. The clinic's plan shows: Paused, direction 2. The bank's plan
  shows: Done, no direction.
