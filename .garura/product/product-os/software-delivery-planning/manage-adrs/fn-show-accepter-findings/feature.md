# Feature: Give the person who accepts every point found on the way, and check it is whole

## What it does
While a decision is drafted as an ADR, the agent gathers each thing it found on the way that the brief did not ask about, each with five parts, and the draft carries them in their own section, For the Person Who Accepts This, which the person reads before they answer; the template's check fails a point that misses a part, so a person who was not in the work can decide with every finding in view.
- A point is one thing found while the context was gathered: an older page that disagrees with the decision, an agent that broke a rule, a file that is out of date, or a second part that the decision also reaches.
- Each point is written in five parts, in this order:
  - what and where: its plain name and its place, such as a file, a page, an agent or a memory tier;
  - what is wrong, or worth knowing: the detail itself, with the lines, the names and the dates;
  - why it matters: what goes wrong, and for whom;
  - what this decision does about it, or that it does nothing, and why;
  - what you decide: the choice left to the person, or nothing.
- In a Markdown ADR, the section comes after Context, with one sub-heading for each point and one line for each part. In a `decision.yaml` record, the points are a list, each with the point and its five parts.
- A point is written for someone who was not in the work. It gives the detail, never a summary: a point that only says a page is out of date, without which page and how, is not finished.
- A finding that the draft would only mention in passing in its Context goes in this section instead.
- The template's check reads the section when it is there: each point must carry all five parts, and a section with no point fails. A failed check sends the draft back to the skill.
- The person reads the section as part of the draft, which is shown exactly as it will read, before they accept, reject or ask for a change.
- Seven ADRs carry the section today: ADR 059, the first, then 060, 061, 062, 064, 065 and 066.
- Examples, in different kinds of project:
  - In a shop's checkout service, while a decision on how long carts are kept is drafted, the agent finds that the privacy page still says seven days. The point names the page and its line, says the decision makes it thirty days, and leaves the person to decide whether the page changes in the same change.
  - In a hospital's appointment system, the agent finds that a second service reads the same reminder table. The point names the service, says a queue would leave it reading an empty table, and says the decision does nothing about it, for the person to decide.
  - In a harness repository, the agent finds that a memory page is older than the source it was made from. The point names the memory tier, the page and the lines that differ, and asks whether the page is corrected now or later.
- How it meets the capability: a decision is "recorded closely as they're made" only when what was found while it was made is recorded with it, for the person who decides.

Status: built in part. The section in the template, the agent's gathering of the points, the skill's section in the draft and the template's check of each point are built: "A decision record tells the person accepting it what was found on the way" (#930, closed), and "ADR 059 is the first such record." Not built, or open:
- The decision play does not check that the points were gathered, or that each is whole, before it asks the person: "So if the agent gathers no points, or a point misses one of its five parts in the gathered context, the play still passes." (#935).
- The template's check reads a point only when the section is in the draft: "The ADR linter (`adr.py lint`) catches a broken point only when the section is in the record at all." (#935).
- The templates index does not name the section, so "An agent reading the row alone does not learn the section exists." (#941).

## Inputs / Outputs
- In: what the agent found while it gathered the context: the older ADRs, and the files, rules, schemas, plays and agents it read.
- In: the ADR template's section and its rule for a point.
- Out: the gathered context's points, each with its five parts.
- Out: the draft's section For the Person Who Accepts This, one sub-heading for each point with its five parts, or, in a `decision.yaml` record, the list of points.
- Out: the template's check of each point, in the run's check report.

## Rules & behavior
- Each point has its five parts. The reason, in the product owner's words: "update the ADR template so that things that I should know should be properly explained."
- A point is written for a person who was not in the work. The reason: "A point for the person who accepts it is written for someone who was not in the work."
- The detail itself, never a summary. The reason: a point "gives the detail itself (the lines, the names, the dates), not a summary", and the skill's rule: "Give the detail itself, never a summary".
- A finding goes in the section, not in passing. The reason: "A finding you only mention in passing in Context belongs here instead."
- Only what the brief did not ask about. The reason: the agent gathers "each thing you found on the way that the brief did not ask about"; what the brief asks about is the decision itself.
- The person reads the points before answering. The reason: the play will "show the draft exactly as it will read".
- A broken point fails the template's check and goes back to the skill. The reason: without the check, "A record can reach the person who accepts it with nothing explained."

## Acceptance criteria
- Given a gathered context with two points, each with its five parts, when the ADR is drafted, then its section has two sub-headings, each with the five parts, and the template's check reads clean.
- Given a point without what the person decides, when the draft is checked, then the check names the point and the missing part, and the draft goes back to the skill.
- Given a section with no point under it, when the draft is checked, then the check fails.
- Given a drafted ADR with points, when it is shown to the person, then the section is shown as it will read, before the answer.
- Given a run whose gathered context has no points and does not say that none were found, when the play checks the context, then it stops before the person is asked. This is not built (#935).
- Given an agent that reads the templates index, when it reads the ADR template's row, then the row names the section. This is not built (#941).

## Out of scope
- Drafting the rest of the ADR and its other checks. Record a decision as an ADR, with what it overrides and what it changes (fn-record-adr) does it.
- The person's answer. Accept an ADR only on a person's word, then or later (fn-accept-adr) does it.
- The ADR template as a standard, and the templates index. Standards, structure, settings and memory owns them.

## Sources
- .garura/project/issues/1021/context/capabilities.md, the list set on 2026-11-10: "Manage ADRs: Decisions on how the project is built are recorded closely as they're made, so agents can coordinate many pieces from them."
- core/components/agents/adr-keeper.md: "each thing you found on the way that the brief did not ask about"
- core/components/skills/author-decision/SKILL.md: "Give the detail itself, never a summary", "A finding you only mention in passing in Context belongs here instead."
- core/components/skills/author-decision/scripts/adr.py: the check of each point's five parts, and of a section with no point
- core/components/plays/record-decision/SKILL.md: "show the draft exactly as it will read"
- standards/templates/adr.md, in Phoenix memory: "A point for the person who accepts it is written for someone who was not in the work.", "gives the detail itself (the lines, the names, the dates), not a summary"
- standards/templates/_index.md, in Phoenix memory: the row for the ADR template, which does not name the section
- docs/adr/059-the-discovery-loops-knowledge-step-is-one-step-run-by-one-agent.md, and ADRs 060, 061, 062, 064, 065 and 066: each has the section For the Person Who Accepts This
- GitHub #930 (closed), the product owner on 2026-10-28: "update the ADR template so that things that I should know should be properly explained.", "A decision record tells the person accepting it what was found on the way", "ADR 059 is the first such record."
- GitHub #935 (open): "So if the agent gathers no points, or a point misses one of its five parts in the gathered context, the play still passes.", "The ADR linter (`adr.py lint`) catches a broken point only when the section is in the record at all.", "A record can reach the person who accepts it with nothing explained."
- GitHub #941 (open): "An agent reading the row alone does not learn the section exists."
