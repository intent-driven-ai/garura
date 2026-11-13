# Feature: Link each piece of work to its intent across trackers

## What it does
When a play files or takes in a piece of work that serves a business intent, this feature hangs it under that intent by the tracker's own parent and child link, also when the business intents live in another tracker than the work, so a person or an agent can trace the work up to its intent, and the intent down to its work, from the tracker alone.
- What hangs where, by the way of working: an epic serves one or more business intents, its stories hang under it, and each bug, spike and chore hangs under a story. A business intent has no parent. A spike, a chore or a bug reaches its intent through its story and its epic.
- An unplanned epic, which gathers defects that are fixed together, hangs under the intent whose delivered work broke, "as that intent's sub-issue".
- The link is the tracker's own, across trackers too. ADR 065 records the product owner's call: "Decided: the real link stays, as the product owner asked, including across trackers."
- It has been done once, by hand. In the reorganisation of the business intents, the open work moved under the new intents with real links across the repos, between two GitHub repositories of one organization. No play makes the link.
- What is known of links between trackers, from the approved research:
  - On GitHub, "a parent issue can take an existing issue from another repository as a sub-issue", up to 100 of them and eight levels deep. "The docs do not say whether the other repository may be in another organization."
  - Jira links a work item to GitHub through its key, written in a branch name, a commit message or a pull request title.
  - "So there are two kinds of link: a real parent and child link inside one platform, and a key written in the work that an integration reads."
- The product model does not rest on the link: an epic reaches its intents through its slice. The link is for the people and agents who read the tracker.
- In text, an intent is written as BI- and its number, and a piece of work as # and its number, because the numbers of the two trackers overlap.
- Examples, in different kinds of project:
  - In a clinic's booking app, the business intents live in one GitHub repository and the work in another, in one organization. The epic for online booking hangs under the intent for patients booking their own appointments, across the two repositories.
  - In a shop's checkout project, the intents and the work are in one repository. Two defects come in after release, and the unplanned epic that gathers them hangs under the intent whose delivered work broke.
  - In a bank's payments service, the intents live in Jira and the work on GitHub. Which link its epics get there is not decided.
- How it meets the capability: Orchestration's proof is that "Any work traces up to its intent and down to its result."; the tracker shows how far the work for each intent has come only when each piece of work hangs under its intent.

Status: not built. No issue is filed for it. Today:
- /shape-plan makes each epic with no parent; only its stories get one, "with the epic as its parent".
- The adapter's link reads the parent and the child from the one repository it runs in, so it cannot link across two repositories, and on GitLab it "falls back to related-link".
- The links of Garura's own open work were made by hand, in the reorganisation of the business intents.
- ADR 065 asks to "Prove the real parent and child link across trackers before a team relies on it". Between two GitHub repositories of one organization, the reorganisation of the business intents did it by hand; between two platforms, nothing has.

## Inputs / Outputs
- In: the piece of work: its issue in the work tracker, its kind, and its plan, which is given the one business intent it serves.
- In: the intent's issue in the intents tracker, and the settings that name both trackers.
- In: the parent each issue has now, as the tracker holds it.
- Out: the piece of work under its intent by the tracker's own parent and child link, as the tracker shows it when read back.
- Out: for an unplanned epic, the epic under the intent whose delivered work broke.
- Out: where a link cannot be made, the piece of work it is missing for, recorded as owed.

## Rules & behavior
- The link is the tracker's own parent and child link, also across trackers. The reason: "Decided: the real link stays, as the product owner asked, including across trackers."
- Each kind hangs in its place. The reason: "Every Epic serves one or more business intents, every Story hangs under its Epic, and every Bug, Spike and Chore under a Story — as a real parent/child link in the tracker."
- A business intent hangs under nothing. The reason: "A business intent has no parent;"
- An unplanned epic hangs under the intent whose delivered work broke. The reason: "It serves the business intent whose delivered work broke, as that intent's sub-issue."
- The model never rests on the link. The reason: "The ontology does not need one: an Epic reaches its intents through its slice"; so a link that is missing or wrong in the tracker never changes the model.
- The link is made through the one tool that knows the tracker. The reason: "Plays, skills and sub-agents know only the tool, never the tracker."
- In text, an intent is written BI- and its number, and work # and its number. The reason: "BI-7 means an intent and #7 means work, in text.", because "(#65) in a commit links to the work tracker."
- The link is proven before a team relies on it. The reason: "A person or play following that text tries to make a link that may fail, so it has to be proven across trackers before a team relies on it."
- A link that cannot be made never stops a person. The reason, the Must not of Orchestration: "Stop a person. Every gate has a way past it that records what's owed."
- Not decided: what the link is when the intents and the work are on two platforms, such as intents in Jira and work on GitHub.
- Not decided: which plays make the link: the plan plays for each epic, /start-change for an issue it files, the filing of a bug, or more than one of them.
- Not decided: which pieces of work hang straight under an intent: only an epic, as the way of working says, or also a piece of work that no epic holds, as Garura's own open work was moved in the reorganisation of the business intents.
- Not decided: how an epic that serves more than one intent hangs under each of them, since "an issue has only one parent."
- Not decided: whether a GitHub sub-issue may sit in a repository of another organization. The approved research says: "The docs do not say whether the other repository may be in another organization."
- Not decided: how GitLab, Jira and Linear each hold a parent link across projects. No approved source gives it; the approved research names only Jira's key written in the work.

