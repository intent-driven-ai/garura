## Intent
- Goal: A change to the map is made only through /edit-ontology, for one need at a time: the product owner types yes at the questions, the kinds, and the links and rules, each answer recorded word for word with the draft it answered; the map is written with a real example, its version up by one and one log line; scripts read it valid and read that only the kinds the need touches changed and no real name appears; and the change lands through the change plays, so the map changes only on purpose.
- Limit: Nothing is written as agreed before the product owner's yes at that point.
- Limit: Only the kinds the need touches change; an existing kind changes meaning only with a log line that says so.
- Limit: The skill runs only inside the play; no person runs it.
- Limit: The change lands only through the change plays, on the plan's branch when the issue is in a plan.
- Fails if: A draft is written as agreed with no yes recorded after it was shown, or a later stage's draft exists before the earlier yes.
- Fails if: A kind outside the need changed, the version did not go up by one, or the log has no new line or more than one.
- Fails if: The change lands while the ontology check fails, or a page of the map names a real person.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the need and the issue it serves, the ontology as it was before the run, the format the map is written in, the rule for asking a person, the three drafts, the product owner's answers, the check report and the change report.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who decides at each of the three points; the technical lead, who brings the need.
- Scope: In: one need, the three drafts and their pinned checkpoints, the write, the ontology check, the change check, and landing through the change plays. Out: what the map says, the model's checks, a team's own extension, the list of pinned yeses and the way past them, the change plays themselves, and bringing the map to Phoenix memory.

## Expectation
- Scenario: In a harness repository for a bank's payments service, the product owner asks for a Regulation kind. At the kinds checkpoint they type a change to a property's name; the stage is drafted again, and they type yes. After the third yes, the map is written, the check reads it valid, the change check reads that only Regulation and the Capability kind it links to changed, with one version step and one log line, and the change lands through the change plays. In a harness repository for a game studio's build, the write leaves a link to a kind that is not defined; the check fails, the link is fixed, and the change lands only after the check reads valid.
- Done means: Someone other than the one who ran the play reads the decision record, the map before and after, the check report and the change report, and finds a yes for each of the three points, each recorded after its draft was shown, only the kinds the need named changed, the version up by one with one dated log line, no real name, the last check valid, and the change landed through the change plays.
