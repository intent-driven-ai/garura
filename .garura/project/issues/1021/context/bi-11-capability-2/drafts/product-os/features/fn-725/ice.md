## Intent
- Goal: Every capability and feature is linked by the ontology's rules: the business intents a capability serves are named in its index entry and on each intent's Touches list; its needs and what led us to find it name other capabilities only; a feature needs nothing and its order is kept in the slices; the needs field is called `needs`, with every value kept; and each link that names nothing, work, an intent, a domain or a feature, or that a feature holds, is a finding the checks name, never a stop.
- Limit: Links sit on capabilities and features only, never on work items, and business intents never need each other.
- Limit: A link that points at nothing, and an empty "identified by", never stop work.
- Limit: The rename changes a field's name only, and keeps every value.
- Fails if: A serves link written by a change is kept on one side only.
- Fails if: A need or an "identified by" link names a part that does not exist, work or a feature, and no check names it.
- Fails if: A part found on its own is counted as a gap, or the rename drops or changes a value.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the ontology's rules for serves, needs and "identified by", the index's entries and its schema, the intent pages' Touches lists and the script that writes them, the structure check and the gap finder, the files that read `depends_on`, and the product owner's answers on parts found on their own and on needs between features.
- Never read: any memory file by its path, any ICE page, and any file in a plan's evals folder.
- Persona: the technical lead, who links parts as the model grows; and the developer, a person or an AI agent who builds the code, who reads a part's needs to know what comes first.
- Scope: In: the serves link on both sides, needs and "identified by" by the ontology's rules, the rename, and the check that each link points at a part that exists. Out: the ready answer, listing what serves an intent, writing a link on a part that exists, closing one-sided links, an intent's links as work changes it, the plans a plan waits on, and the rules as kinds of the ontology.

## Expectation
- Scenario: In a shop's checkout service, Refunds needs Payments, and Refunds serves the intent "shoppers get their money back"; the intent's Touches list names Refunds, and the structure check names one finding: an old need from the Refund to card feature to a payment feature, and it stops nothing. In a clinic's booking app, Timetable names no "identified by", and no check lists a gap for it; after the rename, every need the index held is under `needs`.
- Done means: Someone other than the one who linked the parts reads the index, the intent pages and the check's report, and finds each serves link on both sides, every need and "identified by" naming a capability that exists, the shop's feature need named as a finding with no stop, no gap for the clinic's Timetable, and the same needs under `needs` as were under `depends_on`.
