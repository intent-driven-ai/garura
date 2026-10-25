# Questions — #892 (Q20 only)

You decide if the new answer to one ontology question is right. The answer now says one thing only: the issue type tells which kind an issue is, and the plan file tells which epic or story stands for which slice or feature. When you say yes, only this answer changes in the ontology; no kind, link or rule changes.

## Q20

**Question:** Given a tracker issue, which kind is it?

**Answer (proposed):** the issue type names the kind: type Epic is an Epic and type Story is a Story, each with no label (rules R1, R2); label `product` is a Business Intent; label `work-item` with its kind is a Spike, a Chore or a Bug. Which Epic stands for a slice, and which Story for a feature, is found by the plan file's `represents` mark, never by type or title (rule R3).

**Why it matters:** The old answer mixed the type and the plan file's mark. For an issue that no plan file names, a play could not tell which one decides. Then it could read the kind wrong, or skip the issue.

**Example:**
- A clinic: an issue of type Epic, "Patients book a visit online", is an Epic. The plan file's mark says it stands for the booking slice.
- A shop: an issue of type Story, "Pay by card", is a Story, also when no plan file names it yet.
- A bank: an issue with label `work-item` and kind Bug, "Statement shows the wrong date", is a Bug.
