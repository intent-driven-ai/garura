# Feature: Give the verdict on the code, and send each finding to the developer or to a person

## What it does
Once a change is reviewed, or the whole built work is checked, this feature gives one verdict by one fixed rule over the findings, decided by a person or by that rule as the project's setting says, and sends each finding back as a handoff plan, to the developer when the builder can fix it alone, to the test writer when it is about a test, or to the product owner when a person must decide, so the product owner knows whether the code keeps to its standards before a person approves its merge, and each finding reaches the one who can fix it.
- The verdict gives each standard the change or the work touches a pass or a fail, with how and where it was checked, and names each standard not checked with its reason. One fixed rule over the findings decides it, so the same findings always give the same verdict:
  - what blocks follows each finding's rank, how serious it is, in the rank table in force, and a profile pass bar may make more block, such as no linter errors at all;
  - a standard that was not checked makes the verdict not a pass;
  - when the project holds no standard for a kind of work, or the profile sets no level, the verdict says so, and that part is neither a pass nor a fail.
- Who decides is a project setting. With it off, the rule's verdict is the verdict, recorded and shown as the harness's own, not a person's. With it on, a person who is not the builder decides, the product owner or the one they name; when that person's decision differs from the rule's, the record keeps both and names each finding left open.
- The merge is not decided here. Ship every change the same way, in Developer tooling, reads this verdict before the merge, and the merge then waits for a person's yes.
- For people, each finding says in plain words what is wrong, where, what it leads to and its rank, with the standard it rests on after it.
- For the builder, each finding becomes a handoff plan: what is wrong, where it is, by file and line, and the way back, what must be true again, as guidance and never code. It never names the check, its rule, its id or its tool. For example:
  - in a shop's checkout service: in the order search, what a shopper types is joined into the database query, so a typed command could reach the database; the search must pass what was typed as a value only;
  - in a clinic's booking app: in the cancel handler, a failed save is caught and dropped, so a patient is told a visit was cancelled when it was not; the failure must reach the patient;
  - in a coding agent's harness: a skill reads memory by its path; it must read memory only through the memory tool.
- Who gets it follows the recovery rule's test, whether the builder can fix it from what it already has:
  - the developer, when the way back is a change of the code the builder controls;
  - the test writer, when the finding is about a test, such as a test that asserts nothing; never the builder, who never sees a test;
  - the product owner, when it needs judgment or authority the builder does not hold, such as a library the architecture's technology does not include, a change of the deployment design or an environment, a rule that fires on something it should not, a missing standard, a level the code cannot meet, or code that departs from the design in force with no confirmed update;
  - a person, whenever it is in doubt.
- Before the work is accepted, the developer and the test writer get a handoff plan through Build the work test first; after it is accepted, a finding is a defect for Fix defects test first, which takes in "a finding in a review".
- The product owner decides each finding a person must decide: it is fixed, the standard it rests on is updated through its owner, a level is moved by an approved decision, or the review is decided on record. Nothing lets a finding through any other way.
- The verdict and the findings are kept where no part that builds the work reads them.
- How it meets the capability: every standard gets an answer, and each finding goes back without the builder seeing the checks, as Code → Validation asks; it must not "Let a builder grade itself, weaken a check to pass".

