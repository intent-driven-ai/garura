# ADR 066 — Names Say Who Does the Work: Five Roles Own the Verbs, Loops Are Named loop-<from>-<to>, and a Name May Start With a Tool's Command

**Status:** Accepted
**Date:** 2026-11-03
**Level:** framework
**Decided by:** Kapil Viren Ahuja
**Decided in:** #1021, with the five roles recorded in #1015
**Supersedes:** ADR 046 (in part — §1, the list of short words, which gains `env`, `perf` and `uat`; §2, the words "or starts with" and the verbs it moved because of them; §3, loops named `complete-<phase>`; §4, in whole, with what ADR 048 and ADR 059 changed in it) · ADR 045 (in part — §3, the five final names and the Learn loop's list of plays; §4, the name "Discovery loop"; §2's examples "the Discovery loop" and "the Ship loop") · ADR 028 (in part — "The agentic lifecycle is five loops" and "Later"; §2 item 3, where marketing leaves the design areas; §4, that the change chain is a loop)
**Amends:** ADR 029 — Context, the six phases: the second is Spec, not Intent · ADR 038 — §3, "A new play, `initialize`": it is an engine thing, not a play, and its job stands · ADR 053 — §4, "The seven design lens plays ... are not dropped": two are
**Affects:** the naming rules — `core/components/memory/standards/rules/naming.md`, `naming.yaml`, `rename-map.yaml`, `core/tools/lint-components/lib/rules/naming.js` and `test/naming.test.js`, `core/tools/naming/` · the words — `docs/standards/harness-standard.md`, `CLAUDE.md`, `core/components/memory/standards/rules/pipeline-next.md`, `docs/components/loops.md`, `core/grounding/glossary.md`, `core/config.yaml`, `core/components/plays/install-garura/SKILL.md`, `core/tools/memory/GUIDE.md`, the ontology's wording, and Phoenix memory's copies of `naming.md` and `naming.yaml` · later, every play and loop the list names, under `core/components/plays/` and `core/components/loops/`
**ICE impact:** None now: nothing is renamed, and no play's goal, limit or check changes. When the parts are renamed, each ICE that names one changes in wording only, through /edit-play or /edit-loop, and its fingerprint is stamped again. The ICE of the two dropped design plays goes when they are deleted, and /build-epic and /learn-outcomes stop reading the `realized` stamp when those plays are rebuilt. `initialize` has no ICE yet. The ontology (read at version 15) and the ICE kind do not change.
**Business intent check:** none — a framework naming decision; no person's business intent changes, and the Business Intent kind does not change
**Related:** ADR 004, ADR 031, ADR 048, ADR 049, ADR 052, ADR 059, ADR 065, #608, #609, #610, #611, #1015, #1021

## Context

This record is only about how this project is built.

Verbs today do not say who acts. `author` starts 21 live skills, and `shape` starts ten plays that shape a slice, make a plan, write an eval or write a design lens. The product owner wants the verbs right before more of the product model is written.

Nothing is renamed by this decision; the plays are renamed later. The full list of names, old and new, is `.garura/project/issues/1021/context/names.md`.

## For the Person Who Accepts This

### The list names plays and loops, but no skill and no agent, and the verb `remove` is still unrecorded

- **What and where:** The skill verbs and agent endings in `core/components/memory/standards/rules/naming.yaml` (lines 32 to 59), and ADR 046 §5. The 75 skills under `core/components/skills/`.
- **What is wrong, or worth knowing:** The brief says the fixed verb lists are replaced, and gives `author`, on 21 live skills, as its example. But `names.md` names no skill and no agent, and #1015 asks that every verb, skill verbs included, gets a role. Separately, `remove` is in the source `naming.yaml` (line 56), but not in ADR 046 §5 and not in Phoenix memory's `naming.yaml`. ADR 065 left it because the verbs change next.
- **Why it matters:** If the skill list goes too, 72 of the 75 skill names fail the naming check, with no new names to move to (`commit-files` and `merge-pr` keep a verb that stays, and `platform-adapter` is the named exception). If it stays, `author` stays too, which is the brief's own example of the problem. Meanwhile `remove-model-part` and `remove-plan` fail the check in any project that reads Phoenix memory's copy.
- **What this decision does:** Only the play and loop lists change. ADR 046 §5 stands, and `remove` is not recorded.
- **What you decide:** Decided: skills and agents keep their verbs for now, and get their own list in a later decision. `remove` stays undecided, in that later decision.

### The list drops two design plays, and the brief gave no reason

- **What and where:** `/shape-marketing-lens` and `/shape-measure-lens`, with their skills `author-marketing-lens` and `author-measure-lens`, under `core/components/`. `names.md` line 10.
- **What is wrong, or worth knowing:** The brief's six parts do not mention the drop. ADR 053 §4 says the seven lens plays are not dropped and are rebuilt when their stage comes, and ADR 028 §2 lists marketing as a design area. Both plays are stale today, so no install lays them. `/shape-marketing-lens` is the only play that covers how a slice is found (SEO, AEO, GEO) and its reach signals. `/shape-measure-lens` is the only play that sets a slice to `realized`, and the stale /build-epic still refuses a slice without it (`scripts/check_ready_epic.py`, lines 187 to 190).
- **Why it matters:** This repo records a dropped play in an ADR with its reason (`CLAUDE.md`, ADR 051). Whoever rebuilds /build-epic and /learn-outcomes needs to know the stamp is gone.
- **What this decision does:** It records the drop with its reason, and changes ADR 053 §4 and ADR 028 §2. Nothing is deleted by this decision.
- **What you decide:** Decided: they go. In the product owner's words: "They didn't have good reasons to exist. They'll be added if needed, and for now they go."

