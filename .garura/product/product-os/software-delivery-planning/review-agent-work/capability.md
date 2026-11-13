# Capability: Review what agents make (Argus)

## Directional intent
Review what agents make (Argus): People review business intents, ADRs, memories, domains, capabilities, ICE and agent decisions in one tool.
This is the line for the second capability of Developer tooling that the product owner agreed in his reply to the leans, "yes, record it with self-review dropped". His first words for it were "Review what agents make (Argus): People review ADRs, memories, domains, capabilities and ICE in one tool."; the lean he agreed widened it to name business intents and agent decisions, "which the design shows". The words this page uses:
- A run is one run of a loop. A loop is a command that runs Garura's plays in rounds, on one branch, until its goal is met, and ends by landing one change. The design and its issues call it a drive, its old name ("A Drive Is Now Called a Loop"). A play is a command a person types to run one piece of work from start to end.
- What agents make is what a run leaves behind:
  - business intents: each a need the product meets, in its users' words, which only a person confirms;
  - the ICE under each: the agent intent an agent works from, with its Intent, Context and Expectation;
  - the product model: its domains, capabilities and features, the product's limits and its decisions;
  - ADRs: the records of a decision on how the project is built;
  - memory: what agents decide from, in three tiers (an issue's short-term memory, the project's Garura memory and the global Phoenix memory), with the memory updates that wait for a person;
  - agent decisions: each decision an agent made, with its trace, the steps it took and the memory lines each step rested on.
- A piece is one thing a person answers: one intent, ICE, domain, capability, feature, limit, decision, ADR, memory update or agent decision.
- Argus is the review tool: one web page where a person reads what a run made and answers each piece. It is a Phoenix tool, one of the tools built beside Garura, with no Garura code in it, and it is tracked in the Phoenix project.
- Garura's side is the part inside Garura that opens a review on what a run changed, keeps every answer on the run's branch, has a piece that was sent back reworked, and applies the answers in one commit. The review step is its last part, and the run's last step.
- The contract is the one written agreement between the two: the review pack Garura sends, which carries the pieces by meaning and never as files, the requests, and the events that come back, one numbered event for each action of the person.
- An answer is what a person does to a piece: accept it, send it back with a comment, drop it, comment on it, edit or remove its words, or, for a memory update, approve or reject it in their own words.

This capability does nine jobs:
- Open a review on what a run changed, and keep every answer on the run's branch.
- Read what a run made, as business intents with their ICE and as the product, with the whole model's approval state.
- Answer each piece, in the page or one card at a time.
- Accept or send back each ADR that waits for a person.
- See what memory holds, and approve or reject each memory update that waits for a person.
- Check each agent decision against the memory it rested on.
- Send a piece back and get it reworked.
- Finish the review and have every answer applied in one commit.
- Run Argus apart from Garura, and point Garura at it.

The person reviews the outcome, never the plays. In the product owner's words: "That is what we need to review. That's what the outcome is." and "Reviewing the play itself does nothing." "The pull request is not where the person reviews." It only lands the change.
Argus is where a person gives these answers, and it changes no rule on who may give them:
- Only a person confirms a business intent. Product model must not "let an agent confirm an intent".
- A memory update is decided by the rules of Memory, in Standards, structure, settings and memory: "Only a person decides, one update at a time."
- Accepting an ADR follows Manage ADRs, in Orchestration: "Only a person accepts an ADR. Only where the person does it moves."
- The approval state kept on each piece of the model, and the rule that agents build only from approved pieces, are Product model's. The review step writes it from the person's answers, and "The review tool writes nothing to the model."
Once the answers are applied, the change lands through Ship every change the same way, the first capability of Developer tooling, and the merge waits for the person's yes.
Until Argus exists, a person's answers reach the work in other ways, and each stays as it is:
- A memory update is decided by typing in a session: "the person types the decision in a Claude Code session that records their exact reply".
- A play's checkpoint shows its summary and waits "for the typed response".
- The review of each change posts its verdict on the pull request, and "the comment ALWAYS names its decider".
- A page is written from "text a person approved, word for word".
- At the end of the Discovery loop, the person types confirm or drop for each intent, and the intents stay proposed: the loop "ends at the pull request".
It matters because "Agents now make more in one run than a pull request can show.", and because, in the product owner's words, "agents can only work on things which are approved." It sits in software delivery planning with Ship every change the same way, and the domain's first paragraph says so. It works in the project, on the run's branch and in Argus, and production is never touched.

