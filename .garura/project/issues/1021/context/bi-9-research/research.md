# BI-9 (Orchestration): what the new features should be

Research only, 2026-11-10, for #1021 (the chore that reorganises Garura's business intents around the phases
and their transitions). Scope: the BI-9 features that are not built, as the brief named them. That means G1 to
G5 of capability 5 (Give every gate a way past) and the new features of the other four capabilities. The built
features are being drafted by others and are not covered here.

This run wrote this file and eight memory updates, mu-20261110-006 to mu-20261110-013. All eight wait for a
person. Nothing else changed: no model page, no setting, nothing in git, nothing on GitHub. No decision trace was
recorded, because every lean below is a proposal, not a decision.

Each feature below has four parts:
- what Garura already has or says;
- outside practice;
- the lean;
- the open points.

A model page named as `<folder>/...` sits under `.garura/product/product-os/software-delivery-planning/`. A
Phoenix memory file is named by its memory path, and was read through the memory tool.

## In short

**Capability 5, Give every gate a way past**
- **G1. Every gate has a way past.** A rule and a check, not a play. Each gate a play declares names its kind,
  its way past and what using it records, and the play linter fails a gate that names no way past.
- **G2. What is owed is kept in one place.** Each owed entry is written in the issue folder of the work that made
  it. A tool reads every issue's entries as one list, the way the gate learner already reads every issue's
  ledger. There is no global file.
- **G3. A skipped checkpoint is recorded even when evidence is off.** A skip always writes one line to the issue's
  gate ledger. The evidence file stays optional, and the ledger line does not.
- **G4. Each guardrail says what it guards and its way past.** Each guardrail names the shortcut it guards and the
  play that owns that work. When a person is present it asks rather than refuses, and each pass is recorded as
  owed.
- **G5. The pinned yeses.** A typed yes is a way past of its own kind, not an exception. The person holds it, so
  no person is stopped; only the agent waits. It stays pinned, it is recorded, and it may carry what is still
  owed.

**The other four capabilities**
- **Choose the next item.** It is proposed from the plan files: the person's direction, the tree's order, items
  not blocked. The person says which item is Now.
- **Work out the plans a plan waits on.** A script writes the list from the model's "needs" links. It orders the
  work and never holds a landing.
- **Pause a plan.** A person pauses a plan in a plan session. The plan's branch lands on main, and the same plan
  script writes `branch: null`, never by hand.
- **Start a loop from a schedule or a hook.** The trigger is a part of the loop's ICE. The team's scheduler runs
  the loop's command, and a run with no person present asks nothing and never reaches the merge.
- **Run a round's plays side by side.** Only when the round meets the scoped-write fan-out's five conditions.
  Discovery does not meet them today.
- **The status display.** A status-line command reads the run's status file. A Claude Code plugin cannot set the
  status line, so the install adds the setting to the team's file after a yes.
- **One tool knows the tracker.** The Agent-work tool (#1023) has verbs about work, not about GitHub. A check
  fails any part that names a tracker.
- **Link work across trackers.** A real parent link where both trackers are on one platform, else the intent's
  key written in the work.
- **Say what each type means.** One short list of the types and how each is marked, shipped to every project.
- **Record the ADR in its change.** On an open change's branch, /record-decision opens nothing and writes the ADR
  there.
- **Keep ADRs to how the project is built.** A brief about what the model holds is shown as model work, with a
  way past.
- **Take the design choices from Spec → Design.** Taken as a decision brief inside the design play's run, so the
  person answers once.

## Words used here

- **Gate**: a place where a play waits for a person or stops on a check. **Checkpoint**: a gate that waits for a
  person.
- **Way past** (#992 says **key**): what a person may do to go on past a gate. Using it records what is owed.
- **Owed**: what a later play or person must still do because a way past was used.
- **Pinned**: a checkpoint that "Always fires. No config value, policy, or ledger can turn it off."
  (Phoenix memory `standards/rules/gate-config.md` line 12). **Off**: a checkpoint that never waits, because
  named machine checks carry it (line 14). **Machine wall**: a script check that halts whatever the settings
  say, such as a pre-flight halt or a stop condition (lines 122-125).
- **Guardrail**: a check the coding tool runs before an agent acts, which refuses a shortcut past a play
  (`install-into-project/fn-lay-guardrails/feature.md` line 5).

---

## Capability 5: Give every gate a way past

The line he set: "No gate stops a person; each has a way past it, and using it records what is owed where a later
play finds it." (`.garura/project/issues/1021/context/capabilities.md` line 100). BI-9's Must not: "Stop a
person. Every gate has a way past it that records what's owed." (`intents/bi-9.md` line 13).

### G1. Every gate has a way past

**What Garura has or says**
- **The principle is written, but no ADR records it.** #992 (a person is never stopped; every gate has a key,
  open) says: "A gate in Garura is never a hard stop: it always has a key to pass it, and using the key records
  what must be done later. Only evidence is enforced." Its Done means asks that "The gates in today's plays that
  stop a person with no key are listed in the ADR, each with what its key would record or why it keeps a human
  beat." The inventory found no ADR that records it (`bi-9-inventory/inventory.md` line 601).
- **The harness standard says it for the model only.** Principle 6, "Nothing is blocked", says "missing links are
  warnings to fix later, not stops" (`docs/standards/harness-standard.md` lines 68-75).
- **Three ways past are built.**
  1. /update-plan: a rule break is shown with what works instead. "The person may override it ('do it anyway');
     the override is recorded." (`core/components/plays/update-plan/reference/ice.md` C3, lines 26-30). The
     landing's commit carries `Override:` and `Owed:` lines (`update-plan/scripts/commit_plan.py` lines 18-19).
  2. /shape-slice proposes a thin ICE, with both thin marks, for a part that has none. It never stops (ADR 052 §5;
     Phoenix memory ontology line 579: "Work starts ... nothing stopped").
  3. When a found feature has no slice, "its story goes where the person names and the slice is recorded as owed"
     (update-plan ICE C11, lines 62-69; `turn-intents-into-work/fn-add-found-feature/feature.md` line 27).
- **Approved pages of other intents already build to the rule.**
  - An upgrade's no keeps the part as it was and names it as owed (`upgrade-project/capability.md` line 82;
    `upgrade-project/fn-keep-edits/feature.md` line 33; `upgrade-project/fn-move-model/feature.md` line 40).
  - Initialize's no leaves the part so the next run names it again (`initialize/fn-883/feature.md` line 36).
  - BI-2: "A missing choice is a gap, not a stop ... the gap stays on record so a later step knows it was skipped,
    not forgotten." (`design-technology-architecture/capability.md` line 58).
