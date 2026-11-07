# Feature: Update the spec to match what's built

## What it does
When the work changes what the product does, the pages of the spec that it makes out of date are updated to say what the product now does.
- The spec is what the product model says the product is for and what it does. The product model is the shared map of the product that people and agents read. Each part of the spec has a page:
  - A business intent is what a person or the organisation wants, in their own words.
  - A domain is a big area of the product that groups capabilities. A capability is something the product can do. A feature is one thing a person can do inside a capability.
  - An ICE is the agent's intent for one capability or feature: what an agent must make true there, for whom, and how it is checked. It has its own page beside its part's page.
- The update starts from one of two things:
  - A change to the work. The agents built or changed something and it landed, or the planned work changed. The planned work is the work items in the team's tracker, the tool where a team keeps its issues, such as GitHub, and the plan files that hold them as a tree.
  - A drift that was found. Drift is a place where a page and the work no longer say the same thing. Find where the spec and what's built no longer match (fn-find-spec-drift) will find drift across the whole spec. Today a person or an agent finds it during the work.
- For each page that is out of date, the new words describe what the work now does. A person reads them and approves them, and only then do they go on the page. The update can change a few lines of a page or replace the whole page.
- The two sides of the spec follow different things:
  - A domain, capability, feature or ICE page follows what was built. Its new words describe the work as it is now.
  - An intent page follows the person. When an intent and the work disagree, the person decides whether the intent changes or the work changes.
- An intent keeps its record of what was done for it through every change of its words.
- The feature exists because agents decide from the spec. When the work moves on and the pages stay behind, the agents build from a description of a product that is no longer there. This feature is how the pages catch up with the work.

Status: built in part. A person's approved words can go on any page of the spec, a few lines or a whole page, all or nothing. An intent page can be rewritten from approved words, and its record of what was done is kept. Not built: a step that, after a change lands, finds the pages it made out of date. Today a person asks for each update by hand. Also not built: keeping an intent's list of Sources on a rewrite, and adding to an intent's record of what was done as work finishes.

## Inputs / Outputs
- In: a change that landed: what the agents built or changed, the work item it came from, and the parts of the spec it touches.
- In: a change to the planned work: a work item added, moved, dropped or rewritten in the tracker or in a plan file.
- In: a drift that was found: the page, what it says, what the work shows, and where each comes from.
- In: the new words for each page that a person approved, and the name of that person. For an intent, the person's decision: the intent changes, or the work changes.
- Out: each page that was out of date now says what the work does, in the words the person approved. Every other line on it is as it was.
- Out: an intent page that changed still holds its record of what was done. It reads proposed, unless the person who confirmed the new words is named.
- Out: a record of each page that changed, with each changed line before and after, and the person who approved it.
- Out: the follow-on changes it causes, each handed to the feature that owns it: an intent's issue in the tracker, a link between an intent and a part, and a story whose ICE changed.

## Rules & behavior
- Only words a person approved go on a page. This is true for a few lines and for a whole page. The reason: the spec is what the person approved and what agents decide from. Words that nobody approved would change both, and nobody would know.
- What was built is the ground truth for domains, capabilities, features and their ICE. When their pages and the work disagree, the new words describe the work as it is, not as the page said it would be. The reason: agents decide from the model, so a page that describes work that is not there leads them in the wrong direction.
- An intent changes only when the person decides it. A difference between an intent and the work goes to the person, who decides whether the intent or the work changes. An agent never rewrites an intent to match the code. The reason: an intent says what the person wants. An intent rewritten to match the code would say what the agent built, not what the person asked for.
- An intent reads confirmed only when the person who confirmed its new words is named. A rewrite that names nobody goes back to proposed, whatever the page said before. The reason: only a person confirms or drops a business intent.
- The record stays. When an intent's words change, its record of what was done stays as it was. Its list of the parts it touches also stays, unless the new words give a new list. The reason: the words are new, but what happened to the intent is history.
- Nothing is fixed in silence. Each page that is out of date is named to a person, with what it says and what the work shows, before any word changes. The reason: a silent fix changes what the person approved without their knowledge.
- An update is all or nothing. Each line it changes must be on its page, all checks run before the first write, and if a write fails, every page goes back to how it was. Every line the update does not name stays word for word. The reason: half an update leaves pages that say something nobody approved.
- Each follow-on change goes to the feature that owns it. A changed intent's issue goes to Keep the tracker's words matched to the model (fn-keep-tracker-matched). A link between an intent and a part goes to Keep an intent's links current (fn-keep-intent-links-current). A story whose ICE changed goes to Turn intents into agent work. The reason: each part then has one writer and one set of checks.
- Not built: finding the pages that a landed change makes out of date. Nothing runs after a change lands to find the parts it touched and the pages it made out of date. Today a person or an agent sees it and asks for the update. A change that nobody sees leaves the spec behind. An older play that was written to bring the model up to match what shipped waits for a rebuild.
- Not built: a rewrite keeps the intent's Sources. A Source is a saved copy of what a person gave, such as a file, a document or their own words. An intent that discovery saved lists its Sources, and a rewrite drops that list. The rewritten intent then loses its link to what the person gave.
- Not built: the record grows as the work finishes. An intent's page is meant to record what was delivered for it and the value of each piece, with links to the finished work items. No step adds to it, so each page reads "(nothing yet)", and no page of the spec says what was built for an intent. Nothing marks an intent met when its proof holds either. An intent is met by its proof, never because its work is finished.

