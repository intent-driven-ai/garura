# Feature: Run initialize again

## What it does
- Words this page uses. The product profile is the project's lasting record of its setup answers, kept in the project's product model; it is where a new run finds the earlier answers. Phoenix memory is the one shared memory on the machine that every project draws from, and a memory block is the set of Phoenix memory files that one answer selects (for example the database standards for a database answer). A rule group is a set of the review's rules that check one kind of thing (for example database or front end), which the review runs or skips as a whole. The mapping is the record that tells the plays which of the tracker's own types to use for each type they file (Business Intent, Epic, Story, Bug, Chore, Spike); a stand-in is a type the tracker already has, mapped in place of one it cannot make. The brief is the message `initialize` shows the product owner, where they confirm, correct, or type yes or no.
- Lets the product owner run `initialize` again at any time, when the project changes: it gains a database, a web surface, personal data or a new tracker, or it drops one. The set-up then follows the project without a reinstall.
- A second run reads the earlier answers from the product profile and proposes each one again with the earlier answer as its source, so the product owner confirms what still holds and corrects only what changed.
- From the new answers it rebuilds the project's memory, the review rule-group record and the tracker set-up, through the same features as the first run.
- The same run also takes in what changed in Phoenix memory since the project last took it, because each run compares the project's memory blocks with Phoenix memory (Give each project its own memory blocks, fn-883).

## Inputs / Outputs
- In: the earlier answers, as the product profile records them.
- In: the project as it is now, for proposals where the project has changed.
- In: the product owner's typed reply to the brief: a confirmation or a correction for each question, and a yes or no for each tracker change.
- Out: the questions, each with the earlier answer proposed and named as its source.
- Out: the rebuilt memory, rule-group record and tracker set-up, through Build the project's memory (fn-project-memory), Choose the review rule groups (fn-review-rule-groups) and Set up the tracker's work-item types (fn-881).
- Out: the change record, a list of what changed since the last run, kept with the project's settings beside the mapping and shown in the brief: answers changed, memory files added or taken out, rule groups now kept or skipped, tracker types made or mapped, the tracker the mapping now points to, and the old mapping when it changed. Where the change record is kept is our default; the sources do not say.

## Rules & behavior
- An earlier answer is a proposal, never an answer, on a new run. The product owner confirms it again, because the project may have changed.
- When the project itself now shows a different answer than the earlier one (for example a database it did not have), the proposal names the project as its source and the earlier answer is shown beside it, because what the project holds now is newer evidence than an old answer, and the earlier answer beside it lets the product owner see what changed before confirming. Our default; the sources do not say how a change is shown.
- A run with every answer unchanged and no change in Phoenix memory changes nothing, so a repeat run is always safe to start. Our default; the sources do not say this.
- The tracker rule holds on every run: nothing is made in the tracker and no stand-in is mapped before a typed yes, because the tracker is an outside system the whole team sees, and a re-run is as able to make a wrong type as a first run.
- When a changed answer rules out something the first run built (for example the database answer goes from yes to no), the re-run takes the database block out of the project's memory, marks the review's database rule group as skipped with the new answer, and records both in the change record, because a standard or a rule group the project no longer needs gives only noise.
- When the tracker answer changes (for example from GitHub to Jira), the re-run sets up the work-item types in the new tracker as a first run does: it reads the new tracker's types, lists what is missing, and makes nothing and maps nothing before the product owner's typed yes. After that yes the mapping points to the new tracker, and the change record keeps the old mapping. The re-run leaves the old tracker as it is, with no type made, changed or removed there, because the old tracker may still hold the team's work items. Our default; the sources do not say what a re-run does when the tracker changes.
- When the product profile holds no earlier answers (the first run never finished), the run asks the questions as a first run does, with proposals from the project and Phoenix memory only, and says in plain words that no earlier answers were found, so the product owner knows nothing is carried over. Our default; the sources do not say what a re-run does with no earlier answers.
- When a question has no earlier answer while the others do (a question new since the last run, because the questions are built from Phoenix memory and Phoenix memory can change), the run asks it as a first run does, with a proposal from the project as it is now or from Phoenix memory and that source named, and marks it as new in the brief, so the product owner sees it is not a carried-over answer. Our default; the sources do not say what a re-run does with a new question.
- When the product owner says no to the tracker changes, the memory and rule-group changes from the other confirmed answers still apply, the mapping still points to the old tracker, and the change record shows the tracker part as declined, so the next run proposes the tracker set-up again. The memory and the rule groups are kept only in the project and follow answers the product owner confirmed, while the tracker yes is a separate decision about an outside system; a no to it does not undo the confirmed answers. Our default; the sources do not say what a no to the tracker does to the rest of the run.
- A run never removes a work-item type from the tracker, because a type may hold work items the team still uses. Our default; the sources do not say what a re-run does to a type no longer needed.

