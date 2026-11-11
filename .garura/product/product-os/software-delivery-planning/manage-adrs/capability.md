# Capability: Manage ADRs

## Directional intent
Manage ADRs: Decisions on how the project is built are recorded closely as they're made, so agents can coordinate many pieces from them.
These are the agreed words for the fourth capability of Orchestration. For what already exists, the product owner said: "Anything that already exists, like managing ADRs and execution tracking, just use what is already built to do that." So this page is written from what is built, and the parts that are not built are named here and wait on research. The words this page uses:
- An ADR, an architecture decision record, is the record of one decision on how the project is built: what was decided and why, the options weighed and why each lost, what it overrides and what it changes. In the product owner's words, "an ADR is only for how this project is being developed".
- An ADR is proposed until a person accepts it. A newer ADR supersedes an older one, in full or in part, or amends a part of it. An accepted ADR is never edited.
- A forward pointer is the one line an older ADR gains when a newer ADR supersedes or amends it: it names the newer ADR and the part it changes. The index is the list of every ADR in the project's ADR folder, with its number, title, status and date.
- The decision play is /record-decision. A play is a command a person or an agent types to run one piece of work from start to end. A loop is a command that runs plays in rounds until its goal is met, and ends in a review where a person answers what it made.
- A business intent is what a person wants, in their words. An agent intent (ICE) is what an agent works from for one part of the product.

This capability does four jobs that are built:
- Record a decision as an ADR, with what it overrides and what it changes.
- Accept an ADR only on a person's word, then or later.
- Keep older ADRs pointing forward and the index current.
- Give the person who accepts every point found on the way, and check it is whole. This one is built in part.

And three jobs that are not built:
- Record the ADR in the change it belongs to.
- Keep ADRs to how the project is built, and move what the model holds into the model.
- Take in each design choice that Spec → Design hands over.

The work is split between parts: the decision play holds the order of the steps and the person's answer, an agent gathers what the decision touches and checks the draft, a skill drafts it, and scripts do the fixed steps. In the decision behind them: "a sub-agent gathers the context and checks, a skill drafts, scripts do the mechanical work; a small play holds the person's approval."
Accepting an ADR by hand is pinned to a person: the decision play waits for the person's typed answer, and no setting turns the wait off. This intent's Must not reads: "Stop a person. Every gate has a way past it that records what's owed." Whether the person's typed answer is the way past this gate, or a stop kept on purpose, is open (#992, every gate has a key). The way past itself, and where what is owed is kept, belong to Give every gate a way past.
Other capabilities hand their decisions here. The four capabilities of Spec → Design decide what each design choice says, and hand the record here, in words such as: "Manage ADRs (Orchestration) owns the records; this capability decides what each choice says and hands it over." Review what agents make (Argus), in Developer tooling, gives the person a card for each ADR that waits, and "the accept is carried out as Manage ADRs says".
It matters because a decision holds only when its reader can see what it replaces: "A new decision is only safe when its reader can see what it replaces." Agents read the accepted ADRs to keep later work in step with them: the outside review reads "the decision records (`docs/adr/**`)" as part of the design a change must follow. It sits in software delivery planning with the other capabilities of Orchestration, and the domain's first paragraph says so.

