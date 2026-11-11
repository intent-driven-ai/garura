# Feature: Test the built code, its settings and its libraries for security weaknesses

## What it does
Once a piece of work is built and the record of the build's separate test run shows every test passing, this feature tests the whole built code at rest, by a part that is not the builder, against the product profile's security level, so the product owner knows whether the code meets that level before it runs.
- It tests three things in the built work:
  - the code the project wrote, for weaknesses in how it is written, such as a database query built from what a person typed;
  - the libraries the code uses, for versions with a known weakness;
  - the code, its settings files and the records of the build, for any secret's value, such as a password or a key.
- It tests the whole of the built work, not only the lines a change added. Check the code against its standards already matches the review's security rules against the lines of each change; this feature takes that record as evidence and does not match the same rules again.
- Each result is compared with the pass bar and with each capability's security need. A weakness the pass bar does not allow is a finding even when the tool's own check passes, and a part of the pass bar that no test of the code can measure is named as not tested, never as passed.
- Which tests run, and with which tools, comes from memory first: the project's own code and memory, such as the tools its settings already name, then Garura memory, then Phoenix memory. When none of them answers what a part of the pass bar asks, the part is named as not tested, and a memory update is raised for a person to approve.
- Each finding names the weakness, where it is, and the part of the pass bar or the security need it breaks. For a secret, it names only where the value was found, never the value.
- It runs on a copy of the built code where the deployment design places the tests, never on a builder's own machine, and nothing that builds the work sees its results.
- How it meets the capability: this is the test of the code at rest that the old slice check ran as "static analysis, lint, dependency scans", now against the profile's security level and for the whole built work.

Status: not built. What exists covers only part of it:
- The review of each change matches the review's security rules against the lines a change adds, with "No LLM judgment.", and a finding of the most serious rank rejects the change. It is live, and it belongs to Check the code against its standards. It reads names and words and runs no scan: its rule for the libraries asks for "file, cve-list", a list of known weaknesses, but matches only the name of the file that lists them. Three of its defects are open: #438, #890 and #535; by #890, scripts in plays and skills are classed as prose, "so code rules never check them".
- The old slice check, /validate-epic, is stale. It ran "static analysis, lint, dependency scans" through a family of tool runners, compared the results with the profile's bars, and held that "An unmeasured bar is not a passed bar."
- The quality auditor, an agent, can "Run dependency vulnerability scan" and "Run SAST scan", a static security scan, when a check asks for them; only the stale plays ask.
- No memory tier holds what a security test of code must cover.

## Inputs / Outputs
- In: a copy of the built code, its settings files and the records of the build.
- In: the libraries the code uses, with their versions, from the project's own files.
- In: the product profile's security level and pass bar, and each capability's security need, from the product model.
- In: the security tools and settings the project already names, and memory's answers for the project's kind of product.
- In: the record of the review of each change, and the record of the build's separate test run.
- Out: a result for each part of the pass bar and each security need that a test of the code measures, and each part not tested, with its reason.
- Out: each weakness as a finding, with where it is and what it breaks, for Give the security verdict, and send each finding to the developer or to a person (fn-send-security-findings).

## Rules & behavior
- The whole built work, not only the change. The reason: the review looks only at the lines each change adds, and the review's own scan is for changes only: "Use only from check-change play; never invoke standalone for full-repo audits."
- The review's rules are not matched again. The reason: reviewing a change against its standards is Check the code against its standards' work by the approved list, and BI-4 takes records as evidence "and does not run the same tests again."
- A tool's own pass is not the verdict. The reason: "Green is the entry condition, never the verdict".
- Not tested is never passed. The reason: "An unmeasured bar is not a passed bar."
- No secret's value in any finding, result or log, only where it was found. The reason: people and agents read these records, "so a secret written there is no longer secret.", and the review's own rule for a secret asks for a "redacted-snippet".
- Not the builder, and never seen by the builder. The test runs on a copy, never on a builder's own machine. The reason: "A builder believes its own work, so its opinion isn't evidence.", and with "security scan results", "giving it to the builder only invites teaching-to-the-test."
- Memory first, and no tool or number is a rule here. The reason: the bar is set per product, as memory's own learning says: "The NUMBERS live in the product profile, per product — never in this KB."
- Not decided: what a test of the code must cover for a pass bar that names a security standard. No memory tier holds it, so it waits for research that a person approves as a memory update.
- Not decided: where the test runs while no testing environment and no deployment design exist, as today.
- Not decided: the rank given to each finding, while #934, one severity from P1 to P4 for findings and defects, is open.

