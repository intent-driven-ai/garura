# Feature: Define the approval state each kind carries

## What it does
The map names one approval state that every kind of the model carries, approved, changed or in progress, with what an approval keeps, and maps the states of today onto it, so that a person and an agent can tell from the map which parts a person approved.
- ADR 033 (accepted, approval is part of the product model, and agents work only on approved pieces): "Approval is part of the product model itself, not a record kept beside it."
- Its three states: "**Approved** — a person accepted these exact words." The piece keeps a fingerprint of its words, who approved it, when, and in which review. Changed: the piece is new, or its words no longer match the fingerprint. In progress: a person sent it back, and it is being reworked.
- Its one lifecycle, which the map is to hold: "The ontology names one approval lifecycle for every kind and maps these onto it. So a page and its approval state never disagree." An approved business intent is confirmed, an approved decision is accepted, and an approved capability or feature is active.
- #645 (every piece of the model carries its approval state, under #964, each piece carries its approval state and agents build only from approved pieces) plans it: "The ontology (`core/components/memory/standards/schemas/product-os/ontology.md`) names one approval lifecycle for every kind, and maps today's states onto it". It is not built: the map names no approval state.
- A write is never stopped: a write to an approved piece moves it to changed, by its fingerprint, and "No play has to remember to say so."
- Examples, in different kinds of project:
  - In a clinic's booking app, the product owner approves the ICE of the Reminders capability in a review. The map says what that approval keeps, so a reader finds the fingerprint, who approved it and when.
  - In a bank's payments service, a play rewrites an approved feature page. By the map's rule the feature reads changed, and no agent builds from it until a person approves it again.
  - In a game studio's build, a person sends a capability back. It reads in progress until its new version is answered.
- How it meets the capability: the map says not only what each part is, but whether a person agreed to it.

Status: not built (#645, every piece of the model carries its approval state; planned, under #964).

## Inputs / Outputs
- In: ADR 033's states and its mapping of today's states, and the need through the map's play.
- Out: the map, with one approval state for every kind, what an approval keeps, and the mapping of confirmed, accepted and active onto it.

## Rules & behavior
- One approval state for every kind. The reason: "The ontology names one approval lifecycle for every kind and maps these onto it."
- Changed is worked out from the fingerprint, not remembered. The reason: "worked out from the fingerprint, with no play having to remember".
- A rule of approval stops work, never a write. The reason: "A write is never blocked (ADR 031 §2)."
- Not decided: how approval is recorded outside the review step, for a pinned yes in a play run by hand (#647, decide how approval is recorded outside the review step).

## Acceptance criteria
- Given the map, when a reader looks at any kind of the model, then it names the approval state the kind carries, and what an approval keeps. This is not built.
- Given a business intent, a decision and a capability, when a reader looks up their states, then the map maps confirmed, accepted and active onto approved. This is not built.
- Given an approved piece whose words a play changes, when a reader checks it by the map's rule, then it reads changed, and the write was not stopped. This is not built.

## Out of scope
- Keeping the approval state on each part of the model, and the rule that agents build only from approved parts. Manage the model, in Product model, owns them (#964, each piece carries its approval state and agents build only from approved pieces; #646, agents build only from approved pieces).
- Writing approval from a person's answers in the review. Review what agents make (Argus), in Developer tooling, owns it.
- Confirming or dropping a business intent. Only a person does it; the map's play never does it.

## Sources
- docs/adr/033-approval-in-the-product-model.md, the title: "Approval Is Part of the Product Model, and Agents Work Only on Approved Pieces"; line 30: "Approval is part of the product model itself, not a record kept beside it."; lines 40-42: "**Approved** — a person accepted these exact words.", "**Changed** — the piece is new, or its words no longer match the fingerprint it was approved with.", "**In progress** — a person sent it back, and it is being reworked."; line 50: "No play has to remember to say so."; lines 60-64: "An approved business intent is `confirmed`.", "An approved decision is `accepted`.", "An approved capability or functionality is `active`.", "The ontology names one approval lifecycle for every kind and maps these onto it. So a page and its approval state never disagree."
- GitHub #645 (open): "The ontology (`core/components/memory/standards/schemas/product-os/ontology.md`) names one approval lifecycle for every kind, and maps today's states onto it", "worked out from the fingerprint, with no play having to remember", "A write is never blocked (ADR 031 §2)."
- GitHub #964 (open): "Every piece of the product model says whether a person approved it, changed it, or it is still in progress; agents build only from approved pieces."; #646 (open): "An agent takes an ICE only when the ICE itself, the capability or functionality it sits on, and the business intent it is built from are all approved."; #647 (open): "Decide how approval is recorded outside the review step"
- .garura/product/product-os/software-delivery-planning/review-agent-work/capability.md, lines 36 and 87: "The review step writes it from the person's answers", "Out: the approval state on each piece, the rule that agents build only from approved pieces, and how approval is recorded outside the review step. Product model owns them (#964)."
- standards/schemas/product-os/ontology.md, in Phoenix memory: a search of its text on 2026-11-11 finds no approval state.
- The stock-take of Product model, .garura/project/issues/1021/context/bi-11-inventory/inventory.md, sections 1.7, 2.11 and 3.3.
