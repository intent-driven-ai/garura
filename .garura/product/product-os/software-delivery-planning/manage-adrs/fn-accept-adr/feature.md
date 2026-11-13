# Feature: Accept an ADR only on a person's word, then or later

## What it does
An ADR becomes accepted only when a person says so. Run by hand, the decision play shows the drafted ADR and waits for the person's typed answer, at a checkpoint no setting turns off. Inside a loop, it does not stop: it saves the ADR as proposed, and the person accepts it at the loop's end review, or later by hand, so an agent records a decision and a person decides it.
- Run by hand, the person is shown the draft exactly as it will read, with the older ADRs it supersedes or amends and the part of each, what it affects, its effect on agent intent and its business-intent check. The person types one of three answers:
  - accept: the person's exact words are kept with their name, and the ADR is written as accepted;
  - reject: nothing is written, and the run ends halted with the reason rejected;
  - change, with what to change: the change is added to the brief, and the ADR is drafted and shown again.
- The checkpoint is pinned. It is "never skipped by config or policy", and the settings that turn other checkpoints off do not reach it.
- What an accept writes on the ADR: its Status line reads Accepted, its Date line the day it was accepted, and its Decided by line the person who accepted it. A `decision.yaml` record gets the same, as its status and the person in its metadata.
- The answer must be the person's own typed reply. A recorded answer with no reply, or not marked as the person's, writes nothing.
- An accept names a person, or it is refused. Only a proposed ADR can be accepted; an ADR already accepted, superseded or rejected is refused.
- Inside a loop, the decision play opens no issue and no branch, does not wait, and saves the ADR as proposed. No answer is recorded, and the forward pointers wait for the accept.
- Later, by hand, `/record-decision accept <file>` completes a proposed ADR. The person is shown it and types accept; the play checks the ADR against the template, that it is still proposed and that each older ADR it names exists; then it writes the accept, the forward pointers from the ADR's own Supersedes and Amends lines, and the index.
- A run that stops and is resumed never asks the person again once the answer is recorded.
- A decision that would change a person's business intent never reaches the accept: it is stopped and shown to the person before it is written.
- Today no loop runs the decision play. The one loop that is built, the Discovery loop, runs its three discover plays, so the path inside a loop is built but not used.
- Examples, in different kinds of project:
  - In a clinic's booking app, the technical lead reads a drafted ADR to keep all bookings in one region, types accept, and the ADR reads Accepted with their name and today's date.
  - In a shop's checkout service, the product owner asks for a change, to name what happens to carts saved before the decision; the ADR is drafted again with it and shown before they accept.
  - In a data team's reporting service, a loop's run saved an ADR as proposed; at the loop's end review the person accepts it with `/record-decision accept` and its file.
  - In a bank's payments service, the product owner rejects a drafted ADR, and no new ADR is in the ADR folder.
- How it meets the capability: the decisions agents "coordinate many pieces from" are a person's decisions; an agent drafts the record and never accepts it.

Accepting an ADR by hand is pinned to a person: the run waits for their typed answer, and no setting turns the wait off. This intent's Must not reads: "Stop a person. Every gate has a way past it that records what's owed." Whether the person's typed answer at this checkpoint is the way past it, or a stop kept on purpose, is open. The way past itself is Give every gate a way past's.

Status: built, in /record-decision, with its accept pinned when run by hand, and apply_adr.py over adr.py. Not built, or open:
- The accept writes the git user's full name on the Decided by line.
- The place where a person accepts is to move onto a card in the review tool. Accept or send back each ADR that waits for a person (fn-review-adrs), in Review what agents make (Argus), is to do it, and it is not built.
- No loop runs the decision play yet, so no ADR has been saved as proposed by a loop and accepted at its end review.

## Inputs / Outputs
- In: the drafted ADR, as proposed, and its gathered context: the older ADRs with their parts, what it affects, its effect on agent intent and its business-intent check.
- In: run by hand, the person's typed answer, accept, reject or a change, and the name of the person who answers.
- In: inside a loop, the loop's contract.
- In: for a later accept, the proposed ADR's file and the person's typed accept.
- Out: on accept, the ADR written as Accepted with the date and who accepted it, and the answer record with the person's exact words.
- Out: on reject, no new ADR, and the run closed halted with the reason rejected.
- Out: inside a loop, the ADR written as proposed, no answer record, and its forward pointers left for the accept.
- Out: the run's manifest: whether it was decided, its status, and who accepted it.

