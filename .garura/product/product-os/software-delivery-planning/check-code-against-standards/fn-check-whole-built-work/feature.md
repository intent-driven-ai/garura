# Feature: Check the whole built work against its standards and the profile's levels

## What it does
Once a piece of work is built, this feature checks the whole of its code, not only one change's lines, by a part that is not the builder, against the project's coding standards, the architecture and the design in force, and the profile's maintainability level, with its reliability level where the pass bar names a check of the code, so the product owner knows whether the built work as a whole keeps to what the project set.
- A piece of work is what Build the work test first builds under one chosen item of the plan, such as an epic that stands for a slice. A slice is an ordered group of features that one person can test end to end on one surface.
- It checks what no single change shows: a bar that many small changes break together, such as a size limit for each part of the code that no one change crossed; and whether the whole built work keeps to the architecture and to the design of the work, such as each component the design names being built where the design puts it.
- It checks the profile's maintainability level, its pass bar and each capability's maintainability need. It checks the reliability level only where its pass bar or a capability's reliability need names a check of the code, such as a test or a linter. A part of reliability that can only be measured on the running product, such as how long it stays up under use, is named as not checked here, and goes to the product owner.
- The checks run through tools wherever the standards name one, such as the build, the type check, the linter and a measure of the code; an agent that is not the builder judges only what no tool checks, such as whether the code keeps to the design, and names the standard it rests on.
- It takes as evidence, and does not run again, the reviews of each change and the record of the build's separate test run. It never tests the security, performance or accessibility levels; the other capabilities of Code → Validation do.
- Each result is compared with its standard or its pass bar; a tool's own clean run is not the result. A standard or a bar that no check measured is named with its reason and is never a pass.
- What it finds, for example, in different kinds of product:
  - in a bank's statements job, the maintainability pass bar sets a size limit for each part of the code; after five changes, none of which crossed it alone, one part is over it;
  - in a coding agent's harness, whose reliability pass bar names its own checkers' tests, one of those tests fails on the whole built work;
  - in a shop's checkout service, the design puts the price rules in one component, and the whole built work holds a second copy of them in the payment screen.
- How it meets the capability: the review of each change sees only that change's lines; this check shows that the whole built work keeps to the project's standards and the levels it committed to.

Status: not built. What exists covers only parts of it:
- The old slice check, /validate-epic, is stale and waits for a rebuild. It ran "everything mechanically through a per-tool runner family", the work's tests, the scans of the code and the slice's quality checks, and compared the results with the product profile's floors: "Green is the entry condition, never the verdict". It read an epic record the model no longer holds.
- The quality auditor, an agent, "Independently verifies code quality standards: linting, unit tests, type checking, build, and project-defined quality vision gates.", and reports what it measured against each bar; only stale plays ask it for that full run.
- The runner for a slice's written quality checks is built, and no live play runs it; a missing tool is a finding, "never a silent pass". No approved page writes a slice's quality checks now.
- Garura's own profile sets maintainability and reliability at medium, with pass bars that name tests and linters; nothing checks the code against them.

## Inputs / Outputs
- In: a copy of the whole built work of a piece of work.
- In: the project's coding standards and the checks its code already holds.
- In: the architecture with its technology, the deployment design, the declared surfaces and the design of the work in force.
- In: the product profile's maintainability and reliability levels with their pass bars, and each capability's maintainability and reliability needs.
- In: the records of the review of each change in the work, and the record of the build's separate test run.
- Out: a result for each standard, each part of each pass bar and each need, with how and where it was checked, and each part not checked, with its reason; for Give the verdict on the code, and send each finding to the developer or to a person (fn-send-code-findings).

## Rules & behavior
- The whole built work, not one change. The reason: a bar such as a size limit is about the whole code, and the review of each change sees only its own lines; Test security already tests "the whole of the built work, not only the lines a change added." for security.
- Against the levels the profile commits to. The reason: the old check compared results with the profile's floors, and "The NUMBERS live in the product profile, per product — never in this KB."
- Reliability only where its pass bar names a check of the code. The reason: a measure of the running product cannot be faked from the code, and the running build is tested only in the testing environment, by the other capabilities of Code → Validation.
- A tool's own pass is not the result. The reason: "Green is the entry condition, never the verdict".
- Not checked is never passed. The reason: "An unmeasured bar is not a passed bar."
- Records are evidence, not run again. The reason: "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again."
- Not the builder, and on a copy, never in production. The reason: "A builder believes its own work, so its opinion isn't evidence.", and "We are never touching production."
- Not decided: where the part of reliability that can only be measured on the running product is checked.
- Not decided: when this check runs, once the whole piece of work is built or also after each change to it, and which parts run again.

## Acceptance criteria
- Given a maintainability pass bar with a size limit and a part of the code over it after several changes, none over it alone, when the whole built work is checked, then that part is named with the bar it breaks.
- Given a reliability pass bar that names a measure of the running product only, when the whole built work is checked, then reliability is named as not checked here, with its reason, and not passed.
- Given a tool the standards name that cannot run, when the whole built work is checked, then that part is named as not checked and is not a pass.
- Given a security level in the profile, when the whole built work is checked, then no security test runs here.
- Given the record of the build's separate test run, when the whole built work is checked, then the tests are not run again.

## Out of scope
- Reviewing each change before its merge. Review each change against the standards for what it holds (fn-review-each-change) does it.
- Testing security, performance, accessibility and the user experience. The other capabilities of Code → Validation do it.
- Giving the verdict and sending each finding back. Give the verdict on the code, and send each finding to the developer or to a person (fn-send-code-findings) does it.
- Setting a level, a pass bar or a capability's need. Specify the product sets them, and only an approved decision moves them.

## Sources
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again."
- .garura/product/product-os/intents/bi-4.md: "A builder believes its own work, so its opinion isn't evidence."
- .garura/product/product-os/software-delivery-planning/build-work-test-first/capability.md: "Out: checking the code against the project's standards. Check the code against its standards, in Code → Validation, owns it; the build follows the standards while it writes."
- .garura/product/product-os/software-delivery-planning/test-security/fn-test-code-security/feature.md: "It tests the whole of the built work, not only the lines a change added."
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md: "We are never touching production."
- .garura/product/product-os/_spine.yaml, Garura's own product profile: "lint_grounding.py --spine link check + check_ice_workable.py tests", "ready-check and linter tests; spine before/after diff on the rename"
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "everything mechanically through a per-tool runner family", "An unmeasured bar is not a passed bar."
- core/components/plays/validate-epic/reference/ice.md: "Green is the entry condition, never the verdict"
- core/components/agents/quality-auditor.md: "Independently verifies code quality standards: linting, unit tests, type checking, build, and project-defined quality vision gates."
- core/components/skills/check-quality-gates/SKILL.md: "never a silent pass"
- knowledge/technology/validation-floor-profile-benchmarks.md, in Phoenix memory: "The NUMBERS live in the product profile, per product — never in this KB."
- .garura/project/issues/1021/context/names.md: "/validate-slice (was /validate-epic)"