Features:
- Open a review on what a run changed, and keep every answer on the run's branch (fn-open-review): at a loop's end, Garura works out by meaning what the run changed, sends it to Argus as a review pack, opens the review for the person, and keeps each action as a file on the run's branch as it happens, so no agent reads the web page.
- Read what a run made, as business intents with their ICE and as the product (fn-read-outcome): one calm page shows the whole model's approval state first, then each changed intent with its ICE and each changed domain, capability, feature, limit and decision, in plain words with why it changed, never as files.
- Answer each piece, in the page or one card at a time (fn-answer-pieces): the person accepts, sends back with a comment or drops each changed piece, and may comment on, edit or remove words, in the page or on Catch up cards, where a swipe right accepts and any change is typed.
- Accept or send back each ADR that waits for a person (fn-review-adrs): the ADRs section lists the ADRs that wait and those accepted, and a person's accept is carried out as Manage ADRs says.
- See what memory holds, and approve or reject each memory update that waits for a person (fn-review-memory): the Memory section shows Garura memory and a picked issue's short-term memory, and each waiting update gets its own approve or reject, in the person's words; Ask memory, a question box in plain words, is mocked only.
- Check each agent decision against the memory it rested on (fn-check-agent-decisions): the Agent decisions section shows each decision with its trace, each step's source in its place and checked again, and the person marks it as looking right or sends it back so the agent decides again.
- Send a piece back and get it reworked (fn-send-back): the play that writes that kind of piece reworks that one piece on the run's branch, from the person's comment, and the new version comes back with a reply while the review goes on.
- Finish the review and have every answer applied in one commit (fn-apply-answers): the review step applies all the answers in one commit on the run's branch, writes approval from them, and hands the change to Ship every change the same way.
- Run Argus apart from Garura, and point Garura at it (fn-run-tool-apart): Argus runs as a small server that a person starts once, holds no Garura code, and meets Garura only through the written contract, at the one address Garura's settings name, so it can move later.

What is not built yet:
- Nothing of Argus is built, in Garura or in any other repository. Its design is a draft of 18 October 2026, with a mockup of "made-up shop data", and its stories are open.
- Nothing of Garura's side is built. No part builds a review pack, opens a review, keeps the answers, reworks a piece sent back or applies the answers, and no setting names Argus's address.
- What exists feeds it or stands in for it:
  - Each play inside a loop writes what its checkpoint would have shown into the loop's review folder, and the record reads "decided: false" until the loop's review answers it.
  - The memory tool keeps each memory update and each agent decision with its trace.
  - The Discovery loop "ends at the pull request" with the person's typed confirm or drop, and its record reads "applied_to_model: false".
- No piece of the model carries an approval state yet, so no answer is kept on the piece it answers.
- The story for the three sections is behind the design: it still names one "Memory and ADRs" section, and it writes an approved update to "Garura or Phoenix memory for a promotion", while a page moves up from Argus only to Garura memory, and Phoenix memory is not reached from Garura.

### Benefit hypothesis
- Who it serves: the product owner, who reviews what a run made and gives the answers only a person may give; the agents, which build only from what a person approved; the plays that write each kind of piece, which rework a piece sent back; and Ship every change the same way, which lands the applied answers.
- What we believe: a person who reads what a run made as intents and product, in plain words, and answers each piece in one calm place, judges the agents' work at the level of the outcome without reading raw files, and the agents then build only from what that person approved, if the work stands on these rules:
  - The person reviews the outcome, never the plays.
  - Garura and Argus meet only through the written contract, and Argus holds no Garura code.
  - Every action is one numbered event, kept on the run's branch as it happens, and none is lost.
  - A swipe never changes a piece; every change is typed.
  - The review step applies every answer in one commit, and Argus writes nothing to the model.
  - Only a person answers, by the rules of the part that owns each kind.
