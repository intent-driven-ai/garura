# Feature: Give every finding and defect one severity, P1 to P4

## What it does
Anyone who files a defect or reviews a change gives it one severity, P1 to P4, by written rules that start from an industry standard, and the same value says what is fixed first, so a review, a defect and the tracker speak one scale.
- In #934's words: "Anyone who files a defect or reviews a change gives it one severity, P1 to P4, by written rules that start from an industry standard, and the same value says what gets fixed first."
- The rules come in three layers, as #934 plans them:
  - generic: the base is Mozilla's S1 to S4 scale, so P1 blocks work or testing, or loses data, with no way around it, and P4 is cosmetic, with little or no impact;
  - surfaces: what blocked means, and what raises or lowers a level, on the web, on a phone, on an API, on a command line, for a coding agent, and for business rules;
  - architecture and technology: a change is tested against the architecture memory of #933, and a load-bearing pattern broken sets the floor at P1.
- "Severity and the order of fixing are one value". "No second priority field and no matrix."
- "a change is not a defect and gets no severity".
- The product owner, 2026-10-28: "pick which is the closest industry standard and use that … I don't want to keep arguing with everyone that we're coming up with our own standards."
- Today the review of each change gives each finding P1 to P4, and the mechanical table that sorts a change's findings uses the same labels with other meanings: "The scale and the mechanical PR table (`standards/rules/pr.md`) use the same labels with different meanings; one must govern."
- An approved page waits on it: "The severity rules, P1 to P4. #934 holds them, under Standards, structure, settings and memory in the tracker."
- Examples, in different kinds of project:
  - In a bank's payments service, a change breaks the contract of the payments API. By the surface rules for an API, it is P1.
  - In a mobile game, a button sits out of line on a phone. By the surface rules for a phone, it can be P2, where on a wide screen it would be lower.
  - In a news site, a footer has a spelling mistake. It is P4: cosmetic, with little or no impact.
- How it meets the capability: one written standard for how bad a finding is, held the same way by every part that rates one.

Status: not built (#934, findings and defects get one severity, P1 to P4, in three layers; it waits on #933, an architecture memory for teams building a harness). Not built, or open:
- No severity rules are in memory. A first page was taken out of the change it was written in, because it "mixed its own scale with the mechanical PR table".
- The review and the mechanical table use P1 to P4 with different meanings.
- Until the tracker holds one severity field, a defect's text opens with its severity.

## Inputs / Outputs
- In: a finding from a review, or a defect being filed, with the surface it is on.
- In: the written severity rules in three layers, and the architecture memory for the third.
- Out: one severity, P1 to P4, with the rule it rests on and why.

## Rules & behavior
- One severity, P1 to P4, from the closest industry standard. The reason, in the product owner's words: "pick which is the closest industry standard and use that".
- Severity and the order of fixing are one value. The reason: "No second priority field and no matrix."
- A change is not a defect. The reason: "a change is not a defect and gets no severity".
- Not decided: which of the two P1-to-P4 tables governs where they differ; #934 says "one must govern".
- Not decided: how the review of each change records a finding that is a change, not a defect.

## Acceptance criteria
- Given a change that breaks an API's contract, when a reviewer rates it, then it is P1 by the written rules for an API. This is not built.
- Given a defect filed under a story, when it is filed, then it carries one severity and no second priority field. This is not built.
- Given a change that is not a defect, when it is reviewed, then it gets no severity. This is not built.

## Out of scope
- Filing a defect under its story. Record a defect under the story that brought it in (fn-record-defect-under-story), in Track execution in the team's tracker, does it.
- The review's verdict. Check the code against its standards, in Code → Validation, owns it.
- The architecture memory the third layer tests against (#933). Build your own harness, in Standards, structure, settings and memory, owns it.
- The tracker's severity field. Track execution in the team's tracker, in Orchestration, owns it.

## Sources
- GitHub #934 (open): "Anyone who files a defect or reviews a change gives it one severity, P1 to P4, by written rules that start from an industry standard, and the same value says what gets fixed first.", "Severity and the order of fixing are one value", "No second priority field and no matrix.", "a change is not a defect and gets no severity", "The scale and the mechanical PR table (`standards/rules/pr.md`) use the same labels with different meanings; one must govern.", "mixed its own scale with the mechanical PR table", and the three layers; the product owner on 2026-10-28: "pick which is the closest industry standard and use that … I don't want to keep arguing with everyone that we're coming up with our own standards."
- GitHub #933 (open): "A team building a Phoenix harness has an architecture memory to build and review against"
- core/components/memory/standards/rules/pr.md, line 3: "Deterministic mapping from KB quality standard IDs to PR severity buckets P1–P4."
- .garura/product/product-os/software-delivery-planning/track-execution/fn-record-defect-under-story/feature.md, line 53: "The severity rules, P1 to P4. #934 holds them, under Standards, structure, settings and memory in the tracker."
- The stock-take, .garura/project/issues/1021/context/bi-10-inventory/inventory.md, sections 1.7 and 7.1
