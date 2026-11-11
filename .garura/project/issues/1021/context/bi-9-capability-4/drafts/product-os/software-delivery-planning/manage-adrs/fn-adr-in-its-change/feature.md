# Feature: Record the ADR in the change it belongs to

## What it does
The decision play, run on the branch of a change that is already open, records the ADR in that change, so a decision lands with the work it decides. When no change is open, it opens its own change, as it does today.
- Today, run by hand, the decision play opens a change of its own first: its first step "cuts the branch off fresh main". So an ADR that belongs to a change on another branch cannot land in that change, and "the change lands without its ADR, and the issue stays open until a second, small change records the ADR. This happened on #816". #816 was a change on a plan's branch.
- Its other mode, the loop's contract, is for loops: handed one, it opens no issue or branch and checks that the current branch is the loop's. In #822's words, "that is meant for loops, not for a play run inside a change."
- What it is to do, as #822 sets it:
  - run by hand on an open change's branch, record the ADR on that branch, in that change;
  - still open its own change when no change is open;
  - a test or a scenario shows both.
- The ADR keeps every other rule of the decision play: it is drafted from the one template, it shows what it overrides and what it changes, and it is accepted only on a person's word.
- In the change's review, an ADR is reviewed by a person, line by line, so an ADR in the change is reviewed in the same pull request as the work it decides.
- Outside practice, in the approved facts:
  - Shopware adds every code change that carries out a decision to the same merge request as its ADR, and labels that merge request ADR.
  - The UK Government Digital Service keeps decisions in version control beside the application. On GitHub, a proposed ADR can be a draft pull request, and the pull request's status stands for the decision's status until it is accepted.
  - AWS Prescriptive Guidance: an ADR starts Proposed, is reviewed, and becomes Accepted or Rejected; a code reviewer checks a change against the ADRs.
- Examples, in different kinds of project:
  - In a shop's checkout service, a developer's change moves guest carts into the database. The technical lead runs the decision play on that change's branch, and the ADR that keeps carts for thirty days is in the same pull request as the code.
  - In a clinic's booking app, no change is open. The technical lead runs the decision play, and it opens its own change, as today.
  - In a harness repository, a change on a plan's branch alters how a play asks its questions. The ADR is recorded in that change, and the issue does not wait for a second, small change.
- How it meets the capability: decisions on how the project is built are "recorded closely as they're made", and the closest place is the change that makes them.

Status: not built (#822, /record-decision cannot join a change that is already open; under #968, a person records a decision as an ADR in the change it belongs to and sees every point found on the way). What exists:
- Run by hand, the decision play opens and lands its own change, through the opening play and the four change plays.
- Handed a loop's contract, it opens nothing and works on the loop's branch.

## Inputs / Outputs
- In: a decision brief, from the person.
- In: the branch the decision play runs on, and whether it belongs to a change that is open.
- Out: on an open change's branch, the ADR written on that branch, in that change, with no new issue, branch or pull request.
- Out: with no change open, the ADR in a change of its own, as today.

## Rules & behavior
- On the branch of an open change, the ADR goes into that change. The reason: otherwise "the change lands without its ADR, and the issue stays open until a second, small change records the ADR."
- With no change open, the decision play opens its own. The reason: #822 asks that "It still opens its own change when no change is open."
- The work and its ADR travel together. The reason, from outside practice: "every code change needed to carry out the decision is added to the same merge request as the ADR".
- The loop's contract stays for loops. The reason: "that is meant for loops, not for a play run inside a change."
- Only a person accepts the ADR, in whichever change it is recorded. The reason: "Only a person accepts an ADR."
- The ADR is reviewed with the work. The reason: a change that adds an ADR has its review by a "human, line by line", and in outside practice "a code reviewer checks a change against the ADRs and links the one it breaks".
- Not decided: when an ADR recorded in a change is accepted: before the change's pull request opens, or when the change merges.
- Not decided: what happens to the ADR when the change it belongs to is turned down.
- Not decided: how the decision play tells that the branch it runs on belongs to an open change.

## Acceptance criteria
- Given a change that is open on its own branch, when a person runs the decision play by hand on that branch, then the ADR is written on that branch, in that change, and no new issue, branch or pull request is opened. This is not built.
- Given no change is open, when a person runs the decision play by hand, then it opens its own change, and one test shows both this case and the case above. This is not built.
- Given an ADR recorded in an open change, when the change is reviewed, then the ADR is reviewed in the same pull request as the work it decides. This is not built.
- Given an ADR recorded in an open change, when no person has accepted it, then it does not read accepted. This is not built.

## Out of scope
- Drafting the ADR and checking it. Record a decision as an ADR, with what it overrides and what it changes (fn-record-adr) does it.
- Accepting the ADR, then or later. Accept an ADR only on a person's word, then or later (fn-accept-adr) does it.
- The points found on the way, for the person who accepts. Give the person who accepts every point found on the way, and check it is whole (fn-show-accepter-findings) does them.
- Opening and landing the change. Ship every change the same way, in Developer tooling, owns it.
- Reviewing the change that holds the ADR. Check the code against its standards, in Code → Validation, owns it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, the list set on 2026-11-10, line 99: "Manage ADRs: Decisions on how the project is built are recorded closely as they're made, so agents can coordinate many pieces from them."
- core/components/plays/record-decision/SKILL.md, lines 18-24, 72 and 141-143: "Only a person accepts an ADR.", "it opens no issue or branch, skips the end sequence, does not stop for approval, and saves the ADR as proposed for the loop's final review", "the current branch equals that branch", "cuts the branch off fresh main"
- knowledge/review/adrs.md, in Phoenix memory, lines 5 and 22: "the PR adds or changes an architecture decision record", "human, line by line"
- GitHub #822 (open): "/record-decision cannot join a change that is already open", "that is meant for loops, not for a play run inside a change.", "the change lands without its ADR, and the issue stays open until a second, small change records the ADR. This happened on #816", "an ADR that belongs to a change on a plan branch", "/record-decision, run by hand on an open change's branch, can record the ADR on that branch, in that change.", "It still opens its own change when no change is open.", "A test or scenario shows both cases."
- GitHub #968 (open): "A person records a decision as an ADR, in the change it belongs to, and sees every point found on the way"
- .garura/project/issues/1021/context/answers/bi9-adr-in-change.md, in short-term memory, approved by the product owner on 2026-11-10 as mu-20261110-013, lines 5-7: "every code change needed to carry out the decision is added to the same merge request as the ADR, and the merge request is labelled ADR.", "decisions are kept in version control beside the application; on GitHub a proposed ADR can be a draft pull request, and the pull request's status stands for the decision's status until it is accepted.", "an ADR starts Proposed, is reviewed and becomes Accepted or Rejected", "a code reviewer checks a change against the ADRs and links the one it breaks."