### The Alignment loop connects no two phases, so the new pattern cannot name it

- **What and where:** ADR 031 ("Drift is found and fixed by an Alignment drive"), ADR 049 line 91, ADR 052 lines 63 and 97, and six lines of the ontology (25, 144, 510, 522, 524, 735). ADR 045 §3 gave `/drift` to the Learn loop.
- **What is wrong, or worth knowing:** These records send drift, such as a story out of date with its ICE, or two ICE for one part, to an Alignment loop. It is not built. `names.md` lists six loops, one per transition, and neither it nor `/drift` appears there. Under `loop-<from>-<to>` it has no from and no to.
- **Why it matters:** Until it is named, these records point at a loop with no name and no approval, and no loop fixes drift.
- **What this decision does:** It names the six loops and leaves those records as they are.
- **What you decide:** Decided: the Alignment loop is unapproved and unnamed. The product owner names it later. It does not move into `/loop-run-product`, and the older ADRs that mention it stay as they are.

### The loop names call the second phase Spec, and no record said the phase was renamed

- **What and where:** `/loop-product-spec` and `/loop-spec-design` (`names.md` line 23); the open point "Phase name" in #1015; the phase table in `core/components/memory/standards/rules/naming.md` (lines 39 to 46); ADR 029's six phases; `docs/philosophy/intent.md` lines 12 and 49.
- **What is wrong, or worth knowing:** The loop names and the model's new pages say Spec, but the rule files and ADR 029 still say Intent, and #1015 left the question open. `docs/philosophy/intent.md` says an intent sits "at a level above any specification", and that in intent-driven work "the spec is an intermediate the system generates from intent and memory". `/loop-product-spec` is the loop whose output is intents.
- **Why it matters:** The harness standard is written for other teams to take. They would read a loop named for specs next to a page saying an intent is not a spec.
- **What this decision does:** It names the second phase Spec (Decision §8). The rule files' wording changes with the renames, ADR 029 gains a forward pointer, and the page stays as it is.
- **What you decide:** Decided: Spec, not Intent. `docs/philosophy/intent.md` stays: an intent sits above a specification, and a person's intent becomes a spec.

## Decision

### 1. Five roles own the verbs

The roles are specifier, designer, builder, validator and orchestrator. A verb belongs to one role, and a role can have several verbs. The verb says who does the work.

| Role | Verbs |
|------|-------|
| Specifier | `specify`, `learn` |
| Designer | `design` |
| Builder | `build`, `fix`, `refactor` |
| Validator | `validate` |
| Orchestrator | `shape`, `reshape`, `view`, `list` (`view` means one, `list` means more than one) |

### 2. These replace the fixed verb lists for plays

Each role's verbs replace the lifecycle, change, plan and harness verb lists, as `names.md` shows. `release` has no role yet: the name for `/release-increment` is still open, and `/release-slice` is the proposal.

### 3. Loops are their own category

A loop has no role. There is one for each transition between the phases, named `loop-<from>-<to>`: `/loop-product-spec`, `/loop-spec-design`, `/loop-design-code`, `/loop-code-validation`, `/loop-validation-run` and `/loop-run-product`. There is no Ship loop. The plain names Discovery, Slice, Execute, Ship and Learn go: a loop's full name is its command. Only a loop's name starts with `loop`.

The Alignment loop is unapproved and unnamed: the product owner names it later, it does not move into `/loop-run-product`, and the older ADRs that mention it stay as they are.

### 4. The work plays have no role

`/start-work`, `/commit-work`, `/review-work` and `/merge-work` open, commit, review and merge work. They are not tied to a role, because anyone can run them. Their final place is still open.

### 5. Some things have no role, and some are not plays

`/install-garura` and `/uninstall-garura` are product plays with no role. Locking a design is a governance check. Initialize, seeding memory and upgrade are engine things, not plays.

### 6. A name may start with a tool's command

A name may not be exactly a tool's built-in command, but it may start with one. `env`, `perf` and `uat` join the allowed short words.

### 7. Two design plays are dropped

`/shape-marketing-lens` and `/shape-measure-lens` get no new name, and they go. In the product owner's words: "They didn't have good reasons to exist. They'll be added if needed, and for now they go." Nothing is deleted by this decision.

### 8. The second phase is Spec

The second of the six phases is called Spec, not Intent. `docs/philosophy/intent.md` stays as it is.

### What this changes in older ADRs

