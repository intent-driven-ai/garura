Thin: proposed from the person's words; deepen with `/discover-capabilities`.

## Intent
- Goal: As the findings move, the product model changes, or the product owner changes which kinds of change may go ahead on their own, the recommendations and the changes in flight are updated on their own: a waiting one shows its findings' weight before and after, one whose part was merged or retired is worked out again or withdrawn with why, one another change already met is withdrawn naming it, a turned-down one is raised again only when its findings move, and a landed change whose findings faded becomes a new recommendation to take it back; what held before stays readable with why it changed, so that the recommendations stay true to what consumers want now.
- Limit: What held before is never written over or deleted; a withdrawn recommendation stays readable with why.
- Limit: A landed change is never undone by an update, and a setting change applies only to what has not gone ahead yet.
- Limit: It writes only its own recommendations and their records: no page, link, work item or memory changes.
- Fails if: A recommendation's earlier form, or why it changed, can no longer be read, or a recommendation was deleted instead of withdrawn.
- Fails if: A waiting recommendation stays on a part that the model merged or retired.
- Fails if: An update undid a landed change, or the setting alone took back a change that had gone ahead.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the findings as updated with what held before, the product model as it is now, the recommendations and changes with their records, and the project's setting for which kinds of change may go ahead on their own and for when a want counts as faded.
- Never read: the connected tools and forums themselves, production, anything that would bring back who a person is, and any ICE page.
- Persona: the product owner, who wants the recommendations kept true to what consumers want now, with how each one moved.
- Scope: In: updating, working out again, withdrawing and raising again the recommendations as findings, the model and the setting change, and keeping what held before. Out: updating the findings, changing the model, and changing the setting.

## Expectation
- Scenario: A team's planning tool merges two capabilities. A waiting recommendation for a new feature on the old one is worked out again on the merged one, with why, and its old form stays readable. A want for a print button fades after a change landed that met it, and its waiting recommendation is withdrawn, naming that change. A recommendation for a calendar view, turned down while its want was weak, is raised again when the want grows strong, showing what moved.
- Done means: Someone other than the one who made the updates reads the recommendations and their records, and finds every earlier form readable with why it changed, none on a merged or retired part, none deleted, and no landed change undone by an update.
