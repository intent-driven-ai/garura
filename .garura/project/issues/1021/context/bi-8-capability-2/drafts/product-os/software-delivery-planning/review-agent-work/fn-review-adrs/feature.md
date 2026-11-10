# Feature: Accept or send back each ADR that waits for a person

## What it does
In the ADRs section of Argus, the person reads each ADR that waits to be accepted, and the ones accepted before, in plain words, and accepts it or sends it back with a comment, on a card like any other piece; the accept is carried out as Manage ADRs says, so recording a decision keeps its own rules and only the place where the person answers moves.
- An ADR is the record of one decision on how the project is built: what was decided and why, what it overrides, and what it changes. A run saves the ADRs it writes as proposed, and only a person accepts one.
- What the section lists: "the decisions a person records", first "the ones waiting to be accepted", then the accepted ones.
- The person gives each ADR one of two answers:
  - Accept: "The ADR is accepted, and older ones get a pointer." Garura carries it out through the decision play's own accept.
  - Send back, with a comment: the decision play "reworks it from your comment", and the ADR comes back as a new revision.
- Examples, in different kinds of project:
  - A shop's team: an ADR to keep a guest's cart for thirty days waits; the product owner accepts it.
  - A bank's payments service: an ADR that every payment runs in one region is sent back with "name what happens when that region is down".
  - A school's timetable app: an ADR accepted last month shows under the accepted ones, for reference.
- How it meets the capability: "ADRs" are one of the things people review in the one tool, and their accept moves onto a card.

Status: not built (#664). Today a person accepts an ADR by typing: run by hand, the decision play stops for the person's accept; inside a loop it saves the ADR as proposed, and the person accepts it "at the loop's final review with `/record-decision accept <file>`". The story's text is behind the design: it still names one "Memory and ADRs" section, which was split into three.

## Inputs / Outputs
- In: each ADR that waits for a person, and the accepted ones, turned by Garura into pieces of the review pack.
- In: the person's answer on each one, accept or send back with a comment.
- Out: for an accepted ADR, the decision play's accept: the ADR marked accepted, pointers on the older ADRs it changes, and the index of ADRs.
- Out: for a sent-back ADR, the comment, for the decision play to rework it.

## Rules & behavior
- Only a person accepts an ADR, and only the place moves. The reason: "Only a person accepts an ADR. Only where the person does it moves."
- The accept is carried out by the decision play, by its own rules. The reason: recording an ADR is Manage ADRs', and a card only takes the person's answer: "Accept, or send back with a comment."
- Every answer is the person's own, one ADR at a time. The reason: the decision play's rule, "You never accept an ADR yourself".
- Not decided: whether a product decision that waits for a person is answered here or under the Product section's decisions.
- Not decided: who writes the approval when the person accepts an ADR on a card, the review step at Finish or the decision play at once.

## Acceptance criteria
- Given an ADR a loop's run saved as proposed, when the review opens, then it shows in the ADRs section as waiting, in plain words. This is not built.
- Given the person accepts it, when the answer is applied, then the ADR reads accepted, the older ADRs it changes have their pointers, and the index lists it, exactly as the decision play's own accept writes them. This is not built.
- Given the person sends it back with a comment, when the decision play reworks it, then a new revision comes back to the card with a reply. This is not built.
- Given no person answered an ADR, when the review ends, then the ADR still reads proposed.

## Out of scope
- Writing an ADR and deciding what accepting it writes. Manage ADRs, in Orchestration, owns them.
- The memory and the agent decisions. See what memory holds, and approve or reject each memory update that waits for a person (fn-review-memory) and Check each agent decision against the memory it rested on (fn-check-agent-decisions) cover them.
- Applying the answers in one commit. Finish the review and have every answer applied in one commit (fn-apply-answers) does it.

## Sources
- .garura/project/issues/617/specs/review-tool.md, the design: "the decisions a person records", "the ones waiting to be accepted", "Accept, or send back with a comment."
- .garura/project/issues/617/specs/review-tool-mockup.html: "The ADR is accepted, and older ones get a pointer.", "reworks it from your comment"
- docs/adr/036-approved-answer-lands-in-short-term-memory.md: "Only a person accepts an ADR. Only where the person does it moves."
- docs/adr/037-agent-decisions-keep-a-trace-and-the-review-tool-has-five-sections.md: "the ADRs a person records with `/adr`, waiting for a person"
- core/components/plays/record-decision/SKILL.md: "at the loop's final review with `/record-decision accept <file>`", "You never accept an ADR yourself"
- GitHub #664 (open): "A person accepts a proposed ADR on a card.", "Memory and ADRs"
- The list set on 2026-11-10, in .garura/project/issues/1021/context/capabilities.md: "Manage ADRs: Decisions on how the project is built are recorded closely as they're made, so agents can coordinate many pieces from them."
