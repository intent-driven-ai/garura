# Feature: Test the running build for accessibility with tools, in the testing environment

## What it does
Once the built work runs in the testing environment, this feature runs on each declared surface a person opens, by a part that is not the builder, the tools that check what the pass bar, each capability's accessibility need and the surface's accessibility guideline say a tool checks, and records each result with what was checked and where, so the product owner knows which parts of the accessibility level a tool found met.
- What it checks comes only from the pass bar, each capability's accessibility need and the surface's accessibility guideline, each of which says for each part whether a tool checks it. For example:
  - a shop's checkout page, whose browser guideline says a tool checks that each field has a label a screen reader can read out and that text stands out from its background;
  - a clinic's booking page: that no information is shown by colour alone, such as a free slot marked only in green;
  - a school's timetable app for phones: what the app's guideline says a tool checks, such as a name on each button that the phone's screen reader can read out;
  - a team's command-line tool: what its guideline says a tool checks; a command line whose guideline names nothing for accessibility is named as not tested.
- Which tools it uses comes from the project's own settings and code first, then from memory. A part for which no tool is known is named as not tested, never as passed.
- Each result is compared with its part of the pass bar, the need or the guideline. A tool's own score counts only when the pass bar names that score. A clean run of a tool says nothing of a part that the pass bar, a need or the guideline says a person checks.
- One run of a page-audit tool may also give a speed figure. This feature keeps only what the accessibility pass bar, the needs and the guidelines name.
- It reaches the running build only on its declared surfaces, with the testing environment's made-up data and its own test accounts. A test that needs a secret, such as a test account's password, takes it at run time from where the deployment design keeps the testing environment's secrets, and writes its value nowhere.
- Each run records what it checked, on which surface and screen, with which tool, so a second run on the same built work can repeat it.
- A part a tool could not reach, such as a screen behind a step the test could not do, and a tool that could not run are named as not tested, each with its reason.
- How it meets the capability: the approved list tests accessibility "against the product profile's accessibility level and each surface's accessibility guideline." This feature is the part of that test a tool can do, on the running product, in the testing environment.

Status: not built. What exists covers only part of it:
- The old slice check, /validate-epic, is stale. Its page-audit runner, a "frontend audit tool class (lighthouse, pa11y, axe).", ran only on a local page, "Code-level + local-page audits only (C5).", read every score a page audit gave, an accessibility score among them, and the count of errors an accessibility tool printed, and compared each with a target written for the slice. A target with no number was only checked to be there.
- The quality auditor, an agent, can "Run Lighthouse audits (if threshold defined and URL provided)" when a check asks; only the stale plays ask.
- The quality-check runner, a skill that runs each quality check written down for a slice, is built and no live play runs it. A check whose tool is missing is a finding, never a pass, and its test examples name an accessibility tool.
- Nothing checks a mobile app, a command line or a coding agent's surface for accessibility.
- Garura's own profile sets no accessibility level, no capability in its model has an accessibility need, and no surface is declared, so no surface has an accessibility guideline.
- No testing environment is declared or built, because Environment setup is not built.

## Inputs / Outputs
- In: the product profile's accessibility level and pass bar with how it is checked, and each capability's accessibility need.
- In: the declared surfaces, who opens each, each one's accessibility guideline, and how each is reached in the testing environment.
- In: the testing environment, as Environment setup declares and builds it, with its made-up data and its test accounts.
- In: where the deployment design keeps the testing environment's secrets, and which tests it places there.
- In: the tools the project's settings and code already name.
- Out: for each part a tool checks, the result, a pass or a fail, and the surface, the screen and the tool; and each part not tested, with its reason, for Give the accessibility verdict, and send each finding to the developer or to a person (fn-send-accessibility-findings).

## Rules & behavior
- In the testing environment only. The reason, in the product owner's words: "We are never touching production."; and a builder's machine "is not where the path's tests are counted", where the old runner's local page ran.
- What to check, and that a tool checks it, comes from the pass bar, the needs and the guideline, never from what the AI agent knows by itself. The reason: "The NUMBERS live in the product profile, per product — never in this KB.", and the pass bar is "(the standard / how it's measured)".
- A tool's own score is not the verdict. The reason: "Green is the entry condition, never the verdict".
- Not tested is never passed. The reason: "An unmeasured bar is not a passed bar.", and "a check that didn't run is NEVER a check that passed."
- A tool's clean run never passes a part a person must check. The reason: the quality-check runner skips a check a person owns, "Human-owned cards are visibly skipped, never judged."
- Only the accessibility results. The reason: a tool is not a capability, and the approved Test performance page gives the speed figure of a page audit to Test performance.
- Made-up data, test accounts, and secrets at run time, never written. The reason: each environment holds "made-up records written for the tests", and "The design names only where each secret is kept."
- A part that is not the builder runs the tools, and the builder never sees the results. The reason: a result checked after the work exists is a failure condition, and "giving it to the builder only invites teaching-to-the-test."
- Not decided: what a pass bar that names a whole standard asks of a tool, part by part, when the surface's guideline does not list the parts. No memory tier holds it.
- Not decided: how the test reaches each surface of the running build: through the slice's usage guide, as the eval does, or through what the deployment design records for each surface.
- Not decided: where the test runs while no testing environment is declared, as today.

