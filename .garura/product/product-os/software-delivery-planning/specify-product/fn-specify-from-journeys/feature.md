# Feature: Specify from a prototype's journeys

## What it does
A prototype's screens show what it has, and a journey shows what it is for. A journey records who comes to the prototype, what they set out to do, each step they take with what it showed, and what they end with. This feature works out who the prototype serves, then uses it one step at a time in a browser with no window, and keeps a picture and the text of every step. It runs for a prototype only, because a document or plain words have no steps to take.

Status: built, but it can still change data on a deployed site.

## Inputs / Outputs
- In: the prototype, as a file, a local page or a link.
- In: the capture record, which names the views the journeys must cover.
- In: whether a step may change data. It is yes for a file or a local prototype. For a deployed site, it is only what the person said.
- In: the person's write-up, when the discovery loop gives one. The walk starts from its walkthrough and then covers the rest. A run started by hand has no write-up.
- Out: the journeys record: the prototype's main sections, each journey's person, section, goal, steps and end, the steps it could not take, and each view not walked with why.
- Out: for each step, a picture, the visible text and a short record of what changed.
- Out: a check report that says whether the record is complete.

## Rules & behavior
- Every main section gets a journey of its own. A main section is a menu item, a tab or a part of the first screen. It is never only a step on the way to another goal.
- A goal is what the person wants to have at the end, in the product's own words, such as "see where every piece of work stands before planning the week". It is never a screen or a rule.
- A step is a click, typed text, a key press or going back. The walk finds its target by the words a person sees, or by its place in the list of controls.
- Each step reports only what changed: the new lines and how many went. One browser stays open for each journey and closes itself after ten minutes with no step. This keeps a long journey quick.
- A step that cannot be taken is a finding. The walk notes it and tries another way, so the journey does not end there.
- On a deployed site, the walk refuses a click on a control with any of these words, unless the person cleared the site: accept, approve, reject, drop, send back, delete, remove, finish, submit, save, pay, buy, upload, sign out, log out, reset. This tests clicks only. Typing and key presses are not tested, and a button with other words, such as "Create", is not stopped. The test also finds these words inside longer words, so a tab named "Payments" is refused too.
- Run by hand, the run asks the person once, before the walk, whether a deployed site is safe for such steps. Inside the loop, it reads the answer given at the start. With no answer, it takes no such step and names what it could not walk.
- The check needs at least one journey. Each journey needs its person, its goal, its end and two or more steps, and each step needs what was done, what it showed and its saved picture and text. Whether a journey means anything stays with the walker's judgment.

## Acceptance criteria
- Given a captured view on no journey and not named as not walked, when the check runs, then it names that view and reads not ok.
- Given a main section that is no journey's section, when the check runs, then it names that section and reads not ok.
- Given a journey with one step, when the check runs, then it reports that journey and reads not ok.
- Given a step that names a picture the evidence does not hold, when the check runs, then it reports that step and reads not ok.
- Given a deployed site the person has not cleared and a step that clicks "Delete", when the step runs, then the walk refuses it and the step's record says why.
- Given a file prototype and a step that clicks "Delete", when the step runs, then the walk takes it.

## Out of scope
- Keeping the prototype's views before the walk. Specify from a file (fn-specify-from-file) and Specify from a deployed site (fn-specify-from-site) do this.
- Drafting intents from the journeys. Specify intents (fn-specify-intents) does this.

## Sources
- The product owner approved this page and its ICE on 2026-11-06.
- core/components/skills/walk-prototype/SKILL.md: "A screen shows what a prototype has.", "Every main section of the prototype is some journey's goal.", "see where every piece of work stands before planning the week"
- core/components/plays/discover-intent/reference/ice.md: "A prototype is understood by using it", "a step that changes data (pay, delete, submit, accept"
- core/components/plays/discover-intent/SKILL.md: "ask them once, before the walk"
- core/components/plays/discover-intent/scripts/walk_prototype.py: "a click on a control that answers or changes data", "an idle helper"
- core/components/plays/discover-intent/scripts/check_journeys.py: "every view the capture kept"
- core/components/agents/prototype-reader.md: "plan the journeys from its walkthrough first"
