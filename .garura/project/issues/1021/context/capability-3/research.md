# Keep the original business intents: research and drafts (issue 1021, capability 3)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are under `.garura/project/issues/1021/context/capability-3/drafts/product-os/software-delivery-planning/keep-original-intents/`.

What this run did besides reading:
- It ran the model's gap finder (`core/components/skills/find-model-gaps/scripts/find_gaps.py`) read only, with its output in this folder: `checks/gap-candidates.json`.
- It tried one rewrite of an intent page through author-intent-page's script, on a throwaway copy outside the repo, never on the model: `checks/rewrite-sources-test.json`.

## The overlap with Specify the product

"Kept exactly as given" overlaps Specify the product in three places:
- Its Specify-from features (a file, a project folder, a deployed site, a document, plain words, and a video, not built) capture each Source and keep it exactly as given, with a fingerprint of each saved file. Its page has "In: keeping what a person gives as a Source." and a rule that "the Source must outlive the link or the file".
- Specify intents writes each intent's first page and never overwrites it (`persist_intent.py`: "an intent page is never overwritten"), and it keeps the person's answers and their confirm or drop replies in their exact words.
- Its Never line: "An intent page is never overwritten".

It also hands over the other half cleanly. Its page says: "Out: keeping intents up to date as the product changes. This capability does not do it, and no capability in the model owns it yet."

Three ways to draw the line:

1. **Split by time.** Specify the product takes things in: it captures each Source and writes each intent's first page. This capability keeps them afterwards: an intent's words change only through approved words, its links and record stay current, intents are replaced or retired on approval, drift is named, and what was given is read back later. Specify's pages change in one line only, the Out line above, which would name this capability. The cost: "kept exactly as given" happens in two places, at capture there and over time here, so a reader needs both pages.
2. **All keeping here.** The six Specify-from features and the Source rules move here, and Specify keeps only the understanding: walking journeys, and writing intents, domains and capabilities. One home for everything a person gave. The cost: one /discover-intent run is split across two capabilities, and the approved Specify pages are reopened: six features, its In line, its rules and its ICE.
3. **Split by kind.** Specify owns everything about Sources for good, including any later read-back; this capability owns only the intents: their words, links, replacing and retiring, tracker and drift. No kind is shared. The cost: the first half of this capability's agreed line ("Everything a person gives is kept exactly as given") would describe Specify's work, and "Read back what a person gave" would become a new feature of Specify.

My lean is option 1. Specify's own page already hands over "keeping intents up to date", the agreed line marks this capability unique for the keeping, and both proof lines it answers in Product → Spec ("Everything a person gave can still be read as given.", "An intent that drifts from the product gets named.") are about what happens after capture. The drafts are written to option 1. Under option 3 only the read-back feature moves; under option 2 the six Specify-from features come in and the drafts gain a capture section.

A second, smaller overlap is with Manage the model. The link rules and the gap skills are model work, and remove-model-part also merges capabilities and removes slices. The drafts keep only the intent's side here (its Touches list, repointing parts away from an intent, removing an intent's page) and leave the link rules, the merges and the slices with Manage the model.

## Features found

Six features. Four are built or built in part; two are not built.

