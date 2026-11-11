# BI-11 (Product model): what Garura has for defining what a product is made of, and for managing the model

Research only, 2026-11-11, for #1021 (the chore that reorganises Garura's business intents around the phases and their
transitions). Nothing under `.garura/product/`, `.garura/core/`, `.claude/` or `core/`, on GitHub or in git was changed.
No memory update was raised or decided, and no decision trace was recorded, because the brief allowed this one file
only. Read-only checks were run from the repository root on 2026-11-11: the ontology check, the model's structure
check, the ready check and the gap finder on the product model (each wrote its report outside the repository), and the
test suites of the model's skills. Memory was read only through the memory tool.

Scope: BI-11 only. Its page: Outcome "One living map of the product: an ontology that defines what a product is made
of, a model defined and managed as it grows, a link to the work, and a source of new ideas and experiments." Proof: "A
person changes the ontology through one play and the model still passes its checks.", "Any part can be added, changed
or removed.", "From any intent, you can list what serves it.", "The model proposes an idea with its evidence, a person
confirms it, and an experiment records the result." Must not: "Block work because the model is incomplete, let an agent
confirm an intent, or name a plan." (`intents/bi-11.md` lines 3, 10-13 and 15). The agreed two capabilities are in
`capabilities.md` lines 122-124.

## In one paragraph

