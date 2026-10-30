# Feature: A person adds a new feature found while a plan is in progress, to the model, its slice and its epic

## What it does
While working on a plan, a person finds a feature the plan did not know about and says so in the /update-plan session, in their own words. The play works out the feature's capability, slice and epic, shows it, and asks before it joins the running list, because a model change is big. It lands with everything else on one plain "approved": the feature joins the product model under its capability with a thin ICE, its slice, its epic and its story, and the plan file and GitHub agree with it.

## Inputs / Outputs
- Input: the person's own words in the /update-plan session that name a feature found while the plan is in progress.
- Input: the person's plain "approved" for the whole running list.
- Output: the new feature in the product model under its capability, with a thin ICE and both thin marks, linked to the business intent and to the issue that found it.
- Output: the feature in its slice, and its story under that slice's epic when the plan has one, on the epic's feature-to-story list.
- Output: the plan file, GitHub and the model agree.

## Rules & behavior
- The play shows the new feature, with its capability, slice and epic, and the person confirms it before it joins the running list.
- Nothing reaches the model, GitHub or the plan file before a plain "approved".
- The model is written only through the model sub-agent and its skills (the page skill, then link-model-part), never by hand.
- The feature lands with everything else on the one "approved".
- When the feature does not fit a slice, the person is told and offered what works.
- Bugs, chores and spikes never change the model.

## Acceptance criteria
- Given a test session that names one new feature, when the person has not yet approved, then nothing has changed.
- Given the same session, when the person approves once, then the feature's page holds its thin ICE, its page and model entry both carry the thin mark, it is linked to the intent and to the issue that found it, and its story sits under its slice's epic and on the epic's list.
- Given the landing, when the plan file, GitHub and the model are compared, then the compare finds no difference.

## Out of scope
- Shaping a new slice: that is /shape-slice's.
- Writing an eval scenario: the eval scenarios for the feature are owed to /shape-eval afterwards.
- Changing work already in the plan.
- The session itself (#730) and the thin page and model entry of a part found during work (#979): this feature uses them.

## Sources
- The approved /update-plan session on plan 717, entry 3: "A person adds a new feature found while a plan is in progress, to the model, its slice and its epic"
- Issue #931, the story that found it

Thin: proposed by `/shape-slice` from the person's answers; deepen with `/discover-capabilities`.

## Agent intent (ICE)
- Goal: After the person's plain "approved", the new feature is in the product model under its capability, with a thin ICE and both thin marks, linked to the business intent and to the issue that found it, in its slice and with its story under that slice's epic when the plan has one; and the plan file, GitHub and the model agree.
- Limit: Nothing reaches the model, GitHub or the plan file before a plain "approved".
- Limit: The model is written only through the model sub-agent and its skills (the page skill, then link-model-part), never by hand.
- Limit: It shapes no new slice, writes no eval scenario (it names them as owed for /shape-eval), and never changes work already in the plan.
- Limit: Bugs, chores and spikes never change the model.
- Fails if: the feature reaches the model, GitHub or the plan file before the person's plain "approved".
- Fails if: the feature lands in the model but not in the plan file or GitHub, or in those but not in the model.
- Fails if: the feature lands with no thin ICE, or with only one of the two thin marks.
- Fails if: the feature has no link to the business intent, or no record of the issue that found it.
- Fails if: the feature joins a slice it does not fit, and the person was not told and offered what works.
- Fails if: after the landing, the epic's feature-to-story list does not match the plan file.
- Fails if: the feature joins the running list without being shown and confirmed first.
- Context: A builder or the product owner works on a plan and finds a feature the plan did not know about. In the /update-plan session they say so in their own words; the play works out its capability, slice and epic, shows it, and asks before it joins the running list, because a model change is big. It lands with everything else on one "approved". It builds on the session (#730) and uses the landed model skills for a part found during work (#979's thin page and spine entry). The eval scenarios for the feature are owed to /shape-eval afterwards.
- Checked by: A test session that names one new feature, approved once: before approval nothing changed; after it, the feature's page holds its thin ICE, its page and model entry both carry the thin mark, it is linked to the intent and to the issue that found it, its story sits under its slice's epic and on the epic's list, and the compare of the plan file, GitHub and the model finds no difference.
