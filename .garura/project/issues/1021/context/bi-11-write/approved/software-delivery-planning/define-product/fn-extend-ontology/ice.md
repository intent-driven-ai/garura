## Intent
- Goal: A team adds its own kinds, properties or rules to the map Garura provides, in its own project, and changes the plays that read them in the same change, so the map fits the team's product and the map and the plays still go hand in hand.
- Limit: The team's additions never change what a kind Garura provides means.
- Limit: An upgrade loses nothing the team added.
- Limit: A team that adds nothing reads the same map as every other project.
- Fails if: A team's addition lands while a play that reads it is not changed with it.
- Fails if: An upgrade removes or changes a team's addition without asking the team.
- Fails if: A team's addition changes the meaning of a kind Garura provides.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the map Garura provides and its version, the team's additions, the plays that read each kind, how the install lays the map's play, and the product owner's answer on extending the map.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead of a team, who adds a kind its product needs and changes the plays with it; the product owner, who agrees the addition.
- Scope: In: a team's additions to the map in its own project, the plays changed with them, and keeping them on an upgrade. Out: changing the map Garura provides, building the team's plays, and the upgrade itself.

## Expectation
- Scenario: In a game studio's build, the technical lead adds a Level kind and changes the plays that write and check the studio's model in the same change; at the next upgrade of Garura's map, the Level kind is still there and the plays still read it. In an agency's client portal, which adds nothing, the upgrade brings the new map as it does to every project.
- Done means: Someone other than the one who added the kind reads the team's map, its plays and the upgrade's report, and finds the Level kind there with the plays that read it changed in the same change, no kind Garura provides changed in meaning, and the Level kind still there after the upgrade.
