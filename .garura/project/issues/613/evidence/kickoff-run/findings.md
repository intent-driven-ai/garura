# #613 item 8 — Kickoff on a real prototype: findings (as they come)

Test project `argus-shop`: Garura installed from `feature/613-the-kickoff-drive` (full scope),
pushed to the private sandbox repo `intent-driven-ai/test-sandbox` (Kapil, 2026-10-20: one
sandbox repo for all tests). Prototype: the Argus mockup, copied in as `prototype/argus.html`.
Phoenix memory on the machine at `7d4d49d`. Kickoff run headless (`claude -p "/kickoff …"`),
its plays as sub-agents (the default runner).

## Before the run

- K-0 — the install writes the absolute shared-memory path into the project's committed
  `.garura/install-manifest.json` (`"memory": "/…/argus-shared-memory"`). Any project that
  commits its install record commits that path — with the default, the user's home folder. It
  reached the sandbox repo's first push; the sandbox history was rewritten and force-pushed
  clean (3 commits, minutes old). For its own issue.
- K-1 — this branch changes two Phoenix memory files (`standards/rules/drive-contract.md`,
  `standards/rules/pipeline-next.md`); Phoenix memory on the machine has the older copies until
  #613 lands, so the run reads the old drive contract and has no Next line for `kickoff`.

## Run 1 (2026-10-20) — stopped at /intent's questions, then stopped by Kapil

- K-2 — Python leaves `__pycache__/` beside the stamped scripts in the installed
  `.claude/skills/kickoff/scripts/`; it is outside the issue folder, so `commit_run_files.py`
  would call the tree unclean and halt the drive after the first play. To watch on the rerun.
