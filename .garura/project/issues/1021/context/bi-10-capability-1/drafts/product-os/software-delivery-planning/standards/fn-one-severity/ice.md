Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: Every finding of a review and every defect gets one severity, P1 to P4, by written rules in three layers, generic, surface, and architecture and technology, that start from the closest industry standard, and the same value says what is fixed first.
- Limit: One value; no second priority field and no matrix.
- Limit: A change is not a defect and gets no severity.
- Limit: The rules start from the closest industry standard, and each difference from it is recorded.
- Fails if: Two tables give P1 to P4 different meanings, and both are used.
- Fails if: One finding or defect carries two values, a severity and a separate priority.
- Fails if: A severity is given with no written rule behind it.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: #934 and its three layers, the industry scale it starts from, the mechanical table of the review of each change, how the review and the defect filing give a severity today, and the architecture memory of #933.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead and the developer, a person or an AI agent who builds the code, who rate findings and defects; and the product owner, who reads what is fixed first.
- Scope: In: the scale, its three layers and their rules. Out: filing the defect, the review's verdict, the architecture memory, and the tracker's field.

## Expectation
- Scenario: In a bank's payments service, a review finds a change that breaks the payments API's contract and rates it P1 by the written rule for an API, with the rule named. In a mobile game, a defect filed for a button out of line on a phone is rated P2 by the surface rule for a phone, and carries no second priority.
- Done means: Someone other than the one who rated them reads the severity rules and a set of rated findings and defects, and finds each with one value from P1 to P4, each value backed by a named written rule, and no second priority field.
