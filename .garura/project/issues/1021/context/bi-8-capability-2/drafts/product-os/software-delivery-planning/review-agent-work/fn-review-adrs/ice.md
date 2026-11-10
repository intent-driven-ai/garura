Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: In the ADRs section, the person reads each ADR that waits to be accepted, and the accepted ones, in plain words, and accepts each one or sends it back with a comment on its card, and Garura carries out each accept through the decision play's own accept and each send-back through its rework, so an ADR becomes accepted only on a person's word and by the rules of Manage ADRs.
- Limit: Only a person accepts an ADR, one at a time; an agent never does.
- Limit: What an accept writes is what the decision play's own accept writes, nothing more and nothing less.
- Limit: An ADR no person answered stays proposed.
- Fails if: An ADR reads accepted with no person's answer on record.
- Fails if: An accepted ADR's pointers or its line in the index differ from what the decision play's own accept writes.
- Fails if: A sent-back ADR comes back with no reply on its comment.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the ADRs that wait for a person and the accepted ones, the decision play's accept and what it writes, and the person's answers so far.
- Never read: any memory file by its path, any ICE page, and production.
- Persona: the product owner, who accepts each decision on how the project is built.
- Scope: In: listing the ADRs that wait and the accepted ones, accepting or sending back each one, and carrying the answer to the decision play. Out: writing an ADR, what an accept writes, memory updates, agent decisions, and applying the answers in one commit.

## Expectation
- Scenario: A bank's payments service's run saved two ADRs as proposed. The product owner accepts the first, and on Finish it reads accepted, with its pointer on the older ADR it changes and its line in the index. He sends the second back with "name what happens when that region is down"; the decision play reworks it and it comes back with a reply.
- Done means: Someone other than the one who built it compares each ADR's state after the review with the person's answers, and an accepted one with what the decision play's own accept writes, and finds them the same, with no ADR accepted without a person.
