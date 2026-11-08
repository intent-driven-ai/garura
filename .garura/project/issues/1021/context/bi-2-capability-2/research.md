# Manage surfaces: research and drafts (issue 1021, BI-2 capability 2)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are under `.garura/project/issues/1021/context/bi-2-capability-2/drafts/product-os/software-delivery-planning/manage-surfaces/`: the capability page and its ICE page, and two feature pages, each with its ICE page. All three ICE pages carry the thin mark, because nothing of the capability is built.

What this run did besides reading:
- It copied what it read from memory through the memory tool into `bi-2-capability-2/memory/`, with `manifest.json`.
- It ran no placement: the domain (software delivery planning) was decided by the product owner.
- It checked each draft page with the structure check, each ICE page with a small shape check, and every quote in a Sources section against its file. The record is `lint.json`.
- It read GitHub issues (no write) to find the planned work. The decisions this run made are in `cite-request.json`, for the caller to record with `memory.py cite`.
- The pages were written by hand in short-term memory, as the brief asked. No skill drafts pages of the approved BI-1 shape into short-term memory.

## What is built, and what is only planned

In one line: nothing declares the project's surfaces. A surface is a place where a person, or another system, opens the product to use it. What exists is a rough list written once, a surface chosen for each slice on its own, an eval that guesses the kind from a name, stale design plays, an older contract for the surface a piece of work promised, and planned work tracked under BI-2.

Built and in the current flow:
- **A rough list of surface kinds in the product profile, written once.** When the product is first specified, `/discover-domains` (Specify the product, feature "Specify domains") writes a rough profile through `author-domains`: "the `shape` at a rough cut", "(stage / users / monetization / surfaces)". Its save adds the profile only when there is none ("the profile block: added ONLY if the live spine has none.", `core/components/plays/discover-domains/scripts/persist_seed.py`). `/discover-capabilities` firms the profile later but copies the shape as it is (`proposed = dict(profile)` in `core/components/plays/discover-capabilities/scripts/rollup_box.py`, then only state, quality levels and compliance change). So nobody confirms the list on its own, and nothing changes it after the first write except an edit by hand. The schema holds one word for each kind: `surfaces: [string] # web | mobile | cli | api | desktop | embedded` (`standards/schemas/product-os/product-profile.yaml`, line 26, Phoenix memory). No name, no person, no reason. Garura's own profile has no shape at all (`.garura/product/product-os/_spine.yaml`, its `profile` holds only state, quality levels and compliance).
- **One surface for each slice, chosen with the slice.** `/shape-slice`, through `author-slice`, picks the one surface and the person who tests it: "the thing the outcome names: a screen, a command line command or an endpoint", taken from the "intent page (asked by, outcome), the personas and journeys in the model, and the placement", and never asked of the person (`core/components/skills/author-slice/SKILL.md`, step 2). It does not read the profile's list. Garura's own slice is on "the Claude Code command line" (`.garura/product/product-os/slices/sl-intent-to-design.yaml`).
- **The eval finds its kind of surface by words in a name.** `/shape-eval` picks the step library whose `matches` words appear in the slice's surface name, which it reads from a Surface line in the slice's hidden file (`core/components/plays/shape-eval/scripts/eval_common.py`, `kind_of`). Only the command-line library exists: "A library for the browser page, the mobile app and the backend endpoint is added when a slice first needs it." (`standards/schemas/eval/_index.md`, Phoenix memory). A slice with no library gets no eval. One finding on the way: the script that writes the hidden file (`core/components/plays/shape-slice/scripts/write_hidden_file.py`) writes no Surface line in its opening; only the test sample of `/shape-eval` has one. This run opened no evals folder, so it did not check a real hidden file.
- **Phoenix memory reads surfaces, and never proposes one.** Domain shelves use the profile's surfaces to choose other things, for example "Push — when `shape.surfaces` includes mobile" (`knowledge/domains/notifications.md`) and `selection_keys: [shape.users, shape.surfaces, ...]` (`knowledge/domains/user-management.md`); UX learnings have `surface: web-app-or-site` as a condition (`knowledge/technology/ux-responsive-default-adaptive-on-evidence.md`). No learning says which kind of surface fits a person or a job. No current part does this selection; the stale design plays would.

