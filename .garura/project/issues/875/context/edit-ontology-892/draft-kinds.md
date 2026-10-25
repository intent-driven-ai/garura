# Kinds — #892 (no kind changes)

You confirm that this change leaves every kind as it is. Q20 is a question, not a kind: only its answer changes. Epic and Story keep what version 12 says, and the version 12 log line already names Q20's new answer, so no new log line is added.

Reuse: the answer uses only what version 12 already has (issue types Epic and Story, the labels `product` and `work-item`, rules R1 to R3, the plan file's `represents` mark). Terms: none new. Kinds: none added, none changed.

## K1

**Question:** Does this change leave every kind as it is, with only Q20's answer new?

**Answer (proposed):** Yes. No kind is added or changed. Epic and Story keep what version 12 says. The ontology stays at version 12.

**Why it matters:** If a kind changed here without a log line, a play that reads the ontology could use a meaning that no person agreed to.

**Example:**
- A clinic: an Epic "Patients book a visit online" stays an Epic; only the way the question about it is answered is clearer.
- A shop: a Story "Pay by card" stays a Story, also when no plan file names it yet.
- A bank: a Bug "Statement shows the wrong date" stays a Bug under its Story.
