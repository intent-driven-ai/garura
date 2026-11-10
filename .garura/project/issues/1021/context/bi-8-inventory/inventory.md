# BI-8 (Developer tooling): what Garura has for landing a change and for reviewing what agents made

Research only, 2026-11-10, for #1021 (the chore that reorganises Garura's business intents around the phases and their
transitions). Nothing under `.garura/product/`, `.garura/core/` or `.claude/`, on GitHub or in git was changed. No
memory update was raised and no decision trace was recorded, because the brief allowed this one file only.

Scope: BI-8 only. Its page: "People judge what agents made at the level of the outcome, reviewing ADRs, memories,
domains, capabilities and ICE in tools that ship with Garura. Argus comes first." (`intents/bi-8.md` line 3). The
agreed capabilities are Ship every change the same way and Review what agents make (Argus) (`capabilities.md` lines
85-87). The review of a change against its standards is BI-4's (`capabilities.md` line 47); it is noted here as a
boundary, not held.

## In one paragraph

Garura already lands every change through the same plays, but BI-8's page does not say so. Five change plays open a
change, commit it, raise it with a self-review, have it reviewed from outside, and merge it. Every play that ends a
piece of work runs the last four, and so does every loop. The merge always waits for a person's typed yes. The other
checkpoints are switched off by setting and replaced by machine checks. In Garura's own repository the review's
checkpoint is still on, because the installed settings call the review play by its old name. On 20 October the product
owner chose one review, after the pull request, with the self-review gone. That choice sits only in an old plan: no
issue, no ADR and no code carry it, and the agreed line of 3 November and BI-4's approved pages still name a
self-review. Argus, the review tool, is designed in detail, with five sections, a mockup, a contract with Garura, ten
stories and a spike, but none of it is built, here or in any other repository. Today a person's answers reach the work in
other ways: memory updates approved by typing in a session, review verdicts posted on the pull request, typed
confirmations kept in short-term memory, and pages written word for word from what a person approved. BI-8's page
speaks only of Argus. It names fewer kinds of thing than Argus is designed to show, and it says the tools "ship with
Garura" while Argus is designed to stand apart from Garura. Nothing in the model names BI-8 today.

## Words used here

- **Change**: one piece of work raised for review and merged on its own, such as a pull request on GitHub (the
  definition on BI-4's approved page, `check-code-against-standards/capability.md` line 5).
- **The change plays**: `/start-change`, `/commit-change`, `/propose-change`, `/check-change` and `/merge-change`.
  **The end sequence** is the last four, in that order, which a play marked `position: end` runs after its own work
  (Phoenix memory `standards/rules/pipeline-position.md` lines 70-74). The agreed new names are `/start-work`,
  `/commit-work`, `/review-work` (was `/propose-change`) and `/merge-work`, with `/validate-work` (was `/check-change`)
  under the Validator role (`names.md` lines 16 and 26-27). Nothing is renamed yet.
- **Self-review**: the check of a change by the side that made it, before the pull request opens. **Outside review**:
  `/check-change`, the review by a part that is not the builder. It is BI-4's.
- **Checkpoint** (the plays say gate): a place where a play waits for a person's typed yes. **Pinned**: always waits.
  **Off**: never waits; named machine checks carry what the person checked, and the skip is recorded. **Conditional**:
  waits unless a learned policy says this shape of change may pass (Phoenix memory `standards/rules/gate-config.md`
  lines 8-14).
- **Machine check** (the plays say machine wall): a script check that halts the play on a failure, whatever the
  setting.
- **One-off change**: a change for an issue in no plan. **Plan branch**: `plan/<id>/base`, where a plan's issues land
  (ADR 060 §1).
- **Argus**, **the review tool**: one web page where a person reads what agents made and answers each piece. **Review
  pack**: what Garura sends it. **Event**: one numbered record of one action of the person. **Catch up**: one card at
  a time. **Send back**: return a piece, with a comment, to be done again (`617/specs/review-tool.md` lines 47-56).
- **Memory update**: a proposed addition to memory that only a person approves (`core/tools/memory/README.md` lines
  140-151). **Agent decision** with its **trace**: the steps an agent took to decide, each with its memory source
  (ADR 037 §1).
- **Paths**: a path that starts with an issue number, such as `613/specs/plan.md` or `617/specs/review-tool.md`, is
  under `.garura/project/issues/`. Model pages are under `.garura/product/product-os/`, and a bare `review-tool.md` is
  `617/specs/review-tool.md`.
- **A run**: one run of a loop or of a play. **Product model**, **spine**, **ICE**, **Phoenix memory**, **Garura
  memory** and **short-term memory**: as in the earlier inventories.

States: **Live** · **Live, stand-in** (works until the designed part exists) · **Designed only** · **Planned only** (an
open issue) · **Read by nothing** (a setting no script reads) · **Neither** (no build and no issue).

## 1. Ship every change the same way

The agreed line: "Every change goes from opening to merge through the same steps, with a self-review, an outside review
and a person's yes." (`capabilities.md` line 86).

### 1.1 The five change plays

| Play | What it does | What it checks by script | Where a person's yes sits |
|---|---|---|---|
| `/start-change` | Finds or makes the issue, cuts its branch where it will land, a worktree when the setting asks, and the issue's short-term folder (`SKILL.md` lines 10-14, 223-226). | Nothing typed starts nothing; a new issue's title is at least 15 characters and tagged, and its description is complete (`validate_issue.py`, a hard halt, lines 171-184). | Step 2, "Confirm New Issue", only when no issue was found. Off by setting (`core/config.yaml` line 204). |
| `/commit-change` | Commits by concern with conventional messages that name the issue. "commits only; it does not push" (line 12). | Not on main; sensitive files by name and content (`analyze_changeset.py` lines 36-46), a "hard block" that the setting never lifts (lines 149-152); the issue can be found; a stop condition, at most 5 rounds. | A checkpoint only on a sensitive flag, a scanner warning or a low-confidence issue match (lines 171-184). Off (line 205). |
| `/propose-change` | Runs the self-review, pushes, and opens the pull request against where the branch lands, with the self-review and the issue in it (lines 114-192). | On a change branch; clean tree; one pull request per branch; `check_self_review.py` before any push, which halts on a blocking line (lines 157-166); the base read from the branch name (lines 168-176). | Step 2, "Confirm Raise". Off (line 206), replaced by `check_self_review.py` (lines 148-152). |
| `/check-change` | The outside review. BI-4's (`check-code-against-standards/fn-review-each-change`). | See section 1.5. | Step 5, the decision gate. Off in the source settings (line 207), on in this repository (section 1.4). |
| `/merge-change` | Merges, switches to where the change landed and pulls, deletes the branch, closes an issue that landed on its plan branch, sets its plan item Done, and commits and pushes its run records (lines 148-166). | An approval verdict, mergeable, no failing required checks; when one is false it halts and "the human is not asked" (lines 137-142). | Step 2, "Confirm Merge", **pinned**: "no config value, policy, or ledger turns it off" (lines 132-146; `core/config.yaml` lines 208-209). |

*State:* Live and in use in this repository ("runs on every change in Garura's own repository",
`check-code-against-standards/capability.md` line 6). Every install carries them, in both kinds ("change chain",
`install.py` lines 15-23). They work on GitHub; the GitLab path is "UNTESTED here"
(`check-change/scripts/platform_adapter.py` line 34). ADR 025 promises "A ship is always commit-change →
propose-change → review-change → merge-change: all four, in order, every time." (lines 68-70).

### 1.2 The self-review today

- **What runs.** `/propose-change` Step 1: `repo-orchestrator` with the `assess-pr` skill, against `self-review.md`,
  writes a checklist that goes into the pull request (lines 114-132). The rules: matches the issue, no scope creep,
  reasonable size, no stray files; tests present, clean commits, no secrets, "Docs in step", nothing obviously broken
  (Phoenix memory `standards/rules/self-review.md` lines 19-35). *State:* Live.
- **What the rules say it is, against what the play does.** The rules: "It is **not** the approve/reject gate — that is
  `review-change`'s job." and "it does not block the raise on its own" (same file, lines 15-17; `review-change` is the
  old name). The play: `check_self_review.py` halts the raise "to a human" when a line of the self-review reads
  BLOCKER, BLOCKING, P1 or FAIL (`check_self_review.py` lines 12-18; `SKILL.md` lines 163-166).
