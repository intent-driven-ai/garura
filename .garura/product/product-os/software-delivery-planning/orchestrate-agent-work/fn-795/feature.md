# Feature: Choose the slice that shows an intent is served

## What it does
A person names a business intent, and /shape-slice chooses the one slice that shows the intent is served: the features from any capability in build order, the one surface a person tests them on, and the persona who tests them there, the tester. The person sees it in one brief and types yes, so what is delivered next is chosen before any work item exists.
- It reads the intent from the product model. When the model has no page for the intent, it writes the page from the intent's issue, says so, and goes on.
- It reads the product model and memory first, and asks the person only what neither answers, in one brief, never as a list of questions. It asks before it shapes the slice only when a gap blocks the slice and no one but the person can answer it.
- The surface and the tester are never a question. An intent does not depend on a surface, so the run proposes them, and the brief shows them for the person's yes.
- It asks no more questions than the project's question setting allows. The questions only the person can answer count first, and every gap left unasked is written as an assumption that the brief shows.
- Every question and answer is kept in the issue's short-term memory, and a question already answered there is never asked again. A proposed answer names its source; where none exists, the question carries no proposed answer, and the brief shows how many have none.
- The slice holds features from any capability, one for each thing the tester must do or see on the surface, in the order the tester can test them, with why that order. What it does not take is listed with why. The slice is written into the model's index with its link to the intent, and its own record holds the tester and what they do.
- A slice that already serves the intent is used again, and no new slice is made. When it no longer serves the intent as it is, a feature is pulled in or pushed out, and the slice stays testable end to end. A slice in progress, whose epic has a story started or done, is never touched by a shaping run; a new slice is shaped instead.
- When nothing can be tested end to end on one surface, no slice is written, and the run says why.
- Each part the slice needs and the model lacks is added or filled at its folder and marked to be deepened later. A part with no ICE gets a thin ICE, with both thin marks, and the brief warns that a thin ICE is enough to start but can give weak stories and weak checks later. Nothing stops, and the person is never sent back to a discovery play.
- The model's own checks must pass for the slice's own pages. An older problem in a page the run does not use is a warning in the brief.
- The person replies yes, change or stop. A change goes back and is shown again; a stop undoes every write. Nothing is committed before the yes. The run opens its own change and lands it through the change plays, on the plan's branch when the intent has a plan.
- With --edit and their own words, a person changes a slice that exists, also one in progress: its name, its outcome, the tester's action, or a part's one-line in the model's index, after they see each change old and new and type yes. The brief says when the slice is in progress and names its epic as out of date. A history line keeps who asked, when, and their words.
- Examples, in different kinds of project:
  - In a clinic's booking app, for the intent that patients book their own appointments online, the slice is self-booking on the booking screen, tested by a patient: pick a free slot, then confirm the booking. Paying for the visit is left out, because the intent is met before any payment.
  - In a shop's checkout project, for the intent that shoppers can check out without an account, the slice is pay without an account on the checkout page, tested by a first-time shopper: enter an address, pay by card, and see the receipt.
  - In a command line tool for data teams, for the intent that an analyst sees a file's size before loading it, the slice is one command that reads a file and prints its row count, tested by a data analyst; a part with no ICE gets a thin one, and the brief warns.
- How it meets the capability: this is "A person chooses what is delivered next as a slice": the slice is chosen, from the model first, before the plan and its work items are made from it.

Status: built, in /shape-slice, with the author-slice skill making each choice. It is the first play of the shaping loop: /shape-slice, then /shape-plan, then /shape-eval. The same run also writes the slice's hidden file; Write the evals that check the work, in Design → Code, holds that part. Not built, or open:
- It must not run until the Agent-work tool lands, because it reads an intent's issue from the wrong repository. This stops a person with no way past it.
- Plays read the whole model by one rule once its index has ICE entries, so older parts break.
- Its checkpoint is pinned: no setting skips the person's yes.

## Inputs / Outputs
- In: a business intent's issue number, and, with --edit, the person's own words.
- In: the intent's page in the product model, or its issue when the model has none.
- In: the product model's index and the pages of each domain, capability and feature, and memory, read through the memory tool.
- In: the project's question setting, and the person's earlier answers in the issue's short-term memory.
- In: the person's reply: yes, change and what to change, or stop, with any answers by their id.
- Out: one slice in the model's index: its features in build order, its surface, and the business intents it serves; and its record, with the tester and what they do, why that order, and what is left out.
- Out: the parts the slice needs and the model lacked, added or filled at their folders, marked to be deepened, with a thin ICE where a part had none.
- Out: the intent's page, when the model had none.
- Out: the brief, and the record of every question and answer.
- Out: one change, landed through the change plays after the yes.
- Out, when nothing can be tested end to end: no slice, and the reason.

