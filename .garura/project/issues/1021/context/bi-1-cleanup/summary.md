# BI-1 clean-up: what changes and why (draft)

This is a draft. Nothing in the product model, on GitHub or in git was changed. It lists every line on the
approved Product → Spec (BI-1) pages that the product owner's decisions made while building BI-2 and BI-3 make
wrong, and gives the new words for each line. The decisions are in
`.garura/project/issues/1021/context/capabilities.md` (the notes under "Spec → Design" and "Design → Code") and
in the approved BI-3 pages:

1. The lens wording is gone, and BI-3's five capabilities replace "Design slices", "Use the lenses on each
   slice", "Design for evaluation and testing" and "Bring the design together for a vertical slice". "Build the
   work" is now "Build the work test first". Choosing the slice leaves Design → Code; its place is settled when
   Orchestrate agent work through planning is reviewed.
2. The builder never sees a test, an eval or a story's expectations. Gather the work under a chosen plan item
   splits each story: the builder gets the title, goals, limits and Context guidance, and the test writer gets
   the expectations.
3. Write the evals that check the work writes the slice's hidden file, just before the evals.
4. Gather the work under a chosen plan item collects each story's context (Collect each story's context from
   its guidance), not the build.
5. No design lock or gate, and seeding memory is not the model's.

**The pages in scope.** 48 pages: 3 capabilities and 21 features, each with its page and its ICE page.

**What changes.** 23 lines on 6 pages. No line is removed: each of the 23 is replaced, and only the wrong part of
each line changes. The other 42 pages need no change: all 26 Specify the product pages, 11 of the 12 Keep the
spec matched pages, and 5 of the 10 Turn intents into agent work pages (Change the work items, both pages, and
the ICE pages of Cut an intent into epics and stories, Write a story from its ICE and Add a feature found
during work). No BI-1 page uses the lens wording, the dropped lock or memory seeding, so decisions 1 (its lens
part) and 5 change nothing here.

**Who writes it.** enrich-grounding's named-lines script (`change_lines.py`) makes all 23 changes in one
all-or-nothing run, from `change-lines-request.json`.

## The pages

| Page | Lines changed |
|------|---------------|
| Turn intents into agent work: capability.md | 9 |
| Turn intents into agent work: ice.md | 1 |
| Cut an intent into epics and stories: feature.md | 4 |
| Write a story from its ICE: feature.md | 5 |
| Add a feature found during work: feature.md | 3 |
| Update the spec to match what's built: feature.md | 1 |

Each line is counted once, under its main kind. Three lines carry two kinds (noted below).

## Each kind of change

### A. The hidden file: Design slices becomes Write the evals that check the work: 6 lines on 4 pages

Two of these lines also name who chooses the slice (kind E), and two also name who writes the eval (kind B).

Before (`software-delivery-planning/turn-intents-into-work/capability.md`, line 51):

> - Each line of an ICE has one reader. The "Fails if" lines go to the slice's hidden file, which Design slices writes. Every other line goes to the story. The reason: each line then has one meaning, so the story and the eval never disagree.

After:

> - Each line of an ICE has one reader. The "Fails if" lines go to the slice's hidden file, which Write the evals that check the work writes just before the evals. Every other line goes to the story. The reason: each line then has one meaning, so the story and the eval never disagree.

Lines: capability.md 42 and 51; Cut an intent into epics and stories 42; Write a story from its ICE 39; Add a
feature found during work 29 and 39.

### B. The eval: Design for evaluation and testing becomes Write the evals that check the work: 2 lines on 2 pages

Before (`software-delivery-planning/turn-intents-into-work/fn-cut-intent-into-work/feature.md`, line 43):

> - The eval that tests the slice. Design for evaluation and testing writes it.

After:

> - The eval that tests the slice. Write the evals that check the work writes it.

Lines: capability.md 43; Cut an intent into epics and stories 43.

### C. Collecting the context: the build becomes Gather the work under a chosen plan item: 5 lines on 2 pages

