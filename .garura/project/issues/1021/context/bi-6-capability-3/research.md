# Build features or update the product model, on its own or at least as recommendations: research and drafts (issue 1021, BI-6 capability 3)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are in `.garura/project/issues/1021/context/bi-6-capability-3/drafts/product-os/software-delivery-planning/build-or-update-product/`: the capability page and its ICE page, and five feature pages, each with its ICE page. All six ICE pages carry the thin mark, because no part of this capability is built. They sit under software delivery planning, with the first two capabilities of Run → Product, for now.

In one line: nothing in Garura turns what a product's consumers want into a change to that product, and nothing recommends one; the first two capabilities, which would hand on the findings, are not built either. What exists gives patterns and hand-off targets only: the stale /learn-outcomes proposed changes to the model's meaning, each citing its outcome with a confidence tier, for one person's yes at one checkpoint; the memory update path waits for a person's word and keeps it as given, a turned-down one included; the plays' checkpoint settings can learn which kinds of change pass without waiting, with a list a person pins for good; and every part that would make a change (Specify the product, Add a feature found during work, Update the spec to match what's built, Replace or retire an intent, the design capabilities) already asks a person before it writes. So today an automatic change would still meet a person at its owner.

What this run did besides reading:
- It copied the memory files it decided from into `bi-6-capability-3/memory/`, with `manifest.json`, all from Phoenix memory: the ten domain shelves, the ontology, the checkpoint setting rule (`standards/rules/gate-config.md`), the cardinal rule on recommendations (`standards/rules/no-unbacked-recommendation.md`), the handoff rule (`standards/rules/expectation-generation.md`), and three learnings on agents (`agent-assistive.md`, `agent-supervised-autonomous.md`, `agentic-guardrails-baseline.md`).
- It searched Phoenix memory through the memory tool for autonom, recommendation, reversib, undo, human-in-the-loop and escalat.
- It ran the placement skill (find-work-placement) over the ten domain shelves. The result is unmatched (`bi-6-capability-3/placement/routing-result.json`, VALID by the skill's own check), as for the first two capabilities. The domain is not reopened, so no node is proposed.
- It read the model's approved pages it needed: the first two capabilities of Run → Product with their features, ICE and approval records; BI-6's page and BI-9's page; Specify the product, Specify intents and Specify against what exists; Turn intents into agent work and Add a feature found during work; Keep the spec matched to what's built, Update the spec to match what's built, Replace or retire an intent and Find where the spec and what's built no longer match; the openings of Gather the work under a chosen plan item, Write the evals that check the work, Design the work, Build the work test first and Fix defects test first; Manage surfaces and its update feature; Design the technology and architecture and its update feature; the domain page.
- It read the repo: `core/components/plays/learn-outcomes/` (stale), `core/components/skills/author-learnings/SKILL.md` (stale), `core/components/plays/update-plan/reference/ice.md`, `core/components/plays/update-plan/scripts/place_feature.py`, `core/components/plays/shape-slice/SKILL.md`, `core/tools/memory/README.md`, ADRs 026, 031, 033, 034 and 062, the design note `docs/philosophy/intent-and-adlc.md`, `.garura/project/issues/1021/context/capabilities.md` and the stock-take `bi-6-inventory/inventory.md`.
- It read GitHub, read only: open issues searched for recommend, autonomous, autonomy, learn loop, propose a change, new feature, update the model, product model moves, drift, experiment, idea, what to build and auto; it read #992, #990, #964, #979, #901, #611, #539, #545 and the closed #544. No open issue is about turning consumers' wants into product changes.
- It did no web research, so no memory update is raised.
- The decisions made from memory are in `cite-request.json`, for the caller to record with `memory.py cite` (the tool writes outside this run's folder).
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## The name

Proposed: *Build features or update the product model, on its own or at least as recommendations*. Folder: `build-or-update-product`.
- It keeps both halves of his words, building features and updating the model, and the "automatically, or at least" sense: *on its own* is the plain wording the first two capabilities use for automatic, and *at least as recommendations* keeps recommending as the floor.
- *The product model* stands for his "product intent model"; the capability page explains it as the business intents and the product model.
- Other names weighed: the list's own wording, "Build features into the product, or update the product intent model, automatically, or at least recommend those changes." (exact, and what the first two capabilities' pages already point to, but long); *Act on what consumers want* (short, but drops both halves); *Change the product from the findings, on its own or as recommendations* (drops building features by name and the "at least").

Words the pages use, and why:
- **Change**: one thing done to the product because of findings (a new feature, new words on a page, a new or changed business intent, a part retired).
- **Recommendation**: a change written out for the product owner to decide, with the findings it rests on.
- **On its own**: without waiting for a person's yes before the change starts; never without a person seeing it.
- **Go ahead on its own** and **set going**: plain words for acting automatically. The word gate is not used on the pages outside quotes.

## What is built, and what is only planned

Built and live, none of it for this capability:
- **The memory update path** (`core/tools/memory/README.md`): an agent raises a draft, and a person decides it, "approve or reject, who, their exact reply, and where they decided"; "Only a person decides, one update at a time."; a turned-down update keeps "the person and their reply exactly as given". Relevance: the pattern for a recommendation that waits for the product owner and keeps his answer.
- **Add a feature found during work** (Turn intents into agent work, through /update-plan): a person names a feature found while the plan is in progress, it is placed by fixed rules, "The script makes no judgment", and it lands with a thin ICE on one approval: "The model is written only through the model's own skills, never by hand, and only after". It cannot land today: "Known break: #1036." Relevance: the hand-off for a new feature under an intent that has a plan.
- **Update the spec to match what's built**, built in part: "A person's approved words can go on any page of the spec, a few lines or a whole page, all or nothing." Relevance: the hand-off for new words on a page and for an intent change the product owner decides.
- **Replace or retire an intent**, built in part: "An agent never replaces or retires an intent itself, even when the work no longer serves it." Relevance: the hand-off for retiring.
- **Specify intents** (/discover-intent): only a person confirms an intent; run by hand the confirm is pinned, inside a loop intents are saved as proposed for the loop's end review. Relevance: a new business intent comes only from a person's words.
- **The checkpoint settings** (`standards/rules/gate-config.md`, in Phoenix memory): every checkpoint is a setting; a conditional checkpoint learns from a person's answers ("Any rejection, requested edit, or correction resets the shape to gated."), and "`never_auto:` in the policy file is the human's permanent pin". The learning play's checkpoint is pinned: "a wrong model learning bends the product model". Relevance: a built way for a kind of change to earn going ahead without waiting, and a pin that names this very risk.

Built but stale:
- **/learn-outcomes with author-learnings**, stale: "waits for the rebuild of the learn loop on the current product model (#855)". It read Garura's own records of delivered work and proposed changes to the model's meaning: "Each proposed change carries the outcome that justifies it and a confidence tier."; "/learn-outcomes surfaces low-confidence changes one by one at the checkpoint."; one person approved the whole change. Its rule that "every proposed change cites the outcome that justifies it" is the pattern for every change resting on findings. It wrote the model itself; under the approved pages, page changes are Keep the spec matched's.

Planned only, or ideas on record:
- **The product owner's list, item 3** (2026-11-10), the only agreed source for this capability, and the first two capabilities' Out lines that hand it on.
- **Specify against what exists** ("Status: to build."): "What's given is sorted against what exists: a new intent, an enhancement, a new feature under one, or a clash."; its thin ICE: "Limit: A person decides any clash, and nothing existing changes on its own."
- **#990** (open): "When a story's design is approved, the model takes it."; "Each piece it changes is marked in review, not approved; a person approves it later."; "Leaving it is always allowed, and it leaves a record of what is owed." Relevance: the pattern for a change made first and reviewed after.
- **#979** (open): a thin page for a part found during work, "Approve the page before it is written, as with any model write."
- **#992** (open): "A gate in Garura is never a hard stop: it always has a key to pass it, and using the key records what must be done later." BI-9's Must not says the same: "Stop a person. Every gate has a way past it that records what's owed."
- **#964** (open): "Each piece of the product model carries its approval state, and agents build only from approved pieces".
- **#901** (open): /discover-intent changes a business intent that exists, writing "nothing until the person types yes".
- **The design note on intent and the agent lifecycle** ("designed, not in force", under #539): "A signal can be resolved **by humans or by agents. It depends on the maturity of the agents.**"; "resolution is owned deliberately, at a level of autonomy someone chose, and never assumed by default."; and its open question, "maturity has to be a recorded, deliberate setting rather than an impression". #544, which would have built it, was closed as not planned on 2026-11-02.
- **#611** (open spike): the Learn loop's recipe. Not about this capability's line, and not reopened.

What memory holds, and does not:
- **The autonomy learnings** (Phoenix memory, written for agents built into a product): assistive first, "Every effecting action is **staged for a human to approve**" and "The human is the commit button", keeping the record of what was suggested and what the person did as "data that later justifies (or denies) more autonomy"; then supervised autonomy, which acts inside a fence and escalates, "Not for irreversible, high-consequence actions". The guardrails baseline names "A kill switch." and a defined human-handoff trigger. The pages quote them only as reasons.
- **The cardinal rule**: "Silence beats a wrong answer." and "A play that recommends an action must be able to name the source that backs it."
- **The handoff rule** for recoveries: mechanical fixes are autonomous; what needs "judgment or authority the builder does not hold" goes to a person. A pattern only.
- **The ontology**: "Any play may write the intents, ICE or other kinds it finds" (ADR 031) and the rules "never stop a write", but "only a person confirms or drops a business intent", and an ICE whose capability serves no confirmed intent is "kept, not worked on".
- **No tier holds**: which kinds of product change an agent may make on its own; how sure a change must be; how a recommendation is shaped or where it is kept.

## The open points, each with options and a lean

None of these is decided here. The drafts follow each lean and name the rest as not decided on the pages. The decided points are not reopened: the first capability connects and takes in; the second understands and hands its findings on whole, says what is wanted and never what to do, and names defects and parts no page names for their owners, how they reach them left open; production is never touched; no lens, no seeding memory, no design lock or gate; the domain is settled at BI-6's close.

### 1. The line between "automatically" and "recommend", against BI-6's Must not

What holds:
- BI-6's Must not: "Change an intent, or promote memory, without a person." Promoting memory is not on BI-6's list, so here the Must not binds intents.
- Only a person confirms or drops an intent (ontology, ADR 031). Keep the spec matched: "Words change only from words a person approved." and "Never: fix drift in silence." Specify against what exists: "nothing existing changes on its own".
- Every part that would make a change asks a person before it writes today, including Add a feature found during work (only after the person's approval) and Turn intents into agent work ("Nothing reaches the tracker, the plan file or the model before the product owner's typed yes").
- Phoenix memory pins the old learning play's checkpoint, because "a wrong model learning bends the product model".
- His words: "This needs to be built for high autonomy.", "an autonomous kind of agent running that goes back and does this thing for me.", and the list's "automatically, or at least recommend those changes".

Options:
1. **Recommend only, always.** Every change is a recommendation the product owner decides; on his yes it goes to its owner. Gain: the Must not and every owner's yes are kept with room to spare; nothing new is needed downstream. Cost: no autonomy at all, against "built for high autonomy" and "does this thing for me"; every change waits on him.
2. **A project setting the product owner sets, kind by kind; recommend by default; a fixed list never automatic.** Every kind of change starts as recommend. He may set a kind to go ahead on its own. Never allowed, whatever the setting: a new business intent; an intent's words, proof, must-not or stage; retiring or replacing an intent; new words on a page that exists; taking a part out. The one kind proposed as ever allowed: a new feature under a capability that already serves a confirmed intent, resting on a clear want of the product's own consumers. A change that goes ahead is handed to its owner marked as set going by this capability and waiting for review, shown to him at once with its findings and a way back; setting the kind back stops it at once; his record of answers by kind sits beside the setting. Each owner keeps its own rules, so today such a change still meets a person at its owner. Gain: autonomy where he grants it, the Must not kept exactly, and the setting is his own decision, as the design note asks ("That autonomy level is itself a human decision"). Cost: until an owner agrees to write on this capability's word, marked in review, going ahead on its own ends at that owner's yes; a setting and a record to build.
3. **Learned autonomy.** As option 2, but a kind earns going ahead on its own from his answers, the way the plays' conditional checkpoints learn: a run of approvals of one kind as it was moves it to on its own, and any turn-down or change moves it back; the never list is pinned. Gain: the autonomy follows evidence, as memory's assistive-then-supervised rungs describe, and the learner is built. Cost: the agent's autonomy grows without his deliberate word, against the design note's "never assumed by default"; the first months are all recommendations.

Lean: **2**, with 3 named as a way it could grow, not decided. What a person sees after a change that went ahead: it is listed apart with what changed, where, its findings and items, and how to take it back. How it is undone: he turns it down; before it is built it is taken back through the part that made it (for a feature, removed with his name through Manage the model, and its work items dropped through Turn intents into agent work); once built, taking it back is a new change he decides.

Two points the product owner may want to settle with this line:
- Whether linking a new part to an intent counts as changing that intent. The Touches list on an intent's page is written by a script "whenever a play links a part to it"; it is a link, not the intent's words or stage. Lean: it does not count; the intent's words, proof, must-not and stage are what the person confirmed.
- Whether the pinned learning checkpoint in Phoenix memory binds this capability. It belongs to the stale learning play, and unpinning is "an intent change to that play (edit-play), never a config edit". Named as not decided on the pages.

### 2. What a recommendation holds, how it reaches the product owner, and what happens to one he turns down

Options:
1. **One record per change, in one current list he reads with the second capability's report.** It holds: the change's kind and part; the draft words for the owner where words change; the findings it rests on, whole, with their items; why; how sure, as facts carried from the findings; who decides; what it would set going and which part owns each step. He approves, changes or turns it down; his answer is kept word for word with who, when and where. A turned-down one is kept with his reason and raised again only when its findings move, showing what moved. An unanswered one stops nothing else. Gain: checkable without a search, nothing asked twice, nothing lost. Cost: a record kind the model does not have.
2. **One checkpoint per run, as /learn-outcomes had**: all changes at once, the less sure ones one by one. Gain: built once before. Cost: a run's changes stand or fall together, and nothing keeps a turned-down change between runs.
3. **Recommendations filed as issues in the tracker.** Gain: people already read the tracker. Cost: a write to an outside system for something that is a decision, not work; work items are Turn intents into agent work's.

Lean: **1**. How sure is shown as facts (how many items, from how many connections, over what time, any weak mark, any finding against an intent), never a confidence word the agent picks, to match the second capability. Where the list is kept and where he reads it (a file in the project, beside the second capability's report, or the planned review tool, whose agreed line names no recommendation) is named as not decided; so is whether he answers one at a time or many at once.

### 3. "Building features into the product": how a change starts down the existing path

What holds: the parts exist or are planned, each asks a person, and none starts from another part's record today. Turn intents into agent work makes epics and stories "after the product owner's yes"; the build phase starts when "The technical lead names one item by its ID, at any level of the plan"; Orchestration is "Narrowed on 2026-11-06: running the work once it exists." and is not yet reviewed.

Options:
1. **Hand each change to the part that owns its first step, with its findings and approved words, and follow it until it lands or is turned down.** A new feature under an intent with a plan to Add a feature found during work; a new feature or capability no plan holds, or a new intent in the product owner's words, to Specify the product (Specify against what exists); new words or an intent change to Update the spec to match what's built; retiring to Replace or retire an intent or Manage the model; a surface or architecture change to Manage surfaces or Design the technology and architecture. From there the work goes on as for any feature. It writes nothing itself and does not order the building. Gain: one writer per part, every owner's checks run, no new path. Cost: each change meets its owner's yes; how a change reaches an owner whose play starts from a person is open.
2. **Hand everything to Orchestration**, which picks the path and the order. Gain: one hand-off. Cost: Orchestration is not reviewed, and its approved one line is running work that already exists.
3. **Write the change itself** (thin pages, issues) to go faster. Cost: against the brief, against "Each fix is made by the part that owns it", and every owner's checks are skipped.

Lean: **1**. It does not wait for the plan: ordering the work is Orchestration's. Where the product owner approved exact words in a recommendation, those are offered to the owner as the approved words it needs, so he is not asked the same words twice; whether owners take them is not decided, because each would change its own rule. For work items, Turn intents into agent work's yes is tied to the list of work items, which a recommendation does not hold, so that yes stays.

### 4. A finding against an intent, a weak finding, and what the competition is doing

Options:
1. **None of them ever leads to a change that goes ahead on its own.** A finding against an intent becomes a question for the product owner (the second capability names it "never settled"); a weak finding stays as weak, listed as calling for no change yet or recommended with its weak mark; a competitor finding is context for a change a want of the product's own consumers calls for, never a change on its own. Gain: what goes ahead without a yes rests on what the product's own consumers clearly want. Cost: a rival's move nobody among the product's users talks about leads to nothing automatic.
2. **A competitor finding may go ahead when it agrees with a strong want.** Gain: faster reaction to rivals. Cost: the want alone already allows it, so the rival adds nothing to the rule.
3. **All of them may, under the setting.** Cost: a weak finding "sends the next capability after the wrong change", and a finding against an intent is the product owner's to settle.

Lean: **1**.

### 5. How every change is checked to rest on findings and items a person can check

Options:
1. **Each recommendation and change names its findings by their place in the handed-on set, and through them every item; a script, not the agent, refuses one that names no finding, names a finding not in the latest set, or goes ahead on its own from a weak finding, a finding against an intent or a competitor alone; someone other than the one who proposed it reads each against its items; and each decision keeps a trace, as the memory tool's decision traces do, so a later check names a change whose findings moved.** Gain: the floor is mechanical, and a person or a judge with no context reads the meaning. Cost: one more check to build.
2. **The product owner's review is the check.** Gain: nothing to build. Cost: changes that go ahead on their own would have no check before he reads them.
3. **A judge with no context reads every recommendation.** Gain: an outside reader on each. Cost: a model call on every change, including the plain ones.

Lean: **1**. Whether a judge with no context reads every recommendation or only the changes that go ahead on their own is a smaller point, left open on the research side; the pages carry the rule (every change names its findings) and the Done means (checked by someone other than the doer).

### Smaller points, named as not decided on the pages

- Whether working out a change and Specify against what exists sort the same way, as one shared step.
- How draft words for a page are checked before anyone sees them.
- Where the list of recommendations is kept and where the product owner reads it; one at a time or many at once.
- Whether a kind can earn going ahead on its own from his answers (point 1, option 3).
- Whether the owning parts may write a new feature on this capability's word, marked waiting for review.
- Whether other kinds may ever be allowed, such as work items for an allowed feature without the typed yes in Turn intents into agent work (depends on Orchestration).
- Whether the pinned learning checkpoint in Phoenix memory binds this capability.
- How a change reaches each owner: a record the owner reads, or starting the owner's play.
- Whether owners take an approved recommendation as their approved words.
- How a defect and a part no page names reach their owners (left open by the second capability; restated, not reopened).
- How long a want must fade before a waiting recommendation is withdrawn; how the update learns that the model changed.

## The persona

What holds: the personas used so far are the product owner, the technical lead, the developer and the devops engineer. BI-6 is asked by the product owner, item 3 is his words, he decides what the product becomes next, and the first two capabilities name him.
1. **The product owner**: decides each recommendation, sets which kinds of change may go ahead on their own, and reads what went ahead. Gain: the same reader as BI-6's page and the first two capabilities. Cost: none found.
2. **The technical lead**, for the build half. Cost: this capability starts no build; the build phase already names the technical lead as the one who names the item to build.
3. **A new persona**, such as a product strategist. Cost: no approved page, list or issue uses one.

Lean: 1, no new persona. The drafts follow it.

## The features found

1. **Work out the change each finding calls for, with why and how sure** (fn-propose-changes). Not built. For each finding handed on, the change it calls for, or none yet, with its findings, why, how sure, who decides and which part would make it. Sources: his words ("start building features into the product or start updating the product intent model"); the list's item 3; the second capability's hand-on ("What to do about it, building a feature or changing the model, or recommending it, is the next capability's work."); the stale author-learnings, as a pattern; Specify against what exists, as a planned pattern.
2. **Recommend each change to the product owner, and keep his answer** (fn-recommend-changes). Not built. One current list; approve, change or turn down, kept word for word; a turned-down one raised again only when its findings move. Sources: his words ("or at least making those recommendations"); the memory update path and the stale learning play's checkpoint, as patterns.
3. **Let the changes the product owner allows go ahead on their own, and show each one with a way back** (fn-act-on-its-own). Not built. The setting by kind, the never list, the conditions, the showing, the way back, the stop, and the record beside the setting. Sources: his words ("automatically", "an autonomous kind of agent running that goes back and does this thing for me."); the agreed Settings line ("Everything that can be turned on or off lives in settings."); the checkpoint settings, #990 and the design note, as patterns.
4. **Start each change down the path that builds it, through the part that owns each step** (fn-start-changes). Not built. Hand-off to each owner with findings and approved words, and following each change. Sources: his words ("start building features into the product"); the brief's decided point that building means starting the path; Keep the spec matched's "Each fix is made by the part that owns it"; the owners' approved pages.
5. **Update the recommendations as the findings and the product change** (fn-update-recommendations). Not built. Updates, re-works, withdraws and raises again, keeping what held before. Sources: his wording rule ("this should be reflected as updating arch. as the project changes."); the approved update features of Environment setup and of the second capability.

Candidates not drafted, and why:
- **Write the change itself** (thin pages, epics, stories, code): the brief and the approved owners forbid it.
- **Measure whether a change worked**, or judge an intent met: #545 is parked and not on BI-6's list.
- **Promote what is learned into memory**: not on BI-6's list.
- **Choose the order in which changes are built**: Orchestration's.
- **A separate check feature** for traceability: it is a rule of every feature and a Done means, not a job a person does inside the capability.
- **A feature for experiments** (try a change on some users and keep the result): the agreed Manage the model line holds "the source of what to try next", and nothing on BI-6's list asks for experiments.

## Thin marks, and why

- The capability's ICE and all five feature ICE carry the thin mark, with at most three Limits and three Fails if each: no part of this capability is built.

## Lines elsewhere that are out of step (not changed here)

- BI-6's proof reads "Drift between the model and the work gets named." and "Each learning is promoted on purpose."; neither speaks of building or recommending changes from what consumers want. The stock-take's disagreement 1 already proposes rewording the first proof at BI-6's close.
- BI-6's page will list this capability and its features in its Touches list when they are written.
- Phoenix memory pins the checkpoint of the stale learning play; if this capability's changes count as that play's learning, the pin would forbid anything going ahead on its own.
- Phoenix memory's naming files read "learn: Run -> Product. Read what happened and correct the intent." (stock-take, section 7); BI-6's Must not and Keep the spec matched forbid an agent to correct an intent without a person.
- The agreed Manage the model line ends "the source of what to try next", which reaches into recommending what to build (stock-take, disagreement 6); it is reviewed with the Product model intent.
- The agreed line for Review what agents make (Argus) names no recommendations, and where the product owner reads them is not decided.
- The agreed map of what a product is made of has no kind for a recommendation and no link from a change to the findings it rests on, as it has none for a finding or an item.
- Add a feature found during work cannot land today (#1036), so the main hand-off for a new feature under a planned intent is broken until it is fixed.

## Assumptions

- Assumed: "the product intent model" in his words means the business intents and the product model together.
- Assumed: BI-6's Must not, for this capability, binds an intent's words, proof, must-not and stage, its confirmation, and retiring or replacing it; linking a new part to an intent through the Touches list is not changing the intent (point 1).
- Assumed, from the brief: building a feature means starting the existing path, and this capability writes no code, issue or page.
- The examples come from several kinds of product: a clinic's booking app, a shop's checkout, a recipe app, a team's planning tool and a school's timetable app.

## Memory updates

None drafted. What no tier answers is named as not decided instead: which kinds of product change an agent may make on its own, how sure a change must be, and how a recommendation is shaped or kept. This run did no web research, and drafting an answer from the agent's own knowledge would break the rule; a person may ask for the research, and its answer would go to a memory update for approval. The placement is unmatched; the domain is not reopened, so no node is proposed.

## Checks

- **Structure check** (`lint_grounding.py`): the capability page (`--kind capability --stage directional`) and the five feature pages (`--kind feature`): ok, no errors, no warnings. The first run found two bullets under five words (*His answer is one of three:* and *What it updates:*); both now say what they introduce.
- **ICE shape and wording check** (a small script in the session's scratch folder, the one used for the first capability, pointed at this folder): each of the six ICE pages holds Intent, Context and Expectation in that order, exactly one Goal, one to three Limits and one to three Fails if, the thin mark as its first line, the fixed Read line with what to look for, the Context labels in order (Read, Never read, Persona, Scope), a Scenario, and a Done means checked by someone other than the doer. No part page holds an ICE section, and each has its ICE page beside it. Outside quotes and the Sources, no page says lens, seed, lock or gate, or names a business intent's number; no page, nor this file, `cite-request.json` or `routing-result.json`, holds a home folder, a temp folder or a real name.
- **Quotes on the pages** (the same script): all 302 quote checks on the twelve pages pass, word for word (spaces joined; markdown marks read as one): each quote in a Sources line is in a file that line names, and each quote in a page body or its ICE page is in a file that page's Sources name. Memory quotes are checked against this run's copies in `memory/`, the product owner's words against `page-approvals.md` and `capabilities.md`, the GitHub quotes against the issues' text read today.
- **Planted errors**: the script was run on a copy with nine planted errors (a changed word in a body quote, two wrong quotes in a page body, a changed quote in a Sources line, a missing thin mark, a forbidden word, five Limits on a thin ICE, a Done means by the doer, an ICE section on a part page); it named all nine. A tenth plant, the right words under another file, was not an error: that file holds the same words.
- **Quotes in this file**: all 86 are found word for word in the files read. The first run found 16 misses, all from this file's own wording: proposed names written in quote marks (now in italics) and single words in quote marks that threw the pairing of quotes off (now plain).
- **Placement**: `routing-result.json` passes the skill's own check (`validate_route.py`: VALID), unmatched.
- **Decision traces**: `cite-request.json` holds six decisions made from memory, each step with its tier, path, lines and fingerprint from the memory tool's read answer.
- **Not decided lines**: each "Not decided" line on the pages was read against the approval records of the first two capabilities and the brief's decided points; none reopens one. How a defect and a part no page names reach their owners is restated as left open, as the second capability left it; where recommendations are kept is a new point for this capability, beside the second capability's open point on where its report is kept.