- **How the rules are found.** By path, over the folders the settings list (`SKILL.md` lines 79-89,
  `resolve_standard.py` lines 1-16), not through the memory tool. The run record keeps a path inside the person's
  home folder (for example `613/context/self-review.md` line 3, which also names the old `review-change`).
- **A second self-review, by the building session.** "It reviews its own work, and writes the guidelines it reviews
  against." ... "That review produces no verdict." (`.garura/user-provided/managing-work.md` lines 229-243), from #521
  (let a building session review its own work, closed).
- **The 20 October choice.** "[The product owner] (2026-10-20): **one review, after the pull request** — the
  self-review before it goes; its checks move into the review plays, and its hard checks (no secrets, a clean tree,
  the issue named) become machine checks before the pull request opens." (`613/specs/plan.md` lines 63-73, under "What
  this plan leaves out"; log line 204). Confirmed as recorded. It was "A business intent of its own; filed when [the
  product owner] asks." No issue carries it (issue titles and bodies searched for "self-review"), and no ADR names a
  self-review (`docs/adr/` searched).
- **What came after it.** #939 (filed 2026-10-28; the reviews leave out the agents' working records) keeps it: "A
  person reviewing a change, themselves before raising it or in the PR review". The agreed line of 3 November says
  "with a self-review". BI-4's approved pages of 9 November say "raising the change with its self-review"
  (`check-code-against-standards/capability.md` lines 12 and 56; `fn-review-each-change/feature.md` line 63).
- **The three hard checks are already machine checks, in part.** No secrets: `/commit-change`'s sensitive-file scan,
  a hard block. A clean tree: `/propose-change` pre-flight (C3). The issue named: `/commit-change` (C3) and
  `/propose-change` (C4, SE-4). What is not checked by machine: client, company and personal references in what is
  pushed (#888, #672, #982, #914, all open).

### 1.3 How a change lands

- **A one-off change.** `feature/<issue>-<slug>` from an up-to-date main (`start-change/SKILL.md` lines 12-13); the pull
  request goes to main (`propose-change/SKILL.md` lines 175-176); the merge lands on main, where "the code host closes
  issues only on main" (`merge_pr.py` lines 18-21).
- **An issue in a plan.** `plan/<id>/<issue>-<slug>`, cut from `plan/<id>/base` (ADR 060 §1, lines 93-97); the pull
  request goes to the plan branch; the merge closes the issue there, its capability once every issue under it is
  closed, and sets only that item Done in the plan file (`merge-change/SKILL.md` lines 148-158; ADR 064). #1014
  (merge-change closes the Epic when every issue under it is closed, against the no-roll-up rule) is open.
- **A plan's own branch.** It lands on main whenever the plan pauses, with issues still open (ADR 060 §2, lines 99-103;
  `merge-change/SKILL.md` lines 125-126).
- **Inside a loop.** The plays skip their own start and end; "The loop opens and lands the change" (Phoenix memory
  `standards/rules/loop-contract.md` lines 63-68). The loop's end runs the same end sequence, "the merge keeping its
  pinned human approval" (`core/components/loops/_shared/loop-run.md` lines 395-401).