Before (`software-delivery-planning/turn-intents-into-work/fn-write-story-from-ice/feature.md`, line 41):

> - Collecting the context when the build runs. Build the work does this.

After:

> - Collecting the context when the work is gathered. Collect each story's context from its guidance, in Gather the work under a chosen plan item, does this.

Lines: capability.md 20 and 52; Write a story from its ICE 24, 30 and 41.

### D. What the builder reads: its part of the story, not the whole story: 4 lines on 3 pages

Before (`software-delivery-planning/turn-intents-into-work/capability.md`, line 37):

> - In: writing each story from its feature's ICE and its capability's ICE. The builder reads the story and never the ICE, so this is where the intent reaches the agent.

After:

> - In: writing each story from its feature's ICE and its capability's ICE. The builder reads the story's title, goals, limits and Context guidance, never its expectations or the ICE, so this is where the intent reaches the agent.

Lines: capability.md 31 and 37; ice.md 21; Write a story from its ICE 10.

### E. Choosing the slice: Design slices is gone, and no new owner is named: 3 lines on 3 pages

The owner is not named because where the plan is made is settled when Orchestrate agent work through planning
is reviewed. The jobs the slice step does today (a thin ICE where a slice needs one, an intent's page from its
issue) are given to "the step that chooses the slice".

Before (`software-delivery-planning/turn-intents-into-work/fn-add-found-feature/feature.md`, line 38):

> - Designing a new slice. Design slices does it.

After:

> - Choosing a new slice. It left Design → Code, and its place is settled when Orchestrate agent work through planning is reviewed.

Lines: capability.md 44; Add a feature found during work 38; Update the spec to match what's built 55.

### F. The slice is shaped, not designed: 2 lines on 1 page

Before (`software-delivery-planning/turn-intents-into-work/fn-cut-intent-into-work/feature.md`, line 6, start of the line):

> It runs as /shape-plan, once for each intent, after the slice is designed. ...

After:

> It runs as /shape-plan, once for each intent, after the slice is shaped. ...

Lines: Cut an intent into epics and stories 6 and 23.

### G. Build the work becomes Build the work test first: 1 line on 1 page

Before (`software-delivery-planning/turn-intents-into-work/capability.md`, line 45):

> - Out: breaking a story into tasks and building it. Build the work owns the build. Today /build-epic cuts an epic into stories, tasks, tests and docs inside the build.

After:

> - Out: breaking a story into tasks and building it. Build the work test first owns the build. Today /build-epic cuts an epic into stories, tasks, tests and docs inside the build.

Totals: A 6 + B 2 + C 5 + D 4 + E 3 + F 2 + G 1 = 23.

### Left alone, as asked

- Sources lines that quote other files as they still stand. No quoted file changed in a way that breaks a quote
  (see the checks), so no Sources line changes.
- "Known break" and "Not built" lines about filed issues and missing checks, which are still true.
- "The capability list the product owner locked on 2026-11-03": there, "locked" means agreed.
- "A capability seeded here" (Specify capabilities, line 21): seeding a capability from a person's answers, not
  memory.

## Lines I was unsure of

1. **Kept a sentence, and added one: Turn intents into agent work, capability page, line 20.** "The build step
   that reads a story's Context guidance and collects its context is not built." is quoted word for word by two
   approved BI-3 pages (Gather the work under a chosen plan item, Sources line 71, and Collect each story's
   context from its guidance, Sources line 54). Rewriting it would break those quotes, which are outside this
   scope. So the sentence stays, and a new sentence after it names the new owner: "That step is now Collect each
   story's context from its guidance, in Gather the work under a chosen plan item." The same claim on Write a
   story from its ICE (line 30) is not quoted elsewhere, so there it is rewritten.
2. **"designed" to "shaped" (kind F).** These two lines do not name Design slices. But Design the work now runs
   after the plan, so "after the slice is designed" would read as if the plan came after the design. They could
   also stay as they are.
