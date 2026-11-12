# Need

In the product owner's words (2026-11-12, accepting ADR 067): update the rule so a play finds a feature's story through the model when no plan file marks it; mark a feature built when its story is closed, and do not stop.

What ADR 067 (`docs/adr/067-a-play-finds-a-features-story-by-the-issue-the-model-names-when-no-plan-file-marks-it.md`, accepted, #1048) needs in the ontology:
1. The Feature kind gains the property `issue`: the Story filed for that feature in the tracker (optional, one value).
2. Story R3, Q20 and the Plan rule: a play finds a feature's Story by the plan file's `represents` mark, or, when the plan file marks none, by the feature's `issue` (of type Story; open means it is used and moved under the slice's epic, shown before the yes; closed means the feature is already built; never by title). An Epic is still found only by the plan file.
3. The Story kind's "one Story for each Feature in each Epic", and the Feature kind's "In the tracker as" line and its Clinic example: not for a feature whose `issue` names a closed Story (already built).

Issue: #1050 (a Chore under #1025).

## Touches
Feature
Story
Plan
