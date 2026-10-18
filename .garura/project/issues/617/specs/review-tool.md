---
plan_for: 617
kind: tool-plan
serves: "#617 — the intent review tool and the product review tool (ADR 032, Q7)"
status: draft
updated: 2026-10-18
---

# Tool plan — the outcome review tool

This plan says what the review tool is, how it talks to Garura, what the person
sees and does, and in what order it gets built. It is written from Kapil's brief
of 17 October (quoted below), ADR 032, Q7 in `decisions.md`, and the two
prototypes that came before it.

A mockup sits beside this file: `review-tool-mockup.html`. Open it in Safari.

## What Kapil asked for

Kapil, 2026-10-17:

> "eventually, all of these tools are going to move into Griffin. The way I want
> you to build the tool is that it is easily extractable and movable out of
> Garura."
>
> "they should be running on a server. Garura should have access to that tool on
> a server URL ... It can call that server with a specific request intent ... and
> then the tool operates."
>
> Show: "the full model, the full set of intents, the final version, the changes
> to the version. The user can swap between the two."
>
> Allow: "giving comments, doing edits, deleting something, selecting a part of
> the screen and leaving a comment."
>
> "Every time a change is made, it should have a direct connection back to
> Garura for listening."
>
> "The user interface ... needs to be very classy and simple. We don't want it to
> be a massive PR and add complex cognition load on the user."

Design: the layout of his 15 October screenshot (white page, quiet left rail,
big plain headline, one row of numbers, a "needs you" list). Colours from the
Phoenix design system (the Phoenix design system notes).
Phoenix logo, not a company one.

## The idea in one paragraph

The review tool is a small web server that knows nothing about Garura. Garura
sends it a **review pack**: a bundle of pieces (intents, capabilities, limits,
decisions), each with its words before and after the drive. The tool shows the
pack to a person in a calm page. Every time the person does something — a
comment, an edit, an accept — the tool records it as a numbered **event**.
Garura listens to those events and writes them as files on the drive's branch.
When the person presses **Finish**, Garura applies the answers. Moving the tool
to Griffin means moving one folder and changing one address in Garura's config.

## 1. Extractable — the rules that keep it movable

The line between the tool and Garura is the **contract**: a written, versioned
description of the review pack, the requests and the events. Everything else
follows from keeping that line clean.

1. **One folder, no ties.** The tool lives in `core/tools/outcome-review/`. It
   has its own README, its own tests and its own version number. It imports no
   Garura code and reads no Garura path.
2. **Garura words are data, not code.** "Intent", "capability", "limit" and
   "decision" arrive inside the pack as kinds with a label and an icon. The tool
   code never names them. A product other than Garura could send its own kinds.
3. **Talk only through the contract.** The contract is a JSON schema file in the
   tool's folder (`contract/v1.json`). Garura keeps a test that checks the packs
   it builds against that schema, so a break shows up on the Garura side first.
4. **Storage behind one small door.** The tool stores reviews through one store
   interface: save a pack, add an event, read events from a number. Today that
   is files on disk. In Griffin it can be a database. Nothing else changes.
5. **Settings from the outside.** Port, data folder, public address and access
   token come from environment variables. Nothing is hard-coded. The default
   port is 4390 (free today; 4321, 4380 and 4381 are taken).
6. **Everything bundled.** Fonts, scripts and the logo ship inside the folder.
   No CDN. It works offline on a laptop and the same way on a hosted server.
7. **A boundary check.** A test in Garura's lint fails if any file in the tool's
   folder mentions `.garura`, `core/components` or imports from outside its
   folder.
8. **The move.** Copy the folder into Griffin. Run it there. Change
   `review.server_url` in Garura's `config.yaml`. Nothing else.