Built, but stale or older:
- **The stale design play for a slice's screens** (`core/components/plays/shape-ux-lens/`, "waits for the rebuild of the design plays after the shaping loop (#855, ADR 053)") reads the profile's surfaces and records, for its own slice only, "`personas` and `surfaces` (medium each surface runs on," and why (`core/components/skills/author-ux-lens/SKILL.md`). The agreed names call it "/design-surface (was /shape-ux-lens)". The stale architecture lens picks a part that is "a surface the profile exposes".
- **The older surface contract.** ADR 022 and `standards/rules/surface-contract.md` (Phoenix memory): an epic declared its surface type, one of web_dashboard, server_api, cli, library or service_read_model, with the check each type needs and the deploy target each accepts. "The surface is declared once, at the cut, and checked — never re-derived." ADR 048 removed the epic record that held it, and left open "Where the structured surface contract (type, how a person reaches it, what must open) lives after the epic record leaves". The stale `/build-epic` still asks for a `Surface: <type>` line.

Only planned:
- **GitHub #553 (open), "A surface declares what it is before anyone designs it".** It is the one item under BI-2's issue in the tracker. The product owner's note of 2026-10-29: "an API can be a surface", and "This work is part of the lens work, not built yet". Its stories: #559, every surface carries its kind ("medium") and a reason, decided by a person, and "Changing a medium later is recorded as a decision, not a silent edit."; #560, a written definition that tells a surface from an integration point, checked ("CVS downloads are integration points. we will never expose that as a surface."); #562, "The profile's surface list contains only surfaces, and contains every surface the capability needs."; #561, a slice's outcome traced to the journey steps that deliver it. All four were written against play names that are gone (`/shape`, `/ux`, `/understand`).
- **Initialize (not built; `cap-initialize` in the model).** Its setup questions cover "the surfaces (web, mobile, command line, API)", and the answers go into the product profile. Its review rule groups skip the front-end group for "Surfaces with no web and no mobile", and the back-end service group for surfaces with no API and no running service. It runs again when the project "gains a database, a web surface, personal data or a new tracker, or it drops one".
- **BI-2:** "Each position is written down and can change later."

Not this capability: #561 (a slice's outcome traced to its journey steps) is about cutting slices, so it belongs to Design slices, though it sits under #553 today. #978 (`/shape-story`, a story's design with a "Surface (experience)" part) is the design of one story, under Use the lenses on each slice.

## The overlaps, and how the line could be drawn

### With "Specify the product" (BI-1): who writes the profile's list of surfaces

Specify the product's approved feature "Specify domains" has: "Out: one rough product profile, only when none exists: the product's stage, users, way of earning and surfaces (where people use it, such as the web), with coarse quality levels." Its capability page owns the profile's quality roll-up. The profile today holds kinds only.

1. **Specify proposes, Manage surfaces confirms and keeps.** The rough list stays where it is: Specify writes it once, from what a person gave. This capability takes it as one proposal, and is where each surface is named, given its kind, who opens it and why, confirmed by a person, and later updated. Specify's approved pages do not change. The cost: two writers in time, a rough one first and a confirmed one after, and the place of the confirmed list is not decided (see "Gaps").
2. **Manage surfaces owns the list outright.** Specify stops writing surfaces in its rough profile and only passes on what it saw, for example that a prototype runs in a browser. The cost: one line of an approved Specify page and the `author-domains` skill change, and until this capability is built the profile has no surfaces at all, so the shelves that select on them get nothing.
3. **Specify keeps the list; this capability only adds the kind's reason and updates.** The cost: two writers of one list for good, and the defect #562 found (things that are not surfaces on the list, a real one missing) stays with a step that never asks a person about surfaces.

My lean is option 1. It keeps the approved Specify pages as they are (they already say "rough"), and gives one place where a person confirms and changes the list. The drafts follow it: the first rough list is Out, read as a proposal.

### With "Design slices" (BI-3): a slice picks one surface and its tester

As built, `author-slice` picks each slice's one surface on its own and never asks. Nothing ties it to a project list.