- How we will know: as the business intent first written for Argus set out, "After a drive, a person reviews everything it made in Argus — not in a pull request — and every answer is recorded.", "A person can go through a big review one card at a time on a laptop or a phone." and "Argus runs on its own, without Garura's code."; and each run ends in one commit that matches what the person chose.
  - This is not tested today, because nothing of it is built.

### Boundary (In / Out / Never)
- In: opening a review on what a loop's run changed, building its review pack by meaning, and keeping every action as a file on the run's branch.
- In: Argus's five sections, Intents, Product, ADRs, Memory and Agent decisions, read in the page and answered there or one card at a time.
- In: taking the person's answer on each ADR that waits, each memory update that waits and each agent decision, and carrying it out through the part that owns its kind.
- In: having a piece that was sent back reworked by the play that writes its kind, and showing the new version with a reply.
- In: the review step: applying all the answers in one commit and writing approval from them, for a run that ended and for one that stopped.
- In: Argus itself, as a Phoenix tool: its contract, its server and its page, built apart from Garura.
- Out: committing, raising, the outside review, and merging the change with the person's yes. Ship every change the same way, the first capability of Developer tooling, owns them; reviewing a change against its standards is Check the code against its standards, in Code → Validation.
- Out: the approval state on each piece, the rule that agents build only from approved pieces, and how approval is recorded outside the review step. Product model owns them.
- Out: what a memory update is, who may decide it, and what moving a page up does. Memory, in Standards, structure, settings and memory, owns them; the person's yes to move a page to Garura memory is given here.
- Out: recording an ADR, and what accepting one writes. Manage ADRs, in Orchestration, owns it.
- Out: running a loop's rounds, its checker and its questions. Run plays as loops, in Orchestration, owns it.
- Out: writing each kind of piece. The play that writes that kind does it, and here only on the person's send-back.
- Out: the findings and recommendations of Run → Product. This line names none of them, and where they are read is open on their own pages.
- Out: moving Argus into Griffin, which comes later.
- Never: write the model from Argus. The reason: "Plays write the model. The review tool writes nothing to the model."
- Never: let an agent answer a piece: confirm an intent, approve a memory update, accept an ADR or pass its own decision. The reason: Product model must not "let an agent confirm an intent", and "Nothing is approved in bulk, and an agent never answers one".
- Never: change a piece by a swipe. The reason, in the product owner's words: "Any changes have to be entered."
- Never: make the person read raw files to judge a piece. The one exception is an agent decision's source, shown as its memory, file and lines, "because the person must check it". The reason: Developer tooling must not "Make people read raw files to know what was made."
- Never: put Garura code in Argus, or let it read a Garura path. The reason: "it imports no Garura code, so it can move into Griffin later".
- Never: let an agent read the review's web page; the answers reach the work only as files on the run's branch. The reason: "Claude still never reads the web page: the answers are files on the branch".
- Never: move a page to Phoenix memory from a review. The reason, in the product owner's words: "Going to the Phoenix is not designed yet. That would need an organizational change."
- Never: touch production. The reason, in the product owner's words: "We are never touching production."

### Guiding rules
- The outcome, never the plays or the plan. The reason: "Reviewing the play itself does nothing.", and "The plan is not reviewed here."
- One tool, five sections, one review. The reason: the five sections are "Intents | Product | ADRs | Memory | Agent decisions.", kept in one app: "One server, one link, one review."
- Calm, and light on the person. The reason, in the product owner's words: "We don't want it to be a massive PR and add complex cognition load on the user."
- The whole model's approval state each time Argus opens, not only at a run's end. The reason, in his words: "Every time somebody opens up this tool, they should be able to see what is changed, what is approved, and what is in progress."
- Every action goes back to Garura as it happens, and none is lost. The reason, in his words: "Every time a change is made, it should have a direct connection back to Garura for listening."; and "Every event has a number and is kept in a log."
- A send-back reworks one piece, never the whole run. The reason: "The play that writes that kind of piece re-runs for that one piece, on the same branch."
- The answers become real in one commit, and the merge stays the person's. The reason: "The merge stays pinned to the person."
- Easy to move out of Garura. The reason, in his words: "The way I want you to build the tool is that it is easily extractable and movable out of Garura."
- One reviewer in the first version. The reason: two people at once is "Not in version 1."
- Not decided: which runs a review covers, a loop's run only or also a play run by hand, whose review stays its own today: "Run by hand, a play's review is unchanged."
- Not decided: whether Garura's install lays Argus, a setting only points at it, or a team uses it alongside, while BI-8's page says the tools "ship with Garura".

