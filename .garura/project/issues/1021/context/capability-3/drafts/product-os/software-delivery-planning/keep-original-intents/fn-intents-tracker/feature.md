# Feature: Keep intents in their own tracker

## What it does
A setting names the tracker that holds business intents, apart from agent work, and each intent page names its issue there.
- A tracker is the tool where a team keeps its issues, such as GitHub. The project's settings name two: one for business intents, and one for agent work, which is the epics, stories, bugs, chores and spikes that agents build.
- Each intent page names its issue in the intents tracker, and the page's id is made from that issue's number: bi-1 for issue 1.
- In text, BI-1 means a business intent and #1 means a work issue.
- The feature exists so that intents have their own short numbers and stay clearly apart from the work.

Status: built in part. The setting, the page's issue line and the naming rule are in place. Three things are not built: a tool that reads the setting, filing an intent from a play, and keeping the issue's words and the page's words the same.

## Inputs / Outputs
- In: the project's settings: for intents and for work, each tracker's platform, owner and name.
- In: an intent's issue number in the intents tracker.
- Out: the intent page's Tracker line and its id, both made from that number.
- Out, not built: a new intent's issue, filed in the intents tracker by a tool.

## Rules & behavior
- Only tools know the tracker. Plays, skills and sub-agents name no tracker; a tool reads the settings and reaches it. The reason: a team can choose GitHub, GitLab, Jira or Linear as a setting, and a new tracker then means changing one tool.
- The code host is its own setting, and the tool reads both. The reason: a team on Jira or Linear still keeps its pull requests on GitHub or GitLab, so one setting would otherwise mean two things.
- The page's id is its issue's. An id that does not match the issue refuses the page. The reason: the page and the issue are one intent.
- Short-term memory folders belong to work issues only. Short-term memory is the folder of working records kept for one issue. The reason: each tracker numbers its issues from one, so an intent's number used as a folder would open a work issue's records.
- Not built: no script reads the setting yet. The parts that reach a tracker still name it directly, and they move onto the tool over time.
- Not built: no play files an intent in the intents tracker. The intents there today were filed outside any play.
- Not built: nothing keeps the issue's words and the page's words the same. The intent is written in both places, so the two can drift apart.

## Acceptance criteria
- Given settings that name an intents tracker and a work tracker, when a tool files a new intent, then it goes to the intents tracker and its page is named after that issue. This is not built.
- Given a draft whose id does not match its issue, when its page is written, then it is refused and nothing is written.
- Given an intent page and its issue, when they are compared, then the title, outcome, why, asked by, proof and limits say the same in both. This is not built.

## Out of scope
- The tool that reaches the tracker for agent work, and tracking the work's status. Track execution in the team's tracker owns them.
- Making the issue types a tracker needs, such as Business Intent. Initialize does it.
- The words of the intent. Write an intent from approved words (fn-write-intent-page) does it.

## Sources
- core/config.yaml: "# Which tracker holds what. Tools read this; plays, skills and sub-agents never name a tracker."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "to keep business intents in a tracker of their own, so they have their own short numbers", "Business intents and agent work each live in a tracker named in the project's settings."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "The code host is its own setting, and the tool reads both.", "No script reads the new `trackers` settings yet", "BI-7 means an intent and #7 means work, in text.", "Short-term memory folders belong to work issues only."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "The product owner also wants a team to be able to choose GitHub, GitLab, Jira or Linear as a setting", "A team on Jira or Linear still has its pull requests on GitHub or GitLab."
- core/components/skills/author-intent-page/SKILL.md: "An id that is not `bi-<digits>`, or not `bi-<issue>`, refuses the page."
- .garura/product/product-os/software-delivery-planning/initialize/fn-881/feature.md: "It reads which tracker the project uses and the issue types that tracker already has"