Features:
- Record a decision as an ADR, with what it overrides and what it changes (fn-record-adr): from a decision brief, the decision is drafted from the one ADR template, with every older ADR it supersedes or amends named with the part, what it changes named by real paths, and its effect on agent intent and on business intents; a decision that would change a person's business intent is stopped and shown to the person.
- Accept an ADR only on a person's word, then or later (fn-accept-adr): run by hand, the decision play waits for the person's typed accept, reject or change; inside a loop it saves the ADR as proposed for the loop's end review; and a proposed ADR is accepted later by hand.
- Keep older ADRs pointing forward and the index current (fn-keep-adrs-linked): once an ADR is accepted, each older ADR it changes gains one forward pointer, the only edit it ever gets, and the index is rebuilt from the ADR folder.
- Give the person who accepts every point found on the way, and check it is whole (fn-show-accepter-findings): each thing found while the ADR was drafted that the brief did not ask about is written in its own section, with its five parts, and shown before the person decides. Built in part.
- Record the ADR in the change it belongs to (fn-adr-in-its-change): not built. The decision play, run on the branch of a change that is already open, records the ADR in that change (#822, under #968).
- Keep ADRs to how the project is built, and move what the model holds into the model (fn-keep-adrs-to-build): not built. Every ADR is reviewed, and what is about what the product model holds moves into the model (#1022).
- Take in each design choice that Spec → Design hands over (fn-take-design-choices): not built. Each design choice of the four capabilities of Spec → Design reaches the decision play as a decision brief.

What is not built yet:
- An ADR cannot be recorded in the change it belongs to. Run by hand, the decision play opens its own change from main, so "the change lands without its ADR, and the issue stays open until a second, small change records the ADR. This happened on #816" (#822).
- An older ADR can be left with no forward pointer while the run reports it linked (#850).
- The decision play does not check that the points for the person who accepts are gathered and whole (#935), and the templates index does not name their section (#941).
- No play hands a decision to the decision play. Only a person runs it today, and no loop runs it: the one loop that is built, the Discovery loop, runs /discover-intent, /discover-domains and /discover-capabilities.
- Nothing catches a decision made in a session that no one records.
- The ADRs have not been reviewed for what belongs in the product model instead (#1022).

### Benefit hypothesis
- Who it serves: the technical lead and the developer, who record decisions on how the project is built; the person who accepts each ADR, such as the product owner or the technical lead; the agents and plays that read the accepted ADRs to keep later work in step, such as the outside review; and the capabilities that hand their decisions here, the four of Spec → Design and the ADR cards of Review what agents make (Argus).
- What we believe: when each decision is recorded as it is made, from one template, with what it overrides and what it changes in plain view, and is accepted only by a person, people and agents can coordinate many pieces from the decisions that hold, if the work stands on these rules:
  - What a decision overrides and changes is shown before anyone accepts it.
  - Only a person accepts an ADR.
  - An accepted ADR is never edited; an older one gains only its forward pointer.
  - The index is rebuilt after each accept.
  - An ADR never changes a person's business intent.
- How we will know: every ADR in the ADR folder has a row in the index with its own status; every accepted ADR names who accepted it, with that person's typed answer on record; every older ADR named in an accepted ADR's Supersedes or Amends line points forward to it; and no ADR changed a person's business intent.
  - The third does not hold in every case today (#850).
  - Whether each ADR landed in the change it belongs to is not tested, because it cannot today (#822).

### Boundary (In / Out / Never)
- In: recording a decision as an ADR from the one template, with what it overrides, what it changes, its effect on agent intent and its business-intent check, in a run that writes nothing else.
- In: accepting an ADR only on a person's word: by hand at a pinned checkpoint, at a loop's end review, or later by hand.
- In: the forward pointers on older ADRs, and the index of ADRs.
- In: the points found on the way for the person who accepts, and their check.
- In, not built yet: recording the ADR in the change it belongs to, keeping ADRs to how the project is built, and taking in each design choice that Spec → Design hands over.
- Out: product decisions in the product model, such as a move of the product profile, kept as a `decision.yaml` record. Product model owns them. The decision play has a second shape for them, but the one product decision in the model was written by /discover-capabilities, whose save step "writes one decision per box-move".
- Out: what each design choice says. The four capabilities of Spec → Design decide it: Design the technology and architecture, Deployment design, Environment setup and Manage surfaces. This capability records what they hand over.
- Out: the card where a person accepts or sends back an ADR in the review tool. Review what agents make (Argus), in Developer tooling, owns it; the accept it carries out is this capability's.
- Out: the ADR template as a standard, the names of the parts, and the settings that turn checkpoints on or off. Standards, structure, settings and memory owns them.
- Out: reviewing a change that adds or changes an ADR, and its verdict. Check the code against its standards, in Code → Validation, owns it.
- Out: opening and landing the change an ADR is recorded in. Ship every change the same way, in Developer tooling, owns it.
- Out: running a loop's rounds and its end review. Run plays as loops owns the run, and Review what agents make (Argus) owns the review.
- Out: the way past the pinned accept, and where what is owed is kept. Give every gate a way past owns them.
- Out: ordering the work a decision opens, and tracking it in the team's tracker. Orchestrate agent work through planning and Track execution in the team's tracker own them.
- Never: let anyone but a person accept an ADR. The reason: "Only a person accepts an ADR."
- Never: edit an accepted ADR, other than its forward pointer. The reason: "An accepted ADR is never edited."
- Never: let an ADR change a person's business intent. The reason: "An ADR never changes a person's business intent."
- Never: write a record off the template. The reason: "no record is written off the template".
- Never: make up a decision's reasons, options or consequences. The reason: "No outside research: a decision's reasons come from the brief and the person, never from you."

### Guiding rules
- Show what a decision overrides and changes before anyone accepts it. The reason: "A new decision is only safe when its reader can see what it replaces."
- A script finds the older ADRs that may be affected; reading them decides. The reason: "Candidates are found mechanically; which ones really apply is judged by reading them."
- Scripts do the fixed steps, an agent the judgment, a skill the draft, and the play the person's answer. The reason: "a sub-agent gathers the context and checks, a skill drafts, scripts do the mechanical work; a small play holds the person's approval."
- Every check runs before the first write. The reason: "Every check runs before the first write, so a stop writes nothing".
- A run writes only the record, the forward pointers and the index. The reason: a script checks that "only the record, its pointers, the index and the run's own records changed".
- Run by hand, the decision play opens and lands its own change; inside a loop it opens nothing and does not stop. The reason: "run by hand it opens and lands its own change; handed a loop's contract, it opens no issue or branch of its own and works on the loop's branch."
- An ADR is only for how the project is built. The reason, in the product owner's words: "an ADR is only for how this project is being developed".
- Not decided: whether product decisions in the model are written by this capability's tool or by the model's own plays.
- Not decided: whether the person's typed answer at the pinned accept is the way past it that Orchestration's Must not asks for, or a stop kept on purpose (#992).
- Not decided: whether the rule that an ADR never changes a person's business intent is reworded once every ADR is reviewed (#1022).

## Sources
- .garura/project/issues/1021/context/capabilities.md, the list set on 2026-11-10: "Manage ADRs: Decisions on how the project is built are recorded closely as they're made, so agents can coordinate many pieces from them.", "Anything that already exists, like managing ADRs and execution tracking, just use what is already built to do that.", "the domain (lean: software delivery planning, its opening widened, as for BI-6, BI-7 and BI-8)"
- .garura/product/product-os/intents/bi-9.md: "Stop a person. Every gate has a way past it that records what's owed."
- .garura/product/product-os/software-delivery-planning/design-technology-architecture/capability.md: "Manage ADRs (Orchestration) owns the records; this capability decides what each choice says and hands it over."
- .garura/product/product-os/software-delivery-planning/deployment-design/capability.md and .garura/product/product-os/software-delivery-planning/environment-setup/capability.md: the same words, in their Out lines
- .garura/product/product-os/software-delivery-planning/manage-surfaces/capability.md: "Manage ADRs (Orchestration) owns the records; this capability decides what the update says and hands it over."
- .garura/product/product-os/software-delivery-planning/review-agent-work/fn-review-adrs/feature.md: "the accept is carried out as Manage ADRs says"
- core/components/plays/record-decision/SKILL.md: "Only a person accepts an ADR.", "no record is written off the template", "Every check runs before the first write, so a stop writes nothing", "only the record, its pointers, the index and the run's own records changed"
- core/components/plays/record-decision/reference/ice.md: "Candidates are found mechanically; which ones really apply is judged by reading them.", "An ADR never changes a person's business intent.", "a sub-agent gathers the context and checks, a skill drafts, scripts do the mechanical work; a small play holds the person's approval.", "run by hand it opens and lands its own change; handed a loop's contract, it opens no issue or branch of its own and works on the loop's branch."
- core/components/agents/adr-keeper.md: "A new decision is only safe when its reader can see what it replaces.", "No outside research: a decision's reasons come from the brief and the person, never from you."
- core/components/skills/author-decision/SKILL.md and its scripts/adr.py: the draft, and the fixed steps (next number, check, index, candidates, pointers, accept, guard)
- core/components/agents/change-reviewer.md: "the decision records (`docs/adr/**`)"
- core/components/loops/complete-discovery/SKILL.md: "You run `/discover-intent`, `/discover-domains` and `/discover-capabilities`"
- standards/templates/adr.md, in Phoenix memory: "An accepted ADR is never edited.", "An ADR never changes a person's business intent."
- .garura/product/product-os/decisions/dec-cap-initialize-security-none-medium.yaml: the one product decision in the model, "decided_by: /discover-capabilities"
- core/components/plays/discover-capabilities/SKILL.md: "writes one decision per box-move"
- docs/adr/ and docs/adr/_index.md: the ADRs recorded so far, and their index
- GitHub #1022 (open), the product owner on 2026-11-02: "an ADR is only for how this project is being developed", "That rule, in the ADR template, may need rewording once this review is done."
- GitHub #822 (open): "the change lands without its ADR, and the issue stays open until a second, small change records the ADR. This happened on #816"
- GitHub #968 (open): "A person records a decision as an ADR, in the change it belongs to, and sees every point found on the way"
- GitHub #992 (open): "A gate in Garura is never a hard stop: it always has a key to pass it, and using the key records what must be done later."
- GitHub #850, #935 and #941 (open): the known defect and the planned work named under What is not built yet.
- GitHub #632 (closed), the product owner on 2026-10-09: "check if this adr invalidates any older ones"
- The stock-take of Orchestration, .garura/project/issues/1021/context/bi-9-inventory/inventory.md, sections 4, 6.3, 9, 10 and 11 (lean 6): "Nothing catches a decision made in a session that no one records."
- The short line beside each feature: the opening words of that feature's own page; for the three with no page, lean 6 of the stock-take and the issue named.
- Shelf: none. No knowledge shelf in any memory tier covers how a team keeps its ADRs; knowledge/review/adrs.md, in Phoenix memory, covers only how a change that adds or changes one is reviewed.
- .garura/product/product-os/software-delivery-planning/domain.md: "It also orchestrates the work: it chooses and orders what runs next, runs plays as loops, tracks the work in the team's tracker, records each decision on how the project is built as an ADR, and gives every gate a way past."
