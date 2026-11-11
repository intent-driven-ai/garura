## Intent
- Goal: The change plays, the plan plays, the knowledge plays and the play that records a decision carry the names of the naming standard in force, with every reference to them changed in the same batch, setting keys included, and nothing else changed, so the old-name check finds none of their old names; under ADR 046 that is done, and ADR 066's names follow in one change after the reviews of BI-10 and BI-11.
- Limit: Names and references only; no play's behaviour changes.
- Limit: A play removed with no successor stays in the rename map with no new name.
- Limit: Past records and accepted ADRs keep their old words.
- Fails if: An old name of this family is still used outside past records after its batch.
- Fails if: A rename changes what a play does, or leaves a setting keyed by an old name.
- Fails if: A play keeps a one-word name.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the rename map's lines for this family, the agreed new names, ADR 046, ADR 051, ADR 059 and ADR 066, the setting keys named after plays, the rename tool, and the old-name check.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead, who runs the rename; and the developer, a person or an AI agent who builds the code, who types these plays every day.
- Scope: In: the names of the change, plan, knowledge and record plays, and every reference to them. Out: the naming rule, the rename map and the check, what these plays do, and taking out old names in a project.

## Expectation
- Scenario: In a bank's payments service, the team renames its play that reviews a change and its one-word play `/today` to names the rule gives; every guide, script and setting key changes in the same batch, and the old-name check finds no old name left. In a harness repository, after the reviews, ADR 066's rename makes /update-plan /reshape-plan and /list-focus-issues /list-issues, in one change.
- Done means: Someone other than the one who ran the rename runs the old-name check and reads the rename's changes and the settings, and finds no old name of the family left outside past records, only names and references changed, every setting key under its play's new name, and no one-word play.
