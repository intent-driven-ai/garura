## Intent
- Goal: After initialize, the project holds a record that names every rule group of the review as kept or skipped, each with the answer that decided it, so that a review which reads it, once a later story under #862 changes the review, runs only the kept groups and names the groups it skipped.
- Limit: Skip a rule group only when an answer rules it out; never skip one by silence.
- Limit: Record which groups fit; never decide what a group checks, and never change a rule inside one.
- Fails if: the record keeps a rule group the answers rule out, so a review that reads it would run that group, as in #860.
- Fails if: the record skips a group and does not name the answer that skipped it.
- Fails if: the record skips a group that no answer speaks to.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the confirmed answers about the surfaces and about a database, personal data, permissions and a running service; the review's rule groups as the review's owners name them in memory; and the record of an earlier run.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who reads the review's findings and wants only the ones that fit the project.
- Scope: In: one entry per rule group, kept or skipped, with the answer that decided it. Out: running the review, changing the review to read the record, what each group checks, and the rules inside each group.

## Expectation
- Scenario: Garura itself answers no front end, no back-end service, no database and no running service, and has no recorded answer on permissions. The record marks the front-end, back-end service, database and running-service groups as skipped, each with its answer, and keeps the permission group with "no answer speaks to it". A team's command-line tool with the same four answers gets the same four skipped, and a clinic's booking app with a web front end and patient records keeps the front-end and personal-data groups.
- Done means: Someone other than the one who ran Initialize reads the record against the answers and finds every rule group named, every skipped group with the answer that ruled it out, and no group skipped where no answer speaks to it.