- **Write an intent from approved words** (fn-write-intent-page). Built. Writes or rewrites an intent's page from words a person approved, never confirms by itself, and keeps the What-was-done and Touches blocks on a rewrite; a few lines can change instead through the page skill's named-lines request. Source: `core/components/skills/author-intent-page/` (SKILL.md, `scripts/write_page.py`), `core/components/skills/enrich-grounding/scripts/change_lines.py` (#993, changing named lines of any page).
- **Keep an intent current** (fn-keep-intent-current). Built in part. Keeps each intent's Touches list (the parts it reaches into, each marked adds, changes or removes) in step with the model's index; one script writes it for /discover-intent, /discover-domains, /shape-slice and the loop's gap-closing step, and the gap finder reports a link held on one side only. Not built: the Touches list from the two index skills, the record of what was done, and the met stage. Source: `intent_touches.py` (stamped into those plays and skills), `find-model-gaps`, `link-model-gaps`; the ontology's Touches and What-was-done properties.
- **Replace or retire an intent** (fn-replace-intent). Built. Moves the parts that serve an old intent to a new one, or drops the link, and removes the old page once nothing names it, all or nothing, only with the approver's name. Source: `core/components/skills/remove-model-part/` (SKILL.md, `scripts/remove_part.py`); ADR 065 rule 1.
- **Keep intents in their own tracker** (fn-intents-tracker). Built in part. The settings name an intents tracker apart from the work tracker, each intent page names its issue and takes its id from it, and BI-1 means an intent while #1 means work. Not built: a tool that reads the setting, filing an intent from a play, and keeping the issue's words and the page's words the same. Source: `core/config.yaml` (`trackers`), ADR 065 rule 4 and its decisions, `author-intent-page`'s id rule.
- **Name an intent's drift** (fn-name-intent-drift). Not built; its ICE is thin. Finds where an intent and the product no longer agree and names it to a person. Its basis is the agreed one line ("with no drift"), Product → Spec's proof line ("An intent that drifts from the product gets named."), the ontology's six lines that send drift to the Alignment loop, and ADR 031's Work This Creates ("The Alignment drive"). What exists today is the discovery loop's gap finder, which finds two of its cases during discovery only.
- **Read back what a person gave** (fn-read-back-given). Not built; its ICE is thin. Proves each kept Source still matches the fingerprints its capture recorded, and that each Source and its intents still name each other. Its basis is the agreed one line ("Everything a person gives is kept exactly as given") and Product → Spec's proof line ("Everything a person gave can still be read as given."). No list or old page names it as a feature.

Candidates not drafted, because only an ontology rule records them (the same bar capability 2 used):
- Record what was done for an intent as work finishes. The ontology's property says "updated as work finishes"; every page reads "(nothing yet)" and nothing writes it.
- Mark an intent met when its proof holds. The work checks accept met (`check_ice_workable.py`); nothing sets it.
- Show a clash between two intents that touch one capability in opposite ways, before work starts. Specify against what exists (not built) already covers a clash at input time.

The first two are named as not built on Keep an intent current.

## Gaps that matter, with what shows them

- **A rewrite drops the intent's list of Sources.** An intent saved by /discover-intent lists its Sources (`persist_intent.py` writes a `**Sources:**` block). author-intent-page keeps only the Touches and What-was-done blocks on a rewrite. The throwaway test confirmed it: after a rewrite, the Sources block was gone. So a rewritten intent loses its link to what the person gave, while the Source record still names the intent. This works against "kept exactly as given" more than anything else found.
- **Touches lists are out of step today.** The gap finder, run read only on the model, reports 43 links to an intent held on one side only. Six are on Product → Spec: the software delivery planning domain, Turn intents into agent work and its four features are in the index under the intent, and its page does not list them. The cause: link-model-part and remove-model-part write the index only, and /discover-capabilities writes a capability's intents in the index but not the Touches list. Inside the discovery loop the gap-closing step writes the missing side; outside it, nothing does.
- **Nothing outside discovery finds drift.** ADR 031 sent drift to an Alignment drive, "(its own drive, not yet designed)". ADR 045 gave a `/drift` play to the Learn loop; ADR 066 supersedes that part of ADR 045 and decides "the Alignment loop is unapproved and unnamed", for the product owner to name later.
- **No tool reads the trackers setting.** ADR 065: "No script reads the new `trackers` settings yet". A search of `core/` finds the setting read nowhere. The intents in the intents tracker were filed once, outside any play.
- **Where Sources live is unsettled, and it decides what a read-back reads.** /discover-intent keeps each snapshot in the issue's own evidence folder (`{stm_base}<issue>/evidence/intent/<run-ts>/source-<name>/`), while the ontology's Source kind says `{product_base}_evidence/intent/<timestamp>/`. The memory rules say a run never decides from another issue's short-term memory. So a read-back across Sources needs that settled first. This project's own model holds no Source at all: its intents came from the product owner's approved words, not from discovery.
- **The Touches list and features.** The ontology says the Touches list "does not name features; a feature is reached through its parent capability". `intent_touches.py` and author-intent-page accept the kind feature, the gap finder reports a feature missing from the list, and Product → Spec's page lists twelve features. The drafts keep the fixed form as built (domain, capability or feature) and do not decide this.

## Open points for the product owner

- Where the line with Specify the product goes: option 1, 2 or 3 above. The drafts follow option 1.
- Whether to keep the two features that are not built. Both rest on the agreed one line and Product → Spec's proof lines, not on a listed feature. Without them, nothing in the model answers those two proof lines.
- Where Keep intents in their own tracker belongs: here, under Track execution in the team's tracker (Orchestration), or under Settings.
- Whether Replace or retire an intent stays here, given that the same skill does Manage the model's capability merges and slice removals.
- Whether the Touches list may name features, as the tools and Product → Spec's page do, or only domains and capabilities, as the ontology says.
- Once this is approved, Specify the product's Out line ("no capability in the model owns it yet") needs to name this capability. That is a named-lines change to an approved page, and this run did not make it.
- The name and place of the step that names drift, which ADR 066 leaves to the product owner.

## Details left out of the pages

The pages hold what each part does, its main rules with their reasons, the gaps that matter and the checks that prove it. An agent that builds or changes these parts finds the rest in the code:
- The fields of each request and report (`intent-draft.json`, `intent-page.json`, `lines-request.json`, `remove-request.json`, `remove-report.json`, `gaps.json`).
- The fixed order of the parts on an intent page, and the exact form of its stage and Tracker lines.
- The older form of the Touches list (`**ICE built from it...:**`) that `intent_touches.py` still reads.
- The order the removal script works in (repoints, merges, slices, intents) and how it keeps the index's comments and layout.
- A page in a holding folder that the gap-closing step moves under its parent, and the relink that follows it.
- How the discovery loop saves intents as proposed and lets a later round rewrite only pages it saved.

## Structure check

`python3 .claude/skills/discover-capabilities/scripts/lint_grounding.py` on each page, with `--kind capability --stage directional` for the capability and `--kind feature` for each feature: all seven pages read ok, with no error and no warning. The record is `.garura/project/issues/1021/context/capability-3/lint.json`.

The structure check has no kind for an ICE page, so a small check in the same record tested each of the seven ICE pages: the three sections in order, exactly one Goal, at least one Limit, one Fails if and one Done means, the fixed Read line, the thin mark on the two parts that are not built and on no other. All seven read ok.

Every quote in a Sources section was checked against its file, word for word: 102 quotes, none missing. Four Sources lines carry no quote: the short line beside each feature, the shelf line, and the two lines about the throwaway rewrite.

## What this run read from memory

Six files from Phoenix memory, through the memory tool, copied to `.garura/project/issues/1021/context/capability-3/memory/` with `manifest.json`: the ontology, the ICE rubric, the model-write rule, and the capability, feature and content-standard grounding templates. Nothing in Garura or Phoenix memory holds the note "anyone writes; align later"; the drafts take it from ADR 043, ADR 031 and the ontology, which say the same. The decision and its trace are in `cite-request.json`, for the caller to record; this run writes nothing outside `capability-3/`.