3. **"The step that chooses the slice" (kind E).** It names no capability, by the rule that nothing moves until
   Orchestration is reviewed. Making a thin ICE where a slice needs one, and writing an intent's page from its
   issue, are the slice play's jobs today; who owns them later is open.
4. **Only the build's owner changed on capability line 45.** BI-3 has no step that breaks a story into tasks
   (Design the work designs every story in one design). The /build-epic sentence still describes the stale play
   correctly, so it stays.
5. **Kept: "a new builder, who never saw the prototype, builds the product from the intents and the model
   alone"** (Specify the product, capability line 37, and its ICE line 20). This is the rebuild test's agent,
   not the builder of a story, so decision 2 does not reach it.
6. **No Sources line added.** The new owner names rest on capabilities.md and the BI-3 pages, which these pages
   do not quote. The BI-2 clean-up added none either. If a page should back them, one Sources line per page that
   quotes the Design → Code note would do it.

## Check results (on a copy in the session scratchpad, never the live model)

The copy holds the three capability folders, all 48 pages.

- **The request runs.** `change_lines.py` exited 0 on the copy: 6 pages, 23 changes, 0 lines removed. Before
  writing the request, each "old" line was checked to be on its page exactly once.
- **Only the named lines changed.** All 48 copy pages were compared with the live pages: 42 are the same, and on
  the other 6, 23 lines went out and 23 came in, exactly the request's lines.
- **Structure check** (`python3 .claude/skills/discover-capabilities/scripts/lint_grounding.py --doc <page> --kind capability --stage directional`,
  and `--kind feature`), on the 5 changed part pages (1 capability, 4 features), before and after the change:
  all pass both times, with 0 errors and 0 warnings. The one changed ICE page has no `--kind` for a single-page
  check, so the line comparison covers it.
- **Sources quotes on the changed pages.** 83 quotes on the 5 changed pages that have a Sources section, each
  checked against the file it names (model pages in scope read from the copy, Phoenix memory read through the
  memory tool): 83 match, 0 not found. 11 Sources lines name no file (the product owner's words, GitHub issues,
  a list of old model parts) and were not checked. The checker was tested with one planted wrong quote and found
  it.
- **Quotes of the changed pages from other pages.** 16 quotes across the model name one of the 6 changed pages
  (12 on BI-3 pages, 4 on Keep the spec matched pages): all 16 still match the copy.
- **Grep.** Body lines outside Sources that name Design slices, Design for evaluation and testing, Build the
  work, "the build collects", "build step", "the slice is designed" or the builder reading the whole story: 23
  in the live model, 1 in the copy (unsure item 1, kept on purpose).
- **The live model is untouched.** `git status` shows no change under `.garura/product`.

## Appendix: files and line numbers

- `.garura/project/issues/1021/context/bi-1-cleanup/change-lines-request.json`: one request for
  `change_lines.py`, 6 pages and 23 changes. `source` names the product owner's decisions and the approved BI-3
  pages.
- Line numbers by kind (pages under `software-delivery-planning/turn-intents-into-work/` unless named):
  - A: capability.md:42, capability.md:51, fn-cut-intent-into-work/feature.md:42, fn-write-story-from-ice/feature.md:39, fn-add-found-feature/feature.md:29, fn-add-found-feature/feature.md:39
  - B: capability.md:43, fn-cut-intent-into-work/feature.md:43
  - C: capability.md:20, capability.md:52, fn-write-story-from-ice/feature.md:24, fn-write-story-from-ice/feature.md:30, fn-write-story-from-ice/feature.md:41
  - D: capability.md:31, capability.md:37, ice.md:21, fn-write-story-from-ice/feature.md:10
  - E: capability.md:44, fn-add-found-feature/feature.md:38, software-delivery-planning/keep-spec-matched/fn-update-spec-to-match-built/feature.md:55
  - F: fn-cut-intent-into-work/feature.md:6, fn-cut-intent-into-work/feature.md:23
  - G: capability.md:45
