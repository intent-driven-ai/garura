# Test the user experience on each surface: research and drafts (issue 1021, BI-4 capability 5)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-4-capability-5/drafts/product-os/software-delivery-planning/test-user-experience/`: the capability page and its ICE page, and four feature pages, each with its ICE page. All five ICE pages carry the thin mark, because no part of this capability is built.

In one line: Garura has never tested how a built product looks and lays out on its surface. No surface is declared, so no surface has properties or guidelines; no work has a screen design, because Design the work is not built; and Garura's one slice is on the Claude Code command line. What exists is near it, not on it: the prototype capture and the prototype walk open a page in a browser and keep a full-page picture, its text and its controls, at one fixed screen size, for reading a prototype; the rebuild eval walks a rebuilt product against a prototype and leaves layout out on purpose; the stale slice check only planned to open each page and see it show; and the quality-check runner, built and unused, skips a check a person owns, such as "Layout matches the approved UX direction", and records nothing the person found. Memory holds learnings for browser layouts, the design system, navigation and screen states, and says nothing on how to test a built screen against them, how to compare it with a wireframe or a prototype, or how to test a command line, a mobile app or a coding agent's surface for its user experience.

What this run did besides reading:
- It copied the memory files it decided from into `bi-4-capability-5/memory/`, with `manifest.json`, all from Phoenix memory: the learnings on responsive layout, design tokens and components, screen states, navigation, the component architecture and accessibility; the surface rule (surface contract); the retired design pipeline's rules and its screen page schema; the UX page template and shape of the old slice design; the quality check cards schema; the eval step library index and the command-line step library; the ontology; the recovery rule (expectation generation); the review's severity table (`standards/rules/pr.md`); the builder isolation rule; the user-facing voice rule; and the product profile schema.
- It read Garura memory through the memory tool: the approved pages of Manage surfaces, Design the work, Environment setup, Deployment design, Build the work test first, Fix defects test first and BI-4's first four capabilities; the spine's product profile (no surface, no shape) and slices; and searched it for a design system or design tokens (none, beyond model pages).
- It searched every tier for viewport, breakpoint, screen size, responsive, wireframe, screenshot, visual regression, usability, design system, design token, pixel, prototype, Storybook, Playwright and user experience, and for a frontend quality shelf (`**/quality/frontend/**`) and a design system file (`**/design-system*`): no tier holds either file, and no tier says how to test a built screen's layout or look.
- It read the repo: `core/components/skills/walk-prototype/`, `core/components/plays/discover-intent/scripts/walk_prototype.py` and `capture_source.py`, `core/tools/rebuild-eval/`, the stale `core/components/plays/validate-epic/` and `core/components/plays/shape-ux-lens/` with `core/components/skills/author-ux-lens/`, `core/components/skills/check-quality-gates/` and `check-quality/`, and `core/tools/lint-components/`. Garura's repo holds no design tokens, theme or style sheet of its own.
- It searched open GitHub issues for responsive, viewport, wireframe, design system, layout, screen size, visual, UX, user experience, screenshot, breakpoint, mobile and surface (read only), and read #934, #553, #559 and #561. Only #934 speaks to a user experience finding (its surface layer of severity); #553, #559 and #561 are about declaring surfaces and tracing a slice's outcome, which Manage surfaces and the slice's design own.
- It ran no placement: the domain (software delivery planning) was decided. It did no web research, so no memory update is raised.
- The decisions made from memory are in `cite-request.json`, for the caller to record with `memory.py cite` (the tool writes outside this run's folder).
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## The name

Kept: "Test the user experience on each surface". Folder: `test-user-experience`.
- It is the agreed name, and the approved pages of Test what the product does, Test security, Test performance and Test accessibility already name it so, as the owner of what they leave out.
- The words "on each surface" carry the point of the capability: the test differs by kind of surface, a browser page at several screen sizes, a command line by what it prints and asks.
- A shorter name, "Test the user experience", was weighed: it sits beside the other four "Test …" names, but it drops the surface, and the approved pages would then quote a name the model does not hold.
- The list's longer line is the first line of the page's intent, so the two yardsticks, the surface and the screen design, are the first thing a reader sees.

## What is built, and what is only planned

Built and live (none of it tests a built product's user experience):
- **The prototype capture and the prototype walk** (for /discover-intent, Specify the product). `capture_source.py` takes "full-page screenshot(s) + the page HTML, via a headless browser" (line 8) and keeps each view's picture and visible text (`keep_view`, lines 46-51). `walk_prototype.py` walks a journey a step at a time, "click, type, press a key, go back" (walk-prototype `SKILL.md`, line 3), and after each step keeps "its picture, its visible text, and the controls and fields the person could use next" (lines 6-7). Both open the page at one screen size set in code: `walk_prototype.py` line 143 and `capture_source.py` line 157 both open the browser page at 1280 by 900. So an agent can already open a page, act on it and picture it; nothing opens a page at several sizes, and neither has ever opened a built product.
- **The rebuild eval** (`core/tools/rebuild-eval/`, installed here). An agent walks a product rebuilt from the model against what its prototype does, and judges each behaviour met, partly met or missing. Its compare prompt says, lines 21-22: "Words, layout and design may differ; judge whether a person can do the same thing and see the same result." It tests the model, not a build, and leaves layout out by design.
- **Manage surfaces and Design the work (approved, not built).** A surface's properties include "which screen sizes (viewports) it serves" and, for a coding agent, "its own characteristics, for example that each piece of work runs as a command and the person answers by typing"; its guidelines include "working within the project's design system" and, for a coding agent, "how it asks a person a question and how it reports back" (`manage-surfaces/capability.md` lines 8-9). The screen design shows each screen "either as wireframes, simple drawings of each screen, written in Markdown files, or as a prototype built with the project's design system" (`design-work/capability.md` line 9), as the screen design setting says (line 14). For a command line, the surface part is "the command, what it prints and how a person answers" (`fn-design-chosen-work/feature.md` line 17). The design is in force from its confirmation, and a build that departs from it is brought into it "once the technical lead confirms it" (`fn-update-work-design/feature.md` lines 13-14). Deployment design must make "every declared surface can be reached the way its kind needs" (`deployment-design/capability.md` line 76).

Built but stale or unused:
- **/validate-epic** (agreed new name /validate-slice), stale (#855). Its plan for a browser surface was "a browser open of each `must_open`" (`SKILL.md` line 204), the surface rule's "a real browser check that opens each `must_open` artifact and observes it render" (`surface-contract.md` line 52). It named no screen size and compared nothing with a design. Its frontend runner ran page audits (lighthouse, pa11y, axe) whose figures are Test accessibility's and Test performance's.
- **check-quality-gates** (skill, built; no live play runs it). "Human-owned cards are visibly skipped, never judged." (line 3). Its test example of a card a person owns is "Layout matches the approved UX direction", owner human (`fixtures/brownfield/quality-gates.yaml` lines 36-40). Its schema in Phoenix memory: "Design, UX, and security judgment are never runner-owned:" (`quality-gates.yaml` line 20), with the gold example "Layout matches the UX lens's approved direction", judged by a "HITL walk at /launch; fresh-context reviewer on the PR" (lines 78-82). Nothing records what that person found.
- **The stale design play for a slice's screens** (/shape-ux-lens, agreed new name /design-surface), with **author-ux-lens**: it wrote a record of each screen, and "the render script (not this skill) turns this record into `lens/wireframes.html` afterwards" (`author-ux-lens/SKILL.md` line 158), "so a product owner can look at the design rather than read a description of it" (`shape-ux-lens/SKILL.md` line 3). Its template keeps layout to "Regions and content, never pixels, never colors, never component libraries." (`grounding/lens/ux.md` line 43), and names "the name of the design system the real look comes from and" where it lives (line 90). Nothing ever compared a built screen with it.
- **The retired design pipeline's rules**, still in Phoenix memory: "Every screen MD file has a `## Wireframe` section with explicit layout pattern, named components, data fields, and actions per state." (`design.md` line 51); its screen page example notes "Viewport: desktop ≥1024" (`screen-inventory.yaml` line 77). The approved Design the work does not adopt this format, and has "Not decided: one standard for a design, with its parts and where it is kept." (`fn-design-chosen-work/feature.md` line 68).
- **check-quality** (skill, built, never used): items FE-15 and FE-16, "Design system tokens used for color, spacing, and typography (no hardcoded hex/px values)" and design system components used (`reference/all-requirements.md` lines 171-172), reading `quality/frontend/component-architecture.md`, which is in no memory tier. These check code, not a running screen; they belong with checking the code against its standards. The pages quote none of them.
- **The review of each change** (/check-change, live): row FE-15 at P3 matches a colour, a padding or a margin written as a fixed value in the lines a change adds (`standards/rules/pr.md` line 264). It belongs to capability 6 by the approved list; this capability takes its record as evidence.
- **The command-line step library** (live, read by /shape-eval): "A Claude Code play is a command-line surface: the runner starts the play as a command in the test project and gives it the scripted answers." (`steps-command-line.yaml` lines 5-6). The runner is not built; the library checks output words, which is behaviour, the eval's.

Planned only:
- "Test the user experience on each surface, against the surface's properties and guidelines (for a browser page, how it lays out across screen sizes) and the screen design from Design the work. New." It was on no earlier list.
- No play name: the agreed names hold "/validate-perf (new)" and "/validate-security (new)" (`names.md` line 16), and none for the user experience.
- The declared surfaces (Manage surfaces), the screen design and its setting (Design the work), the testing environment (Environment setup) and which tests run where (Deployment design): approved, not built.
- One severity for findings and defects, #934 (open), with a surface layer: "mobile (a misalignment can be P2 on a phone)" and "a coding agent (output a person cannot read or act on is at least P2; the same feedback given again raises it)".

What memory holds, and does not:
- For a browser surface: "Responsive is the default." with "Adaptive only on evidence." (`ux-responsive-default-adaptive-on-evidence.md` lines 22-28, "surface: web-app-or-site"); a small set of design tokens and a reused component library (`ux-design-system-tokens.md`); the states every screen must handle (`ux-state-and-feedback.md`); navigation by product shape (`ux-navigation-by-shape.md`); and, for one stack, "breakpoints 320px+, 768px+, 1200px+" (`frontend-component-orchestration.md` line 127). A domain shelf says "Responsive rendering — one experience that reflows across viewports. The floor — always." (`knowledge/domains/content-management.md` line 74). This is memory's current answer for what a browser surface should be. The pages do not write it as a rule: Manage surfaces reads it to propose a surface's properties, a person confirms them, and this capability tests what was confirmed.
- For a coding agent: Garura's own rules on how a play asks a person and reports back, which Manage surfaces names as the guideline examples. Nothing on testing a surface against them.
- No tier says how to test a built screen against a surface's layout or design system, how to compare it with a Markdown wireframe or a prototype, how close a match must be, which browsers or phones to use, or how to test a mobile app, a command line or a coding agent's surface for its user experience. No tier holds a frontend quality shelf or a design system of its own.
- The BI-4 stock-take has no line on the user experience beyond the surface rule's required check.

Not part of this capability, named so the line is clear:
- What the product does against each story: capability 1, the eval.
- What the accessibility level, its pass bar, a capability's accessibility need or a surface's accessibility guideline names, even layout: capability 4.
- Page speed and other figures a page audit gives while it opens a screen: capability 3.
- The review's rows on each change, FE-15 among them: capability 6.
- Users who test the product and accept it: "User acceptance testing (planned): Users test the product and accept it.", in Validation → Run.

## The open points, each with options and a lean

None of these is decided here. Where a lean rests on what is built or on approved pages, the drafts follow it; the rest is named as not decided on the pages. The settled rules of BI-4 (in the testing environment only; the yardstick read, never set; not tested is never passed; a tool's own score is not the verdict; a part not walked is "not walked"; the product owner names who walks; nothing declared is said plainly, neither a pass nor a fail; the builder knows what it must meet and gets only a handoff plan; who gets a finding; records taken as evidence; rounds a project setting; the line with accessibility by the yardstick) are not reopened.

### 1. What is compared

What holds: the list says "against the surface's properties and guidelines (for a browser page, how it lays out across screen sizes) and the screen design from Design the work"; Manage surfaces holds properties and guidelines per surface; Design the work holds the screen design per piece of work, wireframes or a prototype; the design in force can change by a confirmed update, also after a departure.

1. **All three, each answered part by part: each property and guideline of the declared surface, and each screen of the screen design in force at each size the surface names.** A built screen that departs from the design in force with no confirmed update is a finding for the product owner. Gain: follows the list's words; a design updated after a departure is not failed against its old version. Cost: two yardsticks from two owners to read on each run.
2. **The screen design only**, taking it as the surface's properties and guidelines already applied. Gain: one yardstick. Cost: a surface property the design forgot, such as a screen size, is never tested; the list names both.
3. **The surface only**, with the screen design left to the person's judgment. Cost: drops the list's second yardstick.

Lean: 1. The drafts follow it.

### 2. How a built screen is compared with a Markdown wireframe, and with a prototype

What holds: the screen design is one of two ways, "wireframes in MD files" or "prototypes using the project's design system" (his words); the retired design pipeline's wireframes name "explicit layout pattern, named components, data fields, and actions per state", but Design the work has agreed no standard for a design; the stale UX template kept layout to regions and content, "never pixels"; the prototype walk can walk a prototype step by step and picture each step; the rebuild eval's agent compares a rebuild with a prototype by what a person can do and see, leaving layout out. No tier says how to compare a built screen with either.

For a **wireframe**:
1. **The person reads the wireframe beside the picture of the built screen at each size, and judges each part it shows there and in its place.** Gain: works for any wireframe, since a wireframe is a drawing for people. Cost: a person's time on every screen at every size.
2. **A tool checks that the words the wireframe names (labels, fields, actions) are on the built screen, and the person judges only the arrangement.** Gain: less of a person's time. Cost: needs a wireframe format that names its parts in a way a tool can read, which Design the work has not agreed.
3. **An agent that is not the builder compares first and the person confirms.** Gain: faster. Cost: an agent's judgment is not repeatable, and memory keeps UX judgment off the runner.

For a **prototype**:
1. **The prototype and the build are walked with the same steps, pictured at the same sizes, and the person judges them side by side.** Gain: uses what is built (the walker), and a prototype built with the design system shows the look as well as the layout. Cost: the prototype must be runnable in the testing environment.
2. **A picture-by-picture comparison by a tool.** Cost: no memory or project source names one, and a prototype is not a pixel-exact target; it would need research and a memory update.
3. **The prototype read as a wireframe** (its screens pictured once and read beside the build). Cost: loses its flows and states.

Lean: wireframe 1, prototype 1. The drafts follow them. Named as not decided on the walk page: whether an agent may mark differences first (wireframe 3, with the person still judging every part); how close a built screen must be to count as matching when the design does not say; and what a wireframe must show for the comparison, while Design the work has no agreed standard for a design.

### 3. What a tool can check, what only a person can judge, and who that person is

What holds: memory's quality check schema keeps "Design, UX, and security judgment" off the runner and gives "Layout matches the UX lens's approved direction" to a person; the built runner skips such a check in view; the surface rule's least check for a page is to open it and see it render; the walker already pictures a page and lists its text and controls; Manage surfaces' guidelines say nothing about how each is checked. Settled: the person who walks is named by the product owner, never the builder; a part not walked is "not walked".

1. **A tool gathers, a person judges.** A tool opens each screen at each size the surface names, keeps its picture, text and controls, and checks only what needs no judgment (each screen opens and shows; a command or play runs to its end) and what a guideline says a tool checks. Whether a screen lays out as its surface says, keeps to the design system and matches its screen design is the named person's judgment. Gain: matches what is built and memory's split; the verdict stays honest. Cost: a person's time each round.
2. **The surface's declaration says, for each property and guideline, whether a tool or a person checks it**, as the accessibility pass bar does. Gain: one place says it. Cost: Manage surfaces' approved pages hold no "how checked" for a property or guideline; it would be a gap for that capability to close, and until then nothing would be tested.
3. **Tools for layout (for example, a page wider than its screen) and the person only for the design system and the screen design.** Gain: less of a person's time. Cost: no tier names which layout checks a tool can make, so the checks would come from the agent's own knowledge.

Lean: 1, with option 2 kept for any guideline that says a tool checks a part, so a guideline that names a tool check is used. The drafts follow it. The person: named by the product owner, for the project or the run, never the builder (settled); the drafts add no new persona.

### 4. Which screen sizes, and which surfaces

What holds: a browser surface's properties include "which screen sizes (viewports) it serves", and whether one layout reflows or each device gets its own; memory's learnings recommend one layout that reflows and, for one stack, three breakpoints; the list says "on each surface"; Manage surfaces declares a command line, a browser page, a mobile app, a coding agent and an endpoint as kinds; for an endpoint, the design's surface part is "what it takes and what it gives back".

Screen sizes:
1. **Only the sizes the surface's declaration names; a surface that names none is not tested for its layout, and goes to the product owner.** Gain: the yardstick is read, never set. Cost: nothing is tested for layout until Manage surfaces declares sizes.
2. **The sizes memory's learnings name.** Cost: writes memory's current answer as a rule, which the standing rule forbids.
3. **The sizes the screen design shows.** Cost: a design that forgot a size passes; the design follows the surface, not the other way round.

Lean: 1. The drafts follow it.

Surfaces:
1. **Every declared surface, each by what it offers: a browser page and a mobile app screen by screen at each size; a command line and a coding agent's surface by running it in a test project with set answers and reading what it prints and how it asks; an endpoint only for what its own properties and guidelines name, while what it gives back for a story is the eval's.** A kind nothing says how to test is named as not tested and goes to the product owner. Gain: follows "on each surface" and the yardstick; no surface is skipped quietly. Cost: a mobile app stays not tested until a way to open it is approved; an endpoint will mostly have nothing to test.
2. **Every surface a person opens, as Test accessibility; an endpoint is not tested here.** Gain: matches the sibling. Cost: an endpoint's declared guidelines are tested by no capability.
3. **Only surfaces with screens, browser and mobile.** Cost: drops the product owner's "same for agentic like claude-code we need to use the characteristics."

Lean: 1. The drafts follow it.

### 5. How a command line or a coding agent's surface is tested for its characteristics

What holds: Manage surfaces' coding agent property, "each piece of work runs as a command and the person answers by typing", and its guidelines, "how it asks a person a question and how it reports back in plain words"; the design's surface part for a command line, "the command, what it prints and how a person answers"; the command-line step library runs a play in a test project with scripted answers (runner not built); the approved eval page runs "A command-line slice, a play too" in a test project in the testing environment; #934's coding agent layer, "output a person cannot read or act on is at least P2".

1. **A tool runs the command or the play in a test project in the testing environment with set answers, and keeps what it printed and each question it asked; the named person judges it against the declared characteristics and guidelines and the surface part of the design.** Gain: the same way in as the eval, the same split as a browser page. Cost: a person reads each transcript.
2. **Leave it to the eval**, whose steps already check printed words. Cost: the eval checks what a story expects, not how the play asks or reports; that is a guideline, this capability's yardstick.
3. **A tool checks the guidelines' words**, for example that each question asks one thing. Cost: no tier says how a tool would check that; it would be the agent's own judgment.

Lean: 1. The drafts follow it. Where the set answers come from is the same open point as how the test reaches each surface.

### 6. The line with the eval and with accessibility

Settled for accessibility, by the yardstick: what the accessibility level, its pass bar, a capability's accessibility need or a surface's accessibility guideline names is capability 4's, even layout; the rest of the surface and the screen design are this one's; one tool run or one walk may serve both, and each reads only its own yardstick.

For the eval (behaviour), what holds: the eval runs with no agent and tests each story's goals and expectations; the approved eval page leaves "the user experience on each surface" out.

1. **By the yardstick, as with accessibility.** What a story's goals and expectations name is the eval's; what the surface's declaration and the screen design name is here. One defect may fail both, such as a field the story needs and the design shows; each answers its own yardstick, and both handoff plans may name the same way back. Gain: the same line drawn three times; no part has two owners. Cost: two findings for one cause.
2. **By who checks**: everything a script can check is the eval's. Cost: a layout at several sizes is not in any story's expectation, so it would be tested nowhere.
3. **By what changes**: what a person can do is the eval's; how it looks is here. Gain: close to option 1. Cost: "how it lays out" can stop a person doing a step, so the line blurs.

Lean: 1. The drafts follow it.

### 7. The persona

What holds (settled with capabilities 1 to 4): the product owner reads the verdict, names who walks and decides each finding a person must decide; the developer gets each finding the builder can fix alone. The technical lead confirms the screen design in Design the work.

1. **The product owner and the developer, as capabilities 1 to 4; the person who walks is named by the product owner, not a persona; the technical lead is reached through Design the work when the product owner decides the design is updated.** Gain: the same readers for every verdict of Code → Validation. Cost: the technical lead learns of a design finding second hand.
2. **Add the technical lead as a reader of each finding about the screen design.** Gain: the designer sees it at once. Cost: against the settled rule that a finding changing the screen design goes to the product owner.
3. **A new persona, a user experience tester or designer.** Cost: no approved page uses it.

Lean: 1. The drafts follow it.

### 8. What a failure sends back, and to whom

Settled: what is wrong, where and the way back, never the test, its rule, its id, its tool or a figure; the developer only when the way back is a change of the code the builder controls; the product owner when it changes the design system, the screen design, a surface's declaration, property or guideline, a part the builder does not control, or a level; a person when in doubt.

What the handoff plan says for a user experience finding:
1. **What a person meets that differs, on which surface, screen and size, and what must be true again, in plain words, with no figure and no picture the test kept.** For example: on a phone-size screen a shopper must scroll sideways to reach the pay button; the page must fit the phone's width. Gain: keeps the settled rule; the builder has the surface and the screen design, so plain words are enough. Cost: the builder does not see the picture.
2. **The same, with the picture of the built screen.** Cost: a picture is a test result, against the settled rule.
3. **A symptom only, with no size.** Cost: the builder cannot find which layout failed.

Lean: 1. The drafts follow it.

Who gets it, examples drafted under the settled rule: a page that does not reflow, or a screen built from a part other than the one the design system has for it, goes to the developer; a design system that lacks a part the screen design needs, a screen design that cannot fit the smallest size its surface names, a part the builder does not control such as a map another company shows inside the page, a surface's declaration, property or guideline, a built screen that departed from the design with no confirmed update, or a part not walked because no person was named, go to the product owner.

### 9. When nothing is declared to test against (Garura's own case)

Settled with capabilities 3 and 4: the verdict says so plainly, and is neither a pass nor a fail. The drafts apply it when no surface is declared and the work has no screen design. When only one of the two is there, that one is tested and the verdict names the other as missing.

### 10. One testing feature or two

1. **Two: the tools, and a person's walk**, as Test accessibility. Gain: each has its own who, its own cost and its own record; the tools' pictures feed the walk. Cost: two pages.
2. **Two, split by yardstick: the surface, and the screen design.** Gain: each owner's yardstick on its own page. Cost: both need a tool part and a person part, so the rules for who walks would sit twice.
3. **One feature that does both.** Cost: a person's time and the walk's record mix with every tool check.

Lean: 1. The drafts follow it.

### 11. How often a person walks again

The same point as for accessibility: the whole walk at every size each round, only what a change could touch, or the walk only once the tools and the eval pass. No lean; named as not decided on the retest page.

### Smaller points, named as not decided on the pages

- Whether an agent that is not the builder may mark where the pictures differ from the screen design first; the person still judges every part (point 2).
- How close a built screen must be to its prototype or wireframe to count as matching, when the design does not say (point 2).
- What a wireframe must show for the comparison, while Design the work has no agreed standard for a design (point 2).
- Whether the person walks only the slice's steps, or every screen the built work shows.
- Which browsers and phones, or stand-ins for them, the tools use when the surface names none.
- How the test reaches each surface of the running build: through the slice's usage guide, as the eval does, or through what the deployment design records for each surface.
- Where the tests run while no testing environment and no deployment design exist, as today.
- Where the verdict and the handoff plans are kept, and how a handoff plan reaches the developer.
- The rank of each finding, while #934 is open.
- Which parts run again on each change, and what counts as the same finding coming back (point 11).

## The features found

1. **Test the running build's user experience with tools, in the testing environment** (fn-test-user-experience-with-tools). Not built. Parts exist: the prototype capture and walk open a page, act on it and keep a full-page picture, its text and controls, at one fixed size; the stale slice check planned to open each page and see it show; the command-line step library runs a play with scripted answers (runner not built); the quality-check runner treats a missing tool as a finding. Sources: item 5 of the approved list ("for a browser page, how it lays out across screen sizes"); Manage surfaces ("which screen sizes (viewports) it serves"); `walk_prototype.py` and `capture_source.py`; /validate-epic ("a browser open of each `must_open`"); the surface rule; `steps-command-line.yaml`; check-quality-gates.
2. **Walk the running build against its surface and its screen design, in the testing environment** (fn-walk-against-screen-design). Not built. Sources: item 5 of the approved list ("and the screen design from Design the work"); his words on the screen design ("wireframes in MD files", "build prototypes using the project's design system") and on surfaces ("web would be responsive, adaptive, view ports etc.", "same for agentic like claude-code we need to use the characteristics."); memory's quality check schema ("Design, UX, and security judgment are never runner-owned:", "Layout matches the UX lens's approved direction", "HITL walk at /launch; fresh-context reviewer on the PR"); the built runner's fixture ("Layout matches the approved UX direction"); the walker ("click, type, press a key, go back"); the approved Test accessibility walk, which hands this walk over by name.
3. **Give the user experience verdict, and send each finding to the developer or to a person** (fn-send-user-experience-findings). Not built. Sources: BI-4's proof and must-not; the recovery rule; the ontology's handoff plan rule; /validate-epic's verdict and fix report; the approved Fix defects test first ("a finding in a review"); capability 4's approval that "a finding about the design system's colours or the screen design goes to the product owner"; capability 3's approval of the verdict when nothing is set; #934's surface layer.
4. **Test the user experience again as the product changes** (fn-retest-user-experience). Not built. Sources: /validate-epic's rounds ("Implement ↔ validate is expected to loop — scope narrows per round, 3 rejections halt to a human."); Manage surfaces' update ("a browser page built for desktop screens must now serve phones", "the design system that screens are built from is replaced", "From its confirmation, the updated surface is the one in force."); Design the work's update ("From its confirmation, the updated design is the one in force.", the departure brought into the design); the Settings line; /loop-code-validation (a name).

Candidates not drafted, and why:
- **Check that the code uses the design system's tokens and components** (check-quality FE-15 and FE-16, the review's FE-15 row): a check of the code, capability 6's by the approved list.
- **Check each screen design for its states, its navigation or its wireframe sections** (memory's learnings, the retired design pipeline's rules): a check of a design, not of the built work; Design the work owns the design.
- **Compare pictures of the build with the prototype by a tool**: no memory or project source names one (point 2).
- **Test the slice's outcome against its journeys** (#561): about a slice's design, not the built work.
- **Users test the product and accept it**: user acceptance testing, in Validation → Run.
- **A user experience tester persona**: point 7.

## Thin marks, and why

All five ICE pages open with the thin mark, with at most three Limits and three Fails if each: no part of this capability is built.

## Lines elsewhere that are out of step (not changed here)

- The stale UX template and shape say accessibility "lives in the marketing lens"; that play is dropped, and the approved list draws the line with accessibility by the yardstick.
- The surface rule (`surface-contract.md`) was written for an epic record that no longer exists; its required check for a page is the least this capability's tools do.
- The domain page says it "does not run the evals, release the work, or run the product"; this capability runs a copy of the product in the testing environment to test it. As approved, the domain line changes at BI-4's close.
- BI-4's own page lists its first four capabilities among what it touches; this one is added when it is written.

## Assumptions

- Assumed: user experience tests run in the testing environment that Environment setup declares, never in production and never on a builder's own machine. The list recorded it for "security and performance tests"; the product owner approved the same for the eval, Test performance and Test accessibility.
- Assumed: the parts of this capability read the declared surfaces and the screen design in force, with their confirmed updates, from the product model and Design the work's output, and never write them.
- Assumed: a command-line slice, a play too, runs in a test project inside the testing environment, as the approved eval page says.
- The examples come from several kinds of product: a shop's checkout page, a clinic's booking page with a prototype, a school's timetable app with a layout for phones and one for tablets, a team's release command, and a coding agent's play.

## Memory updates

None drafted. What no tier answers is named as not decided instead: how to compare a built screen with a wireframe or a prototype and how close a match must be, which layout checks a tool can make, which browsers and phones to use, and how to test a mobile app, a command line or a coding agent's surface for its user experience. This run did no web research, and drafting an answer from the agent's own knowledge would break the rule; a person may ask for the research, and its answer would go to a memory update for approval.

## Checks

- **Structure check** (`lint_grounding.py`): the capability page (`--kind capability --stage directional`) and the four feature pages (`--kind feature`): ok, no errors, no warnings, on the first run and after every edit.
- **ICE shape check** (a small script in the session's scratch folder): each of the five ICE pages opens with the thin mark, holds Intent, Context and Expectation in that order, exactly one Goal, one to three Limits and one to three Fails if, the fixed Read line, the Context labels in order (Read, Never read, Persona, Scope), a Scenario, and a Done means checked by someone other than the doer. No part page holds an ICE section, and each has its ICE page beside it. Outside quotes and source paths, no page says lens, seed, lock or gate, or names a real person, a home folder, a temp folder, a particular plan or a business intent's number. Run once on a copy with five planted errors (no thin mark, four Limits, a Done means by the doer, an ICE section on a part page, a forbidden word); it named all five.
- **Quotes** (a second small script): all 261 quotes on the ten pages are found word for word (spaces joined; markdown and comment marks and YAML's doubled apostrophes read as one) in their files: each quote in a Sources line in that line's own file, and each quote in a page body or its ICE page in a file that page's Sources name. Memory quotes are checked against this run's copies in `memory/`, the product owner's words against `page-approvals.md` and `capabilities.md`, the GitHub quotes against #934's text read today. His quotes are tidied for spelling only ("seecurity" to "security", "assessibility" to "accessibility", "shoudl" to "should", "wirerames" to "wireframes", "designes" to "designed", "liek" to "like", "deign" to "design"), and each Sources line that tidies says so. Run once on a copy with three planted errors (a changed word, the right words in the wrong file, a made-up quote); it named all three. The 81 quotes in this file were checked the same way against every file read; all are found.
- **Not decided lines against the approvals**: each "Not decided" line on the pages was read against the approval records of capabilities 1 to 4 and the list of six. None reopens a settled rule: four are new to the user experience (which browsers and phones, an agent's first pass with the person still judging every part, how close a match must be, what a wireframe must show), and the rest are the same as the earlier capabilities left open (how a surface is reached, where the tests run today, where the verdict is kept, the rank of a finding, which parts run again, the same finding, which screens a person walks). One draft line, that an agent's marks would let the person judge only what it marked, read as weakening the rule that every part a person must judge is walked, and was reworded so the person still judges every part.
