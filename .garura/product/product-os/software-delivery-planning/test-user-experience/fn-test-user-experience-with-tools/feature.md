# Feature: Test the running build's user experience with tools, in the testing environment

## What it does
Once the built work runs in the testing environment, this feature opens on each declared surface, by a part that is not the builder, each screen the screen design shows at each screen size the surface names, keeps a picture of it with the text and the controls it shows, checks what a tool can check, and records each result with what was checked and where, so the person who walks has the evidence beside them and the product owner knows which parts a tool found met.
- What it opens, and at which sizes, comes only from the surface's properties and guidelines and from the screen design in force. A surface is a place where a person, or another system, opens the product to use it; Manage surfaces declares its properties, such as the screen sizes it serves, and its guidelines, such as working within the project's design system. For example:
  - a shop's checkout page, whose browser surface reflows one layout across a phone, a tablet and a desktop screen size: each checkout screen is opened and pictured at the three sizes;
  - a clinic's booking page, whose screen design is a prototype built with the clinic's design system: the build and the prototype are walked with the same steps and pictured at the same sizes, so the person who walks can set them side by side;
  - a school's timetable app, whose surface gives phones and tablets a layout of their own: each layout is opened on the sizes of its own device;
  - a team's release command, or a coding agent's play that a person runs in a terminal: it is run in a test project with set answers, and what it printed and each question it asked are kept.
- What a tool checks needs no judgment: that each screen the screen design shows opens and shows at each size, that a command or a play runs to its end, and what a surface's guideline says a tool checks. Whether a screen lays out as its surface says, keeps to the design system and matches its screen design is left to the person's walk, never passed by a tool.
- Which tools it uses comes from the project's own settings and code first, then from memory. A screen, a size or a kind of surface that no known tool can open is named as not tested, never as passed.
- One run of a tool may also give what Test accessibility or Test performance reads, such as whether a field has a label or how fast a page shows. This feature keeps only what its own yardstick names.
- It reaches the running build only on its declared surfaces, with the testing environment's made-up data and its own test accounts. A test that needs a secret, such as a test account's password, takes it at run time from where the deployment design keeps the testing environment's secrets, and writes its value nowhere.
- Each run records which screen it opened, on which surface, at which size, with which tool, and what it found, so a second run on the same built work can repeat it.
- A screen a tool could not reach, a size it could not open, and a tool that could not run are named as not tested, each with its reason.
- The pictures and the results go to the person who walks and to the verdict, never to a part that builds the work.
- How it meets the capability: the approved list tests the user experience "against the surface's properties and guidelines (for a browser page, how it lays out across screen sizes)". This feature is the part of that test a tool can do, on the running product, in the testing environment, and it gathers what the person judges from.

Status: not built. What exists covers only part of it:
- The prototype capture and the prototype walk, built for Specify the product, open a page in a browser and keep a full-page picture of it with its visible text; the walk also keeps the controls and fields on screen after each step. Both open the page at one screen size fixed in their code, 1280 by 900, and neither opens a built product or runs in a testing environment.
- The old slice check, /validate-epic, is stale. For a browser surface it planned "a browser open of each `must_open`", to see each page show; it named no screen size and compared nothing with a design.
- For a command line, and for a coding agent's play, the eval's step library says a runner "starts the play as a command in the test project and gives it the scripted answers"; the runner is not built.
- The quality-check runner, a skill that runs each quality check written down for a slice, is built and no live play runs it. A check whose tool is missing is a finding, never a pass.
- No surface is declared and no screen design is written, so nothing names the screens or the sizes to open.
- No testing environment is declared or built, because Environment setup is not built.

## Inputs / Outputs
- In: the declared surfaces, who opens each, each one's properties, such as the screen sizes it serves, and its guidelines, and how each is reached in the testing environment.
- In: the screen design in force for the work, with the screens it shows and the screen design setting, wireframes or a prototype.
- In: the testing environment, as Environment setup declares and builds it, with its made-up data and its test accounts.
- In: where the deployment design keeps the testing environment's secrets, and which tests it places there.
- In: the tools the project's settings and code already name.
- Out: for each screen at each size, a picture with the text and the controls it shows, and for a command or a play, what it printed and asked, for Walk the running build against its surface and its screen design, in the testing environment (fn-walk-against-screen-design).
- Out: for each part a tool checks, the result, a pass or a fail, with the surface, the screen, the size and the tool; and each part not tested, with its reason, for Give the user experience verdict, and send each finding to the developer or to a person (fn-send-user-experience-findings).

## Rules & behavior
- In the testing environment only. The reason, in the product owner's words: "We are never touching production."; and a builder's machine "is not where the path's tests are counted".
- What to open, at which sizes and what to check comes from the surface's declaration and the screen design, never from what the AI agent knows by itself and never straight from a learning in memory. The reason: the surface's properties include "which screen sizes (viewports) it serves", and "A person confirms each surface, property and guideline".
- A tool gathers, and checks only what needs no judgment. The reason: as built, the quality-check runner never judges a check a person owns, "Human-owned cards are visibly skipped, never judged.", and its own example of one is "Layout matches the approved UX direction".
- A tool's own score is not the verdict. The reason: "Green is the entry condition, never the verdict".
- Not tested is never passed. The reason: "An unmeasured bar is not a passed bar.", and "a check that didn't run is NEVER a check that passed."
- Only what this yardstick names is kept. The reason: a tool is not a capability, and the approved Test accessibility page reads "One run of a tool, or one walk by a person, may serve both; each capability reads only what its own yardstick names."
- Made-up data, test accounts, and secrets at run time, never written. The reason: each environment holds "made-up records written for the tests", and "The design names only where each secret is kept."
- A part that is not the builder runs the tools, and the builder never sees the pictures or the results. The reason: a result checked after the work exists is a failure condition, and "giving it to the builder only invites teaching-to-the-test."
- Not decided: which browsers and phones, or stand-ins for them, the tools use when the surface names none.
- Not decided: how the test reaches each surface of the running build: through the slice's usage guide, as the eval does, or through what the deployment design records for each surface.
- Not decided: where the test runs while no testing environment is declared, as today.