## Sources
- The product owner on 2026-11-10: "Review what agents make (Argus): People review ADRs, memories, domains, capabilities and ICE in one tool.", "yes, record it with self-review dropped"
- The lean he agreed on 2026-11-10: "its line is widened to name business intents and agent decisions, which the design shows.", "Ship every change the same way", "Manage ADRs", "Memory: Agents decide from three tiers of memory (Phoenix global, Garura project, short-term), and people control what enters them.", "Run plays as loops"
- .garura/product/product-os/intents/bi-8.md: "Agents now make more in one run than a pull request can show.", "Make people read raw files to know what was made.", "ship with Garura"
- .garura/product/product-os/intents/bi-11.md: "let an agent confirm an intent"
- The review tool's design, with the product owner's words of 17 to 20 October 2026: "The way I want you to build the tool is that it is easily extractable and movable out of Garura.", "Every time a change is made, it should have a direct connection back to Garura for listening.", "We don't want it to be a massive PR and add complex cognition load on the user.", "Any changes have to be entered.", "Every time somebody opens up this tool, they should be able to see what is changed, what is approved, and what is in progress.", "One server, one link, one review.", "Every event has a number and is kept in a log.", "Nothing is approved in bulk, and an agent never answers one", "because the person must check it", "Claude still never reads the web page: the answers are files on the branch", "Moving memory up is not done here", "Not in version 1."
- The review tool's mockup: "made-up shop data"
- docs/adr/032-drive-review-of-outcomes.md, with the product owner's words: "That is what we need to review. That's what the outcome is.", "Reviewing the play itself does nothing.", "The play that writes that kind of piece re-runs for that one piece, on the same branch.", "The pull request is not where the person reviews.", "The plan is not reviewed here.", "The merge stays pinned to the person.", "Run by hand, a play's review is unchanged."
- docs/adr/033-approval-in-the-product-model.md, with the product owner's words: "agents can only work on things which are approved.", "Plays write the model. The review tool writes nothing to the model."
- docs/adr/036-approved-answer-lands-in-short-term-memory.md: "Only a person accepts an ADR. Only where the person does it moves."
- docs/adr/037-agent-decisions-keep-a-trace-and-the-review-tool-has-five-sections.md: "Intents | Product | ADRs | Memory | Agent decisions."
- docs/adr/045-a-drive-is-now-called-a-loop.md: "A Drive Is Now Called a Loop"
- core/tools/memory/README.md: "Only a person decides, one update at a time.", "the person types the decision in a Claude Code session that records their exact reply"
- standards/rules/gate-config.md, in Phoenix memory: "for the typed response"
- core/components/plays/check-change/SKILL.md: "the comment ALWAYS names its decider"
- core/components/skills/enrich-grounding/scripts/write_approved.py: "text a person approved, word for word"
- core/components/plays/create-play/references/write_loop_review.py: "decided: false"
- core/components/loops/complete-discovery/scripts/record_confirmation.py: "ends at the pull request", "applied_to_model: false"
- .garura/product/product-os/software-delivery-planning/environment-setup/capability.md, the product owner on 2026-11-08: "We are never touching production."
- The stock-take of Developer tooling (2026-11-10), sections 2, 3, 6 and 8.
- The short line beside each feature: the opening words of that feature's own page.
- Shelf: none covers reviewing what agents made. The experience shelf in Phoenix memory, knowledge/domains/experience.md, names "HITL queues & approvals" among the parts that govern the agents built into a product, a loose match only.
- .garura/product/product-os/software-delivery-planning/domain.md: "It also lands every change the same way, with an outside review and a person's yes, and gives people one tool to review what agents made."
- The product owner's words of 2026-11-11: "Argus can only allow from short term to the project memory. Going to the Phoenix is not designed yet. That would need an organizational change."