## Acceptance criteria
- Given a landed change after which a capability no longer keeps a rule that its page states, when the person approves the new words, then the page states what the capability does now, and every other line on the page is as it was.
- Given a page that is out of date and new words that no person approved, when the update is asked for, then the page does not change.
- Given an intent that the work no longer matches, when the difference is named, then the intent page does not change until the person decides, and the decision names that person.
- Given an intent rewritten from approved words with no confirming person named, when the rewrite lands, then the page reads proposed.
- Given an intent with a record of what was done, when its words change, then the record is on the page as it was before.
- Given an update that names a line that is not on its page, when it runs, then no page changes and the person is told the page and the line.
- Given an intent that discovery saved with its Sources, when its words are rewritten, then its Sources are still on the page. This is not built.
- Given a change that lands and makes a feature's page out of date, when it lands, then that page is named to a person as out of date. This is not built.

## Out of scope
- The first page of an intent or a part. Specify the product writes it from what a person gives, and Design slices writes an intent's page from its issue when the model has none.
- A feature found while its work goes on. Add a feature found during work (fn-add-found-feature), in Turn intents into agent work, puts it in the model.
- Finding drift across the whole spec. Find where the spec and what's built no longer match (fn-find-spec-drift) will do it.
- The link between an intent and the parts that serve it. Keep an intent's links current (fn-keep-intent-links-current) keeps it on both sides.
- An intent's issue in the tracker. Keep the tracker's words matched to the model (fn-keep-tracker-matched) does it.
- A story whose ICE changed, and any other work item. Turn intents into agent work changes the work items.
- What users say once the product runs. The Run → Product business intent (BI-6) asks for it.

## Sources
- The product owner on 2026-11-07, on this feature: "this feature is about keeping the specs updated to meet the implementation", "we also have to make sure that whatever is on the page is meeting the capability"
- The capability page the product owner approved on 2026-11-07: "What was built is the ground truth for the domains, capabilities and features.", "An intent changes only from a person's approved words.", "Never: fix drift in silence."
- GitHub #977 (open): "The product model falls behind the work.", "What was built is the ground truth: the model is brought up to match it, not the other way round"
- core/components/skills/author-intent-page/SKILL.md: "It drafts nothing.", "It never confirms by itself.", "a rewrite with no stage goes back to proposed, whatever the old page said", "A rewrite keeps the old page's What-was-done"
- core/components/skills/author-intent-page/SKILL.md: "Used through product-os-keeper by any play or run that has a person's approved words for an intent page."
- core/components/skills/author-intent-page/scripts/write_page.py: "It keeps the old page's What-was-done block"
- core/components/skills/enrich-grounding/SKILL.md: "on any page — domain, capability, feature or intent — update and fix mode can instead change only the lines a request names", "change of meaning is the person's or an approved design's"
- core/components/skills/enrich-grounding/scripts/change_lines.py: "exactly those lines and keeps every other line word for word", "Every named line must be on its page exactly once"
- core/components/skills/enrich-grounding/scripts/write_approved.py: "This script copies each approved text to its page exactly as it is.", "It decides nothing and composes nothing."
- core/components/plays/discover-intent/scripts/persist_intent.py: 'lines.append("**Sources:**")'
- A rewrite tried on a throwaway copy of a page saved by discovery: the Sources block was gone afterwards and only What was done was kept.
- core/components/plays/learn-outcomes/SKILL.md: "update the LIVING product model to match reality", "waits for the rebuild of the learn loop on the current product model"
- core/components/plays/shape-slice/SKILL.md: "writes the intent page from the issue when the model has none"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "Only a person confirms or drops it; an agent never does.", "It is met by its proof, never because its work is finished."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "What was delivered for it and the value each piece brought, with links to the finished work items — updated as work finishes"
- standards/schemas/product-os/ontology.md, in Phoenix memory: "When one of those ICE changes after the story is made, its scope of work, its Context guidance and its feature's entry in the slice's hidden file are drift for the Alignment loop."