1. **The declared surfaces are the list a slice picks from.** Design slices picks a slice's one surface from the declared surfaces, and names the screen or command inside it (the ontology's example: "Vertical: the checkout in the mobile app"). A slice that needs a surface not on the list goes on, and the surface is named for a person to declare here. The cost: `author-slice` reads one more input, and a slice's surface must point to a declared one.
2. **Slices choose freely; this capability collects.** Each slice keeps choosing its own surface, and a new one is added to the declared list afterwards, as an update. The cost: the kind is still decided by whichever slice comes first, which is the failure #559 records ("So the medium gets assumed by whichever play designs first.").
3. **The kind lives on each slice's surface.** No project list: each slice records its surface's kind and reason, as #559's words literally say ("Every surface record carries a medium and a reason for it."). This capability keeps only the list of kinds. The cost: the same surface in two slices can get two kinds, and nobody declares the project's surfaces, against the agreed line.

My lean is option 1. It is the only one where a person decides each kind before the first slice is designed, and it keeps the "surface and tester are never a question" rule of `/shape-slice`: the slice still proposes, from a list a person already confirmed. The drafts follow it ("Each slice then picks its one surface from the declared ones").

### With "Design for evaluation and testing" (BI-3): the step library of each kind of surface

As built, the eval matches words in the slice's surface name against each library's `matches` list, and only a command-line library exists. The kinds are named four ways today (see "Gaps").

1. **The declared kind names the library.** Each declared surface has a kind from one list, and the eval finds its step library by that kind, through the slice's surface, not by words in a name. This capability owns the list of kinds and each surface's kind; Design for evaluation and testing owns the libraries, their sentences and when a new one is written. A declared kind with no library is shown as a gap, never a stop. The cost: the eval reads one more link, and the kinds must use the library names.
2. **Keep them apart.** The eval keeps matching words; the declared kinds serve people and memory only. The cost: two lists that drift, and a slice named "the booking screen" matches no library even when its surface is declared a browser page.
3. **Declaring a new kind asks for its library.** When this capability declares a kind with no library, it asks for the library to be written. The cost: it reaches into the eval capability's job, against ADR 057's "added when a slice first needs it".

My lean is option 1. The drafts put the libraries and the eval Out, and say the eval "finds the library from the kind declared here".

### With "Design the technology and architecture" (BI-2, approved)

Its approved page has "Out: the project's surfaces (Manage surfaces), ...", its main parts include "what the person sees", and its update example is "it gains a database or a new surface".

1. **What each surface is, here; what it is built with, there.** This capability declares each surface, its kind, who opens it and why. The architecture names the part that serves each surface and its technology, for example the web front end of a browser surface with its framework and version. A new surface here is a reason to update the architecture there. The cost: none on the approved pages; the architecture reads the declared surfaces.
2. **Kind and technology together here.** Each surface carries its kind and its technology, such as "browser, with a named web framework". The cost: technology in two places, against the approved page, which holds "the technology of each part".
3. **Surfaces become part of the architecture.** Manage surfaces turns into a feature of Design the technology and architecture. The cost: reopens an approved boundary and the agreed list.

My lean is option 1. The drafts follow it.

### The siblings under BI-2, and two neighbours

No decision asked, but the drafts draw these lines, and one of them needs a look:
- **Seed the memory for the lenses (part of initialize).** Initialize's setup questions (not built) already ask about the surfaces and keep the answer in the profile, and the answer picks memory blocks and review rule groups. The drafts treat it like the first capability's line with initialize: declared here, read there; when initialize runs first, on a fresh project, its confirmed surfaces answer is one proposal here, and the setup answers are named among the inputs. Under the other two ways (initialize sets the first surfaces, or initialize stops asking), only the Out line on seeding and one input line change.
- **Lock the design.** The drafts leave "how the surfaces are updated once the design is locked" as not decided.
- **Deployment design and Environment setup.** Out. The older contract tied each surface type to a valid deploy target ("a real local URL, preview URL, or declared server endpoint" for a web page); that pairing may need a look when Deployment design is drafted.
- **Use the lenses on each slice.** The screens lens is to be named `/design-surface`. The name reads like this capability, but the play designs one slice's screens. Out here; the name is a point to watch, not to decide in this draft.
- **Bring the design together for a vertical slice.** Its agreed line lists "surfaces" among the parts brought together for one slice. Out here: it joins one slice's design.

## The persona

The drafts name the product owner, not the architect of the first capability, because what is built says so: initialize's setup questions, where the surfaces are asked, are answered by the product owner; `/shape-slice`, which picks a slice's surface, names the product owner in its scenarios; and in #559 it was the product owner who decided each kind and gave the reasons ("i realise you never asked me this and assumed this is all terminal"). The stale screens play also names a "product designer" in one scenario; nothing built names a designer as the one who declares surfaces.

