## Intent
- Goal: Whenever the settings turn a checkpoint off, the play writes one record of the skip in its issue's own folder, naming the play, the checkpoint, the setting that skipped it and when, whatever the evidence setting says, so no checkpoint passes in silence; the evidence file stays a setting, and a skip teaches the learned policy nothing.
- Limit: The skip's record does not depend on the evidence setting, and the setting itself does not change.
- Limit: A skip is never counted as a person's answer.
- Limit: The settings, the evidence setting and the learned policy stay with Settings, and where a run's records live stays with Structure.
- Fails if: A checkpoint was skipped by the settings and its issue's folder holds no record of it.
- Fails if: A skip record leaves out the setting that skipped the checkpoint.
- Fails if: A skip record changes a shape's streak in the learned policy.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the gate settings and how each checkpoint resolves, the evidence setting, the issue's gate records and the answers they take, the close every play runs, and the rule that a silent gate is not a gate.
- Never read: any memory file by its path, and any ICE page.
- Persona: the developer, who turned some checkpoints off and still wants to see every one that was skipped.
- Scope: In: the skip record in the issue's folder, what it names, and keeping it out of what the learned policy learns. Out: the settings, the evidence setting and the learned policy, where a run's records live, what is owed, and the ways past at a gate.

## Expectation
- Scenario: In an online shop's project the evidence file is off and /commit-change's checkpoint is off. A developer runs /commit-change for issue 12; the checkpoint does not wait, and issue 12's folder gains one record naming /commit-change, its checkpoint, the setting that skipped it and when. The next time the learner writes the policy, no shape's streak changes because of the record.
- Done means: Someone other than the one who built it runs a play whose checkpoint is off, once with the evidence file off and once with it on, and finds one skip record in the issue's folder each time, naming the setting that skipped it, and no change to the learned policy from either.