Garura has a written map of what a product is made of, and a set of tools that write the model, but not yet one
living map that keeps itself in step. The ontology is at version 15: thirteen kinds, 47 questions (45 answered, one in
part, one not yet), and its check reads valid. It changes only through /edit-ontology, with the product owner's typed
yes at three pinned points, and Phoenix memory holds the same version, so every project reads it. But a product project
can never change it (the play is installed only in a harness repository), and nothing checks the model after the
ontology changes. Today the model fails its own structure check (21 errors), and the check, the page templates, the
index's schema and the glossary still describe an older ontology: 249 warnings ask for an ICE section that version 6
moved to its own page. The model is written by one sub-agent through its skills, and the six that carry scripts pass all their tests. A part can
be added, its words changed, its page moved and an intent repointed, but no skill removes a feature, a domain or an
ICE, and a capability that has its own ICE page cannot be merged, which is 38 of the 41. The ready check runs, but
today it calls no part ready: 249 are partly ready, mostly because "identified by" is missing, which the ontology both
allows and counts as a gap, and the 13 older parts whose ICE is still inside their page read as not ready (#1033). What
serves an intent is held on both sides (the intent page's Touches list and the index), with 21 links on one side only,
and no command lists it for a person. Approval on each part (#964), the model moving with the work (#990), one tool
that creates and edits the model (#1030) and the --edit option in every play (#962) are planned only. Nothing proposes
ideas or records experiments, and no issue plans it. No part in the model serves BI-11 yet. About 50 lines on 38
approved pages of other intents already hand work to it. The old capability "Link the product model" (`cap-723`, filed
under the closed intent `bi-722`) and its four features belong here.

The four proof lines today:

| Proof | State | Where |
|---|---|---|
| A person changes the ontology through one play and the model still passes its checks | Built in part: the one play is built; the model's checks are not run by it, and today the model fails them | Sections 1.2, 1.6, 2.7 |
| Any part can be added, changed or removed | Built in part: add and change are built; removal covers an intent page, a capability merge and a slice only | Sections 2.2-2.4 |
| From any intent, you can list what serves it | Built in part: the links are kept, with 21 on one side only; no command lists them for a person | Section 2.9 |
| The model proposes an idea with its evidence, a person confirms it, and an experiment records the result | Neither: no build and no issue | Section 2.12 |

## Words used here

- **Business intent**: what a person wants, in their words. Written **BI-n** when it lives in the intents tracker
  (`intent-driven-ai/garura-intents`). A work issue is written **#n** and lives in `intent-driven-ai/garura`.
- **The ontology**: the written map of what a product is made of, `core/components/memory/standards/schemas/product-os/
  ontology.md` (source). A **kind** is one sort of thing in it (Business Intent, Domain, Capability, Feature, ICE and
  so on).
- **The model**: Garura's own product model, `.garura/product/product-os/`. A **part** is one domain, capability,
  feature, ICE or slice in it. The **index** is the model's list of every part, `_spine.yaml`. An **ICE page** is a
  part's `ice.md`, beside its page. A **thin** part or ICE is one proposed from a person's words and marked to be
  deepened.
- **The keeper**: the sub-agent that writes the model, `product-os-keeper` (`core/components/agents/product-os-keeper.md`).
- **The model's skills**: the page skill (`enrich-grounding`), the two index skills (`link-model-part`,
  `remove-model-part`), the intent-page skill (`author-intent-page`), the gap finder and closer (`find-model-gaps`,
  `link-model-gaps`), and the discovery writers (`author-domains`, `enrich-capability-ice`).
- **The structure check**: `lint_grounding.py` (one script, copied into each play that writes the model). **The ready
  check**: `check_ice_workable.py`. **The Touches list**: the list on an intent page of the parts it reaches into.
- **Paths**: a path that starts with an issue number, such as `1021/context/...`, is under `.garura/project/issues/`. A
  model page written as `<folder>/capability.md` is under `.garura/product/product-os/software-delivery-planning/`.
  Old parts live under `.garura/product/product-os/capabilities/` and `.../features/`. Phoenix memory files are named by
  their memory path and were read through the memory tool.

States: **Live** · **Live, out of step** (works, but disagrees with a later rule or decision) · **Designed only** (an ADR
or doc, no build) · **Planned only** (an open issue) · **Neither** (no build and no issue).

## 1. Define what a product is made of

The agreed line: "People and agents share one agreed map of what a product is made of, changed only on purpose."
(`capabilities.md` line 122).

### 1.1 Built: the ontology

- `ontology.md`, version 15, updated 2026-10-31 (lines 1-5), 893 lines. "The agreed map of what a product is made of in
  Garura ... A person and an agent reading it use the same words for the same things. It defines thirteen kinds in two
  layers ... It grows one kind at a time, through the `edit-ontology` play, and the product owner agrees each change."
  (line 9).
- **Thirteen kinds**: the product layer (Business Intent, Source, Domain, Capability, Feature, Slice, ICE), the Plan,
  and the work layer (Epic, Story, Spike, Chore, Bug). Each has what it is, who reads it, where it lives, a properties
  table, relationships, rules and examples from three fields (shop, clinic, bank). "Not yet defined: None." (lines
  868-870).
- **47 questions it must answer** (lines 27-169). 45 are answered. Q3 ("When two intents touch the same part of the
  product and want opposite things, is that shown to a person before any work starts?") is "partly"; Q4 ("which work
  did agents finish on their own, and where did a person have to step in?") is "not yet", because "no kind yet holds
  where a person stepped in" (lines 35-40).
- **The rules that matter to this intent.** "**Nothing is blocked** (the product owner, 2026-10-21). A plan can be built
  and worked on before the product model is complete" (line 23). "No play owns a kind ... The rules below say what holds
  once the product is **aligned**; they never stop a write ... What a rule can stop is work, never a write ... One thing
  is never left to alignment: only a person confirms or drops a business intent." (line 25).
- **A log line for each version**, from the first (2026-10-08) to v15 (2026-10-31) (lines 872-893).
- **The check.** `author-product-ontology/scripts/check_ontology.py` holds the format: front matter, the four sections,
  every question's "Answered by" and status, every kind's parts, every relationship pointing at a defined kind (lines
  7-16). Run on 2026-11-11: `"valid": true`, no problems. Its tests: 27 passed.
- *State:* Live.

### 1.2 Built: changing the ontology through one play

- **/edit-ontology** (`core/components/plays/edit-ontology/`, compiled from `reference/ice.md`). Intent: "A person changes
  Garura's product ontology — its kinds, their links and their rules — one need at a time. Every change is agreed with
  the product owner, checked by a script, and landed through the change plays." (`ice.md` lines 8-10).
- **Three pinned checkpoints**: the questions, the kinds, the links and rules (C2, `ice.md` lines 15-17). Step 2 is
  "**pinned** — the product owner decides, C2; never skipped by config" (`SKILL.md` lines 147-148); Steps 4 and 6 are
  pinned too (lines 168, 181-182). Each answer is recorded word for word with the sha256 of the draft shown.
- **Scripts decide**: the ontology check after the write (C5: "The run ends only when the ontology check passes"), and a
  change check that only the kinds the need touches changed, the version is up by one with one log line, and no real
  name appears (Step 8, lines 214-231). Its tests: 11 passed.
- **The skill**: `author-product-ontology`, seven steps in four stages (scope, kinds, links, write), "Run by the
  `edit-ontology` play only" (`SKILL.md` line 11), run through the keeper.
- **It lands through the change plays** (C7), on the plan's branch when the issue is in a plan.
- **Only in a harness repository.** "It is installed only in a harness repo, never into a product project."
  (`author-product-ontology/SKILL.md` line 15). The install's `full` scope leaves out "edit-ontology" and
  "author-product-ontology" (`install-garura/scripts/install.py` lines 210-218). So a team's product project cannot
  change the ontology it works by.
- **The skill's defaults point at a machine-wide copy** of memory in the home folder (`author-product-ontology/SKILL.md`
  lines 34-35). The play passes the source path, so the default is not used by the play; BI-10's stock-take records that
  the machine-wide copy is to go (ADR 055 §8).
- *State:* Live, in Garura's own repository and harness repositories.

### 1.3 Built: the ontology reaches every project

- The settings name it by its place in memory: `ontology: standards/schemas/product-os/ontology.md`, "A play hands this
  to its agent; the agent reads it through the memory tool" (`core/config.yaml` lines 181-183).
- Phoenix memory holds it: the memory tool answers `standards/schemas/product-os/ontology.md` from the `phoenix` tier, at
  version 15, and its 893 lines are the same as the source, word for word (read on 2026-11-11). Garura memory in this
  repository holds no copy.
- #868 (the current ontology and other current standards are in no memory tier) was filed when Phoenix memory held
  version 4. Its ontology part now holds; its wider check of every standard is BI-10's (its parent is #921, Phoenix
  memory stays up to date as Garura is built).
- *State:* Live.

### 1.4 Built in part: the parts that read the ontology, and where they are out of step

| Part | What it says | Out of step with the ontology |
|---|---|---|
| Page templates (`standards/schemas/product-os/grounding/capability.md`, `feature.md`) | "## Agent intent (ICE) — the last section, at every stage" (capability.md lines 56-59, 108; feature.md lines 47-50) | Since v6 "The ICE is on its own page, never a section of the capability page" (ontology line 362). There is no template for an ICE page. #1030: "The page template and the page skill still describe the older shape, and nothing stopped it." |
| The index's schema (`standards/schemas/product-os/spine.yaml`, version 2, line 26) | `depends_on: [string]  # "needs" (ontology v5) ... Field renamed to needs under #725` (lines 91-92, 113-114); `identified_by: string` (lines 93, 115); an `ices` list (line 131) | The field is still `depends_on`; `identified_by` holds one id, while the ontology says it "may name more than one" (line 345) |
| The structure check (`lint_grounding.py`) | Checks headings, a floor of substance, the index against the pages, and each ICE entry (lines 3-25) | Still warns that a part with an intent has no `## Agent intent (ICE)` section: 249 warnings on parts whose ICE is on its own page (section 2.7). It does not check `depends_on` or `identified_by` (`features/fn-725/feature.md` line 28) |
| The discovery writers (`enrich-capability-ice`, `author-domains`) | Write the ICE inside the page, from the templates | #762 (/discover-capabilities and its skills write ICE nodes) is open. The page skill already writes `ice.md` when the index has an `ices` list (`enrich-grounding/SKILL.md` line 51) |
| The glossary (`core/grounding/glossary.md`) | "ProductOS ... a 3-level tree ... plus personas and journeys" (line 61); a capability "carries ICE" (line 62); the ICE is "attached to a capability or feature node ... Workable only when built from a confirmed business intent" (line 65); "Product ontology ... Built with `author-product-ontology`" (line 68) | Since v6 the ICE has its own page and "no link to a business intent" (ontology line 482); the ontology changes through /edit-ontology |
| The model itself | 13 parts keep their ICE inside the page; 249 have an ICE page (a read of `_spine.yaml`) | #765 (move each ICE section to its own ICE node) is open; the 13 are all old parts (section 4) |

- *State:* Live, out of step.

### 1.5 Where the ontology disagrees with itself, or the model with the ontology

1. **"Identified by" is both normal and a gap.** The property: "empty when it was found on its own" (ontology line 345).
   The rule: "A missing domain or a missing "identified by" never stops work; it is a gap, and its ICE is partly ready."
   (line 369). The ready check follows the rule, so 257 parts carry the gap "has no identified by" and none reads ready
   (section 2.6). `features/fn-725/feature.md` line 23 says the opposite: "Empty means that the node was found on its
   own. This is normal and gives no warning."
2. **A feature needs another feature.** The ontology: a feature "never needs anything and is never identified by
   anything" (line 409); "Garura's own model: fn-727 → fn-724 is not allowed; it becomes cap-718 → cap-723 (the move is
   #765)" (line 412). The index holds six feature needs: `fn-727` needs `fn-724`, and `fn-743`, `fn-744`, `fn-745`,
   `fn-746` and BI-7's `fn-748` need `fn-741` (a read of `_spine.yaml`). `features/fn-725/feature.md` line 21 still
   says "A feature can need a capability or another feature". BI-10's close kept `fn-741`'s id for `fn-748`
   (`capabilities.md` line 117). Orchestration's approved page leaves it open: "Not decided: whether a feature's own
   needs count too, as the page of fn-725 says, or only the needs of its capability, as the ontology says."
   (`orchestrate-agent-work/fn-work-out-waits-on/feature.md` line 42).
3. **"Identified by" holds one id in the index, and may hold more in the ontology** (spine schema line 93; ontology
   line 345). `cap-723` holds the one string `cap-718`.
4. **The model holds kinds the ontology does not define.** The index holds a `profile` block (the product's levels and
   compliance) and the model a `decisions/` folder with one product decision
   (`dec-cap-initialize-security-none-medium.yaml`). The ontology has no Product Profile and no Decision kind (no
   "profile" in its text). Approved pages hand both to Product model (section 3.3).
5. **The model does not record which shape it is in.** The index has no version; only its schema file does. BI-7's
   approved page: "Not decided: how the upgrade tells which shape a model is in. The spine records no version of its
   shape, so today only the old names tell." (`upgrade-project/fn-move-model/feature.md` line 24).

### 1.6 Not built: the model is not checked when the ontology changes

- /edit-ontology checks only the ontology document and its change (Steps 7-8). It changes "only the kinds that need
  touches" (C1), so it never touches the templates, the schema, the structure check or the model, and runs none of the
  model's checks. The proof's "the model still passes its checks" has no step that tests it.
- The model fails its checks today (21 errors, section 2.7), so the proof does not hold even before a change.
- *State:* Neither (no issue asks /edit-ontology to check the model).

### 1.7 Planned only

- #694 (the product model rules say what ADR 043 changed — who writes each kind, loose nodes, Sources), under #723. Its
  text names gone plays (/vision, /understand) and "functionalities".
- #725 (the field `depends_on` renamed `needs`, and a check that each need and identified-by link points at a part that
  exists), under #723.
- #761 (plays write ICE nodes) with #762 (/discover-capabilities and its skills write ICE nodes), #763 (the judges check
  plain English and the three parts) and #1033 (plays read the whole model by one rule once its index has ICE entries,
  so older parts break); #1031 and #1037 under it are closed.
- #764 (move Garura's own model to ICE nodes) with #765 (move each ICE section to its own ICE node, and lose nothing).
- #645 (every piece of the model carries its approval state): "The ontology ... names one approval lifecycle for every
  kind", under #964.

### 1.8 Neither

- A step in /edit-ontology that runs the model's checks before and after the change and shows what it breaks.
- A way for a team's project to change or extend the ontology.
- A recorded version of the model's shape.
- Kinds for the product profile and the product decision.

## 2. Manage the model

