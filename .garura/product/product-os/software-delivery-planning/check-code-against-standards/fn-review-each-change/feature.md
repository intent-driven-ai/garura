# Feature: Review each change against the standards for what it holds

## What it does
Before a change is merged, a part that is not its builder reads which kinds of work the change holds, runs the checks the standards of each kind name on what the change adds, judges each part that carries a design against what was committed before the change, and records each finding with the standard it breaks and where, so the decision to merge rests on something outside the change.
- A change is one piece of work raised for review and merged on its own, such as a pull request on GitHub. It may hold code, tests and settings, and the documents, decision records, product model pages and memory written with them. The agents' working records, such as a run's notes, are not part of it.
- First, the kinds of work are read from what the change holds, each with the files that show it, and never from a fixed list. The standard of each kind says how it is reviewed: which of the review's rules and which tools apply, and whether its design is checked. For example, the code a shop's checkout service runs, its tests, its settings, a decision record, or the plays and skills of a coding agent's harness, the parts that tell a coding agent how to work.
- Then the tools run, for every check that needs no judgment:
  - a tool matches the review's rules that fit the project against the lines the change adds and the files it changes; the rules come in rule groups, each a set of rules that check one kind of thing, such as a database, and a project's record says which groups fit it;
  - the checks the project's code already holds run, such as its linter and its type check;
  - the tests inside the code are not run again when the record of the build's separate test run covers the code the change holds; when no such record is there, as for a change made outside the build, they run once through a tool, and the record says no separate run was on record.
- Then, for each part that carries a design, an agent that is not the builder reads the design decided before the change, from what was committed before it, the decision records and memory, and never from what the change adds, and judges whether the change keeps to it. For a product's code, that design is the architecture with its technology and the design of the work in force; for a coding agent's harness, the decided patterns of how its parts work together.
- Each finding names the standard it rests on, the file and the line, and its rank, how serious it is. A check that could not run is named with its reason and is never a pass. A kind of work with no standard is named as having nothing to check against.
- Findings it records, for example, in different kinds of product:
  - in a shop's checkout service, a change builds a database query by joining in what a shopper typed;
  - in a school's timetable app, a change adds a library that the architecture's technology does not include;
  - in a coding agent's harness, a change makes a skill read memory by its path instead of through the memory tool;
  - in a team's release command, a new test asserts nothing.
- How it meets the capability: every change is checked from outside, against standards set before it, before a person approves its merge; Code → Validation must not "Let a builder grade itself".

