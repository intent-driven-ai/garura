## Intent
- Goal: The plays that build and install the harness, the ontology play and the loop carry the names of the naming standard in force, with every reference to them changed in the same batch and nothing else changed, so the old-name check finds none of their old names; under ADR 046 they are /create-play, /edit-play, /create-loop, /edit-loop and /complete-discovery, and ADR 066's names follow in one change after the reviews of BI-10 and BI-11.
- Limit: Names and references only; no part's behaviour changes.
- Limit: A renamed play's or loop's ICE changes in wording only, and its fingerprint is stamped again.
- Limit: Past records and accepted ADRs keep their old words.
- Fails if: An old name of this family is still used outside past records after its batch.
- Fails if: A rename changes what a play or the loop does.
- Fails if: A renamed play or loop has no line in the rename map.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the rename map's lines for this family, the agreed new names, ADR 046 and ADR 066, the rename tool, the old-name check, and the ICE source of each play and of the loop.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead, who runs the rename; and the developer, a person or an AI agent who builds the code, who uses the builders.
- Scope: In: the names of the four builders, the ontology play, the two install plays and the loop, and every reference to them. Out: the naming rule, the rename map and the check, building parts, taking out old names in a project, and running the loop.

## Expectation
- Scenario: In a bank's payments service, the team's harness renames its play maker to `create-play` in one batch; every guide and script that named it changes, its ICE changes in wording only, and the old-name check finds no old name of the family left. In a harness repository, after the reviews, ADR 066's rename makes the builders /build-play, /fix-play, /build-loop and /fix-loop and the loop /loop-product-spec, in one change.
- Done means: Someone other than the one who ran the rename runs the old-name check and the linter and reads the rename's changes, and finds no old name of the family left outside past records, only names and references changed, each ICE changed in wording only with its fingerprint stamped again, and each rename in the map.