## Acceptance criteria
- Given a browser surface that names a phone, a tablet and a desktop screen size, when the tools run in the testing environment, then each screen the screen design shows is opened and pictured at each of the three, with the surface, the screen, the size and the tool recorded, and nothing outside the testing environment is reached.
- Given a screen that does not open at one of the sizes, when the run ends, then that part fails, with the screen and the size.
- Given a part that a person must judge, such as whether the screen matches its wireframe, when the tools run clean, then the part is not counted as passed.
- Given a surface that names no screen size, when the tools run, then its layout is named as not tested, with its reason.
- Given a coding agent's play, when the tools run, then the play runs in a test project with the set answers, and what it printed and each question it asked are kept for the walk.
- Given two runs on the same built work, when their records are read, then they name the same screens and sizes, and each part has the same pass or fail.
- Given the pictures and the results, when the inputs of the parts that build the work are checked, then none of them names them.

## Out of scope
- Judging each screen against the surface and the screen design. Walk the running build against its surface and its screen design, in the testing environment (fn-walk-against-screen-design) does it.
- Giving the verdict and sending each finding back. Give the user experience verdict, and send each finding to the developer or to a person (fn-send-user-experience-findings) does it.
- What the product does against each story. The slice's eval tests it, in Test what the product does, with evals the builder never sees.
- What a surface's accessibility guideline or the accessibility level names. Test accessibility checks it.
- The review's rules on the lines each change adds. Check the code against its standards owns them.
- Declaring and building the testing environment, its data and its test accounts. Environment setup does it.

## Sources
- The list the product owner approved on 2026-11-09, in .garura/project/issues/1021/context/capabilities.md: "Test the user experience on each surface, against the surface's properties and guidelines (for a browser page, how it lays out across screen sizes) and the screen design from Design the work.", "Assumed: security and performance tests run in the testing environment Environment setup declares, never in production."
- The product owner on 2026-11-07, in .garura/project/issues/1021/context/bi-4-capability-5/page-approvals.md: "We are never touching production."
- .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "A surface is a place where a person, or another system, opens the product to use it.", "which screen sizes (viewports) it serves", "A person confirms each surface, property and guideline"
- .garura/product/product-os/software-delivery-planning/design-work/capability.md: "The screen design setting decides whether each screen is shown as wireframes in Markdown files or as a prototype built with the project's design system."
- .garura/product/product-os/software-delivery-planning/test-accessibility/capability.md: "One run of a tool, or one walk by a person, may serve both; each capability reads only what its own yardstick names."
- .garura/product/product-os/software-delivery-planning/test-product-with-evals/fn-run-slice-eval/feature.md: "A command-line slice, a play too, runs in a test project there."
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md: "is not where the path's tests are counted", "made-up records written for the tests"
- .garura/product/product-os/software-delivery-planning/deployment-design/capability.md: "The design names only where each secret is kept.", "This capability says which tests run in which environment and what a change must pass to move on."
- .garura/product/product-os/software-delivery-planning/build-work-test-first/fn-write-usage-guide/feature.md: "Matching each name in the eval to the guide, running the eval, and giving the verdict."
- core/components/plays/discover-intent/scripts/walk_prototype.py: "the controls and fields the person could use next"; the line that opens its browser page sets one screen size, 1280 by 900, and capture_source.py sets the same.
- core/components/plays/discover-intent/scripts/capture_source.py: "full-page screenshot(s) + the page HTML, via a headless browser"
- core/components/plays/validate-epic/SKILL.md: "waits for the rebuild of the execute loop on the plan and eval plays (#855, ADR 049)", "a browser open of each `must_open`", "An unmeasured bar is not a passed bar."
- core/components/plays/validate-epic/reference/ice.md: "Green is the entry condition, never the verdict"
- core/components/plays/validate-epic/scripts/runners/_runner_common.py: "a check that didn't run is NEVER a check that passed."
- core/components/skills/check-quality-gates/SKILL.md: "Human-owned cards are visibly skipped, never judged.", "A card whose demanded tooling is absent is a missing-tool FINDING"
- core/components/skills/check-quality-gates/fixtures/brownfield/quality-gates.yaml: "Layout matches the approved UX direction"
- standards/schemas/eval/steps-command-line.yaml, in Phoenix memory: "the runner starts the play as a command in the test project and gives it the scripted answers"
- standards/schemas/eval/_index.md, in Phoenix memory: "A library for the browser page, the mobile app and the backend endpoint is added when a slice first needs it."
- docs/philosophy/idd-principles.md: "giving it to the builder only invites teaching-to-the-test."
- core/tools/memory/GUIDE.md: "Do not guess. Draft the answer as a memory update, and a person approves or rejects it:"