Status: built in part. The review of each change gives its verdict by one fixed rule, reject "if any P1 finding (or a runnable suite is red)", with "no LLM judgment."; the project's setting decides whether a person decides it or the rule's verdict stands; the decision is recorded with who made it and posted on the change; and the merge in Developer tooling reads it. Both ways are on record in Garura's own repository: one change decided by the rule ("decided_by: harness") and one by the person ("decided_by: human", "recommended: approve", with the findings left open listed). Not built:
- A tool that did not run is recorded and is never a pass, but the rule over the findings can still approve the change.
- Findings come out as "an id, a class and a short label", each naming its rule (#902); they are posted on the change and kept on its branch, where a part that builds the work could read them.
- Nothing writes a handoff plan, sends a finding to the developer, the test writer or a person by who can fix it, or hands a finding after acceptance to the defect fix.
- One severity for findings and defects is planned (#934).
- In Garura's own repository the setting still names the review's old play name, so a person decides there (#772).

## Inputs / Outputs
- In: the findings of the review of each change, or the results of the check of the whole built work, each with the standard it rests on, where it was found and its rank, and each standard not checked, with its reason.
- In: the rank table in force, the profile's pass bars, and the project's setting for who decides the review.
- In: the person's decision, when the setting asks a person.
- In: what the builder controls, the standards with their owners, and whether the work was already accepted.
- Out: the verdict, with a pass or a fail for each standard touched, how and where each was checked, each standard not checked with its reason, each part with nothing to check against, who decided, and, when a person's decision differs from the rule's, both, with each finding left open.
- Out: for each finding, the plain-words record for people, and a handoff plan to the developer or the test writer through Build the work test first, to the product owner, or, after acceptance, to Fix defects test first as a defect; and, in the verdict, where each one went.

## Rules & behavior
- One fixed rule gives the verdict. The reason: the rule reads the findings with "no LLM judgment.", so the same findings give the same verdict.
- Not checked is never passed. The reason: "An unmeasured bar is not a passed bar."
- Nothing to check against is said plainly, never read as a pass. The reason: the product owner approved the same for performance, "neither a pass nor a fail".
- Who decides is a project setting. The reason: "Everything that can be turned on or off lives in settings."
- A person's decision that differs from the rule's is on record with each finding it left open. The reason: Code → Validation must not "weaken a check to pass", and a finding let through with no record is let through in silence.
- The merge stays in Developer tooling. The reason, from the product owner's approved list: "reviewing a change against its standards is BI-4's", while merging stays with Ship every change the same way.
- Plain words for people. The reason, in the product owner's words: "A defect needs to have a problem statement clearly defined.", "Where is the problem happening, and what would it lead to?"
- What is wrong, where and the way back, never the check or its rule. The reason: a handoff plan "never names the failure condition, its id or the check", and the builder never gets the checks' results.
- The way back is guidance, never code. The reason: the way back is "the inverse of the failure, as guidance, never code", and how to build it is the developer's.
- The builder only when it can fix it alone; the test writer for a test; a person otherwise, and whenever it is in doubt. The reason: the recovery rule's test, "Can the builder fix this from information it already has, deterministically?"; "Only the test writer changes, adds or takes out a test"; and the product owner's approval with Test security of "the line on a finding that changes the architecture, the deployment design or an environment settled as the product owner's".
- Code that departs from the architecture or the design in force with no confirmed update goes to the product owner. The reason: the architecture and the design change only when a person confirms them: "An agent proposes each choice and a person confirms it.", "the technical lead confirms or changes each choice".
- Before acceptance to the build, after acceptance to the defect fix. The reason: the approved Fix defects test first takes in "a finding in a review".
- The verdict stays away from the builder. The reason: "giving it to the builder only invites teaching-to-the-test."
- Not decided: where the verdict and the handoff plans are kept so a person reads them and no part that builds the work does; today the review posts every finding on the change and keeps its records on the change's branch.
- Not decided: the rank of each finding, while #934, one severity from P1 to P4 for findings and defects, is open.

## Acceptance criteria
- Given findings of which none has a rank that blocks, and every standard checked, when the verdict is given, then it is a pass, and each finding still goes back.
- Given a linter the standards name that did not run, when the verdict is given, then it is not a pass, and the linter is named with its reason.
- Given a kind of work with no standard, when the verdict is given, then that part is named as having nothing to check against, neither a pass nor a fail.
- Given the setting off and a blocking finding, when the verdict is given, then the change is rejected and the record shows the harness decided; given the setting on and a person who approves over that finding, then the record keeps the rule's verdict, the person's decision and the finding left open.
- Given a search query built by joining in what a shopper typed, when the handoff plan is written, then it names the file, the line and the way back, goes to the developer, and names no check, rule, id or tool.
- Given a test that asserts nothing, when it is sent back, then it goes to the test writer and not to the builder.
- Given a library the architecture's technology does not include, when it is sent back, then it goes to the product owner.
- Given a finding after the work was accepted, when it is sent back, then it goes to Fix defects test first as a defect.
- Given a verdict, when the inputs of the parts that build the work are checked, then none of them names it.

## Out of scope
- Reviewing each change and checking the whole built work. Review each change against the standards for what it holds (fn-review-each-change) and Check the whole built work against its standards and the profile's levels (fn-check-whole-built-work) do them.
- Merging the change with a person's yes. Ship every change the same way, in Developer tooling, does it.
- Fixing a finding. Build the work test first does it before the work is accepted, and Fix defects test first after.
- Updating a standard, the architecture or the design, or moving a level. Their owners do, after a person's yes.
- Recording a defect in the tracker. Orchestration owns it.
- Reviewing again and counting the rounds. Check the code again as the product and its standards change (fn-recheck-code) does it.

## Sources
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "reviewing a change against its standards is BI-4's"
- The capability list the product owner agreed on 2026-11-03, in the same file: "Settings: Everything that can be turned on or off lives in settings."
- The product owner's approval of Test security on 2026-11-09, in .garura/project/issues/1021/context/bi-4-capability-2/page-approvals.md: "with the line on a finding that changes the architecture, the deployment design or an environment settled as the product owner's"
- The product owner's approval of Test performance on 2026-11-09, in .garura/project/issues/1021/context/bi-4-capability-3/page-approvals.md: "with the verdict saying so plainly, neither a pass nor a fail, when no performance level is set"
- The product owner on a defect, 2026-10-27, quoted in GitHub #902 (open): "A defect needs to have a problem statement clearly defined.", "Where is the problem happening, and what would it lead to?", "an id, a class and a short label"
- .garura/product/product-os/intents/bi-4.md: "Let a builder grade itself, weaken a check to pass, or merge without a person."
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-update-tests-and-code/feature.md: "Only the test writer changes, adds or takes out a test, always with its reason.", "A handoff plan is the exact list of the work it calls for."
- .garura/product/product-os/software-delivery-planning/fix-defects-test-first/capability.md: "In: taking in a defect reported anywhere: a person's words, a finding in a review, the eval after the work was accepted, or a bug in a plan.", "Out: recording a defect in the tracker"
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "An agent proposes each choice and a person confirms it."
- .garura/product/product-os/software-delivery-planning/design-work/capability.md: "the technical lead confirms or changes each choice"
- core/components/plays/check-change/SKILL.md: "if any P1 finding (or a runnable suite is red)"
- core/components/plays/check-change/scripts/compute_verdict.py: "no LLM judgment."
- .garura/project/issues/993/review/decision.yaml: "decided_by: harness"
- .garura/project/issues/1031/review/decision.yaml: "decided_by: human", "recommended: approve"
- core/components/plays/validate-epic/SKILL.md: "An unmeasured bar is not a passed bar."
- standards/rules/expectation-generation.md, in Phoenix memory: "Can the builder fix this from information it already has, deterministically?", "the inverse of the failure, as guidance, never code"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The handoff plan never names the failure condition, its id or the check."
- docs/philosophy/idd-principles.md: "giving it to the builder only invites teaching-to-the-test."
- GitHub #934 (open): "Findings and defects get one severity, P1 to P4"
- GitHub #772 (open): "The install keeps old play names in the project config, so the check-change gate is on"