## Acceptance criteria
- Given built code that uses one library version with a known weakness that the pass bar does not allow, when the test runs, then a finding names the library, its version and where the code uses it.
- Given a settings file that holds a key's value, when the test runs, then a finding names the file and the line, and no finding, result or log holds the value.
- Given a tool that exits clean while its result breaks the pass bar, when the result is compared, then it is a finding.
- Given a part of the pass bar that no test of the code can measure, when the test ends, then the part is named as not tested with its reason, and not as passed.
- Given a run of this feature, when its record is read, then it ran on a copy and not on a builder's own machine, and no part that builds the work was given its results.

## Out of scope
- The review of each change against its standards, with the review's security rules. Check the code against its standards does it.
- The tests inside the code. Build the work test first's separate check runs them.
- Testing the running build. Test the running build for security in the testing environment (fn-test-running-security) does it.
- Giving the verdict and sending each finding back. Give the security verdict, and send each finding to the developer or to a person (fn-send-security-findings) does it.
- Fixing a weakness, such as moving to a library version without it. Build the work test first does it before the work is accepted, and Fix defects test first after.
- Keeping a secret's value out of each commit. Ship every change the same way, in Developer tooling, does it.

## Sources
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "Test security, against the product profile's security level.", "reviewing a change against its standards is BI-4's", "BI-4 takes the record of BI-3's separate test run as evidence and does not run the same tests again."
- .garura/product/product-os/intents/bi-4.md: "A builder believes its own work, so its opinion isn't evidence."
- standards/rules/pr.md, in Phoenix memory: "No LLM judgment.", "file, cve-list", "redacted-snippet"
- core/components/plays/check-change/SKILL.md: "if any P1 finding (or a runnable suite is red)"
- core/components/skills/check-pr-quality/SKILL.md: "Use only from check-change play; never invoke standalone for full-repo audits."
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "static analysis, lint, dependency scans", "An unmeasured bar is not a passed bar."
- core/components/plays/validate-epic/reference/ice.md: "Green is the entry condition, never the verdict"
- core/components/agents/quality-auditor.md: "Run dependency vulnerability scan", "Run SAST scan"
- core/components/skills/check-quality/SKILL.md: "security/owasp-secure-coding.md"
- knowledge/technology/validation-floor-profile-benchmarks.md, in Phoenix memory: "The NUMBERS live in the product profile, per product — never in this KB."
- docs/philosophy/idd-principles.md: "security scan results", "giving it to the builder only invites teaching-to-the-test."
- .garura/product/product-os/software-delivery-planning/deployment-design/capability.md: "so a secret written there is no longer secret.", "This capability says which tests run in which environment and what a change must pass to move on."
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md: "is not where the path's tests are counted"
- core/components/plays/commit-change/SKILL.md: "C6's guarantee is unchanged: actual secrets never commit."
- GitHub #438 (open): "review-change rejects planning docs and skill prose as P1 security defects"
- GitHub #890 (open): "the review's path table treats scripts in plays and skills as prose, so code rules never check them"
- GitHub #535 (open): "has no model of what the project is, so Garura's own scripts are never code-checked"
- GitHub #934 (open): "Findings and defects get one severity, P1 to P4"
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
