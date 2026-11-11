## Intent
- Goal: Any team that installs Garura in its own repository can build and change its own plays and loops there with Garura's builders, without Garura's source folders, and reads a written architecture of what each part may do through the memory tool; the parts it builds pass the same linters as Garura's own, and a harness repository carries only what builds a harness and runs no loop.
- Limit: The builders run on the installed layout only after an accepted ADR changes ADR 055 section 5.
- Limit: A harness repository gets the builders, the change plays and the parts they call, and nothing product-facing.
- Limit: The architecture pages are read through the memory tool, never by their path.
- Fails if: A team with Garura installed and no Garura source folders cannot build or change a play or a loop in its own repository.
- Fails if: A part built in a team's repository reaches into Garura's source folders.
- Fails if: A harness install lays a product play or a loop, or a full install lays a builder.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the team's repository and its kind of install, the install's harness and full kinds, the builders as laid, ADR 055 and the new ADR that changes its section 5 once accepted, the harness standard, the installed layout, and the architecture pages of #933 (an architecture memory for a team building a harness) once written.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead of any team, who builds the team's own harness in its own repository; and the product owner, who decides what the team builds.
- Scope: In: the harness kind of install, the builders on the installed layout, building a team's plays and loops in its own repository, and reading the written architecture. Out: choosing and laying the install, where each part lives, the severity of review findings, moving pages up into Phoenix memory, recording the ADR, and building each play and loop.

## Expectation
- Scenario: In a retailer's own repository, the team installs Garura with no Garura source folders, and the technical lead builds a play that checks refunds with /create-play; it lands where the installed layout keeps plays, and the play linter passes. In an insurer's repository, the technical lead builds a claims loop, reads the architecture pages through the memory tool, and finds that a sub-agent may read memory only through the memory tool; the loop linter passes. In a design agency's repository, the full install lays no builder.
- Done means: Someone other than the one who built them reads the retailer's and the insurer's repositories, and finds the play and the loop built without Garura's source folders, both linters passing, no part that reaches into Garura's source, and the architecture pages cited in the insurer's review; and reads the agency's install record and finds no builder laid.