- **Gates with no way past today** (inventory section 5, lines 476-491; section 9, lines 662-670):
  - the pinned yeses (see G5);
  - the machine walls, which are "never gated by this block" (gate-config lines 122-125);
  - /update-plan's stop on uncommitted work: "the person cleans up" (update-plan ICE C2, line 21);
  - three plays that "must not run" until the Agent-work tool exists (#1023, the Agent-work tool);
  - a stop written on an approved page and not yet built. A play that needs a tracker type that is missing and
    unmapped is to "stop with a plain message that points to initialize"
    (`initialize/fn-881/feature.md` line 38).
- **How a gate is declared today.** Each checkpoint "declares its risk class inline (e.g. `Checkpoint (class:
  one-way-door)`)", and a pinned one adds `pinned` (gate-config lines 86-91). Nothing declares a way past.

**Outside practice** (mu-20261110-006)
- **GitHub push protection.** A person may push a blocked secret by picking a reason: "It's used in tests", "It's
  a false positive" or "I'll fix it later". Each bypass adds an alert, an audit log entry and an email that names
  the reason. "I'll fix it later" leaves the alert open.
  [GitHub, about push protection](https://docs.github.com/en/code-security/concepts/secret-security/about-push-protection)
- **GitHub rulesets.** A ruleset names who may bypass it, by role, team or app
  ([about rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)).
  Its insights list "Actions where someone has bypassed one or more rulesets", and the top bypassers
  ([managing rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/managing-rulesets-for-a-repository)).
- **Azure Policy.** A waiver accepts the non-compliance for now. It carries free metadata, such as who asked, who
  approved and a ticket, and an optional expiry. An expired exemption "is preserved for record-keeping".
  [Azure Policy exemption structure](https://learn.microsoft.com/en-us/azure/governance/policy/concepts/exemption-structure)
- **Microsoft Entra break-glass accounts.** The emergency way in is kept on purpose. Every use raises an alert and
  is reviewed afterwards.
  [Microsoft Entra, emergency access](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access)
- **Snyk.** An ignore is written to a policy file in the repository, with a reason and an expiry (30 days by
  default). [Snyk, ignore](https://docs.snyk.io/developer-tools/snyk-cli/commands/ignore)
- **What they share.** The way past is offered, never hidden. Using it records who, when, why and what was
  skipped.

**Lean.** G1 is a rule and a check, not a play. Every gate a play declares names three things: its kind, its way
past, and what using the way past records. The play linter fails a gate that names no way past. Machine walls that
guard evidence stay walls ("Only evidence is enforced", #992), but each halt names what the person can do next.
Today's list of gates goes into the ADR that #992 asks for.

**Open points**
1. Do machine walls count as gates under the Must not?
   - A payments service: no. A failing security check is a wall; the person fixes the code and runs it again.
   - A marketing site: yes. A broken-link check can be passed with "fix later", and the skip is recorded.
   - A data team's notebook project: half. A missing input file stops the run, and the way past is to name
     another file.
2. Must every way past carry a reason, as push protection does?
   - A bank: yes, always. An auditor reads the reasons.
   - A solo developer's side project: no. Who and when are enough.
   - A school's admissions app: only for the pinned yeses.
3. Does a way past expire, as an Azure waiver or a Snyk ignore does?
   - A health app: yes. Each skip comes back after 30 days.
   - A game studio: no. It stays owed until someone pays it.
   - A logistics firm: it expires when the plan it belongs to closes.

### G2. What is owed is kept in one place that a later play reads

**What Garura has or says**
- **What is owed is written in many places, and none of them is a home** (inventory lines 497-499):
  - the plan session's commit message (`Owed:` lines; Phoenix memory ontology line 628);
  - the thin marks on a page and its spine entry;
  - an upgrade's report (`upgrade-project/fn-upgrade-in-one-step/feature.md` line 36);
  - initialize's record of types still missing (`initialize/fn-881/feature.md` lines 28, 40);
  - the gate ledger of each issue;
  - issues filed for findings (#1004, work stays on its scope: a finding outside it is recorded and the work moves
    on);
  - a pending question at Argus's Finish: "Not decided: whether Finish ... lets the person finish with some left
    unanswered, named as owed." (`review-agent-work/fn-answer-pieces/feature.md` line 40).
- **#992 (every gate has a key) asks for a home.** A key records "where the debt is kept so a later play finds it
  (for example the not-yet-learned list of #990)".
- **#990 (the product model moves with the work) designs one such list**, open and not built: "one list of
  changes not yet learned (issue, branch, what was left, who chose, when), so Learn processes exactly that list
  later and never hunts through every issue's short-term memory."
- **The product owner on global records**, in #943 (gate records live in the issue's evidence folder, not in a
  global file): "eval aka records should go in evidence folder that is it. why do we need a global evidence.. if
  we do then we need to create a proper structure". ADR 039 puts every write of a piece of work under its issue.
- **A pattern that fits both already exists.** "Each issue keeps its own history" in its gate ledger, and "The
  learner reads every issue's history ... and writes one project policy" (gate-config lines 48-55).
- **A plan file has no owed field.** Its operational parts live in the plan file and git only (ontology line 629).

**Outside practice** (mu-20261110-007)
- **Atlassian.** Teams lose product-wide priorities "when technical debt is not in the same backlog as new
  features". The alternative to an issue type is "custom fields and labels for all types of technical debt" that
  share one workflow.
  [Atlassian, 3 steps to taming technical debt](https://www.atlassian.com/blog/jira/3-steps-taming-technical-debt)
- **GitHub push protection.** "I'll fix it later" becomes an open alert in the repository's security list.
  [GitHub, about push protection](https://docs.github.com/en/code-security/concepts/secret-security/about-push-protection)
- **Azure Policy.** Each exemption is its own record beside the resource, and the resource shows as Exempt in
  compliance. Microsoft advises revisiting exemptions regularly.
  [Azure Policy exemption structure](https://learn.microsoft.com/en-us/azure/governance/policy/concepts/exemption-structure)

**Lean.** Each owed entry is written in the issue folder of the work that made it, and lands with that change. It
has one fixed shape:
- what was skipped;
- the gate;
- who used the way past;
- when;
- why;
- what pays it.

A tool reads every issue's entries as one list, the way the gate learner reads every issue's ledger. A later play
reads the entries in its own scope at pre-flight, and the plan views show how many are open. There is no global
file, as #943 asks. #990's not-yet-learned list is one kind of entry in it.

**Open points**
1. Who reads the list: every play at its start, the plan views, or only Learn?
   - A clinic's booking app: every play at its start, so nothing owed is built over.
   - A shop's checkout: only the plan views; the person decides when to pay.
   - A research team's data pipeline: only Learn, once a week.
2. Is a big owed entry also an issue in the tracker, as Atlassian advises?
   - A bank: yes, every entry is an issue under the work that made it.
   - A start-up: no, the list in the repository is enough.
   - An agency: only the entries a client must see.
3. Who closes an entry?
   - A health app: only a person, with what paid it.
   - A news site: the play that does the owed work closes it.
   - An internal tool team: either one, and the close is recorded.

### G3. A skipped checkpoint is recorded even when the evidence file is off

**What Garura has or says**
- **The rule.** An off checkpoint "records `gate skipped by config (<resolution path>)` as a Checkpoint Decisions
  row in the evidence file and proceeds. Skips are always visible in evidence — a silent gate is not a gate."
  (gate-config lines 116-118).
- **The rule fails by default.** The evidence file is written only when `evidence.record` resolves true
  (`core/components/plays/_shared/play-close.md` line 86). The source settings set it to false
  (`core/config.yaml` lines 140-142), and only the Discovery loop turns it on (line 144). The opening,
  committing, raising and reviewing checkpoints are off (lines 203-207), so each of their skips is silent.
- **A record that does not depend on that setting already exists.** A conditional checkpoint writes one line per
  crossing to the issue's committed ledger with `gate_eval.py append`. The answers it takes are `approved_clean`,
  `approved_edited`, `rejected`, `auto_pass` and `deferred_to_loop_review`
  (`core/components/plays/create-play/references/gate_eval.py` lines 19-32). The learner skips
  `deferred_to_loop_review` (line 24). An off checkpoint writes no ledger line.
- **One off checkpoint does leave a record.** When /check-change's checkpoint is off, "the computed recommendation
  is recorded and posted as a clearly marked harness verdict" (its description).
- **Related open work outside BI-9:** #969 (every run's records are kept in the evidence folder of its issue) and
  #943 (gate records live in the issue's folder).

**Outside practice** (mu-20261110-006). GitHub records every ruleset bypass in the ruleset's insights. Every
push-protection bypass adds an audit log entry, whatever else the repository has set.
[Managing rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/managing-rulesets-for-a-repository);
[about push protection](https://docs.github.com/en/code-security/concepts/secret-security/about-push-protection).

**Lean.** Every skipped checkpoint writes one line to the issue's gate ledger, with a new answer such as
`skipped_by_config` and the setting that skipped it. The learner skips that answer as it skips
`deferred_to_loop_review`. The evidence file stays optional, and the ledger line does not. So the skip record no
longer depends on a setting.

**Open points**
1. Is a skip by config a debt (G2) or only a record?
   - An online shop: only a record, because the machine checks carried what the person checked.
   - A hospital system: a debt, because a person must read it later.
   - An open-source library: a record, and the review lists the skips.
2. Should the line also name the machine checks that carried the checkpoint, and their results?
   - A payments team: yes, each check and its result.
   - A personal blog: no, the setting is enough.
   - A logistics app: only the checks that failed and were retried.

### G4. Each guardrail says what it guards and its way past

**What Garura has or says**
- **#893 (an agent cannot do a play's work without the play: guardrails laid by the install), open, not
  shaped.** The shortcuts it names: running a play's bundled scripts by hand, writing a play's record files, editing
  a compiled play or its ICE without /edit-play, and finishing a failed step by hand and going on. It proposes a run
  marker, a hook that refuses the shortcut, and a review check. "Not decided: Which paths and which plays the hook
  covers, and how a person overrides it on purpose."
- **BI-7's approved pages hand this part to Orchestration.** "This feature lays them. What each guardrail guards,
  and how a person gets past one on purpose, is Orchestration's." (`install-into-project/fn-lay-guardrails/feature.md`
  line 7; lines 19, 28, 39; `install-into-project/capability.md` line 64). Its check: "the coding tool refuses it
  and names the way past" (line 34).
- **BI-3 waits on it.** Blocking a read of the evals "is left to the guardrails the install will lay (#893)"
  (quoted in `fn-lay-guardrails/feature.md` line 49).
- **Nothing is laid today.** "No install touches the coding tool's own settings today" (`fn-lay-guardrails/feature.md`
  line 16). This repository's Claude Code project settings hold no Garura hook.
- **An older idea is closed.** #775 (Garura's guardrails ship with the harness and can be turned on or off) is
  closed as not planned (`fn-lay-guardrails/feature.md` line 16).

**Outside practice** (mu-20261110-008). All from [Claude Code hooks](https://code.claude.com/docs/en/hooks):
- A PreToolUse hook runs before each tool call. It may answer allow, deny, ask or defer.
- **deny** stops the call, and its reason is shown to Claude, not to the person.
- **ask** "prompts the user to confirm", and its reason is shown to the person in the permission prompt.
- **defer** ends the turn so that the call can be resumed later, in non-interactive mode only.
- A hook that exits with code 2 blocks the call. A hook that fails any other way, or times out, does not block
  unless it is set to block on failure.

Push protection gives a model for recording each pass with a reason (mu-20261110-006).

**Lean.** Each guardrail is one entry with three parts:
- **What it guards:** the shortcut, and the play that owns that work.
- **How it answers:** with a person present, it answers "ask". The prompt names the play to run, and why.
- **Its way past:** the person's yes in the coding tool's own prompt. Each pass writes an owed entry (G2).

With no person present, as in a headless or scheduled run, it refuses and names the play. Nobody is stopped,
because nobody is there. The install lays the guardrails (BI-7), and Orchestration owns this list of what each one
guards and how it is passed.

**Open points**
1. Which shortcuts are guarded first?
   - A team's harness repository: editing a compiled play without /edit-play.
   - A shop's checkout project: running a play's scripts by hand.
   - A clinic's booking app: a builder reading the evals folder.
2. In a run with no person present, is a refusal a stop of a person?
   - A start-up running loops at night: no. The run halts and the morning summary names the guardrail.
   - A regulated insurer: no, and the run must never pass a guardrail on its own.
   - A games company: the run may pass it once and record it as owed.
3. Is the way past the coding tool's own prompt, or a word typed in the session?
   - A team on Claude Code only: the tool's prompt, which shows the reason.
   - A team on several coding tools: a typed word, the same in every tool.
   - An open-source project: a line in the pull request that the review reads.

### G5. The pinned yeses

**What Garura has or says**
- **The pinned set.** "merge-change's land-on-main step" ("merging to main is the one irreversible action in the
  chain"), "intent's confirm step when run by hand (only a person confirms a business intent — ADR 031)" and "adr's
  accept step when run by hand (only a person accepts a decision record — #632)" (gate-config lines 98-108). The
  shaping checkpoints of /shape-slice, /shape-plan and /shape-eval, and the three of /edit-ontology, are pinned too
  (inventory line 488).
- **The merge's yes.** "no config value, policy, or ledger turns it off" (`core/components/plays/merge-change/SKILL.md`
  line 134).
- **Inside a loop, two of them already have a way past.** The intent's confirm and the ADR's accept are saved as
  proposed and decided at the loop's end. Any other pinned checkpoint "is asked up front or becomes the loop's
  question ... never deferred to the loop's review" (gate-config lines 92-96).
- **The question is open in three places:**
  - #992 (every gate has a key): "The ADR says whether these are keys of their own kind (the person's typed 'yes'
    is the key) or exceptions to the principle."
  - BI-8: "Not decided: whether the merge's typed yes is the way past the merge's checkpoint that Orchestration's
    Must not asks for, or a stop kept on purpose (#992)." (`ship-every-change/capability.md` line 91).
  - BI-8 again: the same sentence at `.garura/product/product-os/features/fn-673/feature.md` line 47.

**Outside practice** (mu-20261110-006). Even the strictest checks keep a way past, but it belongs to a named
person, never to the automation, and every use is recorded:
- GitHub rulesets name who may bypass, and list each bypass.
- Push protection lets the people with bypass rights "review and approve bypass requests from other contributors".
- A break-glass account is kept on purpose, and every use raises an alert and a review.

**Lean.** A pinned yes is a way past of its own kind, not an exception. The person holds the key, so no person is
stopped; what waits is the agent. The Must not holds when three things are true:
1. The yes is always open to the person.
2. The yes is recorded: who, when, and the exact reply.
3. The person may answer "yes, with this still owed", and what follows becomes an owed entry (G2).

No setting and no agent ever turns a pinned yes into a skip. The machine walls inside the merge (approved,
mergeable, no failing required checks) stay walls on evidence.

**Open points**
1. May a person answer "yes, but" at a pinned checkpoint, with the "but" kept as owed?
   - A clinic's booking app: yes. "Merge, but the reminder text needs a second look" is kept as owed.
   - A bank: no. A pinned yes is whole, or it is not given.
   - A design studio: yes, but only at the shaping checkpoints, never at the merge.
2. Does some project need a second person's yes at a pinned checkpoint, as push protection's delegated bypass
   has?
   - A payments team: yes, for the merge to main.
   - A solo founder: no, one yes.
   - A hospital system: yes, for confirming an intent that touches patient data.

---

## O1. Orchestrate agent work through planning: the new features

### Choose which item is worked next (fn-choose-next-item)

**What Garura has or says**
- **BI-3's approved pages hand the choice here:**
  - "It starts from the ID a person names and never chooses an item. The reason: choosing which work comes next
    belongs to Orchestrate agent work through planning." (`gather-work-under-item/fn-gather-item-tree/feature.md`
    line 30).
  - "what is built next is chosen in Orchestration" (`build-work-test-first/fn-build-code-to-pass/feature.md`
    line 25).
- **The plan already holds what a person sets** (Phoenix memory ontology):
  - the plan's Direction: 1 next, 2 next in line, 3 later or none. "It is not a ranking" (line 595);
  - "Now: The work item being worked on" (line 599);
  - an item's status, including Blocked (`core/tools/plan/README.md` line 21);
  - nothing worked out by a script: "no roll-ups" (line 623).
- **ADR 051 (the /next play is dropped; the plan is the work list):** "If a 'what next' view is needed later, it is
  a new play that reads the plan files. It is built when it is needed, from its own ICE." (§3, lines 32-34).
- **Today it is a way of working.** An orchestrator session picks the work, and each item gets its own session,
  branch and pull request (`.garura/user-provided/managing-work.md` lines 135-158). This came from #518 (how
  orchestrator and worker sessions hand work back and forth, closed).
- **The question is already open** in the inventory (open question 10, lines 890-893).

**Outside practice** (mu-20261110-011). The Kanban Guide: start work on an item "only when there is a clear signal
that there is capacity to do so", and control the work in progress explicitly. It sets no order for which item is
pulled first. [Kanban Guide](https://kanbanguides.org/english/)

**Lean.** The next item is proposed from the plan files alone. The candidates are the open items of In Progress
plans with Direction 1, that are not Blocked, whose plans waited on are done, taken in the tree's order. The person
says which item becomes Now. A loop may take the proposal on its own only where the person allowed that in the
settings, as BI-6's "allowed kind" does (`build-or-update-product/capability.md` line 83). There is no score and
no ranking.

**Open points**
1. Who says yes to the next item: a person each time, or a loop on its own?
   - An agency with client deadlines: a person, each time.
   - A start-up: the loop takes the next item in the plan's order.
   - A regulated team: the loop proposes and a person says yes.
2. Is Now one item for each plan, or one for each session?
   - A small team: one for each plan.
   - A team that runs three sessions side by side: one for each session.
   - A solo developer: one in the whole project.

### Work out the plans a plan waits on (fn-work-out-waits-on)

**What Garura has or says**
- **The ontology says what it is** (Phoenix memory):
  - "Needs plans: The other plans it needs — worked out from its features' capabilities' needs, never set by hand"
    (line 600);
  - "It needs another plan when a feature in it belongs to a capability that needs a capability whose features
    are in that plan." (line 621);
  - "Two plans that need each other are one plan." (line 630).
- **Shown, never written.** /list-plans shows Waits on, and `core/tools/plan/plan.py` reads `needs_plans`
  (lines 177, 237). No script writes it (inventory lines 189-191).
- **The model links it reads are moving.** Capabilities and features hold "needs" links: fn-725, under cap-723
  (Link the product model), which goes to BI-11. Its plan line: "Finding which plans a plan needs. Build a plan
  (cap-718) and Manage a plan (cap-720) own it." (`.garura/product/product-os/features/fn-725/feature.md` line 54).
- **It orders the work and gates nothing.** ADR 060 removed the rule that held a landing back: "the link gives the
  order of work, not a gate on landing" (ADR 060, "The ontology's landing rule leaves the ontology").
- **The model never names a plan** (ADR 065 rule 3, line 139). So the script works from the plan side: the plan's
  features, their capabilities' needs, then the plans that hold those features.

**Outside practice** (mu-20261110-011). GitHub issues can be marked "blocked by" or "blocking", by hand or through
the command line or API, and "Blocked issues are marked with a 'Blocked' icon".
[GitHub, creating issue dependencies](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies)

**Lean.** A plan script works out `needs_plans` whenever a plan's items change, at /update-plan's landing and
/shape-plan's. It reads the model's needs links and the plan files, and a person never sets the field. It warns
when two plans need each other. It orders the work and never holds a landing.

**Open points**
1. When is it worked out: at each landing, each time a plan is shown, or on request?
   - A logistics app: at each landing, because a carrier link must land before tracking.
   - A news site: on request; the order is mostly editorial.
   - A bank: at each landing, and the review checks it.
2. Should the tracker also show it, as "blocked by" between the epics?
   - A team that lives in GitHub Projects: yes, the Blocked icon is what they see.
   - A team that reads only /list-plans: no.
   - A team on Jira: yes, as Jira's own "blocks" link.

### Pause a plan and start it again, with its branch field kept true (fn-pause-plan)

**What Garura has or says**
- **The rule is decided.** "When the plan pauses, its branch merges into main ... The branch is then deleted, and
  the plan file says `branch: null`." "When the plan starts again, a new branch is cut from main."
  (`.garura/user-provided/managing-work.md` lines 160-177; ADR 060 §1-§3).
- **Starting is built.** `plan_branch.py go` cuts the branch main-first (`core/tools/plan/README.md` lines 48-65;
  ADR 061). It already handles a branch that is gone on the remote after a pause (`plan_branch.py` lines 19, 242).
- **The landing is BI-8's.** BI-8 lands a paused plan's branch (fn-673) and hands the pause itself on: "Pausing a
  plan and changing its items. Turn intents into agent work, in Product → Spec, and Orchestration own them."
  (`ship-every-change/fn-land-plan-with-evidence/feature.md` line 42).
- **What is missing.** Nothing writes the branch field. ADR 060's section "Recorded on #730 — nothing writes a plan
  file's branch field yet; it is kept by hand" (line 75) left the write to #730 (the /update-plan session). #730
  is closed as completed, but a search of the plan tool, /merge-change and /update-plan scripts finds no such write.
- **A related idea was dropped.** #991 (/propose-change asks the plan's Status and Direction when a plan's branch
  is proposed for main) was closed as not planned on 2026-10-31.

**Outside practice.** None needed: the internal sources settle the shape.

**Lean.** Pausing is one instruction in an /update-plan session, such as "pause plan 717". It sets Status to
Paused, and the plan's branch is raised to main through the change plays. When that merge lands, main's plan file
reads `branch: null`. The same script that cut the branch (`plan_branch.py`) writes it, never a person. Starting
again is the `go` that exists.

**Open points**
1. When is `branch: null` written: by the merge as it lands, or by the next session that reads the plan?
   - A team that merges by hand at the end of the day: by the merge.
   - A team that rarely pauses: by the next session.
   - A team with several plans in flight: by the merge, so the views are right at once.
2. Does a pause ask for the plan's Direction too, as #991 proposed?
   - A product team that pauses for a holiday: no, the direction stays.
   - An agency that switches clients: yes, the direction drops to 3 (later).
   - A start-up: only when the person says so.

---

## L1. Run plays as loops: the new features

### Start a loop from a schedule or a hook, and keep a record across rounds (fn-start-loop-on-trigger, #699)

**What Garura has or says**
- **The loop principles name both** (`docs/components/loops.md`):
  - "Something starts the loop. A person, a schedule (every night) or a hook (a pull request opens). The loop says
    which." (line 30);
  - "Keep a record across rounds." (line 34);
  - its table says what is missing: "No trigger part: schedules and hooks are not supported (#699)" and "No single
    record tells the next round what was tried and whether it worked (#699)".
- **#699 (loop builders and the loop linter check the loop principles), open, under BI-10's side.** It asks for "a
  'Trigger' part to the loop's ICE and the run block" and "a round log the shared run writes and reads".
- **Today a person runs the loop's command.** A headless runner exists (`run_play_headless.py`; loop-run.md step
  R5). Each round leaves its files, and `round_state.py` decides done, again or ask.
- **A loop needs a person at two points.** It asks its questions first (R3) and briefs the person at R5b. Its end
  keeps "the merge keeping its pinned human approval" (R7; inventory line 230).

**Outside practice** (mu-20261110-010)
- **GitHub Actions** starts a workflow on a schedule, at "once every 5 minutes" at most, which "will only run on
  the default branch" and "can be delayed". It also starts on an event such as a pull request, or by hand.
  [GitHub, events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- **Claude Code's GitHub Action**, given a prompt, runs with no person present on any GitHub event, including a
  cron schedule. The prompt may be a skill from `.claude/skills/`. A scheduled run is attributed to the user who
  last changed the schedule, and runs can be capped with `--max-turns`.
  [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)

**Lean.** The trigger is a part of each loop's ICE: a person, a schedule or an event. The loop runs the same way
whatever starts it. Garura runs no scheduler of its own: the team's scheduler, such as GitHub Actions, starts the
loop's command. A run with no person present asks nothing. Its questions wait in the round log and the status
file, the run stops at "asking", and it never reaches the merge. The record across rounds is one round log in the
run's folder, written and read by the shared run.

**Open points**
1. What may a run with no person present do when it reaches a question?
   - A nightly test loop at a shop: stop at the first question and leave a morning summary.
   - A data team: answer from memory where it can, and record each answer as owed.
   - A regulated team: stop before any write.
2. Who sets up the scheduler?
   - A team on GitHub: the install offers a workflow file, shown first, on a yes.
   - A team on GitLab: initialize asks and records the schedule; the team adds the pipeline.
   - A solo developer: they run the command by hand or from their own cron.

### Run a round's plays side by side (fn-run-plays-side-by-side)

**What Garura has or says**
- **The loop run puts it off.** "The first build runs the plays one after another, in turn; side by side comes once
  the scoped-write guard can tell two plays' writes apart." (`core/components/loops/_shared/loop-run.md` line 158).
  "No play takes another play's output as its input" (lines 155-158).
- **The rule for writes at once exists, for the sub-tasks of one step.** The scoped-write fan-out is allowed "only
  when all five hold" (Phoenix memory `standards/rules/concurrent-fanout.md` lines 29-51):
  1. its own write scope, declared before dispatch, where "none sits inside another";
  2. no shared file;
  3. distinct output paths;
  4. no sibling dependency;
  5. guarded after the join.
- **Two of those five fail for Discovery today.**
  - A domain's folder holds its capabilities' folders (inventory lines 60-61), so the domain play's scope holds the
    capability play's scope, and condition 1 fails.
  - Each play's persist writes the model's spine, a shared file, so condition 2 fails.
- **Building code side by side is planned elsewhere:** #488 (parallel build loop with worktree isolation) and #501
  (self-contained play chains with parallel worktrees), both under BI-3.

**Outside practice.** None needed. Garura's own rule settles the conditions.

**Lean.** A round runs its plays side by side only when it meets the scoped-write fan-out's five conditions. Each
play's write scope is given as files or kinds, not folders. The spine and other shared files are written once,
after the join. The scoped-write guard checks the round's whole change. Otherwise the round runs in turn. Rounds
that write code wait for #488's worktrees.

**Open points**
1. Is the speed worth the risk for a round that writes the model?
   - A team with a large prototype: yes, three plays at once save most of an hour.
   - A team with a small brief: no, the round is already quick.
   - A team that reviews every page: no, one play's pages at a time are easier to read.

### The status display for a long run (its status file is built)

**What Garura has or says**
- **The rule.** "The run presents a status ... A display shows it." For Claude Code, the display is "a plugin
  installed only when the install chooses Claude Code", which "reads the file and shows a line about once a minute"
  (Phoenix memory `standards/rules/run-status.md` lines 6-11).
  - The file is `{stm_base}<issue>/status/run-<name>.json`, machine-local (lines 15-16).
  - Its fields are kind, name, issue, run_id, state, round, play, step, started_at, updated_at and note
    (lines 20-44).
  - The memory copy still says "drive" (lines 15, 18, 48-49).
- **ADR 041 §6:** "For Claude Code, that display is a separate plugin, installed only for Claude Code." (line 68).
- **The file is written.** `loop_status.py` writes it, with the states running, asking, checking, landing, done and
  halted (`core/components/loops/complete-discovery/scripts/loop_status.py` lines 1-23).
- **No part owns building the display**, and no issue carries it. BI-7 lays it once it is built, and says the run
  status rule owns building it (inventory lines 304-307).
- **A play's own status is named for later.** The file name is "the drive's name (later, a play's)" (run-status.md
  line 15).

**Outside practice** (mu-20261110-009)
- **The status line is a command set in settings.** It receives the session's data as JSON and shows what the
  command prints, so it can read any file.
  [Claude Code status line](https://code.claude.com/docs/en/statusline)
- **It goes quiet while the session waits.** It runs on events such as a new assistant message. Those events "can
  go quiet when the main session is idle, for example while a coordinator waits on background subagents".
  `refreshInterval` re-runs it every N seconds (same page).
- **A plugin cannot set the status line.** A plugin's settings apply "Only `agent` and `subagentStatusLine`". A
  plugin can ship monitors, background commands whose changes appear as notifications.
  [Claude Code plugin reference](https://code.claude.com/docs/en/plugins-reference)

**Lean.** The display is a small status-line command. It reads the newest run status file of the current
repository and prints one line:
- the loop and its round;
- the play and its step;
- the state;
- the minutes so far;
- a stale mark when `updated_at` is old.

It sets `refreshInterval`, because a loop waits on its plays' sub-agents. A plugin cannot set the status line, so
the install adds the `statusLine` entry to the team's settings after showing it first and getting a yes, keeping
every setting the team has (BI-7's rule, `fn-lay-guardrails/feature.md` line 27). The display reads the file and
never controls the run (run-status.md line 54). Building it sits here, in Run plays as loops.

**Open points**
1. Which form does it take: the main status line (needs the team's settings), the sub-agent rows (a plugin can set
   those), or a monitor notification?
   - A team that already has its own status line: the sub-agent rows, so theirs stays.
   - A team with no status line: the main status line.
   - A team that leaves loops running and looks away: a notification when the state changes.
2. What shows a run when no Claude Code window is open, such as a headless run at night? (inventory open question 11)
   - A team on Claude Code: nothing live; a summary at the end.
   - A team on Codex: the same status file, read by another tool.
   - A team with nightly loops: a summary posted in the morning.

---

## T1. Track execution in the team's tracker: the new features

### One tool knows the tracker (fn-one-tool-knows-tracker, #1023)

**What Garura has or says**
- **ADR 065 rule 4:** "Plays, skills and sub-agents know only the tool, never the tracker. Parts move onto the tool
  over time. The code host is its own setting, and the tool reads both." (lines 141-143).
- **#1023 (an Agent-work tool reads the tracker setting), open, under BI-9.**
  - It reads `trackers`, one tracker for business intents and one for agent work, and the code host as its own
    setting.
  - It starts from `platform-adapter`, which serves GitHub and GitLab today.
  - It moves the parts that reach a tracker directly: "3 plays, 11 skills and 3 agents hold `gh` commands, and 10
    plays, 6 skills and 1 agent name GitHub."
  - It fixes `github.owner`.
  - Its acceptance: "Changing the setting changes the tracker, with no other edit" and "A check fails any part that
    names a tracker directly."
  - Until it lands, /shape-slice, /shape-plan and /shape-eval "must not run".
- **The settings disagree.** `core/config.yaml` lines 7-23 hold the old `platform`/`github` block (its owner a personal
  account) and the new `trackers` block (owner `intent-driven-ai`). No script reads `trackers`
  (inventory 3.1).
- **#620 (tools become a first-class Garura component; work-item meanings move to work intelligence), open, under
  BI-10's side.** A tool holds its program, its commands, the minimum version and an install check. The plan tool
  already lives as a tool at `core/tools/plan/`.

**Outside practice.** None needed. ADR 065 and #1023 settle the shape.

**Lean.** One tool, Agent-work, sits beside the plan tool. Its verbs are about work, not about GitHub:
- read an item;
- file an item of a type under a parent;
- set an item's state;
- list items;
- link an item to its intent.

It reads `trackers` and the code-host setting. `platform-adapter`'s issue verbs move into it, and the pull-request
verbs stay with the code host. A check fails any play, skill or agent that names a tracker. GitHub comes first,
then GitLab; Jira and Linear are later stories, as #1023 allows.

**Open points**
1. What does the tool do when the tracker lacks a type it must file? Today's approved page says the play stops
   (`initialize/fn-881/feature.md` line 38), which breaks the Must not.
   - A team on GitHub with no Spike type: file it as a Chore and record the stand-in as owed.
   - A bank on a fixed-type tracker: use the stand-in initialize mapped, or ask the person.
   - A start-up: stop, name initialize, and offer to file it as a Story.
2. Are pull requests part of Agent-work, or a second tool for the code host?
   - A team on GitHub for both: one tool.
   - A team on Jira with GitLab: two tools.
   - A team on Linear with GitHub: two tools, linked by key.

### Link work across trackers (fn-link-work-across-trackers)

**What Garura has or says**
- **ADR 065 keeps the real link, across trackers too.** The section "A real parent and child link between an epic
  and its intent would cross trackers" ends: "Decided: the real link stays, as the product owner asked, including
  across trackers." (lines 85-91). Between two platforms, "the keeper knows of no such link" (line 88).
- **Proven by hand between two GitHub repositories of one organization.** In #1021, BI issues in `garura-intents`
  hold sub-issues in `garura` (inventory lines 374-386). No play makes the link.
- **The model does not need the link.** An Epic reaches its intents through its slice (ADR 065 line 88).

**Outside practice** (mu-20261110-012)
- **GitHub sub-issues.** An existing issue "from other repositories" can be added as a sub-issue. A parent holds up
  to 100 sub-issues, up to eight levels deep. The docs do not say whether the other repository may sit in another
  organization: not confirmed.
  [GitHub, adding sub-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues)
- **Jira** links a work item through its key, written in a branch name, a commit message or a pull request title.
  [Atlassian, reference work items in your development work](https://support.atlassian.com/jira-software-cloud/docs/reference-issues-in-your-development-work/);
  [GitHub for Jira](https://support.atlassian.com/jira-cloud-administration/docs/use-the-github-for-jira-app/)

**Lean.** Agent-work has one verb: link this work item to its business intent. Where both trackers are on one
platform, it makes the real parent link, as #1021 did by hand. Otherwise it writes the intent's key into the work
item and its pull requests, the way Jira reads keys. /shape-plan links each epic. /start-change links an issue it
files when a parent is named.

**Open points**
1. What is the link when the intents tracker and the work tracker are on different platforms?
   - A team with intents in Jira and work in GitHub: the Jira key in each epic's title.
   - A team with intents in GitHub and work in Linear: a Linear link to the GitHub issue.
   - A team with intents in a document: the plan file is the only link.
2. Which plays make the link?
   - A team that plans everything: only the plan plays.
   - A team that files a lot of one-off work: /start-change too.
   - A team that fixes bugs often: the bug filing too, under its story.

### Say what each work-item type means (fn-say-what-each-type-means)

**What Garura has or says**
- **Initialize defers to this feature:**
  - "what each tracker type means is for Track execution in the team's tracker, in Orchestration, to say;
    Initialize never decides those" (`initialize/capability.md` line 23; line 60);
  - its brief takes "the list of types the plays need, each with the one-line meaning the brief shows, as Track
    execution in the team's tracker gives it" (`initialize/fn-881/feature.md` line 23);
  - "Not decided: what a stand-in for an Epic or a Story can be ... how a work item is marked is for Track execution
    in the team's tracker to decide." (line 35).
- **The meanings exist only as a way of working.** The table "What am I filing?" in
  `.garura/user-provided/managing-work.md` (lines 33-48) gives each type, what it is and when it is filed.
  #952 (Garura's way of working is defined as engine rules and settings) says that folder is evidence, not rules.
- **Garura's own organization holds the types,** each with a description, made by hand
  (`initialize/fn-881/feature.md` line 18).
- **The ontology holds the kinds and their places** (Phoenix memory ontology lines 9-21, the Epic kind from
  line 646).
- **#620 (tools become a first-class component) moves the meanings** to the work-intelligence shelf of memory.

**Outside practice.** None needed. Internal sources settle the content.

**Lean.** One short list holds the meaning of each type Garura files and how each is marked: its type, its parent
and no label. The install brings it to every project. Following #620, it sits on the work-intelligence shelf, and
a project may change it. Initialize's brief reads it, the filing plays read it, and it fills each tracker type's
own description. The ontology stays the source of what each kind is; this list is its one-line form for the
tracker.

**Open points**
1. Where does the list live: a memory shelf, a project setting, or inside the Agent-work tool?
   - A team that renames Story to "User story": a setting it can change.
   - A Garura-wide default: a memory shelf.
   - A team with many trackers: the tool, beside each tracker's way of making a type.
2. What may stand in for an Epic or a Story in a tracker that cannot make them?
   - A tracker with only Task and Bug: Task with a parent link.
   - Jira: Epic and Story exist, so no stand-in.
   - GitLab's free tier: an issue with a fixed title prefix, which ADR 056's no-label rule would need to allow.

---

## A1. Manage ADRs: the new features

### Record the ADR in the change it belongs to (fn-adr-in-its-change, #822 under #968)

**What Garura has or says**
- **#822 (/record-decision cannot join a change that is already open), open.** Run by hand, it opens its own
  branch from main, so "the change lands without its ADR, and the issue stays open until a second, small change
  records the ADR. This happened on #816." Done when the play run on an open change's branch records the ADR
  there, still opens its own change when none is open, and a test shows both.
- **#968 (a person records a decision as an ADR in the change it belongs to, and sees every point found on the
  way), open, under BI-9.** It holds #822, #935 (/record-decision checks that the points for the person who
  accepts are gathered and whole) and #850 (apply_adr.py reports linked but writes no forward pointer).
- **Two modes exist today.** Run by hand, it prepends start-change and appends the four change plays. Inside a
  loop, it opens nothing and saves the ADR as proposed (`core/components/plays/record-decision/SKILL.md` lines
  20-24). Run by hand, its accept is pinned (line 199). `/record-decision accept <file>` completes a proposed ADR
  later.

**Outside practice** (mu-20261110-013)
- **Shopware:** "all necessary code changes have to be added to the merge request" with the ADR, and the merge
  request gets the "ADR" label.
  [Shopware ADR](https://developer.shopware.com/docs/resources/references/adr/2020-06-25-implement-architecture-decision-records.html)
- **UK Government Digital Service:** "The status of your ADR's pull request (PR) reflects the status of the
  decision until it has been accepted."
  [GDS Way, architecture decisions](https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html)
- **AWS:** an ADR moves from Proposed to Accepted or Rejected; once accepted it is not changed, and a new ADR
  supersedes it.
  [AWS Prescriptive Guidance, ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)

**Lean.** Run on the branch of an open change, /record-decision opens nothing. It writes the ADR as proposed on
that branch, and the change's review reads it with the work. The person accepts it at its pinned checkpoint, in the
same session or later with `accept`. Run with no open change, it opens its own change, as today.

**Open points**
1. When is an ADR inside a change accepted: before the pull request opens, or when the change merges?
   - A bank: before it opens, so the review reads an accepted decision.
   - An open-source library: when it merges, as GDS does.
   - A start-up: at the merge's yes, in one answer.
2. What happens to the ADR when its change is turned down?
   - A health app: it stays proposed, on its own branch, for later.
   - A shop: it goes with the change.
   - A platform team: it lands alone as Rejected, with the reason.

### Keep ADRs to how the project is built (fn-keep-adrs-to-build, #1022)

**What Garura has or says**
- **#1022 (review every ADR: anything about what the product model holds moves to the model), open, under
  BI-9.**
  - "an ADR is only for how this project is being developed: its architecture, its pieces, and why they are built
    that way. A change to the ontology, and why the ontology changed, is an ADR. What is written inside the
    product model is not."
  - "Business intents are requirements ... no ADR is needed to do it."
  - It reads every ADR and shows the list to the product owner before anything moves.
  - It came up when an ADR drafted for #1021 was about which intents exist, and stopped at the template's rule
    that an ADR never changes a business intent.
- **What exists.** There are 64 numbered ADRs and two superseded ones (inventory 4.1). There is one product
  decision in the model, written by /discover-capabilities, not by /record-decision (inventory 4.2).
- **The question is already open** in the inventory (open question 9, lines 886-889).

**Outside practice** (mu-20261110-013). AWS scopes ADRs to "every architecturally significant decision": structure,
non-functional requirements, dependencies, interfaces and construction techniques.
[AWS Prescriptive Guidance, ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)

**Lean.** The line becomes a check at the start of /record-decision, not only a one-off sort. A brief about what the
model holds (an intent, a capability, a feature, a profile level) is shown as model work, with the part that owns
it. The person may still record it ("do it anyway"), and it is kept as owed. #1022's review applies the same test
once to the 64 ADRs. The ontology's changes stay ADRs.

**Open points**
1. Is a move of the product profile an ADR, or a product fact in the model?
   - A health app: an ADR, because a higher security level changes how the system is built.
   - A retail team: a product fact; the ADR covers only the build.
   - A games company: both. The model holds the level, and an ADR says why the build changed.
2. Where does the reason for a change in the model live, if not in an ADR?
   - A clinic's booking app: on the page, in its "what was done" part.
   - A bank: in the change's pull request and its commit.
   - A product team using Argus: in the answer on the card.

### Take the design choices that Spec → Design hands over (fn-take-design-choices)

**What Garura has or says**
- **BI-2's four approved capabilities hand the record over:** "Manage ADRs (Orchestration) owns the records; this
  capability decides what each choice says and hands it over." (`design-technology-architecture/capability.md`
  line 41; `deployment-design/capability.md` line 63; `environment-setup/capability.md` line 56;
  `manage-surfaces/capability.md` line 52). Each update feature says the same, for example
  `design-technology-architecture/fn-update-architecture/feature.md` line 56.
- **BI-2's own rules:**
  - "A person confirms each choice and each update." (`design-technology-architecture/capability.md` line 57);
  - "An update replaces what held before and keeps it." (line 47);
  - "Not decided: the place in the model, because the model has no kind for the project's architecture." (line 59).
- **The two ADR shapes do not name a project's own architecture.** /record-decision writes Markdown for "Garura's
  own ADRs, `docs/adr/NNN-<slug>.md`" and YAML for "a product decision ... beside its node" (`record-decision/SKILL.md`
  lines 13-14). A target project's choice of architecture is how that project is built, but the Markdown shape names
  Garura's own folder.
- **No play hands a design choice to /record-decision today** (inventory 4.3).
- **Argus carries out an accept** "as Manage ADRs says" (`review-agent-work/capability.md` lines 35, 50, 89).

**Outside practice** (mu-20261110-013). AWS: accepted ADRs are not changed; "a new ADR ... supersedes the previous
ADR". This matches BI-2's "An update replaces what held before and keeps it."
[AWS Prescriptive Guidance, ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)

**Lean.** Manage ADRs takes each design choice as a decision brief: what was decided, why, what else was weighed,
and its source. It takes the brief from the design play inside that play's run, in the loop-contract form: saved as
proposed, with no second change. The person's confirm of the choice in BI-2 is the ADR's accept, so the person
answers once. Each project keeps its ADRs in its own folder, named in settings. An update supersedes the older ADR.

**Open points**
1. Is BI-2's confirm of a choice the same act as accepting its ADR, or two acts?
   - A small product team: one act.
   - A bank with an architecture board: two. The team confirms and the board accepts.
   - An agency: one act for the team, with the client's yes recorded beside it.
2. Where does a project keep its ADRs?
   - A team new to ADRs: `docs/adr/`, as Garura does.
   - A team with ADRs already in a wiki: a folder named in settings, and the wiki links to it.
   - A team that wants one place: in the product model, if the model gains a kind for it.

---

## Memory updates raised

All eight go to this issue's short-term memory, wait for a person, and are used only once approved and applied.
Each draft carries its links in its text, because the memory tool's `sources` field takes memory lines only.

| ID | Topic | Sources |
|---|---|---|
| mu-20261110-006 | Ways past a check, and what each use records (G1, G3, G5) | [push protection](https://docs.github.com/en/code-security/concepts/secret-security/about-push-protection); [about rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets); [managing rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/managing-rulesets-for-a-repository); [Azure exemptions](https://learn.microsoft.com/en-us/azure/governance/policy/concepts/exemption-structure); [Entra emergency access](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access); [Snyk ignore](https://docs.snyk.io/developer-tools/snyk-cli/commands/ignore) |
| mu-20261110-007 | Where what is owed is kept (G2) | [Atlassian tech debt](https://www.atlassian.com/blog/jira/3-steps-taming-technical-debt); [push protection](https://docs.github.com/en/code-security/concepts/secret-security/about-push-protection); [Azure exemptions](https://learn.microsoft.com/en-us/azure/governance/policy/concepts/exemption-structure) |
| mu-20261110-008 | A Claude Code hook as a guardrail with a way past (G4) | [Claude Code hooks](https://code.claude.com/docs/en/hooks) |
| mu-20261110-009 | Showing a long run in Claude Code (L1 status display) | [status line](https://code.claude.com/docs/en/statusline); [plugin reference](https://code.claude.com/docs/en/plugins-reference) |
| mu-20261110-010 | Starting a run from a schedule or an event (L1 trigger) | [GitHub Actions events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows); [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions) |
| mu-20261110-011 | Waiting on other work, and pulling the next item (O1) | [GitHub issue dependencies](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies); [Kanban Guide](https://kanbanguides.org/english/) |
| mu-20261110-012 | Linking work across trackers (T1) | [GitHub sub-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues); [Jira work item keys](https://support.atlassian.com/jira-software-cloud/docs/reference-issues-in-your-development-work/); [GitHub for Jira](https://support.atlassian.com/jira-cloud-administration/docs/use-the-github-for-jira-app/) |
| mu-20261110-013 | An ADR in the same change as its work (A1) | [Shopware ADR](https://developer.shopware.com/docs/resources/references/adr/2020-06-25-implement-architecture-decision-records.html); [GDS Way](https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html); [AWS ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html) |

## Found, not filed

- ADR 041 §6 (line 68) and the run status rule (lines 9-11) say a plugin shows the status, but a Claude Code plugin
  cannot set the main status line, only `agent` and `subagentStatusLine`
  ([plugin reference](https://code.claude.com/docs/en/plugins-reference)).
- Phoenix memory's ontology (v15) line 21 says a Business Intent carries the label `product` and a Spike, Chore or
  Bug the label `work-item`, while `managing-work.md` line 75 says "No labels, for now."
- An approved BI-7 page has a play stop with no way past when a tracker type is missing and unmapped
  (`initialize/fn-881/feature.md` line 38), against BI-9's Must not.
- #775 (Garura's guardrails ship with the harness and can be turned on or off) is closed as not planned, while #1004
  (work stays on its scope) and #952 (Garura's way of working as engine rules and settings) still say they sit under
  it.
- The memory tool's `propose` takes only memory lines as `sources`, so a web draft's links can live only in its text.
