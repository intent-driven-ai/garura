# Feature: Keep the tracker's words matched to the model

## What it does
Keeps the words of an intent's issue in the tracker matched to the words on its page in the product model.
- A business intent is what a person or the organisation wants, in their own words. Each one is written in two places: its page in the product model, which agents read, and its issue in the tracker, which people find and follow. Its title, outcome, why, who asks for it, proof it is met and limits must say the same in both.
- A tracker is the tool where a team keeps its issues, such as GitHub. The project's settings name two: one for business intents, and one for agent work, which is the epics, stories, bugs, chores and spikes that agents build.
- Each intent page names its issue in the intents tracker, and the page's id is made from that issue's number: bi-1 for issue 1. In text, BI-1 means a business intent and #1 means a work issue.
- The page is the source. Its words are the ones a person approved, and the issue follows them. When the page changes, the issue is changed to match after a person's yes. When the two differ, the difference is named to a person.
- The feature exists because people read the issue and agents read the page. When the two say different things, people and agents work from two different intents.

Status: built in part. Each intent page names its issue, and its id must match that issue. Not built: comparing an issue's words with its page, changing the issue when the page changes, and a tool that reads the setting that names the intents tracker.

## Inputs / Outputs
- In: the intent page, and the issue number on its Tracker line.
- In: the project's settings: for intents, the tracker's platform, owner and name.
- In, not built: the issue as the intents tracker holds it now, with its title and text.
- Out: the page's Tracker line and its id, both made from the issue's number.
- Out, not built: for each intent, whether its issue matches its page, and each part that differs, with the words on each side.
- Out, not built: the issue's title and text changed to the page's words, after a person's yes.

## Rules & behavior
- The page's id is its issue's. An id that does not match the issue refuses the page. The reason: the page and the issue are one intent.
- The page holds the approved words, and the issue follows it. The reason: a page's words change only through words a person approved, so the page is the one place that holds what the person approved.
- A difference is named, never overwritten in silence. When an issue says something its page does not, a person decides which words stand. When the issue's words stand, the page is changed through Update an intent from approved words (fn-update-intent-from-approved-words). The reason: a person may have changed the intent in the tracker on purpose, and only a person changes an intent.
- Nothing is written to the tracker before a person's yes. The reason: people and agents pick up what is in the tracker, so what lands there must be what the person approved.
- Only tools know the tracker. Plays, skills and sub-agents name no tracker; a tool reads the settings and reaches it. The reason: a team can choose GitHub, GitLab, Jira or Linear as a setting, and a new tracker then means changing one tool.
- The code host is its own setting, apart from the trackers. The code host is where the team's code and pull requests live. The reason: a team on Jira or Linear still keeps its pull requests on GitHub or GitLab, so one setting would otherwise mean two things.
- Not built: no tool reads the setting that names the intents tracker. /shape-slice asks the code host for an intent's issue in the repository the play runs in, which holds the work. In a project whose intents live in their own tracker, it then reads a work issue with the same number, and may draft an intent page from the wrong issue.
- Not built: nothing compares an intent's issue with its page, and nothing changes the issue when the page is rewritten. So after a rewrite, the issue still says the old words, and no one is told.

## Acceptance criteria
- Given a draft whose id does not match its issue, when its page is written, then it is refused and nothing is written.
- Given an intent page rewritten from approved words, when the person says yes, then its issue in the intents tracker shows the new title and words. This is not built.
- Given an intent whose issue was changed by hand in the tracker, when the two are compared, then each part that differs is named to a person, and neither the page nor the issue changes. This is not built.
- Given settings that name an intents tracker apart from the work tracker, when a play reads an intent's issue, then it reads it from the intents tracker. This is not built.

## Out of scope
- Which tracker holds intents, and the setting that names it. Settings owns the project's settings.
- The tool that reaches the tracker for agent work, and tracking the work's status. Track execution in the team's tracker owns them.
- Making the issue types a tracker needs, such as Business Intent. Initialize a project for Garura does it.
- Choosing an intent's words. The person approves them, and Update an intent from approved words (fn-update-intent-from-approved-words) writes them on the page.
- Filing a new intent's issue, and closing a retired intent's issue. No play does either yet, and no capability owns them yet.

## Sources
- core/config.yaml: "# Which tracker holds what. Tools read this; plays, skills and sub-agents never name a tracker."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "Business intents and agent work each live in a tracker named in the project's settings.", "No script reads the new `trackers` settings yet", "BI-7 means an intent and #7 means work, in text."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "The code host is its own setting, and the tool reads both.", "The product owner also wants a team to be able to choose GitHub, GitLab, Jira or Linear as a setting", "A team on Jira or Linear still has its pull requests on GitHub or GitLab."
- core/components/skills/author-intent-page/SKILL.md: "An id that is not `bi-<digits>`, or not `bi-<issue>`, refuses the page.", "`**Tracker:** #<issue>` line right under it"
- core/components/plays/shape-slice/SKILL.md: "python3 scripts/platform_adapter.py --verb view-issue --arg issue_number=<intent-issue>"
- core/components/plays/shape-slice/scripts/platform_adapter.py: '["gh", "issue", "view", str(a["issue_number"]), "--json", fields]'
- standards/schemas/product-os/ontology.md, in Phoenix memory: "it becomes a **Business Intent** here and an issue labelled `product` in the tracker", "Only a person confirms or drops it; an agent never does."
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/capability.md: "Nothing reaches the tracker, the plan file or the model before the product owner's typed yes"
- .garura/product/product-os/software-delivery-planning/initialize/fn-881/feature.md: "It reads which tracker the project uses and the issue types that tracker already has"
- The capability list the product owner locked on 2026-11-03: "Settings: Everything that can be turned on or off lives in settings.", "Track execution in the team's tracker: The product's execution is tracked in the tracker Garura connects to"
- The boundary the product owner approved on 2026-11-07: "keeping an intent's words in the tracker matched to its page."
