# Set a project up after the install (Initialize): research and redrafts (issue 1021, BI-7 capability 4)

Draft only. Nothing under `.garura/product/`, `.garura/core/` or `.claude/`, on GitHub or in git changed. The redrafts are in `.garura/project/issues/1021/context/bi-7-capability-4/drafts/product-os/software-delivery-planning/initialize/`: the capability page and its ICE page, and the six feature pages, each with its ICE page, in the folders they have in the model. The line-by-line changes are in `bi-7-capability-4/changes.md`.

In one line: Initialize is designed and not built. No front door runs it, no tool writes a project's own memory, the product profile has no place for its answers, the review has no list of rule groups to skip, and the tracker adapter cannot list or make an issue type. The six pages written on 2026-10-25 still describe the right jobs; what no longer holds is around them: it was called a play, it named a Phoenix install that is not built, it defined the product profile differently from every approved page, it assumed one tracker, it named a plan, and 35 of its rules were labelled "our default".

What this run did besides reading:
- It read the seven pages in the model, their spine entries (`_spine.yaml` lines 175-211 and 929-979) and the decision `dec-cap-initialize-security-none-medium`; BI-7's page and the three approved capabilities of Install and distribute; `capabilities.md` lines 71-84; the stock-take, sections 2, 5, 8, 10 and lean 3; ADR 038 (whole), ADR 039 Decision 4 and its "Not decided here", ADR 048 Decision 1, ADR 056, ADR 059 line 40, ADR 066 §5 and its amendment line; the install play's guide (`core/components/plays/install-garura/SKILL.md` lines 90-102), the one-line command's last lines (`installer/install.sh` lines 375-392), the memory tool (`memory.py`, `pull.py`, `GUIDE.md`, `contract/v5.json`), the settings source (`core/config.yaml` lines 1-24) and its commit db63ea98, the tracker adapter (`platform-adapter/SKILL.md` and its GitHub and GitLab verbs), the rule for asking a person (`core/components/skills/_shared/asking-a-person.md`), and every approved page of another intent that names Initialize (listed below).
- It read GitHub, read only: #862, #881, #883 (open), #860, #875, #882 (closed), #946 (open), PR #886 and its two review verdicts, #862's parent and sub-issues, and the issue types of Garura's own GitHub organization.
- It searched memory through the memory tool (`--issue 1021`): every tier for initialize (Phoenix memory: no hit; Garura memory: only the product model's own pages), Phoenix memory for rule groups, issue types, stand-ins, onboarding, project set-up and setup questions, and for the review's rules and the product profile. No tier holds a standard or a knowledge page on setting a project up for a harness. What it found and used:
  - The review's rules are one table, "Deterministic mapping from KB quality standard IDs to PR severity buckets P1–P4." (Phoenix memory `standards/rules/pr.md` line 3). Its ids start with SEC, ARCH, BE, CODE, TEST, DOC, FE, OPS, PERF, DATA and DEBT (lines 104-348); none is called a rule group, and permissions and personal data are not families of their own (permission rules are SEC-14 and SEC-18).
  - The product profile is "THE BOX — the product's committed boundaries" (Phoenix memory `standards/schemas/product-os/product-profile.yaml` line 3): a shape, a level and a gate per quality dimension, and compliance. It has no field for setup answers; its `shape.surfaces` overlaps the surfaces question (line 26).
  - The ontology says how each kind is marked in the tracker: "In the tracker, an Epic is an issue of type Epic and a Story an issue of type Story, each with no label." (Phoenix memory `standards/schemas/product-os/ontology.md` line 21).
  - The GitLab adapter's note: "GitLab's issue types and work-item hierarchy have not been mapped or tested here" (Phoenix memory `tools/gitlab/adapter.md` line 74). So GitLab has types the adapter does not reach; the pages say the adapter's GitLab entry sets none, not that GitLab has none.
- It copied the memory files it decided from into `bi-7-capability-4/memory/`, with `manifest.json`, all from Phoenix memory: the grounding content standard, the capability and feature templates, the ICE schema, the product profile schema, the ontology, the review's rule table, the review shelf's index and the GitLab adapter note.
- It did no web research, so no memory update is drafted. Every line rests on what is built, the product owner's words, an issue, an ADR or an approved page.
- It recorded no decision trace with `memory.py cite`, because that tool writes outside this run's folder.
- The pages were written by hand in short-term memory, as on the earlier runs: no skill drafts pages of the approved shape outside the live model.

## The name

*Set a project up after the install (Initialize)*: the product owner's name on the list he set on 2026-11-10 (`capabilities.md` line 79), and the name BI-7's three approved capabilities already use for it. The folder stays `initialize/` and the id stays `cap-initialize`, as decided. The old title, "Initialize a project for Garura", is still named by one approved page of another intent (below).

Words the pages use, and why:
- **Initialize**: the capability's short name, with a capital, as on the approved pages. Lines kept from the old pages keep their lower-case "initialize".
- **Engine thing**: ADR 066 §5's words, read as one run of the same install engine behind the install's two front doors, as decided. The pages name the difference with a play (a command a person types that runs sub-agents and skills) and leave how it is started not decided.
- **Product profile**: the approved pages' meaning, "the record of the product's shape and the quality levels it commits to". The old pages called it "the project's record of its setup answers", which no approved page and no schema says.
- **Memory block**, **part**, **selection**, **rule group**, **mapping**, **stand-in**, **brief**: kept from the old pages.

## What is built, and what is only planned

Built around Initialize, not Initialize itself:
- **Nothing runs it.** The install play's guide: "A play run after the install, `initialize` (not built yet), will set up the project's own memory." (`install-garura/SKILL.md` lines 96-98). The memory guide every agent reads: "A new project starts with no memory of its own. A play run after the install, `initialize`, will set it up from Phoenix memory; it is not built yet. Until then, lookups go up to Phoenix memory." (`core/tools/memory/GUIDE.md` lines 22-24). ADR 059: "the `initialize` play is not built" (line 40).
- **The one-line command says "initialized".** It ends with "Garura $INSTALLED_VERSION initialized successfully!" (`installer/install.sh` line 384), though nothing has set the project up. Found and not filed. A team reading it could think the set-up is done.
- **No tool writes Garura memory.** "the tool has no command that writes Garura or Phoenix memory" (`core/tools/memory/contract/v5.json` line 1359). This repository has no Garura memory folder of its own besides the product model (`.garura/core/` holds no `memory/`).
- **Phoenix memory arrives by download.** "When the place is empty, the first command that needs Phoenix memory downloads it there from its source (download)." (`core/tools/memory/pull.py` lines 11-12). The Phoenix install of #883 ("once per machine") is not built. A failed reach is refused with `tier_missing` (`memory.py` lines 172-177), and the guide says "`tier_missing` means a tier cannot be reached. Say so." (`GUIDE.md` line 41).
- **The pieces a change check would use exist.** Phoenix memory is "read only at its approved version" (`memory.py` line 26); every `read` answer carries a fingerprint; and "`citations --check` names every decision whose source no longer says what it said" (`GUIDE.md` lines 78-79).
- **The review runs every group.** "It runs every rule group, a set of the review's rules that check one kind of thing, such as a database, on every project." (`check-code-against-standards/capability.md` line 24, approved, BI-4). The rule table has id families, not named groups (memory, above).
- **The tracker adapter.** 25 verbs; `create-issue-typed` and `set-issue-type` on GitHub only (`platform-adapter/SKILL.md` lines 54-55). On GitHub "An `issue_type` the repository does not have stops with exit 1, and nothing is made." (`reference/github/verbs.md` line 236). On GitLab "Not on GitLab: GitLab has no issue types here." (`reference/gitlab/verbs.md` line 234). No verb lists a tracker's types or makes one. No Jira or Linear entry.
- **Two trackers in the settings.** Since 2026-11-02 (commit db63ea98, in #1021) the settings name `trackers.intents` ("business intents") and `trackers.work` ("agent work: epics, stories, bugs, chores, spikes"), and "Tools read this; plays, skills and sub-agents never name a tracker." (`core/config.yaml` lines 14-23). The old fn-881 page assumes one tracker.
- **Garura's own organization has the types, by hand.** Read on 2026-11-10: Story, Bug, Feature, Business Intent, Chore, Spike and Epic, each with a description. #881: "the organization `intent-driven-ai` got the Epic type by hand on 2026-10-25."
- **The profile's security level was raised for Initialize.** `dec-cap-initialize-security-none-medium` (accepted 2026-10-25) set the profile's security to medium with the gate "no tracker or mapping write before the typed yes, on a test GitHub organization; no write to Phoenix memory or another project's memory". Kept; nothing in the redraft changes it.

Planned only (open issues): #862 (the set-up, under Install and distribute's tracker issue, with #881 and #883 under it), #881 (tracker types), #883 (Phoenix memory in three steps; its first step is Memory's), #868 (source memory reaches the Phoenix memory repository), #946 (one folder for every settings file but `config.yaml`; Settings').

Left open when the capability was first recorded (PR #886, round 1): "PM-4 (no committed home yet for the setup-answer records)". Still open.

## What no longer holds on each page

Capability page (`initialize/capability.md`):
- Line 1, the title "Initialize a project for Garura": BI-7's list names it "Set a project up after the install (Initialize)". Retitled.
- Line 7, "One play, `initialize`, asks the setup questions": ADR 066 §5, "Initialize, seeding memory and upgrade are engine things, not plays.", and ADR 038's own status line, "initialize is an engine thing, not a play". Now "One run of Initialize"; the page names the difference with #862's "one play".
- Line 4, "Today a project gets all of the memory": #862's "Today an install copies all of the memory" no longer holds for a project; ADR 038 made the install bring no memory into it. What holds is that every lookup goes up to all of Phoenix memory. Reworded.
- Line 16, "The product profile is the project's record of its setup answers": every approved page that defines it says "the record of the product's shape and the quality levels it commits to", and the schema has no place for answers. Redefined; #862's wish that the profile records the answers is kept, and where is not decided.
- Line 20, "The Phoenix install owns it: it runs once per machine and lays Phoenix memory": not built; today the memory tool downloads Phoenix memory on first need, and how it reaches a machine is Memory's (decided). Now Out, to Memory.
- Line 22, "the review play, /check-change, owns it": the approved owner is Check the code against its standards, in Code → Validation (BI-4). Updated.
- Line 23, "/shape-slice and /shape-plan own them" and "a later story of this business intent": the owners are now Turn intents into agent work (BI-1) and Track execution in the team's tracker (Orchestration); "this business intent" meant #862, which is now one issue under BI-7. Now "a later story under #862".
- Line 36, "says the Phoenix install must run on this machine": points to a step that does not exist. Now "says in plain words that Phoenix memory could not be reached".
- Lines 54-68, the ICE section: a part's own page holds no ICE section now; it moves to `ice.md`, with one Goal (the five Goals are joined), and the Checked by line becomes the Done means.
- Missing before, added: it serves Install and distribute (BI-7); BI-7's line that Initialize starts where the install stops; Upgrade a project's hand-off ("running the set-up again when a new version asks something new"); what is not built; the rule that Initialize asks and records and decides nothing that Memory, the review or Track execution owns; no tracker in its own steps (BI-10's Must not); production never touched.

Ask the setup questions (`fn-setup-questions/feature.md`):
- Line 4, the product profile's meaning: as above.
- Line 15, the folder a run with no issue uses ("our default"): a detail of how short-term memory works, Memory's. Dropped.
- Line 22, "Our default; the sources do not say how the questions are shown": the rule for asking a person now says it ("Each question asks one thing.", "several examples from different domains, never just one", and it covers "a brief that ends with questions"). Kept as a rule with that reason.
- Lines 24, 33, 44, 61, the Phoenix install: as on the capability.
- Line 26, "Initialize goes on to the memory, review-rule and tracker features only when every question has an answer": a gate with no way past it, against Orchestration's Must not, "Stop a person. Every gate has a way past it that records what's owed." Now not decided (open point 8).
- Missing before, added: proposals come from the project's own code and memory first, then Garura memory, then Phoenix memory, never from an agent's own knowledge (the product owner's standing rule, and the memory guide's "Never answer from what you already know").

Build the project's memory (`fn-project-memory/feature.md`):
- Line 8, the product profile's meaning: as above.
- Line 28, "How a block is found, and how a project's memory is written from a file, are our default": ADR 039 lists "how `initialize` builds a project's Garura memory from the part it needs" under "Not decided here". Now not decided (open point 3).
- Lines 19, 32, 47, 53, the Phoenix install: as above.
- Line 55, "issue #860 owns it": #860 was closed on 2026-10-25; the out-of-scope line is dropped.
- Line 56, "the business intent puts this after the memory tool is fully live": the memory tool's home and the machine-wide copy are Memory's (ADR 055 §8 keeps the copy for now). Now Out, to Memory.
- Line 69 (Sources), the product owner's words "i agree never take the whole file. read it, and build project's memory." sit only in issue 882's short-term memory, which this run does not decide from. The redraft cites PR #886's public verdict instead: "The product owner's rule: never take the whole file; read it, and build the project's memory."

Choose the review rule groups (`fn-review-rule-groups/feature.md`):
- Line 12, the record "kept in the product profile beside the setup answers ... Our default": where it is kept is open, with the answers (open point 4).
- Line 17, "Which answer decides which group is our default": what each group checks belongs to the review's owners (decided). The six rules stay on the page as examples, because the Deployment design page quotes one of their reasons ("because nothing is deployed or kept running for its rules to check"); the full list is not decided (open point 5).
- Line 37, "the review play, /check-change, owns it": the owner is Check the code against its standards.
- Line 38, "a later story of this business intent ... Our default; the sources ... do not say which story changes the review": BI-4's approved page now says it: "changing the review to read that record is a later story (#862)". The words BI-4 quotes from this line are kept as they were.

Set up the tracker's work-item types (`fn-881/feature.md`):
- Line 14, the six one-line meanings, "our default": what each type means is Track execution's (decided). The list is removed; the brief shows Track execution's words.
- Line 31, the example stand-in "the plain Issue type with a label named after the needed type": ADR 056 says an Epic and a Story are marked by their type, "Neither has a label.", and "An Epic is never filed as type Feature." The example is removed; what a stand-in for an Epic or a Story can be is not decided (open point 6).
- Lines 25, 35, where the mapping and its record are kept, "our default: with the project's settings": the install and the upgrade write Garura's settings file, and Initialize and the install "never write the same files". Not decided (open point 6).
- The one-tracker assumption: the settings now name two trackers. Added: Business Intent is set up in the intents tracker, the five work-item types in the work tracker.
- Lines 55-56, "/shape-plan and the other filing plays own them", "a later story of this business intent ... Our default": owner now Turn intents into agent work; the later story is the one the product owner asked this page to name in PR #886's first review ("the #881 page must name the later story that changes the filing plays"). Kept as Out, with that reason.
- Line 66, ADR 048's second bullet ("The **work layer** is tracker issues labelled `work-item`: Epic, Story, Spike, Chore and Bug.") was amended by ADR 056: only a Spike, a Chore and a Bug keep the label. The quote is dropped; the first bullet is kept.
- Line 77, "found in plan 788 while fixing #875": a page names no plan (Product model's Must not, "name a plan", and the product owner's rule). Removed from the ICE.
- Not built, added: the adapter cannot list or make a type, its GitLab entry sets none, Jira and Linear have no entry.

Run initialize again (`fn-rerun-initialize/feature.md`), now Update the setup as the project changes:
- Line 1, the title: the product owner's rule words a later change as updating "as the project changes". Retitled; id kept.
- Line 46, "Reinstalling Garura (the Garura install owns it)": now Install into a project and Upgrade a project.
- Missing before, added: Upgrade a project hands a new version's new question here; a new question can come from a new Garura version, not only from Phoenix memory.
- Lines 16, 20, 21, 24-28, "Our default" on seven rules: each follows from a sourced rule (the answers are the person's, a yes to one tracker write is not a yes to another, the reliability need for an unchanged run), so each stays as a rule with its reason; where the change record is kept is not decided.

Give each project its own memory blocks (`fn-883/feature.md`), now Update each project's own memory as Phoenix memory changes:
- Line 1, the title: its distinct job is the later update as Phoenix memory changes, worded by the same rule. Retitled; id kept (it is #883's).
- Lines 13, 19, 24, 38, 46, 62, 70, the Phoenix install and "a folder in the person's home folder that the Phoenix install laid": not built; the tool downloads Phoenix memory. Reworded; the step is Memory's.
- Lines 22 and 30, the block list's fingerprint and Phoenix memory version, "our default": how a run tells that a part changed is not decided (open point 7). The need to keep a list, so a later run can find changes, stays: #883 asks that initialize "can run again to take in changes".
- Lines 31-37, "our default" on the yes, the reply per part, and each reply's effect: the yes stays a rule, now with BI-7's Must not as its reason ("Change what a project's people changed without asking them."); a no stays the way past, with Orchestration's Must not; per part or per block is not decided (open point 7); the three effects of a yes are joined into one rule.
- Line 92, "Quality need: an install changes 0 files in any project's Garura memory": the ICE page's shape has no Quality need line. The need is already the spine's reliability target for the capability and a Fails if line of this ICE.

## Pages of other intents that name Initialize

Each was read against the redraft. Every quote they take from Initialize's pages is kept word for word in the redraft, and the check in `checks/quotes.json` covers the redraft side.
- Still hold, with the same words on Initialize's pages: BI-2's `design-technology-architecture/capability.md` (lines 71, 83) and `fn-set-architecture/feature.md` (lines 25, 90-91); `fn-update-architecture/feature.md` (line 74, "A project changes (it gains a database, a web surface or a new tracker)"); `manage-surfaces/capability.md` (lines 26, 102), `fn-declare-surfaces/feature.md` (lines 16, 27, 37, 89) and `fn-update-surfaces/feature.md` (lines 7, 15, 22, 71-72); `environment-setup/capability.md` (line 116), `fn-declare-environments/feature.md` (lines 20, 31, 37, 104) and `fn-update-environments/feature.md` (lines 7, 18, 22, 77); `deployment-design/capability.md` (lines 124-125), `fn-design-how-project-runs/feature.md` (lines 19, 41, 130) and `fn-update-deployment/feature.md` (lines 7, 20, 24, 82). BI-4's `check-code-against-standards/capability.md` (lines 24, 60, 106) and `fn-review-each-change/feature.md` (lines 22, 66, 75). BI-6's `connect-use-and-market/capability.md` (line 84), `fn-connect-tools/feature.md` (lines 18, 40, 65-66), `fn-update-connections/feature.md` (lines 14, 31, 51), `fn-take-in-use/feature.md` (line 59) and `fn-take-in-what-people-say/feature.md` (line 60). BI-4's `test-security` pages quote the decision and the spine's gate, which are unchanged.
- Words kept on Initialize's pages because other pages quote them: "A tracker is an outside system, and a write there is visible to the whole team."; "A project changes (it gains a database, a web surface or a new tracker)"; "Initialize starts where that install stops, so a project has no Garura memory of its own until initialize runs, and the two never write the same files."; "whether there is a database, personal data, permissions or a running service"; "the technology standards, the tools and frameworks"; "the surfaces (web, mobile, command line, API)"; "In: what the project already shows, for the proposed answers: its files and its config."; "Where nothing backs a proposal, the question carries no proposed answer and the person answers it; there is never a default in place of a source"; "A rule group is a set of the review's rules that check one kind of thing"; "a group skipped by mistake hides real findings"; "because nothing is deployed or kept running for its rules to check"; "Changing the review play (/check-change) to read this record, run no rule of a skipped group and name the skipped groups in its own record"; "It reads which tracker the project uses and the issue types that tracker already has"; "when the project changes: it gains a database, a web surface, personal data or a new tracker, or it drops one."
- Would not hold word for word: BI-1's `keep-spec-matched/fn-keep-tracker-matched/feature.md` line 47, "Making the issue types a tracker needs, such as Business Intent. Initialize a project for Garura does it." It names the old title. Its meaning still holds; its name for the capability would be out of date after the retitle.
- Would not hold in one place: `decisions/dec-cap-initialize-security-none-medium.yaml`, `affects`, names "the ICE Limit lines" on `initialize/capability.md`. After the write they sit on `initialize/ice.md`. The decision's meaning and its gate are unchanged.

## The open points: options and a lean

Each is a proposal with its evidence, for the product owner to decide. The pages name each as not decided and carry no lean.

### 1. How a person starts Initialize, since it is an engine thing and not a play
- **Option A, its own run through the install's front doors**, named as the next step at the end of the install's report. Install into a project's approved page already ends the report with "the next step: Initialize, once it is built", and its lean on "one step" was the install alone.
- **Option B, the install ends by offering it**: "set the project up now?"; a no leaves the project installed and not set up.
- **Option C, the first play run in a project with no Garura memory of its own starts it.** No separate step, but a play that stops to ask set-up questions blocks work (Product model must not "Block work because the model is incomplete") and is a gate with no way past it.
- **Lean: A.** It keeps "It lays the pieces and stops." and "the two never write the same files", and matches the approved install report. B can be added later without changing the install's own steps.
- Related, not Initialize's to settle: whether BI-7's "A first install takes one step." counts the set-up. With A, it does not.

### 2. How an engine run reads memory and drafts its proposals
The memory guide says "Only agents call the tool", and a proposal with its source, or memory "written for the project", needs an agent's judgment. An engine is steps and scripts.
- **Option A, the engine hands the reading and drafting to an agent** through the team's coding tool, and does the mechanical steps itself (the install's check already runs the memory tool's `health` command "the way an agent does", `install-garura/SKILL.md` line 100).
- **Option B, the asking and building part is a play after all**, and the engine does only the tracker and the records. This reopens ADR 066 §5.
- **Option C, the engine reads only by named places in Phoenix memory**, with no judgment: choices and blocks come from fixed places, and no proposal is drafted beyond what the project's files show by rule.
- **Lean: A.** It keeps ADR 066's reading and the guide's rule. The cost: Initialize needs a coding tool's agent to run, which Support each coding tool must provide for each tool.

### 3. How a part is found in a Phoenix file and the project's memory written from it
ADR 039 leaves it "Not decided here". What memory may hold is Memory's.
- **Option A, by the file's own sections**: a section that speaks to the answer is read, and what it means for this project is written, naming the file and the section (the old page's default).
- **Option B, Phoenix memory marks each section with the answers it serves**, so selection is mechanical. It changes Phoenix memory's shape, which is Memory's to decide.
- **Option C, the person picks the parts** from a list Initialize shows for each answer.
- **Lean: A now, and ask Memory for B.** A works on Phoenix memory as it is; B is the lasting answer, and makes the selection checkable. C asks the person too much.

### 4. Where the setup answers and the rule-group record are kept
#862: "the profile records them". The profile's schema has no place; the product profile is "THE BOX". Left open since PR #886 ("PM-4 (no committed home yet for the setup-answer records)").
- **Option A, in the product profile, in a place Product model adds** for the answers and the rule-group record, kept apart from the box's levels.
- **Option B, in a set-up record of Initialize's own in Garura memory**, with the profile's `shape.surfaces` filled from the surfaces answer.
- **Option C, in a settings file of Initialize's own** (#946's folder).
- **Lean: A.** It is what #862 says, the review and every later play already read the profile, and the install never changes the product model ("The install never changes a product model the project already has", `install.py` line 53), so the line with the install holds. Product model defines the place.

### 5. Which review rule groups there are, and which answer rules out each
Memory's rule table has id families, not named groups; permissions and personal data are not families.
- **Option A, the review's owners name each group and the answer that rules it out**, in the review's rules in memory, and Initialize records from that list.
- **Option B, Initialize holds the list of six** (the old page's default).
- **Option C, the person picks the groups to skip** in the brief, each with a proposal from the answers.
- **Lean: A.** What a group checks is the review's (decided), and a list kept by Initialize would drift from the rules it names. The six on the page stay as examples.

### 6. Where the tracker mapping and its record are kept, and what a stand-in for an Epic or a Story is
- Where:
  - **Option A, a settings file of Initialize's own in the settings folder #946 plans**, which the install lays nothing into, so the two never write the same file.
  - **Option B, in Garura's main settings file beside `trackers`**, where tools already read. The install and the upgrade write that file, against "the two never write the same files".
  - **Option C, in the product profile with the answers.** The mapping is a setting about how plays file, not a fact about the product.
  - **Lean: A**, with Settings deciding the file's place.
- What a stand-in for an Epic or a Story can be, when a tracker cannot make the type: ADR 056 says "Neither has a label." and "A later change decides how these four kinds are marked."
  - **Option A, Track execution in the team's tracker decides how each kind is marked when its type cannot be made**, and Initialize proposes from that.
  - **Option B, no stand-in for an Epic or a Story**: the type stays missing and the filing plays stop, as for a failed make.
  - **Lean: A.** #881 asks for a stand-in "where a tracker cannot make a type", for every type.

### 7. How a later run tells that a part changed, and what a yes is given to
- How:
  - **Option A, a fingerprint of each part in the project's block list**, compared on each run (the old page's default). The memory tool already gives one with each read, and its decision check already names a source that changed.
  - **Option B, Phoenix memory's version**: any part whose file changed since that version is shown. Coarser; it names parts that did not change.
  - **Option C, Phoenix memory's own release notes** (#921, #966, Memory's), once they exist.
  - **Lean: A.** It is exact and uses what the tool does today.
- What a yes is given to:
  - **Option A, each part, with a yes or no to a whole block applying to every part under it** (the old page's default).
  - **Option B, each block only.**
  - **Lean: A.** One changed standard can be welcome and another in the same block not.

### 8. A question the person leaves unanswered
The old page held every other job back until every question had an answer, a gate with no way past it.
- **Option A, the rest of the set-up goes on**: the open question is recorded as owed, nothing is set up from it, a rule group it would decide is kept, and the next run asks it again.
- **Option B, wait for every answer** (the old page).
- **Lean: A.** Orchestration must not "Stop a person. Every gate has a way past it that records what's owed.", and a kept group "can only add findings".

### 9. An answer no memory tier holds anything for
- **Option A, name the gap only**: the answer is kept, nothing is built for it, and Memory fills the gap when a person promotes something.
- **Option B, Initialize researches the gap and raises a memory update** for a person to approve, used only after the yes (the product owner's standing rule for anything researched).
- **Lean: B.** It is the standing rule's own path, and it leaves the decision with a person. It makes Initialize slower for a project in a field memory does not cover.

### 10. The feature list
- **Option A, keep the six, retitle two** by the product owner's rule for later changes (the drafts).
- **Option B, five features**: fold fn-883's "each project its own" rules into Build the project's memory, and its Phoenix-change update into Update the setup as the project changes.
- **Lean: A.** Each of the six has its own source (#862's checks, #881, #883), and the two updates have different triggers and different decisions: a person's answer changed, or Phoenix memory changed under an answer that did not.

## The persona

- **Lean: the product owner**, for the capability and every feature, as on BI-7's first three capabilities and on the old pages. BI-7 is asked by the product owner; every decision Initialize waits for is the product owner's (confirming the answers, a write to the team's tracker, taking a changed standard in); and the approved pages of other intents already send a decision a person must make to the product owner.
- Other options weighed:
  - **The technical lead**, who knows the stack, could answer the standards, tools and frameworks questions. But each proposal comes from the project's files, so the product owner confirms rather than researches, and no approved page gives the technical lead a decision about the project's memory or tracker.
  - **The devops engineer**, for the running-service question. On the approved pages that persona decides environments, not a project's memory.
  - **A team admin of the tracker**, who has the right to add a type. The page names that case as "making failed" and leaves it to "a person with the right"; adding a persona is the product owner's choice.

## The features

No feature was merged, split or dropped. Two are retitled to the job a person does; the ids stay. None is built.

1. **Ask the setup questions** (`fn-setup-questions`): asks the product owner one short brief of questions built from Phoenix memory, each with choices and a proposed answer that names its source, and keeps the answers the person confirms or corrects. Not built. Sources: #862 (its checks and rules 2 and 3), #883, ADR 038 §3, the rule for asking a person, the memory guide.
2. **Build the project's memory** (`fn-project-memory`): builds the project's own Garura memory from only the blocks the answers call for, from the relevant part of Phoenix memory and never a copy, and records the answers in the product profile. Not built; no tool writes Garura memory. Sources: #862, #883, ADR 039 Decision 4, PR #886's round 2 verdict, the glossary.
3. **Choose the review rule groups** (`fn-review-rule-groups`): records each review rule group as kept or skipped with the answer that decided it, for the review to read. Not built; the review runs every group. Sources: #862, its "Identified by" #860, BI-4's approved page.
4. **Set up the tracker's work-item types** (`fn-881`): finds the trackers the settings name and their types, makes each missing type after a typed yes, and records a stand-in, also on a yes, where a type cannot be made. Not built; the adapter cannot list or make a type. Sources: #881, ADR 048, ADR 056, the settings, the adapter, PR #886's round 1 verdict.
5. **Update the setup as the project changes** (`fn-rerun-initialize`, was "Run initialize again"): a new run proposes the earlier answers and follows the project, and a new version's new question. Not built. Sources: #862, #881, #883, Upgrade a project, the capability's reliability need.
6. **Update each project's own memory as Phoenix memory changes** (`fn-883`, was "Give each project its own memory blocks"): keeps each project's blocks its own and names, on each run, what changed in Phoenix memory under them, taken in on a yes. Not built; the tool's fingerprints and decision check exist. Sources: #883, ADR 039, BI-7's and Orchestration's Must not.

Not a feature here, and why:
- Getting Phoenix memory onto a machine (the Phoenix install of #883): Memory's, decided.
- Seeding memory for the lenses (`capabilities.md` line 17): dropped by the product owner on 2026-11-08 (line 19) ("seeding memory - drop it."), and out of this run's scope as decided.
- Changing the review and the filing plays to read Initialize's records: later stories under #862; they change other capabilities' plays.
- Connections to outside tools: BI-6's `fn-connect-tools` leaves "whether Initialize asks for the connections" not decided; it stays theirs.

## The hand-offs

- **Install into a project** (BI-7, approved): lays the pieces and the memory tool, no memory, and names Initialize as the next step. The two never write the same files.
- **Upgrade a project** (BI-7, approved): hands back the run when a new version asks something new; never writes the project's memory, rule groups or tracker types.
- **Support each coding tool** (BI-7, approved): Initialize sets a project up whichever tool; if open point 2 goes to A, each tool must give Initialize an agent to read memory.
- **Memory** (BI-10): how Phoenix memory reaches a machine and is versioned, what may enter each tier, promotion, the machine-wide copy, and #868.
- **Settings** (BI-10): where Initialize's settings file would live (#946), and what each setting means.
- **Check the code against its standards** (BI-4): what each rule group checks, the list of groups, and the change that makes the review read Initialize's record.
- **Track execution in the team's tracker** and **Turn intents into agent work**: what each tracker type means and how a work item is marked; filing work items and the change that makes the filing plays read the mapping.
- **Product model** (BI-11): where the answers sit in the product profile.
- **Specify the product** (BI-1): the profile's levels and the box; Initialize never moves them.

## What the write will need (for the product owner's yes, not done here)

- The seven pages written word for word (enrich-grounding, approved mode), replacing the old pages, each part's ICE on its own `ice.md`.
- cap-initialize and its six features: `intents: [bi-7]` (link-model-part); new one-lines for the capability's two retitled features; seven entries in the spine's `ices` list, none thin (`checks/spine-simulation.json` shows the seven pages are orphans until then).
- cap-initialize keeps `detail: detailed`, with its NFR needs and its decision. The capability page is laid out in the detailed shape (round 2, on the coordinator's word), so it passes the detailed check; the round-1 page in the directional shape is kept at `bi-7-capability-4/drafts-round-1/capability-directional-shape.md`.
- `nfr_needs` and the decision link kept as they are.
- BI-7's page lists the seven parts it touches (21 now, 28 after).
- Optional, for the product owner: BI-1's `fn-keep-tracker-matched` line 47 renamed to the new title, and the decision's `affects` line pointed at `initialize/ice.md`.

## Checks

- The structure check (`.claude/skills/discover-capabilities/scripts/lint_grounding.py`) on each draft page: all seven pass (`checks/lint.json`). The capability passes with `--stage detailed`, the stage its spine entry names. The checker reads no text before the first `##` heading, so the capability's opening is not checked by it.
- The ICE shape of each of the seven `ice.md` pages: one Goal, Limits, Fails if, the fixed Read line with what to look for, Never read, Persona, Scope, a Scenario and a Done means checked by someone other than the doer, no Thin line and no home or temp path; all pass (`checks/ice-shape.json`). Each Goal was read against its Limits: none contradict. Where a Goal depends on a yes (the tracker types, a re-run's tracker change), it names the state when the person says no, and where it depends on reaching Phoenix memory, it says so, so no Limit makes its Goal fail.
- Every quote in the pages' Sources was checked against its file, its GitHub issue or pull request (read only) or its copy in `bi-7-capability-4/memory/`, with the spacing of wrapped lines ignored: 133 quotes, all found. Quotes in the pages' bodies were checked against the same page's sources: all found, except six words the old pages already set in quote marks as their own terms ("nothing fits", "Cannot make", "making failed", "no file fits", "no block fits", "no answer speaks to it"), which quote no source (`checks/quotes.json`).
- The model-wide check, run on a throwaway copy of the model with the drafts in place: 7 new errors, each an ICE page with no entry in the spine's `ices` list yet, which the write adds (`checks/spine-simulation.json`).