- **Changes that reach a branch with no pull request, by design.** When a plan's work starts, main's plan file is set
  to In Progress, "committed and pushed on main" (ADR 061 §3, lines 84-88; `start-change/SKILL.md` lines 214-219).
  `/update-plan` makes "one commit on the plan's branch, pushed" (its `SKILL.md` line 4), and "the plan's branch
  reaches main later through the change plays" (line 661). `/merge-change` commits and pushes its run records after
  the merge, on the branch the change landed on (lines 159-165).

### 1.4 The settings

- **The checkpoint switches.** `core/config.yaml` lines 194-216: start, commit, propose and check are off "per the #467
  ruling"; the merge is pinned. The rule: off "granted only in the same change that adds the replacement checks"
  (Phoenix memory `gate-config.md` line 14). The pinned set includes "merge-change's land-on-main step" (same file,
  lines 90-103).
- **In this repository the review's checkpoint is on.** The installed settings still say `review-change: off`
  (`.garura/core/config.yaml` line 168), the play's old name. So `/check-change` finds no switch of its own and falls
  back to the standard class, which is `on` (line 159). #772 (the install keeps old play names in the project
  settings, so the check-change gate is on) is open. BI-4's approved page says the same: "In Garura's own repository
  the setting that turns off the person's decision still names the review's old play name, so a person decides there
  (#772)." (`check-code-against-standards/capability.md` line 32). Both ways are on record in this repository
  (`fn-send-code-findings/feature.md` line 26).
- **`review-pr.bypass: true`** (`core/config.yaml` lines 95-97). Its stated job: "whether it hard-blocks" the merge on
  a reject (Phoenix memory `pipeline-position.md` lines 72-74; `check-change/SKILL.md` lines 313-315 and 351-352). No
  script reads it. The one script that reads the `review-pr` block reads only `standards_order`
  (`fetch_pr_context.py` line 220). `/merge-change` marks a change approved only when the decision reads approve
  (`read_merge_state.py` lines 48-58), so a reject always stops the merge. *State:* Read by nothing. That it is set on
  purpose for a one-developer repository is not written in any file or issue I found; an old design note says it
  "Gates `ship` unless `review-pr.bypass=false`" (`docs/design/playbook-catalog.md` line 60).

### 1.5 The review plays that exist, and the practices they follow

- **One review play, no review loop.** `/check-change` is the only review play. The loops folder holds only
  `complete-discovery`. ADR 029 §5 expected that "the review will likely be a drive of its own" (line 51). ADR 032 §1
  decided "It is not a drive of its own" (line 29). The 20 October idea of review split into plays (code quality,
  security, design) run as a drive (`613/specs/plan.md` lines 63-66) was never filed.
- **What `/check-change` does.** "The guiding rule: the change under review is never its own standard." (line 48). It
  sorts the change into kinds of work from the diff, takes each kind's treatment from the review shelf in memory, runs
  linters, has one agent per design-bearing kind check the design against committed sources, at once (lines 223-236),
  and gives a verdict by one fixed rule: "reject if any P1 finding (or a runnable suite is red), otherwise approve"
  (lines 291-304). It posts the decision on the pull request, naming who decided (lines 330-341).
- **Against the practices the product owner asked the review plays to adopt** ("parallel reviewers, a verification step
  that filters false positives, dedupe, severity meanings, a cap on nits, excluded paths, evidence for each finding",
  `613/specs/plan.md` lines 65-68): parallel reviewers, in part (one per design-bearing kind); severity meanings, yes
  (P1 to P4, by the `pr.md` taxonomy, lines 293-297); evidence for each finding, yes (SE-6, lines 306-307). A step that
  filters false positives, a dedupe step and a cap on small findings: none found in the play, its ICE, its agent or its
  skill.
  Excluded paths: planned (#939). This is BI-4's to build; it is listed because the decision was taken about the change
  pipeline.

### 1.6 Planned only

- **The pipeline as a whole.** #510 (change delivery pipeline: propose, review, merge): "A change can go from finished
  work to merged without a human intervening to unstick the pipeline". Its tracker parent is BI-4's issue
  (garura-intents #4), not BI-8's. #610 (decide the Ship loop's recipe, "every change lands the same way"), also under
  BI-4's issue; ADR 066 says "There is no Ship loop" (line 77) and "#610 decides a Ship loop that no longer exists"
  (line 153).
- **Under #510:** #976 (several ready issues land in one change: one branch, one pull request, one review); #915
  (landing a plan branch on main shows that every commit was reviewed and that the plan, its epics and the commits
  agree); #939 (the reviews leave out the agents' working records and keep the model and memory); #517 (a pull request
  template); #452 (propose-change halts on its own evidence files); #537, #857, #996 (commit-change's record and its
  clean-tree check); #579, #583, #787, #1014 (merge-change defects); #672 (the pre-merge reviews enforce the
  no-client-names rule), with #888 under it (the change plays push with no scan).
- **Elsewhere:** #982 and #914 (home-folder paths in committed run records, BI-10's tracker); #992 (a person is never
  stopped: every gate has a key; its open point asks whether the merge's typed yes "is the key" or an exception); #990
  (the model moves with the work: `/propose-change` lets the person update the model now or leave it for Learn, BI-11's
  tracker); #501 (self-contained play chains in parallel worktrees); fn-744 (rename the change plays, in the model under
  `bi-734`).

### 1.7 Neither

- The 20 October one-review change itself (section 1.2).
- A machine check that the docs move with a play: only the self-review's "Docs in step" judgment. The review's docs
  playbook fires only "the PR changes human-facing prose" (Phoenix memory `knowledge/review/docs.md` line 5), so a play
  change that leaves its docs behind is not caught. #529 and #973 ask for a guard (section 7).
