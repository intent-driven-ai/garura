# Decisions for #818 (the plan play, /shape-plan), the product owner, 2026-10-25

The product owner approved the draft intent (C1–C11, F1–F9) with a plain "yes", which accepts each proposed answer:

1. Q-find-1 — the plan file marks each work item with what it stands for (`represents: <slice id>` on an epic, `represents: <feature id>` on a story), and the play uses a marked item; it never matches by title. For plan 788, #794 is marked as the epic of sl-intent-to-design and #795, #818, #798 as its stories (fn-795, fn-818, fn-798), once, by hand, before the first run.
2. Q-found-1 — on a found story the play adds the "Scope of work" and "Context guidance" sections when they are missing, and keeps every line the person wrote; it never rewrites or deletes their text.
3. Q-label-1 — an epic and a story are marked by the tracker's issue type field (Epic, Story), with no label (managing-work.md "No labels, for now"). The ontology's "labelled work-item" line is fixed with /edit-ontology as its own small change.
4. Q-change-1 (from the /shape-slice 788 run, #866) — a feature that leaves the slice has its story moved out of the plan; the story stays in the tracker and is never deleted. A feature that comes in gets one story.
5. Q-label-1, the type (2026-10-25) — the organization has no Epic issue type; it has Feature (checked with the GitHub API: Business Intent, Feature, Story, Bug, Chore, Spike). The product owner's words: "use Feature instead of EPIC.. organization has feature - right? change work types to use feature as well". An epic is filed as an issue of type Feature, a story as type Story, no label. The kind keeps its name, Epic, in the ontology; only its tracker type is Feature. managing-work.md's work types say so.
