# Review what agents make (Argus): research and drafts (issue 1021, BI-8 capability 2)

Draft only, 2026-11-10. Nothing under `.garura/product/`, `.garura/core/` or `.claude/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-8-capability-2/drafts/product-os/software-delivery-planning/review-agent-work/`: the capability page and its ICE page, and nine feature pages, each with its ICE page. All ten ICE pages carry the thin mark, because nothing of this capability is built. They sit under software delivery planning for now; the domain is settled at BI-8's close, and the capability page says so.

In one line: Argus, the review tool, and Garura's side of the review are designed in detail and filed as stories, and none of it is built, in Garura or anywhere else. What Argus would show is already kept as data (memory updates, agent decisions with their traces, proposed ADRs, the plays' review records), and today a person's answers reach the work in other ways: typed in a session, typed at a checkpoint, posted on the pull request, or written word for word to a page.

What this run did besides reading:
- It copied the memory files it decided from into `bi-8-capability-2/memory/`, with `manifest.json`, all from Phoenix memory through the memory tool: the grounding templates (`_content-standard.md`, `capability.md`, `feature.md`), the checkpoint setting rule (`standards/rules/gate-config.md`), the loop contract (`standards/rules/loop-contract.md`) and the experience domain shelf (`knowledge/domains/experience.md`).
- It searched Phoenix memory through the memory tool for review tool, Argus, human review and approve each. Only the experience shelf answered, with its line on "HITL queues & approvals" for the agents built into a product (lines 162-172): a loose match, quoted on the capability page as a shelf only.
- It read GitHub, read only: #680, #681, #641, #642, #643, #644, #664, #648, #649, #650, the spike #647, #617, #964, the states of #645, #646, #658, #659 and #569, #681's place in the Phoenix project (Status Todo, Garura tools Argus), and the Phoenix project's repository (`gh repo view intent-driven-ai/phoenix`: empty).
- It did no web research, so no memory update is raised.
- It ran no placement: the domain is not reopened.
- The decisions made from memory are in `cite-request.json`, for the caller to record with `memory.py cite` (the tool writes outside this run's folder).
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.
- One slip, outside this folder: the work area for checks is shared with the drafter of BI-8's first capability, whose check scripts had the same names. Running them once by mistake re-ran that drafter's own checks on its own drafts, which rewrote `bi-8-capability-1/checks/quotes.json` and `bi-8-capability-1/checks/ice-shape.json` from those drafts as they stood. Nothing else there changed. This run's checks were then run again from scripts of its own.

## The line, and the name

- His first words (`page-approvals.md` line 8): "Review what agents make (Argus): People review ADRs, memories, domains, capabilities and ICE in one tool."
- The lean he agreed (`capabilities.md` line 90): "its line is widened to name business intents and agent decisions, which the design shows."; his reply (`page-approvals.md` line 9): "yes, record it with self-review dropped".
- The line on the page: "Review what agents make (Argus): People review business intents, ADRs, memories, domains, capabilities, ICE and agent decisions in one tool."
- Stand: the line adds only the two words he agreed. The brief also lists features among what the line names; the old line does not name them, and the lean he agreed adds only business intents and agent decisions. Adding features would put a third word in his line that he did not see. Features stay on the page through the Product section (domain, capability and feature, `review-tool.md` lines 206-211). If he wants features named in the line, it is one word.
- Name and folder: Review what agents make (Argus), `review-agent-work`, as the brief sets.
- His words on drafting (`page-approvals.md` line 10): "yes.. these are all built and we are buildign not from resarch but acual implementation... so build all not just one". Stand: for this capability "these are all built" does not hold. The evidence is in "What is built" below. Every feature is drafted, as "build all" asks, and every one is marked not built.

## What is designed

- **The design**, `.garura/project/issues/617/specs/review-tool.md` (576 lines, status draft, updated 2026-10-18), with the mockup beside it (`review-tool-mockup.html`, "made-up shop data", line 682). It holds the idea (lines 47-56), the rules that keep the tool movable (lines 58-90), how Garura and the tool talk (lines 92-146), the review pack (lines 148-183), what the person sees, with Catch up and the three later sections (lines 185-346), what the person can do (lines 348-372), approval in the product model (lines 374-427), the build order in nine stories (lines 460-524), risks (lines 526-541), and two open decisions, D1 and D2 (lines 543-557). Line 576 moves the tool out: "the tool is Argus, a Phoenix tool" and "the review tool needs to be built separately".
- **The spike's notes**, `.garura/project/issues/617/specs/decisions.md`, Q1 to Q7, with the product owner's words of 17 October.
- **ADR 032**: the review is the last step of a run (§1), on the outcome, not the plays (§2), not on the pull request (§3, line 49), accept, drop or send back (§4), the answers applied as one commit with the merge pinned to the person (§5, lines 59-69), a stopped run gets the same review (§6), a dropped box-move (§7); "Run by hand, a play's review is unchanged." (line 99).
- **ADR 033**: approval lives in the model, on every piece (§1), three states (§2), agents work only on approved pieces (§3), approval follows links (§4), only the review step writes approval and "The review tool writes nothing to the model." (§6, line 68), the tool shows the whole model's state each time it opens (§7, line 72).
- **ADR 036 §7** and **ADR 037 §3-§4**: memory and ADRs are reviewed in the tool; five sections, Intents, Product, ADRs, Memory and Agent decisions (ADR 037 line 48); Ask memory, a plain-words search over the three tiers on the same memory tool, "mocked only for now" (line 62).
- **ADR 041 §7**: "Until Argus exists, a drive ends at the pull request" (line 70), with the person's typed confirm or drop kept in short-term memory.
- **ADR 045**: a drive is now called a loop. The design and the issues still say drive; the pages say a loop's run.
- **#680** (closed as not planned on 2026-11-02, "Replaced by garura-intents#8."): "It is a Phoenix tool, built separately from Garura and tracked in the Phoenix project under **Garura tools**"; "it imports no Garura code, so it can move into Griffin later"; and four lines under "How this will be judged", quoted on the capability page.
- `.garura/user-provided/managing-work.md` lines 110-115: "Tools built beside Garura — Argus (the review tool), and later Griffin, Sphinx and others — are Phoenix tools".

## What is built

Nothing of Argus:
- No folder in Garura's tracked source holds it. The folder the design first named, `core/tools/outcome-review/` (line 64), which #641, #642, #643 and #644 still name, has no history: `git log --all -- core/tools/outcome-review` printed nothing on 2026-11-10.
- No setting names it: `review.server_url`, which #648 asks for and the design names (line 85), is not in `core/config.yaml`.
- No other repository holds it: the Phoenix project's repository is empty (`gh repo view intent-driven-ai/phoenix`, checked 2026-11-10). #681 reads Todo in the Phoenix project, with Garura tools set to Argus.
- A local prototype that the design names, `core/tools/play-reviewer/` (`review-tool.md` lines 304-307 and 514-524), is on this machine, outside git (listed in `.git/info/exclude`). Its own guide calls it "A small browser tool to review one Garura play and leave comments for Claude." ADR 037 says "a local prototype stands in for memory approvals" (line 98). It is not Argus and not tracked; the memory tool's updates were all decided in a session, none in a review tool (stock-take section 2.4). The pages do not rest on it.

Nothing of Garura's side: no script builds a review pack, opens a review, listens, has a piece reworked or applies the answers. No tracked file is named `build_review_pack.py`, `open_review.py` or `review_listen.py` (`git ls-files`, 2026-11-10); only the design and #648 name them. #648, #649 and #650 are open.

What exists that Argus and the review step would read, call or replace:
- **The plays' review records inside a loop.** Each play writes what its checkpoint would have shown into the loop's review folder, "so the loop's end review can read every play's record in one place", and the record "reads `decided: false` until the loop's review answers it" (`core/components/plays/create-play/references/write_loop_review.py` lines 4-8); with `--decisions`, "the record then carries every decision the play made, each with its trace" (lines 15-18). The loop contract says the same: "The loop's end review reads the record." (Phoenix memory `standards/rules/loop-contract.md`, rule 4, lines 69-75). This is the input for the pack's line on why each piece changed.
- **The memory tool** (`core/tools/memory/README.md`): `cite` and `citations --check` keep each agent decision with its trace and read every step's source again (lines 127-128); `propose`, `updates`, `decide` and `apply` keep each memory update (lines 134-137), and `decide` names where a person decided, "`review-tool`, or `session`" (line 136). The design's Garura half of the three sections calls these (`review-tool.md` lines 504-508).
- **ADRs.** `/record-decision` saves an ADR as proposed inside a loop, and the person accepts it "at the loop's final review with `/record-decision accept <file>`" (`core/components/plays/record-decision/SKILL.md` line 202).
- **The stand-in at a loop's end.** "Until the review tool (Argus) exists, Discovery ends at the pull request" (`core/components/loops/complete-discovery/scripts/record_confirmation.py` lines 4-8), and its record reads `applied_to_model: false   # Argus's review step writes the approval (#650)` (line 71).
- **The mockup as a test input.** The Discovery loop's runs were made "on the Argus mockup" (ADR 041 line 7), and the rebuild eval reads `argus.html` (`core/tools/rebuild-eval/README.md` line 75).

How a person's answers reach the work today (stock-take section 2.4, re-checked):
- Memory updates: "the person types the decision in a Claude Code session that records their exact reply" (`core/tools/memory/README.md` lines 147-149).
- Checkpoints: "render the approval prompt, wait for the typed response." (Phoenix memory `standards/rules/gate-config.md` lines 114-115).
- The review of each change: "the comment ALWAYS names its decider" (`core/components/plays/check-change/SKILL.md` lines 331-332).
- Pages: `write_approved.py` writes "from text a person approved, word for word" (line 3); `author-intent-page` "never confirms by itself" (`SKILL.md` line 78).
- The end of the Discovery loop: typed confirm or drop, kept in short-term memory, the model untouched.
- What does not exist: an approval state on each piece (#964, with #645, #646 and the spike #647), so no answer is kept on the piece it answers.

## What is only in issues

| Issue | What it is about | State |
|---|---|---|
| #681 | Argus itself: a person reads a run's outcome and answers each piece | open; Phoenix project Todo |
| #641 | The written contract: the pack, the requests, the events | open |
| #642 | The server, keeping every action as a numbered event | open |
| #643 | Reading a review: the whole model's state, intents with their ICE, the product | open |
| #644 | Answering in the page or one card at a time | open |
| #664 | The memory and ADR sections (filed as one "Memory and ADRs" section) | open |
| #648 | Garura opens a review on what a run changed and keeps every answer on its branch | open |
| #649 | A piece sent back comes back reworked, with Garura's reply | open |
| #650 | The run's last step applies the answers in one commit and writes approval | open |
| #645, #646, #647 | Approval state on every piece; agents build only from approved pieces; the spike on approval outside the review step | open, under #964 (Product model) |
| #680 | The business intent for Argus | closed as not planned, replaced by BI-8's tracker issue |

Out of step, found and not filed:
- #641, #642, #643 and #644 each say "The tool lives in `core/tools/outcome-review/`" inside Garura, against the 20 October decision that "the review tool needs to be built separately" (`review-tool.md` line 576) and #680's "built separately from Garura". The pages follow the later decision.
- #664 (known, stock-take section 2.3): one "Memory and ADRs" section, and an approved update written to "Garura or Phoenix memory for a promotion", against ADR 037 §3 and the design's "Moving memory up is not done here" (lines 327-328). The pages follow the design.
- The titles of #681 and #648-#650 say "drive", the old name of a loop (ADR 045).
- The mockup's ADR card says "The /adr play reworks it from your comment."; the decision play is `/record-decision` now. The pages say the decision play.

## The persona

- Who reviews: **the product owner**. BI-8 is "Asked by: the product owner" (`intents/bi-8.md` line 7). ADR 032 and the design speak of "the person", with one reviewer in the first version (`review-tool.md` line 538: "Not in version 1."). The answers only a person may give, confirming an intent and accepting an ADR, are the product owner's in every approved page so far. In another project it is the person who gave the loop its goal; the pages say the product owner, as BI-7's did.
- Who else it serves, named in the Benefit hypothesis: the agents, which build only from what a person approved (Product model's rule, #964); the plays that write each kind of piece, which rework a piece sent back; Ship every change the same way, which lands the applied answers.
- No real names: the design and the ADRs name a person; the pages say the product owner and quote only his words.

## The features

Nine, from the stock-take's lean 5, with #664 split into three. Each is a job a person does; none is built.

1. **Open a review on what a run changed, and keep every answer on the run's branch** (`fn-open-review`). At a loop's end, Garura builds the pack by meaning, opens the review, and keeps each action as a file on the branch. Not built. #648; design §2-§3 and story 5.
2. **Read what a run made, as business intents with their ICE and as the product** (`fn-read-outcome`). The overview with the whole model's approval state, then Intents and Product, with the two switches. Not built; the mockup shows it. #643; design §4 and story 3; ADR 033 §7.
3. **Answer each piece, in the page or one card at a time** (`fn-answer-pieces`). Accept, send back, drop, comment, edit, remove; Catch up, where a swipe right accepts and any change is typed. Not built; the mockup shows it. #644; design §4 item 6 and §5; #681's decided line.
4. **Accept or send back each ADR that waits for a person** (`fn-review-adrs`). Not built; ADRs are accepted by typing today. #664; ADR 037 §3; design §4 item 7.
5. **See what memory holds, and approve or reject each memory update that waits for a person** (`fn-review-memory`). Ask memory is mocked only. Not built; the memory tool's side exists. #664; ADR 037 §3-§4; design §4 item 7.
6. **Check each agent decision against the memory it rested on** (`fn-check-agent-decisions`). Not built; the traces and their check exist. #664; ADR 037 §1-§3; design §4 item 7.
7. **Send a piece back and get it reworked** (`fn-send-back`). Not built. #649; ADR 032 §4; ADR 033 §2; design story 6.
8. **Finish the review and have every answer applied in one commit** (`fn-apply-answers`). Not built; the Discovery loop's typed stand-in exists. #650; ADR 032 §5-§7; ADR 033 §6; design story 7.
9. **Run Argus apart from Garura, and point Garura at it** (`fn-run-tool-apart`). Not built. #641 and #642; design §1-§2, story 1 and 2; #680.

Why #664 is three features: ADR 037 split the one section into three because "a person's ADRs, the memory that exists, and the agents' decisions are three different things to review." (line 110). Each has its own answers (accept or send back; approve or reject in the person's words; looks right or send back, `review-tool-mockup.html` lines 1286-1295) and its own owner of the rules (Manage ADRs; Memory; the trace is the memory tool's `cite`). The other way, one feature for #664, keeps the story whole but puts three jobs on one page, against "one job is one feature".

Why the contract and the server are one feature: the person's job is one, start Argus once and point Garura at it; #641 and #642 are its two halves.

Order on the capability page: the person's path (open, read, answer, the three sections, send back, finish), then running Argus.

Built pieces of Garura's side: none. The parts that exist (the review records, the memory tool's commands, the decision play's accept, the stand-in) are inputs or stand-ins, named on each page's Status line, not features of this capability.

## Hand-off to Ship every change the same way

Ship every change the same way is BI-8's first capability, drafted at the same time by someone else; these drafts name it and do not draft it.
- The review step makes its one commit on the run's branch; "Then the end sequence lands the change. The pull request only lands it. The merge stays pinned to the person." (ADR 032 §5, line 69). Committing, raising, the outside review and the merge are Ship's; the outside review itself is BI-4's.
- For a dropped run, ADR 032 §6 says "the pull request is closed, the branch is deleted, and nothing merges". Who does the closing and the deleting is left as a Not decided line on `fn-apply-answers` (open point 11).

## The open points, each with options and a lean

None is decided here. The pages state each as Not decided, with no lean. The decided points are not reopened: the capability holds the whole review, Garura's side and Argus; Argus is a Phoenix tool with no Garura code (#680); the widened line; the owning intents' rules on who may confirm; every feature not built and every ICE thin; the domain for now; production never touched.

### 1. What BI-8's "tools that ship with Garura" means for a tool built outside Garura

- **A. Laid by Garura's install.** Install into a project lays Argus beside the plays. Gain: one step gets a team everything. Cost: a Phoenix tool, "built separately from Garura", would arrive inside Garura's install, and the install would have to lay a server; the design says a person starts it "once" and "Claude only checks `/v1/health` and never starts it" (lines 528-531).
- **B. Pointed at by a setting.** Garura's settings name Argus's address (`review.server_url`, design line 85, #648); a person starts Argus once, on a laptop or hosted; Garura checks it is up and never starts it. Gain: it is what the design and #648 already say, and "Moving the tool to Griffin means moving one folder and changing one address in Garura's config." (lines 55-56). Cost: a team without Argus running gets no review tool, only the stand-in.
- **C. Used alongside, with nothing in Garura.** Gain: no tie at all. Cost: Garura could not open a review or check that the tool is up.

Lean: **B**. BI-8's outcome words "in tools that ship with Garura" (`intents/bi-8.md` line 3) then need new words at BI-8's close, such as "in tools that work with Garura", in words the product owner approves.

### 2. Which runs "a whole run" covers (BI-8's proof "A person reviews a whole run in the tool.")

- **A. A loop's run only.** ADR 032 §1 makes the review a loop's last step, and "Run by hand, a play's review is unchanged." (line 99).
- **B. A play run by hand too.** Each play run by hand also opens a review in Argus at its end. Cost: every play's own checkpoint changes, through each play's ICE source.
- **C. Any time, everything not approved.** Argus opens on the whole model each time (ADR 033 §7); a review can be opened on all that is not approved, whatever wrote it. Cost: a review not tied to a run has no run's branch for its answers; where they land is not designed.

Lean: **A** for opening a review and applying its answers, with what Argus shows each time it opens being the whole model's state (ADR 033 §7), so a piece a play wrote by hand shows there as changed too. The product owner's words of 18 October lean the same way: "for any of the commands later on, as you set and change a business intent, an [ICE], or the product model, this tool needs to keep good track of what is approved and what needs to be changed." (`review-tool.md` lines 376-378).

### 3. Where BI-6's findings and recommendations get reviewed

- **A. In Argus, as new kinds in the pack.** Kinds are data, "A product other than Garura could send its own kinds." (line 69), so nothing in Argus changes; and he wants "every review in the one tool" (ADR 036 line 137).
- **B. A file in the project, beside BI-6's report.** BI-6's own pages name it as one option.
- **C. In the plan session, where a change is approved before it lands.**

Lean: **A**, once he names it. Until then this line names no recommendation, and BI-6's "Not decided" lines stand as they are.

### 4. Which tool comes after Argus

- **A. None named.** "Argus comes first" stays with no second until he names one.
- **B. The status display for Claude Code** (ADR 041 §6). It shows where a run stands and reviews nothing.
- **C. Griffin or Sphinx** (`managing-work.md` line 110). They are later Phoenix tools, not review tools.

Lean: **A**. No source names a second review tool; it is his to name.

### 5. How events reach Garura (the design's D1, lines 545-550)

- **A. Garura's listener connects to Argus and reads its event stream.** The design recommends it: "no server in Garura, works on a laptop and hosted, already proven in both prototypes".
- **B. Argus calls a Garura address on every event.** It needs Garura to run a server, and a hosted Argus cannot reach a laptop.

Lean: **A**, as the design recommends. #642 says to settle it with the product owner before the stream is built.

### 6. A person's own edits (the design's D2, lines 552-557)

- **A. Allow them, and amend ADR 032 through the decision play**, so the review step applies the edit and checks it against the ontology.
- **B. Keep ADR 032 as is**: Edit becomes a send-back that carries the new words, and the play writes them.

Lean: **A**, as the design recommends: he asked for "giving comments, doing edits, deleting something" (line 33-34). #644 says to settle it with him before Edit is built.

### 7. Who writes the approval when a person accepts a card, and what an answer on an agent decision writes

ADR 036 (line 121) and ADR 037 (line 101) leave both open; ADR 033 §6 says only the review step writes approval.
- **A. The review step, at Finish,** carrying each answer through its owner: the memory tool's `decide` with the person's words and then `apply`; the decision play's accept for an ADR. An agent decision's "Looks right" writes nothing more than the kept answer; a send-back has the agent decide again.
- **B. Each card at once**, as soon as the person answers it.

Lean: **A**: it keeps ADR 033 §6 and ADR 032 §5's one commit, and the design's own Garura half of the three sections says "Garura calls the memory tool's `decide` with the person's words and then `apply`, and the `/adr` accept for an ADR" (lines 506-508). Cost: a memory update that blocks the work waits until Finish.

### 8. Where a product decision that waits for a person is answered

- **A. Under the Product section's decisions.** ADR 032 §2 lists decisions in the product model.
- **B. In the ADRs section.** ADR 036 read literally ("every ADR review happens there").

Lean: **A**: ADR 037 §3 defines the ADRs section as "the ADRs a person records with `/adr`", the project's own decisions; a product decision is a piece of the product.

### 9. Whether the Memory section lists Phoenix memory

- **A. Garura memory and the picked issue's short-term memory listed; Phoenix memory reached through Ask memory.** His brief: "omstly garura memory inside the projecdt, and once an issue is selected then its STM" (ADR 037 line 56).
- **B. All three tiers listed**, as ADR 036 §7 had it.

Lean: **A**, from his brief.

### 10. Where Argus's code is kept

- **A. Its own repository under the Phoenix project**, as "built separately" asks.
- **B. A folder inside Garura**, as #641-#644 still say.

Lean: **A**. The Phoenix project's repository is empty today, so the choice is open. #641-#644 then need their "The tool lives in" lines changed when he says so.

### 11. Whether Finish waits for every changed piece to have an answer

#644 says "Finish review unlocks when every changed piece has an answer." Orchestration's Must not (`intents/bi-9.md` line 13) is "Stop a person. Every gate has a way past it that records what's owed."
- **A. Keep #644's rule.** A review applies only once every piece is answered.
- **B. Let the person finish at any time.** The pieces left unanswered stay changed, are named as owed in the commit's record, and no agent builds from them (Product model's rule).

Lean: **B**, because it keeps Orchestration's Must not, and an unanswered piece is still safe: it is not approved. This is the one place the design adds a stop for the person; it is named here so it is not added unseen. The page states it as Not decided.

Also on the pages as Not decided, with no lean: who closes the pull request and deletes the branch of a dropped run (point in the hand-off above; lean: Ship every change the same way, which owns the pull request and the branch).

## Lines of other intents' approved pages, checked against the drafts

- **BI-6, `understand-consumers-and-competition/fn-hand-on-findings/feature.md`** line 18 ("A review tool where people review what agents make is planned, and not built for findings of this kind."), line 35 (Not decided: "such as a file in the project or the planned review tool"), line 47 ("Building the review tool. Review what agents make, in Developer tooling, owns it."), `ice.md` line 16: all hold. Line 52 quotes the list of 3 November as it was; it holds as a dated quote.
- **BI-6, `build-or-update-product/fn-recommend-changes/feature.md`** line 37: "the planned review tool, whose agreed line names "ADRs, memories, domains, capabilities and ICE" and no recommendation." Its point holds: the widened line still names no recommendation. Its quote no longer is the agreed line once the widened line is approved. Owed when BI-6's page is next touched, or at BI-8's close, in words he approves. Lines 51 and 55 and `ice.md` line 16 hold.
- **BI-8's own page**, `intents/bi-8.md` line 3: "reviewing ADRs, memories, domains, capabilities and ICE in tools that ship with Garura" does not hold against the widened line and open point 1; owed at BI-8's close, in his words. The proof "A person reviews a whole run in the tool." (line 10) holds under open point 2's lean. "Their answers become part of the work." (line 11) holds: it is `fn-apply-answers`. The Must not, "Make people read raw files to know what was made." (line 13), holds; the one exception the design makes, an agent decision's source shown as its memory, file and lines, is shown inside Argus and is named on the capability page.
- **BI-11's Must not**, "let an agent confirm an intent" (`intents/bi-11.md` line 15): holds; the pages quote it as the reason.
- **BI-10's Memory line** and **BI-9's Manage ADRs line** (`capabilities.md` lines 106 and 99): hold; the pages hand both to their owners.
- **BI-9's Must not** (`intents/bi-9.md` line 13): holds on every page, given open point 11 stays open until he answers it.
- **BI-4 and BI-3 lines** that name Developer tooling name Ship every change the same way, not this capability; nothing here touches them.

## Checks

- Structure: `checks/lint.json`. Ten pages, all pass with no errors and no warnings, after four label bullets were written out in full.
- Quotes: `checks/quotes.json`. Every quote in Sources was looked for in its own file, issue or memory copy, and every quote in the page text in the sources its page lists: 365 found, 0 not found. Twelve quoted phrases inside examples and scenarios are an example person's own words (for example a comment typed on a send-back), not quotes of a source; they are listed apart.
- ICE shape: `checks/ice-shape.json`. Ten ICE pages: each opens with the thin line, has Intent, Context and Expectation in order, exactly one Goal, three Limits and three Fails if, the fixed Read line, Never read, Persona and Scope, a Scenario, and a Done means checked by someone other than the doer; no part's own page holds an ICE section.
- Goal against Limits: `checks/goal-limits.json`, each read by hand.
