# Feature: Keep the tracker's words matched to the model

## What it does
The planned side stays matched to the spec: each intent's issue in the tracker says what the intent's page in the product model says.
- A business intent is what a person or the organisation wants, in their own words. The product model is the shared map of the product that people and agents read, and the spec is what it says the product is for and what it does.
- Each intent is written in two places. Its page in the product model is what agents read. Its issue in the tracker is what people find and follow, and it is part of the planned side of the work. The tracker is the tool where a team keeps its issues, such as GitHub.
- The project's settings name two trackers: one for business intents, and one for agent work. Agent work is the epics, stories, bugs, chores and spikes that agents build.
- The page is the source. It holds the words that a person approved. The issue follows the page:
  - When an intent's page gets new words, its issue is changed to the same words, after a person's yes.
  - When an intent is replaced or retired, its issue is changed to say so, after a person's yes.
  - When an issue and its page say different things, the difference is named to a person.
- The words that must match are the title, the outcome, why it matters, who asks for it, the proof it is met, and the limits.
- The feature exists because people read the issue and agents read the page. When the two say different things, people and agents work from two different intents.

Status: built in part. Each intent page names its issue, and the page's id is made from that issue's number, so each can be found from the other. Not built: comparing an issue's words with its page, changing the issue when the page changes, changing the issue of a replaced or retired intent, and a tool that reads the setting that names the intents tracker.

## Inputs / Outputs
- In: an intent page whose words changed, after the person approved them.
- In: an intent that was replaced or retired, after the person approved it.
- In: a difference found between an intent's issue and its page.
- In: the intent's issue as the intents tracker holds it now.
- Out: the page's id and its Tracker line, both made from the issue's number.
- Out: the issue now says what the page says, after a person's yes. This is not built.
- Out: each difference between an issue and its page, with the words on each side, named to a person. This is not built.
- Out: the issue of a replaced or retired intent says so, after a person's yes. This is not built.

## Rules & behavior
- The page's id is its issue's number. For example, the page bi-1 is for issue 1. A page whose id does not match its issue is refused. The reason: the page and the issue are one intent, so each must lead to the other.
- The page holds the approved words, and the issue follows it. The reason: a page's words change only through words a person approved, so the page is the one place that holds what the person approved.
- A difference is named, never overwritten in silence. When an issue says something its page does not, a person decides which words stand. When the issue's words stand, the page changes through Update the spec to match what's built (fn-update-spec-to-match-built). The reason: a person may have changed the intent in the tracker on purpose, and only a person changes an intent.
- Nothing is written to the tracker before a person's yes. The reason: people and agents pick up what is in the tracker, so what goes there must be what the person approved.
- The tracker is a setting. Only a tool reads which tracker holds intents and reaches it. The rest of the work names no tracker. The reason: a team can choose GitHub, GitLab, Jira or Linear as a setting, and a new tracker then means a change to one tool.
- Not built: no tool reads the setting that names the intents tracker. The play that shapes a slice reads an intent's issue from the repository it runs in, which holds the agent work. In a project whose intents are in their own tracker, it can read a work issue with the same number and draft an intent page from the wrong issue.
- Not built: nothing compares an intent's issue with its page, and nothing changes the issue when the page changes. So after a rewrite, the issue still says the old words, and nobody is told.
- Not built: a replaced or retired intent's issue stays as it was. Nothing closes it or points it to the new intent, so people still see an intent that the spec no longer holds.

## Acceptance criteria
- Given an intent page whose id does not match its issue, when the page is written, then it is refused and nothing is written.
- Given an intent page that got new words from approved words, when the person says yes, then its issue in the intents tracker shows the same title and words. This is not built.
- Given an intent whose issue was changed by hand in the tracker, when the issue and the page are compared, then each difference is named to a person, and neither the page nor the issue changes. This is not built.
- Given an intent retired with the person's approval, when the person says yes to the tracker change, then its issue says that the intent was retired, or names the intent that replaced it. This is not built.
- Given settings that name an intents tracker apart from the work tracker, when an intent's issue is read, then it is read from the intents tracker. This is not built.

## Out of scope
- Which tracker holds intents, and the setting that names it. Settings owns the project's settings.
- Tracking the agent work's own status in the tracker. Track execution in the team's tracker owns it.
- Making the issue types a tracker needs, such as Business Intent. Initialize a project for Garura does it.
- Choosing an intent's words. The person approves them, and Update the spec to match what's built (fn-update-spec-to-match-built) puts them on the page.
- Changing an epic or a story that no longer matches the spec. Turn intents into agent work changes the work items.
- Filing a new intent's issue. No play does it yet, and no capability owns it yet.

## Sources
- The capability page the product owner approved on 2026-11-07: "In: keeping an intent's words in the tracker matched to its page.", "The tracker follows the page."
- core/config.yaml: "# Which tracker holds what. Tools read this; plays, skills and sub-agents never name a tracker."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "Business intents and agent work each live in a tracker named in the project's settings.", "No script reads the new `trackers` settings yet", "BI-7 means an intent and #7 means work, in text."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "The product owner also wants a team to be able to choose GitHub, GitLab, Jira or Linear as a setting"
- core/components/skills/author-intent-page/SKILL.md: "An id that is not `bi-<digits>`, or not `bi-<issue>`, refuses the page.", "`**Tracker:** #<issue>` line right under it"
- core/components/plays/shape-slice/SKILL.md: "python3 scripts/platform_adapter.py --verb view-issue --arg issue_number=<intent-issue>"
- core/components/plays/shape-slice/scripts/platform_adapter.py: '["gh", "issue", "view", str(a["issue_number"]), "--json", fields]'
- standards/schemas/product-os/ontology.md, in Phoenix memory: "it becomes a **Business Intent** here and an issue labelled `product` in the tracker", "Only a person confirms or drops it; an agent never does."
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/capability.md: "Nothing reaches the tracker, the plan file or the model before the product owner's typed yes"
- .garura/product/product-os/software-delivery-planning/initialize/fn-881/feature.md: "It reads which tracker the project uses and the issue types that tracker already has"
- The capability list the product owner locked on 2026-11-03: "Settings: Everything that can be turned on or off lives in settings.", "Track execution in the team's tracker: The product's execution is tracked in the tracker Garura connects to"
