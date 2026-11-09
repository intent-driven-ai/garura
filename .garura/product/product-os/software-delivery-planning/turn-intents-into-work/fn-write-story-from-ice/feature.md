# Feature: Write a story from its ICE

## What it does
This feature writes the words of a story. A story is the work item, an issue in the team's tracker, that stands for one feature and delivers it. Its words come from the feature's ICE and that feature's capability's ICE. An ICE is the agent's intent for one capability or feature: what an agent must make true there, for whom, and how it is checked.
The story gets a title, a scope of work and Context guidance:
- The scope of work says what the feature must do (its goals), the limits it must stay inside, and what is expected when it is done.
- The Context guidance says what to read, what never to read, who the work is for, and what is in and what is out.
Every line of the two ICE goes into the story, in the story's own words, except the "Fails if" lines, which say how the work fails.
It runs inside Cut an intent into epics and stories for each story of a new set of work items, and inside Change the work items for one story a person asks for.
The feature exists because the builder reads the story's title, goals, limits and Context guidance, the test writer reads its expectations, and neither reads the ICE. The story is where the model's intent reaches the agent.

Status: built.

## Inputs / Outputs
- In: one clean copy for each feature: its ICE and its capability's ICE, with every "Fails if" line and every line under it taken out. A script writes the copy, and the copy names no ICE page.
- In: the slice's name and outcome, and each feature's name and one line. A slice is an ordered group of features that one person can test end to end.
- In, on a second round: the problems the check found, or the product owner's change in their own words.
- Out: for each feature, a draft story with its title, goals, limits, expectations and the four Context lines.
- Out: the check's answer: ok, or each problem with the slice and the feature it is in.

## Rules & behavior
- The writer reads only the clean copies and the list of slices and features. It never opens an ICE page. The reason: an ICE page holds the "Fails if" lines, and the eval judges the build by them.
- The writer uses every line of the clean copy. The reason: the builder never opens the ICE, so a line the story leaves out never reaches the build.
- The Context guidance says where to look, never the facts. The reason: Gather the work under a chosen plan item collects the context when it gathers the work and puts it in the issue's short-term memory, so the builder reads it in one place.
- The writer never writes a failure condition, a recovery condition, the words "Fails if", or the phrases that say who fixes a failure. A limit says what the feature must stay inside; it is not a failure said the other way round. The reason: these belong in the slice's hidden file, which no builder reads.
- A script checks every draft before anyone sees it. Each story needs a title, the three parts of the scope of work and the four Context lines. The script reads the original ICE pages itself and refuses any line of a "Fails if" block, the words "Fails if" or a recovery phrase. A failed check sends back only the stories it names. The reason: the writer never saw the failure lines, so only a reader that has them can prove none got in.
- A story is drafted only from a ready ICE. The reason: work cannot start from a missing part, or from an intent no person confirmed.
- Plain words and personas, and no real names. The reason: people read the story in the tracker, and the eval reads it to write its tests.
- Not built: no check stops a story or its Context guidance from naming the eval, the hidden file or the folder that holds them, though an older page of the model sets that rule.
- Not built: no builder reads a story yet. The step that reads the Context guidance and collects the context is not built. It is Collect each story's context from its guidance, in Gather the work under a chosen plan item.

## Acceptance criteria
- Given a feature whose two ICE are ready, when its story is drafted and checked, then the story has a title, goals, limits, expectations and the four Context lines.
- Given a draft that holds a line of a "Fails if" block of its ICE, when the check runs, then it names that story and the draft goes back to the writer.
- Given the clean copies of a run, when they are searched for "fails if" and for the name of an ICE page, then nothing is found.

## Out of scope
- Which stories exist, and filing them in the tracker. Cut an intent into epics and stories (fn-cut-intent-into-work) and Change the work items (fn-change-work-items) do this.
- The slice's hidden file, written from the "Fails if" lines. Write the evals that check the work writes it, just before the evals.
- Writing or deepening the ICE itself. Specify the product does this.
- Collecting the context when the work is gathered. Collect each story's context from its guidance, in Gather the work under a chosen plan item, does this.

## Sources
- core/components/skills/author-work-items/SKILL.md: "Never open any other file, and never an ICE page: those pages hold the failure lines, which are not yours to read."
- core/components/skills/author-work-items/SKILL.md: "Use every line of the two ICE that the clean copy holds.", "Say where to look; never copy the facts themselves.", "A limit says what the feature must stay inside; it is not a failure said the other way round."
- core/components/skills/author-work-items/SKILL.md: "Rewrite only the slice or story each problem names, and keep every other draft as it is."
- core/components/plays/shape-plan/scripts/gather_plan.py: "block taken out: the line and every line under it", "The clean copy names no ICE page."
- core/components/plays/shape-plan/scripts/check_drafts.py: "read from the original ICE pages that gather.json names"
- core/components/plays/update-plan/scripts/feature_ice.py: "`body` checks the story the writer drafted, the same way /shape-plan checks its drafts"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "The builder reads the story and that collected context, and never an ICE page."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "When the build play runs, its context sub-agent reads the story's Context guidance, collects the context, and puts it in the issue's short-term memory"
- .garura/product/product-os/software-delivery-planning/cap-718/fn-818/feature.md: "A story never names the eval, the hidden file or the plan's evals folder."
- core/components/plays/shape-plan/reference/ice.md: "No story, no epic and no plan file holds a failure condition or a recovery condition."
- GitHub #1002 (closed): a story added in a plan session is drafted from the feature's ICE.