## Features found

Two features, neither built. Each ICE is thin.

- **Declare the project's surfaces** (fn-declare-surfaces). Not built. Sets the list of places where people or other systems use the product, each with its name, its kind, who opens it, what they do there and why, proposed from the project's code and memory and confirmed by a person; only surfaces go on the list. Sources: the agreed one line; BI-2's outcome; #553 with its note "an API can be a surface"; #559 (kind and reason, decided by a person); #560 (surface or integration point); #562 (only surfaces, every surface needed); the rough list Specify writes (built, `author-domains`); initialize's surfaces question (planned, model page); the stale screens play's per-slice "medium each surface runs on". The definition (#560) and the kind (#559) are rules of this one feature, not features of their own, because they are part of declaring a surface.
- **Update the surfaces as the project changes** (fn-update-surfaces). Not built. When the project gains or drops a surface, or a kind must change, a person confirms an update, and what held before stays readable with why. Sources: BI-2's proof "Each position is written down and can change later."; #559's "Changing a medium later is recorded as a decision, not a silent edit."; initialize's re-run "when the project changes: it gains ... a web surface ... or it drops one" (planned); the architecture's update example "it gains a database or a new surface"; the decision schema's replace-never-edit rule. What is built is the gap: the profile's list is never changed after its first write.

Candidates not drafted:
- **Show which slice is on each surface.** In #562 the product owner asked "show me the four surfaces and which slice delivers each". It is a request inside a defect, not a planned feature. Named here only.
- **Where a surface's contract lives (its type, how a person reaches it, what must open).** ADR 048 left it open. It could become part of a declared surface, but nothing agreed says so. An open point below.
- **A step library for each kind of surface.** Planned under ADR 057, owned by Design for evaluation and testing.

## Gaps that matter

- **Nothing declares the project's surfaces, and nothing asks a person for a surface's kind.** As #553 says: "Nobody ever asked what kind of screen this is." The cost recorded there: "all of them cost a rewrite after the design was already written".
- **Four lists of kinds disagree.** The profile: web, mobile, cli, api, desktop, embedded. The eval: command line, browser page, mobile app, backend endpoint. The older contract: web_dashboard, server_api, cli, library, service_read_model. Initialize: web, mobile, command line, API. Phoenix memory's learnings add a fifth word, `web-app-or-site`. An agent reading one cannot match it to the others without a guess.
- **The model has no place for a declared surface.** The profile's list holds a word per kind, with no name, person or reason; the ontology (v15) has no kind for a surface and lists nothing as not yet defined. The pages say "Not decided".
- **The planned work is written against plays that are gone.** #553 and its stories name `/shape`, `/ux` and `/understand`, which no longer exist under those names; they need new words before anyone builds from them.
- **The eval may find no surface in a real hidden file.** As read in the code, the hidden-file script writes no Surface line, while the eval reads one. Not checked on a real file. This is Design for evaluation and testing's to confirm, named here because the eval's kind is where this capability's list would be read.

## Open points for the product owner

- The line with Specify the product: option 1, 2 or 3. The drafts follow option 1.
- The line with Design slices: option 1, 2 or 3. The drafts follow option 1.
- The line with Design for evaluation and testing: option 1, 2 or 3. The drafts follow option 1.
- The line with Design the technology and architecture: option 1, 2 or 3. The drafts follow option 1.
- The persona: the product owner, from what is built. The first capability used the architect.
- Whether a surface's contract (its type, how a person reaches it, what must open) becomes part of a declared surface, or stays with the eval and the build.
- Whether #553 and its stories, once reworded, become the work items of these two features; #561 would then move to Design slices.

## Details left out of the pages

Left for an agent that builds these parts to find in the code and memory: the field names of the profile, the slice record and the older contract; how the eval matches a name to a library; the review rule groups initialize would skip for each answer; and which Phoenix memory shelves and learnings select on surfaces.

## Structure check

`python3 .claude/skills/discover-capabilities/scripts/lint_grounding.py` on each page: `--kind capability --stage directional` for the capability, `--kind feature` for each feature. All three pages read ok, with no error and no warning. The first run already had none; nothing had to be fixed for the check. The record is `lint.json`.