- Undoing a merge.

## 2. Review what agents make (Argus)

The agreed line: "People review ADRs, memories, domains, capabilities and ICE in one tool." (`capabilities.md` line 87).

### 2.1 Designed

The design is `.garura/project/issues/617/specs/review-tool.md` (576 lines, status draft, updated 2026-10-18), with a
mockup beside it (`review-tool-mockup.html`). ADRs 032, 033, 036, 037 and 041 decide parts of it.

- **What it is.** "a small web server that knows nothing about Garura. Garura sends it a **review pack** ... When the
  person presses **Finish**, Garura applies the answers." (lines 47-56). Garura's listener reads the event stream and
  writes each event as a file on the branch; "Claude still never reads the web page" (lines 122-129).
- **Five sections.** Intents, Product, ADRs, Memory and Agent decisions (ADR 037 §3, lines 46-56; review-tool.md lines
  187-192). Intents shows each business intent with its ICE under it; Product shows domain, capability and feature, then
  limits and decisions (lines 206-215). Memory has "Ask memory", a plain-words question box over the three tiers, on the
  same vectorless memory tool, "mocked only for now" (ADR 037 §4, lines 58-64; review-tool.md lines 267-277). The memory
  updates waiting for a person are approved or rejected there, one at a time (lines 317-330). Agent decisions shows each
  decision with its trace, each step's source re-checked (lines 278-307).
- **What a person can do.** Comment on words or on an area, edit, remove, drop, accept, send back, finish; approve or
  reject a memory update (lines 348-361). Catch up: "swipe right approves. Swipe left leaves the piece as it is, unread.
  Any change has to be entered" (#680; review-tool.md lines 254-257).
- **What it shows every time.** The whole model's state, approved, changed or in progress, "not only at the end of a
  drive" (ADR 033 §7, lines 70-72).
- **Who writes what.** "The review step writes **approved** or **in progress**, from the person's answers. Plays write
  the model. The review tool writes nothing to the model." (ADR 033 §6, lines 66-68).
- **Where it lives.** First "in `core/tools/outcome-review/`" (line 64), built "inside garura - as part of 606 plan"
  (lines 514-517). Then, 2026-10-20: "the tool is Argus, a Phoenix tool ... the review tool needs to be built
  separately" (line 576). #680: "It is a Phoenix tool, built separately from Garura and tracked in the Phoenix project
  under **Garura tools**"; "it imports no Garura code, so it can move into Griffin later". `managing-work.md` lines
  110-115 say every tool built beside Garura is a Phoenix tool, tracked in that one org project.
- **Two open decisions.** D1, how events reach Garura (recommended: Garura's listener connects to the tool); D2, whether
  a person's direct edit needs an amendment to ADR 032 (lines 543-557). One reviewer only in version 1 (lines 538-539).

### 2.2 Built

- **Nothing of the tool.** No folder in Garura's tracked source holds it, and `core/tools/outcome-review` has no
  history in git (`git log --all`). No setting names it (`review.server_url`, promised in #648, is not in
  `core/config.yaml`). The org's `phoenix` repository is empty. `phoenix-harnesses`, a console prototype, has apps
  for Griffin, Phoenix and Sphinx only, and no issue names it for Argus. In the org project "Phoenix", #680 reads
  Done (it was closed as not planned) and #681, #641-#644 and #664 read Todo.
- **The mockup.** Real and in use as a test input: the Discovery loop's runs were made on "the Argus mockup" (ADR 041
  line 7; test-sandbox #1).
- **The pieces Argus would show, already kept as data.** Memory updates, with `propose`, `updates`, `decide` and `apply`
  (`core/tools/memory/README.md` lines 135-137); agent decisions with their traces, with `cite` and `citations --check`
  (line 127); proposed ADRs from `/record-decision`; the model's pages and spine.
- **The stand-in at a loop's end.** "Until the review tool (Argus) exists, Discovery ends at the pull request: the
  person types **confirm** or **drop** for each intent" (`record_confirmation.py` lines 4-8; ADR 041 §7, lines 70-74;
  `complete-discovery/SKILL.md` line 214). The record says `applied_to_model: false   # Argus's review step writes the
  approval (#650)` (line 71). *State:* Live, stand-in.

### 2.3 Planned only

| Issue | What it is about | Tracker parent |
|---|---|---|
| #681 | Argus itself: "a person reads a drive's outcome and answers each piece" (a drive is now a loop, ADR 045) | BI-8 (garura-intents #8) |
| #641, #642, #643, #644 | The contract; the server with numbered events; reading a review; answering it in the page or one card at a time | #681 |
| #664 | The Memory and ADRs section | #681 |
| #648 | Garura opens a review on what a drive changed and records every answer on the drive's branch | BI-8 |
| #649 | A sent-back piece comes back reworked, with Garura's reply | BI-8 |
| #650 | The drive's last step applies the review's answers in one commit and writes approval | BI-8 |
| #645, #646, #647 | Every piece carries its approval state; agents build only from approved pieces; how approval is recorded outside the review step | #964, under BI-11 (garura-intents #11) |

- #664 is behind the design. It still names one "Memory and ADRs" section, which ADR 037 §3 split into three (ADR 037
  lists #664 under Affects for this reason). Its first done line, "it is written to its tier: ... Garura or Phoenix memory
  for a promotion", goes against the design, "Moving memory up is not done here" (review-tool.md lines 328-330).
- #569 (a per-play review viewer) was closed as not planned on 2026-10-18; the design replaces it (lines 559-561).
- #680 (the business intent for Argus) was closed as not planned on 2026-11-02 with "Replaced by garura-intents#8."

### 2.4 How a person's answers become part of the work today

