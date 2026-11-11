# Feature: Every approved tracker write lands once, and is picked up after a stop

## What it does
When a plan session's list is approved, this feature makes the list's tracker writes one by one through the adapter, records each write as soon as it is made, and on a run again goes on from its record, so each approved write lands exactly once, also when the run stopped part way, and nothing the person did not approve reaches the tracker.
- The writes it makes: close an issue, as completed or as not planned; reopen one; give it a new title, a new text, a new type or a new parent; and make a new issue with its type and its parent. It adds no label and deletes nothing.
- Before the first write it checks the approval: the person's answer reads "approved", and the sha256 of the list as it is now is the one recorded with the approval. Any other answer, or a list that changed after the approval, refuses the whole run, and nothing is written; the session shows the list again.
- Each write is recorded at once. A run again skips each write its record holds. A record made for another list is refused, never skipped over.
- Each new issue carries a marker line, "Made by /update-plan (list <12 hex>, op <id>).", and before it makes one it searches the tracker for that line. An issue an earlier run made is found and used, never made twice.
- A write whose result is already in the tracker, such as a close of an issue already closed with the same reason, is recorded as already true, with no write.
- It reads the plan's issues just before its first write and again after its last, so the session can check that nothing else changed.
- In the session, the model is written first, then the tracker, then the plan file. The plan file is written only once the record shows every write made, so the plan file never says what the tracker does not.
- When a write fails, the run stops; its record names that write and keeps every write before it. The session runs it once more; a second failure stops the landing and names the failed write for the person. The next session on the plan asks: carry on, or start fresh.
- /shape-plan holds the same rule in its own writer, for the first epics and stories of a plan: nothing before the product owner's yes on the exact files they saw, a record after every write, and a second run with nothing new writes nothing. It puts no marker line on an issue it makes; the next run finds those issues through the plan file written from the record.
- Examples, in different kinds of project:
  - In a shop's checkout plan, a session closes two stories and adds a chore. The code host times out on the chore. The run again finds the two closes in its record and makes only the chore.
  - In a bank's payments plan, the run stops just after the tracker made a new bug, and before the record was written. The run again finds the bug by its marker line and uses it, so there is one bug, not two.
  - In a game studio's plan, the product owner approves a list and then adds one more instruction. The list's sha256 no longer matches, so nothing is written until they approve the new list.
- How it meets the capability: the tracker shows the work only if what lands there is exactly what a person approved, once.