## Acceptance criteria
- Given a browser guideline that says a tool checks each field's label, when the tools run in the testing environment, then each field gets a pass or a fail with its screen and the tool, and nothing outside the testing environment is reached.
- Given a page-audit run that gives an accessibility score and a speed score, when the results are recorded, then only what the accessibility pass bar names is kept here, and the score counts only when the pass bar names it.
- Given a part that the guideline says a person checks, when the tools run clean, then the part is not counted as passed.
- Given a command line whose guideline names nothing for accessibility, when the tools run, then the surface is named as not tested, with its reason.
- Given a tool that could not run, when the run ends, then each part it should have checked is named as not tested, and not as passed.
- Given two runs on the same built work, when their records are read, then they name the same checks, and each part has the same pass or fail.

## Out of scope
- Walking the build with a keyboard alone and with a screen reader. Walk the running build with a keyboard alone and with a screen reader, in the testing environment (fn-walk-with-keyboard-and-screen-reader) does it.
- Giving the verdict and sending each finding back. Give the accessibility verdict, and send each finding to the developer or to a person (fn-send-accessibility-findings) does it.
- The review's accessibility rules on the lines each change adds. Check the code against its standards owns them.
- An accessibility line in a story's expectations. The slice's eval tests it, in Test what the product does, with evals the builder never sees.
- How a browser page lays out across screen sizes, and the screen design. Test the user experience on each surface checks them.
- The speed figures of a page audit. Test performance reads them.
- Declaring and building the testing environment, its data and its test accounts. Environment setup does it.

## Sources
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "Test accessibility, against the product profile's accessibility level and each surface's accessibility guideline.", "Assumed: security and performance tests run in the testing environment Environment setup declares, never in production."
- The product owner on 2026-11-07, in .garura/project/issues/1021/context/bi-4-capability-4/page-approvals.md: "We are never touching production."
- standards/schemas/product-os/product-profile.yaml, in Phoenix memory: "WCAG 2.1 AA", "(the standard / how it's measured)"
- .garura/product/product-os/software-delivery-planning/specify-product/fn-specify-capabilities/feature.md: "a target someone can measure and how it is checked"
- .garura/product/product-os/software-delivery-planning/manage-surfaces/fn-declare-surfaces/feature.md: "and meeting the accessibility level the product commits to"
- .garura/product/product-os/_spine.yaml, Garura's own product profile: it holds reliability, maintainability and security, each "level: medium", and no accessibility level.
- knowledge/technology/validation-floor-profile-benchmarks.md, in Phoenix memory: "The NUMBERS live in the product profile, per product — never in this KB."
- knowledge/domains/payments.md, in Phoenix memory, what an accessible screen may need: "keyboard, labels, contrast on every pay screen"
- core/components/plays/validate-epic/scripts/runners/runner_frontend.py: "frontend audit tool class (lighthouse, pa11y, axe).", "Code-level + local-page audits only (C5)."
- core/components/plays/validate-epic/scripts/runners/_runner_common.py: "a check that didn't run is NEVER a check that passed."
- core/components/plays/validate-epic/scripts/check_gates.py: "where the target is prose-only, the metric is presence-required."
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "An unmeasured bar is not a passed bar."
- core/components/plays/validate-epic/reference/ice.md: "Green is the entry condition, never the verdict"
- core/components/agents/quality-auditor.md: "Run Lighthouse audits (if threshold defined and URL provided)"
- core/components/skills/check-quality-gates/SKILL.md: "Human-owned cards are visibly skipped, never judged.", "A card whose demanded tooling is absent is a missing-tool FINDING"
- core/components/skills/check-quality-gates/fixtures/brownfield/quality-gates.yaml: "requires: { tool: axe-core, tool_bins: [axe-bf-fixture-absent] }"
- .garura/product/product-os/software-delivery-planning/test-performance/capability.md: "One run of a page-audit tool may give both a speed figure and an accessibility figure; a tool is not a capability, and the accessibility figure is Test accessibility's."
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md: "is not where the path's tests are counted", "made-up records written for the tests"
- .garura/product/product-os/software-delivery-planning/deployment-design/capability.md: "The design names only where each secret is kept.", "This capability says which tests run in which environment and what a change must pass to move on."
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-write-usage-guide/feature.md: "Matching each name in the eval to the guide, running the eval, and giving the verdict."
- docs/philosophy/idd-principles.md: "giving it to the builder only invites teaching-to-the-test."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