**Stack:** Python standard library for the server (no installs, as the two
prototypes proved). Plain HTML, CSS and JavaScript for the page, no build step
(as #569 asked). Two small libraries copied in: one for word-level differences,
one to clean any HTML before it is shown.

## 2. How Garura and the tool talk

```
 Garura (on the laptop, on the drive's branch)          Review tool (server)
 ──────────────────────────────────────────────         ─────────────────────
 build the pack ── POST /v1/reviews ───────────────────▶ store pack, give a link
 open the link in Safari                                 person reviews
 start the listener ◀── GET /v1/reviews/{id}/events ──── each action = one event
   writes each event to review_dir                       (numbered, replayable)
 send-back fixed ─── PUT /v1/reviews/{id}/pack ────────▶ new revision shown,
                 ─── POST /v1/reviews/{id}/replies ────▶ "fixed" note on comment
 person presses Finish ◀── event: finished ──────────── page shows "Sent to Garura"
 apply answers, commit, land the change
```

**The requests (version 1):**

| Request | What it does |
|---|---|
| `GET /v1/health` | Is the tool up? Which contract version? |
| `POST /v1/reviews` | Start a review from a pack. Returns the review id and the link to open. |
| `GET /v1/reviews/{id}` | The pack, its revision, and the person's answers so far. |
| `GET /v1/reviews/{id}/events?since=N` | A live stream of events after number N. |
| `PUT /v1/reviews/{id}/pack` | A new revision of the pack, after Garura fixed a send-back. |
| `POST /v1/reviews/{id}/replies` | Garura answers a comment ("changed as asked", "could not, because …"). |
| `POST /v1/reviews/{id}/close` | Garura closes the review once the change has landed. |

The page itself uses its own requests to record actions. Those are inside the
tool and are not part of the contract.

**The listener.** Kapil asked that every change goes straight back to Garura.
Garura's listener is a small script, `review_listen.py`, that Claude runs under
the Monitor tool as soon as the review link opens. It connects to the event
stream and, for each event, does two things: it appends the event to
`review_dir/events.jsonl`, and it rewrites `review_dir/answers.json` (the
person's answers so far). It prints one line per event, so Claude sees each
action as it happens. Claude still never reads the web page: the answers are
files on the branch, as Q7 says.

What Claude does with live events:

- **send back** — Claude may start fixing that piece at once, while the person
  keeps reviewing. The fix comes back to the page as a new revision.
- **comment, edit, accept, drop** — recorded; acted on at Finish.
- **finished** — Claude runs the review step (story 7) and applies everything.

**Why the listener connects to the tool, not the other way round.** If the tool
had to call Garura, Garura would have to run its own server, and a hosted tool in
Griffin could not reach a laptop. With the listener connecting out, the same
design works on a laptop and in Griffin. This is open decision D1 below.

**Events never get lost.** Every event has a number and is kept in a log. If the
listener drops (Monitor stops after 30 minutes, the laptop sleeps), it reconnects
with the last number it saw and gets everything it missed. The two prototypes
already proved this.

## 3. The review pack — what Garura sends

The pack is outcome-shaped, not file-shaped. The tool never sees a file path.

```
review pack
├── review: id, title ("Kickoff — Shop checkout"), drive, branch, base,
│           started, revision, checker note, stopped-because (failed drive only)
├── kinds: intent, domain, capability, functionality, limit, decision
│          (label, plural, icon, which tool shows it, which verbs it allows)
├── pieces[] — one per intent, domain, capability, functionality, limit, decision
│   ├── id, kind, title, one line
│   ├── change: added | changed | removed | same
│   ├── status: e.g. proposed / confirmed (shown, never edited by the tool)
│   ├── sections[] — labelled parts in reading order
│   │     label ("Outcome", "Why", "Proof it is met", "Goal", "Limit" …),
│   │     before (text or empty), after (text or empty), editable yes/no
│   ├── links[] — to other pieces (an intent's Touches; a capability's intents)
│   ├── parent — where it sits (capability → domain)
│   └── why changed — one plain sentence from the play record behind it
└── stats: counts per change and per kind (the tool can also work them out)
```

Garura builds the pack with `build_review_pack.py` (the "what did the drive
change" script, story 3 in `decisions.md`). It compares the branch with main and
reads the pages and the spine by meaning. The play records only feed the "why
changed" line; the plays are never shown.

## 4. What the person sees

**One page, five sections in it.** A switch at the top left: **Intents** |
**Product** | **ADRs** | **Memory** | **Agent decisions**. Intents and Product
are the two tools ADR 032 names, as two views of one app; ADR 036 added a third
section, "Memory and ADRs", which Kapil split into three on 18 Oct (item 7
below). One server, one link, one review. (Occam: two servers would mean two listeners and two links for
one decision.)

**Two switches, each with two settings.** These answer Kapil's four things to see:

| | **Final** (how it reads now) | **Changes** (what moved) |
|---|---|---|
| **Everything** | the full set of intents, or the full product model, clean | the full set, with changes marked in place |
| **Only changed** | only what this drive touched, clean | only what this drive touched, with changes marked (the default) |

The default is "Only changed" + "Changes", because that is the review. One click
gives the full model or the clean final text.

**Layout** (like the screenshot):

1. **Left rail.** Phoenix mark and name. The Intents | Product | ADRs | Memory | Agent decisions
   switch. The list of
   pieces: intents grouped by stage, each with its agent intents (ICE) listed
   under it as their own pieces, one per capability or functionality it is built
   into; the product as domain → capability → functionality, then Limits, then
   Decisions. An ICE is answered in Intents; the product page shows the same
   lines read-only, with a link to answer them there, so nothing is answered
   twice. Each piece has a small dot: green
   added, amber changed, red removed, none for same. A tick once the person has
   answered it.
2. **Top bar.** The review title, the Final | Changes switch, the Everything |
   Only changed switch, and the **Finish review** button.
3. **Overview** (the landing page). A big plain headline: "Kickoff changed 3
   intents and 14 parts of the product." One row of numbers: Added, Changed,
   Removed, Answered, Waiting for you. One progress bar. A "Needs you" list: the
   pieces still without an answer, most important first (intents first, then
   box-moves, then the rest). The checker's note in one quiet line.
4. **A piece.** The title, its kind and change chips, the one-line why. The
   sections in reading order, as normal text. In **Changes**, removed words are
   struck through in red and added words are underlined in green, inside the
   sentence. Links to other pieces appear as small chips ("Touches: Checkout ·
   Guest checkout") that jump to the other tool.
5. **Right column, on a piece.** The decision buttons — **Accept**, **Send back**,
   **Drop** — and the comment thread for this piece, with Garura's replies.

6. **Catch up** — the main way to work through a big review (Kapil, 18 Oct,
   after Teams mobile "Catch up"). A drive can leave 18 changes, and later many
   more, so the person goes through them one card at a time:
   - one change per card: what it is, why it changed, and only the parts that
     changed (the rest is one line: "4 more parts did not change · See the full
     page");
   - **swipe right / →** accept; **swipe left / ←** leave for later (it stays
     unread). **Send back** and **Drop** are buttons, because they take a
     comment: send back needs one, drop asks for one. **Comment** (`c`) adds a
     comment and stays on the card;
   - **Undo** for a few seconds after each action (`z`);
   - order: each business intent, then its agent intents, then the product
     parts it touches; then limits and decisions — so each card has the one
     before it as context;
   - a bar of segments shows where you are and how each card was answered;
   - at the end: the cards left for later ("Go through them now"), then "All
     caught up" with the counts and **Finish review**;
   - works on a phone: the card fills the screen, the four buttons stack 2 × 2.
   Teams does the same with chat messages: a card per message, swipe right
   "Mark as read", swipe left "Keep unread", buttons to act without opening the
   chat (Microsoft message MC1260707, rolled out April–June 2026).
   Every action in Catch up is the same event as in the full page, so Garura
   cannot tell them apart and nothing changes on its side.

7. **ADRs, Memory and Agent decisions** (Kapil, 18 Oct: "intents · product ·
   adr(s) -> these are the adrs that a human puts, using /adr · memory -> this is
   list of memories that exist.. omstly garura memory inside the projecdt, and
   once an issue is selected then its STM ... then the agent adrs - we call this
   evidence, aka agent-decisions"; named **Agent decisions**, because "evidence"
   already names each play's run records). The three sections:
   - **ADRs** — the decisions a person records with `/adr`: the ones waiting to
     be accepted, and the accepted ones. Accept, or send back with a comment.
   - **Memory** — what memory holds: Garura memory for the project, and an
     issue's short-term memory once an issue is picked. **Ask memory**: a
     plain-words question box; the answer comes with the memory it came from.
     Underneath is the same memory tool the agents use — find, search and read,
     the way Claude Code works — with no index (vectorless, ADR 035 §4). Kapil:
     "the tool withing garua is how claude code works. the tool we are building
     which will got into griffin will use nlp, but it will use vectorless search.
     the same tool under both, just that the interface for tool should be nlp."
     Mocked only for now ("design the interface and create some mocks for now.
     no need to build this whole this now"). The memory updates waiting for a
     person live here too, below.
   - **Agent decisions** — every decision an agent made, with its trace
     (#659): the steps the agent took, in order. Kapil, 19 Oct: one or two
     lines "leave no context"; a decision rests on several things — "a project
     profile, domain, its security level and then the file where knowledge is
     put... this sort of thinking is critical to show.. these are called
     traces". So each step shows what the agent looked for, what it found, and
     its source — the tier, file and lines, in their place: the lines around
     them, numbered, with the lines the agent used marked. Each step's source
     is checked again: unchanged, changed (with what the lines say now, in
     their place), gone, or no source. The page shows the memory tool's own
     answers, in the contract's shape: `citations --check` and `updates` (for
     a decision that came from a memory update: what was missing, who approved
     it, and their words). Grouped by play, problems first. Looks right, or send back so the agent decides again
     from memory as it is now. The mockup's records are real tool output over
     real Phoenix memory lines, made by `.garura/project/issues/659/evidence/
     make_decisions.py`; the local page reads them live.
   The paragraphs below were written for the one combined section; they now
   read across these three.

   Earlier text, kept: a third section next to Intents and Product (ADR 036
   §7, Kapil 18 Oct). It shows short-term, Garura and Phoenix memory: what each
   tier holds, the memory updates waiting for a person, the ADRs waiting for a
   person, and which memory each decision came from. Every memory review and
   ADR review happens here, with the Catch up cards above. Built in #664.

   **Memory updates** (Kapil, 18 Oct, #658: "use the tool we built for product
   and intent... that now shows memory's created in STM, and each needs an
   explicit approval from a human"). Every memory update lands in an issue's
   short-term memory ("STM - always STM"). The section lists each update
   waiting for a person, one card each: the issue, what was missing, the drafted
   entry, where the draft came from (the person, the web, the model, or memory —
   marked), the sources, and whether it blocks the work. Each one needs its own
   explicit answer from a person: **Approve** or **Reject**, with the person's
   words. Nothing is approved in bulk, and an agent never answers one: the
   tool records the person's answer as an event, and only then does Garura
   apply the update to the issue's short-term memory. Moving memory up is not
   done here: `/learn-memory` (short-term to Garura memory) and
   `/promote-memory` (Garura to Phoenix memory, approved outside Garura) are
   their own plays — planned, not filed yet. The mockup shows these sections
   (the ADRs, Memory and Agent decisions switches).

**Keeping the load low** — the rules the page follows:

- One question per piece: "What do you want to do with this?"
- No file paths, no field names, no YAML. Labels in plain words.
- Pieces that did not change are hidden unless the person asks for Everything.
- Long sections are folded after a few lines, with "Show all".
- Counts and progress are always in view, so the person knows how much is left.
- One accent colour for action (Phoenix cyan). Magenta only for the few numbers
  that matter. Change colours (green, amber, red) only on changes.
- Keyboard: `j` / `k` next and previous piece, `a` accept, `s` send back, `c`
  comment, `f` switch Final / Changes.
- Nothing is lost if the page closes. Every action is saved the moment it happens.

## 5. What the person can do

| Action | How | What it becomes |
|---|---|---|
| **Comment** | select any words → "Comment"; or the comment box on a piece | a comment pinned to those words (by the words, not by a line number, so it survives a new revision) |
| **Comment on an area** | the "Point" tool (`p`): drag a box over any part of the screen → "Comment" | a comment pinned to that piece, section and box, for things words cannot point at (a group of chips, a diagram) |
| **Edit** | select words → "Edit", or the pencil on a section | the person's new words for that section; shown as their change |
| **Delete a part** | select words → "Remove", or the bin on a section | that part marked for removal |
| **Drop a piece** | the **Drop** button | the whole intent, capability or decision taken out |
| **Accept** | the **Accept** button | the piece becomes real at Finish |
| **Send back** | the **Send back** button, with a comment | Garura re-runs the play that writes that kind, for that one piece; it comes back as a new revision |
| **Finish** | the **Finish review** button, once every changed piece has an answer | Garura applies all answers |
| **Approve a memory update** | the **Approve** button on one update, with the person's words | the update is approved; Garura writes it to its issue's short-term memory |
| **Reject a memory update** | the **Reject** button on one update, with the person's words | nothing is written; the work that waits on it stays stopped |

**Comment states.** Each comment is open, answered (Garura replied) or resolved
(the person ticked it). Resolving no longer means deleting, which was a gap in
both prototypes.

**Edits and ADR 032.** ADR 032 allows accept, drop and send back. A direct edit
by the person is new. It fits the ADR's spirit — the person owns the outcome —
but it changes what the review step must do: apply the person's words, then
check them against the ontology's rules. If an edit breaks a rule (for example,
an intent with no proof), Garura replies on that piece and it stays open. This
needs a short amendment to ADR 032, through `/adr`. See D2 below.

### Approval is part of the product model

Kapil, 2026-10-18: "for any of the commands later on, as you set and change a
business intent, an [ICE], or the product model, this tool needs to keep good
track of what is approved and what needs to be changed." And then: "that whole
review and approval thing is part of the product model itself. It's not outside
of it. Every time somebody opens up this tool, they should be able to see what
is changed, what is approved, and what is in progress. It's just critical
because agents can only work on things which are approved. Agents cannot work
on things which are non-approved. Commands can impact it, but that lifecycle is
very critical to the governance of the product model and what is being built."

So approval is not a side record kept by the tool or by the review step. It is
part of the product model, on every piece, and the ontology governs it:

- **Every piece carries its approval state.** Business intents, ICE, domains,
  capabilities, functionalities, the product limits and decisions. Three states
  the person sees:
  - **Approved** — a person accepted these exact words. The piece keeps a
    fingerprint of its words (a short code worked out from the text), who
    approved it, when, and in which review.
  - **Changed** — new, or its words no longer match the fingerprint it was
    approved with. It waits for a person.
  - **In progress** — a person sent it back, and it is being reworked. The
    comments stay open until the new version comes back and is answered.
  - A dropped piece leaves the model; its drop is kept in git and in the review.
- **Agents work only on approved pieces.** This is the governance rule. A play
  may still write anything — a command can change an approved piece — but the
  write moves that piece to **changed**, and no agent builds from it until a
  person approves it again. This widens today's ontology rule ("work starts only
  from an ICE built from a confirmed business intent", `ontology.md`) from
  business intents to every piece, and keeps its principle: a rule stops work,
  never a write.
- **Links carry approval.** An ICE built from a business intent that is not
  approved is not approved either. A functionality inside a capability that is
  not approved waits with it.
- **It lines up with the states that exist.** An approved business intent is
  `confirmed`; an approved decision is `accepted`; an approved capability or
  functionality is `active`. The ontology names one lifecycle that these map
  onto, so a page and its approval state never disagree.
- **The tool shows it every time it opens**, not only at the end of a drive.
  The overview counts the whole model: approved, changed, in progress. Each
  piece shows its state, for example "Approved 17 Oct by Kapil", "Changed since
  approved", "In progress — 2 open comments". "Only changed" means "everything
  not approved". A drive's review is the same view, narrowed to what that drive
  changed.
- **Who writes it.** Plays write the model; writing changes the piece's state
  to changed, by the fingerprint, with no play having to remember. Only the
  review step writes "approved" or "in progress", from a person's answers. The
  tool writes nothing to the model; it shows what the pack says, so moving it to
  Griffin changes nothing.
- **This needs the ontology and an ADR.** The lifecycle and the rule are
  added to the ontology (#597) as part of every kind, and recorded in an ADR
  that amends ADR 032 and the ontology rule above.

## 6. The look

From the screenshot: white page, very light grey rail, thin hairlines instead of
boxes, big headings, small grey labels, lots of air, numbers large and plain.

From Phoenix (`phoenix.css`):

**Light only.** No dark mode (Kapil, 18 Oct: the light page reads far better;
the Phoenix dark colours made it hard). The Phoenix colours are used as accents
on a white page:

| Use | Colour |
|---|---|
| page | `#FFFFFF` |
| rail | `#F6F7FA` |
| card / raised | `#F1F3F7` |
| main text | `#0A0E1A` (Phoenix bg, used as ink) |
| quiet text | `#5B6478` |
| action, active, links | `#0891B2` (Phoenix pressed cyan, readable on white) |
| key numbers, the BInt tag | `#DB2777` (Phoenix magenta, one step deeper for white) |
| the ICE tag | `#7C3AED` (Phoenix lavender, deeper) |
| signature | cyan → magenta line under the headline and on the progress bar |

Fonts: Space Grotesk for headings and numbers, Nunito for text (the Phoenix
pair), bundled in the folder.

**Logo.** No Phoenix logo file exists on this machine (searched `~/cto`). The
mockup uses a stand-in mark: a simple rising-flame shape in the cyan → magenta
gradient, with the word "Phoenix". Swap in the real logo when there is one — it
is one file in the tool's folder.

## 7. Build order

Each line is one story. Each is a slice that works on its own.

1. **The contract.** Write `contract/v1.json`: the pack, the requests, the
   events. Two example packs: a small Kickoff, and a failed drive. Done when
   both examples pass the schema check.
2. **The server.** Health, start a review, read it, the event stream with replay,
   new revision, replies, close. File store behind the store door. Settings from
   environment variables. The boundary check. Done when the server's tests pass
   with the example packs and nothing in the folder names Garura.
3. **Reading.** The page: overview, Intents and Product views, Final | Changes,
   Everything | Only changed, links between the two tools, the BInt and ICE
   tags, light only. Done when the example pack reads well at full width and on
   a phone.
4. **Acting.** Comment on words, comment on an area, edit, remove, drop, accept,
   send back, comment states, Finish — in the full page and in Catch up (cards,
   swipe, later pile, undo). Every action saved as an event. Done when each
   action, from either place, shows up as the same event in the stream.
5. **Garura's side — open and listen.** `build_review_pack.py` (what the drive
   changed, against main), `open_review.py` (check the server is up, send the
   pack, open Safari), `review_listen.py` (the listener; writes `events.jsonl`
   and `answers.json` into `review_dir`). Done when a real branch produces a pack
   the server accepts, and an action in the page lands as a file on the branch.
5a. **Approval in the product model.** The approval state on every kind, in the
   ontology and the model; a check that agents only take approved pieces; the
   pack builder reads the state; the review step writes it. Done when a piece
   approved in one review shows as "changed" after a play changes its words,
   stays "approved" when no play touches it, and an agent refuses to work from a
   piece that is not approved.
6. **The send-back loop.** Garura re-runs one piece, sends a new revision and
   replies on the comment. Comments stay pinned across revisions. Done when a
   send-back comes back to the page with Garura's reply.
7. **The review step.** Apply the answers as one commit (accept, drop, edit,
   remove), the failed-drive path, and the box-move drop. This is stories 4–6 in
   `decisions.md`, now fed by `answers.json`. Done when a Kickoff branch ends in
   one commit that matches what the person chose.
8. **Kickoff uses it.** #613 runs the review as its last step.

9. **ADRs, Memory and Agent decisions.** The three sections (#664), in two halves
   like the rest; Ask memory's plain-words interface is mocked only.
   The tool half: the section's page and cards — what each memory tier holds,
   the memory updates waiting in short-term memory with an explicit Approve or
   Reject on each, the ADRs waiting, and which memory each decision came from.
   The Garura half: the pack of what is waiting (from the memory tool's
   `updates` and the decision records), and applying each answer — Garura calls
   the memory tool's `decide` with the person's words and then `apply`, and the
   `/adr` accept for an ADR.

Stories 1–4 and the tool half of 9 touch only the tool. Stories 5–8 and the
Garura half of 9 touch only Garura. That split is the extraction line, tested
every day it is built.

**Where it is built, and what stands in until then** (Kapil, 18 Oct, #658: "we
will build the tool with all the sections inside garura - as part of 606 plan.
it remains a local prototype for now."). The tool, with all its sections, is
built inside Garura as part of the #606 plan. Until then, "we will use the local
tool itself": the local prototype in `core/tools/play-reviewer/` (never
committed) gains a memory-updates page that lists the updates waiting in
short-term memory and records each person's Approve or Reject through the
memory tool. #658 builds that page. It is not a design of its own (Kapil, 18 Oct: "ensure
that its part of same design. and not build solo"): it uses this tool's mockup — the same rail,
top bar, look and Catch up cards — opened on the Memory section, with Agent decisions live
too, and Intents, Product and ADRs shown but not yet built.

## 8. Risks

- **Starting the server in auto mode.** Auto mode stopped Claude from starting
  the pr-reviewer server (memory note). Here the server can run as a background
  service on the laptop (started once, by Kapil), so Claude only checks
  `/v1/health` and never starts it. In Griffin it is always on.
- **Large product models.** Griffin's model has about 60 files and an 821-line
  spine. The pack sends pieces, not files, and the page shows only changed
  pieces by default, so size stays small for the person.
- **Comments on words that later change.** Pinned by the words around them. If
  a revision removes those words, the comment stays on the piece, marked
  "the words it pointed at have changed".
- **Two people at once.** Not in version 1. Events are added one by one, never
  whole-record overwrites, so adding a second reviewer later is safe.
- **Access.** On a laptop it listens only on 127.0.0.1 with a token. Hosted in
  Griffin, Griffin's own login goes in front. The contract does not change.

## 9. Open decisions

**D1 — How events reach Garura.**
- A — Garura's listener connects to the tool and reads the event stream
  (recommended: no server in Garura, works on a laptop and hosted, already proven
  in both prototypes).
- B — the tool calls a Garura address on every event (needs Garura to run a
  server; a hosted tool cannot reach a laptop).

**D2 — The person's direct edits.**
- A — allow them, and amend ADR 032 through `/adr`: the review step applies the
  edit and checks it against the ontology (recommended: this is what Kapil asked
  for).
- B — keep ADR 032 as is: "Edit" in the page becomes a send-back carrying the new
  words, and the play writes them.

**Still open from Q7:** what #569 becomes. This plan replaces its per-play viewer;
its comment → fix → approve loop is section 5 and story 6. Recommended: close
#569 with a pointer to the new stories, when Kapil asks.

## 10. What we keep from the prototypes

From `core/tools/play-reviewer/` and `~/projects/prototypes/tools/pr-reviewer/`:

- kept: standard-library server, numbered event stream with replay, the
  listener under Monitor, comments pinned by words, safe file writes, the light
  and dark tokens, select-and-act menus;
- dropped: loading content once at start, whole-record overwrites, deleting a
  comment to resolve it, hard-coded ports and browser, CDN libraries, the
  file-by-file view.
