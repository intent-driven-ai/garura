Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: The map defines the product profile and the product decision as kinds, each with its properties, links, rules and real examples, added one at a time through the map's play, so the profile and the decisions every model keeps follow the map like every other part.
- Limit: Each kind is added only through the map's play, one need at a time, with the product owner's yes.
- Limit: The kinds define what the profile and a decision hold; they never change a model's profile or decisions.
- Limit: A decision on how a project is built stays an ADR, outside these kinds.
- Fails if: The model holds a profile block or a product decision whose properties the map does not define.
- Fails if: A kind is added without the product owner's yes at the map's three points.
- Fails if: A model's profile or decision changes because a kind was defined.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the profile block and the decisions in the model, the product profile and decision schemas, the map's kinds and their format, the approved pages that hand the profile and the product decision to Product model, and the product owner's answer to question 8.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who agrees each kind; the technical lead, who reads the profile before a capability is detailed.
- Scope: In: the Product Profile and Product Decision kinds of the map, with their properties, links, rules and examples. Out: writing a model's profile and decisions, moving the profile, decisions on how a project is built, and the setup answers.

## Expectation
- Scenario: In a shop's checkout service, a reader finds the profile's kind in the map, with its levels, gates and compliance, and the decision kind, which links the decision that raised the security level to the capability it admitted. In a school's internal timetable tool, the profile's kind holds every level low, and the model has no decision.
- Done means: Someone other than the one who added the kinds reads the map and a model's profile block and decision record, and finds both kinds defined with their properties, links, rules and examples, each property of the model's profile and decision defined in the map, and no model changed by the change to the map.