## Rules & behavior
- The model and memory first; the person is asked only what neither answers. The reason: "It asks the person only about what neither of them answers."
- One brief, not a list of questions. The reason: "The run talks to the person in one brief, by the shared rule for asking a person".
- The surface and the tester are proposed, never asked. The reason: "an intent does not depend on a surface, so the run proposes the surface and the tester when it shapes the slice".
- One surface and one tester, or no slice. The reason: "A thing with no screen or surface that a person can test end to end is not a slice", and "a slice with no surface a person can test cannot be checked".
- The build order is the order the tester can test them. The reason: "a feature that another one needs comes first."
- A slice that serves is used again; a slice in progress is never touched by a shaping run. The reason: its stories were written from it, and "A slice in progress (its epic is past ready: a story is started or done) is never touched by a shaping run".
- The plan does not choose. The reason: the plan "does not pick, rank or test slices; the person chose the slice at `/shape-slice`."
- A part with no ICE gets a thin one, and nothing stops. The reason: "The run never sends the person back, and nothing stops."
- A proposed answer names its source, or there is none. The reason: "A proposed answer always names its source; where none exists the question carries no proposed answer, and the count is shown."
- Nothing is kept before the yes. The reason: "A stop undoes every write."
- Plain words and personas. The reason: every page a person reads "uses personas, and names no real person".
- It writes no plan, no epic, no story and no eval. The reason: those are made after the slice is chosen, and "It writes no plan, no epic, no story and no eval."
- Not decided: whether the pinned yes of this checkpoint is a way past of its own kind, or an exception to Orchestration's Must not.

## Acceptance criteria
- Given a confirmed intent with a model page and no slice that serves it, when the product owner types yes to the brief, then the model's index holds one slice that serves the intent, with features in build order, one surface and one tester, and the commit exists only after the yes.
- Given an intent that a slice not in progress already serves, when the run ends, then no new slice is made and that slice lists the intent.
- Given an intent whose kept slice has a story started, when a shaping run would change that slice, then the slice is left as it is and a new slice is shaped.
- Given an intent for which nothing can be tested end to end, when the run ends, then no slice is written and the run says why.
- Given a feature the slice needs with no ICE, when the run ends, then it has a thin ICE with both thin marks, the brief warns, and the run did not stop.
- Given a shaped slice, when the person types stop, then the model is as it was before the run and nothing is committed.
- Given an intent with no model page, when the run ends, then the model has the intent's page, written from the issue, and the run said so.

## Out of scope
- The slice's hidden file of failure and recovery conditions, and the lines of it an edit may change. Write the evals that check the work, in Design → Code, owns them.
- Making the plan, its epics and its stories from the slice. Cut an intent into epics and stories (fn-cut-intent-into-work), in Turn intents into agent work, does it.
- Writing an ICE in full, and detailing a capability or a feature. Specify the product, in Product → Spec, does it.
- The kinds of the model, the rules of its pages and its index, and the model's checks. Product model owns them.
- The question setting and the rule for asking a person. Standards, structure, settings and memory owns them.
- The tool that reads the intent's issue from the team's tracker. Track execution in the team's tracker owns it.

## Sources
- The product owner on 2026-11-10: "A person chooses what is delivered next as a slice, sees every plan and where it stands, and sets the order and status of the work as it runs."
- The product owner on 2026-11-09: "making the plan is part of the orchestration, not this intent"
- core/components/plays/shape-slice/reference/ice.md: "It asks the person only about what neither of them answers.", "The run talks to the person in one brief, by the shared rule for asking a person", "an intent does not depend on a surface, so the run proposes the surface and the tester when it shapes the slice", "A slice in progress (its epic is past ready: a story is started or done) is never touched by a shaping run", "The run never sends the person back, and nothing stops.", "A stop undoes every write.", "uses personas, and names no real person"
- core/components/plays/shape-slice/SKILL.md: "A proposed answer always names its source; where none exists the question carries no proposed answer, and the count is shown.", "the person decides; never skipped by config"
- core/components/skills/author-slice/SKILL.md: "a feature that another one needs comes first."
- docs/adr/049-a-slice-is-shaped-then-planned-then-given-its-eval.md: "A thing with no screen or surface that a person can test end to end is not a slice"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "does not pick, rank or test slices; the person chose the slice at `/shape-slice`."
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/capability.md: "the step that chooses the slice proposes a thin one where a slice needs it"
- .garura/product/product-os/software-delivery-planning/keep-spec-matched/fn-update-spec-to-match-built/feature.md: "the step that chooses the slice writes an intent's page from its issue when the model has none"
- .garura/product/product-os/software-delivery-planning/write-work-evals/capability.md: "Its hidden file part comes from the slice play, /shape-slice (fn-795)."
- The research and drafts for Orchestrate agent work through planning, the old page of Shape a slice and the page this one replaces, as they read on 2026-11-10: "a slice with no surface a person can test cannot be checked", "It writes no plan, no epic, no story and no eval."
