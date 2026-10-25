# Feature: Choose the review rule groups

## What it does
- Runs after the setup answers are confirmed. It records which rule groups of the review fit the project and which do not, so a review in the project runs only the groups that fit.
- The answers about the project decide the groups: a project with no front end, no back-end service, no database or no running service gets none of those groups. For Garura itself the answers rule out front end, back-end service, database and running service. The permission group stays kept for Garura until Garura's own answer to the permissions question says it has none (see Rules & behavior).
- The review reads this record and names, in its own record, the groups it skipped. That is how the product owner sees that a review did not run a rule and why.

## Inputs / Outputs
- In: the confirmed answers from fn-setup-questions, in particular the surfaces and whether there is a database, personal data, permissions or a running service.
- In: the review's rule groups as Phoenix memory holds them, read through the memory tool.
- Out: the project's rule-group record, kept in the product profile beside the setup answers, so the review reads it where every later play reads the project's facts. It holds one entry per rule group: the group's name, kept or skipped, and the question and answer that decided it (or "no answer speaks to it" for a group kept by default). Our default; the sources do not say where the record is kept or its shape.
- Out (in the review, not here): the review record that names each group it skipped, read from this record.

## Rules & behavior
- A group is skipped only when an answer says the project lacks what the group checks; otherwise it is kept. A database group on a project with no database gives only noise, but a group skipped by mistake hides real findings, so only a clear answer can skip one.
- Which answer decides which group (our default; the sources name the groups for Garura but not the full list, see the manifest's gaps):
  - Surfaces with no web and no mobile: the front-end group is skipped, because there is no screen for its rules to check.
  - Surfaces with no API and no running service: the back-end service group is skipped, because there is no service code for its rules to check.
  - Database no: the database group is skipped, because there is no schema, query or data store for its rules to check.
  - Running service no: the running-service group is skipped, because nothing is deployed or kept running for its rules to check.
  - Permissions no: the permission group is skipped, because the project gives no person or role any access for its rules to check. Permissions yes keeps it.
  - Personal data no: the personal-data group is skipped, because the project holds no data about a person for its rules to check. Personal data yes keeps it, and it is never skipped by another answer, because a leak of personal data is the costliest miss.
- For Garura itself, #862 names four groups that do not fit: front end, back-end service, database and running service. The sources do not give Garura's answer to the permissions question, so the permission group stays kept for Garura until that answer says no; #860's permission findings stop only then. Our default, held in the manifest's gaps.
- Each kept or skipped group names the answer that decided it, so a person can see why a rule did not run.
- A group no answer speaks to is kept, so a rule is never skipped by silence. Our default; the sources do not say what happens to such a group.
- The record changes only through initialize. When the project changes, a new run (fn-rerun-initialize) rewrites it from the new answers.

## Acceptance criteria
- Given answers that say there is no front end, no back-end service, no database and no running service, when the rule groups are chosen, then the record marks those four groups as skipped, each with the answer that decided it.
- Given answers that say the project has no permissions, when the rule groups are chosen, then the record marks the permission group as skipped with the permissions answer; given the answer yes, the group is kept.
- Given answers that say the project holds personal data, when the rule groups are chosen, then the personal-data group is kept with that answer named.
- Given that record, when a review runs in the project, then it runs no rule of a skipped group and its record names the groups it skipped.
- Given a rule group that no answer speaks to, when the groups are chosen, then that group is kept.

## Out of scope
- Running the review and deciding its findings (the review play, /check-change, owns it).
- Asking the questions (fn-setup-questions owns it).
- Writing or changing the rules inside a group (the review's own memory owns them).

## Sources
- GitHub #862: "a review in that project runs only the rule groups that fit it (for Garura itself: no front end, no back-end service, no database, no running service), and the review record names the groups it skipped".
- GitHub #862, Identified by: "#860 (the review of PR #858 ran database, permission and front-end rules on Garura's own tool files)".
- Shelf: none (routing.yaml, unmatched).

## Agent intent (ICE)
- Goal: After initialize, the project holds a record of which review rule groups fit it, each kept or skipped group naming the answer that decided it.
- Goal: A review in the project runs only the kept groups, and its record names the groups it skipped.
- Limit: Skip a rule group only when an answer rules it out; never skip one by silence.
- Fails if: a review in the project runs a rule group the answers rule out, as in #860.
- Fails if: a review skips a group and its record does not name it.
- Context: serves the product owner, who reads review findings, and the review play that reads the record in the product profile; for Garura itself the front end, back-end service, database and running service groups are skipped, and the permission group is kept until Garura's permissions answer says no; out are running the review and the rules inside each group.
- Checked by: run `initialize` on Garura with its answers, then run a review on a change to its tools and check that no database or front-end finding appears and that the review record names the skipped groups.
