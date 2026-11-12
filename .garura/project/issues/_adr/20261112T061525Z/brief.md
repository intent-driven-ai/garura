## Decision

One tracker issue per feature, linked one way from the issue to the product model. This supersedes ADR 067.

1. **The model holds no issue number.** The product model holds no tracker issue number. The `issue` field on features is removed, and the 23 values now in Garura's model are deleted. No play or skill writes it again.
2. **Three units of work.** In the tracker there are three units of work: Epic, Feature and Story.
   - Each product feature has exactly one Feature issue. It names its feature in its text (`Represents: <feature id>`), so the link runs one way, from the issue to the model.
   - A Story always sits inside a Feature issue.
   - Bug, Chore and Spike stay as they are today.
3. **How a play finds a feature's issue.** A play finds it by the plan file's mark. When the plan file marks none, the play finds the Feature issue in the tracker that names the feature. It never finds an issue by its title. It never makes a second issue for one feature or one story.
4. **Slices and plans are groups.** They are many-to-many with features: two slices, or two plans, can hold the same feature. A slice pulls in only features that are not yet built. A Feature issue sits under one epic at a time. When a second epic needs it, the play asks the person which epic it goes under.
5. **A built feature.** When a feature is built (its Feature issue is closed), every slice and plan that holds it counts it as complete.
6. **An orphan Story.** A Story with no Feature issue as its parent is matched to its feature by researching the product model. When no feature exists yet, the feature is created and its Feature issue is filed.

## Why now

ADR 067, accepted earlier on 2026-11-12, put the link in the model: a feature named its story's issue. At checkpoint 1 of the ontology change (#1050), the product owner corrected the model:
- A link held on both sides drifts and costs upkeep, so the issue alone carries the link.
- Each unit of work is one issue, never duplicated.
- Slices and plans only group features.

/shape-plan's fix for #1025 (PR #1047) and the plan rebuild for business intent 1 wait on this rule.

## Options considered

- **One issue per feature, linked from the issue to the model (chosen).** It gives one place to look, a link with one side to keep, and no duplicates.
- **ADR 067: the model holds the feature's story issue.** Lost: the link has two sides to keep in step, and the model drifts from the tracker. The product owner prefers no two-way links.
- **One Story for each feature in each epic (the older rule in ADR 048 and ADR 049).** Lost: it files a second issue for the same feature whenever a second slice holds it.
- **Match an issue by its title.** Lost: titles change, so a renamed issue would be filed again.

## Decided by

The product owner, 2026-11-12, at checkpoint 1 of the ontology change for #1050.

## Decided in

Issue #1051 (a Chore under #1025, "/shape-plan reuses an open story for a feature instead of filing a second one").

## Shape

markdown

## Change at acceptance (the product owner, 2026-11-12: "change 1-6")

1. Narrow part 1: no feature carries a tracker issue number. Intent pages keep their "Tracker:" line; ids stay.
2. The Feature issue holds the feature's scope of work and Context guidance, written from its ICE; Stories are the pieces of work inside it. The epic's feature-to-story map names Feature issues (one line per feature).
3. Closing a Feature issue is a person's call, through /reshape-plan "finish". No roll-up (ADR 064 stands).
4. A play matches only issues of type Feature that carry the exact `Represents: <feature id>` line. Two Feature issues naming one feature is a duplicate: the run stops and asks the person.
5. Clean-up (work this creates, before the 23 model values are deleted): map each open issue of type Feature to its product feature by adding the `Represents:` line, or retype it.
6. The same clean-up files or links a Feature issue for each of the 23 features whose stories lose their only link, before the values are deleted.