- **ADR 046** — §2's "or starts with" and the verbs it moved go, and the rule that no name is a built-in stands. §3's idea stands with a new word: one word marks a loop. §4 goes in whole, with its rule that an object is a product-model word, because `work`, `env` and `surface` are not. §1 gains three short words, and its other rules stand. §5 and §6 stand: skills and agents keep their verbs for now.
- **ADR 045** — §3's five names and §4's name go. §1, §5 and §2's rule stand: a loop is always named in full, and no command is called just `/loop`.
- **ADR 028** — "five loops", "Later" and §4 as a loop go, and the change chain stays as commands. What §1, §2, §3 and §5 say each stage does stands, except that marketing leaves §2's design areas.
- **ADR 029** — the second of the six phases in its Context is Spec, not Intent. How a loop runs, the loop owning its change and plays standing on their own all stand, and "Each drive solves one transition" agrees with this decision. Its "five transitions" is background; the rule files already list run to product as the sixth.
- **ADR 038** — §3's "A new play": `initialize` is an engine thing. Its job stands.
- **ADR 053** — §4: five lens plays stay as it says, and two are dropped.

### What this does not change

- **ADR 049** — the three plays, their order and where evals live all stand. It holds no verb rule.
- **ADR 065** — none of its four rules changes. It left `remove` undecided, so it needs no pointer; the later decision on skills and agents settles it.
- **ADR 004** — agents stay `<domain>-<role>`.
- **ADR 048 and ADR 059** — their changes to ADR 046 §4 end with §4. Their own decisions stand.
- **ADR 031, ADR 049 and ADR 052** — they mention the Alignment loop, which is unapproved and unnamed, so they stay as they are.
- **ADR 006 and ADR 018** are already superseded. ADR 017, 021, 022, 023, 024, 025, 026, 035, 037, 039, 040, 041, 042, 043, 044, 051, 054, 055, 060 and 061 were searched, and they share only a path, a play name or a word with this decision.

## Consequences

### Positive

- A play's name says who does the work and what it does.
- There is one loop to remember for each transition.
- A designer can use `design-`, and no agreed name is exactly a built-in command.

### Negative / Risks

- Every command people type changes again, twelve days after ADR 046 changed them, and a project's learned gate policies, kept by play name, start again.
- `/design` and `/design-slice` now sit side by side in the command list, and a tool can add a name like `design-surface` at any time. It already has `design-login` and `design-sync`. ADR 046 banned the prefix to avoid this clash.
- Until the rename lands, the naming files and the linter keep today's rules, so they disagree with this record. They cannot change first, because the plays still under old verbs, such as `/discover-intent` and `/record-decision`, and the one loop would then fail the check.
- `/review-work` raises a change for review and `/validate-work` judges it, so the first can be read the wrong way. `fix` now covers both fixing a defect and changing a play's goal, so its one meaning gets wider.
- `release` has no role until `/release-increment` is named, and the work plays have no final place yet.
- Skills keep their old verbs until their own list is decided, so `author` still does not say who acts. `remove` stays unrecorded, so `remove-model-part` and `remove-plan` still fail the check in a project that reads Phoenix memory's copy.
- No play covers how a slice is found, or sets the `realized` stamp, unless one is added if needed. The stale /build-epic still asks for that stamp until it is rebuilt.
- The older records still send drift to an Alignment loop with no name and no approval, until the product owner names it.

## Alternatives Considered

- **Only five verbs, one per role, for everything** — it reads badly for the orchestrator, whose work is several kinds of thing, and names like `/orchestrate-start` do not say what they do. A builder also builds, fixes and refactors.
- **Keep today's verbs and only list them by role** — names still would not tell who does the work.
- **Move opening, committing, reviewing and merging into shared steps inside build plays** — anyone can run them, so they are not a builder's, and it would mean a large rebuild.
- **Keep loops named for what they do, like Discovery and Execute** — the product owner wants one thing to remember for each transition.
- **Keep the ban on starting a name with a built-in command** — it blocks `design-`, which the product owner wants a designer to use.

## Work This Creates

- After acceptance, the forward pointers on ADR 028, ADR 029, ADR 038, ADR 045, ADR 046 and ADR 053.
- The rename, as one change: the naming files, the linter and its tests, the rename map, the harness standard, `CLAUDE.md`, the other pages under Affects, each play's ICE wording, and then Phoenix memory's copies. The rule files' phase wording moves from Intent to Spec in it. ADR 029's wording changes only through its forward pointer, because an accepted ADR is never edited.
- A later decision gives skills and agents their own list, and settles the verb `remove`.
- Delete the two dropped design plays and their skills, and take the `realized` check out of /build-epic and /learn-outcomes when they are rebuilt.
- The product owner names the Alignment loop, which stays unapproved until then.
- #608, #609, #610 and #611, the open loop-recipe issues, are rewritten under the new loops. #610 decides a Ship loop that no longer exists.
- Settle the name for `/release-increment` and the work plays' final place.

## References

- `.garura/project/issues/1021/context/names.md`
- `.garura/project/issues/_adr/20261102-220451/brief.md`
- #1015 — the five roles and their open points
- ADR 028, ADR 029, ADR 038, ADR 045, ADR 046, ADR 053
