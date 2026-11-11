# Lock the design: research and drafts (issue 1021, BI-2 capability 6)

Draft only. Nothing under `.garura/product/`, on GitHub or in git changed. The drafts are under `.garura/project/issues/1021/context/bi-2-capability-6/drafts/product-os/software-delivery-planning/lock-design/`: the capability page and its ICE page, and three feature pages, each with its ICE page. All four ICE pages carry the thin mark, because nothing of the capability is built.

What this run did besides reading:
- It copied what it read from memory through the memory tool into `bi-2-capability-6/memory/`, with `manifest.json`.
- It ran no placement: the domain (software delivery planning) was decided by the product owner.
- It read GitHub issue #893 (no write) to find planned work.
- It checked each page with the structure check, each ICE page with a small shape check, and every quote in a Sources section against its file. The record is `lint.json`.
- The decisions this run made from memory are in `cite-request.json`, for the caller to record with `memory.py cite` (recording them writes outside `bi-2-capability-6/`).
- The pages were written by hand in short-term memory, as the brief asked and as the first four BI-2 capabilities were. No skill drafts pages of the approved shape into short-term memory: the page skills write only into the live model. That missing skill is named here, not worked around further.

The product owner's words used here, as the coordinator gave them on 2026-11-08: "lock this design and bi-2 is locked". Decided on 2026-11-08 and not reopened: seeding memory is dropped from BI-2 and not drafted; the pages do not use the old name for the design views of a slice, and call that capability "designing each slice (Design → Code)"; the capability sits in software delivery planning.

## What is built, and what is only planned

In one line: nothing locks the project's design or checks for a lock before a build. What exists are older pieces that lock one file, decide approval, accept one decision, protect a slice in flight, or check readiness for a different thing.

Built, live (the nearest pieces):
- **The ready check before work on an agent intent** (`core/components/plays/shape-plan/scripts/check_ice_workable.py`). Each run it gives ready, partly ready or not ready; not ready stops work. "Writing is never blocked; this check stops work, not writes." The plan play skips and names a feature that is not ready ("a feature whose ICE is not ready is skipped and named"). It is the pattern closest to a governance check: a rule worked out from the model, run by a play at its start, never a play of its own. It reads the business intent's confirmation, not a design.
- **The business intent as the one gate** (ADR 047 §8): "No tokens are spent on work that no person has approved: the business intent is the one gate." Only a person confirms an intent (gate-config, Phoenix memory: "only a person confirms a business intent").
- **The decision record's accept step** (`/record-decision`, `core/components/skills/author-decision/scripts/adr.py`: "proposed -> accepted, on a person's word"). A pinned human step ("only a person accepts a decision record"). An accepted record is never edited: "accepted decisions are not edited — supersede or amend with a new record" (decision schema, Phoenix memory). This is the nearest built lock, one decision at a time.
- **A slice in flight** (ADR 058; `/shape-slice` C7 and C20). A shaping run never touches a slice whose build has started; only an edit a person approves changes it, and the brief "names each epic past ready, with its status, as out of date, because work already started from the old text." Its rule: "No change to work in flight is silent." This is the built answer to reopening something agents already build from, for slices.
- **The eval as a fixed yardstick** (`/shape-eval` C7): "An eval is a fixed yardstick." Scenarios are only added, never changed.
- **The change plays' human gates.** `/check-change` stops at one decision gate resolved by gate-config; `/merge-change` lands only an approved change, and its land-on-main step is pinned. BI-4: "a person approves the merge."
- **The gate rules** (gate-config, Phoenix memory). A pinned gate "NEVER resolves off"; pre-flight halts are "machine's walls, not human courtesies." and are never switched off by config.
- **Fingerprints that catch drift.** The memory tool: "`cite` refuses a source that is gone or changed. `citations --check` names every decision whose source no longer says what it said." A compiled play "records a fingerprint of its intent + expectation precisely so that drift is detectable." (`/edit-play`).