Status: built, in the track-plan-changes skill, which /update-plan uses (#730, the plan session, closed). Not built, or open:
- After a stop in the middle of a create, the tracker's search "may not find an issue made seconds earlier". The skill's words ask whoever runs it again to search for the marker, and to "wait a minute and search again"; no script waits.
- Only the writes of a plan session land this way, and /shape-plan's in its own writer. Other writes, such as the new issue /start-change files and the close at the merge, go through other parts with their own records.
- The writes go through a copy of the adapter beside the skill, which reads the older code-host setting, not the settings' trackers (#1023, an Agent-work tool reads the tracker setting).

## Inputs / Outputs
- In: the approved list, and the person's answer with the list's sha256.
- In: the writes the session's script took from the list: each with its id, its issue and its new value; a new issue with its title, text, type and parent.
- In: the plan's issue numbers, to read before and after.
- In: the record of an earlier run of the same list, when there is one.
- Out: each write made in the tracker, in the list's order.
- Out: the record: whether every write is made, the list's sha256, each write with how it was done (done, made, found or already), and the write that failed.
- Out: the issues as they were just before the first write and just after the last.
- Out: an end that says which way it went: every write made or already true; a write failed and is named; or refused, with nothing written.

## Rules & behavior
- Only the approved list, for the very list the person saw. The reason: the writer refuses unless the approval is for the list as it is now, "so only the list the person saw lands."; and "What lands is exactly the list the person saw when they approved it."
- Only through the adapter. The reason: "Only the list the person approved, and only through the platform adapter's verbs."
- Each write is recorded as soon as it is made, and a run again never repeats one. The reason: "Each write is recorded as soon as it is made; a run again never repeats one, and a create looks for its own marker first, so an issue is never made twice."
- A record made for another list is refused. The reason: "a record from another list is refused, never skipped over."; a record of other writes cannot say which of these writes were made.
- No label is added and nothing is deleted. The reason: "No labels are added, and nothing is deleted."
- A write already true is recorded as already, with no write. The reason: a run again must not fail, or write twice, on what is already done.
- The model, then the tracker, then the plan file; and the plan file only when every write is made. The reason: the session writes "the model first, then the tracker, then the plan file", and "the plan file step writes only when the tracker record reads ok: true."
- It decides nothing. The reason: "It is mechanical — what to change was decided in the session; this skill decides nothing."
- A write that keeps failing stops the landing. The person can carry on once its cause is fixed, or start the list fresh. Neither lands the rest of the list with the failed write recorded as owed, so it stops a person with no way past that records what is owed.
- Not decided: whether a landing may go on past a write that keeps failing, with that write recorded as owed.

## Acceptance criteria
- Given an approved list of three writes, when the second write fails, then the record holds the first, names the second as failed, and the plan file is not written; and when it runs again after the cause is fixed, the first is skipped and the second and third are made once.
- Given a create whose issue the tracker made before the run stopped, when the run goes again, then the issue is found by its marker line and no second issue is made.
- Given a list changed after the person approved it, when the writes run, then nothing is written and the run is refused.
- Given an answer other than "approved", when the writes run, then nothing is written.
- Given a close of an issue already closed as completed, when the writes run, then it is recorded as already true and no write is made.

## Out of scope
- Working out and checking each entry of the list. Change the work items (fn-change-work-items), in Turn intents into agent work, does it for the work items, and Orchestrate agent work through planning for the statuses.
- Making the first epics and stories of a plan, in /shape-plan's own writer, and the check after a landing that the plan file and the tracker agree. Turn intents into agent work, in Product → Spec, owns them.
- Knowing the tracker in one tool. One tool knows the tracker (fn-one-tool-knows-tracker) does it, and it is not built.
- A way past a write that keeps failing. Give every gate a way past, in Orchestration, owns it.

## Sources
- .garura/project/issues/1021/context/capabilities.md, the product owner on 2026-11-10: "Anything that already exists, like managing ADRs and execution tracking, just use what is already built to do that."
- core/components/skills/track-plan-changes/SKILL.md: "Each write is recorded as soon as it is made; a run again never repeats one, and a create looks for its own marker first, so an issue is never made twice.", "Only the list the person approved, and only through the platform adapter's verbs.", "No labels are added, and nothing is deleted.", "It is mechanical — what to change was decided in the session; this skill decides nothing.", "Made by /update-plan (list <12 hex>, op <id>).", "may not find an issue made seconds earlier", "wait a minute and search again, so no issue is made twice."
- core/components/skills/track-plan-changes/scripts/track_changes.py: "so only the list the person saw lands.", "a record from another list is refused, never skipped over.", "run again, it skips each op the record has."
- core/components/plays/update-plan/reference/ice.md: "What lands is exactly the list the person saw when they approved it.", "the model first, then the tracker, then the plan file"
- core/components/plays/update-plan/SKILL.md: "the plan file step writes only when the tracker record reads ok: true.", "a second failure stops the landing and names the failed op for the person", "carry on, or start fresh"
- core/components/plays/shape-plan/scripts/write_work_items.py: "The record is written after every tracker write, not only at the end.", "the play still writes the plan file from it, so the next run finds those issues and makes no copy.", "A second run with nothing new writes nothing."
- .garura/product/product-os/software-delivery-planning/turn-intents-into-work/fn-change-work-items/feature.md: "Nothing is written to the tracker, the plan file or the model before a plain"
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- GitHub #730 (closed): "The /update-plan session: instructions, checks, one approval, one landing on the plan's branch"
- GitHub #1023 (open): "An Agent-work tool reads the tracker setting, so no play, skill or sub-agent names a tracker"
