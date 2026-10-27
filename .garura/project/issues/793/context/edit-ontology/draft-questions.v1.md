# Draft — the questions (stage `scope`, step 1) — #793

**Need:** the delivery plays (/shape-features, /build-feature, /validate-feature, /next) must work on a piece of **Work**, not on a Slice or an Epic. The ontology must say what these plays read and write on that Work, and what becomes of Slice and Epic.

## The part of the ontology these questions are about

- **Work today (ontology v6).** Work is a tracked issue of one of five types: Feature, Story, Spike, Chore or Bug. Each piece of work carries one ICE. A Story builds one functionality and carries that functionality's ICE. Spikes, Chores and Bugs sit under a functionality and carry the same ICE. Work holds only five properties: type, issue, ICE, a copy of the ICE on the issue, and open or closed. It holds nothing about how the work is designed, built or checked.
- **Slice and Epic are not kinds in the ontology.** They live only in the spine (`spine.yaml`, lists `slices` and `epics`). A Slice is a bundle of functionalities. Seven lenses (quality, ux, agentic, architecture, measure, run) design it, and then it is stamped "realized". /shape-features cuts a realized slice into Epics. An Epic is a part a user can try. It moves through the statuses ready, in delivery, validated, fix required and delivered. /build-feature builds an epic and /validate-feature stamps it.
- **The flow the product owner wants (2026-10-22).** After a change starts: shape the work (ask questions, then design it: how far the change reaches, which parts change, which code changes) → build a set of checks (the eval suite) from the design → build the work; the builder never sees the checks → validate the build.

Each question below is one that a person asks to find something out. How the kinds answer it is decided in later stages.

## New questions

- **Q17** — Given a piece of work, how will it be built: which questions were asked about it and what were the answers, how far does the change reach, and which parts and code will it change?
  - *Shop:* The store manager asks about Story #122 "Guest checkout". The answer: two questions were answered (guests give an email; no saved cards). The change reaches the cart and the payment page. It changes the checkout form and the order service.
  - *Clinic:* The front-desk lead asks about Story #343 "Send a reminder". The answer: the reminder goes one day before the visit. The change reaches the booking calendar and the message sender. It adds one scheduled job.
  - *Bank:* The credit officer asks about Bug #60 "Score is wrong for joint applications". The answer: the change reaches only the scoring rules. It changes one rule file and its tests.

- **Q18** — Given a piece of work, which checks will judge if its build is done, and when were they written?
  - *Shop:* For Story #122: nine checks, written after the design and before the build. One check: "A guest with no email cannot pay."
  - *Clinic:* For Story #343: five checks. One check: "No reminder goes to a patient who cancelled."
  - *Bank:* For Chore #56: three checks. One check: "The scores before and after the move are the same for 1,000 sample applications."

- **Q19** — Given a piece of work, what was built for it: which change (branch, pull request), and which of its checks passed?
  - *Shop:* Story #122 was built on pull request #140. Eight of nine checks passed.
  - *Clinic:* Spike #344 "Which SMS provider?" was not built into code. It ended with a written answer.
  - *Bank:* Bug #60 was built on pull request #71. All checks passed.

- **Q20** — Given a piece of work, did its build pass validation? If not, what failed, and where?
  - *Shop:* Story #122 did not pass. The failure: "The payment page is slower than the 2-second bar, on mobile."
  - *Clinic:* Story #343 passed in round 1.
  - *Bank:* Chore #56 did not pass in round 1. The failure: "A security scan found a secret in the config file." It passed in round 2.

- **Q21** — Given a piece of work that was sent back, how many rounds did it have, and what did each round fix?
  - *Shop:* Story #122 had two rounds. Round 2 fixed only the slow payment page.
  - *Bank:* Chore #56 had two rounds. Round 2 fixed only the secret in the config file.
  - *School:* Story #210 "Parents see homework" had three rounds and then stopped for a person to decide.

- **Q22** — Where does this piece of work stand in delivery now: what is done on it, and what is the next step?
  - *Shop:* Story #122: designed, checks written, built; the next step is to fix the payment page.
  - *Clinic:* Story #343: validated; the next step is release (release is outside this need).
  - *Bank:* Story #55 "Score the application": not designed yet; the next step is to shape it.

- **Q23** — Given a piece of work, which quality bars, screens, architecture choices and running costs must its build follow, and where are they written?
  - *Shop:* Story #122 must follow "Pay in under 2 seconds" and "Card data never stored". The checkout screen shows the guest email field.
  - *Clinic:* Story #343 must follow "No health details in a text message".
  - *Bank:* Story #55 must follow "Every decision is explained in plain words to the applicant", and it runs on the existing scoring service.

- **Q24** — Given a piece of work, what can a person open and try, to see that it works?
  - *Shop:* For Story #122: open the shop with no account, put a book in the cart, and pay.
  - *Clinic:* For Story #343: book a visit for tomorrow and see the text message arrive.
  - *Bank:* For Story #55: send in a test application and see the score and its reasons.

- **Q25** — Given a functionality, which delivery work did it get, and is its build done?
  - *Shop:* Guest checkout: Story #122 (validated) and Bug #130 (in build). The build is not done.
  - *Clinic:* Send a reminder: Story #343 (validated) and Spike #344 (closed). The build is done.
  - *Bank:* Score the application: Story #55 (not designed). The build is not started.

- **Q26** — A product already has Slices and Epics. Given one of them, which work now holds what it held: its functionalities, its lens designs, its epic pages and its statuses?
  - *Shop:* Slice "Checkout without an account" bundled Guest checkout and Pay by card, with seven lens pages. Epic "Guest pays" was validated. The store manager asks where each of these is now.
  - *Clinic:* Epic "Reminder is sent" was in delivery. The front-desk lead asks which piece of work carries its build now.
  - *Bank:* Slice "One-day decision" was planned, not realized. The credit officer asks what happens to its plan order.

## Questions that change

- **Q7** — "where each one stands" now also means the stage of delivery of each piece of work (Q22), not only open or closed in the tracker.
  - *Clinic:* Plan #340 shows Story #343 "validated" and Spike #344 "closed".
- **Q13** — no change in words. A piece of work still carries one ICE; Q17–Q24 add what the work holds about its own design, checks, build and verdict.

## Left for later stages (not questions)

- That the builder never sees the checks is a rule (step 6), not a question.
- The stages a piece of work moves through, and whether Slice and Epic are kept, replaced or retired, are design choices (steps 4 and 6). Q22 and Q26 ask only what a person wants to find out.

## For the product owner

Confirm or change each question, one at a time, starting with Q17. Say if a question is missing, for example about /next choosing the next piece of work.
