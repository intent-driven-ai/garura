# Understand what consumers want and what the competition is doing: research and drafts (issue 1021, BI-6 capability 2)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-6-capability-2/drafts/product-os/software-delivery-planning/understand-consumers-and-competition/`: the capability page and its ICE page, and five feature pages, each with its ICE page. All six ICE pages carry the thin mark, because no part of this capability is built. They sit under software delivery planning, with the first capability, for now; the domain is settled at BI-6's close.

In one line: nothing in Garura sorts, sums or places what a product's users and market say or do, and nothing understands a competitor; nothing is even taken in yet, because the first capability of Run → Product is not built. What exists gives patterns only: Specify the product groups the parts of what one person gives by the need each meets and maps every part (the coverage map); each agent decision keeps a trace of the lines it rests on, and a check names a decision whose source changed; the placement skill places work on memory's shelves; the plan session's placing script places a new feature on the model by fixed rules and asks a person what no rule settles; the stale /learn-outcomes cited the outcome behind every change and tiered each by confidence. One built skill researches a "competitive landscape" on the web, for the technical designer, and writes it straight into short-term memory. Phoenix memory holds nothing on drawing wants from feedback, posts and figures, or on following competitors.

What this run did besides reading:
- It copied the memory files it decided from into `bi-6-capability-2/memory/`, with `manifest.json`, all from Phoenix memory: the ten domain shelves, the ontology, the cardinal rule on recommendations (`no-unbacked-recommendation.md`), the checkpoint setting rule (`gate-config.md`), the old provenance rule (`features.md`), the old MVP recommendation schema (`mvp-recommendation.yaml`), and three learnings on agents (`agent-supervised-autonomous.md`, `agentic-guardrails-baseline.md`, `agent-derive-once-apply-many.md`).
- It searched Phoenix memory through the memory tool for competit, market research, voice of, sentiment, feedback, review, jobs to be done, cluster, theme, market, insight, confidence, signal, hypothes, injection and untrusted; and Garura memory for competit, consumer, rival and what people say. Garura memory answered only with the first capability's own pages.
- It ran the placement skill (find-work-placement) over the ten domain shelves. The result is unmatched (`bi-6-capability-2/placement/routing-result.json`, VALID by the skill's own check), as for the first capability. The domain is not reopened: the capability sits with the first one, under software delivery planning, until BI-6's close.
- It read the model's approved pages it needed: the first capability and its four features with their ICE, and its approval record; Keep the spec matched to what's built and Find where the spec and what's built no longer match; Specify the product and Specify against what exists; Fix defects test first; Test what the product does, with evals the builder never sees; Design the technology and architecture (the update wording); Environment setup's update feature; the domain page; BI-6's intent page.
- It read the repo: `core/components/skills/author-business-intent/SKILL.md`, `find-work-placement`, `research-domain-context`, `author-learnings`, `author-marketing-lens` (stale), `judge-grounding`; `core/components/plays/learn-outcomes/` (stale), `shape-slice/SKILL.md`, `update-plan/scripts/place_feature.py`; the agent tech-designer; `core/tools/memory/GUIDE.md` and `README.md`; ADRs 027, 028 and 037; the design notes `docs/philosophy/intent-and-adlc.md`, `docs/design/playbook-catalog.md` and `docs/design/briefs.md`; the glossary; the stock-take `bi-6-inventory/inventory.md`; and the git history of the deleted /specify play.
- It read GitHub, read only: open issues searched for competitor, competition, market research, market, consumer, customer needs, feedback, insight, user research, what users want, sentiment, review, theme, cluster, signal and voice of; it read #545 and #539 and the intents tracker's BI-6 issue. No open issue is about understanding consumers or competitors.
- It did no web research, so no memory update is raised.
- The decisions made from memory are in `cite-request.json`, for the caller to record with `memory.py cite` (the tool writes outside this run's folder).
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## The name

Kept: "Understand what consumers want and what the competition is doing". Folder: `understand-consumers-and-competition`.
- It is the name on the list the product owner set on 2026-11-10, close to his own words ("start understanding what it is that the consumers want and what the competition is doing"), and the first capability's approved page already hands its work on by this name.
- Shorter names weighed and not taken: *Understand consumers and competitors* (it drops "want" and "doing", the two words that say what is understood); *Learn what consumers want* ("learn" is the verb of the stale /learn-outcomes and of the planned Learn loop, which promote memory and change the model, neither of which this capability does).

Words the pages use, and why:
- **Consumers**: the people the product is for, those who use it and those who talk about it or its kind of product. His word, kept; explained on the capability page.
- **The competition** and **a competitor the project follows**: the other products people could choose instead; one is followed only with the product owner's yes.
- **Item**: one figure, message or post the first capability took in, as its approved page defines it.
- **Want**: a need or a problem that comes up across many items. **Finding**: one want, or one thing a competitor is doing, with its items, counts, how sure it is and where it is placed.
- The word "signal" is not used: the glossary's Signals are "User CLI invocations that enter the Garura system", while the design note uses the word for anything received.

## What is built, and what is only planned

Built and live, none of it for this capability:
- **Grouping by need, with every part mapped** (Specify the product, through author-business-intent in /discover-intent): "Group the parts by the need they meet", and "Every part is mapped to the intent it serves (the coverage map); never merge two needs, never leave a part out." It works on what one person gives, one source at a time, not on many consumers' items. Relevance: the pattern for sorting items into wants with every item accounted for.
- **A decision's trace and its check** (ADR 037, accepted; the memory tool's `cite` and `citations --check`): each decision keeps the steps it took, each with its source lines and a fingerprint; "`cite` refuses a source that is gone or changed. `citations --check` names every decision whose source no longer says what it said." Relevance: the pattern for a finding that names each item it rests on, and a check that the items still say it.
- **The placement skill** (find-work-placement): "Search the product knowledge base for where a piece of work belongs — its domain, capability, and feature"; an area no shelf lists is "never folded into a domain whose shelf does not list its work". It places on memory's shelves, not on the product's own model. Relevance: the pattern for naming a finding as fitting none instead of forcing it.
- **The plan session's placing script** (`update-plan/scripts/place_feature.py`): it will "place each new feature of a draft by fixed rules", and "The script makes no judgment": what no rule settles becomes a question for a person. Relevance: placing on the product's own model, by rules a person can check.
- **A judge with no context** (judge-grounding): an "isolated, clean-context judge sub-agent" that sees only the page and never "the author's reasoning". Relevance: a way for someone other than the doer to check a finding against its items.
- **Briefs that name their basis** (/shape-slice): "A proposed answer always names its source; where none exists the question carries no proposed answer, and the count is shown." Relevance: the pattern for the report to the product owner.
- **research-domain-context**, live in a full install only, used by the technical designer: "Search the web for market data, competitive landscape, industry trends, regulatory context" and "Write domain-context.md to the specified STM path". It writes its research straight into short-term memory, not as a memory update a person approves. It is not used for this capability, and it is out of step with the rule that research waits for a person.

Built but stale or deleted:
- **/learn-outcomes with author-learnings**, stale ("waits for the rebuild of the learn loop on the current product model (#855)"). It read Garura's own records of delivered work, never a product's users. Its patterns: "every proposed change cites the outcome that justifies it", and "Each proposed change carries the outcome that justifies it and a confidence tier.", with "high-confidence batched, low-confidence surfaced one by one".
- **The old /specify play**, deleted in the realignment to the ProductOS command model (#453). Its first stage was market research by a `market-analyst` agent, "market brief with TAM/SAM/SOM, competitive landscape", researched on the web once, before a product was built. History only; it is not a reading of a product's consumers.
- **/shape-marketing-lens with author-marketing-lens**, stale and dropped: it designed how one slice is found and reached, and read no consumer or competitor.

Planned only, or ideas on record:
- **The product owner's list, item 2** (2026-11-10), the only agreed source for this capability, and the first capability's approved Out line: "understanding what consumers want and what the competition is doing from what is taken in, which includes sorting it, summing it and placing it on the intents it bears on."
- **The playbook catalog's `triage-feedback`** ("Discovery draft. Not scoped, not implemented.", 2026-04-23): "Ingest customer feedback (tickets, sentiment, analytics) → cluster into themes → auto-file via `capture` → link to existing capabilities." Its themes and its links to capabilities are this capability's; auto-filing is not.
- **The design note on intent and the agent lifecycle** ("designed, not in force"): "Signals land on intents. Only on intents."; "A signal can be resolved by humans or by agents." and resolution moves to agents as they mature
- **#545** (open, parked, "Not approved to build"): "Human-reported signals on a business intent accumulate over time as a history". Measuring stays parked and out of this capability.
- **Specify against what exists** (Specify the product, "Status: to build."): "What's given is sorted against what exists: a new intent, an enhancement, a new feature under one, or a clash."

What memory holds, and does not:
- **The experience shelf** keeps, for products that model what people want: "Every node, edge, inference, and recommendation traces to evidence (URL, snippet, timestamp, extraction method, confidence)." and calls signals "hypotheses, not facts". It points the same way as naming each item and showing how sure a finding is; the pages quote it as a reason and write none of the shelf's building advice as a rule.
- **The ecommerce shelf** names "learn from behaviour and reviews" and review analysis, for a shop analysing its own buyers' reviews. Not about this capability.
- **The agent learnings**: supervised autonomy hands off "to a human with the context" on low confidence; the guardrails baseline names "prompt-injection and untrusted-content defense"; derive once, apply many says "source content is attacker-controllable text" and that a plan derived once is applied by deterministic code. They are written for agents built into a product; the pages quote only the untrusted-content line as a reason.
- **The cardinal rule** on recommendations: "Silence beats a wrong answer." and "The gap is reported."
- **The old provenance rule** (`features.md`, for the retired epic shape) tagged each field with its source and a confidence, and an assumption is "NEVER silent in the scope body". History.
- **No tier holds**: how to draw wants from free words and figures; how close two items must be to rest under one want; what makes a finding weak; who a product's competitors are or how to follow one; how often to understand and report.

## The open points, each with options and a lean

None of these is decided here. The drafts follow each lean and name the rest as not decided on the pages. The decided points are not reopened: the first capability connects and takes in, keeps each item as the tool gave it with connection, place and date, takes out every person's details, reads through one tool, and leaves where items are kept to an ontology decision; this capability understands and hands on, and changes no intent, page, model part or memory; the third capability builds or recommends; no lens, no seeding memory, no design lock or gate; the domain is settled at BI-6's close.

### 1. What "understanding what consumers want" produces

1. **Wants drawn from many items, each with its items, counts and place.** A want is a need or a problem in plain words; it lists every item it rests on, quoted word for word or figure for figure, with the items that say the opposite; it is summed (how many items, from how many connections, over what time, and how the count moved); it is placed on the intents, capabilities and features it bears on, or named as fitting none, a possible new need. Every item is under a want or listed as not used, with why. Gain: every finding can be checked against its items; nothing is lost; the next capability can act on parts. Cost: the most work per run; the lists grow.
2. **A periodic summary of themes**, without a link from each theme to its items. Gain: short to read. Cost: no one can check a theme, and two runs cannot be compared.
3. **Each item tagged with the part it bears on**, with no grouping into wants. Gain: simple. Cost: no understanding; the product owner reads hundreds of tags.

Lean: 1. The drafts follow it, with placing on intents and on the parts that serve them. A narrower form, placing on intents only (the design note's "Only on intents."), would leave the next capability to find the capability or feature each time.

### 2. What "what the competition is doing" covers, and where it comes from

Which competitors:
1. **Proposed from memory first and from the rivals people name in what is taken in, each with its source; the product owner says yes to each one followed.** A rival named often and not followed is shown as a proposal. Research, only when nothing names one, waits as a memory update. Gain: one yes per competitor, then the work runs on its own; no rival comes from the agent's own knowledge. Cost: a rival nobody names and memory does not hold is missed until the product owner names it.
2. **Every product people compare with this one is followed on its own.** Gain: no wait on a person. Cost: a passing mention or another kind of product becomes "the competition".
3. **Only the competitors memory names.** Cost: a new project's memory names none.

What is read about them, and from where:
1. **Only what people say, in the items the first capability took in** (feedback and forums). Gain: no new reading, no widening of the first capability's approved connections, and every finding is people's words with its source. Cost: the competition is seen only through what people say; a rival's change nobody has talked about is not seen.
2. **Also a competitor's own public pages** (its release notes, price list), read as a new kind of connection the first capability sets up through its one tool with the product owner's yes. Gain: what a rival itself says. Cost: widens the first capability's four kinds of connection, a change to an approved page for the product owner to approve; a rival's own pages are its own claims.
3. **Research on the web, raised as a memory update a person approves** before use. Gain: a built path. Cost: one study at a time, not a running understanding; each waits on a person.

Lean: competitors by 1 (with research only to propose a rival when nothing names one), and reading by 1 now; reading a competitor's own pages is named on the page as not decided. Never from what the AI agent knows by itself, in every option.

### 3. How the understanding stays repeatable and checkable when an agent does it

What holds: the first capability keeps each item as given, so items do not change under a finding; the decision trace and its check already exist for memory; the evals hold "two runs of one eval on one built product give the same verdict".
1. **Every finding names each item it rests on, quoted exactly; every item is accounted for; counts and sums are made by a tool; a second run on the same items gives the same wants, the same items under each, the same counts and the same places; someone other than the one who drew a finding checks it against its items.** Gain: a person can check any finding in minutes; a change in a finding means new items or a changed model, never the agent's mood. Cost: grouping free words the same way twice needs a method no tier holds yet.
2. **Findings name their items, but a second run may group them differently, as long as each finding is supported.** Gain: easier to build. Cost: two runs can disagree, and the next capability may act on one and not the other.
3. **The first run's grouping is kept, and each later run only places new items under it or adds a want.** Gain: stable by construction. Cost: an early bad grouping is kept until someone changes it.

Lean: 1 as the rule; 3 is one way to meet it, and named on the page as not decided (keep the grouping and place only new items, or draw again and compare).

### 4. How sure a finding must be before it is handed on, and how a weak one is shown

What holds: people's details are taken out before anything is kept, so items can be counted, never people; memory's cardinal rule wants the gap reported; the stale learning play surfaced low-confidence changes one by one.
1. **No threshold holds a finding back. Each finding shows its weight as facts a person can check: how many items, from how many connections, over what time, from words, figures or both, and the items that say the opposite. One that rests on few items or one connection is marked weak, shown in a part of its own and handed on as weak.** Gain: nothing hidden, nothing overstated; the next capability and the product owner weigh it. Cost: the report holds weak findings too; what counts as "few" is a project setting no source sets.
2. **A threshold**, such as a number of items from at least two connections, below which a finding is kept back as watched and not handed on. Gain: a shorter report. Cost: a number nobody set; a want under it is hidden while it grows.
3. **Confidence words chosen by the agent** (high, medium, low). Gain: familiar. Cost: a judgment no one can check.

Lean: 1. The pages also say a finding counts items, never people, because no person's details are kept; a want written many times by one person cannot be told from many people, and finding out would undo the first capability's rule.

### 5. Who sees the findings, how, and what goes to the third capability

1. **One current report for the product owner, kept up to date as new items come in, with what is new or has moved marked; weak findings in a part of their own; defects and parts no page names apart, with their owners. Nothing waits for his yes, because nothing outside the findings changes. The third capability takes the same findings, whole.** Gain: he reads what changed first; the next step acts on exactly what he sees. Cost: how often, and which change is big enough to tell him early, are project settings no source sets.
2. **A report on a schedule only**, such as each week. Gain: simple. Cost: a sudden change waits for the next report.
3. **Findings only to the third capability**; the product owner sees only its recommendations. Gain: less to read. Cost: he cannot check what the recommendations rest on, against his ask to understand consumers and competitors himself.

Lean: 1. Where the report is kept and where he reads it (a file in the project, or the planned review tool) is named as not decided; where the findings are kept, and as what kind of record, is a change to the agreed map, like what is taken in.

### 6. The lines with Keep the spec matched, Specify the product and the evals

What holds: Keep the spec matched compares the spec with the agents' work only, "not what the user is telling"; Specify the product turns what a person gives into the model, and Specify against what exists (to build) sorts what is given; Fix defects test first takes in "a defect reported anywhere" and names a defect no feature covers "as a new need for Specify the product"; Test what the product does, with evals the builder never sees sends a failure before acceptance to Build the work test first and one after to Fix defects test first.
1. **This capability names, and the owners act.** A want is placed and handed to the third capability. A defect (users say a feature the model holds does not do what its page says) is named for Fix defects test first, with its items, and is not a want. A part of the product that no page names, seen in what people do, is named for Keep the spec matched to what's built. A want that fits no intent is a possible new need for the third capability, which may take it to Specify the product. Gain: each finding has one owner; this capability changes nothing. Cost: the same report carries three kinds of hand-off.
2. **Everything goes to the third capability**, which sorts defects and gaps too. Gain: one hand-off. Cost: a defect waits for a recommendation step it does not need.
3. **This capability ignores defects and spec gaps.** Cost: users' reports of defects are lost, or counted as wants.

Lean: 1, with whether a defect and a spec gap reach their owners straight from here or through the third capability named as not decided. A product that fails what its stories asked, found by an eval, is never this capability's: the evals and their fixers own it.

### 7. How autonomous

What holds: "This needs to be built for high autonomy."; of continuous integration, "It would act like an agent." and "basically reflecting and telling us what needs to be done."; BI-6's must-not names a person only for changing an intent and promoting memory; this capability changes neither.
1. **The understanding, placing, report and updates run on their own each time new items come in; the product owner says yes only to which competitors are followed.** Gain: the shape he asked for; one yes per competitor. Cost: a wrong grouping reaches the report before anyone looks; the weak marks and the item lists are the guard.
2. **A person approves each report before it goes to the third capability.** Cost: a wait on every run for a change that changes nothing.
3. **No yes at all, competitors included.** Cost: the competition becomes whatever people mention (point 2).

Lean: 1.

### Smaller points, named as not decided on the pages

- How wants are drawn from free words and figures, and how close two items must be to rest under one want (no tier holds it).
- How few items, or connections, make a finding weak (a project setting).
- How a second run is made to give the same wants (point 3).
- Where the findings and the report are kept, and as what kind of record (point 5).
- Whether a competitor's own public pages may be read, as a new kind of connection (point 2).
- How a competitor is told apart from a product people only mention.
- Whether placing here and Specify against what exists sort the same way, as one shared step.
- Whether a defect and a part no page names reach their owners straight from here (point 6).
- How a finding is held against an intent in the model (no kind holds it).
- How often the report reaches the product owner, and which change is big enough to tell him early.
- How long a want must stop coming up to be marked as fading, and how the update learns that the model changed.

## The persona

What holds: the personas used so far are the product owner, the technical lead, the developer and the devops engineer. BI-6 is asked by the product owner, item 2 is his words, and the first capability's approved pages name him as the one who "wants what consumers want and what the competition is doing understood from what really happened".
1. **The product owner**: reads what consumers want and what the competition is doing, checks a finding against its items, and says yes to each competitor followed. Gain: the same reader as BI-6's page and the first capability. Cost: none found.
2. **A new persona**, such as a product researcher or a market analyst. Cost: no approved page, list or issue uses one, and his own words ask for this.
3. **The technical lead** for the placing on capabilities and features. Cost: placing decides nothing; the technical lead decides how work is built, not what consumers want.

Lean: 1, no new persona. The drafts follow it.

## The features found

1. **Understand what consumers want, from what is taken in** (fn-understand-consumer-wants). Not built. Sorts the items into wants and sums each, with every item it rests on, the items that say the opposite, its counts by connection and over time, how sure it is, and every item accounted for. Sources: his words ("start understanding what it is that the consumers want"); the list's item 2; the first capability's Out line ("sorting it, summing it"); Specify the product's coverage map, as a built pattern; the playbook catalog's "cluster into themes", as an idea never built.
2. **Understand what the competition is doing, from what people say about it** (fn-understand-competition). Not built. Proposes competitors from memory and from the rivals people name, with the product owner's yes for each, and draws what people say each does, offers or lacks, with its items. Sources: his words ("what the competition is doing"); the list's item 2; the first capability's feature that takes in what people say about "the products it competes with"; research-domain-context, as what exists and is not used.
3. **Place each finding on the intents, capabilities and features it bears on** (fn-place-findings). Not built. Names the parts each finding bears on, with why, or names it as fitting none or against an intent, and names a defect or a part no page names for its owner. Sources: the first capability's Out line ("placing it on the intents it bears on"); Specify against what exists (to build); Fix defects test first's intake; Keep the spec matched's rule that each fix is made by its owner; the placement skill and the placing script, as built patterns.
4. **Show the findings to the product owner, and hand them to the next capability** (fn-hand-on-findings). Not built. One current report with what is new or moved, weak findings apart, defects and spec gaps with their owners, and the same findings handed whole to the third capability. Sources: his words ("basically reflecting and telling us what needs to be done.", said of continuous integration; "or at least making those recommendations", the third capability's); the list's items 2 and 3; the slice play's brief and the cardinal rule, as patterns.
5. **Update the understanding as new items come in and the product changes** (fn-update-understanding). Not built. Updates wants and places, marks fading wants, proposes competitors to add or drop, and keeps what held before with why. Sources: his wording rule, recorded on the architecture page ("this should be reflected as updating arch. as the project changes."); the approved update features of Environment setup and of the first capability.

Candidates not drafted, and why:
- **Two features split by kind of item** (one for figures, one for words): a want often rests on both, such as messages asking for evening appointments and the figures of people leaving the booking page, so it is one job.
- **Build features, update the model, or recommend changes**: the third capability's, by his list.
- **Judge whether an intent is met, or measure it** (#545): parked, and not on BI-6's list.
- **Promote what is learned into memory**: not on BI-6's list.
- **Read a competitor's own pages**, or **research competitors on the web as a running job**: no source plans either; the first is open point 2's option 2, and research is used only to propose a rival, through a memory update.
- **File a defect or a work item**: Fix defects test first and Orchestration own them.
- **Rank the wants by importance**: what matters most is the next capability's and the product owner's call; the report orders by facts a person can check.

## Thin marks, and why

- The capability's ICE and all five feature ICE carry the thin mark, with at most three Limits and three Fails if each: no part of this capability is built.

## Lines elsewhere that are out of step (not changed here)

- BI-6's proof reads "Drift between the model and the work gets named." and "Each learning is promoted on purpose."; neither speaks of understanding consumers or competitors. The inventory's disagreement 1 already proposes rewording the first proof at BI-6's close.
- BI-6's page will list this capability in its Touches list when it is written.
- The agreed map of what a product is made of has no kind for a finding and no link from a finding to an intent; the first capability's items have the same open point.
- research-domain-context writes web research straight into short-term memory, not as a memory update a person approves, against ADR 035's rule. It is not used here.
- The glossary's Signals mean play invocations, while the design note's signal is anything received from outside; the pages use neither.
- Fix defects test first lists where a defect can be reported ("a person's words, a finding in a review, the eval after the work was accepted, or a bug in a plan"); a defect named by this capability from what users say fits "a defect reported anywhere" as written.
- The agreed line for Review what agents make (Argus) lists "ADRs, memories, domains, capabilities and ICE"; findings are not among them, and the report's place is not decided.

## Assumptions

- Assumed: "consumers" means the people the product is for, those who use it and those who talk about it or its kind of product; for a product teams use, the teams.
- Assumed, from the brief: the product owner's words on autonomy for continuous integration apply to this kind of work, and his list leaves building and recommending to the third capability.
- Assumed: this capability reads only what the first capability took in, and starts no read of its own.
- The examples come from several kinds of product: a shop's checkout, a clinic's booking app, a recipe app, a team's planning tool and a school's timetable app.

## Memory updates

None drafted. What no tier answers is named as not decided instead: how to draw wants from free words and figures, what makes a finding weak, who a product's competitors are and how to follow one, and how often to report. This run did no web research, and drafting an answer from the agent's own knowledge would break the rule; a person may ask for the research, and its answer would go to a memory update for approval. The placement is unmatched; the domain is not reopened, so no node is proposed.

## Checks

- **Structure check** (`lint_grounding.py`): the capability page (`--kind capability --stage directional`) and the five feature pages (`--kind feature`): ok, no errors, no warnings, after every edit.
- **ICE shape and wording check** (a small script in the session's scratch folder): each of the six ICE pages holds Intent, Context and Expectation in that order, exactly one Goal, one to three Limits and one to three Fails if, the thin mark as its first line, the fixed Read line with what to look for, the Context labels in order (Read, Never read, Persona, Scope), a Scenario, and a Done means checked by someone other than the doer. No part page holds an ICE section, and each has its ICE page beside it. Outside quotes and the Sources, no page says lens, seed, lock or gate, or names a business intent's number; no page holds a home folder, a temp folder or a real name.
- **Quotes** (the same script): all 160 quote checks on the twelve pages pass, word for word (spaces joined; markdown marks and YAML's doubled apostrophes read as one): each quote in a Sources line is in a file that line names, and each quote in a page body or its ICE page is in a file that page's Sources name. Memory quotes are checked against this run's copies in `memory/`, the product owner's words against `page-approvals.md` and `capabilities.md`. The first run found three labels written in quote marks (a want's wording and two placing results); they are now plain words.
- **Planted errors**: the script was run on copies with nine planted errors (a changed word in a quote, the right words in the wrong file in a Sources line, the same in a body, a made-up quote, a missing thin mark, a forbidden word, an ICE section on a part page, a Done means by the doer, five Limits on a thin ICE); it named all nine.
- **Quotes in this file**: all 73 are found word for word in the files read (the deleted /specify play is checked against its last version in git, and the GitHub quotes against the issues' text read today). The first run found one that joined two lines of a quoted block in the design note; it is now quoted in part.
- **Placement**: `routing-result.json` passes the skill's own check (`validate_route.py`: VALID).
- **Decision traces**: `cite-request.json` holds five decisions made from memory, each step with its tier, path, lines and fingerprint from the memory tool's read answer.
- **Not decided lines**: each "Not decided" line on the pages was read against the first capability's approval record and the brief's decided points; none reopens one. Where findings are kept is named as a change to the agreed map, like what is taken in, which the first capability left to the ontology; reading a competitor's pages is named as a new kind of connection the first capability would set up through its one tool with the product owner's yes, which keeps its approved rules.
