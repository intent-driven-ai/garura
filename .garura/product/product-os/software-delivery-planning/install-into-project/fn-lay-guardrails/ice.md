Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: The install lays Garura's guardrails, which keep an agent from doing a play's work without the play, in every project it installs into, in the coding tool's own form, keeps each in the install record so the take-out removes it, and changes the team's own coding tool settings only on the person's yes, keeping every setting the team already has.
- Limit: The coding tool's own settings file is the team's: the change is shown first and waits for the person's yes, and every setting the team had stays.
- Limit: Every guardrail laid has a way past it, as Orchestration defines it.
- Limit: Each guardrail and each change to the team's file is in the install record, and the take-out removes exactly those.
- Fails if: A project installed with Garura has no guardrails, or an agent there runs a play's script with no run of that play and nothing refuses it.
- Fails if: A setting the team had in its coding tool's settings file is changed or gone, or the file changed without the person's yes.
- Fails if: After a take-out, a guardrail of Garura's is still there, or one of the team's own settings is gone.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the guardrails Orchestration defines with their ways past, the coding tool's own settings file as the team has it, the hooks the team already has, and the install record.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who wants every agent in the project to work through the plays.
- Scope: In: laying, recording and taking out the guardrails, and the change to the team's coding tool settings. Out: what each guardrail guards and its way past, the run marker inside each play, the check in the review of each change, and each tool's form.

## Expectation
- Scenario: A clinic's booking app has hooks of its own in its coding tool's settings. Garura is installed: the change to that file is shown, the product owner says yes, the guardrails are added beside the team's hooks, and the record names them. An agent then tries to run a play's script by hand and is refused, with the way past named. At take-out, Garura's guardrails go and the team's hooks stay.
- Done means: Someone other than the one who installed it compares the coding tool's settings file before the install, after it and after the take-out, finds every setting of the team's kept and the person's yes on record, and tries a play's script by hand and sees it refused.
