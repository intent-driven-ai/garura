## Intent
- Goal: When the project changes, or a new version of Garura asks something new, a new run of Initialize proposes each earlier answer from the product profile with it named as its source, and the project's memory and its rule-group record follow the answers the product owner confirms, its tracker set-up follows them after the product owner's typed yes, and a change record names what changed, while a run with nothing changed changes nothing.
- Limit: Treat an earlier answer only as a proposal, and make or map nothing in the tracker before a typed yes.
- Limit: Never remove an issue type from the tracker on a re-run, and never change the old tracker when the tracker answer changes.
- Fails if: a re-run keeps a memory block or rule group that a changed answer rules out.
- Fails if: a re-run with every answer unchanged and no Phoenix memory change changes a memory file, the rule-group record or the tracker.
- Fails if: after a tracker change the mapping points to the new tracker without the product owner's yes, or anything in the old tracker changes.

## Context
- Read: Gather it from the memory layer. Look first at the project's existing memory and its existing implementation, then Garura memory, then Phoenix memory. If none of them answers, research it and raise a memory update for a person to approve. For this part, look for: the earlier answers in the product profile; the project's files and settings as they are now; the questions as Phoenix memory and the installed version give them now; and the record of the last run's memory blocks, rule groups and tracker set-up.
- Never read: any memory file by its path, and any ICE page.
- Persona: the product owner, who sets the project up again when it changes.
- Scope: In: proposing the earlier answers, marking a new question, rebuilding from the new answers through the first run's features, a change of tracker, and the change record. Out: the first run's own features, taking in a change to Phoenix memory under the blocks, moving work items between trackers, and installing or upgrading Garura.

## Expectation
- Scenario: A school's timetable app was set up with no database. It gains one, and a new Garura version adds a question. The product owner runs Initialize again: each earlier answer is proposed with the product profile named as its source, the database question proposes yes from the project's new schema folder with the earlier no beside it, and the new question is marked new. After the confirmation the project's memory holds the database block, the database rule group is kept, and the change record names both; nothing else changed.
- Done means: Someone other than the one who ran it compares the project's memory, the rule-group record and the tracker before and after with the change record, and finds that only what the changed answers decide has changed; and a further run with every answer unchanged changes nothing.