- **Memory updates.** A person approves or rejects each one, and only then is it written to the issue's short-term
  memory (`README.md` lines 146-151). Until the tool exists, "the person types the decision in a Claude Code session"
  (`decided_in: session`). The memory tool lists 11 updates in all: 5 applied and 1 rejected, each decided in a
  session, and 5 waiting; none was decided in a review tool (`memory.py updates`). *State:* Live.
- **The review verdict.** `decision.yaml` names the decision and who made it (`human` or `harness`); `post_verdict.py`
  posts it and refuses a record without both (`check-change/SKILL.md` lines 330-341); `/merge-change` reads it. *State:*
  Live.
- **Checkpoint replies.** A typed approval, recorded as a checkpoint row in the run's evidence; a skipped checkpoint is
  recorded as skipped (each change play's Step C1). The learned-gate ledger keeps each crossing (Phoenix memory
  `gate-config.md` lines 62-81). *State:* Live.
- **Confirming an intent and accepting an ADR, by hand.** Pinned: "only a person confirms a business intent" and "only a
  person accepts a decision record" (Phoenix memory `gate-config.md` lines 104-108). *State:* Live.
- **Pages written from a person's words.** `write_approved.py` writes a page "from text a person approved, word for
  word", and refuses a request that does not name the person (`enrich-grounding/scripts/write_approved.py` lines 1-40);
  `author-intent-page` "never confirms by itself" and writes confirmed only with the person who confirmed it
  (`author-intent-page/SKILL.md` lines 25 and 78). This is how #1021 has written every approved page. *State:*
  Live.
