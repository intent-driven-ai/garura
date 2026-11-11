## Intent
- Goal: Each checkpoint a play declares resolves from the settings, first match wins: a pinned checkpoint always waits; otherwise the play's own switch, then for a conditional checkpoint the policy learned from a person's earlier answers, then the switch of its kind of risk, then the default, and with no settings it waits; each answer at a conditional checkpoint is kept in its issue's gate history, and at the play's close the learner writes one policy for the project that lets a kind of change pass after a run of clean answers and keeps every permanent pin, so a team decides once where its people wait.
- Limit: No setting, policy or ledger turns a pinned checkpoint off; an off setting that would match one is refused and recorded.
- Limit: The settings reach only checkpoints, never a pre-flight halt, a sensitive-file block, a stop condition or an eval failure.
- Limit: A checkpoint is turned off only in the change that adds the checks that replace it.
- Limit: Any rejection, requested edit or correction makes a kind of change wait again, and a person's permanent pin is never learned away.
- Limit: The learned policy is a setting of the project, never memory.
- Fails if: A pinned checkpoint passes because of a setting or the learned policy.
- Fails if: A checkpoint waits that its play's setting turns off, or passes that its setting leaves on, because the play reads its switch under another name.
- Fails if: A kind of change passes on its own without its run of clean answers, or after a rejection, or after a person pinned it.
- Fails if: A person's answer at a conditional checkpoint is not in its issue's gate history.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the gate rule with its three kinds, its order of resolution and its pinned list, the `gates` settings, each play's declared checkpoints and the name under which it reads its switch, each issue's gate history, the learned policy with its permanent pins, and the scripts that classify a change, keep the history and learn the policy.
- Never read: any memory file by its path, any ICE page, and the learned policy as memory.
- Persona: the product owner or the technical lead, who decides once for the project which checkpoints wait for a person.
- Scope: In: the checkpoint settings, how a checkpoint resolves from them, each issue's gate history, and the learned policy with its permanent pins. Out: the way past each gate, the record of each skipped checkpoint, the list of pinned yeses, pinning a checkpoint or adding one to a play, where a run's records live, and the evidence setting.

## Expectation
- Scenario: In a clinic's booking app, the team turns /commit-change's checkpoint off; it no longer waits, and the merge onto main still waits for the product owner's yes though a setting would turn it off, with "pinned — config bypass refused" recorded. In a news site's content service, a person approves the same kind of model change three times with no edit, and on the next run /discover-capabilities lets it pass on its own; when the person then rejects one, that kind waits again.
- Done means: Someone other than the one who set the switches reads the settings, each issue's gate history and the learned policy, and finds the clinic's /commit-change passing with no wait, its merge asked, the refused bypass recorded, the news site's three clean answers and the rejection in their issues' histories, and the policy letting that kind pass only between the third answer and the rejection.
