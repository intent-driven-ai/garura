# BI-2 clean-up: what changes and why (draft)

This is a draft. Nothing in the product model, on GitHub or in git was changed. It lists every line
that the product owner's three decisions of 2026-11-08 make wrong in the Spec → Design business
intent (BI-2) and in its four capabilities, and gives the new words for each line. The decisions
are recorded in `.garura/project/issues/1021/context/capabilities.md`, the note under the
Spec → Design list:

1. Seeding memory is dropped from BI-2. It belongs to the play that starts the build. Right now
   the work only updates the model.
2. The word lens is no longer used for designing a slice. Each line that used it now says
   "designing each slice (Design → Code)". The new name is settled when BI-3 is reviewed.
3. There is no lock and no gate in BI-2. Each design can run at any time.

**The pages in scope.** There are 30 pages, not 16. BI-2 touches 15 parts: 4 capabilities and 11
features. Each part has a page and an ICE page, so 15 x 2 = 30 pages. With BI-2's own page, that
makes 31.

**What changes.** 71 lines on 24 of the 31 pages: 5 lines on BI-2 and 66 lines on 23 capability
and feature pages. Seven feature ICE pages need no change: Set the project's architecture, Declare
a surface, Design how the project runs, Prepare a cartridge for each cloud, Declare the
environments, Build an environment and Set up a dev sandbox. 13 of the 71 changes remove a whole
line, and 58 replace a line.

**Who writes it.** enrich-grounding's named-lines script (`change_lines.py`) makes all 71
changes in one all-or-nothing run, from `change-lines-request.json`. `bi-2-page.md` gives the
reasons for using this script on the BI-2 page instead of author-intent-page's rewrite.

## 1. The BI-2 page diff, in full

From the Stage line to the end, the page is byte for byte the same: the Stage line, the Tracker
line, the 15 Touches lines and the What-was-done line.

```diff
--- a/.garura/product/product-os/intents/bi-2.md
+++ b/.garura/product/product-os/intents/bi-2.md
@@ -1,17 +1,15 @@
 # Spec → Design
 
-**Outcome:** The project's positions are set for the whole project: technology and architecture, surfaces, deployment and environments. The memory each lens needs is seeded, and a design is locked before agents take over.
+**Outcome:** The project's positions are set for the whole project: technology and architecture, surfaces, deployment and environments.
 
-**Why:** Without shared positions, each builder invents its own answer. Without the lock, agents drift.
+**Why:** Without shared positions, each builder invents its own answer.
 
 **Asked by:** the product owner
 
 **Proof it is met:**
 - Each position is written down and can change later.
-- Each lens has its memory.
-- No agent builds from a design that isn't locked.
 
-**Must not:** Block on anything except the lock, which is the only gate.
+**Must not:** Block other work. Each design can be run at any time.
 
 **Stage:** confirmed — by the product owner, 2026-11-02
 **Tracker:** #2
```

## 2. Each kind of change

### A. The reason "must not block on anything except the lock" becomes "blocks no work, and each design can run at any time": 19 lines on 15 pages

The rest of each line is kept word for word. Two forms of the old reason are replaced:
"the Spec → Design business intent must not block on anything except the lock" (15 lines) and
"the business intent's only gate is the lock" (4 lines). On Environment setup's capability page,
the line also says "and a person's yes before a live step is already the rule". That part is kept,
and the list's "and" is fixed.

Before (`software-delivery-planning/design-technology-architecture/capability.md`, line 46):

> - Never: block work on a missing choice. The work goes on from the project's code and memory, and the open choice is named. The reason: the Spec → Design business intent must not block on anything except the lock.

After:

> - Never: block work on a missing choice. The work goes on from the project's code and memory, and the open choice is named. The reason: the Spec → Design business intent blocks no work, and each design can run at any time.

Before (`software-delivery-planning/environment-setup/capability.md`, line 81):

> - A missing declaration is a gap, not a stop. Slices are designed and built with an environment still open, and the gap is named. Only building an environment needs its confirmed declaration, because it stands up something live. The reason: the business intent's only gate is the lock, and a person's yes before a live step is already the rule.

After:

> - A missing declaration is a gap, not a stop. Slices are designed and built with an environment still open, and the gap is named. Only building an environment needs its confirmed declaration, because it stands up something live. The reason: the Spec → Design business intent blocks no work, each design can run at any time, and a person's yes before a live step is already the rule.

Pages:
- Design the technology and architecture: capability.md
- Design the technology and architecture: fn-set-architecture/feature.md
- Design the technology and architecture: fn-update-architecture/feature.md
- Manage surfaces: capability.md
- Manage surfaces: fn-declare-surfaces/feature.md
- Manage surfaces: fn-update-surfaces/feature.md
- Deployment design: capability.md
- Deployment design: fn-cloud-cartridges/feature.md
- Deployment design: fn-design-how-project-runs/feature.md
- Deployment design: fn-update-deployment/feature.md
- Environment setup: capability.md
- Environment setup: fn-build-environment/feature.md
- Environment setup: fn-declare-environments/feature.md
- Environment setup: fn-dev-sandbox/feature.md
- Environment setup: fn-update-environments/feature.md

### B. Lines about locking the design, or opening a locked design, are removed: 16 lines on 12 pages

- 11 lines are removed whole: 3 capability Out lines ("Out: locking the design before agents
  take over..."), 4 "Not decided: how ... is updated once the design is locked" lines, and 4 Out
  of scope lines ("Opening a locked design for an update...").
- 5 lines lose only their locking clause: Manage surfaces' Out line on deployment,
  environments and locking, and the Scope line of the four "update" ICE pages, which listed
  "opening a locked design" among what is out.

Before (`software-delivery-planning/design-technology-architecture/fn-update-architecture/feature.md`, line 41):

> - Not decided: how the architecture is updated once the design is locked. Lock the design owns the lock, the only gate, and it is not built.

After:

> (line removed)

Before (`software-delivery-planning/manage-surfaces/capability.md`, line 54):

> - Out: how the product is deployed (Deployment design), its environments (Environment setup), and locking the design before agents take over (Lock the design, the only gate).

After:

> - Out: how the product is deployed (Deployment design) and its environments (Environment setup).

Before (`software-delivery-planning/deployment-design/fn-update-deployment/ice.md`, line 16):

> - Scope: In: updating how the whole project runs and each cloud's cartridge as the project and the clouds change, and keeping what held before with why it changed. Out: setting the first design, preparing the first cartridges, moving what already runs onto the updated design, setting up a new environment, updating the architecture, raising a quality level in the product profile, decision records, opening a locked design, production, and moving a memory update into Phoenix memory.

After:

> - Scope: In: updating how the whole project runs and each cloud's cartridge as the project and the clouds change, and keeping what held before with why it changed. Out: setting the first design, preparing the first cartridges, moving what already runs onto the updated design, setting up a new environment, updating the architecture, raising a quality level in the product profile, decision records, production, and moving a memory update into Phoenix memory.

Pages:
- Design the technology and architecture: capability.md
- Design the technology and architecture: fn-update-architecture/feature.md
- Manage surfaces: fn-update-surfaces/feature.md
- Deployment design: capability.md
- Deployment design: fn-update-deployment/feature.md
- Environment setup: capability.md
- Environment setup: fn-update-environments/feature.md
- Manage surfaces: capability.md
- Design the technology and architecture: fn-update-architecture/ice.md
- Manage surfaces: fn-update-surfaces/ice.md
- Deployment design: fn-update-deployment/ice.md
- Environment setup: fn-update-environments/ice.md

### C. ICE Scope lines that end "... and the lock": 4 lines on 4 pages

"and the lock" is removed and the list's "and" is fixed. These lines also listed "seeding memory".
That item is renamed to match each capability's own Out line, for example "putting the memory that
fits the deployment design into the project", because it is still out of scope. On the
architecture page, "each slice's design through the lenses" also becomes "designing each slice
(Design → Code)". Each line is counted once, under this kind.

Before (`software-delivery-planning/design-technology-architecture/ice.md`, line 17):

> - Scope: In: proposing, setting and updating the project's architecture, with its technology, for the whole project. Out: each slice's design through the lenses, the product profile, writing and keeping decision records, seeding memory, moving a memory update into Phoenix memory, surfaces, deployment, environments and the lock.

After:

> - Scope: In: proposing, setting and updating the project's architecture, with its technology, for the whole project. Out: designing each slice (Design → Code), the product profile, writing and keeping decision records, putting the memory that matches the architecture into the project, moving a memory update into Phoenix memory, surfaces, deployment and environments.

Pages:
- Design the technology and architecture: ice.md
- Manage surfaces: ice.md
- Deployment design: ice.md
- Environment setup: ice.md

### D. "Use the lenses on each slice" and the lens definition: 6 lines on 5 pages

"Use the lenses on each slice" becomes "Designing each slice (Design → Code)". The sentence "A lens
is one view of a slice's design, such as its screens or its architecture." is removed. On the
architecture capability page, the part that says what slice design covers for architecture is
kept.

Before (`software-delivery-planning/design-technology-architecture/capability.md`, line 39):

> - Out: designing one slice through the lenses. A lens is one view of a slice's design, such as its screens or its architecture: for architecture, the parts the slice passes through and what crosses between them. Use the lenses on each slice (Design → Code) owns it, and builds on the project's architecture.

After:

> - Out: designing one slice: for architecture, the parts the slice passes through and what crosses between them. Designing each slice (Design → Code) owns it, and builds on the project's architecture.

Pages:
- Design the technology and architecture: capability.md
- Design the technology and architecture: fn-set-architecture/feature.md
- Manage surfaces: capability.md
- Manage surfaces: fn-declare-surfaces/feature.md
- Deployment design: capability.md

### E. Out lines that hand seeding memory to "Seed the memory for the lenses": 5 lines on 5 pages

The first sentence, which says what is out, is kept. The second sentence now says that the work
belongs to the play that starts the build, not to the product model. On Manage surfaces, "and
reads the declared surfaces" is kept as "and that play reads the declared surfaces".

Before (`software-delivery-planning/deployment-design/capability.md`, line 64):

> - Out: putting the memory that fits the deployment design into the project. Seed the memory for the lenses, a part of the project set-up step (initialize), owns it.

After:

> - Out: putting the memory that fits the deployment design into the project. It belongs to the play that starts the build, not to the product model.

Pages:
- Design the technology and architecture: capability.md
- Design the technology and architecture: fn-set-architecture/feature.md
- Deployment design: capability.md
- Environment setup: capability.md
- Manage surfaces: capability.md

### F. Sources lines that quote a line that changes: 16 lines on 15 pages

- 15 lines quote BI-2's Must not. In each, only that quote changes, to the new Must not.
  No Sources line quotes one of BI-2's removed lines, so no quote is dropped.
- 1 line on Deployment design's capability page quotes Manage surfaces' Out line on deployment,
  environments and locking (kind B). Its quote becomes the new text of that line.

Before (`software-delivery-planning/deployment-design/fn-cloud-cartridges/feature.md`, line 67):

> - .garura/product/product-os/intents/bi-2.md: "Block on anything except the lock, which is the only gate."

After:

> - .garura/product/product-os/intents/bi-2.md: "Block other work. Each design can be run at any time."

Before (`software-delivery-planning/deployment-design/capability.md`, line 99):

> - .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "Out: how the product is deployed (Deployment design), its environments (Environment setup), and locking the design before agents take over (Lock the design, the only gate)."

After:

> - .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "Out: how the product is deployed (Deployment design) and its environments (Environment setup)."

Pages:
- Design the technology and architecture: capability.md
- Design the technology and architecture: fn-set-architecture/feature.md
- Design the technology and architecture: fn-update-architecture/feature.md
- Manage surfaces: capability.md
- Manage surfaces: fn-declare-surfaces/feature.md
- Manage surfaces: fn-update-surfaces/feature.md
- Deployment design: capability.md
- Deployment design: fn-cloud-cartridges/feature.md
- Deployment design: fn-design-how-project-runs/feature.md
- Deployment design: fn-update-deployment/feature.md
- Environment setup: capability.md
- Environment setup: fn-build-environment/feature.md
- Environment setup: fn-declare-environments/feature.md
- Environment setup: fn-dev-sandbox/feature.md
- Environment setup: fn-update-environments/feature.md

### Left alone, as asked

- Sources lines that quote the capability list's old "Seed the memory for the lenses..." and "Lock
  the design..." lines. That text is kept in capabilities.md, so the quotes still match.
- Sources lines and paths that name real files, such as `shape-run-lens`, `author-run-lens`,
  `lens/run.yaml` and `deploy-local-environment` ("seed step", "seeded TEST users").
- Quotes of ADR 066, and Sources lines that say "The capability list the product owner locked on
  2026-11-03". There, "locked" means agreed, not the dropped lock.

## 3. Lines I was unsure of

1. **Kept: Update the architecture, feature page, line 18.** "An older skill refused to change a
   locked architecture until it was moved back to draft. No play calls it." This states what a
   built skill does: author-technical-approach refuses to edit an `architecture.yaml` whose
   status is LOCKED. The page's Sources line 72 quotes it: "architecture.yaml is LOCKED -- drop to
   DRAFT first." It is not about the lock the decision dropped, so the decision does not make it
   wrong. It is the one body line the grep still finds. If the grep must come back empty, the line
   could say "an architecture marked final" instead. That describes the skill less exactly, so I
   did not change it.
2. **Kept: four Sources lines that now back nothing on their page.** These are the capability-list
   quotes of "Lock the design..." on the four "update" feature pages: Update the architecture
   line 78, Update the surfaces line 85, Update the deployment design line 89 and Update the
   environments line 82. They were the source of the Not decided and Out of scope lines that kind B
   removes. The quotes still match capabilities.md, so I left them as asked. After the change,
   though, no line on those pages rests on them.
3. **The Must not wording.** I used "Each design can be run at any time." in place of the example
   "Each of these can be run at any time.", because on the page "these" has nothing clear to point
   to. If you prefer "Each of these", one BI-2 line and its 15 Sources quotes change together.
4. **"not to the product model" in place of "not to this model"** (kind E). On a capability page,
   "this model" has nothing clear to point to, and the pages already say "the product model"
   elsewhere.
5. **Renamed, not dropped: "seeding memory" in the four capability ICE Scope lines** (kind C).
   Putting the memory into the project is still out of scope for these capabilities, so it stays
   in each Out list under the same name as the capability's Out line. Dropping it from the lists
   would also pass the grep.
6. **Kept: Set the project's architecture, feature page, line 25.** "The project set-up step,
   initialize, will ask about the technology standards, tools and frameworks, to choose the memory
   the project gets. It is not built." It describes the initialize capability's planned set-up
   questions and uses none of the three words. The decision moves seeding memory out of BI-2. It
   does not say what initialize asks, so I left the line.
7. **Wording until BI-3 is reviewed.** Manage surfaces' capability page, line 12, now reads
   "Designing the slice stays with Design slices and with designing each slice (Design → Code)".
   The repetition goes away when the slice-design capability gets its new name.

## 4. Check results (on a scratch copy, never the live model)

The copy holds the four capability folders and bi-2.md:
`<session scratchpad>/bi2-cleanup-copy/`.

- **The request runs.** enrich-grounding's `change_lines.py` ran with exit 0 on the copy: 24 pages,
  71 changes, 13 lines removed. Before writing the request, I checked that each "old" line is on
  its page exactly once.
- **Only the named lines changed.** All 31 copy pages were compared with the live pages: 0
  mismatches. 71 lines went out and 58 came in, exactly the request's lines.
- **Structure check**
  (`python3 .claude/skills/discover-capabilities/scripts/lint_grounding.py --doc <page> --kind capability --stage directional`,
  and `--kind feature`): run on the 4 capability pages and the 11 feature pages, before and after
  the change. All 15 pages pass both times, with 0 errors and 0 warnings. ICE pages have no
  `--kind` for a single-page check, so they are covered by the line comparison and the grep.
- **Grep.** Body lines outside Sources, whole words lock, locks, locked, locking, lens, lenses,
  seed, seeds, seeded, seeding, and "only gate". The live model has 56 such lines; the copy has 1.
  That one is unsure item 1, kept on purpose.
- **Sources quotes still match.** Every quoted string in a Sources line that names one of the 31
  pages was checked against the copy's new text: 62 quotes, 0 not found.
- **Outside the scope.** No page outside the 31 quotes BI-2 or any line that changes (grep over
  `.garura/product`). So the change breaks no quote elsewhere.
- **The live model is untouched.** `git status` shows no change under `.garura/product`.

## Appendix: files

- `.garura/project/issues/1021/context/bi-2-cleanup/bi-2-page.md`: BI-2's new text, its diff, and
  the choice of skill.
- `.garura/project/issues/1021/context/bi-2-cleanup/change-lines-request.json`: one request for
  `change_lines.py`, 24 pages and 71 changes, with BI-2 first. `source` holds the product owner's
  words.
- Line numbers of every change, by kind:
  - BI-2: intents/bi-2.md:3, intents/bi-2.md:5, intents/bi-2.md:11, intents/bi-2.md:12, intents/bi-2.md:14
  - A: design-technology-architecture/capability.md:46, design-technology-architecture/fn-set-architecture/feature.md:49, design-technology-architecture/fn-update-architecture/feature.md:39, manage-surfaces/capability.md:55, manage-surfaces/fn-declare-surfaces/feature.md:57, manage-surfaces/fn-update-surfaces/feature.md:39, deployment-design/capability.md:68, deployment-design/fn-cloud-cartridges/feature.md:39, deployment-design/fn-design-how-project-runs/feature.md:69, deployment-design/fn-update-deployment/feature.md:44, environment-setup/capability.md:63, environment-setup/fn-build-environment/feature.md:47, environment-setup/fn-declare-environments/feature.md:58, environment-setup/fn-dev-sandbox/feature.md:58, environment-setup/fn-update-environments/feature.md:42, design-technology-architecture/capability.md:59, manage-surfaces/capability.md:71, deployment-design/capability.md:87, environment-setup/capability.md:81
  - B: design-technology-architecture/capability.md:45, design-technology-architecture/fn-update-architecture/feature.md:41, design-technology-architecture/fn-update-architecture/feature.md:58, manage-surfaces/fn-update-surfaces/feature.md:41, manage-surfaces/fn-update-surfaces/feature.md:62, deployment-design/capability.md:66, deployment-design/fn-update-deployment/feature.md:46, deployment-design/fn-update-deployment/feature.md:71, environment-setup/capability.md:59, environment-setup/fn-update-environments/feature.md:43, environment-setup/fn-update-environments/feature.md:65, manage-surfaces/capability.md:54, design-technology-architecture/fn-update-architecture/ice.md:16, manage-surfaces/fn-update-surfaces/ice.md:15, deployment-design/fn-update-deployment/ice.md:16, environment-setup/fn-update-environments/ice.md:16
  - C: design-technology-architecture/ice.md:17, manage-surfaces/ice.md:15, deployment-design/ice.md:16, environment-setup/ice.md:16
  - D: design-technology-architecture/capability.md:39, design-technology-architecture/fn-set-architecture/feature.md:65, manage-surfaces/capability.md:12, manage-surfaces/capability.md:48, manage-surfaces/fn-declare-surfaces/feature.md:75, deployment-design/capability.md:57
  - E: design-technology-architecture/capability.md:42, design-technology-architecture/fn-set-architecture/feature.md:68, deployment-design/capability.md:64, environment-setup/capability.md:57, manage-surfaces/capability.md:51
  - F: design-technology-architecture/capability.md:66, design-technology-architecture/fn-set-architecture/feature.md:74, design-technology-architecture/fn-update-architecture/feature.md:64, manage-surfaces/capability.md:78, manage-surfaces/fn-declare-surfaces/feature.md:84, manage-surfaces/fn-update-surfaces/feature.md:68, deployment-design/capability.md:95, deployment-design/fn-cloud-cartridges/feature.md:67, deployment-design/fn-design-how-project-runs/feature.md:108, deployment-design/fn-update-deployment/feature.md:77, environment-setup/capability.md:90, environment-setup/fn-build-environment/feature.md:78, environment-setup/fn-declare-environments/feature.md:90, environment-setup/fn-dev-sandbox/feature.md:89, environment-setup/fn-update-environments/feature.md:72, deployment-design/capability.md:99