- **Typed confirm or drop at a loop's end.** Kept in short-term memory, not applied to the model (section 2.2).
- **What does not exist.** An approval state on each piece of the model (#645) and the step that writes it (#650). So no
  answer is yet kept on the piece it answers, and no agent checks one before it builds (#646).

### 2.5 Neither

- Reviewing a play run by hand in the tool. ADR 032: "Run by hand, a play's review is unchanged." (line 99).
- Reviewing BI-6's findings and recommendations in it: "Not decided: where the report is kept and where he reads it,
  such as a file in the project or the planned review tool." (`fn-hand-on-findings/feature.md` line 35;
  `fn-recommend-changes/feature.md` line 37).
- More than one reviewer at a time ("Not in version 1", review-tool.md line 538).
- Any tool after Argus. The page says "tools"; `managing-work.md` line 110 names Griffin and Sphinx as later Phoenix
  tools, not as review tools. A status display for Claude Code is planned elsewhere (Phoenix memory
  `standards/rules/run-status.md`; `613/specs/plan.md` lines 56-61).

## 3. The model today for BI-8

- No domain, capability, feature, slice or ICE names `bi-8` (count of spine parts by intent). BI-8's page says "What was
  done: (nothing yet)" (line 18).
- `cap-721`, "Start and land work against a plan: plan branches in start-change and merge-change" (`_spine.yaml` lines
  47-59), no domain, with `fn-731` (start-change cuts a plan's branch, and each issue's branch from it) and `fn-673`
  (merge-change lands an issue on its plan branch, and a plan on main whenever it pauses) (lines 675-699). All three
  name `bi-717`, whose tracker issue #717 is closed as completed. Their ICE is a section on their own pages. Built
  (section 1.3).
- `fn-744`, "Rename the change, plan, knowledge and record plays" (lines 834-845), under `cap-742`, naming `bi-734`
  (closed as not planned).
- `fn-review-rule-groups` (record which review rule groups fit the project), under Initialize, BI-7's.
- The approved pages of other intents that name BI-8's two capabilities:

| Intent | Page and line | What it says |
|---|---|---|
| BI-3 | `build-work-test-first/capability.md` line 65 | "Out: opening the branch, committing, reviewing and landing the change. Ship every change the same way, in Developer tooling, owns them." |
| BI-3 | `fix-defects-test-first/capability.md` line 70 | The same line. |
| BI-3 | `fix-defects-test-first/fn-fix-defect-code/feature.md` lines 21 and 77 | "the change is landed through Ship every change the same way"; "Committing, reviewing and landing the change. Ship every change the same way does them." |
| BI-4 | `test-product-with-evals/capability.md` line 52 | "Out: opening the branch, committing and landing the change. Ship every change the same way, in Developer tooling, owns them." |
| BI-4 | `test-security/capability.md` line 56; `fn-test-code-security/feature.md` line 56 | "keeping a secret's value out of each commit, and landing the change. Ship every change the same way ... owns them." |
| BI-4 | `check-code-against-standards/capability.md` lines 12, 56, 81 | "raising the change with its self-review, and merging it with a person's yes stay with Ship every change the same way"; "its merge reads this capability's verdict"; "Either way the merge waits for a person's yes in Developer tooling." |
| BI-4 | `check-code-against-standards/ice.md` lines 6 and 19 | "opening, committing, raising and merging the change, with the person's yes on the merge, stay with Ship every change the same way"; "the product owner gives the merge their yes in Developer tooling." |
| BI-4 | `fn-review-each-change/feature.md` line 63 | "Raising the change, its self-review, and merging it with a person's yes. Ship every change the same way, in Developer tooling, does them." |
| BI-4 | `fn-send-code-findings/feature.md` lines 10, 26, 47, 71; `ice.md` line 3 | "Ship every change the same way, in Developer tooling, reads this verdict before the merge"; "the merge in Developer tooling reads it"; "the merge is left to Ship every change the same way." |
| BI-6 | `fn-hand-on-findings/feature.md` lines 18, 47; `ice.md` line 16 | "A review tool where people review what agents make is planned"; "Building the review tool. Review what agents make, in Developer tooling, owns it." |
| BI-6 | `fn-recommend-changes/feature.md` lines 37, 51; `ice.md` line 16 | The review tool's agreed line "names ... no recommendation"; "Building the review tool. Review what agents make, in Developer tooling, owns it." |
| BI-7 | `install-into-project/fn-lay-guardrails/feature.md` line 40 | "The run marker inside each play, and the check in the review of each change. How a play is built, and Ship every change the same way, own them." |

- The tracker and the agreed list disagree. BI-8's tracker issue (garura-intents #8) has four sub-issues: #681, #648,
  #649 and #650, all about Argus. The change pipeline (#510) and the Ship loop spike (#610) sit under BI-4's issue.
  #973 sits under BI-7's issue.

## 4. ADRs and docs that decide how a change lands and how review works

- **ADR 012**: a play commits its own evidence. **ADR 025**: the four end plays always run "in order, every time"
  (lines 68-70).
- **ADR 028 §4**: "Change — every change lands the same way" (lines 50-52), the source of the phrase. Superseded in
  part by **ADR 066**: "§4, that the change chain is a loop" goes; "There is no Ship loop" (line 77).
- **ADR 029 §5**: every run of a loop ends in a review (lines 49-51). **ADR 032**: the review is the last step and not
  a loop of its own (§1, line 29); the person reviews the outcome, not the plays (§2); in review tools, "The pull request
  is not where the person reviews." (§3, lines 42-49); accept, drop or send back (§4); the answers applied as one commit
  and "The merge stays pinned to the person." (§5, lines 59-69); a play run by hand keeps its own review (line 99).
- **ADR 033**: approval lives in the model, on every piece, with three states; agents work only on approved pieces;
  only the review step writes approval (§6); the tool shows the whole model's state each time it opens (§7).
- **ADR 036 §7** (lines 74-81): memory and ADRs are reviewed in the tool; "Until the tool has this section, a person
  approves by typing". **ADR 037 §3-§4**: five sections and Ask memory. **ADR 041 §7**: until Argus exists, a loop
  ends at the pull request with typed confirm or drop.
- **ADR 060** and **ADR 061**: plan branches, where each change lands, and main's plan file committed first. **ADR
  064**: a plan item follows its own issue, with no roll-ups.
- **ADR 066 §4** (lines 81-83): "`/start-work`, `/commit-work`, `/review-work` and `/merge-work` open, commit, review
  and merge work. They are not tied to a role, because anyone can run them. Their final place is still open." Its
  risks: "`/review-work` raises a change for review and `/validate-work` judges it, so the first can be read the wrong
  way." (line 132).
- **No ADR** records the 20 October one-review choice, or that `review-pr.bypass` is meant to be on.
- **Docs.** `docs/philosophy/idsd.md` line 110: the person's output side is "reviewed in an intent review tool and a
  product review tool (ADR 032)". `docs/components/plays.md` lines 362-366 describe the change plays; the same table
  lists `implement`, `validate`, `launch`, `deploy`, `refactor` and `learn` (lines 355-361), none of which is a play
  today, and says merge-change returns "to main" (line 366), though a plan's issue lands on its plan branch.

## 5. Memory

Searched through the memory tool with `--issue 1021`, every tier, for review tool, Argus, pull request, self-review,
code review, the change plays and approve.

- No tier holds a knowledge page on reviewing agent output, on review tools, or on how a team should land a change.
  Phoenix memory's one line on reviews in the field is a cost, "long code reviews" (`knowledge/technology/
  delivery-triangle.md` line 41).
- Phoenix memory holds the rules the change plays follow: `standards/rules/self-review.md`, `pipeline-position.md`,
  `pipeline-next.md` (the "Change loop (git)", line 29), `gate-config.md`, `loop-contract.md`, `pr.md`,
  `templates/pr-body.md`, and the review shelf `knowledge/review/` (seven playbooks: decision records, documentation,
  harness, memory, code, config maps, tests).
- Phoenix memory's naming rule gives skills the verbs "open: Git — open a pull request." and "merge: Git — merge a pull
  request." (`standards/rules/naming.yaml` lines 53-54).
- Garura memory holds the approved pages quoted in section 3, and BI-8's page.

## 6. What the evidence puts in doubt on BI-8's page

- **Item 1 is not on the page at all.** The outcome is about judging what agents made, in tools. The why argues against
  the pull request as the place to review. Neither proof, nor the must-not, speaks of opening, committing, raising or
  merging a change. Yet nineteen approved lines of BI-3 (4), BI-4 (14) and BI-7 (1) hand those jobs to "Ship every
  change the same way, in Developer tooling" (section 3), and `names.md` lines 26-27 put the work plays "under
  Developer tooling".
- **"reviewing ADRs, memories, domains, capabilities and ICE"** (Outcome). The design shows more: business intents
  first, then features, limits, product decisions and agent decisions (ADR 037 §3; review-tool.md lines 206-215). Only a
  person confirms a business intent (ADR 031; BI-11's must-not "let an agent confirm an intent"), and ADR 032 puts
  that confirmation "in the intent review tool, not on the pull request" (line 98). The agreed line has the same five words.
- **"in tools that ship with Garura"** (Outcome). Argus is designed to be "built separately from Garura", to import "no
  Garura code" and to "move into Griffin later" (#680; review-tool.md line 576). No install lays a review tool, and the
  design has the person start the server once and "Claude only checks `/v1/health` and never starts it" (review-tool.md
  lines 528-531). "Ship with" can mean installed together, or only used together; no source says which.
- **"Argus comes first"** (Outcome). No source names the tool that comes second.
- **"A person reviews a whole run in the tool."** The design reviews a loop's run at its end (ADR 032 §1), and also shows
  the whole model every time it opens (ADR 033 §7). A play run by hand keeps its own review (ADR 032, line 99). Which
  runs "a whole run" means is not said.
- **"Their answers become part of the work."** Already true in part without the tool (section 2.4). What the tool adds,
  the approval kept on each piece, is BI-11's (#964, #645-#647), not BI-8's.
- **What pulls against the must-not, "Make people read raw files to know what was made":**
  1. Outside a loop the pull request, a diff of files, is where a run by hand is reviewed (ADR 032, line 99).
  2. Inside a loop, until Argus exists, the run "ends at the pull request" (ADR 041 §7).
  3. The review's findings come out as "an id, a class and a short label" (#902, open; BI-4's
     `check-code-against-standards/capability.md` line 30).
  4. The design itself makes one exception: an agent decision's source is shown "as its memory, file and lines, because
     the person must check it" (review-tool.md lines 336-338).
  5. The self-review, in the pull request body, is a checklist over the diff (`assess-pr`).
  - Not a pull: the plays' briefs and plan views already show outcomes in plain words, not files (for example
    `/shape-slice`'s `render_brief.py`, and `/show-plan` printing from the plan file).

## 7. Where BI-8's parts touch other intents

- **Code → Validation (BI-4), Check the code against its standards.** The review of each change, its verdict and who
  decides it are BI-4's (`check-code-against-standards/capability.md` lines 6, 8 and 81; `capabilities.md` line 47). The
  line between them: Ship every change runs the review as a step and its merge reads the verdict; it never judges.
  Three places blur that line. BI-7's `fn-lay-guardrails/feature.md` line 40 gives "the check in the review of each
  change" to Ship every change. The self-review is a review of the change, named on BI-4's approved pages as Ship
  every change's. And the review practices of section 1.5 were decided for the change pipeline, but sit inside BI-4's
  review.
- **Orchestration (BI-9).** Its must-not: "Stop a person. Every gate has a way past it that records what's owed." The
  pinned merge has no way past it (`merge-change/SKILL.md` lines 132-136); nor do the hard halts on sensitive files, a
  dirty tree, a new issue's title or a blocking self-review line (section 1.1). #992 leaves open whether a typed yes "is
  the key". Manage ADRs (BI-9) owns recording an ADR; Argus's ADRs section would move `/record-decision`'s pinned accept
  onto a card (#664). Turning a plan into work and running it are BI-9's; landing each piece of it is Ship every change.
  ADR 066 §4 leaves the work plays' place open.
- **Standards, structure, settings and memory (BI-10).** Settings: the checkpoint switches, `review-pr`, #772 and the
  learned-gate ledger. Memory: "people control what enters them"; the memory update and its approval are Memory's rule,
  and Argus's Memory section is where a person would give it. Agent decisions and their traces are Memory's (`cite`).
  Standards: the naming of the work plays (fn-744), and any lint rule that keeps docs in step (#529).
- **Product model (BI-11).** The approval state on every piece and the rule that agents build only from approved pieces
  (#964 with #645-#647). The review step that writes it (#650) is BI-8's. #990 (the model moves with the work, and
  `/propose-change` offers to update it now or leave it) is under BI-11's issue but changes a change play. BI-11's
  must-not, "let an agent confirm an intent", is why the confirm stays with a person in the tool.
- **Install and distribute (BI-7).** The install lays the change plays (`install.py` lines 15-23). If Argus is to "ship
  with Garura", laying or pointing at it is an install question.
- **Run → Product (BI-6).** Where its findings and recommendations are read is not decided; the agreed Argus line names
  no recommendation (`fn-recommend-changes/feature.md` line 37).
- **Where #973 fits** (Garura's docs and command pages stay in step with what ships, open; #529, the command cheat sheet
  drifts from the plays, under it). See lean 7.

## 8. Leans

Each is a proposal with its evidence, not a decision.

### Lean 1: give Ship every change the same way its words on BI-8's page

- **Option A, BI-8 keeps it**, and its page gains a line for it in the outcome and one proof (for example "every change
  lands through the same steps, and a person says yes to each merge"), in the product owner's words.
- **Option B, Orchestration (BI-9) takes it**, as the part that runs the work. ADR 066 §4 says the work plays have no
  role "because anyone can run them".
- **Option C, leave the page as it is.**

**Lean: A.** `names.md` lines 26-27 put the work plays under Developer tooling, and nineteen approved lines of BI-3, BI-4
and BI-7 already point there (section 3). B would change those nineteen lines. C leaves a capability its intent never
names.

### Lean 2: the self-review

- **Option A, keep it**, as the agreed line says: a check of hygiene by the side that made the change, with no verdict,
  in the pull request. Its rules already say "it does not block the raise on its own" (Phoenix memory `self-review.md`
  line 17). Then `check_self_review.py`, which halts on a blocking line, is out of step with its own rules, and either
  the rules or the script changes.
- **Option B, drop it, as chosen on 20 October.** Its hard checks are already machine checks (section 1.2); its other
  checks move into the review plays, which are BI-4's. The agreed line, three approved BI-4 lines
  (`check-code-against-standards/capability.md` lines 12 and 56; `fn-review-each-change/feature.md` line 63) and #939
  change.

**Lean: A**, unless the product owner says the 20 October choice still stands. The later words, the agreed line of 3
November and the pages approved on 9 November, keep the self-review, and the 20 October choice was never filed. This is
open question 1.

### Lean 3: the features of Ship every change the same way, from the evidence only

1. Open each change where it will land: the issue, its branch (a plan's branch or main), its short-term folder. Built
   (`/start-change`; ADR 060, ADR 061).
2. Commit by concern, with the issue named and nothing sensitive. Built (`/commit-change`); open defects #537, #857, #996.
3. Raise the change with its self-review (or without it, by lean 2), against where it lands. Built (`/propose-change`);
   planned #452, #517, #939.
4. Merge on the review's approval and a person's yes; close the issue and its plan item. Built (`/merge-change`, pinned);
   open defects #579, #583, #787, #1014.
5. Land a plan's branch on main with evidence that every commit was reviewed. Planned (#915).
6. Land several ready issues in one change. Planned (#976).
7. Scan every push for client, company and personal references. Planned (#888, #672, #982, #914).
8. Keep the docs and command pages in step with each change. Planned (#973, #529), by lean 7.

The outside review is a step of this path, not a feature of it: it is BI-4's (`fn-review-each-change`,
`fn-send-code-findings`). #510 and #610 would move to BI-8's tracker issue; #610 is overtaken by ADR 066 (line 153).

### Lean 4: cap-721 and its two features join Ship every change the same way

- **Option A:** merge `cap-721` into Ship every change, so `fn-731` and `fn-673` become its features, and repoint them
  from `bi-717` to `bi-8`. `bi-717`'s own words stay.
- **Option B:** keep `cap-721` as a capability of its own under BI-8.
- **Option C:** leave it with `bi-717`, whose tracker issue is closed.

**Lean: A.** Cutting a plan's branch and landing on it are feature 1 and feature 4 of lean 3, for an issue in a plan.

### Lean 5: what Review what agents make holds

- **Option A, the whole review a person does**: the Garura side (#648 open and listen, #649 send back, #650 apply the
  answers) and the tool (#681 with #641-#644 and #664), as features, with the tool's build tracked in the Phoenix
  project as #680 says. The approval state on each piece stays BI-11's (#964).
- **Option B, the Garura side only**, with Argus named as the tool it uses, outside the model.

**Lean: A.** The agreed line is about what a person does in the tool, and the tracker already files #681 and its
stories under BI-8's issue. The cost: the model then holds a part that Garura's code never contains, which is open
question 2.

Features, from the evidence only: read a run's outcome, intents with their ICE and the product (#643); answer each piece
in the page or one card at a time (#644); review ADRs, memory and memory updates, and agent decisions with their traces
(#664, Ask memory mocked only); send a piece back and get it reworked (#649); apply the answers in one commit (#650);
open a review on what a run changed and keep every answer on its branch (#648); the contract between the two (#641,
#642).

### Lean 6: the line on what is reviewed names business intents and agent decisions

The agreed line and BI-8's outcome name "ADRs, memories, domains, capabilities and ICE". The design shows business
intents, features, limits, decisions and agent decisions too (section 2.1). Lean: the product owner widens the line,
for example "business intents and their ICE, the product model, ADRs, memory and agent decisions", or says the five
words are on purpose. #664 also needs bringing up to ADR 037.

### Lean 7: #973 goes to Ship every change the same way

- **Option A, BI-8, Ship every change the same way**: each change that alters a play brings the docs and command pages
  it affects. #973's own words are about each change: "something keeps them in step when a play changes". The
  self-review already asks it ("Docs in step", Phoenix memory `self-review.md` line 35), and nothing else checks it:
  the review's docs playbook fires only when the docs themselves change (`knowledge/review/docs.md` line 5). The drift
  is real: `docs/components/plays.md` lines 355-361 list six plays that do not exist. The guard #529 asks for, a rule
  in the component lint, is a Standards rule (BI-10) that this path runs.
- **Option B, Standards (BI-10)**: #529 asks that "The guard runs as part of the normal component lint", and BI-10's
  proof is "The checks hold every part to the standard."
- **Option C, Install and distribute (BI-7)**, where the tracker files it: the docs are what a team reads to install and
  upgrade.
- **Option D, Check the code against its standards (BI-4)**: its page counts documents as code (line 5), and its review
  runs the component lint on harness changes.

**Lean: A.** The promise is kept at each change, which is what this capability does, and it gives the self-review's
"Docs in step" a machine check. The cost: if lean 2 goes to B, the check needs to be a machine check before the pull
request opens.

### Lean 8: the domain

Software delivery planning, with its opening changed to say it also lands every change and lets people review what
agents made, as for BI-6 and BI-7 (its opening already says "It also gets Garura itself into a project",
`software-delivery-planning/domain.md` line 4). The other option is a domain of its own for Developer tooling. Lean:
the same domain, until a second is needed.

### Lean 9: found and not filed, to file when the product owner says so

- `review-pr.bypass` is read by no script, while a memory rule says it decides whether a reject blocks the merge
  (section 1.4).
- The self-review rules say the self-review does not block the raise and name the old `review-change`;
  `check_self_review.py` blocks it (section 1.2).
- `/propose-change` reads its rules by path, not through the memory tool, and records a home-folder path (section 1.2;
  the path part is #982 and #914).
- #664 names one Memory and ADRs section and writes promotions, against ADR 037 and the design (section 2.3).
- `docs/components/plays.md` lists six plays that are gone (section 4); this is #973's work.

## 9. Open questions (no source answers them)

1. Does the self-review stay (the agreed line of 3 November, BI-4's pages of 9 November) or go (the choice of 20
   October)? And if it stays, may it halt the raise?
2. What "tools that ship with Garura" means for Argus: laid by the install, pointed at by a setting, or only used
   alongside, while it stays a Phoenix tool with no Garura code?
3. Which runs "a whole run" covers: a loop's run only, or a play run by hand too?
4. Are business intents and agent decisions left out of the agreed line on purpose?
5. Is the merge's typed yes a key of its own kind under BI-9's must-not, or an exception to it (#992)?
6. Is `review-pr.bypass: true` still wanted, and what should it do, since no script reads it?
7. Where do BI-6's findings and recommendations get reviewed: in Argus, or elsewhere?
8. Which tool comes after Argus?
