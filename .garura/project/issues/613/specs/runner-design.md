# #613 — the Kickoff runner: design note (item 3)

What the drive is as a component and how it runs end to end. It rests on ADR 029 (drives),
ADR 031 (business intent and ICE), ADR 034 (a play answers from memory inside a drive),
ADR 035–039 (memory; the issue ID governs), the drive contract
(`standards/rules/drive-contract.md`) and the #662 run, which already ran the three plays under
one drive contract. Three points need Kapil's decision; they are marked **Decide**.

## 1. What Kickoff is

- **A play of the drive kind**, `core/components/plays/kickoff/`, with an ICE source
  (`reference/ice.md`) written from #613's acceptance criteria and compiled by `/play-creator`
  like every play (CLAUDE.md). The compiler learns the drive kind in item 5: a drive's steps run
  other plays in a fixed order and carry no rules of their own (ADR 029 §2).
- **Pipeline position: both.** Kickoff opens the change (`start-change`: one issue, one branch)
  and lands it (the end sequence). The plays inside open nothing (drive contract, step 3).
- **Its one rule is to run its plays**: `/intent` → `/vision` → `/understand` (once, for every
  capability `/vision` seeded). Every other rule lives in the plays.

## 2. Where its run lives — the issue ID governs

Everything the drive and its plays write goes under the drive's issue (ADR 039;
`drive-contract.md`):

| What | Where |
|------|-------|
| The drive's own run: the contract, its run record, the checker's verdict | `{stm_base}<issue>/context/kickoff/<run-ts>/` |
| Each play's working folder, answers and markers | `{stm_base}<issue>/context/<play>/…`, `{stm_base}<issue>/status/` |
| Each play's review record for the drive's end | `{stm_base}<issue>/review/drive/` |
| Memory updates and decision traces | `{stm_base}<issue>/review/memory-updates/`, `context/citations.jsonl` (the memory tool) |
| Evidence | `{stm_base}<issue>/evidence/kickoff/` and each play's `evidence/<play>/` |
| The gate history | `{stm_base}<issue>/review/gate-evals.jsonl` |

After each play, the drive commits the issue's run files on its branch (the #662 run found the
plays leave them uncommitted inside a drive — finding V-4). The plays commit their own model
change, as today.

## 3. How it runs, step by step

1. **Pre-flight** — a working prototype is given and it runs (a folder that starts, or a link
   that answers); else halt (ADR 029 §6).
2. **Open the change** — `start-change` (one issue, one branch).
3. **Questions first** (ADR 029 §2, ADR 034) — the drive asks what it can before any play runs:
   the prototype, the product's name, and the facts a person must give (for example who asks
   for it). The answers go to the issue's short-term memory and into the drive contract's
   `answers`. Each play's agents then look in memory first (through the tool); a question no tier
   and no answer covers stops the drive and comes to the person, as a memory update a person
   approves (drive contract, step 5). In the #662 run this happened three times: `/intent`'s
   "who asks" and "proof", and `/vision`'s missing knowledge (`mu-20261020-001`).
4. **Write the drive contract** — one file for all three plays (`drive_run_id`, `drive`,
   `branch`, `issue`, `review_dir`, per-play `inputs` and `answers`).
5. **Run the plays** — each with `--contract`, in order; after each, check its own done check
   (its stop condition) and commit the issue's run files. A play that misses its done check
   halts the drive.
6. **The checker** (ADR 029 §2) — a different model, sub-agent or coding agent, picked by the
   config, checks the result against Kickoff's done means: intents proposed with their sources,
   a domain with its capabilities, every capability detailed, `citations --check` clean, no
   answer from the model alone. It writes pass or reject, with reasons, to
   `context/kickoff/<run-ts>/check.yaml`. A reject halts the drive.
7. **Evidence** — the shared close (`_shared/play-close.md`), with the drive's own record.
8. **End** — see **Decide (b)**.

## 4. The checker, by config

```yaml
drives:
  kickoff:
    checker:
      kind: subagent        # subagent | model | coding-agent
      model: <a different model from the session's>
```

Default: a fresh sub-agent on a different model, handed only the drive's outputs (the model
diff, the plays' review records, the trace check), never the drive's reasoning — the same
isolation the grounding judge has. **Decide (c).**

## 5. Decisions for Kapil

**(a) How the drive runs its three plays.**
1. Each play in its own fresh Claude Code session, started by a bundled script (`claude -p` in
   the project, as the #662 run did), so it loads the project's own installed plays and agents
   and starts with a clean context; the drive's session stays small and relays questions to the
   person. The config names the command (Codex: `codex exec`).
2. All three as sub-plays inside the drive's one session.
Recommend 1: the #662 run proved it, and three heavy plays in one session fill its context
(the run cost about $20 across the three).

**(b) How the drive ends, before the review tool exists (#641–#650).**
1. It opens the pull request and stops. The person reads the plays' review records, confirms or
   drops each proposed intent by typing (recorded like `/intent`'s own confirmation), and then
   the review and the merge run, the merge waiting for the person's approve.
2. It runs the whole end sequence, and the person confirms the intents at the pinned merge gate.
Recommend 1: confirming intents is the person's decision (ADR 031 §5); keeping it a separate
step before the merge makes it clear, and the review tool replaces that step later.

**(c) The checker's default.**
1. A sub-agent on a different model (for example Sonnet when the session runs Opus).
2. A different coding agent (Codex).
Recommend 1: it works with what every Garura install has; the config can name Codex.

## 6. What this leaves to later items

- Item 4: the plays' remaining stops (the close not asking `template-manager`, I-2; the run
  files left uncommitted, V-4 — the drive commits them, step 5).
- Item 5: the compiler's drive kind. Item 6: the checker. Item 7: Kickoff itself. Item 8: a run
  on a real prototype Kapil picks, and the three halts.
- Not in #613: the person's plan and issues (ADR 029 §6, waiting on Kapil); the review as the
  drive's last step (#650).