## Rules & behavior
- Only a person accepts or rejects an ADR. The reason: "Only a person accepts an ADR.", and the template's rule: "Only a person moves it to `accepted` or `rejected`".
- The accept by hand is pinned, and no setting turns it off. The reason: it is "a pinned gate, class one-way-door: a record of a decision is the project's memory", and "A pinned gate NEVER resolves off".
- The answer is the person's own typed reply. The reason: the script refuses any other, with "the decision must be the person's own typed reply (by: person, reply)".
- No agent and no play accepts on its own. The reason: the play's rule, "You never accept an ADR yourself", and the agent's, "never run `adr.py accept` or `pointer`".
- An accept names a person. The reason: the script refuses with "only a person accepts an ADR — --by names them".
- Only a proposed ADR is accepted. The reason: "only a proposed ADR can be accepted", and a draft must be proposed: "the draft must be Proposed — only a person's word makes it accepted".
- A reject writes nothing. The reason: "the person rejected the ADR — nothing is written".
- Inside a loop there is no stop, and the ADR waits as proposed. The reason: "Inside a loop, an ADR is written as `proposed` and accepted at the loop's final review; run by hand, the person accepts it before it is written as `accepted`."
- The person is never asked twice. The reason: "a resume never re-asks the person once `decision.yaml` exists".
- Not decided: whether the person's typed answer at this pinned checkpoint is the way past it that Orchestration's Must not asks for, or a stop kept on purpose.
- Not decided: whose name the Decided by line carries, the git user's full name as the accept writes it today, or a persona.

## Acceptance criteria
- Given a drafted ADR run by hand, when the person types accept, then it reads Accepted with today's date and the person's name, and the answer record keeps the person's exact words.
- Given a drafted ADR run by hand, when the person types reject, then no new ADR file is in the ADR folder, no older ADR changed, the index is unchanged, and the run closed halted with the reason rejected.
- Given a drafted ADR, when the person types a change, then the ADR is drafted again with the change and shown again before anything is written.
- Given settings that turn checkpoints off, when the decision play runs by hand, then it still waits for the person's answer.
- Given a run inside a loop, when the draft is ready, then the run does not wait, the ADR reads proposed, no older ADR changed, and no answer is recorded.
- Given a proposed ADR, when the person types accept on `/record-decision accept <file>`, then it reads Accepted, each older ADR it names points forward to it, and the index lists it as Accepted.
- Given an ADR that is already accepted, when an accept is run on it, then it is refused and nothing changes.
- Given an accept that names no person, when it is run, then it is refused and nothing changes.

## Out of scope
- Drafting the ADR and checking it. Record a decision as an ADR, with what it overrides and what it changes (fn-record-adr) does it.
- The forward pointers and the index that an accept writes. Keep older ADRs pointing forward and the index current (fn-keep-adrs-linked) does them.
- The card where a person accepts or sends back an ADR in the review tool. Review what agents make (Argus), in Developer tooling, owns it, through Accept or send back each ADR that waits for a person (fn-review-adrs).
- The way past the pinned checkpoint, and where what is owed is kept. Give every gate a way past owns them.
- Running a loop and its end review. Run plays as loops owns the run, and Review what agents make (Argus) owns the review.
- The settings that turn checkpoints on or off. Standards, structure, settings and memory owns them.

## Sources
- The capability list set on 2026-11-10: "Manage ADRs: Decisions on how the project is built are recorded closely as they're made, so agents can coordinate many pieces from them."
- core/components/plays/record-decision/SKILL.md: "Only a person accepts an ADR.", "never skipped by config or policy", "You never accept an ADR yourself", "a resume never re-asks the person once `decision.yaml` exists", "show the draft exactly as it will read", "the person accepts it at the loop's final review with `/record-decision accept <file>`", "it opens no issue or branch, skips the end sequence, does not stop for approval, and saves the ADR as proposed for the loop's final review"
- core/components/plays/record-decision/reference/ice.md: "a pinned gate, class one-way-door: a record of a decision is the project's memory"
- core/components/plays/record-decision/scripts/apply_adr.py: "the decision must be the person's own typed reply (by: person, reply)", "the person rejected the ADR — nothing is written", "only a proposed ADR can be accepted", "the draft must be Proposed — only a person's word makes it accepted"
- core/components/skills/author-decision/scripts/adr.py: "only a person accepts an ADR — --by names them"
- core/components/agents/adr-keeper.md: "never run `adr.py accept` or `pointer`"
- core/components/loops/complete-discovery/SKILL.md: "You run `/discover-intent`, `/discover-domains` and `/discover-capabilities`"
- standards/templates/adr.md, in Phoenix memory: "Only a person moves it to `accepted` or `rejected`", "Inside a loop, an ADR is written as `proposed` and accepted at the loop's final review; run by hand, the person accepts it before it is written as `accepted`."
- standards/rules/gate-config.md, in Phoenix memory: "A pinned gate NEVER resolves off", "only a person accepts a decision record"
- docs/adr/036-approved-answer-lands-in-short-term-memory.md: "Only a person accepts an ADR. Only where the person does it moves."
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- .garura/product/product-os/software-delivery-planning/review-agent-work/fn-review-adrs/feature.md: "the accept is carried out as Manage ADRs says"
- The product owner on 2026-10-09: "write it, approve it"