- K-3 — **`/intent` read one screen of the Argus mockup.** The capture kept only the first,
  Overview screen (4.7 KB of text) of a prototype with five sections, Catch up and its cards;
  the play clicks a view only when one is named, and nothing named them. `/intent` drafted two
  business intents that were rules about agents ("agents build only from what a person
  approved") — Kapil: "completely wrong … none of it reflects what Argus does". **Fixed on this
  branch** (Kapil, "1"): C1, F1, REC1 and S1 of `/intent`'s ICE now require a prototype to be
  captured view by view; `capture_source.py` finds every view itself (two clicks deep, never an
  answer button or an outside link) and records what it found, kept and could not reach. On the
  mockup: 36 views kept (about 99 KB of text), 4 unreached with why.
- K-4 — the business intents were drawn from rules written in the page, not the person's
  purpose, and the mockup's sample shop data confused it (its Q1). Held: the rerun shows whether
  this remains once `/intent` sees every view.

## Run 2 (2026-10-20) — after the /intent fix

- Set-up: run 1's record kept beside the run (scratch); the test project reset to `main`,
  reinstalled from `d617f19a`. Stand-in for K-2: the test project's `.gitignore` gains
  `__pycache__/`, so the drive is not stopped by Python caches — K-2 still needs its own fix
  in Garura (an installed project gets no such ignore).
- Run 2 result (baseline for the journeys, Kapil "1"): 36 views kept (161 controls found, 4
  unreached — Catch up controls that timed out); $2.32; stopped at 10 questions, not answered.
  Drafted 3 business intents — "people decide what AI agents build", "agents work only from
  knowledge a person has approved", "anyone can check why an agent decided" — and 12 ICE that
  now reach every section (change overview, piece review, answering, comments, the action feed,
  the product model, limits, recorded decisions, Ask memory, memory contents, memory updates,
  decision traces). **K-4 stands:** the business intents are still rules about agents, not why
  a person uses Argus; seeing every view alone does not fix it.
- K-5 — Kapil, 2026-10-20: "if it's a prototype … it should try to run, create journey steps,
  and understand it, even deeply." Being built: `/intent` walks a prototype in journeys and
  drafts from them (C15).
- K-5 built: `/intent` C15, F15, S9, REC15 (ICE) → Step 1b "walk the prototype in journeys"
  (`business-intent-keeper` → new skill `walk-prototype`; scripts `walk_prototype.py`, one
  replayable step per call, and `check_journeys.py`, with `--draft` checking each business
  intent names its journey); the drafting skill starts a prototype's intents from the journeys,
  and a business intent is never a rule the system enforces (K-4). Kickoff asks, for a link,
  whether the walk may change data (`answers.intent.may_change_data`). 118 script tests pass;
  `lint_play`, `lint_drive` and `lint-components` pass.

## Run 3 (2026-10-20) — with journeys; cut off

- K-6 — **the drive started `/intent`'s sub-agent in the background** and ended its turn; the
  headless session stopped it 10 minutes later ("Background tasks still running 10m after the
  last turn (subagent 'Run /intent play in drive'); stopping them"). The walk had taken about 35
  steps (106 files). Fixed in the shared drive run: R5 dispatches each play's sub-agent in the
  foreground and waits. Headless runs also set `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0`.

## Run 4 (2026-10-20) — with journeys; stopped at /intent's 20 questions

Result: 37.1 min, $8.41 (Opus 5.5 $6.84, Sonnet 5.5 $1.56, the run's own `modelUsage`).
6 journeys, 107 steps; the journey check reads ok — 35 of 35 views on a journey. 6 business
intents, each from a journey: sign off a drive · understand a change before answering · intents
say what was asked · the agents' questions get answered · agent decisions still stand · recorded
decisions get answered. 10 ICE under them. 20 questions (2 general, 3 per intent), not answered.

### Effectiveness (T242)

| | Run 1 | Run 2 | Run 4 |
|---|---|---|---|
| What `/intent` saw | 1 screen | 36 views | 36 views + 6 journeys, 107 steps |
| Business intents | 2, rules about agents | 3, rules about agents | 6, what a reviewer gets |
| ICE | 12 | 12 | 10 |

- K-4 is fixed: each business intent is what a person gets, and names its journey.
- K-7 — a gap: **reading the product model as a whole** is no longer its own ICE. Run 2 had
  "Read the product, part by part" and "Guard the product-wide limits"; run 4 folds the Product
  view and the limits page into "Reading a change in full". ADR 032 names two review tools —
  intents and product — so the product reading is one of Argus's two halves.
- K-8 — every journey has the same person ("the person who reviews what a drive changed"). True
  for Argus today; a prototype with several kinds of user should show several.
- K-9 — 20 questions is a lot to put to a person at once; most are who-asks and proof per
  intent, which the prototype cannot show.

### Where the time and the money went (T243)

| Phase | Time | Who | Cost (share) |
|---|---|---|---|
| Drive set-up: pre-flight, issue, branch, questions, contract | 2 min | drive (Sonnet 5.5) | in the Sonnet $1.56 |
| Capture every view (script) | 3 min | `capture_source.py` | none |
| Walk 6 journeys, 107 steps | 25 min | `business-intent-keeper` (Opus 5.5) | about $3.9 |
| Write and check the journeys | 3 min | same agent | (in the line above) |
| Draft 6 intents and 10 ICE, check them | 7 min | `business-intent-keeper` (Opus 5.5) | about $2.9 |
| Orchestration across the run (drive, `/intent`, issue agent) | throughout | Sonnet 5.5 | about $1.6 |

(The Opus split between walk and draft is estimated from each agent's share of tokens in the
session logs; the totals are measured.)

- K-10 — the walk replays every earlier step in a fresh browser: one step takes 5.8 s with 1
  step replayed, 11.1 s with 28. About 12 of the walk's 25 minutes were browser time. One open
  browser per journey removes most of it, with no change to what is walked.
- K-11 — the walk's tokens grow with every step: the agent reads each step's full page text
  (the Argus page is several thousand words), and its context is re-read on every call — 14.4
  million cache-read tokens on Opus. Handing the agent only what changed since the last step,
  and the controls now on screen, should cut most of it.
- K-12 — models: the drive and `/intent`'s orchestration ran on Sonnet 5.5 (the headless
  session's model); only `business-intent-keeper` ran on Opus 5.5, because its file pins
  `model: opus`. The walk (look, pick the next click, write what showed) is high-volume and
  low-judgment — a fit for Sonnet 5.5 at medium effort; the draft (framing business intents) is
  where every earlier run went wrong — keep Opus 5.5 at high effort. Not yet measured: a run
  with these settings, compared with run 4 on cost, time and the intents' quality.
- K-13 — the 20 questions were shown without the draft (Q2 asked about "six goals" never shown),
  and who asks / why / proof were asked once per intent, 18 times. Kapil: "these questions, to
  me, don't make sense."
- K-14 — **the drive was a pipeline, not a drive.** It stopped at `/intent`'s first questions
  instead of going on to `/vision` and `/understand` and looping back. Kapil: ADR 029 and 035
  stand; "you are just stopping there, not leveraging the capability that the drive has between
  those three things together." A question stops the drive only when no play of it can answer.

## The fixes before run 5 (2026-10-20)

| Finding | Fix | Commit |
|---|---|---|
| K-10, K-11, K-12, K-7 | one browser per journey (28 steps: about 4 min → 23 s); each step tells only what changed; the walk on its own agent `prototype-walker` (Sonnet 5.5, medium effort), the draft on `business-intent-keeper` (Opus 5.5, high effort); every main section is some journey's goal | `89b74658` |
| K-14 | the drive loops in rounds; a play's question goes to the drive (`open-<play>.json`); `round_state.py` decides done / again / ask; Kickoff C4, C5, F5, S3, D7 | `3a31667d` |
| K-13, K-14 | `/intent` inside a drive hands its questions to the drive and fills them next round; memory first, research as a memory update; who asks from the journeys' roles; questions asked once, after the draft, in the prototype giver's words (C16) | `4a75304f` |

## Run 5 (2026-10-20) — the loop; stopped by Kapil after round 2

- The loop worked. Round 1: `/intent` saved 6 intents and handed 7 questions to the drive (no
  stop); `/vision` seeded the `collaboration` domain (1 question); `/understand` detailed 12
  capabilities (74 questions). `round-1.json` read `again`. Round 2: `/intent` filled gaps from
  the model ("model answered area and context questions"), then `/vision` and `/understand` ran
  again. The walk took 5 minutes (run 4: 21), 7 journeys, 87 steps, a journey of its own for the
  product model (K-7 fixed).
- K-15 — **82 questions left after round 2** — mostly a few knowledge gaps asked again for each
  of 12 capabilities: who may approve and how they are known; speed targets; rules that apply to
  the review record (SOC 2, GDPR); two people in one review; undoing a finished review. Kapil:
  asking 80 questions is not realistic — the drive must build the missing memory, and that needs
  its own tool: **a memory builder, part of Argus**. Also: "are they not getting answered from
  the prototype? I think it should" — an audit of every question against the prototype is
  running. Kapil stopped run 5 ("there is no point running that").
- Audit of the 82 questions against the prototype (`question-audit.md`, a quote and line for
  each): **14 answered, 25 partly answered, 5 real gaps in the prototype, 38 no screen could
  ever show** (business proof, speed targets, compliance, where it sits in the knowledge base).
- K-16 — **`/vision` and `/understand` never read the prototype**: they work from the model
  only, so 39 questions the prototype answers fully or partly were left open.
- K-17 — **the same question is asked many times**: the business proof 15 times (each of six
  intents, once per play), speed targets 11 times, who may answer 8 times, compliance 5 times.
- K-18 — the drive's questions can be wrong about the prototype: one claims it "does not show" a
  removed piece that it does show (Saved cards); a domain rule the drive wrote contradicts the
  prototype (answers on the ADRs and Agent decisions tabs act at once, with no Finish).
- For Kapil's prototype (not Garura): 5 screen states it should show (a second person opening
  the same review; editing or deleting a comment; an answer that did not reach Garura; the full
  event trail; a failed second check), and one contradiction — a decision with no source is
  labelled "not allowed" yet still offers "Looks right".
- K-0 and K-2 fixed in the install: the record writes a home path as `~/…` (uninstall expands
  it); an installed project's `.claude/skills/.gitignore` (and `.agents/skills/`) and
  `.garura/.gitignore` ignore Python caches.
- Kapil, 2026-10-20: "fix the drive or intent first, and then merge … Don't do it on the test
  run. The test run is giving you where drive and intent are broken." The memory builder was
  built in Garura, not tried on run 5's record; the next run is after the merge.

## #689 runs (2026-10-21) — after ADR 043 and the rebuild eval

Each run was in a fresh local copy of `argus-shop` with no remote: the prototype, its write-up
and Garura installed from the #689 branch. Plays ran on their own models (Opus 5.5 where none
is set). The rebuild eval ran on Sonnet 5.5 at high effort. Nothing was pushed.

- Rebuild of the `/understand` output (6 intents, 1 domain, 10 capabilities, 36
  functionalities): 107 things a person can do or see on the prototype; 99 came back, 7 in
  part, 1 missing. Kept 95.8%, drift 4.2%; the brief describes 97.2% of the prototype; 5 misses
  are the drive's, 0 the builder's. Cost $3.92.
- Kickoff run 1 (88 min active, $73.41): 10 intents, 2 domains (ALM and collaboration), 8
  capabilities, 31 functionalities, 0 gaps; stopped at its brief. K-19 — `collaboration` is the
  field of one feature many products share, and it held none of the prototype's main sections;
  Memory and Agent decisions were folded into ALM. Kapil: "stop and fix vision".
- The fix (`d4541fa8`): every main section of the screens sits in a domain whose research
  covers that kind of work (`areas` in the seed manifest, checked by
  `grounding_check.py --journeys`); a domain that holds no main section is not written. On run
  1's manifest the check fails all 6 sections and both domains.
- Kickoff run 2 (67 min, $64.41: Opus $62.09, Sonnet $2.30, Haiku $0.02): 6 intents, 3
  domains (Application Lifecycle Management for Intents, Product and ADRs; Knowledge Management
  for Memory; AI Observability for Agent decisions), 10 capabilities, 32 functionalities, 0
  gaps, every section mapped with a quote and its source; 3 rounds, then the brief (5 gaps, 1
  settled point, 4 knowledge pages, 1 prototype note). Kapil accepted the run as it stands and
  waived its rebuild eval (2026-10-21: "skip the eval. i accept this run").
- K-20 — Kapil had named the second field Agentic Engineering; the drive found Knowledge
  Management and AI Observability instead. Not taught to the plays (no product answers in
  skills).
- K-21 — `find-model-gaps` reported no gaps while links went one way only (parent to child
  without child to parent); the drive sent it back and round 2 fixed them. The gap script does
  not count one-way links. For its own issue.
- K-22 — the brief writer wrote the round-3 brief by hand instead of through its skill; the
  brief check still passed. For its own issue.