## Acceptance criteria
- Given a project that was initialized before, when the product owner runs `initialize` again, then each question proposes the earlier answer from the product profile and names it as its source.
- Given the product owner changes the database answer from no to yes, when the run ends, then the project's memory holds the database block and the review's database rule group is kept.
- Given the database answer changes from yes to no, when the run ends, then the database block is no longer in the project's memory and the database rule group is recorded as skipped.
- Given the tracker answer changes from GitHub to Jira and the product owner types yes to Jira's missing types, when the run ends, then those types are made in Jira and the mapping points to Jira.
- Given the tracker answer changes from GitHub to Jira and the product owner types yes, when the run ends, then the change record keeps the old GitHub mapping and nothing in the GitHub tracker changes.
- Given the tracker answer changes, the database answer changes from no to yes, and the product owner says no to the tracker changes, when the run ends, then nothing is made in the new tracker, the mapping is unchanged, the project's memory holds the database block, the database rule group is kept, and the change record shows the tracker part as declined.
- Given a project initialized before and a question added to the setup questions since that run, when `initialize` runs again, then the brief marks that question as new and proposes an answer from the project or Phoenix memory with its source named, and every other question proposes its earlier answer.
- Given a product profile with no earlier answers, when initialize runs again, then it asks every question as a first run does and says that no earlier answers were found.
- Given every answer confirmed unchanged and no change in Phoenix memory, when the run ends, then no memory file, rule-group record or tracker type changes.
- Given a work-item type no longer needed, when initialize runs again, then the type stays in the tracker.

## Out of scope
- The first run's questions, memory, rule groups and tracker types: Ask the setup questions (fn-setup-questions), Build the project's memory (fn-project-memory), Choose the review rule groups (fn-review-rule-groups) and Set up the tracker's work-item types (fn-881) own them; this feature reuses them.
- Finding and taking in a change to Phoenix memory under the blocks the project already holds: Give each project its own memory blocks (fn-883) owns it; this feature only runs it as part of the same run.
- Moving the old tracker's work items to the new tracker: no part of initialize does it, because initialize files and moves no work item.
- Reinstalling Garura (the Garura install owns it, and it lays no memory).

## Sources
- GitHub #862: "a project can run `initialize` again when it changes".
- GitHub #862, Rule 3: "The answers are the person's; a proposed answer always names its source."
- GitHub #881: "It makes each missing type only after the person's typed yes"; "whatever the project uses — GitHub, Jira, Linear or another tracker — it finds the work-item types the plays need, and makes the ones that are missing."
- GitHub #883: "It can run again to bring changes in."
- Shelf: none; no knowledge shelf in memory covers setting up a software project.

## Agent intent (ICE)
- Goal: The product owner can run `initialize` again when the project changes, and the memory, the rule-group record and the tracker set-up follow the new answers.
- Goal: On a new run each question proposes the earlier answer from the product profile and names it as its source.
- Limit: Treat an earlier answer only as a proposal, and make or map nothing in the tracker before a typed yes.
- Limit: Never remove a work-item type from the tracker on a re-run, and never change the old tracker when the tracker answer changes.
- Fails if: a re-run keeps a memory block or rule group that a changed answer rules out.
- Fails if: a re-run with every answer unchanged and no Phoenix memory change changes a memory file, the rule-group record or the tracker.
- Fails if: after a tracker change the mapping points to the new tracker without the product owner's yes, or anything in the old tracker changes.
- Context: serves the product owner when the project changes; reads the product profile's earlier answers and the project as it is now; reuses the first run's features; out are the reinstall and moving work items between trackers.
- Checked by: initialize a test project, change one answer on a second run, and check that only what that answer decides has changed.