The structure check has no mode for one ICE page, so a small check in the same record tested each of the three ICE pages: the three sections in order, exactly one Goal, at least one Limit, Fails if and Done means, no more than three Limits and three Fails if (the rubric's limit for a thin ICE), the fixed Read line first, the Context labels in order (Read, Never read, Persona, Scope), a Done means checked by someone other than the doer, the thin mark at the top, and no plan named. All three read ok. No ICE page has a Never read line: nothing found says what these parts must not read. No part page has an ICE section. The approved ICE pages of the first capability have up to five Fails if lines on a thin ICE; these drafts keep to the rubric's three.

Every quote in a Sources section was checked against its file, word for word: 97 quotes, none missing. Two Sources lines carry no quote: the short line beside each feature, and the shelf line. The quotes of GitHub issues were checked against the issue texts as read on 2026-11-07.

## What this run read from memory

Through the memory tool, copied to `.garura/project/issues/1021/context/bi-2-capability-2/memory/` with `manifest.json`: from Phoenix memory, the product profile, spine, slice, product-os, decision and ontology schemas, the eval step library index and the command-line library, the surface contract rule, the resolution rule, the capability and feature grounding templates, the ICE rubric, the knowledge index, three domain shelves (notifications, user management, experience) and two UX learnings. From Garura memory (the product model), five lines read for the decision traces (see `cite-request.json`). No tier was missing.

---

# Addendum, round 2 (2026-11-07): redrafted around the product owner's correction

The round 1 drafts are kept unchanged in `drafts-round-1/`. The drafts in `drafts/` are now round 2. Nothing outside `bi-2-capability-2/` changed.

## The product owner's correction, as given

The product owner on 2026-11-07, on the first drafts: "the surface needs to be designed based on what they offer for example web would be responsive, adaptive, view ports etc. same for agentic like claude-code we need to use the characteristics. declare the surface, and its properties is what this is about for each surface we need to define guidelines example for web - we need to handle for design system etc. hence the way this functionality needs to be defined is around the surface selected and the design would be for that surface"

So the capability is now about declaring each surface the project has with its **properties** (what it offers and how it behaves) and its **guidelines** (what every design on it must handle), so that every design on that surface is made for it. Designing each slice stays with Design slices and Use the lenses on each slice, which read what is declared here.

## What changed on each page

- **Capability page.** The directional intent now says each surface holds its properties and its guidelines, with his examples (responsive, adaptive, viewports; a coding agent's characteristics; working within a design system). The features are renamed. "What is not built yet" adds that a slice's own design decides parts of this alone (the stale screens play reads the design system from the profile or an earlier decision and records the visual core as a decision later slices reuse), and that Phoenix memory holds properties and guidelines only in parts. The Benefit hypothesis is now "every slice is designed for the surface it is on". Boundary: a second In line for properties and guidelines; the Out line on the lenses now says they design the slice following the surface's properties and guidelines; the Out line on technology now names the technology of a design system (its component library and version) as the architecture's. New guiding rules: the design follows the surface; each property and guideline names its source; each guideline serves a property or a quality level of the profile; the profile's quality levels bound the guidelines and are never changed here. The memory-first rule now covers properties and guidelines.
- **Capability ICE.** The Goal now covers properties and guidelines and that every design on the surface follows them. A new Fails if: a slice's design breaks a property or guideline of its surface with no gap or update to explain it. A new Done means compares each slice's design with its surface's properties and guidelines. Read and Scope widened. Still thin.
- **Feature 1, now "Declare a surface, its properties and its guidelines"** (same folder, `fn-declare-surfaces`). It holds the kind, who opens it and why as before, and adds properties and guidelines, with examples from several kinds of surface. It says why they are one step: the guidelines follow from what the surface offers. Status adds what is built or in memory for properties and guidelines. New rules: the code's own design system is described as it is; each guideline serves a property or a profile quality level; the profile bounds the guidelines. New acceptance criteria for an existing design system, a memory learning, and a guideline below the profile's accessibility level. Still thin.
- **Feature 2, "Update the surfaces as the project changes"** (`fn-update-surfaces`). Reworded to cover properties and guidelines: new examples (a page must now serve phones, the design system is replaced, the accessibility level rises), new triggers (a raised profile level, a changed memory learning that a guideline names as its source), "one answer in force for each property and each guideline", and new acceptance criteria. Still thin.

## What is built or in memory for properties and guidelines, by kind of surface

Read through the memory tool (Phoenix memory) and in the source. Nothing below is written into a page as a rule; the pages say where the answer comes from.

**Browser (web page or web app).** The only kind with learnings matched to it. Phoenix memory's learnings carry a `surface` condition, and every value is a web or screen one: `web-app-or-site`, `web-app`, `content-site`, `any-public-ui`.
- Properties in memory:
  - one layout that reflows or a layout for each device: `knowledge/technology/ux-responsive-default-adaptive-on-evidence.md` ("Any web surface that must work across device sizes."), and `knowledge/domains/content-management.md` ("Responsive rendering — one experience that reflows across viewports.");
  - screen sizes: only as one learning's current answer, tied to one stack: `knowledge/technology/frontend-component-orchestration.md` ("**Responsive floor:** breakpoints 320px+, 768px+, 1200px+", conditions `surface: web-app`, `stack: react-nextjs-app-router`). An old sample in `standards/schemas/screen-inventory.yaml` ("Viewport: desktop ≥1024") belongs to a retired design pipeline;
  - navigation by the product's shape: `knowledge/technology/ux-navigation-by-shape.md` ("Any web surface with more than a couple of destinations.").
- Guidelines in memory:
  - a design system: `knowledge/technology/ux-design-system-tokens.md` ("How the product's visual consistency is held — design tokens and a reused component set.", "Any web surface, especially once there's more than a handful of screens.");
  - accessibility: `knowledge/technology/ux-accessibility-floor.md` (`surface: any-public-ui`; it also says how it is checked: "automated checks (axe) in CI plus a manual keyboard");
  - states and feedback, and forms: `ux-state-and-feedback.md`, `ux-forms-and-validation.md` (`has-forms: true`).
- Built (stale): the screens lens keeps a "visual core" for each slice: a closed list of state words with their tones, the rule that a state word always prints beside its colour, and "the name of the design system the real look comes from and" where it lives (`standards/schemas/product-os/grounding/lens/ux.md`). Its schema says the visual core is "set once, referenced by every capability" (`standards/schemas/product-os/lens/ux.yaml`). `author-ux-lens` reads the design-system name "from the product profile or an existing product decision", says plainly when none exists, and reuses a visual-core decision once one exists, so as built the first slice sets it for the product. The profile has no field for a design system.
- Older (ADR 022, `standards/rules/surface-contract.md`): for `web_dashboard`, a "real browser check that opens each `must_open` artifact", a valid target of "a real local URL, preview URL, or declared server endpoint", and the first piece of work must build the app's shell.

**Mobile app.** No learning is matched to it. Domain shelves name what it brings: push and text alerts (`knowledge/domains/notifications.md`), one-tap phone wallets ("Wallets — Apple Pay / Google Pay one-tap. Add when `shape.surfaces` includes mobile.", `knowledge/domains/payments.md`). Two web learnings mention it in passing: navigation collapses into a drawer on mobile (`ux-navigation-by-shape.md`), and type and spacing shrink on mobile (`frontend-component-orchestration.md`). No eval step library for it yet.

**Command line, and a coding agent such as Claude Code.** No learning is matched to it. What exists is Garura's own, for its own plays:
- Properties: "A Claude Code play is a command-line surface: the runner starts the play as" a command and gives it the scripted answers (`standards/schemas/eval/steps-command-line.yaml`); a long run writes a status file, and "for Claude Code, a plugin" shows it (`standards/rules/run-status.md`); the Claude Code install takes agents and skills, has no play type, and an agent carries its model while a skill has none (`core/components/plays/install-garura/scripts/adapters/claude.py`, which serves Support each coding tool).
- Guidelines: the rule for asking a person ("Each question asks one thing.", `core/components/skills/_shared/asking-a-person.md`); lead in the person's language ("When addressing the user, lead in the language the user operates in:", `standards/rules/user-facing-voice.md`); approvals are typed ("Never use `AskUserQuestion` for checkpoints. Output summary, wait for typed response.", `CLAUDE.md`); no name is a tool's built-in ("Never a tool's own command.", `standards/rules/naming.md`).
- Older (ADR 022): for `cli`, "a command run that executes `human_run_target` and asserts its output".
- Phoenix memory treats "agentic" differently from his words: "So agentic is a pattern across all three" experience surfaces (conversational, generative, orchestrated), "not a fourth surface" (`knowledge/domains/experience.md`). His words treat a coding agent such as Claude Code as a surface with its own characteristics. The drafts follow his words and give the coding agent as an example kind; whether it is its own kind or a command line with agentic characteristics is an open point.

**API that another system calls.** The product owner decided "an API can be a surface" (#553). Older (ADR 022): `server_api`, checked by "an HTTP/API check that calls the declared endpoint", reachable at "a reachable HTTP endpoint". Shelves use it to choose other things (a content API when the surfaces span more than one; `api` "for agent consumption" in `experience.md`). No eval step library yet.

**Other kinds the product owner named.** #553 and #559 record his own starting list: "terminal CUI types, full blown browser CX, mobile app types, or someting that is more like IDX? generative HTML types?", and "terminal, browser, mobile, IDE-like, generative" as a starting vocabulary. Nothing in memory describes an IDE-like or a generative surface.

In short: for a browser surface, properties and guidelines can be proposed from Phoenix memory today. For a mobile app, an API, an IDE-like or a generative surface, memory has almost nothing, so they would be researched and raised as memory updates. For a coding agent, Garura's own rules exist but are written for Garura's plays, not as learnings any project can match.

## Are the guidelines a separate job?

Partly, yes. They have inputs of their own: the design system the project names, the product profile's quality levels, Phoenix memory's guideline learnings, and Garura's own rules for its plays. They also have a check of their own: a slice's design is checked against them, and the accessibility learning names its own test. Properties come mostly from the project's code and what the surface offers. Kept in one feature as asked, because each guideline follows from a property or a quality level of the surface it belongs to; the product owner decides.

## The overlaps, adjusted

- **Specify the product.** Lean unchanged (option 1). The capability now also reads the profile's quality levels to bound the guidelines, and never writes them.
- **Design slices.** Lean unchanged (option 1): a slice picks its surface from the declared ones, and its design then follows that surface's properties and guidelines.
- **Design for evaluation and testing.** Lean unchanged (option 1). One note: the older contract tied each type of surface to the check that proves it runs; if a property ever names how a surface is reached for a test, the eval still owns the step library and the check.
- **Use the lenses on each slice (neighbour).** This line moved most. As built, the stale screens lens decides the product's design system and visual core from the first slice. With the new focus: the surface's guidelines, such as the design system to work within, are declared here once; the lens applies them to each slice's screens, states and look, and never sets them.
- **Design the technology and architecture: where a design system choice sits.** The approved architecture pages stay unchanged.
  1. **Here: which design system the designs on a surface work within, and the guideline to stay within it.** There: the technology it is built with, such as a component library and its version, as "the technology of each part" the approved page already holds. In the lens: its use in each slice. The cost: one design system touches three places, each with one job.
  2. **All in the architecture.** The design system is a technology choice. The cost: a design system is also a style guide and a design file, not only code, and the approved pages hold technology only, so they would need a new line.
  3. **In the screens lens, as built.** The first slice records it and later slices reuse it. The cost: the first slice decides for the whole product, the same failure the first capability avoids for technology.
  
  My lean is option 1. The drafts follow it: the capability's Out line names "the technology a surface and its design system are built with, such as a web framework or a component library and their versions" as the architecture's, and keeps naming the design system and its guideline here.
- **Persona.** Unchanged: the product owner.

## New open points for the product owner

- Whether the guidelines stay in the declaring feature (as drafted) or become a feature of their own, given they have their own inputs and checks.
- Whether a coding agent such as Claude Code is its own kind of surface, or a command line with agentic characteristics, given that Phoenix memory treats agentic as a pattern across surfaces.
- Where a design system sits: option 1, 2 or 3 above. The drafts follow option 1.
- For kinds with no learnings in memory (mobile app, API, IDE-like, generative), properties and guidelines go through research and memory updates. The drafts say this; no list was invented.

## Checks, round 2

- Structure check: the capability (`--kind capability --stage directional`) and both features (`--kind feature`) read ok, with no error and no warning, on the first run.
- ICE shape check: all three ICE pages read ok: one Goal, three Limits and three Fails if at most (thin), the fixed Read line first, Context labels in order, a Done means checked by someone other than the doer, the thin mark, and no plan named. No part page has an ICE section.
- Quote check: every quote in the three Sources sections was found word for word in its file; the count is in `lint.json`. The product owner's 2026-11-07 words are checked against this addendum, which holds them as given.