The agreed line: "A living map, added to and pruned as work is done, and the source of what to try next. (unique)"
(`capabilities.md` line 123), with "Feature to add when this capability is reviewed: a tool that knows how to create and
edit the product model (#1030). Not built, and to be built later." (line 124).

### 2.1 Built: one sub-agent writes the model, only through its skills

- The keeper is "the autonomous owner of the persistent product model" (`product-os-keeper.md` line 19). Its rule:
  "Change the product model by hand. You may change any part of it — a page, the spine, an intent page, the profile —
  but only through a skill (the product owner, 2026-10-29). ... When no skill covers a change, say so and stop: the
  missing skill is built, never worked around." (lines 176-184, under NEVER).
- The written contract for model writes: "A model-writing play edits the real product model in place on the feature
  branch" (`standards/rules/direct-model-write.md` lines 14-16); "The LLM writes only per-node doc files; a keyed script
  owns every shared file" (line 30); "Outside a play. Two more writers, each run by `product-os-keeper` and keyed by its
  request" (lines 53-60).
- ADR 065 rule 1 (accepted 2026-11-02): "`link-model-part` adds or changes a part. `remove-model-part` takes a part out,
  with the name of the person who approved it. ... Plays move onto these two skills over time" (ADR 065 lines 129-131).
- *State:* Live.

### 2.2 Built in part: add a part found during work

- **The page.** `enrich-grounding` writes a new feature page under a capability that exists (`new-feature`), the
  minimum ICE for a part that has none (`thin`), and a page a person approved word for word, a domain, capability,
  feature or ICE page (`approved`, `write_approved.py`, #1031). Its tests: 16 passed for `write_approved.py`.
- **The index entry.** `link-model-part` writes a new domain, capability, feature or ICE entry, with the thin mark in
  both places when it is thin; "All or nothing"; "Only inside the product model" (`link-model-part/SKILL.md` lines
  52-62). Its tests: 48 passed.
- **Who uses it today.** /update-plan for a feature found during a plan (BI-1's "Add a feature found during work",
  `turn-intents-into-work/fn-add-found-feature/`, #931 closed), and the #1021 reorganisation itself.
- **Not built:** "A shared step, not a per-play feature" that lets any play add a thin page inside the change already
  open (#979, a feature found during work gets a thin page in the product model, inside the open change, without the
  full discovery). #979: "The shared play step comes later."
- *State:* Live for the skills; the shared step Planned only.

### 2.3 Built: change a part

| What changes | How | Evidence |
|---|---|---|
| Named lines of any page (domain, capability, feature, intent) | `enrich-grounding`, `change_lines.py`, all or nothing (#993) | `enrich-grounding/SKILL.md` description; tests: 19 passed |
| A whole page a person approved | `enrich-grounding`, `write_approved.py` (#1031) | tests: 16 passed |
| An intent page, from its draft; a rewrite keeps "What was done" | `author-intent-page`, `write_page.py` | `author-intent-page/SKILL.md` lines 9-13; tests: 50 passed |
| A part's one-line, its intents (added only), its issue, its thin mark | `link-model-part`, `update` mode | `link_part.py` lines 39-42 |
| A thin mark taken off; a feature filed under another capability; a page moved with its ICE page | `link-model-part`, `thin: false`, `capability`, `doc` (#1037) | `link_part.py` lines 42-56 |

- **Not built:** changing a capability's domain once it has one (`link-model-gaps` sets it only for a loose part:
  "Never move a node already under a parent", `link-model-gaps/SKILL.md` line 61); writing a need or an
  identified-by link after a part is made (`link_part.py` takes `identified_by` only on `new`, and no field for needs);
  taking the thin mark off an ICE ("mode `update` only marks an ICE that is there thin", `link_part.py` lines 66-67).
- **Planned:** one way for a person to change a record through the play that owns it, `/<play> #<id> --edit: <their
  words>` (#962, with #901 for /discover-intent, #905 the shared rule and check, #906 for /discover-domains, #907 for
  /discover-capabilities and #910 for /create-play). Built for /shape-slice (#908, closed). Today /discover-intent
  refuses when "an intent page already exists" (`discover-intent/scripts/persist_intent.py` lines 22-29).
- *State:* Live for the skills; Planned only for the plays.

### 2.4 Built in part: take parts out

- `remove-model-part` repoints parts from an old intent to a new one, or drops it; removes an intent page once nothing
  names it; merges a capability into another; removes a slice and its record. It needs "the person who approved it",
  refuses while a page still names the part, and puts every file back when a write fails (`remove-model-part/SKILL.md`
  lines 11-13, 72-85). Its tests: 63 passed.
- **What it cannot take out.** `REMOVABLE = ("intent", "capability", "slice")` (`remove_part.py` line 78), and "a
  capability is never simply removed: it merges `into` another" (`SKILL.md` line 35). No skill removes a feature, a
  domain or an ICE.
- **What it cannot merge.** A capability "has its own entry in the spine's `ices` list, so it cannot be merged here"
  (`remove_part.py` lines 227-228). Today 38 of the 41 capabilities have an ICE entry; only `cap-723`, `cap-718` and
  `cap-shape-eval` could be merged (a read of `_spine.yaml`).
- Inside a loop, `link-model-gaps` also removes the dropped part of a duplicate marked `agreed: true`
  (`link-model-gaps/SKILL.md` lines 32-35). ADR 065: "Its key is an agreed gaps.json, not a person's name. ... It leaves
  ADR 044's exception inside a loop standing for now." (lines 37-43).
- *State:* Live in part.

### 2.5 Built in part: link the parts

| Link | Built | Evidence |
|---|---|---|
| A part serves an intent, on both sides (the index's `intents` and the intent page's Touches list) | Live in part | `intent_touches.py` writes the intent's side ("It is never written by an LLM", lines 1-14), in the plays that save intents and domains, the play that fills a slice's parts and the loop's gap closer. "The two skills that change the model's index outside a play, and the play that writes capabilities, do not write an intent's list" (`keep-spec-matched/capability.md` line 28). The gap finder finds 21 links on one side only (section 2.8) |
| Needs and identified by | Planned only | The field is still `depends_on`; no check that a link points at a part (`features/fn-725/feature.md` lines 4, 28); #725 open. No capability has a need; six features do, against the ontology (section 1.5) |
| A domain for search | Planned only | "a search by domain shows its business intents and capabilities" (`capabilities/cap-723/capability.md` line 35); #726 open; no script searches by domain |
| A slice serves an intent | Live | `/shape-slice` writes it; the link is kept on the slice's side only (ontology line 205) |

- *State:* Live in part.

### 2.6 Built: the ready check

- `check_ice_workable.py`, four identical copies (`create-play/references/`, `discover-intent/`, `shape-plan/`,
  `update-plan/`). It answers ready, partly ready or not ready for each ICE, with what stops it and the gaps
  (`features/fn-724/feature.md` lines 3-27; #724 and #760 closed).
- **Run on the model on 2026-11-11:** 0 ready, 249 partly ready, 13 not ready. The gaps: "has no identified by" on 257
  parts, "thin ICE" on 129, "has no domain yet" on 5. The 13 not ready are the 13 old parts whose ICE is inside their
  page, each stopped by "has no ICE" (`cap-723`, `cap-718`, `cap-shape-eval`, `fn-724`, `fn-597`, `fn-725`, `fn-726`,
  `fn-727`, `fn-728`, `fn-818`, `fn-798`, `fn-898`, `fn-931`).
- **Why:** "Once the ICE list exists, `check_ice_workable.py` reads only ICE entries, so a part with its ICE inside its
  page "has no ICE"." (#1033). "/shape-plan would skip every older feature." (#1033); /shape-plan: "a feature whose ICE
  is not ready is skipped and named" (`shape-plan/SKILL.md` line 5).
- **Open:** #805 (the ready check says when needs were not checked): "Without `--done`, needs are not judged: a
  capability with an open need is answered ready, and nothing in the answer says needs were not checked."
- *State:* Live, out of step.

### 2.7 Built: the structure check

- `lint_grounding.py`: "It enforces SHAPE and LINK INTEGRITY — never content quality" (lines 3-25). 13 copies, all the
  same (one in /create-play's references and one in each play that writes the model). The live plays that run it:
  /discover-intent, /discover-domains, /discover-capabilities and /shape-slice. /shape-slice's model check "does not go
  on until it reads valid" (`shape-slice/SKILL.md` line 608).
- **Run on the whole model on 2026-11-11 (`--root` and `--spine`): not ok, 21 errors, 263 warnings.**
  - Errors: 8 in `cap-718/fn-727` and `cap-718/fn-728` (four missing sections each); 12 in BI-1's three features
    `specify-product/fn-specify-from-video`, `fn-validate-attribution` and `fn-specify-against-existing` (four missing
    sections each); 1 in `features/fn-931` (a bullet "is a telegraphic label").
  - Warnings: 249 "no '## Agent intent (ICE)' yet — its spine entry names a business intent, so its agent intent should
    be written (alignment)", on parts whose ICE is on its own page; 13 "no ICE yet"; 1 "no domain yet" (`cap-723`).
- The review of a change has no playbook for model pages: "No installed linter reads the product model, so Layer 1 was a
  by-hand check" (#870, open, under #939).
- *State:* Live, out of step.

### 2.8 Built: find and close the gaps inside the model

- `find-model-gaps` lists loose parts, links to nothing, capabilities with no features, intents nothing serves, links on
  one side only, empty domains and likely duplicates, and says for each the link to make or the play that does the work;
  "Read only" (`find-model-gaps/SKILL.md` lines 27-60, 79). Tests: 7 passed.
- `link-model-gaps` makes what the model can take: attributes loose parts, links both sides, merges agreed duplicates
  (`link-model-gaps/SKILL.md` lines 23-44). Tests: 9 passed.
- Used by the Shared Loop Run after each round, inside the Discovery loop only (both skills' descriptions).
- **Run of the gap finder on the model on 2026-11-11:** 1 loose part (`cap-723`, no domain); 4 intents nothing serves
  (`bi-11`, `bi-5`, `bi-734`, `bi-756`); 21 links on one side only, for example `cap-model-routing` serves `bi-7` in the
  index and `bi-7`'s page does not list it, and `bi-788`'s page lists `cap-orchestrate-agent-work` while the index does
  not name `bi-788`; no duplicates; no links to nothing.
- *State:* Live, inside a loop.

### 2.9 Built in part: list what serves an intent

- The ontology answers it on paper: Q15 "Given a business intent, which ICE do agents work on for it?" and Q25 "Given a
  business intent, which slices serve it?" are answered (lines 71-73, 101-103).
- The data is there: the index's `intents` on each part, and each intent page's Touches list. Ten intent pages of sixteen
  have a Touches list; `bi-11.md` has none.
- Scripts read it inside plays only: /shape-slice's `find_serving_slice.py` and /shape-plan's `gather_plan.py` find the
  slices that serve an intent; the gap finder lists intents nothing serves.
- **No command lists what serves an intent for a person**, and no script searches by domain. The planned views are #726
  (domains for search, under #723) and BI-8's Argus Intents view (#643, a person can read a review: the whole model's
  approval state, each intent with its ICE). #541 (build the Product Graph, under BI-11, "Not approved to build") asks
  "Given a business intent, every agent intent that served it is listable with its cost".
- *State:* Live in part.

### 2.10 Built in part: one way to write the index

- ADR 065 rule 1 wants every play on the two index skills. #1024 (plays change the model's index through the two index
  skills): "Today eight plays write the index with their own scripts: `/discover-domains`, `/discover-capabilities`,
  `/shape-slice`, `/learn-outcomes`, `/shape-measure-lens`, `/build-epic`, `/validate-epic`, `/release-epic`." Three of
  them are live; five are marked stale. "The skills grow what they need: a new slice, the product profile, an epic's
  status."
- *State:* Live in part; Planned only for the move.

### 2.11 Planned only

- #964 (each piece of the model carries its approval state, and agents build only from approved pieces), with #645 (the
  approval state: approved, changed or in progress), #646 (agents build only from approved pieces) and #647 (decide how
  approval is recorded outside the review step). From ADR 033 (accepted): "Approval Is Part of the Product Model, and
  Agents Work Only on Approved Pieces".
- #990 (the product model moves with the work: a design approval updates it, and /propose-change lets the person update
  it now or leave it for Learn): "Leaving it is always allowed, and it leaves a record of what is owed."
- #1030 (a tool that knows how to create and edit the product model): "Today a language model composes the model's
  pages, and they drift from the ontology." "Not decided: What the tool covers, how it is built, what it replaces, and
  when it is built."
- #962 and its stories (the --edit standard, section 2.3).
- #979 (the shared step for a part found during work, section 2.2).
- #1024 (the index through the two skills, section 2.10).
- #723 (link the product model) with #725 and #726 (section 2.5), #805 and #1033 (section 2.6).
- #541 (build the Product Graph), "Not approved to build" (section 2.9).

### 2.12 Neither: ideas and experiments

- No part proposes an idea from the model, and none records an experiment. A search for "experiment" finds no part
  that does either: in `core/components/` only a domain shelf, branch-name rules and word lists; nothing in `docs/adr/`
  or the glossary; in the model only BI-11's own page; and one old design note: "`experiment` — A/B hypothesis framing,
  exposure management, result analysis" (`docs/design/playbook-catalog.md` line 138, "Discovery draft. Not scoped, not
  implemented.", line 3). No open issue has "experiment", "idea" or "hypothesis" in its title.
- The nearest built parts:
  - The ontology writes a business intent's outcome "as a hypothesis (what should be true, why it matters, and how we
    will know it is met)" (line 175), and an intent "is met by its proof" (line 219).
  - The measure lens holds a baseline, a target and a proof for each delivery metric, "Delivery-pipe ONLY ... product
    outcomes are strategy's to measure" (`standards/schemas/product-os/lens/measure.yaml` lines 1-36); its play
    /shape-measure-lens is stale.
  - #541 names one idea the model could show: "A business intent connected to more fix-type agent intents than
    delivery-type ones says we are repairing rather than delivering what the org asked for."
  - #545 (measure intents: outcome on business, speed and autonomy on agent), under BI-6, "Not approved to build", parked
    (`capabilities.md` line 68).
  - BI-6's approved "Build features or update the product model, on its own or at least as recommendations" recommends
    changes from what happens in use (`build-or-update-product/capability.md` lines 3-14).
- *State:* Neither.

## 3. What approved pages hand to these two

About 50 lines on 38 approved pages of other intents name Product model, one of its two capabilities or its Must not (a
search of `.garura/product/product-os/` on 2026-11-11, leaving out the lines that only say ADR 066's rename "runs after
the reviews of BI-10 and BI-11" and the lines that quote `capabilities.md` as a source). These are promises BI-11's
pages must keep. By capability:

### 3.1 To Define what a product is made of

- "What each kind is in the product model, and changing it. Define what a product is made of, in Product model, owns the
  ontology." (`track-execution/fn-say-what-each-type-means/feature.md` line 59).
- "The model's own trace from an epic to its intents, through its slice. Define what a product is made of, in Product
  model, owns the kinds and their links." (`track-execution/fn-link-work-across-trackers/feature.md` line 62).
- "The ICE as a kind of the product model, with its rules, belongs to Define what a product is made of, in Product model;
  this capability holds the ICE of plays and loops." (`standards/capability.md` line 32; the same as an Out at line 98);
  "What a good ICE holds, as a kind of the product model. Define what a product is made of, in Product model, owns it."
  (`standards/fn-build-from-ice/feature.md` line 47); "Out: the ICE kind of the product model. Define what a product is
  made of, in Product model, owns it." (`build-your-own-harness/capability.md` line 82).
- "Out: the shape of the product model itself, which Product model defines. This capability only moves a project's
  model to the shape a version reads." (`upgrade-project/capability.md` line 65); "The model's shape itself and how it is
  versioned. Product model owns it." (`upgrade-project/fn-move-model/feature.md` line 52).
- "What a plan file holds, as the ontology's Plan kind says. Product model owns it." (`features/fn-628/feature.md` line
  57; `features/fn-729/feature.md` line 60).
- "Where the project's architecture sits in the product model. Product model owns the model's kinds."
  (`manage-adrs/fn-take-design-choices/feature.md` line 46).
- "where the setup answers sit in the profile (Product model)" (`initialize/capability.md` line 61); "Not decided: where
  in the product profile the answers sit. Its shape has no place for them today, and Product model defines it."
  (`initialize/fn-project-memory/feature.md` line 35; again at line 57).
- "Out: what the product model holds inside its folder. Product model owns it." (`structure/capability.md` line 66;
  `structure/fn-garura-folder-list/feature.md` line 56).
- "Out: what the product model holds and how it is written. Product model (BI-11) owns it; the model is read here as
  part of Garura memory." (`memory/capability.md` line 85).

### 3.2 To Manage the model

- "Out: the rules for which part links to which, and drift inside the model with no work in it, such as two ICE for one
  part or the same part written twice. ... Manage the model owns them, and also merges capabilities and removes slices."
  (`keep-spec-matched/capability.md` line 51); "Drift inside the model with no work in it, such as two ICE for one part, a
  thin mark kept in one place only, or the same part written twice. Manage the model owns it."
  (`keep-spec-matched/fn-find-spec-drift/feature.md` line 51); "Merging one capability into another, and removing a
  slice. The same tools do them, and Manage the model owns them." (`keep-spec-matched/fn-replace-or-retire-intent/
  feature.md` line 44); "The rules for which kind of part links to which, and links inside the model with no work in
  them. Manage the model owns them." (`keep-spec-matched/fn-keep-intent-links-current/feature.md` line 46).
- "Merging or taking out another part goes to Manage the model." (`build-or-update-product/capability.md` line 29; again
  at line 70, at `fn-start-changes/feature.md` line 11, and in `fn-start-changes/ice.md` line 4).
- "Out: the link rules the step after each round applies to the product model. Manage the model, in Product model, owns
  them." (`run-plays-as-loops/capability.md` line 73; again at `fn-run-plays-side-by-side/feature.md` line 59 and
  `fn-run-loop/feature.md` line 80).
- "Learning a change left for later into the product model. Manage the model, in Product model, owns how the model takes
  in the work (#990)." (`give-every-gate-a-way-past/fn-keep-what-is-owed/feature.md` line 54).
- "The needs links on capabilities and features, and their name in the model's index. Product model owns them: "Needs"
  and "identified by" link capabilities and features (fn-725)." (`orchestrate-agent-work/fn-work-out-waits-on/feature.md`
  line 54).
- "Removing parts of the product model. Product model owns it." (`orchestrate-agent-work/fn-remove-plan/feature.md` line
  56).

### 3.3 To Product model, with no capability named

- **The approval state on each part.** "The approval state kept on each piece of the model, and the rule that agents
  build only from approved pieces, are Product model's (#964)." (`review-agent-work/capability.md` line 36; as an Out at
  line 87, with "how approval is recorded outside the review step"); also `fn-answer-pieces/feature.md` line 53,
  `fn-apply-answers/feature.md` lines 25, 33 and 47, `fn-open-review/feature.md` lines 22 and 48.
- **The Must not, quoted as a reason.** "Only a person confirms a business intent. Product model must not "let an agent
  confirm an intent"." (`review-agent-work/capability.md` line 33; again at line 95).
- **Product decisions.** "Out: product decisions in the product model, such as a move of the product profile, kept as a
  `decision.yaml` record. Product model owns them." (`manage-adrs/capability.md` line 63; also `fn-record-adr/feature.md`
  lines 7 and 67, `fn-keep-adrs-linked/feature.md` line 59, `fn-keep-adrs-to-build/feature.md` line 55).
- **The model's pages and intent pages.** "Writing what moves into the model's pages. Product model owns them." and
  "Changing what a business intent says. Product model owns the intent pages, and the product owner decides each
  change." (`manage-adrs/fn-keep-adrs-to-build/feature.md` lines 53-54). This second line disagrees with BI-1's approved
  Keep the spec matched, which holds "updating an intent or a model part when the implementation changes, only from words
  a person approved" (`keep-spec-matched/capability.md` line 44).
- **Everything about the model, from Orchestration.** "Out: the product model: its kinds, its pages, its index and their
  rules. Product model owns them." (`orchestrate-agent-work/capability.md` line 78); "The kinds of the model, the rules
  of its pages and its index, and the model's checks. Product model owns them." (`orchestrate-agent-work/fn-795/
  feature.md` line 69).

## 4. The old parts, and other parts that belong here

Filed under the closed intent `bi-722` ("A product model can be managed, and grows as plans are built",
`intents/bi-722.md`; #722 closed as not planned). None has a domain (`cap-723` is `domain: ''`), and none has an ICE
page: each keeps its ICE inside its page, so the ready check calls each "not ready" (section 2.6). All four features sit
in the holding folder `features/`.

| Part | What its page says | How far built | Belongs to |
|---|---|---|---|
| `cap-723` (`capabilities/cap-723/capability.md`) | "Link the product model: needs, identified by, and loose domains"; "work can start before the model is complete, if the model links its parts by these rules" (line 5); In: "the link rules above, written once in the ontology", the ready check, "the check that each link points at a part that exists", "search by domain" (lines 15-18) | Built in part: the rules are in the ontology and the ready check is built; the link check and the search are not. #723 open. Its Out names gone capabilities: "Build a plan, View plans, Manage a plan" (line 19) | Manage the model |
| `fn-597` | "Rebuild the product model as an ontology"; "This feature delivered version 5 (2026-10-21)" (line 10); "Domain stays under "Not yet defined" on purpose" (line 22) | Built, now at version 15, where Domain is defined and "Not yet defined" is empty; #597 closed. Its sources name "plan #722" (line 47) | Define what a product is made of |
| `fn-724` | "A capability or feature is ready without a domain": "A missing domain is a warning, never a block" (line 4) | Built: the ready check, four copies; #724 closed. Today it reads 0 ready, 249 partly ready, 13 not ready (section 2.6) | Manage the model |
| `fn-725` | "Needs" and "identified by" link capabilities and features; rename `depends_on` to `needs` "in all the files that use it (53 today)" (line 4); "A feature can need a capability or another feature" (line 21) | Not built: #725 open. Line 21 disagrees with ontology v6 and later (section 1.5) | Manage the model |
| `fn-726` | "Domains link to business intents and capabilities, outside the plan tree": a search by domain, and a check that no domain is in a plan or the tracker (lines 3-10) | Not built: #726 open. "Garura's own model has no domains yet (`domains: []`)" (line 39) is out of date: the index has one domain. Line 77 names "Garura's own plans 717, 722 and 734" | Manage the model |

- **The index entry of `cap-723`** keeps its own quality needs, and they name plans and a check not built: "0 need or
  identified-by links that point at nothing or at work across Garura's own model (plans 717, 722, 734)" and "gate:
  lint_grounding.py --spine on .garura/product/product-os exits 0 once the link check (#725) lands" (`_spine.yaml`
  lines 31-38). The product profile's reliability and maintainability gates read the same checks ("lint_grounding.py
  --spine link check + check_ice_workable.py tests"; "ready-check and linter tests; spine before/after diff on the
  rename", `_spine.yaml` lines 4288 and 4291).
- **It can be merged.** `cap-723` has no ICE entry and its folder holds only its page, so `remove-model-part` can merge
  it (`remove_part.py` lines 193-207 and 227-228). Its features are in the holding folder, so each can be filed under its new
  capability with its page moved (`link-model-part`, `capability` and `doc`, #1037).
- **Other parts.** No part in the index names `bi-11` (a read of `_spine.yaml`: 0 matches). The other old parts are
  someone else's, as `capabilities.md` line 106 leaves them: Build a plan (`cap-718`) with `fn-727`, `fn-728` and
  `fn-818`, and `fn-931`, to BI-1; the hidden eval (`cap-shape-eval`, `fn-798`, `fn-898`) to BI-3; and deleting
  `sl-intent-to-design`.
- **Owed parts with no page.** #1030 (the tool the product owner asked for), and every planned item of sections 1.7 and
  2.11: no page in the model names #964, #990, #962, #979, #1024 or #541 as a feature of BI-11.
- **The old intent pages, as information only.**

| Page | Title | Tracker | Still named by |
|---|---|---|---|
| `bi-717` | People plan work toward a business intent, and pick it up across days and people | #717 closed as completed | The index: the domain, `cap-718`, `fn-727`, `fn-728`; `intents/bi-788.md` |
| `bi-722` | A product model can be managed, and grows as plans are built | #722 closed as not planned | The index: `cap-723`, `fn-597`, `fn-724`, `fn-725`, `fn-726`; the pages `cap-723` and `fn-724` |
| `bi-734` | Garura publishes a standard for building agentic harnesses | #734 closed as not planned | `standards/capability.md` line 6, as history only |
| `bi-756` | The agent intent (ICE) is its own part of the product model | #756 closed as not planned | Nothing. Its page still says "One ICE exists for each pair of business intent and capability or feature" (line 12), which its own tracker issue and ontology v6 replaced |
| `bi-788` | Agents design a named piece of work | #788 closed as not planned | The index: the domain, `cap-718`, `cap-shape-eval`, `fn-818`, `fn-798`, `fn-898`, the slice `sl-intent-to-design` and its record; six pages |

  Four of them carry a "**Plan:**" line that names their plan file (`bi-717.md` line 13, `bi-722.md` line 15,
  `bi-734.md` line 15, `bi-756.md` line 20).
- **The tracker.** BI-11's sub-issues (garura-intents#11): #723, #964, #979, #761, #764, #962, #990, #541, #1024 and
  #1030 open; #757 closed. Under them: #724 and #597 closed, #725, #726 and #694 open (under #723); #645, #646 and #647
  open (under #964); #762, #763 and #1033 open, #1031 and #1037 closed (under #761); #765 open (under #764); #901, #905,
  #906, #907 and #910 open, #908 closed (under #962).

## 5. Gates with no way past, in the built parts of the two

BI-9's Must not: "Stop a person. Every gate has a way past it that records what's owed." BI-11's own: "Block work because
the model is incomplete".

| Gate | Where | Way past today | What is recorded |
|---|---|---|---|
| The three checkpoints of /edit-ontology | Define: "**pinned** — the product owner decides, C2; never skipped by config" (`edit-ontology/SKILL.md` lines 147-148, 168, 181-182) | None. The person types yes or a change; a change sends the stage back | Each answer word for word, with the sha256 of the draft shown (`decisions.json`) |
| The ontology check and the change check | Define: "The run ends only when the ontology check passes" (C5); scope, version and names (Step 8) | Fix each problem and run again (REC5) | The check reports |
| A dirty ontology file at the start | Define: pre-flight, "Hard halt (REC1)" (`edit-ontology/SKILL.md` line 65) | Commit or put away the edit first | — |
| Changing the ontology in a product project | Define: "never into a product project" (`author-product-ontology/SKILL.md` line 15; `install.py` lines 210-218) | None in that project; a harness repository can | — |
| A part's ICE inside its page, once the index has ICE entries | Manage: the ready check calls the 13 older parts "not ready: has no ICE"; /shape-plan skips them (#1033) | None until each ICE gets its own page (#765) or each part is read by its own shape (#1033) | /shape-plan names each skipped feature |
| The model check of /shape-slice | Manage: "the run does not go on until it reads valid" (`shape-slice/SKILL.md` line 608) | A fix loop; #1033 reports 7 "thin mark drift" problems on the slice that serves `bi-788` that "the fix loop cannot clear" (not re-run here) | — |
| Removing a feature, a domain or an ICE | Manage: `REMOVABLE = ("intent", "capability", "slice")` (`remove_part.py` line 78) | None: "When no skill covers a change, say so and stop" (`product-os-keeper.md` lines 183-184) | The keeper's failure names the missing skill |
| Merging a capability that has its own ICE page | Manage: "cannot be merged here" (`remove_part.py` lines 227-228); 38 of 41 capabilities | None | — |
| A removal with no approver's name, or a page that still names the part | Manage: refused (`remove-model-part/SKILL.md` lines 74-77) | Name the person; fix each named line through the page skill first | The refusal names each path and line |
| A page move while a page names the old path | Manage: refused (`link-model-part/SKILL.md` lines 78-81) | Fix those lines first | — |
| A model in an older shape | Manage: every script that reads the model stops on the old names (`model_names.py`, 22 copies); "naming a path no project has" (`upgrade-project/fn-move-model/feature.md` line 20) | Run the move script from a copy of Garura's source (the same page, line 19) | The message names the key and the script |
| A new intent page where one exists | /discover-intent refuses "an intent page already exists" (`persist_intent.py` lines 22-29) | `author-intent-page` with `rewrite`, through the keeper, outside the play; the play's own --edit is planned (#901) | — |
| An agent confirming an intent | The ontology: "only a person confirms or drops a business intent" (line 25), BI-11's own Must not | None, on purpose. `author-intent-page` refuses `confirmed` with nobody named, but takes any name it is given (`write_page.py` lines 111-116); no fingerprint or record of the person's reply is checked (#645 plans one) | The name the caller gives |

- So the stops with no way past in BI-11's built parts are: the pinned checkpoints of /edit-ontology (whether a pinned
  yes is a key or a stop kept on purpose is BI-9's open question, #992, every gate has a key), changing the ontology in
  a product project, removing a feature, a domain or an ICE, merging a capability that has its own ICE page, and the 13
  older parts the ready check stops. The last one also breaks BI-11's own Must not: work is blocked because the model is
  in a half-moved shape.

## 6. What is new: not built and planned in no issue

Each would need outside research before it is drafted, except where marked.

1. **The model proposes an idea with its evidence, a person confirms it, and an experiment records the result** (the
   fourth proof line). No kind for an idea or an experiment, no part and no issue (section 2.12). Research needed: how
   hypothesis-driven product work writes an idea and its evidence, how an experiment is recorded (what is tried, for how
   long, against which measure, and the result), how product tools link an experiment to the outcome it tests, and what
   a product model itself can show as an idea (an intent nothing serves, a part with only fix work, a thin part never
   deepened).
2. **A command that lists what serves an intent, for a person.** The data is in the index and on the intent pages; only
   plays read it (section 2.9). #726 plans the search by domain and #541 a graph that is not approved to build; neither
   is a plain list from an intent. Mechanical; no research needed.
3. **Removing a feature, a domain or an ICE, and merging a capability that has its own ICE page** (section 2.4). #1024
   names what the skills must grow ("a new slice, the product profile, an epic's status"), not these. Mechanical; no
   research needed.
4. **Showing what an ontology change breaks in the model, before it lands** (section 1.6). Mechanical in part (run the
   structure check before and after). Light research on how teams that keep a formal schema or ontology test the data
   written against it when the schema changes.
5. **A recorded version of the model's shape**, so an upgrade knows which moves a model needs (section 1.5, BI-7's
   hand-off). Mechanical; light research on how data stores record their schema version.
6. **The product profile and the product decision as kinds of the ontology** (section 1.5). An ontology change through
   /edit-ontology; no outside research needed.
7. **A way for a team's project to change or extend the ontology** (section 1.2). Needed only if the product owner wants
   it (question 2). Research on how tools with a shared base model let a team add its own kinds without breaking the
   base.
8. **Writing a need or an identified-by link, or a new domain, on a part that exists** (section 2.3). #725 plans the
   rename and the check, and says any play may write the links; no skill writes them on a part that exists.
   Mechanical; no research needed.

## 7. Where BI-11's parts touch other intents

- **Product → Spec (BI-1).** Specify the product writes the model's first pages, through the discovery plays and their
  writers (`author-domains`, `enrich-capability-ice`), which still write the ICE inside the page (#762). Keep the spec
  matched keeps each intent's links current on both sides, updates words from approved text, and replaces or retires
  intents with `remove-model-part`; it hands "the rules for which part links to which", merges and slice removal to
  Manage the model (section 3.2). Add a feature found during work, in Turn intents into agent work, uses the page skill
  and `link-model-part`. The rebuild eval is Specify the product's check (`specify-product/ice.md` line 21).
- **Validation → Run (BI-5, parked).** Its agreed line "Evaluate the product model: The model is tested too, not just
  the code." (`capabilities.md` line 50) is unplaced. BI-5's stock-take weighed moving it here, "under Manage the model,
  with the structural checks, the judge and the ready check", and leaned to BI-1 (`bi-5-inventory/inventory.md` lines
  485-497).
- **Run → Product (BI-6).** Build features or update the product model recommends changes from what happens in use, and
  hands "Merging or taking out another part" to Manage the model (section 3.2). BI-11's "source of new ideas and
  experiments" sits next to it; measuring each intent (#545) is parked under BI-6.
- **Install and distribute (BI-7).** Move the product model to the new version's shape needs the model's shape and its
  version, which Product model owns (section 3.1); Initialize needs a place in the profile for its answers.
- **Developer tooling (BI-8).** Argus shows and answers each model piece; the approval state it writes is Product model's
  (#964, section 3.3). #870 (a review playbook for model pages) sits under #939 there.
- **Orchestration (BI-9).** Work out the plans a plan waits on reads the needs links (fn-725); the loops' gap-closing step
  applies Manage the model's link rules; ADRs record decisions on how the project is built, and product decisions stay
  in the model (section 3.3; #1022, review every ADR, under BI-9). ADR 065 rule 3, "The product model never names a
  plan", is BI-11's Must not.
- **Standards, structure, settings and memory (BI-10).** Standards holds the ICE of plays and loops; the ICE kind is
  Define's. Memory keeps Phoenix memory in step, which is how the ontology reaches projects (#868 under #921). Structure
  gives "what the product model holds inside its folder" to Product model. The ADR 066 rename runs after the reviews of
  BI-10 and BI-11 (`capabilities.md` line 118).

## 8. Leans

Each is a proposal with its evidence, not a decision.

### Lean 1: the two lines

1. **Define what a product is made of** — keep the product owner's words: "People and agents share one agreed map of what
   a product is made of, changed only on purpose." They fit what is built: the map is the ontology, every project reads
   the same version from Phoenix memory, and "on purpose" is one play with the product owner's typed yes. The page makes
   plain that the map also covers the shape of the model (its version, the profile and the decisions) and that it is
   Garura's own until question 2 is answered.
2. **Manage the model** — reword lightly, keeping his words, to name the change the proof asks for: "A living map, added
   to, changed and pruned as work is done, and the source of what to try next. (unique)". The basis: the proof "Any part
   can be added, changed or removed." "Pruned" already covers removed. Where ideas and experiments sit is question 1.

### Lean 2: the features of Define what a product is made of, from the evidence only

1. Write down what a product is made of: the kinds, what each holds, how they link, the rules, a real example of each,
   and the questions it must answer. Built (version 15; 13 kinds; 47 questions, Q3 partly, Q4 not yet). From `fn-597`.
2. Change the map through one play, one need at a time, with the product owner's yes at three points, checked by a
   script and landed through the change plays. Built, in harness repositories only.
3. Bring the current map to every project. Built (Phoenix memory holds version 15, the same as the source); kept in step
   by Memory in BI-10 (#868, #921).
4. Keep every part that reads the map in step with it: the page templates, the index's schema, the structure check, the
   ready check, the discovery writers and the glossary. Built, out of step (section 1.4); planned in part (#694, #725,
   #761 with #762 and #1033, #765).
5. Show what a change to the map breaks in the model, before it lands, as findings to fix later, never a stop. Neither
   (the first proof line).
6. Say which shape a model is in, so an upgrade knows what to move. Neither (BI-7's hand-off).
7. Define the product profile and the product decision as kinds, with where a setup answer sits in the profile. Neither
   (hand-offs from BI-7 and BI-9).
8. Define the approval state each kind carries. Planned (#645, under #964; ADR 033).

### Lean 3: the features of Manage the model, from the evidence only

1. Add a part found during work: its page and its index entry, thin when thin, inside the change already open. Built in
   part (the skills; the shared play step is #979).
2. Change a part from words a person approved: named lines, a whole page, an intent page, its one-line, intents and
   issue, its thin mark, its capability or its folder. Built; not built: a capability's domain once set, its needs and
   identified-by after it is made, an ICE's thin mark. Planned: the --edit option in each play that owns a record (#962
   with #901, #905, #906, #907 and #910).
3. Take a part out on a person's named approval: repoint parts from an old intent, remove an intent page, merge a
   capability, remove a slice. Built in part; no removal of a feature, a domain or an ICE, and no merge of a capability
   that has its own ICE page (section 6, item 3).
4. Link the parts by the map's rules: what each part serves, on both sides; what it needs; what led us to find it; the
   domain it sits in. Built in part (both sides of "serves", with 21 one-way links today); planned (#725). From
   `cap-723`, `fn-725` and `fn-726`.
5. Say whether work can start on each part: ready, partly ready or not ready, with the gaps. Built; out of step (0
   ready today; #805, #1033). From `fn-724`.
6. Check the model's structure and links on every change, as findings, never a stop. Built, out of step (21 errors, 249
   warnings for a section the map moved); planned in part (#870).
7. Find and close the gaps inside the model: loose parts, duplicates, one-way links, two ICE for one part, missing work.
   Built, inside a loop only (`find-model-gaps`, `link-model-gaps`).
8. List what serves an intent, and what sits in a domain. Built in part (the data; no command); planned in part (#726,
   and #541 not approved to build). From `fn-726`.
9. Keep each part's approval state, so agents build only from approved parts. Planned (#964 with #645, #646 and #647).
10. Move the model with the work: a design approval updates it, and a change left for later is listed for Learn. Planned
    (#990).
11. Change the index only through the two index skills. Built in part (three live plays still write it, #1024).
12. A tool that knows how to create and edit the product model. Planned, not approved to build (#1030), the product
    owner's own feature for this capability.
13. Propose what to try next from the model, with its evidence, and record each experiment's result. Neither; research
    needed (section 6, item 1). Its place is question 1.

### Lean 4: the old parts

- **Merge `cap-723` into Manage the model** once its page is written, with `bi-722` repointed to `bi-11` on each part,
  as the work order of #1021 says ("Link the product model (cap-723) and its features to BI-11", `capabilities.md` line
  106). Before the merge, file `fn-597` under Define what a product is made of, and `fn-724`, `fn-725` and `fn-726`
  under Manage the model, each with its page moved out of the holding folder (`link-model-part`, #1037).
- **Keep the four ids**, since each names its own tracker issue (#597, #724, #725, #726). Rewrite each page to what was
  built and to version 15: `fn-597` to the ontology as it is now (Lean 2, feature 1), `fn-724` to the three-answer ready
  check with today's answers, `fn-725` to the needs and identified-by rules of version 15 (capabilities only, unless
  question 5 says otherwise), `fn-726` to the domains the model has. Each gets its ICE on its own page; that also clears
  5 of the 13 parts the ready check stops.
- **Take out the words that name a plan**, by BI-11's own Must not and ADR 065 rule 3: `_spine.yaml` lines 35 (`cap-723`'s
  quality need), `features/fn-597/feature.md` line 47 and `features/fn-726/feature.md` line 77. `cap-723`'s quality
  needs are listed for review by the merge (`needs_to_review`), and the profile's two gates that name the link check and the
  rename, neither built (lines 4288 and 4291), are reviewed with them.
- **Delete `intents/bi-722.md` and `intents/bi-756.md`** once nothing names them, with the other old intent pages (the
  work order of #1021). `bi-756` is named by nothing today.

### Lean 5: the domain

Software delivery planning, with its opening widened to say it also keeps one living map of the product: what a product
is made of, and the model that grows and is pruned as work is done, as for BI-6 to BI-10
(`software-delivery-planning/domain.md` line 4). The fit is better than BI-10's: the domain "turns a business intent
into working code", and every play that does it reads the model. The other choice is a domain of its own for the
product model, with no shelf to ground it: "No domain shelf holds the product model of a framework itself"
(`capabilities/cap-723/capability.md` line 45).

### Lean 6: the tracker follows the model

- Keep #962 (the --edit standard) under BI-11, for Manage the model, feature 2.
- Keep #761 and #764 under BI-11, for Define what a product is made of, feature 4. #765 has 13 parts left, all old parts
  that the #1021 clean-up rewrites; it closes when they have their ICE pages.
- Rewrite #694 to today's names (it names /vision, /understand and functionalities), or fold it into #761.
- Leave #868 under BI-10's #921: its ontology part holds today.
- Keep #541 under BI-11 as the long-run design of Manage the model, features 8 and 13, still not approved to build.

### Lean 7: found and not filed, to file when the product owner says so

- The model fails its own structure check: 21 errors (section 2.7).
- The structure check asks for an ICE section inside 249 pages whose ICE is on its own page; the page templates still put
  the ICE inside the page, and there is no ICE page template (section 1.4).
- The glossary says a capability "carries ICE", and the ICE is "attached" and "built from a confirmed business intent"
  (lines 61-68), against version 15.
- The ontology says an empty "identified by" means found on its own and also counts a missing one as a gap, so no part
  reads ready (section 1.5).
- Six features need a feature in the index, against the ontology; `fn-725` says they may (section 1.5).
- The ontology says "identified by" may name more than one; the index's schema holds one (section 1.5).
- `remove-model-part` cannot merge a capability that has its own ICE page, and no skill removes a feature, a domain or
  an ICE (section 2.4).
- /edit-ontology runs none of the model's checks (section 1.6).
- `author-product-ontology` defaults to the machine-wide copy of memory in the home folder (`SKILL.md` lines 34-35).
- Seven places in the index and on part pages still name a plan, besides the "Plan:" lines of four old intent
  pages (section 4): `_spine.yaml` lines 35 and 1213, `fn-597` line 47, `fn-726` line 77,
  `fn-798` line 48, `fn-818` line 60 and `fn-931` line 33 (a search of the model).
- `author-intent-page` writes "confirmed" for any name it is given; nothing checks that the person replied (section 5).
- 21 intent links are kept on one side only; the index skills and /discover-capabilities write no Touches line
  (section 2.8; `keep-spec-matched/capability.md` line 28, BI-1's).

## 9. Questions only the product owner can answer

Each has our proposed answer and its basis.

1. **Where do ideas and experiments sit: a feature of Manage the model, as your line puts it ("the source of what to
   try next"), or a capability of its own? And where does it end against Run → Product (BI-6), which already recommends
   changes from what happens in use?**
   - Proposed: one feature of Manage the model, as your line says. It proposes ideas from what the model itself shows (an
     intent nothing serves, a part with only fix work and no delivery, a thin part never deepened), each with its
     evidence; a person confirms or drops each idea; an experiment is then recorded with what is tried, the measure and
     the result. Ideas from use and the market stay BI-6's. The idea and the experiment become kinds of the ontology
     through /edit-ontology, after outside research.
   - Basis: `capabilities.md` line 123 ("and the source of what to try next"); the fourth proof line ("The model proposes
     an idea with its evidence"); BI-6's approved page works "from the findings the second capability of Run → Product
     hands on" (`build-or-update-product/capability.md` line 4); #541's example of an idea the model can show ("more
     fix-type agent intents than delivery-type ones"); nothing is built or planned (section 2.12).
   - Examples: a shop's model shows its checkout capability got three bug fixes and no new feature in a quarter, so it
     proposes "rework the guest checkout", and an experiment runs it for a month against the share of shoppers who
     leave; a clinic's model shows the intent "patients cancel online" with no capability serving it, so it proposes a
     cancel feature; a bank's model shows the credit decision's ICE has been thin for two months, so it proposes
     deepening it before the next plan.
2. **Is the ontology Garura's alone, or may a team's project change or extend it with kinds of its own?**
   - Proposed: Garura's alone for now. Every project reads the same version from Phoenix memory, /edit-ontology stays a
     harness play, and a team that needs a new kind asks for it as a change to Garura. A team's own kinds come later, only
     if a team asks.
   - Basis: "It is installed only in a harness repo, never into a product project." (`author-product-ontology/SKILL.md`
     line 15); `install.py` lines 210-218; every play and check reads one ontology (section 1.3); your line "People and
     agents share one agreed map".
   - Examples: a games studio wants a "Level" kind beside Feature and asks Garura for it; a hospital keeps Garura's kinds
     and adds clinical rules only on its pages; an agency running five client products wants every product on the same
     map so its people move between them.
3. **Your first proof says the model "still passes its checks" after an ontology change. Today the model fails them (21
   errors), and the check still asks for an ICE section the ontology moved. Should /edit-ontology run the model's
   checks before and after the change and show each new finding at its last checkpoint, as findings to fix later and
   never a stop, with the check first brought in step with version 15?**
   - Proposed: yes, in that order: first the structure check, the templates and the index's schema follow version 15,
     and the 21 errors are fixed; then /edit-ontology shows what each change breaks, and the findings are recorded as
     owed.
   - Basis: `intents/bi-11.md` line 10; /edit-ontology changes "only the kinds that need touches" (C1) and checks only
     the ontology (section 1.6); "missing links are warnings to fix later, not stops" (harness standard lines 70-72);
     BI-11's Must not, "Block work because the model is incomplete".
   - Examples: a shop renames a kind and sees every page and key that must move before the change lands; a bank adds a
     "Regulation" kind and sees that 12 capabilities now lack a link to it, recorded as owed; a news site changes the
     ICE's Context lines and sees which 30 ICE pages read the old way.
4. **Is a part "found on its own" a gap? The ontology says an empty "identified by" means found on its own, and also
   that a missing one is a gap, so today no part in the model reads ready.**
   - Proposed: no. An empty "identified by" means found on its own and is not a gap; the Capability rule changes through
     /edit-ontology, and the ready check follows.
   - Basis: ontology line 345 against line 369; the ready check's run (0 ready; 257 parts with "has no identified by");
     `features/fn-725/feature.md` line 23 ("This is normal and gives no warning").
   - Examples: a shop's first capability, Checkout, was found on its own and should be ready on its first day; a clinic's
     Reminders capability was found while building Booking and names it; a school's Timetable was asked for directly and
     names nothing.
5. **Can a feature need another feature? The ontology says only capabilities need each other, but the index holds six
   feature needs, BI-10 kept one for BI-7, and `fn-725`'s page says features may.**
   - Proposed: keep the ontology's rule. Needs link capabilities only. The four needs inside Standards (`fn-743` to
     `fn-746` on `fn-741`) are order of work inside one capability, which the plan keeps; BI-7's `fn-748` on `fn-741`
     becomes "Upgrade a project needs Standards"; and `fn-727` on `fn-724` goes with the clean-up of `cap-718`.
   - Basis: ontology lines 364, 409 and 412; #756's record of the 2026-10-22 decision ("'needs' between capabilities
     only"); Orchestration's open point (`fn-work-out-waits-on/feature.md` line 42); `capabilities.md` line 117.
   - Examples: a shop's "Refund to card" needs the Payments capability, not one payment feature; a clinic's "Video visit"
     needs the Calendar capability; a bank orders "Upload documents" before "Score the application" inside one plan,
     without a need in the model.
6. **Which capability holds the model's checks (the structure check, the ready check and the gap finder): Manage the
   model, or "Evaluate the product model", BI-5's line, which is parked?**
   - Proposed: Manage the model holds them (Lean 3, features 5 to 7). The rebuild eval stays with Specify the product
     (BI-1), whose approved ICE already names it, and the page judge stays in the plays that write pages.
   - Basis: your first proof line; BI-5's stock-take, disagreement 2 (`bi-5-inventory/inventory.md` lines 485-497);
     `specify-product/ice.md` line 21; Orchestration's page hands "the model's checks" to Product model
     (`fn-795/feature.md` line 69).
   - Examples: a shop's structure check runs on every change that touches its model; a clinic runs its gap finder after
     each discovery round; a bank runs a rebuild test only when its specification is first written.
7. **When a person changes a part that exists in their own words (#962, `--edit`), is that Manage the model's, or Keep
   the spec matched's in BI-1? One approved page also gives "Changing what a business intent says" to Product model.**
   - Proposed: the --edit standard and its shared check are Manage the model's (any part can be changed), and each play
     that owns a record carries it. Keep the spec matched stays the owner of drift from what was built. The ADR page's
     line is reworded at BI-11's close to point at both.
   - Basis: #962 is filed under BI-11; `manage-adrs/fn-keep-adrs-to-build/feature.md` line 54; `keep-spec-matched/
     capability.md` line 44 ("In: updating an intent or a model part when the implementation changes, only from words a
     person approved"); the second proof line.
   - Examples: a product owner rewords a shop's checkout intent after a talk with sales (an edit); a clinic's developer
     finds that booking now sends a text as well as an email, and the page is brought up to it (drift); a bank's technical lead
     moves a feature to another capability (an edit).
8. **Should the product profile and the product decision become kinds of the ontology? The model holds both, approved
   pages give both to Product model, and the ontology defines neither.**
   - Proposed: yes, one need each through /edit-ontology, with a place in the profile for Initialize's setup answers.
   - Basis: the index's `profile` block and the `decisions/` folder (section 1.5); `initialize/fn-project-memory/
     feature.md` line 35; `manage-adrs/capability.md` line 63; the keeper names "the profile" among what it may
     change through a skill (`product-os-keeper.md` line 176).
   - Examples: a shop's profile sets security high for payments, and the decision that raised it is kept; a clinic records
     its health-data compliance in the profile; an internal tool keeps a low profile and no decisions.
