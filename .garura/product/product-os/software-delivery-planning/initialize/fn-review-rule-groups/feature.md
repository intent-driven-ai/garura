# Feature: Choose the review rule groups

## What it does
Once the setup answers are confirmed, Initialize records which of the review's rule groups fit the project and which do not, each with the answer that decided it, so a review in the project runs only the groups that fit and names the groups it skipped.
- A rule group is a set of the review's rules that check one kind of thing (front end, back-end service, database, running service, permissions, personal data); the review runs or skips a group as a whole, so this feature decides per group, never per rule.
- The answers about the project decide the groups: a project with no front end, no back-end service, no database or no running service gets none of those groups. For Garura itself the answers rule out front end, back-end service, database and running service. The permission group stays kept for Garura until Garura's own answer to the permissions question says it has none (see Rules & behavior).
- The review reads this record and names, in its own record, the groups it skipped. That is how the product owner sees that a review did not run a rule and why. The change to the review that makes it do this is a later story of Initialize, not this feature (see Out of scope); this feature writes the record the review reads.
- What each group checks, and which groups the review has, are the review's: Check the code against its standards, in Code → Validation, with the review's rules in memory. This feature records which groups fit; it never decides what a group checks.
- Examples, in different kinds of project:
  - A team's command-line tool with no screens, no service and no database skips the front-end, back-end service, database and running-service groups.
  - A clinic's booking app with a web front end and patient records keeps the front-end and personal-data groups.
  - A bank's payments service with an API, a database and customer accounts keeps the back-end service, database, permission and personal-data groups.
- How it meets the capability: the capability's fourth check, "A review in the project runs only the rule groups that fit it, and the review's record names each group it skipped", rests on this record.

Status: not built. Every review runs every rule group on every project. No list of the review's rule groups exists yet: the review's rules in memory carry ids by kind of work, but none is named as a group, and no answer is tied to one.

## Inputs / Outputs
- In: the confirmed answers from Ask the setup questions (fn-setup-questions), in particular the surfaces and whether there is a database, personal data, permissions or a running service.
- In: the review's rule groups as the review's owners name them in memory, read through the memory tool.
- Out: the project's rule-group record, read by the review. It holds one entry per rule group: the group's name, kept or skipped, and the question and answer that decided it (or "no answer speaks to it" for a group kept for that reason).
- Out (in the review, not here): the review record that names each group it skipped, read from this record.

## Rules & behavior
- A group is skipped only when an answer says the project lacks what the group checks; otherwise it is kept. A database group on a project with no database gives only noise, but a group skipped by mistake hides real findings, so only a clear answer can skip one.
- Examples of answers that rule a group out:
  - Surfaces with no web and no mobile: the front-end group is skipped, because there is no screen for its rules to check.
  - Surfaces with no API and no running service: the back-end service group is skipped, because there is no service code for its rules to check.
  - Database no: the database group is skipped, because there is no schema, query or data store for its rules to check.
  - Running service no: the running-service group is skipped, because nothing is deployed or kept running for its rules to check.
  - Permissions no: the permission group is skipped, because the project gives no person or role any access for its rules to check. Permissions yes keeps it.
  - Personal data no: the personal-data group is skipped, because the project holds no data about a person for its rules to check. Personal data yes keeps it, and it is never skipped by another answer, because a leak of personal data is the costliest miss.
- Not decided: the full list of the review's rule groups and which answer rules out each one. The review's owners name them; this page's examples are not that list.
- For Garura itself, four groups that do not fit: front end, back-end service, database and running service. Garura's answer to the permissions question is not yet recorded, so the permission group stays kept for Garura until that answer says no; the permission findings on Garura's own tool files stop only then. The reason: a group no answer speaks to is kept.
- Each kept or skipped group names the answer that decided it, so a person can see why a rule did not run.
- A group no answer speaks to is kept, so a rule is never skipped by silence. The reason: a group skipped by mistake hides real findings, while a kept group can only add findings.
- The record changes only through initialize. When the project changes, a new run (Update the setup as the project changes, fn-rerun-initialize) rewrites it from the new answers.
- Not decided: where the record is kept, for the review to read it.

## Acceptance criteria
- Given answers that say there is no front end, no back-end service, no database and no running service, when the rule groups are chosen, then the record marks those four groups as skipped, each with the answer that decided it.
- Given answers that say the project has no permissions, when the rule groups are chosen, then the record marks the permission group as skipped with the permissions answer; given the answer yes, the group is kept.
- Given answers that say the project holds personal data, when the rule groups are chosen, then the personal-data group is kept with that answer named.
- Given that record, when it is read, then it lists every rule group by name as kept or skipped, each with the answer that decided it, which is all a review needs to run no rule of a skipped group and to name the groups it skipped.
- Given a rule group that no answer speaks to, when the groups are chosen, then that group is kept.

## Out of scope
- Running the review and deciding its findings (Check the code against its standards, in Code → Validation, owns it; its review of each change is /check-change).
- Changing the review play (/check-change) to read this record, run no rule of a skipped group and name the skipped groups in its own record: a later story of Initialize owns it, outside this feature, because it changes the review and not initialize. This feature only writes the record the review reads.
- What each rule group checks, which groups the review has, and the rules inside each group (the review's owners and the review's rules in memory own them).
- Asking the questions (Ask the setup questions, fn-setup-questions, owns it).

## Sources
- .garura/product/product-os/software-delivery-planning/check-code-against-standards/capability.md: "It runs every rule group, a set of the review's rules that check one kind of thing, such as a database, on every project.", "changing the review to read that record is a later story", "the review's rules with which of them fit a project (memory, and Initialize's record)"
- .garura/product/product-os/software-delivery-planning/initialize/capability.md: "A review in the project runs only the rule groups that fit it, and the review's record names each group it skipped"
- standards/rules/pr.md, in Phoenix memory, the review's rule table: "Deterministic mapping from KB quality standard IDs to PR severity buckets P1–P4."
- Shelf: none; no knowledge shelf in memory covers setting up a software project.