Status: built in part. The review of each change, /check-change, runs on every change in Garura's own repository. It reads the change from the code host, has an agent sort it into kinds of work and take each kind's treatment from the review's rules in memory, matches the rule table with a tool and "No LLM judgment.", runs the project's linter, Garura's own linters for its plays, skills and agents, and the tests when a change touches them, has an agent check the design of Garura's harness and memory against committed sources, and records each finding with its basis. Not built:
- Reading the record of the build's separate test run instead of running the tests; that separate run is not built either.
- Running only the rule groups that fit the project: Initialize, which sets a project up for Garura after the install, writes the record of them in an approved feature, and "Changing the review play (/check-change) to read this record" is left to a later story (#862).
- Checking a product's code against its own coding standards, its architecture or the design of its work. For code the review's standard is "industry best practice", and no review reads a project's coding standards. An architecture memory for a harness to review against is planned (#933, #967).
- Rules that measure. The rule table matches names and words; a rule whose evidence asks for a figure, such as a function's complexity, matches only a file's name. In practice the review's agent also reads the code against the review's rubric for code and ranks each finding by the table's words; these findings carry no rule of the table.
- Checking the scripts inside plays and skills as code: the review classes them as prose, "so code rules never check them" (#890, #535).
- A standard for product model pages (#870), leaving the agents' working records out of the review (#939), and stopping when the review's rules cannot be found (#974).

## Inputs / Outputs
- In: the change: what it adds, the files it changes, and what was committed before it.
- In: the review's rules for each kind of work, and the project's record of the rule groups that fit it, from memory, the project's own copy first.
- In: the project's coding standards and the checks its code already holds, such as its linter settings.
- In: the architecture with its technology, the deployment design, the declared surfaces and the design of the work in force, with their confirmed updates.
- In: the record of the build's separate test run, when there is one.
- Out: the kinds of work the change holds, each with the files that show it and the standard it was reviewed against.
- Out: each finding, with the standard it rests on, the file and the line, and its rank; each check that could not run, with its reason; each kind with nothing to check against; and whether the tests were taken from the separate run's record or run once here. These go to Give the verdict on the code, and send each finding to the developer or to a person (fn-send-code-findings).

## Rules & behavior
- Not the builder. A part that is not the builder reviews the change. The reason: "A builder believes its own work, so its opinion isn't evidence."
- The change is never its own standard. A design is read from what was committed before the change, never from what the change adds. The reason: "The guiding rule: the change under review is never its own standard.", "otherwise the branch grades its own homework."
- Kinds are read from the change, never from a fixed list. The reason: the review assesses "what categories of work the diff actually contains" on every run, and a change can hold a kind no list foresaw.
- Only the rules that fit the project. A rule group the project's record skips does not run, and the record of the review names it; a group no answer speaks to is kept. The reason: "a review in that project runs only the rule groups that fit it", and "a group skipped by mistake hides real findings".
- Against the project's own standards, the architecture and the design. A product's code is checked against its coding standards, its architecture and the design of the work in force, not only against the review's rules. The reason: Build the work test first hands over "checking the code against the project's standards", and each slice "is then designed and built on the project's architecture, and does not choose its own."
- A tool checks, an agent judges only the rest. Every check that needs no judgment runs through a tool; an agent judges only what no tool checks, and each judgment names the standard it rests on, from a committed source, and the file and line. The reason: the rule table is matched with "No LLM judgment." and the tool "MUST produce a byte-identical" result on the same change, while an agent's judgment can be checked only against the standard it names.
- Records are evidence, not run again. The reason, from the product owner's approved list: "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again." Where no separate run is on record, running the tests once is not running them again.
- Not checked is never passed. A tool that is missing or crashed is named with its reason. The reason: "Neither is a pass, and neither stops the review."
- The review's rules must be there. When they cannot be found in any tier, the review stops and says what is missing and where it looked. The reason: "It should stop and say the rules are missing."
- The agents' working records stay out; the product model and memory stay in. The reason: "The product model and the project's memory are outputs of the change and must be reviewed."
- Not decided: how the record of the build's separate test run is matched to the code a change holds.
- Not decided: whether the review may write a treatment by hand for a kind of work no standard covers, as it does today for product model pages (#870).
- Not decided: whether a finding that blocks needs a second, independent run before it counts, while an agent's judgment may not repeat.
- Not decided: where the checks run while no deployment design places them; today the review runs in the session that raised the change.

## Acceptance criteria
- Given a change that holds code, its tests and a decision record, when it is reviewed, then each kind is named with the files that show it and reviewed against its own standard.
- Given a change whose code builds a database query by joining in what a person typed, when it is reviewed, then a tool records a finding with the standard, the file and the line.
- Given a change that rewrites a play and also rewrites the page that describes how plays work, when the play's design is checked, then the design is read from what was committed before the change, never from the rewritten page.
- Given a project whose record skips the database rule group, when a change is reviewed, then no rule of that group runs, and the review's record names the group as skipped.
- Given a change whose code is covered by the record of the build's separate test run, when it is reviewed, then the tests are not run again and the record is named; given a change with no such record, the tests run once and the record says none was on record.
- Given a linter the project's standards name that is not installed, when the change is reviewed, then the check is named as not run, with its reason, and is not a pass.
- Given no tier holding the review's rules, when the review starts, then it stops and names what is missing.

## Out of scope
- Raising the change, its self-review, and merging it with a person's yes. Ship every change the same way, in Developer tooling, does them.
- Giving the verdict and sending each finding back. Give the verdict on the code, and send each finding to the developer or to a person (fn-send-code-findings) does it.
- Checking the whole built work rather than one change. Check the whole built work against its standards and the profile's levels (fn-check-whole-built-work) does it.
- Choosing which rule groups fit the project. Initialize records it, and this feature reads the record.
- Writing the review's rules, the coding standards, the architecture or the design. Their owners do, and this feature reads them.
- Running the tests inside the code as part of the build. Build the work test first does it.

## Sources
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "reviewing a change against its standards is BI-4's", "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again."
- .garura/product/product-os/intents/bi-4.md: "A builder believes its own work, so its opinion isn't evidence.", "Let a builder grade itself, weaken a check to pass, or count a check that did not run as a pass."
- .garura/product/product-os/software-delivery-planning/build-work-test-first/capability.md: "Out: checking the code against the project's standards. Check the code against its standards, in Code → Validation, owns it; the build follows the standards while it writes."
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "Each slice is then designed and built on the project's architecture, and does not choose its own."
- .garura/product/product-os/software-delivery-planning/initialize/fn-review-rule-groups/feature.md: "a group skipped by mistake hides real findings", "Changing the review play (/check-change) to read this record, run no rule of a skipped group and name the skipped groups in its own record"
- core/components/plays/check-change/reference/ice.md: "The guiding rule: the change under review is never its own standard.", "what categories of work the diff actually contains"
- core/components/plays/check-change/SKILL.md: "Neither is a pass, and neither stops the review."
- core/components/skills/check-pr-quality/SKILL.md: "MUST produce a byte-identical"
- .garura/project/issues/1031/review/quality-findings.yaml: "rubric_findings - defects found by reading the code against the playbooks' rubric and by running it."
- standards/rules/pr.md, in Phoenix memory: "No LLM judgment.", "file, function, complexity-score"
- knowledge/review/code.md, in Phoenix memory: "the standard is industry best practice, not a garura-internal design."
- knowledge/review/harness.md, in Phoenix memory: "otherwise the branch grades its own homework."
- knowledge/review/tests.md, in Phoenix memory: "execute the test suite and confirm it passes."
- GitHub #862 (open): "a review in that project runs only the rule groups that fit it"
- GitHub #933 (open): "a review tests a change against it."
- GitHub #890 (open): "so code rules never check them"
- GitHub #535 (open): "has no model of what the project is, so Garura's own scripts are never code-checked"
- GitHub #870 (open): "check-change has no review playbook for two kinds of change that plays make all the time"
- GitHub #939 (open): "The product model and the project's memory are outputs of the change and must be reviewed."
- GitHub #974 (open): "It should stop and say the rules are missing."
