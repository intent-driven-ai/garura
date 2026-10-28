# Draft — the questions (stage `scope`, step 1) — #793, round 2

**Need:** the delivery chain works on Work, not on Slices and Epics. A slice cut into verticals gives **Stories under a Feature**. There is no new kind.

## The part of the ontology these questions are about

- **Work today (ontology v6)** has five types: Feature, Story, Spike, Chore, Bug. Each piece of work carries one ICE.
- **Its rules today:** a Feature carries its capability's ICE, and **one capability has one Feature**. A Story builds one functionality and carries its ICE, and **one functionality has exactly one Story**. Spikes, Chores and Bugs sit under a functionality. In the tracker: Business Intent → Feature → Story → Spike, Chore or Bug.
- **Slices and Epics today** are not kinds. They are only two lists in the spine (`slices`, `epics`). A slice bundles functionalities. An epic is cut from a slice and names the functionalities it delivers (one or more).

## The open point (a question, not a decision)

A vertical cut from a slice can go across **more than one functionality**. Today **one functionality has exactly one Story**, and a Story builds one functionality. So: can one Story build more than one functionality, and can one functionality have more than one Story? Q18 asks this. The answer is decided at the links stage, with you.

## New questions

- **Q17** — Given a feature, which stories sit under it?
  - *Shop:* Feature #121 (Checkout) → Story #122 (Guest checkout), Story #123 (Pay by card).
  - *Clinic:* Feature #341 (Booking) → Story #342 (Pick a free slot), Story #343 (Send a reminder).
  - *Bank:* Feature #54 (Credit decision) → Story #55 (Score the application).

- **Q18** — Given a story, which functionalities does it build? And given a functionality, which stories build it?
  - *Shop:* Story #122 → Guest checkout and Pay by card (two functionalities, one vertical). Guest checkout ← Story #122 only.
  - *Clinic:* Story #343 → Send a reminder. Send a reminder ← Story #343, and later Story #350 (reminder by email).
  - *Bank:* Story #55 → Score the application. Score the application ← Story #55 only.

- **Q19** — Which piece of work can start next, and what does the model say about why?
  - *Shop:* Not Story #122: its ICE is not ready, because Checkout needs Cart, and Cart's Story #119 is open. Next: Story #119.
  - *Clinic:* Story #343: open, its ICE is ready, and Booking needs nothing.
  - *Bank:* Story #55: open, its ICE is ready, and Loan application (Feature #52) is done.

- **Q20** — A product has slices and epics from before this change. Given one of them, which feature and which stories hold it now?
  - *Shop:* Slice "Checkout without an account" → Feature #121. Its epic "Guest pays" → Story #122.
  - *Clinic:* Slice "Self-booking" → Feature #341. Its epic "Reminder is sent" → Story #343.
  - *Bank:* Slice "One-day decision" (planned, not cut) → Feature #54, no stories yet.

## Existing questions that change

- **Q7** (the plan of a business intent) — changes. The plan's tree today is Business Intent → Capability → Functionality → Spike, Chore, Bug. It must also show the Feature and its Stories.
- **Q13** (given an ICE, which work carries it, "and which Story builds its functionality") — changes if Q18 lets a functionality have more than one Story: "which Story" becomes "which Stories".
- **Q10, Q11** — no change in words. Q19 uses them.
- **Q1–Q6, Q8, Q9, Q12, Q14–Q16** — no change.

## For the product owner

Confirm or change each question, starting with Q17. Then say how you want Q18 answered: one Story to one functionality as today, or a Story that goes across more than one.
