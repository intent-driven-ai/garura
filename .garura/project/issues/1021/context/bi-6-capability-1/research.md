# Connect to what happens in use and in the market: research and drafts (issue 1021, BI-6 capability 1)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-6-capability-1/drafts/product-os/software-delivery-planning/connect-use-and-market/`: the capability page and its ICE page, and four feature pages, each with its ICE page. All five ICE pages carry the thin mark, because no part of this capability is built. They sit under software delivery planning because that is the lean on the domain (open point 1); the domain is not decided.

In one line: nothing in Garura connects to a product's web analytics, product analytics, user feedback or forums, and nothing reads one. Three built parts read an outside system, and each gives a pattern this capability can reuse: the tracker connector (the settings name the tracker, only a tool knows how to reach it, and the code host's own command line holds the access), the capture of a prototype (what a person shares is kept as a Source, exactly as it was when read, and a walk never changes data on a deployed site the person has not cleared), and web research (it drafts a page for memory only as a memory update a person approves). The one learning play, /learn-outcomes, is stale and read only Garura's own records. Phoenix memory has a shelf on building analytics into a product and nothing on reading a product's analytics, feedback or forums. A listener outside Garura (Griffin, which "Listens — to the product, to signals, to quality — and reports.") is a design note.

What this run did besides reading:
- It copied the memory files it decided from into `bi-6-capability-1/memory/`, with `manifest.json`, all from Phoenix memory: the ten domain shelves, the product profile schema, the ontology, the review's rule table (`standards/rules/pr.md`), the checkpoint setting rule (`gate-config.md`) and the learning on environments, migrations and keys (`run-environments-canary-migrations.md`).
- It searched every tier through the memory tool for analytics, feedback, user feedback, forum, Reddit, competition, market research, survey, review analysis, signal, telemetry, listen, connector, credential, API key, personal data, PII and privacy.
- It ran the placement skill (find-work-placement) over the ten domain shelves. The result is unmatched (`bi-6-capability-1/placement/routing-result.json`); open point 1 uses it.
- It read the model's approved pages it needed: the domain page, Keep the spec matched to what's built, Specify the product, Deployment design, Environment setup with its update feature, Deployment design's update feature, Initialize with its re-run feature, Manage surfaces, Fix defects test first, Test security (the example of the page shape), the intent pages of BI-6, BI-9 and BI-10 and Garura's own product profile in the spine.
- It read the repo: `core/config.yaml`; the tracker connector (`core/components/skills/platform-adapter/`, `core/components/skills/track-plan-changes/scripts/tracker.py`); the prototype capture and walk (`core/components/plays/discover-intent/`, `core/components/skills/walk-prototype/`); the research skills (`author-knowledge-page`, `propose-kb-node`, `research-domain-context`) and the agent knowledge-builder; the memory tool (`core/tools/memory/README.md`, `GUIDE.md`, `updates.py`); the stale `learn-outcomes` and `shape-marketing-lens`; ADRs 027, 035, 038 and 065; the design notes `docs/philosophy/intent-and-adlc.md` and `docs/design/playbook-catalog.md`; `.garura/user-provided/managing-work.md`; the agreed names; and the stock-take `bi-6-inventory/inventory.md`.
- It read GitHub, read only: the open issues found by searching for analytics, feedback, market, competition, Reddit, forum, telemetry, usage, signal, listener, Griffin, connector, integration, MCP and outcome; it read #545, #539, #544 (closed as not planned), #611 and the intents tracker's BI-6 issue with its two sub-issues. No open issue is about connecting to analytics, feedback or forums.
- It did no web research, so no memory update is raised.
- The decisions made from memory are in `cite-request.json`, for the caller to record with `memory.py cite` (the tool writes outside this run's folder).
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## The name

Kept: "Connect to what happens in use and in the market". Folder: `connect-use-and-market`.
- It is the name on the list the product owner set on 2026-11-10, and "connect" is his own verb ("connect to tools that access web analytics, product analytics, user feedback, and forums like Reddit").
- The words "in use and in the market" draw both lines: the inside of the work is Keep the spec matched's, and understanding is the next capability's.
- Shorter names weighed and not taken: *Listen to use and the market* (it would read as the listener outside Garura, which open point 2 leaves open); *Take in signals from use and the market* ("signal" is the design note's word, marked "designed, not in force", and not a plain word).

Words the pages use, and why:
- **Connection**: one outside tool or forum the project reads. The word "source" was avoided, because a Source in the product model is what a business intent was drawn from, and every page has a Sources section.
- **What is taken in**: each figure, message or post a connection holds, kept as the tool gave it.
- Web analytics, product analytics, user feedback and forum are explained on the capability page, the first two with Phoenix memory's own line ("Web analytics — the existing page-load/CTA layer", "Product analytics — feature usage, adoption, retention, cohorts, paths.").

## What is built, and what is only planned

Built and live, reading an outside system, none of it for this capability:
- **The tracker connector.** The settings name each tracker: "Which tracker holds what. Tools read this; plays, skills and sub-agents never name a tracker." (`core/config.yaml` line 14). ADR 065, section 4 (accepted): "Tools read the settings and know how to reach the tracker. Plays, skills and sub-agents know only the tool, never the tracker." BI-10's confirmed must-not: "Name a tracker in a play, skill or sub-agent, because they only know the tool." The adapter "Resolves the active platform from config and dispatches to the correct CLI (gh for GitHub, glab for GitLab)." (`platform-adapter/SKILL.md` line 3); `core/config.yaml` holds no key, so the access sits with the code host's own command line. It reads and writes issues; its writes wait for a person's yes in the plays that use it. Relevance: the pattern for naming a connection in the settings and keeping the tool's name out of plays, skills and sub-agents.
- **The capture and walk of a prototype** (/discover-intent with walk-prototype and the prototype-reader agent, installed here). It "Keeps what they shared as Sources, exactly as they were when read" (`discover-intent/SKILL.md` line 4); a Source is kept as a snapshot "with when it was read, what it shows in plain words, and who gave it" (`reference/ice.md` C6); a walk "Never changes data on a deployed site the person has not cleared." (`walk-prototype/SKILL.md` line 3). Specify the product's approved page: a capture writes one record with "the kind of Source, the date it was read, who gave it" and "a fingerprint of each saved file", because "the Source must outlive the link or the file"; and "a model drawn from a source nobody read has no basis." Relevance: the pattern for keeping what is taken in as given, with where and when, and for reading without writing.
- **Web research through memory updates.** author-knowledge-page and propose-kb-node read the web (their allowed tools include `WebSearch` and `WebFetch`) and draft pages "researched with its sources"; the agent raises each with the memory tool's `propose` and `draft_source: web`, and "Nothing in it is used until a person approves it." (`core/tools/memory/README.md`). The knowledge-builder agent that runs this is in the full install only. research-domain-context also reads the web, for the tech-designer agent. Relevance: Garura reads public web pages today only to draft memory, never to read what people say about a product.

Built but stale or dropped:
- **/learn-outcomes**, stale ("waits for the rebuild of the learn loop on the current product model (#855)"). It read a delivered unit's own records: the measures design, the validation verdicts, the run design ("what production actually needed versus what was planned") and the epic's status. It never read an outside tool, and every input it read is gone or stale (inventory, section 2). Its name stays under the Specifier role (`names.md` line 6).
- **/shape-marketing-lens**, stale and dropped (`names.md` line 10: "Dropped: /shape-marketing-lens, /shape-measure-lens."). It designed "the reach signals worth capturing" into one slice. It read none of them.

Planned only, or ideas on record:
- **The product owner's list, item 1** (2026-11-10), the only agreed source for this capability.
- **Griffin**, in the design note on intent and the agent lifecycle (`docs/philosophy/intent-and-adlc.md` line 144, marked "designed, not in force"): "Listens — to the product, to signals, to quality — and reports. It can also spawn its own agents to act on what it hears." Griffin is a Phoenix tool built beside Garura (`.garura/user-provided/managing-work.md`, "Phoenix tools and the Phoenix project").
- **Signals**, in the same note: "A signal is what we receive. It can be anything — a person saying something, a market moving, work landing, a measure reading." (lines 337-338); "Signals land on intents. Only on intents." (line 335); "Until the system is connected, those signals come from humans" (lines 401-402).
- **ADR 027** (accepted): Perception, the first part of the agentic tool's design, is "What enters the system, and how it is received and routed". This capability is the first piece of it for use and the market.
- **ADR 035 and ADR 038** (accepted): memory is reached through one tool so that "a move to Griffin changes only the tool" (ADR 038 line 53). The same shape would let the reads move to a listener outside Garura later.
- **#545** (open, filed under BI-6's tracker issue, "Not approved to build", parked): "Human-reported signals on a business intent accumulate over time as a history"; the product owner then: "we are not at the measurement and connected state yet". His 2026-11-10 list now asks to connect; #545's measuring stays parked and out of this capability.
- **#544** (closed as not planned, 2026-11-02): "Nothing raises a signal to whoever owns its resolution.", with "a standing watcher" among the candidates, and "Griffin is the harness whose job this most resembles". History only.
- **The playbook catalog** (`docs/design/playbook-catalog.md`, "Discovery draft. Not scoped, not implemented.", 2026-04-23): `triage-feedback`, "Ingest customer feedback (tickets, sentiment, analytics) → cluster into themes → auto-file via `capture` → link to existing capabilities." An idea, not an agreed plan; only its first step is this capability's, and its theming and filing are understanding.

What memory holds, and does not:
- **Phoenix memory's analytics shelf** (`knowledge/domains/analytics.md`) is about building analytics into a product: goals, funnels, product analytics over web analytics. Its lines on web and product analytics explain the words on the pages. Its consumer intent, "measure me without abusing my data", and its privacy-aware collection are memory's answers for building a product's analytics; the pages quote the first as a reason and write none of the shelf's building advice as a rule.
- **The experience shelf** keeps "Every node, edge, inference, and recommendation traces to evidence (URL, snippet, timestamp, extraction method, confidence). Signals are hypotheses, not facts" (lines 35-37), for products that model what visitors want. It points the same way as keeping each item as given, with where and when, and is not used as a rule.
- **The product profile schema** holds a privacy level and the "regimes the box admits"; "The box moves ONLY by an approved decision." Garura's own profile sets no privacy level and lists no regime (`_spine.yaml`, `compliance: []`).
- **The learning on environments and keys**: "Credentials and provider keys live only in secrets management, never in the repo or the config files." (`run-environments-canary-migrations.md` lines 65-66).
- **No tier holds**: which tools and forums a project can connect to and how each is reached; what may be kept from a feedback message or a forum post; how often to read and how far back; how a person's details are found and taken out; any learning on reading user feedback or forums.

## The open points, each with options and a lean

None of these is decided here. The drafts follow each lean and name the rest as not decided on the pages. The decided points are not reopened: this capability connects and takes in, and does not interpret or change the product or the model (items 2 and 3); reading the tools through their own tools is not touching production, and nothing writes to them or to the product; promoting learnings and measuring each intent are not on BI-6's list; Keep the spec matched keeps the inside of the work; no lens, no seeding memory, no design lock.

### 1. The domain

What holds: the model has one domain, software delivery planning, whose first paragraph says it "turns a business intent into working code that a check from the outside can prove" and ends "It does not release the work or run the product." (`domain.md` line 4). Reading tools that hold a product's use is not running it, but learning from use and the market is not in that paragraph either. At BI-4's close the same paragraph was changed so the domain also tests the work, instead of a second domain. The placement over Phoenix memory's ten domain shelves is unmatched for both the field Garura serves (software delivery) and the job this capability does (learning from a product's use and its market): each shelf is a field a product is built for, and the analytics shelf says how to build analytics into a product. BI-6's other two items, understanding consumers and competitors and building features or updating the model, would sit with this one; item 3 writes back into pages of software delivery planning.

1. **Keep this capability in software delivery planning, and change the domain's first paragraph at BI-6's close**, so the domain also takes back what happens in use and in the market and keeps the intents true to it; "It does not release the work or run the product" stays true. Gain: one domain, as every approved capability; the same move as BI-4's close; item 3 lands in the same domain's pages; no domain page to research now. Cost: the domain's name, "software delivery planning", stretches further; learning from the market is not delivery.
2. **A second domain for learning from a product's use and its market**, holding BI-6's three capabilities, with its own domain page later. Gain: each domain says plainly what it covers. Cost: a domain page researched with its sources, named as the field already names itself (the nothing-fits path, through a memory update a person approves), before this page can be linked; item 3 still writes into software delivery planning; the first split of the model's domains.
3. **Widen and rename the one domain at BI-6's close** to the whole loop from intent to working code and back. #539's title already says "Garura becomes true product engineering". Gain: one domain whose name fits all of it. Cost: renaming the domain changes every approved page that names it; bigger than this capability.

Lean: 1. The drafts sit under `software-delivery-planning/connect-use-and-market/`, and the capability page says the domain is not decided. If 2 is chosen, the pages move to a new domain folder (for example `learning-from-use-and-market/`) and their words do not change, except the sentence on why it matters to its domain.

### 2. Inside Garura, or a listener outside it, and how autonomous

What holds: the product owner on autonomy: "This needs to be built for high autonomy." and, on CI and CD, "an autonomous kind of agent running that goes back and does this thing for me. I almost feel like that part of CI/CD needs to sit outside of Khoros." ("Khoros" read as Garura). Griffin "Listens — to the product, to signals, to quality — and reports." and is planned beside Garura. Memory and the tracker are each reached through one tool that reads the settings, so that "a move to Griffin changes only the tool". BI-6's must-not names a person only for changing an intent and promoting memory; the pinned learn checkpoint is for "a wrong model learning" that "bends the product model" (`gate-config.md` lines 98-101).

1. **Garura connects itself**: a tool inside Garura reads every connection on a schedule. Gain: works with nothing else built. Cost: the keys and the reading of outside accounts sit inside the project that agents build in.
2. **A listener outside Garura reads every connection, holds the keys, and reports in**; Garura only takes in its reports. Gain: matches his feeling that the autonomous part sits outside, and keeps keys away from the project's agents. Cost: nothing reads until the listener is built; Garura cannot take in anything today.
3. **One tool, either way**: plays, skills and sub-agents call one Garura tool that reads the settings; today the tool reaches each connection itself; later it can read what a listener outside Garura reports, with no change to Garura's agents. In both cases the reads run on their own as the settings say; a person says yes only to each connection and each change of one. Gain: the shape of two accepted ADRs and BI-10's must-not; works now and moves later. Cost: the tool's two ways in must keep the same rules.

Lean: 3. The drafts follow it: the guiding rule Only the tool knows the connection, reads that run on their own, and a "Not decided" line on whether the reads are made by Garura's tool or by a listener outside Garura.

### 3. Keys and access

What holds: approved Deployment design: "The design names only where each secret is kept.", because every agent reads it, "so a secret written there is no longer secret."; it designs "where secrets, such as passwords and keys, are kept". The tracker's access sits with the code host's own command line, and the settings hold no key. Memory's learning keeps keys "only in secrets management".

The rule is settled by the approved pages: the settings name each connection and where its key is kept, never the key; a read takes the key where it is kept at the moment of reading and never writes it down. Where the keys are kept is open:
1. **Where the deployment design keeps the project's secrets.** Gain: one place for every secret of the project. Cost: the deployment design is not built, and it designs the path of the product's environments, not the accounts the team reads.
2. **Each tool's own login**, as for the tracker, so Garura holds no key. Gain: matches what is built. Cost: an unattended read needs a login that lasts somewhere; not every tool may have one.
3. **The listener outside Garura holds every key** (with open point 2's option 2 or 3). Gain: no key near the project's agents. Cost: the listener is not built.

Lean: 1 now, and 3 when a listener exists. The drafts write only the settled rule and name where keys are kept as not decided. Also not decided: whether each key must be one that can read and cannot write (no source says what each tool allows).

### 4. People's data: what is kept and what never

What holds: feedback and forum posts can hold names and personal data. Approved Environment setup: "the review already treats real personal data in an environment other than production as a finding". The review's rule table flags words such as email, phone and personalData in a change (DATA-17, P2). The profile holds a privacy level and compliance regimes, and only an approved decision moves them. A Source "is kept as it was when read".

1. **Keep the words and figures, never who.** Each message or post is kept in its own words, and each figure as the tool gave it, with its connection, where it was and when it was read; a person's name, handle, contact details and anything else that points to one person are taken out, from the words too, before anything is kept; from analytics only figures about many people, never one person's record. The profile's privacy level and compliance needs are read. Gain: what the next capability needs, people's words and what they did, without personal data in files every agent reads. Cost: no one can follow up with the writer; how details are found in free words is not decided.
2. **As given, bounded only by the product's privacy level and compliance needs.** Gain: nothing lost for a product with no privacy concern. Cost: Garura's own profile sets no privacy level, so nothing would bound it; personal data would sit in project files.
3. **Keep nothing; read at the moment of understanding** and record only what was read and when. Gain: no data kept. Cost: the next capability has nothing fixed to cite, and two reads may differ.

Lean: 1. The drafts follow it. Never kept, in every option: a key's value; anything read from production other than through the team's own tools; anything from a place or topic the connection does not name. Not decided: how details are found and taken out of free words, and how that is checked; whether the profile's privacy level can ask for more, such as keeping no words at all.

### 5. Where, and as what, what is taken in is kept

What holds: a Source has a kind, the date read, a snapshot, what it shows and who gave it ("The git user who ran the reading play"); it lives with the product's evidence; "It is kept as it was when read; the snapshot never changes afterwards." Its kinds are prototype, document and statement; none is a read from a tool. Every memory write goes to an issue's short-term memory, and an agent never decides from another issue's short-term memory. The design note calls what is received a signal; #544, which would have built signals, was closed as not planned.

1. **Kept the way a Source is kept, with a new kind for a read from a connection**, through a change to the ontology (Define what a product is made of). Gain: reuses the built capture and its rule. Cost: a Source shows a business intent, and "Given by" is a person, not a tool.
2. **A kind of its own** in the ontology, through the same change. Gain: it says what it is. Cost: a new kind.
3. **In each read's issue folder in short-term memory.** Gain: no ontology change. Cost: a read that runs on its own has no issue, and the next capability could not decide from another issue's short-term memory.

Lean: 1 or 2, decided with the ontology, not here. The pages keep each item as given, with where and when, never changed afterwards, and name where and as what as not decided.

### 6. Who sets up the connections, and how they are updated

What holds: "Settings: Everything that can be turned on or off lives in settings."; trackers are named in the settings; Initialize, planned, asks set-up questions after the install and runs again "when the project changes: it gains a database, a web surface, personal data or a new tracker, or it drops one."; the approved update features keep it so that "what held before stays readable with why it changed".

1. **This capability's own feature**: when the product owner wants the project to learn from use, the connections are proposed from the project's code and memory, each with its source, and he says yes to each; a later feature updates them as the product and its tools change, keeping what held before. Gain: works without Initialize; a product with no users yet has nothing to connect at install. Cost: one more place that writes settings.
2. **Initialize asks for the connections** at set-up and on each re-run. Gain: one moment of set-up. Cost: Initialize is not built, serves no intent in the spine, and runs at install, often before there is any use to read.
3. **Each read asks** for what it needs. Cost: no lasting record; the same question each time.

Lean: 1. The drafts follow it with two features (first set-up and update), and name as not decided whether Initialize asks for connections and hands them over.

### 7. How far taking in goes: placing on intents

What holds: decided, this capability connects and takes in and does not interpret. The design note says signals "land on intents", and the inventory's proposed intake placed what was reported on the intents it bears on.

1. **Keep only what the tool itself says** (its page, event, feature name, thread or product named); placing on intents is understanding, the next capability's. Gain: keeps the decided boundary; placing is judgment. Cost: the next capability does the placing for every item.
2. **Take in and place on intents here.** Cost: judgment inside taking in, against the decided line.
3. **Take in and file each item as a work item or a defect.** Cost: filing is understanding and Orchestration's; Fix defects test first already takes in a defect reported anywhere.

Lean: 1. The drafts follow it.

### 8. The persona

What holds: the personas used so far are the product owner, the technical lead, the developer and the devops engineer (and the architect on Design the technology and architecture). BI-6 is asked by the product owner, and items 1 and 2 are his words. The devops engineer decides how the project runs and where its secrets are kept (Deployment design).

1. **The product owner**: chooses what the project reads, says yes to each connection and each change, hears when a connection keeps failing, and wants what consumers want understood from what happened. Gain: the same reader as BI-6's page; no new persona. Cost: the person who looks after each tool's account is not named.
2. **The product owner and the devops engineer**, who keeps each connection's key where the project keeps its secrets. Gain: keys with the person who decides where secrets are kept. Cost: Deployment design's secrets are for the product's environments, and where connection keys are kept is open (point 3).
3. **A new persona**, such as someone who looks after a product's analytics and feedback. Cost: no approved page or source uses one; the product owner's own words ask for this.

Lean: 1, no new persona. The drafts follow it.

### Smaller points, named as not decided on the pages

- Which tools and forums a project can connect to, and how each is reached (no tier holds it).
- Where a connection's key is kept, and whether each key must be one that cannot write (point 3).
- How often the reads run and how far back each reads.
- How a person's details are found and taken out of free words, and how that is checked (point 4).
- Where what is taken in is kept, and as what kind of record (point 5).
- Whether the reads are made by Garura's tool or by a listener outside Garura (point 2).
- Whether Initialize asks for the connections (point 6).
- How many failed reads make a connection one that keeps failing.

## The features found

1. **Choose the tools and forums a project reads, and connect to them** (fn-connect-tools). Not built. Proposes the connections from what the project already holds, records each approved one by name with where its key is kept, and proves it with a first read that changes nothing. Sources: his words ("connect to tools that access web analytics, product analytics, user feedback, and forums like Reddit"); the list's item 1; the Settings line; the tracker pattern (`core/config.yaml` line 14, ADR 065 section 4, BI-10's must-not); Deployment design's names-only rule; Initialize's rule that a write to an outside system "is visible to the whole team."
2. **Take in how the product is used, from its web analytics and product analytics** (fn-take-in-use). Not built. Reads each connected analytics tool and keeps each figure as the tool gave it, with the connection, the time it covers and when it was read, never one person's record. Sources: his words; the list's items 1 and 2 and the assumption on production; the analytics shelf's words; the Source rule; Environment setup's line on personal data; the stale /learn-outcomes and the dropped marketing design, as what it is not.
3. **Take in what people say about the product and its market, from feedback tools and forums** (fn-take-in-what-people-say). Not built. Reads each connected feedback tool and forum, only the places and topics named, and keeps each message or post in its own words with where and when, with every person's details taken out. Sources: his words ("user feedback, and forums like Reddit", "what the competition is doing"); the list; the Source rule; Environment setup's line on personal data; the web research skills, as what exists; the playbook catalog's `triage-feedback` idea, its first step only.
4. **Update the connections as the product and its tools change** (fn-update-connections). Not built. Proposes a new, changed or dropped connection when the product gains a surface, its code starts or stops using a tool, or a connection keeps failing, keeps what held before and why, with the product owner's yes. Sources: his standing rule that changing something later is worded as updating it as the project changes; the approved update features of Environment setup and Deployment design; Initialize's re-run; Manage surfaces; the Settings line.

Candidates not drafted, and why:
- **Take in what a person reports from use** (the inventory's proposed intake): item 1 names tools; a person's own words already reach Specify the product as a Source, and a defect reported anywhere reaches Fix defects test first.
- **Place what is taken in on the intents it bears on**: understanding, the next capability's (point 7).
- **Measure each intent** (#545): parked, and not on BI-6's list.
- **Read Garura's own run records** (session stamps, run evidence, decision traces): they are Garura's records, not a product's use or market, and the inventory places them with Orchestration and Memory.
- **A listener outside Garura**: a Phoenix tool beside Garura, not a Garura feature; it bears on how the reads run (point 2).
- **Research competitors on the web**: no source plans it; what people say about rivals in a connected forum is taken in by feature 3, and understanding what the competition is doing is the next capability's.

## Thin marks, and why

- The capability's ICE and all four feature ICE carry the thin mark, with at most three Limits and three Fails if each: no part of this capability is built.

## Lines elsewhere that are out of step (not changed here)

- The domain page's first paragraph does not cover learning from use and the market (point 1). Under the lean it changes at BI-6's close, in words the product owner approves.
- BI-6's page has no Touches list; this capability is added when it is written.
- BI-6's proof reads "Drift between the model and the work gets named." and "Each learning is promoted on purpose."; neither speaks of connecting to use and the market. The inventory's disagreement 1 already proposes rewording the first proof at BI-6's close.
- #545 records "we are not at the measurement and connected state yet"; his 2026-11-10 list asks to connect. #545 stays parked for measuring.
- The ontology's Source kind has no kind for a read from a tool, and its "Given by" is the git user (point 5).
- `core/config.yaml` has no block for connections; the Settings capability is not reviewed yet.

## Assumptions

- Assumed, recorded with the list: reading web analytics, product analytics, user feedback and forums through their own tools is not touching production.
- Assumed, from the decided boundary: nothing in this capability writes to any connected tool or forum, or to the product.
- Assumed: a key is a secret in the sense of the approved Deployment design, so its names-only rule applies.
- Assumed: B16 means BI-6, and Khoros means Garura, as recorded in `capabilities.md`.
- The examples come from several kinds of product: a shop's checkout, a clinic's booking app, a school's timetable app, a team's planning tool and a recipe app.

## Memory updates

None drafted. What no tier answers is named as not decided instead: which tools and forums a project can connect to and how each is reached, what may be kept from feedback and forum posts, how often to read, and how a person's details are found and taken out. This run did no web research, and drafting an answer from the agent's own knowledge would break the rule; a person may ask for the research, and its answer would go to a memory update for approval. The placement is unmatched; a domain page for a second domain would go through the nothing-fits path (propose-kb-node, research with sources, a memory update) only if the product owner chooses option 1.2.

## Checks

- **Structure check** (`lint_grounding.py`): the capability page (`--kind capability --stage directional`) and the four feature pages (`--kind feature`): ok, no errors, no warnings, on the first run and after every edit.
- **ICE shape and wording check** (a small script in the session's scratch folder): each of the five ICE pages holds Intent, Context and Expectation in that order, exactly one Goal, one to three Limits and one to three Fails if, the thin mark as its first line, the fixed Read line with what to look for, the Context labels in order (Read, Never read, Persona, Scope), a Scenario, and a Done means checked by someone other than the doer. No part page holds an ICE section, and each has its ICE page beside it. Outside quotes and the Sources, no page says lens, seed, lock or gate, names a real person, a home folder, a temp folder, a particular plan or a business intent's number; no file of this run holds a home or temp folder path or a real name.
- **Quotes** (the same script): all 257 quote checks on the ten pages pass, word for word (spaces joined; markdown marks and YAML's doubled apostrophes read as one): each quote in a Sources line is in a file that line names, and each quote in a page body or its ICE page is in a file that page's Sources name. Memory quotes are checked against this run's copies in `memory/`, the product owner's words against `page-approvals.md` and `capabilities.md`, the GitHub quotes against the issues' text read today.
- **Planted errors**: the script was run once on a copy with seven planted errors (a changed word in a quote, the right words in the wrong file, a made-up quote, a missing thin mark, a forbidden word, an ICE section on a part page, a Done means by the doer); it named all seven.
- **Quotes in this file**: all 83 are found word for word in the files read. The first run found eight that were not: five were this file's own phrases or weighed names put in quote marks, now written without them; one quoted the ontology with a small letter where it has a capital, now fixed; and two were not quotes at all. Seven quotes that joined pieces with three dots were rewritten as whole quotes.
- **Placement**: `routing-result.json` passes the skill's own check (`validate_route.py`: VALID).
- **Not decided lines**: each "Not decided" line on the pages was read against the decided points in the brief; none reopens one. They are the smaller points listed under the open points above.
