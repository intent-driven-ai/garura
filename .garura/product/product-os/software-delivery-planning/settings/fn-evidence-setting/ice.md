## Intent
- Goal: Each play resolves at its pre-flight, first match wins, its own evidence switch, then the default, then on, and writes its evidence file at its end only when the flag is on, while the one loop always writes its own and every run by hand shows the person its report whatever the flag says, so a team keeps the record of each run that it chooses to keep.
- Limit: Only a play writes evidence; no agent and no skill writes an evidence file.
- Limit: The report a person reads is never turned off by this setting.
- Limit: With no setting at all, evidence is kept.
- Fails if: A play with its flag off writes an evidence file, or a play with its flag on writes none.
- Fails if: A run by hand ends with no report to the person.
- Fails if: The evidence file is off and the report does not say so.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the evidence settings, the default and each play's switch, the evidence rule and its order of resolution, the close every play runs, how a play inside another play or a loop closes, and the loop's own evidence setting.
- Never read: any memory file by its path, and any ICE page.
- Persona: the technical lead, who decides which runs keep their record; and the product owner, who reads a run's report and, when it is kept, its evidence.
- Scope: In: the default evidence setting, each play's switch, how a play resolves them, and the note in the report when evidence is off. Out: recording each skipped checkpoint, what the evidence file and the report hold, where a run's records live, and the checkpoint settings.

## Expectation
- Scenario: In an open-source library, the default is off and /check-change's switch is on; a /commit-change run writes no evidence file and its report says so, and a /check-change run writes its evidence file. In a hospital system's project, the team turns the default on, and every play's run writes its evidence file, while the Discovery loop writes its own as before.
- Done means: Someone other than the one who set the switches reads each run's report and the issue's folders, and finds the library's /commit-change with no evidence file and "evidence skipped (record=false)" in its report, its /check-change with an evidence file, the hospital's runs each with an evidence file, and every run by hand with its report.