## Acceptance criteria
- Given a plan whose intent lives in an intents tracker on the same platform as the work, when /shape-plan makes the plan's epic, then the tracker shows the epic as a sub-issue of the intent's issue. This is not built.
- Given an epic that already hangs under its intent, when the plan play runs again, then no second link is made and nothing else changes. This is not built.
- Given defects gathered in an unplanned epic, when the epic is filed, then it hangs under the intent whose delivered work broke. This is not built.
- Given a link the tracker refuses, when the play goes on, then the person is not stopped, and the missing link is recorded as owed. This is not built.

## Out of scope
- Knowing the two trackers in one tool. One tool knows the tracker (fn-one-tool-knows-tracker) does it, and it is not built.
- The type of each work item, and its parent under its epic or its story. Mark each work item by its type, under the right parent, with no label (fn-mark-item-type) does it.
- Making the epics and stories of an intent. Turn intents into agent work, in Product → Spec, owns it; this feature holds their link to the intent.
- The model's own trace from an epic to its intents, through its slice. Define what a product is made of, in Product model, owns the kinds and their links.
- Recording what is owed when a way past is used. Give every gate a way past, in Orchestration, owns it.

## Sources
- The capability list the product owner locked on 2026-11-03: "Track execution in the team's tracker: The product's execution is tracked in the tracker Garura connects to, for completion status and the backlog."; and his words of 2026-11-10: "Is there anything new? If so, then do research for that."
- 1021/context/answers/bi9-cross-tracker-links.md, in short-term memory (mu-20261110-012, approved by the product owner on 2026-11-10): "a parent issue can take an existing issue from another repository as a sub-issue", "a parent holds up to 100 sub-issues, nested up to eight levels", "The docs do not say whether the other repository may be in another organization.", "Jira links a work item to GitHub through its key", "written in a branch name, a commit message or a pull request title", "So there are two kinds of link: a real parent and child link inside one platform, and a key written in the work that an integration reads."
- docs/adr/065-the-models-index-is-changed-through-two-skills-the-model-never-names-a-plan-and-only-tools-know-the-tracker.md: "Decided: the real link stays, as the product owner asked, including across trackers.", "The ontology does not need one: an Epic reaches its intents through its slice", "A person or play following that text tries to make a link that may fail, so it has to be proven across trackers before a team relies on it.", "Prove the real parent and child link across trackers before a team relies on it", "BI-7 means an intent and #7 means work, in text.", "(#65) in a commit links to the work tracker.", "Plays, skills and sub-agents know only the tool, never the tracker."
- .garura/user-provided/managing-work.md: "Every Epic serves one or more business intents, every Story hangs under its Epic, and every Bug, Spike and Chore under a Story — as a real parent/child link in the tracker.", "A business intent has no parent;", "It serves the business intent whose delivered work broke, as that intent's sub-issue.", "as that intent's sub-issue", "an issue has only one parent."
- standards/schemas/product-os/ontology.md, in Phoenix memory: "A Spike, Chore or Bug is a child of one Story. It reaches the Feature, the Epic and the Business Intent through that Story."
- .garura/product/product-os/intents/bi-9.md: "Any work traces up to its intent and down to its result.", "Stop a person. Every gate has a way past it that records what's owed."
- core/components/plays/shape-plan/scripts/write_work_items.py: "the epic to `make` becomes an issue of type Epic, with no label, in one write.", "with the epic as its parent"
- core/components/skills/platform-adapter/reference/github/verbs.md, its attach-sub-issue: both the parent and the child are read from the one repository that `gh repo view` names.
- core/components/skills/platform-adapter/SKILL.md: "Attach a child issue to a parent (GitHub only; GitLab falls back to related-link)"
- The research for this capability's new features, T1, "Link work across trackers": its open points are the Not decided lines here.
- Shelf: none. No knowledge shelf in any memory tier covers how a team tracks its work in a tracker.
