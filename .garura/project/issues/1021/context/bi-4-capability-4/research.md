# Test accessibility: research and drafts (issue 1021, BI-4 capability 4)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-4-capability-4/drafts/product-os/software-delivery-planning/test-accessibility/`: the capability page and its ICE page, and four feature pages, each with its ICE page. All five ICE pages carry the thin mark, because no part of this capability is built.

In one line: Garura can hold an accessibility level for a product and has never tested a product against one. Garura's own profile sets no accessibility level, no capability in its model has an accessibility need, and no surface is declared, so no surface has an accessibility guideline yet. The old slice check, /validate-epic, ran page audits (lighthouse, pa11y, axe) on a local page, read the accessibility score and an error count, compared them with targets written for the slice, and is stale. The review of each change has accessibility rows, but they match words on the lines a change adds, rank as minor, and belong to capability 6. Nothing uses a built product with a keyboard alone or a screen reader. Memory holds one learning on accessibility, written for browser pages, and nothing on how to test a mobile app, a command line or a coding agent's surface.

What this run did besides reading:
- It copied the memory files it decided from into `bi-4-capability-4/memory/`, with `manifest.json`, all from Phoenix memory: the accessibility learning, the product profile schema, the spine schema, the ICE schema, the ontology, the recovery rule (expectation generation), the builder isolation rule, the surface rule (surface contract), the review's severity table (`standards/rules/pr.md`), the rules for features and for design, the screen page schema of the retired design pipeline, the quality check cards schema and the quality and UX shapes of the old slice design, the marketing and UX page templates, the eval index, the note that the profile floor is the bar, the note on one-shot cleanliness, the notes on forms, on responsive layout and on a component library, and the user management, payments and e-commerce shelves.
- It read Garura memory through the memory tool: the spine's product profile (no accessibility level), the spine and every page of the model for an accessibility need (none), and the approved Manage surfaces pages for what a surface's accessibility guideline is.
- It searched every tier for accessibility, a11y, WCAG, screen readers, keyboards, contrast, the page-audit tools and assistive use, and for an accessibility standards shelf (`**/quality/frontend/**`, `**/accessibility-performance.md`): no tier holds one.
- It searched open GitHub issues for accessibility, a11y, WCAG, screen reader, keyboard, axe, lighthouse, pa11y and contrast: none is about testing a product's accessibility. It read #222 (closed, not planned), and #934 for the line on severity (all read only).
- It ran no placement: the domain (software delivery planning) was decided. It did no web research, so no memory update is raised.
- The decisions made from memory are in `cite-request.json`, for the caller to record with `memory.py cite` (the tool writes outside this run's folder).
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## The name

Kept: "Test accessibility". Folder: `test-accessibility`.
- It is the agreed name, and it sits beside "Test security" and "Test performance", which follow the same pattern; the profile's own word is accessibility.
- The list's longer line, "Test accessibility, against the product profile's accessibility level and each surface's accessibility guideline", is the first line of the page's intent, so the two yardsticks are the first thing a reader sees.
- A plainer name, Test that everyone can use it, was weighed: plainer for a business reader, but it drops the profile's word and reads close to capability 5, the user experience on each surface.

## What is built, and what is only planned

Built and live:
- **The product profile can hold an accessibility level.** The schema: `accessibility:  { level: string, gate: string }  # e.g. high, "WCAG 2.1 AA"`, on the scale "none < low < medium < high < xhigh", where the gate is "(the standard / how it's measured)". A part's own needs include `accessibility: string`. Specify the product sets each capability's need with "a target someone can measure and how it is checked", and rolls it up into the profile.
- **Garura's own profile sets no accessibility level.** It holds reliability, maintainability and security, each at medium, no capability has an accessibility need, and its one slice is on "the Claude Code command line". So, today, Garura would have nothing to test itself against here.
- **The review of each change** (/check-change, with the quality auditor running check-pr-quality) has accessibility rows in the severity table: FE-01 to FE-05 at P3 match words on the lines a change adds (a picture with no `alt`, a button, a link or a click handler in a component file, a colour written as a code, `role=` or `aria-`, a click on a plain block), and FE-10 at P4 notes a change to a build workflow file. P3 is "Highlights without blocking. Missing docs, borderline complexity, accessibility, naming.", with "No LLM judgment." Nothing renders a page or uses one. It belongs to capability 6 by the approved list.
- **Manage surfaces (approved, not built)** gives a browser surface the guideline of "meeting the accessibility level the product commits to"; "A guideline meets the levels the profile commits to, such as an accessibility level, and never changes them."; a guideline that asks for less "is named as below the profile, and the profile's level stands."; and a raised level proposes "the accessibility guideline of each surface it touches" at the new level. For a coding agent, its example guidelines are how it asks a person and reports back, with nothing on accessibility.

Built but stale or unused:
- **/validate-epic** (agreed new name /validate-slice), stale (#855). Its frontend runner is a "frontend audit tool class (lighthouse, pa11y, axe).", with "Code-level + local-page audits only (C5)." It read every category score of a page audit, the accessibility score among them, and the count of errors pa11y printed, and its benchmark check compared each with the slice's measure page: a target with a number was compared, and "where the target is prose-only, the metric is presence-required." The measure page was dropped with the agreed names. It had nothing for a keyboard alone or a screen reader, and its surface check for a browser page only opens each page and sees it render.
- **quality-auditor** (agent, live): "Run Lighthouse audits (if threshold defined and URL provided)"; only the stale plays ask it to.
- **check-quality-gates** (skill, built; no live play runs it, only a loop's stop condition names its output). It runs each quality check a slice's design wrote down, and gives "pass | fail | error | missing-tool | human": "A card whose demanded tooling is absent is a missing-tool FINDING", and "Human-owned cards are visibly skipped, never judged." Its test examples include an accessibility check, "WCAG 2.1 AA automated checks clean", run by axe-core. Its schema in Phoenix memory keeps judgment for a person: "Design, UX, and security judgment are never runner-owned:", "they carry owner: human and the runner skips them VISIBLY", with the example "HITL walk at /launch; fresh-context reviewer on the PR". Nothing records what that person found.
- **check-quality** (skill, built, never used): a scored audit with an accessibility level from 1 to 5 and frontend items with fixed numbers for contrast and page speed, reading `frontend/accessibility-performance.md`, which is in no memory tier. Its numbers have no source a page could quote, and "The NUMBERS live in the product profile, per product — never in this KB." The pages quote none of them.
- **The old slice design** (stale): the UX shape left accessibility out, "it lives in the marketing lens", and the marketing page set a bar for each slice, "accessibility (moved here from the profile)", with a gold example "Verified by an automated accessibility pass on the rendered view". The agreed names dropped that play ("Dropped: /shape-marketing-lens, /shape-measure-lens."). The approved list now puts the yardstick in the profile and on each surface.
- **The retired design pipeline's rules**, still in Phoenix memory: "Every Interactive Screen Declares a WCAG Level", "A screen without an accessibility section is assumed inaccessible.", with screen lines such as "Keyboard navigation through all form fields" and "Screen reader announcements for validation errors". The approved Design the work does not carry an accessibility section.
- **walk-prototype** (skill, live, for /discover-intent): an agent walks a prototype in a browser, "click, type, press a key, go back". It does not test accessibility; it shows that an agent can already press keys in a browser.

Planned only:
- "Test accessibility, against the product profile's accessibility level and each surface's accessibility guideline. New." It was on no earlier list.
- No play name: the agreed names hold "/validate-perf (new)" and "/validate-security (new)", and none for accessibility.
- Each surface's accessibility guideline (Manage surfaces), the testing environment (Environment setup) and which tests run where (Deployment design): approved, not built.
- #222, "NFR validation: Accessibility audit (axe, lighthouse a11y)", is closed as not planned ("Deferring — will pick up from features backlog when the time is right."). It is history, not a source for a feature.
- One severity scale for findings and defects, #934 (open), with a layer for each kind of surface.

What memory holds, and does not:
- One learning on accessibility, `knowledge/technology/ux-accessibility-floor.md`, for "surface: any-public-ui", "Any public or user-facing UI." It recommends a named grade of the standard, keyboard-first use, semantic markup, focus management and respect for a person's settings, and to test with "automated checks (axe) in CI plus a manual keyboard + screen-reader pass on key flows." When a law or a contract asks for more, it says to "raise the profile's a11y bar for that product". This is memory's current answer. The pages do not write it as a rule: it is what Manage surfaces would read to propose a browser surface's accessibility guideline, and it is the source for the split between tools and a person.
- Domain shelves tie accessible screens to the web and mobile: "WCAG 2.1 AA on every auth screen" when the surfaces include web or mobile, and "keyboard, labels, contrast on every pay screen".
- The note on profile floors names "performance and accessibility" audits among the checks it applies to; the numbers live in the profile.
- The note on one-shot cleanliness lists "accessibility checks" and says "These are tools, not judgment — they either pass or they don't." That differs from the accessibility learning, which asks for a person's pass too. The pages follow the approved rule that a tool's own pass is not the verdict, and do not write either note as a rule.
- The note on a component library sets numbers for one stack; the pages quote none of them.
- No tier says what a named standard asks of a test part by part, which parts a tool can check and which only a person can, how to test a mobile app, a command line or a coding agent's surface for accessibility, or which screen readers a walk uses. No tier has a shelf of accessibility standards.
- The BI-4 stock-take has no line on accessibility.

Not part of this capability, named so the line is clear:
- Layout across screen sizes, the design system, and the screen design from Design the work: capability 5.
- The review's accessibility rows on each change: capability 6.
- An accessibility line in a story's expectations: the slice's eval, capability 1.
- Users who test the product and accept it: "User acceptance testing (planned): Users test the product and accept it.", in Validation → Run.

## The open points, each with options and a lean

None of these is decided here. Where a lean rests on what is built or on approved pages, the drafts follow it; the rest is named as not decided on the pages. The settled rules of BI-4 (in the testing environment only; the yardstick read, never set; not tested is never passed; a tool's own score is not the verdict; no level set is said plainly; the builder knows the level and the guidelines and gets only a handoff plan; who gets a finding; records taken as evidence; rounds a project setting; only an approved decision moves a level; a tool is not a capability) are not reopened.

### 1. The yardstick, and which wins when the profile and a surface differ

What holds: the list tests "against the product profile's accessibility level and each surface's accessibility guideline"; the profile holds a level and a gate, "(the standard / how it's measured)"; a part's own need can hold accessibility; Manage surfaces (approved) says a guideline "never changes" the levels, and one that asks for less is "named as below the profile, and the profile's level stands."

1. **Both, with the profile's level as the floor.** Each part of the pass bar, each capability's need and each part of each surface's guideline is answered; a guideline may add what its surface needs; a guideline below the profile is named, the profile's level is tested on that surface, and the gap goes to the product owner, whose way back is an update through Manage surfaces. Gain: follows the approved Manage surfaces rule; no surface can quietly ask for less. Cost: two yardsticks to read on each surface.
2. **The profile only; the guideline only says how it is met on its surface.** Gain: one yardstick. Cost: drops the list's second yardstick, and a surface's own needs, such as those of a phone, are not tested.
3. **The guideline only, as the profile's level turned into rules for that surface.** Gain: one concrete list for each surface. Cost: a surface with no guideline, as today, gets no test at all, and a guideline below the profile would pass.

Lean: 1. The drafts follow it.

A part of this point is left open: what a pass bar that names a whole standard, such as "WCAG 2.1 AA", asks of a test, part by part. Options: (a) the surface's guideline lists the parts, proposed from memory's learning for that kind of surface and confirmed by a person, and the verdict answers each listed part; (b) the standard's parts are researched and raised as a memory update for a person to approve, then used by every surface; (c) a tool's own rule set stands for the standard, which the settled rule rules out. Lean: (a), and (b) only when a person asks for the research. The tools feature names it as not decided.

### 2. The line with capability 5, the user experience on each surface

What holds: capability 5 is "Test the user experience on each surface, against the surface's properties and guidelines (for a browser page, how it lays out across screen sizes) and the screen design from Design the work."; this capability is against the accessibility level and each surface's accessibility guideline; a tool is not a capability (settled).

1. **By yardstick.** What the accessibility level, its pass bar, a capability's accessibility need or a surface's accessibility guideline names is tested here, even when it is about layout, such as text that must still read when a person makes it larger. What the surface's other properties and guidelines name, such as how a browser page lays out across screen sizes and the design system, and the screen design, is capability 5's. One tool run or one walk may serve both; each reads only its own yardstick. Gain: the same line the approved pages drew between performance and accessibility for one page audit; no part has two owners. Cost: a person may walk for both at once and must keep two records apart.
2. **By who checks.** Tools here; every person's walk there. Cost: the keyboard and screen reader walk, the heart of accessibility, would leave this capability.
3. **One capability for both.** Cost: against the approved list of six, which keeps them apart.

Lean: 1. The drafts follow it. The screen design, its accessibility notes included, is capability 5's yardstick by the list's own words.

### 3. What a tool can check, what only a person can, and who does the person's part

What holds: memory's learning pairs "automated checks (axe)" with "a manual keyboard + screen-reader pass on key flows"; the quality check runner skips a check a person owns, in view, and never judges it; nothing does the person's part; no persona in the model walks a build; an agent can already press keys in a browser (the prototype walk). No tier says which parts of a standard a tool can check.

1. **Tools for what a tool can check; a person who is not the builder, named by the product owner, walks the slice with a keyboard alone, with a screen reader and in the other ways the guideline names; the pass bar, a need or the guideline says for each part which of the two checks it; a part a person must check that no one walked is not tested.** Gain: matches memory's split and the built handling of a check a person owns; the verdict stays honest. Cost: a person's time in each round; the product owner must name who.
2. **Option 1, but an agent that is not the builder does the keyboard-alone part through a browser, and only the screen reader is a person's.** Gain: less of a person's time. Cost: memory calls the keyboard pass manual; nothing says an agent's walk counts.
3. **Tools only; the person's part is left to user acceptance testing in Validation → Run.** Cost: a pass here would read as tested when the person's part was not, against the settled rule that nothing not tested counts as a pass.

Lean: 1. The drafts follow it; option 2 is named as not decided on the walk feature.

### 4. Which surfaces accessibility applies to, beyond a browser page

What holds: memory's learning holds for "Any public or user-facing UI."; memory's surface rule counts a command line as "a command-line entry point a human runs" and an endpoint as one "a human or integration calls"; the domain shelves tie accessible screens to web and mobile; Manage surfaces gives an accessibility guideline only as an example for a browser surface, and for a coding agent its guidelines are how it asks and reports back; only the command-line step library exists for evals; memory says nothing on testing a mobile app, a command line or a coding agent for accessibility.

1. **Every declared surface a person opens, each against its own guideline; a surface only another system meets, such as an endpoint, is not tested here; a surface whose guideline names nothing for accessibility, or whose kind memory has no way to test, is named as not tested and goes to the product owner.** Gain: no person's surface is skipped quietly; a command line read by a screen reader is not forgotten. Cost: a command line, a coding agent's surface and a mobile app stay not tested until a guideline and a way to test are approved.
2. **Only browser pages and mobile apps, where memory has learnings.** Gain: nothing stays open. Cost: decides from memory's gaps; a person who uses a screen reader with a command-line tool is never served.
3. **Every surface, an endpoint too.** Cost: no memory says what accessibility means for a surface no person sees.

Lean: 1. The drafts follow it. Whether an endpoint a person calls directly counts as a surface a person opens is decided by its declaration in Manage surfaces, which names who opens it.

### 5. The line with capability 6 for accessibility rules on the code

What holds: the approved list gives "reviewing a change against its standards" to capability 6; the review's FE-01 to FE-05 rows match words on added lines and rank as P3; capabilities 2 and 3 drew the same line for security and performance (approved).

1. **Split by yardstick and by what is done.** Capability 6 holds the review of each change with its accessibility rows; this capability tests the running build against the level and the guidelines, by tools and a person's walk, never by matching words, and takes capability 6's record as evidence. Gain: the line already approved twice. Cost: two capabilities look at accessibility, one by reading code, one by using the product.
2. **A test of the code at rest here too**, as Test security tests the code at rest. Cost: no memory names a tool or a rule for it; the review already matches the same words.
3. **All accessibility in one capability**, the review's rows included. Cost: one review with two owners, against the approved line.

Lean: 1. The drafts follow it.

### 6. The persona

What holds (settled with capabilities 1 to 3): the product owner reads the verdict and decides each finding a person must decide; the developer gets each finding the builder can fix alone. The personas in use in the model are the product owner, the developer, the technical lead, the devops engineer and the architect; none walks a build.

1. **The product owner and the developer, as capabilities 1 to 3; the person who walks is named by the product owner, not a persona.** Gain: the same readers for every verdict of Code → Validation; no new persona. Cost: who walks is a name in a setting or a run, not a role the model knows.
2. **A new persona, an accessibility tester, who walks the build.** Gain: the walk has a role. Cost: no approved page uses it.
3. **The people who use the product with a keyboard alone or a screen reader, as the ones it serves.** Gain: names who gains. Cost: they are the product's users, not readers of the verdict; no approved page of Code → Validation serves its product's users directly.

Lean: 1. The drafts follow it.

### 7. What a failure sends back, and to whom

What holds (settled): a handoff plan names what is wrong, where and the way back, never the test, its rule, its id, its tool or the figures; the developer only when the way back is a change of the code the builder controls; the product owner when it changes the architecture, the deployment design, an environment, a surface's declaration or guideline, the design or the level; a person when in doubt.

What the handoff plan says for an accessibility finding:
1. **What a person cannot do, on which surface and screen, in which way (a keyboard alone, a screen reader, larger text), and the way back, in plain words, with no figure.** For example: a shopper using a keyboard alone cannot leave the address field on the checkout page; the keyboard must move on to the next field. Gain: keeps the settled rule; the builder knows the level and the guideline, so plain words are enough to fix. Cost: the builder does not see which part of the standard by its number.
2. **The same, and the part of the standard by its number.** Cost: names the test's rule, against the settled rule.
3. **A symptom only, as for the eval.** Cost: the builder cannot find the screen.

Lean: 1. The drafts follow it. An earlier draft line asked whether a handoff plan may name the part of the standard in plain words; it was taken off the page, because saying what is wrong in plain words already covers it and the line read as reopening the settled rule.

Who gets it, examples drafted under the settled rule: a button with no name a screen reader can read out, or a dialog the keyboard cannot leave, goes to the developer; the colours of the design system that every screen uses (a surface's guideline), the screen design, a part the builder does not control such as a payment form another company shows inside the page, a lower level, a surface whose guideline names nothing, or a part not walked because no person was named, go to the product owner.

### 8. When the profile sets no accessibility level (Garura's own case)

Settled with capability 3: the verdict says so plainly, and is neither a pass nor a fail. The drafts apply it when the profile sets no level, no capability has a need and no guideline names accessibility. When a guideline names accessibility and the profile sets no level, the guideline is tested and the verdict says the profile sets none.

### 9. One testing feature or two

1. **Two: the tools, and a person's walk.** Gain: each has its own who, its own cost and its own record; a product whose guideline names no person's check never needs the walk. Cost: two pages.
2. **One feature that does both.** Gain: shorter. Cost: the rules for a person's time, who walks and the walk's record would mix with every tool check.

Lean: 1. The drafts follow it.

### 10. How often a person walks again

What holds: rounds are a project setting (settled); a walk costs a person's time; the old slice check bounded its re-checks by what changed.

1. **The whole walk each round.** Cost: a person's time in every round.
2. **Only the steps a change could touch, and the whole walk when the level or the guideline changes.** Cost: needs a rule for what a change touches, which is not written.
3. **The walk only once the tools and the slice's eval pass.** Gain: no person's time on a build that fails anyway. Cost: an accessibility failure found late.

No lean; named as not decided on the retest feature, beside the same question for the tools.

### Smaller points, named as not decided on the pages

- What a pass bar that names a whole standard asks of a test, part by part (point 1).
- Whether an agent that is not the builder may do the keyboard-alone part of the walk (point 3).
- Whether the person walks only the slice's steps, or every screen the built work shows.
- Which screen reader, browser or phone the walk uses when the guideline does not name them.
- How the test reaches each surface of the running build: through the slice's usage guide, as the eval does, or through what the deployment design records for each surface.
- Where the tests run while no testing environment and no deployment design exist, as today.
- Where the verdict and the handoff plans are kept, and how a handoff plan reaches the developer.
- The rank of each finding, while #934 is open.
- Which parts run again on each change, and what counts as the same finding coming back (point 10).

## The features found

1. **Test the running build for accessibility with tools, in the testing environment** (fn-test-accessibility-with-tools). Not built; the stale slice check ran page audits on a local page and compared scores with targets; the quality auditor can run a page audit when asked; the quality check runner can run an accessibility tool's check and treats a missing tool as a finding. Sources: item 4 of the approved list; the profile schema ("WCAG 2.1 AA", "(the standard / how it's measured)"); /validate-epic's frontend runner ("frontend audit tool class (lighthouse, pa11y, axe).", "Code-level + local-page audits only (C5).") and its comparison with targets; quality-auditor ("Run Lighthouse audits (if threshold defined and URL provided)"); check-quality-gates and its accessibility example; memory's learning ("automated checks (axe) in CI").
2. **Walk the running build with a keyboard alone and with a screen reader, in the testing environment** (fn-walk-with-keyboard-and-screen-reader). Not built. Sources: memory's learning ("a manual keyboard + screen-reader pass on key flows."); the quality check runner's handling of a check a person owns ("Human-owned cards are visibly skipped, never judged.") and its schema's person-owned example ("HITL walk at /launch; fresh-context reviewer on the PR"); the retired design pipeline's screen lines ("Keyboard navigation through all form fields", "Screen reader announcements for validation errors"); the slice as what "one person can test end to end on one surface".
3. **Give the accessibility verdict, and send each finding to the developer or to a person** (fn-send-accessibility-findings). Not built. Sources: BI-4's proof and must-not; the recovery rule; the ontology's handoff plan rule; /validate-epic's verdict and fix report; the approved Fix defects test first ("a finding in a review"); capability 2's approval of who gets a finding that changes the architecture; capability 3's approval of the verdict when no level is set; Manage surfaces' rule for a guideline below the profile.
4. **Test accessibility again as the product changes** (fn-retest-accessibility). Not built. Sources: /validate-epic's rounds ("Implement ↔ validate is expected to loop — scope narrows per round, 3 rejections halt to a human."); the profile's rule that only an approved decision moves the level; the Settings line; Manage surfaces' update of a guideline at a raised level ("the accessibility guideline of each surface it touches is proposed at the new level."); /loop-code-validation (a name).

Candidates not drafted, and why:
- **Run the review's accessibility rows on each change**: capability 6's, by the approved list (point 5).
- **Check each screen design for its accessibility section**: a rule of the retired design pipeline, about a design, not the built work; Design the work does not carry it.
- **Test the code at rest for accessibility**: no memory names a tool or a rule (point 5).
- **Test how a browser page lays out across screen sizes, and the screen design**: capability 5's (point 2).
- **Raise the accessibility level when a law or a contract asks for more**: Specify the product sets the level; memory's learning says to "raise the profile's a11y bar for that product".
- **Users test the product and accept it**: user acceptance testing, in Validation → Run.
- **An accessibility tester persona**: point 6.

## Thin marks, and why

All five ICE pages open with the thin mark, with at most three Limits and three Fails if each: no part of this capability is built.

## Lines elsewhere that are out of step (not changed here)

- The stale UX shape says accessibility "lives in the marketing lens", and the marketing page says it "moved here from the profile"; that play is dropped, and the approved list puts the yardstick in the profile and on each surface.
- The note on one-shot cleanliness calls accessibility checks "tools, not judgment"; memory's accessibility learning asks for a person's pass as well.
- The scored quality check (unused) carries fixed numbers for contrast and page speed with no standard behind them in any tier.
- The stale slice check ran its page audits on a local page; the drafts allow testing only in the testing environment, as settled.
- The domain page says it "does not run the evals, release the work, or run the product"; this capability runs a copy of the product in the testing environment to test it. As approved, the domain line changes at BI-4's close.
- BI-4's own page lists its first three capabilities among what it touches; this one is added when it is written.

## Assumptions

- Assumed: accessibility tests run in the testing environment that Environment setup declares, never in production and never on a builder's own machine. The list recorded it for "security and performance tests"; the product owner approved the same for the eval and for Test performance.
- Assumed: the person who walks is named by the product owner, for the project or for a run, and is never the builder.
- Assumed: the parts of this capability read the product profile, each capability's accessibility need, each surface's accessibility guideline and the decisions that moved them from the product model, and never write them.
- The examples come from several kinds of product: a shop's checkout page, a clinic's booking page, a school's timetable app for phones, and a team's command-line tool.

## Memory updates

None drafted. Four things no tier answers are named as not decided instead: what a named standard asks of a test part by part, which parts a tool can check and which only a person, how to test a mobile app, a command line or a coding agent's surface for accessibility, and which screen readers a walk uses. This run did no web research, and drafting an answer from the agent's own knowledge would break the rule; a person may ask for the research, and its answer would go to a memory update for approval.

## Checks

- **Structure check** (`lint_grounding.py`): the capability page (`--kind capability --stage directional`) and the four feature pages (`--kind feature`): ok, no errors, no warnings, on the first run and after every edit.
- **ICE shape check** (a small script in the session's scratch folder): each of the five ICE pages opens with the thin mark, holds Intent, Context and Expectation in that order, exactly one Goal, one to three Limits and one to three Fails if, the fixed Read line, the Context labels in order (Read, Never read, Persona, Scope), a Scenario, and a Done means checked by someone other than the doer. No part page holds an ICE section, and each has its ICE page beside it. Outside quotes and source paths, no page says lens, seed, lock or gate, or names a real person, a home folder, a temp folder, a particular plan or a business intent's number. Run once on a copy with five planted errors (no thin mark, four Limits, a Done means by the doer, an ICE section on a part page, a forbidden word); it named all five.
- **Quotes** (a second small script): all 231 quotes on the ten pages are found word for word (spaces joined; markdown marks and YAML's doubled apostrophes read as one) in its file: each quote in a Sources line in that line's own file, and each quote in a page body or its ICE page in a file that page's Sources name. Memory quotes are checked against this run's copies in `memory/`, the product owner's words against `page-approvals.md` and `capabilities.md`, GitHub quotes against the issue texts read today. One quote of his was tidied for spelling only ("seecurity" to "security", "assessibility" to "accessibility"), and its Sources line says so. Run once on a copy with three planted errors (a changed word, the right words in the wrong file, a made-up quote); it named all three. The 89 quotes in this file were checked the same way against every file read; all are found.
- **Not decided lines against the approvals**: each "Not decided" line on the pages was read against the approval records of capabilities 1 to 3 and the list of six. One line, whether a handoff plan may name the part of the standard it breaks, read as reopening the settled handoff rule and was taken off the page (point 7). The rest do not reopen a settled rule; they are new to accessibility (a pass bar that names a whole standard, an agent's keyboard walk, which screens a person walks, which screen reader) or the same as the earlier capabilities left open (how a surface is reached, where the tests run today, where the verdict is kept, the rank of a finding, which tests run again, the same finding).