Built, but stale or old (no live play uses them for this):
- **The draft and locked status of design files.** `author-technical-approach`, `author-lld`, `author-implementation-plan` and `author-verification-scenarios` give their file a status ("Lifecycle: DRAFT → VALIDATED → LOCKED"), refuse to overwrite a locked one ("architecture.yaml is LOCKED -- drop to DRAFT first."; "NEVER overwrite a LOCKED architecture.yaml -- return structured failure") and always write draft. The glossary: "an architecture artifact starts DRAFT, moves to LOCKED after human review; agents treat it as authoritative thereafter". No step ever sets locked (a search for code that writes it found none), and only the tech-designer agent lists these skills.
- **The old rule that a locked file is the answer** (`standards/rules/resolution.md`, Phoenix memory: "the LOCKED artifact wins unconditionally."; tech-designer: "if LOCKED, use as authoritative (stop descending)."). Superseded in part by ADR 035 ("Superseded in part by ADR 035 §5"; glossary: "Superseded by ADR 035: agents find memory only through the memory tool").
- **The stale build play's two checks** (`/build-epic`, stale). Its readiness script refuses a slice unless "the slice exists in the spine `slices` index and its status is `realized`" and every design document exists. ADR 028 dropped that refusal ("The realized-slice gate goes."; design areas: "None of them is a must-have."), and ADR 066 notes "the stale /build-epic still refuses a slice without it". Its ICE also had a person approve each epic's spec before the build ran alone: "the build does not start until they approve it." and "agent carries the epic to done alone."; "a fix round carries none and is" not gated. Later: "The spec-approval checkpoint is no longer a pinned human gate: it resolves" by config, now off. This is the old per-epic hand-off to agents, the closest built thing to "before agents take over".
- **The product profile's locked state.** Spine schema (Phoenix memory): "locked (no play sets it now, ADR 053)". ADR 053: `/shape-scope` "was the only play that set a capability `active` and set the product profile `locked`" and "After this decision no play does this."
- **Approval in the product model** (ADR 033, accepted, not built). "Agents work only on approved pieces"; "This is the governance rule of the product model."; a piece keeps a fingerprint, and "A piece changed after it was approved is caught by its fingerprint, with no play having to remember to flag it." Not built: "Until they are, nothing writes approval." ADR 047 later took the agent intent and its part out of it; the rest stands. The ontology (v15) has no approval lifecycle.

Only planned or decided:
- **The agreed line**: "Lock the design: A design is locked before agents take over. This is the only gate, because without it agents drift. It is a governance check, not a play. Its final place is settled when it is built."
- **BI-2**: "a design is locked before agents take over."; "Without the lock, agents drift."; "No agent builds from a design that isn't locked."; "Block on anything except the lock, which is the only gate."
- **ADR 066 §5** and `names.md`: "Locking a design is a governance check." / "Lock the design is a governance check." No play name exists for it.
- **ADR 028** (stage 2): domains and capabilities are updated, "then lock them." **ADR 029**: the next loop "locks domains and capabilities." Both are about locking the product model in Product → Spec, not the design; neither is built.
- **The four approved BI-2 capabilities** hand the lock here: each update feature says "Not decided: how the architecture is updated once the design is locked. Lock the design owns the lock, the only gate, and it is not built." (the same for the surfaces, the deployment design and the environments) and "Opening a locked design for an update. Lock the design owns the lock."
- **#893** (open business intent, not shaped): "An agent cannot do a play's work without the play"; hooks "laid by the Garura install, so every project that uses Garura gets them"; "A Claude Code hook (a script Claude Code runs before each tool call) refuses:"; not decided: "Which paths and which plays the hook covers, and how a person overrides it on purpose."
- **BI-9** (Orchestration): "Every gate has a way past it that records what's owed."

## What "a governance check, not a play" can mean, in what is built

