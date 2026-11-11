## Intent
- Goal: The lifecycle plays and the design lens plays carry the names of the naming standard in force, with every reference to them changed in the same batch and nothing else changed, so the old-name check finds none of their old names; under ADR 046 that is done, and ADR 066's names, with two lens plays dropped, follow in one change after the reviews of BI-10 and BI-11.
- Limit: Names and references only; moving these plays onto the new model is separate work.
- Limit: A dropped play gets no new name, and its drop is recorded in an ADR with the reason.
- Limit: Past records and accepted ADRs keep their old words.
- Fails if: An old name of this family is still used outside past records after its batch.
- Fails if: A rename changes what a lifecycle or lens play does.
- Fails if: A dropped play is still laid by the install, or keeps a new name.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the rename map's lines for this family, the agreed new names, ADR 046, ADR 053 and ADR 066, the rename tool, the old-name check, and the ICE source of each lifecycle and lens play.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead, who runs the rename; and the product owner, who decides which plays go.
- Scope: In: the names of the lifecycle and lens plays, the two dropped plays, and every reference to them. Out: the naming rule, the rename map and the check, what each play does, and taking out old names in a project.

## Expectation
- Scenario: In a bank's payments service, the team renames its play that turns a request into a spec to the specifier's verb in one batch; every guide that named it changes, its ICE changes in wording only, and the old-name check finds no old name left. In a harness repository, after the reviews, ADR 066's rename makes /shape-slice /design-slice, and the two dropped lens plays are gone with no new name.
- Done means: Someone other than the one who ran the rename runs the old-name check and reads the rename's changes and the list of plays, and finds no old name of the family left outside past records, only names and references changed, and the two dropped plays absent with an ADR naming why.