1. **A state in the project's records and a check that each building play runs at its start.** The lock is a record a person's yes creates (with a fingerprint of each position, the gaps, who, when, why). The check is a script, like the ready check, that a building play runs before its first build step; no setting turns it off, as gate-config already says for pre-flight halts. The yes is given at whatever step shows the design to the person, and recorded by one tool command, like the decision record's accept. Built pattern: the ready check, the accept step, ADR 033's fingerprint. Cost: every play that builds must call it; an agent that skips the play is not stopped (the gap #893 names).
2. **A hook laid by the install.** A Claude Code hook refuses a building agent's work when no lock is on record, as #893 proposes for play shortcuts. Built pattern: none in Garura yet. It stops even an agent that skips the play. Cost: not built, not decided; tied to one coding tool, while Garura aims to support several; a hook sees tool calls, not the build of a work item, so it is hard to aim.
3. **A decision record.** The lock is an accepted decision (this version of the design is locked), made through Manage ADRs' accept step and replaced by a superseding record. Built pattern: the accept step and supersede-never-edit, live today. Cost: the gate depends on the decision tooling; the check must read decision records; and gaps are not decisions.

My lean is option 1. It matches the one built governance check (the ready check, which "stops work, not writes"), keeps the lock out of every play's own steps, and leaves room for option 2 as a backstop once #893 is decided. The drafts follow it, but name the final place as not decided, as the agreed line does.

## The overlaps, and how the line could be drawn

### With the four BI-2 capabilities (each one's update feature and the lock)

Each update feature makes and confirms an update and leaves to this capability how it works once the design is locked.

1. **The locked version stays in force; the update is locked on its own yes.** The position's own feature makes and confirms the update; the old lock stays in force meanwhile, so builds keep starting; then the product owner locks the new version, and work started on the old version is named, not stopped (as ADR 058 does for a slice). Cost: one more yes after each confirmed update, though several updates can be locked with one yes.
2. **Open first, as built in the older skills.** A person opens the lock ("drop to DRAFT first"), the update is made, the design is locked again. Cost: while it is open nothing is locked, so every build waits for the length of the update.
3. **The confirmation of an update is also its lock.** One yes. Cost: the architect or the devops engineer, who confirm their positions, would hand the design to agents for the product owner; the lock's owner would differ by position.

My lean is option 1. It never leaves a time with nothing locked, keeps the four update features as they are, and keeps one owner for the lock. The drafts follow it.

### With Manage ADRs (Orchestration)

Each position choice is handed to Manage ADRs as a decision record, accepted on a person's word and never edited after.

1. **The lock is its own yes and record; it names the decision records of the version it covers, accepted or proposed.** A record still proposed does not hold the lock back. Cost: two kinds of record about the same design, which must agree.
2. **The lock is itself a decision record**, accepted and superseded through Manage ADRs (governance option 3). Cost: as above.
3. **Locking is accepting every record of the design; no separate step.** Cost: no single moment; gaps have no record; the lock would wait on every record.

My lean is option 1. It keeps the gate apart from the decision tooling and never makes the lock wait on another step. The drafts follow it.

### With the build (no agent builds from an unlocked design)

1. **The check is this capability's; every play that builds runs it once, when a build starts.** A build already started is not checked again (as built, "a fix round carries none and is" not gated). The check hands the builder the locked version. Cost: each building play must call it.
2. **Build the work owns the check in its own readiness step**, reading the lock recorded here. Cost: each building play would carry its own copy of the rule, and copies drift (Garura already has two copies of the ready check and twelve of the structure check).
3. **The check runs at every build step, or again at the review before merge.** Cost: a lock that moves mid-build stops work midway; a check at review catches it only after the tokens are spent.

My lean is option 1. The drafts follow it. Open inside it: which plays besides Build the work run the check. Fixing a defect and refactoring build code too; my lean is that they run it, because the proof names no exception, and it costs a project with no lock one yes. The pages leave it as not decided.

### With designing each slice (Design → Code)

1. **Designing each slice goes on before and after the lock; only the build waits.** Cost: a slice designed on a version that later changes may need rework, found when its build starts.
2. **Designing each slice waits for the lock too**, reading "agents take over" as the start of Design → Code. Cost: blocks something other than a build, against the business intent's must-not.
3. **As option 1, and when a build starts, a slice designed on an older version is named as out of date.** Cost: one more thing to track.

My lean is option 1, with option 3 left as not decided on the check page. Whether a slice's own design needs a lock is settled with BI-3.

### With the business intent's confirmation, and with the Orchestration intent

- **ADR 047's "the business intent is the one gate"** and BI-2's "the only gate" are read as gates at two different steps: the confirmation stops any work on an agent intent whose business intent no person confirmed; the lock stops only the start of a build. The check before a build does not replace the ready check. The pages say so in an Out line.
- **BI-9's "Every gate has a way past it that records what's owed."** The way past the lock is one person's yes: a design can be locked as it stands, even with every position a gap, and the gaps are what is owed. No agent builds past it.
- Assumed: the person's yes before an environment is built (Environment setup, approved) is a step before a live action, not a second gate on design or build; the drafts leave it as it is.

### Siblings and other neighbours

No decision asked; the drafts draw these lines:
- **Specify the product** owns the product profile and its locked state, which no play sets; out here.
- **Ship every change the same way** owns the review and merge of each change; out here.
- **#893** owns hooks for every play; out here, and a possible backstop for the check later.
- **Locking the product model's domains and capabilities** (ADR 028, ADR 029) belongs to Product → Spec; not drafted here.

## The persona

- **The product owner** locks the design and each update. From what is built: BI-2 names the product owner under Asked by; the domain page "serves the product owner, who names the work and approves its design"; the decision play's scenario "(product owner, a product decision)" is the one who accepts a record; gate-config pins the accept and confirm steps to a person; and his own words, "lock this design and bi-2 is locked".
- **The developer**, a person or an agent who builds each work item, is the one the check stops or lets through. From the stale build play's scenario "(developer, the approval gate)", where the build waited for a person's approval, and the developer of the approved dev sandbox feature.
- **The architect and the devops engineer** confirm the updates of the positions they own (approved pages), and their updates reach the builders once locked.

## Features found

Three features, none built. Each ICE is thin. They follow the shape the product owner asked for on the earlier capabilities: one job is one feature, and a later change is an update as the project changes.

- **Lock the design** (fn-lock-design). Not built. A person locks the project's design as it stands, the four positions at their confirmed versions, each with a fingerprint, with each open choice named as a gap and each decision record named with its status, and the lock records who, when and why. Sources: the agreed line; BI-2; his words "lock this design and bi-2 is locked"; ADR 066 §5; the older draft and locked status ("moves to LOCKED after human review"); ADR 033 (approval with a fingerprint, not built); the accept step of a decision record; the profile's locked state (no play sets it); the stale build play's spec approval.
- **Check the lock before an agent builds** (fn-check-lock). Not built. When a build of a work item starts, a check confirms a lock is in force and hands the builder the locked version with its gaps; with no lock that build does not start and the check names what to lock and who locks it; nothing else waits. Sources: BI-2's proof and must-not; the ready check ("stops work, not writes"); the stale build play's readiness check (dropped by ADR 028) and its spec approval; the old "if LOCKED, use as authoritative" rule; the memory tool's fingerprint check; gate-config's machine walls; #893 (planned hooks).
- **Update the locked design as the project changes** (fn-update-locked-design). Not built. When a position changes after the lock, the locked version stays in force until the product owner locks the confirmed update, the old lock stays readable, and work started on the old version is named, not stopped. Sources: the four approved update features' "Not decided" and "Out of scope" lines; the older skills' "drop to DRAFT first"; ADR 058's slice in flight; the decision schema's supersede-never-edit rule; BI-2's "Each position is written down and can change later."

Candidates not drafted as features of their own:
- **See what is locked**: part of locking (what the lock shows) and of the check (its message). ADR 033 gives the review tool the job of showing approval state, under Review what agents make.
- **Open the lock**: replaced by keeping the locked version in force during an update (overlap lean 1).
- **Lock each slice's design or spec before its build**: the stale build play did it per epic; it belongs with BI-3 and Build the work.
- **Lock the product model or the product profile**: Product → Spec and Specify the product.
- **Hooks against play shortcuts**: #893, for every play.

## Gaps that matter

- **Nothing records a lock or checks for one.** As built, a build starts from whatever the design says that day, which is the drift BI-2 names.
- **No step ever set "locked"** in the older lifecycle, and no play sets the profile's locked state. The pattern exists only as a word.
- **The approval decided in ADR 033 is not built**, so nothing in the model records a person's approval of exact words with a fingerprint. The lock would be the first such record.
- **The model has no kind for the project's design**, so where the lock is kept is not decided, as on the other four pages.
- **An agent that skips the building play is not stopped** under the lean (option 1); only #893's hooks would stop it, and they are not decided.

## Open points for the product owner

- What "a governance check, not a play" is: option 1, 2 or 3. The drafts follow option 1 and name the final place as not decided.
- The line with the four update features: option 1, 2 or 3. The drafts follow option 1 (the locked version stays in force; the product owner locks each confirmed update).
- The line with Manage ADRs: option 1, 2 or 3. The drafts follow option 1.
- The line with the build: option 1, 2 or 3. The drafts follow option 1. Whether fixing a defect and refactoring also run the check is not decided on the pages; my lean is yes.
- The line with designing each slice: option 1, 2 or 3. The drafts follow option 1.
- A new project with nothing set can be locked with every position a gap, so one yes is always the way past. The drafts say so.
- One lock for the whole design, not one per position. The drafts say so.
- Where the product owner gives the yes (the end review of the Spec → Design loop, the review tool, or a command): not decided on the pages.
- The personas: the product owner locks; the developer is checked; the architect and the devops engineer confirm updates.
- The feature names: "Lock the design", "Check the lock before an agent builds", "Update the locked design as the project changes".

## Details left out of the pages

Left for an agent that builds these parts to find in the code and memory: the field names of the lock record, the fingerprint method, the exit codes of the check, the old skills' status values beyond draft and locked, and the gate-config resolution order.

## What this run read from memory

Through the memory tool, copied to `.garura/project/issues/1021/context/bi-2-capability-6/memory/` with `manifest.json`, all from Phoenix memory: the gate rules (`standards/rules/gate-config.md`), the old resolution rule (`standards/rules/resolution.md`), the product profile, spine, decision and ontology schemas, and the capability and feature grounding templates with the content standard. From short-term memory, a search showed only the earlier BI-2 drafts. Garura memory holds nothing on a lock beyond the approved model pages. No tier was missing.

## Checks

See `lint.json` for the full record.

- **Structure check** (`python3 .claude/skills/discover-capabilities/scripts/lint_grounding.py`): `--kind capability --stage directional` on the capability page, `--kind feature` on each of the three feature pages. All four read ok, with no error and no warning. The one error on the way (a four-word bullet, "The lock records:") was fixed.
- **ICE shape check** on the four ICE pages: the thin mark first; Intent, Context and Expectation in order; exactly one Goal; three Limits and three Fails if on each; the fixed Read line first; the Context labels in order; a Scenario; each Done means checked by someone other than the doer. All four read ok. The capability's ICE and the check's ICE have a Never read line on a plan's evals folder. No part page has an ICE section.
- **Quotes**: 129 quotes in the Sources sections, checked word for word against their files (memory quotes against this run's short-term copies, the agreed lines against `capabilities.md`, #893 against its text as read today, and the product owner's words of 2026-11-08 against this file), and 6 quotes in the page bodies checked against the files each page cites. None missing. Two Sources lines carry no quote: the short line beside each feature, and the shelf line.
- **Scan**: no page uses the word for the old design views of a slice, mentions seeding memory, names a plan, a real person or a home-folder path.
